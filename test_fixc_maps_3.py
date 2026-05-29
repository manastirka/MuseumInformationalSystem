import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-maps-3')

import json

import pytest

import locality_data
from runtime_lock_utils import load_json_file, write_json_file


@pytest.fixture
def temp_cache(tmp_path, monkeypatch):
    """Point the module at an isolated cache file and reset in-memory state."""
    cache_file = tmp_path / 'locality_geocache.json'
    monkeypatch.setattr(locality_data, 'CACHE_FILE', str(cache_file))
    locality_data._geocache.clear()
    if hasattr(locality_data, '_geocache_loaded'):
        monkeypatch.setattr(locality_data, '_geocache_loaded', False)
    return cache_file


def test_save_geocache_merges_concurrent_on_disk_entries(temp_cache):
    """Finding 1: a concurrent process's on-disk entries must not be clobbered."""
    # Another process wrote an entry to disk after this worker last loaded.
    write_json_file(str(temp_cache), {'other place': {'lat': 1.0, 'lon': 2.0}})

    # This worker has its own freshly-derived entry in memory only.
    locality_data._geocache['my place'] = {'lat': 3.0, 'lon': 4.0}
    locality_data._save_geocache()

    on_disk = load_json_file(str(temp_cache), default={})
    assert 'other place' in on_disk, "concurrent on-disk entry was clobbered"
    assert 'my place' in on_disk
    assert on_disk['other place'] == {'lat': 1.0, 'lon': 2.0}
    assert on_disk['my place'] == {'lat': 3.0, 'lon': 4.0}


def test_save_geocache_keeps_memory_in_sync_with_merge(temp_cache):
    """After save, in-memory cache reflects the merged on-disk state."""
    write_json_file(str(temp_cache), {'disk only': {'lat': 5.0, 'lon': 6.0}})
    locality_data._geocache['mem only'] = {'lat': 7.0, 'lon': 8.0}
    locality_data._save_geocache()
    assert 'disk only' in locality_data._geocache
    assert 'mem only' in locality_data._geocache


def test_empty_geocache_loads_at_most_once(temp_cache, monkeypatch):
    """Finding 2: an empty cache file must not trigger a reload on every call."""
    # No cache file on disk -> load yields an empty dict every time.
    assert not temp_cache.exists()

    calls = {'n': 0}
    real_load = locality_data._load_geocache

    def counting_load():
        calls['n'] += 1
        return real_load()

    monkeypatch.setattr(locality_data, '_load_geocache', counting_load)

    # Mock network so geocode_locality does not hit Nominatim.
    monkeypatch.setattr(locality_data, 'fetch_url', lambda url, timeout=10: None)
    monkeypatch.setattr(locality_data.time, 'sleep', lambda *a, **k: None)

    # First call loads once; subsequent calls must not reload from the empty file.
    locality_data.get_locality_data_local_only('Somewhere Unknown')
    locality_data.get_locality_data_local_only('Another Unknown')
    locality_data.get_locality_data_local_only('Third Unknown')

    assert calls['n'] == 1, f"_load_geocache ran {calls['n']} times on an empty cache"
