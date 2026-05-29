"""Reproducing/behavior tests for the content-vehicles cluster (Phase C low bugs).

Covers four LOW-severity hardening fixes:
1. museum_content_views.handle_add_visitor / handle_add_research:
   in-memory IDs must not collide via len()+1 (use max(id)+1).
2. vehicle_depot_views.handle_add_vehicle_reservation JSON-fallback:
   int(vehicle_id) must be guarded (no 500 on missing/blank).
3. notification_views.api_get_notifications:
   unread_count must come from a COUNT over all rows, not the LIMIT-50 page.
4. vehicle_depot_views.handle_add_vehicle_reservation JSON-fallback:
   reservation record must include 'status' (and the other PG-shape fields).
"""

import os
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


# --- Finding 1: visitor/research in-memory ID collision -------------------

def test_add_visitor_id_unique_after_existing_higher_id(app):
    """A pre-existing record with a higher id than len() must not cause a
    duplicate id (len()+1 would collide / overwrite logically)."""
    # Two records but their ids are 1 and 5 -> len()+1 == 3 would collide later.
    visitor_records = [{'id': 1}, {'id': 5}]
    form = {'date': '2026-05-29', 'visitor_type': 'individual'}
    with app.test_request_context('/admin/add-visitor', method='POST', data=form):
        content_views.handle_add_visitor(visitor_records=visitor_records)
    new_id = visitor_records[-1]['id']
    ids = [record['id'] for record in visitor_records]
    assert new_id == 6
    assert len(ids) == len(set(ids)), f"duplicate ids: {ids}"


def test_add_research_id_unique_after_existing_higher_id(app):
    research_projects = [{'id': 1}, {'id': 7}]
    form = {'title': 'X', 'project_code': 'P1'}
    with app.test_request_context('/admin/add-research', method='POST', data=form):
        content_views.handle_add_research(research_projects=research_projects)
    new_id = research_projects[-1]['id']
    ids = [project['id'] for project in research_projects]
    assert new_id == 8
    assert len(ids) == len(set(ids)), f"duplicate ids: {ids}"


# --- Finding 2: int(vehicle_id) guard in JSON fallback --------------------

def _no_db_env():
    return mock.patch.dict(os.environ, {}, clear=False)


def test_add_reservation_missing_vehicle_id_no_500(app, monkeypatch):
    """Missing vehicle_id in the JSON-fallback branch must not raise; it
    should flash an error and redirect (HTTP 302), not crash with TypeError."""
    monkeypatch.delenv('DATABASE_URL', raising=False)
    reservations = []
    form = {'employee_name': 'Pera', 'start_date': '2026-05-29', 'end_date': '2026-05-30'}
    with app.test_request_context('/vehicles/add-reservation', method='POST', data=form):
        resp = vehicle_depot_views.handle_add_vehicle_reservation(
            phase3a_databases=mock.MagicMock(),
            get_vehicle_reservations=lambda *a, **k: reservations,
            save_reservations=lambda: True,
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
            save_reservations=lambda: True,
        )
    status = resp[1] if isinstance(resp, tuple) else getattr(resp, 'status_code', 302)
    assert status == 302
    assert reservations == []


# --- Finding 4: JSON-fallback reservation record shape (status etc.) ------

def test_add_reservation_json_fallback_includes_status(app, monkeypatch):
    monkeypatch.delenv('DATABASE_URL', raising=False)
    reservations = []
    form = {
        'vehicle_id': '3',
        'employee_name': 'Pera',
        'start_date': '2026-05-29',
        'end_date': '2026-05-30',
        'start_time': '08:00',
        'end_time': '16:00',
        'estimated_km': '120',
        'driver_name': 'Mika',
        'driver_license': 'B',
        'passengers': '2',
        'purpose': 'Terenski rad',
    }
    with app.test_request_context('/vehicles/add-reservation', method='POST', data=form):
        vehicle_depot_views.handle_add_vehicle_reservation(
            phase3a_databases=mock.MagicMock(),
            get_vehicle_reservations=lambda *a, **k: reservations,
            save_reservations=lambda: True,
        )
    assert len(reservations) == 1
    record = reservations[0]
    assert record['vehicle_id'] == 3
    assert record['status'] == 'Активна'
    for key in ('start_time', 'end_time', 'estimated_km', 'driver_name',
                'driver_license', 'passengers'):
        assert key in record, f"missing key {key} in JSON-fallback reservation"


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
