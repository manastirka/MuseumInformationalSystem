#!/usr/bin/env python3
"""BAZELINI (LOCKED) регресиони пакет за модул месечних радних листа.

Овај фајл закључава потврђено-исправно стање целог ланца радних листа
(унос → чување → двостепено одобравање → враћање на допуну → админ
откључавање → увоз из Word-а → раздвајање текуће/архиве → бирач година),
онако како ради на продукцији на дан 2026-07-28.

Правило: сваки тест чува ТАЧНО ЈЕДАН решен баг. Ако неки тест овде падне,
то значи да је нека од закључаних гаранција регресирала — тест се НЕ
прилагођава, него се поправља код. Историја и упутство: docs/radne-liste-baseline.md.

Пусти цео пакет:
    SECRET_KEY=test-secret REDIS_URL='' FLASK_ENV=testing \
    SESSION_TYPE=filesystem SESSION_FILE_DIR=logs/qa_flask_session \
    RATELIMIT_STORAGE_URL=memory:// python3 -m pytest -q test_radne_liste_baseline.py

Делови који пишу у базу прескачу се без PostgreSQL-а; .doc конверзија
прескаче се без LibreOffice-а (soffice).
"""

import io
import os
import shutil
import sys
from datetime import datetime

import pytest

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', 'logs/qa_flask_session')
os.environ.setdefault('WTF_CSRF_ENABLED', 'False')

import timesheet_postgres as tp
import timesheet_employee_views as ev
import timesheet_admin_views as tav
from timesheet_repository import TimesheetRepository
import timesheet_import as ti
import radna_lista_word_parser as rl
import doc_konverzija as dk

# Фикстура-генератор радних листа (није пакет — додајемо фолдер на путању).
_FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'tests', 'fixtures', 'radne_liste')
sys.path.insert(0, _FIXTURES_DIR)
import make_fixtures as mk  # noqa: E402


# ===========================================================================
# Заједнички алат: детекција базе/soffice, чишћење, помоћне периоде
# ===========================================================================
def _pg_available():
    try:
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT 1')
                cur.fetchone()
        return True
    except Exception:
        return False


_DB = pytest.mark.skipif(not _pg_available(), reason='PostgreSQL није доступан')
_NEED_SOFFICE = pytest.mark.skipif(
    (shutil.which('soffice') or shutil.which('libreoffice')) is None,
    reason='soffice/LibreOffice није доступан')

_CURRENT_YEAR = datetime.now().year


def _months_ago(n):
    """(month, year) за месец N месеци уназад — сигурно после рока за унос."""
    now = datetime.now()
    idx = now.year * 12 + (now.month - 1) - n
    return idx % 12 + 1, idx // 12


def _delete_by_email(email):
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM timesheet_report_days WHERE report_id IN "
                "(SELECT id FROM timesheet_reports WHERE employee_email=%s)", (email,))
            cur.execute("DELETE FROM timesheet_reports WHERE employee_email=%s", (email,))
            conn.commit()


def _day_rows(report_id):
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT day, work_in_museum, work_outside, sick_leave_lt30 "
                "FROM timesheet_report_days WHERE report_id=%s ORDER BY day",
                (report_id,))
            return cur.fetchall()


def _seed_report(email, name, month, year, status='SUBMITTED',
                 imported_from=None, is_locked=None):
    if is_locked is None:
        is_locked = status in ('SUBMITTED', 'APPROVED')
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO timesheet_reports "
                "(employee_name, employee_email, month, year, status, is_locked, imported_from) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (name, email, month, year, status, is_locked, imported_from))
            rid = cur.fetchone()['id']
            conn.commit()
            return rid


def _status_row(report_id):
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COALESCE(status,'DRAFT') AS status, head_verified_by, "
                "director_verified_by, is_verified FROM timesheet_reports WHERE id=%s",
                (report_id,))
            return cur.fetchone()


# ===========================================================================
# 1) МАТРИЦА ПРИСУСТВА СЕ ЧУВА END-TO-END (до базе и назад)
#    БАГ: матрица се тихо брисала — форма уноса није учитавала дане, а save је
#    DELETE-then-reinsert па је празан re-save брисао постојеће дане уз лажни
#    „успешно сачувано". Fix: prod-2026-07-27-8 (+ guard против тихог брисања).
# ===========================================================================
_MATRIX_EMAIL = 'baseline.matrica@example.invalid'
_MATRIX_NAME = 'Базелина Матрица'


