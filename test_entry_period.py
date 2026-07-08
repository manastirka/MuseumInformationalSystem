#!/usr/bin/env python3
"""Spec tests for the timesheet entry period (podrazumevani mesec za unos).

Business rule (potvrdio korisnik 2026-07-08): during the current month the
employee fills the report for the PREVIOUS month (deadline the 10th; see
can_submit_for_review). January rolls back to December of the previous year.
The default month must NOT depend on how far into the month it is, nor on any
existing rows — it is purely date-driven.

The reproducing case is 2026-07-08: after the test-data reset the entry page
offered JULY (current month) instead of JUNE. These tests pin the correct
behavior and guard the day-10 deadline alignment.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-entry-period')
os.environ.setdefault('DATABASE_URL', 'postgresql://test:test@localhost:5432/test')

import unittest
from datetime import datetime
from unittest.mock import patch


class _FixedDatetime(datetime):
    """datetime subclass whose now() is frozen (repo idiom)."""

    _frozen = None

    @classmethod
    def freeze(cls, value):
        cls._frozen = value
        return cls

    @classmethod
    def now(cls, tz=None):
        if tz is not None:
            return cls._frozen.replace(tzinfo=tz)
        return cls._frozen


# (frozen today) -> expected (month, year) for entry default
PERIOD_CASES = [
    # reported bug: 8th of July -> June, NOT July
    ('bug_jul_8', datetime(2026, 7, 8), (6, 2026)),
    # first 10 days of the month still default to the previous month
    ('jul_1', datetime(2026, 7, 1), (6, 2026)),
    ('jul_10', datetime(2026, 7, 10), (6, 2026)),
    # mid-month and month-end must also stay on the previous month
    ('jul_20_mid', datetime(2026, 7, 20), (6, 2026)),
    ('jul_31_end', datetime(2026, 7, 31), (6, 2026)),
    # January rolls back to December of the previous year
    ('jan_5_rollover', datetime(2027, 1, 5), (12, 2026)),
    ('jan_25_rollover', datetime(2027, 1, 25), (12, 2026)),
    # December defaults to November of the same year
    ('dec_15', datetime(2026, 12, 15), (11, 2026)),
    ('dec_3', datetime(2026, 12, 3), (11, 2026)),
]


class DefaultEntryPeriodTests(unittest.TestCase):
    """Centralized period function in timesheet_postgres.default_entry_period."""

    def _period(self, today):
        import timesheet_postgres as tp
        with patch.object(tp, 'datetime', _FixedDatetime.freeze(today)):
            return tp.default_entry_period()

    def test_period_cases(self):
        for label, today, expected in PERIOD_CASES:
            with self.subTest(case=label):
                self.assertEqual(self._period(today), expected)

    def test_period_is_row_independent(self):
        """Two calls with the same date return the same period regardless of
        any DB state — the function must never read rows."""
        first = self._period(datetime(2026, 7, 8))
        second = self._period(datetime(2026, 7, 8))
        self.assertEqual(first, second, (6, 2026))


class ViewDelegatesToCentralPeriodTests(unittest.TestCase):
    """The employee view default must delegate to the one central function."""

    def _view_period(self, today):
        # The view delegates to timesheet_postgres.default_entry_period, so the
        # frozen clock must be patched there; patching succeeds end-to-end only
        # if the delegation is actually wired.
        import timesheet_employee_views as views
        import timesheet_postgres as tp
        with patch.object(tp, 'datetime', _FixedDatetime.freeze(today)):
            return views._default_entry_period()

    def test_view_matches_bug_case(self):
        self.assertEqual(self._view_period(datetime(2026, 7, 8)), (6, 2026))

    def test_view_matches_all_cases(self):
        for label, today, expected in PERIOD_CASES:
            with self.subTest(case=label):
                self.assertEqual(self._view_period(today), expected)


class DeadlineAlignmentTests(unittest.TestCase):
    """The default period must be submittable/editable under the day-10 rule
    on days 1-10 of the following month (the on-time window)."""

    def test_default_period_submittable_within_deadline(self):
        import timesheet_postgres as tp
        for today in (datetime(2026, 7, 1), datetime(2026, 7, 10),
                      datetime(2027, 1, 10)):
            with self.subTest(today=today.isoformat()):
                with patch.object(tp, 'datetime', _FixedDatetime.freeze(today)):
                    month, year = tp.default_entry_period()
                    ok, _ = tp.can_submit_for_review(month, year)
                    self.assertTrue(ok)

    def test_default_period_editable_as_draft_within_deadline(self):
        import timesheet_postgres as tp
        today = datetime(2026, 7, 8)
        with patch.object(tp, 'datetime', _FixedDatetime.freeze(today)):
            month, year = tp.default_entry_period()
            ok, _ = tp.can_edit_timesheet_by_status(month, year, 'DRAFT')
            self.assertTrue(ok)


if __name__ == '__main__':
    unittest.main()
