import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-maps-3')

import json
import tempfile
import importlib
from unittest import mock

import pytest


# ---------------------------------------------------------------------------
# Finding 1: DB connection leaked on exception path in init_feature_links_table
# ---------------------------------------------------------------------------

class _FakeConn:
    """Fake managed connection that records close() and raises on execute."""

    def __init__(self, raise_on_execute=False, raise_on_commit=False):
        self.closed = False
        self.committed = False
        self._raise_on_execute = raise_on_execute
        self._raise_on_commit = raise_on_commit

    def execute(self, *args, **kwargs):
        if self._raise_on_execute:
            raise RuntimeError("DDL boom")
        return self

    def commit(self):
        if self._raise_on_commit:
            raise RuntimeError("commit boom")
        self.committed = True

    def close(self):
        self.closed = True


def test_init_feature_links_table_closes_connection_on_execute_error():
    import map_feature_paper_enricher as enricher

    fake = _FakeConn(raise_on_execute=True)
    with mock.patch.object(enricher.db, 'get_connection', return_value=fake):
        with pytest.raises(RuntimeError):
            enricher.init_feature_links_table()

    assert fake.closed, "connection must be returned to the pool (close) even on DDL error"


def test_init_feature_links_table_closes_connection_on_commit_error():
    import map_feature_paper_enricher as enricher

    fake = _FakeConn(raise_on_commit=True)
    with mock.patch.object(enricher.db, 'get_connection', return_value=fake):
        with pytest.raises(RuntimeError):
            enricher.init_feature_links_table()

    assert fake.closed, "connection must be closed even when commit fails"


def test_init_feature_links_table_closes_connection_on_success():
    import map_feature_paper_enricher as enricher

    fake = _FakeConn()
    with mock.patch.object(enricher.db, 'get_connection', return_value=fake):
        enricher.init_feature_links_table()

    assert fake.committed
    assert fake.closed


# ---------------------------------------------------------------------------
# Finding 2: _load_geocache rebinds module global instead of mutating it,
# breaking callers that did `from locality_data import _geocache`.
# ---------------------------------------------------------------------------

def test_load_geocache_mutates_shared_reference():
    import locality_data

    # Simulate an external importer that captured the reference at import time
    # (as geocode_all_localities.py does): `from locality_data import _geocache`.
    imported_ref = locality_data._geocache

    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as fh:
        json.dump({'bor, srbija': {'lat': 44.1, 'lon': 22.1}}, fh)
        cache_path = fh.name

    try:
        with mock.patch.object(locality_data, 'CACHE_FILE', cache_path):
            locality_data._load_geocache()

        # The externally-captured reference must see the loaded entries,
        # i.e. _load_geocache mutated the existing dict rather than rebinding.
        assert 'bor, srbija' in imported_ref, (
            "externally imported _geocache reference is stale; "
            "_load_geocache rebound the global instead of mutating it"
        )
        assert imported_ref is locality_data._geocache
    finally:
        os.unlink(cache_path)