@_DB
def test_matrica_cuva_se_end_to_end_do_baze():
    """БАГ (2026-07-27-8): попуни → сачувај → тачни редови у
    timesheet_report_days → поновно отварање враћа исте вредности."""
    month, year = datetime.now().month, datetime.now().year  # текући месец = у прозору
    _delete_by_email(_MATRIX_EMAIL)
    try:
        r = tp.save_timesheet_to_postgres(
            user_email=_MATRIX_EMAIL, user_name=_MATRIX_NAME, month=month, year=year,
            daily_data={'5': {'rad_na_mestu': 8, 'van_muzeja': 2},
                        '10': {'bolovanje_manje_30': 8}},
            work_description='x', organization_unit='X', position='Y')
        assert r.success, r.error.message if r.error else r
        rid = r.data['report_id']

        # Тачне вредности у бази.
        by_day = {row['day']: row for row in _day_rows(rid)}
        assert len(by_day) == 2
        assert float(by_day[5]['work_in_museum']) == 8.0
        assert float(by_day[5]['work_outside']) == 2.0
        assert float(by_day[10]['sick_leave_lt30']) == 8.0

        # Поновно отварање (учитавач форме уноса) враћа дане за репопулацију.
        data = ev._load_timesheet_entry_data(_MATRIX_NAME, _MATRIX_EMAIL, month, year)
        assert data is not None
        days = {d['dan']: d for d in data['daily_data']}
        assert float(days[5]['rad_na_mestu']) == 8.0
        assert float(days[10]['bolovanje_manje_30']) == 8.0
    finally:
        _delete_by_email(_MATRIX_EMAIL)


@_DB
def test_matrica_prazan_resave_ne_brise_postojece():
    """БАГ (2026-07-27-8): празан re-save НЕ сме тихо да обрише већ попуњену
    листу; мора вратити VALIDATION_ERROR и оставити податке нетакнуте."""
    month, year = datetime.now().month, datetime.now().year
    _delete_by_email(_MATRIX_EMAIL)
    try:
        r = tp.save_timesheet_to_postgres(
            user_email=_MATRIX_EMAIL, user_name=_MATRIX_NAME, month=month, year=year,
            daily_data={'5': {'rad_na_mestu': 8}}, work_description='x',
            organization_unit='X', position='Y')
        rid = r.data['report_id']
        assert len(_day_rows(rid)) == 1

        wiped = tp.save_timesheet_to_postgres(
            user_email=_MATRIX_EMAIL, user_name=_MATRIX_NAME, month=month, year=year,
            daily_data={}, work_description='x', organization_unit='X', position='Y')
        assert not wiped.success, 'празан save не сме да успе тихо'
        assert wiped.error.error_type == tp.TimesheetErrorType.VALIDATION_ERROR
        assert len(_day_rows(rid)) == 1, 'подаци морају остати'
    finally:
        _delete_by_email(_MATRIX_EMAIL)


# ===========================================================================
# 2) ВРАЋЕНА ЛИСТА НА ДОПУНУ ЈЕ ИЗМЕНЉИВА ВЛАСНИКУ — И СТАРИЈА ОД ПРЕТХОДНОГ МЕСЕЦА
#    БАГ: враћена (REJECTED) листа старија од рока није могла да се допуни —
#    24h прозор (editable_until) мора да прегази календарски рок за ТАЈ извештај.
#    Fix: prod-2026-07-27 (dopuna) — save слој поштује прозор.
# ===========================================================================
_REJ_EMAIL = 'baseline.vracena@example.invalid'
_REJ_NAME = 'Базелина Враћена'


@_DB
def test_vracena_stara_lista_je_izmenljiva_vlasniku():
    """БАГ (2026-07-27): листа из месеца СТАРИЈЕГ од претходног, враћена на
    допуну, мора бити изменљива власнику (24h прозор гази рок)."""
    month, year = _months_ago(4)  # добро после рока
    _delete_by_email(_REJ_EMAIL)
    try:
        rid = _seed_report(_REJ_EMAIL, _REJ_NAME, month, year, status='SUBMITTED')

        # Пре враћања: власник не може да мења стару поднету листу.
        blocked = tp.save_timesheet_to_postgres(
            user_email=_REJ_EMAIL, user_name=_REJ_NAME, month=month, year=year,
            daily_data={'12': {'rad_na_mestu': 8}}, work_description='x',
            organization_unit='X', position='Y')
        assert not blocked.success

        # Шеф/админ враћа на допуну → отвара 24h прозор.
        rej = tp.reject_timesheet(rid, 'sef@example.invalid', 'Допуни дане 12. и 13.')
        assert rej.success
        assert _status_row(rid)['status'] == 'REJECTED'

        # Сада власник МОЖЕ да сачува иако је месец давно прошао.
        saved = tp.save_timesheet_to_postgres(
            user_email=_REJ_EMAIL, user_name=_REJ_NAME, month=month, year=year,
            daily_data={'12': {'rad_na_mestu': 8}}, work_description='допуна',
            organization_unit='X', position='Y')
        assert saved.success, saved.error.message if saved.error else saved
        assert len(_day_rows(rid)) == 1
    finally:
        _delete_by_email(_REJ_EMAIL)


# ===========================================================================
# 3) ДВОСТЕПЕНО ОДОБРЕЊЕ: ОБА ПОТПИСА (шеф + директор) → APPROVED
#    БАГ: листа је приказивана као одобрена уз само један потпис.
#    Fix: prod-2026-07-27-5 (head_verified_by / director_verified_by, migr. 034).
# ===========================================================================
_2SIG_EMAIL = 'baseline.dvostepeno@example.invalid'
_2SIG_NAME = 'Базелина Двостепени'
_HEAD = 'sef.baseline@example.invalid'
_DIRECTOR = 'direktor.baseline@example.invalid'


