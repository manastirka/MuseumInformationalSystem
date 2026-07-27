#!/usr/bin/env python3
"""Two-signature approval: a report is APPROVED only when BOTH the department
head and the director have confirmed. One signature keeps it SUBMITTED; return
to revision resets both signatures.

Covers the pure signature-plan routing (no DB) and the DB status machine
(confirm_timesheet_signature + reject_timesheet reset). DB parts skip without PG.
"""

import os
import unittest
from datetime import datetime

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-2sig')

import timesheet_postgres as tp
from timesheet_admin_views import _signature_plan


# ---------------------------------------------------------------------------
# Pure routing of the signature plan (no DB)
# ---------------------------------------------------------------------------
DEPT = 'Биологија'
HEAD = 'sef.bio@nhmbeo.rs'
DIRECTOR = 'direktor@nhmbeo.rs'
EMPLOYEE = 'zaposleni@nhmbeo.rs'
HEADS = {DEPT: HEAD}


def _sess(role, email, is_head=False, dept=DEPT):
    return {'user_role': role, 'user_email': email,
            'is_department_head': is_head, 'user_department': dept}


class SignaturePlanTests(unittest.TestCase):
    def test_head_signs_head_slot_for_regular_employee(self):
        plan = _signature_plan(_sess('sef_odeljenja', HEAD, is_head=True),
                               DEPT, EMPLOYEE, HEADS)
        self.assertTrue(plan['allowed'])
        self.assertEqual(plan['slot'], 'head')
        self.assertTrue(plan['head_required'])

    def test_director_signs_director_slot_for_regular_employee(self):
        plan = _signature_plan(_sess('direktor', DIRECTOR), DEPT, EMPLOYEE, HEADS)
        self.assertTrue(plan['allowed'])
        self.assertEqual(plan['slot'], 'director')
        self.assertTrue(plan['head_required'])

    def test_admin_fills_both(self):
        plan = _signature_plan(_sess('admin', 'admin@nhmbeo.rs'), DEPT, EMPLOYEE, HEADS)
        self.assertEqual(plan['slot'], 'both')

    def test_headless_department_needs_only_director(self):
        plan = _signature_plan(_sess('direktor', DIRECTOR), 'Едукација', EMPLOYEE, {})
        self.assertTrue(plan['allowed'])
        self.assertEqual(plan['slot'], 'director')
        self.assertFalse(plan['head_required'])

    def test_head_own_report_needs_only_director(self):
        # Report belongs to the head themselves → head not required, director signs.
        plan = _signature_plan(_sess('direktor', DIRECTOR), DEPT, HEAD, HEADS)
        self.assertFalse(plan['head_required'])
        self.assertEqual(plan['slot'], 'director')

    def test_same_person_head_and_director_fills_both(self):
        # A person who is BOTH the department head and the director: one
        # confirmation fills both slots (cannot sign twice).
        plan = _signature_plan(
            _sess('direktor', HEAD, is_head=True), DEPT, EMPLOYEE, HEADS)
        self.assertEqual(plan['slot'], 'both')

    def test_director_cannot_sign_own_report(self):
        plan = _signature_plan(_sess('direktor', DIRECTOR), 'Едукација', DIRECTOR, {})
        self.assertFalse(plan['allowed'])

    def test_regular_user_denied(self):
        plan = _signature_plan(_sess('employee', EMPLOYEE), DEPT, EMPLOYEE, HEADS)
        self.assertFalse(plan['allowed'])


# ---------------------------------------------------------------------------
# DB status machine
# ---------------------------------------------------------------------------
def _pg_available():
    try:
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT 1')
                cur.fetchone()
        return True
    except Exception:
        return False


EMP_EMAIL = 'dvostepeno.test@example.com'
EMP_NAME = 'Двостепени Тест'


