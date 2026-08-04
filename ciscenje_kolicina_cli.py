"""Чишћење колоне `minerals.quantity` за штампани опсег (инв. број ≤ 3572).

Проблем: при увозу је ТЕКСТ из инвентарске књиге (`inventory_entries.quantity`,
изворна књига = извор истине) лоше пресликан у цео број у `minerals.quantity` —
датуми су постали огромни бројеви (13.5.2002 → 1352002), сабирци „N+1“ и белешке
су изгубљени. Овај алат ЧИТА оригинал из књиге и по правилима испод рачуна чисту
вредност, никад не губећи информацију (све избачено из количине иде у comments).

Правила (извор = `inventory_entries.quantity`):
  1) N+1 је ЗБИР: 2+1→3, 8+1→9, 3+5+5+1+4+16→34.
  2) Сложено са текстом: 3+1 Ima 3 kom → количина 4 + напомена „Ima 3 kom“.
  3) ДАТУМ → парсира се у ISO и уписује у `minerals.acquisition_date` (само ако
     је празан; ако је попуњен → конфликт у РУЧНИ ПРЕГЛЕД), количина = NULL,
     оригинал се ипак чува у comments („Из књиге, поље количина: …“).
     Само месец+година → 1. у месецу; сама година → 1. јануар (обе се означе
     као претпоставка у извештају).
  4) РИМСКИ (I, II, III, IV…) → арапски број.
  5) „ima X a ne Y“ → количина X (стваран број), цео текст у comments.
  6) ЧИСТ ТЕКСТ без броја (raspada se, Plus 1 antimonit, локације) → количина
     NULL, текст у comments.
  7) Празно или већ чист број 1–99 → не дира се.

Облик који се не може поуздано сврстати иде у листу ЗА РУЧНИ ПРЕГЛЕД и остаје
непромењен.

Језгро (`parse_date`, `classify_quantity`, `plan_cleanup`) су чисте функције над
обичним речницима — тестирају се без базе. `flask ocisti-kolicine` је танак
омотач: ПОДРАЗУМЕВАНО dry-run; `--execute` тражи откуцавање имена базе.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timezone
from typing import Dict, List, Optional, Tuple

PRINTED_BOOK_MAX = 3572
INPUT_BY = 'ocisti-kolicine'
COMMENT_BOOK_PREFIX = 'Из књиге, поље количина:'

# Српски називи месеци (латиница, како стоје у бази) + честе скраћенице.
_MONTHS = {
    'januar': 1, 'jan': 1, 'februar': 2, 'feb': 2, 'mart': 3, 'mar': 3,
    'april': 4, 'apr': 4, 'maj': 5, 'jun': 6, 'juni': 6, 'jul': 7, 'juli': 7,
    'avgust': 8, 'aug': 8, 'septembar': 9, 'sep': 9, 'sept': 9,
    'oktobar': 10, 'okt': 10, 'novembar': 11, 'nov': 11, 'decembar': 12, 'dec': 12,
}

_ROMAN = {
    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8,
    'IX': 9, 'X': 10, 'XI': 11, 'XII': 12,
}

_DMY_RE = re.compile(r'\b(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})\b')
_MONTH_YEAR_RE = re.compile(
    r'(?i)\b(' + '|'.join(sorted(_MONTHS, key=len, reverse=True)) + r')\s+((?:19|20)\d{2})\b')
_YEAR_ONLY_RE = re.compile(r'^(?:inv(?:\.|entarisano)?\s+)?((?:19|20)\d{2})\.?$', re.I)
_IMA_RE = re.compile(r'(?i)\bima\s+(\d+)\s+a\s+ne\s+\d+')
_PURE_INT_RE = re.compile(r'^\d+$')
_ADDITIVE_RE = re.compile(r'^\d+(?:\s*\+\s*\d+)+$')
# Водећи број/збир, па сепаратор (размак/зарез/тачка-зарез/двотачка), па остатак.
_LEAD_NUM_RE = re.compile(r'^(\d+(?:\s*\+\s*\d+)*)[\s,;:]+(\S.*)$', re.S)


def _build_iso(year: int, month: int, day: int) -> Optional[str]:
    """Валидан ISO датум или None (одбацује 31.2. и сл.)."""
    try:
        return date(year, month, day).isoformat()
    except ValueError:
        return None


def parse_date(value: str) -> Optional[Tuple[str, Optional[str]]]:
    """Врати (ISO_датум, претпоставка|None) ако текст садржи датум, иначе None.

    Претпоставка се пуни само када дан (или дан+месец) није познат, па је
    допуњен — то се пријављује у dry-run извештају.
    """
    if not value:
        return None
    s = value.strip()

    m = _DMY_RE.search(s)
    if m:
        iso = _build_iso(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        if iso:
            return iso, None

    m = _MONTH_YEAR_RE.search(s)
    if m:
        iso = _build_iso(int(m.group(2)), _MONTHS[m.group(1).lower()], 1)
        if iso:
            return iso, 'претпостављен 1. у месецу (позната само месец+година)'

    m = _YEAR_ONLY_RE.match(s)
    if m:
        iso = _build_iso(int(m.group(1)), 1, 1)
        if iso:
            return iso, 'претпостављен 1. јануар (позната само година)'

    return None


def _sum_additive(expr: str) -> int:
    """Збир свих сабирака у изразу типа „3+5+1“."""
    return sum(int(n) for n in re.findall(r'\d+', expr))


def _book_comment(original: str) -> str:
    return f'{COMMENT_BOOK_PREFIX} {original.strip()}'


def classify_quantity(original: Optional[str]) -> Dict:
    """Чиста класификација једне вредности количине из књиге.

    Враћа речник:
      rule    — назив правила (за груписање у извештају),
      action  — 'set' | 'null' | 'date' | 'skip' | 'review',
      quantity— циљна количина (int) за 'set', иначе None,
      comment_add — текст који треба ДОПИСАТИ у comments ('' ако нема),
      date_iso, date_assumption — само за action 'date'.
    """
    s = (original or '').strip()
    if s == '':
        return {'rule': 'prazno', 'action': 'skip', 'quantity': None, 'comment_add': ''}

    low = s.lower()

    # (3) Датум → структурисано у acquisition_date; количина NULL; траг у comments.
    parsed = parse_date(s)
    if parsed is not None:
        iso, assumption = parsed
        return {
            'rule': 'datum', 'action': 'date', 'quantity': None,
            'comment_add': _book_comment(s), 'date_iso': iso,
            'date_assumption': assumption,
        }

    # Хоризонт/откоп = стратиграфска локација, никад количина (нпр. „7 Horizont“).
    if 'horizont' in low:
        return {'rule': 'tekst', 'action': 'null', 'quantity': None,
                'comment_add': s}

    # (5) „ima X a ne Y“ → количина X, цео текст у comments.
    m = _IMA_RE.search(s)
    if m:
        return {'rule': 'ima_x_ne_y', 'action': 'set', 'quantity': int(m.group(1)),
                'comment_add': s}

    # (1) Чист збир „N+M+…“.
    if _ADDITIVE_RE.match(s):
        return {'rule': 'zbir', 'action': 'set', 'quantity': _sum_additive(s),
                'comment_add': ''}

    # (7) Чист цео број.
    if _PURE_INT_RE.match(s):
        n = int(s)
        if 1 <= n <= 99:
            return {'rule': 'cist_broj', 'action': 'set', 'quantity': n,
                    'comment_add': ''}
        # ≥100 или 0 — правила га не покривају (сумњиво), у ручни преглед.
        return {'rule': 'veliki_broj', 'action': 'review', 'quantity': None,
                'comment_add': ''}

    # (2) Водећи број/збир + текстуална напомена.
    m = _LEAD_NUM_RE.match(s)
    if m:
        lead, rest = m.group(1), m.group(2).strip()
        # Водећи број па ЈОШ један број/збир = спојене колоне → ручни преглед.
        if _ADDITIVE_RE.match(rest) or _PURE_INT_RE.match(rest):
            return {'rule': 'vise_brojeva', 'action': 'review', 'quantity': None,
                    'comment_add': ''}
        qty = _sum_additive(lead) if '+' in lead else int(lead)
        return {'rule': 'broj_plus_tekst', 'action': 'set', 'quantity': qty,
                'comment_add': rest}

    # (4) Римски број (само чист, нпр. „IX horizont“ је већ отишао горе).
    if s.upper() in _ROMAN:
        return {'rule': 'rimski', 'action': 'set', 'quantity': _ROMAN[s.upper()],
                'comment_add': ''}

    # (6) Чист текст без водећег броја → количина NULL, текст у comments.
    if not s[0].isdigit():
        return {'rule': 'tekst', 'action': 'null', 'quantity': None,
                'comment_add': s}

    return {'rule': 'za_pregled', 'action': 'review', 'quantity': None,
            'comment_add': ''}


# --------------------------------------------------------------------------- #
# Планирање над учитаним редовима (чиста функција).
# --------------------------------------------------------------------------- #

def _is_empty(value) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == '')


def _append_comment(existing, addition: str) -> str:
    """Допиши у нов ред, никад не гази постојеће."""
    if _is_empty(existing):
        return addition
    return f'{existing.rstrip()}\n{addition}'


def _is_clean_small_count(value) -> bool:
    """Физички потврђен, чист мали број (1–99) — не сме се дирати."""
    return isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= 99


def plan_cleanup(mineral_rows: List[Dict], book_map: Dict[int, str],
                 *, only_dates: bool = False) -> Dict:
    """Чиста анализа. `mineral_rows`: id, number (норм. int), quantity, comments,
    acquisition_date. `book_map`: норм. број → оригинал количине.

    `only_dates=True` (опрезни блок): примени САМО правило датума; све остало иде
    у ручни преглед, непромењено. У оба режима физички потврђен мали чист број
    (1–99) се НЕ ДИРА (заштита стварне количине од датума у књизи).

    Враћа: changes (за примену), clean (нетакнути мали бројеви), review (ручни
    преглед), и сажетак. Никад не мења улаз.
    """
    changes: List[Dict] = []
    review: List[Dict] = []
    clean: List[Dict] = []
    rule_counts: Dict[str, int] = {}

    for mr in mineral_rows:
        num = mr.get('number')
        old_qty = mr.get('quantity')

        # Заштита: физички потврђен мали чист број се не дира ни у ком режиму.
        if _is_clean_small_count(old_qty):
            clean.append({'number': num, 'old_quantity': old_qty,
                          'original': book_map.get(num)})
            continue

        original = book_map.get(num)
        if original is None:
            review.append({'number': num, 'reason': 'нема извора у књизи',
                           'original': None, 'old_quantity': old_qty})
            continue

        info = classify_quantity(original)
        action = info['action']

        if only_dates and action != 'date':
            review.append({'number': num, 'reason': f'ван правила датума ({info["rule"]})',
                           'original': original, 'old_quantity': old_qty})
            continue

        if action == 'skip':
            continue
        if action == 'review':
            review.append({'number': num, 'reason': info['rule'],
                           'original': original, 'old_quantity': old_qty})
            continue

        new_qty = info['quantity']
        comment_add = info['comment_add']
        new_date = None
        date_assumption = None

        if action == 'date':
            new_date = info['date_iso']
            date_assumption = info.get('date_assumption')
            existing_date = mr.get('acquisition_date')
            if not _is_empty(existing_date):
                existing_iso = (existing_date.isoformat()
                                if hasattr(existing_date, 'isoformat')
                                else str(existing_date))
                if existing_iso != new_date:
                    review.append({
                        'number': num, 'reason': 'датум конфликт (acquisition_date попуњен)',
                        'original': original, 'old_quantity': mr.get('quantity'),
                        'existing_date': existing_iso, 'book_date': new_date})
                    continue
                # Исти датум већ уписан → не дирамо датум, само чистимо количину.
                new_date = None

        # Нема стварне промене (количина иста, ништа за датум/коментар) → прескочи.
        nothing_changes = (
            new_qty == old_qty and new_date is None and comment_add == ''
        )
        if action == 'set' and nothing_changes:
            continue

        change = {
            'id': mr.get('id'), 'number': num, 'original': original,
            'rule': info['rule'], 'old_quantity': old_qty, 'new_quantity': new_qty,
            'set_null': action in ('null', 'date'), 'comment_add': comment_add,
            'new_date': new_date, 'date_assumption': date_assumption,
        }
        changes.append(change)
        rule_counts[info['rule']] = rule_counts.get(info['rule'], 0) + 1

    return {
        'changes': changes,
        'clean': clean,
        'review': review,
        'summary': {
            'changes_total': len(changes),
            'clean_total': len(clean),
            'review_total': len(review),
            'rule_counts': rule_counts,
        },
    }


# --------------------------------------------------------------------------- #
# Слој базе — танак омотач око чистог језгра.
# --------------------------------------------------------------------------- #

def _norm_number(value) -> Optional[int]:
    if value is None:
        return None
    digits = ''.join(ch for ch in str(value) if ch.isdigit())
    if not digits:
        return None
    n = int(digits)
    return n if n > 0 else None


def load_book_map(conn) -> Dict[int, str]:
    """Норм. инв. број (1..3572) → оригинал количине из штампане књиге.

    Ако исти број има више различитих непразних текстова → изостави га (biће
    пријављен као „нема једнозначног извора“ кроз недостатак у мапи).
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT inventory_number, quantity FROM inventory_entries
            WHERE quantity IS NOT NULL AND btrim(quantity) <> ''
        """)
        rows = cur.fetchall()
    by_num: Dict[int, set] = {}
    for inv, qty in rows:
        n = _norm_number(inv)
        if n is None or not (1 <= n <= PRINTED_BOOK_MAX):
            continue
        by_num.setdefault(n, set()).add(qty.strip())
    return {n: next(iter(texts)) for n, texts in by_num.items() if len(texts) == 1}


def load_mineral_rows(conn, od: int = 1, do: int = PRINTED_BOOK_MAX) -> List[Dict]:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, inventory_number, quantity, comments, acquisition_date
            FROM minerals
        """)
        cols = [d[0] for d in cur.description]
        out = []
        for row in cur.fetchall():
            r = dict(zip(cols, row))
            n = _norm_number(r['inventory_number'])
            if n is None or not (od <= n <= do):
                continue
            r['number'] = n
            out.append(r)
    out.sort(key=lambda r: r['number'])
    return out


