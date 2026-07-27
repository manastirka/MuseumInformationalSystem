#!/usr/bin/env python3
"""Regression tests for the "vraćena radna lista se ne može dopuniti" bug.

Scenario: an admin/šef returns an employee's timesheet NA DOPUNU (status
REJECTED). The reject grants a fresh 24 h edit window (``editable_until =
NOW() + 24h``, ``is_locked = FALSE``) that is meant to override the normal
day-10 calendar deadline for that report only.

The save layer (``timesheet_postgres.save_timesheet``) already honours that
window. The bug is in the entry VIEW (``render_timesheet_entry``): it derives
``can_edit`` purely from ``can_edit_timesheet_by_status(month, year, status)``,
which enforces the calendar deadline and ignores the active window. So a report
returned after the 10th of the following month renders with every input and the
save button ``disabled`` — the employee cannot make the required corrections,
which makes the whole return-for-revision flow useless.
"""

import os
import unittest
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-vracena-lista')

import app as museum_app
import timesheet_employee_views
import timesheet_postgres


def _rejected_report(edit_window_active):
    """A REJECTED report as returned by _load_timesheet_entry_data."""
    return {
        'exists': True,
        'daily_data': [],
        'OPosao': 'обављени послови',
        'is_verified': False,
        'is_locked': False,
        'verified_by': None,
        'verified_at': None,
        'version': 2,
        'has_pending_request': False,
        'has_approved_request': False,
        'status': 'REJECTED',
        'submitted_at': None,
        'rejection_note': 'Допуни дане 15. и 16.',
        'edit_window_active': edit_window_active,
        'report_id': 42,
    }


class VracenaListaEditableTests(unittest.TestCase):
    def _render_entry(self, timesheet_data):
        """Invoke render_timesheet_entry() and capture the template context.

        The default entry period is the PREVIOUS month; combined with the
        forced past-deadline ``can_edit_timesheet_by_status`` below this
        reproduces the real production timing where a report is returned
        after the day-10 deadline.
        """
        captured = {}

        def _capture_render(template_name, **context):
            captured.update(context)
            return 'OK'

        with museum_app.app.test_request_context('/timesheet/entry'):
            museum_app.session['user_name'] = 'Test User'
            museum_app.session['user_email'] = 'user@example.com'
            with patch.object(
                timesheet_employee_views, '_load_timesheet_entry_data',
                return_value=timesheet_data,
            ), patch.object(
                timesheet_employee_views, '_resolve_employee_profile',
                return_value=('Одељење', 'Запослени'),
            ), patch.object(
                timesheet_postgres, 'ensure_draft_exists', return_value=42,
            ), patch.object(
                # Force the calendar deadline to be CLOSED, as it is for any
                # report returned after the 10th of the following month.
                timesheet_postgres, 'can_edit_timesheet_by_status',
                return_value=(False, 'Време за измену радне листе је истекло.'),
            ), patch.object(
                timesheet_postgres, 'can_submit_for_review',
                return_value=(False, 'Подношење је затворено.'),
            ), patch.object(
                timesheet_employee_views, 'render_template',
                side_effect=_capture_render,
            ):
                timesheet_employee_views.render_timesheet_entry()
        return captured

    def test_rejected_report_in_active_window_is_editable(self):
        """A returned report with a live 24 h window must be editable."""
        ctx = self._render_entry(_rejected_report(edit_window_active=True))
        self.assertEqual(ctx['status'], 'REJECTED')
        self.assertTrue(
            ctx['can_edit'],
            "Vraćena lista sa aktivnim 24h prozorom mora biti izmenjiva u UI-ju",
        )
        self.assertTrue(
            ctx['show_submit_button'],
            "Zaposleni mora moći ponovo da pošalje vraćenu listu",
        )

    def test_rejection_note_is_shown(self):
        """The šef/admin comment must reach the employee view."""
        ctx = self._render_entry(_rejected_report(edit_window_active=True))
        self.assertEqual(ctx['rejection_note'], 'Допуни дане 15. и 16.')

    def test_rejected_report_after_window_expired_stays_locked(self):
        """Once the 24 h window has passed the report is not editable here."""
        ctx = self._render_entry(_rejected_report(edit_window_active=False))
        self.assertFalse(
            ctx['can_edit'],
            "Istekli prozor: dopuna nije moguća bez novog otključavanja",
        )


if __name__ == '__main__':
    unittest.main()
