import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-travel-finance')
os.environ.setdefault('DATABASE_URL', 'postgresql://localhost/test')

import importlib
import sys
import types

from flask import Flask

tfv = importlib.import_module('travel_finance_views')


class FakeCursor:
    """Minimal psycopg-like cursor that returns seeded procurement rows."""

    def __init__(self, rows):
        self._rows = rows
        self._mode = None

    def execute(self, sql, params=None):
        s = ' '.join(sql.split())
        if 'information_schema.tables' in s:
            self._mode = 'exists'
        else:
            self._mode = 'select'

    def fetchone(self):
        if self._mode == 'exists':
            return {'exists': True}
        return None

    def fetchall(self):
        return list(self._rows)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class FakeConn:
    def __init__(self, rows):
        self._rows = rows

    def cursor(self):
        return FakeCursor(self._rows)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _install_fake_psycopg(monkeypatch, rows):
    fake = types.ModuleType('psycopg')
    fake.connect = lambda *args, **kwargs: FakeConn(rows)
    fake_rows = types.ModuleType('psycopg.rows')
    fake_rows.dict_row = object()
    fake.rows = fake_rows
    monkeypatch.setitem(sys.modules, 'psycopg', fake)
    monkeypatch.setitem(sys.modules, 'psycopg.rows', fake_rows)


def _make_app():
    app = Flask(__name__)
    app.secret_key = 'test-secret'
    return app


def _call_list(monkeypatch, rows):
    _install_fake_psycopg(monkeypatch, rows)
    app = _make_app()
    with app.test_request_context('/api/nabavka/list'):
        from flask import session
        session['user_email'] = 'u@nhmbeo.rs'
        session['user_role'] = 'admin'
        resp = tfv.api_nabavka_list()
    if isinstance(resp, tuple):
        body, status = resp[0], resp[1]
    else:
        body, status = resp, 200
    return body.get_json(), status


def test_nabavka_list_well_formed_items(monkeypatch):
    rows = [
        {
            'id': 1,
            'datum': '2026-05-01',
            'podnosilac': 'Тест',
            'items': [{'description': 'Микроскоп', 'estimated': 100}],
            'procenjeno': 100,
            'status': 'pending',
            'created_at': None,
        }
    ]
    payload, status = _call_list(monkeypatch, rows)
    assert status == 200
    assert payload['success'] is True
    assert len(payload['requests']) == 1
    assert payload['requests'][0]['opis'].startswith('Микроскоп')


def test_nabavka_list_item_missing_description_does_not_mask_as_empty_success(monkeypatch):
    # Row whose first item dict lacks the 'description' key. Pre-fix this raises
    # KeyError, caught by the broad handler that returns success+empty list,
    # making ALL rows silently vanish with HTTP 200.
    rows = [
        {
            'id': 7,
            'datum': '2026-05-02',
            'podnosilac': 'Тест',
            'items': [{'estimated': 100}],
            'procenjeno': 100,
            'status': 'pending',
            'created_at': None,
        }
    ]
    payload, status = _call_list(monkeypatch, rows)
    # The request must NOT be silently dropped. Either it is rendered (with an
    # empty/blank opis) returning the row, or an honest failure is reported.
    if payload.get('success'):
        assert status == 200
        assert len(payload['requests']) == 1, (
            "row with missing 'description' was silently swallowed as empty success"
        )
        assert payload['requests'][0]['id'] == 7
    else:
        assert status != 200


def test_nabavka_list_non_dict_item_does_not_mask_as_empty_success(monkeypatch):
    # Row whose first item is a bare string (non-dict). Pre-fix this raises
    # TypeError, masked as success+empty list.
    rows = [
        {
            'id': 9,
            'datum': '2026-05-03',
            'podnosilac': 'Тест',
            'items': ['just a string'],
            'procenjeno': 50,
            'status': 'pending',
            'created_at': None,
        }
    ]
    payload, status = _call_list(monkeypatch, rows)
    if payload.get('success'):
        assert status == 200
        assert len(payload['requests']) == 1, (
            "row with non-dict item was silently swallowed as empty success"
        )
        assert payload['requests'][0]['id'] == 9
    else:
        assert status != 200


def test_nabavka_list_empty_items_uses_placeholder(monkeypatch):
    rows = [
        {
            'id': 3,
            'datum': '2026-05-04',
            'podnosilac': 'Тест',
            'items': [],
            'procenjeno': 0,
            'status': 'pending',
            'created_at': None,
        }
    ]
    payload, status = _call_list(monkeypatch, rows)
    assert status == 200
    assert payload['success'] is True
    assert len(payload['requests']) == 1
    assert payload['requests'][0]['opis'] == 'Без описа'
