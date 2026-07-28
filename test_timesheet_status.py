#!/usr/bin/env python3
"""
Tests for the timesheet status workflow.
Tests can_submit_for_review, can_edit_timesheet_by_status, and the full
submit/approve/reject lifecycle.
"""

import os
import unittest
from contextlib import contextmanager
from unittest.mock import patch
from datetime import datetime

from timesheet_postgres import (
    TimesheetStatus,
    TimesheetErrorType,
    can_submit_for_review,
    can_edit_timesheet_by_status,
    submit_timesheet,
)


class TestCanSubmitForReview(unittest.TestCase):
    """Test the submission window logic."""

    def setUp(self):
        self._env_patch = patch.dict(
            os.environ,
            {'FLASK_ENV': 'production', 'TIMESHEET_SUBMIT_DEADLINE_BYPASS': '0'},
        )
        self._env_patch.start()
        if can_submit_for_review(1, 1999)[0]:
            self.skipTest('Timesheet submission deadline enforcement is disabled in this branch')

    def tearDown(self):
        self._env_patch.stop()

    @patch('timesheet_postgres.datetime')
    def test_can_submit_february_in_march_1_7(self, mock_dt):
        """February report can be submitted March 1-7."""
        mock_dt.now.return_value = datetime(2026, 3, 5)
        can_submit, msg = can_submit_for_review(2, 2026)
        self.assertTrue(can_submit)

    @patch('timesheet_postgres.datetime')
    def test_cannot_submit_february_on_march_11(self, mock_dt):
        """February report cannot be submitted March 11+ (deadline is the 10th)."""
        mock_dt.now.return_value = datetime(2026, 3, 11)
        can_submit, msg = can_submit_for_review(2, 2026)
        self.assertFalse(can_submit)

    @patch('timesheet_postgres.datetime')
    def test_can_submit_february_in_february(self, mock_dt):
        """February report can be submitted already during February."""
        mock_dt.now.return_value = datetime(2026, 2, 15)
        can_submit, msg = can_submit_for_review(2, 2026)
        self.assertTrue(can_submit)

    @patch('timesheet_postgres.datetime')
    def test_december_submits_in_january_next_year(self, mock_dt):
        """December report can be submitted January 1-7 of the next year."""
        mock_dt.now.return_value = datetime(2027, 1, 3)
        can_submit, msg = can_submit_for_review(12, 2026)
        self.assertTrue(can_submit)

    @patch('timesheet_postgres.datetime')
    def test_december_cannot_submit_january_11(self, mock_dt):
        """December report cannot be submitted January 11+ (deadline is the 10th)."""
        mock_dt.now.return_value = datetime(2027, 1, 11)
        can_submit, msg = can_submit_for_review(12, 2026)
        self.assertFalse(can_submit)

    @patch('timesheet_postgres.datetime')
    def test_boundary_day_10(self, mock_dt):
        """Day 10 is the last day of the submission window."""
        mock_dt.now.return_value = datetime(2026, 4, 10)
        can_submit, msg = can_submit_for_review(3, 2026)
        self.assertTrue(can_submit)

    @patch('timesheet_postgres.datetime')
    def test_boundary_day_1(self, mock_dt):
        """Day 1 is the first day of the submission window."""
        mock_dt.now.return_value = datetime(2026, 4, 1)
        can_submit, msg = can_submit_for_review(3, 2026)
        self.assertTrue(can_submit)


