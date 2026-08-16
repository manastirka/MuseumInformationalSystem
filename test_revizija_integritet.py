#!/usr/bin/env python3
"""Тестови исправки интегритета из ревизије 2026-08 (батч 2).

Сваки тест је писан тако да ПАДА на коду пре одговарајуће исправке:
  1. 2909c0d — force-edit чита стари статус под закљученом трансакцијом;
     admin више не руши са UnboundLocalError, audit траг за reopen_approved
     увек постоји; шеф одељења не сме да отвори ОВЕРЕНУ листу.
  2. 39809a4 — module_access: пад DB уписа враћа грешку БЕЗ фалбек фајла;
     flash успеха и audit тек после успешног чувања.
  3. 62c9336 — посете/истраживачки пројекти иду у PostgreSQL (миграција 040),
     не у процесну листу која нестаје при рестарту.
  4. 4227715 — одобрење теренске: пад резервације возила се ВИДНО пријављује
     (warning у одговору), не тихи success.
  5. 12b135c — fail-closed: пад провере статуса пре уписа радне листе враћа
     503 и НЕ уписује; check_timesheet_lock_status при паду ДИЖЕ изузетак.
  6. 22791f6 — mineral PG слој: update/delete непостојећег id → неуспех.
  7. 6202b49 — can_access_owned_record: директор има админ паритет над туђим
     финансијским плановима и профилима мапа.
  8. 19e9be1 — једна рута одобрења радне листе: секундарна
     /api/timesheet/<id>/approve је уклоњена, детаљ страна зове примарну;
     примарна рута бележи потпис шефа (мигр. 034) и административни траг
     админа (мигр. 035) у бази.

БЕЗБЕДНОСТ: ради ИСКЉУЧИВО над базом чије име садржи '_test'
(подразумевано museum_system_test) — никад над museum_system.

Покретање:
    python -m pytest test_revizija_integritet.py -q
"""

import json
import os

import pytest

TEST_DB_URL = os.environ.get(
    'MIS_TEST_DB_URL',
    'postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system_test',
)
if '_test' not in TEST_DB_URL.rsplit('/', 1)[-1]:
    pytest.skip(
        'MIS_TEST_DB_URL не показује на *_test базу — заштита продукционе базе',
        allow_module_level=True,
    )

os.environ['DATABASE_URL'] = TEST_DB_URL
os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', 'logs/qa_flask_session')
os.environ.setdefault('WTF_CSRF_ENABLED', 'False')
os.environ.setdefault('RATELIMIT_STORAGE_URL', 'memory://')

import psycopg  # noqa: E402

PLAIN_URL = TEST_DB_URL.replace('postgresql+psycopg://', 'postgresql://')


def _pg_available():
    try:
        with psycopg.connect(PLAIN_URL, connect_timeout=3) as conn:
            conn.execute('SELECT 1')
        return True
    except Exception:
        return False


if not _pg_available():
    pytest.skip('PostgreSQL (museum_system_test) није доступан',
                allow_module_level=True)

import app as museum_app  # noqa: E402

museum_app.app.config['TESTING'] = True
museum_app.app.config['WTF_CSRF_ENABLED'] = False

BASE = 'https://localhost'


@pytest.fixture(scope='module', autouse=True)
def _preusmeri_bazu_na_test():
    """У пуном suite-у је app можда већ увезен са DATABASE_URL из .env
    (museum_system!) и pool-ови већ везани — преусмери env и ресетуј СВЕ
    pool-ове на *_test базу док траје овај модул, па врати старо стање."""
    import postgres_service
    import timesheet_postgres as tp
    old_env = os.environ.get('DATABASE_URL')
    old_tp_url = tp.DATABASE_URL
    os.environ['DATABASE_URL'] = TEST_DB_URL
    postgres_service.close_connection_pools()
    tp.close_connection_pool()
    tp.DATABASE_URL = TEST_DB_URL
    yield
    postgres_service.close_connection_pools()
    tp.close_connection_pool()
    tp.DATABASE_URL = old_tp_url
    if old_env is not None:
        os.environ['DATABASE_URL'] = old_env


def _db():
    return psycopg.connect(PLAIN_URL)


