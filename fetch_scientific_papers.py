#!/usr/bin/env python3
"""
Fetch Scientific Papers from OpenAlex API
Links papers to geological map sheet localities (OGK) in Serbia.

Usage:
    python fetch_scientific_papers.py                  # Fetch all localities
    python fetch_scientific_papers.py --locality Bor   # Fetch single locality
    python fetch_scientific_papers.py --resume          # Resume interrupted fetch
    python fetch_scientific_papers.py --dry-run         # Preview queries only
"""

import os
import sys
import json
import time
import argparse
import logging
from datetime import datetime, date
from urllib.parse import quote
import urllib.request
import urllib.error

import scientific_papers_database as db
from runtime_lock_utils import load_json_file, write_json_file

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Paths
GEO_MAP_PATH = 'data/geological_map_sheets.json'
STATE_PATH = 'data/scientific_papers_fetch_state.json'

# OpenAlex API config
OPENALEX_BASE = 'https://api.openalex.org'
POLITE_EMAIL = 'aca.lukovic@nhmbeo.rs'
MAX_RESULTS_PER_QUERY = 50  # Max per query to keep DB size in check
REQUEST_DELAY = 0.2  # ~5 req/sec to stay well under limits
MAX_RETRIES = 5

# Serbian geological term translation dictionary
SERBIAN_TO_ENGLISH = {
    # Geological periods
    'Prekambrijum': 'Precambrian',
    'Rifeo-kambrijum': 'Riphean Cambrian',
    'Kambrijum': 'Cambrian',
    'Ordovicijum': 'Ordovician',
    'Silur': 'Silurian',
    'Devon': 'Devonian',
    'Karbon': 'Carboniferous',
    'Perm': 'Permian',
    'Trijas': 'Triassic',
    'Jura': 'Jurassic',
    'Kreda': 'Cretaceous',
    'Paleogen': 'Paleogene',
    'Neogen': 'Neogene',
    'Kvartar': 'Quaternary',
    'Pleistocen': 'Pleistocene',
    'Holocen': 'Holocene',
    'Miocen': 'Miocene',
    'Oligocen': 'Oligocene',
    'Eocen': 'Eocene',
    'Paleocen': 'Paleocene',
    'Pliocen': 'Pliocene',

    # Tectonic features
    'Karpato-Balkanidi': 'Carpatho-Balkanides',
    'Karpato-Balkanidi (A)': 'Carpatho-Balkanides',
    'Srpsko-Makedonska Masa': 'Serbian-Macedonian Massif',
    'Srpsko-Makedonska Masa (B)': 'Serbian-Macedonian Massif',
    'Vardarska Zona': 'Vardar Zone',
    'Dinaridi': 'Dinarides',
    'Panonski Basen': 'Pannonian Basin',
    'Rodopska Masa': 'Rhodope Massif',
    'Moravska Zona': 'Morava Zone',
    'Timočki Magmatski Kompleks': 'Timok Magmatic Complex',
    'Šumadijska Zona': 'Sumadija Zone',

    # Mineral resources
    'Metali': 'metal ore deposits',
    'Nemetali': 'non-metallic minerals',
    'Ugljevi': 'coal deposits',
    'Gradjevinski materijal': 'construction materials quarry',
    'Nemetalne mineralne sirovine': 'non-metallic mineral resources',
    'Metalične mineralne sirovine': 'metallic mineral resources',
    'Mineralne vode': 'mineral waters springs',
    'Energetske sirovine': 'energy resources',
    'Termomineralne vode': 'thermal mineral waters',
}


def translate_term(term: str) -> str:
    """Translate a Serbian geological term to English."""
    # Direct lookup
    if term in SERBIAN_TO_ENGLISH:
        return SERBIAN_TO_ENGLISH[term]
    # Try without parenthetical codes
    base = term.split('(')[0].strip()
    if base in SERBIAN_TO_ENGLISH:
        return SERBIAN_TO_ENGLISH[base]
    # Return as-is if no translation
    return term