def apply_cleanup(conn, plan: Dict) -> int:
    """УПИС промена у једној трансакцији. Враћа број измењених редова."""
    applied = 0
    now = datetime.now(timezone.utc)
    with conn.cursor() as cur:
        for ch in plan['changes']:
            sets = []
            params: Dict = {'id': ch['id'], 'now': now}
            if ch['set_null']:
                sets.append('quantity = NULL')
            else:
                sets.append('quantity = %(q)s')
                params['q'] = ch['new_quantity']
            if ch['new_date'] is not None:
                sets.append('acquisition_date = %(d)s')
                params['d'] = ch['new_date']
            if ch['comment_add']:
                # Допиши у нов ред на серверу — не гази постојеће.
                sets.append(
                    "comments = CASE WHEN comments IS NULL OR btrim(comments) = '' "
                    "THEN %(c)s ELSE comments || E'\\n' || %(c)s END")
                params['c'] = ch['comment_add']
            sets.append('updated_at = %(now)s')
            cur.execute(f"UPDATE minerals SET {', '.join(sets)} WHERE id = %(id)s",
                        params)
            applied += cur.rowcount
    conn.commit()
    return applied


_RULE_LABELS = {
    'zbir': 'N+1 збир', 'broj_plus_tekst': 'број + напомена',
    'datum': 'датум → acquisition_date', 'rimski': 'римски број',
    'ima_x_ne_y': '„ima X a ne Y“', 'tekst': 'чист текст → NULL',
    'cist_broj': 'чист број 1–99',
}