def _login(client, *, email, role, user_id=990001,
           department='Природњачки музеј', **extra):
    with client.session_transaction() as s:
        s['user_id'] = user_id
        s['user_email'] = email
        s['user_name'] = 'Тест Ревизија'
        s['user_role'] = role
        s['user_department'] = department
        s['is_admin'] = role in ('admin', 'direktor')
        for k, v in extra.items():
            s[k] = v
    return client


def _client():
    return museum_app.app.test_client()


ADMIN_EMAIL = 'admin.integritet@example.invalid'
DIREKTOR_EMAIL = 'direktor.integritet@example.invalid'


def _insert_report(email, name, *, status, month=1, year=2020):
    with _db() as conn:
        cur = conn.execute(
            """
            INSERT INTO timesheet_reports
                (employee_name, employee_email, month, year, organization_unit,
                 position, duties_summary, special_tasks, status)
            VALUES (%s, %s, %s, %s, 'Тест', 'Тест', '', '', %s)
            RETURNING id
            """,
            (name, email, month, year, status),
        )
        report_id = cur.fetchone()[0]
        conn.commit()
    return report_id


def _report_row(report_id):
    with _db() as conn:
        conn.row_factory = psycopg.rows.dict_row
        return conn.execute(
            """
            SELECT status, head_verified_by, director_verified_by,
                   admin_approved_by, admin_approved_at
            FROM timesheet_reports WHERE id = %s
            """,
            (report_id,),
        ).fetchone()


def _delete_reports(email):
    with _db() as conn:
        conn.execute('DELETE FROM timesheet_reports WHERE employee_email = %s',
                     (email,))
        conn.execute('DELETE FROM user_notifications WHERE user_email = %s',
                     (email,))
        conn.commit()


def _delete_audit(changed_by):
    with _db() as conn:
        conn.execute('DELETE FROM audit_log WHERE changed_by = %s',
                     (changed_by,))
        conn.commit()


def _create_user(email, *, role, full_name='Тест Ревизија'):
    with _db() as conn:
        cur = conn.execute(
            """
            INSERT INTO users (email, full_name, password_hash, salt, role_id,
                               position, is_active, is_first_login)
            VALUES (%s, %s, 'x', 'x', (SELECT id FROM roles WHERE name = %s),
                    'Тест', TRUE, FALSE)
            RETURNING id
            """,
            (email, full_name, role),
        )
        user_id = cur.fetchone()[0]
        conn.commit()
    return user_id


def _create_profile(email, full_name, department):
    with _db() as conn:
        conn.execute(
            """
            INSERT INTO employee_profiles (full_name, email, position, department)
            VALUES (%s, %s, 'Тест', %s)
            """,
            (full_name, email, department),
        )
        conn.commit()


def _delete_identity(email):
    with _db() as conn:
        conn.execute('DELETE FROM employee_profiles WHERE email = %s', (email,))
        conn.execute('DELETE FROM users WHERE email = %s', (email,))
        conn.commit()


# ===========================================================================
# 1. force-edit ОВЕРЕНЕ листе (2909c0d)
# ===========================================================================
FE_ADMIN_EMP = 'fe.admin.zaposleni@example.invalid'
FE_DIR_EMP = 'fe.direktor.zaposleni@example.invalid'
FE_SEF_EMP = 'fe.sef.zaposleni@example.invalid'
FE_SEF_EMAIL = 'fe.sef@example.invalid'
FE_DEPT = 'Ревизија-Тест Одељење ФЕ'


def _audit_reopen_row(report_id, changed_by):
    with _db() as conn:
        return conn.execute(
            """
            SELECT 1 FROM audit_log
            WHERE action = 'reopen_approved' AND table_name = 'timesheet_report'
              AND record_id = %s AND changed_by = %s
            """,
            (report_id, changed_by),
        ).fetchone()


