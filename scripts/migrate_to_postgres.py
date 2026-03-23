#!/usr/bin/env python3
"""
Phase 2 Migration Helper

Extracts data from local SQLite sources and streams them into PostgreSQL.
The script is intentionally modular so each dataset can be migrated
independently (minerals, bird ringing, inventory, timesheet).
"""

import json
import os
import sqlite3
from contextlib import contextmanager
from typing import Generator, Iterable, Tuple, Optional

import psycopg
from psycopg.rows import dict_row

SQLITE_PATHS = {
    "minerals": "PrirodnjackiMuzej/prirodnjacki_muzej.sqlite",
    "bird_ringing": "data/bird_ringing.db",
    "inventory": "data/inventory_book.db",
    "timesheet": "localSQLtesting/museum_timesheet.db",
}


def chunked(iterable: Iterable, size: int) -> Generator[list, None, None]:
    """Yield successive chunks from an iterable."""
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


@contextmanager
def sqlite_conn(path: str):
    """Yield a read-only SQLite connection."""
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def pg_conn() -> Generator[psycopg.Connection, None, None]:
    """Yield a PostgreSQL connection using DATABASE_URL."""
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL must be set for migration.")
    with psycopg.connect(dsn, autocommit=False) as conn:
        yield conn


def migrate_bird_ringing(batch_size: int = 1000) -> None:
    """
    Stream bird ringing records into PostgreSQL.
    Assumes the target schema already exists (`bird_ringing_records`, `bird_species`).
    """
    source = SQLITE_PATHS["bird_ringing"]
    with sqlite_conn(source) as sqlite_db, pg_conn() as pg_db:
        cursor = sqlite_db.execute("SELECT * FROM bird_ringing ORDER BY id")
        for rows in chunked(cursor, batch_size):
            transformed = [_transform_bird_row(row) for row in rows]
            _insert_bird_batch(pg_db, transformed)
        pg_db.commit()


def _transform_bird_row(row: sqlite3.Row) -> Tuple:
    """Normalize a SQLite bird ringing row for Postgres COPY."""
    coords = _parse_coordinates(row["coordinates"])
    raw_data = dict(row)
    return (
        row["ring_number"],
        row["color_ring"],
        row["species"],
        row["age"],
        row["sex"],
        row["location"],
        coords,
        row["coordinate_accuracy"],
        row["date"],
        row["time"],
        row["metal_ring_position"],
        row["plastic_ring"],
        row["catching_method"],
        row["bait"],
        row["manipulation"],
        row["status"],
        row["ringer"],
        row["clutch_size"],
        row["pullus_age"],
        row["wing_length"],
        row["third_primary_feather"],
        row["mass"],
        row["molting"],
        row["back_claw"],
        row["bill_length"],
        row["bill_measurement_method"],
        row["head_length"],
        row["tarsus"],
        row["tarsus_measurement_method"],
        row["tail_length"],
        row["fat_deposits"],
        row["pectoral_muscle"],
        row["incubation_patch"],
        row["alula"],
        row["carpal_feathers"],
        row["sex_determination"],
        row["protected_areas"],
        row["notes"],
        json.dumps(raw_data),
    )


def _parse_coordinates(value: Optional[str]) -> Optional[str]:
    """Convert 'lat,lon' string to WKT POINT; returns None if unparsable."""
    if not value:
        return None
    try:
        lat_str, lon_str = [v.strip() for v in value.split(",", 1)]
        lat, lon = float(lat_str), float(lon_str)
        return f"SRID=4326;POINT({lon} {lat})"
    except Exception:
        return None