@_DB
def test_dvostepeno_jedan_potpis_nije_odobreno():
    """БАГ (2026-07-27-5): један потпис (само шеф) држи листу SUBMITTED —
    НИЈЕ одобрено док не потпише и директор."""
    month, year = _months_ago(2)
    _delete_by_email(_2SIG_EMAIL)
    try:
        rid = _seed_report(_2SIG_EMAIL, _2SIG_NAME, month, year, status='SUBMITTED')
        r = tp.confirm_timesheet_signature(rid, _HEAD, 'head', head_required=True)
        assert r.success and not r.data['approved']
        row = _status_row(rid)
        assert row['status'] == 'SUBMITTED'
        assert row['head_verified_by'] == _HEAD
        assert row['director_verified_by'] is None
        assert not row['is_verified']
    finally:
        _delete_by_email(_2SIG_EMAIL)


@_DB
def test_dvostepeno_oba_potpisa_odobravaju():
    """БАГ (2026-07-27-5): тек ОБА потписа (шеф + директор) → APPROVED."""
    month, year = _months_ago(2)
    _delete_by_email(_2SIG_EMAIL)
    try:
        rid = _seed_report(_2SIG_EMAIL, _2SIG_NAME, month, year, status='SUBMITTED')
        tp.confirm_timesheet_signature(rid, _HEAD, 'head', head_required=True)
        r = tp.confirm_timesheet_signature(rid, _DIRECTOR, 'director', head_required=True)
        assert r.success and r.data['approved']
        row = _status_row(rid)
        assert row['status'] == 'APPROVED'
        assert row['head_verified_by'] == _HEAD
        assert row['director_verified_by'] == _DIRECTOR
        assert row['is_verified']
    finally:
        _delete_by_email(_2SIG_EMAIL)


@_DB
def test_dvostepeno_vracanje_resetuje_oba_potpisa():
    """БАГ (2026-07-27-5): враћање на допуну ресетује ОБА потписа (нови круг
    одобравања креће од нуле)."""
    month, year = _months_ago(2)
    _delete_by_email(_2SIG_EMAIL)
    try:
        rid = _seed_report(_2SIG_EMAIL, _2SIG_NAME, month, year, status='SUBMITTED')
        tp.confirm_timesheet_signature(rid, _HEAD, 'head', head_required=True)
        rej = tp.reject_timesheet(rid, _DIRECTOR, 'Допуни дане')
        assert rej.success
        row = _status_row(rid)
        assert row['status'] == 'REJECTED'
        assert row['head_verified_by'] is None
        assert row['director_verified_by'] is None
    finally:
        _delete_by_email(_2SIG_EMAIL)


# ===========================================================================
# 4) ДИРЕКТОР ПОТВРЂУЈЕ ЛИСТЕ ИЗ СВИХ ОДЕЉЕЊА; ШЕФ САМО СВОЈЕ
#    БАГ: гејт одобравања је користио стару политику једног верификатора па је
#    директор био блокиран за регуларне запослене у одељењима са шефом.
#    Fix: 37e9262 (fix/direktor-odobravanje) — гејт делегира на sign-политику.
# ===========================================================================
_DEPT = 'Биологија-baseline'
_OTHER_DEPT = 'Геологија-baseline'


def _sess(role, email, is_head=False, dept=''):
    return {'user_role': role, 'user_email': email,
            'is_department_head': is_head, 'user_department': dept}


def test_direktor_moze_sve_odeljenje_sef_samo_svoje():
    """БАГ (37e9262): директор сме да потпише листу запосленог из БИЛО КОГ
    одељења; шеф сме само у СВОМ одељењу, не у туђем."""
    heads = {_DEPT: _HEAD}
    can_sign = tav.can_user_sign_report_for_department

    # Директор — оба одељења.
    assert can_sign(_sess('direktor', _DIRECTOR), _DEPT,
                    target_employee_email='emp@x', department_heads=heads)
    assert can_sign(_sess('direktor', _DIRECTOR), _OTHER_DEPT,
                    target_employee_email='emp@x', department_heads={_OTHER_DEPT: 'x@y'})

    # Шеф Биологије — своје да, туђе (Геологија) не.
    assert can_sign(_sess('sef_odeljenja', _HEAD, is_head=True, dept=_DEPT), _DEPT,
                    target_employee_email='emp@x', department_heads=heads)
    assert not can_sign(_sess('sef_odeljenja', _HEAD, is_head=True, dept=_DEPT),
                        _OTHER_DEPT, target_employee_email='emp@x',
                        department_heads={_OTHER_DEPT: 'drugi@y'})


def test_direktor_dobija_director_slot_za_regularnog():
    """БАГ (37e9262): за регуларног запосленог у одељењу СА шефом, директор
    добија валидан 'director' слот (стара verify-политика га је одбијала)."""
    plan = tav._signature_plan(_sess('direktor', _DIRECTOR), _DEPT, 'emp@x',
                               {_DEPT: _HEAD})
    assert plan['allowed'] and plan['slot'] == 'director'
    # Документује коренски узрок бага: стара политика је одбијала директора.
    assert not tav.can_user_verify_report_for_department(
        _sess('direktor', _DIRECTOR), _DEPT,
        target_employee_email='emp@x', department_heads={_DEPT: _HEAD})


