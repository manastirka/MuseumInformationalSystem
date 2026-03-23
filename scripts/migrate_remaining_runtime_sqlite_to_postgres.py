#!/usr/bin/env python3
"""
Migrate remaining runtime SQLite datasets into PostgreSQL.

Datasets:
- scientific_papers
- chat_room
- mail_cache
"""

import argparse
import hashlib
import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

import psycopg
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'data'
MAIL_CACHE_DIR = DATA_DIR / 'mail_cache'
MAIL_SETTINGS_PATH = DATA_DIR / 'mail_settings.json'
MIGRATION_SQL = ROOT / 'migration' / '007_remaining_sqlite_runtime_to_postgres.sql'

load_dotenv(ROOT / '.env')


@contextmanager
def sqlite_conn(path: Path):
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def pg_conn():
    dsn = os.environ.get('DATABASE_URL')
    if not dsn:
        raise RuntimeError('DATABASE_URL must be set for PostgreSQL migration.')
    dsn = dsn.replace('postgresql+psycopg://', 'postgresql://', 1)
    with psycopg.connect(dsn, autocommit=False) as conn:
        yield conn


def ensure_schema(conn):
    conn.execute(MIGRATION_SQL.read_text())
    conn.commit()


def set_sequence(conn, table: str, column: str = 'id'):
    conn.execute(
        f"""
        SELECT setval(
            pg_get_serial_sequence('{table}', '{column}'),
            COALESCE((SELECT MAX({column}) FROM {table}), 1),
            TRUE
        )
        """
    )


def migrate_scientific_papers():
    source = DATA_DIR / 'scientific_papers.db'
    if not source.exists():
        print(f"Skipping scientific_papers: {source} not found")
        return

    with sqlite_conn(source) as sqlite_db, pg_conn() as conn:
        ensure_schema(conn)
        rows = sqlite_db.execute("SELECT * FROM scientific_papers ORDER BY id").fetchall()
        for row in rows:
            conn.execute(
                """
                INSERT INTO scientific_papers (
                    id, openalex_id, doi, title, abstract,
                    publication_year, cited_by_count, journal_name, volume, issue,
                    authors_json, keywords_json, concepts_json,
                    is_open_access, oa_url, pdf_url, language,
                    source_api, search_query, fetch_date, created_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, COALESCE(%s::timestamptz, now())
                )
                ON CONFLICT (id) DO UPDATE SET
                    openalex_id = EXCLUDED.openalex_id,
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
                """,
                (
                    row['id'], row['openalex_id'], row['doi'], row['title'], row['abstract'],
                    row['publication_year'], row['cited_by_count'], row['journal_name'], row['volume'], row['issue'],
                    row['authors_json'], row['keywords_json'], row['concepts_json'],
                    bool(row['is_open_access']), row['oa_url'], row['pdf_url'], row['language'],
                    row['source_api'], row['search_query'], row['fetch_date'], row['created_at'],
                ),
            )

        rows = sqlite_db.execute("SELECT * FROM paper_locality_links ORDER BY id").fetchall()
        for row in rows:
            conn.execute(
                """
                INSERT INTO paper_locality_links (
                    id, paper_id, locality_name, ogk_code, link_type, relevance_rank, search_query
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    paper_id = EXCLUDED.paper_id,
                    locality_name = EXCLUDED.locality_name,
                    ogk_code = EXCLUDED.ogk_code,
                    link_type = EXCLUDED.link_type,
                    relevance_rank = EXCLUDED.relevance_rank,
                    search_query = EXCLUDED.search_query
                """,
                (
                    row['id'], row['paper_id'], row['locality_name'], row['ogk_code'],
                    row['link_type'], row['relevance_rank'], row['search_query'],
                ),
            )

        feature_table = sqlite_db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='paper_feature_links'"
        ).fetchone()
        if feature_table:
            rows = sqlite_db.execute("SELECT * FROM paper_feature_links ORDER BY id").fetchall()
            for row in rows:
                conn.execute(
                    """
                    INSERT INTO paper_feature_links (
                        id, paper_id, feature_type, feature_name, feature_id, link_type, relevance_rank, search_query
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        paper_id = EXCLUDED.paper_id,
                        feature_type = EXCLUDED.feature_type,
                        feature_name = EXCLUDED.feature_name,
                        feature_id = EXCLUDED.feature_id,
                        link_type = EXCLUDED.link_type,
                        relevance_rank = EXCLUDED.relevance_rank,
                        search_query = EXCLUDED.search_query
                    """,
                    (
                        row['id'], row['paper_id'], row['feature_type'], row['feature_name'],
                        row['feature_id'], row['link_type'], row['relevance_rank'], row['search_query'],
                    ),
                )

        set_sequence(conn, 'scientific_papers')
        set_sequence(conn, 'paper_locality_links')
        if feature_table:
            set_sequence(conn, 'paper_feature_links')
        conn.commit()
    print("Migrated scientific_papers.db -> PostgreSQL")


