"""Tests za globalni audit trag (ZADATAK #4).

Pokriva:
  * helper ``audit_support.record_audit`` — upis, split int/text id, JSONB-safe
    serijalizacija, best-effort (na grešku vraća False, ne diže izuzetak);
  * instrumentaciju reprezentativnih mutacija (brisanje minerala, grant/revoke
    dozvola, kreiranje korisnika) — da zaista zovu record_audit sa ispravnom
    akcijom/entitetom;
  * čitač ``audit_log_views.render_audit_log`` — filteri (entitet/akcija/korisnik).

Integracioni delovi rade protiv dev baze (DATABASE_URL iz .env) i preskaču se
kad nije dostupna; svi upisani redovi se čiste.
"""

import os
from datetime import datetime
from unittest import mock

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-audit-trail')

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

import flask
import pytest

import audit_support


# ---------------------------------------------------------------------------
# 1. Helper: split id, best-effort, JSONB-safe
# ---------------------------------------------------------------------------

def test_split_entity_id_int():
    assert audit_support._split_entity_id(123) == (123, '123')


def test_split_entity_id_numeric_string():
    assert audit_support._split_entity_id('456') == (456, '456')


def test_split_entity_id_text():
    assert audit_support._split_entity_id('pera@nhmbeo.rs') == (None, 'pera@nhmbeo.rs')


def test_split_entity_id_none():
    assert audit_support._split_entity_id(None) == (None, None)


def test_record_audit_never_raises_and_returns_false_on_db_error():
    def boom():
        raise RuntimeError('db unavailable')

    # Mora vratiti False i NE dići izuzetak (best-effort posmatrač).
    result = audit_support.record_audit(
        action='DELETE', entity_type='mineral', entity_id=1,
        summary='x', get_postgres_connection=boom,
    )
    assert result is False


def test_record_audit_serializes_datetime_in_values():
    """old_values sa datetime/Decimal ne sme da obori upis (JSONB-safe dumps)."""
    captured = {}

    class _Cur:
        def execute(self, sql, params):
            captured['params'] = params
        def __enter__(self):
            return self
        def __exit__(self, *a):
            return False

    class _Conn:
        def cursor(self):
            return _Cur()
        def __enter__(self):
            return self
        def __exit__(self, *a):
            return False

    ok = audit_support.record_audit(
        action='DELETE', entity_type='mineral', entity_id=7,
        old_values={'id': 7, 'kada': datetime(2026, 7, 22, 10, 0, 0)},
        changed_by='t@x', get_postgres_connection=lambda: _Conn(),
    )
    assert ok is True
    # params: (table_name, record_id, record_ref, action, changed_by, old_json, new_json, summary, ip, ua)
    assert captured['params'][0] == 'mineral'
    assert captured['params'][1] == 7
    assert captured['params'][4] == 't@x'


# ---------------------------------------------------------------------------
# 2. Instrumentacija: mutacije zovu record_audit
# ---------------------------------------------------------------------------

@pytest.fixture
def app():
    application = flask.Flask(__name__)
    application.secret_key = 'test-secret'
    for endpoint in ('manage_user_access', 'admin_mineral_collection'):
        application.add_url_rule(f'/{endpoint}', endpoint, lambda: '', methods=['GET'])
    return application


def test_delete_mineral_records_audit(app):
    import collection_management_views as cmv

    fake_db = mock.MagicMock()
    fake_db.get_mineral_by_id.return_value = {'id': 42, 'item_name': 'Кварц'}
    fake_db.delete_mineral.return_value = True

    with app.test_request_context('/admin/delete_mineral/42', method='POST'):
        with mock.patch.object(cmv.audit_support, 'record_audit') as spy:
            cmv.handle_delete_mineral(42, get_mineral_database=lambda: fake_db)

    assert spy.call_count == 1
    kwargs = spy.call_args.kwargs
    assert kwargs['action'] == audit_support.ACTION_DELETE
    assert kwargs['entity_type'] == 'mineral'
    assert kwargs['entity_id'] == 42


def test_delete_mineral_no_audit_when_delete_fails(app):
    import collection_management_views as cmv

    fake_db = mock.MagicMock()
    fake_db.get_mineral_by_id.return_value = {'id': 42}
    fake_db.delete_mineral.return_value = False  # brisanje nije uspelo

    with app.test_request_context('/admin/delete_mineral/42', method='POST'):
        with mock.patch.object(cmv.audit_support, 'record_audit') as spy:
            cmv.handle_delete_mineral(42, get_mineral_database=lambda: fake_db)

    spy.assert_not_called()


def test_grant_module_access_records_permission_grant(app):
    import admin_user_management_views as auv

    module_access = {
        'mineral_database': {'name': 'Минерали', 'default_access': False, 'authorized_users': []},
    }
    form = {'user_email': 'pera@nhmbeo.rs', 'module_key': 'mineral_database'}

    with app.test_request_context('/admin/grant_access', method='POST', data=form):
        with mock.patch.object(auv.audit_support, 'record_audit') as spy:
            auv.grant_module_access(
                load_module_access=lambda: module_access,
                save_module_access=lambda: True,
                module_access=module_access,
            )

    assert spy.call_count == 1
    kwargs = spy.call_args.kwargs
    assert kwargs['action'] == audit_support.ACTION_PERMISSION_GRANT
    assert kwargs['entity_type'] == 'module_access'
    assert kwargs['entity_id'] == 'pera@nhmbeo.rs'