# ===========================================================================
# 5) АДМИН ОТКЉУЧАВАЊЕ УНОСА ПО КОРИСНИКУ; НЕ-АДМИН 403; МЕХАНИЗАМ ЗАХТЕВА НЕ ПОСТОЈИ
#    БАГ/одлука: механизам „захтева за откључавање" уклоњен; откључава искључиво
#    админ/директор по кориснику/месецу (editable_until). Fix: prod-2026-07-27-4.
# ===========================================================================
_ADMIN = 'admin.baseline@example.invalid'


def _real_employee():
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT email, full_name FROM users "
                        "WHERE full_name IS NOT NULL AND email IS NOT NULL "
                        "ORDER BY id LIMIT 1")
            return cur.fetchone()


@_DB
def test_admin_otkljucava_unos_po_korisniku():
    """БАГ (2026-07-27-4): админ откључа стари месец по кориснику → тај корисник
    може да сачува и поднесе иако је рок прошао; SUBMITTED листа се не дира."""
    emp = _real_employee()
    assert emp is not None, 'база мора имати бар једног корисника'
    email, name = emp['email'], emp['full_name']
    month, year = _months_ago(4)
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM timesheet_reports WHERE employee_email=%s "
                        "AND month=%s AND year=%s", (email, month, year))
            conn.commit()
    try:
        # Пре откључавања: стари месец је блокиран.
        blocked = tp.save_timesheet_to_postgres(
            user_email=email, user_name=name, month=month, year=year,
            daily_data={'10': {'rad_na_mestu': 8}}, work_description='x',
            organization_unit='X', position='Y')
        assert not blocked.success

        res = tp.admin_unlock_entry(email, month, year, _ADMIN)
        assert res.success, res.error.message if res.error else res
        rid = res.data['report_id']

        saved = tp.save_timesheet_to_postgres(
            user_email=email, user_name=name, month=month, year=year,
            daily_data={'10': {'rad_na_mestu': 8}}, work_description='допуна',
            organization_unit='X', position='Y')
        assert saved.success
        submitted = tp.submit_timesheet(rid, email)
        assert submitted.success
        assert _status_row(rid)['status'] == 'SUBMITTED'

        # Поновно откључавање SUBMITTED листе се одбија (не дира поднету листу).
        again = tp.admin_unlock_entry(email, month, year, _ADMIN)
        assert not again.success
        assert again.error.error_type == tp.TimesheetErrorType.VALIDATION_ERROR
    finally:
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM timesheet_reports WHERE employee_email=%s "
                            "AND month=%s AND year=%s", (email, month, year))
                conn.commit()


@_DB
def test_neadmin_ne_moze_da_otkljuca_403():
    """БАГ (2026-07-27-4): не-админ на рути откључавања добија 403."""
    import app as museum_app
    museum_app.app.config['WTF_CSRF_ENABLED'] = False
    client = museum_app.app.test_client()
    with client.session_transaction() as s:
        s['user_id'] = 999
        s['user_email'] = 'zaposleni.baseline@example.invalid'
        s['user_role'] = 'employee'
        s['is_admin'] = False
    resp = client.post('/api/admin/timesheet/unlock',
                       json={'employee_email': 'x@y', 'from_month': 1, 'from_year': 2020},
                       base_url='https://localhost')
    assert resp.status_code == 403


def test_mehanizam_zahteva_za_otkljucavanje_ne_postoji():
    """ОДЛУКА (2026-07-27-4): не постоји рута којом запослени ТРАЖИ откључавање
    радне листе — откључава искључиво админ/директор."""
    import app as museum_app
    suspect = []
    for r in museum_app.app.url_map.iter_rules():
        path = str(r).lower()
        endpoint = (r.endpoint or '').lower()
        if 'timesheet' in path or 'timesheet' in endpoint:
            if any(k in path or k in endpoint
                   for k in ('edit_request', 'edit-request', 'unlock-request',
                             'request-unlock', 'zahtev-otkljuc', 'zahtev_unlock')):
                suspect.append(str(r))
    assert not suspect, f'механизам захтева за откључавање не сме постојати: {suspect}'


# ===========================================================================
# 6) УВОЗ ИЗ WORD-А: .docx (три варијанте шаблона) и .doc (magic + soffice)
#    БАГ/функција: увоз радних листа из .doc/.docx. Fix: prod-2026-07-20-8.
# ===========================================================================
def test_uvoz_docx_tri_varijante_daju_istu_matricu():
    """ФУНКЦИЈА (2026-07-20-8): три варијанте .docx шаблона — дани-редови,
    дани-колоне (транспоновано) и латиница — дају ИСТУ канонску матрицу."""
    rows = rl.parse_radna_lista(mk.build_correct_matrix_days_rows())
    cols = rl.parse_radna_lista(mk.build_transposed_days_cols())
    latin = rl.parse_radna_lista(mk.build_latin_variant())

    assert rows['orientation'] == 'days_rows'
    assert cols['orientation'] == 'days_cols'
    expected = mk.expected_daily_data()
    assert rows['daily_data'] == expected
    assert cols['daily_data'] == expected
    assert latin['daily_data'] == expected
    assert cols['totals'] == rows['totals']