def _fmt(value) -> str:
    return '∅' if value is None else str(value)


def _print_report(plan: Dict, od: int, do: int, only_dates: bool, *, executed: bool):
    s = plan['summary']
    print(f"\n===== ЧИШЋЕЊЕ КОЛИЧИНА (minerals.quantity, опсег {od}–{do}) =====")
    print(f"Режим: {'ИЗВРШЕНО (--execute)' if executed else 'DRY-RUN (без измена)'}"
          f"   Правила: {'САМО датум' if only_dates else 'сва (1–7)'}")
    print(f"Промена: {s['changes_total']}   Нетакнуто (чист број 1–99): "
          f"{s['clean_total']}   За ручни преглед: {s['review_total']}\n")

    if plan['changes']:
        print(f"  {'инв':>5} | {'оригинал из књиге':30} | {'стара':>6} | "
              f"{'нови acquisition_date':22} | додато у comments")
        print("  " + "─" * 96)
        for ch in sorted(plan['changes'], key=lambda c: c['number']):
            date_col = ch['new_date'] or ''
            if ch['date_assumption']:
                date_col += ' (претпост.)'
            new_q = 'NULL' if ch['set_null'] else _fmt(ch['new_quantity'])
            cadd = (ch['comment_add'][:44] + '…') if len(ch['comment_add']) > 45 else ch['comment_add']
            print(f"  {ch['number']:>5} | {ch['original'][:30]:30} | "
                  f"{_fmt(ch['old_quantity']):>6} | {date_col:22} | {cadd}")
            if not ch['set_null']:
                print(f"        └ нова количина: {new_q}")
        print()

    if plan['clean']:
        print(f"── НЕТАКНУТО — физички потврђен чист број 1–99 ({len(plan['clean'])}) " + "─" * 12)
        for r in sorted(plan['clean'], key=lambda c: c['number']):
            print(f"   инв {r['number']:>5} | количина {r['old_quantity']} остаје | "
                  f"књига: {_fmt(r.get('original'))}")
        print()

    if plan['review']:
        print(f"── ЗА РУЧНИ ПРЕГЛЕД — непромењено ({len(plan['review'])}) " + "─" * 18)
        for r in sorted(plan['review'], key=lambda c: c['number']):
            extra = ''
            if r.get('existing_date'):
                extra = f" | acq={r['existing_date']} vs књига={r['book_date']}"
            print(f"   инв {r['number']:>5} | {r['reason']:38} | "
                  f"књига: {_fmt(r.get('original'))} | стара количина: {_fmt(r['old_quantity'])}{extra}")
        print()
    print("=" * 60 + "\n")


