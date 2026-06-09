#!/usr/bin/env python3
"""Regression tests for startup-time lazy loading improvements."""

import os
import subprocess
import sys
import json
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

os.environ['FLASK_ENV'] = 'testing'
os.environ['SECRET_KEY'] = 'test-secret'
os.environ['REDIS_URL'] = ''

import app as museum_app


def _assert_fresh_import_state(expression):
    """Import ``app`` in a pristine subprocess and assert ``expression`` there.

    These regressions guard the state of module-level globals *immediately
    after import*. When the whole suite runs in one process, earlier test
    modules may legitimately initialize this shared state, so the check must
    happen in a fresh interpreter to stay order-independent.
    """
    code = (
        "import os;"
        "os.environ.setdefault('FLASK_ENV', 'testing');"
        "os.environ.setdefault('SECRET_KEY', 'test-secret');"
        "os.environ.setdefault('REDIS_URL', '');"
        "import app;"
        f"assert {expression}, {expression!r}"
    )
    result = subprocess.run(
        [sys.executable, '-c', code],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__)),
        timeout=300,
    )
    if result.returncode != 0:
        raise AssertionError(
            f'fresh-import check failed: {expression}\n{result.stderr[-2000:]}'
        )


class StartupLazyLoadingTests(unittest.TestCase):
    def test_auth_service_stays_uninitialized_after_import(self):
        _assert_fresh_import_state('app.auth_system.initialized is False')

    def test_timesheet_service_stays_uninitialized_after_import(self):
        _assert_fresh_import_state('app.timesheet_repository.initialized is False')

    def test_module_access_state_stays_uninitialized_after_import(self):
        _assert_fresh_import_state('app._module_access_mtime is None')

    def test_dashboard_preferences_state_stays_uninitialized_after_import(self):
        _assert_fresh_import_state('app._dashboard_prefs_mtime is None')

    def test_login_tracker_stays_uninitialized_after_import(self):
        _assert_fresh_import_state('app._login_tracker_initialized is False')

    def test_fallback_employees_stay_uninitialized_after_import(self):
        _assert_fresh_import_state('app.MUSEUM_EMPLOYEES is None')

    def test_create_app_does_not_eagerly_load_library_database(self):
        original_library = museum_app.LIBRARY_DATABASE
        self.addCleanup(setattr, museum_app, 'LIBRARY_DATABASE', original_library)
        museum_app.LIBRARY_DATABASE = None

        with patch.object(museum_app, 'load_library_database', side_effect=AssertionError('library should stay lazy')):
            created_app = museum_app.create_app()

        self.assertIs(created_app, museum_app.app)
        self.assertIsNone(museum_app.LIBRARY_DATABASE)

    def test_lazy_loaded_dict_defers_loader_until_first_access(self):
        loader = Mock(return_value={'items': [1, 2, 3]})
        lazy_dict = museum_app.LazyLoadedDict(loader, 'test payload')

        loader.assert_not_called()
        self.assertEqual(lazy_dict['items'], [1, 2, 3])
        loader.assert_called_once()

    def test_news_refresh_rebuilds_types(self):
        lazy_dict = museum_app.LazyLoadedDict(museum_app.build_news_database, 'news database')

        with patch.object(
            museum_app,
            'load_news_data',
            side_effect=[
                [{'type': 'Вест'}],
                [{'type': 'Објава'}],
            ],
        ):
            self.assertEqual(lazy_dict['types'], ['Вест'])
            lazy_dict.refresh()
            self.assertEqual(lazy_dict['types'], ['Објава'])

    def test_vehicle_cache_loads_on_demand_and_reloads_explicitly(self):
        original_cache = museum_app._MUSEUM_VEHICLES_CACHE
        self.addCleanup(setattr, museum_app, '_MUSEUM_VEHICLES_CACHE', original_cache)
        museum_app._MUSEUM_VEHICLES_CACHE = None

        with patch.object(museum_app, 'load_vehicles', return_value=[{'id': 1}]) as mocked_loader:
            self.assertEqual(museum_app.get_museum_vehicles(), [{'id': 1}])
            self.assertEqual(mocked_loader.call_count, 1)

            self.assertEqual(museum_app.get_museum_vehicles(), [{'id': 1}])
            self.assertEqual(mocked_loader.call_count, 1)

            self.assertEqual(museum_app.get_museum_vehicles(force_reload=True), [{'id': 1}])
            self.assertEqual(mocked_loader.call_count, 2)

    def test_reservation_cache_loads_on_demand_and_reloads_explicitly(self):
        original_cache = museum_app._VEHICLE_RESERVATIONS_CACHE
        self.addCleanup(setattr, museum_app, '_VEHICLE_RESERVATIONS_CACHE', original_cache)
        museum_app._VEHICLE_RESERVATIONS_CACHE = None

        with patch.object(museum_app, 'load_reservations', return_value=[{'id': 9}]) as mocked_loader:
            self.assertEqual(museum_app.get_vehicle_reservations(), [{'id': 9}])
            self.assertEqual(mocked_loader.call_count, 1)

            self.assertEqual(museum_app.get_vehicle_reservations(), [{'id': 9}])
            self.assertEqual(mocked_loader.call_count, 1)

            self.assertEqual(museum_app.get_vehicle_reservations(force_reload=True), [{'id': 9}])
            self.assertEqual(mocked_loader.call_count, 2)

    def test_auth_proxy_initializes_on_first_access(self):
        proxy = museum_app.LazyServiceProxy(
            Mock(return_value=SimpleNamespace(available=True)),
            'auth proxy test',
        )

        self.assertFalse(proxy.initialized)
        self.assertTrue(proxy.available)
        self.assertTrue(proxy.initialized)

    def test_login_tracker_initializes_on_first_auth_use(self):
        original_state = museum_app._login_tracker_initialized
        self.addCleanup(setattr, museum_app, '_login_tracker_initialized', original_state)
        museum_app._login_tracker_initialized = False

        with patch.object(museum_app, 'init_login_tracker') as mocked_init:
            tracker = museum_app.ensure_login_tracker_initialized()

        mocked_init.assert_called_once()
        self.assertTrue(museum_app._login_tracker_initialized)
        self.assertIs(tracker, museum_app.login_tracker)

    def test_fallback_employee_cache_initializes_on_first_access(self):
        original_employees = museum_app.MUSEUM_EMPLOYEES
        self.addCleanup(setattr, museum_app, 'MUSEUM_EMPLOYEES', original_employees)
        museum_app.MUSEUM_EMPLOYEES = None

        with patch.object(museum_app, 'get_fallback_employees', return_value={'admin@example.com': {'user_id': 1}}) as mocked_loader:
            employees = museum_app.get_museum_employees()

        mocked_loader.assert_called_once()
        self.assertEqual(employees, {'admin@example.com': {'user_id': 1}})

    def test_timesheet_proxy_initializes_on_first_access(self):
        proxy = museum_app.LazyServiceProxy(
            Mock(return_value=SimpleNamespace(available=True, get_overall_summary=lambda: {})),
            'timesheet proxy test',
        )

        self.assertFalse(proxy.initialized)
        self.assertTrue(proxy.available)
        self.assertTrue(proxy.initialized)

    def test_module_access_loader_skips_reload_when_mtime_is_unchanged(self):
        original_modules = museum_app.MODULE_ACCESS
        original_mtime = museum_app._module_access_mtime
        self.addCleanup(setattr, museum_app, 'MODULE_ACCESS', original_modules)
        self.addCleanup(setattr, museum_app, '_module_access_mtime', original_mtime)

        museum_app.MODULE_ACCESS = {'cached': {'name': 'Cached'}}
        museum_app._module_access_mtime = 123.0

        with patch.object(museum_app, '_get_file_mtime', return_value=123.0):
            with patch('builtins.open', side_effect=AssertionError('should not reopen file')):
                loaded = museum_app.load_module_access()

        self.assertEqual(loaded, {'cached': {'name': 'Cached'}})

    def test_module_access_loader_refreshes_when_file_changes(self):
        original_file = museum_app.MODULE_ACCESS_FILE
        original_modules = museum_app.MODULE_ACCESS
        original_defaults = museum_app.MODULE_ACCESS_DEFAULTS
        original_mtime = museum_app._module_access_mtime
        self.addCleanup(setattr, museum_app, 'MODULE_ACCESS_FILE', original_file)
        self.addCleanup(setattr, museum_app, 'MODULE_ACCESS', original_modules)
        self.addCleanup(setattr, museum_app, 'MODULE_ACCESS_DEFAULTS', original_defaults)
        self.addCleanup(setattr, museum_app, '_module_access_mtime', original_mtime)

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'module_access.json')
            with open(path, 'w', encoding='utf-8') as handle:
                json.dump({'example': {'authorized_users': ['user@example.com']}}, handle)

            museum_app.MODULE_ACCESS_FILE = path
            museum_app.MODULE_ACCESS_DEFAULTS = {
                'example': {'authorized_users': [], 'restricted_users': [], 'name': 'Example'}
            }
            museum_app.MODULE_ACCESS = {}
            museum_app._module_access_mtime = None

            loaded = museum_app.load_module_access(force=True)

        self.assertEqual(loaded['example']['authorized_users'], ['user@example.com'])

    def test_dashboard_preferences_loader_skips_reload_when_mtime_is_unchanged(self):
        original_prefs = museum_app.DASHBOARD_PREFERENCES
        original_mtime = museum_app._dashboard_prefs_mtime
        self.addCleanup(setattr, museum_app, 'DASHBOARD_PREFERENCES', original_prefs)
        self.addCleanup(setattr, museum_app, '_dashboard_prefs_mtime', original_mtime)

        museum_app.DASHBOARD_PREFERENCES = {'cached@example.com': {'enabled_widgets': ['museum_databases']}}
        museum_app._dashboard_prefs_mtime = 456.0

        with patch.object(museum_app, '_get_file_mtime', return_value=456.0):
            with patch('builtins.open', side_effect=AssertionError('should not reopen file')):
                loaded = museum_app.load_dashboard_preferences()

        self.assertEqual(loaded['cached@example.com']['enabled_widgets'], ['museum_databases'])

    def test_dashboard_preferences_loader_refreshes_when_file_changes(self):
        original_file = museum_app.DASHBOARD_PREFS_FILE
        original_prefs = museum_app.DASHBOARD_PREFERENCES
        original_mtime = museum_app._dashboard_prefs_mtime
        self.addCleanup(setattr, museum_app, 'DASHBOARD_PREFS_FILE', original_file)
        self.addCleanup(setattr, museum_app, 'DASHBOARD_PREFERENCES', original_prefs)
        self.addCleanup(setattr, museum_app, '_dashboard_prefs_mtime', original_mtime)

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'dashboard_preferences.json')
            with open(path, 'w', encoding='utf-8') as handle:
                json.dump({'user@example.com': {'enabled_widgets': ['news']}}, handle)

            museum_app.DASHBOARD_PREFS_FILE = path
            museum_app.DASHBOARD_PREFERENCES = {}
            museum_app._dashboard_prefs_mtime = None

            loaded = museum_app.load_dashboard_preferences(force=True)

        self.assertEqual(loaded['user@example.com']['enabled_widgets'], ['news'])

    def test_get_user_modules_uses_freshly_loaded_preferences_on_first_call(self):
        stale_prefs = {'admin': {'enabled_widgets': ['museum_databases']}}
        stale_modules = {
            'museum_databases': {'name': 'Databases', 'description': 'db', 'icon': 'bi-database'},
            'timesheet': {'name': 'Timesheet', 'description': 'ts', 'icon': 'bi-calendar-check'},
        }
        fresh_prefs = {'admin': {'enabled_widgets': ['museum_databases', 'timesheet']}}
        fresh_modules = {
            'museum_databases': {'name': 'Databases', 'description': 'db', 'icon': 'bi-database'},
            'timesheet': {'name': 'Timesheet', 'description': 'ts', 'icon': 'bi-calendar-check'},
        }

        with patch.object(museum_app, 'DASHBOARD_PREFERENCES', stale_prefs), patch.object(
            museum_app,
            'MODULE_ACCESS',
            stale_modules,
        ), patch.object(
            museum_app,
            'load_dashboard_preferences',
            return_value=fresh_prefs,
        ), patch.object(
            museum_app,
            'load_module_access',
            return_value=fresh_modules,
        ), patch.object(
            museum_app,
            'user_has_module_access',
            side_effect=lambda user_email, user_role, module_key: True,
        ):
            modules = museum_app.get_user_modules('admin', 'admin')

        self.assertEqual([module['key'] for module in modules], ['museum_databases', 'timesheet'])

    def test_dashboard_response_disables_browser_caching(self):
        with museum_app.app.test_request_context('/dashboard'):
            museum_app.session['user_role'] = 'admin'
            museum_app.session['user_name'] = 'Admin User'
            museum_app.session['user_email'] = 'admin'

            response = museum_app.core_app_views.render_dashboard(
                get_user_modules=lambda user_email, user_role: [],
            )

        self.assertEqual(response.headers['Cache-Control'], 'no-cache, no-store, must-revalidate')
        self.assertEqual(response.headers['Pragma'], 'no-cache')
        self.assertEqual(response.headers['Expires'], '0')


if __name__ == '__main__':
    unittest.main()