def migrate_chat_room():
    source = DATA_DIR / 'chat_room.db'
    if not source.exists():
        print(f"Skipping chat_room: {source} not found")
        return

    with sqlite_conn(source) as sqlite_db, pg_conn() as conn:
        ensure_schema(conn)
        rows = sqlite_db.execute("SELECT * FROM messages ORDER BY id").fetchall()
        for row in rows:
            conn.execute(
                """
                INSERT INTO chat_messages (
                    id, user_id, user_name, user_email, user_department,
                    channel, message, file_name, file_path, file_size, file_type,
                    timestamp, ts_epoch
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    user_id = EXCLUDED.user_id,
                    user_name = EXCLUDED.user_name,
                    user_email = EXCLUDED.user_email,
                    user_department = EXCLUDED.user_department,
                    channel = EXCLUDED.channel,
                    message = EXCLUDED.message,
                    file_name = EXCLUDED.file_name,
                    file_path = EXCLUDED.file_path,
                    file_size = EXCLUDED.file_size,
                    file_type = EXCLUDED.file_type,
                    timestamp = EXCLUDED.timestamp,
                    ts_epoch = EXCLUDED.ts_epoch
                """,
                (
                    row['id'], row['user_id'], row['user_name'], row['user_email'], row['user_department'],
                    row['channel'], row['message'], row['file_name'], row['file_path'], row['file_size'],
                    row['file_type'], row['timestamp'], row['ts_epoch'],
                ),
            )

        rows = sqlite_db.execute("SELECT * FROM presence").fetchall()
        for row in rows:
            conn.execute(
                """
                INSERT INTO chat_presence (
                    user_id, user_name, user_email, user_department, status, last_seen
                ) VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE SET
                    user_name = EXCLUDED.user_name,
                    user_email = EXCLUDED.user_email,
                    user_department = EXCLUDED.user_department,
                    status = EXCLUDED.status,
                    last_seen = EXCLUDED.last_seen
                """,
                (
                    row['user_id'], row['user_name'], row['user_email'],
                    row['user_department'], row['status'], row['last_seen'],
                ),
            )

        rows = sqlite_db.execute("SELECT * FROM unread_cursors").fetchall()
        for row in rows:
            conn.execute(
                """
                INSERT INTO chat_unread_cursors (user_id, channel, last_read_epoch)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id, channel) DO UPDATE SET
                    last_read_epoch = EXCLUDED.last_read_epoch
                """,
                (row['user_id'], row['channel'], row['last_read_epoch']),
            )

        set_sequence(conn, 'chat_messages')
        conn.commit()
    print("Migrated chat_room.db -> PostgreSQL")


def _mail_cache_mapping():
    if not MAIL_SETTINGS_PATH.exists():
        return {}
    settings = json.loads(MAIL_SETTINGS_PATH.read_text())
    return {
        hashlib.sha256(email.encode()).hexdigest()[:16]: email
        for email in settings.keys()
    }


