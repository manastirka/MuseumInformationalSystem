"""Phase C timesheet-employee cluster: low-severity hardening fix tests."""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-timesheet-employee')

from contextlib import contextmanager
from unittest.mock import MagicMock

import pytest

import timesheet_employee_views


class _FakeCursor:
    """Minimal cursor: first fetchone returns the report row; INSERT params captured."""

    def __init__(self, report_row, captured):
        self._report_row = report_row
        self._captured = captured
        self._last_was_select = False

    def execute(self, query, params=None):
        if 'SELECT' in query:
            self._last_was_select = True
        else:
            self._last_was_select = False
            # Capture the user_notifications INSERT params.
            self._captured.append(params)

    def fetchone(self):
        if self._last_was_select:
            return self._report_row
        return None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class _FakeConn:
    def __init__(self, report_row, captured):
        self._report_row = report_row
        self._captured = captured

    def cursor(self):
        return _FakeCursor(self._report_row, self._captured)

    def commit(self):
        pass


def _patch_connection(monkeypatch, report_row, captured):
    @contextmanager
    def fake_get_conn(*args, **kwargs):
        yield _FakeConn(report_row, captured)

    monkeypatch.setattr(
        timesheet_employee_views, 'get_postgres_connection', fake_get_conn
    )


def _run_outcome_notify(monkeypatch, month):
    """Invoke the helper and return the rendered month_name passed to the template."""
    captured = []
    report_row = {
        'employee_email': 'someone@example.com',
        'employee_name': 'Тест Запослени',
        'month': month,
        'year': 2026,
    }
    _patch_connection(monkeypatch, report_row, captured)

    rendered = {}

    def message_template(month_name, year):
        rendered['month_name'] = month_name
        rendered['year'] = year
        return f'msg {month_name} {year}'

    timesheet_employee_views._notify_employee_about_review_outcome(
        1, 'title', 'bi-check-circle', message_template
    )
    # Ensure an INSERT actually happened (report had an email).
    assert captured, 'expected a user_notifications INSERT to be issued'
    return rendered['month_name']


def test_month_zero_does_not_yield_empty_name(monkeypatch):
    """Finding 1: month 0 must not produce an empty month name in the notification."""
    month_name = _run_outcome_notify(monkeypatch, 0)
    assert month_name == '0'
    assert month_name != ''


def test_negative_month_does_not_wrap_to_december(monkeypatch):
    """Finding 1: a negative month must not index from the end (-1 -> 'децембар')."""
    month_name = _run_outcome_notify(monkeypatch, -1)
    assert month_name == '-1'
    assert month_name != 'децембар'


def test_valid_month_still_maps_to_serbian_name(monkeypatch):
    """Regression guard: valid month 1-12 still resolves to the lowercase Serbian name."""
    month_name = _run_outcome_notify(monkeypatch, 3)
    assert month_name == 'март'
