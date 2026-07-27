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
        def save_theme_preferences(self, email, mode, accent, style, density,
                                   palette='plava-klasicna'):
            calls.append((email, mode, accent, style, density, palette))
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

    # palette omitted from the POST -> falls back to the current choice, which
    # in a fresh request context is the app default 'plava-klasicna'.
    assert calls == [('kustos@nhmbeo.rs', 'dark', 'petrolej',
                      'institucionalna', 'komforno', 'plava-klasicna')]


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


def test_current_theme_defaults(theme_app):
    with theme_app.test_request_context('/'):
        assert core_app_views.current_theme_mode() == 'system'
        assert core_app_views.current_theme_accent() == 'zelena'
        assert core_app_views.current_theme_style() == 'institucionalna'
        assert core_app_views.current_theme_density() == 'komforno'


def test_current_theme_normalizes_garbage_values(theme_app):
    with theme_app.test_request_context(
        '/', headers={'Cookie': 'museum_theme=neon; museum_accent=pink; museum_style=brutalizam; museum_density=zbijeno'}
    ):
        assert core_app_views.current_theme_mode() == 'system'
        assert core_app_views.current_theme_accent() == 'zelena'
        assert core_app_views.current_theme_style() == 'institucionalna'
        assert core_app_views.current_theme_density() == 'komforno'


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

def test_set_theme_accepts_contrast_mode(theme_app):
    with theme_app.test_request_context(
        '/set_theme',
        method='POST',
        json={'mode': 'contrast', 'accent': 'zelena'},
    ):
        response = core_app_views.set_theme_preference()
        assert session['museum_theme'] == 'contrast'

    assert response.status_code == 200
    assert any('museum_theme=contrast' in c for c in response.headers.getlist('Set-Cookie'))


def test_current_theme_reads_contrast_cookie(theme_app):
    with theme_app.test_request_context(
        '/', headers={'Cookie': 'museum_theme=contrast'}
    ):
        assert core_app_views.current_theme_mode() == 'contrast'


def test_set_theme_stores_style_and_density(theme_app, monkeypatch):
    calls = []

    class FakeAuth:
        def save_theme_preferences(self, email, mode, accent, style, density,
                                   palette='plava-klasicna'):
            calls.append((email, mode, accent, style, density, palette))
            return True

    import postgres_auth
    monkeypatch.setattr(postgres_auth, 'get_postgres_auth', lambda: FakeAuth())

    with theme_app.test_request_context(
        '/set_theme',
        method='POST',
        json={'mode': 'dark', 'accent': 'bordo', 'style': 'terenska', 'density': 'kompakt'},
    ):
        session['user_email'] = 'kustos@nhmbeo.rs'
        response = core_app_views.set_theme_preference()
        assert session['museum_style'] == 'terenska'
        assert session['museum_density'] == 'kompakt'

    assert calls == [('kustos@nhmbeo.rs', 'dark', 'bordo', 'terenska',
                      'kompakt', 'plava-klasicna')]
    cookies = response.headers.getlist('Set-Cookie')
    assert any('museum_style=terenska' in c for c in cookies)
    assert any('museum_density=kompakt' in c for c in cookies)


def test_set_theme_rejects_invalid_style(theme_app):
    with theme_app.test_request_context(
        '/set_theme',
        method='POST',
        json={'mode': 'light', 'accent': 'zelena', 'style': 'brutalizam'},
    ):
        response = core_app_views.set_theme_preference()

    status = response[1] if isinstance(response, tuple) else response.status_code
    assert status == 400


def test_set_theme_defaults_axes_when_absent(theme_app):
    """Stariji klijenti šalju samo mode+accent — style/density padaju na default."""
    with theme_app.test_request_context(
        '/set_theme',
        method='POST',
        json={'mode': 'dark', 'accent': 'zelena'},
    ):
        response = core_app_views.set_theme_preference()
        assert session['museum_style'] == 'institucionalna'
        assert session['museum_density'] == 'komforno'

    assert response.status_code == 200


def test_set_theme_stores_named_palette(theme_app):
    """Imenovana plava paleta (migracija 033) se čuva u sesiji i kolačiću."""
    with theme_app.test_request_context(
        '/set_theme',
        method='POST',
        json={'mode': 'light', 'accent': 'zelena', 'palette': 'plava-muzejska'},
    ):
        response = core_app_views.set_theme_preference()
        assert session['museum_palette'] == 'plava-muzejska'

    cookies = response.headers.getlist('Set-Cookie')
    assert any('museum_palette=plava-muzejska' in c for c in cookies)


def test_set_theme_rejects_invalid_palette(theme_app):
    with theme_app.test_request_context(
        '/set_theme',
        method='POST',
        json={'mode': 'light', 'accent': 'zelena', 'palette': 'plava-neonska'},
    ):
        response = core_app_views.set_theme_preference()

    status = response[1] if isinstance(response, tuple) else response.status_code
    assert status == 400


def test_set_theme_palette_falls_back_to_current(theme_app):
    """Delimičan POST (bez palette) ne resetuje već izabranu paletu."""
    with theme_app.test_request_context(
        '/set_theme',
        method='POST',
        json={'mode': 'light', 'accent': 'zelena'},
    ):
        session['museum_palette'] = 'plava-tamna'
        core_app_views.set_theme_preference()
        assert session['museum_palette'] == 'plava-tamna'


def test_current_theme_palette_defaults(theme_app):
    with theme_app.test_request_context('/'):
        assert core_app_views.current_theme_palette() == 'plava-klasicna'


def test_normalize_theme_palette_rejects_unknown():
    assert core_app_views.normalize_theme_palette('heritage') == 'heritage'
    assert core_app_views.normalize_theme_palette('plava-tamna') == 'plava-tamna'
    assert core_app_views.normalize_theme_palette('nepostojeca') == 'plava-klasicna'
    assert core_app_views.normalize_theme_palette(None) == 'plava-klasicna'
