"""Усклађивање дигитализоване штампане инвентарске књиге и физичке базе депоа.

Семантика (по кустосу):
  * inventory_entries = дигитализована ШТАМПАНА инвентарска књига; постоји само
    до броја 3572 и извор је истине до те границе.
  * minerals = ФИЗИЧКА база депоа (шта стварно стоји у музеју). Бројеви > 3572
    постоје физички и не дирају се.

Команда `flask uskladi-knjigu-depo` (ПОДРАЗУМЕВАНО dry-run) за опсег <= 3572:
  a) записе из књиге којих нема у minerals УПИШЕ као књижне, ФИЗИЧКИ НЕПОТВРЂЕНЕ
     (physical_presence_confirmed=FALSE, source='printed-book');
  b) поклопљеним записима ДОПУНИ САМО ПРАЗНА поља из књиге (никад не прегази
     попуњено);
  c) КОНФЛИКТЕ (различито име/количина) НЕ мења — генерише преглед за кустоса
     (CSV + сажетак на екрану), уз поделу имена на вероватну транслитерацију
     наспрам суштински различитог.

--execute тражи откуцавање имена базе (потврда) пре икаквог уписа.

Језгро (`plan_*`, `classify_*`, `compute_fills`, `build_insert_row`) су чисте
функције над обичним речницима — тестирају се без базе.
"""

from __future__ import annotations

import csv
import difflib
import os
import unicodedata
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

PRINTED_BOOK_MAX = 3572
IMPORT_SOURCE = 'printed-book'
IMPORT_INPUT_BY = 'uskladi-knjigu-depo'
# Највиши стваран инвентарски број је ~4365 (M4365); све преко овог прага је
# очигледна грешка уноса (нпр. запис-уљез 2932317 „zlato“, без raw вредности).
# Уљез природно испада из означавања/усклађивања (> 3572), само се пријављује.
INTRUDER_MIN_NUMBER = 100000

# Предложено мапирање колона књига -> minerals (пријављено у dry-run извештају).
# Локалитет и начин набавке иду у чисте 1:1 колоне; напомена и сакупљач деле
# слободно текстуално поље `comments` (minerals нема наменску колону за
# сакупљача — предлог за преглед кустоса, не додаје се нова колона без одлуке).
COLUMN_MAPPING = [
    ('locality', 'card_locality', 'локалитет'),
    ('acquisition_info', 'acquisition_method', 'начин набавке'),
    ('notes', 'comments', 'напомена'),
    ('collector', 'comments', 'сакупљач (у comments, ознака „Сакупљач:“)'),
]

_CYR_TO_LAT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'ђ': 'dj', 'е': 'e',
    'ж': 'z', 'з': 'z', 'и': 'i', 'ј': 'j', 'к': 'k', 'л': 'l', 'љ': 'lj',
    'м': 'm', 'н': 'n', 'њ': 'nj', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
    'т': 't', 'ћ': 'c', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'c',
    'џ': 'dz', 'ш': 's',
}


def normalize_number(value) -> Optional[int]:
    """Само цифре из вредности -> позитиван int (M-префикс се скида); иначе None."""
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value > 0 else None
    if isinstance(value, float):
        n = int(round(value))
        return n if n > 0 else None
    digits = ''.join(ch for ch in str(value) if ch.isdigit())
    if not digits:
        return None
    n = int(digits)
    return n if n > 0 else None


def is_in_printed_book(value) -> bool:
    """Тачно за нормализован број у опсегу 1..3572 (штампана књига)."""
    n = normalize_number(value)
    return n is not None and 1 <= n <= PRINTED_BOOK_MAX


def _is_empty(value) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == '')


def _name_key(value) -> str:
    """Кључ за поређење имена: транслитерација ћир->лат, без дијакритике, само
    слова/цифре, mala slova. Изједначава ћирилицу/латиницу и ć/č/š/ž/đ разлике."""
    if value is None:
        return ''
    s = str(value).strip().lower()
    s = ''.join(_CYR_TO_LAT.get(ch, ch) for ch in s)
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    return ''.join(ch for ch in s if ch.isalnum())


