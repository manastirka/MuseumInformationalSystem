#!/usr/bin/env python3
"""Regression tests for projects-misc cluster (exhibition_planner_views)."""

import os
import unittest
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-projects-misc')

import app as museum_app
import exhibition_planner_views


class _FakeCursor:
    """Cursor that records executed SQL and replays scripted fetchone results."""

    def __init__(self, fetchone_results):
        self._fetchone_results = list(fetchone_results)
        self.executed = []

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchone(self):
        if self._fetchone_results:
            return self._fetchone_results.pop(0)
        return None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class _FakeConnection:
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


def _executed_update(cursor):
    return any('UPDATE exhibitions' in (query or '') for query, _ in cursor.executed)


class ExhibitionChecklistAuthTests(unittest.TestCase):
    def _run_checklist(self, cursor, *, user_email, user_role):
        @contextmanager
        def fake_conn(**kwargs):
            yield _FakeConnection(cursor)

        with museum_app.app.test_request_context(
            '/api/exhibitions/42/checklist',
            method='PUT',
            json={'phase1': True},
        ):
            from flask import session

            session['user_email'] = user_email
            session['user_role'] = user_role
            with patch.object(exhibition_planner_views, 'get_postgres_connection', fake_conn):
                return exhibition_planner_views.api_update_exhibition_checklist(42)

    def test_non_owner_cannot_overwrite_checklist(self):
        """A low-privilege user must not overwrite another owner's checklist (IDOR)."""
        cursor = _FakeCursor(
            fetchone_results=[
                {'id': 42, 'created_by_email': 'owner@example.com'},
            ]
        )
        response = self._run_checklist(
            cursor,
            user_email='attacker@example.com',
            user_role='employee',
        )

        status = response[1] if isinstance(response, tuple) else response.status_code
        self.assertEqual(status, 403)
        self.assertFalse(
            _executed_update(cursor),
            'checklist UPDATE must not run for a non-owner non-admin user',
        )

    def test_owner_can_update_checklist(self):
        cursor = _FakeCursor(
            fetchone_results=[
                {'id': 42, 'created_by_email': 'owner@example.com'},
                {'id': 42},
            ]
        )
        response = self._run_checklist(
            cursor,
            user_email='owner@example.com',
            user_role='employee',
        )

        status = response[1] if isinstance(response, tuple) else response.status_code
        self.assertEqual(status, 200)
        self.assertTrue(_executed_update(cursor))

    def test_admin_can_update_any_checklist(self):
        cursor = _FakeCursor(
            fetchone_results=[
                {'id': 42, 'created_by_email': 'owner@example.com'},
                {'id': 42},
            ]
        )
        response = self._run_checklist(
            cursor,
            user_email='admin@example.com',
            user_role='admin',
        )

        status = response[1] if isinstance(response, tuple) else response.status_code
        self.assertEqual(status, 200)
        self.assertTrue(_executed_update(cursor))

    def test_missing_exhibition_returns_404(self):
        cursor = _FakeCursor(fetchone_results=[None])
        response = self._run_checklist(
            cursor,
            user_email='owner@example.com',
            user_role='employee',
        )

        status = response[1] if isinstance(response, tuple) else response.status_code
        self.assertEqual(status, 404)
        self.assertFalse(_executed_update(cursor))


if __name__ == '__main__':
    unittest.main()
