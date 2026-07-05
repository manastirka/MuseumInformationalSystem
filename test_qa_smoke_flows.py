#!/usr/bin/env python3
"""QA smoke journeys for critical production flows."""

import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', 'logs/qa_flask_session')

import app as museum_app


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
    def __init__(self):
        self.executed = []

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeConnection:
    def __init__(self):
        self.cursor_obj = FakeCursor()
        self.committed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True

    def rollback(self):
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class QASmokeFlowTests(unittest.TestCase):
    def setUp(self):
        museum_app.app.config['TESTING'] = True
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def _login_session(self, *, email='user@example.com', role='employee', name='Test User'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = email
            sess['user_name'] = name
            sess['user_role'] = role
            sess['is_admin'] = role == 'admin'

    def test_login_dashboard_logout_journey(self):
        tracker = FakeTracker()
        authenticated_user = {
            'user_id': 7,
            'email': 'employee@example.com',
            'full_name': 'Employee User',
            'role': 'employee',
            'department': 'Geology',
        }

        fake_auth_system = SimpleNamespace(
            available=True,
            verify_credentials=MagicMock(return_value=authenticated_user),
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
        ), patch.object(
            museum_app.core_app_views,
            'render_template',
            return_value='dashboard-page',
        ), patch.object(
            museum_app,
            'get_user_dashboard_view',
            return_value={
                'modules': [{'key': 'timesheet', 'name': 'Timesheet'}],
                'sections': [],
            },
        ):
            login_response = self.client.post(
                '/login',
                data={'email': 'employee@example.com', 'password': 'ValidPass123!'},
                base_url=self.base_url,
            )
            self.assertEqual(login_response.status_code, 302)
            self.assertIn('/dashboard', login_response.location)

            with self.client.session_transaction() as sess:
                self.assertEqual(sess['user_email'], 'employee@example.com')
                self.assertEqual(sess['user_role'], 'employee')

            dashboard_response = self.client.get('/dashboard', base_url=self.base_url)
            self.assertEqual(dashboard_response.status_code, 200)
            self.assertEqual(dashboard_response.get_data(as_text=True), 'dashboard-page')

            logout_response = self.client.get('/logout', base_url=self.base_url)
            self.assertEqual(logout_response.status_code, 302)
            self.assertIn('/index', logout_response.location)

            with self.client.session_transaction() as sess:
                self.assertNotIn('user_email', sess)

        self.assertIn(('employee@example.com', True), tracker.attempts)

    def test_first_login_redirects_to_password_change(self):
        tracker = FakeTracker()
        authenticated_user = {
            'user_id': 11,
            'email': 'new.user@example.com',
            'full_name': 'New User',
            'role': 'employee',
            'is_first_login': True,
        }

        fake_auth_system = SimpleNamespace(
            available=True,
            verify_credentials=MagicMock(return_value=authenticated_user),
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
        ):
            response = self.client.post(
                '/login',
                data={'email': 'new.user@example.com', 'password': 'TempPass123!'},
                base_url=self.base_url,
            )

        self.assertEqual(response.status_code, 302)
        self.assertIn('/change_password', response.location)

    def test_rotated_session_namespace_requires_login_again(self):
        self._login_session(email='admin@nhmbeo.rs', role='admin', name='Admin User')
        original_prefix = museum_app.app.session_interface.key_prefix
        museum_app.app.session_interface.key_prefix = f'{original_prefix}boot:restart-test:'

        try:
            response = self.client.get('/dashboard', base_url=self.base_url)
        finally:
            museum_app.app.session_interface.key_prefix = original_prefix

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)

    def test_admin_password_reset_journey(self):
        self._login_session(email='admin@nhmbeo.rs', role='admin', name='Admin User')
        fake_conn = FakeConnection()

        with patch.object(
            museum_app.password_validator,
            'validate',
            return_value=(True, []),
        ), patch.object(
            museum_app.password_hasher,
            'hash_password',
            return_value=('hashed-password', 'salt'),
        ), patch.object(
            museum_app.admin_user_management_views,
            'get_postgres_connection',
            return_value=fake_conn,
        ), patch.object(
            museum_app,
            'log_security_event',
            MagicMock(),
        ) as log_event_mock:
            response = self.client.post(
                '/api/admin/password_manager/reset',
                json={
                    'email': 'employee@example.com',
                    'new_password': 'NewValidPass123!',
                    'force_change': True,
                },
                base_url=self.base_url,
            )

        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertTrue(body['success'])
        self.assertTrue(fake_conn.committed)
        self.assertTrue(fake_conn.cursor_obj.executed)
        log_event_mock.assert_called()

    def test_admin_science_news_crud_journey(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            news_file = Path(tmpdir) / 'science_news.json'

            self._login_session(email='admin@nhmbeo.rs', role='admin', name='Admin User')
            with patch.object(
                museum_app.depot_science_views,
                '_science_news_file',
                return_value=str(news_file),
            ):
                create_response = self.client.post(
                    '/api/science-news',
                    json={
                        'title': 'QA Science News',
                        'summary': 'Smoke test entry',
                        'category': 'geology',
                        'region': 'world',
                        'source': 'QA',
                    },
                    base_url=self.base_url,
                )
                self.assertEqual(create_response.status_code, 200)
                created = create_response.get_json()['news']
                self.assertEqual(created['title'], 'QA Science News')

                self._login_session(email='employee@example.com', role='employee', name='Employee User')
                list_response = self.client.get('/api/science-news', base_url=self.base_url)
                self.assertEqual(list_response.status_code, 200)
                listed = list_response.get_json()['news']
                self.assertEqual(len(listed), 1)
                self.assertEqual(listed[0]['id'], created['id'])

                self._login_session(email='admin@nhmbeo.rs', role='admin', name='Admin User')
                delete_response = self.client.delete(
                    f"/api/science-news/{created['id']}",
                    base_url=self.base_url,
                )
                self.assertEqual(delete_response.status_code, 200)
                self.assertTrue(delete_response.get_json()['success'])

                final_list_response = self.client.get('/api/science-news', base_url=self.base_url)
                self.assertEqual(final_list_response.status_code, 200)
                self.assertEqual(final_list_response.get_json()['news'], [])

    def test_locked_draft_timesheet_hides_save_actions(self):
        self._login_session(
            email='aleksandar@nhmbeo.rs',
            role='employee',
            name='Aleksandar Lukovic',
        )

        locked_timesheet = {
            'exists': True,
            'daily_data': {},
            'OPosao': '',
            'is_verified': False,
            'is_locked': True,
            'verified_by': None,
            'verified_at': None,
            'version': 1,
            'has_pending_request': False,
            'has_approved_request': False,
            'status': 'DRAFT',
            'submitted_at': None,
            'rejection_note': '',
            'report_id': 277,
        }

        with patch.object(
            museum_app.timesheet_employee_views,
            '_load_timesheet_entry_data',
            return_value=locked_timesheet,
        ), patch.object(
            museum_app.timesheet_employee_views,
            '_build_calendar_data',
            return_value=[],
        ), patch.object(
            museum_app.timesheet_employee_views,
            '_resolve_employee_profile',
            return_value=('Geology', 'Curator'),
        ), patch.object(
            museum_app.timesheet_employee_views,
            '_default_entry_period',
            return_value=(3, 2026),
        ), patch(
            'timesheet_postgres.ensure_draft_exists',
            return_value=277,
        ), patch(
            'timesheet_postgres.can_edit_timesheet_by_status',
            return_value=(True, ''),
        ), patch(
            'timesheet_postgres.can_submit_for_review',
            return_value=(True, ''),
        ):
            response = self.client.get('/timesheet/entry', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Радна листа је закључана. Потребно је одобрење администратора за измене.', html)
        self.assertIn('data-testid="timesheet-save"', html)
        self.assertIn('disabled', html)
        self.assertNotIn('onclick="saveTimesheet()"', html)

    def test_password_reset_db_outage_returns_server_error(self):
        self._login_session(email='admin@nhmbeo.rs', role='admin', name='Admin User')

        with patch.object(
            museum_app.password_validator,
            'validate',
            return_value=(True, []),
        ), patch.object(
            museum_app.password_hasher,
            'hash_password',
            return_value=('hashed-password', 'salt'),
        ), patch.object(
            museum_app.admin_user_management_views,
            'get_postgres_connection',
            side_effect=RuntimeError('database unavailable'),
        ):
            response = self.client.post(
                '/api/admin/password_manager/reset',
                json={
                    'email': 'employee@example.com',
                    'new_password': 'NewValidPass123!',
                },
                base_url=self.base_url,
            )

        self.assertEqual(response.status_code, 500)
        body = response.get_json()
        self.assertFalse(body['success'])


if __name__ == '__main__':
    unittest.main()
