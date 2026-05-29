"""Behavior tests for LOW-severity hardening fixes (cluster: bird-bilja).

Covers:
  1. bird_ringing_database._pg_get_all_records clamps user-controlled
     page/per_page so it never produces a negative OFFSET or LIMIT -1.
  2. import_bilja_collections.run_job isolates a failing batch (row-by-row
     fallback via savepoint) so one bad row no longer aborts the whole import.
"""

import os
from contextlib import contextmanager
from unittest import mock

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-bird-bilja')

import bird_ringing_database as brd
import import_bilja_collections as ibc


# ---------------------------------------------------------------------------
# Fake psycopg-style cursor/connection for capturing parameters
# ---------------------------------------------------------------------------

class _FakeCursor:
    def __init__(self, total_count=0):
        self.executed = []  # list of (query, params)
        self._total = total_count

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchall(self):
        return []

    def fetchone(self):
        return {'total': self._total}

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class _FakeConn:
    def __init__(self, cursor):
        self._cursor = cursor

    def cursor(self):
        return self._cursor

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


# ---------------------------------------------------------------------------
# Finding 1: page/per_page clamping in _pg_get_all_records
# ---------------------------------------------------------------------------

def _run_get_all_records(page, per_page):
    cur = _FakeCursor(total_count=0)
    conn = _FakeConn(cur)

    @contextmanager
    def fake_connect():
        yield conn

    with mock.patch.object(brd, '_pg_connect', fake_connect):
        brd._pg_get_all_records(page=page, per_page=per_page)
    # First execute is the paginated SELECT; its trailing params are
    # filter_params + [per_page, offset].
    select_params = cur.executed[0][1]
    used_per_page, used_offset = select_params[-2], select_params[-1]
    return used_per_page, used_offset


def test_page_zero_does_not_produce_negative_offset():
    per_page, offset = _run_get_all_records(page=0, per_page=50)
    assert offset >= 0, f'OFFSET must not be negative, got {offset}'
    assert per_page >= 1


def test_negative_page_clamped():
    per_page, offset = _run_get_all_records(page=-5, per_page=50)
    assert offset >= 0
    assert per_page >= 1


def test_negative_per_page_does_not_produce_negative_limit():
    per_page, offset = _run_get_all_records(page=1, per_page=-1)
    assert per_page >= 1, f'LIMIT must be >= 1, got {per_page}'
    assert offset >= 0


def test_valid_pagination_preserved():
    per_page, offset = _run_get_all_records(page=3, per_page=25)
    assert per_page == 25
    assert offset == 50


# ---------------------------------------------------------------------------
# Finding 2: run_job isolates a failing batch instead of aborting the import
# ---------------------------------------------------------------------------

class _BatchFailingCursor:
    """executemany rejects any batch containing the poison value; per-row
    execute rejects only the poison row. Mimics psycopg savepoint behavior:
    a failed transaction block does not persist its rows."""

    POISON = 'POISON'

    def __init__(self):
        self.connection = self
        self.rows = []  # successfully persisted rows
        self._txn_rows = None

    # connection.transaction() -> context manager (savepoint)
    @contextmanager
    def transaction(self):
        self._txn_rows = []
        try:
            yield self
        except Exception:
            # rollback: discard rows staged in this block
            self._txn_rows = None
            raise
        else:
            self.rows.extend(self._txn_rows)
            self._txn_rows = None

    def executemany(self, stmt, batch):
        for params in batch:
            if self.POISON in params:
                raise RuntimeError('value rejected by DB')
            self._txn_rows.append(params)

    def execute(self, stmt, params):
        if self.POISON in params:
            raise RuntimeError('value rejected by DB')
        self._txn_rows.append(params)


def test_flush_batch_skips_only_bad_row():
    cur = _BatchFailingCursor()
    batch = [
        ('a',), ('b',), (_BatchFailingCursor.POISON,), ('c',),
    ]
    inserted, skipped = ibc._flush_batch(cur, 'INSERT ...', batch, 'tbl')

    assert inserted == 3, f'expected 3 good rows persisted, got {inserted}'
    assert skipped == 1, f'expected 1 poison row skipped, got {skipped}'
    assert ('a',) in cur.rows
    assert ('b',) in cur.rows
    assert ('c',) in cur.rows
    assert (_BatchFailingCursor.POISON,) not in cur.rows


def test_flush_batch_clean_batch_uses_bulk_path():
    cur = _BatchFailingCursor()
    batch = [('a',), ('b',), ('c',)]
    inserted, skipped = ibc._flush_batch(cur, 'INSERT ...', batch, 'tbl')
    assert inserted == 3
    assert skipped == 0
    assert len(cur.rows) == 3


def test_run_job_does_not_abort_on_bad_row(tmp_path):
    cur = _BatchFailingCursor()
    rows = [('a',), (_BatchFailingCursor.POISON,), ('b',)]

    job = {
        'table': 'tbl',
        'file': 'dummy.xlsx',
        'sheet': 'Sheet1',
        'kind': 'xlsx',
        'mapper': lambda row, src: row,
    }

    # avoid real file/sheet access
    with mock.patch.object(ibc, 'BILJA_DIR', tmp_path):
        (tmp_path / 'dummy.xlsx').write_text('x')
        with mock.patch.dict(ibc.INSERT_STATEMENTS, {'tbl': 'INSERT ...'}, clear=False), \
                mock.patch.object(ibc, '_iter_xlsx_rows', lambda p, s: iter(rows)):
            inserted, skipped = ibc.run_job(cur, job)

    assert inserted == 2, f'good rows should persist, got inserted={inserted}'
    assert skipped == 1, f'only the poison row should be skipped, got skipped={skipped}'
    assert (_BatchFailingCursor.POISON,) not in cur.rows
