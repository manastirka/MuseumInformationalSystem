#!/usr/bin/env python3
"""Regression tests for production-readiness fixes."""

import os
import sys
import json
import io
import shutil
import tempfile
import types
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from flask import Flask, jsonify, session
from PIL import Image

import config as config_module
import security_utils
import image_storage_engine
import image_api
import module_access_support
import collection_management_views
import app_access_support
import admin_system_views
import admin_user_management_views
import fallback_auth_support
import mail_client
import mail_views
import core_app_views
import dashboard_data_support
import travel_finance_views


class FakeLogger:
    def __init__(self):
        self.calls = []

    def error(self, message, extra=None):
        self.calls.append(('error', message, extra))

    def warning(self, message, extra=None):
        self.calls.append(('warning', message, extra))

    def info(self, message, extra=None):
        self.calls.append(('info', message, extra))

    def debug(self, message, extra=None):
        self.calls.append(('debug', message, extra))


class ConfigTests(unittest.TestCase):
    def test_default_config_is_production(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertIs(config_module.get_config(None), config_module.ProductionConfig)

    def test_base_config_disables_fallback_auth_by_default(self):
        module_path = Path(config_module.__file__)
        spec = importlib.util.spec_from_file_location('config_reloaded', module_path)
        reloaded = importlib.util.module_from_spec(spec)

        with patch.dict(os.environ, {}, clear=True):
            spec.loader.exec_module(reloaded)

        self.assertFalse(reloaded.Config.ENABLE_FALLBACK_AUTH)

    def test_production_config_requires_secret_key(self):
        app = Flask(__name__)
        app.config.from_object(config_module.ProductionConfig)
        app.config['SECRET_KEY'] = None

        with patch.dict(os.environ, {'WORKERS': '1', 'REDIS_URL': 'redis://redis:6379/0'}, clear=False):
            with self.assertRaises(RuntimeError):
                config_module.ProductionConfig.init_app(app)

    def test_production_config_requires_redis_url(self):
        app = Flask(__name__)
        app.config.from_object(config_module.ProductionConfig)
        app.config['SECRET_KEY'] = 'production-secret'

        with patch.dict(os.environ, {'WORKERS': '1', 'REDIS_URL': ''}, clear=False):
            with self.assertRaises(RuntimeError):
                config_module.ProductionConfig.init_app(app)

    def test_production_config_requires_redis_session_type(self):
        app = Flask(__name__)
        app.config.from_object(config_module.ProductionConfig)
        app.config['SECRET_KEY'] = 'production-secret'

        with patch.dict(
            os.environ,
            {'WORKERS': '1', 'REDIS_URL': 'redis://redis:6379/0', 'SESSION_TYPE': 'filesystem'},
            clear=False,
        ):
            with self.assertRaises(RuntimeError):
                config_module.ProductionConfig.init_app(app)

    def test_production_config_tolerates_missing_syslog(self):
        app = Flask(__name__)
        app.config.from_object(config_module.ProductionConfig)
        app.config['SECRET_KEY'] = 'production-secret'

        with patch.dict(
            os.environ,
            {'WORKERS': '1', 'REDIS_URL': 'redis://redis:6379/0', 'SESSION_TYPE': 'redis'},
            clear=False,
        ):
            with patch('logging.handlers.SysLogHandler', side_effect=PermissionError('no syslog')):
                config_module.ProductionConfig.init_app(app)

    def test_production_config_uses_redis_rate_limit_with_multiple_workers(self):
        app = Flask(__name__)
        app.config.from_object(config_module.ProductionConfig)
        app.config['SECRET_KEY'] = 'production-secret'
        app.config['RATELIMIT_STORAGE_URL'] = 'memory://'

        with patch.dict(
            os.environ,
            {'WORKERS': '4', 'REDIS_URL': 'redis://redis:6379/0', 'SESSION_TYPE': 'redis'},
            clear=False,
        ):
            with patch('logging.handlers.SysLogHandler', side_effect=PermissionError('no syslog')):
                config_module.ProductionConfig.init_app(app)

        self.assertEqual(app.config['RATELIMIT_STORAGE_URL'], 'redis://redis:6379/0')

    def test_gunicorn_config_does_not_run_as_developer_account(self):
        content = Path('gunicorn.conf.py').read_text(encoding='utf-8')
        self.assertIn("user = os.environ.get('GUNICORN_RUN_USER', 'www-data')", content)
        self.assertIn("group = os.environ.get('GUNICORN_RUN_GROUP', 'www-data')", content)
        self.assertNotIn("user = 'aleksandarlukovic'", content)
        self.assertNotIn("group = 'aleksandarlukovic'", content)

    def test_service_files_do_not_run_as_developer_account(self):
        service_content = Path('museum-system.service').read_text(encoding='utf-8')
        self.assertIn('User=www-data', service_content)
        self.assertIn('Group=www-data', service_content)
        self.assertNotIn('User=aleksandarlukovic', service_content)
        self.assertNotIn('Group=aleksandarlukovic', service_content)

        control_center_content = Path('museum_control_center.py').read_text(encoding='utf-8')
        self.assertIn('User=www-data', control_center_content)
        self.assertIn('Group=www-data', control_center_content)

    def test_start_production_script_safely_loads_env_and_requires_secret_key(self):
        content = Path('start_production.sh').read_text(encoding='utf-8')
        self.assertIn('load_env_file()', content)
        self.assertIn('Malformed .env entry', content)
        self.assertIn('if [ -z "${SECRET_KEY}" ]; then', content)
        self.assertIn('SECRET_KEY uses an insecure placeholder value', content)
        self.assertNotIn("export $(cat .env | grep -v '^#' | xargs)", content)

    def test_production_config_defaults_rate_limit_storage_to_redis(self):
        app = Flask(__name__)
        app.config.from_object(config_module.ProductionConfig)
        app.config['SECRET_KEY'] = 'production-secret'
        app.config['RATELIMIT_STORAGE_URL'] = 'memory://'

        with patch.dict(
            os.environ,
            {'WORKERS': '1', 'REDIS_URL': 'redis://redis:6379/0', 'SESSION_TYPE': 'redis'},
            clear=False,
        ):
            with patch('logging.handlers.SysLogHandler', side_effect=PermissionError('no syslog')):
                config_module.ProductionConfig.init_app(app)

        self.assertEqual(app.config['RATELIMIT_STORAGE_URL'], 'redis://redis:6379/0')
        self.assertEqual(app.config['SESSION_TYPE'], 'redis')


class SecurityUtilsTests(unittest.TestCase):
    def test_init_login_tracker_preserves_object_identity(self):
        original_tracker = security_utils.login_tracker
        configured_tracker = security_utils.init_login_tracker(None)

        self.assertIs(original_tracker, configured_tracker)

    def test_init_login_tracker_passes_redis_url(self):
        original_tracker = security_utils.login_tracker
        fake_tracker = types.SimpleNamespace(use_redis=True, redis_client='client', attempts={}, lockouts={})

        with patch('security_utils.LoginAttemptTracker', return_value=fake_tracker) as tracker_cls:
            configured_tracker = security_utils.init_login_tracker('redis://redis:6379/0')

        tracker_cls.assert_called_once_with(redis_url='redis://redis:6379/0')
        self.assertIs(configured_tracker, original_tracker)
        self.assertTrue(configured_tracker.use_redis)

    def test_module_access_required_uses_current_app_checker(self):
        app = Flask(__name__)
        app.secret_key = 'test-secret'
        app.user_has_module_access = lambda email, role, module_key: (
            email == 'user@example.com' and role == 'user' and module_key == 'maps'
        )

        @app.route('/api/protected')
        @security_utils.module_access_required('maps')
        def protected():
            return jsonify({'success': True})

        client = app.test_client()
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = 'user@example.com'
            sess['user_role'] = 'user'

        response = client.get('/api/protected')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'success': True})

    def test_log_security_event_uses_user_email_session_key(self):
        app = Flask(__name__)
        app.secret_key = 'test-secret'
        fake_logger = FakeLogger()

        with app.test_request_context('/login'):
            session['user_email'] = 'audit@example.com'

            with patch('logging.getLogger', return_value=fake_logger):
                security_utils.log_security_event('login_success', {'email': 'audit@example.com'})

        self.assertTrue(fake_logger.calls)
        _, _, extra = fake_logger.calls[0]
        self.assertEqual(extra['user_email'], 'audit@example.com')