def reconstruct_abstract(inverted_index: dict) -> str:
    """Reconstruct abstract from OpenAlex inverted index format."""
    if not inverted_index:
        return None
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort()
    return ' '.join(word for _, word in word_positions)


def parse_openalex_work(work: dict, search_query: str = None) -> dict:
    """Parse an OpenAlex work into our database format."""
    # Extract authors
    authors = []
    for authorship in work.get('authorships', []):
        author = authorship.get('author', {})
        institutions = authorship.get('institutions', [])
        inst_name = institutions[0].get('display_name', '') if institutions else ''
        inst_country = institutions[0].get('country_code', '') if institutions else ''
        authors.append({
            'name': author.get('display_name', ''),
            'orcid': author.get('orcid', ''),
            'institution': inst_name,
            'country': inst_country,
        })

    # Extract keywords
    keywords = [kw.get('keyword', '') for kw in work.get('keywords', []) if kw.get('keyword')]

    # Extract concepts
    concepts = []
    for concept in work.get('concepts', []):
        concepts.append({
            'name': concept.get('display_name', ''),
            'score': concept.get('score', 0),
            'level': concept.get('level', 0),
        })

    # Open access info
    oa = work.get('open_access', {})
    primary_location = work.get('primary_location', {}) or {}
    source = primary_location.get('source', {}) or {}

    # Abstract
    abstract = reconstruct_abstract(work.get('abstract_inverted_index'))

    # Bibliographic info
    biblio = work.get('biblio') or {}

    return {
        'openalex_id': work.get('id', ''),
        'doi': work.get('doi', ''),
        'title': work.get('title') or '',
        'abstract': abstract,
        'publication_year': work.get('publication_year'),
        'cited_by_count': work.get('cited_by_count', 0),
        'journal_name': source.get('display_name', ''),
        'volume': biblio.get('volume', ''),
        'issue': biblio.get('issue', ''),
        'authors': authors,
        'keywords': keywords,
        'concepts': concepts,
        'is_open_access': oa.get('is_oa', False),
        'oa_url': oa.get('oa_url', ''),
        'pdf_url': primary_location.get('pdf_url', ''),
        'language': work.get('language', ''),
        'source_api': 'openalex',
        'search_query': search_query,
        'fetch_date': datetime.now().strftime('%Y-%m-%d'),
    }


def openalex_search(query: str, max_results: int = MAX_RESULTS_PER_QUERY) -> list:
    """Search OpenAlex API for works matching a query."""
    results = []
    page = 1
    per_page = min(max_results, 50)

    # OpenAlex concept IDs for Earth Science and Geology
    # C127313418 = Geology, C127413603 = Earth science
    concept_filter = "concepts.id:C127313418|C127413603"

    while len(results) < max_results:
        url = (
            f"{OPENALEX_BASE}/works?"
            f"search={quote(query)}"
            f"&filter={concept_filter}"
            f"&sort=cited_by_count:desc"
            f"&per_page={per_page}"
            f"&page={page}"
            f"&mailto={POLITE_EMAIL}"
        )

        data = None
        for attempt in range(MAX_RETRIES):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': f'MuseumInfoSystem/1.0 (mailto:{POLITE_EMAIL})'})
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    works = data.get('results', [])
                    if not works:
                        return results
                    results.extend(works)
                    break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    wait = 5 * 2 ** attempt  # 5, 10, 20, 40, 80s
                    logger.warning(f"Rate limited, waiting {wait}s...")
                    time.sleep(wait)
                elif e.code == 403:
                    logger.warning(f"403 Forbidden for query: {query}")
                    return results
                else:
                    logger.error(f"HTTP {e.code} for query: {query}")
                    if attempt == MAX_RETRIES - 1:
                        return results
                    time.sleep(2 ** attempt)
            except Exception as e:
                logger.error(f"Request error: {e}")
                if attempt == MAX_RETRIES - 1:
                    return results
                time.sleep(2 ** attempt)
        else:
            # All retries exhausted
            logger.warning(f"All retries exhausted for query: {query}")
            return results

        if len(results) >= max_results:
            break

        # Check if there are more pages
        total = data.get('meta', {}).get('count', 0)
        if len(results) >= total:
            break

        page += 1
        time.sleep(REQUEST_DELAY)

    return results[:max_results]


