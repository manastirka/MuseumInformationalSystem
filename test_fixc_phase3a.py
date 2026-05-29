import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-phase3a')
os.environ.setdefault('DATABASE_URL', 'postgresql://test:test@localhost:5432/test')

from unittest.mock import MagicMock, patch

import phase3a_databases


class _FakeCursor:
    """Minimal cursor that replays a queue of (description, rows) results."""

    def __init__(self, results):
        self._results = list(results)
        self.description = None
        self._rows = []
        self.closed = False

    def execute(self, query, params=None):
        description, rows = self._results.pop(0)
        self.description = description
        self._rows = list(rows)

    def fetchall(self):
        return list(self._rows)

    def fetchone(self):
        return self._rows[0] if self._rows else None

    def close(self):
        self.closed = True


def _make_conn(results):
    cur = _FakeCursor(results)
    conn = MagicMock()
    conn.cursor.return_value = cur
    return conn, cur


def _desc(*names):
    return [(name,) for name in names]


def test_heritage_missing_renamed_column_does_not_drop_rows():
    """A schema-drifted heritage row (missing current_location) must not be
    silently swallowed into an empty result via KeyError."""
    # SELECT column list missing 'current_location' (renamed/dropped column).
    columns = _desc('id', 'item_name', 'heritage_type', 'significance_level')
    rows = [(1, 'Икона', 'сликарство', 'изузетно')]

    results = [
        (columns, rows),                 # main heritage_items SELECT
        (_desc('heritage_type'), []),    # DISTINCT heritage_type
        (_desc('category'), []),         # DISTINCT category
        (_desc('subcategory'), []),      # DISTINCT subcategory
        (_desc('significance_level'), []),  # DISTINCT significance_level
        (_desc('current_location'), []), # DISTINCT current_location
        (_desc('condition'), []),        # DISTINCT condition
        (_desc('protection_status'), []),  # DISTINCT protection_status
        (_desc('total', 'exceptional', 'great'), [(1, 0, 0)]),  # statistics
    ]
    conn, cur = _make_conn(results)

    with patch.object(phase3a_databases, 'get_db_connection', return_value=conn):
        result = phase3a_databases.get_cultural_heritage_database()

    # The row must survive (not be zeroed out by a swallowed KeyError).
    assert len(result['heritage_items']) == 1
    item = result['heritage_items'][0]
    assert item['name'] == 'Икона'
    assert item['location'] is None  # absent column maps to None, not a crash


def test_meteorite_missing_renamed_column_does_not_drop_rows():
    """A schema-drifted meteorite row (missing storage_location) must not be
    silently swallowed into an empty result via KeyError."""
    columns = _desc(
        'id', 'specimen_name', 'meteorite_class', 'meteorite_type',
        'fall_location', 'fall_country', 'collector', 'acquisition_method'
    )
    rows = [(1, 'Сошанка', 'H4', 'chondrite', 'Сошанка', 'Србија', 'Петровић', 'поклон')]

    results = [
        (columns, rows),  # main meteorite_specimens SELECT
        (_desc('total', 'classes', 'total_mass_grams', 'witnessed_falls',
               'finds', 'serbian', 'foreign'),
         [(1, 1, 0, 0, 1, 1, 0)]),  # statistics
    ]
    conn, cur = _make_conn(results)

    with patch.object(phase3a_databases, 'get_db_connection', return_value=conn):
        result = phase3a_databases.get_meteorite_collection_database()

    assert len(result['specimens']) == 1
    specimen = result['specimens'][0]
    assert specimen['meteorite_name'] == 'Сошанка'
    assert specimen['storage'] is None  # absent column maps to None, not a crash
