#!/usr/bin/env python3
"""
Tests for the timesheet status workflow.
Tests can_submit_for_review, can_edit_timesheet_by_status, and the full
submit/approve/reject lifecycle.
"""

import unittest
from unittest.mock import patch
from datetime import datetime

from timesheet_postgres import (
    TimesheetStatus,
    can_submit_for_review,
    can_edit_timesheet_by_status,
)


class TestCanSubmitForReview(unittest.TestCase):
    """Test the submission window logic."""

    @patch('timesheet_postgres.datetime')
    def test_can_submit_february_in_march_1_7(self, mock_dt):
        """February report can be submitted March 1-7."""
        mock_dt.now.return_value = datetime(2026, 3, 5)
        can_submit, msg = can_submit_for_review(2, 2026)
        self.assertTrue(can_submit)

    @patch('timesheet_postgres.datetime')
    def test_cannot_submit_february_on_march_8(self, mock_dt):
        """February report cannot be submitted March 8+."""
        mock_dt.now.return_value = datetime(2026, 3, 8)
        can_submit, msg = can_submit_for_review(2, 2026)
        self.assertFalse(can_submit)

    @patch('timesheet_postgres.datetime')
    def test_cannot_submit_february_in_february(self, mock_dt):
        """February report cannot be submitted during February."""
        mock_dt.now.return_value = datetime(2026, 2, 15)
        can_submit, msg = can_submit_for_review(2, 2026)
        self.assertFalse(can_submit)

    @patch('timesheet_postgres.datetime')
    def test_december_submits_in_january_next_year(self, mock_dt):
        """December report can be submitted January 1-7 of the next year."""
        mock_dt.now.return_value = datetime(2027, 1, 3)
        can_submit, msg = can_submit_for_review(12, 2026)
        self.assertTrue(can_submit)

    @patch('timesheet_postgres.datetime')
    def test_december_cannot_submit_january_8(self, mock_dt):
        """December report cannot be submitted January 8+."""
        mock_dt.now.return_value = datetime(2027, 1, 8)
        can_submit, msg = can_submit_for_review(12, 2026)
        self.assertFalse(can_submit)

    @patch('timesheet_postgres.datetime')
    def test_boundary_day_7(self, mock_dt):
        """Day 7 is the last day of the submission window."""
        mock_dt.now.return_value = datetime(2026, 4, 7)
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
    def test_draft_in_next_month_day_8(self, mock_dt):
        """DRAFT is not editable after day 7 of next month."""
        mock_dt.now.return_value = datetime(2026, 4, 8)
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
        self.assertEqual(len(TimesheetStatus), 4)


if __name__ == '__main__':
    unittest.main()
