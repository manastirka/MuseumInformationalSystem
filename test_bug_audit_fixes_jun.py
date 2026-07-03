#!/usr/bin/env python3
"""Regression tests for the 2026-06 bug audit fixes.

Covers:
1. timesheet_postgres.save_timesheet_to_postgres — UPDATE ... RETURNING that
   matches zero rows must return a failed TimesheetResult, not TypeError.
2. timesheet_word_export.generate_word_document — a corrupted month value in
   timesheet_reports must raise a clear ValueError before document generation.
3. travel_finance_views.api_nabavka_list — the director (admin parity) sees
   all procurement requests, not just their own.
"""

import os
import unittest
from contextlib import contextmanager
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')


class _FakeCursor:
    """Cursor returning canned rows keyed by a SQL substring; records SQL."""

    def __init__(self, canned):
        self._canned = canned
        self._pending = None
        self.executed = []

    def execute(self, sql, params=None):
        self.executed.append(sql)
        self._pending = None
        for needle, row in self._canned.items():
            if needle in sql:
                self._pending = row
                return

    def fetchone(self):
        value = self._pending
        if isinstance(value, list):
            return value[0] if value else None
        return value

    def fetchall(self):
        value = self._pending
        if isinstance(value, list):
            return value
        return [value] if value else []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class _FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor

    def cursor(self, *args, **kwargs):
        return self._cursor

    def commit(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


@contextmanager
def _fake_conn_ctx(cursor):
    yield _FakeConnection(cursor)


class SaveTimesheetReturningGuardTests(unittest.TestCase):
    """Bug #1: cur.fetchone()['version'] after UPDATE ... RETURNING."""

    def test_update_matching_zero_rows_returns_failure_not_typeerror(self):
        from datetime import datetime as _dt

        import timesheet_postgres

        cursor = _FakeCursor({
            'FOR UPDATE': {
                'id': 1,
                'version': 1,
                'is_locked': False,
                'is_verified': False,
                'status': 'DRAFT',
                'editable_until': None,
                'edit_window_expired': False,
            },
            'RETURNING version': None,
        })

        # Tekući mesec — uvek unutar roka za unos, da provera roka ne
        # presretne put do UPDATE ... RETURNING grane koju test cilja.
        _today = _dt.now()
        with patch.object(timesheet_postgres, 'get_pg_connection',
                          lambda: _fake_conn_ctx(cursor)):
            result = timesheet_postgres.save_timesheet_to_postgres(
                user_email='test@nhmbeo.rs',
                user_name='Тест Тестић',
                month=_today.month,
                year=_today.year,
                daily_data={},
                work_description='',
                organization_unit='БИОЛОШКО ОДЕЉЕЊЕ',
                position='кустос',
            )

        self.assertFalse(result.success)
        # Pre-fix the TypeError is swallowed by the generic exception handler
        # and surfaces as DATABASE_ERROR; the guard must classify it properly.
        self.assertEqual(result.error.error_type,
                         timesheet_postgres.TimesheetErrorType.CONCURRENT_MODIFICATION)


class WordExportInvalidMonthTests(unittest.TestCase):
    """Bug #2: calendar.monthrange called with an unvalidated month."""

    def test_corrupted_month_raises_clear_error(self):
        import timesheet_word_export

        cursor = _FakeCursor({
            'FROM timesheet_reports': {
                'id': 7,
                'employee_name': 'Тест Тестић',
                'month': 13,
                'year': 2026,
                'organization_unit': 'БИОЛОШКО ОДЕЉЕЊЕ',
                'position': 'кустос',
                'special_tasks': '',
                'extraordinary_tasks': '',
                'duties_summary': '',
                'created_at': None,
            },
            'FROM timesheet_report_days': [],
        })

        with patch.object(timesheet_word_export.psycopg, 'connect',
                          lambda *a, **k: _fake_conn_ctx(cursor)):
            with self.assertRaises(ValueError) as ctx:
                timesheet_word_export.generate_word_document(
                    7, 'postgresql://x/y')

        self.assertIn('месец', str(ctx.exception))


class NabavkaListDirectorParityTests(unittest.TestCase):
    """Bug #3: director must get the admin branch (all requests)."""

    def test_director_sees_all_requests(self):
        import app as museum_app
        import travel_finance_views

        cursor = _FakeCursor({
            'information_schema.tables': {'exists': True},
            'FROM procurement_requests': [],
        })

        with museum_app.app.test_request_context('/api/nabavka/list'):
            from flask import session
            session['user_id'] = 2
            session['user_email'] = 'slavko.spasic@nhmbeo.rs'
            session['user_role'] = 'direktor'
            session['is_admin'] = False

            with patch('psycopg.connect', lambda *a, **k: _fake_conn_ctx(cursor)):
                response = travel_finance_views.api_nabavka_list()

        self.assertTrue(response.get_json()['success'])
        listing_queries = [q for q in cursor.executed
                           if 'FROM procurement_requests' in q]
        self.assertTrue(listing_queries)
        self.assertNotIn('WHERE user_email', listing_queries[0],
                         'director was scoped to own requests — expected admin branch')


if __name__ == '__main__':
    unittest.main()
