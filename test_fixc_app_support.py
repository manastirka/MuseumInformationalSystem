"""Phase C app-support cluster: low-severity hardening fix tests."""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-app-support')

import pytest
from flask import Flask

import app_request_support
import core_app_views


@pytest.fixture
def weather_app():
    """Minimal Flask app with the shared template context processor registered."""
    flask_app = Flask(__name__)
    flask_app.config['SECRET_KEY'] = 'test-secret'
    return flask_app


def test_context_processor_tolerates_weather_dict_missing_condition(weather_app):
    """Finding 1: a weather dict without 'condition' must not crash rendering."""

    def get_current_weather():
        # Returns successfully but omits 'condition' (the latent malformed case).
        return {'temperature': 12, 'windspeed': 3, 'description': 'foo'}

    app_request_support.register_template_context(
        weather_app,
        current_dir='/tmp',
        get_current_weather=get_current_weather,
        default_weather_condition='clear',
        user_has_module_access=lambda *a, **k: False,
    )

    processor = weather_app.template_context_processors[None][-1]
    with weather_app.test_request_context('/'):
        context = processor()

    assert context['weather_condition'] == 'clear'


def test_context_processor_uses_returned_condition_when_present(weather_app):
    """Sanity: a well-formed weather dict still surfaces its condition."""

    def get_current_weather():
        return {'condition': 'rain', 'temperature': 5}

    app_request_support.register_template_context(
        weather_app,
        current_dir='/tmp',
        get_current_weather=get_current_weather,
        default_weather_condition='clear',
        user_has_module_access=lambda *a, **k: False,
    )

    processor = weather_app.template_context_processors[None][-1]
    with weather_app.test_request_context('/'):
        context = processor()

    assert context['weather_condition'] == 'rain'


def test_language_cookie_secure_under_https(weather_app):
    """Finding 2: museum_lang cookie must carry Secure when served over HTTPS."""
    with weather_app.test_request_context(
        '/set_language',
        method='POST',
        json={'language': 'en'},
        base_url='https://example.org',
    ):
        response = core_app_views.set_language_preference()

    set_cookie = response.headers.get('Set-Cookie', '')
    assert 'museum_lang=en' in set_cookie
    assert 'Secure' in set_cookie


def test_language_cookie_not_secure_under_http(weather_app):
    """Finding 2: plain HTTP request must not set Secure (would drop the cookie)."""
    with weather_app.test_request_context(
        '/set_language',
        method='POST',
        json={'language': 'sr-Latn'},
        base_url='http://example.org',
    ):
        response = core_app_views.set_language_preference()

    set_cookie = response.headers.get('Set-Cookie', '')
    assert 'museum_lang=sr-Latn' in set_cookie
    assert 'Secure' not in set_cookie


def test_change_password_endpoint_is_parameterized(weather_app):
    """Finding 3: handle_change_password should redirect via the injected endpoint."""
    import inspect

    sig = inspect.signature(core_app_views.handle_change_password)
    assert 'change_password_endpoint' in sig.parameters
