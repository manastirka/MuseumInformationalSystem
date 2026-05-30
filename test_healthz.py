"""Test the /healthz readiness probe."""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-healthz')

import app as museum_app  # noqa: E402


def test_healthz_is_public_and_returns_status():
    client = museum_app.app.test_client()
    resp = client.get('/healthz', base_url='https://localhost')
    # No DATABASE_URL/REDIS_URL in the test env -> checks are skipped, so healthy.
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['status'] == 'ok'
    assert 'db' in data and 'redis' in data


def test_healthz_requires_no_login():
    # An unauthenticated client must reach it (not redirected to /login).
    client = museum_app.app.test_client()
    resp = client.get('/healthz', base_url='https://localhost')
    assert resp.status_code in (200, 503)
    assert resp.is_json