def _insert_bird_batch(pg_db: psycopg.Connection, rows: Iterable[Tuple]) -> None:
    """Insert batches into staging table using executemany."""
    with pg_db.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO staging_bird_ringing (
                ring_number,
                color_ring,
                species_name,
                age,
                sex,
                location,
                coordinates_wkt,
                coordinate_accuracy,
                event_date,
                event_time,
                metal_ring_position,
                plastic_ring,
                catching_method,
                bait,
                manipulation,
                status,
                ringer,
                clutch_size,
                pullus_age,
                wing_length,
                third_primary_feather,
                mass,
                molting,
                back_claw,
                bill_length,
                bill_measurement_method,
                head_length,
                tarsus,
                tarsus_measurement_method,
                tail_length,
                fat_deposits,
                pectoral_muscle,
                incubation_patch,
                alula,
                carpal_feathers,
                sex_determination,
                protected_areas,
                notes,
                raw_json
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """,
            rows,
        )


def migrate_timesheet(batch_size: int = 1000) -> None:
    """Stream timesheet headers and daily rows into staging tables."""
    source = SQLITE_PATHS["timesheet"]
    with sqlite_conn(source) as sqlite_db, pg_conn() as pg_db:
        with pg_db.cursor() as cur:
            cur.execute("TRUNCATE staging_timesheet_reports")
            cur.execute("TRUNCATE staging_timesheet_days")
        header_cursor = sqlite_db.execute(
            """
            SELECT
                radna_lista_id,
                ime_prezime,
                mesec,
                godina,
                organizaciona_jedinica,
                radno_mesto,
                NULL AS poseban_obim_posla,
                NULL AS vanredni_poslovi,
                NULL AS potpis_zaposlenog,
                NULL AS nalogodavac,
                NULL AS potpis_sefa,
                NULL AS potpis_direktora,
                NULL AS povecanje_umanjenje_zarade,
                NULL AS o_posao,
                created_at
            FROM radna_lista
            ORDER BY radna_lista_id
            """
        )
        for rows in chunked(header_cursor, batch_size):
            transformed = [_transform_timesheet_header(row) for row in rows]
            _insert_timesheet_headers(pg_db, transformed)

        day_cursor = sqlite_db.execute(
            """
            SELECT
                radna_lista_id,
                dan,
                rad_na_mestu,
                van_muzeja,
                godisnji_odmor,
                drzavni_praznik,
                placeno_odsustvo,
                ostalo_odsustvo,
                bolovanje_manje_30,
                bolovanje_vece_30
            FROM radna_lista_dan
            ORDER BY radna_lista_id, dan
            """
        )
        for rows in chunked(day_cursor, batch_size):
            transformed = [_transform_timesheet_day(row) for row in rows]
            _insert_timesheet_days(pg_db, transformed)

        pg_db.commit()


def _transform_timesheet_header(row: sqlite3.Row) -> Tuple:
    return (
        row["radna_lista_id"],
        row["ime_prezime"],
        row["mesec"],
        row["godina"],
        row["organizaciona_jedinica"],
        row["radno_mesto"],
        row["poseban_obim_posla"],
        row["vanredni_poslovi"],
        row["potpis_zaposlenog"],
        row["nalogodavac"],
        row["potpis_sefa"],
        row["potpis_direktora"],
        row["povecanje_umanjenje_zarade"],
        row["o_posao"],
        row["created_at"],
    )


def _insert_timesheet_headers(pg_db: psycopg.Connection, rows: Iterable[Tuple]) -> None:
    with pg_db.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO staging_timesheet_reports (
                radna_lista_id,
                ime_prezime,
                mesec,
                godina,
                organizaciona_jedinica,
                radno_mesto,
                poseban_obim_posla,
                vanredni_poslovi,
                potpis_zaposlenog,
                nalogodavac,
                potpis_sefa,
                potpis_direktora,
                povecanje_umanjenje_zarade,
                o_posao,
                created_at
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """,
            rows,
        )


def _transform_timesheet_day(row: sqlite3.Row) -> Tuple:
    return (
        row["radna_lista_id"],
        row["dan"],
        row["rad_na_mestu"],
        row["van_muzeja"],
        row["godisnji_odmor"],
        row["drzavni_praznik"],
        row["placeno_odsustvo"],
        row["ostalo_odsustvo"],
        row["bolovanje_manje_30"],
        row["bolovanje_vece_30"],
    )


