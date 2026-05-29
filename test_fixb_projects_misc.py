"""Regression tests for projects-misc cluster (Phase B medium bugs).

Covers:
  1. Duplicate 'title' assignment in api_update_exhibition UPDATE builder.
     A payload carrying both 'name' and 'title' (or any other alias pair such
     as type/exhibition_type, startDate/start_date, endDate/end_date) produced
     `SET title = %s, title = %s, ...` which PostgreSQL rejects with
     'multiple assignments to same column "title"'.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-projects-misc')

import contextlib
import re
from unittest.mock import patch

import pytest
from flask import Flask

import exhibition_planner_views as epv


class DuplicateAssignmentError(Exception):
    """Mimic PostgreSQL rejecting multiple assignments to the same column."""


class FakeCursor:
    """Cursor that records SQL and rejects duplicate SET column assignments."""

    def __init__(self, owner_row):
        self._owner_row = owner_row
        self.executed = []
        self._last_one = None

    def execute(self, sql, params=None):
        self.executed.append((sql, params))
        if sql.strip().startswith("SELECT id, created_by_email FROM exhibitions"):
            self._last_one = self._owner_row
            return
        if "UPDATE exhibitions" in sql:
            set_clause = re.search(r"SET\s+(.*?)\s+WHERE", sql, re.DOTALL)
            if set_clause:
                assignments = [a.strip() for a in set_clause.group(1).split(',')]
                columns = [a.split('=')[0].strip() for a in assignments]
                seen = set()
                for col in columns:
                    if col in seen:
                        raise DuplicateAssignmentError(
                            'multiple assignments to same column "%s"' % col
                        )
                    seen.add(col)
            self._last_one = {'id': 1, 'title': 'X', 'status': 'planning', 'progress': 0}
            return
        self._last_one = None

    def fetchone(self):
        return self._last_one

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


def _run_update(app, cursor, payload):
    with app.test_request_context(
        '/api/exhibitions/1', method='PUT', json=payload
    ):
        from flask import session as flask_session
        flask_session['user_email'] = 'owner@example.com'
        flask_session['user_role'] = 'admin'
        with patch.object(epv, 'get_postgres_connection', lambda **kw: _conn_cm(cursor)):
            return epv.api_update_exhibition(1)


def test_update_with_name_and_title_does_not_crash(app):
    cursor = FakeCursor({'id': 1, 'created_by_email': 'owner@example.com'})
    payload = {'name': 'Нова изложба', 'title': 'Нова изложба', 'description': 'опис'}
    resp = _run_update(app, cursor, payload)

    status = resp[1] if isinstance(resp, tuple) else 200
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()

    assert status != 500
    assert body['success'] is True

    update_sql = next(sql for sql, _ in cursor.executed if "UPDATE exhibitions" in sql)
    assert update_sql.count("title = %s") == 1


def test_update_with_alias_pairs_emits_each_column_once(app):
    cursor = FakeCursor({'id': 1, 'created_by_email': 'owner@example.com'})
    payload = {
        'type': 'temporary',
        'exhibition_type': 'temporary',
        'startDate': '2026-01-01',
        'start_date': '2026-01-01',
        'endDate': '2026-02-01',
        'end_date': '2026-02-01',
    }
    resp = _run_update(app, cursor, payload)

    status = resp[1] if isinstance(resp, tuple) else 200
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()

    assert status != 500
    assert body['success'] is True

    update_sql = next(sql for sql, _ in cursor.executed if "UPDATE exhibitions" in sql)
    assert update_sql.count("exhibition_type = %s") == 1
    assert update_sql.count("start_date = %s") == 1
    assert update_sql.count("end_date = %s") == 1


def test_update_single_field_still_works(app):
    cursor = FakeCursor({'id': 1, 'created_by_email': 'owner@example.com'})
    payload = {'name': 'Само назив'}
    resp = _run_update(app, cursor, payload)

    status = resp[1] if isinstance(resp, tuple) else 200
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()

    assert status != 500
    assert body['success'] is True

    update_sql = next(sql for sql, _ in cursor.executed if "UPDATE exhibitions" in sql)
    assert update_sql.count("title = %s") == 1
