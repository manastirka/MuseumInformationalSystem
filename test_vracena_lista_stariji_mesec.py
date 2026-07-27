#!/usr/bin/env python3
"""Regression tests: an OLDER-month returned list must be openable/editable.

Bug: ``render_timesheet_entry`` was hardwired to the PREVIOUS month
(``_default_entry_period``) and ignored ``?month=&year=``. So a list an admin
returned NA DOPUNU for, say, three months ago could not be opened for editing
via ``/timesheet/entry`` — the page always showed the previous month. The fix
lets the entry page open any requested period; a REJECTED list stays editable
through its active window regardless of age, while normal (DRAFT) entry keeps
its month deadline. A navigation banner links to returned lists of other months.
"""

import os
import unittest
from unittest.mock import MagicMock, patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-vracena-stariji')

import app as museum_app
import timesheet_employee_views
import timesheet_postgres

DEFAULT_MONTH, DEFAULT_YEAR = 6, 2026   # "previous month" for the test
OLD_MONTH, OLD_YEAR = 4, 2026           # returned list from 3 months ago


def _rejected(month, year, window=True):
    return {
        'exists': True,
        'daily_data': [],
        'OPosao': 'послови',
        'is_verified': False,
        'is_locked': False,
        'verified_by': None,
        'verified_at': None,
        'version': 2,
        'has_pending_request': False,
        'has_approved_request': False,
        'status': 'REJECTED',
        'submitted_at': None,
        'rejection_note': 'Допуни април.',
        'edit_window_active': window,
        'report_id': 900 + month,
    }


class OlderMonthReturnedListTests(unittest.TestCase):
    def _render(self, query_string, loader_side_effect, returned=None,
                ensure_mock=None):
        captured = {}

        def _capture_render(template_name, **context):
            captured.update(context)
            return 'OK'

        ensure = ensure_mock or MagicMock(return_value=42)
        with museum_app.app.test_request_context('/timesheet/entry?' + query_string):
            museum_app.session['user_name'] = 'Test User'
            museum_app.session['user_email'] = 'user@example.com'
            with patch.object(
                timesheet_employee_views, '_default_entry_period',
                return_value=(DEFAULT_MONTH, DEFAULT_YEAR),
            ), patch.object(
                timesheet_employee_views, '_year_choices',
                return_value=[2025, 2026],
            ), patch.object(
                timesheet_employee_views, '_load_timesheet_entry_data',
                side_effect=loader_side_effect,
            ), patch.object(
                timesheet_employee_views, '_load_returned_reports',
                return_value=(returned if returned is not None else []),
            ), patch.object(
                timesheet_employee_views, '_resolve_employee_profile',
                return_value=('Одељење', 'Запослени'),
            ), patch.object(
                timesheet_postgres, 'ensure_draft_exists', ensure,
            ), patch.object(
                timesheet_postgres, 'can_edit_timesheet_by_status',
                return_value=(False, 'рок истекао'),
            ), patch.object(
                timesheet_postgres, 'can_submit_for_review',
                return_value=(False, 'затворено'),
            ), patch.object(
                timesheet_employee_views, 'render_template',
                side_effect=_capture_render,
            ):
                timesheet_employee_views.render_timesheet_entry()
        return captured

    def test_old_returned_month_opens_and_is_editable(self):
        def loader(name, email, month, year):
            if (month, year) == (OLD_MONTH, OLD_YEAR):
                return _rejected(OLD_MONTH, OLD_YEAR, window=True)
            return None

        ctx = self._render(f'month={OLD_MONTH}&year={OLD_YEAR}', loader)
        self.assertEqual(ctx['selected_month'], OLD_MONTH)
        self.assertEqual(ctx['selected_year'], OLD_YEAR)
        self.assertEqual(ctx['status'], 'REJECTED')
        self.assertTrue(ctx['can_edit'], 'stara vraćena lista mora biti izmenjiva')
        self.assertTrue(ctx['show_submit_button'])

    def test_no_params_still_defaults_to_previous_month(self):
        def loader(name, email, month, year):
            return None
        ctx = self._render('', loader)
        self.assertEqual(ctx['selected_month'], DEFAULT_MONTH)
        self.assertEqual(ctx['selected_year'], DEFAULT_YEAR)

    def test_explicit_old_period_does_not_autocreate_draft(self):
        """Otvaranje starijeg meseca ne sme praviti prazne DRAFT liste."""
        def loader(name, email, month, year):
            if (month, year) == (OLD_MONTH, OLD_YEAR):
                return _rejected(OLD_MONTH, OLD_YEAR)
            return None
        ensure = MagicMock(return_value=42)
        self._render(f'month={OLD_MONTH}&year={OLD_YEAR}', loader, ensure_mock=ensure)
        ensure.assert_not_called()

    def test_default_period_still_autocreates_draft(self):
        """Za normalan (podrazumevani) mesec draft se i dalje pravi."""
        def loader(name, email, month, year):
            return None
        ensure = MagicMock(return_value=42)
        self._render('', loader, ensure_mock=ensure)
        ensure.assert_called_once()

    def test_navigation_lists_other_returned_months(self):
        def loader(name, email, month, year):
            return None  # open default month, empty there
        returned = [
            {'id': 904, 'month': 4, 'year': 2026, 'rejection_note': 'април',
             'edit_window_active': True},
            {'id': 903, 'month': 3, 'year': 2026, 'rejection_note': 'март',
             'edit_window_active': True},
        ]
        ctx = self._render('', loader, returned=returned)
        other = ctx['returned_reports_other']
        self.assertEqual({(r['month'], r['year']) for r in other},
                         {(4, 2026), (3, 2026)})

    def test_navigation_excludes_currently_open_month(self):
        def loader(name, email, month, year):
            if (month, year) == (OLD_MONTH, OLD_YEAR):
                return _rejected(OLD_MONTH, OLD_YEAR)
            return None
        returned = [
            {'id': 904, 'month': 4, 'year': 2026, 'rejection_note': 'април',
             'edit_window_active': True},
            {'id': 903, 'month': 3, 'year': 2026, 'rejection_note': 'март',
             'edit_window_active': True},
        ]
        ctx = self._render(f'month={OLD_MONTH}&year={OLD_YEAR}', loader, returned=returned)
        other = ctx['returned_reports_other']
        # April (open) excluded; March remains.
        self.assertEqual({(r['month'], r['year']) for r in other}, {(3, 2026)})


if __name__ == '__main__':
    unittest.main()
