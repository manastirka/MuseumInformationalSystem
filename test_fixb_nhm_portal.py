"""Phase B regression tests for the nhm-portal cluster.

Covers three confirmed medium-severity findings:
1. update_datasets never refreshes modified datasets (dead existing_modified var).
2. Local search singleton serves stale data after a (re)download (cache not invalidated).
3. Unparsed integer query params crash the portal page and several API endpoints.
"""

import os
import json
import tempfile

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-nhm-portal')

import pytest

import nhm_dataset_downloader as dl
import nhm_portal_views as views


# ---------------------------------------------------------------------------
# Finding 1: update_datasets must re-download modified datasets.
# ---------------------------------------------------------------------------

class _FakeAPI:
    """Minimal stand-in for NHMDataPortalAPI used by update_datasets."""

    def __init__(self, datasets_by_name):
        # datasets_by_name: {name: full dataset dict (current upstream state)}
        self._datasets = datasets_by_name

    def get_all_datasets(self):
        return list(self._datasets.keys())

    def get_dataset(self, name):
        return self._datasets.get(name)


def _make_downloader(tmp_path, fake_api):
    d = dl.NHMDatasetDownloader(data_dir=str(tmp_path))
    d.api = fake_api
    return d


def test_update_datasets_refreshes_modified(tmp_path):
    # Existing local metadata: one dataset, with an OLD metadata_modified.
    existing_metadata = {
        'download_date': '2020-01-01T00:00:00',
        'total_datasets': 1,
        'source': 'Natural History Museum London Data Portal',
        'source_url': 'https://data.nhm.ac.uk',
        'datasets': [
            {'name': 'ds1', 'id': 'id1', 'title': 'Old title',
             'metadata_modified': '2020-01-01T00:00:00'},
        ],
    }
    metadata_file = os.path.join(str(tmp_path), 'datasets_metadata.json')
    with open(metadata_file, 'w', encoding='utf-8') as fh:
        json.dump(existing_metadata, fh)

    # Upstream now reports ds1 with a NEWER metadata_modified (and new title),
    # plus a brand new ds2.
    upstream = {
        'ds1': {'name': 'ds1', 'id': 'id1', 'title': 'New title',
                'metadata_modified': '2026-05-01T00:00:00'},
        'ds2': {'name': 'ds2', 'id': 'id2', 'title': 'Brand new',
                'metadata_modified': '2026-05-02T00:00:00'},
    }
    d = _make_downloader(tmp_path, _FakeAPI(upstream))

    result = d.update_datasets()

    # Read back what was persisted.
    with open(metadata_file, encoding='utf-8') as fh:
        persisted = json.load(fh)
    by_name = {ds['name']: ds for ds in persisted['datasets']}

    # ds1 must have been refreshed to the new upstream state (root cause:
    # existing_modified was built but never used to detect modifications).
    assert by_name['ds1']['title'] == 'New title'
    assert by_name['ds1']['metadata_modified'] == '2026-05-01T00:00:00'
    # ds2 (new) must be present.
    assert 'ds2' in by_name
    assert result['total_datasets'] == 2


def test_update_datasets_keeps_unmodified(tmp_path):
    # ds1 unchanged upstream -> must be kept as-is (no spurious churn).
    existing_metadata = {
        'download_date': '2020-01-01T00:00:00',
        'total_datasets': 1,
        'source': 'Natural History Museum London Data Portal',
        'source_url': 'https://data.nhm.ac.uk',
        'datasets': [
            {'name': 'ds1', 'id': 'id1', 'title': 'Same title',
             'metadata_modified': '2020-01-01T00:00:00'},
        ],
    }
    metadata_file = os.path.join(str(tmp_path), 'datasets_metadata.json')
    with open(metadata_file, 'w', encoding='utf-8') as fh:
        json.dump(existing_metadata, fh)

    upstream = {
        'ds1': {'name': 'ds1', 'id': 'id1', 'title': 'Same title',
                'metadata_modified': '2020-01-01T00:00:00'},
    }
    d = _make_downloader(tmp_path, _FakeAPI(upstream))

    result = d.update_datasets()

    with open(metadata_file, encoding='utf-8') as fh:
        persisted = json.load(fh)
    by_name = {ds['name']: ds for ds in persisted['datasets']}
    assert by_name['ds1']['title'] == 'Same title'
    assert result['total_datasets'] == 1


# ---------------------------------------------------------------------------
# Finding 2: download/update must invalidate the local-search singleton cache.
# ---------------------------------------------------------------------------