def register_cli(app):
    import click

    @app.cli.command('ocisti-kolicine')
    @click.option('--od', type=int, default=3544, show_default=True,
                  help='Доња граница инв. броја (укључиво).')
    @click.option('--do', 'do_', type=int, default=3568, show_default=True,
                  help='Горња граница инв. броја (укључиво).')
    @click.option('--sva-pravila', is_flag=True, default=False,
                  help='Примени сва правила (1–7). Подразумевано: САМО датум '
                       '(опрезни блок 3544–3568).')
    @click.option('--execute', is_flag=True, default=False,
                  help='Изврши упис (подразумевано је dry-run).')
    def ocisti_kolicine(od, do_, sva_pravila, execute):
        """Очисти minerals.quantity читајући оригинал из инвентарске књиге."""
        only_dates = not sva_pravila
        from postgres_service import get_postgres_connection
        with get_postgres_connection() as conn:
            book_map = load_book_map(conn)
            mineral_rows = load_mineral_rows(conn, od, do_)
            plan = plan_cleanup(mineral_rows, book_map, only_dates=only_dates)

            if not execute:
                _print_report(plan, od, do_, only_dates, executed=False)
                click.echo("DRY-RUN: ништа није промењено. За упис: "
                           f"flask ocisti-kolicine --od {od} --do {do_} --execute")
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
            applied = apply_cleanup(conn, plan)
            _print_report(plan, od, do_, only_dates, executed=True)
            click.echo(f"ИЗВРШЕНО: измењено {applied} редова. "
                       f"За ручни преглед остаје {plan['summary']['review_total']}.")
