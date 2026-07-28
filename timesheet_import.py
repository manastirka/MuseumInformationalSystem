"""Увоз радних листа из Word-а у timesheet модул.

Два тока:
  * ТЕКУЋА листа  → као ручни унос: сачувај + пошаљи у ланац одобравања (SUBMITTED).
  * АРХИВСКА листа → као већ одобрена (историја је прошла процедуру): упис директно
    у APPROVED/locked/verified, уз ознаку imported_from='word-arhiva'.

Мапирање имена из документа на корисника је FUZZY и враћа кандидате за потврду —
никад тихо не бира погрешног.
"""

import difflib
import unicodedata

from postgres_service import get_postgres_connection
from timesheet_postgres import save_timesheet_to_postgres, submit_timesheet


# Канонски код категорије → колона у timesheet_report_days.
_CODE_TO_DB = {
    'rad_na_mestu': 'work_in_museum',
    'van_muzeja': 'work_outside',
    'godisnji_odmor': 'vacation',
    'drzavni_praznik': 'public_holiday',
    'placeno_odsustvo': 'paid_leave',
    'ostalo_odsustvo': 'other_leave',
    'bolovanje_manje_30': 'sick_leave_lt30',
    'bolovanje_vece_30': 'sick_leave_gte30',
}
_DB_ORDER = ['work_in_museum', 'work_outside', 'vacation', 'public_holiday',
            'paid_leave', 'other_leave', 'sick_leave_lt30', 'sick_leave_gte30']

_TITLES = ('др', 'dr', 'мр', 'mr', 'проф', 'prof', 'msc', 'мсц', 'phd')


# ---------------------------------------------------------------------------
# Мапирање имена → корисник (fuzzy, са кандидатима)
# ---------------------------------------------------------------------------
def _norm_name(name):
    s = unicodedata.normalize('NFKD', str(name or ''))
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    toks = [t for t in _split_tokens(s) if t and t not in _TITLES]
    return ' '.join(sorted(toks))


def _split_tokens(s):
    out, cur = [], ''
    for ch in s:
        if ch.isalpha():
            cur += ch
        elif cur:
            out.append(cur)
            cur = ''
    if cur:
        out.append(cur)
    return out


def _candidates(cur):
    """(email, display_name) активних корисника из users + employee_profiles."""
    rows = {}
    cur.execute('SELECT email, full_name FROM users WHERE is_active = TRUE')
    for email, full_name in cur.fetchall():
        if email and full_name:
            rows[str(email).lower()] = full_name
    try:
        cur.execute('SELECT email, full_name, name_cyrillic FROM employee_profiles')
        for email, full_name, name_cyr in cur.fetchall():
            if email and email.lower() not in rows and (full_name or name_cyr):
                rows[str(email).lower()] = full_name or name_cyr
    except Exception:
        pass
    return [(e, n) for e, n in rows.items()]


def match_employee(cur, name, threshold=0.82):
    """Врати {'email','full_name','score','confident', 'candidates':[...]}.

    confident=True кад је најбоље поклапање изнад прага и јасно испред другог.
    candidates су top предлози за ручну потврду.
    """
    target = _norm_name(name)
    scored = []
    for email, full_name in _candidates(cur):
        score = difflib.SequenceMatcher(None, target, _norm_name(full_name)).ratio()
        scored.append((score, email, full_name))
    scored.sort(reverse=True)
    top = scored[:5]
    best = top[0] if top else (0.0, None, None)
    second = top[1][0] if len(top) > 1 else 0.0
    confident = best[0] >= threshold and (best[0] - second) >= 0.05
    return {
        'email': best[1] if best[0] >= threshold else None,
        'full_name': best[2] if best[0] >= threshold else None,
        'score': round(best[0], 3),
        'confident': confident,
        'candidates': [{'email': e, 'full_name': n, 'score': round(s, 3)}
                       for s, e, n in top if s > 0.4],
    }


# ---------------------------------------------------------------------------
# Ток 1: ТЕКУЋА листа → као ручни унос (SUBMITTED)
# ---------------------------------------------------------------------------
def import_current(user_email, user_name, parsed):
    """Сачувај као радну листу корисника и пошаљи у ланац одобравања.
    Враћа (ok: bool, message: str, report_id|None)."""
    res = save_timesheet_to_postgres(
        user_email=user_email,
        user_name=user_name or parsed.get('employee_name'),
        month=parsed['month'],
        year=parsed['year'],
        daily_data=parsed['daily_data'],
        work_description=parsed.get('work_description') or '',
        organization_unit=parsed.get('organization_unit') or '',
        position=parsed.get('position') or '',
    )
    if not res.success:
        # TimesheetResult нема .message — порука је у .error.message.
        return False, (res.error.message if res.error else 'Грешка при чувању'), None
    report_id = res.data.get('report_id')
    _mark_imported(report_id, 'word-tekuca')
    sub = submit_timesheet(report_id, user_email)
    if not sub.success:
        # Сачувано као DRAFT, али слање у ланац није успело (нпр. рок).
        sub_msg = sub.error.message if sub.error else 'непознат разлог'
        return True, f'Увезено као нацрт; слање није успело: {sub_msg}', report_id
    return True, 'Увезено и послато на одобравање.', report_id


