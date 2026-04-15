#!/usr/bin/env python3
"""
Import Bilja/ Excel collections into PostgreSQL.

Covers:
  - Kenozojske invertebrate  -> bilja_kenozojske_invertebrate (paleozoology)
  - Radoman Hydrobioidea     -> bilja_hydrobioidea_radoman    (biology)
  - Pavlović suvozemni puževi-> bilja_suvozemni_puzevi_pavlovic (biology)
  - Opšta zbirka Mollusca    -> bilja_opsta_zbirka_mollusca   (biology)
  - Tadić školjke            -> bilja_skoljke_tadic           (biology)
  - Recentni morski mekušci  -> bilja_recentni_morski_mekusci (biology)

Usage:
    # apply schemas first
    psql "$DATABASE_URL" -f db/schema_bilja_paleozoology.sql
    psql "$DATABASE_URL" -f db/schema_bilja_biology.sql

    # then import
    python3 import_bilja_collections.py

Requires:
    pip install openpyxl xlrd==1.2.0 psycopg[binary] python-dotenv
"""

from __future__ import annotations

import datetime as _dt
import logging
import os
import sys
from pathlib import Path
from typing import Any, Callable, Iterable

import openpyxl
import xlrd
import psycopg
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / '.env')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(levelname)-7s  %(message)s',
)
log = logging.getLogger('bilja_import')

BILJA_DIR = Path(__file__).resolve().parent / 'Bilja'


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_database_url() -> str:
    url = os.environ.get('DATABASE_URL')
    if not url:
        raise SystemExit('DATABASE_URL is not set in environment.')
    # psycopg wants plain postgresql:// not postgresql+psycopg://
    if url.startswith('postgresql+psycopg://'):
        url = 'postgresql://' + url[len('postgresql+psycopg://'):]
    return url


def _to_text(v: Any) -> str | None:
    """Stringify cell values; preserve None for empty cells."""
    if v is None:
        return None
    if isinstance(v, str):
        s = v.strip()
        return s or None
    if isinstance(v, (_dt.datetime, _dt.date)):
        return v.strftime('%Y-%m-%d')
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def _to_int(v: Any) -> int | None:
    if v is None or v == '':
        return None
    try:
        if isinstance(v, (int, float)):
            return int(v)
        s = str(v).strip()
        if not s:
            return None
        return int(float(s))
    except (ValueError, TypeError):
        return None


def _iter_xlsx_rows(path: Path, sheet_name: str) -> Iterable[tuple]:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet_name]
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            continue  # skip header
        yield row


def _iter_xls_rows(path: Path, sheet_name: str) -> Iterable[tuple]:
    wb = xlrd.open_workbook(str(path))
    ws = wb.sheet_by_name(sheet_name)
    for r in range(1, ws.nrows):
        yield tuple(ws.cell_value(r, c) for c in range(ws.ncols))


def _row_is_empty(row: tuple) -> bool:
    return all(c is None or (isinstance(c, str) and not c.strip()) for c in row)


# ---------------------------------------------------------------------------
# Row mappers — one per table
# ---------------------------------------------------------------------------

def _map_kenozojske(row: tuple, source_file: str) -> tuple:
    # 16 cols
    return (
        _to_int(row[0]),            # redni_broj
        _to_text(row[1]),           # inventarski_broj
        _to_text(row[2]),           # klasa
        _to_text(row[3]),           # red
        _to_text(row[4]),           # familija
        _to_text(row[5]),           # rod
        _to_text(row[6]),           # vrsta
        _to_text(row[7]),           # sinonim
        _to_text(row[8]),           # lokalitet
        _to_text(row[9]),           # stratigrafski_nivo
        _to_text(row[10]),          # datum_nalaska
        _to_text(row[11]),          # nalazac
        _to_text(row[12]),          # odredba
        _to_text(row[13]),          # napomena
        _to_text(row[14]),          # dimenzije
        _to_text(row[15]),          # broj_primeraka
        source_file,
    )


def _map_radoman(row: tuple, source_file: str) -> tuple:
    # 25 cols
    return (
        _to_int(row[0]),   _to_text(row[1]),  _to_text(row[2]),  _to_text(row[3]),
        _to_text(row[4]),  _to_text(row[5]),  _to_text(row[6]),  _to_text(row[7]),
        _to_text(row[8]),  _to_text(row[9]),  _to_text(row[10]), _to_text(row[11]),
        _to_text(row[12]), _to_text(row[13]), _to_text(row[14]), _to_text(row[15]),
        _to_text(row[16]), _to_text(row[17]), _to_text(row[18]), _to_text(row[19]),
        _to_text(row[20]), _to_text(row[21]), _to_text(row[22]), _to_text(row[23]),
        _to_text(row[24]),
        source_file,
    )