def classify_name_conflict(book_name, mineral_name) -> str:
    """'same' | 'transliteration' | 'substantive'.

    'same' — идентично после нормализације кључа (нема конфликта).
    'transliteration' — различит испис, али исти/врло сличан кључ (само
        дијакритика/ck/писмо) => вероватно иста ствар.
    'substantive' — суштински различито (нпр. Antracit vs Pirit sa galenitom).
    """
    kb, km = _name_key(book_name), _name_key(mineral_name)
    if kb == km:
        return 'same'
    if not kb or not km:
        return 'substantive'
    ratio = difflib.SequenceMatcher(None, kb, km).ratio()
    return 'transliteration' if ratio >= 0.85 else 'substantive'


def _norm_qty(value) -> Optional[str]:
    """Количина као поредбени низ цифара ('' -> None)."""
    if value is None:
        return None
    digits = ''.join(ch for ch in str(value) if ch.isdigit())
    return digits or None


def compute_fills(book: Dict, mineral: Dict) -> Dict[str, str]:
    """Врати {minerals_поље: вредност} САМО за ПРАЗНА циљна поља која књига може
    да попуни. Никад не дира попуњено поље."""
    fills: Dict[str, str] = {}
    if _is_empty(mineral.get('card_locality')) and not _is_empty(book.get('locality')):
        fills['card_locality'] = book['locality'].strip()
    if _is_empty(mineral.get('acquisition_method')) and not _is_empty(book.get('acquisition_info')):
        fills['acquisition_method'] = book['acquisition_info'].strip()
    if _is_empty(mineral.get('comments')):
        composed = _compose_comments(book)
        if composed:
            fills['comments'] = composed
    return fills


def _compose_comments(book: Dict, *, with_provenance: bool = False) -> str:
    """Састави comments из напомене + сакупљача (+ порекло на упису)."""
    parts: List[str] = []
    if not _is_empty(book.get('notes')):
        parts.append(book['notes'].strip())
    if not _is_empty(book.get('collector')):
        parts.append(f"Сакупљач: {book['collector'].strip()}")
    if with_provenance:
        sheet = book.get('sheet')
        row = book.get('row_number')
        ref = []
        if not _is_empty(sheet):
            ref.append(f"лист {str(sheet).strip()}")
        if row not in (None, ''):
            ref.append(f"ред {row}")
        loc = f" ({', '.join(ref)})" if ref else ''
        parts.append(f"Уписано из штампане инвентарске књиге{loc}.")
    return '\n'.join(parts)


def build_insert_row(book: Dict) -> Dict:
    """Нов minerals ред из књишког записа: књижни, ФИЗИЧКИ НЕПОТВРЂЕН."""
    qty = _norm_qty(book.get('quantity'))
    return {
        'inventory_number': (str(book.get('inventory_number')).strip()
                             if book.get('inventory_number') is not None else None),
        'item_name': (book['name'].strip() if not _is_empty(book.get('name')) else None),
        'card_locality': (book['locality'].strip() if not _is_empty(book.get('locality')) else None),
        'acquisition_method': (book['acquisition_info'].strip()
                               if not _is_empty(book.get('acquisition_info')) else None),
        'comments': _compose_comments(book, with_provenance=True) or None,
        'quantity': int(qty) if qty else None,
        'physical_presence_confirmed': False,
        'source': IMPORT_SOURCE,
        'input_by': IMPORT_INPUT_BY,
    }


def detect_conflicts(book: Dict, mineral: Dict) -> List[Dict]:
    """Поклопљени запис: врати конфликте (име/количина) за преглед кустоса."""
    out: List[Dict] = []
    kind = classify_name_conflict(book.get('name'), mineral.get('item_name'))
    if kind != 'same':
        out.append({
            'number': normalize_number(book.get('inventory_number')),
            'field': 'name',
            'book_value': book.get('name'),
            'db_value': mineral.get('item_name'),
            'kind': kind,
            'suggestion': ('вероватна транслитерација — потврдити спајање'
                           if kind == 'transliteration'
                           else 'суштински различито — кустос пресуђује'),
        })
    qb, qm = _norm_qty(book.get('quantity')), _norm_qty(mineral.get('quantity'))
    if qb is not None and qm is not None and qb != qm:
        out.append({
            'number': normalize_number(book.get('inventory_number')),
            'field': 'quantity',
            'book_value': book.get('quantity'),
            'db_value': mineral.get('quantity'),
            'kind': 'quantity',
            'suggestion': 'различита количина — кустос пресуђује',
        })
    return out


