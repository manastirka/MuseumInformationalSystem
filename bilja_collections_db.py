"""
PostgreSQL-backed data layer for the 6 Bilja mollusc collections.

Exposes a Sanja-shape in-memory dict (`{'metadata', 'specimens', 'statistics'}`)
and CRUD helpers that write to the underlying PG tables and refresh the
global caches on `app`.

Registry-driven: one entry per collection covers the table name, display
metadata, column list, and default form/column layout. Adding a new column
requires touching only the registry and the table schema.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Iterable

import psycopg
from psycopg.rows import dict_row

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
# Every column in `fields` maps 1:1 to a TEXT/INTEGER column in the PG table.
# `redni_broj` is INTEGER, all other user fields are TEXT (see db/schema_bilja_*.sql).

_COMMON_TAIL_FIELDS = ('source_file',)  # read-only provenance column

COLLECTIONS: dict[str, dict[str, Any]] = {
    'bilja_kenozojske_invertebrate': {
        'table': 'bilja_kenozojske_invertebrate',
        'category': 'paleozoology',
        'name_sr': 'Кенозојски инвертебрати',
        'name_short': 'Kenozojske invertebrate',
        'description_sr': 'Фосилни инвертебрати (квартар / дилувијум). Палеозоолошка збирка.',
        'icon': 'museum-icon-dinosaur',
        'color': 'warning',
        'module_key': 'bilja_kenozojske_invertebrate',
        'route': 'bilja_kenozojske_invertebrate',
        'collection_group': 'Кенозојски инвертебрати',
        'prefix': 'KENOZ',
        'int_fields': ('redni_broj',),
        'text_fields': (
            'inventarski_broj', 'klasa', 'red', 'familija', 'rod', 'vrsta',
            'sinonim', 'lokalitet', 'stratigrafski_nivo', 'datum_nalaska',
            'nalazac', 'odredba', 'napomena', 'dimenzije', 'broj_primeraka',
        ),
        'default_columns': [
            'inventarski_broj', 'klasa', 'familija', 'rod', 'vrsta',
            'lokalitet', 'stratigrafski_nivo', 'datum_nalaska', 'nalazac',
        ],
    },
    'bilja_hydrobioidea_radoman': {
        'table': 'bilja_hydrobioidea_radoman',
        'category': 'biology',
        'name_sr': 'Hydrobioidea — збирка Павла Радомана',
        'name_short': 'Hydrobioidea (Radoman)',
        'description_sr': 'Рецентни гастроподи (слатководни/бракични), тип-примерци (холотипови/паратипови).',
        'icon': 'museum-icon-snail',
        'color': 'info',
        'module_key': 'bilja_hydrobioidea_radoman',
        'route': 'bilja_hydrobioidea_radoman',
        'collection_group': 'Hydrobioidea — Павле Радоман',
        'prefix': 'HYDRO',
        'int_fields': ('redni_broj',),
        'text_fields': (
            'inventarski_broj', 'klasa', 'red', 'familija', 'rod', 'vrsta',
            'tipska_vrsta', 'sinonim', 'lokalitet', 'rasprostranjenost',
            'datum_nalaska', 'broj_primeraka', 'holotip', 'paratip',
            'lektotip', 'paralektotip', 'dimenzije_ljusture', 'ekoloske_osobine',
            'legator', 'odredba', 'zbirka_orman_kutija', 'ugrozenost',
            'napomena', 'literatura',
        ),
        'default_columns': [
            'inventarski_broj', 'familija', 'rod', 'vrsta', 'lokalitet',
            'broj_primeraka', 'holotip', 'paratip', 'legator',
        ],
    },
    'bilja_suvozemni_puzevi_pavlovic': {
        'table': 'bilja_suvozemni_puzevi_pavlovic',
        'category': 'biology',
        'name_sr': 'Сувоземни пужеви — збирка П. С. Павловића',
        'name_short': 'Сувоземни пужеви (Павловић)',
        'description_sr': 'Рецентни копнени гастроподи — историјска збирка П. С. Павловића.',
        'icon': 'museum-icon-snail',
        'color': 'success',
        'module_key': 'bilja_suvozemni_puzevi_pavlovic',
        'route': 'bilja_suvozemni_puzevi_pavlovic',
        'collection_group': 'Сувоземни пужеви — П. С. Павловић',
        'prefix': 'PAVL',
        'int_fields': ('redni_broj',),
        'text_fields': (
            'inventarski_broj', 'klasa', 'red', 'familija', 'rod', 'vrsta',
            'sinonim', 'lokalitet', 'rasprostranjenost', 'datum_nalaska',
            'broj_primeraka', 'dimenzije_ljusture', 'ekoloske_osobine',
            'ps_pavlovic', 'odredba', 'zbirka_orman_kutija', 'ugrozenost',
            'napomena', 'literatura',
        ),
        'default_columns': [
            'inventarski_broj', 'familija', 'rod', 'vrsta', 'lokalitet',
            'datum_nalaska', 'broj_primeraka', 'zbirka_orman_kutija',
        ],
    },
    'bilja_opsta_zbirka_mollusca': {
        'table': 'bilja_opsta_zbirka_mollusca',
        'category': 'biology',
        'name_sr': 'Општа збирка мекушаца',
        'name_short': 'Општа Mollusca',
        'description_sr': 'Општа збирка мекушаца (Bivalvia + Gastropoda), разни сакупљачи.',
        'icon': 'museum-icon-shell',
        'color': 'primary',
        'module_key': 'bilja_opsta_zbirka_mollusca',
        'route': 'bilja_opsta_zbirka_mollusca',
        'collection_group': 'Општа збирка Mollusca',
        'prefix': 'OPMOLL',
        'int_fields': ('redni_broj',),
        'text_fields': (
            'inventarski_broj', 'klasa', 'red', 'familija', 'rod', 'vrsta',
            'sinonim', 'lokalitet', 'rasprostranjenost', 'datum_nalaska',
            'broj_primeraka', 'dimenzije_ljusture', 'ekoloske_osobine',
            'ps_pavlovic', 'odredba', 'zbirka_orman_kutija', 'ugrozenost',
            'napomena', 'literatura',
        ),
        'default_columns': [
            'inventarski_broj', 'klasa', 'familija', 'rod', 'vrsta',
            'lokalitet', 'broj_primeraka', 'ps_pavlovic',
        ],
    },
    'bilja_skoljke_tadic': {
        'table': 'bilja_skoljke_tadic',
        'category': 'biology',
        'name_sr': 'Збирка шкољки — Анте Тадић',
        'name_short': 'Шкољке (Тадић)',
        'description_sr': 'Рецентни слатководни бивалви (Unio и др.), збирка А. Тадића.',
        'icon': 'museum-icon-shell',
        'color': 'info',
        'module_key': 'bilja_skoljke_tadic',
        'route': 'bilja_skoljke_tadic',
        'collection_group': 'Збирка шкољки — Анте Тадић',
        'prefix': 'TADIC',
        'int_fields': ('redni_broj',),
        'text_fields': (
            'inventarski_broj', 'klasa', 'red', 'familija', 'rod', 'vrsta',
            'podvrsta', 'sinonim', 'lokalitet', 'datum_nalaska',
            'broj_primeraka', 'broj_levih_kapaka', 'broj_desnih_kapaka',
            'boja_ljusture_forel_ule', 'dimenzije_kapka', 'tip_brave',
            'ekoloske_osobine', 'sakupljac', 'odredba', 'zbirka_orman_kutija',
            'napomena', 'literatura',
        ),
        'default_columns': [
            'inventarski_broj', 'familija', 'rod', 'vrsta', 'podvrsta',
            'lokalitet', 'datum_nalaska', 'broj_primeraka', 'sakupljac',
        ],
    },
    'bilja_recentni_morski_mekusci': {
        'table': 'bilja_recentni_morski_mekusci',
        'category': 'biology',
        'name_sr': 'Рецентни морски мекушци',
        'name_short': 'Рецентни морски мекушци',
        'description_sr': 'Рецентни морски мекушци (Bivalvia + Gastropoda).',
        'icon': 'museum-icon-shell',
        'color': 'primary',
        'module_key': 'bilja_recentni_morski_mekusci',
        'route': 'bilja_recentni_morski_mekusci',
        'collection_group': 'Рецентни морски мекушци',
        'prefix': 'MORSK',
        'int_fields': ('redni_broj',),
        'text_fields': (
            'inventarski_broj', 'klasa', 'red', 'familija', 'rod', 'vrsta',
            'sinonim', 'lokalitet', 'rasprostranjenost', 'datum_nalaska',
            'broj_primeraka', 'izbrojan_broj_primeraka', 'dimenzije_ljusture',
            'ekoloske_osobine', 'ps_pavlovic', 'odredba', 'zbirka_orman_kutija',
            'ugrozenost', 'napomena', 'literatura',
        ),
        'default_columns': [
            'inventarski_broj', 'klasa', 'familija', 'rod', 'vrsta',
            'lokalitet', 'broj_primeraka', 'izbrojan_broj_primeraka',
        ],
    },
}


# Serbian Cyrillic labels for all fields (shared across collections; extras are
# per-collection but collisions return the same translation so we can merge).
FIELD_LABELS_SR: dict[str, str] = {
    'id': 'ИД',
    'redni_broj': 'Редни број',
    'inventarski_broj': 'Инвентарски број',
    'klasa': 'Класа',
    'red': 'Ред',
    'familija': 'Фамилија',
    'rod': 'Род',
    'vrsta': 'Врста',
    'podvrsta': 'Подврста',
    'tipska_vrsta': 'Типска врста',
    'sinonim': 'Синоним',
    'lokalitet': 'Локалитет',
    'rasprostranjenost': 'Распрострањеност',
    'stratigrafski_nivo': 'Стратиграфски ниво',
    'datum_nalaska': 'Датум налаза',
    'nalazac': 'Налазач',
    'legator': 'Легатор',
    'sakupljac': 'Сакупљач',
    'odredba': 'Одредба',
    'napomena': 'Напомена',
    'literatura': 'Литература',
    'dimenzije': 'Димензије',
    'dimenzije_ljusture': 'Димензије љуштуре',
    'dimenzije_kapka': 'Димензије капка',
    'tip_brave': 'Тип браве',
    'broj_primeraka': 'Број примерака',
    'izbrojan_broj_primeraka': 'Избројан број примерака',
    'broj_levih_kapaka': 'Бр. левих капака',
    'broj_desnih_kapaka': 'Бр. десних капака',
    'boja_ljusture_forel_ule': 'Боја љуштуре (Forel–Ule)',
    'ekoloske_osobine': 'Еколошке особине',
    'holotip': 'Холотип',
    'paratip': 'Паратип',
    'lektotip': 'Лектотип',
    'paralektotip': 'Паралектотип',
    'zbirka_orman_kutija': 'Збирка (орман, кутија)',
    'ugrozenost': 'Угроженост',
    'ps_pavlovic': 'П. С. Павловић',
    'source_file': 'Извор (фајл)',
}


# ---------------------------------------------------------------------------
# DB connection
# ---------------------------------------------------------------------------

def _database_url() -> str:
    url = os.environ.get('DATABASE_URL', '').strip()
    if not url:
        raise RuntimeError('DATABASE_URL not set — Bilja collections cannot be loaded.')
    if url.startswith('postgresql+psycopg://'):
        url = 'postgresql://' + url[len('postgresql+psycopg://'):]
    return url


def _connect():
    return psycopg.connect(_database_url())


# ---------------------------------------------------------------------------
# Validation / helpers
# ---------------------------------------------------------------------------

_IDENT_RE_OK = {k: None for k in COLLECTIONS}  # known tables whitelist


def _collection_or_raise(key: str) -> dict[str, Any]:
    if key not in COLLECTIONS:
        raise KeyError(f'Unknown Bilja collection: {key!r}')
    return COLLECTIONS[key]


def _all_user_fields(cfg: dict[str, Any]) -> tuple[str, ...]:
    return tuple(cfg['int_fields']) + tuple(cfg['text_fields'])


def _coerce_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    s = str(value).strip()
    if not s:
        return None
    try:
        return int(float(s))
    except ValueError:
        return None


def _coerce_text(value: Any) -> str:
    if value is None:
        return ''
    return str(value).strip()


# ---------------------------------------------------------------------------
# Read: loader
# ---------------------------------------------------------------------------

def _build_statistics(records: list[dict[str, Any]]) -> dict[str, int]:
    localities = {r.get('lokalitet') for r in records if r.get('lokalitet')}
    species = {r.get('vrsta') for r in records if r.get('vrsta')}
    families = {r.get('familija') for r in records if r.get('familija')}
    return {
        'total_specimens': len(records),
        'total_taxa': len(species),
        'total_localities': len(localities),
        'identified_by_count': len(families),  # reuse slot expected by render helpers
    }


def load_collection(key: str) -> dict[str, Any]:
    """Load a single collection in the Sanja-compatible shape."""
    cfg = _collection_or_raise(key)
    table = cfg['table']

    # Column order in SELECT determines order in returned dict; include id first.
    cols = ['id'] + list(_all_user_fields(cfg)) + list(_COMMON_TAIL_FIELDS)
    col_sql = ', '.join(cols)

    with _connect() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(f'SELECT {col_sql} FROM {table} ORDER BY id')  # table name is whitelisted
            rows = cur.fetchall()

    # Normalize None → '' for text fields so templates don't render 'None'.
    specimens: list[dict[str, Any]] = []
    for row in rows:
        item: dict[str, Any] = {'id': row['id']}
        for f in cfg['int_fields']:
            item[f] = row.get(f) if row.get(f) is not None else ''
        for f in cfg['text_fields']:
            item[f] = row.get(f) or ''
        for f in _COMMON_TAIL_FIELDS:
            item[f] = row.get(f) or ''
        item['collection_group'] = cfg['collection_group']
        specimens.append(item)

    return {
        'metadata': {
            'key': key,
            'name': cfg['name_sr'],
            'table': cfg['table'],
            'category': cfg['category'],
        },
        'specimens': specimens,
        'statistics': _build_statistics(specimens),
    }


def load_all() -> dict[str, dict[str, Any]]:
    """Load all 6 Bilja collections into a single dict keyed by collection key."""
    out: dict[str, dict[str, Any]] = {}
    for key in COLLECTIONS:
        try:
            out[key] = load_collection(key)
        except Exception as exc:
            logger.warning('Could not load Bilja collection %s: %s', key, exc)
            out[key] = {
                'metadata': {'key': key, 'name': COLLECTIONS[key]['name_sr'], 'error': str(exc)},
                'specimens': [],
                'statistics': _build_statistics([]),
            }
    return out


# ---------------------------------------------------------------------------
# Write: add / update / delete
# ---------------------------------------------------------------------------

def _form_to_row(cfg: dict[str, Any], form: dict[str, Any]) -> dict[str, Any]:
    row: dict[str, Any] = {}
    for f in cfg['int_fields']:
        row[f] = _coerce_int(form.get(f))
    for f in cfg['text_fields']:
        row[f] = _coerce_text(form.get(f)) or None  # store '' as NULL
    return row


def add_specimen(key: str, form: dict[str, Any]) -> int:
    cfg = _collection_or_raise(key)
    table = cfg['table']
    row = _form_to_row(cfg, form)
    row['source_file'] = _coerce_text(form.get('source_file')) or 'manual-entry'

    cols = list(row.keys())
    placeholders = ', '.join(['%s'] * len(cols))
    col_sql = ', '.join(cols)

    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f'INSERT INTO {table} ({col_sql}) VALUES ({placeholders}) RETURNING id',
                [row[c] for c in cols],
            )
            new_id = cur.fetchone()[0]
        conn.commit()

    _refresh_cache(key)
    return new_id


def update_specimen(key: str, specimen_id: int, form: dict[str, Any]) -> bool:
    cfg = _collection_or_raise(key)
    table = cfg['table']
    row = _form_to_row(cfg, form)
    # Do NOT overwrite source_file on edit.

    if not row:
        return False

    sets = ', '.join(f'{c} = %s' for c in row.keys())
    params = list(row.values()) + [int(specimen_id)]

    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f'UPDATE {table} SET {sets}, updated_at = now() WHERE id = %s',
                params,
            )
            updated = cur.rowcount
        conn.commit()

    _refresh_cache(key)
    return bool(updated)


def delete_specimen(key: str, specimen_id: int) -> bool:
    cfg = _collection_or_raise(key)
    table = cfg['table']
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(f'DELETE FROM {table} WHERE id = %s', [int(specimen_id)])
            deleted = cur.rowcount
        conn.commit()

    _refresh_cache(key)
    return bool(deleted)


def find_specimen(key: str, specimen_id: int) -> dict[str, Any] | None:
    cfg = _collection_or_raise(key)
    table = cfg['table']
    cols = ['id'] + list(_all_user_fields(cfg)) + list(_COMMON_TAIL_FIELDS)
    col_sql = ', '.join(cols)
    with _connect() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(f'SELECT {col_sql} FROM {table} WHERE id = %s', [int(specimen_id)])
            row = cur.fetchone()
    if not row:
        return None
    item: dict[str, Any] = {'id': row['id']}
    for f in cfg['int_fields']:
        item[f] = row.get(f) if row.get(f) is not None else ''
    for f in cfg['text_fields']:
        item[f] = row.get(f) or ''
    for f in _COMMON_TAIL_FIELDS:
        item[f] = row.get(f) or ''
    item['collection_group'] = cfg['collection_group']
    return item


# ---------------------------------------------------------------------------
# Cache refresh — called after each write
# ---------------------------------------------------------------------------

def _refresh_cache(key: str) -> None:
    try:
        import app as museum_app  # deferred to avoid circular import
    except Exception:
        return
    attr = _global_name(key)
    try:
        fresh = load_collection(key)
        setattr(museum_app, attr, fresh)
    except Exception as exc:
        logger.warning('Could not refresh cache for %s: %s', key, exc)


def _global_name(key: str) -> str:
    return key.upper() + '_DATABASE'


def global_names() -> dict[str, str]:
    """Map collection key -> `app.py` module attribute name."""
    return {k: _global_name(k) for k in COLLECTIONS}