def test_revoke_module_access_records_permission_revoke(app):
    import admin_user_management_views as auv

    module_access = {
        'mineral_database': {
            'name': 'Минерали', 'default_access': False,
            'authorized_users': ['pera@nhmbeo.rs'],
        },
    }
    form = {'user_email': 'pera@nhmbeo.rs', 'module_key': 'mineral_database'}

    with app.test_request_context('/admin/revoke_access', method='POST', data=form):
        with mock.patch.object(auv.audit_support, 'record_audit') as spy:
            auv.revoke_module_access(
                load_module_access=lambda: module_access,
                save_module_access=lambda: True,
                module_access=module_access,
            )

    assert spy.call_count == 1
    assert spy.call_args.kwargs['action'] == audit_support.ACTION_PERMISSION_REVOKE


def test_grant_module_access_no_audit_when_already_granted(app):
    import admin_user_management_views as auv

    module_access = {
        'mineral_database': {
            'name': 'Минерали', 'default_access': False,
            'authorized_users': ['pera@nhmbeo.rs'],  # već ima pristup -> nema promene
        },
    }
    form = {'user_email': 'pera@nhmbeo.rs', 'module_key': 'mineral_database'}

    with app.test_request_context('/admin/grant_access', method='POST', data=form):
        with mock.patch.object(auv.audit_support, 'record_audit') as spy:
            auv.grant_module_access(
                load_module_access=lambda: module_access,
                save_module_access=lambda: True,
                module_access=module_access,
            )

    spy.assert_not_called()


# ---------------------------------------------------------------------------
# 3. Integracioni: upis + čitač sa filterima (protiv dev baze)
# ---------------------------------------------------------------------------

psycopg = pytest.importorskip('psycopg')

DATABASE_URL = os.environ.get('DATABASE_URL', '').replace(
    'postgresql+psycopg://', 'postgresql://'
)

MARKER = 'AUDIT_TEST_MARKER_ZADATAK4'


def _connect():
    if not DATABASE_URL:
        pytest.skip('DATABASE_URL is not configured')
    try:
        return psycopg.connect(DATABASE_URL, connect_timeout=5)
    except Exception as exc:
        pytest.skip(f'PostgreSQL unreachable: {exc}')


@pytest.fixture
def db_conn():
    conn = _connect()
    with conn.cursor() as cur:
        cur.execute("SELECT to_regclass('public.audit_log')")
        if cur.fetchone()[0] is None:
            conn.close()
            pytest.skip('audit_log table does not exist (run migration 032)')
        cur.execute("SELECT column_name FROM information_schema.columns "
                    "WHERE table_name='audit_log' AND column_name='changed_by'")
        if cur.fetchone() is None:
            conn.close()
            pytest.skip('audit_log not migrated (migration 032)')
    _cleanup(conn)
    try:
        yield conn
    finally:
        _cleanup(conn)
        conn.close()


def _cleanup(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM audit_log WHERE change_summary LIKE %s", (f'%{MARKER}%',))
    conn.commit()


@pytest.fixture
def app_ctx(db_conn):
    import app as museum_app
    with museum_app.app.test_request_context('/admin/audit-log'):
        yield museum_app.app


def test_record_audit_persists_row(db_conn, app_ctx):
    ok = audit_support.record_audit(
        action='DELETE', entity_type='mineral', entity_id=12345,
        summary=f'{MARKER} обрисан минерал', changed_by='auditor@example.com',
        old_values={'id': 12345, 'item_name': 'Тест'},
    )
    assert ok is True
    with db_conn.cursor() as cur:
        cur.execute(
            "SELECT table_name, record_id, record_ref, action, changed_by, old_values "
            "FROM audit_log WHERE change_summary LIKE %s", (f'%{MARKER}%',),
        )
        row = cur.fetchone()
    assert row is not None
    assert row[0] == 'mineral'
    assert row[1] == 12345
    assert row[3] == 'DELETE'
    assert row[4] == 'auditor@example.com'
    assert row[5]['item_name'] == 'Тест'


def test_viewer_filters_by_action(db_conn):
    import app as museum_app
    import audit_log_views

    # Seed one DELETE and one PERMISSION_GRANT inside a request context.
    with museum_app.app.test_request_context('/admin/audit-log'):
        audit_support.record_audit(action='DELETE', entity_type='mineral', entity_id=1,
                                   summary=f'{MARKER} del mineral', changed_by='a@x')
        audit_support.record_audit(action='PERMISSION_GRANT', entity_type='module_access',
                                   entity_id='b@x', summary=f'{MARKER} grant', changed_by='admin@x')

    # Filter by action=PERMISSION_GRANT -> only the grant row shows.
    with museum_app.app.test_request_context('/admin/audit-log?action=PERMISSION_GRANT'):
        html = audit_log_views.render_audit_log()
    assert f'{MARKER} grant' in html
    assert f'{MARKER} del mineral' not in html

    # Filter by entity=mineral -> only the delete row shows.
    with museum_app.app.test_request_context('/admin/audit-log?entity=mineral'):
        html2 = audit_log_views.render_audit_log()
    assert f'{MARKER} del mineral' in html2
    assert f'{MARKER} grant' not in html2
