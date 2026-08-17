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


# Свако додељивање auth_version-у у SET клаузули; облик десне стране може
# да буде `+ 1` или условни `+ CASE WHEN ...`, па се тражи само леви део.
OPOZIV = 'auth_version = auth_version'

# ЗАШТО ПО ФУНКЦИЈИ, А НЕ БРОЈАЊЕМ ПО ФАЈЛУ
# Претходна верзија овог теста бројала је појављивања низа у ЦЕЛОМ фајлу
# (`count(...) >= 4`). Такав тест пролази и када функција коју треба да штити
# нема ниједан опозив — довољно је да га имају суседне. Тако је
# `api_password_manager_force_change` био без опозива сесије, а свита зелена.
# Провера по функцији пада тачно на месту које је попустило.
MESTA_SA_OPOZIVOM = [
    ('admin_user_management_views.py', 'api_password_manager_reset'),
    ('admin_user_management_views.py', 'api_password_manager_force_change'),
    ('admin_user_management_views.py', 'api_password_manager_toggle_status'),
    ('museum_control_center.py', 'reset_user_password'),
    ('museum_control_center.py', 'force_password_change'),
    ('museum_control_center.py', 'toggle_user_status'),
    ('museum_control_center.py', 'reset_and_show_password'),
    ('museum_control_center.py', 'set_temporary_password'),
    ('migrate_all_employees_to_postgres.py', 'update_existing_user'),
]


def _izvor_funkcije(putanja, ime):
    import ast
    tekst = (Path(__file__).parent / putanja).read_text(encoding='utf-8')
    for cvor in ast.walk(ast.parse(tekst)):
        if isinstance(cvor, ast.FunctionDef) and cvor.name == ime:
            return ast.get_source_segment(tekst, cvor) or ''
    raise AssertionError(f'{putanja}: нема функције {ime} — тест је застарео')


@pytest.mark.parametrize('putanja,funkcija', MESTA_SA_OPOZIVOM)
def test_svaka_promena_prava_opoziva_sesiju(putanja, funkcija):
    assert OPOZIV in _izvor_funkcije(putanja, funkcija), (
        f'{putanja}:{funkcija} мења права или лозинку, а не подиже '
        f'auth_version — постојећа сесија задржава стара права')


def test_force_change_stvarno_salje_bump_u_bazu():
    """Не гледа извор него SQL који је СТВАРНО извршен.

    Провера изнад пада ако низ нестане из функције; ова пада и ако низ остане
    али заврши у грани која се не извршава.
    """
    import admin_user_management_views as auv

    izvrseno = []

    class _Cur:
        rowcount = 1

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def execute(self, sql, params=None):
            izvrseno.append(sql)

    class _Conn:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def cursor(self, **kw):
            return _Cur()

        def commit(self):
            pass

        def rollback(self):
            pass

    app = Flask(__name__)
    app.secret_key = 'test'
    with app.test_request_context(
            '/api/admin/password_manager/force_change', method='POST',
            json={'user_id': 7, 'email': 'neko@nhmbeo.rs'}):
        session['user_email'] = 'admin@nhmbeo.rs'
        with mock.patch.object(auv, 'get_postgres_connection',
                               lambda *a, **k: _Conn()), \
             mock.patch.object(auv, 'audit_support'), \
             mock.patch.object(auv, 'add_sentry_breadcrumb', lambda **k: None):
            odgovor = auv.api_password_manager_force_change(
                log_security_event=lambda *a, **k: None)

    telo = odgovor[0] if isinstance(odgovor, tuple) else odgovor
    assert telo.get_json()['success'] is True, telo.get_json()
    assert izvrseno, 'ниједан SQL није извршен'
    assert any(OPOZIV in sql for sql in izvrseno), izvrseno
