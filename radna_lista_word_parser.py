"""Парсер радне листе из Word (.docx) документа.

Flask-free и без базе — само python-docx + чиста логика, да га тестови и увозни
токови зову директно. Толерантан на варијације:
  * оријентација матрице присуства: дани као РЕДОВИ × категорије као КОЛОНЕ
    (изворни/апп формат) ИЛИ категорије као редови × дани као колоне;
  * ћирилица/латиница у ознакама категорија и месецима;
  * заглавље у пасусима ИЛИ у табели.

Никад тихо не погађа: ако не разуме документ (нема запосленог, месеца/године,
или матрице) диже `RadnaListaParseError` са јасним разлогом; мање недоумице
скупља у `warnings`.
"""

import re
import unicodedata
from datetime import date


class RadnaListaParseError(Exception):
    """Документ се не може поуздано рашчланити (порука објашњава зашто)."""


# Канонски кодови категорија (исти као timesheet_report_days / frontend).
CATEGORY_CODES = [
    'rad_na_mestu', 'van_muzeja', 'godisnji_odmor', 'drzavni_praznik',
    'placeno_odsustvo', 'ostalo_odsustvo', 'bolovanje_manje_30', 'bolovanje_vece_30',
]
# Категорије где ненумерички текст у ћелији (нпр. име празника) значи цео дан.
_FULL_DAY_CATEGORIES = {
    'godisnji_odmor', 'drzavni_praznik', 'placeno_odsustvo',
    'ostalo_odsustvo', 'bolovanje_manje_30', 'bolovanje_vece_30',
}
_STANDARD_DAY_HOURS = 8.0

# Месеци: ћир + лат, номинатив/локатив основе → број.
_MONTHS = {
    1: ('јануар', 'januar'), 2: ('фебруар', 'februar'), 3: ('март', 'mart'),
    4: ('април', 'april'), 5: ('мај', 'maj'), 6: ('јун', 'jun'),
    7: ('јул', 'jul'), 8: ('август', 'avgust', 'аугуст'), 9: ('септембар', 'septembar'),
    10: ('октобар', 'oktobar'), 11: ('новембар', 'novembar'), 12: ('децембар', 'decembar'),
}


def _norm(s):
    """Мала слова + сажети размаци + фолдовање латиничних дијакритика
    (č→c, ž→z, š→s, ć→c, đ→d) преко NFKD. Ћирилица остаје нетакнута (српска
    ћирилична слова немају канонску декомпозицију), па „плаћено" (ћир) и
    „plaćeno" (лат) оба падну на исте кључне речи."""
    s = unicodedata.normalize('NFKD', str(s or ''))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', s.strip().lower())


def _match_category(label):
    """Ознаку колоне/реда мапирај на канонски код категорије или None."""
    t = _norm(label)
    if not t:
        return None
    has = lambda *ks: any(k in t for k in ks)
    if has('боловањ', 'bolovanj'):
        if has('>30', '> 30', 'веће', 'vece', 'више', 'vise', 'преко', 'preko', 'дуже', 'duze'):
            return 'bolovanje_vece_30'
        if has('<30', '< 30', 'мање', 'manje', 'до 30', 'do 30', 'краће', 'krace'):
            return 'bolovanje_manje_30'
        return 'bolovanje_manje_30'  # неозначено боловање → до 30
    if has('годишњ', 'godisnj') or (has('одмор', 'odmor') and not has('плаћен')):
        return 'godisnji_odmor'
    if has('државн', 'drzavn', 'празник', 'praznik'):
        return 'drzavni_praznik'
    if has('плаћен', 'placen'):
        return 'placeno_odsustvo'
    if has('остал', 'ostal'):
        return 'ostalo_odsustvo'
    if has('ван муз', 'van muz') or (has('ван', 'van') and has('муз', 'muz')):
        return 'van_muzeja'
    if has('рад') or has('rad') or has('у музеј', 'u muzej', 'на месту', 'na mestu'):
        return 'rad_na_mestu'
    return None


def _as_int_day(text):
    t = _norm(text)
    m = re.fullmatch(r'(\d{1,2})\.?', t)
    if m:
        d = int(m.group(1))
        return d if 1 <= d <= 31 else None
    return None


def _is_total_label(text):
    return any(k in _norm(text) for k in ('укупно', 'ukupno', 'збир', 'zbir', 'σ'))