def generate_queries_for_locality(locality: dict) -> list:
    """Generate multi-tier search queries for a locality."""
    name = locality['name']
    tumac = locality.get('tumac', {})
    queries = []

    # Tier 1: Core queries
    queries.append({
        'query': f'geology "{name}" Serbia',
        'type': 'core',
        'max_results': 50,
    })
    queries.append({
        'query': f'geological map "{name}" Serbia',
        'type': 'core',
        'max_results': 30,
    })
    queries.append({
        'query': f'"{name}" Serbia geochemistry petrology',
        'type': 'core',
        'max_results': 30,
    })

    # Tier 2: Period combinations (pick most distinctive periods)
    periods = tumac.get('geological_periods', [])
    # Prioritize less common periods
    priority_periods = ['Prekambrijum', 'Rifeo-kambrijum', 'Kambrijum', 'Ordovicijum',
                       'Silur', 'Devon', 'Karbon', 'Perm']
    for period in periods:
        en_period = translate_term(period)
        if en_period != period or period in priority_periods:
            queries.append({
                'query': f'"{name}" Serbia {en_period} geology',
                'type': 'period',
                'max_results': 20,
            })
        if len(queries) > 12:
            break  # Limit period queries

    # Tier 3: Tectonic features
    tectonic = tumac.get('tectonic_features', [])
    seen_tectonic = set()
    for feature in tectonic[:5]:
        en_feature = translate_term(feature)
        if en_feature in seen_tectonic:
            continue
        seen_tectonic.add(en_feature)
        queries.append({
            'query': f'{en_feature} Serbia geology',
            'type': 'tectonic',
            'max_results': 20,
        })

    # Tier 4: Mineral resources
    minerals = tumac.get('mineral_resources', [])
    for resource in minerals[:4]:
        en_resource = translate_term(resource)
        queries.append({
            'query': f'"{name}" {en_resource} Serbia',
            'type': 'mineral',
            'max_results': 20,
        })

    return queries


def load_state() -> dict:
    """Load fetch state for resume capability."""
    if os.path.exists(STATE_PATH):
        return load_json_file(STATE_PATH, default={'completed_localities': [], 'completed_queries': {}, 'stats': {}})
    return {'completed_localities': [], 'completed_queries': {}, 'stats': {}}


def save_state(state: dict):
    """Save fetch state."""
    write_json_file(STATE_PATH, state)


def fetch_for_locality(locality: dict, state: dict, dry_run: bool = False) -> dict:
    """Fetch papers for a single locality. Returns stats."""
    name = locality['name']
    ogk_code = locality.get('ogk_code', '')
    queries = generate_queries_for_locality(locality)

    completed_queries = state.get('completed_queries', {}).get(name, [])
    stats = {'new_papers': 0, 'linked': 0, 'queries': 0, 'skipped': 0}

    for qinfo in queries:
        query = qinfo['query']
        max_results = qinfo['max_results']

        # Skip already completed queries
        if query in completed_queries:
            stats['skipped'] += 1
            continue

        if dry_run:
            logger.info(f"  [{qinfo['type']}] {query} (max: {max_results})")
            stats['queries'] += 1
            continue

        logger.info(f"  [{qinfo['type']}] Searching: {query}")
        works = openalex_search(query, max_results)

        for rank, work in enumerate(works):
            paper_data = parse_openalex_work(work, search_query=query)
            paper_id = db.insert_paper(paper_data)

            if paper_id:
                db.link_paper_to_locality(
                    paper_id, name, ogk_code,
                    link_type=qinfo['type'],
                    relevance_rank=rank,
                    search_query=query
                )
                stats['linked'] += 1
                if paper_data.get('openalex_id'):
                    stats['new_papers'] += 1

        stats['queries'] += 1

        # Track completed query
        if name not in state.get('completed_queries', {}):
            state.setdefault('completed_queries', {})[name] = []
        state['completed_queries'][name].append(query)
        save_state(state)

        time.sleep(REQUEST_DELAY)

    return stats


