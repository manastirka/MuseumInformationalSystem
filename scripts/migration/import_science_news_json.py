#!/usr/bin/env python3
"""Jednokratni, EKSPLICITAN uvoz data/science_news.json u tabelu science_news.

Od kruga 4 revizije 2026-08 naučne vesti žive u PostgreSQL-u (migracija 053);
JSON fajl je samo razvojno/pre-migraciono stanje i u bazu ulazi isključivo
ovim alatom.

    python scripts/migration/import_science_news_json.py
    python scripts/migration/import_science_news_json.py \
        --execute --database museum_system

Podrazumevano dry-run (ispis plana, nula izmena). Upis traži --execute I
--database <ime> koje mora da se poklopi sa current_database(). Uvoz je
upsert po id — postojeći redovi sa istim id se prepisuju, ostali ostaju.
"""

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('json_file', nargs='?',
                        default=str(REPO / 'data' / 'science_news.json'))
    parser.add_argument('--execute', action='store_true',
                        help='zaista upiši (bez ovoga: dry-run)')
    parser.add_argument('--database', help='ime baze, mora = current_database()')
    args = parser.parse_args()

    try:
        from dotenv import load_dotenv
        load_dotenv(REPO / '.env')
    except Exception:
        pass

    import os
    if not os.environ.get('DATABASE_URL'):
        print("DATABASE_URL nije podešen; odbijam.")
        return 1

    json_path = Path(args.json_file)
    if not json_path.is_file():
        print(f"Fajl {json_path} ne postoji.")
        return 1
    items = json.loads(json_path.read_text(encoding='utf-8'))
    if not isinstance(items, list):
        print("Uvoz očekuje JSON listu vesti.")
        return 1
    bez_id = [i for i in items if not (isinstance(i, dict) and i.get('id'))]
    if bez_id:
        print(f"ODBIJENO: {len(bez_id)} stavki nema 'id' — fajl nije ispravan.")
        return 1

    from postgres_service import get_postgres_connection
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT current_database()')
            current = cur.fetchone()[0]
            cur.execute(
                "SELECT to_regclass('public.science_news') IS NOT NULL")
            table_exists = bool(cur.fetchone()[0])
            postojecih = None
            if table_exists:
                cur.execute('SELECT count(*) FROM science_news')
                postojecih = cur.fetchone()[0]

    print(f"Cilj: baza={current}")
    print(f"Iz fajla: {json_path} ({len(items)} vesti)")
    if not table_exists:
        print("ODBIJENO: tabela science_news ne postoji — prvo primeni "
              "migraciju 053 (deploy/run_migrations.py).")
        return 1
    print(f"U bazi već postoji {postojecih} vesti; poklapanja po id se prepisuju.")

    if not args.execute:
        print("\nDRY RUN: ništa nije menjano. Za upis dodaj "
              "--execute --database <ime baze>.")
        return 0
    if not args.database:
        print(f"ODBIJENO: upis traži --execute I --database <ime> "
              f"(current_database() je „{current}“).")
        return 1
    if args.database != current:
        print(f"ODBIJENO: --database {args.database} ≠ current_database() "
              f"„{current}“ — pogrešna baza ili pogrešan DATABASE_URL.")
        return 1

    import science_news_store
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            for item in items:
                science_news_store._upsert_row(cur, item)
        conn.commit()
    print(f"Upisano/prepisano {len(items)} vesti u science_news.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
