"""Reproducing tests for dashboard cluster low-severity hardening (phase C)."""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-dashboard')

import threading

from flask import Flask

import dashboard_data_support
import dashboard_integration_views


def _make_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret'
    return app


# Finding 1: corrupt weather cache file must be treated as a cache miss,
# not propagate json.JSONDecodeError (a ValueError, not an OSError).
def test_corrupt_weather_cache_treated_as_miss(tmp_path, monkeypatch):
    cache_file = tmp_path / 'weather_forecast_daily_cache.json'
    cache_file.write_text('{ this is not valid json', encoding='utf-8')

    monkeypatch.setattr(
        dashboard_data_support, '_WEATHER_FORECAST_CACHE_PATH', cache_file
    )

    bundle, is_stale = dashboard_data_support._read_weather_bundle_from_disk(
        '2026-05-29', allow_stale=False
    )

    assert bundle is None
    assert is_stale is False


# Finding 2: negative / zero ?limit must be clamped to at least 1 before
# reaching fetch_website_news, never yielding wrong/empty slices.
def test_website_news_limit_floored_for_negative_and_zero():
    app = _make_app()
    captured = {}

    def fake_fetch(limit):
        captured['limit'] = limit
        return [{'title': 'x'}]

    for raw in ('-5', '0'):
        captured.clear()
        with app.test_request_context('/?limit=' + raw):
            dashboard_integration_views.api_website_news(fetch_website_news=fake_fetch)
        assert captured['limit'] >= 1, f'limit={raw} not floored: {captured}'

    # Upper clamp must still hold.
    captured.clear()
    with app.test_request_context('/?limit=100'):
        dashboard_integration_views.api_website_news(fetch_website_news=fake_fetch)
    assert captured['limit'] == 12


# Finding 5: total_categories must match the NULL-excluding dropdown count.
def test_total_categories_excludes_none():
    app = _make_app()

    def fake_get_library_database():
        return {
            'books': [
                {'category': 'Геологија', 'status': 'доступна'},
                {'category': None, 'status': 'доступна'},
                {'category': 'Геологија', 'status': 'позајмљена'},
            ],
            'categories': ['Геологија'],
            'statistics': {},
        }

    captured = {}

    def fake_render(template, **context):
        captured.update(context)
        return ''

    import dashboard_integration_views as views

    original_render = views.render_template
    views.render_template = fake_render
    try:
        with app.test_request_context('/'):
            views.render_library_database(get_library_database=fake_get_library_database)
    finally:
        views.render_template = original_render

    assert captured['statistics']['total_categories'] == 1


# Finding 4: _rhmz_warning_cache must be guarded by a dedicated lock.
def test_rhmz_warning_cache_has_lock():
    assert hasattr(dashboard_data_support, '_rhmz_warning_cache_lock')
    assert isinstance(
        dashboard_data_support._rhmz_warning_cache_lock, type(threading.Lock())
    )


# Finding 7: stale-disk fallback returns a clean (bundle, True) without a
# confusing no-op ternary; behavior stays stale=True.
def test_stale_disk_fallback_marks_stale(monkeypatch):
    sentinel = {'location': 'Београд', 'current': {'condition': 'clear'}}

    monkeypatch.setattr(
        dashboard_data_support,
        '_today_weather_cache_key',
        lambda: '2026-05-29',
    )

    with dashboard_data_support._weather_daily_bundle_lock:
        dashboard_data_support._weather_daily_bundle_cache['data'] = None
        dashboard_data_support._weather_daily_bundle_cache['cache_date'] = None

    def fake_read_disk(cache_date=None, *, allow_stale=False):
        if allow_stale:
            return sentinel, True
        return None, False

    def fake_fetch(cache_date):
        raise RuntimeError('network down')

    monkeypatch.setattr(
        dashboard_data_support, '_read_weather_bundle_from_disk', fake_read_disk
    )
    monkeypatch.setattr(
        dashboard_data_support, '_fetch_daily_weather_bundle', fake_fetch
    )

    bundle, is_stale = dashboard_data_support._get_or_fetch_daily_weather_bundle()

    assert bundle is sentinel
    assert is_stale is True
