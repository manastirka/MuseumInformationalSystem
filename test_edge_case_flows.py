#!/usr/bin/env python3
"""Targeted edge-case regressions for auth and admin approval flows."""

import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', 'logs/qa_flask_session')

import app as museum_app
import archive_signature_blueprint


class FakeTracker:
    def __init__(self):
        self.attempts = []

    def is_locked_out(self, email, max_attempts, lockout_duration):
        return False, None

    def record_attempt(self, email, success):
        self.attempts.append((email, success))

    def get_remaining_attempts(self, email, max_attempts):
        return max_attempts - 1


class FakeCursor:
    def __init__(self, fetchone_values=None, fetchall_values=None, rowcount=1):
        self.fetchone_values = list(fetchone_values or [])
        self.fetchall_values = list(fetchall_values or [])
        self.executed = []
        self.rowcount = rowcount

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchone(self):
        if not self.fetchone_values:
            return None
        return self.fetchone_values.pop(0)

    def fetchall(self):
        if not self.fetchall_values:
            return []
        return self.fetchall_values.pop(0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor
        self.committed = False

    def cursor(self):
        return self._cursor

    def commit(self):
        self.committed = True

    def rollback(self):
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class EdgeCaseFlowTests(unittest.TestCase):
    def setUp(self):
        museum_app.app.config['TESTING'] = True
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def _login(self, *, email='user@example.com', role='employee', name='QA User'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = email
            sess['user_name'] = name
            sess['user_role'] = role
            sess['is_admin'] = role == 'admin'

    def test_login_failure_keeps_session_empty_and_records_failed_attempt(self):
        tracker = FakeTracker()
        fake_auth_system = SimpleNamespace(
            available=True,
            verify_credentials=MagicMock(return_value=None),
        )

        with patch.object(
            museum_app,
            'auth_system',
            fake_auth_system,
        ), patch.object(
            museum_app,
            'ensure_login_tracker_initialized',
            return_value=tracker,
        ), patch.object(
            museum_app,
            'log_security_event',
            MagicMock(),
        ) as log_event_mock, patch.object(
            museum_app.core_app_views,
            'render_template',
            return_value='login-page',
        ):
            response = self.client.post(
                '/login',
                data={'email': 'employee@example.com', 'password': 'WrongPass123!'},
                base_url=self.base_url,
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), 'login-page')
        with self.client.session_transaction() as sess:
            self.assertNotIn('user_email', sess)
        self.assertIn(('employee@example.com', False), tracker.attempts)
        log_event_mock.assert_called_with(
            'login_failed',
            {'email': 'employee@example.com', 'remaining_attempts': 4},
        )

    def test_admin_timesheet_approve_missing_report_returns_safe_payload(self):
        self._login(email='admin@nhmbeo.rs', role='admin', name='Admin User')
        fake_cursor = FakeCursor(fetchone_values=[None])

        with patch.object(
            museum_app,
            'timesheet_repository',
            SimpleNamespace(available=True),
        ), patch.object(
            museum_app.timesheet_admin_views,
            'get_postgres_connection',
            return_value=FakeConnection(fake_cursor),
        ):
            response = self.client.post(
                '/api/admin/timesheet/report/999/approve',
                json={'approve': True},
                base_url=self.base_url,
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {'success': False, 'message': 'Извештај није пронађен'},
        )

    def test_admin_batch_approve_rejects_oversized_payload(self):
        self._login(email='admin@nhmbeo.rs', role='admin', name='Admin User')

        with patch.object(
            museum_app,
            'timesheet_repository',
            SimpleNamespace(available=True),
        ):
            response = self.client.post(
                '/api/admin/timesheet/reports/batch-approve',
                json={'report_ids': list(range(1, 102)), 'approve': True},
                base_url=self.base_url,
            )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {'success': False, 'message': 'Максимално 100 извештаја одједном'},
        )

    def test_archive_approve_missing_request_returns_404(self):
        self._login(email='employee@example.com', role='employee')
        fake_cursor = FakeCursor(fetchone_values=[None])

        with patch.object(
            archive_signature_blueprint,
            'get_postgres_connection',
            return_value=FakeConnection(fake_cursor),
        ):
            response = self.client.post(
                '/api/archive/requests/999/approve',
                json={'comments': 'QA approval'},
                base_url=self.base_url,
            )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json(),
            {'success': False, 'message': 'Захтев није пронађен'},
        )

    def test_archive_approve_blocks_user_without_current_step_permission(self):
        self._login(email='employee@example.com', role='employee')
        fake_cursor = FakeCursor(fetchone_values=[('zahtev', 'pending', 0, ['admin'])])

        with patch.object(
            archive_signature_blueprint,
            'get_postgres_connection',
            return_value=FakeConnection(fake_cursor),
        ), patch.object(
            archive_signature_blueprint,
            'can_approve_request',
            return_value=False,
        ):
            response = self.client.post(
                '/api/archive/requests/12/approve',
                json={'comments': 'QA approval'},
                base_url=self.base_url,
            )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.get_json(),
            {'success': False, 'message': 'Немате дозволу за одобрење у овој фази'},
        )


if __name__ == '__main__':
    unittest.main()