def _map_pavlovic_or_opsta(row: tuple, source_file: str) -> tuple:
    # 20 cols, same schema for both sheets
    return (
        _to_int(row[0]),   _to_text(row[1]),  _to_text(row[2]),  _to_text(row[3]),
        _to_text(row[4]),  _to_text(row[5]),  _to_text(row[6]),  _to_text(row[7]),
        _to_text(row[8]),  _to_text(row[9]),  _to_text(row[10]), _to_text(row[11]),
        _to_text(row[12]), _to_text(row[13]), _to_text(row[14]), _to_text(row[15]),
        _to_text(row[16]), _to_text(row[17]), _to_text(row[18]), _to_text(row[19]),
        source_file,
    )


def _map_tadic(row: tuple, source_file: str) -> tuple:
    # 23 cols
    return (
        _to_int(row[0]),   _to_text(row[1]),  _to_text(row[2]),  _to_text(row[3]),
        _to_text(row[4]),  _to_text(row[5]),  _to_text(row[6]),  _to_text(row[7]),
        _to_text(row[8]),  _to_text(row[9]),  _to_text(row[10]), _to_text(row[11]),
        _to_text(row[12]), _to_text(row[13]), _to_text(row[14]), _to_text(row[15]),
        _to_text(row[16]), _to_text(row[17]), _to_text(row[18]), _to_text(row[19]),
        _to_text(row[20]), _to_text(row[21]), _to_text(row[22]),
        source_file,
    )


def _map_morski(row: tuple, source_file: str) -> tuple:
    # 21 cols
    return (
        _to_int(row[0]),   _to_text(row[1]),  _to_text(row[2]),  _to_text(row[3]),
        _to_text(row[4]),  _to_text(row[5]),  _to_text(row[6]),  _to_text(row[7]),
        _to_text(row[8]),  _to_text(row[9]),  _to_text(row[10]), _to_text(row[11]),
        _to_text(row[12]), _to_text(row[13]), _to_text(row[14]), _to_text(row[15]),
        _to_text(row[16]), _to_text(row[17]), _to_text(row[18]), _to_text(row[19]),
        _to_text(row[20]),
        source_file,
    )


# ---------------------------------------------------------------------------
# Insert plans
# ---------------------------------------------------------------------------

