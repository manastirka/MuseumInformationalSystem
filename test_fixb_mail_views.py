"""Regression tests for mail_views (fix batch B)."""

import os
import sys
import types

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-mail-views')

import json
from unittest import mock

from flask import Flask

import mail_views


def _make_app():
    app = Flask(__name__)
    app.secret_key = 'test-secret'
    return app


def _fake_mail_client_module():
    """A stand-in mail_client module that won't touch the network/DB."""
    mod = types.ModuleType('mail_client')
    mod.MAIL_ALLOWED_HOSTS_KEY = 'mail_allowed_hosts'
    mod.get_user_settings = lambda email: {}
    mod.get_allowed_mail_hosts = lambda: []
    mod.normalize_allowed_mail_hosts = lambda hosts: list(hosts or [])
    mod._encrypt = lambda value: 'enc:' + value
    mod.save_user_settings = lambda email, settings: True
    mod.validate_mail_server_settings = lambda settings, allowed_hosts=None: settings
    return mod


def test_settings_save_non_numeric_imap_port_returns_400():
    app = _make_app()
    payload = {
        'imap_server': 'imap.example.com',
        'imap_port': 'abc',
        'smtp_server': 'smtp.example.com',
        'smtp_port': 587,
        'email_address': 'user@example.com',
        'password': 'secret',
    }
    fake_mail_client = _fake_mail_client_module()
    with app.test_request_context(
        '/api/mail/settings',
        method='POST',
        data=json.dumps(payload),
        content_type='application/json',
    ):
        from flask import session
        session['user_email'] = 'user@example.com'
        with mock.patch.dict(sys.modules, {'mail_client': fake_mail_client}), \
                mock.patch.object(
                    mail_views.admin_system_views, 'load_saved_settings', return_value={}
                ):
            response = mail_views.api_mail_settings_save()

    body, status = response
    assert status == 400
    assert body.get_json()['success'] is False
    assert body.get_json()['message'] == 'Порт мора бити број.'


def test_settings_save_non_numeric_smtp_port_returns_400():
    app = _make_app()
    payload = {
        'imap_server': 'imap.example.com',
        'imap_port': 993,
        'smtp_server': 'smtp.example.com',
        'smtp_port': 'not-a-number',
        'email_address': 'user@example.com',
        'password': 'secret',
    }
    fake_mail_client = _fake_mail_client_module()
    with app.test_request_context(
        '/api/mail/settings',
        method='POST',
        data=json.dumps(payload),
        content_type='application/json',
    ):
        from flask import session
        session['user_email'] = 'user@example.com'
        with mock.patch.dict(sys.modules, {'mail_client': fake_mail_client}), \
                mock.patch.object(
                    mail_views.admin_system_views, 'load_saved_settings', return_value={}
                ):
            response = mail_views.api_mail_settings_save()

    body, status = response
    assert status == 400
    assert body.get_json()['success'] is False
    assert body.get_json()['message'] == 'Порт мора бити број.'


def test_settings_save_valid_ports_succeeds():
    app = _make_app()
    payload = {
        'imap_server': 'imap.example.com',
        'imap_port': '993',
        'smtp_server': 'smtp.example.com',
        'smtp_port': 587,
        'email_address': 'user@example.com',
        'password': 'secret',
    }
    fake_mail_client = _fake_mail_client_module()
    with app.test_request_context(
        '/api/mail/settings',
        method='POST',
        data=json.dumps(payload),
        content_type='application/json',
    ):
        from flask import session
        session['user_email'] = 'user@example.com'
        with mock.patch.dict(sys.modules, {'mail_client': fake_mail_client}), \
                mock.patch.object(
                    mail_views.admin_system_views, 'load_saved_settings', return_value={}
                ), \
                mock.patch.object(
                    mail_views.admin_system_views, 'save_settings', return_value=True
                ):
            response = mail_views.api_mail_settings_save()

    body = response
    assert body.get_json()['success'] is True
