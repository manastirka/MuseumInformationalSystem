import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-rruff-db')

import sqlite3
from unittest import mock

import online_mineral_data
import rruff_database


# Finding 1: Wikipedia <ref>...</ref> stripping must remove the citation body.
def test_clean_wiki_markup_strips_reference_body():
    text = 'Quartz<ref name="src">Smith 2001, citation body</ref> is common.'
    cleaned = online_mineral_data.clean_wiki_markup(text)
    assert 'citation body' not in cleaned
    assert 'Smith 2001' not in cleaned
    assert 'Quartz' in cleaned
    assert 'is common' in cleaned


def test_clean_wiki_markup_strips_self_closing_reference():
    text = 'Albite<ref name="x" /> mineral.'
    cleaned = online_mineral_data.clean_wiki_markup(text)
    assert 'Albite' in cleaned
    assert 'mineral' in cleaned
    assert '<ref' not in cleaned


# Finding 4: format_online_data_for_display must never return None.
def test_format_online_data_for_display_empty_returns_dict():
    result = online_mineral_data.format_online_data_for_display({})
    assert result == {}
    assert result is not None
    # Safe to dereference like a dict.
    assert result.get('name', 'fallback') == 'fallback'


def test_format_online_data_for_display_none_returns_dict():
    result = online_mineral_data.format_online_data_for_display(None)
    assert result == {}


# Findings 2 & 3 use an in-memory SQLite DB populated with the expected schema.
def _make_db():
    conn = sqlite3.connect(':memory:')
    conn.execute(
        """
        CREATE TABLE rruff_minerals (
            id INTEGER PRIMARY KEY,
            rruff_id TEXT,
            name TEXT,
            name_plain TEXT,
            formula_rruff TEXT,
            formula_ima TEXT,
            formula_concise TEXT,
            formula_html TEXT,
            ideal_chemistry TEXT,
            chemistry_elements TEXT,
            ima_number TEXT,
            ima_status TEXT,
            ima_mineral TEXT,
            year_first_published TEXT,
            structural_groupname TEXT,
            fleischers_groupname TEXT,
            crystal_system TEXT,
            space_group TEXT,
            country_type_locality TEXT,
            crystal_morphology TEXT,
            oldest_known_age_ma TEXT,
            paragenetic_modes TEXT,
            status_notes TEXT
        )
        """
    )
    conn.executemany(
        "INSERT INTO rruff_minerals (id, rruff_id, name) VALUES (?, ?, ?)",
        [(1, 'R001', 'Quartz'), (2, 'R002', 'Albite'), (3, 'R003', 'Calcite')],
    )
    conn.commit()
    return conn


def _db_instance(conn):
    db = rruff_database.RRUFFDatabase.__new__(rruff_database.RRUFFDatabase)
    db.db_path = ':memory:'
    db.available = True
    db._conn = conn
    return db


# Finding 3: limit=0 must honor an explicit zero (return empty list), not all rows.
def test_get_all_minerals_limit_zero_returns_empty():
    conn = _make_db()
    db = _db_instance(conn)
    with mock.patch.object(db, '_get_connection', return_value=conn):
        result = db.get_all_minerals(limit=0)
    assert result == []


def test_get_all_minerals_limit_none_returns_all():
    conn = _make_db()
    db = _db_instance(conn)
    with mock.patch.object(db, '_get_connection', return_value=conn):
        result = db.get_all_minerals(limit=None)
    assert len(result) == 3


# Finding 2: a failing query must not leak the connection (it must be closed).
def test_get_all_minerals_closes_connection_on_exception():
    closed = {'value': False}

    class FakeConn:
        def __init__(self):
            self.row_factory = None

        def cursor(self):
            raise sqlite3.OperationalError('boom')

        def close(self):
            closed['value'] = True

    fake = FakeConn()
    db = rruff_database.RRUFFDatabase.__new__(rruff_database.RRUFFDatabase)
    db.db_path = ':memory:'
    db.available = True
    with mock.patch.object(db, '_get_connection', return_value=fake):
        result = db.get_all_minerals()
    assert result == []
    assert closed['value'] is True


def test_get_mineral_by_id_closes_connection_on_exception():
    closed = {'value': False}

    class FakeConn:
        def __init__(self):
            self.row_factory = None

        def cursor(self):
            raise sqlite3.OperationalError('boom')

        def close(self):
            closed['value'] = True

    fake = FakeConn()
    db = rruff_database.RRUFFDatabase.__new__(rruff_database.RRUFFDatabase)
    db.db_path = ':memory:'
    db.available = True
    with mock.patch.object(db, '_get_connection', return_value=fake):
        result = db.get_mineral_by_id(1)
    assert result is None
    assert closed['value'] is True


def test_search_minerals_closes_connection_on_exception():
    closed = {'value': False}

    class FakeConn:
        def __init__(self):
            self.row_factory = None

        def cursor(self):
            raise sqlite3.OperationalError('boom')

        def close(self):
            closed['value'] = True

    fake = FakeConn()
    db = rruff_database.RRUFFDatabase.__new__(rruff_database.RRUFFDatabase)
    db.db_path = ':memory:'
    db.available = True
    with mock.patch.object(db, '_get_connection', return_value=fake):
        result = db.search_minerals('quartz')
    assert result == []
    assert closed['value'] is True


def test_search_minerals_success_still_works():
    conn = _make_db()
    db = _db_instance(conn)
    with mock.patch.object(db, '_get_connection', return_value=conn):
        result = db.search_minerals('Quartz')
    assert len(result) == 1
    assert result[0]['name'] == 'Quartz'