def test_admin_force_edit_odobrene_vraca_draft_i_pise_audit():
    """БАГ (2909c0d): стари код је у admin грани референцирао ``status_row``
    који се пуни само у не-admin грани → UnboundLocalError (500) и никад
    записан audit траг. Сада: 200, статус у бази DRAFT и постоји ред
    reopen_approved у audit_log за баш тај report_id."""
    report_id = _insert_report(FE_ADMIN_EMP, 'ФЕ Админ Тест', status='APPROVED')
    client = _login(_client(), email=ADMIN_EMAIL, role='admin')
    try:
        resp = client.post(f'/api/timesheet/{report_id}/force-edit',
                           json={}, base_url=BASE)
        assert resp.status_code == 200, resp.get_data(as_text=True)
        assert resp.get_json().get('success') is True
        row = _report_row(report_id)
        assert row['status'] == 'DRAFT', \
            'оверена листа није враћена у DRAFT у бази'
        assert _audit_reopen_row(report_id, ADMIN_EMAIL) is not None, \
            'нема audit трага reopen_approved за админово откључавање'
    finally:
        _delete_reports(FE_ADMIN_EMP)
        _delete_audit(ADMIN_EMAIL)


def test_direktor_force_edit_odobrene_vraca_draft_i_pise_audit():
    """Исти сценарио за директора (2909c0d): стари статус долази из закључане
    трансакције (result.data['old_status']), па audit траг постоји и када
    scope-грана не остави локални status_row."""
    report_id = _insert_report(FE_DIR_EMP, 'ФЕ Директор Тест', status='APPROVED')
    client = _login(_client(), email=DIREKTOR_EMAIL, role='direktor')
    try:
        resp = client.post(f'/api/timesheet/{report_id}/force-edit',
                           json={}, base_url=BASE)
        assert resp.status_code == 200, resp.get_data(as_text=True)
        assert resp.get_json().get('success') is True
        assert _report_row(report_id)['status'] == 'DRAFT'
        assert _audit_reopen_row(report_id, DIREKTOR_EMAIL) is not None, \
            'нема audit трага reopen_approved за директорово откључавање'
    finally:
        _delete_reports(FE_DIR_EMP)
        _delete_audit(DIREKTOR_EMAIL)


def test_sef_ne_moze_force_edit_odobrene():
    """Шеф одељења НЕ сме да отвори ОВЕРЕНУ листу свог одељења: 403, статус
    у бази остаје APPROVED (провера је ауторитативна и под FOR UPDATE
    локом у force_edit_timesheet — 2909c0d / ревизија #2)."""
    _create_user(FE_SEF_EMAIL, role='sef_odeljenja', full_name='ФЕ Шеф Тест')
    _create_profile(FE_SEF_EMAIL, 'ФЕ Шеф Тест', FE_DEPT)
    _create_profile(FE_SEF_EMP, 'ФЕ Шеф Запослени', FE_DEPT)
    report_id = _insert_report(FE_SEF_EMP, 'ФЕ Шеф Запослени', status='APPROVED')
    client = _login(_client(), email=FE_SEF_EMAIL, role='sef_odeljenja',
                    department=FE_DEPT, is_department_head=True)
    try:
        resp = client.post(f'/api/timesheet/{report_id}/force-edit',
                           json={}, base_url=BASE)
        assert resp.status_code == 403, resp.get_data(as_text=True)
        assert _report_row(report_id)['status'] == 'APPROVED', \
            'шеф је ипак вратио оверену листу у DRAFT'
    finally:
        _delete_reports(FE_SEF_EMP)
        _delete_identity(FE_SEF_EMAIL)
        _delete_identity(FE_SEF_EMP)


# ===========================================================================
# 2. module_access — пад DB уписа без фалбек фајла (39809a4)
# ===========================================================================
MODUL_KORISNIK = 'modul.integritet@example.invalid'


def _audit_count_module_access():
    with _db() as conn:
        return conn.execute(
            "SELECT COUNT(*) FROM audit_log WHERE table_name = 'module_access'"
        ).fetchone()[0]