def test_uvoz_detekcija_formata_po_magic_bajtovima():
    """ФУНКЦИЈА (2026-07-20-8): формат се одлучује по magic бајтовима (не
    екстензији): ZIP→docx, OLE→doc, остало→unknown са описом."""
    assert dk.detect_format(mk.build_correct_matrix_days_rows().read())[0] == 'docx'
    ole = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1' + b'\x00' * 100
    assert dk.detect_format(ole)[0] == 'doc'
    fmt, desc = dk.detect_format(b'%PDF-1.7 ...')
    assert fmt == 'unknown' and 'PDF' in desc


def test_uvoz_doc_bez_soffice_daje_jasnu_poruku(monkeypatch):
    """ФУНКЦИЈА (2026-07-20-8): кад soffice није доступан, .doc увоз пада са
    ЈАСНОМ поруком (не тихом грешком)."""
    monkeypatch.setattr(dk, '_find_soffice', lambda: None)
    ole = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1' + b'\x00' * 100
    with pytest.raises(rl.RadnaListaParseError) as ei:
        rl.parse_radna_lista(io.BytesIO(ole))
    assert 'Увоз .doc формата тренутно није могућ' in str(ei.value)


@_NEED_SOFFICE
def test_uvoz_doc_konverzija_isti_rezultat_kao_docx():
    """ФУНКЦИЈА (2026-07-20-8): стари .doc (magic OLE) се конвертује кроз
    LibreOffice и даје ИСТИ резултат као .docx."""
    import subprocess
    import tempfile
    soffice = shutil.which('soffice') or shutil.which('libreoffice')
    docx_bytes = mk.build_correct_matrix_days_rows().read()
    with tempfile.TemporaryDirectory() as t:
        src = os.path.join(t, 'x.docx')
        with open(src, 'wb') as fh:
            fh.write(docx_bytes)
        subprocess.run(
            [soffice, '--headless', f'-env:UserInstallation=file://{t}/p',
             '--convert-to', 'doc', '--outdir', t, src],
            capture_output=True, timeout=90)
        with open(os.path.join(t, 'x.doc'), 'rb') as fh:
            doc_bytes = fh.read()

    assert dk.detect_format(doc_bytes)[0] == 'doc'
    r_doc = rl.parse_radna_lista(io.BytesIO(doc_bytes))
    r_docx = rl.parse_radna_lista(io.BytesIO(docx_bytes))
    assert r_doc['daily_data'] == r_docx['daily_data']
    assert r_doc['totals'] == r_docx['totals']
    assert r_doc['employee_name'] == r_docx['employee_name']


# --- увоз је ИСКЉУЧИВО админ функција (серверска заштита, не само скривено дугме) ---
_UVOZ_GET_ROUTES = ['/admin/timesheet/uvoz', '/timesheet/uvoz', '/admin/timesheet/uvoz-arhiva']
_UVOZ_POST_ROUTES = ['/timesheet/uvoz/pregled', '/timesheet/uvoz/potvrdi',
                     '/admin/timesheet/uvoz-arhiva/pregled', '/admin/timesheet/uvoz-arhiva/potvrdi']


def _uvoz_client():
    import app as museum_app
    from unittest.mock import patch
    museum_app.app.config['TESTING'] = True
    museum_app.app.config['WTF_CSRF_ENABLED'] = False
    patcher = patch.object(museum_app.app, 'user_has_module_access', lambda *a, **k: True)
    patcher.start()
    return museum_app.app.test_client(), patcher


def _login(client, *, email, role, **extra):
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['user_email'] = email
        sess['user_name'] = 'Тест'
        sess['user_role'] = role
        sess['is_admin'] = role in ('admin', 'direktor')
        for k, v in extra.items():
            sess[k] = v


def test_uvoz_ne_admin_odbijen_na_rutama():
    """ФУНКЦИЈА (2026-07-20-8): не-админ (запослени) бива серверски одбијен на
    СВИМ рутама увоза (GET и POST), не само скривеним дугметом."""
    client, patcher = _uvoz_client()
    try:
        _login(client, email='zaposleni@example.invalid', role='employee')
        for route in _UVOZ_GET_ROUTES:
            resp = client.get(route, base_url='https://localhost')
            assert resp.status_code in (302, 303, 403), f'{route}: {resp.status_code}'
        for route in _UVOZ_POST_ROUTES:
            resp = client.post(route, data={}, base_url='https://localhost')
            assert resp.status_code in (302, 303, 403), f'{route}: {resp.status_code}'
    finally:
        patcher.stop()


def test_uvoz_admin_vidi_obedinjeni_hub():
    """ФУНКЦИЈА (2026-07-20-8): админ види обједињену страницу увоза са ОБА
    тока (појединачни + архивски)."""
    client, patcher = _uvoz_client()
    try:
        _login(client, email='admin@nhmbeo.rs', role='admin')
        resp = client.get('/admin/timesheet/uvoz', base_url='https://localhost')
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert '/timesheet/uvoz/pregled' in body
        assert '/admin/timesheet/uvoz-arhiva/pregled' in body
    finally:
        patcher.stop()


