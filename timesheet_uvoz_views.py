"""Увоз радних листа из Word-а — view хендлери (ИСКЉУЧИВО админ функција).

Обе токове покреће искључиво администрација, са једне обједињене странице:
  * Појединачни: једна .docx → ПРЕГЛЕД парсираног + избор запосленог за кога
    се уводи → потврда → import_current (SUBMITTED, у ланац одобравања).
  * Архивски: више .docx → dry-run извештај (поклапања/упозорења/одбијања) →
    потврда → import_archive (APPROVED, архива).

Парсирани подаци се чувају у сесији између прегледа и потврде (JSON).
"""

import io
import json

from flask import (flash, redirect, render_template, request, session, url_for)

from postgres_service import get_postgres_connection
import radna_lista_word_parser as parser
import timesheet_import as tsimport

_SESSION_KEY_TEKUCA = 'uvoz_radne_tekuca'
_SESSION_KEY_ARHIVA = 'uvoz_radne_arhiva'


def _is_word(filename):
    # Мек филтер по екстензији; ПРАВА одлука о формату је по magic бајтовима
    # у парсеру (људи преименују фајлове).
    return (filename or '').lower().endswith(('.doc', '.docx'))


def _parse_upload(file_storage):
    """Парсирај један отпремљени .docx из меморије. Диже RadnaListaParseError."""
    data = file_storage.read()
    return parser.parse_radna_lista(io.BytesIO(data))


# ---------------------------------------------------------------------------
# Обједињена админ страница увоза
# ---------------------------------------------------------------------------
def render_uvoz_hub():
    return render_template('admin_timesheet_uvoz.html')


# ---------------------------------------------------------------------------
# Појединачни увоз (текућа листа) — админ бира запосленог
# ---------------------------------------------------------------------------
def handle_uvoz_pregled():
    f = request.files.get('docx')
    if f is None or not _is_word(f.filename):
        flash('Изаберите .doc или .docx датотеку радне листе.', 'warning')
        return redirect(url_for('timesheet.uvoz_radne'))
    try:
        parsed = _parse_upload(f)
    except parser.RadnaListaParseError as exc:
        flash(f'Датотека није препозната као радна листа: {exc}', 'danger')
        return redirect(url_for('timesheet.uvoz_radne'))

    # Админ уводи туђе листе: име из документа се мапира на запосленог, а избор
    # се потврђује ручно пре уписа (никад тихо не бирамо погрешног).
    with get_postgres_connection() as conn, conn.cursor() as cur:
        match = tsimport.match_employee(cur, parsed.get('employee_name'))
    session[_SESSION_KEY_TEKUCA] = json.dumps({'parsed': parsed, 'match': match})
    return render_template('timesheet_uvoz_pregled.html', parsed=parsed, match=match)


def handle_uvoz_potvrdi():
    raw = session.pop(_SESSION_KEY_TEKUCA, None)
    if not raw:
        flash('Нема података за увоз — поновите отпремање.', 'warning')
        return redirect(url_for('timesheet.uvoz_radne'))
    data = json.loads(raw)
    parsed = data.get('parsed') or {}
    match = data.get('match') or {}
    email = (request.form.get('employee_email') or match.get('email') or '').strip() or None
    if not email:
        flash('Изаберите запосленог за кога се радна листа увози.', 'warning')
        return redirect(url_for('timesheet.uvoz_radne'))
    name = _name_for_email(email, match) or parsed.get('employee_name')
    ok, msg, _rid = tsimport.import_current(email, name, parsed)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('timesheet.uvoz_radne'))


# ---------------------------------------------------------------------------
# Архивски масовни увоз
# ---------------------------------------------------------------------------
def handle_uvoz_arhiva_pregled():
    files = [f for f in request.files.getlist('docx')
             if f and (f.filename or '').strip()]
    if not files:
        flash('Изаберите једну или више .docx датотека.', 'warning')
        return redirect(url_for('timesheet.uvoz_radne'))

    stavke = []
    with get_postgres_connection() as conn, conn.cursor() as cur:
        for f in files:
            if not _is_word(f.filename):
                stavke.append({'filename': f.filename, 'ok': False,
                               'razlog': 'није .doc ни .docx датотека'})
                continue
            try:
                parsed = _parse_upload(f)
            except parser.RadnaListaParseError as exc:
                stavke.append({'filename': f.filename, 'ok': False, 'razlog': str(exc)})
                continue
            m = tsimport.match_employee(cur, parsed.get('employee_name'))
            stavke.append({
                'filename': f.filename, 'ok': True, 'parsed': parsed,
                'employee_name': parsed.get('employee_name'),
                'mesec': parsed['month'], 'godina': parsed['year'],
                'radni': parsed['totals']['radni'], 'sve': parsed['totals']['sve'],
                'match': m, 'warnings': parsed.get('warnings', []),
            })
    # Чувамо parsed + предложени email за потврду.
    session[_SESSION_KEY_ARHIVA] = json.dumps([
        {'parsed': s['parsed'], 'email': (s['match'].get('email') if s['ok'] else None),
         'name': s['employee_name'] if s['ok'] else None}
        for s in stavke if s['ok']
    ])
    br_ok = sum(1 for s in stavke if s['ok'])
    return render_template('timesheet_uvoz_arhiva_pregled.html', stavke=stavke,
                           br_ok=br_ok, br_odbijeno=len(stavke) - br_ok)


def handle_uvoz_arhiva_potvrdi():
    raw = session.pop(_SESSION_KEY_ARHIVA, None)
    if not raw:
        flash('Нема података за увоз — поновите отпремање.', 'warning')
        return redirect(url_for('timesheet.uvoz_radne'))
    payload = json.loads(raw)
    # Админ може поименично да изабере/потврди email по ставци (form: email_<i>).
    admin_email = session.get('user_email')
    uvezeno, preskoceno = 0, 0
    for i, item in enumerate(payload):
        email = (request.form.get(f'email_{i}') or item.get('email') or '').strip() or None
        if not email:
            preskoceno += 1
            continue
        ok, _msg, _rid = tsimport.import_archive(
            item['parsed'], email, item.get('name'), admin_email)
        if ok:
            uvezeno += 1
        else:
            preskoceno += 1
    flash(f'Архивски увоз: уписано {uvezeno}, прескочено {preskoceno} '
          f'(без поклопљеног запосленог).', 'success' if uvezeno else 'warning')
    return redirect(url_for('timesheet.uvoz_radne'))


# ---------------------------------------------------------------------------
def _name_for_email(email, match):
    """Пуно име за изабрани email из мапирања (кандидати из прегледа)."""
    target = (email or '').lower()
    for c in (match.get('candidates') or []):
        if (c.get('email') or '').lower() == target:
            return c.get('full_name')
    if (match.get('email') or '').lower() == target:
        return match.get('full_name')
    return None
