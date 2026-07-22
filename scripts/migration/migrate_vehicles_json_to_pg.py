#!/usr/bin/env python3
"""Jednokratna rekonciliacija: data/museum_vehicles.json -> PostgreSQL.

Kontekst (ZADATAK #3): vozila su prešla na model gde je baza JEDINI izvor
istine. Pre nego što se JSON izbaci iz upotrebe, treba proveriti da baza ne
gubi nijedan podatak koji je JSON eventualno imao potpunije.

Politika je NAMERNO konzervativna — "fill-only":

  * Postojeće vozilo (spareno po id, pa po registraciji): popunjava se SAMO
    kolona koja je u bazi prazna (NULL ili '') a JSON ima vrednost. Neprazna
    vrednost u bazi se NIKAD ne pregazi (ručne ispravke u bazi pobeđuju).
  * Vozilo kojeg u bazi nema: kompletan INSERT iz JSON zapisa.
  * Neslaganje (obe strane nepUprazne, ali različite): samo se PRIJAVI kao
    KONFLIKT, bez izmene — čovek odlučuje.

Podrazumevano je DRY-RUN (ništa se ne piše). Upis tek uz --apply, u jednoj
transakciji (sve ili ništa).

Primeri:
    python scripts/migration/migrate_vehicles_json_to_pg.py            # dry-run
    python scripts/migration/migrate_vehicles_json_to_pg.py --apply    # upis
    python scripts/migration/migrate_vehicles_json_to_pg.py --json data/museum_vehicles.json
"""

import argparse
import json
import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:  # pragma: no cover - dotenv je opcion
    pass

import psycopg

# Kolone koje se rekonciliraju (id se koristi samo za sparivanje).
FILLABLE_COLUMNS = [
    'name', 'registration', 'type', 'capacity', 'status', 'year',
    'make_model', 'notes', 'image_ids', 'vin', 'model_variant',
    'max_mass_kg', 'curb_mass_kg', 'engine_displacement_cc',
    'engine_power_kw', 'fuel_type', 'fuel_consumption',
]

# Kolone za koje '' takođe znači "prazno" (tekstualne).
TEXT_COLUMNS = {
    'name', 'registration', 'type', 'capacity', 'status', 'year',
    'make_model', 'notes', 'vin', 'model_variant', 'fuel_type',
}


def _db_url():
    url = os.environ.get('DATABASE_URL', '').replace('postgresql+psycopg://', 'postgresql://')
    if not url:
        print('❌ DATABASE_URL nije podešen.', file=sys.stderr)
        sys.exit(2)
    return url


