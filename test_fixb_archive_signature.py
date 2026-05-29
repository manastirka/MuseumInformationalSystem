"""Regression tests for archive-signature cluster (Phase B medium bugs).

Covers:
  1. Division-by-zero / invalid pagination in api_get_archive_requests.
  2. Race in COUNT-based archive_reference generation (api_archive_request).
  3. Race in COUNT-based delovodni number generation (api_register_signature).
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-archive-signature')

import contextlib
from unittest.mock import MagicMock, patch

import pytest
from flask import Flask

import archive_signature_blueprint as asb


@pytest.fixture
def app():
    application = Flask(__name__)
    application.secret_key = 'test-secret'
    application.register_blueprint(asb.archive_signature_bp)
    return application


def _bypass_auth():
    """Patch the auth decorators' runtime checks so routes execute in-process."""
    return patch.dict(
        os.environ, {}
    )


class FakeCursor:
    """Minimal cursor recording executed SQL and serving scripted rows."""

    def __init__(self, script):
        # script: list of (matcher_substring, fetchone_value, fetchall_value)
        self._script = script
        self.executed = []
        self._last = (None, None)

    def execute(self, sql, params=None):
        self.executed.append((sql, params))
        for matcher, one, many in self._script:
            if matcher in sql:
                self._last = (one() if callable(one) else one,
                              many() if callable(many) else many)
                return
        self._last = (None, [])

    def fetchone(self):
        return self._last[0]

    def fetchall(self):
        return self._last[1] or []

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


# ---------------------------------------------------------------------------
# Finding 1: division-by-zero / invalid pagination
# ---------------------------------------------------------------------------

def _run_list(app, query):
    cursor = FakeCursor([
        ("SELECT COUNT(*) FROM archive_requests", (7,), None),
        ("FROM archive_requests", None, []),  # the page SELECT -> no rows
    ])
    with app.test_request_context('/api/archive/requests?' + query):
        from flask import session as flask_session
        flask_session['user_id'] = 1
        flask_session['user_email'] = 'admin@example.com'
        flask_session['user_role'] = 'admin'
        with patch.object(asb, 'get_postgres_connection', lambda **kw: _conn_cm(cursor)):
            return asb.api_get_archive_requests()


def test_per_page_zero_does_not_500(app):
    resp = _run_list(app, 'per_page=0')
    status = resp[1] if isinstance(resp, tuple) else 200
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()
    # Must not be the sanitized 500 error.
    assert status != 500
    assert body['success'] is True
    assert body['per_page'] >= 1
    assert body['total_pages'] >= 1


def test_per_page_non_numeric_returns_400(app):
    resp = _run_list(app, 'per_page=abc')
    status = resp[1] if isinstance(resp, tuple) else 200
    assert status == 400


def test_page_non_numeric_returns_400(app):
    resp = _run_list(app, 'page=xyz')
    status = resp[1] if isinstance(resp, tuple) else 200
    assert status == 400


def test_negative_per_page_clamped(app):
    resp = _run_list(app, 'per_page=-5&page=-2')
    status = resp[1] if isinstance(resp, tuple) else 200
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()
    assert status != 500
    assert body['per_page'] >= 1
    assert body['page'] >= 1


def test_per_page_capped(app):
    resp = _run_list(app, 'per_page=100000')
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()
    assert body['per_page'] <= 100


def test_negative_limit_offset_not_passed_to_db(app):
    cursor = FakeCursor([
        ("SELECT COUNT(*) FROM archive_requests", (7,), None),
        ("FROM archive_requests", None, []),
    ])
    with app.test_request_context('/api/archive/requests?per_page=-5&page=-3'):
        from flask import session as flask_session
        flask_session['user_id'] = 1
        flask_session['user_email'] = 'admin@example.com'
        flask_session['user_role'] = 'admin'
        with patch.object(asb, 'get_postgres_connection', lambda **kw: _conn_cm(cursor)):
            asb.api_get_archive_requests()
    # Find the page SELECT (LIMIT/OFFSET) call and assert non-negative args.
    page_calls = [(sql, params) for sql, params in cursor.executed if 'LIMIT %s OFFSET %s' in sql]
    assert page_calls, "page query was not executed"
    limit, offset = page_calls[0][1][-2], page_calls[0][1][-1]
    assert limit >= 1
    assert offset >= 0