class SpecialtyModuleAccessTests(unittest.TestCase):
    def setUp(self):
        self.module_access = {
            'museum_databases': {'default_access': False, 'authorized_users': []},
            'curator_collections': {'default_access': False, 'authorized_users': []},
            'botany_collection': {'default_access': False, 'authorized_users': []},
            'ornithology_collection': {'default_access': False, 'authorized_users': []},
            'petrology_collection': {'default_access': False, 'authorized_users': []},
            'bird_ringing_database': {'default_access': False, 'authorized_users': []},
            'library_database': {'default_access': False, 'authorized_users': []},
            'maps_karte': {'default_access': False, 'authorized_users': []},
        }

    def test_botanist_only_gets_matching_specialty_modules(self):
        employee_directory = [{
            'email': 'botanicar@nhmbeo.rs',
            'department': 'Биолошко одељење',
            'position': 'Ботаничар кустос',
            'description': 'Истраживање флоре Србије и хербаријума',
        }]

        self.assertTrue(app_access_support.user_has_module_access(
            'botanicar@nhmbeo.rs',
            'employee',
            'botany_collection',
            load_module_access=lambda: self.module_access,
            module_access=self.module_access,
            resolved_module_access=self.module_access,
            resolved_employee_directory=employee_directory,
        ))
        self.assertTrue(app_access_support.user_has_module_access(
            'botanicar@nhmbeo.rs',
            'employee',
            'museum_databases',
            load_module_access=lambda: self.module_access,
            module_access=self.module_access,
            resolved_module_access=self.module_access,
            resolved_employee_directory=employee_directory,
        ))
        self.assertFalse(app_access_support.user_has_module_access(
            'botanicar@nhmbeo.rs',
            'employee',
            'petrology_collection',
            load_module_access=lambda: self.module_access,
            module_access=self.module_access,
            resolved_module_access=self.module_access,
            resolved_employee_directory=employee_directory,
        ))

    def test_petrolog_gets_geology_but_not_biology_modules(self):
        employee_directory = [{
            'email': 'petrolog@nhmbeo.rs',
            'department': 'Геолошко одељење',
            'position': 'Петролог',
            'description': 'Петролошка и геолошка истраживања',
        }]

        self.assertTrue(app_access_support.user_has_module_access(
            'petrolog@nhmbeo.rs',
            'employee',
            'petrology_collection',
            load_module_access=lambda: self.module_access,
            module_access=self.module_access,
            resolved_module_access=self.module_access,
            resolved_employee_directory=employee_directory,
        ))
        self.assertTrue(app_access_support.user_has_module_access(
            'petrolog@nhmbeo.rs',
            'employee',
            'maps_karte',
            load_module_access=lambda: self.module_access,
            module_access=self.module_access,
            resolved_module_access=self.module_access,
            resolved_employee_directory=employee_directory,
        ))
        self.assertFalse(app_access_support.user_has_module_access(
            'petrolog@nhmbeo.rs',
            'employee',
            'botany_collection',
            load_module_access=lambda: self.module_access,
            module_access=self.module_access,
            resolved_module_access=self.module_access,
            resolved_employee_directory=employee_directory,
        ))

    def test_curator_collections_umbrella_tracks_any_matching_collection(self):
        employee_directory = [{
            'email': 'ornitolog@nhmbeo.rs',
            'department': 'Биолошко одељење',
            'position': 'Орнитолог',
            'description': 'Прстеновање птица и орнитолошка збирка',
        }]

        self.assertTrue(app_access_support.user_has_module_access(
            'ornitolog@nhmbeo.rs',
            'employee',
            'curator_collections',
            load_module_access=lambda: self.module_access,
            module_access=self.module_access,
            resolved_module_access=self.module_access,
            resolved_employee_directory=employee_directory,
        ))
        self.assertTrue(app_access_support.user_has_module_access(
            'ornitolog@nhmbeo.rs',
            'employee',
            'bird_ringing_database',
            load_module_access=lambda: self.module_access,
            module_access=self.module_access,
            resolved_module_access=self.module_access,
            resolved_employee_directory=employee_directory,
        ))


class NotificationTemplateRegressionTests(unittest.TestCase):
    def test_admin_panel_uses_real_notification_api_instead_of_sample_data(self):
        content = Path('templates/admin_panel.html').read_text(encoding='utf-8')

        self.assertIn("fetch('/api/notifications')", content)
        self.assertIn("fetch('/api/notifications/read'", content)
        self.assertIn("fetch('/api/notifications/clear'", content)
        self.assertNotIn('Sample notifications - replace with API call', content)
        self.assertNotIn("Нови радни лист", content)

    def test_notification_bell_posts_use_csrf_token(self):
        """POST requests in notificationBell must include CSRF token via secureFetch."""
        content = Path('templates/base.html').read_text(encoding='utf-8')
        import re
        bell_match = re.search(
            r'function notificationBell\(\)\s*\{(.*?)\n    \}',
            content,
            re.DOTALL,
        )
        self.assertIsNotNone(bell_match, "notificationBell function not found in base.html")
        bell_body = bell_match.group(1)
        post_fetches = re.findall(r"(?:fetch|secureFetch)\('/api/notifications/\w+'", bell_body)
        self.assertTrue(len(post_fetches) >= 2, "Expected at least 2 POST fetch calls in notificationBell")
        for call in post_fetches:
            self.assertTrue(
                call.startswith('secureFetch'),
                f"POST to notification API must use secureFetch, not raw fetch: {call}",
            )


class ProcurementRequestTemplateTests(unittest.TestCase):
    def test_nabavka_print_keeps_form_content_visible(self):
        content = Path('templates/finansije/zahtev_nabavka.html').read_text(encoding='utf-8')

        self.assertIn('function printForm()', content)
        self.assertIn('window.print();', content)
        self.assertIn('.content-wrapper {', content)
        self.assertIn('display: block !important;', content)
        self.assertNotIn('.sidebar, .navbar, .footer, .no-print, .sidebar-toggle, .content-wrapper {', content)
        self.assertNotIn("id=\"doublePrintLayout\"", content)
        self.assertNotIn('buildPrintCopies();', content)

    def test_nabavka_print_uses_compact_portrait_layout(self):
        content = Path('templates/finansije/zahtev_nabavka.html').read_text(encoding='utf-8')

        self.assertIn('size: A4 portrait;', content)
        self.assertIn('margin: 5mm;', content)
        self.assertIn('.print-form .card-body {', content)
        self.assertIn('.signature-box {', content)
        self.assertIn('min-height: 24px !important;', content)
        self.assertIn('zoom: 0.82;', content)
        self.assertIn('.table-responsive {', content)
        self.assertIn('border: 1px solid #c7ced6 !important;', content)
        self.assertIn('border-color: #cfd6dd !important;', content)
        self.assertNotIn('.print-sheet-double .print-form {', content)


class DashboardCustomizationPreferenceTests(unittest.TestCase):
    def test_customize_dashboard_defaults_admin_to_museum_databases_only(self):
        app = Flask(__name__)
        app.secret_key = 'test-secret'

        module_access = {
            'museum_databases': {'name': 'Baze', 'description': 'desc', 'icon': 'bi-db'},
            'timesheet': {'name': 'Timesheet', 'description': 'desc', 'icon': 'bi-clock'},
        }

        with app.test_request_context('/dashboard/customize'):
            session['user_email'] = 'admin@example.com'
            session['user_role'] = 'admin'

            with patch('admin_user_management_views.render_template', return_value='ok') as render_mock:
                result = admin_user_management_views.customize_dashboard_preferences(
                    load_dashboard_preferences=lambda: {},
                    load_module_access=lambda: module_access,
                    user_has_module_access=lambda email, role, key: True,
                    load_saved_elements=lambda email: None,
                    save_user_elements=lambda email, elements: True,
                    dashboard_endpoint='dashboard',
                )

        self.assertEqual(result, 'ok')
        self.assertEqual(
            render_mock.call_args.kwargs['enabled_widgets'],
            ['social_feeds', 'website_news', 'quick_actions', 'museum_databases'],
        )

    def test_customize_dashboard_filters_saved_widgets_to_available_modules(self):
        app = Flask(__name__)
        app.secret_key = 'test-secret'

        module_access = {
            'museum_databases': {'name': 'Baze', 'description': 'desc', 'icon': 'bi-db'},
            'timesheet': {'name': 'Timesheet', 'description': 'desc', 'icon': 'bi-clock'},
        }
        prefs = {
            'user@example.com': {
                'enabled_widgets': ['timesheet', 'missing_module'],
            }
        }

        with app.test_request_context('/dashboard/customize'):
            session['user_email'] = 'user@example.com'
            session['user_role'] = 'employee'

            with patch('admin_user_management_views.render_template', return_value='ok') as render_mock:
                result = admin_user_management_views.customize_dashboard_preferences(
                    load_dashboard_preferences=lambda: prefs,
                    load_module_access=lambda: module_access,
                    user_has_module_access=lambda email, role, key: key != 'museum_databases',
                    load_saved_elements=lambda email: None,
                    save_user_elements=lambda email, elements: True,
                    dashboard_endpoint='dashboard',
                )

        self.assertEqual(result, 'ok')
        self.assertEqual(
            render_mock.call_args.kwargs['enabled_widgets'],
            ['social_feeds', 'website_news', 'quick_actions', 'timesheet'],
        )

    def test_customize_dashboard_post_saves_selection_per_user(self):
        app = Flask(__name__)
        app.secret_key = 'test-secret'

        module_access = {
            'timesheet': {'name': 'Timesheet', 'description': 'desc', 'icon': 'bi-clock'},
            'news': {'name': 'Vesti', 'description': 'desc', 'icon': 'bi-newspaper'},
        }
        saved = {}

        def save_user_elements(email, elements):
            saved[email] = list(elements)
            return True

        with app.test_request_context(
            '/dashboard/customize',
            method='POST',
            data={'widgets': ['timesheet', 'news']},
        ):
            session['user_email'] = 'user@example.com'
            session['user_role'] = 'employee'

            with patch('admin_user_management_views.redirect', side_effect=lambda location: location), patch(
                'admin_user_management_views.url_for',
                side_effect=lambda endpoint: f'/{endpoint}',
            ), patch('admin_user_management_views.flash'):
                result = admin_user_management_views.customize_dashboard_preferences(
                    load_dashboard_preferences=lambda: {},
                    load_module_access=lambda: module_access,
                    user_has_module_access=lambda email, role, key: True,
                    load_saved_elements=lambda email: None,
                    save_user_elements=save_user_elements,
                    dashboard_endpoint='dashboard',
                )

        self.assertEqual(result, '/dashboard')
        self.assertEqual(saved, {'user@example.com': ['timesheet', 'news']})


class CollectionCuratorDisplayTests(unittest.TestCase):
    def test_placeholder_curator_email_is_replaced_with_real_collection_curators(self):
        records = [
            {'catalog_number': 'ENT-001', 'curator': 'goran.petkovski@nhmbeo.rs'},
        ]

        normalized = collection_management_views.normalize_collection_curators_for_display('entomology', records)

        self.assertEqual(
            normalized[0]['curator'],
            'Милош Јовић, Александар Стојановић',
        )

    def test_real_curator_email_is_displayed_as_employee_name(self):
        records = [
            {'catalog_number': 'BOT-001', 'curator': 'mniketic@nhmbeo.rs'},
        ]

        normalized = collection_management_views.normalize_collection_curators_for_display('botany', records)

        self.assertEqual(normalized[0]['curator'], 'Марјан Никетић')


class VacationRequestTemplateTests(unittest.TestCase):
    def test_vacation_request_days_are_derived_from_date_range(self):
        content = Path('templates/zahtevi/zahtev_godisnji_odmor.html').read_text(encoding='utf-8')

        self.assertIn('id="brojDana"', content)
        self.assertIn('readonly', content)
        self.assertIn('function calculateVacationDays()', content)
        self.assertIn("document.getElementById('odDatuma').addEventListener('input', syncVacationDaysWithRange);", content)
        self.assertIn("document.getElementById('doDatuma').addEventListener('input', syncVacationDaysWithRange);", content)