# --- токови увоза пишу у базу: архивски → APPROVED, текући → SUBMITTED ---
def _delete_report(report_id):
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM timesheet_report_days WHERE report_id=%s', (report_id,))
            cur.execute('DELETE FROM timesheet_reports WHERE id=%s', (report_id,))
            conn.commit()


@_DB
def test_uvoz_arhivski_upisuje_arhiva_ne_odobreno():
    """ОДЛУКА (fix/revizija-lanca): архивски увоз НИЈЕ званично одобрен извештај.
    Уписује се посебна класификација status='ARHIVA' (is_verified=FALSE,
    imported_from='word-arhiva'), идемпотентно — да не улази у одобрене."""
    email = 'baseline.uvoz.arhiva.2099@example.invalid'
    name = 'Базелина Архивски'
    parsed = rl.parse_radna_lista(
        mk.build_correct_matrix_days_rows(name=name, month=9, year=2099))
    ok, _msg, rid = ti.import_archive(parsed, email, name, 'admin@nhmbeo.rs')
    assert ok and rid is not None
    try:
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT status, is_locked, is_verified, imported_from "
                            "FROM timesheet_reports WHERE id=%s", (rid,))
                row = cur.fetchone()
        assert row['status'] == 'ARHIVA'
        assert row['is_locked']
        assert not row['is_verified'], 'архива се не сме водити као верификована/одобрена'
        assert row['imported_from'] == 'word-arhiva'
        # Идемпотентно: поновни увоз враћа ИСТИ ред.
        ok2, _m2, rid2 = ti.import_archive(parsed, email, name, 'admin@nhmbeo.rs')
        assert ok2 and rid2 == rid
    finally:
        _delete_report(rid)


@_DB
def test_uvoz_tekuci_upisuje_submitted():
    """ФУНКЦИЈА (2026-07-20-8): текући увоз чува и подноси листу (SUBMITTED,
    imported_from='word-tekuca') у ланац одобравања."""
    email = 'baseline.uvoz.tekuca@example.invalid'
    name = 'Базелина Текући'
    month, year = tp.default_entry_period()
    can, _ = tp.can_submit_for_review(month, year)
    if not can:
        now = datetime.now()
        month, year = now.month, now.year
    parsed = rl.parse_radna_lista(
        mk.build_correct_matrix_days_rows(name=name, month=month, year=year,
                                          daily=mk.SAFE_DAILY))
    ok, msg, rid = ti.import_current(email, name, parsed)
    assert ok, msg
    try:
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT status, imported_from FROM timesheet_reports WHERE id=%s", (rid,))
                row = cur.fetchone()
        assert row['imported_from'] == 'word-tekuca'
        assert row['status'] == 'SUBMITTED', f'очекиван SUBMITTED, добијен {row["status"]} ({msg})'
    finally:
        _delete_report(rid)


# ===========================================================================
# 7) РАЗДВАЈАЊЕ ТЕКУЋИХ И АРХИВСКИХ ЛИСТА
#    БАГ/функција: увезене архивске листе су затрпавале текући преглед. Сада:
#    текући преглед = ручни унос текуће године; архива = остало; ништа се не
#    брише, запослени и даље види своју историју по години. Fix: prod-2026-07-27-6.
# ===========================================================================
_ARH_EMAIL = 'baseline.arhiva@example.invalid'
_ARH_NAME = 'Базелина Архива'


@_DB
def test_arhivske_liste_van_tekuceg_ali_u_arhivi():
    """БАГ (2026-07-27-6): увезена архивска листа (2015) НЕ улази у текући
    преглед, али ЈЕСТЕ у архиви; текућа листа обрнуто. Ништа обрисано."""
    repo = TimesheetRepository(tp.DATABASE_URL)
    assert repo.available
    _delete_by_email(_ARH_EMAIL)
    try:
        arh_id = _seed_report(_ARH_EMAIL, _ARH_NAME, 6, 2015,
                              status='APPROVED', imported_from='word-arhiva')
        cur_id = _seed_report(_ARH_EMAIL, _ARH_NAME, 6, _CURRENT_YEAR, status='SUBMITTED')

        def ids(scope, **kw):
            res = repo.list_reports(page=1, per_page=1000, scope=scope,
                                    current_year=_CURRENT_YEAR, search=_ARH_NAME, **kw)
            return {r['id'] for r in res['reports']}

        current = ids('current')
        assert cur_id in current and arh_id not in current
        archive = ids('archive')
        assert arh_id in archive and cur_id not in archive

        # Ништа није обрисано — оба реда постоје.
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) AS n FROM timesheet_reports WHERE employee_email=%s",
                            (_ARH_EMAIL,))
                assert cur.fetchone()['n'] == 2
    finally:
        _delete_by_email(_ARH_EMAIL)


