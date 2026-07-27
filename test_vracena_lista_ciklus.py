#!/usr/bin/env python3
"""End-to-end status-machine test for the return-for-revision (dopuna) cycle.

Exercises the real service functions against PostgreSQL:

    (submitted) -> admin vrati NA DOPUNU (reject) -> employee IZMENI (save)
                -> employee ponovo pošalje (submit) -> admin ODOBRI (approve)

Proves that:
  * a returned report (REJECTED) can be edited AND resubmitted even AFTER the
    calendar deadline, because the 24 h ``editable_until`` window overrides it;
  * only the owner may resubmit their own list (rule 4);
  * approval afterwards flows normally.

Skips cleanly when PostgreSQL is not reachable (e.g. CI without a DB).
"""

import os
import unittest
from datetime import datetime

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-vracena-ciklus')

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


EMP_EMAIL = 'ciklus.dopuna.test@example.com'
EMP_NAME = 'Циклус Допуна Тест'
ADMIN_EMAIL = 'admin.ciklus.test@example.com'
OTHER_EMAIL = 'tudja.lista.test@example.com'


@unittest.skipUnless(_pg_available(), 'PostgreSQL nije dostupan')
class VracenaListaCiklusTests(unittest.TestCase):
    def setUp(self):
        # Prethodni mesec — tako da je van roka za unos "danas", što je upravo
        # uslov pod kojim se bug ispoljava.
        self.month, self.year = tp.default_entry_period()
        self._cleanup()
        self.report_id = self._seed_submitted_report()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM timesheet_reports "
                    "WHERE employee_email = %s AND month = %s AND year = %s",
                    (EMP_EMAIL, self.month, self.year),
                )
                conn.commit()

    def _seed_submitted_report(self):
        """Insert a report already SUBMITTED — the state right before a šef
        returns it for revision."""
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO timesheet_reports "
                    "(employee_name, employee_email, month, year, "
                    " organization_unit, position, special_tasks, status, "
                    " submitted_at, is_locked) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, 'SUBMITTED', NOW(), FALSE) "
                    "RETURNING id",
                    (EMP_NAME, EMP_EMAIL, self.month, self.year,
                     'Природњачки музеј', 'Запослени', 'почетни послови'),
                )
                report_id = cur.fetchone()['id']
                conn.commit()
                return report_id

    def _status(self):
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT status, rejection_note, editable_until, "
                    "(editable_until IS NOT NULL AND NOW() < editable_until) AS window_active "
                    "FROM timesheet_reports WHERE id = %s",
                    (self.report_id,),
                )
                return cur.fetchone()

    def test_full_return_for_revision_cycle(self):
        # 1) Admin vraća NA DOPUNU.
        res = tp.reject_timesheet(self.report_id, ADMIN_EMAIL, 'Допуни дане 15. и 16.')
        self.assertTrue(res.success, (res.error.message if res.error else res))
        row = self._status()
        self.assertEqual(row['status'], 'REJECTED')
        self.assertEqual(row['rejection_note'], 'Допуни дане 15. и 16.')
        self.assertTrue(row['window_active'], 'reject mora otvoriti 24h prozor')

        # 2) Zaposleni IZMENI listu — mora proći uprkos isteklom roku
        #    (prozor override-uje rok). Ovo je jezgro popravke.
        edit = tp.save_timesheet_to_postgres(
            user_name=EMP_NAME,
            user_email=EMP_EMAIL,
            month=self.month,
            year=self.year,
            daily_data={'15': {'rad_na_mestu': 8}, '16': {'rad_na_mestu': 8}},
            work_description='допуњени послови',
            organization_unit='Природњачки музеј',
            position='Запослени',
        )
        self.assertTrue(edit.success, (edit.error.message if edit.error else edit))

        # 3) Prava: TUĐU listu ne sme da pošalje niko osim vlasnika.
        wrong = tp.submit_timesheet(self.report_id, OTHER_EMAIL)
        self.assertFalse(wrong.success)
        self.assertEqual(wrong.error.error_type, tp.TimesheetErrorType.PERMISSION_DENIED)

        # 4) Vlasnik ponovo POŠALJE — prolazi zbog aktivnog prozora.
        resubmit = tp.submit_timesheet(self.report_id, EMP_EMAIL)
        self.assertTrue(resubmit.success, (resubmit.error.message if resubmit.error else resubmit))
        self.assertEqual(self._status()['status'], 'SUBMITTED')

        # 5) Odobrenje prolazi normalno.
        approve = tp.approve_timesheet(self.report_id, ADMIN_EMAIL)
        self.assertTrue(approve.success, (approve.error.message if approve.error else approve))
        self.assertEqual(self._status()['status'], 'APPROVED')


if __name__ == '__main__':
    unittest.main()