def _cell_hours(text, category):
    """Сати из ћелије: број → сати; X/Х → 0 (викенд/нерадно); ненумерички текст
    у категорији одсуства → цео дан (8); иначе 0."""
    t = (text or '').strip()
    if not t or t.upper() in ('X', 'Х', '/', '-', '—'):
        return 0.0
    m = re.search(r'(\d+(?:[.,]\d+)?)', t)
    if m:
        try:
            return float(m.group(1).replace(',', '.'))
        except ValueError:
            return 0.0
    if category in _FULL_DAY_CATEGORIES:
        return _STANDARD_DAY_HOURS
    return 0.0


# ---------------------------------------------------------------------------
# Заглавље
# ---------------------------------------------------------------------------
def _collect_label_values(doc):
    """Скупи „ознака: вредност" парове из пасуса И ћелија табела."""
    pairs = []
    texts = [p.text for p in doc.paragraphs]
    for t in doc.tables:
        for row in t.rows:
            for c in row.cells:
                texts.append(c.text)
    for raw in texts:
        for line in str(raw).split('\n'):
            if ':' in line:
                k, _, v = line.partition(':')
                pairs.append((_norm(k), v.strip()))
    return pairs, texts


def _extract_header(doc):
    pairs, texts = _collect_label_values(doc)

    def find(*keys):
        for k, v in pairs:
            if any(key in k for key in keys) and v:
                return v.strip()
        return None

    name = find('име и презиме', 'ime i prezime', 'запослени', 'zaposleni')
    org = find('организацион', 'organizacion', 'одељењ', 'odeljen', 'јединиц', 'jedinic')
    position = find('радно место', 'radno mesto')

    month, year = _extract_month_year(pairs, texts)
    return {
        'employee_name': _clean_name(name),
        'organization_unit': org or None,
        'position': position or None,
        'month': month,
        'year': year,
    }


def _clean_name(name):
    if not name:
        return None
    # скини титуле/суфиксе типа „Др ", вишеструке размаке
    n = re.sub(r'\s+', ' ', name.strip())
    return n or None


def _extract_month_year(pairs, texts):
    month = year = None
    # 1) експлицитно „Месец: 4  Година: 2015"
    for k, v in pairs:
        if 'месец' in k or 'mesec' in k or 'период' in k or 'period' in k:
            m, y = _parse_month_year_text(v)
            month = month or m
            year = year or y
        if ('година' in k or 'godina' in k) and year is None:
            ym = re.search(r'(19|20)\d{2}', v)
            if ym:
                year = int(ym.group(0))
    # 2) слободан текст „РАДНА ЛИСТА за месец август 2025" / „Август 2025"
    if month is None or year is None:
        for raw in texts:
            m, y = _parse_month_year_text(raw)
            if month is None and m:
                month = m
            if year is None and y:
                year = y
            if month and year:
                break
    return month, year


def _parse_month_year_text(text):
    t = _norm(text)
    month = None
    for num, names in _MONTHS.items():
        if any(nm in t for nm in names):
            month = num
            break
    if month is None:
        m = re.search(r'месец\D{0,4}(\d{1,2})|mesec\D{0,4}(\d{1,2})', t)
        if m:
            val = int(m.group(1) or m.group(2))
            if 1 <= val <= 12:
                month = val
    ym = re.search(r'(19|20)\d{2}', t)
    year = int(ym.group(0)) if ym else None
    return month, year


# ---------------------------------------------------------------------------
# Матрица присуства
# ---------------------------------------------------------------------------
def _table_grid(table):
    return [[c.text for c in row.cells] for row in table.rows]


def _find_matrix(doc, warnings):
    """Нађи табелу матрице и врати (grid, orientation). orientation:
    'days_rows' (дани редови × категорије колоне) или 'days_cols'."""
    best = None
    for t in doc.tables:
        grid = _table_grid(t)
        if len(grid) < 3 or len(grid[0]) < 3:
            continue
        header = grid[0]
        first_col = [r[0] for r in grid]
        cat_in_header = sum(1 for c in header if _match_category(c))
        cat_in_col = sum(1 for c in first_col if _match_category(c))
        days_in_header = sum(1 for c in header[1:] if _as_int_day(c))
        days_in_col = sum(1 for c in first_col[1:] if _as_int_day(c))
        # Праг 2 категорије: апп-извоз прати само „рад на месту" и „ван музеја"
        # у табели (одсуства су у резимеу), а изворна матрица има свих 8.
        if cat_in_header >= 2 and days_in_col >= 8:
            score = cat_in_header + days_in_col
            cand = (score, grid, 'days_rows')
        elif cat_in_col >= 2 and days_in_header >= 8:
            score = cat_in_col + days_in_header
            cand = (score, grid, 'days_cols')
        else:
            continue
        if best is None or cand[0] > best[0]:
            best = cand
    if best is None:
        return None, None
    return best[1], best[2]