@_DB
def test_zaposleni_dohvata_arhivsku_godinu_po_izboru():
    """БАГ (2026-07-27-6): запослени и даље види своју листу из 2015 када
    изабере ту годину — историја није изгубљена раздвајањем прегледа."""
    _delete_by_email(_ARH_EMAIL)
    try:
        _seed_report(_ARH_EMAIL, _ARH_NAME, 6, 2015,
                     status='APPROVED', imported_from='word-arhiva')
        # Учитавач је email-first (штити од истоимених) — рута прослеђује email
        # из сесије, па и тест мора (иначе ред са email-ом није досежан по имену).
        data = ev._load_timesheet_view_data(_ARH_NAME, 6, 2015, user_email=_ARH_EMAIL)
        assert data is not None and data.get('exists')
    finally:
        _delete_by_email(_ARH_EMAIL)


# ===========================================================================
# 8) БИРАЧ ГОДИНА ЈЕ ИЗВЕДЕН ИЗ ПОДАТАКА
#    БАГ: бирач је нудио хардкодован опсег (нпр. до 2024) па архивске листе из
#    2011 нису биле досежне. Сада: од најстарије листе до текуће. Fix: prod-2026-07-27-6.
# ===========================================================================
_YEAR_EMAIL = 'baseline.birac@example.invalid'
_YEAR_NAME = 'Базелина Бирач'


@_DB
def test_birac_godina_izveden_iz_podataka_ukljucuje_2011():
    """БАГ (2026-07-27-6): ако постоји листа из 2011, бирач година мора да је
    понуди — опсег иде од најстарије листе до текуће, непрекидан."""
    _delete_by_email(_YEAR_EMAIL)
    try:
        _seed_report(_YEAR_EMAIL, _YEAR_NAME, 3, 2011, status='APPROVED')
        _seed_report(_YEAR_EMAIL, _YEAR_NAME, 3, 2015, status='APPROVED')
        years = tp.available_report_years(_YEAR_EMAIL)
        assert years[0] == 2011
        assert years[-1] == max(_CURRENT_YEAR, 2015)
        assert years == list(range(2011, years[-1] + 1))  # непрекидан опсег
        # Глобални опсег (админ/шеф) такође укључује најстарију.
        assert 2011 in tp.available_report_years()
    finally:
        _delete_by_email(_YEAR_EMAIL)


# ===========================================================================
# 9) РЕВИЗИЈА ЛАНЦА ОДОБРАВАЊА (fix/revizija-lanca)
#    Независна адверсаријална ревизија је нашла тихе рупе у ланцу. Закључане
#    гаранције:
#      * админ/директор одобравају АДМИНИСТРАТИВНО (посебан траг), никад као
#        лажни двостепени ланац (шеф+директор);
#      * нераз­решено одељење → нема тихог редовног одобрења (само административно);
#      * архива није званично одобрен извештај (status='ARHIVA'), не улази у
#        листу одобрених;
#      * архивски увоз не сме да препише постојећу редовну листу;
#      * учитавач заглавља је email-first (истоимени не виде туђе).
# ===========================================================================
_REV_EMAIL = 'baseline.revizija@example.invalid'
_REV_NAME = 'Базелина Ревизија'
_REV_ADMIN = 'admin.revizija@example.invalid'


@_DB
def test_admin_odobrenje_je_administrativno_ne_dvostepeni_lanac():
    """РЕВИЗИЈА: административно одобрење поставља APPROVED, али бележи посебан
    траг admin_approved_by — а head/director слотови остају NULL (не сме да
    изгледа као два стварна потписа)."""
    month, year = _months_ago(2)
    _delete_by_email(_REV_EMAIL)
    try:
        rid = _seed_report(_REV_EMAIL, _REV_NAME, month, year, status='SUBMITTED')
        sig = tp.confirm_timesheet_signature(rid, _REV_ADMIN, None,
                                             head_required=False, administrative=True)
        assert sig.success and sig.data['approved'] and sig.data['administrative']
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT status, is_verified, admin_approved_by, "
                            "head_verified_by, director_verified_by, verified_role "
                            "FROM timesheet_reports WHERE id=%s", (rid,))
                row = cur.fetchone()
        assert row['status'] == 'APPROVED' and row['is_verified']
        assert row['admin_approved_by'] == _REV_ADMIN
        assert row['head_verified_by'] is None
        assert row['director_verified_by'] is None
        assert row['verified_role'] == 'administrativno'
    finally:
        _delete_by_email(_REV_EMAIL)


@_DB
def test_legacy_approve_timesheet_je_administrativno():
    """РЕВИЗИЈА (налаз #4): legacy approve_timesheet() више не поставља APPROVED
    без потписа тихо — делегира на административно одобрење (обележено трагом)."""
    month, year = _months_ago(2)
    _delete_by_email(_REV_EMAIL)
    try:
        rid = _seed_report(_REV_EMAIL, _REV_NAME, month, year, status='SUBMITTED')
        res = tp.approve_timesheet(rid, _REV_ADMIN)
        assert res.success
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT status, admin_approved_by, head_verified_by, "
                            "director_verified_by FROM timesheet_reports WHERE id=%s",
                            (rid,))
                row = cur.fetchone()
        assert row['status'] == 'APPROVED'
        assert row['admin_approved_by'] == _REV_ADMIN
        assert row['head_verified_by'] is None and row['director_verified_by'] is None
    finally:
        _delete_by_email(_REV_EMAIL)


