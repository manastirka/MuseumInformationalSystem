"""Reproducing/behavior tests for the content-vehicles cluster (Phase C low bugs).

Covers four LOW-severity hardening fixes:
1. museum_content_views.handle_add_visitor / handle_add_research:
   IDs must not collide. Originally the in-memory len()+1 scheme was
   replaced by max(id)+1; since batch 62c9336 (migracija 040) the records
   live in PostgreSQL and the database assigns the id (SERIAL/IDENTITY),
   so the handlers must not compute an id at all.
2. vehicle_depot_views.handle_add_vehicle_reservation JSON-fallback:
   int(vehicle_id) must be guarded (no 500 on missing/blank).
3. notification_views.api_get_notifications:
   unread_count must come from a COUNT over all rows, not the LIMIT-50 page.
4. vehicle_depot_views.handle_add_vehicle_reservation JSON-fallback:
   reservation record must include 'status' (and the other PG-shape fields).
"""

import os
import re
from contextlib import contextmanager
from unittest import mock

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-content-vehicles')

import flask
import pytest

import museum_content_views as content_views
import notification_views
import vehicle_depot_views


@pytest.fixture
def app():
    application = flask.Flask(__name__)
    application.secret_key = 'test-secret'
    application.add_url_rule('/visitors', 'visitors_database', lambda: '', methods=['GET'])
    application.add_url_rule('/research', 'research_database', lambda: '', methods=['GET'])
    application.add_url_rule(
        '/vehicles/reservations',
        'vehicles.vehicle_reservations',
        lambda: '',
        methods=['GET'],
    )
    return application


# --- Finding 1: visitor/research ID assignment belongs to the database ----

class _RecordingWriteCursor:
    def __init__(self):
        self.executed = []

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _fake_pg_conn(cursor):
    conn = mock.MagicMock()
    conn.cursor.return_value = cursor

    @contextmanager
    def _cm(*args, **kwargs):
        yield conn

    return conn, _cm


def _single_insert(cursor, table):
    inserts = [(q, p) for q, p in cursor.executed if f'INSERT INTO {table}' in q]
    assert len(inserts) == 1, f"expected exactly one INSERT INTO {table}"
    return inserts[0]


def _assert_db_assigns_id(query, params):
    """The handler must not compute an id itself: the INSERT column list has
    no `id` column (SERIAL/IDENTITY assigns it) and the parameter count
    matches the placeholders, so no extra id value is smuggled in."""
    column_list = query.split('VALUES')[0]
    assert not re.search(r'\bid\b', column_list), \
        f"INSERT must not set an explicit id column: {column_list}"
    assert len(params) == query.count('%s')


def test_add_visitor_id_assigned_by_database_not_computed(app):
    """Old collision worry (len()+1 over an in-memory list) is now solved by
    PostgreSQL: the handler INSERTs without an id and the database assigns
    a unique one."""
    cursor = _RecordingWriteCursor()
    conn, cm = _fake_pg_conn(cursor)
    form = {'date': '2026-05-29', 'visitor_type': 'individual'}
    with app.test_request_context('/admin/add-visitor', method='POST', data=form):
        with mock.patch.object(content_views, 'get_postgres_connection', cm):
            resp = content_views.handle_add_visitor()
    assert resp.status_code == 302  # success redirect, not the error re-render
    query, params = _single_insert(cursor, 'visitor_records')
    _assert_db_assigns_id(query, params)
    assert params[1] == 'individual'  # visit_date, visitor_type, ...
    conn.commit.assert_called_once()


def test_add_research_id_assigned_by_database_not_computed(app):
    cursor = _RecordingWriteCursor()
    conn, cm = _fake_pg_conn(cursor)
    form = {'title': 'X', 'project_code': 'P1'}
    with app.test_request_context('/admin/add-research', method='POST', data=form):
        with mock.patch.object(content_views, 'get_postgres_connection', cm):
            resp = content_views.handle_add_research()
    assert resp.status_code == 302
    query, params = _single_insert(cursor, 'research_projects')
    _assert_db_assigns_id(query, params)
    assert params[0] == 'X'  # title, project_code, ...
    assert params[1] == 'P1'
    conn.commit.assert_called_once()


# --- Finding 2: int(vehicle_id) guard in JSON fallback --------------------

def _no_db_env():
    return mock.patch.dict(os.environ, {}, clear=False)


