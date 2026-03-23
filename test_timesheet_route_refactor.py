#!/usr/bin/env python3
"""Regression tests for extracted timesheet route wrappers."""

import os
import unittest
from datetime import timedelta
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')

import app as museum_app


class TimesheetRouteRefactorTests(unittest.TestCase):
    def setUp(self):
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def _login(self, *, role='employee'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = 'user@example.com'
            sess['user_name'] = 'Test User'
            sess['user_role'] = role
            sess['is_admin'] = role == 'admin'

    def test_set_language_route_delegates_to_core_module(self):
        with patch.object(
            museum_app.core_app_views,
            'set_language_preference',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/set_language', json={'language': 'en'}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_index_route_delegates_to_core_module(self):
        with patch.object(
            museum_app.core_app_views,
            'render_index',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            dashboard_endpoint='dashboard',
        )

    def test_login_route_delegates_to_core_module(self):
        with patch.object(
            museum_app.core_app_views,
            'handle_login',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/login', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            app_config=museum_app.app.config,
            auth_system=museum_app.auth_system,
            ensure_login_tracker_initialized=museum_app.ensure_login_tracker_initialized,
            log_security_event=museum_app.log_security_event,
            log_fallback_auth_warning_once=museum_app.log_fallback_auth_warning_once,
            authenticate_fallback_user=museum_app.authenticate_fallback_user,
            change_password_endpoint='change_password',
            dashboard_endpoint='dashboard',
        )

    def test_logout_route_delegates_to_core_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.core_app_views,
            'handle_logout',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/logout', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            index_endpoint='index',
        )

    def test_change_password_route_delegates_to_core_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.core_app_views,
            'handle_change_password',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/change_password', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            auth_system=museum_app.auth_system,
            app_config=museum_app.app.config,
            password_validator=museum_app.password_validator,
            dashboard_endpoint='dashboard',
            log_security_event=museum_app.log_security_event,
        )

    def test_dashboard_route_delegates_to_core_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.core_app_views,
            'render_dashboard',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/dashboard', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_user_modules=museum_app.get_user_modules,
        )

    def test_dashboard_classic_route_delegates_to_core_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.core_app_views,
            'render_dashboard',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/dashboard-classic', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_user_modules=museum_app.get_user_modules,
        )

    def test_mineral_database_route_delegates_to_core_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.core_app_views,
            'render_mineral_database_redirect',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/mineral_database', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            user_has_module_access=museum_app.user_has_module_access,
            dashboard_endpoint='dashboard',
            admin_mineral_collection_endpoint='admin_mineral_collection',
        )

    def test_admin_panel_route_delegates_to_core_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.core_app_views,
            'render_admin_panel',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_timesheet_route_delegates_to_extracted_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.timesheet_admin_views,
            'render_timesheet_app',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/timesheet', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            timesheet_repository=museum_app.timesheet_repository,
            timesheet_repository_cls=museum_app.TimesheetRepository,
            user_has_module_access=museum_app.user_has_module_access,
        )

    def test_admin_reports_route_delegates_to_extracted_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.timesheet_admin_views,
            'render_admin_timesheet_reports',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/timesheet_reports', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            timesheet_repository=museum_app.timesheet_repository,
            timesheet_repository_cls=museum_app.TimesheetRepository,
        )

    def test_admin_report_api_delegates_to_extracted_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.timesheet_admin_views,
            'api_admin_get_timesheet_report',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/admin/timesheet/report/7', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            report_id=7,
            timesheet_repository=museum_app.timesheet_repository,
        )

    def test_timesheet_entry_route_delegates_to_employee_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.timesheet_employee_views,
            'render_timesheet_entry',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/timesheet/entry', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_timesheet_save_api_delegates_to_employee_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.timesheet_employee_views,
            'api_save_timesheet',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/timesheet/save', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_timesheet_submit_api_delegates_to_employee_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.timesheet_employee_views,
            'api_timesheet_submit',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/timesheet/11/submit', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(11)

    def test_admin_timesheet_review_route_delegates_to_employee_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.timesheet_employee_views,
            'render_admin_timesheet_review',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/timesheet/review', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_notifications_api_delegates_to_notification_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.notification_views,
            'api_get_notifications',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/notifications', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_notification_mark_read_api_delegates_to_notification_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.notification_views,
            'api_mark_notifications_read',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/notifications/read', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_notification_clear_api_delegates_to_notification_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.notification_views,
            'api_clear_notifications',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/notifications/clear', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_admin_system_settings_route_delegates_to_system_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.admin_system_views,
            'render_admin_system_settings',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/system-settings', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_admin_system_settings_general_api_delegates_to_system_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.admin_system_views,
            'api_save_general_settings',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/admin/settings/general', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_admin_system_settings_security_api_delegates_to_system_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.admin_system_views,
            'api_save_security_settings',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/admin/settings/security', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_admin_logs_api_delegates_to_system_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.admin_system_views,
            'api_get_logs',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/admin/logs', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_session_timeout_minutes_handles_timedelta(self):
        self.assertEqual(museum_app.admin_system_views._session_timeout_minutes(timedelta(hours=8)), 480)

    def test_admin_statistics_route_delegates_to_statistics_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.collection_statistics_views,
            'render_admin_statistics',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/statistics', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_mineral_database=museum_app.get_mineral_database,
            get_meteorite_collection_database=museum_app.get_meteorite_collection_database,
            botany_collection_database=museum_app.BOTANY_COLLECTION_DATABASE,
            paleozoology_collection_database=museum_app.PALEOZOOLOGY_COLLECTION_DATABASE,
            paleobotany_collection_database=museum_app.PALEOBOTANY_COLLECTION_DATABASE,
            petrology_collection_database=museum_app.PETROLOGY_COLLECTION_DATABASE,
            get_cultural_heritage_database=museum_app.get_cultural_heritage_database,
            get_image_storage=museum_app.get_image_storage,
        )

    def test_admin_qr_generator_route_delegates_to_qr_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.qr_management_views,
            'render_admin_qr_generator',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/qr_generator', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            user_has_module_access=museum_app.user_has_module_access,
        )

    def test_admin_qr_field_selection_route_delegates_to_qr_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.qr_management_views,
            'render_admin_qr_field_selection',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/qr_field_selection/botany', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'botany',
            normalize_qr_collection_type=museum_app.normalize_qr_collection_type,
            ensure_qr_collection_access=museum_app.ensure_qr_collection_access,
        )

    def test_admin_qr_labels_with_fields_route_delegates_to_qr_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.qr_management_views,
            'handle_admin_qr_labels_with_fields',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.post('/admin/qr_labels_with_fields/botany', data={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'botany',
            normalize_qr_collection_type=museum_app.normalize_qr_collection_type,
            ensure_qr_collection_access=museum_app.ensure_qr_collection_access,
            get_meteorite_collection_database=museum_app.get_meteorite_collection_database,
            botany_collection_database=museum_app.BOTANY_COLLECTION_DATABASE,
            paleozoology_collection_database=museum_app.PALEOZOOLOGY_COLLECTION_DATABASE,
        )

    def test_admin_qr_mineral_boxes_route_delegates_to_qr_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.qr_management_views,
            'render_admin_qr_mineral_boxes',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/qr_boxes/minerals', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            ensure_qr_collection_access=museum_app.ensure_qr_collection_access,
            get_mineral_database=museum_app.get_mineral_database,
        )

    def test_admin_generate_box_qr_codes_route_delegates_to_qr_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.qr_management_views,
            'handle_admin_generate_box_qr_codes',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.post('/admin/qr_boxes/minerals/generate', data={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            ensure_qr_collection_access=museum_app.ensure_qr_collection_access,
        )

    def test_admin_qr_select_specimens_route_delegates_to_qr_label_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.qr_label_views,
            'render_admin_qr_select_specimens',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/qr_select/botany', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'botany',
            normalize_qr_collection_type=museum_app.normalize_qr_collection_type,
            ensure_qr_collection_access=museum_app.ensure_qr_collection_access,
            get_qr_collection_name=museum_app.get_qr_collection_name,
            get_qr_collection_url=museum_app.get_qr_collection_url,
            get_mineral_database=museum_app.get_mineral_database,
            get_qr_collection_records=museum_app.get_qr_collection_records,
            get_qr_record_identifier=museum_app.get_qr_record_identifier,
            get_qr_record_catalog_label=museum_app.get_qr_record_catalog_label,
            get_qr_record_name=museum_app.get_qr_record_name,
            get_qr_record_summary=museum_app.get_qr_record_summary,
            get_qr_record_location=museum_app.get_qr_record_location,
        )

    def test_admin_qr_labels_selected_route_delegates_to_qr_label_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.qr_label_views,
            'handle_admin_qr_labels_selected',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.post('/admin/qr_labels_selected/botany', data={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'botany',
            normalize_qr_collection_type=museum_app.normalize_qr_collection_type,
            ensure_qr_collection_access=museum_app.ensure_qr_collection_access,
            get_mineral_database=museum_app.get_mineral_database,
            get_qr_collection_records=museum_app.get_qr_collection_records,
            get_qr_record_identifier=museum_app.get_qr_record_identifier,
            get_qr_record_catalog_label=museum_app.get_qr_record_catalog_label,
            get_qr_record_name=museum_app.get_qr_record_name,
            build_collection_highlight_qr_url=museum_app.build_collection_highlight_qr_url,
            get_qr_collection_name=museum_app.get_qr_collection_name,
        )

    def test_admin_qr_label_format_route_delegates_to_qr_label_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.qr_label_views,
            'render_admin_qr_label_format',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/qr_label_format/botany', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'botany',
            normalize_qr_collection_type=museum_app.normalize_qr_collection_type,
            ensure_qr_collection_access=museum_app.ensure_qr_collection_access,
            get_qr_collection_name=museum_app.get_qr_collection_name,
            get_qr_collection_url=museum_app.get_qr_collection_url,
        )

    def test_admin_qr_labels_with_format_route_delegates_to_qr_label_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.qr_label_views,
            'handle_admin_qr_labels_with_format',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.post('/admin/qr_labels_with_format/botany', data={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'botany',
            normalize_qr_collection_type=museum_app.normalize_qr_collection_type,
            ensure_qr_collection_access=museum_app.ensure_qr_collection_access,
            get_qr_collection_url=museum_app.get_qr_collection_url,
        )

    def test_admin_qr_labels_route_delegates_to_qr_label_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.qr_label_views,
            'render_admin_qr_labels',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/qr_labels/botany', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'botany',
            normalize_qr_collection_type=museum_app.normalize_qr_collection_type,
            ensure_qr_collection_access=museum_app.ensure_qr_collection_access,
            get_mineral_database=museum_app.get_mineral_database,
            get_qr_collection_records=museum_app.get_qr_collection_records,
            get_qr_record_identifier=museum_app.get_qr_record_identifier,
            get_qr_record_catalog_label=museum_app.get_qr_record_catalog_label,
            get_qr_record_name=museum_app.get_qr_record_name,
            build_collection_highlight_qr_url=museum_app.build_collection_highlight_qr_url,
            get_qr_collection_name=museum_app.get_qr_collection_name,
            get_qr_collection_url=museum_app.get_qr_collection_url,
        )

    def test_batch_image_upload_route_delegates_to_collection_media_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.collection_media_views,
            'handle_batch_image_upload',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/batch_image_upload', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_accessible_image_upload_databases=museum_app.get_accessible_image_upload_databases,
            normalize_image_upload_database=museum_app.normalize_image_upload_database,
            ensure_image_upload_access=museum_app.ensure_image_upload_access,
            user_has_module_access=museum_app.user_has_module_access,
            get_image_upload_config=museum_app.get_image_upload_config,
            get_batch_uploader=museum_app.get_batch_uploader,
            get_image_upload_records=museum_app.get_image_upload_records,
            get_image_upload_collection_url=museum_app.get_image_upload_collection_url,
            get_image_upload_display_name=museum_app.get_image_upload_display_name,
        )

    def test_qr_view_mineral_box_route_delegates_to_collection_media_module(self):
        with patch.object(
            museum_app.collection_media_views,
            'render_qr_view_mineral_box',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/qr_box/minerals/12', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            '12',
            get_mineral_database=museum_app.get_mineral_database,
        )

    def test_specimen_image_route_delegates_to_collection_media_module(self):
        with patch.object(
            museum_app.collection_media_views,
            'get_specimen_image',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/api/specimen_image/botany/specimen/7', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'botany',
            'specimen',
            '7',
            get_image_storage=museum_app.get_image_storage,
        )

    def test_image_by_id_route_delegates_to_collection_media_module(self):
        with museum_app.app.test_request_context('/api/images/test-image'):
            museum_app.session['user_id'] = 1
            museum_app.session['user_email'] = 'user@example.com'
            museum_app.session['user_role'] = 'employee'

            with patch.object(
                museum_app.collection_media_views,
                'get_image_by_id',
                return_value=museum_app.app.response_class('ok', status=200),
            ) as mocked_handler:
                response = museum_app.get_image_by_id('test-image')

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'test-image',
            get_image_storage=museum_app.get_image_storage,
        )

    def test_qr_view_specimen_route_delegates_to_collection_media_module(self):
        with patch.object(
            museum_app.collection_media_views,
            'render_qr_view_specimen',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/qr_view/botany/BOT-1', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'botany',
            'BOT-1',
            normalize_qr_collection_type=museum_app.normalize_qr_collection_type,
            get_meteorite_collection_database=museum_app.get_meteorite_collection_database,
            botany_collection_database=museum_app.BOTANY_COLLECTION_DATABASE,
            paleozoology_collection_database=museum_app.PALEOZOOLOGY_COLLECTION_DATABASE,
        )

    def test_manage_access_route_delegates_to_user_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.admin_user_management_views,
            'render_manage_user_access',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/manage_access', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            load_module_access=museum_app.load_module_access,
            user_has_module_access=museum_app.user_has_module_access,
            module_access=museum_app.MODULE_ACCESS,
            get_museum_employees=museum_app.get_museum_employees,
        )

    def test_grant_access_route_delegates_to_user_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.admin_user_management_views,
            'grant_module_access',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.post('/admin/grant_access', data={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            load_module_access=museum_app.load_module_access,
            save_module_access=museum_app.save_module_access,
            module_access=museum_app.MODULE_ACCESS,
        )

    def test_revoke_access_route_delegates_to_user_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.admin_user_management_views,
            'revoke_module_access',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.post('/admin/revoke_access', data={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            load_module_access=museum_app.load_module_access,
            save_module_access=museum_app.save_module_access,
            module_access=museum_app.MODULE_ACCESS,
        )

    def test_customize_dashboard_route_delegates_to_user_management_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.admin_user_management_views,
            'customize_dashboard_preferences',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/dashboard/customize', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            load_dashboard_preferences=museum_app.load_dashboard_preferences,
            save_dashboard_preferences=museum_app.save_dashboard_preferences,
            dashboard_preferences=museum_app.DASHBOARD_PREFERENCES,
            module_access=museum_app.MODULE_ACCESS,
            user_has_module_access=museum_app.user_has_module_access,
            dashboard_endpoint='dashboard',
        )

    def test_password_manager_route_delegates_to_user_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.admin_user_management_views,
            'render_admin_password_manager',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/password_manager', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_password_manager_users_api_delegates_to_user_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.admin_user_management_views,
            'api_password_manager_users',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/admin/password_manager/users', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_password_manager_reset_api_delegates_to_user_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.admin_user_management_views,
            'api_password_manager_reset',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/admin/password_manager/reset', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            password_validator=museum_app.password_validator,
            password_hasher=museum_app.password_hasher,
            log_security_event=museum_app.log_security_event,
        )

    def test_password_manager_force_change_api_delegates_to_user_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.admin_user_management_views,
            'api_password_manager_force_change',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/admin/password_manager/force_change', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            log_security_event=museum_app.log_security_event,
        )

    def test_password_manager_toggle_status_api_delegates_to_user_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.admin_user_management_views,
            'api_password_manager_toggle_status',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/admin/password_manager/toggle_status', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            log_security_event=museum_app.log_security_event,
        )

    def test_password_manager_generate_api_delegates_to_user_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.admin_user_management_views,
            'api_password_manager_generate',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/admin/password_manager/generate', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            password_validator=museum_app.password_validator,
        )

    def test_employees_database_route_delegates_to_employee_admin_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.employee_admin_views,
            'render_employees_database',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/employees_database', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_employee_directory=museum_app.get_employee_directory,
        )

    def test_employee_profiles_database_route_delegates_to_employee_admin_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.employee_admin_views,
            'render_employee_profiles_database',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/employee_profiles_database', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_employee_directory=museum_app.get_employee_directory,
        )

    def test_add_user_route_delegates_to_employee_admin_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.employee_admin_views,
            'handle_add_user',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/add_user', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_museum_employees=museum_app.get_museum_employees,
            get_employee_directory=museum_app.get_employee_directory,
            password_hasher=museum_app.password_hasher,
        )

    def test_system_reports_route_delegates_to_museum_content_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.museum_content_views,
            'render_system_reports',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/reports', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_library_database=museum_app.get_library_database,
            get_employee_directory=museum_app.get_employee_directory,
            get_exhibit_statistics=museum_app.get_exhibit_statistics,
            user_has_module_access=museum_app.user_has_module_access,
        )

    def test_exhibits_database_route_delegates_to_museum_content_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.museum_content_views,
            'render_exhibits_database',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/exhibits_database', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            exhibits_database=museum_app.EXHIBITS_DATABASE,
            get_exhibit_statistics=museum_app.get_exhibit_statistics,
        )

    def test_exhibitions_database_route_delegates_to_museum_content_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.museum_content_views,
            'render_exhibitions_database',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/exhibitions_database', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            exhibitions_database=museum_app.EXHIBITIONS_DATABASE,
            get_exhibition_statistics=museum_app.get_exhibition_statistics,
        )

    def test_museum_news_route_delegates_to_museum_content_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.museum_content_views,
            'render_museum_news',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/news', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            news_database=museum_app.NEWS_DATABASE,
        )

    def test_save_news_api_delegates_to_museum_content_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.museum_content_views,
            'api_save_news',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/news/save', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            news_database=museum_app.NEWS_DATABASE,
        )

    def test_add_book_route_delegates_to_museum_content_module(self):
        self._login(role='admin')
        original_library_database = museum_app.LIBRARY_DATABASE
        museum_app.LIBRARY_DATABASE = {'books': [], 'statistics': {}}

        try:
            with patch.object(
                museum_app.museum_content_views,
                'handle_add_book',
                return_value=museum_app.app.response_class('ok', status=200),
            ) as mocked_handler:
                response = self.client.get('/admin/add_book', base_url=self.base_url)
        finally:
            active_library_database = museum_app.LIBRARY_DATABASE
            museum_app.LIBRARY_DATABASE = original_library_database

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once()
        call_kwargs = mocked_handler.call_args.kwargs
        self.assertIs(call_kwargs['library_database'], active_library_database)
        self.assertIs(call_kwargs['save_library_database'], museum_app.save_library_database)
        self.assertIn('phase3a_databases', call_kwargs)

    def test_add_visitor_route_delegates_to_museum_content_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.museum_content_views,
            'handle_add_visitor',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/add_visitor', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            visitor_records=museum_app.VISITOR_RECORDS,
        )

    def test_visitors_database_route_delegates_to_museum_content_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.museum_content_views,
            'render_visitors_database',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/visitors_database', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            visitor_records=museum_app.VISITOR_RECORDS,
        )

    def test_export_visitors_pdf_route_delegates_to_museum_content_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.museum_content_views,
            'export_visitors_to_pdf',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/export_visitors_to_pdf', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            visitors_endpoint='visitors_database',
        )

    def test_add_research_route_delegates_to_museum_content_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.museum_content_views,
            'handle_add_research',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/add_research', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            research_projects=museum_app.RESEARCH_PROJECTS,
        )

    def test_research_database_route_delegates_to_museum_content_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.museum_content_views,
            'render_research_database',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/research_database', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            research_projects=museum_app.RESEARCH_PROJECTS,
        )

    def test_projekti_route_delegates_to_project_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.project_views,
            'render_projects_page',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/projekti', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_projekti_documentation_route_delegates_to_project_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.project_views,
            'render_project_documentation',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/projekti/dokumentacija', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            app_root_path=museum_app.app.root_path,
        )

    def test_projekti_space_planner_route_delegates_to_project_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.project_views,
            'render_project_space_planner',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/projekti/space-planner', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_projekti_space_planner_get_api_delegates_to_project_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.project_views,
            'api_project_space_planner_get',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/projekti/space-planner', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            planner_file=museum_app.PROJECT_SPACE_PLANNER_FILE,
            auto_layout_version=museum_app.PROJECT_AUTO_LAYOUT_VERSION,
            project_space_plan_views=museum_app.PROJECT_SPACE_PLAN_VIEWS,
            project_space_plan_file=museum_app.PROJECT_SPACE_PLAN_FILE,
            project_space_plan_image_size=museum_app.PROJECT_SPACE_PLAN_IMAGE_SIZE,
            project_space_library=museum_app.PROJECT_SPACE_LIBRARY,
            project_common_terms=museum_app.PROJECT_COMMON_TERMS,
            project_auto_detected_spaces=museum_app.PROJECT_AUTO_DETECTED_SPACES,
            project_depot_auto_detected_spaces=museum_app.PROJECT_DEPOT_AUTO_DETECTED_SPACES,
        )

    def test_projekti_space_planner_save_api_delegates_to_project_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.project_views,
            'api_project_space_planner_save',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/projekti/space-planner', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            planner_file=museum_app.PROJECT_SPACE_PLANNER_FILE,
            auto_layout_version=museum_app.PROJECT_AUTO_LAYOUT_VERSION,
            project_space_plan_file=museum_app.PROJECT_SPACE_PLAN_FILE,
            project_space_library=museum_app.PROJECT_SPACE_LIBRARY,
        )

    def test_projekti_file_route_delegates_to_project_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.project_views,
            'serve_project_file',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/projekti_files/example.pdf', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'example.pdf',
            project_directory='Projekti',
        )

    def test_cultural_heritage_route_delegates_to_collection_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.collection_management_views,
            'render_cultural_heritage_database',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/cultural_heritage_database', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_cultural_heritage_database=museum_app.get_cultural_heritage_database,
            prepare_collection_records_for_display=museum_app.prepare_collection_records_for_display,
            get_qr_collection_action_url=museum_app.get_qr_collection_action_url,
            get_image_upload_action_url=museum_app.get_image_upload_action_url,
        )

    def test_add_heritage_item_route_delegates_to_collection_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.collection_management_views,
            'handle_add_heritage_item',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/add_heritage_item', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_cultural_heritage_database=museum_app.get_cultural_heritage_database,
        )

    def test_add_collection_item_route_delegates_to_collection_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.collection_management_views,
            'handle_add_collection_item',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/add_collection_item/botany', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'botany',
            museum_databases_endpoint='museum_databases',
        )

    def test_botany_collection_route_delegates_to_collection_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.collection_management_views,
            'render_standard_collection_database',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/botany_collection', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            collection_name='Ботаничка збирка',
            collection_icon='bi-flower1',
            collection_type='botany',
            records=museum_app.BOTANY_COLLECTION_DATABASE['specimens'],
            statistics=museum_app.BOTANY_COLLECTION_DATABASE['statistics'],
            prepare_collection_records_for_display=museum_app.prepare_collection_records_for_display,
            get_qr_collection_action_url=museum_app.get_qr_collection_action_url,
            get_image_upload_action_url=museum_app.get_image_upload_action_url,
        )

    def test_meteorite_collection_route_delegates_to_collection_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.collection_management_views,
            'render_meteorite_collection',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/meteorite_collection', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_meteorite_collection_database=museum_app.get_meteorite_collection_database,
            prepare_collection_records_for_display=museum_app.prepare_collection_records_for_display,
            get_qr_collection_action_url=museum_app.get_qr_collection_action_url,
            get_image_upload_action_url=museum_app.get_image_upload_action_url,
        )

    def test_mineral_collection_route_delegates_to_collection_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.collection_management_views,
            'render_mineral_collection',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/mineral_collection', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_mineral_database=museum_app.get_mineral_database,
            get_image_upload_action_url=museum_app.get_image_upload_action_url,
        )

    def test_mineral_detail_route_delegates_to_collection_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.collection_management_views,
            'render_mineral_detail',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/mineral_detail/9', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            9,
            get_mineral_database=museum_app.get_mineral_database,
        )

    def test_rruff_detail_route_delegates_to_collection_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.collection_management_views,
            'render_rruff_detail',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/rruff/detail/9', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            9,
            get_mineral_database=museum_app.get_mineral_database,
        )

    def test_add_mineral_route_delegates_to_collection_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.collection_management_views,
            'handle_add_mineral',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/add_mineral', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_mineral_database=museum_app.get_mineral_database,
        )

    def test_edit_mineral_route_delegates_to_collection_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.collection_management_views,
            'handle_edit_mineral',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/edit_mineral/12', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            12,
            get_mineral_database=museum_app.get_mineral_database,
            get_image_storage=museum_app.get_image_storage,
        )

    def test_delete_mineral_image_route_delegates_to_collection_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.collection_management_views,
            'handle_delete_mineral_image',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.post(
                '/admin/edit_mineral/12/delete_image/test-image',
                base_url=self.base_url,
            )

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            12,
            'test-image',
            get_mineral_database=museum_app.get_mineral_database,
            get_image_storage=museum_app.get_image_storage,
        )

    def test_inventory_book_route_delegates_to_collection_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.collection_management_views,
            'render_inventory_book',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/inventory_book', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_inventory_reconciliation_route_delegates_to_collection_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.collection_management_views,
            'render_inventory_reconciliation',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/inventory_reconciliation', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_export_collection_pdf_route_delegates_to_collection_management_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.collection_management_views,
            'export_collection_to_pdf',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/export_collection_to_pdf/botany', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('botany')

    def test_museum_databases_route_delegates_to_museum_overview_module(self):
        self._login(role='admin')
        original_library_database = museum_app.LIBRARY_DATABASE
        museum_app.LIBRARY_DATABASE = {'books': [], 'statistics': {}}

        try:
            with patch.object(
                museum_app.museum_overview_views,
                'render_museum_databases',
                return_value=museum_app.app.response_class('ok', status=200),
            ) as mocked_handler:
                response = self.client.get('/admin/museum_databases', base_url=self.base_url)
        finally:
            active_library_database = museum_app.LIBRARY_DATABASE
            museum_app.LIBRARY_DATABASE = original_library_database

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            library_database=active_library_database,
            get_employee_directory=museum_app.get_employee_directory,
            get_museum_employees=museum_app.get_museum_employees,
            get_mineral_database=museum_app.get_mineral_database,
            get_meteorite_collection_database=museum_app.get_meteorite_collection_database,
            get_cultural_heritage_database=museum_app.get_cultural_heritage_database,
            get_exhibit_statistics=museum_app.get_exhibit_statistics,
            get_exhibition_statistics=museum_app.get_exhibition_statistics,
            bird_ringing_database=museum_app.bird_ringing_database,
            scientific_papers_database=museum_app.scientific_papers_database,
            botany_collection_database=museum_app.BOTANY_COLLECTION_DATABASE,
            ichthyology_collection_database=museum_app.ICHTHYOLOGY_COLLECTION_DATABASE,
            entomology_collection_database=museum_app.ENTOMOLOGY_COLLECTION_DATABASE,
            mycology_collection_database=museum_app.MYCOLOGY_COLLECTION_DATABASE,
            herpetology_collection_database=museum_app.HERPETOLOGY_COLLECTION_DATABASE,
            ornithology_collection_database=museum_app.ORNITHOLOGY_COLLECTION_DATABASE,
            paleozoology_collection_database=museum_app.PALEOZOOLOGY_COLLECTION_DATABASE,
            paleobotany_collection_database=museum_app.PALEOBOTANY_COLLECTION_DATABASE,
            petrology_collection_database=museum_app.PETROLOGY_COLLECTION_DATABASE,
            conservation_biology_database=museum_app.CONSERVATION_BIOLOGY_DATABASE,
            visitor_records=museum_app.VISITOR_RECORDS,
            research_projects=museum_app.RESEARCH_PROJECTS,
            get_qr_collection_action_url=museum_app.get_qr_collection_action_url,
            get_image_upload_action_url=museum_app.get_image_upload_action_url,
            get_image_upload_module_key=museum_app.get_image_upload_module_key,
            user_has_module_access=museum_app.user_has_module_access,
        )

    def test_scientific_papers_route_delegates_to_scientific_paper_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.scientific_paper_views,
            'render_scientific_papers',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/scientific_papers', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            scientific_papers_database=museum_app.scientific_papers_database,
            museum_databases_endpoint='museum_databases',
        )

    def test_scientific_paper_detail_route_delegates_to_scientific_paper_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.scientific_paper_views,
            'render_scientific_paper_detail',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/scientific_paper/17', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            paper_id=17,
            scientific_papers_database=museum_app.scientific_papers_database,
            list_endpoint='scientific_papers_view',
        )

    def test_scientific_papers_by_locality_route_delegates_to_scientific_paper_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.scientific_paper_views,
            'render_scientific_papers_by_locality',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get(
                '/admin/scientific_papers/locality/Test%20Locality',
                base_url=self.base_url,
            )

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            locality_name='Test Locality',
            scientific_papers_database=museum_app.scientific_papers_database,
        )

    def test_locality_papers_api_delegates_to_scientific_paper_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.scientific_paper_views,
            'api_locality_papers',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/locality-papers/Test%20Locality', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            locality_name='Test Locality',
            scientific_papers_database=museum_app.scientific_papers_database,
        )

    def test_feature_papers_api_delegates_to_scientific_paper_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.scientific_paper_views,
            'api_feature_papers',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get(
                '/api/map/feature-papers/locality/Test%20Feature',
                base_url=self.base_url,
            )

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            feature_type='locality',
            feature_name='Test Feature',
            map_feature_paper_enricher=museum_app.map_feature_paper_enricher,
        )

    def test_start_paper_enrichment_api_delegates_to_scientific_paper_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.scientific_paper_views,
            'api_start_paper_enrichment',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/admin/start-paper-enrichment', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            map_feature_paper_enricher=museum_app.map_feature_paper_enricher,
        )

    def test_paper_enrichment_status_api_delegates_to_scientific_paper_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.scientific_paper_views,
            'api_paper_enrichment_status',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/admin/paper-enrichment-status', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            map_feature_paper_enricher=museum_app.map_feature_paper_enricher,
        )

    def test_bird_ringing_database_route_delegates_to_bird_ringing_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.bird_ringing_views,
            'render_bird_ringing_database',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/bird_ringing_database', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            bird_ringing_database=museum_app.bird_ringing_database,
            museum_databases_endpoint='museum_databases',
        )

    def test_bird_ringing_record_detail_route_delegates_to_bird_ringing_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.bird_ringing_views,
            'render_bird_ringing_record_detail',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/bird_ringing_record/17', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            record_id=17,
            bird_ringing_database=museum_app.bird_ringing_database,
            list_endpoint='bird_ringing_database_view',
        )

    def test_add_bird_ringing_route_delegates_to_bird_ringing_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.bird_ringing_views,
            'handle_add_bird_ringing',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/add_bird_ringing', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            bird_ringing_database=museum_app.bird_ringing_database,
            detail_endpoint='bird_ringing_record_detail',
            list_endpoint='bird_ringing_database_view',
        )

    def test_museum_terminology_route_delegates_to_exhibition_planner_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.exhibition_planner_views,
            'render_museum_terminology',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/museum_terminology', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_exhibition_planner_route_delegates_to_exhibition_planner_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.exhibition_planner_views,
            'render_exhibition_planner',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/exhibition_planner', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_get_exhibitions_api_delegates_to_exhibition_planner_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.exhibition_planner_views,
            'api_get_exhibitions',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/exhibitions', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_create_exhibition_api_delegates_to_exhibition_planner_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.exhibition_planner_views,
            'api_create_exhibition',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/exhibitions', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_update_exhibition_api_delegates_to_exhibition_planner_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.exhibition_planner_views,
            'api_update_exhibition',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.put('/api/exhibitions/17', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(17)

    def test_delete_exhibition_api_delegates_to_exhibition_planner_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.exhibition_planner_views,
            'api_delete_exhibition',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.delete('/api/exhibitions/17', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(17)

    def test_update_exhibition_checklist_api_delegates_to_exhibition_planner_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.exhibition_planner_views,
            'api_update_exhibition_checklist',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.put('/api/exhibitions/17/checklist', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(17)

    def test_rruff_api_delegates_to_mineral_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mineral_science_views,
            'api_get_rruff_data',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/rruff/mineral/Quartz', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('Quartz')

    def test_cod_search_api_delegates_to_mineral_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mineral_science_views,
            'api_cod_search',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/cod/search/Quartz', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('Quartz')

    def test_cod_cif_api_delegates_to_mineral_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mineral_science_views,
            'api_cod_get_cif',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/cod/cif/123', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('123')

    def test_crystal_cif_api_delegates_to_mineral_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mineral_science_views,
            'api_crystal_get_cif_by_url',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/crystal/cif', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_crystal_local_cif_api_delegates_to_mineral_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mineral_science_views,
            'api_crystal_get_local_cif',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/crystal/local/R000001', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('R000001')

    def test_cod_structure_api_delegates_to_mineral_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mineral_science_views,
            'api_cod_get_structure',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/cod/structure/Quartz', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('Quartz')

    def test_geochemical_api_delegates_to_mineral_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mineral_science_views,
            'api_get_geochemical_data',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/geochemical/Quartz', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('Quartz')

    def test_local_rruff_api_delegates_to_mineral_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mineral_science_views,
            'api_get_local_rruff_data',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/local_rruff/Quartz', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('Quartz')

    def test_local_rruff_dif_api_delegates_to_mineral_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mineral_science_views,
            'api_get_local_rruff_dif',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/local_rruff/dif/Quartz', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('Quartz')

    def test_local_rruff_cif_api_delegates_to_mineral_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mineral_science_views,
            'api_get_local_rruff_cif',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/local_rruff/cif/Quartz', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('Quartz')

    def test_local_rruff_spectrum_api_delegates_to_mineral_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mineral_science_views,
            'api_get_local_rruff_spectrum',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/local_rruff/spectrum/raman/Quartz', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('raman', 'Quartz')

    def test_local_rruff_powder_xy_api_delegates_to_mineral_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mineral_science_views,
            'api_get_local_rruff_powder_xy',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/local_rruff/powder_xy/Quartz', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('Quartz')

    def test_local_rruff_image_api_delegates_to_mineral_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mineral_science_views,
            'api_serve_local_rruff_image',
            return_value=museum_app.app.response_class(b'ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/api/local_rruff/image/sample.png', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('sample.png')

    def test_local_rruff_microprobe_api_delegates_to_mineral_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mineral_science_views,
            'api_get_local_rruff_microprobe',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/local_rruff/microprobe/Quartz', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('Quartz')

    def test_depot_localities_api_delegates_to_depot_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.depot_science_views,
            'api_get_localities',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/depot/localities', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_mineral_database=museum_app.get_mineral_database,
        )

    def test_science_news_get_api_delegates_to_depot_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.depot_science_views,
            'api_get_science_news',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/science-news', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_science_news_post_api_delegates_to_depot_science_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.depot_science_views,
            'api_add_science_news',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/science-news', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_science_news_delete_api_delegates_to_depot_science_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.depot_science_views,
            'api_delete_science_news',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.delete('/api/science-news/item-1', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(news_id='item-1')

    def test_depot_locality_detail_api_delegates_to_depot_science_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.depot_science_views,
            'api_get_locality_detail',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/depot/locality/Rudnik', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'Rudnik',
            get_mineral_database=museum_app.get_mineral_database,
        )

    def test_website_news_api_delegates_to_dashboard_integration_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.dashboard_integration_views,
            'api_website_news',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/website-news', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            fetch_website_news=museum_app.fetch_website_news,
        )

    def test_weather_details_api_delegates_to_dashboard_integration_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.dashboard_integration_views,
            'api_weather_details',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/weather/details', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_current_weather=museum_app.get_current_weather,
            get_weather_forecast=museum_app.get_weather_forecast,
            get_rhmz_weather_warnings=museum_app.get_rhmz_weather_warnings,
            rhmz_warning_url=museum_app._RHMZ_WARNING_URL,
        )

    def test_library_database_route_delegates_to_dashboard_integration_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.dashboard_integration_views,
            'render_library_database',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/library_database', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_library_database=museum_app.get_library_database,
        )

    def test_nhm_data_portal_route_delegates_to_nhm_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.nhm_portal_views,
            'render_nhm_data_portal',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/nhm_data_portal', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_nhm_search_api_delegates_to_nhm_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.nhm_portal_views,
            'api_nhm_search',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/nhm/search', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_nhm_dataset_api_delegates_to_nhm_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.nhm_portal_views,
            'api_nhm_dataset',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/nhm/dataset/ds-1', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('ds-1')

    def test_nhm_resource_api_delegates_to_nhm_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.nhm_portal_views,
            'api_nhm_resource',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/nhm/resource/res-1', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('res-1')

    def test_nhm_datastore_api_delegates_to_nhm_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.nhm_portal_views,
            'api_nhm_datastore',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/nhm/datastore/res-1', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('res-1')

    def test_nhm_statistics_api_delegates_to_nhm_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.nhm_portal_views,
            'api_nhm_statistics',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/nhm/statistics', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_nhm_local_search_api_delegates_to_nhm_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.nhm_portal_views,
            'api_nhm_local_search',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/nhm/local/search', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_nhm_local_dataset_api_delegates_to_nhm_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.nhm_portal_views,
            'api_nhm_local_dataset',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/nhm/local/dataset/ds-local', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('ds-local')

    def test_nhm_local_statistics_api_delegates_to_nhm_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.nhm_portal_views,
            'api_nhm_local_statistics',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/nhm/local/statistics', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_nhm_local_tags_api_delegates_to_nhm_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.nhm_portal_views,
            'api_nhm_local_tags',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/nhm/local/tags', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_nhm_local_formats_api_delegates_to_nhm_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.nhm_portal_views,
            'api_nhm_local_formats',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/nhm/local/formats', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_nhm_local_authors_api_delegates_to_nhm_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.nhm_portal_views,
            'api_nhm_local_authors',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/nhm/local/authors', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_nhm_download_api_delegates_to_nhm_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.nhm_portal_views,
            'api_nhm_download_datasets',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/nhm/download', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_nhm_data_search_local_api_delegates_to_nhm_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.nhm_portal_views,
            'api_nhm_data_search_local',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/nhm/data/search/local', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_nhm_data_search_nhm_api_delegates_to_nhm_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.nhm_portal_views,
            'api_nhm_data_search_nhm',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/nhm/data/search/nhm', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_financial_requests_route_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'render_financial_requests_page',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/zahtevi/finansijski', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_day_off_route_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'render_day_off_request_page',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/zahtevi/slobodan-dan', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_vacation_route_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'render_vacation_request_page',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/zahtevi/godisnji-odmor', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_misc_request_route_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'render_misc_request_page',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/zahtevi/razno', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_financial_plan_route_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'render_financial_plan_page',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/finansije/plan', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_procurement_request_route_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'render_procurement_request_page',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/finansije/nabavka', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_field_activity_route_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'render_field_activity_page',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/terenska-aktivnost', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_business_trip_route_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'render_business_trip_request_page',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/zahtev-sluzbeni-put', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_museum_vehicles=museum_app.get_museum_vehicles,
        )

    def test_field_trip_create_api_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'api_field_trip_create',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/field-trip/create', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_vehicle_reservations=museum_app.get_vehicle_reservations,
            save_reservations=museum_app.save_reservations,
        )

    def test_accommodation_search_api_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'api_accommodation_search',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/accommodation/search', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_route_calculate_api_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'api_route_calculate',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/route/calculate', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_museum_vehicles=museum_app.get_museum_vehicles,
        )

    def test_procurement_save_api_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'api_nabavka_save',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/nabavka/save', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_procurement_list_api_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'api_nabavka_list',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/nabavka/list', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_procurement_export_api_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'api_nabavka_export_word',
            return_value=museum_app.app.response_class(b'ok', status=200),
        ) as mocked_handler:
            response = self.client.post('/api/nabavka/export-word', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_procurement_export_by_id_api_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'api_nabavka_export_word_by_id',
            return_value=museum_app.app.response_class(b'ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/api/nabavka/export-word/12', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            12,
            can_access_owned_record=museum_app.can_access_owned_record,
        )

    def test_financial_plan_save_api_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'api_finansijski_plan_save',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/finansijski-plan/save', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_postgres_connection=museum_app.get_postgres_connection,
        )

    def test_financial_plan_list_api_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'api_finansijski_plan_list',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/finansijski-plan/list', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_postgres_connection=museum_app.get_postgres_connection,
            current_user_is_admin=museum_app.current_user_is_admin,
        )

    def test_financial_plan_export_api_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'api_finansijski_plan_export_word',
            return_value=museum_app.app.response_class(b'ok', status=200),
        ) as mocked_handler:
            response = self.client.post('/api/finansijski-plan/export-word', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_financial_plan_export_by_id_api_delegates_to_travel_finance_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.travel_finance_views,
            'api_finansijski_plan_export_word_by_id',
            return_value=museum_app.app.response_class(b'ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/api/finansijski-plan/export-word/7', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            7,
            get_postgres_connection=museum_app.get_postgres_connection,
            can_access_owned_record=museum_app.can_access_owned_record,
        )

    def test_vehicle_reservations_route_delegates_to_vehicle_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.vehicle_depot_views,
            'render_vehicle_reservations',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/vehicle_reservations', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_museum_vehicles=museum_app.get_museum_vehicles,
            get_vehicle_reservations=museum_app.get_vehicle_reservations,
        )

    def test_add_vehicle_reservation_route_delegates_to_vehicle_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.vehicle_depot_views,
            'handle_add_vehicle_reservation',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.post('/add_vehicle_reservation', data={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            phase3a_databases=museum_app.__dict__.get('phase3a_databases'),
            get_vehicle_reservations=museum_app.get_vehicle_reservations,
            save_reservations=museum_app.save_reservations,
        )

    def test_vehicle_management_route_delegates_to_vehicle_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.vehicle_depot_views,
            'render_vehicle_management',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/vehicle_management', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_museum_vehicles=museum_app.get_museum_vehicles,
            get_vehicle_reservations=museum_app.get_vehicle_reservations,
        )

    def test_add_vehicle_route_delegates_to_vehicle_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.vehicle_depot_views,
            'handle_add_vehicle',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.post('/add_vehicle', data={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            phase3a_databases=museum_app.__dict__.get('phase3a_databases'),
            get_museum_vehicles=museum_app.get_museum_vehicles,
            save_vehicles=museum_app.save_vehicles,
        )

    def test_edit_vehicle_route_delegates_to_vehicle_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.vehicle_depot_views,
            'handle_edit_vehicle',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.post('/edit_vehicle', data={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            phase3a_databases=museum_app.__dict__.get('phase3a_databases'),
            get_museum_vehicles=museum_app.get_museum_vehicles,
            save_vehicles=museum_app.save_vehicles,
        )

    def test_delete_vehicle_route_delegates_to_vehicle_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.vehicle_depot_views,
            'handle_delete_vehicle',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.post('/delete_vehicle', data={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            phase3a_databases=museum_app.__dict__.get('phase3a_databases'),
            get_museum_vehicles=museum_app.get_museum_vehicles,
            get_vehicle_reservations=museum_app.get_vehicle_reservations,
            save_vehicles=museum_app.save_vehicles,
        )

    def test_virtual_depot_route_delegates_to_vehicle_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.vehicle_depot_views,
            'render_virtual_depot',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/virtual_depot', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_depot_boxes_api_delegates_to_vehicle_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.vehicle_depot_views,
            'api_get_depot_boxes',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/depot/boxes', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_depot_box_contents_api_delegates_to_vehicle_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.vehicle_depot_views,
            'api_get_box_contents',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/depot/box/12A', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('12A')

    def test_mail_client_page_route_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'render_mail_client_page',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/mail', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_mail_settings_page_route_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'render_mail_settings_page',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/mail/settings', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_mail_contacts_api_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'api_mail_contacts',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/mail/contacts', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            get_employee_directory=museum_app.get_employee_directory,
        )

    def test_mail_init_api_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'api_mail_init',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/mail/init', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_mail_folders_api_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'api_mail_folders',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/mail/folders', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_mail_messages_api_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'api_mail_messages',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/mail/messages', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_mail_message_api_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'api_mail_message',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/mail/message/77', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('77')

    def test_mail_attachment_api_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'api_mail_attachment',
            return_value=museum_app.app.response_class(b'ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/api/mail/attachment/77/1', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('77', 1)

    def test_mail_attachments_all_api_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'api_mail_attachments_all',
            return_value=museum_app.app.response_class(b'ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/api/mail/attachments-all/77', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('77')

    def test_mail_send_api_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'api_mail_send',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/mail/send', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_mail_delete_api_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'api_mail_delete',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/mail/delete', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_mail_read_state_api_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'api_mail_read_state',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/mail/read-state', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_mail_move_api_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'api_mail_move',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/mail/move', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_mail_check_api_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'api_mail_check',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/mail/check', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_mail_sync_api_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'api_mail_sync',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/mail/sync', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_mail_settings_get_api_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'api_mail_settings_get',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/mail/settings', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_mail_settings_save_api_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'api_mail_settings_save',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/mail/settings', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_mail_test_connection_api_delegates_to_mail_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.mail_views,
            'api_mail_test_connection',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/mail/test-connection', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_chat_room_page_route_delegates_to_chat_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.chat_views,
            'render_chat_room_page',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/chat', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_chat_messages_api_delegates_to_chat_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.chat_views,
            'api_chat_messages',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/chat/messages', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_chat_send_api_delegates_to_chat_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.chat_views,
            'api_chat_send',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/chat/send', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_chat_status_api_delegates_to_chat_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.chat_views,
            'api_chat_status',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/chat/status', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_chat_file_api_delegates_to_chat_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.chat_views,
            'api_chat_file',
            return_value=museum_app.app.response_class(b'ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/api/chat/file/test.bin', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with('test.bin')

    def test_chat_leave_api_delegates_to_chat_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.chat_views,
            'api_chat_leave',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/chat/leave', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_admin_maps_route_delegates_to_maps_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.maps_layer_views,
            'render_admin_maps',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/maps', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_admin_geological_timeline_route_delegates_to_maps_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.maps_layer_views,
            'render_admin_geological_timeline',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/geological-timeline', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_ore_deposits_api_delegates_to_maps_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_layer_views,
            'api_ore_deposits',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/ore-deposits', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(museum_app.os.path.dirname(museum_app.__file__))

    def test_stratigraphy_api_delegates_to_maps_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_layer_views,
            'api_stratigraphy_localities',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/stratigraphy', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(museum_app.os.path.dirname(museum_app.__file__))

    def test_paleontology_api_delegates_to_maps_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_layer_views,
            'api_paleo_localities',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/paleontology', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(museum_app.os.path.dirname(museum_app.__file__))

    def test_mining_operations_api_delegates_to_maps_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_layer_views,
            'api_mining_operations',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/mining-operations', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(museum_app.os.path.dirname(museum_app.__file__))

    def test_exploration_licenses_api_delegates_to_maps_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_layer_views,
            'api_exploration_licenses',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/exploration-licenses', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(museum_app.os.path.dirname(museum_app.__file__))

    def test_geological_sheets_api_delegates_to_maps_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_layer_views,
            'api_geological_sheets',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/geological-sheets', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(museum_app.os.path.dirname(museum_app.__file__))

    def test_geological_sheet_image_api_delegates_to_maps_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_layer_views,
            'api_geological_sheet_image',
            return_value=museum_app.app.response_class(b'ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/api/map/geological-sheet-image/SHEET1/karta', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'SHEET1',
            'karta',
            museum_app.os.path.dirname(museum_app.__file__),
        )

    def test_geological_sheet_tumac_api_delegates_to_maps_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_layer_views,
            'api_geological_sheet_tumac',
            return_value=museum_app.app.response_class(b'ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/api/map/geological-sheet-tumac/SHEET1', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'SHEET1',
            museum_app.os.path.dirname(museum_app.__file__),
        )

    def test_balkans_terrain_api_delegates_to_maps_terrain_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_terrain_views,
            'api_balkans_terrain',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/balkans-terrain', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            dem_dir=museum_app._DEM_DIR,
        )

    def test_map_tile_index_api_delegates_to_maps_terrain_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_terrain_views,
            'api_map_tile_index',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/tile-index', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            build_tile_index=museum_app._build_tile_index,
        )

    def test_map_tile_api_delegates_to_maps_terrain_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_terrain_views,
            'api_map_tile',
            return_value=museum_app.app.response_class(b'ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/api/map/tile/kml_image_L1_1_1', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            filename='kml_image_L1_1_1',
            extract_tile_to_cache=museum_app._extract_tile_to_cache,
            tile_cache_dir=museum_app._TILE_CACHE_DIR,
        )

    def test_map_3d_terrain_api_delegates_to_maps_terrain_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_terrain_views,
            'api_map_3d_terrain',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/3d-terrain', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            dem_dir=museum_app._DEM_DIR,
            build_tile_index=museum_app._build_tile_index,
            extract_tile_to_cache=museum_app._extract_tile_to_cache,
        )

    def test_create_field_data_api_delegates_to_field_data_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_field_data_views,
            'api_create_field_data',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/map/field-data', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_list_field_data_api_delegates_to_field_data_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_field_data_views,
            'api_list_field_data',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/field-data', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_get_field_data_api_delegates_to_field_data_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_field_data_views,
            'api_get_field_data',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/field-data/17', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            17,
            image_storage_factory=museum_app.get_image_storage,
        )

    def test_update_field_data_api_delegates_to_field_data_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_field_data_views,
            'api_update_field_data',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.put('/api/map/field-data/17', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(17)

    def test_delete_field_data_api_delegates_to_field_data_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_field_data_views,
            'api_delete_field_data',
            return_value=museum_app.app.response_class(
                response='{"success": true}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.delete('/api/map/field-data/17', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            17,
            image_storage_factory=museum_app.get_image_storage,
        )

    def test_geo_zone_map_api_delegates_to_geo_zone_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_geo_zone_views,
            'api_geo_zone_map',
            return_value=museum_app.app.response_class(b'ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/api/map/geo-zones/SHEET1/zone-map', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'SHEET1',
            app_root=museum_app.os.path.dirname(museum_app.__file__),
        )

    def test_geo_zone_metadata_api_delegates_to_geo_zone_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_geo_zone_views,
            'api_geo_zone_metadata',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/geo-zones/SHEET1/metadata', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'SHEET1',
            app_root=museum_app.os.path.dirname(museum_app.__file__),
        )

    def test_geo_zone_legend_api_delegates_to_geo_zone_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_geo_zone_views,
            'api_geo_zone_legend',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/geo-zones/SHEET1/legend', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'SHEET1',
            app_root=museum_app.os.path.dirname(museum_app.__file__),
        )

    def test_geo_zone_process_api_delegates_to_geo_zone_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.maps_geo_zone_views,
            'api_geo_zone_process',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/map/geo-zones/process', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            app_root=museum_app.os.path.dirname(museum_app.__file__),
        )

    def test_geo_zone_legend_update_api_delegates_to_geo_zone_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.maps_geo_zone_views,
            'api_geo_zone_legend_update',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/map/geo-zones/SHEET1/legend', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'SHEET1',
            app_root=museum_app.os.path.dirname(museum_app.__file__),
        )

    def test_geo_manual_calibration_get_api_delegates_to_geo_zone_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_geo_zone_views,
            'api_geo_manual_calibration_get',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/geo-zones/SHEET1/calibration', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'SHEET1',
            app_root=museum_app.os.path.dirname(museum_app.__file__),
        )

    def test_geo_manual_calibration_save_api_delegates_to_geo_zone_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.maps_geo_zone_views,
            'api_geo_manual_calibration_save',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/map/geo-zones/SHEET1/calibration', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'SHEET1',
            app_root=museum_app.os.path.dirname(museum_app.__file__),
        )

    def test_geo_manual_calibration_patch_api_delegates_to_geo_zone_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.maps_geo_zone_views,
            'api_geo_manual_calibration_patch_entry',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.patch('/api/map/geo-zones/SHEET1/calibration/entry', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'SHEET1',
            app_root=museum_app.os.path.dirname(museum_app.__file__),
        )

    def test_geo_manual_calibration_delete_api_delegates_to_geo_zone_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.maps_geo_zone_views,
            'api_geo_manual_calibration_delete',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.delete('/api/map/geo-zones/SHEET1/calibration', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'SHEET1',
            app_root=museum_app.os.path.dirname(museum_app.__file__),
        )

    def test_map_elevation_api_delegates_to_profile_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_profile_views,
            'api_map_elevation',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/elevation', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            sample_elevation_at_point=museum_app._sample_elevation_at_point,
        )

    def test_map_cross_profile_api_delegates_to_profile_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_profile_views,
            'api_map_cross_profile',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/cross-profile', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            app_root=museum_app.os.path.dirname(museum_app.__file__),
            haversine=museum_app._haversine_py,
            batch_sample_elevations=museum_app._batch_sample_elevations,
            interpolate_subsurface=museum_app._interpolate_subsurface,
        )

    def test_digitized_profiles_list_api_delegates_to_profile_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_profile_views,
            'api_digitized_profiles_list',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/digitized-profiles', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            profiles_path=museum_app._DIGITIZED_PROFILES_PATH,
        )

    def test_digitized_profile_get_api_delegates_to_profile_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_profile_views,
            'api_digitized_profile_get',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/digitized-profiles/prof-1', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'prof-1',
            profiles_path=museum_app._DIGITIZED_PROFILES_PATH,
        )

    def test_digitized_profile_create_api_delegates_to_profile_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_profile_views,
            'api_digitized_profile_create',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.post('/api/map/digitized-profiles', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            profiles_path=museum_app._DIGITIZED_PROFILES_PATH,
        )

    def test_digitized_profile_update_api_delegates_to_profile_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_profile_views,
            'api_digitized_profile_update',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.put('/api/map/digitized-profiles/prof-1', json={}, base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'prof-1',
            profiles_path=museum_app._DIGITIZED_PROFILES_PATH,
        )

    def test_digitized_profile_delete_api_delegates_to_profile_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_profile_views,
            'api_digitized_profile_delete',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.delete('/api/map/digitized-profiles/prof-1', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            'prof-1',
            profiles_path=museum_app._DIGITIZED_PROFILES_PATH,
        )

    def test_biodiversity_map_route_delegates_to_biodiversity_module(self):
        self._login(role='admin')

        with patch.object(
            museum_app.maps_biodiversity_views,
            'render_admin_biodiversity_map',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_handler:
            response = self.client.get('/admin/biodiversity-map', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with()

    def test_bird_ringing_localities_api_delegates_to_biodiversity_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_biodiversity_views,
            'api_bird_ringing_localities',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/bird-ringing-localities', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            app_root=museum_app.os.path.dirname(museum_app.__file__),
            bird_ringing_database=museum_app.bird_ringing_database,
        )

    def test_bird_ringing_filters_api_delegates_to_biodiversity_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_biodiversity_views,
            'api_bird_ringing_filters',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/bird-ringing-filters', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            bird_ringing_database=museum_app.bird_ringing_database,
        )

    def test_collection_localities_api_delegates_to_biodiversity_module(self):
        self._login(role='employee')

        with patch.object(
            museum_app.maps_biodiversity_views,
            'api_collection_localities',
            return_value=museum_app.app.response_class(
                response='{}',
                status=200,
                mimetype='application/json',
            ),
        ) as mocked_handler:
            response = self.client.get('/api/map/collection-localities', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked_handler.assert_called_once_with(
            app_root=museum_app.os.path.dirname(museum_app.__file__),
            botany_collection_database=museum_app.BOTANY_COLLECTION_DATABASE,
            ornithology_collection_database=museum_app.ORNITHOLOGY_COLLECTION_DATABASE,
            ichthyology_collection_database=museum_app.ICHTHYOLOGY_COLLECTION_DATABASE,
            herpetology_collection_database=museum_app.HERPETOLOGY_COLLECTION_DATABASE,
            entomology_collection_database=museum_app.ENTOMOLOGY_COLLECTION_DATABASE,
            mycology_collection_database=museum_app.MYCOLOGY_COLLECTION_DATABASE,
        )


if __name__ == '__main__':
    unittest.main()