# ---------------------------------------------------------------------------
# Finding 2: archive_reference race / advisory-lock serialization
# ---------------------------------------------------------------------------

def test_archive_reference_uses_advisory_lock(app):
    cursor = FakeCursor([
        ("SELECT status FROM archive_requests", ('approved',), None),
        ("pg_advisory_xact_lock", None, None),
        # MAX-based extraction (preferred) or COUNT-based fallback both return a number
        ("FROM archive_requests", (4,), None),
        ("UPDATE archive_requests", None, None),
        ("INSERT INTO request_history", None, None),
    ])
    with app.test_request_context('/api/archive/requests/1/archive', method='POST'):
        from flask import session as flask_session
        flask_session['user_id'] = 1
        flask_session['user_email'] = 'admin@example.com'
        flask_session['user_name'] = 'Admin'
        flask_session['user_role'] = 'admin'
        with patch.object(asb, 'get_postgres_connection', lambda **kw: _conn_cm(cursor)):
            resp = asb.api_archive_request(1)
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()
    assert body['success'] is True
    # The transaction must take a per-year advisory lock BEFORE reading the counter
    # so concurrent archivings serialize and cannot mint duplicate references.
    sqls = [sql for sql, _ in cursor.executed]
    assert any('pg_advisory_xact_lock' in s for s in sqls), \
        "archive reference generation must serialize with pg_advisory_xact_lock"
    lock_idx = next(i for i, s in enumerate(sqls) if 'pg_advisory_xact_lock' in s)
    counter_idx = next(i for i, s in enumerate(sqls)
                       if 'archive_year = %s' in s and 'UPDATE' not in s)
    assert lock_idx < counter_idx, "advisory lock must be acquired before reading the counter"


# ---------------------------------------------------------------------------
# Finding 3: registration_number (delovodni) race / advisory-lock serialization
# ---------------------------------------------------------------------------

def test_registration_number_uses_advisory_lock(app):
    cursor = FakeCursor([
        ("SELECT status FROM document_signatures", ('verified',), None),
        ("pg_advisory_xact_lock", None, None),
        ("FROM document_signatures", (3,), None),
        ("UPDATE document_signatures", None, None),
        ("INSERT INTO signature_audit_log", None, None),
    ])
    with app.test_request_context('/api/digital-signatures/1/register', method='POST',
                                  json={}):
        from flask import session as flask_session
        flask_session['user_id'] = 1
        flask_session['user_email'] = 'pravna@example.com'
        flask_session['user_name'] = 'Pravna'
        flask_session['user_role'] = 'sef_pravne_sluzbe'
        with patch.object(asb, 'get_postgres_connection', lambda **kw: _conn_cm(cursor)):
            resp = asb.api_register_signature(1)
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()
    assert body['success'] is True
    sqls = [sql for sql, _ in cursor.executed]
    assert any('pg_advisory_xact_lock' in s for s in sqls), \
        "delovodni number generation must serialize with pg_advisory_xact_lock"
    lock_idx = next(i for i, s in enumerate(sqls) if 'pg_advisory_xact_lock' in s)
    counter_idx = next(i for i, s in enumerate(sqls)
                       if 'EXTRACT(YEAR FROM registered_at)' in s)
    assert lock_idx < counter_idx, "advisory lock must be acquired before reading the counter"


def test_registration_manual_number_skips_lock(app):
    """A manually supplied number must NOT trigger auto-generation/locking."""
    cursor = FakeCursor([
        ("SELECT status FROM document_signatures", ('verified',), None),
        ("UPDATE document_signatures", None, None),
        ("INSERT INTO signature_audit_log", None, None),
    ])
    with app.test_request_context('/api/digital-signatures/1/register', method='POST',
                                  json={'registration_number': '01-9999/2026'}):
        from flask import session as flask_session
        flask_session['user_id'] = 1
        flask_session['user_email'] = 'pravna@example.com'
        flask_session['user_name'] = 'Pravna'
        flask_session['user_role'] = 'sef_pravne_sluzbe'
        with patch.object(asb, 'get_postgres_connection', lambda **kw: _conn_cm(cursor)):
            resp = asb.api_register_signature(1)
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()
    assert body['success'] is True
    assert body['registration_number'] == '01-9999/2026'
    sqls = [sql for sql, _ in cursor.executed]
    assert not any('pg_advisory_xact_lock' in s for s in sqls)