def test_module_access_pad_db_upisa_vraca_gresku_bez_falbeka():
    """БАГ (39809a4): стари код је flash-овао успех ПРЕ чувања, а пад DB
    уписа је тихо падао на фалбек фајл (који се при читању игнорише чим DB
    ред постоји) и уписивао audit. Сада: рута враћа грешку, нема flash-а
    успеха, нема новог реда у audit_log, data/module_access.json нетакнут."""
    from unittest.mock import patch
    import module_access_support

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'data', 'module_access.json')
    file_before = None
    mtime_before = None
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            file_before = f.read()
        mtime_before = os.path.getmtime(file_path)

    audit_before = _audit_count_module_access()
    client = _login(_client(), email=ADMIN_EMAIL, role='admin')
    try:
        with patch.object(museum_app, 'shared_settings_db_enabled',
                          lambda flask_app: True), \
             patch.object(module_access_support, '_save_db_json_setting',
                          lambda **kwargs: False):
            resp = client.post(
                '/admin/grant_access',
                data={'user_email': MODUL_KORISNIK, 'module_key': 'kr_dosije'},
                base_url=BASE,
            )
            assert resp.status_code == 302, resp.status_code
            with client.session_transaction() as s:
                flashes = s.get('_flashes', [])
            categories = [c for c, _ in flashes]
            assert 'success' not in categories, \
                f'рута је пријавила успех иако DB упис није успео: {flashes}'
            assert any('није успело' in msg for _, msg in flashes), \
                f'нема видљиве поруке о неуспеху чувања: {flashes}'

        assert _audit_count_module_access() == audit_before, \
            'audit ред за доделу приступа је уписан упркос паду чувања'

        if file_before is None:
            assert not os.path.exists(file_path), \
                'фалбек фајл је створен упркос паду DB уписа'
        else:
            with open(file_path, 'rb') as f:
                assert f.read() == file_before, \
                    'data/module_access.json је измењен упркос паду DB уписа'
            assert os.path.getmtime(file_path) == mtime_before
    finally:
        # Врати in-memory стање (рута је можда учитала стање из DB реда).
        museum_app.load_module_access(force=True)
        kr = museum_app.MODULE_ACCESS.get('kr_dosije', {})
        if MODUL_KORISNIK in kr.get('authorized_users', []):
            kr['authorized_users'].remove(MODUL_KORISNIK)


def test_save_json_settings_ne_pise_falbek_fajl_kad_db_padne(tmp_path):
    """Слој за упис (39809a4): кад је база конфигурисана а DB упис падне,
    save_json_settings_data враћа False и НЕ пише фалбек фајл. Стари код би
    уписао фајл и вратио True (тихи 'успех' који нестаје при читању)."""
    from unittest.mock import patch
    import module_access_support

    target = tmp_path / 'module_access.json'
    with patch.object(module_access_support, '_save_db_json_setting',
                      lambda **kwargs: False):
        saved = module_access_support.save_json_settings_data(
            setting_key='module_access',
            payload={'proba': {'authorized_users': [MODUL_KORISNIK]}},
            get_postgres_connection=lambda: None,
            file_path=str(target),
        )
    assert saved is False, 'пад DB уписа је пријављен као успех'
    assert not target.exists(), 'фалбек фајл је ипак написан'


# ===========================================================================
# 3. Посете у PostgreSQL (62c9336, миграција 040)
# ===========================================================================
POSETA_MARKER = 'ревизија-интегритет-посета poseta.integritet@example.invalid'


def test_poseta_se_upisuje_u_bazu_ne_u_procesnu_listu():
    """БАГ (62c9336): посете су живеле у процесној листи VISITOR_RECORDS —
    упис нестаје при рестарту и невидљив је другом gunicorn раднику. Сада
    POST /admin/add_visitor мора да остави ред у табели visitor_records,
    читљив кроз НОВУ конекцију на базу."""
    client = _login(_client(), email=ADMIN_EMAIL, role='admin')
    visitor_id = None
    try:
        resp = client.post(
            '/admin/add_visitor',
            data={
                'date': '2020-03-04',
                'visitor_type': 'индивидуална',
                'group_size': '4',
                'nationality': 'Тест',
                'ticket_type': 'пуна',
                'exhibition': 'Тест изложба',
                'feedback_rating': '5',
                'notes': POSETA_MARKER,
            },
            base_url=BASE,
        )
        assert resp.status_code == 302, resp.get_data(as_text=True)

        # Нова, независна конекција — доказ да запис НИЈЕ у процесној листи.
        with psycopg.connect(PLAIN_URL) as fresh:
            fresh.row_factory = psycopg.rows.dict_row
            row = fresh.execute(
                'SELECT id, group_size, visit_date FROM visitor_records '
                'WHERE notes = %s',
                (POSETA_MARKER,),
            ).fetchone()
        assert row is not None, 'посета није уписана у visitor_records у бази'
        assert row['group_size'] == 4
        visitor_id = row['id']

        # Процесна листа је уклоњена из app модула.
        assert not hasattr(museum_app, 'VISITOR_RECORDS'), \
            'процесна листа VISITOR_RECORDS и даље постоји у app.py'
    finally:
        with _db() as conn:
            if visitor_id is not None:
                conn.execute('DELETE FROM visitor_records WHERE id = %s',
                             (visitor_id,))
            else:
                conn.execute('DELETE FROM visitor_records WHERE notes = %s',
                             (POSETA_MARKER,))
            conn.commit()


