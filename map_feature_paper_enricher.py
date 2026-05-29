#!/usr/bin/env python3
"""
Map Feature Paper Enricher
Background process that searches OpenAlex for scientific papers related to
all map features (ore deposits, stratigraphy, paleontology, mining, exploration licenses)
and stores references in the scientific papers database.

Reuses: fetch_scientific_papers.openalex_search(), parse_openalex_work()
        scientific_papers_database.insert_paper(), get_connection()
"""

import os
import re
import json
import time
import logging
import threading
from datetime import datetime
from typing import Dict, List, Optional

import scientific_papers_database as db
from fetch_scientific_papers import openalex_search, parse_openalex_work
from runtime_lock_utils import load_json_file, write_json_file

logger = logging.getLogger(__name__)

# Paths
STATE_PATH = 'data/map_feature_papers_fetch_state.json'
ORE_DEPOSITS_PATH = 'data/ore_deposits.json'
STRATIGRAPHY_PATH = 'data/stratigraphy_localities.json'
PALEO_PATH = 'data/paleo_localities.json'
MINING_PATH = 'data/mining_operations_serbia.json'
LICENSES_PATH = 'data/exploration_licenses_serbia.json'

MAX_RESULTS_PER_QUERY = 15
REQUEST_DELAY = 0.25

# Thread control
_enrichment_lock = threading.Lock()
_enrichment_running = False
_enrichment_status = {
    'running': False,
    'started_at': None,
    'current_feature_type': None,
    'current_feature_name': None,
    'completed_features': 0,
    'total_features': 0,
    'papers_found': 0,
    'links_created': 0,
    'queries_made': 0,
    'errors': 0,
    'finished_at': None,
}

# Commodity symbol -> full English name
COMMODITY_NAMES = {
    'Cu': 'copper', 'Au': 'gold', 'Ag': 'silver', 'Pb': 'lead', 'Zn': 'zinc',
    'PbZn': 'lead zinc', 'Sb': 'antimony', 'Bi': 'bismuth', 'Fe': 'iron',
    'Mn': 'manganese', 'Cr': 'chromium', 'Ni': 'nickel', 'Co': 'cobalt',
    'Mo': 'molybdenum', 'W': 'tungsten', 'Sn': 'tin', 'Li': 'lithium',
    'B': 'boron', 'Ba': 'barite', 'Mg': 'magnesite', 'As': 'arsenic',
    'Hg': 'mercury', 'U': 'uranium', 'Coal': 'coal',
}


# ---------------------------------------------------------------------------
# Database: paper_feature_links table
# ---------------------------------------------------------------------------

