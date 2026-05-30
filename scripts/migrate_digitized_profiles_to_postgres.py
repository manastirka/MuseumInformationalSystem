#!/usr/bin/env python3
"""One-shot migration: load digitized cross-section profiles from the flat JSON
file into PostgreSQL.

Usage (on the server, with DATABASE_URL set):
    python scripts/migrate_digitized_profiles_to_postgres.py
    python scripts/migrate_digitized_profiles_to_postgres.py --verify

Idempotent: upserts each profile by id. The maps endpoints then read/write
Postgres automatically (Postgres-preferred, JSON fallback).
"""

import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

JSON_PATH = REPO / 'data' / 'digitized_profiles.json'
SCHEMA_PATH = REPO / 'db' / 'schema_digitized_profiles.sql'


def _load_json_profiles():
    if not JSON_PATH.exists():
        return []
    try:
        data = json.loads(JSON_PATH.read_text(encoding='utf-8'))
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Could not read {JSON_PATH}: {exc}")
        return []


def main():
    verify_only = '--verify' in sys.argv
    if not os.environ.get('DATABASE_URL'):
        print("DATABASE_URL is not set; refusing to run.")
        return 1

    import phase3a_databases
    from postgres_service import get_postgres_connection

    if not verify_only:
        conn = get_postgres_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(SCHEMA_PATH.read_text(encoding='utf-8'))
            conn.commit()
        finally:
            conn.close()

        profiles = _load_json_profiles()
        print(f"Loading {len(profiles)} digitized profile(s) from {JSON_PATH} ...")
        for profile in profiles:
            if profile.get('id'):
                phase3a_databases.upsert_digitized_profile(profile)

    if not phase3a_databases.digitized_profiles_table_exists():
        print("digitized_profiles table does not exist after migration.")
        return 1
    pg_profiles = phase3a_databases.get_digitized_profiles()
    json_count = len(_load_json_profiles())
    print(f"PostgreSQL now holds {len(pg_profiles)} profile(s) (JSON file has {json_count}).")
    print("Digitized-profiles migration verified OK.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