# ===========================================================================
# 4. Одобрење теренске — пад резервације возила је видљив (4227715)
# ===========================================================================
TEREN_PODNOSILAC = 'teren.podnosilac@example.invalid'


@pytest.fixture
def terenska_zahtev_id():
    chain = [{'role': 'direktor', 'label': 'Директор', 'order': 1}]
    request_data = {
        'field_trip': {
            'vehicle_id': 1,
            'purpose': 'Тест ревизија',
            'start_date': '2020-05-01',
            'end_date': '2020-05-02',
            'location': 'Тест локација',
        }
    }
    with _db() as conn:
        cur = conn.execute(
            """
            INSERT INTO archive_requests
                (request_type, title, status, created_by_email, created_by_name,
                 request_data, approval_chain, current_approval_step)
            VALUES ('terenska_aktivnost', 'Тест теренска', 'pending', %s,
                    'Тест Подносилац', %s::jsonb, %s::jsonb, 0)
            RETURNING id
            """,
            (TEREN_PODNOSILAC, json.dumps(request_data), json.dumps(chain)),
        )
        request_id = cur.fetchone()[0]
        conn.commit()
    yield request_id
    with _db() as conn:
        # approval_signatures/request_history/request_comments су ON DELETE CASCADE.
        conn.execute('DELETE FROM archive_requests WHERE id = %s', (request_id,))
        conn.execute('DELETE FROM user_notifications WHERE user_email = %s',
                     (TEREN_PODNOSILAC,))
        conn.commit()


def test_pad_rezervacije_vozila_vidljiv_u_odgovoru(terenska_zahtev_id):
    """БАГ (4227715): кад INSERT резервације возила падне при коначном
    одобрењу теренске, стари одговор је био голи success:True без иједног
    трага о возилу. Сада одговор носи 'warning' са 'возило НИЈЕ резервисано'
    и поруком разлога. Пад INSERT-а се симулира резултатом идентичним ономе
    који execute_field_trip враћа кад упис у vehicle_reservations дигне
    изузетак (success=False + vehicle_error)."""
    from unittest.mock import patch
    import travel_finance_views

    pozvan = {}

    def _pao_insert(data, *, user_name, user_email):
        pozvan['jeste'] = True
        return {
            'success': False,
            'vehicle_reserved': False,
            'message': 'Захтев за службени пут је креиран',
            'vehicle_error': 'симулиран пад INSERT-а у vehicle_reservations',
        }

    client = _login(_client(), email=DIREKTOR_EMAIL, role='direktor')
    with patch.object(travel_finance_views, 'execute_field_trip', _pao_insert):
        resp = client.post(
            f'/api/archive/requests/{terenska_zahtev_id}/approve',
            json={'comments': 'тест'}, base_url=BASE,
        )
    assert resp.status_code == 200, resp.get_data(as_text=True)
    data = resp.get_json()
    assert data.get('success') is True, data
    assert pozvan.get('jeste'), 'резервација возила уопште није ни покушана'
    assert data.get('warning'), \
        f'нема видљивог упозорења о возилу у одговору: {data}'
    assert 'НИЈЕ резервисано' in data['warning']
    assert data['warning'] in data.get('message', ''), \
        'упозорење није део поруке коју одобравалац види'
    assert (data.get('side_effects') or {}).get('vehicle_error')

    # Одобрење је ипак спроведено у бази (грешка возила га не поништава).
    with _db() as conn:
        row = conn.execute(
            'SELECT status, final_decision FROM archive_requests WHERE id = %s',
            (terenska_zahtev_id,),
        ).fetchone()
    assert row == ('archived', 'approved')


