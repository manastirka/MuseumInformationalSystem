#!/usr/bin/env python3
"""Regression tests for centralized admin mail settings hardening."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from cryptography.fernet import Fernet

import mail_client


class AdminMailSettingsHardeningTests(unittest.TestCase):
    def setUp(self):
        self.admin_views = Path('admin_user_management_views.py').read_text(encoding='utf-8')
        self.template = Path('templates/admin_mail_settings.html').read_text(encoding='utf-8')
        self.start_script = Path('systemd_start.sh').read_text(encoding='utf-8')

    def test_admin_mail_apis_return_json_for_unexpected_failures(self):
        self.assertIn('Unexpected mail settings save failure', self.admin_views)
        self.assertIn("return jsonify({'success': False, 'message': 'Грешка при чувању mail подешавања.'}), 500", self.admin_views)
        self.assertIn('Mail credential encryption failed', self.admin_views)
        self.assertIn("return jsonify({'success': False, 'message': 'Грешка при припреми mail лозинке.'}), 500", self.admin_views)
        self.assertIn('Unexpected mail connection test failure', self.admin_views)
        self.assertIn("return jsonify({'success': False, 'message': 'Грешка при тестирању mail везе.'}), 500", self.admin_views)

    def test_admin_mail_page_surfaces_non_json_server_errors(self):
        self.assertIn('async readJsonResponse(response)', self.template)
        self.assertIn('Сервер није вратио исправан одговор', self.template)
        self.assertIn('const data = await this.readJsonResponse(response);', self.template)
        self.assertNotIn("this.saveResult = 'Грешка при чувању.';", self.template)

    def test_systemd_start_exports_existing_mail_key_file(self):
        self.assertIn('export MAIL_SETTINGS_ENCRYPTION_KEY="$(tr -d', self.start_script)
        self.assertIn('[ -r "data/.mail_key" ]', self.start_script)

    def test_production_uses_existing_local_mail_key_when_env_key_is_absent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            key_file = Path(tmpdir) / '.mail_key'
            key_file.write_bytes(Fernet.generate_key())

            with mock.patch.object(mail_client, '_fernet_instance', None):
                with mock.patch.object(mail_client, 'KEY_FILE', key_file):
                    with mock.patch.dict(os.environ, {'FLASK_ENV': 'production'}, clear=False):
                        with mock.patch.dict(os.environ, {mail_client.MAIL_SETTINGS_KEY_ENV: ''}, clear=False):
                            encrypted = mail_client._encrypt('secret')
                            self.assertEqual(mail_client._decrypt(encrypted), 'secret')


if __name__ == '__main__':
    unittest.main()
