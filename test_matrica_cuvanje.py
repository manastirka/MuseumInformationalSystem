#!/usr/bin/env python3
"""Regression: the attendance matrix (timesheet_report_days) must persist.

Prod bug: the entry form never loaded existing day data into the matrix inputs
(gated to view mode only), so a re-save sent an empty matrix and the existing-
report save path DELETEd all days and reinserted none — silently wiping data
while returning success. Fixed by (a) loading data into the entry form and
(b) refusing to silently wipe an already-populated list from an empty form.

Skips without PostgreSQL.
"""

import os
import unittest
from datetime import datetime

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-matrica')

import timesheet_postgres as tp
import timesheet_employee_views as ev


def _pg_available():
    try:
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT 1')
                cur.fetchone()
        return True
    except Exception:
        return False


EMAIL = 'matrica.cuvanje@example.com'
NAME = 'Матрица Чување'


@unittest.skipUnless(_pg_available(), 'PostgreSQL nije dostupan')
class MatrixPersistenceTests(unittest.TestCase):
    def setUp(self):
        # Current month → within the edit window (avoids the day-10 deadline).
        now = datetime.now()
        self.month, self.year = now.month, now.year
        self._cleanup()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM timesheet_reports WHERE employee_email=%s", (EMAIL,))
                conn.commit()

    def _save(self, daily_data):
        return tp.save_timesheet_to_postgres(
            user_email=EMAIL, user_name=NAME, month=self.month, year=self.year,
            daily_data=daily_data, work_description='x',
            organization_unit='X', position='Y')

    def _day_rows(self, report_id):
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT day, work_in_museum, work_outside, sick_leave_lt30 "
                            "FROM timesheet_report_days WHERE report_id=%s ORDER BY day",
                            (report_id,))
                return cur.fetchall()

    def test_save_writes_matrix_rows(self):
        r = self._save({'5': {'rad_na_mestu': 8, 'van_muzeja': 2},
                        '10': {'bolovanje_manje_30': 8}})
        self.assertTrue(r.success, r.error.message if r.error else r)
        rows = self._day_rows(r.data['report_id'])
        self.assertEqual(len(rows), 2)
        by_day = {row['day']: row for row in rows}
        self.assertEqual(float(by_day[5]['work_in_museum']), 8.0)
        self.assertEqual(float(by_day[5]['work_outside']), 2.0)
        self.assertEqual(float(by_day[10]['sick_leave_lt30']), 8.0)

    def test_reopen_returns_daily_data(self):
        """After save, the entry-data loader returns the days so the form can
        repopulate (end-to-end: what the reopened form reads)."""
        self._save({'5': {'rad_na_mestu': 8}})
        data = ev._load_timesheet_entry_data(NAME, EMAIL, self.month, self.year)
        self.assertIsNotNone(data)
        days = {d['dan']: d for d in data['daily_data']}
        self.assertIn(5, days)
        self.assertEqual(float(days[5]['rad_na_mestu']), 8.0)

    def test_empty_resave_does_not_wipe_existing(self):
        """An empty matrix must NOT silently delete an already-populated list."""
        r = self._save({'5': {'rad_na_mestu': 8}})
        rid = r.data['report_id']
        self.assertEqual(len(self._day_rows(rid)), 1)

        wiped = self._save({})  # empty form
        self.assertFalse(wiped.success, 'prazan save NE sme da uspe tiho')
        self.assertEqual(wiped.error.error_type, tp.TimesheetErrorType.VALIDATION_ERROR)
        # Data preserved.
        self.assertEqual(len(self._day_rows(rid)), 1)

    def test_new_empty_report_is_allowed(self):
        """The guard must not block a brand-new empty report (no prior days)."""
        r = self._save({})
        self.assertTrue(r.success, r.error.message if r.error else r)


if __name__ == '__main__':
    unittest.main()