# ===========================================================================
# 5. Fail-closed провере пре уписа радне листе (12b135c)
# ===========================================================================
UPIS_EMP = 'upis.zaposleni@example.invalid'


def test_pad_provere_statusa_obustavlja_upis_503():
    """БАГ (12b135c): пад провере статуса/прозора пре уписа се логовао као
    warning и НАСТАВЉАО (упис у потенцијално поднету/оверену листу). Сада:
    503 и ред НИЈЕ уписан у timesheet_reports."""
    from unittest.mock import patch
    import timesheet_employee_views

    def _pukla_baza(*args, **kwargs):
        raise RuntimeError('симулиран пад провере статуса')

    client = _login(_client(), email=UPIS_EMP, role='employee')
    try:
        with patch.object(timesheet_employee_views, 'get_postgres_connection',
                          _pukla_baza):
            resp = client.post(
                '/api/timesheet/save',
                json={
                    'month': 1, 'year': 2020,
                    'daily_data': {'5': {'work_in_museum': 8}},
                    'obavljeni_poslovi': 'тест',
                },
                base_url=BASE,
            )
        assert resp.status_code == 503, resp.get_data(as_text=True)
        body = resp.get_json()
        assert body.get('success') is False
        assert 'обустављен' in body.get('message', '')

        with _db() as conn:
            row = conn.execute(
                'SELECT 1 FROM timesheet_reports WHERE employee_email = %s',
                (UPIS_EMP,),
            ).fetchone()
        assert row is None, \
            'радна листа је ипак уписана иако провера статуса није прошла'
    finally:
        _delete_reports(UPIS_EMP)


def test_check_lock_status_dize_izuzetak_pri_padu_konekcije():
    """БАГ (12b135c): check_timesheet_lock_status је при грешци конекције
    враћао (False, False) — „није закључано, није оверено" — и тако отварао
    упис у закључану листу. Сада пад провере ДИЖЕ изузетак."""
    from unittest.mock import patch
    import timesheet_postgres as tp

    def _pukla_konekcija(*args, **kwargs):
        raise ConnectionError('симулиран пад конекције')

    with patch.object(tp, 'get_pg_connection', _pukla_konekcija):
        with pytest.raises(Exception):
            tp.check_timesheet_lock_status('lock.proba@example.invalid', 1, 2020)


# ===========================================================================
# 6. Mineral PG слој — rowcount при измени/брисању (22791f6)
# ===========================================================================
NEPOSTOJECI_MINERAL_ID = 2000000000


@pytest.fixture(scope='module')
def mineral_db():
    from mineral_database_pg import MineralDatabase
    db = MineralDatabase(TEST_DB_URL)
    if not db.available:
        pytest.skip('minerals табела није доступна у тест бази')
    return db


def test_update_mineral_nepostojeci_id_vraca_neuspeh(mineral_db):
    """БАГ (22791f6): UPDATE који не погоди ниједан ред враћао је True —
    позивалац је добијао 'сачувано' за непостојећи запис. Сада rowcount==0
    значи неуспех."""
    assert mineral_db.update_mineral(NEPOSTOJECI_MINERAL_ID, {}) is False, \
        'update непостојећег минерала пријављен као успех'


def test_delete_mineral_nepostojeci_id_vraca_neuspeh(mineral_db):
    """БАГ (22791f6): DELETE без погођеног реда враћао је True. Сада False."""
    assert mineral_db.delete_mineral(NEPOSTOJECI_MINERAL_ID) is False, \
        'delete непостојећег минерала пријављен као успех'


# ===========================================================================
# 7. Паритет директора над туђим записима (6202b49)
# ===========================================================================
PLAN_VLASNIK = 'vlasnik.plan@example.invalid'
MAPA_VLASNIK = 'vlasnik.mapa@example.invalid'
MAPA_PROFIL_ID = 'revizija-integritet-profil'


