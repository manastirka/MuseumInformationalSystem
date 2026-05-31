#!/usr/bin/env python3
"""Regression tests for department-head-scoped timesheet verification.

Business rule: a non-admin user flagged `is_department_head=True` in
employee_profiles must be able to view and verify timesheet reports for
employees in their own department only. Admins keep full access. Regular
employees remain blocked.
"""

import os
import unittest
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

import app as museum_app
import timesheet_admin_views


GEOLOGY = 'ГЕОЛОШКО ОДЕЉЕЊЕ'
BIOLOGY = 'БИОЛОШКО ОДЕЉЕЊЕ'
LEGAL_AFFAIRS = 'ОДСЕК ОПШТИХ И ПРАВНИХ ПОСЛОВА'
FINANCE = 'ГРУПА ЗА ФИНАНСИЈСКО-РАЧУНОВОДСТВЕНЕ ПОСЛОВЕ'


class _FakeCursor:
    """Minimal cursor that returns canned rows and records UPDATEs."""

    def __init__(self, canned):
        self._canned = canned
        self._pending = None
        self.executed = []

    def execute(self, sql, params=None):
        self.executed.append((sql, params))
        for needle, row in self._canned.items():
            if needle in sql:
                self._pending = row
                return
        self._pending = None

    def fetchone(self):
        value = self._pending
        if isinstance(value, list):
            return value[0] if value else None
        return value

    def fetchall(self):
        value = self._pending
        if isinstance(value, list):
            return value
        return [value] if value else []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class _FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor
        self.commits = 0

    def cursor(self):
        return self._cursor

    def commit(self):
        self.commits += 1

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


@contextmanager
def _fake_pg_connection_ctx(cursor):
    conn = _FakeConnection(cursor)
    yield conn


class _CombinedPatch:
    """Enter/exit multiple unittest.mock patch objects as one context."""

    def __init__(self, *patches):
        self._patches = patches

    def __enter__(self):
        for p in self._patches:
            p.start()
        return self

    def __exit__(self, *exc):
        for p in reversed(self._patches):
            p.stop()
        return False


