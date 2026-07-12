"""Tests for per-user UI theme preference (mode + accent, Faza 3 tema)."""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-theme-prefs')

import pytest
from flask import Flask, session

import app_request_support
import core_app_views


@pytest.fixture
def theme_app():
    """Minimal Flask app for exercising the theme preference helpers."""
    flask_app = Flask(__name__)
    flask_app.config['SECRET_KEY'] = 'test-secret'
    return flask_app


def test_set_theme_stores_session_and_cookies(theme_app):
    with theme_app.test_request_context(
        '/set_theme',
        method='POST',
        json={'mode': 'dark', 'accent': 'bordo'},
    ):
        response = core_app_views.set_theme_preference()
        assert session['museum_theme'] == 'dark'
        assert session['museum_accent'] == 'bordo'

    cookies = response.headers.getlist('Set-Cookie')
    assert any('museum_theme=dark' in c for c in cookies)
    assert any('museum_accent=bordo' in c for c in cookies)


def test_set_theme_rejects_invalid_mode(theme_app):
    with theme_app.test_request_context(
        '/set_theme',
        method='POST',
        json={'mode': 'neon', 'accent': 'zelena'},
    ):
        response = core_app_views.set_theme_preference()

    status = response[1] if isinstance(response, tuple) else response.status_code
    assert status == 400
    body = response[0] if isinstance(response, tuple) else response
    assert 'museum_theme' not in body.headers.get('Set-Cookie', '')


def test_set_theme_rejects_invalid_accent(theme_app):
    with theme_app.test_request_context(
        '/set_theme',
        method='POST',
        json={'mode': 'light', 'accent': 'pink'},
    ):
        response = core_app_views.set_theme_preference()

    status = response[1] if isinstance(response, tuple) else response.status_code
    assert status == 400


def test_set_theme_persists_to_db_for_logged_in_user(theme_app, monkeypatch):
    calls = []

    class FakeAuth:
        def save_theme_preferences(self, email, mode, accent):
            calls.append((email, mode, accent))
            return True

    import postgres_auth
    monkeypatch.setattr(postgres_auth, 'get_postgres_auth', lambda: FakeAuth())

    with theme_app.test_request_context(
        '/set_theme',
        method='POST',
        json={'mode': 'dark', 'accent': 'petrolej'},
    ):
        session['user_email'] = 'kustos@nhmbeo.rs'
        core_app_views.set_theme_preference()

    assert calls == [('kustos@nhmbeo.rs', 'dark', 'petrolej')]


def test_set_theme_skips_db_for_anonymous_user(theme_app, monkeypatch):
    import postgres_auth

    def explode():
        raise AssertionError('DB must not be touched for anonymous users')

    monkeypatch.setattr(postgres_auth, 'get_postgres_auth', explode)

    with theme_app.test_request_context(
        '/set_theme',
        method='POST',
        json={'mode': 'light', 'accent': 'zelena'},
    ):
        response = core_app_views.set_theme_preference()

    assert response.status_code == 200


def test_theme_cookies_secure_under_https(theme_app):
    with theme_app.test_request_context(
        '/set_theme',
        method='POST',
        json={'mode': 'dark', 'accent': 'oker'},
        base_url='https://example.org',
    ):
        response = core_app_views.set_theme_preference()

    for cookie in response.headers.getlist('Set-Cookie'):
        assert 'Secure' in cookie


def test_current_theme_defaults_to_system_and_green(theme_app):
    with theme_app.test_request_context('/'):
        assert core_app_views.current_theme_mode() == 'system'
        assert core_app_views.current_theme_accent() == 'zelena'


def test_current_theme_normalizes_garbage_values(theme_app):
    with theme_app.test_request_context(
        '/', headers={'Cookie': 'museum_theme=neon; museum_accent=pink'}
    ):
        assert core_app_views.current_theme_mode() == 'system'
        assert core_app_views.current_theme_accent() == 'zelena'


def test_current_theme_reads_cookie_then_session(theme_app):
    with theme_app.test_request_context(
        '/', headers={'Cookie': 'museum_theme=dark; museum_accent=bordo'}
    ):
        assert core_app_views.current_theme_mode() == 'dark'
        assert core_app_views.current_theme_accent() == 'bordo'
        session['museum_theme'] = 'light'
        session['museum_accent'] = 'oker'
        assert core_app_views.current_theme_mode() == 'light'
        assert core_app_views.current_theme_accent() == 'oker'


def test_context_processor_exposes_theme(theme_app):
    app_request_support.register_template_context(
        theme_app,
        current_dir='/tmp',
        get_current_weather=lambda: {'condition': 'clear'},
        default_weather_condition='clear',
        user_has_module_access=lambda *a, **k: False,
    )

    processor = theme_app.template_context_processors[None][-1]
    with theme_app.test_request_context(
        '/', headers={'Cookie': 'museum_theme=dark; museum_accent=petrolej'}
    ):
        context = processor()

    assert context['current_theme_mode'] == 'dark'
    assert context['current_theme_accent'] == 'petrolej'