@unittest.skipUnless(_pg_available(), 'PostgreSQL nije dostupan')
class TwoSignatureStatusMachineTests(unittest.TestCase):
    def setUp(self):
        now = datetime.now()
        idx = now.year * 12 + (now.month - 1) - 2
        self.year, self.month = idx // 12, idx % 12 + 1
        self._cleanup()
        self.report_id = self._seed_submitted()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM timesheet_reports WHERE employee_email=%s "
                            "AND month=%s AND year=%s", (EMP_EMAIL, self.month, self.year))
                conn.commit()

    def _seed_submitted(self):
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO timesheet_reports "
                    "(employee_name, employee_email, month, year, status, is_locked) "
                    "VALUES (%s, %s, %s, %s, 'SUBMITTED', TRUE) RETURNING id",
                    (EMP_NAME, EMP_EMAIL, self.month, self.year))
                rid = cur.fetchone()['id']
                conn.commit()
                return rid

    def _row(self):
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COALESCE(status,'DRAFT') AS status, head_verified_by, "
                            "director_verified_by, is_verified FROM timesheet_reports WHERE id=%s",
                            (self.report_id,))
                return cur.fetchone()

    def test_one_signature_is_not_approved(self):
        r = tp.confirm_timesheet_signature(self.report_id, HEAD, 'head', head_required=True)
        self.assertTrue(r.success)
        self.assertFalse(r.data['approved'])
        row = self._row()
        self.assertEqual(row['status'], 'SUBMITTED')
        self.assertEqual(row['head_verified_by'], HEAD)
        self.assertIsNone(row['director_verified_by'])
        self.assertFalse(row['is_verified'])

    def test_both_signatures_approve(self):
        tp.confirm_timesheet_signature(self.report_id, HEAD, 'head', head_required=True)
        r = tp.confirm_timesheet_signature(self.report_id, DIRECTOR, 'director', head_required=True)
        self.assertTrue(r.success)
        self.assertTrue(r.data['approved'])
        row = self._row()
        self.assertEqual(row['status'], 'APPROVED')
        self.assertEqual(row['head_verified_by'], HEAD)
        self.assertEqual(row['director_verified_by'], DIRECTOR)
        self.assertTrue(row['is_verified'])

    def test_director_first_then_head_also_approves(self):
        tp.confirm_timesheet_signature(self.report_id, DIRECTOR, 'director', head_required=True)
        self.assertEqual(self._row()['status'], 'SUBMITTED')  # still waiting for head
        r = tp.confirm_timesheet_signature(self.report_id, HEAD, 'head', head_required=True)
        self.assertTrue(r.data['approved'])
        self.assertEqual(self._row()['status'], 'APPROVED')

    def test_headless_director_alone_approves(self):
        r = tp.confirm_timesheet_signature(self.report_id, DIRECTOR, 'director', head_required=False)
        self.assertTrue(r.data['approved'])
        self.assertEqual(self._row()['status'], 'APPROVED')

    def test_admin_both_slot_approves(self):
        r = tp.confirm_timesheet_signature(self.report_id, 'admin@x', 'both', head_required=True)
        self.assertTrue(r.data['approved'])
        self.assertEqual(self._row()['status'], 'APPROVED')

    def test_return_to_revision_resets_signatures(self):
        tp.confirm_timesheet_signature(self.report_id, HEAD, 'head', head_required=True)
        rej = tp.reject_timesheet(self.report_id, DIRECTOR, 'Допуни дане')
        self.assertTrue(rej.success)
        row = self._row()
        self.assertEqual(row['status'], 'REJECTED')
        self.assertIsNone(row['head_verified_by'])
        self.assertIsNone(row['director_verified_by'])

    def test_cannot_sign_non_submitted(self):
        tp.confirm_timesheet_signature(self.report_id, 'admin@x', 'both', head_required=True)
        # now APPROVED — another signature must fail
        r = tp.confirm_timesheet_signature(self.report_id, HEAD, 'head', head_required=True)
        self.assertFalse(r.success)


if __name__ == '__main__':
    unittest.main()
