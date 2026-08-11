"""Revizija 2026-08 (batch 6, stavka 6): odobravanje/brisanje radnih lista
ne sme da guta izuzetke bez loga, ne sme da vraća sirov str(exc) korisniku,
a pad notifikacije ne sme da „poništi" potpis koji je već commit-ovan.

Scenario iz nalaza: confirm_timesheet_signature commit-uje potpis u svojoj
transakciji; potom pad INSERT-a notifikacije obara rutu — admin vidi
„Грешка", lista je već odobrena i zaključana, ponovni pokušaj dobija „Само
поднете листе могу бити одобрене". Notifikacija je sada best-effort
(SAVEPOINT + logger.exception).
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-timesheet-greske')

import logging

import pytest
from flask import session as flask_session

import timesheet_admin_views
import timesheet_postgres
from timesheet_postgres import TimesheetResult


class _Cursor:
    """Fake kursor: SELECT izveštaja + heads; INSERT notifikacije po izboru
    pada; SAVEPOINT/ROLLBACK se beleže radi provere protokola."""

    def __init__(self, notif_fails=False, select_fails=False):
        self.notif_fails = notif_fails
        self.select_fails = select_fails
        self.executed = []
        self._result = None

    def execute(self, sql, params=None):
        squashed = ' '.join(sql.split())
        self.executed.append(squashed)
        self._result = None
        if 'FROM timesheet_reports' in squashed and 'SELECT' in squashed:
            if self.select_fails:
                raise RuntimeError('TAJNA_INTERNA_GRESKA_XYZ')
            self._result = {
                'id': 5, 'employee_name': 'Пера Перић', 'month': 3,
                'year': 2026, 'status': 'SUBMITTED',
                'employee_email': 'pera@example.com',
                'employee_department': 'Геологија',
            }
        elif 'head_email' in squashed:
            self._result = []
        elif 'INSERT INTO user_notifications' in squashed:
            if self.notif_fails:
                raise RuntimeError('notifikacije nedostupne')

    def fetchone(self):
        return self._result

    def fetchall(self):
        return self._result if isinstance(self._result, list) else []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class _Conn:
    def __init__(self, cursor):
        self._cursor = cursor
        self.commits = 0

    def cursor(self):
        return self._cursor

    def commit(self):
        self.commits += 1

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


@pytest.fixture
def admin_ctx():
    import app as museum_app
    with museum_app.app.test_request_context(
            '/api/admin/timesheet/5/approve', method='POST',
            json={'approve': True}):
        flask_session['user_email'] = 'admin@example.com'
        flask_session['user_role'] = 'admin'
        yield


def _fake_signature_ok(*args, **kwargs):
    return TimesheetResult.ok({
        'report_id': 5, 'approved': True, 'administrative': True,
        'status': 'APPROVED', 'head_verified': True, 'director_verified': True,
        'head_verified_by': None, 'director_verified_by': None,
    })


def test_pad_notifikacije_ne_ponistava_potpis(admin_ctx, monkeypatch, caplog):
    """Potpis je commit-ovan — ruta MORA da vrati uspeh iako je notifikacija
    pala, a otkaz notifikacije mora biti logovan."""
    cur = _Cursor(notif_fails=True)
    monkeypatch.setattr(timesheet_admin_views, 'get_postgres_connection',
                        lambda **kw: _Conn(cur))
    monkeypatch.setattr(timesheet_postgres, 'confirm_timesheet_signature',
                        _fake_signature_ok)

    with caplog.at_level(logging.ERROR):
        response = timesheet_admin_views.api_admin_approve_timesheet_report(5)

    payload = (response[0] if isinstance(response, tuple) else response).get_json()
    assert payload['success'] is True, payload
    assert 'одобрен' in payload['message']
    # best-effort protokol: SAVEPOINT pre INSERT-a, ROLLBACK posle pada
    assert any('SAVEPOINT user_notif' == sql for sql in cur.executed)
    assert any('ROLLBACK TO SAVEPOINT user_notif' == sql for sql in cur.executed)
    assert any(record.exc_info for record in caplog.records), \
        'pad notifikacije mora biti logovan sa stack trace-om'


def test_uspesna_notifikacija_ide_kroz_savepoint(admin_ctx, monkeypatch):
    cur = _Cursor(notif_fails=False)
    monkeypatch.setattr(timesheet_admin_views, 'get_postgres_connection',
                        lambda **kw: _Conn(cur))
    monkeypatch.setattr(timesheet_postgres, 'confirm_timesheet_signature',
                        _fake_signature_ok)

    response = timesheet_admin_views.api_admin_approve_timesheet_report(5)
    payload = (response[0] if isinstance(response, tuple) else response).get_json()
    assert payload['success'] is True
    assert any('INSERT INTO user_notifications' in sql for sql in cur.executed)
    assert any('RELEASE SAVEPOINT user_notif' == sql for sql in cur.executed)


def test_greska_se_loguje_i_ne_curi_korisniku(admin_ctx, monkeypatch, caplog):
    """Neuspeh rute: izuzetak se loguje (logger.exception), a korisniku ide
    generička poruka — nikad sirov str(exc)."""
    cur = _Cursor(select_fails=True)
    monkeypatch.setattr(timesheet_admin_views, 'get_postgres_connection',
                        lambda **kw: _Conn(cur))

    with caplog.at_level(logging.ERROR):
        response = timesheet_admin_views.api_admin_approve_timesheet_report(5)

    payload = (response[0] if isinstance(response, tuple) else response).get_json()
    assert payload['success'] is False
    assert 'TAJNA_INTERNA_GRESKA_XYZ' not in payload['message']
    assert payload['message'] == 'Грешка при обради извештаја.'
    assert any(record.exc_info for record in caplog.records), \
        'izuzetak mora biti logovan sa stack trace-om'


def test_nijedan_handler_ne_vraca_sirov_izuzetak():
    """Strukturna zaštita: obrazac "f'Грешка: {str(exc)}'" ne sme da se vrati
    u timesheet_admin_views."""
    from pathlib import Path
    text = (Path(__file__).parent / 'timesheet_admin_views.py').read_text(encoding='utf-8')
    assert "{str(exc)}" not in text
    assert 'except Exception as exc:\n        return jsonify' not in text
