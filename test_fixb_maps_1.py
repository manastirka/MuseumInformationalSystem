"""Reproducing tests for maps-1 cluster medium-severity bugs."""

import json
import os
import threading

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-maps-1')

import pytest
from flask import Flask

import maps_profile_support
import maps_profile_views


@pytest.fixture(autouse=True)
def _force_json_profiles(monkeypatch):
    # These verify the JSON-fallback path (atomic file writes, ownership on
    # JSON-stored profiles). Pin them to JSON regardless of whether the live
    # digitized_profiles Postgres table exists; the PG path has its own tests.
    monkeypatch.setattr(maps_profile_views, '_profiles_pg', lambda: None)


@pytest.fixture
def app():
    application = Flask(__name__)
    application.secret_key = 'test-secret'
    return application


def _write_profiles(tmp_path, profiles):
    path = tmp_path / 'digitized_profiles.json'
    path.write_text(json.dumps(profiles), encoding='utf-8')
    return str(path)


def _patch_profiles(monkeypatch, profiles):
    monkeypatch.setattr(
        maps_profile_support, 'load_digitized_profiles', lambda *a, **k: profiles
    )


# Finding 1: interpolate_subsurface crashes on malformed boundary_points.
def test_interpolate_subsurface_malformed_boundary_points(tmp_path, monkeypatch):
    profiles = [
        {
            'id': 'sheet_AB',
            'endpoint_a': {'lat': 44.0, 'lon': 20.0},
            'endpoint_b': {'lat': 44.1, 'lon': 20.1},
            'image_bounds': {
                'distance_km': 10.0,
                'elevation_top_m': 1000,
                'elevation_bottom_m': -1000,
            },
            'layers': [
                {
                    'unit_code': 'K',
                    # Malformed: bare numbers instead of [dist, elev] pairs.
                    'boundary_points': [5, 7],
                }
            ],
            'faults': [],
        }
    ]
    _patch_profiles(monkeypatch, profiles)

    surface_points = [
        {'dist_km': 0.0, 'lat': 44.0, 'lon': 20.0, 'elevation': 500.0},
        {'dist_km': 5.0, 'lat': 44.05, 'lon': 20.05, 'elevation': 400.0},
    ]
    # Should not raise; malformed layer skipped gracefully.
    result = maps_profile_support.interpolate_subsurface(
        44.0, 20.0, 44.1, 20.1, surface_points, 10.0
    )
    assert result is not None
    assert 'columns' in result


# Finding 4: interpolate_subsurface guards only 'lat' but reads 'lon'.
def test_interpolate_subsurface_missing_lon(tmp_path, monkeypatch):
    profiles = [
        {
            'id': 'sheet_AB',
            'endpoint_a': {'lat': 44.0},  # missing 'lon'
            'endpoint_b': {'lat': 44.1, 'lon': 20.1},
            'image_bounds': {'distance_km': 10.0},
            'layers': [],
            'faults': [],
        }
    ]
    _patch_profiles(monkeypatch, profiles)

    surface_points = [
        {'dist_km': 0.0, 'lat': 44.0, 'lon': 20.0, 'elevation': 500.0},
    ]
    # Should not raise KeyError on endpoint_a['lon'].
    result = maps_profile_support.interpolate_subsurface(
        44.0, 20.0, 44.1, 20.1, surface_points, 10.0
    )
    # Profile is skipped (no usable endpoint), so no nearby -> None.
    assert result is None


# Finding 5: interpolate_subsurface uses hard profile['id'] when emitting faults.
def test_interpolate_subsurface_fault_missing_id(tmp_path, monkeypatch):
    profiles = [
        {
            # No 'id' key.
            'endpoint_a': {'lat': 44.0, 'lon': 20.0},
            'endpoint_b': {'lat': 44.1, 'lon': 20.1},
            'image_bounds': {'distance_km': 10.0},
            'layers': [],
            'faults': [
                {'distance_km': 2.0, 'points': [[0, -100], [5, -200]], 'type': 'normal'}
            ],
        }
    ]
    _patch_profiles(monkeypatch, profiles)

    surface_points = [
        {'dist_km': 0.0, 'lat': 44.0, 'lon': 20.0, 'elevation': 500.0},
    ]
    # Should not raise KeyError on profile['id'] in fault collection.
    result = maps_profile_support.interpolate_subsurface(
        44.0, 20.0, 44.1, 20.1, surface_points, 10.0
    )
    assert result is not None
    assert result['faults']
    assert result['faults'][0]['source_profile'] == ''


# Finding 1 (call-site): api_map_cross_profile should not 500 if subsurface fails.
def test_api_map_cross_profile_subsurface_failure_degrades(app, monkeypatch):
    def boom(*args, **kwargs):
        raise ValueError('subsurface blew up')

    with app.test_request_context(
        '/api/map/cross-profile?lat1=44&lon1=20&lat2=44.1&lon2=20.1&samples=2&subsurface=true'
    ):
        resp = maps_profile_views.api_map_cross_profile(
            app_root=os.path.dirname(__file__),
            haversine=maps_profile_support.haversine_km,
            batch_sample_elevations=lambda pts: [100.0] * len(pts),
            interpolate_subsurface=boom,
        )
    body = resp.get_json() if hasattr(resp, 'get_json') else resp[0].get_json()
    assert body['success'] is True
    assert 'subsurface' not in body['profile']


# Finding 2: list endpoint raw 500 on profile missing 'id'.
def test_api_digitized_profiles_list_missing_id(app, tmp_path):
    profiles = [
        {'sheet_folder': 'sheet1', 'layers': []},  # no 'id'
        {'id': 'good', 'sheet_folder': 'sheet2', 'layers': []},
    ]
    path = _write_profiles(tmp_path, profiles)
    with app.test_request_context('/api/map/digitized-profiles'):
        resp = maps_profile_views.api_digitized_profiles_list(profiles_path=path)
    body = resp.get_json()
    assert body['success'] is True
    ids = [entry['id'] for entry in body['data']]
    assert 'good' in ids


# Finding 2: get endpoint should not crash on entries missing 'id'.
def test_api_digitized_profile_get_missing_id(app, tmp_path):
    profiles = [
        {'sheet_folder': 'sheet1', 'layers': []},  # no 'id'
        {'id': 'good', 'sheet_folder': 'sheet2', 'layers': []},
    ]
    path = _write_profiles(tmp_path, profiles)
    with app.test_request_context('/api/map/digitized-profiles/good'):
        resp = maps_profile_views.api_digitized_profile_get('good', profiles_path=path)
    body = resp.get_json() if hasattr(resp, 'get_json') else resp[0].get_json()
    assert body['success'] is True
    assert body['data']['id'] == 'good'


# Finding 3: concurrent creates must not lose updates (atomic read-modify-write).
def test_concurrent_creates_no_lost_updates(app, tmp_path):
    path = str(tmp_path / 'digitized_profiles.json')

    def make_request(i):
        with app.test_request_context(
            '/api/map/digitized-profiles',
            method='POST',
            json={'id': f'profile_{i}', 'profile_id': f'P{i}', 'sheet_folder': 'sheet'},
        ):
            maps_profile_views.api_digitized_profile_create(profiles_path=path)

    threads = [threading.Thread(target=make_request, args=(i,)) for i in range(20)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    with open(path, encoding='utf-8') as handle:
        saved = json.load(handle)
    saved_ids = {entry['id'] for entry in saved}
    expected_ids = {f'profile_{i}' for i in range(20)}
    assert saved_ids == expected_ids, f"Lost updates: missing {expected_ids - saved_ids}"