class OperationalModuleDraftStorageTests(unittest.TestCase):
    def test_base_template_exposes_user_scoped_draft_helpers(self):
        content = Path('templates/base.html').read_text(encoding='utf-8')

        self.assertIn('const CURRENT_USER_EMAIL =', content)
        self.assertIn('function buildUserScopedStorageKey(namespace, scope = \'\')', content)
        self.assertIn('function saveUserScopedDraft(namespace, data, scope = \'\')', content)
        self.assertIn('function loadUserScopedDraft(namespace, scope = \'\')', content)

    def test_base_template_uses_admin_only_overview_and_approval_sidebar_links(self):
        content = Path('templates/base.html').read_text(encoding='utf-8')

        self.assertIn('url_for(\'archive_signature.admin_archive_dashboard\')', content)
        self.assertIn('url_for(\'approval_center.centar_odobravanje\')', content)
        self.assertIn('url_for(\'approval_center.arhiva\')', content)
        self.assertNotIn('url_for(\'archive_signature.admin_archive_approvals\')', content)
        self.assertNotIn('url_for(\'archive_signature.admin_archive_finansije\')', content)
        self.assertNotIn('url_for(\'archive_signature.admin_archive_terenska\')', content)

    def test_operational_documents_use_user_scoped_draft_storage(self):
        template_paths = [
            'templates/zahtevi/zahtev_slobodan_dan.html',
            'templates/zahtevi/zahtev_godisnji_odmor.html',
            'templates/zahtevi/zahtev_razno.html',
            'templates/finansije/finansijski_plan.html',
            'templates/finansije/zahtev_nabavka.html',
        ]

        for template_path in template_paths:
            with self.subTest(template_path=template_path):
                content = Path(template_path).read_text(encoding='utf-8')
                self.assertIn('saveUserScopedDraft(', content)
                self.assertIn('loadUserScopedDraft(', content)

    def test_business_trip_template_intentionally_resets_on_refresh(self):
        content = Path('templates/zahtevi/zahtev_sluzbeni_put.html').read_text(encoding='utf-8')

        self.assertIn('removeUserScopedDraft(BUSINESS_TRIP_DRAFT_NAMESPACE);', content)
        self.assertIn('function resetBusinessTripFormState()', content)
        self.assertNotIn('saveUserScopedDraft(BUSINESS_TRIP_DRAFT_NAMESPACE', content)


class DashboardWeatherSupportTests(unittest.TestCase):
    FORECAST_HTML = """
    <html><body>
      <table>
        <tr>
          <td>BEOGRAD</td><td>UTORAK</td><td>SREDA</td><td>ČETVRTAK</td><td>PETAK</td><td>SUBOTA</td>
        </tr>
        <tr>
          <td></td><td>07.04.2026.</td><td>08.04.2026.</td><td>09.04.2026.</td><td>10.04.2026.</td><td>11.04.2026.</td>
        </tr>
        <tr>
          <td>Prognoza ažurirana:</td><td colspan="5">06.04. 11:00.</td>
        </tr>
        <tr>
          <td>Maks. temperatura: (°C)</td><td>20</td><td>16</td><td>14</td><td>12</td><td>12</td>
        </tr>
        <tr>
          <td>Min. temperatura: (°C)</td><td>10</td><td>7</td><td>5</td><td>4</td><td>3</td>
        </tr>
        <tr>
          <td>Pojava:</td>
          <td><img src="/icons/suncano.gif" alt="Pojava"></td>
          <td><img src="/icons/slaba_kisa.gif" alt="Pojava"></td>
          <td><img src="/icons/oblacno.gif" alt="Pojava"></td>
          <td><img src="/icons/pljusak_i_grmljavina.gif" alt="Pojava"></td>
          <td><img src="/icons/sneg.gif" alt="Pojava"></td>
        </tr>
      </table>
    </body></html>
    """
    OBSERVED_HTML = """
    <html><body>
      <div>Podaci ažurirani: 10:22 10.02.2026</div>
      <table>
        <tr>
          <th>Stanica</th><th>Temperatura</th><th>Pritisak</th><th>Pravac vetra</th><th>Brzina vetra</th><th>Vlažnost</th><th>Subjektivni osećaj</th><th>Simbol</th><th>Opis vremena</th>
        </tr>
        <tr>
          <td>Beograd</td><td>12</td><td>1012</td><td>ESE</td><td>4</td><td>80</td><td>9</td><td></td><td>Oblačno</td>
        </tr>
      </table>
      <table>
        <tr>
          <th>Stanica</th><th>Vreme</th><th>Temp.</th><th>Prit.</th><th>Vlažnost</th><th>Vetar pravac</th><th>Vetar brzina</th><th>Detaljnije</th>
        </tr>
        <tr>
          <td>Košutnjak</td><td>01:15</td><td>10.5</td><td>996.8</td><td>41</td><td>147</td><td>2.5</td><td>Detaljnije</td>
        </tr>
      </table>
    </body></html>
    """

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self._original_weather_cache_path = dashboard_data_support._WEATHER_FORECAST_CACHE_PATH
        dashboard_data_support._WEATHER_FORECAST_CACHE_PATH = Path(self._tmpdir.name) / 'weather_forecast_daily_cache.json'
        dashboard_data_support._weather_cache['data'] = None
        dashboard_data_support._weather_cache['timestamp'] = None
        dashboard_data_support._weather_cache['cache_date'] = None
        dashboard_data_support._weather_forecast_cache['data'] = None
        dashboard_data_support._weather_forecast_cache['timestamp'] = None
        dashboard_data_support._weather_forecast_cache['cache_date'] = None
        dashboard_data_support._weather_daily_bundle_cache['data'] = None
        dashboard_data_support._weather_daily_bundle_cache['timestamp'] = None
        dashboard_data_support._weather_daily_bundle_cache['cache_date'] = None

    def tearDown(self):
        dashboard_data_support._WEATHER_FORECAST_CACHE_PATH = self._original_weather_cache_path
        self._tmpdir.cleanup()

    def _make_html_response(self, html):
        response = MagicMock()
        response.raise_for_status.return_value = None
        response.text = html
        return response

    def _mock_rhmz_cycle(self):
        return [
            self._make_html_response(self.FORECAST_HTML),
            self._make_html_response(self.OBSERVED_HTML),
        ]

    def test_get_current_weather_uses_rhmz_observed_and_forecast_payloads(self):
        with patch('dashboard_data_support.requests.get', side_effect=self._mock_rhmz_cycle()) as get_mock:
            result = dashboard_data_support.get_current_weather()

        self.assertEqual(get_mock.call_count, 2)
        self.assertEqual(result['condition'], 'cloudy')
        self.assertEqual(result['description'], 'Облачно')
        self.assertEqual(result['temperature'], 12)
        self.assertEqual(result['windspeed'], 14.4)

    def test_get_current_weather_quick_returns_fallback_without_network_refresh(self):
        with patch('dashboard_data_support.requests.get') as get_mock:
            result = dashboard_data_support.get_current_weather_quick()

        get_mock.assert_not_called()
        self.assertEqual(result['condition'], dashboard_data_support.DEFAULT_WEATHER_CONDITION)
        self.assertIsNone(result['temperature'])
        self.assertIsNone(result['windspeed'])

    def test_default_weather_cache_path_uses_runtime_directory(self):
        with patch.dict(os.environ, {}, clear=True):
            cache_path = dashboard_data_support._default_weather_cache_path()

        self.assertEqual(cache_path.name, 'weather_forecast_daily_cache.json')
        self.assertIn(tempfile.gettempdir(), str(cache_path))

    def test_get_weather_forecast_reuses_same_day_disk_cache_without_api_call(self):
        today_key = dashboard_data_support.datetime.now().strftime('%Y-%m-%d')
        cached_payload = {
            'cache_date': today_key,
            'saved_at': dashboard_data_support.datetime.now().isoformat(timespec='seconds'),
            'data': {
                'location': 'Београд',
                'current': {
                    'condition': 'cloudy',
                    'temperature': 17,
                    'windspeed': 11,
                    'description': 'Облачно',
                },
                'days': [
                    {
                        'date': '2026-04-07',
                        'short_label': 'Уто',
                        'day_name': 'Уторак',
                        'date_label': '07.04.',
                        'condition': 'cloudy',
                        'description': 'Облачно',
                        'temp_max': 18,
                        'temp_min': 9,
                        'precipitation_probability': 20,
                        'windspeed': 14,
                    }
                ],
                'updated_at': '07.04.2026. 08:00',
                'source': 'RHMZ Србије',
            },
        }
        dashboard_data_support.write_json_file(dashboard_data_support._WEATHER_FORECAST_CACHE_PATH, cached_payload)

        with patch('dashboard_data_support.requests.get') as get_mock:
            result = dashboard_data_support.get_weather_forecast(days=1)

        get_mock.assert_not_called()
        self.assertEqual(len(result['days']), 1)
        self.assertEqual(result['days'][0]['condition'], 'cloudy')
        self.assertEqual(result['source'], 'RHMZ Србије')

    def test_get_weather_forecast_returns_stale_disk_cache_when_api_fails(self):
        cached_payload = {
            'cache_date': '2026-04-06',
            'saved_at': '2026-04-06T08:00:00',
            'data': {
                'location': 'Београд',
                'current': {
                    'condition': 'rain',
                    'temperature': 8,
                    'windspeed': 18,
                    'description': 'Умерена киша',
                },
                'days': [
                    {
                        'date': '2026-04-06',
                        'short_label': 'Пон',
                        'day_name': 'Понедељак',
                        'date_label': '06.04.',
                        'condition': 'rain',
                        'description': 'Умерена киша',
                        'temp_max': 12,
                        'temp_min': 6,
                        'precipitation_probability': 80,
                        'windspeed': 19,
                    }
                ],
                'updated_at': '06.04.2026. 08:00',
                'source': 'RHMZ Србије',
            },
        }
        dashboard_data_support.write_json_file(dashboard_data_support._WEATHER_FORECAST_CACHE_PATH, cached_payload)

        with patch(
            'dashboard_data_support.requests.get',
            side_effect=RuntimeError('rhmz unavailable'),
        ):
            result = dashboard_data_support.get_weather_forecast(days=1)

        self.assertTrue(result['stale'])
        self.assertEqual(len(result['days']), 1)
        self.assertEqual(result['days'][0]['condition'], 'rain')

    def test_get_weather_forecast_ignores_permission_error_on_disk_read(self):
        with patch('dashboard_data_support.load_json_file', side_effect=PermissionError('denied')), \
             patch('dashboard_data_support.requests.get', side_effect=self._mock_rhmz_cycle()) as get_mock:
            result = dashboard_data_support.get_weather_forecast(days=2)

        self.assertEqual(get_mock.call_count, 2)
        self.assertEqual(len(result['days']), 2)
        self.assertEqual(result['source'], 'RHMZ Србије')

    def test_get_weather_forecast_ignores_permission_error_on_disk_write(self):
        with patch('dashboard_data_support.write_json_file', side_effect=PermissionError('denied')), \
             patch('dashboard_data_support.requests.get', side_effect=self._mock_rhmz_cycle()) as get_mock:
            result = dashboard_data_support.get_weather_forecast(days=2)

        self.assertEqual(get_mock.call_count, 2)
        self.assertEqual(len(result['days']), 2)
        self.assertEqual(result['days'][0]['condition'], 'clear')

    def test_current_and_forecast_share_one_daily_api_call(self):
        with patch('dashboard_data_support.requests.get', side_effect=self._mock_rhmz_cycle()) as get_mock:
            current = dashboard_data_support.get_current_weather()
            forecast = dashboard_data_support.get_weather_forecast(days=2)

        self.assertEqual(get_mock.call_count, 2)
        self.assertEqual(current['condition'], 'cloudy')
        self.assertEqual(forecast['days'][0]['condition'], 'clear')
        self.assertEqual(len(forecast['days']), 2)

    def test_parse_rhmz_observed_page_falls_back_to_kosutnjak_when_beograd_missing_values(self):
        observed_html = """
        <html><body>
          <div>Podaci ažurirani: 06:07 12.03.2026</div>
          <table>
            <tr><td>Beograd</td><td>-</td><td>1010</td><td>NW</td><td>-</td><td>70</td><td>-</td><td></td><td>-</td></tr>
          </table>
          <table>
            <tr><td>Košutnjak</td><td>01:15</td><td>10.5</td><td>996.8</td><td>41</td><td>147</td><td>2.5</td><td>Detaljnije</td></tr>
          </table>
        </body></html>
        """

        result = dashboard_data_support._parse_rhmz_observed_page(observed_html)

        self.assertEqual(result['temperature'], 10.5)
        self.assertEqual(result['windspeed'], 9)
        self.assertEqual(result['description'], '')