def plan_reconciliation(book_rows: List[Dict], mineral_rows: List[Dict]) -> Dict:
    """Чиста анализа над учитаним редовима. Враћа кофере: inserts, fills,
    conflicts, + сажете бројеве. Опсег се очекује већ ограничен на <= 3572."""
    minerals_by_num: Dict[int, Dict] = {}
    for m in mineral_rows:
        n = normalize_number(m.get('inventory_number'))
        if n is not None and n not in minerals_by_num:
            minerals_by_num[n] = m

    inserts: List[Dict] = []
    fills: List[Dict] = []
    conflicts: List[Dict] = []
    fill_counts = {'card_locality': 0, 'acquisition_method': 0, 'comments': 0}

    for b in book_rows:
        n = normalize_number(b.get('inventory_number'))
        if n is None:
            continue
        m = minerals_by_num.get(n)
        if m is None:
            inserts.append({'number': n, 'row': build_insert_row(b)})
            continue
        f = compute_fills(b, m)
        if f:
            for key in f:
                fill_counts[key] = fill_counts.get(key, 0) + 1
            fills.append({'number': n, 'mineral_id': m.get('id'), 'fields': f})
        conflicts.extend(detect_conflicts(b, m))

    name_conf = [c for c in conflicts if c['field'] == 'name']
    return {
        'inserts': inserts,
        'fills': fills,
        'conflicts': conflicts,
        'summary': {
            'inserts': len(inserts),
            'matched': len(book_rows) - len(inserts),
            'fills_rows': len(fills),
            'fill_counts': fill_counts,
            'conflicts_name_total': len(name_conf),
            'conflicts_name_transliteration': sum(1 for c in name_conf if c['kind'] == 'transliteration'),
            'conflicts_name_substantive': sum(1 for c in name_conf if c['kind'] == 'substantive'),
            'conflicts_quantity': sum(1 for c in conflicts if c['field'] == 'quantity'),
        },
    }


# --------------------------------------------------------------------------- #
# Слој базе (учитавање, извештај, извршење) — танак омотач око чистог језгра.
# --------------------------------------------------------------------------- #

_BOOK_SQL = """
    SELECT id, inventory_number, inventory_number_raw, name, locality, quantity,
           acquisition_info, collector, notes, sheet, row_number
    FROM inventory_entries
    WHERE in_printed_book = TRUE
    ORDER BY id
"""

_MINERALS_SQL = """
    SELECT id, inventory_number, item_name, quantity, card_locality,
           acquisition_method, comments, physical_presence_confirmed, source
    FROM minerals
"""


def _load(cur, sql) -> List[Dict]:
    cur.execute(sql)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def load_rows(conn) -> Tuple[List[Dict], List[Dict]]:
    with conn.cursor() as cur:
        return _load(cur, _BOOK_SQL), _load(cur, _MINERALS_SQL)


def report_intruders(conn) -> List[Dict]:
    """Записи-уљези: нереалан инвентарски број (≥ INTRUDER_MIN_NUMBER, нпр.
    2932317 „zlato“). Природно су ван опсега ≤ 3572, само се пријављују."""
    with conn.cursor() as cur:
        cur.execute(r"""
            SELECT id, inventory_number, name FROM inventory_entries
            WHERE regexp_replace(inventory_number,'\D','','g') ~ '^[0-9]+$'
              AND (regexp_replace(inventory_number,'\D','','g'))::bigint >= %s
            ORDER BY id
        """, (INTRUDER_MIN_NUMBER,))
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


def write_conflicts_csv(conflicts: List[Dict], path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['broj', 'polje', 'vrednost_knjiga', 'vrednost_baza', 'tip', 'predlog'])
        for c in conflicts:
            w.writerow([c['number'], c['field'], c['book_value'], c['db_value'],
                        c['kind'], c['suggestion']])


