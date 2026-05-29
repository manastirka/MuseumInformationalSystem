import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-mineral-science')

import json
from unittest import mock

import app as museum_app
import mineral_science_views


# ---------------------------------------------------------------------------
# Finding: Authenticated SSRF in /api/crystal/cif (api_crystal_get_cif_by_url)
# The view must validate the user-supplied URL (scheme + host allowlist)
# BEFORE performing any server-side fetch.
# ---------------------------------------------------------------------------

INTERNAL_URLS = [
    'http://127.0.0.1:6379/',
    'http://localhost/admin',
    'http://169.254.169.254/latest/meta-data/',
    'http://redis:6379/',
    'file:///etc/passwd',
    'gopher://127.0.0.1:6379/_INFO',
    'http://evil.example.com/data_x',
    'https://crystallography.net.evil.com/x.cif',
]


def _call_with_url(url):
    fake_db = mock.MagicMock()
    fake_db.get_cif_data.return_value = 'data_test\n_cell_length_a 1.0\n'
    with mock.patch('cod_database.get_cod_database', return_value=fake_db):
        with museum_app.app.test_request_context('/api/crystal/cif', query_string={'url': url}):
            response = mineral_science_views.api_crystal_get_cif_by_url()
    return response, fake_db


def test_internal_urls_are_rejected_without_fetching():
    for url in INTERNAL_URLS:
        response, fake_db = _call_with_url(url)
        body = response[0] if isinstance(response, tuple) else response
        status = response[1] if isinstance(response, tuple) else 200
        payload = json.loads(body.get_data(as_text=True))
        assert status == 400, f"expected 400 for {url}, got {status}: {payload}"
        assert payload.get('success') is False, url
        # The server must NOT have attempted to fetch the SSRF target.
        fake_db.get_cif_data.assert_not_called()


def test_allowlisted_crystallography_url_is_fetched():
    response, fake_db = _call_with_url('https://www.crystallography.net/cod/1000001.cif')
    body = response[0] if isinstance(response, tuple) else response
    status = response[1] if isinstance(response, tuple) else 200
    payload = json.loads(body.get_data(as_text=True))
    assert status == 200, payload
    assert payload.get('success') is True
    fake_db.get_cif_data.assert_called_once_with('https://www.crystallography.net/cod/1000001.cif')


def test_missing_url_still_returns_400():
    fake_db = mock.MagicMock()
    with mock.patch('cod_database.get_cod_database', return_value=fake_db):
        with museum_app.app.test_request_context('/api/crystal/cif'):
            response = mineral_science_views.api_crystal_get_cif_by_url()
    body = response[0] if isinstance(response, tuple) else response
    status = response[1] if isinstance(response, tuple) else 200
    payload = json.loads(body.get_data(as_text=True))
    assert status == 400
    assert payload.get('success') is False
    fake_db.get_cif_data.assert_not_called()
