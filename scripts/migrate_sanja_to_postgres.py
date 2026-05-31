#!/usr/bin/env python3
"""One-shot migration: load the Sanja Paleogene/Neogene mammal collection from
the flat JSON file into PostgreSQL.

Usage (on the server, with DATABASE_URL set):
    python scripts/migrate_sanja_to_postgres.py            # apply schema + load
    python scripts/migrate_sanja_to_postgres.py --verify   # just report counts

Idempotent: re-running replaces the table contents with the JSON file's current
specimens (upsert by id + prune). The application then reads/writes Postgres
automatically (Postgres-preferred, JSON fallback).
"""

import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

JSON_PATH = REPO / 'Sanja' / 'sanja_paleogene_neogene_mammals.json'
SCHEMA_PATH = REPO / 'db' / 'schema_sanja.sql'


def _load_json_specimens():
    if not JSON_PATH.exists():
        print(f"No JSON source at {JSON_PATH}; nothing to migrate.")
        return []
    payload = json.loads(JSON_PATH.read_text(encoding='utf-8'))
    return payload.get('specimens', []) or []


def main():
    verify_only = '--verify' in sys.argv

    try:
        from dotenv import load_dotenv
        load_dotenv(REPO / '.env')
    except Exception:
        pass
    if not os.environ.get('DATABASE_URL'):
        print("DATABASE_URL is not set; refusing to run.")
        return 1

    import phase3a_databases
    from postgres_service import get_postgres_connection

    if not verify_only:
        # 1) Ensure the table exists (idempotent CREATE ... IF NOT EXISTS).
        ddl = SCHEMA_PATH.read_text(encoding='utf-8')
        conn = get_postgres_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(ddl)
            conn.commit()
        finally:
            conn.close()

        # 2) Load the specimens.
        specimens = _load_json_specimens()
        print(f"Loading {len(specimens)} specimens from {JSON_PATH} ...")
        phase3a_databases.replace_sanja_specimens(specimens)

    # 3) Verify.
    if not phase3a_databases.sanja_table_exists():
        print("Sanja table does not exist after migration — check errors above.")
        return 1
    pg_specimens = phase3a_databases.get_sanja_specimens()
    json_count = len(_load_json_specimens())
    print(f"PostgreSQL now holds {len(pg_specimens)} specimens (JSON file has {json_count}).")
    if not verify_only and len(pg_specimens) != json_count:
        print("WARNING: counts differ — investigate before retiring the JSON file.")
        return 1
    print("Sanja migration verified OK.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
