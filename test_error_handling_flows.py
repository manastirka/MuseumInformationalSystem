#!/usr/bin/env python3
"""Regression tests for outage handling and sanitized error responses."""

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


class ErrorHandlingFlowTests(unittest.TestCase):
    def setUp(self):
        museum_app.app.config['TESTING'] = True
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def _login(self, *, email='user@example.com', role='employee'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = email
            sess['user_name'] = 'QA User'
            sess['user_role'] = role
            sess['is_admin'] = role == 'admin'

    def test_weather_details_returns_safe_fallback_on_forecast_failure(self):
        self._login()

        with patch.object(
            museum_app,
            'get_current_weather',
            return_value={'condition': 'clear', 'temperature': 20, 'windspeed': 3},
        ), patch.object(
            museum_app,
            'get_weather_forecast',
            side_effect=RuntimeError('weather backend token=secret'),
        ), patch.object(
            museum_app,
            'get_rhmz_weather_warnings',
            return_value={'has_warning': False, 'sections': []},
        ):
            response = self.client.get('/api/weather/details', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'Неке временске податке тренутно није могуће учитати.')
        self.assertEqual(body['current']['condition'], 'clear')
        self.assertNotIn('secret', response.get_data(as_text=True))

    def test_website_news_hides_upstream_failure_details(self):
        self._login()
        with patch.object(
            museum_app,
            'fetch_website_news',
            side_effect=RuntimeError('rss parse failed for secret-host'),
        ):
            response = self.client.get('/api/website-news', base_url=self.base_url)

        self.assertEqual(response.status_code, 500)
        body = response.get_json()
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'Није могуће учитати вести са сајта.')
        self.assertEqual(body['news'], [])
        self.assertNotIn('secret-host', response.get_data(as_text=True))

    def test_nhm_search_hides_upstream_failure_details(self):
        self._login()
        fake_nhm = SimpleNamespace(
            get_status=lambda: {'connected': True},
            search_datasets=MagicMock(side_effect=RuntimeError('nhm api key leaked')),
        )

        with patch('nhm_data_portal_api.get_nhm_api', return_value=fake_nhm):
            response = self.client.get('/api/nhm/search?q=fossil', base_url=self.base_url)

        self.assertEqual(response.status_code, 500)
        body = response.get_json()
        self.assertFalse(body['success'])
        self.assertEqual(body['error'], 'Грешка при претрази NHM података')
        self.assertNotIn('api key', response.get_data(as_text=True))

    def test_mail_init_hides_backend_failure_details(self):
        self._login(email='employee@example.com', role='employee')

        with patch('mail_client.MailClient', side_effect=RuntimeError('imap://secret-host offline')):
            response = self.client.get('/api/mail/init', base_url=self.base_url)

        self.assertEqual(response.status_code, 500)
        body = response.get_json()
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'Грешка при повезивању на сервер поште.')
        self.assertNotIn('secret-host', response.get_data(as_text=True))

    def test_admin_password_reset_hides_database_failure_details(self):
        self._login(email='admin@nhmbeo.rs', role='admin')

        with patch.object(
            museum_app.password_validator,
            'validate',
            return_value=(True, []),
        ), patch.object(
            museum_app.password_hasher,
            'hash_password',
            return_value=('hash', 'salt'),
        ), patch.object(
            museum_app.admin_user_management_views,
            'get_postgres_connection',
            side_effect=RuntimeError('postgres://secret-db down'),
        ), patch.object(
            museum_app,
            'log_security_event',
            MagicMock(),
        ):
            response = self.client.post(
                '/api/admin/password_manager/reset',
                json={
                    'email': 'employee@example.com',
                    'new_password': 'StrongPass123!',
                    'force_change': True,
                },
                base_url=self.base_url,
            )

        self.assertEqual(response.status_code, 500)
        body = response.get_json()
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'Грешка при ресетовању лозинке.')
        self.assertNotIn('secret-db', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
