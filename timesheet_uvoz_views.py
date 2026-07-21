"""Увоз радних листа из Word-а — view хендлери (ток запосленог + админ архива).

Токови:
  * Запослени: једна .docx → ПРЕГЛЕД парсираног → потврда → import_current
    (SUBMITTED, у ланац одобравања).
  * Админ: више .docx → dry-run извештај (поклапања/упозорења/одбијања) →
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
# Ток запосленог — текућа листа
# ---------------------------------------------------------------------------
def render_uvoz_form():
    return render_template('timesheet_uvoz.html')


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

    # Упозори ако име из документа не личи на пријављеног корисника (можда туђа
    # датотека) — али увоз иде као текућа листа ПРИЈАВЉЕНОГ корисника.
    session_name = session.get('user_name') or ''
    name_ok = _slican(parsed.get('employee_name'), session_name)
    session[_SESSION_KEY_TEKUCA] = json.dumps(parsed)
    return render_template('timesheet_uvoz_pregled.html', parsed=parsed,
                           name_ok=name_ok, session_name=session_name)


def handle_uvoz_potvrdi():
    raw = session.pop(_SESSION_KEY_TEKUCA, None)
    if not raw:
        flash('Нема података за увоз — поновите отпремање.', 'warning')
        return redirect(url_for('timesheet.uvoz_radne'))
    parsed = json.loads(raw)
    user_email = session.get('user_email')
    user_name = session.get('user_name')
    ok, msg, _rid = tsimport.import_current(user_email, user_name, parsed)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('timesheet.timesheet_entry'))


# ---------------------------------------------------------------------------
# Ток админа — архивски масовни увоз
# ---------------------------------------------------------------------------
def render_uvoz_arhiva_form():
    return render_template('timesheet_uvoz_arhiva.html')


def handle_uvoz_arhiva_pregled():
    files = [f for f in request.files.getlist('docx')
             if f and (f.filename or '').strip()]
    if not files:
        flash('Изаберите једну или више .docx датотека.', 'warning')
        return redirect(url_for('timesheet.uvoz_arhiva'))

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
        return redirect(url_for('timesheet.uvoz_arhiva'))
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
    return redirect(url_for('timesheet.uvoz_arhiva'))


# ---------------------------------------------------------------------------
def _slican(a, b):
    """Груба провера да два имена личе (за упозорење о туђој датотеци)."""
    import difflib
    na = tsimport._norm_name(a)
    nb = tsimport._norm_name(b)
    if not na or not nb:
        return True  # без поређења не дижемо лажну узбуну
    return difflib.SequenceMatcher(None, na, nb).ratio() >= 0.7