def _parse_matrix(grid, orientation, warnings):
    """Врати daily_data {day: {cat: hours}} само за дане са неким сатима."""
    daily = {}
    if orientation == 'days_rows':
        header = grid[0]
        col_cat = {j: _match_category(header[j]) for j in range(1, len(header))}
        for row in grid[1:]:
            if not row or _is_total_label(row[0]):
                continue
            day = _as_int_day(row[0])
            if day is None:
                continue
            rec = {}
            for j, cat in col_cat.items():
                if cat and j < len(row):
                    h = _cell_hours(row[j], cat)
                    if h:
                        rec[cat] = rec.get(cat, 0.0) + h
            if rec:
                daily[day] = rec
    else:  # days_cols: категорије редови × дани колоне
        header = grid[0]
        col_day = {j: _as_int_day(header[j]) for j in range(1, len(header))}
        for row in grid[1:]:
            if not row:
                continue
            cat = _match_category(row[0])
            if not cat or _is_total_label(row[0]):
                continue
            for j, day in col_day.items():
                if day is None or j >= len(row):
                    continue
                h = _cell_hours(row[j], cat)
                if h:
                    daily.setdefault(day, {})
                    daily[day][cat] = daily[day].get(cat, 0.0) + h
    return daily


# ---------------------------------------------------------------------------
# Обављени послови
# ---------------------------------------------------------------------------
def _extract_work_description(doc):
    paras = [p.text for p in doc.paragraphs]
    out, grab = [], False
    for p in paras:
        norm = _norm(p)
        if not grab and ('обављени послови' in norm or 'obavljeni poslovi' in norm
                         or 'опис обављених' in norm or 'редовни послови' in norm):
            grab = True
            # прескочи сам наслов ако је чист наслов
            if norm in ('обављени послови', 'obavljeni poslovi', 'опис обављених послова'):
                continue
        if grab:
            if _norm(p) in ('потписи', 'potpisi', 'дневни уноси', 'dnevni unosi'):
                break
            if p.strip():
                out.append(p.strip())
    text = '\n'.join(out).strip()
    return text or None


# ---------------------------------------------------------------------------
# Јавни улаз
# ---------------------------------------------------------------------------
def parse_radna_lista(source):
    """Рашчлани .docx (путања или file-like). Враћа dict или диже
    RadnaListaParseError. `warnings` носи неблокирајуће напомене."""
    try:
        import docx
    except ImportError as exc:  # pragma: no cover
        raise RadnaListaParseError(f'python-docx није доступан: {exc}')
    try:
        doc = docx.Document(source)
    except Exception as exc:
        raise RadnaListaParseError(f'датотека није исправан .docx: {exc}')

    warnings = []
    header = _extract_header(doc)
    if not header['employee_name']:
        raise RadnaListaParseError('није пронађено име запосленог (нема „Име и презиме").')
    if not header['month'] or not header['year']:
        raise RadnaListaParseError('није препознат месец и/или година радне листе.')
    if not 1 <= header['month'] <= 12:
        raise RadnaListaParseError(f'нелогичан месец: {header["month"]}.')

    grid, orientation = _find_matrix(doc, warnings)
    if grid is None:
        raise RadnaListaParseError(
            'није пронађена матрица присуства (табела са категоријама и данима).')
    daily = _parse_matrix(grid, orientation, warnings)
    if not daily:
        warnings.append('матрица нема ниједан дан са унетим сатима.')

    totals = _totals(daily)
    if totals['radni'] == 0 and totals['sve'] == 0:
        warnings.append('укупан број сати је 0 — проверите документ.')

    return {
        'employee_name': header['employee_name'],
        'organization_unit': header['organization_unit'],
        'position': header['position'],
        'month': header['month'],
        'year': header['year'],
        'daily_data': {str(d): rec for d, rec in sorted(daily.items())},
        'work_description': _extract_work_description(doc),
        'totals': totals,
        'orientation': orientation,
        'warnings': warnings,
    }


def _totals(daily):
    radni = sum(rec.get('rad_na_mestu', 0) + rec.get('van_muzeja', 0)
                for rec in daily.values())
    sve = sum(sum(rec.values()) for rec in daily.values())
    per_cat = {c: 0.0 for c in CATEGORY_CODES}
    for rec in daily.values():
        for c, h in rec.items():
            per_cat[c] = per_cat.get(c, 0.0) + h
    return {'radni': radni, 'sve': sve, 'po_kategoriji': per_cat}
