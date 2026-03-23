#!/usr/bin/env python3
"""
Scientific Papers Database Module
PostgreSQL-backed scientific papers storage linked to geological map sheet localities.
"""

import json
import logging
import threading
from typing import Dict, List, Optional

from psycopg.rows import dict_row

from postgres_service import get_postgres_connection

logger = logging.getLogger(__name__)

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS scientific_papers (
    id BIGSERIAL PRIMARY KEY,
    openalex_id TEXT UNIQUE,
    doi TEXT,
    title TEXT NOT NULL,
    abstract TEXT,
    publication_year INTEGER,
    cited_by_count INTEGER DEFAULT 0,
    journal_name TEXT,
    volume TEXT,
    issue TEXT,
    authors_json TEXT,
    keywords_json TEXT,
    concepts_json TEXT,
    is_open_access BOOLEAN DEFAULT FALSE,
    oa_url TEXT,
    pdf_url TEXT,
    language TEXT,
    source_api TEXT DEFAULT 'openalex',
    search_query TEXT,
    fetch_date TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS paper_locality_links (
    id BIGSERIAL PRIMARY KEY,
    paper_id BIGINT NOT NULL REFERENCES scientific_papers(id) ON DELETE CASCADE,
    locality_name TEXT NOT NULL,
    ogk_code TEXT,
    link_type TEXT DEFAULT 'search',
    relevance_rank INTEGER DEFAULT 0,
    search_query TEXT,
    UNIQUE (paper_id, locality_name)
);
CREATE TABLE IF NOT EXISTS paper_feature_links (
    id BIGSERIAL PRIMARY KEY,
    paper_id BIGINT NOT NULL REFERENCES scientific_papers(id) ON DELETE CASCADE,
    feature_type TEXT NOT NULL,
    feature_name TEXT NOT NULL,
    feature_id TEXT,
    link_type TEXT DEFAULT 'search',
    relevance_rank INTEGER DEFAULT 0,
    search_query TEXT,
    UNIQUE (paper_id, feature_type, feature_name)
);
CREATE INDEX IF NOT EXISTS scientific_papers_doi_idx ON scientific_papers(doi);
CREATE INDEX IF NOT EXISTS scientific_papers_year_idx ON scientific_papers(publication_year);
CREATE INDEX IF NOT EXISTS scientific_papers_citations_idx ON scientific_papers(cited_by_count DESC);
CREATE INDEX IF NOT EXISTS scientific_papers_journal_idx ON scientific_papers(journal_name);
CREATE INDEX IF NOT EXISTS scientific_papers_language_idx ON scientific_papers(language);
CREATE INDEX IF NOT EXISTS scientific_papers_oa_idx ON scientific_papers(is_open_access);
CREATE INDEX IF NOT EXISTS scientific_papers_search_idx
    ON scientific_papers
    USING gin (
        to_tsvector(
            'simple',
            COALESCE(title, '') || ' ' ||
            COALESCE(abstract, '') || ' ' ||
            COALESCE(authors_json, '') || ' ' ||
            COALESCE(keywords_json, '')
        )
    );
CREATE INDEX IF NOT EXISTS paper_locality_links_paper_idx ON paper_locality_links(paper_id);
CREATE INDEX IF NOT EXISTS paper_locality_links_locality_idx ON paper_locality_links(locality_name);
CREATE INDEX IF NOT EXISTS paper_locality_links_ogk_idx ON paper_locality_links(ogk_code);
CREATE INDEX IF NOT EXISTS paper_feature_links_paper_idx ON paper_feature_links(paper_id);
CREATE INDEX IF NOT EXISTS paper_feature_links_type_name_idx ON paper_feature_links(feature_type, feature_name);
"""

_schema_ready = False
_schema_lock = threading.Lock()


def dict_factory(cursor, row):
    """Compatibility shim kept for callers that still import it."""
    return row


def get_connection(*, row_factory=None):
    """Get PostgreSQL connection and ensure schema exists."""
    global _schema_ready

    conn = get_postgres_connection(row_factory=row_factory or dict_row)
    with _schema_lock:
        if not _schema_ready:
            conn.execute(_SCHEMA_SQL)
            conn.commit()
            _schema_ready = True
    return conn


def init_database():
    """Ensure the scientific papers schema exists."""
    conn = get_connection()
    conn.close()
    logger.info("Scientific papers PostgreSQL schema ready")


def insert_paper(paper_data: dict) -> Optional[int]:
    """Insert a paper into the database. Returns paper ID."""
    conn = get_connection()
    try:
        if paper_data.get('openalex_id'):
            row = conn.execute(
                """
                INSERT INTO scientific_papers (
                    openalex_id, doi, title, abstract,
                    publication_year, cited_by_count, journal_name, volume, issue,
                    authors_json, keywords_json, concepts_json,
                    is_open_access, oa_url, pdf_url, language,
                    source_api, search_query, fetch_date
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (openalex_id) DO UPDATE SET
                    doi = EXCLUDED.doi,
                    title = EXCLUDED.title,
                    abstract = EXCLUDED.abstract,
                    publication_year = EXCLUDED.publication_year,
                    cited_by_count = EXCLUDED.cited_by_count,
                    journal_name = EXCLUDED.journal_name,
                    volume = EXCLUDED.volume,
                    issue = EXCLUDED.issue,
                    authors_json = EXCLUDED.authors_json,
                    keywords_json = EXCLUDED.keywords_json,
                    concepts_json = EXCLUDED.concepts_json,
                    is_open_access = EXCLUDED.is_open_access,
                    oa_url = EXCLUDED.oa_url,
                    pdf_url = EXCLUDED.pdf_url,
                    language = EXCLUDED.language,
                    source_api = EXCLUDED.source_api,
                    search_query = EXCLUDED.search_query,
                    fetch_date = EXCLUDED.fetch_date
                RETURNING id
                """,
                (
                    paper_data.get('openalex_id'),
                    paper_data.get('doi'),
                    paper_data.get('title'),
                    paper_data.get('abstract'),
                    paper_data.get('publication_year'),
                    paper_data.get('cited_by_count', 0),
                    paper_data.get('journal_name'),
                    paper_data.get('volume'),
                    paper_data.get('issue'),
                    json.dumps(paper_data.get('authors', []), ensure_ascii=False) if paper_data.get('authors') else None,
                    json.dumps(paper_data.get('keywords', []), ensure_ascii=False) if paper_data.get('keywords') else None,
                    json.dumps(paper_data.get('concepts', []), ensure_ascii=False) if paper_data.get('concepts') else None,
                    bool(paper_data.get('is_open_access')),
                    paper_data.get('oa_url'),
                    paper_data.get('pdf_url'),
                    paper_data.get('language'),
                    paper_data.get('source_api', 'openalex'),
                    paper_data.get('search_query'),
                    paper_data.get('fetch_date'),
                ),
            ).fetchone()
            conn.commit()
            return row['id'] if row else None

        row = conn.execute(
            """
            INSERT INTO scientific_papers (
                doi, title, abstract,
                publication_year, cited_by_count, journal_name, volume, issue,
                authors_json, keywords_json, concepts_json,
                is_open_access, oa_url, pdf_url, language,
                source_api, search_query, fetch_date
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            RETURNING id
            """,
            (
                paper_data.get('doi'),
                paper_data.get('title'),
                paper_data.get('abstract'),
                paper_data.get('publication_year'),
                paper_data.get('cited_by_count', 0),
                paper_data.get('journal_name'),
                paper_data.get('volume'),
                paper_data.get('issue'),
                json.dumps(paper_data.get('authors', []), ensure_ascii=False) if paper_data.get('authors') else None,
                json.dumps(paper_data.get('keywords', []), ensure_ascii=False) if paper_data.get('keywords') else None,
                json.dumps(paper_data.get('concepts', []), ensure_ascii=False) if paper_data.get('concepts') else None,
                bool(paper_data.get('is_open_access')),
                paper_data.get('oa_url'),
                paper_data.get('pdf_url'),
                paper_data.get('language'),
                paper_data.get('source_api', 'openalex'),
                paper_data.get('search_query'),
                paper_data.get('fetch_date'),
            ),
        ).fetchone()
        conn.commit()
        return row['id'] if row else None
    except Exception as exc:
        logger.error("Error inserting paper: %s", exc)
        conn.rollback()
        return None
    finally:
        conn.close()


def link_paper_to_locality(paper_id: int, locality_name: str, ogk_code: str = None,
                           link_type: str = 'search', relevance_rank: int = 0,
                           search_query: str = None):
    """Link a paper to a geological map sheet locality."""
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO paper_locality_links
                (paper_id, locality_name, ogk_code, link_type, relevance_rank, search_query)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (paper_id, locality_name) DO NOTHING
            """,
            (paper_id, locality_name, ogk_code, link_type, relevance_rank, search_query),
        )
        conn.commit()
    except Exception as exc:
        logger.error("Error linking paper %s to locality %s: %s", paper_id, locality_name, exc)
        conn.rollback()
    finally:
        conn.close()


def _build_search_where(search=None, locality_filter=None, year_filter=None,
                        journal_filter=None, min_citations=None):
    clauses = []
    params = []

    if search:
        clauses.append(
            """
            to_tsvector(
                'simple',
                COALESCE(sp.title, '') || ' ' ||
                COALESCE(sp.abstract, '') || ' ' ||
                COALESCE(sp.authors_json, '') || ' ' ||
                COALESCE(sp.keywords_json, '')
            ) @@ websearch_to_tsquery('simple', %s)
            """
        )
        params.append(search)

    if locality_filter:
        clauses.append(
            """
            sp.id IN (
                SELECT paper_id
                FROM paper_locality_links
                WHERE locality_name = %s
            )
            """
        )
        params.append(locality_filter)

    if year_filter:
        clauses.append("sp.publication_year = %s")
        params.append(int(year_filter))

    if journal_filter:
        clauses.append("sp.journal_name = %s")
        params.append(journal_filter)

    if min_citations:
        clauses.append("sp.cited_by_count >= %s")
        params.append(int(min_citations))

    return (" AND ".join(clauses) if clauses else "TRUE"), params


def _normalize_paper(paper: Dict) -> Dict:
    paper['authors'] = _parse_json_field(paper.get('authors_json'))
    paper['keywords'] = _parse_json_field(paper.get('keywords_json'))
    paper['concepts'] = _parse_json_field(paper.get('concepts_json'))
    return paper


def get_all_papers(page=1, per_page=50, search=None, locality_filter=None,
                   year_filter=None, journal_filter=None, sort_by='cited_by_count',
                   sort_order='DESC', min_citations=None):
    """
    Get scientific papers with pagination and filters.
    Returns: (papers, total_count, total_pages)
    """
    conn = get_connection()
    try:
        where_sql, params = _build_search_where(
            search=search,
            locality_filter=locality_filter,
            year_filter=year_filter,
            journal_filter=journal_filter,
            min_citations=min_citations,
        )

        allowed_sorts = {'cited_by_count', 'publication_year', 'title', 'journal_name', 'id'}
        if sort_by not in allowed_sorts:
            sort_by = 'cited_by_count'
        if sort_order.upper() not in ('ASC', 'DESC'):
            sort_order = 'DESC'

        total_count = conn.execute(
            f"SELECT COUNT(*) AS count FROM scientific_papers sp WHERE {where_sql}",
            params,
        ).fetchone()['count']

        total_pages = max(1, (total_count + per_page - 1) // per_page)
        offset = (page - 1) * per_page

        rows = conn.execute(
            f"""
            SELECT sp.*,
                   (
                       SELECT COUNT(*)
                       FROM paper_locality_links
                       WHERE paper_id = sp.id
                   ) AS locality_count
            FROM scientific_papers sp
            WHERE {where_sql}
            ORDER BY sp.{sort_by} {sort_order}, sp.id DESC
            LIMIT %s OFFSET %s
            """,
            params + [per_page, offset],
        ).fetchall()

        papers = [_normalize_paper(dict(row)) for row in rows]
        return papers, total_count, total_pages
    finally:
        conn.close()


def get_paper_by_id(paper_id: int) -> Optional[Dict]:
    """Get a single paper by ID with linked localities."""
    conn = get_connection()
    try:
        paper = conn.execute(
            "SELECT * FROM scientific_papers WHERE id = %s",
            (paper_id,),
        ).fetchone()
        if not paper:
            return None

        result = _normalize_paper(dict(paper))
        result['localities'] = [
            dict(row) for row in conn.execute(
                """
                SELECT locality_name, ogk_code, link_type, relevance_rank
                FROM paper_locality_links
                WHERE paper_id = %s
                ORDER BY relevance_rank ASC
                """,
                (paper_id,),
            ).fetchall()
        ]
        return result
    finally:
        conn.close()


def get_papers_by_locality(locality_name: str, page=1, per_page=50,
                           sort_by='cited_by_count', sort_order='DESC'):
    """Get papers linked to a specific locality with pagination."""
    conn = get_connection()
    try:
        allowed_sorts = {'cited_by_count', 'publication_year', 'title', 'journal_name', 'id'}
        if sort_by not in allowed_sorts:
            sort_by = 'cited_by_count'
        if sort_order.upper() not in ('ASC', 'DESC'):
            sort_order = 'DESC'

        total_count = conn.execute(
            """
            SELECT COUNT(*) AS count
            FROM scientific_papers sp
            INNER JOIN paper_locality_links pl ON sp.id = pl.paper_id
            WHERE pl.locality_name = %s
            """,
            (locality_name,),
        ).fetchone()['count']

        total_pages = max(1, (total_count + per_page - 1) // per_page)
        offset = (page - 1) * per_page

        rows = conn.execute(
            f"""
            SELECT sp.*,
                   pl.link_type,
                   pl.relevance_rank,
                   (
                       SELECT COUNT(*)
                       FROM paper_locality_links
                       WHERE paper_id = sp.id
                   ) AS locality_count
            FROM scientific_papers sp
            INNER JOIN paper_locality_links pl ON sp.id = pl.paper_id
            WHERE pl.locality_name = %s
            ORDER BY sp.{sort_by} {sort_order}, sp.id DESC
            LIMIT %s OFFSET %s
            """,
            (locality_name, per_page, offset),
        ).fetchall()

        papers = [_normalize_paper(dict(row)) for row in rows]
        return papers, total_count, total_pages
    finally:
        conn.close()


def search_papers(query: str, limit: int = 100) -> List[Dict]:
    """Full-text search across title, abstract, authors, and keywords."""
    if not query:
        return []

    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT sp.*,
                   (
                       SELECT COUNT(*)
                       FROM paper_locality_links
                       WHERE paper_id = sp.id
                   ) AS locality_count
            FROM scientific_papers sp
            WHERE to_tsvector(
                      'simple',
                      COALESCE(sp.title, '') || ' ' ||
                      COALESCE(sp.abstract, '') || ' ' ||
                      COALESCE(sp.authors_json, '') || ' ' ||
                      COALESCE(sp.keywords_json, '')
                  ) @@ websearch_to_tsquery('simple', %s)
            ORDER BY sp.cited_by_count DESC, sp.id DESC
            LIMIT %s
            """,
            (query, limit),
        ).fetchall()
        return [_normalize_paper(dict(row)) for row in rows]
    finally:
        conn.close()


def get_statistics() -> Dict:
    """Get database statistics."""
    conn = get_connection()
    try:
        stats = {}
        stats['total_papers'] = conn.execute(
            "SELECT COUNT(*) AS count FROM scientific_papers"
        ).fetchone()['count']
        stats['localities_covered'] = conn.execute(
            "SELECT COUNT(DISTINCT locality_name) AS count FROM paper_locality_links"
        ).fetchone()['count']

        avg = conn.execute(
            "SELECT AVG(cited_by_count) AS avg_citations FROM scientific_papers WHERE cited_by_count > 0"
        ).fetchone()['avg_citations']
        stats['avg_citations'] = round(avg, 1) if avg else 0

        stats['open_access_count'] = conn.execute(
            "SELECT COUNT(*) AS count FROM scientific_papers WHERE is_open_access = TRUE"
        ).fetchone()['count']

        year_row = conn.execute(
            """
            SELECT MIN(publication_year) AS year_min, MAX(publication_year) AS year_max
            FROM scientific_papers
            WHERE publication_year IS NOT NULL
            """
        ).fetchone()
        stats['year_min'] = year_row['year_min'] or 0
        stats['year_max'] = year_row['year_max'] or 0

        stats['top_journals'] = [
            {'journal': row['journal_name'], 'count': row['count']}
            for row in conn.execute(
                """
                SELECT journal_name, COUNT(*) AS count
                FROM scientific_papers
                WHERE journal_name IS NOT NULL AND journal_name != ''
                GROUP BY journal_name
                ORDER BY count DESC
                LIMIT 10
                """
            ).fetchall()
        ]

        stats['top_localities'] = [
            {'locality': row['locality_name'], 'count': row['count']}
            for row in conn.execute(
                """
                SELECT locality_name, COUNT(*) AS count
                FROM paper_locality_links
                GROUP BY locality_name
                ORDER BY count DESC
                LIMIT 10
                """
            ).fetchall()
        ]

        stats['papers_by_year'] = [
            {'year': row['publication_year'], 'count': row['count']}
            for row in conn.execute(
                """
                SELECT publication_year, COUNT(*) AS count
                FROM scientific_papers
                WHERE publication_year IS NOT NULL
                GROUP BY publication_year
                ORDER BY publication_year DESC
                LIMIT 30
                """
            ).fetchall()
        ]

        stats['most_cited'] = [
            {
                'id': row['id'],
                'title': row['title'],
                'citations': row['cited_by_count'],
                'year': row['publication_year'],
                'journal': row['journal_name'],
            }
            for row in conn.execute(
                """
                SELECT id, title, cited_by_count, publication_year, journal_name
                FROM scientific_papers
                ORDER BY cited_by_count DESC, id DESC
                LIMIT 5
                """
            ).fetchall()
        ]

        return stats
    finally:
        conn.close()


def get_all_localities() -> List[str]:
    """Get all unique locality names for filter dropdown."""
    conn = get_connection()
    try:
        return [
            row['locality_name']
            for row in conn.execute(
                """
                SELECT DISTINCT locality_name
                FROM paper_locality_links
                ORDER BY locality_name
                """
            ).fetchall()
        ]
    finally:
        conn.close()


def get_all_journals() -> List[str]:
    """Get all unique journal names for filter dropdown."""
    conn = get_connection()
    try:
        return [
            row['journal_name']
            for row in conn.execute(
                """
                SELECT DISTINCT journal_name
                FROM scientific_papers
                WHERE journal_name IS NOT NULL AND journal_name != ''
                ORDER BY journal_name
                """
            ).fetchall()
        ]
    finally:
        conn.close()


def get_all_years() -> List[int]:
    """Get all unique publication years for filter dropdown."""
    conn = get_connection()
    try:
        return [
            row['publication_year']
            for row in conn.execute(
                """
                SELECT DISTINCT publication_year
                FROM scientific_papers
                WHERE publication_year IS NOT NULL
                ORDER BY publication_year DESC
                """
            ).fetchall()
        ]
    finally:
        conn.close()


def get_locality_paper_count(locality_name: str) -> int:
    """Get paper count for a specific locality (for map popups)."""
    conn = get_connection()
    try:
        return conn.execute(
            """
            SELECT COUNT(*) AS count
            FROM paper_locality_links
            WHERE locality_name = %s
            """,
            (locality_name,),
        ).fetchone()['count']
    finally:
        conn.close()


def get_locality_paper_summary(locality_name: str) -> Dict:
    """Get a summary of papers for a locality (for map popups / API)."""
    conn = get_connection()
    try:
        summary = dict(conn.execute(
            """
            SELECT COUNT(*) AS paper_count,
                   AVG(sp.cited_by_count) AS avg_citations,
                   MAX(sp.cited_by_count) AS max_citations
            FROM scientific_papers sp
            INNER JOIN paper_locality_links pl ON sp.id = pl.paper_id
            WHERE pl.locality_name = %s
            """,
            (locality_name,),
        ).fetchone())

        summary['top_papers'] = [
            dict(row) for row in conn.execute(
                """
                SELECT sp.id, sp.title, sp.cited_by_count, sp.publication_year, sp.journal_name, sp.doi
                FROM scientific_papers sp
                INNER JOIN paper_locality_links pl ON sp.id = pl.paper_id
                WHERE pl.locality_name = %s
                ORDER BY sp.cited_by_count DESC, sp.id DESC
                LIMIT 5
                """,
                (locality_name,),
            ).fetchall()
        ]
        return summary
    finally:
        conn.close()


def rebuild_fts_index():
    """Refresh query planner statistics for scientific papers search."""
    conn = get_connection()
    try:
        conn.execute("REINDEX INDEX scientific_papers_search_idx")
        conn.execute("ANALYZE scientific_papers")
        conn.commit()
    finally:
        conn.close()
    logger.info("Scientific papers search index rebuilt")


def _parse_json_field(value):
    """Parse a JSON string field, returning empty list on failure."""
    if not value:
        return []
    if isinstance(value, (list, dict)):
        return value
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []


if __name__ == '__main__':
    init_database()
    print("Scientific papers PostgreSQL schema initialized")
