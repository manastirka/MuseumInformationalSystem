#!/usr/bin/env python3
"""Tests for the personalized home dashboard with per-role element filtering.

Covers: role-based element filtering (including rejection of a forged POST
with forbidden elements), the default four elements for a regular employee,
and behavior when a saved configuration references elements the user can no
longer access (role change).
"""

import os
import unittest
from copy import deepcopy
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

import app as museum_app
import dashboard_config_support

REGULAR_EMAIL = 'test.zaposleni@nhmbeo.rs'
SOCIAL_MARKER = 'Facebook - Природњачки музеј'
WEBSITE_NEWS_MARKER = 'website-news-container'
QUICK_ACTIONS_MARKER = 'Брзе акције'
TIMESHEET_MARKER = 'Систем за радне листе'
MINERAL_MARKER = 'База минерала'
MINERAL_QUICK_ACTION_MARKER = 'Претрага минерала'
SYSTEM_LOGS_MARKER = 'Системски логови'


class DashboardElementFilteringTests(unittest.TestCase):
    def setUp(self):
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

        self.saved_elements = None
        patchers = [
            patch.object(
                museum_app,
                'load_module_access',
                lambda force=False: deepcopy(museum_app.MODULE_ACCESS_DEFAULTS),
            ),
            patch.object(museum_app, 'load_dashboard_preferences', lambda force=False: {}),
            patch.object(museum_app, 'get_employee_directory', lambda: []),
            patch.object(
                museum_app,
                'load_user_dashboard_elements',
                lambda user_email: self.saved_elements,
            ),
        ]
        for patcher in patchers:
            patcher.start()
            self.addCleanup(patcher.stop)

    def _login(self, *, email=REGULAR_EMAIL, role='kustos'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = email
            sess['user_name'] = 'Test Korisnik'
            sess['user_role'] = role
            sess['is_admin'] = role == 'admin'

    def _get_dashboard(self):
        response = self.client.get('/dashboard', base_url=self.base_url)
        self.assertEqual(response.status_code, 200)
        return response.get_data(as_text=True)

    # --- Requirement 2: default four elements for a regular employee ---

    def test_regular_user_gets_default_four_elements(self):
        self._login()
        html = self._get_dashboard()

        self.assertIn(TIMESHEET_MARKER, html)
        self.assertIn('Музејске вести', html)
        self.assertIn(WEBSITE_NEWS_MARKER, html)
        self.assertIn(QUICK_ACTIONS_MARKER, html)

        self.assertNotIn(SOCIAL_MARKER, html)
        self.assertNotIn(MINERAL_MARKER, html)
        self.assertNotIn(MINERAL_QUICK_ACTION_MARKER, html)

    def test_director_keeps_full_view(self):
        self._login(email='direktor@nhmbeo.rs', role='direktor')
        html = self._get_dashboard()

        self.assertIn(SOCIAL_MARKER, html)
        self.assertIn(WEBSITE_NEWS_MARKER, html)
        self.assertIn(QUICK_ACTIONS_MARKER, html)
        self.assertIn(TIMESHEET_MARKER, html)
        self.assertIn(MINERAL_MARKER, html)
        self.assertIn(MINERAL_QUICK_ACTION_MARKER, html)

    def test_department_head_keeps_full_view_of_allowed_modules(self):
        self._login(email='sef.bio@nhmbeo.rs', role='sef_odeljenja')
        html = self._get_dashboard()

        self.assertIn(SOCIAL_MARKER, html)
        self.assertIn(WEBSITE_NEWS_MARKER, html)
        self.assertIn(QUICK_ACTIONS_MARKER, html)
        self.assertIn(TIMESHEET_MARKER, html)
        self.assertNotIn(MINERAL_MARKER, html)

    def test_admin_keeps_existing_default_widget(self):
        self._login(email='admin', role='admin')
        html = self._get_dashboard()

        self.assertIn(SOCIAL_MARKER, html)
        self.assertIn('Музејске базе података', html)
        self.assertNotIn(MINERAL_MARKER, html)

    # --- Requirement 1: role change / stale saved config is skipped at render ---

    def test_saved_forbidden_element_is_skipped_at_render(self):
        self.saved_elements = ['mineral_database', 'timesheet', 'website_news']
        self._login()
        html = self._get_dashboard()

        self.assertNotIn(MINERAL_MARKER, html)
        self.assertIn(TIMESHEET_MARKER, html)
        self.assertIn(WEBSITE_NEWS_MARKER, html)
        self.assertNotIn(QUICK_ACTIONS_MARKER, html)
        self.assertNotIn(SOCIAL_MARKER, html)

    def test_same_saved_config_shows_element_for_authorized_role(self):
        self.saved_elements = ['mineral_database', 'timesheet', 'website_news']
        self._login(email='direktor@nhmbeo.rs', role='direktor')
        html = self._get_dashboard()

        self.assertIn(MINERAL_MARKER, html)
        self.assertIn(TIMESHEET_MARKER, html)

    def test_legacy_preferences_keep_sections_visible(self):
        with patch.object(
            museum_app,
            'load_dashboard_preferences',
            lambda force=False: {REGULAR_EMAIL: {'enabled_widgets': ['timesheet']}},
        ):
            self._login()
            html = self._get_dashboard()

        self.assertIn(SOCIAL_MARKER, html)
        self.assertIn(WEBSITE_NEWS_MARKER, html)
        self.assertIn(QUICK_ACTIONS_MARKER, html)
        self.assertIn(TIMESHEET_MARKER, html)


class CustomizeDashboardTests(unittest.TestCase):
    def setUp(self):
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

        csrf_was_enabled = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.addCleanup(
            museum_app.app.config.__setitem__, 'WTF_CSRF_ENABLED', csrf_was_enabled
        )

        self.saved_calls = []

        def fake_save(user_email, elements):
            self.saved_calls.append((user_email, list(elements)))
            return True

        patchers = [
            patch.object(
                museum_app,
                'load_module_access',
                lambda force=False: deepcopy(museum_app.MODULE_ACCESS_DEFAULTS),
            ),
            patch.object(museum_app, 'load_dashboard_preferences', lambda force=False: {}),
            patch.object(museum_app, 'get_employee_directory', lambda: []),
            patch.object(museum_app, 'load_user_dashboard_elements', lambda user_email: None),
            patch.object(museum_app, 'save_user_dashboard_elements', fake_save),
        ]
        for patcher in patchers:
            patcher.start()
            self.addCleanup(patcher.stop)

    def _login(self, *, email=REGULAR_EMAIL, role='kustos'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = email
            sess['user_name'] = 'Test Korisnik'
            sess['user_role'] = role
            sess['is_admin'] = role == 'admin'

    def test_customize_offers_only_allowed_elements(self):
        self._login()
        response = self.client.get('/dashboard/customize', base_url=self.base_url)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)

        self.assertIn(QUICK_ACTIONS_MARKER, html)
        self.assertIn(TIMESHEET_MARKER, html)
        self.assertNotIn(SYSTEM_LOGS_MARKER, html)
        self.assertNotIn(MINERAL_MARKER, html)

    def test_customize_offers_everything_to_admin(self):
        self._login(email='admin', role='admin')
        response = self.client.get('/dashboard/customize', base_url=self.base_url)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)

        self.assertIn(SYSTEM_LOGS_MARKER, html)
        self.assertIn(MINERAL_MARKER, html)

    def test_forged_post_with_forbidden_element_is_rejected(self):
        self._login()
        response = self.client.post(
            '/dashboard/customize',
            data={'widgets': ['system_logs', 'timesheet']},
            base_url=self.base_url,
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.saved_calls, [])

    def test_forged_post_with_unknown_element_is_rejected(self):
        self._login()
        response = self.client.post(
            '/dashboard/customize',
            data={'widgets': ['nepostojeci_element']},
            base_url=self.base_url,
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.saved_calls, [])

    def test_valid_post_saves_selection(self):
        self._login()
        response = self.client.post(
            '/dashboard/customize',
            data={'widgets': ['timesheet', 'news', 'website_news', 'quick_actions']},
            base_url=self.base_url,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.saved_calls,
            [(REGULAR_EMAIL, ['timesheet', 'news', 'website_news', 'quick_actions'])],
        )


