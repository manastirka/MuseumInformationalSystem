#!/usr/bin/env python3
"""Route-level tests for admin unlock of timesheet entry.

Rights: only admin/direktor may unlock (non-admin → 403). Effect: after an
admin unlocks, the chosen employee's old month becomes editable+submittable;
another (not-unlocked) month stays closed. Skips without PostgreSQL.
"""

import os
import unittest
from datetime import datetime

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-unlock-route')
os.environ.setdefault('WTF_CSRF_ENABLED', 'False')

import app as museum_app
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
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT email, full_name FROM users "
                        "WHERE full_name IS NOT NULL AND email IS NOT NULL "
                        "ORDER BY id LIMIT 1")
            return cur.fetchone()


@unittest.skipUnless(_pg_available(), 'PostgreSQL nije dostupan')
class AdminUnlockRouteTests(unittest.TestCase):
    def setUp(self):
        # Neki testovi (test_csrf.py) ostavljaju CSRF uključen globalno; forsiraj
        # ga OFF ovde da POST rute nisu zavisne od redosleda izvršavanja.
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'
        emp = _real_employee()
        self.email = emp['email']
        now = datetime.now()
        idx = now.year * 12 + (now.month - 1) - 5
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

    def _login(self, role='admin', email='admin@example.com'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = email
            sess['user_name'] = 'Admin'
            sess['user_role'] = role
            sess['is_admin'] = role == 'admin'

    def _payload(self):
        return {'employee_email': self.email, 'from_month': self.month,
                'from_year': self.year}

    def test_non_admin_cannot_unlock(self):
        self._login(role='employee')
        resp = self.client.post('/api/admin/timesheet/unlock', json=self._payload(), base_url=self.base_url)
        self.assertEqual(resp.status_code, 403)

    def test_admin_unlock_enables_that_user_old_month(self):
        self._login(role='admin')
        resp = self.client.post('/api/admin/timesheet/unlock', json=self._payload(), base_url=self.base_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.get_json()['success'])

        # The unlocked employee can now save + submit the old month.
        emp = _real_employee()
        saved = tp.save_timesheet_to_postgres(
            user_email=self.email, user_name=emp['full_name'], month=self.month,
            year=self.year, daily_data={'10': {'rad_na_mestu': 8}},
            work_description='x', organization_unit='X', position='Y')
        self.assertTrue(saved.success, saved.error.message if saved.error else saved)

    def test_director_can_unlock_parity(self):
        self._login(role='direktor')
        resp = self.client.post('/api/admin/timesheet/unlock', json=self._payload(), base_url=self.base_url)
        self.assertEqual(resp.status_code, 200)

    def test_other_month_stays_closed_for_same_user(self):
        """Unlock ne sme da otvori DRUGI mesec koji nije otključan."""
        self._login(role='admin')
        self.client.post('/api/admin/timesheet/unlock', json=self._payload(), base_url=self.base_url)
        # A different, not-unlocked old month must still be blocked.
        other_idx = self.year * 12 + (self.month - 1) - 1
        oy, om = other_idx // 12, other_idx % 12 + 1
        emp = _real_employee()
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM timesheet_reports WHERE employee_email=%s "
                            "AND month=%s AND year=%s", (self.email, om, oy))
                conn.commit()
        blocked = tp.save_timesheet_to_postgres(
            user_email=self.email, user_name=emp['full_name'], month=om, year=oy,
            daily_data={'10': {'rad_na_mestu': 8}}, work_description='x',
            organization_unit='X', position='Y')
        self.assertFalse(blocked.success, 'neotključan mesec mora ostati zatvoren')
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM timesheet_reports WHERE employee_email=%s "
                            "AND month=%s AND year=%s", (self.email, om, oy))
                conn.commit()

    def test_unlock_page_renders_for_admin(self):
        self._login(role='admin')
        resp = self.client.get('/admin/timesheet/otkljucaj-unos', base_url=self.base_url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('unlock-submit', resp.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
