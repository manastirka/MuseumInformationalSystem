#!/usr/bin/env python3
"""Regression tests for production-readiness fixes."""

import os
import unittest
from unittest.mock import patch

from flask import Flask, jsonify, session

import config as config_module
import security_utils


class FakeLogger:
    def __init__(self):
        self.calls = []

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

    def test_production_config_requires_secret_key(self):
        app = Flask(__name__)
        app.config.from_object(config_module.ProductionConfig)
        app.config['SECRET_KEY'] = None

        with self.assertRaises(RuntimeError):
            config_module.ProductionConfig.init_app(app)

    def test_production_config_tolerates_missing_syslog(self):
        app = Flask(__name__)
        app.config.from_object(config_module.ProductionConfig)
        app.config['SECRET_KEY'] = 'production-secret'

        with patch('logging.handlers.SysLogHandler', side_effect=PermissionError('no syslog')):
            config_module.ProductionConfig.init_app(app)


class SecurityUtilsTests(unittest.TestCase):
    def test_init_login_tracker_preserves_object_identity(self):
        original_tracker = security_utils.login_tracker
        configured_tracker = security_utils.init_login_tracker(None)

        self.assertIs(original_tracker, configured_tracker)

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


if __name__ == '__main__':
    unittest.main()