def main():
    parser = argparse.ArgumentParser(description='Fetch scientific papers from OpenAlex')
    parser.add_argument('--locality', type=str, help='Fetch for a single locality')
    parser.add_argument('--resume', action='store_true', help='Resume interrupted fetch')
    parser.add_argument('--dry-run', action='store_true', help='Preview queries without fetching')
    parser.add_argument('--max-per-query', type=int, default=MAX_RESULTS_PER_QUERY,
                       help='Max results per query (default: 50)')
    args = parser.parse_args()

    # Load geological map sheets
    if not os.path.exists(GEO_MAP_PATH):
        logger.error(f"Geological map sheets file not found: {GEO_MAP_PATH}")
        sys.exit(1)

    localities = load_json_file(GEO_MAP_PATH, default=[])

    logger.info(f"Loaded {len(localities)} geological map sheet localities")

    # Initialize database
    db.init_database()

    # Load or reset state
    if args.resume:
        state = load_state()
        logger.info(f"Resuming: {len(state.get('completed_localities', []))} localities already done")
    else:
        state = {'completed_localities': [], 'completed_queries': {}, 'stats': {}}

    # Filter to single locality if specified
    if args.locality:
        localities = [l for l in localities if l['name'].lower() == args.locality.lower()]
        if not localities:
            logger.error(f"Locality '{args.locality}' not found")
            sys.exit(1)
        logger.info(f"Fetching for single locality: {localities[0]['name']}")

    # Process localities
    total_new = 0
    total_linked = 0
    total_queries = 0
    start_time = time.time()

    for i, locality in enumerate(localities):
        name = locality['name']

        # Skip completed (unless single locality mode)
        if not args.locality and name in state.get('completed_localities', []):
            logger.info(f"[{i+1}/{len(localities)}] {name} - already done, skipping")
            continue

        elapsed = time.time() - start_time
        if i > 0 and elapsed > 0 and not args.dry_run:
            rate = i / elapsed * 60  # localities per minute
            remaining = (len(localities) - i) / rate if rate > 0 else 0
            logger.info(f"[{i+1}/{len(localities)}] Processing: {name} (ETA: {remaining:.0f} min)")
        else:
            logger.info(f"[{i+1}/{len(localities)}] Processing: {name}")

        if args.dry_run:
            queries = generate_queries_for_locality(locality)
            logger.info(f"  Generated {len(queries)} queries:")
            for q in queries:
                logger.info(f"    [{q['type']}] {q['query']} (max: {q['max_results']})")
            total_queries += len(queries)
            continue

        stats = fetch_for_locality(locality, state, dry_run=args.dry_run)
        total_new += stats['new_papers']
        total_linked += stats['linked']
        total_queries += stats['queries']

        logger.info(f"  -> {stats['new_papers']} new, {stats['linked']} linked, "
                    f"{stats['queries']} queries, {stats['skipped']} skipped")

        # Mark locality complete
        state.setdefault('completed_localities', []).append(name)
        save_state(state)

    elapsed = time.time() - start_time

    if args.dry_run:
        logger.info(f"\n=== DRY RUN COMPLETE ===")
        logger.info(f"Total queries to execute: {total_queries}")
        logger.info(f"Estimated API calls: {total_queries}")
        logger.info(f"Estimated time: {total_queries * 0.15 / 60:.1f} minutes")
    else:
        logger.info(f"\n=== FETCH COMPLETE ===")
        logger.info(f"Time: {elapsed/60:.1f} minutes")
        logger.info(f"New papers: {total_new}")
        logger.info(f"Paper-locality links: {total_linked}")
        logger.info(f"API queries: {total_queries}")

        # Show DB stats
        db_stats = db.get_statistics()
        logger.info(f"Total papers in DB: {db_stats['total_papers']}")
        logger.info(f"Localities covered: {db_stats['localities_covered']}")


if __name__ == '__main__':
    main()
