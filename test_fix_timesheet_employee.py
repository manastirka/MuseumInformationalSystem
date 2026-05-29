#!/usr/bin/env python3
"""Regression tests for timesheet_employee_views render_timesheet_view().

Covers the confirmed crash bug: an out-of-range ``month``/``year`` query
param (e.g. ``?month=13`` or ``?month=0``) reaches
``_build_calendar_data`` outside any try/except in the template-render
path, raising ``calendar.IllegalMonthError`` (and ``ValueError`` for a
year-0) and producing a 500 for any authenticated user.
"""

import os
import unittest
from datetime import datetime
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-timesheet-employee')

import app as museum_app
import timesheet_employee_views


class RenderTimesheetViewMonthValidationTests(unittest.TestCase):
    def _call_with_params(self, query_string):
        """Invoke render_timesheet_view() in a request context.

        DB-touching helpers are mocked so only the month/year handling and
        the template-render path (which calls _build_calendar_data) are
        exercised.
        """
        with museum_app.app.test_request_context(
            '/timesheet/view?' + query_string
        ):
            museum_app.session['user_name'] = 'Test User'
            museum_app.session['user_email'] = 'user@example.com'
            with patch.object(
                timesheet_employee_views,
                '_load_timesheet_view_data',
                return_value=None,
            ), patch.object(
                timesheet_employee_views,
                '_resolve_employee_profile',
                return_value=('Одељење', 'Запослени'),
            ):
                return timesheet_employee_views.render_timesheet_view()

    def test_month_above_range_does_not_crash(self):
        response = self._call_with_params('month=13&year=2026')
        self.assertEqual(response.status_code, 200)

    def test_month_zero_does_not_crash(self):
        response = self._call_with_params('month=0&year=2026')
        self.assertEqual(response.status_code, 200)

    def test_year_zero_does_not_crash(self):
        response = self._call_with_params('month=5&year=0')
        self.assertEqual(response.status_code, 200)

    def test_out_of_range_month_falls_back_to_current_month(self):
        captured = {}

        def _capture(year, month):
            captured['year'] = year
            captured['month'] = month
            return []

        with museum_app.app.test_request_context(
            '/timesheet/view?month=13&year=2026'
        ):
            museum_app.session['user_name'] = 'Test User'
            museum_app.session['user_email'] = 'user@example.com'
            with patch.object(
                timesheet_employee_views,
                '_load_timesheet_view_data',
                return_value=None,
            ), patch.object(
                timesheet_employee_views,
                '_resolve_employee_profile',
                return_value=('Одељење', 'Запослени'),
            ), patch.object(
                timesheet_employee_views,
                '_build_calendar_data',
                side_effect=_capture,
            ):
                response = timesheet_employee_views.render_timesheet_view()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(captured['month'], datetime.now().month)

    def test_valid_month_is_preserved(self):
        captured = {}

        def _capture(year, month):
            captured['year'] = year
            captured['month'] = month
            return []

        with museum_app.app.test_request_context(
            '/timesheet/view?month=3&year=2026'
        ):
            museum_app.session['user_name'] = 'Test User'
            museum_app.session['user_email'] = 'user@example.com'
            with patch.object(
                timesheet_employee_views,
                '_load_timesheet_view_data',
                return_value=None,
            ), patch.object(
                timesheet_employee_views,
                '_resolve_employee_profile',
                return_value=('Одељење', 'Запослени'),
            ), patch.object(
                timesheet_employee_views,
                '_build_calendar_data',
                side_effect=_capture,
            ):
                response = timesheet_employee_views.render_timesheet_view()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(captured['month'], 3)
        self.assertEqual(captured['year'], 2026)


if __name__ == '__main__':
    unittest.main()
