"""Phase C low-severity hardening tests for travel_finance_views.

Covers:
- api_field_trip_create timesheet_updated honesty (no false success when no
  monthly report row exists / when DATABASE_URL is unset).
- api_nabavka_list admin detection consistency (is_admin session flag).
- file-backed reservation id stability after deletions.
- api_nabavka_save / api_nabavka_list guard when DATABASE_URL is unset.
"""

import os
from contextlib import contextmanager
from unittest.mock import MagicMock

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-travel-finance')

import app as museum_app  # noqa: E402
import travel_finance_views as tfv  # noqa: E402


def _ctx(json_body):
    return museum_app.app.test_request_context(
        '/x', method='POST', json=json_body,
    )


def _login_direktor():
    """Direct field-trip creation is an admin/direktor operator path since the
    unified approval framework; ordinary users go through request approval."""
    from flask import session
    session['user_role'] = 'direktor'
    session['user_email'] = 'direktor@example.com'
    session['user_name'] = 'Директор'


# ---------------------------------------------------------------------------
# Finding 1: timesheet_updated honesty
# ---------------------------------------------------------------------------

def test_field_trip_no_database_url_does_not_claim_timesheet_updated(monkeypatch):
    monkeypatch.delenv('DATABASE_URL', raising=False)
    body = {
        'update_timesheet': True,
        'start_date': '2026-05-01',
        'end_date': '2026-05-02',
    }
    with _ctx(body):
        _login_direktor()
        resp = tfv.api_field_trip_create()
        payload = resp.get_json()
    assert payload['success'] is True
    # Must NOT falsely claim the timesheet was updated when nothing was written.
    assert payload['timesheet_updated'] is False


def test_field_trip_no_monthly_report_marks_skipped_not_updated(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'postgresql://u:p@localhost/db')

    fake_cur = MagicMock()
    # SELECT timesheet_reports -> no monthly report row exists.
    fake_cur.fetchone.return_value = None

    fake_conn = MagicMock()
    fake_conn.cursor.return_value.__enter__.return_value = fake_cur

    @contextmanager
    def fake_connect(*args, **kwargs):
        yield fake_conn

    fake_psycopg = MagicMock()
    fake_psycopg.connect.side_effect = fake_connect
    monkeypatch.setitem(__import__('sys').modules, 'psycopg', fake_psycopg)

    body = {
        'update_timesheet': True,
        'start_date': '2026-05-01',
        'end_date': '2026-05-01',
    }
    with _ctx(body):
        _login_direktor()
        resp = tfv.api_field_trip_create()
        payload = resp.get_json()

    assert payload['success'] is True
    assert payload['timesheet_updated'] is False
    assert payload.get('timesheet_skipped') is True


def test_field_trip_timesheet_updated_when_day_written(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'postgresql://u:p@localhost/db')

    fake_cur = MagicMock()
    # SELECT timesheet_reports -> a monthly report row exists.
    fake_cur.fetchone.return_value = {'id': 42}

    fake_conn = MagicMock()
    fake_conn.cursor.return_value.__enter__.return_value = fake_cur

    @contextmanager
    def fake_connect(*args, **kwargs):
        yield fake_conn

    fake_psycopg = MagicMock()
    fake_psycopg.connect.side_effect = fake_connect
    monkeypatch.setitem(__import__('sys').modules, 'psycopg', fake_psycopg)

    body = {
        'update_timesheet': True,
        'start_date': '2026-05-01',
        'end_date': '2026-05-01',
    }
    with _ctx(body):
        _login_direktor()
        resp = tfv.api_field_trip_create()
        payload = resp.get_json()

    assert payload['success'] is True
    assert payload['timesheet_updated'] is True
    assert payload.get('timesheet_skipped') is not True


# ---------------------------------------------------------------------------
# ZADATAK #3: PostgreSQL je jedini izvor istine za rezervacije — bez tihog
# JSON fallback-a. Kad baza nije dostupna, rezervacija se NE kreira i greška
# se prijavljuje (ne maskira se kao uspeh).
# ---------------------------------------------------------------------------

def test_no_database_url_does_not_silently_reserve_vehicle(monkeypatch):
    monkeypatch.delenv('DATABASE_URL', raising=False)

    body = {
        'vehicle_id': 7,
        'start_date': '2026-05-01',
        'end_date': '2026-05-02',
        'purpose': 'x',
        'location': 'Niš',
    }
    with _ctx(body):
        _login_direktor()
        resp = tfv.api_field_trip_create()
        payload = resp.get_json()

    # No JSON fallback: the museum vehicle reservation is not created and the
    # unavailable database is surfaced as an error rather than a false success.
    assert payload['vehicle_reserved'] is False
    assert payload.get('vehicle_error')


# ---------------------------------------------------------------------------
# Finding 2: admin detection via is_admin flag
# ---------------------------------------------------------------------------

def test_nabavka_list_admin_via_is_admin_flag(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'postgresql://u:p@localhost/db')

    fake_cur = MagicMock()
    # First fetchone -> table exists check ({'exists': True}); then fetchall.
    fake_cur.fetchone.return_value = {'exists': True}
    fake_cur.fetchall.return_value = []

    fake_conn = MagicMock()
    fake_conn.cursor.return_value.__enter__.return_value = fake_cur

    @contextmanager
    def fake_connect(*args, **kwargs):
        yield fake_conn

    fake_psycopg = MagicMock()
    fake_psycopg.connect.side_effect = fake_connect
    monkeypatch.setitem(__import__('sys').modules, 'psycopg', fake_psycopg)

    with museum_app.app.test_request_context('/api/nabavka/list'):
        from flask import session
        session['user_email'] = 'admin@example.com'
        # No user_role; admin only via is_admin flag.
        session['is_admin'] = True
        resp = tfv.api_nabavka_list()
        assert resp.get_json()['success'] is True

    # The executed admin SELECT must NOT be the per-user (WHERE user_email) query.
    executed_sql = ' '.join(
        str(call.args[0]) for call in fake_cur.execute.call_args_list
    )
    # The admin branch query (no WHERE user_email filter) must have run.
    assert 'WHERE user_email' not in executed_sql


# ---------------------------------------------------------------------------
# Finding 4: explicit guard when DATABASE_URL is unset
# ---------------------------------------------------------------------------

def test_nabavka_list_unset_database_url_is_not_masked_as_success(monkeypatch):
    monkeypatch.delenv('DATABASE_URL', raising=False)
    with museum_app.app.test_request_context('/api/nabavka/list'):
        resp = tfv.api_nabavka_list()
        body = resp[0] if isinstance(resp, tuple) else resp
        payload = body.get_json()
    assert payload['success'] is False


def test_nabavka_save_unset_database_url_returns_clear_error(monkeypatch):
    monkeypatch.delenv('DATABASE_URL', raising=False)
    with _ctx({'datum': '2026-05-01', 'podnosilac': 'x', 'items': []}):
        resp = tfv.api_nabavka_save()
        body = resp[0] if isinstance(resp, tuple) else resp
        payload = body.get_json()
    assert payload['success'] is False
