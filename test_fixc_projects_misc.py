"""Regression tests for projects-misc cluster (Phase C low-severity hardening).

Covers:
  1. api_create_exhibition returned HTTP 500 instead of a clean 400 when the
     JSON payload carried 'name' (or 'title') with a literal null value.
     `data.get('name', '').strip()` only falls back to '' when the key is
     ABSENT; when the key is present with value None the .strip() call raised
     AttributeError, which the broad except turned into a 500 leaking str(exc)
     instead of the intended 400 'Назив изложбе је обавезан'.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-projects-misc')

import contextlib
from unittest.mock import patch

import pytest
from flask import Flask

import exhibition_planner_views as epv


class FakeCursor:
    def __init__(self):
        self.executed = []

    def execute(self, sql, params=None):
        self.executed.append((sql, params))

    def fetchone(self):
        return {
            'id': 1,
            'title': 'X',
            'status': 'planning',
            'progress': 0,
            'created_at': '2026-05-29',
        }

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class FakeConn:
    def __init__(self, cursor):
        self._cursor = cursor
        self.committed = False

    def cursor(self):
        return self._cursor

    def commit(self):
        self.committed = True

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


@contextlib.contextmanager
def _conn_cm(cursor):
    yield FakeConn(cursor)


@pytest.fixture
def app():
    application = Flask(__name__)
    application.secret_key = 'test-secret'
    return application


def _run_create(app, cursor, payload):
    with app.test_request_context('/api/exhibitions', method='POST', json=payload):
        from flask import session as flask_session
        flask_session['user_email'] = 'owner@example.com'
        flask_session['user_name'] = 'Owner'
        with patch.object(epv, 'get_postgres_connection', lambda **kw: _conn_cm(cursor)):
            return epv.api_create_exhibition()


def test_create_with_null_name_returns_400_not_500(app):
    cursor = FakeCursor()
    resp = _run_create(app, cursor, {'name': None})

    status = resp[1] if isinstance(resp, tuple) else 200
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()

    assert status == 400
    assert body['success'] is False
    assert body['message'] == 'Назив изложбе је обавезан'


def test_create_with_null_title_returns_400_not_500(app):
    cursor = FakeCursor()
    resp = _run_create(app, cursor, {'title': None})

    status = resp[1] if isinstance(resp, tuple) else 200
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()

    assert status == 400
    assert body['success'] is False
    assert body['message'] == 'Назив изложбе је обавезан'


def test_create_with_valid_name_still_succeeds(app):
    cursor = FakeCursor()
    resp = _run_create(app, cursor, {'name': 'Нова изложба'})

    status = resp[1] if isinstance(resp, tuple) else 200
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()

    assert status == 200
    assert body['success'] is True

    insert_sql, params = next(
        (sql, p) for sql, p in cursor.executed if "INSERT INTO exhibitions" in sql
    )
    assert params[0] == 'Нова изложба'


def test_create_with_title_fallback_still_succeeds(app):
    cursor = FakeCursor()
    resp = _run_create(app, cursor, {'title': 'Из наслова'})

    status = resp[1] if isinstance(resp, tuple) else 200
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()

    assert status == 200
    assert body['success'] is True

    insert_sql, params = next(
        (sql, p) for sql, p in cursor.executed if "INSERT INTO exhibitions" in sql
    )
    assert params[0] == 'Из наслова'