@pytest.fixture
def tudji_plan_id():
    with _db() as conn:
        cur = conn.execute(
            """
            INSERT INTO financial_plans
                (odeljenje, odeljenje_text, kustos, plan_data, user_email)
            VALUES ('тест', 'Тест одељење', 'Оригинал кустос', '{}'::jsonb, %s)
            RETURNING id
            """,
            (PLAN_VLASNIK,),
        )
        plan_id = cur.fetchone()[0]
        conn.commit()
    yield plan_id
    with _db() as conn:
        conn.execute('DELETE FROM financial_plans WHERE user_email = %s',
                     (PLAN_VLASNIK,))
        conn.commit()


def test_direktor_menja_tudji_finansijski_plan(tudji_plan_id):
    """БАГ (6202b49): чување туђег плана је пуштало само role=='admin', па је
    директор (који листу планова види admin-паритетом) добијао 403. Сада
    can_access_owned_record пушта директора: 200 и ред у бази промењен."""
    client = _login(_client(), email=DIREKTOR_EMAIL, role='direktor')
    resp = client.post(
        '/api/finansijski-plan/save',
        json={
            'id': tudji_plan_id,
            'odeljenje': 'тест',
            'odeljenjeText': 'Тест одељење',
            'kustos': 'Измењено од директора',
            'datumIzrade': '2026-01-01',
            'selectedYear': '2026',
            'years': {},
        },
        base_url=BASE,
    )
    assert resp.status_code == 200, resp.get_data(as_text=True)
    assert resp.get_json().get('success') is True
    with _db() as conn:
        kustos = conn.execute(
            'SELECT kustos FROM financial_plans WHERE id = %s',
            (tudji_plan_id,),
        ).fetchone()[0]
    assert kustos == 'Измењено од директора', \
        'туђи финансијски план није измењен у бази'


@pytest.fixture
def tudji_mapa_profil():
    profile = {'id': MAPA_PROFIL_ID, 'digitized_by': MAPA_VLASNIK,
               'sheet_folder': 'оригинал'}
    with _db() as conn:
        conn.execute(
            """
            INSERT INTO digitized_profiles (id, digitized_by, profile)
            VALUES (%s, %s, %s::jsonb)
            ON CONFLICT (id) DO UPDATE
              SET digitized_by = EXCLUDED.digitized_by,
                  profile = EXCLUDED.profile
            """,
            (MAPA_PROFIL_ID, MAPA_VLASNIK, json.dumps(profile)),
        )
        conn.commit()
    yield MAPA_PROFIL_ID
    with _db() as conn:
        conn.execute('DELETE FROM digitized_profiles WHERE id = %s',
                     (MAPA_PROFIL_ID,))
        conn.commit()


def test_direktor_menja_tudji_mapa_profil(tudji_mapa_profil):
    """БАГ (6202b49): измена туђег дигитализованог профила је пуштала само
    role=='admin' → директор 403. Сада 200 и ред у бази промењен."""
    client = _login(_client(), email=DIREKTOR_EMAIL, role='direktor')
    resp = client.put(
        f'/api/map/digitized-profiles/{tudji_mapa_profil}',
        json={'sheet_folder': 'измењено-директор'},
        base_url=BASE,
    )
    assert resp.status_code == 200, resp.get_data(as_text=True)
    assert resp.get_json().get('success') is True
    with _db() as conn:
        row = conn.execute(
            """
            SELECT digitized_by, profile->>'sheet_folder'
            FROM digitized_profiles WHERE id = %s
            """,
            (tudji_mapa_profil,),
        ).fetchone()
    assert row is not None
    assert row[1] == 'измењено-директор', 'профил мапе није измењен у бази'
    assert row[0] == DIREKTOR_EMAIL


# ===========================================================================
# 8. Једна рута одобрења радне листе (19e9be1) + потписи 034/035
# ===========================================================================
ODOB_SEF_EMAIL = 'odobrenje.sef@example.invalid'
ODOB_EMP = 'odobrenje.zaposleni@example.invalid'
ODOB_EMP2 = 'odobrenje2.zaposleni@example.invalid'
ODOB_DEPT = 'Ревизија-Тест Одељење Одобрење'


