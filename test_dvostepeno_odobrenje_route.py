#!/usr/bin/env python3
"""Route-level two-signature approval through the admin approve endpoint.

Head confirmation alone leaves the report SUBMITTED; the director's second
confirmation flips it to APPROVED. A regular employee cannot approve (403).
Skips without PostgreSQL.
"""

import os
import unittest
from datetime import datetime
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-2sig-route')
os.environ.setdefault('WTF_CSRF_ENABLED', 'False')

import app as museum_app
import timesheet_postgres as tp
import timesheet_admin_views as tav

DEPT = 'Биологија-тест'
HEAD = 'sef.bio.test@example.com'
DIRECTOR = 'direktor.test@example.com'
EMP_EMAIL = 'dvostepeno.route@example.com'
EMP_NAME = 'Двостепени Роут'


def _pg_available():
    try:
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT 1')
                cur.fetchone()
        return True
    except Exception:
        return False


@unittest.skipUnless(_pg_available(), 'PostgreSQL nije dostupan')
class TwoSignatureRouteTests(unittest.TestCase):
    def setUp(self):
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'
        now = datetime.now()
        idx = now.year * 12 + (now.month - 1) - 2
        self.year, self.month = idx // 12, idx % 12 + 1
        self._cleanup()
        self.report_id = self._seed()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM timesheet_reports WHERE employee_email=%s "
                            "AND month=%s AND year=%s", (EMP_EMAIL, self.month, self.year))
                cur.execute("DELETE FROM employee_profiles WHERE email=%s", (EMP_EMAIL,))
                conn.commit()

    def _seed(self):
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO employee_profiles (full_name, email, position, department, is_department_head) "
                    "VALUES (%s, %s, %s, %s, FALSE)",
                    (EMP_NAME, EMP_EMAIL, 'Кустос', DEPT))
                cur.execute(
                    "INSERT INTO timesheet_reports "
                    "(employee_name, employee_email, month, year, status, is_locked) "
                    "VALUES (%s, %s, %s, %s, 'SUBMITTED', TRUE) RETURNING id",
                    (EMP_NAME, EMP_EMAIL, self.month, self.year))
                rid = cur.fetchone()['id']
                conn.commit()
                return rid

    def _status(self):
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COALESCE(status,'DRAFT') AS status, head_verified_by, "
                            "director_verified_by FROM timesheet_reports WHERE id=%s",
                            (self.report_id,))
                return cur.fetchone()

    def _login(self, role, email, is_head=False, dept=None):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = email
            sess['user_name'] = email
            sess['user_role'] = role
            sess['is_admin'] = role == 'admin'
            sess['is_department_head'] = is_head
            sess['user_department'] = dept or ''

    def _approve(self):
        return self.client.post(
            f'/api/admin/timesheet/report/{self.report_id}/approve',
            json={'approve': True}, base_url=self.base_url)

    def test_head_then_director_two_step(self):
        with patch.object(tav, '_get_department_heads', return_value={DEPT: HEAD}):
            # 1) Head signs → still SUBMITTED (one signature).
            self._login('sef_odeljenja', HEAD, is_head=True, dept=DEPT)
            r1 = self._approve()
            self.assertEqual(r1.status_code, 200)
            self.assertFalse(r1.get_json().get('approved'))
            row = self._status()
            self.assertEqual(row['status'], 'SUBMITTED')
            self.assertEqual(row['head_verified_by'], HEAD)
            self.assertIsNone(row['director_verified_by'])

            # 2) Director signs → APPROVED (both signatures).
            self._login('direktor', DIRECTOR)
            r2 = self._approve()
            self.assertEqual(r2.status_code, 200)
            self.assertTrue(r2.get_json().get('approved'))
            self.assertEqual(self._status()['status'], 'APPROVED')

    def test_director_alone_does_not_approve_headed_dept(self):
        with patch.object(tav, '_get_department_heads', return_value={DEPT: HEAD}):
            self._login('direktor', DIRECTOR)
            r = self._approve()
            self.assertEqual(r.status_code, 200)
            self.assertFalse(r.get_json().get('approved'))
            self.assertEqual(self._status()['status'], 'SUBMITTED')

    def test_admin_single_call_approves(self):
        self._login('admin', 'admin@example.com')
        r = self._approve()
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.get_json().get('approved'))
        self.assertEqual(self._status()['status'], 'APPROVED')

    def test_regular_employee_forbidden(self):
        self._login('employee', 'emp@example.com')
        r = self._approve()
        self.assertEqual(r.status_code, 403)


if __name__ == '__main__':
    unittest.main()
