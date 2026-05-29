"""Phase C maps-2 hardening tests for maps_geo_zone_views.api_geo_zone_process."""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-maps-2')

import json
import sys
import types

from flask import Flask

# geo_zone_processor pulls in heavy optional deps (sklearn/scipy) that may not be
# installed in the test environment. The view does `import geo_zone_processor`
# at its first line, so stub it before importing the view under test.
if 'geo_zone_processor' not in sys.modules:
    _stub = types.ModuleType('geo_zone_processor')
    _stub.process_sheet = lambda *a, **k: {'status': 'ok'}
    sys.modules['geo_zone_processor'] = _stub

import geo_zone_processor  # noqa: E402  (stub or real)

import maps_geo_zone_views

_test_app = Flask(__name__)


def _split(rv):
    # Views return either a Response (implicit 200) or a (Response, status) tuple.
    if isinstance(rv, tuple):
        return rv[0], rv[1]
    return rv, rv.status_code


def _call_process(data, content_type='application/json'):
    with _test_app.test_request_context(
        '/api/map/geo-zones/process',
        method='POST',
        data=data,
        content_type=content_type,
    ):
        return _split(maps_geo_zone_views.api_geo_zone_process(app_root='/tmp/museum-test-c-maps-2'))


def test_json_array_body_returns_clean_400_not_crash():
    # A JSON array (not an object) must not raise AttributeError; it should
    # fall through to the clean 400 'folder required' response.
    resp, status = _call_process(json.dumps(['not', 'an', 'object']))
    assert status == 400
    payload = resp.get_json()
    assert payload['success'] is False
    assert payload['message'] == 'Потребан је назив фасцикле (folder)'


def test_json_string_body_returns_clean_400():
    resp, status = _call_process(json.dumps("just-a-string"))
    assert status == 400
    assert resp.get_json()['success'] is False


def test_json_null_body_returns_clean_400():
    resp, status = _call_process(json.dumps(None))
    assert status == 400
    assert resp.get_json()['success'] is False


def test_valid_json_object_still_processes(monkeypatch):
    import geo_zone_processor

    captured = {}

    def fake_process_sheet(folder, sheet_data=None, force=False):
        captured['folder'] = folder
        captured['force'] = force
        return {'status': 'ok'}

    monkeypatch.setattr(geo_zone_processor, 'process_sheet', fake_process_sheet)
    monkeypatch.setattr(maps_geo_zone_views, '_load_geological_sheets', lambda app_root: [])

    resp, status = _call_process(json.dumps({'folder': 'sheet1', 'force': True}))
    assert status == 200
    assert resp.get_json()['success'] is True
    assert captured == {'folder': 'sheet1', 'force': True}


def test_form_body_still_processes(monkeypatch):
    import geo_zone_processor

    captured = {}

    def fake_process_sheet(folder, sheet_data=None, force=False):
        captured['folder'] = folder
        captured['force'] = force
        return {'status': 'exists'}

    monkeypatch.setattr(geo_zone_processor, 'process_sheet', fake_process_sheet)
    monkeypatch.setattr(maps_geo_zone_views, '_load_geological_sheets', lambda app_root: [])

    with _test_app.test_request_context(
        '/api/map/geo-zones/process',
        method='POST',
        data={'folder': 'sheetX', 'force': 'true'},
    ):
        resp, status = _split(
            maps_geo_zone_views.api_geo_zone_process(app_root='/tmp/museum-test-c-maps-2')
        )

    assert status == 200
    assert resp.get_json()['success'] is True
    assert captured == {'folder': 'sheetX', 'force': True}