class DepartmentHeadAuthTests(unittest.TestCase):
    """Route-level tests that assert the new decorator + scope rules."""

    def setUp(self):
        # A sibling test (test_image_api_security.py::setUpClass) globally
        # enables CSRF and never resets it. Force it off for this test class
        # so POSTs to the approve endpoints reach the view regardless of
        # previous-test ordering.
        self._prev_csrf = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def tearDown(self):
        museum_app.app.config['WTF_CSRF_ENABLED'] = self._prev_csrf

    def _login_as_department_head(self, *, department=GEOLOGY):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 17
            sess['user_email'] = 'biljana.mitrovic@nhmbeo.rs'
            sess['user_name'] = 'Биљана Митровић'
            sess['user_role'] = 'employee'
            sess['is_admin'] = False
            sess['user_department'] = department
            sess['is_department_head'] = True

    def _login_as_regular_employee(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 99
            sess['user_email'] = 'other.employee@nhmbeo.rs'
            sess['user_name'] = 'Other Employee'
            sess['user_role'] = 'employee'
            sess['is_admin'] = False
            sess['user_department'] = BIOLOGY
            sess['is_department_head'] = False

    def _login_as_admin(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = 'admin@nhmbeo.rs'
            sess['user_name'] = 'Admin'
            sess['user_role'] = 'admin'
            sess['is_admin'] = True
            sess['user_department'] = 'УПРАВА'
            sess['is_department_head'] = False

    # ------------------------------------------------------------------
    # /admin/timesheet_reports (list view)
    # ------------------------------------------------------------------
    def test_list_route_allows_department_head(self):
        self._login_as_department_head()

        with patch.object(
            museum_app.timesheet_admin_views,
            'render_admin_timesheet_reports',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked:
            response = self.client.get('/admin/timesheet_reports', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked.assert_called_once()

    def test_list_route_blocks_regular_employee(self):
        self._login_as_regular_employee()

        with patch.object(
            museum_app.timesheet_admin_views,
            'render_admin_timesheet_reports',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked:
            response = self.client.get('/admin/timesheet_reports', base_url=self.base_url)

        # Non-admin non-dept-head must not reach the view.
        self.assertNotEqual(response.status_code, 200)
        mocked.assert_not_called()

    def test_list_route_still_allows_admin(self):
        self._login_as_admin()

        with patch.object(
            museum_app.timesheet_admin_views,
            'render_admin_timesheet_reports',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked:
            response = self.client.get('/admin/timesheet_reports', base_url=self.base_url)

        self.assertEqual(response.status_code, 200)
        mocked.assert_called_once()

    # ------------------------------------------------------------------
    # Approve endpoint
    # ------------------------------------------------------------------
    def _patched_pg(self, report_row):
        """Patch the repository availability probe and the Postgres connection
        so the approve endpoint can be tested without a live database.

        Other tests in the suite occasionally leave
        `museum_app.timesheet_repository.available == False`; we patch the
        module-level availability check so these tests stay deterministic in
        a full-suite run.
        """
        cursor = _FakeCursor({
            'FROM timesheet_reports tr': report_row,
            'FROM users WHERE full_name': None,  # no notify user
        })

        pg_patch = patch.object(
            timesheet_admin_views,
            'get_postgres_connection',
            lambda **kwargs: _fake_pg_connection_ctx(cursor),
        )
        repo_patch = patch.object(
            timesheet_admin_views,
            '_timesheet_repository_available',
            return_value=True,
        )

        combined = _CombinedPatch(pg_patch, repo_patch)
        return combined, cursor

    def test_approve_endpoint_allows_department_head_for_own_department(self):
        self._login_as_department_head()

        report_row = {
            'id': 42,
            'employee_name': 'Геолог Један',
            'employee_department': GEOLOGY,
            'month': 1,
            'year': 2026,
        }
        patcher, cursor = self._patched_pg(report_row)
        with patcher:
            response = self.client.post(
                '/api/admin/timesheet/report/42/approve',
                json={'approve': True},
                base_url=self.base_url,
            )

        body = response.get_json()
        self.assertEqual(
            response.status_code, 200,
            f"expected 200, got {response.status_code}; json={body}; data={response.data[:500]!r}",
        )
        self.assertTrue(body.get('success'), f"expected success, got {body}")

    def test_approve_endpoint_blocks_department_head_for_other_department(self):
        self._login_as_department_head(department=GEOLOGY)

        report_row = {
            'id': 43,
            'employee_name': 'Биолог Један',
            'employee_department': BIOLOGY,
            'month': 1,
            'year': 2026,
        }
        patcher, _ = self._patched_pg(report_row)
        with patcher:
            response = self.client.post(
                '/api/admin/timesheet/report/43/approve',
                json={'approve': True},
                base_url=self.base_url,
            )

        self.assertEqual(response.status_code, 403)

    def test_approve_endpoint_blocks_regular_employee(self):
        self._login_as_regular_employee()

        response = self.client.post(
            '/api/admin/timesheet/report/42/approve',
            json={'approve': True},
            base_url=self.base_url,
        )

        self.assertNotEqual(response.status_code, 200)


class DepartmentScopingHelperTests(unittest.TestCase):
    """Pure-unit tests for the authorization helper."""

    def test_admin_can_act_on_any_department(self):
        from timesheet_admin_views import can_user_verify_report_for_department

        session = {'user_role': 'admin', 'is_department_head': False, 'user_department': 'X'}
        self.assertTrue(can_user_verify_report_for_department(session, BIOLOGY))
        self.assertTrue(can_user_verify_report_for_department(session, GEOLOGY))

    def test_department_head_can_act_only_on_own_department(self):
        from timesheet_admin_views import can_user_verify_report_for_department

        session = {
            'user_role': 'employee',
            'is_department_head': True,
            'user_department': GEOLOGY,
        }
        self.assertTrue(can_user_verify_report_for_department(
            session, GEOLOGY, target_employee_email='employee@x'))
        self.assertFalse(can_user_verify_report_for_department(session, BIOLOGY))

    def test_regular_employee_cannot_act(self):
        from timesheet_admin_views import can_user_verify_report_for_department

        session = {
            'user_role': 'employee',
            'is_department_head': False,
            'user_department': GEOLOGY,
        }
        self.assertFalse(can_user_verify_report_for_department(session, GEOLOGY))

    def test_legal_affairs_head_scoped_to_own_dept(self):
        """ana.zivanovic (sef_pravne_sluzbe) verifies only Legal Affairs."""
        from timesheet_admin_views import can_user_verify_report_for_department
        session = {
            'user_role': 'sef_pravne_sluzbe',
            'is_department_head': True,
            'user_department': LEGAL_AFFAIRS,
        }
        self.assertTrue(can_user_verify_report_for_department(
            session, LEGAL_AFFAIRS, target_employee_email='employee@x'))
        self.assertFalse(can_user_verify_report_for_department(session, GEOLOGY))
        self.assertFalse(can_user_verify_report_for_department(session, FINANCE))

    def test_accounting_head_scoped_to_own_dept(self):
        """dusica.ivic (sef_racunovodstva) verifies only Finance group."""
        from timesheet_admin_views import can_user_verify_report_for_department
        session = {
            'user_role': 'sef_racunovodstva',
            'is_department_head': True,
            'user_department': FINANCE,
        }
        self.assertTrue(can_user_verify_report_for_department(
            session, FINANCE, target_employee_email='employee@x'))
        self.assertFalse(can_user_verify_report_for_department(session, LEGAL_AFFAIRS))
        self.assertFalse(can_user_verify_report_for_department(session, BIOLOGY))


class DepartmentHeadSelfApprovalTests(unittest.TestCase):
    """A department head must not approve their own timesheet report —
    conflict of interest. The director signs off head reports instead.
    """

    def test_head_cannot_self_approve_by_email_match(self):
        from timesheet_admin_views import can_user_verify_report_for_department
        biljana = {
            'user_role': 'sef_odeljenja',
            'is_department_head': True,
            'user_department': GEOLOGY,
            'user_email': 'biljana.mitrovic@nhmbeo.rs',
        }
        # Her own report in her own dept
        self.assertFalse(can_user_verify_report_for_department(
            biljana, GEOLOGY,
            target_employee_email='biljana.mitrovic@nhmbeo.rs',
            department_heads={GEOLOGY: 'biljana.mitrovic@nhmbeo.rs'},
        ))

    def test_head_cannot_self_approve_case_mismatch(self):
        from timesheet_admin_views import can_user_verify_report_for_department
        biljana = {
            'user_role': 'sef_odeljenja',
            'is_department_head': True,
            'user_department': GEOLOGY,
            'user_email': 'Biljana.Mitrovic@NHMBEO.RS',  # case-mixed
        }
        self.assertFalse(can_user_verify_report_for_department(
            biljana, GEOLOGY,
            target_employee_email='biljana.mitrovic@nhmbeo.rs',
            department_heads={GEOLOGY: 'biljana.mitrovic@nhmbeo.rs'},
        ))

    def test_head_cannot_self_approve_when_email_is_null_via_heads_fallback(self):
        """If employee_email is NULL on the report, fall back to checking
        the heads mapping so a head still can't self-approve."""
        from timesheet_admin_views import can_user_verify_report_for_department
        biljana = {
            'user_role': 'sef_odeljenja',
            'is_department_head': True,
            'user_department': GEOLOGY,
            'user_email': 'biljana.mitrovic@nhmbeo.rs',
        }
        self.assertFalse(can_user_verify_report_for_department(
            biljana, GEOLOGY,
            target_employee_email=None,
            department_heads={GEOLOGY: 'biljana.mitrovic@nhmbeo.rs'},
        ))

    def test_head_can_approve_other_employee_same_department(self):
        """Self-approval guard doesn't touch the normal case — approving
        a subordinate's report in the same department."""
        from timesheet_admin_views import can_user_verify_report_for_department
        biljana = {
            'user_role': 'sef_odeljenja',
            'is_department_head': True,
            'user_department': GEOLOGY,
            'user_email': 'biljana.mitrovic@nhmbeo.rs',
        }
        self.assertTrue(can_user_verify_report_for_department(
            biljana, GEOLOGY,
            target_employee_email='aca.lukovic@nhmbeo.rs',
            department_heads={GEOLOGY: 'biljana.mitrovic@nhmbeo.rs'},
        ))


class SelfApprovalHolesRegressionTests(unittest.TestCase):
    """Self-approval must be blocked for every head regardless of role flavor
    AND regardless of whether the session still has user_email or the DB has
    the target email populated. Regression for a hole where Dusica/Ana could
    self-verify when the direct-email guard couldn't fire.
    """

    FIN = 'ГРУПА ЗА ФИНАНСИЈСКО-РАЧУНОВОДСТВЕНЕ ПОСЛОВЕ'
    LEGAL = 'ОДСЕК ОПШТИХ И ПРАВНИХ ПОСЛОВА'

    def test_sef_racunovodstva_blocked_on_stale_session(self):
        """Dusica's session is missing user_email (possible mid-deploy).
        She still must not be able to verify her own report because the
        heads-mapping guard catches it."""
        from timesheet_admin_views import can_user_verify_report_for_department
        session = {
            'user_role': 'sef_racunovodstva',
            'is_department_head': True,
            'user_department': self.FIN,
            # no user_email
        }
        heads = {self.FIN: 'dusica.ivic@nhmbeo.rs'}
        self.assertFalse(can_user_verify_report_for_department(
            session, self.FIN,
            target_employee_email='dusica.ivic@nhmbeo.rs',
            department_heads=heads,
        ))

    def test_sef_pravne_sluzbe_blocked_on_stale_session(self):
        """Same guarantee for Ana Živanović (Legal Affairs head)."""
        from timesheet_admin_views import can_user_verify_report_for_department
        session = {
            'user_role': 'sef_pravne_sluzbe',
            'is_department_head': True,
            'user_department': self.LEGAL,
        }
        heads = {self.LEGAL: 'ana.zivanovic@nhmbeo.rs'}
        self.assertFalse(can_user_verify_report_for_department(
            session, self.LEGAL,
            target_employee_email='ana.zivanovic@nhmbeo.rs',
            department_heads=heads,
        ))

    def test_head_can_still_approve_subordinate_with_stale_session(self):
        """The stricter guard must not overreach — if Dusica's session is
        stale but she's approving Milena (not herself), let her through."""
        from timesheet_admin_views import can_user_verify_report_for_department
        session = {
            'user_role': 'sef_racunovodstva',
            'is_department_head': True,
            'user_department': self.FIN,
        }
        heads = {self.FIN: 'dusica.ivic@nhmbeo.rs'}
        self.assertTrue(can_user_verify_report_for_department(
            session, self.FIN,
            target_employee_email='milenar@nhmbeo.rs',
            department_heads=heads,
        ))


class DepartmentHeadRoleMappingTests(unittest.TestCase):
    """The login handler must flag sef_odeljenja, sef_pravne_sluzbe, and
    sef_racunovodstva as department heads (drives session['is_department_head']).
    """

    def test_department_head_roles_constant(self):
        from core_app_views import DEPARTMENT_HEAD_ROLES
        self.assertIn('sef_odeljenja', DEPARTMENT_HEAD_ROLES)
        self.assertIn('sef_pravne_sluzbe', DEPARTMENT_HEAD_ROLES)
        self.assertIn('sef_racunovodstva', DEPARTMENT_HEAD_ROLES)
        # Admin and director are handled separately — must NOT be in this set.
        self.assertNotIn('admin', DEPARTMENT_HEAD_ROLES)
        self.assertNotIn('direktor', DEPARTMENT_HEAD_ROLES)
        self.assertNotIn('employee', DEPARTMENT_HEAD_ROLES)


class JinjaHelperTests(unittest.TestCase):
    def test_is_department_head_helper_reflects_session(self):
        from flask import render_template_string, session as flask_session

        with museum_app.app.test_request_context('/'):
            flask_session['is_department_head'] = True
            rendered_true = render_template_string(
                '{{ "yes" if is_department_head() else "no" }}'
            )
        self.assertEqual(rendered_true, 'yes')

        with museum_app.app.test_request_context('/'):
            flask_session['is_department_head'] = False
            rendered_false = render_template_string(
                '{{ "yes" if is_department_head() else "no" }}'
            )
        self.assertEqual(rendered_false, 'no')


if __name__ == '__main__':
    unittest.main()
