"""Revizija 2026-08, stavka 6: opoziv sesije preko users.auth_version.

Deaktivacija, promena uloge i promena/reset lozinke podižu auth_version;
sesija sa starom (ili bez) verzijom se ruši pri prvom sledećem zahtevu.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-auth-version')

from pathlib import Path
from unittest import mock

import pytest
from flask import Flask, session

import security_utils


@pytest.fixture(scope='module', autouse=True)
def _primeni_migraciju_051():
    """Idempotentno primeni migraciju 051 na test bazu (obrazac iz
    test_audit_trail.py) — kolona je preduslov i za druge testove svite
    koji gađaju prave rute za reset lozinke / status naloga."""
    import psycopg
    url = os.environ['DATABASE_URL'].replace('postgresql+psycopg://', 'postgresql://')
    sql = (Path(__file__).parent / 'migration'
           / '051_users_auth_version.sql').read_text(encoding='utf-8')
    try:
        with psycopg.connect(url) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()
    except Exception as exc:
        pytest.skip(f'test baza nedostupna: {exc}')
    yield


class _FakeCursor:
    def __init__(self, row):
        self._row = row
        self.executed = []

    def execute(self, sql, params=None):
        self.executed.append((sql, params))

    def fetchone(self):
        return self._row

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class _FakeConn:
    def __init__(self, row):
        self._cur = _FakeCursor(row)

    def cursor(self):
        return self._cur

    def commit(self):
        pass

    def rollback(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _make_app():
    app = Flask(__name__)
    app.secret_key = 'test-secret'
    app.add_url_rule('/login', 'login', lambda: '')
    return app


def _check(row, session_data, path='/dashboard'):
    app = _make_app()
    with app.test_request_context(path):
        for k, v in session_data.items():
            session[k] = v
        with mock.patch('postgres_service.get_postgres_connection',
                        lambda **kw: _FakeConn(row)):
            result = security_utils.validate_session_auth_version()
        cleared = 'user_id' not in session
    return result, cleared


def test_vazeca_sesija_prolazi():
    result, cleared = _check((3,), {'user_id': 1, 'auth_version': 3})
    assert result is None
    assert not cleared


def test_stara_verzija_rusi_sesiju():
    result, cleared = _check((4,), {'user_id': 1, 'auth_version': 3})
    assert result is not None
    assert cleared
    # redirect na login
    assert result.status_code in (301, 302)


def test_sesija_bez_verzije_se_rusi():
    # sesije od pre uvođenja mehanizma nemaju auth_version — padaju jednom
    result, cleared = _check((1,), {'user_id': 1})
    assert result is not None
    assert cleared


def test_deaktiviran_ili_obrisan_korisnik_se_rusi():
    result, cleared = _check(None, {'user_id': 1, 'auth_version': 3})
    assert result is not None
    assert cleared


def test_api_putanja_dobija_401_json():
    result, cleared = _check((4,), {'user_id': 1, 'auth_version': 3},
                             path='/api/nesto')
    assert cleared
    response, status = result
    assert status == 401


def test_fallback_nalog_se_ne_proverava():
    app = _make_app()
    with app.test_request_context('/dashboard'):
        session['user_id'] = 1
        session['auth_source'] = 'fallback'
        called = {'db': False}

        def _boom(**kw):
            called['db'] = True
            raise AssertionError('ne sme do baze')

        with mock.patch('postgres_service.get_postgres_connection', _boom):
            result = security_utils.validate_session_auth_version()
    assert result is None
    assert called['db'] is False


def test_neprijavljen_zahtev_prolazi():
    result, _cleared = _check((1,), {})
    assert result is None


def test_greska_baze_je_fail_open():
    app = _make_app()
    with app.test_request_context('/dashboard'):
        session['user_id'] = 1
        session['auth_version'] = 3

        def _boom(**kw):
            raise RuntimeError('db down')

        with mock.patch('postgres_service.get_postgres_connection', _boom):
            result = security_utils.validate_session_auth_version()
        assert 'user_id' in session
    assert result is None


def test_migracija_051_postoji_i_dodaje_kolonu():
    sql = open(os.path.join(os.path.dirname(__file__),
                            'migration', '051_users_auth_version.sql')).read()
    assert 'ADD COLUMN IF NOT EXISTS auth_version' in sql


def test_bump_na_promenama_prava():
    """Sva mesta koja menjaju prava moraju da podižu auth_version."""
    src_admin = open('admin_user_management_views.py').read()
    assert src_admin.count('auth_version = auth_version + 1') >= 4
    src_auth = open('postgres_auth.py').read()
    assert 'auth_version = auth_version + 1' in src_auth
    src_mcc = open('museum_control_center.py').read()
    assert src_mcc.count('auth_version = auth_version + 1') >= 4