@pytest.fixture
def odeljenje_sa_sefom():
    _create_user(ODOB_SEF_EMAIL, role='sef_odeljenja', full_name='Одоб Шеф Тест')
    _create_profile(ODOB_SEF_EMAIL, 'Одоб Шеф Тест', ODOB_DEPT)
    _create_profile(ODOB_EMP, 'Одоб Запослени Тест', ODOB_DEPT)
    yield
    _delete_reports(ODOB_EMP)
    _delete_identity(ODOB_SEF_EMAIL)
    _delete_identity(ODOB_EMP)


def test_sef_odobrava_primarnom_rutom_potpis_u_bazi(odeljenje_sa_sefom):
    """19e9be1: детаљ страна зове ПРИМАРНУ руту
    /api/admin/timesheet/report/<id>/approve — шеф одељења кроз њу бележи
    свој потпис (head_verified_by, мигр. 034); листа остаје SUBMITTED док
    директор не потпише."""
    report_id = _insert_report(ODOB_EMP, 'Одоб Запослени Тест',
                               status='SUBMITTED')
    client = _login(_client(), email=ODOB_SEF_EMAIL, role='sef_odeljenja',
                    department=ODOB_DEPT, is_department_head=True)
    resp = client.post(
        f'/api/admin/timesheet/report/{report_id}/approve',
        json={'approve': True}, base_url=BASE,
    )
    assert resp.status_code == 200, resp.get_data(as_text=True)
    body = resp.get_json()
    assert body.get('success') is True, body
    assert body.get('approved') is False, \
        'листа проглашена одобреном са само једним потписом'
    row = _report_row(report_id)
    assert row['head_verified_by'] == ODOB_SEF_EMAIL, \
        'потпис шефа није забележен у бази (head_verified_by)'
    assert row['status'] == 'SUBMITTED'
    assert row['admin_approved_by'] is None


def test_admin_administrativno_odobrenje_trag_u_bazi():
    """19e9be1 + мигр. 035: админ кроз примарну руту одобрава
    АДМИНИСТРАТИВНО — статус APPROVED уз admin_approved_by/at траг, а
    head/director слотови остају празни (не изгледа као два потписа)."""
    report_id = _insert_report(ODOB_EMP2, 'Одоб Запослени Два',
                               status='SUBMITTED')
    client = _login(_client(), email=ADMIN_EMAIL, role='admin')
    try:
        resp = client.post(
            f'/api/admin/timesheet/report/{report_id}/approve',
            json={'approve': True}, base_url=BASE,
        )
        assert resp.status_code == 200, resp.get_data(as_text=True)
        body = resp.get_json()
        assert body.get('success') is True, body
        assert body.get('approved') is True
        row = _report_row(report_id)
        assert row['status'] == 'APPROVED'
        assert row['admin_approved_by'] == ADMIN_EMAIL, \
            'нема административног трага (admin_approved_by) у бази'
        assert row['admin_approved_at'] is not None
        assert row['head_verified_by'] is None
        assert row['director_verified_by'] is None
    finally:
        _delete_reports(ODOB_EMP2)


def test_sekundarna_ruta_odobrenja_uklonjena():
    """19e9be1: секундарна рута /api/timesheet/<id>/approve је УКЛОЊЕНА —
    сада 404. На старом коду рута је постојала (за непостојећи извештај би
    вратила 400/JSON, никад 404)."""
    client = _login(_client(), email=ADMIN_EMAIL, role='admin')
    resp = client.post('/api/timesheet/999999999/approve',
                       json={}, base_url=BASE)
    assert resp.status_code == 404, \
        f'секундарна рута одобрења и даље постоји (status {resp.status_code})'


def test_detalj_strana_zove_primarnu_rutu():
    """19e9be1: approveReport у admin_timesheet_report_detail.html мора да
    зове примарни handler, не уклоњену секундарну руту."""
    template_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'templates', 'admin_timesheet_report_detail.html',
    )
    with open(template_path, encoding='utf-8') as f:
        html = f.read()
    assert '/api/admin/timesheet/report/${reportId}/approve' in html, \
        'детаљ страна не зове примарну руту одобрења'
    assert '/api/timesheet/${reportId}/approve' not in html, \
        'детаљ страна и даље зове уклоњену секундарну руту'