def apply_reconciliation(conn, plan: Dict) -> Dict:
    """УПИС: нови књижни редови (непотврђени) + допуна празних поља. Конфликти се
    НЕ дирају. Све у једној трансакцији. Враћа броје примењеног."""
    applied = {'inserted': 0, 'filled_rows': 0}
    with conn.cursor() as cur:
        now = datetime.now(timezone.utc)
        for item in plan['inserts']:
            r = item['row']
            cur.execute("""
                INSERT INTO minerals
                    (inventory_number, item_name, card_locality, acquisition_method,
                     comments, quantity, physical_presence_confirmed, source,
                     input_by, input_date, created_at, updated_at)
                VALUES (%(inventory_number)s, %(item_name)s, %(card_locality)s,
                        %(acquisition_method)s, %(comments)s, %(quantity)s,
                        %(physical_presence_confirmed)s, %(source)s, %(input_by)s,
                        %(now)s, %(now)s, %(now)s)
            """, {**r, 'now': now})
            applied['inserted'] += 1
        for item in plan['fills']:
            fields = item['fields']
            set_clause = ', '.join(f"{k} = %({k})s" for k in fields)
            params = {**fields, 'id': item['mineral_id'], 'now': now}
            cur.execute(
                f"UPDATE minerals SET {set_clause}, updated_at = %(now)s WHERE id = %(id)s",
                params)
            applied['filled_rows'] += 1
    conn.commit()
    return applied


def _print_report(plan: Dict, intruders: List[Dict], csv_path: str, *, executed: bool):
    s = plan['summary']
    print("\n========== УСКЛАЂИВАЊЕ КЊИГА ↔ ДЕПО (опсег ≤ %d) ==========" % PRINTED_BOOK_MAX)
    print(f"Режим: {'ИЗВРШЕНО (--execute)' if executed else 'DRY-RUN (без измена)'}")
    print("\nПредложено мапирање колона (књига → minerals):")
    for src, dst, label in COLUMN_MAPPING:
        print(f"  • {src:16s} → minerals.{dst:20s} ({label})")
    print(f"\n(a) УПИС књижних записа којих нема у депоу: {s['inserts']}")
    print(f"    → уписују се као physical_presence_confirmed=FALSE, source='{IMPORT_SOURCE}'")
    print(f"(b) ПОКЛОПЉЕНО записа: {s['matched']}; допуна празних поља у {s['fills_rows']} редова:")
    for k, v in s['fill_counts'].items():
        print(f"    → {k:20s}: {v}")
    print(f"(c) КОНФЛИКТИ (иду у преглед, НЕ мењају се):")
    print(f"    → име различито: {s['conflicts_name_total']} "
          f"(транслитерација ~{s['conflicts_name_transliteration']}, "
          f"суштински {s['conflicts_name_substantive']})")
    print(f"    → количина различита: {s['conflicts_quantity']}")
    print(f"    → CSV преглед за кустоса: {csv_path}")
    if intruders:
        print(f"\nЗАПИСИ-УЉЕЗИ (искључени из означавања/усклађивања): {len(intruders)}")
        for it in intruders:
            print(f"    → id={it['id']} број={it['inventory_number']} име={it['name']!r}")
    print("=" * 58 + "\n")


def register_cli(app):
    import click

    @app.cli.command('uskladi-knjigu-depo')
    @click.option('--execute', is_flag=True, default=False,
                  help='Изврши упис/допуну (подразумевано је dry-run).')
    @click.option('--csv-out', default='data/uskladi_knjigu_depo_konflikti.csv',
                  show_default=True, help='Путања за CSV преглед конфликата.')
    def uskladi_knjigu_depo(execute, csv_out):
        """Усклади дигитализовану штампану књигу и физичку базу депоа (≤ 3572)."""
        from postgres_service import get_postgres_connection
        with get_postgres_connection() as conn:
            book_rows, mineral_rows = load_rows(conn)
            plan = plan_reconciliation(book_rows, mineral_rows)
            intruders = report_intruders(conn)
            write_conflicts_csv(plan['conflicts'], csv_out)

            if not execute:
                _print_report(plan, intruders, csv_out, executed=False)
                click.echo("DRY-RUN: ништа није промењено. За упис: "
                           "flask uskladi-knjigu-depo --execute")
                return

            with conn.cursor() as cur:
                cur.execute("SELECT current_database()")
                dbname = cur.fetchone()[0]
            typed = click.prompt(
                f"Потврда: откуцај име базе ('{dbname}') да извршиш упис",
                default='', show_default=False)
            if typed.strip() != dbname:
                click.echo("Име базе се не поклапа — прекид, ништа није промењено.")
                return
            applied = apply_reconciliation(conn, plan)
            _print_report(plan, intruders, csv_out, executed=True)
            click.echo(f"ИЗВРШЕНО: уписано {applied['inserted']}, "
                       f"допуњено {applied['filled_rows']} редова. Конфликти нетакнути.")
