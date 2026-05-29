"""Phase B regression tests for timesheet_employee_views (cluster: timesheet-employee)."""

import os
import sys
import types
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-timesheet-employee')

from flask import Flask

import timesheet_employee_views as tev


def _make_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret'
    return app


def _install_fake_timesheet_postgres(save_result):
    """Provide a stub timesheet_postgres module so the deferred imports succeed."""
    fake = types.ModuleType('timesheet_postgres')

    class _ErrType:
        class _V:
            value = 'x'
        CONCURRENT_MODIFICATION = _V()
        LOCKED = _V()
        VALIDATION_ERROR = _V()

    fake.TimesheetErrorType = _ErrType
    fake.get_user_department_and_position = lambda *a, **k: ('Одсек', 'Позиција')
    fake.save_timesheet_to_postgres = MagicMock(return_value=save_result)
    fake.submit_timesheet = MagicMock(
        return_value=SimpleNamespace(success=True, data={}, error=None)
    )
    return fake


def test_save_succeeds_when_status_check_raises():
    """Regression: if the pre-save status check raises (connection/SELECT failure)
    after int(month) succeeds, report_row must not be left unbound. The save still
    succeeds, so the endpoint must return success rather than a NameError-driven
    failure message."""
    app = _make_app()

    save_result = SimpleNamespace(
        success=True,
        data={'message': 'Сачувано', 'version': 2, 'report_id': 7},
        error=None,
    )
    fake_pg = _install_fake_timesheet_postgres(save_result)

    # Make the pre-save status check raise AFTER int(month)/int(year) succeed.
    boom = MagicMock(side_effect=RuntimeError('pool exhausted'))

    with patch.dict(sys.modules, {'timesheet_postgres': fake_pg}), \
            patch.object(tev, 'get_postgres_connection', boom):
        with app.test_request_context(
            '/api/timesheet/save',
            method='POST',
            json={
                'month': 5,
                'year': 2026,
                'daily_data': {},
                'obavljeni_poslovi': 'rad',
                'version': 1,
            },
        ):
            tev.session['user_email'] = 'emp@example.com'
            tev.session['user_name'] = 'Запослени'
            resp = tev.api_save_timesheet()

    # Endpoint returns either a Response or (Response, status) tuple.
    response = resp[0] if isinstance(resp, tuple) else resp
    payload = response.get_json()

    # The save persisted, so the API must report success and must NOT surface a
    # NameError ('report_row' is not defined) as a generic error message.
    assert payload['success'] is True, payload
    assert 'report_row' not in payload.get('message', '')
    assert payload['report_id'] == 7
    assert payload['auto_resubmitted'] is False


def test_save_returns_locked_when_already_submitted():
    """Sanity: when the status check works and the report is SUBMITTED, the
    endpoint short-circuits with a 423 locked response (unchanged behavior)."""
    app = _make_app()

    save_result = SimpleNamespace(
        success=True,
        data={'message': 'Сачувано', 'version': 2, 'report_id': 7},
        error=None,
    )
    fake_pg = _install_fake_timesheet_postgres(save_result)

    cur = MagicMock()
    cur.fetchone.return_value = {'status': 'SUBMITTED'}
    cur.__enter__ = MagicMock(return_value=cur)
    cur.__exit__ = MagicMock(return_value=False)

    conn = MagicMock()
    conn.cursor.return_value = cur
    conn.__enter__ = MagicMock(return_value=conn)
    conn.__exit__ = MagicMock(return_value=False)

    with patch.dict(sys.modules, {'timesheet_postgres': fake_pg}), \
            patch.object(tev, 'get_postgres_connection', MagicMock(return_value=conn)):
        with app.test_request_context(
            '/api/timesheet/save',
            method='POST',
            json={
                'month': 5,
                'year': 2026,
                'daily_data': {},
                'obavljeni_poslovi': 'rad',
                'version': 1,
            },
        ):
            tev.session['user_email'] = 'emp@example.com'
            tev.session['user_name'] = 'Запослени'
            resp = tev.api_save_timesheet()

    response, status = resp
    assert status == 423
    payload = response.get_json()
    assert payload['success'] is False
    assert payload['error_type'] == 'locked'
