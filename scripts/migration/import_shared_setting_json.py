#!/usr/bin/env python3
"""Jednokratni, EKSPLICITAN uvoz JSON fajla u app_shared_settings (PostgreSQL).

Od kruga 4 revizije 2026-08 čitanje deljenih podešavanja NIKAD ne pada na JSON
fajl kad je DATABASE_URL podešen — odsustvo DB reda znači "nema posebnih
podešavanja". Stari fajl (npr. data/module_access.json) se u bazu unosi samo
ovim alatom, svesnom odlukom operatera.

    python scripts/migration/import_shared_setting_json.py \
        module_access data/module_access.json
    python scripts/migration/import_shared_setting_json.py \
        module_access data/module_access.json --execute --database museum_system

Podrazumevano dry-run (ispis plana, nula izmena). Upis traži --execute I
--database <ime> koje mora da se poklopi sa current_database(). Postojeći DB
red za isti ključ se PREPISUJE — plan to jasno kaže pre upisa.
"""

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('setting_key', help="ključ u app_shared_settings (npr. module_access)")
    parser.add_argument('json_file', help="putanja JSON fajla za uvoz")
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
    try:
        payload = json.loads(json_path.read_text(encoding='utf-8'))
    except ValueError as exc:
        print(f"Fajl {json_path} nije ispravan JSON: {exc}")
        return 1
    if not isinstance(payload, dict):
        print("Uvoz očekuje JSON objekat na vrhu fajla.")
        return 1

    from postgres_service import get_postgres_connection
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT current_database()')
            current = cur.fetchone()[0]
            cur.execute(
                "SELECT to_regclass('public.app_shared_settings') IS NOT NULL")
            table_exists = bool(cur.fetchone()[0])
            existing = None
            if table_exists:
                cur.execute(
                    'SELECT setting_value FROM app_shared_settings '
                    'WHERE setting_key = %s', (args.setting_key,))
                row = cur.fetchone()
                if row:
                    existing = row[0] if not isinstance(row, dict) else row['setting_value']

    print(f"Cilj: baza={current}  ključ={args.setting_key}")
    print(f"Iz fajla: {json_path} ({len(payload)} stavki na vrhu)")
    if existing is not None:
        print("PAŽNJA: DB red za ovaj ključ VEĆ POSTOJI i biće PREPISAN.")
    else:
        print("DB red za ovaj ključ ne postoji — biće upisan nov.")

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

    from module_access_support import save_json_settings_data
    ok = save_json_settings_data(
        setting_key=args.setting_key,
        payload=payload,
        get_postgres_connection=get_postgres_connection,
    )
    if not ok:
        print("NEUSPEH: upis u bazu nije prošao (vidi log).")
        return 1
    print(f"Upisano: {args.setting_key} <- {json_path}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
