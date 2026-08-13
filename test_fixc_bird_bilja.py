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
# Finding 2 (revidirano u krugu 4, stavka 8): delimičan uvoz NE postoji.
# Raniji ugovor (bad row se preskače, ostatak se upiše) je ukinut kao kršenje
# projektnog pravila 3 — sada red koji ne može da se parsira ulazi u listu
# grešaka (parse_job), a neuspeh upisa znači rollback + nenulti exit (main).
# ---------------------------------------------------------------------------

def test_parse_job_prikuplja_greske_umesto_preskakanja(tmp_path):
    rows = [('a', 'x'), ('LOSE',), ('b', 'y')]

    def mapper(row, src):
        if row == ('LOSE',):
            raise ValueError('neparsiv red')
        return row + (src,)

    job = {
        'table': 'tbl',
        'file': 'dummy.xlsx',
        'sheet': 'Sheet1',
        'kind': 'xlsx',
        'mapper': mapper,
    }
    with mock.patch.object(ibc, 'BILJA_DIR', tmp_path):
        (tmp_path / 'dummy.xlsx').write_text('x')
        with mock.patch.object(ibc, '_iter_xlsx_rows', lambda p, s: iter(rows)):
            parsed, empty, errors = ibc.parse_job(job)

    assert len(parsed) == 2
    assert empty == 0
    assert len(errors) == 1 and 'neparsiv red' in errors[0]


class _ScriptedCursor:
    """Odgovara na plan-upite; executemany puca kao da je baza odbila red."""

    def __init__(self, conn):
        self.conn = conn
        self._pending = None
        self.executemany_called = False

    def execute(self, query, params=None):
        q = ' '.join(query.split())
        if 'current_database' in q:
            self._pending = ('testdb',)
        elif 'to_regclass' in q:
            self._pending = (True,)
        elif 'count(*)' in q:
            self._pending = (0,)
        else:
            self._pending = None

    def executemany(self, stmt, rows):
        self.executemany_called = True
        raise RuntimeError('DB je odbila red')

    def fetchone(self):
        return self._pending

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class _ScriptedConn:
    def __init__(self):
        self.cursor_obj = _ScriptedCursor(self)
        self.rolled_back = False
        self.committed = False

    def cursor(self):
        return self.cursor_obj

    def rollback(self):
        self.rolled_back = True

    def commit(self):
        self.committed = True

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _fake_job_env(tmp_path):
    job = {
        'table': 'tbl',
        'file': 'dummy.xlsx',
        'sheet': 'Sheet1',
        'kind': 'xlsx',
        'mapper': lambda row, src: row + (src,),
    }
    (tmp_path / 'dummy.xlsx').write_text('x')
    return job


def test_main_neuspeh_upisa_znaci_rollback_i_nenulti_exit(tmp_path, monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'postgresql://x@localhost/testdb')
    conn = _ScriptedConn()
    job = _fake_job_env(tmp_path)
    with mock.patch.object(ibc, 'BILJA_DIR', tmp_path), \
            mock.patch.object(ibc, 'JOBS', [job]), \
            mock.patch.dict(ibc.INSERT_STATEMENTS, {'tbl': 'INSERT ...'}, clear=False), \
            mock.patch.object(ibc, '_iter_xlsx_rows', lambda p, s: iter([('a', 'x')])), \
            mock.patch.object(ibc.psycopg, 'connect', lambda url: conn):
        code = ibc.main(['--execute', '--database', 'testdb'])

    assert code != 0, 'delimicni/neuspeli uvoz ne sme da vrati uspeh'
    assert conn.rolled_back, 'neuspeh upisa mora da izazove rollback'
    assert not conn.committed


def test_main_bez_execute_je_dry_run_bez_upisa(tmp_path, monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'postgresql://x@localhost/testdb')
    conn = _ScriptedConn()
    job = _fake_job_env(tmp_path)
    with mock.patch.object(ibc, 'BILJA_DIR', tmp_path), \
            mock.patch.object(ibc, 'JOBS', [job]), \
            mock.patch.dict(ibc.INSERT_STATEMENTS, {'tbl': 'INSERT ...'}, clear=False), \
            mock.patch.object(ibc, '_iter_xlsx_rows', lambda p, s: iter([('a', 'x')])), \
            mock.patch.object(ibc.psycopg, 'connect', lambda url: conn):
        code = ibc.main([])

    assert code == 0
    assert not conn.cursor_obj.executemany_called, 'dry-run ne sme da upisuje'
    assert not conn.committed


def test_main_execute_bez_database_se_odbija(tmp_path, monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'postgresql://x@localhost/testdb')
    conn = _ScriptedConn()
    job = _fake_job_env(tmp_path)
    with mock.patch.object(ibc, 'BILJA_DIR', tmp_path), \
            mock.patch.object(ibc, 'JOBS', [job]), \
            mock.patch.dict(ibc.INSERT_STATEMENTS, {'tbl': 'INSERT ...'}, clear=False), \
            mock.patch.object(ibc, '_iter_xlsx_rows', lambda p, s: iter([('a', 'x')])), \
            mock.patch.object(ibc.psycopg, 'connect', lambda url: conn):
        code = ibc.main(['--execute'])

    assert code != 0
    assert not conn.cursor_obj.executemany_called