def _load_json(path):
    if not os.path.exists(path):
        print(f'❌ JSON fajl ne postoji: {path}', file=sys.stderr)
        sys.exit(2)
    with open(path, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    return data if isinstance(data, list) else []


def _is_empty(column, value):
    """Da li je vrednost iz baze 'prazna' za svrhu popunjavanja."""
    if value is None:
        return True
    if column in TEXT_COLUMNS and isinstance(value, str) and value.strip() == '':
        return True
    if column == 'image_ids' and value == []:
        return True
    return False


def _json_has_value(column, value):
    if value is None:
        return False
    if column in TEXT_COLUMNS and isinstance(value, str) and value.strip() == '':
        return False
    if column == 'image_ids' and not value:
        return False
    # fuel_consumption == 0 je "nepoznato", ne stvarna potrošnja — ne popunjavaj
    # NULL (nepoznato) sa zavaravajućom nulom.
    if column == 'fuel_consumption' and value in (0, 0.0):
        return False
    return True


def _fetch_db_vehicles(conn):
    cols = ', '.join(['id'] + FILLABLE_COLUMNS)
    with conn.cursor() as cur:
        cur.execute(f'SELECT {cols} FROM vehicles')
        rows = cur.fetchall()
        names = [d[0] for d in cur.description]
    return [dict(zip(names, row)) for row in rows]


def _match(db_vehicles, jrec):
    """Spari JSON zapis sa DB redom: prvo po id, pa po registraciji."""
    jid = jrec.get('id')
    for row in db_vehicles:
        if jid is not None and row['id'] == jid:
            return row
    jreg = (jrec.get('registration') or '').strip()
    if jreg and jreg not in ('-', '--'):
        for row in db_vehicles:
            if (row.get('registration') or '').strip() == jreg:
                return row
    return None


def reconcile(conn, json_vehicles, *, apply):
    db_vehicles = _fetch_db_vehicles(conn)
    fills = []       # (id, column, old, new)
    conflicts = []   # (id, column, db_value, json_value)
    inserts = []     # json records with no DB match

    for jrec in json_vehicles:
        db_row = _match(db_vehicles, jrec)
        if db_row is None:
            inserts.append(jrec)
            continue
        for column in FILLABLE_COLUMNS:
            jval = jrec.get(column)
            dval = db_row.get(column)
            if not _json_has_value(column, jval):
                continue
            if _is_empty(column, dval):
                fills.append((db_row['id'], column, dval, jval))
            elif dval != jval:
                conflicts.append((db_row['id'], column, dval, jval))

    _report(fills, conflicts, inserts)

    if not apply:
        print('\nℹ️  DRY-RUN — ništa nije upisano. Pokreni sa --apply za upis.')
        return

    if not fills and not inserts:
        print('\n✅ Nema šta da se migrira; baza je već potpuna.')
        return

    with conn.cursor() as cur:
        for vehicle_id, column, _old, new in fills:
            cur.execute(
                f'UPDATE vehicles SET {column} = %s, updated_at = now() WHERE id = %s',
                (new, vehicle_id),
            )
        for jrec in inserts:
            cur.execute(
                """
                INSERT INTO vehicles (
                    id, name, registration, type, capacity, status, year,
                    make_model, notes, image_ids, vin, model_variant,
                    max_mass_kg, curb_mass_kg, engine_displacement_cc,
                    engine_power_kw, fuel_type, fuel_consumption
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    jrec.get('id'), jrec.get('name'), jrec.get('registration'),
                    jrec.get('type'), jrec.get('capacity'), jrec.get('status', 'Активно'),
                    jrec.get('year'), jrec.get('make_model'), jrec.get('notes'),
                    jrec.get('image_ids') or [], jrec.get('vin'), jrec.get('model_variant'),
                    jrec.get('max_mass_kg'), jrec.get('curb_mass_kg'),
                    jrec.get('engine_displacement_cc'), jrec.get('engine_power_kw'),
                    jrec.get('fuel_type'), jrec.get('fuel_consumption'),
                ),
            )
    conn.commit()
    print(f'\n✅ Upisano: {len(fills)} popunjavanja, {len(inserts)} novih vozila.')


def _report(fills, conflicts, inserts):
    print('=' * 64)
    print('REKONCILIACIJA VOZILA: JSON -> PostgreSQL (fill-only)')
    print('=' * 64)

    print(f'\n▶ Popunjavanja praznih kolona ({len(fills)}):')
    for vehicle_id, column, old, new in fills:
        print(f'   vozilo #{vehicle_id}: {column}: {old!r} -> {new!r}')
    if not fills:
        print('   (nema)')

    print(f'\n▶ Nova vozila za INSERT ({len(inserts)}):')
    for jrec in inserts:
        print(f"   id={jrec.get('id')} {jrec.get('name')} ({jrec.get('registration')})")
    if not inserts:
        print('   (nema)')

    print(f'\n▶ KONFLIKTI — obe strane popunjene, različite ({len(conflicts)}):')
    print('   (NE menjaju se automatski — baza pobeđuje; proveri ručno)')
    for vehicle_id, column, dval, jval in conflicts:
        print(f'   vozilo #{vehicle_id}: {column}: baza={dval!r}  json={jval!r}')
    if not conflicts:
        print('   (nema)')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', default='data/museum_vehicles.json',
                        help='putanja do JSON fajla (podrazumevano data/museum_vehicles.json)')
    parser.add_argument('--apply', action='store_true',
                        help='stvarno upiši izmene (podrazumevano je dry-run)')
    args = parser.parse_args()

    json_vehicles = _load_json(args.json)
    print(f'Učitano {len(json_vehicles)} vozila iz {args.json}')

    conn = psycopg.connect(_db_url())
    try:
        reconcile(conn, json_vehicles, apply=args.apply)
    finally:
        conn.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