def migrate_mail_cache():
    if not MAIL_CACHE_DIR.exists():
        print(f"Skipping mail_cache: {MAIL_CACHE_DIR} not found")
        return

    hash_to_email = _mail_cache_mapping()
    db_files = sorted(path for path in MAIL_CACHE_DIR.glob('*.db') if path.is_file())
    if not db_files:
        print("Skipping mail_cache: no SQLite cache files found")
        return

    with pg_conn() as conn:
        ensure_schema(conn)
        for db_path in db_files:
            email = hash_to_email.get(db_path.stem)
            if not email:
                print(f"Skipping unknown mail cache file: {db_path.name}")
                continue

            with sqlite_conn(db_path) as sqlite_db:
                rows = sqlite_db.execute("SELECT * FROM folders").fetchall()
                for row in rows:
                    conn.execute(
                        """
                        INSERT INTO mail_cache_folders (user_email, name, uidvalidity, highest_uid, unseen)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (user_email, name) DO UPDATE SET
                            uidvalidity = EXCLUDED.uidvalidity,
                            highest_uid = EXCLUDED.highest_uid,
                            unseen = EXCLUDED.unseen
                        """,
                        (email, row['name'], row['uidvalidity'], row['highest_uid'], row['unseen']),
                    )

                rows = sqlite_db.execute("SELECT * FROM messages").fetchall()
                for row in rows:
                    conn.execute(
                        """
                        INSERT INTO mail_cache_messages (
                            user_email, folder, uid, from_name, from_address,
                            reply_to_name, reply_to_address, subject, date_iso,
                            is_read, has_body, text_body, html_body, to_json, cc_json,
                            attachments_json, links_json
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        ON CONFLICT (user_email, folder, uid) DO UPDATE SET
                            from_name = EXCLUDED.from_name,
                            from_address = EXCLUDED.from_address,
                            reply_to_name = EXCLUDED.reply_to_name,
                            reply_to_address = EXCLUDED.reply_to_address,
                            subject = EXCLUDED.subject,
                            date_iso = EXCLUDED.date_iso,
                            is_read = EXCLUDED.is_read,
                            has_body = EXCLUDED.has_body,
                            text_body = EXCLUDED.text_body,
                            html_body = EXCLUDED.html_body,
                            to_json = EXCLUDED.to_json,
                            cc_json = EXCLUDED.cc_json,
                            attachments_json = EXCLUDED.attachments_json,
                            links_json = EXCLUDED.links_json
                        """,
                        (
                            email, row['folder'], row['uid'], row['from_name'], row['from_address'],
                            row['reply_to_name'], row['reply_to_address'], row['subject'], row['date_iso'],
                            bool(row['is_read']), bool(row['has_body']), row['text_body'], row['html_body'],
                            row['to_json'], row['cc_json'], row['attachments_json'], row['links_json'],
                        ),
                    )

                rows = sqlite_db.execute("SELECT * FROM meta").fetchall()
                for row in rows:
                    conn.execute(
                        """
                        INSERT INTO mail_cache_meta (user_email, key, value)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (user_email, key) DO UPDATE SET value = EXCLUDED.value
                        """,
                        (email, row['key'], row['value']),
                    )

                rows = sqlite_db.execute("SELECT * FROM pending_reads").fetchall()
                for row in rows:
                    conn.execute(
                        """
                        INSERT INTO mail_cache_pending_reads (user_email, folder, uid)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (user_email, folder, uid) DO NOTHING
                        """,
                        (email, row['folder'], row['uid']),
                    )
            print(f"Migrated mail cache for {email}")

        conn.commit()


def main():
    parser = argparse.ArgumentParser(description="Migrate remaining runtime SQLite datasets to PostgreSQL.")
    parser.add_argument(
        '--dataset',
        choices=['scientific_papers', 'chat_room', 'mail_cache', 'all'],
        default='all',
    )
    args = parser.parse_args()

    if args.dataset in ('scientific_papers', 'all'):
        migrate_scientific_papers()
    if args.dataset in ('chat_room', 'all'):
        migrate_chat_room()
    if args.dataset in ('mail_cache', 'all'):
        migrate_mail_cache()


if __name__ == '__main__':
    main()