class ResolveEnabledElementsUnitTests(unittest.TestCase):
    def test_default_four_for_regular_employee(self):
        allowed = ['social_feeds', 'website_news', 'quick_actions', 'timesheet', 'news']
        enabled = dashboard_config_support.resolve_enabled_elements(
            REGULAR_EMAIL,
            'kustos',
            allowed_keys=allowed,
            saved_elements=None,
            legacy_enabled_widgets=None,
            admin_widget_users=['admin'],
            module_keys=['timesheet', 'news', 'mineral_database'],
        )
        self.assertEqual(
            sorted(enabled),
            sorted(['timesheet', 'news', 'website_news', 'quick_actions']),
        )

    def test_saved_elements_filtered_by_current_access(self):
        enabled = dashboard_config_support.resolve_enabled_elements(
            REGULAR_EMAIL,
            'kustos',
            allowed_keys=['website_news', 'timesheet'],
            saved_elements=['mineral_database', 'timesheet', 'website_news'],
            legacy_enabled_widgets=None,
            admin_widget_users=['admin'],
            module_keys=['timesheet', 'mineral_database'],
        )
        self.assertEqual(enabled, ['timesheet', 'website_news'])

    def test_privileged_role_defaults_to_full_view(self):
        allowed = ['social_feeds', 'website_news', 'quick_actions', 'timesheet', 'news']
        enabled = dashboard_config_support.resolve_enabled_elements(
            'sef.bio@nhmbeo.rs',
            'sef_odeljenja',
            allowed_keys=allowed,
            saved_elements=None,
            legacy_enabled_widgets=None,
            admin_widget_users=['admin'],
            module_keys=['timesheet', 'news', 'mineral_database'],
        )
        self.assertEqual(sorted(enabled), sorted(allowed))


if __name__ == '__main__':
    unittest.main()
