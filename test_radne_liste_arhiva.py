#!/usr/bin/env python3
"""Separation of current vs archived timesheet reports in the admin view.

CURRENT view = manually-entered reports of the current year
(imported_from IS NULL AND year = current_year). ARCHIVE = everything else
(imported archival rows OR other years). Nothing is deleted — only the display
is split. Employees keep access to their own history via year selection.

Skips without PostgreSQL.
"""

import os
import unittest
from datetime import datetime

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-arhiva')

import timesheet_postgres as tp
from timesheet_repository import TimesheetRepository


def _pg_available():
    try:
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT 1')
                cur.fetchone()
        return True
    except Exception:
        return False


EMP_EMAIL = 'arhiva.test@example.com'
EMP_NAME = 'Архива Тест'


@unittest.skipUnless(_pg_available(), 'PostgreSQL nije dostupan')
class ArchiveSeparationTests(unittest.TestCase):
    def setUp(self):
        self.current_year = datetime.now().year
        self.repo = TimesheetRepository(tp.DATABASE_URL)
        self.assertTrue(self.repo.available)
        self._cleanup()
        # An imported ARCHIVAL list from 2015.
        self.archive_id = self._seed(month=6, year=2015, imported='word-arhiva')
        # A fresh manually-entered current-year list (June of current year).
        self.current_id = self._seed(month=6, year=self.current_year, imported=None)

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM timesheet_reports WHERE employee_email=%s", (EMP_EMAIL,))
                conn.commit()

    def _seed(self, month, year, imported):
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO timesheet_reports "
                    "(employee_name, employee_email, month, year, status, imported_from) "
                    "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    (EMP_NAME, EMP_EMAIL, month, year,
                     'APPROVED' if imported else 'SUBMITTED', imported))
                rid = cur.fetchone()['id']
                conn.commit()
                return rid

    def _ids(self, scope, **kw):
        res = self.repo.list_reports(page=1, per_page=1000, scope=scope,
                                     current_year=self.current_year, search=EMP_NAME, **kw)
        return {r['id'] for r in res['reports']}

    def test_imported_2015_not_in_current_view(self):
        current = self._ids('current')
        self.assertIn(self.current_id, current, 'нова листа текуће године мора бити у текућем прегледу')
        self.assertNotIn(self.archive_id, current, 'увезена архивска листа не сме у текући преглед')

    def test_imported_2015_is_in_archive(self):
        archive = self._ids('archive')
        self.assertIn(self.archive_id, archive, 'увезена архивска листа мора бити у архиви')
        self.assertNotIn(self.current_id, archive, 'текућа листа не сме у архиву')

    def test_archive_year_filter(self):
        # Filtering the archive by 2015 shows the 2015 list.
        self.assertIn(self.archive_id, self._ids('archive', year=2015))

    def test_new_june_current_year_in_current_view(self):
        self.assertIn(self.current_id, self._ids('current'))

    def test_current_view_ignores_user_year_param(self):
        # In current scope, a user-supplied year is ignored (pinned to current).
        current = self._ids('current', year=2015)
        self.assertIn(self.current_id, current)
        self.assertNotIn(self.archive_id, current)

    def test_employee_can_still_reach_2015_by_year(self):
        """Employee history is not lost: their own read-only loader finds the
        2015 report when they select that month/year."""
        import timesheet_employee_views as ev
        data = ev._load_timesheet_view_data(EMP_NAME, 6, 2015)
        self.assertIsNotNone(data, 'запослени мора да нађе своју листу из 2015 по избору године')
        self.assertTrue(data.get('exists'))

    def test_nothing_deleted(self):
        """Both rows still exist in the DB regardless of view separation."""
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) AS n FROM timesheet_reports WHERE employee_email=%s",
                            (EMP_EMAIL,))
                self.assertEqual(cur.fetchone()['n'], 2)


if __name__ == '__main__':
    unittest.main()