class FinancialPlanSupportTests(unittest.TestCase):
    def test_financial_plan_totals_ignore_exhibition_metadata_and_sum_selected_year(self):
        totals_by_year, grand_total = travel_finance_views._financial_plan_totals(
            {
                'selectedYear': '2028',
                'years': {
                    '2028': {
                        'exhibition': {
                            'name': 'Minerali Srbije',
                            'place': 'Beograd',
                            'time': 'Maj',
                        },
                        'oprema': [{'activity': 'Vitrina', 'amount': 120000}],
                        'projekti': [{'activity': 'Terenski rad', 'amount': 30000}],
                    }
                },
            }
        )

        self.assertEqual(totals_by_year, {'2028': 150000})
        self.assertEqual(grand_total, 150000)

    def test_build_financial_plan_document_renders_only_selected_year(self):
        document = travel_finance_views._build_financial_plan_document(
            {
                'odeljenjeText': 'Геолошко',
                'kustos': 'Тест Корисник',
                'datumIzrade': '2026-04-07',
                'selectedYear': '2028',
                'years': {
                    '2028': {
                        'oprema': [{'rbr': 1, 'activity': 'Витрина', 'amount': 120000}],
                    },
                    '2029': {
                        'oprema': [{'rbr': 1, 'activity': 'Стара ставка', 'amount': 555}],
                    },
                },
            }
        )

        paragraph_text = '\n'.join(paragraph.text for paragraph in document.paragraphs)
        self.assertIn('Година: 2028', paragraph_text)
        self.assertNotIn('Година: 2029', paragraph_text)

    def test_financial_plan_save_updates_existing_owned_plan(self):
        cursor = MagicMock()
        cursor.__enter__.return_value = cursor
        cursor.__exit__.return_value = False
        cursor.fetchone.side_effect = [('owner@example.com',), (7,)]

        connection = MagicMock()
        connection.__enter__.return_value = connection
        connection.__exit__.return_value = False
        connection.cursor.return_value = cursor

        app = Flask(__name__)
        app.secret_key = 'test-secret'

        payload = {
            'id': 7,
            'kustos': 'Тест Корисник',
            'odeljenje': 'geolosko',
            'odeljenjeText': 'Геолошко',
            'datumIzrade': '2026-04-07',
            'selectedYear': '2028',
            'years': {
                '2028': {
                    'oprema': [{'activity': 'Витрина', 'amount': 120000}],
                }
            },
        }

        with app.test_request_context('/api/finansijski-plan/save', method='POST', json=payload):
            session['user_email'] = 'owner@example.com'
            session['user_role'] = 'employee'
            response = travel_finance_views.api_finansijski_plan_save(
                get_postgres_connection=lambda: connection,
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()['updated'])
        self.assertEqual(response.get_json()['id'], 7)
        executed_queries = [call.args[0] for call in cursor.execute.call_args_list]
        self.assertTrue(any('UPDATE financial_plans' in query for query in executed_queries))