def _insert_timesheet_days(pg_db: psycopg.Connection, rows: Iterable[Tuple]) -> None:
    with pg_db.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO staging_timesheet_days (
                radna_lista_id,
                dan,
                rad_na_mestu,
                van_muzeja,
                godisnji_odmor,
                drzavni_praznik,
                placeno_odsustvo,
                ostalo_odsustvo,
                bolovanje_manje_30,
                bolovanje_vece_30
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """,
            rows,
        )

def migrate_minerals(batch_size: int = 1000) -> None:
    """Stream museum mineral inventory into staging table."""
    source = SQLITE_PATHS["minerals"]
    with sqlite_conn(source) as sqlite_db, pg_conn() as pg_db:
        cursor = sqlite_db.execute(
            """
            SELECT
                "Inv. broj" AS inv_broj,
                "Predmet" AS predmet,
                "Način nabavljanja" AS acquisition_method,
                "Datum nabavljanja" AS acquisition_date,
                "Datum unosa u bazu" AS input_date,
                "Uneo u bazu" AS input_by,
                "Legator / Našao / Doneo" AS donor,
                "Identifikovao" AS identifier,
                "Komentar/napomena" AS comments,
                "Napomena/opis" AS description,
                "Gde se nalazi" AS storage_location,
                "Lokalitet sa kartice" AS card_locality,
                "U bibliografiji" AS bibliography_flag,
                "Količina" AS quantity
            FROM minerali
            ORDER BY id
            """
        )
        for rows in chunked(cursor, batch_size):
            transformed = [_transform_mineral_row(row) for row in rows]
            _insert_mineral_batch(pg_db, transformed)
        pg_db.commit()


def _transform_mineral_row(row: sqlite3.Row) -> Tuple:
    """Normalize mineral fields for staging."""
    return (
        row["inv_broj"],
        row["predmet"],
        row["acquisition_method"],
        row["acquisition_date"],
        row["input_date"],
        row["input_by"],
        row["donor"],
        row["identifier"],
        row["comments"],
        row["description"],
        row["storage_location"],
        row["card_locality"],
        row["bibliography_flag"],
        row["quantity"],
    )


def _insert_mineral_batch(pg_db: psycopg.Connection, rows: Iterable[Tuple]) -> None:
    with pg_db.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO staging_minerals (
                inventory_number,
                item_name,
                acquisition_method,
                acquisition_date,
                input_date,
                input_by,
                donor,
                identifier,
                comments,
                description,
                storage_location,
                card_locality,
                bibliography_flag,
                quantity
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            rows,
        )


def migrate_inventory(batch_size: int = 1000) -> None:
    """Stream inventory book entries into staging table."""
    source = SQLITE_PATHS["inventory"]
    with sqlite_conn(source) as sqlite_db, pg_conn() as pg_db:
        cursor = sqlite_db.execute("SELECT * FROM inventory_book ORDER BY id")
        for rows in chunked(cursor, batch_size):
            transformed = [_transform_inventory_row(row) for row in rows]
            _insert_inventory_batch(pg_db, transformed)
        pg_db.commit()


def _transform_inventory_row(row: sqlite3.Row) -> Tuple:
    return (
        row["inventory_number"],
        row["inventory_number_raw"],
        row["name"],
        row["locality"],
        row["quantity"],
        row["acquisition_info"],
        row["collector_donator"],
        row["notes"],
        row["sheet"],
        row["row_number"],
        row["category"],
        row["revisited"],
        row["physical_location"],
        row["revision_date"],
    )


def _insert_inventory_batch(pg_db: psycopg.Connection, rows: Iterable[Tuple]) -> None:
    with pg_db.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO staging_inventory (
                inventory_number,
                inventory_number_raw,
                name,
                locality,
                quantity,
                acquisition_info,
                collector,
                notes,
                sheet,
                row_number,
                category,
                revisited,
                physical_location,
                revision_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            rows,
        )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Phase 2 migration helper.")
    parser.add_argument(
        "--dataset",
        choices=SQLITE_PATHS.keys(),
        required=True,
        help="Dataset to migrate into staging tables.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Rows per batch when streaming from SQLite.",
    )
    args = parser.parse_args()

    if args.dataset == "bird_ringing":
        migrate_bird_ringing(batch_size=args.batch_size)
        print("✅ Bird ringing staging import complete.")
    elif args.dataset == "minerals":
        migrate_minerals(batch_size=args.batch_size)
        print("✅ Mineral staging import complete.")
    elif args.dataset == "inventory":
        migrate_inventory(batch_size=args.batch_size)
        print("✅ Inventory staging import complete.")
    elif args.dataset == "timesheet":
        migrate_timesheet(batch_size=args.batch_size)
        print("✅ Timesheet staging import complete.")
    else:
        raise NotImplementedError(f"Dataset '{args.dataset}' migration not implemented yet.")


if __name__ == "__main__":
    main()