def init_feature_links_table():
    """Create the paper_feature_links table if it doesn't exist."""
    conn = db.get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS paper_feature_links (
                id BIGSERIAL PRIMARY KEY,
                paper_id BIGINT NOT NULL REFERENCES scientific_papers(id) ON DELETE CASCADE,
                feature_type TEXT NOT NULL,
                feature_name TEXT NOT NULL,
                feature_id TEXT,
                link_type TEXT DEFAULT 'search',
                relevance_rank INTEGER DEFAULT 0,
                search_query TEXT,
                UNIQUE(paper_id, feature_type, feature_name)
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_fl_paper ON paper_feature_links(paper_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_fl_type_name ON paper_feature_links(feature_type, feature_name)")
        conn.commit()
    finally:
        conn.close()


def link_paper_to_feature(paper_id: int, feature_type: str, feature_name: str,
                          feature_id: str = None, link_type: str = 'search',
                          relevance_rank: int = 0, search_query: str = None):
    """Link a paper to a map feature."""
    conn = db.get_connection()
    try:
        row = conn.execute("""
            INSERT INTO paper_feature_links
                (paper_id, feature_type, feature_name, feature_id, link_type, relevance_rank, search_query)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (paper_id, feature_type, feature_name) DO NOTHING
            RETURNING id
        """, (paper_id, feature_type, feature_name, feature_id, link_type, relevance_rank, search_query)).fetchone()
        conn.commit()
        return row is not None
    except Exception as e:
        logger.error(f"Error linking paper {paper_id} to feature {feature_type}/{feature_name}: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Latin name extraction (Python port of JS extractLatinNames)
# ---------------------------------------------------------------------------

_LATIN_RE = re.compile(r'([A-Z][a-z]{2,})(?:\s+(?:cf\.|aff\.)?\s*([a-z]{2,}))?')

def extract_latin_names(text: str) -> List[str]:
    """Extract Latin binomial names from a text that may contain Cyrillic."""
    if not text:
        return []
    names = []
    for m in _LATIN_RE.finditer(text):
        word = m.group(1)
        # Skip if not pure ASCII (catches Cyrillic)
        if not word.isascii():
            continue
        full = m.group(0).strip()
        if len(full) > 3:
            names.append(full)
    # Deduplicate preserving order
    seen = set()
    result = []
    for n in names:
        if n not in seen:
            seen.add(n)
            result.append(n)
    return result


# ---------------------------------------------------------------------------
# Smart query generators per feature type
# ---------------------------------------------------------------------------

def _queries_for_ore(feature: dict) -> List[dict]:
    """Generate search queries for an ore deposit."""
    queries = []
    name = feature.get('name', '')
    commodities = feature.get('commodities', [])
    deposit_type = feature.get('deposit_type', '')

    mineral_names = []
    for c in commodities:
        sym = c.get('symbol', '') if isinstance(c, dict) else str(c)
        full = COMMODITY_NAMES.get(sym, sym)
        if full:
            mineral_names.append(full)

    # Primary: mineral names + deposit name + Serbia
    parts = mineral_names[:3] + ([f'"{name}"'] if name else []) + ['Serbia ore deposit']
    if deposit_type:
        parts.insert(-1, deposit_type.split(':')[0].strip())
    queries.append({'query': ' '.join(parts)[:220], 'max_results': MAX_RESULTS_PER_QUERY})

    # Broad: district + commodity
    district = feature.get('district', '')
    if district and name:
        queries.append({
            'query': f'{" ".join(mineral_names[:2])} "{district}" Serbia geology',
            'max_results': 10,
        })

    return queries


def _queries_for_stratigraphy(feature: dict) -> List[dict]:
    """Generate search queries for a stratigraphy locality."""
    queries = []
    name = feature.get('name', '')
    period_en = feature.get('period_en', '')
    finds = feature.get('finds', '')

    latin = extract_latin_names(finds)

    if latin:
        # Primary: first 2 Latin names + locality
        quoted = ' '.join(f'"{n}"' for n in latin[:2])
        q = f'{quoted} "{name}" Serbia' if name else f'{quoted} Serbia stratigraphy'
        queries.append({'query': q[:220], 'max_results': MAX_RESULTS_PER_QUERY})
        # Per-taxon
        for taxon in latin[:4]:
            queries.append({
                'query': f'"{taxon}" Serbia {period_en}'.strip()[:220],
                'max_results': 10,
            })
    else:
        # Fallback: period + locality
        parts = []
        if period_en:
            parts.append(period_en)
        if name:
            parts.append(f'"{name}"')
        parts.append('stratigraphy Serbia')
        queries.append({'query': ' '.join(parts)[:220], 'max_results': MAX_RESULTS_PER_QUERY})

    return queries


def _queries_for_paleontology(feature: dict) -> List[dict]:
    """Generate search queries for a paleontology locality."""
    queries = []
    name = feature.get('name', '')
    period_en = feature.get('period_en', '')
    era_en = feature.get('era_en', '')
    finds = feature.get('finds', '')

    latin = extract_latin_names(finds)

    if latin:
        quoted = ' '.join(f'"{n}"' for n in latin[:2])
        q = f'{quoted} Serbia {period_en}'.strip() if period_en else f'{quoted} Serbia paleontology'
        queries.append({'query': q[:220], 'max_results': MAX_RESULTS_PER_QUERY})
        for taxon in latin[:4]:
            queries.append({
                'query': f'"{taxon}" Serbia {period_en}'.strip()[:220],
                'max_results': 10,
            })
    else:
        parts = []
        if period_en:
            parts.append(period_en)
        if era_en:
            parts.append(era_en)
        if name:
            parts.append(f'"{name}"')
        parts.append('paleontology Serbia')
        queries.append({'query': ' '.join(parts)[:220], 'max_results': MAX_RESULTS_PER_QUERY})

    return queries


def _queries_for_mining(feature: dict) -> List[dict]:
    """Generate search queries for a mining operation."""
    queries = []
    name = feature.get('name_en') or feature.get('name', '')
    commodity = feature.get('commodity', '')
    municipality = feature.get('municipality', '')

    comm_names = []
    for s in commodity.split(','):
        s = s.strip()
        full = COMMODITY_NAMES.get(s, s)
        if full:
            comm_names.append(full)

    parts = comm_names[:2]
    if name:
        parts.append(f'"{name}"')
    if municipality:
        parts.append(municipality)
    parts.append('mine Serbia')
    queries.append({'query': ' '.join(parts)[:220], 'max_results': MAX_RESULTS_PER_QUERY})

    # Broad: company + mining Serbia
    company = feature.get('company', '')
    if company and name:
        queries.append({
            'query': f'{" ".join(comm_names[:2])} mining "{name}" Serbia',
            'max_results': 10,
        })

    return queries


def _queries_for_license(feature: dict) -> List[dict]:
    """Generate search queries for an exploration license."""
    queries = []
    area_name = feature.get('license_area_name', '')
    minerals = feature.get('minerals', [])
    deposits = feature.get('key_deposits', [])
    municipality = feature.get('municipality', '')

    mineral_names = []
    for m in minerals:
        if isinstance(m, dict):
            mineral_names.append(m.get('name', '').lower())
        else:
            full = COMMODITY_NAMES.get(str(m), str(m))
            mineral_names.append(full)

    parts = mineral_names[:2]
    if deposits:
        parts.append(f'"{deposits[0]}"')
    elif area_name:
        parts.append(f'"{area_name}"')
    parts.append('Serbia exploration')
    queries.append({'query': ' '.join(parts)[:220], 'max_results': MAX_RESULTS_PER_QUERY})

    # Broad: area name + municipality
    if area_name and municipality:
        queries.append({
            'query': f'{" ".join(mineral_names[:2])} "{area_name}" {municipality} Serbia geology',
            'max_results': 10,
        })

    return queries


# ---------------------------------------------------------------------------
# Load all features from JSON data files
# ---------------------------------------------------------------------------

def _load_json(path: str) -> list:
    """Load a JSON file, returning empty list on error."""
    if not os.path.exists(path):
        logger.warning(f"Data file not found: {path}")
        return []
    try:
        return load_json_file(path, default=[])
    except Exception as e:
        logger.error(f"Error loading {path}: {e}")
        return []


def load_all_features() -> List[dict]:
    """Load all map features across all layer types. Returns list of (type, name, id, feature, queries)."""
    features = []

    # Ore deposits
    ores = _load_json(ORE_DEPOSITS_PATH)
    for item in ores:
        name = item.get('name', '')
        if not name:
            continue
        features.append({
            'type': 'ore',
            'name': name,
            'id': item.get('identifier', ''),
            'queries': _queries_for_ore(item),
        })

    # Stratigraphy
    strat = _load_json(STRATIGRAPHY_PATH)
    for item in strat:
        name = item.get('name', '')
        if not name:
            continue
        features.append({
            'type': 'stratigraphy',
            'name': name,
            'id': '',
            'queries': _queries_for_stratigraphy(item),
        })

    # Paleontology
    paleo = _load_json(PALEO_PATH)
    for item in paleo:
        name = item.get('name', '')
        if not name:
            continue
        features.append({
            'type': 'paleontology',
            'name': name,
            'id': '',
            'queries': _queries_for_paleontology(item),
        })

    # Mining operations
    mining = _load_json(MINING_PATH)
    for item in mining:
        name = item.get('name_en') or item.get('name', '')
        if not name:
            continue
        features.append({
            'type': 'mining',
            'name': name,
            'id': item.get('id', ''),
            'queries': _queries_for_mining(item),
        })

    # Exploration licenses
    lic_data = _load_json(LICENSES_PATH)
    lic_list = lic_data.get('exploration_licenses', []) if isinstance(lic_data, dict) else lic_data
    for item in lic_list:
        name = item.get('license_area_name', '')
        if not name:
            continue
        features.append({
            'type': 'license',
            'name': name,
            'id': item.get('id', ''),
            'queries': _queries_for_license(item),
        })

    return features


# ---------------------------------------------------------------------------
# State management (resume support)
# ---------------------------------------------------------------------------

def _load_state() -> dict:
    if os.path.exists(STATE_PATH):
        try:
            return load_json_file(STATE_PATH, default={'completed_features': {}, 'completed_queries': {}})
        except Exception:
            pass
    return {'completed_features': {}, 'completed_queries': {}}


def _save_state(state: dict):
    write_json_file(STATE_PATH, state)


def _feature_key(ftype: str, fname: str) -> str:
    return f"{ftype}::{fname}"


# ---------------------------------------------------------------------------
# Core enrichment logic
# ---------------------------------------------------------------------------

def enrich_all_features():
    """Iterate all features, search OpenAlex, store results. Resumable."""
    global _enrichment_status

    init_feature_links_table()
    db.init_database()

    features = load_all_features()
    state = _load_state()
    completed = state.get('completed_features', {})
    completed_queries = state.get('completed_queries', {})

    _enrichment_status['total_features'] = len(features)
    _enrichment_status['completed_features'] = len(completed)

    logger.info(f"Paper enrichment: {len(features)} features total, {len(completed)} already done")

    for i, feat in enumerate(features):
        if not _enrichment_running:
            logger.info("Paper enrichment stopped by user")
            break

        fkey = _feature_key(feat['type'], feat['name'])

        if fkey in completed:
            continue

        _enrichment_status['current_feature_type'] = feat['type']
        _enrichment_status['current_feature_name'] = feat['name']

        for qinfo in feat['queries']:
            if not _enrichment_running:
                break

            query = qinfo['query']
            qkey = f"{fkey}||{query}"

            if qkey in completed_queries:
                continue

            try:
                works = openalex_search(query, qinfo.get('max_results', MAX_RESULTS_PER_QUERY))
                _enrichment_status['queries_made'] += 1

                for rank, work in enumerate(works):
                    paper_data = parse_openalex_work(work, search_query=query)
                    paper_id = db.insert_paper(paper_data)
                    if paper_id:
                        created = link_paper_to_feature(
                            paper_id, feat['type'], feat['name'],
                            feature_id=feat.get('id'),
                            relevance_rank=rank,
                            search_query=query,
                        )
                        if created:
                            _enrichment_status['links_created'] += 1
                        _enrichment_status['papers_found'] += 1

            except Exception as e:
                logger.error(f"Error searching for {feat['type']}/{feat['name']}: {e}")
                _enrichment_status['errors'] += 1

            # Track completed query
            completed_queries[qkey] = True
            state['completed_queries'] = completed_queries
            _save_state(state)

            time.sleep(REQUEST_DELAY)

        # Mark feature complete
        completed[fkey] = datetime.now().isoformat()
        state['completed_features'] = completed
        _save_state(state)

        _enrichment_status['completed_features'] = len(completed)

    _enrichment_status['finished_at'] = datetime.now().isoformat()
    logger.info(
        f"Paper enrichment finished: {_enrichment_status['papers_found']} papers, "
        f"{_enrichment_status['links_created']} links, "
        f"{_enrichment_status['queries_made']} queries"
    )


# ---------------------------------------------------------------------------
# Background thread management
# ---------------------------------------------------------------------------

def start_enrichment_background() -> bool:
    """Launch the enrichment in a background daemon thread. Returns False if already running."""
    global _enrichment_running, _enrichment_status

    if not _enrichment_lock.acquire(blocking=False):
        return False

    try:
        if _enrichment_running:
            _enrichment_lock.release()
            return False

        _enrichment_running = True
        _enrichment_status.update({
            'running': True,
            'started_at': datetime.now().isoformat(),
            'current_feature_type': None,
            'current_feature_name': None,
            'completed_features': 0,
            'total_features': 0,
            'papers_found': 0,
            'links_created': 0,
            'queries_made': 0,
            'errors': 0,
            'finished_at': None,
        })
    finally:
        _enrichment_lock.release()

    def _run():
        global _enrichment_running
        try:
            enrich_all_features()
        except Exception as e:
            logger.error(f"Paper enrichment thread crashed: {e}")
        finally:
            _enrichment_running = False
            _enrichment_status['running'] = False

    thread = threading.Thread(target=_run, daemon=True, name='paper-enricher')
    thread.start()
    logger.info("Map feature paper enrichment background thread started")
    return True


def stop_enrichment():
    """Signal the enrichment thread to stop."""
    global _enrichment_running
    _enrichment_running = False


def get_enrichment_status() -> dict:
    """Return current enrichment progress for admin UI."""
    return dict(_enrichment_status)


# ---------------------------------------------------------------------------
# API helper: paper summary for map popups
# ---------------------------------------------------------------------------

def get_feature_paper_summary(feature_type: str, feature_name: str) -> dict:
    """Return top papers with truncated abstracts for a map feature popup."""
    conn = db.get_connection()
    try:
        summary = conn.execute("""
            SELECT COUNT(*) as paper_count,
                   AVG(sp.cited_by_count) as avg_citations
            FROM scientific_papers sp
            INNER JOIN paper_feature_links pfl ON sp.id = pfl.paper_id
            WHERE pfl.feature_type = %s AND pfl.feature_name = %s
        """, (feature_type, feature_name)).fetchone()

        papers = [dict(row) for row in conn.execute("""
            SELECT sp.id, sp.title, sp.abstract, sp.cited_by_count,
                   sp.publication_year, sp.journal_name, sp.doi, sp.is_open_access
            FROM scientific_papers sp
            INNER JOIN paper_feature_links pfl ON sp.id = pfl.paper_id
            WHERE pfl.feature_type = %s AND pfl.feature_name = %s
            ORDER BY sp.cited_by_count DESC
            LIMIT 5
        """, (feature_type, feature_name)).fetchall()]

        # Truncate abstracts
        for p in papers:
            if p.get('abstract') and len(p['abstract']) > 250:
                p['abstract'] = p['abstract'][:250] + '...'

        result = dict(summary or {'paper_count': 0, 'avg_citations': None})
        result['papers'] = papers
        return result
    finally:
        conn.close()


def get_feature_paper_count(feature_type: str, feature_name: str) -> int:
    """Quick count of papers for a feature."""
    conn = db.get_connection()
    try:
        count = conn.execute("""
            SELECT COUNT(*) AS count FROM paper_feature_links
            WHERE feature_type = %s AND feature_name = %s
        """, (feature_type, feature_name)).fetchone()['count']
        return count or 0
    finally:
        conn.close()
