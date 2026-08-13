"""Skladište naučnih vesti (revizija 2026-08, krug 4, stavka 5).

PostgreSQL (tabela science_news, migracija 053) je izvor istine čim je
DATABASE_URL podešen i tabela postoji; JSON fajl (data/science_news.json)
ostaje SAMO kao razvojno/pre-migraciono stanje. Bez tihog fallback-a: kvar
probe ili čitanja uz podešen DATABASE_URL DIŽE izuzetak umesto da tiho
posluži zastareli fajl (obrazac Sanja/Bilja iz batča 6). Jednokratni uvoz
fajla: scripts/migration/import_science_news_json.py.
"""

import json
import logging
import os

from runtime_lock_utils import load_json_file, update_json_file

logger = logging.getLogger(__name__)


def _get_postgres_connection():
    from postgres_service import get_postgres_connection
    return get_postgres_connection()


def _cell(row, index, key):
    if row is None:
        return None
    return row[key] if isinstance(row, dict) else row[index]


def uses_pg():
    """True kad je PostgreSQL backend aktivan (DATABASE_URL + tabela).

    None-konfiguracija ili legitimno odsutna tabela (pre-migraciono stanje)
    vraćaju False; kvar probe DIŽE — pad baze ne sme tiho da preusmeri
    čitanje/pisanje na zastareli JSON."""
    if not os.environ.get('DATABASE_URL'):
        return False
    with _get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT to_regclass('public.science_news') IS NOT NULL AS present")
            row = cur.fetchone()
    return bool(_cell(row, 0, 'present'))


def _item_from_row(row):
    value = _cell(row, 0, 'item')
    return json.loads(value) if isinstance(value, str) else value


def get_all_news(news_file):
    """Sve vesti kao lista dict-ova (JSON oblik zapisa)."""
    if uses_pg():
        with _get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT item FROM science_news '
                    'ORDER BY datum DESC, created_at DESC')
                return [_item_from_row(r) for r in cur.fetchall()]
    try:
        if os.path.exists(news_file):
            return load_json_file(news_file, default=[])
    except Exception as exc:
        logger.error("Error loading science news: %s", exc)
    return []


def _upsert_row(cur, item):
    cur.execute(
        """
        INSERT INTO science_news (id, datum, auto_fetched, item)
        VALUES (%s, %s, %s, %s::jsonb)
        ON CONFLICT (id) DO UPDATE SET
            datum = EXCLUDED.datum,
            auto_fetched = EXCLUDED.auto_fetched,
            item = EXCLUDED.item
        """,
        (str(item.get('id')), str(item.get('date') or ''),
         bool(item.get('auto_fetched')), json.dumps(item, ensure_ascii=False)),
    )


def add_news_item(news_file, item, cap=100):
    """Ručni unos: upsert po id + orezivanje na ``cap`` najnovijih zapisa."""
    if uses_pg():
        with _get_postgres_connection() as conn:
            with conn.cursor() as cur:
                _upsert_row(cur, item)
                cur.execute(
                    """
                    DELETE FROM science_news WHERE id NOT IN (
                        SELECT id FROM science_news
                        ORDER BY created_at DESC LIMIT %s)
                    """,
                    (cap,),
                )
            conn.commit()
        return

    def _add(existing):
        payload = [n for n in list(existing or [])
                   if n.get('id') != item.get('id')]
        payload.insert(0, item)
        return payload[:cap]

    update_json_file(news_file, _add, default=[])


def delete_news_item(news_file, news_id):
    """Brisanje po id. Vraća True ako je zapis postojao."""
    if uses_pg():
        with _get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM science_news WHERE id = %s',
                            (str(news_id),))
                found = cur.rowcount > 0
            conn.commit()
        return found

    if not os.path.exists(news_file):
        return False
    holder = {'found': False}

    def _remove(all_news):
        kept = [n for n in list(all_news or []) if n.get('id') != news_id]
        holder['found'] = len(kept) != len(all_news or [])
        return kept

    update_json_file(news_file, _remove, default=[])
    return holder['found']


def insert_fetched_items(news_file, items, max_items=50):
    """RSS auto-fetch: row-level upis novih stavki + orezivanje auto vesti.

    Ručne vesti se nikad ne orezuju ovim putem; auto_fetched zapisa ostaje
    najviše ``max_items - broj ručnih`` (isti odnos kao merge_news za JSON)."""
    if not uses_pg():
        raise RuntimeError('insert_fetched_items je samo za PostgreSQL backend')
    with _get_postgres_connection() as conn:
        with conn.cursor() as cur:
            for item in items:
                cur.execute('SELECT 1 FROM science_news WHERE id = %s',
                            (str(item.get('id')),))
                if cur.fetchone():
                    continue
                _upsert_row(cur, item)
            cur.execute(
                'SELECT count(*) AS broj FROM science_news WHERE NOT auto_fetched')
            manual_count = _cell(cur.fetchone(), 0, 'broj') or 0
            allowed_auto = max(0, max_items - int(manual_count))
            cur.execute(
                """
                DELETE FROM science_news WHERE auto_fetched AND id NOT IN (
                    SELECT id FROM science_news WHERE auto_fetched
                    ORDER BY datum DESC, created_at DESC LIMIT %s)
                """,
                (allowed_auto,),
            )
        conn.commit()


def last_auto_fetch_at():
    """Vreme poslednjeg auto-fetch zapisa u bazi (None ako ih nema)."""
    with _get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT max(created_at) AS poslednji FROM science_news '
                'WHERE auto_fetched')
            return _cell(cur.fetchone(), 0, 'poslednji')