def test_singleton_cache_invalidated_after_update(tmp_path, monkeypatch):
    # Point the module singletons at a clean temp dir.
    dl._downloader = None
    dl._local_search = None

    metadata_file = os.path.join(str(tmp_path), 'datasets_metadata.json')
    index_file = os.path.join(str(tmp_path), 'search_index.json')

    # Seed initial on-disk metadata + index.
    initial_meta = {
        'download_date': '2020-01-01T00:00:00',
        'total_datasets': 1,
        'datasets': [
            {'name': 'ds1', 'id': 'id1', 'title': 'Old title',
             'metadata_modified': '2020-01-01T00:00:00'},
        ],
    }
    initial_index = {
        'created': '2020-01-01T00:00:00',
        'total_datasets': 1,
        'datasets': [{'name': 'ds1', 'title': 'Old title', 'title_lower': 'old title',
                      'notes_lower': '', 'author_lower': '', 'tags': []}],
        'tags': {}, 'authors': {}, 'formats': {}, 'keywords': {},
    }
    with open(metadata_file, 'w', encoding='utf-8') as fh:
        json.dump(initial_meta, fh)
    with open(index_file, 'w', encoding='utf-8') as fh:
        json.dump(initial_index, fh)

    search = dl.NHMLocalSearch(data_dir=str(tmp_path))
    dl._local_search = search

    # Prime the caches (read stale data into the process).
    assert search.get_dataset('ds1')['title'] == 'Old title'

    # Build a downloader that shares the temp dir and a fake API that now
    # reports a modified ds1.
    upstream = {
        'ds1': {'name': 'ds1', 'id': 'id1', 'title': 'New title',
                'metadata_modified': '2026-05-01T00:00:00'},
    }
    d = dl.NHMDatasetDownloader(data_dir=str(tmp_path))
    d.api = _FakeAPI(upstream)
    dl._downloader = d

    d.update_datasets()

    # After the update, the shared singleton must NOT keep serving the stale
    # cached title.
    assert dl.get_nhm_local_search().get_dataset('ds1')['title'] == 'New title'

    dl._downloader = None
    dl._local_search = None


# ---------------------------------------------------------------------------
# Finding 3: non-numeric integer query params must not crash (no 500/ValueError).
# ---------------------------------------------------------------------------

def _make_flask_app():
    os.makedirs(os.environ['SESSION_FILE_DIR'], exist_ok=True)
    from flask import Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    return app


def test_api_nhm_local_search_bad_int_no_crash(monkeypatch):
    app = _make_flask_app()

    class _FakeSearch:
        def is_available(self):
            return True

        def search(self, query, filters=None, limit=50, offset=0):
            return {'success': True, 'results': [], 'total': 0,
                    'limit': limit, 'offset': offset}

    monkeypatch.setattr('nhm_dataset_downloader.get_nhm_local_search',
                        lambda: _FakeSearch())

    with app.test_request_context('/api/nhm/local/search?limit=abc&offset=xyz'):
        resp = views.api_nhm_local_search()
        # tuple => error response; bare Response => success. Must not raise.
        if isinstance(resp, tuple):
            body, status = resp
            assert status != 500
        else:
            data = json.loads(resp.get_data(as_text=True))
            assert data['success'] is True


def test_api_nhm_search_bad_int_no_crash(monkeypatch):
    app = _make_flask_app()

    class _FakeNHM:
        def get_status(self):
            return {'connected': True}

        def search_datasets(self, query='', rows=25, start=0):
            return {'count': 0, 'results': []}

    monkeypatch.setattr('nhm_data_portal_api.get_nhm_api', lambda: _FakeNHM())

    with app.test_request_context('/api/nhm/search?rows=abc&start=xyz&q=fish'):
        resp = views.api_nhm_search()
        if isinstance(resp, tuple):
            body, status = resp
            assert status != 500


def test_api_nhm_data_search_local_bad_int_no_crash(monkeypatch):
    app = _make_flask_app()
    with app.test_request_context('/api/nhm/data/search/local?q=pirit&limit=abc'):
        resp = views.api_nhm_data_search_local()
        if isinstance(resp, tuple):
            body, status = resp
            assert status != 500
        else:
            data = json.loads(resp.get_data(as_text=True))
            assert data['success'] is True


def test_api_nhm_data_search_nhm_bad_int_no_crash(monkeypatch):
    app = _make_flask_app()

    class _FakeNHM:
        def get_status(self):
            return {'connected': True}

        def datastore_search(self, resource_id, query='', limit=50, offset=0):
            return {'total': 0, 'records': []}

    monkeypatch.setattr('nhm_data_portal_api.get_nhm_api', lambda: _FakeNHM())

    with app.test_request_context('/api/nhm/data/search/nhm?q=pirit&limit=abc&offset=xyz'):
        resp = views.api_nhm_data_search_nhm()
        if isinstance(resp, tuple):
            body, status = resp
            assert status != 500
        else:
            data = json.loads(resp.get_data(as_text=True))
            assert data['success'] is True


def test_render_portal_bad_page_no_crash(monkeypatch):
    app = _make_flask_app()

    class _FakeSearch:
        def is_available(self):
            return False

        def get_statistics(self):
            return {}

    class _FakeNHM:
        DEPARTMENTS = {}

        def get_status(self):
            return {'connected': False, 'total_datasets': 0}

    monkeypatch.setattr('nhm_dataset_downloader.get_nhm_local_search',
                        lambda: _FakeSearch())
    monkeypatch.setattr('nhm_data_portal_api.get_nhm_api', lambda: _FakeNHM())
    monkeypatch.setattr('flask.render_template',
                        lambda *a, **k: 'OK')
    monkeypatch.setattr('nhm_portal_views.render_template',
                        lambda *a, **k: 'OK')

    with app.test_request_context('/admin/nhm_data_portal?page=abc'):
        # Must not raise ValueError -> 500.
        out = views.render_nhm_data_portal()
        assert out == 'OK'


if __name__ == '__main__':
    raise SystemExit(pytest.main([__file__, '-q']))