def test_add_reservation_missing_vehicle_id_no_500(app, monkeypatch):
    """Missing vehicle_id must not raise; it should flash an error and
    redirect (HTTP 302), not crash with TypeError."""
    monkeypatch.delenv('DATABASE_URL', raising=False)
    reservations = []
    form = {'employee_name': 'Pera', 'start_date': '2026-05-29', 'end_date': '2026-05-30'}
    with app.test_request_context('/vehicles/add-reservation', method='POST', data=form):
        resp = vehicle_depot_views.handle_add_vehicle_reservation(
            phase3a_databases=mock.MagicMock(),
            get_vehicle_reservations=lambda *a, **k: reservations,
        )
    status = resp[1] if isinstance(resp, tuple) else getattr(resp, 'status_code', 302)
    assert status == 302
    # Nothing should have been appended for an invalid request.
    assert reservations == []


def test_add_reservation_blank_vehicle_id_no_500(app, monkeypatch):
    monkeypatch.delenv('DATABASE_URL', raising=False)
    reservations = []
    form = {'vehicle_id': '', 'start_date': '2026-05-29', 'end_date': '2026-05-30'}
    with app.test_request_context('/vehicles/add-reservation', method='POST', data=form):
        resp = vehicle_depot_views.handle_add_vehicle_reservation(
            phase3a_databases=mock.MagicMock(),
            get_vehicle_reservations=lambda *a, **k: reservations,
        )
    status = resp[1] if isinstance(resp, tuple) else getattr(resp, 'status_code', 302)
    assert status == 302
    assert reservations == []


# --- ZADATAK #3: bez PostgreSQL backend-a nema tihog JSON fallback-a -------

def test_add_reservation_without_db_backend_is_clear_error_not_silent(app, monkeypatch):
    """When the PostgreSQL backend is unavailable the reservation must NOT be
    silently written to an in-memory/JSON list; the handler flashes an error
    and redirects without creating anything."""
    monkeypatch.delenv('DATABASE_URL', raising=False)
    reservations = []
    form = {
        'vehicle_id': '3',
        'employee_name': 'Pera',
        'start_date': '2026-05-29',
        'end_date': '2026-05-30',
        'purpose': 'Terenski rad',
    }
    with app.test_request_context('/vehicles/add-reservation', method='POST', data=form):
        resp = vehicle_depot_views.handle_add_vehicle_reservation(
            phase3a_databases=None,
            get_vehicle_reservations=lambda *a, **k: reservations,
        )
    status = resp[1] if isinstance(resp, tuple) else getattr(resp, 'status_code', 302)
    assert status == 302
    # No fallback store: nothing must have been created.
    assert reservations == []


# --- Finding 3: unread_count from COUNT, not LIMIT-50 page -----------------

class _FakeCursor:
    """Minimal cursor: first execute returns the page rows, the second
    (COUNT) returns the true unread total."""

    def __init__(self, page_rows, unread_total):
        self._page_rows = page_rows
        self._unread_total = unread_total
        self._mode = None

    def execute(self, query, params=None):
        if 'COUNT(*)' in query:
            self._mode = 'count'
        else:
            self._mode = 'page'

    def fetchall(self):
        return self._page_rows

    def fetchone(self):
        return {'unread_count': self._unread_total}

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class _FakeConn:
    def __init__(self, cursor):
        self._cursor = cursor

    def cursor(self):
        return self._cursor

    def commit(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def test_unread_count_uses_count_query_not_page(app):
    """50 read rows on the page but 60 unread overall -> unread_count must be
    60, derived from a COUNT, not 0 (the page count) and not capped at 50."""
    page_rows = [
        {'id': i, 'title': 't', 'message': 'm', 'icon': '', 'type': '',
         'is_read': True, 'time': '01.01.2026 00:00'}
        for i in range(50)
    ]
    fake_cursor = _FakeCursor(page_rows, unread_total=60)
    fake_conn = _FakeConn(fake_cursor)

    @contextmanager
    def fake_get_conn(*args, **kwargs):
        yield fake_conn

    with app.test_request_context('/api/notifications'):
        flask.session['user_email'] = 'user@example.com'
        with mock.patch.object(notification_views, 'get_postgres_connection', fake_get_conn):
            resp = notification_views.api_get_notifications()
    payload = resp.get_json()
    assert payload['success'] is True
    assert payload['unread_count'] == 60