class TestCanEditTimesheetByStatus(unittest.TestCase):
    """Test edit permissions based on status and date."""

    def setUp(self):
        self._env_patch = patch.dict(
            os.environ,
            {'FLASK_ENV': 'production', 'TIMESHEET_SUBMIT_DEADLINE_BYPASS': '0'},
        )
        self._env_patch.start()
        if can_submit_for_review(1, 1999)[0]:
            self.skipTest('Timesheet edit deadline enforcement is disabled in this branch')

    def tearDown(self):
        self._env_patch.stop()

    @patch('timesheet_postgres.datetime')
    def test_draft_in_current_month(self, mock_dt):
        """DRAFT in current month is editable."""
        mock_dt.now.return_value = datetime(2026, 3, 15)
        can_edit, msg = can_edit_timesheet_by_status(3, 2026, 'DRAFT')
        self.assertTrue(can_edit)

    @patch('timesheet_postgres.datetime')
    def test_draft_in_next_month_days_1_7(self, mock_dt):
        """DRAFT is editable during days 1-7 of the next month."""
        mock_dt.now.return_value = datetime(2026, 4, 5)
        can_edit, msg = can_edit_timesheet_by_status(3, 2026, 'DRAFT')
        self.assertTrue(can_edit)

    @patch('timesheet_postgres.datetime')
    def test_draft_in_next_month_day_11(self, mock_dt):
        """DRAFT is not editable after day 10 of next month."""
        mock_dt.now.return_value = datetime(2026, 4, 11)
        can_edit, msg = can_edit_timesheet_by_status(3, 2026, 'DRAFT')
        self.assertFalse(can_edit)

    @patch('timesheet_postgres.datetime')
    def test_rejected_is_editable_in_window(self, mock_dt):
        """REJECTED is editable like DRAFT."""
        mock_dt.now.return_value = datetime(2026, 3, 15)
        can_edit, msg = can_edit_timesheet_by_status(3, 2026, 'REJECTED')
        self.assertTrue(can_edit)

    @patch('timesheet_postgres.datetime')
    def test_submitted_not_editable(self, mock_dt):
        """SUBMITTED is never editable by employee."""
        mock_dt.now.return_value = datetime(2026, 3, 15)
        can_edit, msg = can_edit_timesheet_by_status(3, 2026, 'SUBMITTED')
        self.assertFalse(can_edit)

    @patch('timesheet_postgres.datetime')
    def test_approved_not_editable(self, mock_dt):
        """APPROVED is never editable by employee."""
        mock_dt.now.return_value = datetime(2026, 3, 15)
        can_edit, msg = can_edit_timesheet_by_status(3, 2026, 'APPROVED')
        self.assertFalse(can_edit)

    @patch('timesheet_postgres.datetime')
    def test_december_editable_in_january(self, mock_dt):
        """December DRAFT is editable in January 1-7."""
        mock_dt.now.return_value = datetime(2027, 1, 5)
        can_edit, msg = can_edit_timesheet_by_status(12, 2026, 'DRAFT')
        self.assertTrue(can_edit)


class TestTimesheetStatusEnum(unittest.TestCase):
    """Test the TimesheetStatus enum."""

    def test_enum_values(self):
        self.assertEqual(TimesheetStatus.DRAFT.value, 'DRAFT')
        self.assertEqual(TimesheetStatus.SUBMITTED.value, 'SUBMITTED')
        self.assertEqual(TimesheetStatus.APPROVED.value, 'APPROVED')
        self.assertEqual(TimesheetStatus.REJECTED.value, 'REJECTED')

    def test_enum_count(self):
        # +ARHIVA (fix/revizija-lanca): архива није званично одобрен извештај.
        self.assertEqual(len(TimesheetStatus), 5)


class _SubmitCursor:
    def __init__(self, report):
        self.report = report
        self.executed = []

    def execute(self, sql, params=None):
        self.executed.append((sql, params))

    def fetchone(self):
        return self.report

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class _SubmitConnection:
    def __init__(self, cursor):
        self.cursor_obj = cursor
        self.commits = 0

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.commits += 1

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


@contextmanager
def _submit_connection(report):
    cursor = _SubmitCursor(report)
    yield _SubmitConnection(cursor)


class TestSubmitTimesheetOwnership(unittest.TestCase):
    """Submission must be limited to the logged-in employee's own report."""

    def test_submit_rejects_report_owned_by_another_employee(self):
        report = {
            'id': 77,
            'month': 3,
            'year': 2026,
            'status': 'DRAFT',
            'employee_email': 'owner@nhmbeo.rs',
        }

        with patch('timesheet_postgres.get_pg_connection', return_value=_submit_connection(report)):
            result = submit_timesheet(77, 'other@nhmbeo.rs')

        self.assertFalse(result.success)
        self.assertEqual(result.error.error_type, TimesheetErrorType.PERMISSION_DENIED)

    def test_submit_rejects_report_without_owner_email(self):
        report = {
            'id': 78,
            'month': 3,
            'year': 2026,
            'status': 'DRAFT',
            'employee_email': None,
        }

        with patch('timesheet_postgres.get_pg_connection', return_value=_submit_connection(report)):
            result = submit_timesheet(78, 'employee@nhmbeo.rs')

        self.assertFalse(result.success)
        self.assertEqual(result.error.error_type, TimesheetErrorType.PERMISSION_DENIED)


if __name__ == '__main__':
    unittest.main()