INSERT_STATEMENTS: dict[str, str] = {
    'bilja_kenozojske_invertebrate': """
        INSERT INTO bilja_kenozojske_invertebrate (
            redni_broj, inventarski_broj, klasa, red, familija, rod, vrsta,
            sinonim, lokalitet, stratigrafski_nivo, datum_nalaska, nalazac,
            odredba, napomena, dimenzije, broj_primeraka, source_file
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,
    'bilja_hydrobioidea_radoman': """
        INSERT INTO bilja_hydrobioidea_radoman (
            redni_broj, inventarski_broj, klasa, red, familija, rod, vrsta,
            tipska_vrsta, sinonim, lokalitet, rasprostranjenost, datum_nalaska,
            broj_primeraka, holotip, paratip, lektotip, paralektotip,
            dimenzije_ljusture, ekoloske_osobine, legator, odredba,
            zbirka_orman_kutija, ugrozenost, napomena, literatura, source_file
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,
    'bilja_suvozemni_puzevi_pavlovic': """
        INSERT INTO bilja_suvozemni_puzevi_pavlovic (
            redni_broj, inventarski_broj, klasa, red, familija, rod, vrsta,
            sinonim, lokalitet, rasprostranjenost, datum_nalaska, broj_primeraka,
            dimenzije_ljusture, ekoloske_osobine, ps_pavlovic, odredba,
            zbirka_orman_kutija, ugrozenost, napomena, literatura, source_file
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s)
    """,
    'bilja_opsta_zbirka_mollusca': """
        INSERT INTO bilja_opsta_zbirka_mollusca (
            redni_broj, inventarski_broj, klasa, red, familija, rod, vrsta,
            sinonim, lokalitet, rasprostranjenost, datum_nalaska, broj_primeraka,
            dimenzije_ljusture, ekoloske_osobine, ps_pavlovic, odredba,
            zbirka_orman_kutija, ugrozenost, napomena, literatura, source_file
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s)
    """,
    'bilja_skoljke_tadic': """
        INSERT INTO bilja_skoljke_tadic (
            redni_broj, inventarski_broj, klasa, red, familija, rod, vrsta,
            podvrsta, sinonim, lokalitet, datum_nalaska, broj_primeraka,
            broj_levih_kapaka, broj_desnih_kapaka, boja_ljusture_forel_ule,
            dimenzije_kapka, tip_brave, ekoloske_osobine, sakupljac, odredba,
            zbirka_orman_kutija, napomena, literatura, source_file
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s)
    """,
    'bilja_recentni_morski_mekusci': """
        INSERT INTO bilja_recentni_morski_mekusci (
            redni_broj, inventarski_broj, klasa, red, familija, rod, vrsta,
            sinonim, lokalitet, rasprostranjenost, datum_nalaska, broj_primeraka,
            izbrojan_broj_primeraka, dimenzije_ljusture, ekoloske_osobine,
            ps_pavlovic, odredba, zbirka_orman_kutija, ugrozenost, napomena,
            literatura, source_file
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s)
    """,
}


JOBS: list[dict[str, Any]] = [
    {
        'table': 'bilja_kenozojske_invertebrate',
        'file': 'Copy of KENOZOJSKE INVERTEBRATE INVENTARSKA  KNJIGA nova verzija Bilja 24 02 2026 .xlsx',
        'sheet': 'Sheet1',
        'kind': 'xlsx',
        'mapper': _map_kenozojske,
    },
    {
        'table': 'bilja_hydrobioidea_radoman',
        'file': 'PAVLE RADOMAN HYDROBIOIDEA PROBA.xlsx',
        'sheet': 'Sheet1',
        'kind': 'xlsx',
        'mapper': _map_radoman,
    },
    {
        'table': 'bilja_suvozemni_puzevi_pavlovic',
        'file': 'Zbirka  suvozemnih puzeva P S Pavlovic 2022 oktobar.xlsx',
        'sheet': 'Sheet1',
        'kind': 'xlsx',
        'mapper': _map_pavlovic_or_opsta,
    },
    {
        'table': 'bilja_opsta_zbirka_mollusca',
        'file': 'Zbirka  suvozemnih puzeva P S Pavlovic 2022 oktobar.xlsx',
        'sheet': 'Opsta zbirka Mollusca',
        'kind': 'xlsx',
        'mapper': _map_pavlovic_or_opsta,
    },
    {
        'table': 'bilja_skoljke_tadic',
        'file': 'Zbirka Skoljki Ante Tadic zavrseno.xls',
        'sheet': 'Sheet1',
        'kind': 'xls',
        'mapper': _map_tadic,
    },
    {
        'table': 'bilja_recentni_morski_mekusci',
        'file': 'РЕЦЕНТНИ МОРСКИ МЕКУШЦИ.xlsx',
        'sheet': 'Sheet1',
        'kind': 'xlsx',
        'mapper': _map_morski,
    },
]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_job(cur, job: dict[str, Any]) -> tuple[int, int]:
    path = BILJA_DIR / job['file']
    if not path.exists():
        raise FileNotFoundError(f'Missing source file: {path}')

    iterator: Callable[[Path, str], Iterable[tuple]]
    iterator = _iter_xlsx_rows if job['kind'] == 'xlsx' else _iter_xls_rows

    stmt = INSERT_STATEMENTS[job['table']]
    mapper = job['mapper']
    source_file = job['file']

    inserted = skipped = 0
    batch: list[tuple] = []
    BATCH = 200

    for row in iterator(path, job['sheet']):
        if _row_is_empty(row):
            skipped += 1
            continue
        try:
            batch.append(mapper(row, source_file))
        except Exception as exc:
            log.warning('  bad row skipped in %s: %s', job['table'], exc)
            skipped += 1
            continue
        if len(batch) >= BATCH:
            cur.executemany(stmt, batch)
            inserted += len(batch)
            batch.clear()

    if batch:
        cur.executemany(stmt, batch)
        inserted += len(batch)

    return inserted, skipped


def main(argv: list[str]) -> int:
    truncate = '--truncate' in argv
    only = None
    for a in argv:
        if a.startswith('--only='):
            only = a.split('=', 1)[1]

    db_url = _get_database_url()
    log.info('Connecting to PostgreSQL…')

    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            for job in JOBS:
                if only and job['table'] != only:
                    continue
                log.info('---- %s  (%s | %s) ----', job['table'], job['file'], job['sheet'])

                if truncate:
                    log.info('  TRUNCATE %s', job['table'])
                    cur.execute(f'TRUNCATE TABLE {job["table"]} RESTART IDENTITY')

                inserted, skipped = run_job(cur, job)
                log.info('  inserted=%d  skipped=%d', inserted, skipped)

        conn.commit()

    log.info('Done.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