def test_nerazreseno_odeljenje_nema_tihog_redovnog_odobrenja():
    """РЕВИЗИЈА (налаз #2): кад одељење/шеф није разрешен (нема шефа у мапи),
    директор НЕ добија тихи редован 'director' слот — једини пут је
    АДМИНИСТРАТИВНО (обележено). Шеф/запослени немају овлашћење (deny)."""
    # Директор, непознато одељење (празна мапа шефова) → административно, не 'director'.
    plan = tav._signature_plan(_sess('direktor', _DIRECTOR), 'Нераз­решено', 'emp@x', {})
    assert plan['allowed'] and plan['administrative']
    assert plan['slot'] != 'director'
    # Шеф туђег/непознатог одељења → нема овлашћење (обичан deny, не административно).
    plan2 = tav._signature_plan(
        _sess('sef_odeljenja', 'sef@x', is_head=True, dept='Друго'),
        'Нераз­решено', 'emp@x', {})
    assert not plan2['allowed']
    # Обичан запослени → deny.
    plan3 = tav._signature_plan(_sess('employee', 'e@x'), 'Нераз­решено', 'emp@x', {})
    assert not plan3['allowed']


@_DB
def test_arhivski_uvoz_ne_prepisuje_redovnu_listu():
    """РЕВИЗИЈА (налаз b1): архивски увоз преко ПОСТОЈЕЋЕ редовне (не-архивске)
    листе се ОДБИЈА — не сме да обрише/препише стварне податке."""
    email = 'baseline.rev.overwrite@example.invalid'
    name = 'Базелина Оверврајт'
    _delete_by_email(email)
    try:
        # Постојећа редовна листа (ручни унос) са једним даном.
        rid = _seed_report(email, name, 9, 2098, status='DRAFT', is_locked=False)
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO timesheet_report_days (report_id, day, "
                            "work_in_museum) VALUES (%s, 5, 8)", (rid,))
                conn.commit()
        parsed = rl.parse_radna_lista(
            mk.build_correct_matrix_days_rows(name=name, month=9, year=2098))
        ok, msg, out_id = ti.import_archive(parsed, email, name, 'admin@nhmbeo.rs')
        assert not ok and out_id is None, 'увоз преко редовне листе мора да се одбије'
        # Постојећа листа нетакнута: и даље DRAFT са својим даном.
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT status FROM timesheet_reports WHERE id=%s", (rid,))
                assert cur.fetchone()['status'] == 'DRAFT'
                cur.execute("SELECT COUNT(*) AS n FROM timesheet_report_days "
                            "WHERE report_id=%s", (rid,))
                assert cur.fetchone()['n'] == 1
    finally:
        _delete_by_email(email)


@_DB
def test_load_header_email_first_ne_vraca_tudje_po_imenu():
    """РЕВИЗИЈА (налаз c1): два ИСТОИМЕНА запослена са различитим email-овима —
    учитавач заглавља враћа СВОЈ ред по email-у, никад туђи по имену."""
    name = 'Истоимени Баз'
    email_a = 'baseline.rev.imenjak.a@example.invalid'
    email_b = 'baseline.rev.imenjak.b@example.invalid'
    _delete_by_email(email_a)
    _delete_by_email(email_b)
    try:
        rid_a = _seed_report(email_a, name, 8, 2098, status='APPROVED')
        rid_b = _seed_report(email_b, name, 8, 2098, status='APPROVED')
        fields = "id, employee_name"
        hdr_a = ev._load_report_header(name, 8, 2098, fields, employee_email=email_a)
        hdr_b = ev._load_report_header(name, 8, 2098, fields, employee_email=email_b)
        assert hdr_a['id'] == rid_a
        assert hdr_b['id'] == rid_b
        assert hdr_a['id'] != hdr_b['id']
    finally:
        _delete_by_email(email_a)
        _delete_by_email(email_b)


@_DB
def test_arhiva_nije_u_listi_odobrenih():
    """РЕВИЗИЈА (контекст А): архивска листа (status='ARHIVA') се НЕ рачуна као
    одобрена — is_verified је FALSE, па не носи зелену ознаку „Одобрено"."""
    email = 'baseline.rev.arhiva.stat@example.invalid'
    name = 'Базелина Архива Стат'
    _delete_by_email(email)
    try:
        parsed = rl.parse_radna_lista(
            mk.build_correct_matrix_days_rows(name=name, month=7, year=2097))
        ok, _msg, rid = ti.import_archive(parsed, email, name, 'admin@nhmbeo.rs')
        assert ok and rid is not None
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT status, is_verified FROM timesheet_reports "
                            "WHERE id=%s", (rid,))
                row = cur.fetchone()
        assert row['status'] == 'ARHIVA'
        assert not row['is_verified']
    finally:
        _delete_by_email(email)


if __name__ == '__main__':
    sys.exit(pytest.main([__file__, '-v']))