def _mark_imported(report_id, source):
    with get_postgres_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE timesheet_reports SET imported_from=%s, imported_at=NOW() WHERE id=%s",
            (source, report_id),
        )
        conn.commit()


# ---------------------------------------------------------------------------
# Ток 2: АРХИВСКА листа → посебна класификација status='ARHIVA'
# ---------------------------------------------------------------------------
def import_archive(parsed, employee_email, employee_name, admin_email):
    """Упис архивске листе са посебном класификацијом status='ARHIVA'.

    Архива НИЈЕ званично одобрен извештај — не улази у листу/статистику
    одобрених, приказује се неутрално („Архива"). Заобилази прозор за унос
    (историја), али не производи APPROVED ни за један месец.

    Идемпотентно по (email|name, month, year): ажурира се САМО постојећи
    архивски ред. Ако за тај месец већ постоји ручно унета/редовна листа (нпр.
    DRAFT/SUBMITTED/APPROVED из редовног тока), архивски увоз се ОДБИЈА да не би
    преписао стварне податке.
    Враћа (ok, message, report_id)."""
    month, year = parsed['month'], parsed['year']
    name = employee_name or parsed.get('employee_name')
    with get_postgres_connection() as conn, conn.cursor() as cur:
        report_id = _find_report(cur, employee_email, name, month, year)
        if report_id is not None:
            # Не преписуј постојећу НЕ-архивску листу (редован ток).
            cur.execute(
                "SELECT COALESCE(imported_from, '') AS imported_from "
                "FROM timesheet_reports WHERE id=%s", (report_id,))
            row = cur.fetchone()
            existing_source = row[0] if row else ''
            if existing_source != 'word-arhiva':
                return (False,
                        'За овај месец већ постоји редовна (не-архивска) радна '
                        'листа — архивски увоз је одбијен да не би преписао '
                        'постојеће податке.',
                        None)
        if report_id is None:
            cur.execute(
                """
                INSERT INTO timesheet_reports
                    (employee_email, employee_name, month, year, organization_unit,
                     position, special_tasks, version)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
                RETURNING id
                """,
                (employee_email, name, month, year,
                 parsed.get('organization_unit') or '', parsed.get('position') or '',
                 parsed.get('work_description') or ''),
            )
            report_id = cur.fetchone()[0]
        else:
            cur.execute(
                """
                UPDATE timesheet_reports SET
                    employee_email=COALESCE(%s, employee_email),
                    organization_unit=%s, position=%s, special_tasks=%s, updated_at=NOW()
                WHERE id=%s
                """,
                (employee_email, parsed.get('organization_unit') or '',
                 parsed.get('position') or '', parsed.get('work_description') or '',
                 report_id),
            )
        _write_days(cur, report_id, parsed['daily_data'])
        cur.execute(
            """
            UPDATE timesheet_reports SET
                status='ARHIVA', is_locked=TRUE, is_verified=FALSE,
                verified_by=NULL, verified_at=NULL, verified_role='arhiva',
                reviewed_at=NOW(), reviewed_by_email=%s, editable_until=NULL,
                imported_from='word-arhiva', imported_at=NOW(), updated_at=NOW()
            WHERE id=%s
            """,
            (admin_email, report_id),
        )
        conn.commit()
    return True, 'Уписано као архивска листа (није званично одобрена).', report_id


def _find_report(cur, email, name, month, year):
    if email:
        cur.execute(
            "SELECT id FROM timesheet_reports WHERE LOWER(employee_email)=LOWER(%s) "
            "AND month=%s AND year=%s LIMIT 1",
            (email, month, year),
        )
        row = cur.fetchone()
        if row:
            return row[0]
    cur.execute(
        "SELECT id FROM timesheet_reports WHERE employee_email IS NULL "
        "AND employee_name=%s AND month=%s AND year=%s LIMIT 1",
        (name, month, year),
    )
    row = cur.fetchone()
    return row[0] if row else None


def _write_days(cur, report_id, daily_data):
    cur.execute("DELETE FROM timesheet_report_days WHERE report_id=%s", (report_id,))
    for day_str, rec in daily_data.items():
        vals = {col: 0.0 for col in _DB_ORDER}
        for code, hours in rec.items():
            col = _CODE_TO_DB.get(code)
            if col:
                vals[col] += float(hours or 0)
        if sum(vals.values()) <= 0:
            continue
        cur.execute(
            f"""
            INSERT INTO timesheet_report_days
                (report_id, day, {', '.join(_DB_ORDER)})
            VALUES (%s, %s, {', '.join(['%s'] * len(_DB_ORDER))})
            """,
            [report_id, int(day_str)] + [vals[c] for c in _DB_ORDER],
        )
