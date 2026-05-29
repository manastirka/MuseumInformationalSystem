"""Regression tests for archive-signature cluster (Phase C low-severity hardening).

Covers:
  1. Approve/reject derive step label and finalization decision from the
     authoritative APPROVAL_CHAINS constant, not the per-row stored chain.
  2. Creator who also holds an approver role cannot approve/reject own request.
  3. Concurrent approvals serialize via SELECT ... FOR UPDATE row lock.
  4. Finalization keys off APPROVAL_CHAINS length, so an empty/short stored
     chain does not cause premature finalization.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-archive-signature')

import contextlib
from unittest.mock import patch

import pytest
from flask import Flask

import archive_signature_blueprint as asb


@pytest.fixture
def app():
    application = Flask(__name__)
    application.secret_key = 'test-secret'
    application.register_blueprint(asb.archive_signature_bp)
    return application


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


def _insert_params(cursor, table):
    """Return params of the first INSERT recorded against the given table."""
    for sql, params in cursor.executed:
        if 'INSERT INTO ' + table in sql:
            return params
    return None


# ---------------------------------------------------------------------------
# Finding 1 + 4: finalization & label derive from APPROVAL_CHAINS, not the
# per-row stored approval_chain.
# ---------------------------------------------------------------------------

def _run_approve(app, *, request_type, status, current_step, stored_chain,
                 creator_email, user_email='approver@example.com',
                 user_role='direktor'):
    # row: request_type, status, current_approval_step, approval_chain,
    #      created_by_email, title
    request_row = (request_type, status, current_step, stored_chain,
                   creator_email, 'Тест захтев')
    cursor = FakeCursor([
        ("FROM archive_requests WHERE id = %s", request_row, None),
        ("UPDATE approval_signatures", None, None),
        ("UPDATE archive_requests", None, None),
        ("INSERT INTO request_history", None, None),
        ("INSERT INTO user_notifications", None, None),
    ])
    with app.test_request_context('/api/archive/requests/1/approve',
                                  method='POST', json={'comments': 'ok'}):
        from flask import session as flask_session
        flask_session['user_id'] = 1
        flask_session['user_email'] = user_email
        flask_session['user_name'] = 'Approver'
        flask_session['user_role'] = user_role
        with patch.object(asb, 'get_postgres_connection', lambda **kw: _conn_cm(cursor)):
            resp = asb.api_approve_archive_request(1)
    return resp, cursor


def test_approve_step0_two_level_chain_does_not_finalize_when_stored_chain_empty(app):
    """Stored chain is empty/short, but 'zahtev' has 2 levels in APPROVAL_CHAINS.

    Approving step 0 must NOT finalize the request; it must advance to in_review.
    Pre-fix the code keyed off the empty stored chain and finalized after one
    approval.
    """
    resp, cursor = _run_approve(
        app,
        request_type='zahtev',
        status='pending',
        current_step=0,
        stored_chain=[],            # drifted / empty stored chain
        creator_email='owner@example.com',
        user_role='sef_odeljenja',  # valid approver for step 0 of 'zahtev'
    )
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()
    assert body['success'] is True
    # 'zahtev' has two levels -> approving step 0 must not be final.
    assert body['final'] is False
    # The advancing UPDATE (not the finalizing one) must have run.
    update_sqls = [sql for sql, _ in cursor.executed if 'UPDATE archive_requests' in sql]
    assert update_sqls, "no archive_requests UPDATE executed"
    assert any("status = 'in_review'" in s for s in update_sqls), \
        "must advance to in_review, not finalize, on first of two approvals"
    assert not any("status = 'approved'" in s for s in update_sqls), \
        "must not finalize after a single approval of a two-level chain"


def test_approve_final_step_finalizes_using_authoritative_chain(app):
    """Final step of the authoritative chain finalizes even if stored chain drifted."""
    resp, cursor = _run_approve(
        app,
        request_type='zahtev',
        status='in_review',
        current_step=1,             # last step of 'zahtev' (len 2)
        stored_chain=[],            # drifted
        creator_email='owner@example.com',
        user_role='direktor',
    )
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()
    assert body['success'] is True
    assert body['final'] is True
    update_sqls = [sql for sql, _ in cursor.executed if 'UPDATE archive_requests' in sql]
    assert any("status = 'approved'" in s for s in update_sqls)


def test_approve_notification_label_from_authoritative_chain(app):
    """Notification approver label comes from APPROVAL_CHAINS, not stored chain."""
    resp, cursor = _run_approve(
        app,
        request_type='zahtev',
        status='pending',
        current_step=0,
        stored_chain=[],            # stored label gone -> would yield blank
        creator_email='owner@example.com',
        user_role='sef_odeljenja',
    )
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()
    assert body['success'] is True
    notif_params = _insert_params(cursor, 'user_notifications')
    assert notif_params is not None, "no creator notification inserted"
    # message is the 3rd column param: (user_email, title, message, icon, type)
    message = notif_params[2]
    assert 'Шеф одељења' in message, \
        "step label must come from APPROVAL_CHAINS even when stored chain is empty"


# ---------------------------------------------------------------------------
# Finding 2: self-approval / self-rejection guard.
# ---------------------------------------------------------------------------

def test_creator_cannot_approve_own_request(app):
    """A creator who also holds the approver role must be blocked (403)."""
    resp, cursor = _run_approve(
        app,
        request_type='zahtev',
        status='pending',
        current_step=0,
        stored_chain=APPROVAL_CHAIN_ZAHTEV(),
        creator_email='self@example.com',
        user_email='self@example.com',   # same as creator
        user_role='sef_odeljenja',
    )
    status = resp[1] if isinstance(resp, tuple) else 200
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()
    assert status == 403
    assert body['success'] is False
    # Must not have advanced/updated the request.
    assert not any('UPDATE archive_requests' in sql for sql, _ in cursor.executed)


def test_creator_cannot_reject_own_request(app):
    request_row = ('zahtev', 'pending', 0, APPROVAL_CHAIN_ZAHTEV(),
                   'self@example.com', 'Тест захтев')
    cursor = FakeCursor([
        ("FROM archive_requests WHERE id = %s", request_row, None),
        ("UPDATE approval_signatures", None, None),
        ("UPDATE archive_requests", None, None),
        ("INSERT INTO request_history", None, None),
        ("INSERT INTO user_notifications", None, None),
    ])
    with app.test_request_context('/api/archive/requests/1/reject',
                                  method='POST', json={'comments': 'no'}):
        from flask import session as flask_session
        flask_session['user_id'] = 1
        flask_session['user_email'] = 'self@example.com'
        flask_session['user_name'] = 'Self'
        flask_session['user_role'] = 'sef_odeljenja'
        with patch.object(asb, 'get_postgres_connection', lambda **kw: _conn_cm(cursor)):
            resp = asb.api_reject_archive_request(1)
    status = resp[1] if isinstance(resp, tuple) else 200
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()
    assert status == 403
    assert body['success'] is False
    assert not any('UPDATE archive_requests' in sql for sql, _ in cursor.executed)


def test_non_creator_approver_still_allowed(app):
    """A different user with the approver role must still be able to approve."""
    resp, cursor = _run_approve(
        app,
        request_type='zahtev',
        status='pending',
        current_step=0,
        stored_chain=APPROVAL_CHAIN_ZAHTEV(),
        creator_email='owner@example.com',
        user_email='boss@example.com',   # different from creator
        user_role='sef_odeljenja',
    )
    status = resp[1] if isinstance(resp, tuple) else 200
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()
    assert status != 403
    assert body['success'] is True


# ---------------------------------------------------------------------------
# Finding 3: concurrent approvals serialize via SELECT ... FOR UPDATE.
# ---------------------------------------------------------------------------

def test_approve_locks_request_row_for_update(app):
    resp, cursor = _run_approve(
        app,
        request_type='zahtev',
        status='pending',
        current_step=0,
        stored_chain=APPROVAL_CHAIN_ZAHTEV(),
        creator_email='owner@example.com',
        user_role='sef_odeljenja',
    )
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()
    assert body['success'] is True
    select_sqls = [sql for sql, _ in cursor.executed
                   if 'FROM archive_requests WHERE id = %s' in sql]
    assert select_sqls, "request row SELECT was not executed"
    assert any('FOR UPDATE' in s for s in select_sqls), \
        "the request row must be locked FOR UPDATE to serialize concurrent approvals"


def test_reject_locks_request_row_for_update(app):
    request_row = ('zahtev', 'pending', 0, APPROVAL_CHAIN_ZAHTEV(),
                   'owner@example.com', 'Тест захтев')
    cursor = FakeCursor([
        ("FROM archive_requests WHERE id = %s", request_row, None),
        ("UPDATE approval_signatures", None, None),
        ("UPDATE archive_requests", None, None),
        ("INSERT INTO request_history", None, None),
        ("INSERT INTO user_notifications", None, None),
    ])
    with app.test_request_context('/api/archive/requests/1/reject',
                                  method='POST', json={'comments': 'no'}):
        from flask import session as flask_session
        flask_session['user_id'] = 1
        flask_session['user_email'] = 'boss@example.com'
        flask_session['user_name'] = 'Boss'
        flask_session['user_role'] = 'sef_odeljenja'
        with patch.object(asb, 'get_postgres_connection', lambda **kw: _conn_cm(cursor)):
            resp = asb.api_reject_archive_request(1)
    body = (resp[0] if isinstance(resp, tuple) else resp).get_json()
    assert body['success'] is True
    select_sqls = [sql for sql, _ in cursor.executed
                   if 'FROM archive_requests WHERE id = %s' in sql]
    assert select_sqls, "request row SELECT was not executed"
    assert any('FOR UPDATE' in s for s in select_sqls), \
        "the request row must be locked FOR UPDATE to serialize concurrent rejections"


def APPROVAL_CHAIN_ZAHTEV():
    return list(asb.APPROVAL_CHAINS['zahtev'])
