"""Phase C hardening tests for the nhm-portal cluster.

Covers three confirmed LOW-severity findings:
1. Reverse mineral translation map drops base synonyms (duplicate target values)
   and the 'fosilI' key has a stray uppercase I so 'fosil'/'fosili' never match.
2. Minerals lacking both id and inventarni_broj are silently deduplicated away.
3. Negative limit/offset query params produce wrong slicing instead of being
   clamped to a sane floor.
"""

import os
import json

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-nhm-portal')

import pytest

import nhm_portal_views as views


def _make_flask_app():
    os.makedirs(os.environ['SESSION_FILE_DIR'], exist_ok=True)
    from flask import Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    return app


# ---------------------------------------------------------------------------
# Finding 1: reverse translation map + 'fosilI' typo.
# ---------------------------------------------------------------------------

def test_reverse_map_keeps_base_serbian_forms():
    rev = views._MINERAL_TRANSLATIONS_REVERSE
    # English -> Serbian back-translation must yield the base Serbian form,
    # not the plural alias that happened to be defined later in the map.
    assert rev['magnetite'] == 'magnetit'
    assert rev['agate'] == 'ahat'


def test_fossil_serbian_to_english_translation_works():
    # Forward Serbian -> English translation of 'fosil' must succeed; the key
    # had a stray uppercase I ('fosilI') that _translate_words could never hit.
    translated, original = views._translate_words('fosil', views._MINERAL_TRANSLATIONS)
    assert translated == 'fossil'
    assert original == 'fosil'


# ---------------------------------------------------------------------------
# Finding 2: distinct minerals without id/inventarni_broj must not be dropped.
# ---------------------------------------------------------------------------

def test_minerals_without_key_are_not_deduplicated(monkeypatch):
    app = _make_flask_app()

    class _FakeMineralDB:
        available = True

        def search_minerals(self, query):
            # Two distinct specimens, neither having id nor inventarni_broj.
            return {
                'minerals': [
                    {'naziv': 'Specimen A', 'lokalitet': 'Loc A'},
                    {'naziv': 'Specimen B', 'lokalitet': 'Loc B'},
                ]
            }

    import sys
    import types

    fake_module = types.ModuleType('mineral_database_pg')
    fake_module.MineralDatabase = _FakeMineralDB
    monkeypatch.setitem(sys.modules, 'mineral_database_pg', fake_module)

    with app.test_request_context('/api/nhm/data/search/local?q=test&type=minerals'):
        resp = views.api_nhm_data_search_local()
        data = json.loads(resp.get_data(as_text=True))
        assert data['success'] is True
        names = sorted(r['naziv'] for r in data['results'])
        assert names == ['Specimen A', 'Specimen B']
        assert data['total'] == 2


# ---------------------------------------------------------------------------
# Finding 3: negative limit/offset must be clamped, not slice from the tail.
# ---------------------------------------------------------------------------

def test_data_search_local_negative_limit_does_not_truncate_tail(monkeypatch):
    app = _make_flask_app()

    class _FakeMineralDB:
        available = True

        def search_minerals(self, query):
            return {
                'minerals': [
                    {'id': i, 'naziv': 'M%d' % i} for i in range(10)
                ]
            }

    import sys
    import types

    fake_module = types.ModuleType('mineral_database_pg')
    fake_module.MineralDatabase = _FakeMineralDB
    monkeypatch.setitem(sys.modules, 'mineral_database_pg', fake_module)

    with app.test_request_context(
        '/api/nhm/data/search/local?q=test&type=minerals&limit=-5'
    ):
        resp = views.api_nhm_data_search_local()
        data = json.loads(resp.get_data(as_text=True))
        assert data['success'] is True
        # A negative limit must not silently drop the last 5 records via
        # results[:-5]. Clamped to a floor of 1, we expect a single record.
        assert len(data['results']) == 1


def test_local_search_negative_params_clamped(monkeypatch):
    app = _make_flask_app()
    captured = {}

    class _FakeSearch:
        def is_available(self):
            return True

        def search(self, query, filters=None, limit=50, offset=0):
            captured['limit'] = limit
            captured['offset'] = offset
            return {'success': True, 'results': [], 'total': 0}

    monkeypatch.setattr('nhm_dataset_downloader.get_nhm_local_search',
                        lambda: _FakeSearch())

    with app.test_request_context(
        '/api/nhm/local/search?limit=-5&offset=-3'
    ):
        views.api_nhm_local_search()
        assert captured['limit'] >= 1
        assert captured['offset'] >= 0


def test_data_search_nhm_negative_limit_clamped(monkeypatch):
    app = _make_flask_app()
    captured = {}

    class _FakeNHM:
        def get_status(self):
            return {'connected': True}

        def datastore_search(self, resource_id, query='', limit=50, offset=0):
            captured['limit'] = limit
            captured['offset'] = offset
            return {'total': 0, 'records': []}

    monkeypatch.setattr('nhm_data_portal_api.get_nhm_api', lambda: _FakeNHM())

    with app.test_request_context(
        '/api/nhm/data/search/nhm?q=pirit&limit=-5&offset=-3'
    ):
        views.api_nhm_data_search_nhm()
        assert captured['limit'] >= 1
        assert captured['offset'] >= 0


if __name__ == '__main__':
    raise SystemExit(pytest.main([__file__, '-q']))