class BusinessTripSupportTests(unittest.TestCase):
    def test_business_trip_template_uses_location_inputs_for_route_trigger(self):
        content = Path('templates/zahtevi/zahtev_sluzbeni_put.html').read_text(encoding='utf-8')

        self.assertIn("if (this.value && getLocations().length > 0) {", content)
        self.assertNotIn("document.getElementById('lokacija').value", content)

    def test_business_trip_template_uses_osm_route_planner_without_google_scripts(self):
        content = Path('templates/zahtevi/zahtev_sluzbeni_put.html').read_text(encoding='utf-8')

        self.assertIn('function openOpenStreetMap()', content)
        self.assertIn('https://unpkg.com/leaflet@1.9.4/dist/leaflet.js', content)
        self.assertIn("secureFetch('/api/osm/route-preview'", content)
        self.assertIn('function applyOsmRouteToForm()', content)
        self.assertIn('id="osmRouteModal"', content)
        self.assertIn('id="selectedLocationsSummary"', content)
        self.assertIn('class="form-control form-control-sm osm-route-stop-input"', content)
        self.assertIn('removeUserScopedDraft(BUSINESS_TRIP_DRAFT_NAMESPACE);', content)
        self.assertIn('resetBusinessTripFormState();', content)
        self.assertNotIn('maps.googleapis.com', content)
        self.assertNotIn('google.maps', content)
        self.assertNotIn('openMapPlanner', content)
        self.assertNotIn('mapModal', content)
        self.assertNotIn('Подаци са Google Maps', content)
        self.assertNotIn('https://nominatim.openstreetmap.org/search', content)
        self.assertNotIn('https://router.project-osrm.org/route/v1/driving/', content)

    def test_business_trip_template_uses_manual_accommodation_fields(self):
        content = Path('templates/zahtevi/zahtev_sluzbeni_put.html').read_text(encoding='utf-8')

        self.assertIn('id="accommodationName"', content)
        self.assertIn('id="accommodationLocation"', content)
        self.assertIn('id="accommodationPrice"', content)
        self.assertIn('id="accommodationNights"', content)
        self.assertIn('function getManualAccommodationData()', content)
        self.assertNotIn('function searchAccommodation()', content)
        self.assertNotIn('id="accommodationResults"', content)
        self.assertNotIn('Претражи смештај', content)

    def test_business_trip_template_does_not_double_kilometers_for_fuel_cost(self):
        content = Path('templates/zahtevi/zahtev_sluzbeni_put.html').read_text(encoding='utf-8')

        self.assertIn('const liters = Math.round(km * vehicle.consumption / 100 * 10) / 10;', content)
        self.assertNotIn('const liters = Math.round((km * 2) * vehicle.consumption / 100 * 10) / 10;', content)

    def test_business_trip_accommodation_search_endpoint_removed(self):
        blueprint_content = Path('blueprints/travel_finance.py').read_text(encoding='utf-8')
        content = Path('travel_finance_views.py').read_text(encoding='utf-8')

        self.assertNotIn('/api/accommodation/search', blueprint_content)
        self.assertNotIn('def api_accommodation_search()', content)
        self.assertNotIn('https://maps.googleapis.com/maps/api/place/textsearch/json', content)
        self.assertNotIn('Google Places', content)

    def test_business_trip_uses_official_2026_toll_tariff_subset(self):
        self.assertEqual(travel_finance_views.TOLL_PRICES_FROM_BELGRADE['SUBOTICA'], 850)
        self.assertEqual(travel_finance_views.TOLL_PRICES_FROM_BELGRADE['ČAČAK (PAKOVRAĆE)'], 720)
        self.assertEqual(travel_finance_views.TOLL_PRICES_FROM_BELGRADE['KRUŠEVAC ZAPAD'], 970)
        self.assertEqual(travel_finance_views.TOLL_PRICES_FROM_BELGRADE['BELA PALANKA'], 1430)
        self.assertEqual(travel_finance_views.TOLL_PRICES_FROM_BELGRADE['PIROT'], 1570)

    def test_route_calculation_uses_updated_official_pirot_toll(self):
        app = Flask(__name__)
        app.secret_key = 'test-secret'

        with app.test_request_context(
            '/api/route/calculate',
            method='POST',
            json={'destinations': ['Pirot'], 'vehicle_id': None},
        ):
            response = travel_finance_views.api_route_calculate(
                get_museum_vehicles=lambda: [],
            )

        body = response.get_json()
        self.assertTrue(body['success'])
        self.assertEqual(body['toll_outbound'], 1570)
        self.assertEqual(body['toll_return'], 1570)
        self.assertEqual(body['toll_round_trip'], 3140)

    def test_admin_archive_dashboard_includes_financial_plan_overview(self):
        content = Path('templates/admin_archive_dashboard.html').read_text(encoding='utf-8')

        self.assertIn('Финансијски планови запослених', content)
        self.assertIn("fetch('/api/finansijski-plan/list')", content)
        self.assertIn("financialPlans.summary.year2026", content)
        self.assertIn("`/finansije/plan?plan_id=${plan.id}`", content)
        self.assertIn('get classifiedDocs()', content)
        self.assertNotIn('Нови захтев', content)
        self.assertNotIn('showNewRequestModal', content)

    def test_admin_archive_approvals_groups_documents_by_type(self):
        content = Path('templates/admin_archive_approvals.html').read_text(encoding='utf-8')

        self.assertIn('get groupedPending()', content)
        self.assertIn('Одсуства, разно и општи захтеви.', content)
        self.assertIn('Финансијски планови и остали финансијски документи.', content)
        self.assertIn('Путни и теренски документи.', content)

    def test_financial_plan_template_supports_plan_id_query_param(self):
        content = Path('templates/finansije/finansijski_plan.html').read_text(encoding='utf-8')

        self.assertIn("new URLSearchParams(window.location.search).get('plan_id')", content)
        self.assertIn('loadPlan(parseInt(planIdFromUrl, 10));', content)

    def test_osm_route_preview_proxies_geocoding_and_routing_server_side(self):
        app = Flask(__name__)
        app.secret_key = 'test-secret'

        geocode_payload = [
            [{'lat': '44.8176', 'lon': '20.4633', 'display_name': 'Природњачки музеј, Београд'}],
            [{'lat': '43.8914', 'lon': '20.3497', 'display_name': 'Чачак, Србија'}],
            [{'lat': '44.8176', 'lon': '20.4633', 'display_name': 'Природњачки музеј, Београд'}],
        ]
        route_payload = {
            'routes': [
                {
                    'distance': 300000,
                    'duration': 14400,
                    'geometry': {'type': 'LineString', 'coordinates': [[20.46, 44.81], [20.34, 43.89]]},
                    'legs': [
                        {'distance': 150000, 'duration': 7200},
                        {'distance': 150000, 'duration': 7200},
                    ],
                }
            ]
        }

        def fake_get(url, **kwargs):
            response = MagicMock()
            response.raise_for_status.return_value = None
            if 'nominatim.openstreetmap.org/search' in url:
                response.json.return_value = geocode_payload.pop(0)
                return response
            if 'router.project-osrm.org/route/v1/driving/' in url:
                response.json.return_value = route_payload
                return response
            raise AssertionError(f'Unexpected URL: {url}')

        with app.test_request_context(
            '/api/osm/route-preview',
            method='POST',
            json={'locations': ['Čačak']},
        ):
            with patch.object(travel_finance_views.http_requests, 'get', side_effect=fake_get):
                response = travel_finance_views.api_osm_route_preview()

        body = response.get_json()
        self.assertTrue(body['success'])
        self.assertEqual(len(body['resolved_points']), 3)
        self.assertEqual(body['route']['distance'], 300000)
        self.assertEqual(len(body['route']['legs']), 2)

    def test_field_trip_create_does_not_try_to_reserve_private_vehicle(self):
        app = Flask(__name__)
        app.secret_key = 'test-secret'
        saved_reservations = []

        with app.test_request_context(
            '/api/field-trip/create',
            method='POST',
            json={
                'vehicle_id': 'sopstveni',
                'start_date': '2026-04-08',
                'end_date': '2026-04-09',
                'location': 'Ђердап',
                'purpose': 'Теренски рад',
                'update_timesheet': False,
            },
        ):
            session['user_email'] = 'user@example.com'
            session['user_name'] = 'Test User'
            # Direct field-trip creation is an admin/direktor operator path;
            # ordinary users go through the approval framework.
            session['user_role'] = 'direktor'

            response = travel_finance_views.api_field_trip_create(
                get_vehicle_reservations=lambda: saved_reservations,
                save_reservations=lambda: self.fail('Private vehicle must not create a museum reservation'),
            )

        body = response.get_json()
        self.assertTrue(body['success'])
        self.assertFalse(body['vehicle_reserved'])
        self.assertEqual(saved_reservations, [])


class ModuleAccessSupportTests(unittest.TestCase):
    def setUp(self):
        module_access_support._db_setting_failure_cache.clear()

    def test_load_db_json_setting_backs_off_after_failure(self):
        get_postgres_connection = MagicMock(side_effect=RuntimeError('db unavailable'))

        # Pad baze se sada diže kao SharedSettingsUnavailable (nikad tihi None),
        # a backoff i dalje sprečava ponovni pokušaj ka bazi unutar intervala.
        with self.assertRaises(module_access_support.SharedSettingsUnavailable):
            module_access_support._load_db_json_setting(
                get_postgres_connection=get_postgres_connection,
                setting_key='system_settings',
            )
        with self.assertRaises(module_access_support.SharedSettingsUnavailable):
            module_access_support._load_db_json_setting(
                get_postgres_connection=get_postgres_connection,
                setting_key='system_settings',
            )

        self.assertEqual(get_postgres_connection.call_count, 1)


class CoreAuthFlowTests(unittest.TestCase):
    def test_fallback_auth_returns_canonical_admin_email(self):
        user = fallback_auth_support.authenticate_fallback_user(
            'admin',
            'secret',
            app_config={
                'ENABLE_FALLBACK_AUTH': True,
                'ADMIN_EMAIL': 'admin@nhmbeo.rs',
                'ADMIN_DEFAULT_PASSWORD': 'secret',
                'ADMIN_USERNAME': 'admin',
            },
            logger=FakeLogger(),
        )

        self.assertEqual(user['email'], 'admin@nhmbeo.rs')
        self.assertEqual(user['auth_source'], 'fallback')
        self.assertEqual(user['login_identifier'], 'admin')

    def test_fallback_auth_rejects_unconfigured_admin_alias(self):
        user = fallback_auth_support.authenticate_fallback_user(
            'admin',
            'secret',
            app_config={
                'ENABLE_FALLBACK_AUTH': True,
                'ADMIN_EMAIL': 'admin@nhmbeo.rs',
                'ADMIN_DEFAULT_PASSWORD': 'secret',
            },
            logger=FakeLogger(),
        )

        self.assertIsNone(user)

    def test_fallback_auth_rejects_blocked_bootstrap_password(self):
        fake_logger = FakeLogger()

        user = fallback_auth_support.authenticate_fallback_user(
            'admin@nhmbeo.rs',
            'Museum2025!Secure',
            app_config={
                'ENABLE_FALLBACK_AUTH': True,
                'ADMIN_EMAIL': 'admin@nhmbeo.rs',
                'ADMIN_DEFAULT_PASSWORD': 'Museum2025!Secure',
            },
            logger=fake_logger,
        )

        self.assertIsNone(user)
        self.assertTrue(fake_logger.calls)

    def test_change_password_accepts_fallback_admin_password_and_updates_primary_auth(self):
        app = Flask(__name__)
        app.secret_key = 'test-secret'
        auth_system = types.SimpleNamespace(
            available=True,
            verify_credentials=MagicMock(side_effect=[None]),
            update_password=MagicMock(return_value=True),
        )
        validator = types.SimpleNamespace(validate=MagicMock(return_value=(True, [])))
        fallback_auth = MagicMock(
            return_value={
                'email': 'admin@nhmbeo.rs',
                'auth_source': 'fallback',
                'login_identifier': 'admin',
            }
        )

        @app.route('/change_password')
        def change_password_route():
            return 'change-password'

        @app.route('/dashboard')
        def dashboard_route():
            return 'dashboard'

        with app.test_request_context(
            '/change_password',
            method='POST',
            data={
                'current_password': 'old-secret',
                'new_password': 'NewSecret123!',
                'confirm_password': 'NewSecret123!',
            },
        ):
            session['user_id'] = 1
            session['user_email'] = 'admin@nhmbeo.rs'
            session['login_identifier'] = 'admin'
            session['auth_source'] = 'fallback'

            response = core_app_views.handle_change_password(
                auth_system=auth_system,
                app_config={'ENABLE_FALLBACK_AUTH': True},
                password_validator=validator,
                dashboard_endpoint='dashboard_route',
                log_security_event=MagicMock(),
                authenticate_fallback_user=fallback_auth,
            )

        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard', response.location)
        auth_system.update_password.assert_called_once_with('admin@nhmbeo.rs', 'NewSecret123!')
        fallback_auth.assert_called_once_with('admin', 'old-secret')

    def test_login_does_not_fallback_when_primary_auth_is_available(self):
        app = Flask(__name__)
        app.secret_key = 'test-secret'
        app.jinja_env.globals['csrf_token'] = lambda: ''
        auth_system = types.SimpleNamespace(
            available=True,
            verify_credentials=MagicMock(return_value=None),
        )
        tracker = types.SimpleNamespace(
            is_locked_out=MagicMock(return_value=(False, None)),
            record_attempt=MagicMock(),
            get_remaining_attempts=MagicMock(return_value=4),
        )
        fallback_auth = MagicMock(
            return_value={
                'email': 'admin@nhmbeo.rs',
                'full_name': 'System Administrator',
                'role': 'admin',
                'user_id': 1,
                'is_first_login': True,
            }
        )

        with app.test_request_context(
            '/login',
            method='POST',
            data={'email': 'admin', 'password': 'old-secret'},
        ):
            with patch.object(core_app_views, 'render_template', return_value='login-page'):
                response = core_app_views.handle_login(
                    app_config={
                        'MAX_LOGIN_ATTEMPTS': 5,
                        'ACCOUNT_LOCKOUT_DURATION': 1800,
                        'ENABLE_FALLBACK_AUTH': True,
                    },
                    auth_system=auth_system,
                    ensure_login_tracker_initialized=lambda: tracker,
                    log_security_event=MagicMock(),
                    log_fallback_auth_warning_once=MagicMock(),
                    authenticate_fallback_user=fallback_auth,
                    change_password_endpoint='change_password',
                    dashboard_endpoint='dashboard',
                )

        self.assertEqual(response, 'login-page')
        fallback_auth.assert_not_called()
        tracker.record_attempt.assert_called_once_with('admin', success=False)


