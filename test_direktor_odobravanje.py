#!/usr/bin/env python3
"""Regression: the DIRECTOR must be able to approve/return regular employees'
timesheets (second signature). Prod bug: approval/return gates still used the
old single-verifier policy (can_user_verify_report_for_department), which blocks
the director for regular employees in headed departments — so the director saw
no approve buttons and reject 403'd.

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
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-direktor')
os.environ.setdefault('WTF_CSRF_ENABLED', 'False')

import app as museum_app
import timesheet_postgres as tp
import timesheet_admin_views as tav

DEPT = 'Биологија-дир-тест'
HEAD = 'sef.bio.dir@example.com'
DIRECTOR = 'slavko.spasic@example.com'
EMP_EMAIL = 'direktor.reg@example.com'
EMP_NAME = 'Регуларни Запослени'


def _pg_available():
    try:
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT 1')
                cur.fetchone()
        return True
    except Exception:
        return False


class SignGatePolicyTests(unittest.TestCase):
    """Root cause: the sign gate for a regular employee in a headed dept must
    ALLOW the director (new two-signature rule), where the old verify policy
    denied them."""

    def _sess(self, role, email, is_head=False, dept=None):
        return {'user_role': role, 'user_email': email,
                'is_department_head': is_head, 'user_department': dept or ''}

    def test_signature_plan_allows_director_for_regular_employee(self):
        plan = tav._signature_plan(self._sess('direktor', DIRECTOR), DEPT, EMP_EMAIL,
                                   {DEPT: HEAD})
        self.assertTrue(plan['allowed'])
        self.assertEqual(plan['slot'], 'director')

    def test_old_verify_policy_denied_director_documents_bug(self):
        # The stale policy that caused the prod bug denies the director here.
        self.assertFalse(tav.can_user_verify_report_for_department(
            self._sess('direktor', DIRECTOR), DEPT,
            target_employee_email=EMP_EMAIL, department_heads={DEPT: HEAD}))

    def test_sign_gate_allows_director_and_head_denies_stranger(self):
        can_sign = tav.can_user_sign_report_for_department
        self.assertTrue(can_sign(self._sess('direktor', DIRECTOR), DEPT,
                                 target_employee_email=EMP_EMAIL, department_heads={DEPT: HEAD}))
        self.assertTrue(can_sign(self._sess('sef_odeljenja', HEAD, is_head=True, dept=DEPT),
                                 DEPT, target_employee_email=EMP_EMAIL, department_heads={DEPT: HEAD}))
        # A head of another department cannot sign.
        self.assertFalse(can_sign(self._sess('sef_odeljenja', 'other@x', is_head=True, dept='Друго'),
                                  DEPT, target_employee_email=EMP_EMAIL, department_heads={DEPT: HEAD}))


@unittest.skipUnless(_pg_available(), 'PostgreSQL nije dostupan')
class DirectorRejectRouteTests(unittest.TestCase):
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
                    "VALUES (%s, %s, %s, %s, FALSE)", (EMP_NAME, EMP_EMAIL, 'Кустос', DEPT))
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
                cur.execute("SELECT COALESCE(status,'DRAFT') AS status FROM timesheet_reports WHERE id=%s",
                            (self.report_id,))
                return cur.fetchone()['status']

    def _login_director(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_email'] = DIRECTOR
            sess['user_name'] = 'Славко Спасић'
            sess['user_role'] = 'direktor'
            sess['is_admin'] = False
            sess['is_department_head'] = False
            sess['user_department'] = 'ДИРЕКТОР'

    def test_director_can_return_regular_employee_to_revision(self):
        self._login_director()
        with patch.object(tav, '_get_department_heads', return_value={DEPT: HEAD}):
            resp = self.client.post(
                f'/api/timesheet/{self.report_id}/reject',
                json={'note': 'Допуни дане 15. и 16.'}, base_url=self.base_url)
        self.assertEqual(resp.status_code, 200,
                         f'директор мора моћи да врати листу; body={resp.get_json()}')
        self.assertEqual(self._status(), 'REJECTED')


if __name__ == '__main__':
    unittest.main()
