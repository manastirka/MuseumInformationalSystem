#!/usr/bin/env python3
"""Regression tests for director-scoped admin access.

Business rule (updated 2026-06): the museum director (user_role='direktor')
has FULL admin parity — all `admin_required` routes admit the director.
The director keeps director-specific behavior where being admin would take
something away: mailbox access stays (mail is blocked for 'admin' only) and
the timesheet self-approval guard still treats the director as 'direktor'
(cannot verify their own report).
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


BIOLOGY = 'БИОЛОШКО ОДЕЉЕЊЕ'
GEOLOGY = 'ГЕОЛОШКО ОДЕЉЕЊЕ'
EDUCATION = 'ГРУПА ЗА ЕДУКАЦИЈУ, КОМУНИКАЦИЈУ И МАРКЕТИНГ'
GALLERY = 'ГРУПА ЗА ИЗЛОЖБЕНЕ ПОСЛОВЕ – ГАЛЕРИЈА'


class _FakeCursor:
    def __init__(self, canned):
        self._canned = canned
        self._pending = None

    def execute(self, sql, params=None):
        for needle, row in self._canned.items():
            if needle in sql:
                self._pending = row
                return
        self._pending = None

    def fetchone(self):
        v = self._pending
        if isinstance(v, list):
            return v[0] if v else None
        return v

    def fetchall(self):
        v = self._pending
        if isinstance(v, list):
            return v
        return [v] if v else []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class _FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor

    def cursor(self):
        return self._cursor

    def commit(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


@contextmanager
def _fake_pg_connection_ctx(cursor):
    yield _FakeConnection(cursor)


class DirectorRouteAccessTests(unittest.TestCase):
    """Route-level tests: director can/can't access specific admin routes."""

    def setUp(self):
        self._prev_csrf = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def tearDown(self):
        museum_app.app.config['WTF_CSRF_ENABLED'] = self._prev_csrf

    def _login_as_director(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_email'] = 'slavko.spasic@nhmbeo.rs'
            sess['user_name'] = 'Славко Спасић'
            sess['user_role'] = 'direktor'
            sess['is_admin'] = False
            sess['user_department'] = 'Директор'
            sess['is_department_head'] = False

    def _login_as_regular_employee(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 99
            sess['user_email'] = 'other.employee@nhmbeo.rs'
            sess['user_name'] = 'Other'
            sess['user_role'] = 'employee'
            sess['is_admin'] = False
            sess['user_department'] = BIOLOGY
            sess['is_department_head'] = False

    # ---- Director-allowed (business/oversight) ----
    def test_director_can_access_admin_panel(self):
        self._login_as_director()
        response = self.client.get('/admin', base_url=self.base_url, follow_redirects=False)
        # admin_panel renders a template; just verify it's not blocked (302 would
        # be a flash-redirect to /dashboard from the auth decorator).
        self.assertEqual(response.status_code, 200)

    def test_director_can_access_admin_statistics(self):
        self._login_as_director()
        response = self.client.get('/admin/statistics', base_url=self.base_url, follow_redirects=False)
        self.assertNotEqual(response.status_code, 302,
                            "director was redirected (blocked) from /admin/statistics")

    def test_director_can_access_manage_user_access(self):
        self._login_as_director()
        response = self.client.get('/admin/manage_access', base_url=self.base_url, follow_redirects=False)
        self.assertNotEqual(response.status_code, 302,
                            "director was redirected (blocked) from /admin/manage_access")

    # ---- Director has full admin parity (business decision 2026-06) ----
    def test_director_can_access_password_manager(self):
        self._login_as_director()
        response = self.client.get('/admin/password_manager', base_url=self.base_url, follow_redirects=False)
        self.assertEqual(response.status_code, 200,
                         f"director should have admin parity, got {response.status_code}")

    def test_director_can_access_system_settings(self):
        self._login_as_director()
        response = self.client.get('/admin/system-settings', base_url=self.base_url, follow_redirects=False)
        self.assertEqual(response.status_code, 200)

    def test_director_can_access_mail_settings(self):
        self._login_as_director()
        response = self.client.get('/admin/mail-settings', base_url=self.base_url, follow_redirects=False)
        self.assertEqual(response.status_code, 200)

    def test_director_can_access_add_user(self):
        self._login_as_director()
        response = self.client.get('/admin/add_user', base_url=self.base_url, follow_redirects=False)
        self.assertEqual(response.status_code, 200)

    def test_director_can_reach_grant_access(self):
        self._login_as_director()
        # Unknown module key: handler runs (proving the decorator admits the
        # director) but bails out before persisting anything.
        response = self.client.post(
            '/admin/grant_access', base_url=self.base_url,
            data={'user_email': 'x@y.com', 'module_key': 'nonexistent_module_xyz'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('/dashboard', response.headers.get('Location', ''),
                         "redirect to /dashboard means the decorator denied access")

    # ---- Regular employee still blocked everywhere ----
    def test_employee_blocked_from_admin_panel(self):
        self._login_as_regular_employee()
        response = self.client.get('/admin', base_url=self.base_url, follow_redirects=False)
        self.assertIn(response.status_code, (302, 403))


class DirectorTimesheetScopingTests(unittest.TestCase):
    """Director approving timesheet reports must work across all departments."""

    def setUp(self):
        self._prev_csrf = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def tearDown(self):
        museum_app.app.config['WTF_CSRF_ENABLED'] = self._prev_csrf

    def _login_as_director(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_email'] = 'slavko.spasic@nhmbeo.rs'
            sess['user_name'] = 'Славко Спасић'
            sess['user_role'] = 'direktor'
            sess['is_admin'] = False
            sess['user_department'] = 'Директор'
            sess['is_department_head'] = False

    def _patched_pg(self, report_row, heads=None):
        """Mock the approve endpoint's DB calls.

        `report_row` populates the SELECT against `timesheet_reports tr`.
        `heads` is a list of `{department, head_email}` rows returned for the
        _get_department_heads lookup (matches 'FROM users u' in the SQL).
        """
        cursor = _FakeCursor({
            'FROM timesheet_reports tr': report_row,
            'FROM users u': heads or [],
            'FROM users WHERE full_name': None,
        })
        pg_patch = patch.object(
            timesheet_admin_views, 'get_postgres_connection',
            lambda **kw: _fake_pg_connection_ctx(cursor),
        )
        repo_patch = patch.object(
            timesheet_admin_views, '_timesheet_repository_available',
            return_value=True,
        )
        return pg_patch, repo_patch

    def test_director_blocked_for_regular_biology_employee(self):
        """Biology has a head (Верица). Director must NOT verify a regular
        Biology employee's report — that's the head's job."""
        self._login_as_director()
        row = {'id': 10, 'employee_name': 'X', 'employee_email': 'employee.bio@nhmbeo.rs',
               'employee_department': BIOLOGY, 'month': 1, 'year': 2026}
        heads = [{'department': BIOLOGY, 'head_email': 'verica.stojanovic@nhmbeo.rs'}]
        pg_patch, repo_patch = self._patched_pg(row, heads=heads)
        with pg_patch, repo_patch:
            response = self.client.post(
                '/api/admin/timesheet/report/10/approve',
                json={'approve': True}, base_url=self.base_url,
            )
        self.assertEqual(response.status_code, 403)

    def test_director_can_approve_biology_head_own_report(self):
        """Director DOES verify the Biology head's (Верица) own report —
        heads need someone above them to sign off."""
        self._login_as_director()
        row = {'id': 12, 'employee_name': 'Верица Стојановић',
               'employee_email': 'verica.stojanovic@nhmbeo.rs',
               'employee_department': BIOLOGY, 'month': 1, 'year': 2026}
        heads = [{'department': BIOLOGY, 'head_email': 'verica.stojanovic@nhmbeo.rs'}]
        pg_patch, repo_patch = self._patched_pg(row, heads=heads)
        with pg_patch, repo_patch:
            response = self.client.post(
                '/api/admin/timesheet/report/12/approve',
                json={'approve': True}, base_url=self.base_url,
            )
        self.assertEqual(response.status_code, 200,
                         f"director blocked from head's report; data={response.data[:300]!r}")
        self.assertTrue(response.get_json().get('success'))

    def test_director_approves_education_group_reports(self):
        """Edu group has no designated sef — director is the approver."""
        self._login_as_director()
        row = {'id': 20, 'employee_name': 'Z', 'employee_email': 'edu@nhmbeo.rs',
               'employee_department': EDUCATION, 'month': 2, 'year': 2026}
        # No heads row for Edu department.
        pg_patch, repo_patch = self._patched_pg(row, heads=[])
        with pg_patch, repo_patch:
            response = self.client.post(
                '/api/admin/timesheet/report/20/approve',
                json={'approve': True}, base_url=self.base_url,
            )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json().get('success'))

    def test_director_approves_gallery_group_reports(self):
        """Gallery group has no designated sef — director is the approver."""
        self._login_as_director()
        row = {'id': 21, 'employee_name': 'W', 'employee_email': 'gal@nhmbeo.rs',
               'employee_department': GALLERY, 'month': 2, 'year': 2026}
        pg_patch, repo_patch = self._patched_pg(row, heads=[])
        with pg_patch, repo_patch:
            response = self.client.post(
                '/api/admin/timesheet/report/21/approve',
                json={'approve': True}, base_url=self.base_url,
            )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json().get('success'))

    def test_director_blocked_for_regular_legal_affairs_employee(self):
        """Legal Affairs has a head (Ана Живановић). Regular employees there
        are her responsibility, not the director's."""
        self._login_as_director()
        legal = 'ОДСЕК ОПШТИХ И ПРАВНИХ ПОСЛОВА'
        row = {'id': 30, 'employee_name': 'Legal Employee',
               'employee_email': 'ana.kovacevic@nhmbeo.rs',
               'employee_department': legal, 'month': 2, 'year': 2026}
        heads = [{'department': legal, 'head_email': 'ana.zivanovic@nhmbeo.rs'}]
        pg_patch, repo_patch = self._patched_pg(row, heads=heads)
        with pg_patch, repo_patch:
            response = self.client.post(
                '/api/admin/timesheet/report/30/approve',
                json={'approve': True}, base_url=self.base_url,
            )
        self.assertEqual(response.status_code, 403)


class EducationGalleryApprovalRuleTests(unittest.TestCase):
    """Business rule: Edu and Gallery groups have no sef — only the director
    (and admin) can verify their timesheet reports. Department heads from
    other departments must not be able to reach into these groups.
    """

    def test_director_approves_edu_and_gallery(self):
        from timesheet_admin_views import can_user_verify_report_for_department
        director = {'user_role': 'direktor', 'is_department_head': False,
                    'user_department': 'Директор'}
        heads = {BIOLOGY: 'verica@x', GEOLOGY: 'biljana@x'}  # no Edu/Gallery
        self.assertTrue(can_user_verify_report_for_department(
            director, EDUCATION, target_employee_email='e@x', department_heads=heads))
        self.assertTrue(can_user_verify_report_for_department(
            director, GALLERY, target_employee_email='g@x', department_heads=heads))

    def test_other_department_head_cannot_reach_edu_or_gallery(self):
        from timesheet_admin_views import can_user_verify_report_for_department
        bio_head = {'user_role': 'sef_odeljenja', 'is_department_head': True,
                    'user_department': BIOLOGY}
        self.assertFalse(can_user_verify_report_for_department(bio_head, EDUCATION))
        self.assertFalse(can_user_verify_report_for_department(bio_head, GALLERY))

    def test_regular_employee_cannot_reach_edu_or_gallery(self):
        from timesheet_admin_views import can_user_verify_report_for_department
        employee = {'user_role': 'employee', 'is_department_head': False,
                    'user_department': EDUCATION}
        self.assertFalse(can_user_verify_report_for_department(employee, EDUCATION))
        self.assertFalse(can_user_verify_report_for_department(employee, GALLERY))


class DirectorAuthHelperTests(unittest.TestCase):
    """Unit tests for can_user_verify_report_for_department head-vs-employee rule."""

    def test_director_blocked_for_regular_employee_in_headed_dept(self):
        from timesheet_admin_views import can_user_verify_report_for_department
        director = {'user_role': 'direktor', 'is_department_head': False,
                    'user_department': 'Директор'}
        heads = {BIOLOGY: 'verica@x', GEOLOGY: 'biljana@x'}
        self.assertFalse(can_user_verify_report_for_department(
            director, BIOLOGY, target_employee_email='someone.else@x',
            department_heads=heads))
        self.assertFalse(can_user_verify_report_for_department(
            director, GEOLOGY, target_employee_email='random@x',
            department_heads=heads))

    def test_director_allowed_for_head_own_report(self):
        from timesheet_admin_views import can_user_verify_report_for_department
        director = {'user_role': 'direktor', 'is_department_head': False,
                    'user_department': 'Директор'}
        heads = {BIOLOGY: 'verica@x', GEOLOGY: 'biljana@x'}
        self.assertTrue(can_user_verify_report_for_department(
            director, BIOLOGY, target_employee_email='verica@x',
            department_heads=heads))
        self.assertTrue(can_user_verify_report_for_department(
            director, GEOLOGY, target_employee_email='BILJANA@X',  # case-insensitive
            department_heads=heads))

    def test_director_denied_when_no_head_context(self):
        """Missing head context must not fall back to broad director approval."""
        from timesheet_admin_views import can_user_verify_report_for_department
        director = {'user_role': 'direktor', 'is_department_head': False,
                    'user_department': 'Директор'}
        self.assertFalse(can_user_verify_report_for_department(
            director, BIOLOGY, target_employee_email='someone@x'))
        self.assertFalse(can_user_verify_report_for_department(
            director, GEOLOGY, target_employee_email='head@x'))

    def test_director_view_is_cross_department(self):
        from timesheet_admin_views import can_user_view_report_for_department
        director = {'user_role': 'direktor', 'is_department_head': False,
                    'user_department': 'Директор'}
        self.assertTrue(can_user_view_report_for_department(director, BIOLOGY))
        self.assertTrue(can_user_view_report_for_department(director, EDUCATION))


class DirectorSelfApprovalTests(unittest.TestCase):
    """The director cannot verify their own timesheet — admin signs it off."""

    def test_director_cannot_self_approve_own_dept(self):
        from timesheet_admin_views import can_user_verify_report_for_department
        slavko = {
            'user_role': 'direktor', 'is_department_head': False,
            'user_department': 'ДИРЕКТОР',
            'user_email': 'slavko.spasic@nhmbeo.rs',
        }
        # Own report in his own department (no head there)
        self.assertFalse(can_user_verify_report_for_department(
            slavko, 'ДИРЕКТОР',
            target_employee_email='slavko.spasic@nhmbeo.rs',
            department_heads={},
        ))

    def test_director_cannot_self_approve_case_mixed(self):
        from timesheet_admin_views import can_user_verify_report_for_department
        slavko = {
            'user_role': 'direktor', 'is_department_head': False,
            'user_department': 'ДИРЕКТОР',
            'user_email': 'Slavko.Spasic@NHMBEO.RS',
        }
        self.assertFalse(can_user_verify_report_for_department(
            slavko, 'ДИРЕКТОР',
            target_employee_email='slavko.spasic@nhmbeo.rs',
            department_heads={},
        ))

    def test_director_still_approves_other_no_head_dept(self):
        """Guard only fires on director's OWN email — other no-head reports
        (Edu, Gallery) remain approvable."""
        from timesheet_admin_views import can_user_verify_report_for_department
        slavko = {
            'user_role': 'direktor', 'is_department_head': False,
            'user_department': 'ДИРЕКТОР',
            'user_email': 'slavko.spasic@nhmbeo.rs',
        }
        self.assertTrue(can_user_verify_report_for_department(
            slavko, EDUCATION,
            target_employee_email='edu.staff@nhmbeo.rs',
            department_heads={},
        ))

    def test_is_director_template_helper(self):
        from flask import render_template_string, session as flask_session
        with museum_app.app.test_request_context('/'):
            flask_session['user_role'] = 'direktor'
            out = render_template_string('{{ "yes" if is_director() else "no" }}')
        self.assertEqual(out, 'yes')

        with museum_app.app.test_request_context('/'):
            flask_session['user_role'] = 'admin'
            out = render_template_string('{{ "yes" if is_director() else "no" }}')
        self.assertEqual(out, 'no')


class ReportListAnnotationTests(unittest.TestCase):
    """End-to-end style: hit /admin/timesheet_reports as director and verify
    that `can_verify` is correctly assigned per report — so the template can
    disable the approve button for reports the director shouldn't touch.
    """

    def setUp(self):
        self._prev_csrf = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def tearDown(self):
        museum_app.app.config['WTF_CSRF_ENABLED'] = self._prev_csrf

    def _login_as_director(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_email'] = 'slavko.spasic@nhmbeo.rs'
            sess['user_name'] = 'Славко Спасић'
            sess['user_role'] = 'direktor'
            sess['is_admin'] = False
            sess['user_department'] = 'Директор'
            sess['is_department_head'] = False

    def test_list_annotation_director(self):
        """Director listing: annotate helper should flag bio-employee report
        as non-verifiable, head-own report as verifiable, edu report as
        verifiable."""
        from timesheet_admin_views import _annotate_reports_with_verify_flag
        reports = [
            {'id': 100},  # regular biology employee
            {'id': 101},  # biljana (geology head) own report
            {'id': 102},  # edu employee (no head)
        ]

        report_meta = [
            {'id': 100, 'employee_email': 'bio.worker@nhmbeo.rs',
             'employee_department': BIOLOGY},
            {'id': 101, 'employee_email': 'biljana.mitrovic@nhmbeo.rs',
             'employee_department': GEOLOGY},
            {'id': 102, 'employee_email': 'edu.staff@nhmbeo.rs',
             'employee_department': EDUCATION},
        ]
        heads_rows = [
            {'department': BIOLOGY, 'head_email': 'verica.stojanovic@nhmbeo.rs'},
            {'department': GEOLOGY, 'head_email': 'biljana.mitrovic@nhmbeo.rs'},
        ]

        class _Cur:
            def __init__(self):
                self._next = None
            def execute(self, sql, params=None):
                if 'FROM timesheet_reports tr' in sql:
                    self._next = report_meta
                elif 'FROM users u' in sql:
                    self._next = heads_rows
                else:
                    self._next = None
            def fetchall(self):
                return self._next or []
            def fetchone(self):
                return (self._next or [None])[0]
            def __enter__(self): return self
            def __exit__(self, *a): return False

        class _Conn:
            def cursor(self): return _Cur()
            def __enter__(self): return self
            def __exit__(self, *a): return False

        # Within a request context so `session` is readable
        with museum_app.app.test_request_context('/'):
            from flask import session as flask_session
            flask_session['user_role'] = 'direktor'
            flask_session['user_email'] = 'slavko.spasic@nhmbeo.rs'
            flask_session['is_department_head'] = False
            with patch('timesheet_admin_views.get_postgres_connection',
                       lambda **kw: _Conn()):
                _annotate_reports_with_verify_flag(reports)

        self.assertFalse(reports[0]['can_verify'], "director should NOT verify regular bio employee")
        self.assertTrue(reports[1]['can_verify'], "director SHOULD verify biljana (head) own report")
        self.assertTrue(reports[2]['can_verify'], "director SHOULD verify edu report (no head)")


class VerifiedRoleAuditTests(unittest.TestCase):
    """The approve endpoint must record which role signed off (audit trail).
    Column: timesheet_reports.verified_role. Cleared on unapprove.
    """

    def setUp(self):
        self._prev_csrf = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def tearDown(self):
        museum_app.app.config['WTF_CSRF_ENABLED'] = self._prev_csrf

    def _login_as_director(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_email'] = 'slavko.spasic@nhmbeo.rs'
            sess['user_role'] = 'direktor'
            sess['user_department'] = 'Директор'
            sess['is_department_head'] = False

    def _run_approve(self, report_row, heads, approve):
        """Capture the UPDATE's params so we can assert verified_role."""
        captured = []
        class _Cur:
            def __init__(self):
                self._pending = None
            def execute(self, sql, params=None):
                captured.append((sql, params))
                if 'FROM timesheet_reports tr' in sql:
                    self._pending = report_row
                elif 'FROM users u' in sql:
                    self._pending = heads
                elif 'FROM users WHERE full_name' in sql:
                    self._pending = None
                else:
                    self._pending = None
            def fetchall(self):
                v = self._pending
                return v if isinstance(v, list) else ([v] if v else [])
            def fetchone(self):
                v = self._pending
                return v[0] if isinstance(v, list) and v else v
            def __enter__(self): return self
            def __exit__(self, *a): return False
        class _Conn:
            def cursor(self): return _Cur()
            def commit(self): pass
            def __enter__(self): return self
            def __exit__(self, *a): return False

        self._login_as_director()
        with patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: _Conn()), \
             patch('timesheet_admin_views._timesheet_repository_available',
                   return_value=True):
            response = self.client.post(
                f'/api/admin/timesheet/report/{report_row["id"]}/approve',
                json={'approve': approve}, base_url=self.base_url,
            )
        return response, captured

    def test_approve_sets_verified_role(self):
        row = {'id': 501, 'employee_name': 'Edu Worker',
               'employee_email': 'edu@nhmbeo.rs',
               'employee_department': EDUCATION, 'month': 3, 'year': 2026}
        response, captured = self._run_approve(row, heads=[], approve=True)
        self.assertEqual(response.status_code, 200)
        # Find the UPDATE ... SET is_verified = TRUE ... verified_role = %s
        update_calls = [c for c in captured
                        if 'UPDATE timesheet_reports' in c[0]
                        and 'verified_role' in c[0]
                        and 'is_verified = TRUE' in c[0]]
        self.assertTrue(update_calls, f"no verify UPDATE captured; got {[c[0][:60] for c in captured]}")
        # verified_role is the second param (see SQL order)
        params = update_calls[0][1]
        self.assertIn('direktor', params,
                      f"expected director role in UPDATE params, got {params}")

    def test_unapprove_clears_verified_role(self):
        row = {'id': 502, 'employee_name': 'Edu Worker',
               'employee_email': 'edu@nhmbeo.rs',
               'employee_department': EDUCATION, 'month': 3, 'year': 2026,
               'status': 'APPROVED'}
        response, captured = self._run_approve(row, heads=[], approve=False)
        self.assertEqual(response.status_code, 200)
        update_calls = [c for c in captured
                        if 'UPDATE timesheet_reports' in c[0]
                        and 'is_verified = FALSE' in c[0]]
        self.assertTrue(update_calls, f"no unapprove UPDATE captured")
        sql = update_calls[0][0]
        self.assertIn('verified_role = NULL', sql,
                      "unapprove must clear verified_role")


class OnlyVerifiableFilterTests(unittest.TestCase):
    """The `?only_verifiable=1` query param filters the reports list to only
    those the current user can actually sign off (based on `can_verify`).
    """

    def setUp(self):
        self._prev_csrf = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def tearDown(self):
        museum_app.app.config['WTF_CSRF_ENABLED'] = self._prev_csrf

    def _login_as_director(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_email'] = 'slavko.spasic@nhmbeo.rs'
            sess['user_role'] = 'direktor'
            sess['user_department'] = 'Директор'
            sess['is_department_head'] = False

    def test_filter_keeps_only_verifiable(self):
        """Given 3 reports, 2 non-verifiable for director, 2 verifiable, the
        filtered view shows only the verifiable ones."""
        fake_repo = MagicMock()
        fake_repo.available = True
        fake_repo.list_reports.return_value = {
            'reports': [
                {'id': 601, 'employee_name': 'Bio Worker',
                 'month': 3, 'year': 2026, 'organization_unit': '',
                 'is_verified': False, 'is_locked': False, 'status': 'SUBMITTED',
                 'work_in_museum': 0, 'work_outside': 0, 'vacation': 0,
                 'public_holiday': 0, 'paid_leave': 0, 'other_leave': 0,
                 'sick_lt30': 0, 'sick_gte30': 0, 'total_hours': 0},
                {'id': 602, 'employee_name': 'Верица Стојановић',
                 'month': 3, 'year': 2026, 'organization_unit': '',
                 'is_verified': False, 'is_locked': False, 'status': 'SUBMITTED',
                 'work_in_museum': 0, 'work_outside': 0, 'vacation': 0,
                 'public_holiday': 0, 'paid_leave': 0, 'other_leave': 0,
                 'sick_lt30': 0, 'sick_gte30': 0, 'total_hours': 0},
                {'id': 603, 'employee_name': 'Edu Worker',
                 'month': 3, 'year': 2026, 'organization_unit': '',
                 'is_verified': False, 'is_locked': False, 'status': 'SUBMITTED',
                 'work_in_museum': 0, 'work_outside': 0, 'vacation': 0,
                 'public_holiday': 0, 'paid_leave': 0, 'other_leave': 0,
                 'sick_lt30': 0, 'sick_gte30': 0, 'total_hours': 0},
            ],
            'total': 3, 'page': 1, 'total_pages': 1,
        }
        fake_repo.get_month_summary.return_value = None
        fake_repo.get_overall_summary.return_value = None

        report_meta = [
            {'id': 601, 'employee_email': 'bio.worker@nhmbeo.rs',
             'employee_department': BIOLOGY},
            {'id': 602, 'employee_email': 'verica.stojanovic@nhmbeo.rs',
             'employee_department': BIOLOGY},
            {'id': 603, 'employee_email': 'edu@nhmbeo.rs',
             'employee_department': EDUCATION},
        ]
        heads_rows = [
            {'department': BIOLOGY, 'head_email': 'verica.stojanovic@nhmbeo.rs'},
        ]

        class _Cur:
            def __init__(self):
                self._pending = None
            def execute(self, sql, params=None):
                if 'FROM timesheet_reports tr' in sql:
                    self._pending = report_meta
                elif 'FROM users u' in sql:
                    self._pending = heads_rows
                else:
                    self._pending = None
            def fetchall(self):
                return self._pending or []
            def fetchone(self):
                return (self._pending or [None])[0]
            def __enter__(self): return self
            def __exit__(self, *a): return False

        class _Conn:
            def cursor(self): return _Cur()
            def __enter__(self): return self
            def __exit__(self, *a): return False

        self._login_as_director()
        with patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: _Conn()), \
             patch.object(museum_app, 'timesheet_repository', fake_repo):
            response = self.client.get(
                '/admin/timesheet_reports?only_verifiable=1',
                base_url=self.base_url,
            )
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        # 603 (Edu, no head) and 602 (head's own) stay; 601 filtered out.
        self.assertIn('timesheet-report-approve-602', body)
        self.assertIn('timesheet-report-approve-603', body)
        self.assertNotIn('timesheet-report-approve-601', body)
        self.assertIn('Филтер активан', body)


class NotificationFlowTests(unittest.TestCase):
    """Verify the approve/unapprove notifications and verifier-notify on submit.

    Covers three bug fixes:
    1. Unapprove must send a "verification revoked" notification to the employee.
    2. Approve notification must use employee_email from the report, not a
       fragile full_name lookup.
    3. On submit, notify admin + director + the target department's head
       (not just admins — and definitely not with a broken SQL query).
    """

    def setUp(self):
        self._prev_csrf = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def tearDown(self):
        museum_app.app.config['WTF_CSRF_ENABLED'] = self._prev_csrf

    def _login_as_director(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_email'] = 'slavko.spasic@nhmbeo.rs'
            sess['user_role'] = 'direktor'
            sess['user_department'] = 'ДИРЕКТОР'
            sess['is_department_head'] = False

    def _approve_cursor_factory(self, report_row, heads, captured):
        class _Cur:
            def __init__(self):
                self._pending = None
            def execute(self, sql, params=None):
                captured.append((sql, params))
                if 'FROM timesheet_reports tr' in sql:
                    self._pending = report_row
                elif 'FROM users u' in sql:
                    self._pending = heads
                elif 'FROM users WHERE full_name' in sql:
                    self._pending = None
                else:
                    self._pending = None
            def fetchall(self):
                v = self._pending
                return v if isinstance(v, list) else ([v] if v else [])
            def fetchone(self):
                v = self._pending
                return v[0] if isinstance(v, list) and v else v
            def __enter__(self): return self
            def __exit__(self, *a): return False

        class _Conn:
            def cursor(self): return _Cur()
            def commit(self): pass
            def __enter__(self): return self
            def __exit__(self, *a): return False
        return _Conn

    def _extract_notify_inserts(self, captured):
        """Return list of (user_email, title, message, icon, type) from any
        INSERT INTO user_notifications calls in the captured SQL log."""
        rows = []
        for sql, params in captured:
            if 'INSERT INTO user_notifications' in sql and params:
                rows.append(params)
        return rows

    def test_unapprove_sends_notification_to_employee(self):
        """Bug fix: unapprove previously sent NO notification. Now it must."""
        row = {'id': 701, 'employee_name': 'X',
               'employee_email': 'verica.stojanovic@nhmbeo.rs',
               'employee_department': BIOLOGY,
               'month': 4, 'year': 2026,
               'status': 'APPROVED'}
        heads = [{'department': BIOLOGY, 'head_email': 'verica.stojanovic@nhmbeo.rs'}]
        captured = []
        Conn = self._approve_cursor_factory(row, heads, captured)

        self._login_as_director()
        with patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_admin_views._timesheet_repository_available',
                   return_value=True):
            response = self.client.post(
                f'/api/admin/timesheet/report/{row["id"]}/approve',
                json={'approve': False}, base_url=self.base_url,
            )
        self.assertEqual(response.status_code, 200)

        notify_rows = self._extract_notify_inserts(captured)
        self.assertTrue(notify_rows, "expected unapprove notification; got none")
        # Params: (user_email, title, message)  (icon/type are in the SQL)
        self.assertEqual(notify_rows[0][0], 'verica.stojanovic@nhmbeo.rs')
        self.assertIn('Верификација', notify_rows[0][1])  # title
        self.assertIn('повучена', notify_rows[0][2])      # message mentions revocation

    def test_approve_uses_employee_email_from_report(self):
        """Bug fix: approve previously did SELECT email FROM users WHERE
        full_name = ... which is fragile. Now it uses the already-fetched
        employee_email directly. Proof: no full_name lookup in captured SQL."""
        row = {'id': 702, 'employee_name': 'Verica Stojanovic',  # anglicized
               'employee_email': 'verica.stojanovic@nhmbeo.rs',
               'employee_department': BIOLOGY,
               'month': 4, 'year': 2026}
        heads = [{'department': BIOLOGY, 'head_email': 'verica.stojanovic@nhmbeo.rs'}]
        captured = []
        Conn = self._approve_cursor_factory(row, heads, captured)

        self._login_as_director()
        with patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_admin_views._timesheet_repository_available',
                   return_value=True):
            response = self.client.post(
                f'/api/admin/timesheet/report/{row["id"]}/approve',
                json={'approve': True}, base_url=self.base_url,
            )
        self.assertEqual(response.status_code, 200)

        # Assert no fragile full_name lookup was made
        for sql, _ in captured:
            self.assertNotIn('FROM users WHERE full_name', sql,
                             "approve path still has fragile full_name lookup")

        # Assert the notification went to the email straight from the report
        notify_rows = self._extract_notify_inserts(captured)
        self.assertEqual(notify_rows[0][0], 'verica.stojanovic@nhmbeo.rs')

    def _stub_notify_conn(self, candidates, heads_rows, captured):
        """Fake cursor that returns `candidates` for the candidate SELECT and
        `heads_rows` for the `_get_department_heads` query."""
        class _Cur:
            def __init__(self):
                self._pending = None
            def execute(self, sql, params=None):
                captured.append((sql, params))
                if 'FROM users u\n                      JOIN roles r' in sql or 'leadership' in sql:
                    # Candidate SELECT — match by the "IN ( ...leadership...)"
                    self._pending = candidates
                elif "FROM users u\n        JOIN roles r" in sql or 'r.name = ANY' in sql:
                    self._pending = heads_rows
                else:
                    self._pending = None
            def fetchall(self):
                return self._pending or []
            def fetchone(self):
                return (self._pending or [None])[0]
            def __enter__(self): return self
            def __exit__(self, *a): return False

        class _Conn:
            def cursor(self): return _Cur()
            def commit(self): pass
            def __enter__(self): return self
            def __exit__(self, *a): return False
        return _Conn

    def test_notify_bio_employee_submission(self):
        """Bio employee submits → Верица (bio head) + admin get notified.
        Director does NOT (bio has a head; submitter is not a head)."""
        from timesheet_employee_views import _notify_verifiers_about_submission

        candidates = [
            {'email': 'admin@nhmbeo.rs', 'role': 'admin', 'department': None},
            {'email': 'slavko.spasic@nhmbeo.rs', 'role': 'direktor',
             'department': 'ДИРЕКТОР'},
            {'email': 'verica.stojanovic@nhmbeo.rs', 'role': 'sef_odeljenja',
             'department': BIOLOGY},
            {'email': 'biljana.mitrovic@nhmbeo.rs', 'role': 'sef_odeljenja',
             'department': GEOLOGY},
            {'email': 'ana.zivanovic@nhmbeo.rs', 'role': 'sef_pravne_sluzbe',
             'department': 'ОДСЕК ОПШТИХ И ПРАВНИХ ПОСЛОВА'},
            {'email': 'dusica.ivic@nhmbeo.rs', 'role': 'sef_racunovodstva',
             'department': 'ГРУПА ЗА ФИНАНСИЈСКО-РАЧУНОВОДСТВЕНЕ ПОСЛОВЕ'},
        ]
        heads_rows = [
            {'department': BIOLOGY, 'head_email': 'verica.stojanovic@nhmbeo.rs'},
            {'department': GEOLOGY, 'head_email': 'biljana.mitrovic@nhmbeo.rs'},
            {'department': 'ОДСЕК ОПШТИХ И ПРАВНИХ ПОСЛОВА',
             'head_email': 'ana.zivanovic@nhmbeo.rs'},
            {'department': 'ГРУПА ЗА ФИНАНСИЈСКО-РАЧУНОВОДСТВЕНЕ ПОСЛОВЕ',
             'head_email': 'dusica.ivic@nhmbeo.rs'},
        ]
        captured = []
        Conn = self._stub_notify_conn(candidates, heads_rows, captured)

        with patch('timesheet_employee_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: Conn()):
            _notify_verifiers_about_submission(
                'Тест Биолог', 'bio.worker@nhmbeo.rs', BIOLOGY)

        inserts = [p for sql, p in captured
                   if 'INSERT INTO user_notifications' in sql]
        recipients = {p[0] for p in inserts}

        # Bio employee in a dept WITH a head — only admin + bio head notified.
        self.assertEqual(
            recipients,
            {'admin@nhmbeo.rs', 'verica.stojanovic@nhmbeo.rs'},
            f"wrong recipients; got {recipients}",
        )
        # Director and other dept heads must NOT be pinged.
        self.assertNotIn('slavko.spasic@nhmbeo.rs', recipients)
        self.assertNotIn('biljana.mitrovic@nhmbeo.rs', recipients)

    def test_notify_edu_employee_submission_includes_director(self):
        """Edu group has no head → admin + director get notified."""
        from timesheet_employee_views import _notify_verifiers_about_submission

        candidates = [
            {'email': 'admin@nhmbeo.rs', 'role': 'admin', 'department': None},
            {'email': 'slavko.spasic@nhmbeo.rs', 'role': 'direktor',
             'department': 'ДИРЕКТОР'},
            {'email': 'verica.stojanovic@nhmbeo.rs', 'role': 'sef_odeljenja',
             'department': BIOLOGY},
        ]
        heads_rows = [
            {'department': BIOLOGY, 'head_email': 'verica.stojanovic@nhmbeo.rs'},
            # No row for Edu → director approves Edu.
        ]
        captured = []
        Conn = self._stub_notify_conn(candidates, heads_rows, captured)

        with patch('timesheet_employee_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: Conn()):
            _notify_verifiers_about_submission(
                'Тест Едукатор', 'edu@nhmbeo.rs', EDUCATION)

        inserts = [p for sql, p in captured
                   if 'INSERT INTO user_notifications' in sql]
        recipients = {p[0] for p in inserts}
        self.assertEqual(
            recipients,
            {'admin@nhmbeo.rs', 'slavko.spasic@nhmbeo.rs'},
            f"wrong recipients; got {recipients}",
        )

    def test_notify_dept_head_own_submission_includes_director(self):
        """Биљана submits her own timesheet → admin + director get notified
        (director signs off heads). Биљана herself is excluded."""
        from timesheet_employee_views import _notify_verifiers_about_submission

        candidates = [
            {'email': 'admin@nhmbeo.rs', 'role': 'admin', 'department': None},
            {'email': 'slavko.spasic@nhmbeo.rs', 'role': 'direktor',
             'department': 'ДИРЕКТОР'},
            # Биљана excluded by the SQL (submitter)
            {'email': 'verica.stojanovic@nhmbeo.rs', 'role': 'sef_odeljenja',
             'department': BIOLOGY},
        ]
        heads_rows = [
            {'department': BIOLOGY, 'head_email': 'verica.stojanovic@nhmbeo.rs'},
            {'department': GEOLOGY, 'head_email': 'biljana.mitrovic@nhmbeo.rs'},
        ]
        captured = []
        Conn = self._stub_notify_conn(candidates, heads_rows, captured)

        with patch('timesheet_employee_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: Conn()):
            _notify_verifiers_about_submission(
                'Биљана Митровић', 'biljana.mitrovic@nhmbeo.rs', GEOLOGY)

        inserts = [p for sql, p in captured
                   if 'INSERT INTO user_notifications' in sql]
        recipients = {p[0] for p in inserts}
        self.assertIn('admin@nhmbeo.rs', recipients)
        self.assertIn('slavko.spasic@nhmbeo.rs', recipients,
                      "director must be notified of a head's own submission")
        self.assertNotIn('biljana.mitrovic@nhmbeo.rs', recipients,
                         "submitter (herself a head) must not be pinged")

    def test_notify_uses_fixed_sql_shape(self):
        """The new query uses JOIN roles, not the broken `WHERE role=...`."""
        from timesheet_employee_views import _notify_verifiers_about_submission

        captured = []
        Conn = self._stub_notify_conn([], [], captured)
        with patch('timesheet_employee_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: Conn()):
            _notify_verifiers_about_submission(
                'X', 'x@nhmbeo.rs', BIOLOGY)

        sqls = [sql for sql, _ in captured]
        self.assertTrue(any('JOIN roles r' in s for s in sqls))
        self.assertFalse(any("WHERE role = 'admin'" in s for s in sqls),
                         "broken SQL pattern must be gone")


class ForceEditAccessTests(unittest.TestCase):
    """`/api/timesheet/<id>/force-edit` must open to admin + director + dept
    heads (scope-checked per report). Non-scoped heads get 403."""

    def setUp(self):
        self._prev_csrf = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def tearDown(self):
        museum_app.app.config['WTF_CSRF_ENABLED'] = self._prev_csrf

    def _stub_conn(self, report_dept, report_email, heads_rows):
        class _Cur:
            def __init__(self):
                self._pending = None
            def execute(self, sql, params=None):
                if 'FROM timesheet_reports tr' in sql and 'ep.email' in sql:
                    # _lookup_report_department expects row with department+email
                    self._pending = [{'employee_department': report_dept,
                                      'employee_email': report_email}]
                elif 'FROM users u' in sql:
                    self._pending = heads_rows
                else:
                    self._pending = None
            def fetchall(self):
                return self._pending or []
            def fetchone(self):
                return (self._pending or [None])[0]
            def __enter__(self): return self
            def __exit__(self, *a): return False
        class _Conn:
            def cursor(self): return _Cur()
            def commit(self): pass
            def __enter__(self): return self
            def __exit__(self, *a): return False
        return _Conn

    def test_geology_head_can_force_edit_geology_report(self):
        Conn = self._stub_conn(GEOLOGY, 'aca.lukovic@nhmbeo.rs',
                               [{'department': GEOLOGY,
                                 'head_email': 'biljana.mitrovic@nhmbeo.rs'}])

        with self.client.session_transaction() as sess:
            sess['user_id'] = 17
            sess['user_email'] = 'biljana.mitrovic@nhmbeo.rs'
            sess['user_role'] = 'sef_odeljenja'
            sess['user_department'] = GEOLOGY
            sess['is_department_head'] = True

        fake_result = MagicMock(success=True, data={'message': 'ok'})
        with patch('timesheet_employee_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_postgres.force_edit_timesheet', return_value=fake_result):
            r = self.client.post('/api/timesheet/42/force-edit', base_url=self.base_url)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.get_json().get('success'))

    def test_geology_head_cannot_force_edit_biology_report(self):
        Conn = self._stub_conn(BIOLOGY, 'bio.worker@nhmbeo.rs',
                               [{'department': BIOLOGY,
                                 'head_email': 'verica.stojanovic@nhmbeo.rs'},
                                {'department': GEOLOGY,
                                 'head_email': 'biljana.mitrovic@nhmbeo.rs'}])

        with self.client.session_transaction() as sess:
            sess['user_id'] = 17
            sess['user_email'] = 'biljana.mitrovic@nhmbeo.rs'
            sess['user_role'] = 'sef_odeljenja'
            sess['user_department'] = GEOLOGY  # wrong dept vs report
            sess['is_department_head'] = True

        with patch('timesheet_employee_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: Conn()):
            r = self.client.post('/api/timesheet/42/force-edit', base_url=self.base_url)
        self.assertEqual(r.status_code, 403)

    def test_director_can_force_edit_edu_report(self):
        Conn = self._stub_conn(EDUCATION, 'edu@nhmbeo.rs', [])

        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_email'] = 'slavko.spasic@nhmbeo.rs'
            sess['user_role'] = 'direktor'
            sess['user_department'] = 'ДИРЕКТОР'
            sess['is_department_head'] = False

        fake_result = MagicMock(success=True, data={'message': 'ok'})
        with patch('timesheet_employee_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_postgres.force_edit_timesheet', return_value=fake_result):
            r = self.client.post('/api/timesheet/42/force-edit', base_url=self.base_url)
        self.assertEqual(r.status_code, 200)


class SaveAutoResubmitTests(unittest.TestCase):
    """When an employee clicks 'Сачувај измене' on a REJECTED report, the
    save endpoint must implicitly resubmit it (status REJECTED → SUBMITTED)
    and fire the re-evaluation notification. Without this, fixed reports
    get stuck in REJECTED and the head never sees the fix."""

    def test_save_of_rejected_report_auto_resubmits(self):
        from timesheet_employee_views import api_save_timesheet

        captured = []
        class _Cur:
            def __init__(self):
                self._pending = None
                self._call = 0
            def execute(self, sql, params=None):
                captured.append((sql, params))
                # The status pre-check in api_save_timesheet
                if 'SELECT status FROM timesheet_reports' in sql:
                    self._pending = {'status': 'REJECTED'}
                elif 'FROM users u' in sql and 'JOIN roles r' in sql:
                    # Candidate recipients for the notification
                    self._pending = [
                        {'email': 'biljana.mitrovic@nhmbeo.rs',
                         'role': 'sef_odeljenja', 'department': GEOLOGY},
                    ]
                else:
                    self._pending = None
            def fetchall(self):
                return self._pending if isinstance(self._pending, list) else []
            def fetchone(self):
                return self._pending if not isinstance(self._pending, list) else (self._pending[0] if self._pending else None)
            def __enter__(self): return self
            def __exit__(self, *a): return False
        class _Conn:
            def cursor(self): return _Cur()
            def commit(self): pass
            def __enter__(self): return self
            def __exit__(self, *a): return False

        save_result = MagicMock(success=True, data={'report_id': 999, 'version': 2, 'message': 'ok'})
        submit_result = MagicMock(success=True, data={'was_rejected': True, 'message': 'resubmitted'})

        with museum_app.app.test_request_context(
            '/api/timesheet/save',
            method='POST',
            json={'month': 4, 'year': 2026, 'daily_data': {}, 'obavljeni_poslovi': '{}'},
        ):
            from flask import session as flask_session
            flask_session['user_email'] = 'aca.lukovic@nhmbeo.rs'
            flask_session['user_name'] = 'Александар Луковић'

            with patch('timesheet_employee_views.get_postgres_connection',
                       lambda **kw: _Conn()), \
                 patch('timesheet_employee_views.save_timesheet_to_postgres',
                       return_value=save_result) \
                     if False else patch('timesheet_postgres.save_timesheet_to_postgres',
                                         return_value=save_result), \
                 patch('timesheet_postgres.submit_timesheet', return_value=submit_result), \
                 patch('timesheet_postgres.get_user_department_and_position',
                       return_value=(GEOLOGY, 'кустос')), \
                 patch('timesheet_admin_views.get_postgres_connection',
                       lambda **kw: _Conn()):
                response = api_save_timesheet()

        # api_save_timesheet returns a Flask Response — extract JSON
        import json
        if hasattr(response, 'get_json'):
            data = response.get_json()
        else:
            # Tuple (response, status)
            data = json.loads(response[0].get_data(as_text=True))

        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('auto_resubmitted'),
                        "save on a REJECTED report must auto-resubmit")
        self.assertIn('поново поднет', data.get('message', ''))


class ResubmissionNotificationTests(unittest.TestCase):
    """When an employee resubmits after a reject/return, the recipients must
    get a 're-evaluation' notification (icon bi-arrow-repeat, type warning),
    not the plain 'new submission' one."""

    def test_is_resubmission_changes_title_icon_and_type(self):
        from timesheet_employee_views import _notify_verifiers_about_submission

        captured = []
        class _Cur:
            def __init__(self):
                self._pending = [
                    {'email': 'admin@nhmbeo.rs', 'role': 'admin', 'department': None},
                    {'email': 'verica.stojanovic@nhmbeo.rs', 'role': 'sef_odeljenja',
                     'department': BIOLOGY},
                ]
            def execute(self, sql, params=None):
                captured.append((sql, params))
                if 'FROM users u' in sql and 'JOIN roles r' in sql:
                    pass  # uses default self._pending
                elif 'SELECT COALESCE(d.name' in sql:
                    self._pending = None  # not used in this test
                elif 'SELECT' in sql and 'FROM users u' in sql:
                    # _get_department_heads — return Biology head row
                    self._pending = [{'department': BIOLOGY,
                                      'head_email': 'verica.stojanovic@nhmbeo.rs'}]
            def fetchall(self): return self._pending or []
            def fetchone(self):
                return (self._pending or [None])[0]
            def __enter__(self): return self
            def __exit__(self, *a): return False
        class _Conn:
            def cursor(self): return _Cur()
            def commit(self): pass
            def __enter__(self): return self
            def __exit__(self, *a): return False

        with patch('timesheet_employee_views.get_postgres_connection',
                   lambda **kw: _Conn()), \
             patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: _Conn()):
            _notify_verifiers_about_submission(
                'Ана Пауновић', 'ana.paunovic@nhmbeo.rs', BIOLOGY,
                is_resubmission=True,
            )

        inserts = [p for sql, p in captured
                   if 'INSERT INTO user_notifications' in sql]
        self.assertTrue(inserts, "at least one notification must be sent")
        for params in inserts:
            # (email, title, message, icon, type)
            _, title, message, icon, ntype = params
            self.assertIn('реевалуација', title,
                          "resubmission title must mention реевалуација")
            self.assertEqual(icon, 'bi-arrow-repeat')
            self.assertEqual(ntype, 'warning')
            self.assertIn('поново', message)


class ReturnButtonListRenderTests(unittest.TestCase):
    """The list page renders a `return-to-employee` button on each SUBMITTED
    report that the current user is authorized to verify, and does NOT
    render it on the user's own report nor on reports they cannot verify."""

    def setUp(self):
        self._prev_csrf = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def tearDown(self):
        museum_app.app.config['WTF_CSRF_ENABLED'] = self._prev_csrf

    def test_head_sees_return_button_on_subordinate_submitted_report(self):
        fake_repo = MagicMock()
        fake_repo.available = True
        common = {
            'month': 4, 'year': 2026, 'organization_unit': '',
            'is_verified': False, 'is_locked': True, 'status': 'SUBMITTED',
            'work_in_museum': 0, 'work_outside': 0, 'vacation': 0,
            'public_holiday': 0, 'paid_leave': 0, 'other_leave': 0,
            'sick_lt30': 0, 'sick_gte30': 0, 'total_hours': 0,
        }
        fake_repo.list_reports.return_value = {
            'reports': [
                dict(id=801, employee_name='Bio Subordinate', **common),
                dict(id=802, employee_name='Верица Стојановић', **common),  # head's own
            ],
            'total': 2, 'page': 1, 'total_pages': 1,
        }
        fake_repo.get_month_summary.return_value = None
        fake_repo.get_overall_summary.return_value = None

        report_meta = [
            {'id': 801, 'employee_email': 'bio@nhmbeo.rs',
             'employee_department': BIOLOGY},
            {'id': 802, 'employee_email': 'verica.stojanovic@nhmbeo.rs',
             'employee_department': BIOLOGY},
        ]
        heads_rows = [{'department': BIOLOGY,
                       'head_email': 'verica.stojanovic@nhmbeo.rs'}]

        class _Cur:
            def __init__(self): self._pending = None
            def execute(self, sql, params=None):
                if 'FROM timesheet_reports tr' in sql:
                    self._pending = report_meta
                elif 'FROM users u' in sql:
                    self._pending = heads_rows
                else:
                    self._pending = None
            def fetchall(self): return self._pending or []
            def fetchone(self):
                return (self._pending or [None])[0]
            def __enter__(self): return self
            def __exit__(self, *a): return False
        class _Conn:
            def cursor(self): return _Cur()
            def __enter__(self): return self
            def __exit__(self, *a): return False

        with self.client.session_transaction() as sess:
            sess['user_id'] = 27
            sess['user_email'] = 'verica.stojanovic@nhmbeo.rs'
            sess['user_role'] = 'sef_odeljenja'
            sess['user_department'] = BIOLOGY
            sess['is_department_head'] = True

        with patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: _Conn()), \
             patch.object(museum_app, 'timesheet_repository', fake_repo):
            r = self.client.get('/admin/timesheet_reports', base_url=self.base_url)
        self.assertEqual(r.status_code, 200)
        body = r.get_data(as_text=True)
        # Button must render for subordinate (801) and NOT for own report (802)
        self.assertIn('timesheet-report-return-801', body,
                      "head must see return button on subordinate SUBMITTED report")
        self.assertNotIn('timesheet-report-return-802', body,
                         "head must NOT see return button on their own report")


class RejectSubmittedReportAccessTests(unittest.TestCase):
    """`/api/timesheet/<id>/reject` opens to admin + director + dept heads
    with per-report scope. Heads return SUBMITTED reports in their own dept;
    director returns Edu/Gallery + heads' own reports."""

    def setUp(self):
        self._prev_csrf = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def tearDown(self):
        museum_app.app.config['WTF_CSRF_ENABLED'] = self._prev_csrf

    def _stub_conn(self, report_dept, report_email, heads_rows):
        class _Cur:
            def __init__(self):
                self._pending = None
            def execute(self, sql, params=None):
                if 'FROM timesheet_reports tr' in sql and 'ep.email' in sql:
                    self._pending = [{'employee_department': report_dept,
                                      'employee_email': report_email}]
                elif 'FROM users u' in sql:
                    self._pending = heads_rows
                else:
                    self._pending = None
            def fetchall(self): return self._pending or []
            def fetchone(self):
                return (self._pending or [None])[0]
            def __enter__(self): return self
            def __exit__(self, *a): return False
        class _Conn:
            def cursor(self): return _Cur()
            def commit(self): pass
            def __enter__(self): return self
            def __exit__(self, *a): return False
        return _Conn

    def test_bio_head_can_reject_biology_submission(self):
        Conn = self._stub_conn(BIOLOGY, 'bio.worker@nhmbeo.rs',
                               [{'department': BIOLOGY,
                                 'head_email': 'verica.stojanovic@nhmbeo.rs'}])

        with self.client.session_transaction() as sess:
            sess['user_id'] = 27
            sess['user_email'] = 'verica.stojanovic@nhmbeo.rs'
            sess['user_role'] = 'sef_odeljenja'
            sess['user_department'] = BIOLOGY
            sess['is_department_head'] = True

        fake_result = MagicMock(success=True, data={'message': 'ok'})
        with patch('timesheet_employee_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_postgres.reject_timesheet', return_value=fake_result), \
             patch('timesheet_employee_views._notify_employee_about_review_outcome',
                   return_value=None):
            r = self.client.post('/api/timesheet/50/reject',
                                 json={'note': 'Нетачне сате'},
                                 base_url=self.base_url)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.get_json().get('success'))

    def test_geology_head_cannot_reject_biology_submission(self):
        Conn = self._stub_conn(BIOLOGY, 'bio.worker@nhmbeo.rs',
                               [{'department': BIOLOGY,
                                 'head_email': 'verica.stojanovic@nhmbeo.rs'},
                                {'department': GEOLOGY,
                                 'head_email': 'biljana.mitrovic@nhmbeo.rs'}])

        with self.client.session_transaction() as sess:
            sess['user_id'] = 17
            sess['user_email'] = 'biljana.mitrovic@nhmbeo.rs'
            sess['user_role'] = 'sef_odeljenja'
            sess['user_department'] = GEOLOGY
            sess['is_department_head'] = True

        with patch('timesheet_employee_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: Conn()):
            r = self.client.post('/api/timesheet/50/reject',
                                 json={'note': 'Није моје одељење'},
                                 base_url=self.base_url)
        self.assertEqual(r.status_code, 403)

    def test_director_can_reject_edu_submission(self):
        Conn = self._stub_conn(EDUCATION, 'edu@nhmbeo.rs', [])

        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_email'] = 'slavko.spasic@nhmbeo.rs'
            sess['user_role'] = 'direktor'
            sess['user_department'] = 'ДИРЕКТОР'
            sess['is_department_head'] = False

        fake_result = MagicMock(success=True, data={'message': 'ok'})
        with patch('timesheet_employee_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_postgres.reject_timesheet', return_value=fake_result), \
             patch('timesheet_employee_views._notify_employee_about_review_outcome',
                   return_value=None):
            r = self.client.post('/api/timesheet/50/reject',
                                 json={'note': 'Недостаје потпис'},
                                 base_url=self.base_url)
        self.assertEqual(r.status_code, 200)

    def test_reject_requires_note(self):
        Conn = self._stub_conn(BIOLOGY, 'bio.worker@nhmbeo.rs',
                               [{'department': BIOLOGY,
                                 'head_email': 'verica.stojanovic@nhmbeo.rs'}])

        with self.client.session_transaction() as sess:
            sess['user_id'] = 27
            sess['user_email'] = 'verica.stojanovic@nhmbeo.rs'
            sess['user_role'] = 'sef_odeljenja'
            sess['user_department'] = BIOLOGY
            sess['is_department_head'] = True

        with patch('timesheet_employee_views.get_postgres_connection',
                   lambda **kw: Conn()), \
             patch('timesheet_admin_views.get_postgres_connection',
                   lambda **kw: Conn()):
            r = self.client.post('/api/timesheet/50/reject',
                                 json={'note': '   '},
                                 base_url=self.base_url)
        self.assertEqual(r.status_code, 400)


class EditWindowExpiryTests(unittest.TestCase):
    """After the 24 h editable_until window lapses, the employee's save
    path must refuse the edit and auto-relock the report."""

    def test_save_blocked_when_editable_until_passed(self):
        from timesheet_postgres import save_timesheet_to_postgres, TimesheetErrorType

        captured = []
        class _Cur:
            def __init__(self):
                self._pending = None
            def execute(self, sql, params=None):
                captured.append((sql, params))
                if 'FROM timesheet_reports' in sql and 'edit_window_expired' in sql:
                    # Simulate report found, expired edit window.
                    self._pending = {
                        'id': 1, 'version': 1, 'is_locked': False,
                        'is_verified': False, 'status': 'REJECTED',
                        'editable_until': 'past',
                        'edit_window_expired': True,
                    }
                elif 'UPDATE timesheet_reports' in sql and 'is_locked = TRUE' in sql:
                    self._pending = None
                else:
                    self._pending = None
            def fetchall(self): return [self._pending] if self._pending else []
            def fetchone(self): return self._pending
            def __enter__(self): return self
            def __exit__(self, *a): return False
        class _Conn:
            def cursor(self): return _Cur()
            def commit(self): pass
            def __enter__(self): return self
            def __exit__(self, *a): return False

        with patch('timesheet_postgres.get_pg_connection',
                   lambda **kw: _Conn()):
            result = save_timesheet_to_postgres(
                user_email='x@nhmbeo.rs',
                user_name='X',
                month=3, year=2026,
                daily_data={},
                work_description='',
                organization_unit='',
                position='',
            )

        self.assertFalse(result.success,
                         "save must refuse when editable_until has passed")
        # Must have emitted the auto-relock UPDATE
        relocks = [c for c in captured
                   if 'UPDATE timesheet_reports' in c[0]
                   and 'is_locked = TRUE' in c[0]]
        self.assertTrue(relocks, "expired window must auto-relock the report")


class DirectorNavMenuTests(unittest.TestCase):
    """Verify director sees the cross-department reports link in the navbar."""

    def setUp(self):
        self._prev_csrf = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def tearDown(self):
        museum_app.app.config['WTF_CSRF_ENABLED'] = self._prev_csrf

    def _login_as_director(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_email'] = 'slavko.spasic@nhmbeo.rs'
            sess['user_name'] = 'Славко Спасић'
            sess['user_role'] = 'direktor'
            sess['is_admin'] = False
            sess['user_department'] = 'Директор'
            sess['is_department_head'] = False

    def test_director_nav_shows_admin_timesheet_link(self):
        self._login_as_director()
        response = self.client.get('/', base_url=self.base_url, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        # Director shares the admin nav: direct link to the reports overview,
        # no personal entry form (the director does not fill a monthly report).
        self.assertIn('/admin/timesheet', body)
        self.assertNotIn('Унос радних листа', body)
        # Must NOT show the department-head label (which is scoped).
        self.assertNotIn('Извештаји (одељење)', body)


if __name__ == '__main__':
    unittest.main()
