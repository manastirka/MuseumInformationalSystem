#!/usr/bin/env python3
"""Service-layer tests for admin unlock of timesheet entry (per employee/month).

admin_unlock_entry reuses editable_until so a late employee can enter+submit an
old month that is past the normal deadline; SUBMITTED/APPROVED lists are not
touched. Skips when PostgreSQL is unavailable.
"""

import os
import unittest
from datetime import datetime

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-unlock')

import timesheet_postgres as tp


def _pg_available():
    try:
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT 1')
                cur.fetchone()
        return True
    except Exception:
        return False


def _real_employee():
    """A real user email/name to unlock (unlock looks up users.full_name)."""
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT email, full_name FROM users "
                        "WHERE full_name IS NOT NULL AND email IS NOT NULL "
                        "ORDER BY id LIMIT 1")
            return cur.fetchone()


ADMIN = 'admin.unlock.test@example.com'


@unittest.skipUnless(_pg_available(), 'PostgreSQL nije dostupan')
class AdminUnlockEntryTests(unittest.TestCase):
    def setUp(self):
        emp = _real_employee()
        self.assertIsNotNone(emp, 'baza mora imati bar jednog korisnika')
        self.email = emp['email']
        self.name = emp['full_name']
        # Old month: 4 months ago (well past the day-10 deadline).
        now = datetime.now()
        idx = now.year * 12 + (now.month - 1) - 4
        self.year, self.month = idx // 12, idx % 12 + 1
        self._cleanup()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM timesheet_reports "
                            "WHERE employee_email = %s AND month = %s AND year = %s",
                            (self.email, self.month, self.year))
                conn.commit()

    def _status(self, report_id):
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COALESCE(status,'DRAFT') AS status, is_locked, "
                            "(editable_until IS NOT NULL AND NOW() < editable_until) AS win "
                            "FROM timesheet_reports WHERE id = %s", (report_id,))
                return cur.fetchone()

    def test_unlock_enables_entry_and_submit_for_old_month(self):
        # Before unlock: a fresh save for the old month is blocked by deadline.
        blocked = tp.save_timesheet_to_postgres(
            user_email=self.email, user_name=self.name, month=self.month,
            year=self.year, daily_data={'10': {'rad_na_mestu': 8}},
            work_description='x', organization_unit='X', position='Y')
        self.assertFalse(blocked.success, 'stari mesec bez otključavanja ne sme proći')

        # Admin unlocks.
        res = tp.admin_unlock_entry(self.email, self.month, self.year, ADMIN)
        self.assertTrue(res.success, res.error.message if res.error else res)
        rid = res.data['report_id']
        self.assertTrue(self._status(rid)['win'], 'unlock mora otvoriti prozor')
        self.assertFalse(self._status(rid)['is_locked'])

        # After unlock: employee can save and submit the old month.
        saved = tp.save_timesheet_to_postgres(
            user_email=self.email, user_name=self.name, month=self.month,
            year=self.year, daily_data={'10': {'rad_na_mestu': 8}},
            work_description='допуна', organization_unit='X', position='Y')
        self.assertTrue(saved.success, saved.error.message if saved.error else saved)
        submitted = tp.submit_timesheet(rid, self.email)
        self.assertTrue(submitted.success, submitted.error.message if submitted.error else submitted)
        self.assertEqual(self._status(rid)['status'], 'SUBMITTED')

    def test_unlock_does_not_touch_submitted_list(self):
        res = tp.admin_unlock_entry(self.email, self.month, self.year, ADMIN)
        rid = res.data['report_id']
        tp.submit_timesheet(rid, self.email)  # -> SUBMITTED
        again = tp.admin_unlock_entry(self.email, self.month, self.year, ADMIN)
        self.assertFalse(again.success)
        self.assertEqual(again.error.error_type, tp.TimesheetErrorType.VALIDATION_ERROR)

    def test_unknown_employee_fails(self):
        res = tp.admin_unlock_entry('nepostojeci@example.com', self.month, self.year, ADMIN)
        self.assertFalse(res.success)
        self.assertEqual(res.error.error_type, tp.TimesheetErrorType.NOT_FOUND)


if __name__ == '__main__':
    unittest.main()