class FakeCursor:
    def __init__(self, rows=None, one=None):
        self.rows = rows or []
        self.one = one
        self.executed = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchall(self):
        return self.rows

    def fetchone(self):
        if self.one is not None:
            return self.one
        if self.rows:
            return self.rows[0]
        return None


class FakeConnection:
    def __init__(self, rows=None, one=None):
        self.cursor_obj = FakeCursor(rows, one=one)
        self.committed = False
        self.rolled_back = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        pass


class FakeS3Client:
    def __init__(self):
        self.objects = {}

    def upload_file(self, source_path, bucket, key):
        self.objects[(bucket, key)] = Path(source_path).read_bytes()

    def download_file(self, bucket, key, destination_path):
        payload = self.objects[(bucket, key)]
        destination = Path(destination_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)

    def delete_object(self, Bucket, Key):
        self.objects.pop((Bucket, Key), None)

    def list_objects_v2(self, Bucket, Prefix, ContinuationToken=None):
        contents = [
            {'Key': key}
            for (bucket, key), _payload in sorted(self.objects.items())
            if bucket == Bucket and key.startswith(Prefix)
        ]
        return {'Contents': contents, 'IsTruncated': False}


class ImageBackupTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix='image-backup-test-'))

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _new_engine(self, base_path: Path):
        with patch.object(image_storage_engine.ImageStorageEngine, '_ensure_db_table', return_value=None):
            return image_storage_engine.ImageStorageEngine(str(base_path))

    def _object_storage_env(self):
        return {
            'IMAGE_STORAGE_BACKEND': 'object',
            'AWS_S3_BUCKET': 'museum-images-test',
            'IMAGE_STORAGE_OBJECT_PREFIX': 'museum-images',
        }

    def test_create_local_backup_writes_metadata_manifest(self):
        base_path = self.tmpdir / 'store'
        originals = base_path / 'originals'
        originals.mkdir(parents=True)
        image_id = 'img_1'
        original_file = originals / f'{image_id}.jpg'
        original_file.write_bytes(b'jpeg-bytes')

        fake_row = {
            'image_id': image_id,
            'database_name': 'mineral',
            'entity_type': 'collection_item',
            'entity_id': '42',
            'original_filename': 'original.jpg',
            'file_extension': '.jpg',
            'file_path': str(original_file),
            'thumbnail_small': '',
            'thumbnail_medium': '',
            'thumbnail_large': '',
            'description': 'desc',
            'file_size': 10,
            'file_hash': 'abc123',
            'width': 1,
            'height': 1,
            'custom_metadata': {'label': 'value'},
            'backed_up': False,
            'backup_date': None,
            'created_at': None,
            'updated_at': None,
        }
        fake_conn = FakeConnection([fake_row])
        engine = self._new_engine(base_path)

        with patch('image_storage_engine._get_db_connection', return_value=fake_conn):
            backup_dir = engine.create_local_backup('snapshot')

        self.assertIsNotNone(backup_dir)
        manifest_path = backup_dir / image_storage_engine.BACKUP_METADATA_FILENAME
        self.assertTrue(manifest_path.exists())
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        self.assertEqual(manifest['image_count'], 1)
        self.assertEqual(manifest['images'][0]['image_id'], image_id)

    def test_restore_from_backup_rehydrates_metadata(self):
        base_path = self.tmpdir / 'restore-store'
        backup_dir = self.tmpdir / 'backup'
        originals_backup = backup_dir / 'originals'
        originals_backup.mkdir(parents=True)
        image_id = 'img_restore'
        backup_image = originals_backup / f'{image_id}.jpg'
        Image.new('RGB', (2, 2), color='white').save(backup_image, format='JPEG')
        manifest = {
            'version': 1,
            'images': [{
                'image_id': image_id,
                'database_name': 'mineral',
                'entity_type': 'collection_item',
                'entity_id': '42',
                'original_filename': 'restored.jpg',
                'file_extension': '.jpg',
                'description': 'desc',
                'file_hash': 'abc123',
                'width': 2,
                'height': 2,
                'custom_metadata': {'label': 'value'},
                'backed_up': True,
                'backup_date': None,
                'created_at': None,
                'updated_at': None,
            }]
        }
        (backup_dir / image_storage_engine.BACKUP_METADATA_FILENAME).write_text(
            json.dumps(manifest),
            encoding='utf-8',
        )

        fake_conn = FakeConnection()
        engine = self._new_engine(base_path)

        with patch('image_storage_engine._get_db_connection', return_value=fake_conn):
            with patch.object(engine, '_generate_thumbnails', return_value={}):
                restored = engine.restore_from_backup(str(backup_dir))

        self.assertTrue(restored)
        self.assertTrue((base_path / 'originals' / f'{image_id}.jpg').exists())
        self.assertTrue(fake_conn.committed)
        self.assertTrue(any('INSERT INTO images' in query for query, _ in fake_conn.cursor_obj.executed))

    def test_object_storage_backup_and_restore_round_trip(self):
        fake_client = FakeS3Client()
        fake_boto3 = types.SimpleNamespace(client=lambda service_name, **kwargs: fake_client)
        image_id = 'img_object_restore'
        source_image = self.tmpdir / 'source.jpg'
        Image.new('RGB', (3, 3), color='white').save(source_image, format='JPEG')

        fake_row = {
            'image_id': image_id,
            'database_name': 'mineral',
            'entity_type': 'collection_item',
            'entity_id': '42',
            'original_filename': 'original.jpg',
            'file_extension': '.jpg',
            'file_path': f'object://originals/{image_id}.jpg',
            'thumbnail_small': '',
            'thumbnail_medium': '',
            'thumbnail_large': '',
            'description': 'desc',
            'file_size': source_image.stat().st_size,
            'file_hash': 'abc123',
            'width': 3,
            'height': 3,
            'custom_metadata': {'label': 'value'},
            'backed_up': True,
            'backup_date': None,
            'created_at': None,
            'updated_at': None,
        }
        source_conn = FakeConnection([fake_row])
        restore_conn = FakeConnection()

        with patch.dict(os.environ, self._object_storage_env(), clear=False):
            with patch.dict(sys.modules, {'boto3': fake_boto3}):
                with patch.object(image_storage_engine.ImageStorageEngine, '_ensure_db_table', return_value=None):
                    source_engine = image_storage_engine.ImageStorageEngine(str(self.tmpdir / 'source-store'))
                    restore_engine = image_storage_engine.ImageStorageEngine(str(self.tmpdir / 'restore-store'))

                source_engine.storage_backend.save_file(source_image, 'originals', f'{image_id}.jpg')

                with patch('image_storage_engine._get_db_connection', return_value=source_conn):
                    backup_dir = source_engine.create_local_backup('snapshot-object')

                self.assertIsNotNone(backup_dir)
                self.assertTrue((backup_dir / 'originals' / f'{image_id}.jpg').exists())

                object_key = f'museum-images/originals/{image_id}.jpg'
                fake_client.delete_object(Bucket='museum-images-test', Key=object_key)
                self.assertNotIn(('museum-images-test', object_key), fake_client.objects)

                with patch('image_storage_engine._get_db_connection', return_value=restore_conn):
                    restored = restore_engine.restore_from_backup(str(backup_dir))

        self.assertTrue(restored)
        self.assertIn(('museum-images-test', object_key), fake_client.objects)
        self.assertIn(
            ('museum-images-test', f'museum-images/thumbnails/small/{image_id}.jpg'),
            fake_client.objects,
        )
        self.assertTrue(restore_conn.committed)
        insert_calls = [params for query, params in restore_conn.cursor_obj.executed if 'INSERT INTO images' in query]
        self.assertTrue(insert_calls)
        self.assertEqual(insert_calls[0][6], f'object://originals/{image_id}.jpg')

    def test_backup_to_server_posts_to_receiver_with_token_and_preserves_metadata(self):
        fake_client = FakeS3Client()
        fake_boto3 = types.SimpleNamespace(client=lambda service_name, **kwargs: fake_client)
        image_id = 'img_remote_backup'
        source_image = self.tmpdir / 'remote-source.jpg'
        Image.new('RGB', (4, 4), color='white').save(source_image, format='JPEG')

        source_row = {
            'image_id': image_id,
            'database_name': 'mineral',
            'entity_type': 'collection_item',
            'entity_id': '42',
            'original_filename': 'original.jpg',
            'file_extension': '.jpg',
            'file_path': f'object://originals/{image_id}.jpg',
            'thumbnail_small': '',
            'thumbnail_medium': '',
            'thumbnail_large': '',
            'description': 'desc',
            'file_size': source_image.stat().st_size,
            'file_hash': 'abc123',
            'width': 4,
            'height': 4,
            'custom_metadata': {'label': 'value'},
            'backed_up': False,
            'backup_date': None,
            'created_at': None,
            'updated_at': None,
        }
        select_conn = FakeConnection([source_row])
        receiver_conn = FakeConnection()
        update_conn = FakeConnection()

        receiver_app = Flask(__name__)
        receiver_app.config['TESTING'] = True
        receiver_app.register_blueprint(image_api.image_api, url_prefix='/api/images')
        receiver_client = receiver_app.test_client()

        def fake_post(url, files=None, data=None, headers=None, timeout=None):
            del url, timeout
            uploaded = files['file']
            uploaded.seek(0)
            response = receiver_client.post(
                '/api/images/backup/receive',
                data={
                    'image_id': data['image_id'],
                    'metadata': data['metadata'],
                    'file': (io.BytesIO(uploaded.read()), 'backup.jpg'),
                },
                headers=headers,
                content_type='multipart/form-data',
            )
            return types.SimpleNamespace(status_code=response.status_code, text=response.get_data(as_text=True))

        env = {
            'IMAGE_STORAGE_BACKEND': 'object',
            'AWS_S3_BUCKET': 'museum-images-test',
            'IMAGE_STORAGE_OBJECT_PREFIX': 'museum-images',
            'IMAGE_BACKUP_TOKEN': 'backup-token',
        }
        with patch.dict(os.environ, env, clear=False):
            with patch.dict(sys.modules, {'boto3': fake_boto3}):
                image_storage_engine._image_storage_instances.clear()
                with patch.object(image_storage_engine.ImageStorageEngine, '_ensure_db_table', return_value=None):
                    source_engine = image_storage_engine.ImageStorageEngine(
                        str(self.tmpdir / 'source-store'),
                        'https://backup.example.com',
                    )
                    source_engine.storage_backend.save_file(source_image, 'originals', f'{image_id}.jpg')
                    source_engine.get_image_path = lambda _image_id, size='original': source_engine.storage_backend.resolve_ref(  # noqa: E731
                        f'object://originals/{image_id}.jpg'
                    )

                    with patch('image_storage_engine._get_db_connection', side_effect=[select_conn, receiver_conn, update_conn]):
                        with patch('image_storage_engine.requests.post', side_effect=fake_post):
                            backed_up = source_engine.backup_to_server(image_id)

        self.assertTrue(backed_up)
        self.assertTrue(update_conn.committed)
        receiver_inserts = [params for query, params in receiver_conn.cursor_obj.executed if 'INSERT INTO images' in query]
        self.assertTrue(receiver_inserts)
        self.assertEqual(receiver_inserts[0][1], 'mineral')
        self.assertEqual(receiver_inserts[0][2], 'collection_item')
        self.assertEqual(receiver_inserts[0][3], '42')


class ImageStorageBackendTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix='image-backend-test-'))

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_local_backend_uses_storage_refs(self):
        backend = image_storage_engine.LocalFilesystemImageBackend(self.tmpdir)
        backend.initialize()

        storage_ref = backend.build_ref('originals', 'example.jpg')
        self.assertEqual(storage_ref, 'local://originals/example.jpg')
        self.assertEqual(backend.resolve_ref(storage_ref), self.tmpdir / 'originals' / 'example.jpg')
        self.assertTrue(backend.is_managed_ref(storage_ref))

    def test_store_image_persists_backend_refs_in_metadata(self):
        source_image = self.tmpdir / 'source.jpg'
        Image.new('RGB', (4, 4), color='white').save(source_image, format='JPEG')
        fake_conn = FakeConnection()

        with patch.object(image_storage_engine.ImageStorageEngine, '_ensure_db_table', return_value=None):
            engine = image_storage_engine.ImageStorageEngine(str(self.tmpdir / 'store'))

        with patch('image_storage_engine._get_db_connection', return_value=fake_conn):
            image_id = engine.store_image(
                file_path=str(source_image),
                database='mineral',
                entity_type='collection_item',
                entity_id='42',
                description='desc',
                metadata={'label': 'value'},
            )

        self.assertIsNotNone(image_id)
        insert_calls = [params for query, params in fake_conn.cursor_obj.executed if 'INSERT INTO images' in query]
        self.assertTrue(insert_calls)
        file_ref = insert_calls[0][6]
        thumb_small_ref = insert_calls[0][7]
        self.assertTrue(file_ref.startswith('local://originals/'))
        self.assertTrue(thumb_small_ref.startswith('local://thumbnails/small/'))
        resolved = engine.storage_backend.resolve_ref(file_ref)
        self.assertIsNotNone(resolved)
        self.assertTrue(resolved.exists())

    def test_object_backend_saves_and_downloads_via_cache(self):
        source_image = self.tmpdir / 'source.jpg'
        source_image.write_bytes(b'object-storage-test')
        fake_client = FakeS3Client()
        fake_boto3 = types.SimpleNamespace(client=lambda service_name, **kwargs: fake_client)

        env = {
            'IMAGE_STORAGE_BACKEND': 'object',
            'AWS_S3_BUCKET': 'museum-images-test',
            'IMAGE_STORAGE_OBJECT_PREFIX': 'museum-images',
            'IMAGE_STORAGE_CACHE_PATH': str(self.tmpdir / 'cache'),
        }
        with patch.dict(os.environ, env, clear=False):
            with patch.dict(sys.modules, {'boto3': fake_boto3}):
                backend = image_storage_engine.ObjectStorageImageBackend(self.tmpdir / 'object-store')
                backend.initialize()

                storage_ref = backend.save_file(source_image, 'originals', 'example.jpg')
                self.assertEqual(storage_ref, 'object://originals/example.jpg')
                self.assertIn(
                    ('museum-images-test', 'museum-images/originals/example.jpg'),
                    fake_client.objects,
                )

                cached_copy = backend.category_dir('originals') / 'example.jpg'
                cached_copy.unlink()

                resolved = backend.resolve_ref(storage_ref)
                self.assertIsNotNone(resolved)
                self.assertEqual(resolved.read_bytes(), b'object-storage-test')

    def test_store_image_persists_object_storage_refs_in_metadata(self):
        source_image = self.tmpdir / 'source.jpg'
        Image.new('RGB', (4, 4), color='white').save(source_image, format='JPEG')
        fake_conn = FakeConnection()
        fake_client = FakeS3Client()
        fake_boto3 = types.SimpleNamespace(client=lambda service_name, **kwargs: fake_client)

        env = {
            'IMAGE_STORAGE_BACKEND': 'object',
            'AWS_S3_BUCKET': 'museum-images-test',
            'IMAGE_STORAGE_OBJECT_PREFIX': 'museum-images',
            'IMAGE_STORAGE_CACHE_PATH': str(self.tmpdir / 'cache'),
        }
        with patch.dict(os.environ, env, clear=False):
            with patch.dict(sys.modules, {'boto3': fake_boto3}):
                with patch.object(image_storage_engine.ImageStorageEngine, '_ensure_db_table', return_value=None):
                    engine = image_storage_engine.ImageStorageEngine(str(self.tmpdir / 'store'))

                with patch('image_storage_engine._get_db_connection', return_value=fake_conn):
                    image_id = engine.store_image(
                        file_path=str(source_image),
                        database='mineral',
                        entity_type='collection_item',
                        entity_id='42',
                        description='desc',
                        metadata={'label': 'value'},
                    )

        self.assertIsNotNone(image_id)
        insert_calls = [params for query, params in fake_conn.cursor_obj.executed if 'INSERT INTO images' in query]
        self.assertTrue(insert_calls)
        file_ref = insert_calls[0][6]
        thumb_small_ref = insert_calls[0][7]
        self.assertTrue(file_ref.startswith('object://originals/'))
        self.assertTrue(thumb_small_ref.startswith('object://thumbnails/small/'))
        self.assertIn(
            ('museum-images-test', f"museum-images/originals/{Path(file_ref.split('object://', 1)[1]).name}"),
            fake_client.objects,
        )


class SharedSettingsPersistenceTests(unittest.TestCase):
    def setUp(self):
        # Očisti procesne keševe da test ne zavisi od redosleda izvršavanja
        # (backoff/last-known-good preživljavaju između klasa u istom procesu).
        module_access_support._db_setting_failure_cache.clear()
        module_access_support._last_known_good.clear()

    def test_module_access_loads_from_postgres_shared_settings(self):
        fake_conn = FakeConnection(one={'setting_value': {
            'example': {'authorized_users': ['user@example.com']}
        }})

        loaded = module_access_support.load_module_access_data(
            module_access_file='/tmp/unused.json',
            current_mtime=None,
            default_access={'example': {'authorized_users': [], 'restricted_users': [], 'name': 'Example'}},
            get_postgres_connection=lambda: fake_conn,
        )

        self.assertEqual(loaded['example']['authorized_users'], ['user@example.com'])

    def test_dashboard_preferences_save_writes_postgres_shared_settings(self):
        fake_conn = FakeConnection()

        saved = module_access_support.save_dashboard_preferences_data(
            dashboard_prefs_file='/tmp/unused-dashboard.json',
            dashboard_preferences={'user@example.com': {'enabled_widgets': ['news']}},
            get_postgres_connection=lambda: fake_conn,
        )

        self.assertTrue(saved)
        executed_sql = ' '.join(query for query, _ in fake_conn.cursor_obj.executed)
        self.assertIn('INSERT INTO app_shared_settings', executed_sql)
        self.assertTrue(fake_conn.committed)

    def test_dashboard_preferences_save_skips_file_when_postgres_succeeds(self):
        fake_conn = FakeConnection()

        with patch('module_access_support.write_json_file') as write_mock:
            saved = module_access_support.save_dashboard_preferences_data(
                dashboard_prefs_file='/tmp/unused-dashboard.json',
                dashboard_preferences={'user@example.com': {'enabled_widgets': ['news']}},
                get_postgres_connection=lambda: fake_conn,
            )

        self.assertTrue(saved)
        write_mock.assert_not_called()

    def test_admin_system_settings_load_uses_shared_storage(self):
        fake_conn = FakeConnection(one={'setting_value': {'institution_name': 'Shared Museum'}})
        original_cache = dict(admin_system_views._saved_settings_cache)
        self.addCleanup(admin_system_views._saved_settings_cache.update, original_cache)
        admin_system_views._saved_settings_cache.update({'data': None, 'timestamp': None, 'db_enabled': None})

        with patch.dict(os.environ, {'DATABASE_URL': 'postgresql://example'}, clear=False):
            with patch.object(admin_system_views, 'get_postgres_connection', return_value=fake_conn):
                loaded = admin_system_views.load_saved_settings()

        self.assertEqual(loaded['institution_name'], 'Shared Museum')


class MailSettingsPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix='mail-settings-test-'))
        self.addCleanup(shutil.rmtree, self.tmpdir, ignore_errors=True)
        self.original_fernet = mail_client._fernet_instance
        self.original_table_flag = mail_client._mail_settings_initialized
        mail_client._fernet_instance = None
        mail_client._mail_settings_initialized = False

    def tearDown(self):
        mail_client._fernet_instance = self.original_fernet
        mail_client._mail_settings_initialized = self.original_table_flag

    def test_save_user_settings_writes_postgres_shared_storage(self):
        fake_conn = FakeConnection()
        env = {
            'DATABASE_URL': 'postgresql://example',
            'MAIL_SETTINGS_ENCRYPTION_KEY': mail_client.Fernet.generate_key().decode(),
        }
        with patch.dict(os.environ, env, clear=False):
            with patch.object(mail_client, 'get_postgres_connection', return_value=fake_conn):
                mail_client.save_user_settings(
                    'user@example.com',
                    {'imap_server': 'imap.example.com', 'password': mail_client._encrypt('secret')},
                )

        executed_sql = ' '.join(query for query, _ in fake_conn.cursor_obj.executed)
        self.assertIn('INSERT INTO mail_user_settings', executed_sql)
        self.assertTrue(fake_conn.committed)

    def test_get_user_settings_reads_from_postgres_shared_storage(self):
        fake_conn = FakeConnection(one={'settings_json': {'imap_server': 'imap.example.com', 'password': 'token'}})
        with patch.dict(os.environ, {'DATABASE_URL': 'postgresql://example'}, clear=False):
            with patch.object(mail_client, 'get_postgres_connection', return_value=fake_conn):
                loaded = mail_client.get_user_settings('user@example.com')

        self.assertEqual(loaded['imap_server'], 'imap.example.com')

    def test_get_user_settings_migrates_legacy_file_settings_and_reencrypts(self):
        user_email = 'user@example.com'
        legacy_key = mail_client.Fernet.generate_key()
        legacy_fernet = mail_client.Fernet(legacy_key)
        legacy_password = legacy_fernet.encrypt(b'legacy-secret').decode()
        legacy_file = self.tmpdir / 'mail_settings.json'
        legacy_file.write_text(json.dumps({
            user_email: {
                'imap_server': 'legacy.example.com',
                'password': legacy_password,
            }
        }), encoding='utf-8')
        key_file = self.tmpdir / '.mail_key'
        key_file.write_bytes(legacy_key)

        fake_conn = FakeConnection()
        env = {
            'DATABASE_URL': 'postgresql://example',
            'MAIL_SETTINGS_ENCRYPTION_KEY': mail_client.Fernet.generate_key().decode(),
        }
        with patch.dict(os.environ, env, clear=False):
            with patch.object(mail_client, 'SETTINGS_FILE', legacy_file):
                with patch.object(mail_client, 'KEY_FILE', key_file):
                    with patch.object(mail_client, 'get_postgres_connection', return_value=fake_conn):
                        loaded = mail_client.get_user_settings(user_email)

        self.assertEqual(loaded['imap_server'], 'legacy.example.com')
        self.assertEqual(mail_client._decrypt(loaded['password']), 'legacy-secret')
        self.assertFalse(legacy_file.exists())
        executed_sql = ' '.join(query for query, _ in fake_conn.cursor_obj.executed)
        self.assertIn('INSERT INTO mail_user_settings', executed_sql)

    def test_mail_settings_fail_closed_in_production_when_postgres_is_unavailable(self):
        env = {
            'FLASK_ENV': 'production',
            'DATABASE_URL': 'postgresql://example',
            'MAIL_SETTINGS_ENCRYPTION_KEY': mail_client.Fernet.generate_key().decode(),
        }
        with patch.dict(os.environ, env, clear=False):
            with patch.object(mail_client, 'get_postgres_connection', side_effect=RuntimeError('db down')):
                with self.assertRaises(RuntimeError):
                    mail_client.get_user_settings('user@example.com')


class MailHostPolicyTests(unittest.TestCase):
    def test_validate_mail_server_settings_rejects_unlisted_host(self):
        with self.assertRaises(ValueError):
            mail_client.validate_mail_server_settings(
                {
                    'imap_server': 'imap.evil.example',
                    'smtp_server': 'smtp.nhmbeo.rs',
                },
                allowed_hosts=['smtp.nhmbeo.rs'],
            )

    def test_mail_connection_test_fails_closed_for_unlisted_host(self):
        result = mail_client.test_imap_connection(
            server='imap.evil.example',
            port=993,
            ssl=True,
            email_address='admin@nhmbeo.rs',
            password='secret',
            allowed_hosts=['imap.nhmbeo.rs'],
        )

        self.assertFalse(result['success'])
        self.assertIn('allowed host list', result['message'])

    def test_banned_mail_host_overrides_allowlist(self):
        with self.assertRaises(ValueError):
            mail_client.ensure_mail_host_allowed(
                'smtp.nhmbeo.rs',
                allowed_hosts=['smtp.nhmbeo.rs'],
                banned_hosts=['smtp.nhmbeo.rs'],
            )

    def test_mail_settings_save_persists_allowed_hosts(self):
        app = Flask(__name__)
        app.secret_key = 'test-secret'
        payload = {
            'imap_server': 'imap.nhmbeo.rs',
            'imap_port': 993,
            'imap_ssl': True,
            'smtp_server': 'smtp.nhmbeo.rs',
            'smtp_port': 587,
            'smtp_starttls': True,
            'email_address': 'admin@nhmbeo.rs',
            'password': 'secret',
            'allowed_hosts': 'imap.nhmbeo.rs\nsmtp.nhmbeo.rs',
        }

        with app.test_request_context('/api/mail/settings', method='POST', json=payload):
            session['user_email'] = 'admin@nhmbeo.rs'
            with patch.object(admin_system_views, 'load_saved_settings', return_value={}):
                with patch.object(admin_system_views, 'save_settings', return_value=True) as save_settings_mock:
                    with patch.object(mail_client, 'get_user_settings', return_value={}):
                        with patch.object(mail_client, '_encrypt', return_value='encrypted-secret'):
                            with patch.object(mail_client, 'save_user_settings') as save_user_settings_mock:
                                response = mail_views.api_mail_settings_save()

        body = response.get_json()
        self.assertTrue(body['success'])
        save_settings_mock.assert_called_once_with(
            {'mail_allowed_hosts': ['imap.nhmbeo.rs', 'smtp.nhmbeo.rs']}
        )
        save_user_settings_mock.assert_called_once()

    def test_admin_mail_settings_save_persists_user_settings_and_global_policy(self):
        app = Flask(__name__)
        app.secret_key = 'test-secret'
        payload = {
            'target_email': 'user@nhmbeo.rs',
            'imap_server': 'imap.nhmbeo.rs',
            'imap_port': 993,
            'imap_ssl': True,
            'smtp_server': 'smtp.nhmbeo.rs',
            'smtp_port': 587,
            'smtp_starttls': True,
            'email_address': 'user@nhmbeo.rs',
            'password': 'secret',
            'allowed_hosts': 'imap.nhmbeo.rs\nsmtp.nhmbeo.rs',
            'banned_hosts': 'blocked.nhmbeo.rs',
        }

        with app.test_request_context('/api/admin/mail-settings', method='POST', json=payload):
            session['user_email'] = 'admin@nhmbeo.rs'
            with patch.object(admin_user_management_views, '_active_user_emails', return_value={'user@nhmbeo.rs'}):
                with patch.object(admin_system_views, 'load_saved_settings', return_value={}):
                    with patch.object(admin_system_views, 'save_settings', return_value=True) as save_settings_mock:
                        with patch.object(mail_client, 'get_user_settings', return_value={}):
                            with patch.object(mail_client, '_encrypt', return_value='encrypted-secret'):
                                with patch.object(mail_client, 'save_user_settings') as save_user_settings_mock:
                                    response = admin_user_management_views.api_admin_mail_settings_save()

        body = response.get_json()
        self.assertTrue(body['success'])
        save_settings_mock.assert_called_once_with(
            {
                'mail_allowed_hosts': ['imap.nhmbeo.rs', 'smtp.nhmbeo.rs'],
                'mail_banned_hosts': ['blocked.nhmbeo.rs'],
            }
        )
        save_user_settings_mock.assert_called_once()


class WsgiTests(unittest.TestCase):
    def _load_wsgi_module(self):
        module_name = 'wsgi_test_module'
        fake_app_module = types.ModuleType('app')
        fake_app_module.create_app = MagicMock(return_value=object())
        app_module_original = sys.modules.get('app')
        sys.modules['app'] = fake_app_module
        try:
            spec = importlib.util.spec_from_file_location(
                module_name,
                Path(__file__).resolve().parent / 'wsgi.py',
            )
            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(module)
            return fake_app_module.create_app
        finally:
            if app_module_original is not None:
                sys.modules['app'] = app_module_original
            else:
                sys.modules.pop('app', None)

    def test_wsgi_builds_web_app_without_background_jobs(self):
        create_app_mock = self._load_wsgi_module()
        create_app_mock.assert_called_once_with()


class BackgroundWorkerTests(unittest.TestCase):
    def test_background_worker_starts_jobs_in_dedicated_process(self):
        module_name = 'background_worker_test_module'
        fake_app_module = types.ModuleType('app')
        fake_app_module.create_app = MagicMock(return_value=object())
        fake_app_module.start_background_jobs = MagicMock(return_value=True)
        app_module_original = sys.modules.get('app')
        sys.modules['app'] = fake_app_module
        try:
            spec = importlib.util.spec_from_file_location(
                module_name,
                Path(__file__).resolve().parent / 'background_worker.py',
            )
            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(module)
            module._stop_requested = True
            with patch.object(module.signal, 'signal'):
                module.run_worker()
        finally:
            if app_module_original is not None:
                sys.modules['app'] = app_module_original
            else:
                sys.modules.pop('app', None)

        fake_app_module.create_app.assert_called_once_with()
        fake_app_module.start_background_jobs.assert_called_once_with()


class StartProductionScriptTests(unittest.TestCase):
    def test_production_startup_requires_mail_key_and_uses_background_worker(self):
        script = (Path(__file__).resolve().parent / 'start_production.sh').read_text(encoding='utf-8')
        self.assertIn('MAIL_SETTINGS_ENCRYPTION_KEY', script)
        self.assertIn('BACKGROUND_WORKER_ENABLED', script)
        self.assertNotIn('START_BACKGROUND_SERVICES', script)


if __name__ == '__main__':
    unittest.main()
