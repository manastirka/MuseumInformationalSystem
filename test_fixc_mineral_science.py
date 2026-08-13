import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-mineral-science')

import json
from unittest import mock

import app as museum_app
import depot_science_views
import mineral_science_views
import crystal_structure_databases


def _unwrap(response):
    body = response[0] if isinstance(response, tuple) else response
    status = response[1] if isinstance(response, tuple) else 200
    payload = json.loads(body.get_data(as_text=True))
    return status, payload


# ---------------------------------------------------------------------------
# Finding: non-string JSON values crash api_add_science_news (unhandled 500)
# A non-string title or an explicit null summary passes the truthiness guard
# but used to raise TypeError on slicing before the try/except.
# ---------------------------------------------------------------------------

def _add_news(data):
    # Skladište (krug 4: science_news_store, PG/JSON) je mokovano — testira se
    # samo validacija/koercija ulaza u api_add_science_news.
    with mock.patch.object(depot_science_views.science_news_store,
                           'add_news_item') as upd:
        upd.side_effect = lambda *a, **k: None
        with museum_app.app.test_request_context(
            '/api/science-news', method='POST', json=data
        ):
            return _unwrap(depot_science_views.api_add_science_news())


def test_int_title_does_not_crash():
    status, payload = _add_news(
        {'title': 123, 'category': 'geology', 'region': 'balkans'}
    )
    assert status == 200, payload
    assert payload.get('success') is True
    assert payload['news']['title'] == '123'


def test_null_summary_does_not_crash():
    status, payload = _add_news(
        {
            'title': 'Valid title',
            'summary': None,
            'category': 'geology',
            'region': 'balkans',
        }
    )
    assert status == 200, payload
    assert payload.get('success') is True
    assert payload['news']['summary'] == ''


def test_valid_string_news_still_works():
    status, payload = _add_news(
        {
            'title': 'Hello',
            'summary': 'World',
            'category': 'geology',
            'region': 'balkans',
        }
    )
    assert status == 200, payload
    assert payload['news']['title'] == 'Hello'
    assert payload['news']['summary'] == 'World'


# ---------------------------------------------------------------------------
# Finding: path-prefix check in api_serve_local_rruff_image uses startswith
# without a trailing separator, so a sibling dir like 'RRUFF_data_backup'
# would pass the prefix check.
# ---------------------------------------------------------------------------

def test_sibling_directory_is_rejected():
    sent = {}

    def fake_send(directory, filename):
        sent['directory'] = directory
        sent['filename'] = filename
        return 'OK'

    with mock.patch.object(
        mineral_science_views, 'send_from_directory', side_effect=fake_send
    ):
        with museum_app.app.test_request_context('/'):
            root = museum_app.app.root_path
            sibling_rel = os.path.relpath(
                os.path.join(root, 'RRUFF_data_backup', 'secret.png'),
                os.path.join(root, 'RRUFF_data'),
            )
            response = mineral_science_views.api_serve_local_rruff_image(sibling_rel)
    status, payload = _unwrap(response)
    assert status == 403, payload
    assert payload.get('success') is False
    assert 'directory' not in sent


def test_legitimate_image_is_served():
    with mock.patch.object(
        mineral_science_views, 'send_from_directory', return_value='OK'
    ) as send:
        with museum_app.app.test_request_context('/'):
            response = mineral_science_views.api_serve_local_rruff_image(
                'sub/image.png'
            )
    assert response == 'OK'
    send.assert_called_once()


# ---------------------------------------------------------------------------
# Finding: get_cif_data caches negative (None) results permanently.
# A transient failure must not be memoized; a later success must be returned.
# ---------------------------------------------------------------------------

def test_transient_failure_is_not_cached():
    db = crystal_structure_databases.CrystalStructureSearch()
    url = 'https://www.crystallography.net/cod/1000001.cif'

    fail_resp = mock.Mock(status_code=500, text='error')
    ok_resp = mock.Mock(status_code=200, text='data_test\n_cell_length_a 1.0\n')

    with mock.patch.object(db.session, 'get', side_effect=[fail_resp, ok_resp]):
        first = db.get_cif_data(url)
        second = db.get_cif_data(url)

    assert first is None
    assert second == 'data_test\n_cell_length_a 1.0\n'


def test_successful_result_is_cached():
    db = crystal_structure_databases.CrystalStructureSearch()
    url = 'https://www.crystallography.net/cod/2000002.cif'

    ok_resp = mock.Mock(status_code=200, text='data_ok\n_atom_x 0.0\n')

    with mock.patch.object(db.session, 'get', return_value=ok_resp) as getter:
        first = db.get_cif_data(url)
        second = db.get_cif_data(url)

    assert first == 'data_ok\n_atom_x 0.0\n'
    assert second == 'data_ok\n_atom_x 0.0\n'
    getter.assert_called_once()
