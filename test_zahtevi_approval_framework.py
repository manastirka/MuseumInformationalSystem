#!/usr/bin/env python3
"""Tests for the unified request-approval framework (operativni moduli).

Covers: per-request approval chains (creator's own step skipped), department
scoping for department heads, 403 for unauthorized approvers, auto-archiving
on final decision (АРХ reference for approved, none for rejected), read-only
archived requests, the approval-queue and archive pages with filters, and the
deferred side effects (procurement enrollment, business-trip execution on
final approval).
"""

import os
import unittest
from datetime import datetime
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-zahtevi-approval')

import app as museum_app  # noqa: F401  (registers blueprints/routes)
import archive_signature_blueprint as asb
import travel_finance_views


GEOLOGY = 'ГЕОЛОШКО ОДЕЉЕЊЕ'
BIOLOGY = 'БИОЛОШКО ОДЕЉЕЊЕ'

EMPLOYEE = {
    'user_id': 10, 'user_email': 'radnik@nhmbeo.rs', 'user_name': 'Радник',
    'user_role': 'employee', 'is_admin': False,
    'user_department': GEOLOGY, 'is_department_head': False,
}
GEOLOGY_HEAD = {
    'user_id': 20, 'user_email': 'sef.geo@nhmbeo.rs', 'user_name': 'Шеф Гео',
    'user_role': 'sef_odeljenja', 'is_admin': False,
    'user_department': GEOLOGY, 'is_department_head': True,
}
BIOLOGY_HEAD = {
    'user_id': 21, 'user_email': 'sef.bio@nhmbeo.rs', 'user_name': 'Шеф Био',
    'user_role': 'sef_odeljenja', 'is_admin': False,
    'user_department': BIOLOGY, 'is_department_head': True,
}
DIRECTOR = {
    'user_id': 30, 'user_email': 'direktor@nhmbeo.rs', 'user_name': 'Директор',
    'user_role': 'direktor', 'is_admin': False,
    'user_department': None, 'is_department_head': False,
}
ADMIN = {
    'user_id': 1, 'user_email': 'admin@nhmbeo.rs', 'user_name': 'Админ',
    'user_role': 'admin', 'is_admin': True,
    'user_department': None, 'is_department_head': False,
}

ZAHTEV_CHAIN = [
    {'role': 'sef_odeljenja', 'label': 'Шеф одељења', 'order': 1},
    {'role': 'direktor', 'label': 'Директор', 'order': 2},
]


class FakeCursor:
    """Minimal cursor recording executed SQL and serving scripted rows."""

    def __init__(self, script):
        # script: list of (matcher_substring, fetchone_value, fetchall_value)
        self._script = script
        self.executed = []
        self._last = (None, None)

    def execute(self, sql, params=None):
        self.executed.append((sql, params))
        for matcher, one, many in self._script:
            if matcher in sql:
                self._last = (one() if callable(one) else one,
                              many() if callable(many) else many)
                return
        self._last = (None, [])

    def fetchone(self):
        return self._last[0]

    def fetchall(self):
        return self._last[1] or []

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor
        self.commit_count = 0

    def cursor(self, *args, **kwargs):
        return self._cursor

    def commit(self):
        self.commit_count += 1

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


# ---------------------------------------------------------------------------
# Unit: chain construction and approval permission
# ---------------------------------------------------------------------------

class ApprovalChainTests(unittest.TestCase):

    def test_employee_gets_full_chain(self):
        chain = asb.build_approval_chain('zahtev', 'employee')
        self.assertEqual([s['role'] for s in chain], ['sef_odeljenja', 'direktor'])

    def test_department_head_creator_skips_own_step(self):
        chain = asb.build_approval_chain('zahtev', 'sef_odeljenja')
        self.assertEqual([s['role'] for s in chain], ['direktor'])

    def test_accounting_head_creator_skips_own_step_in_finance_chain(self):
        chain = asb.build_approval_chain('finansije', 'sef_racunovodstva')
        self.assertEqual([s['role'] for s in chain], ['sef_odeljenja', 'direktor'])

    def test_director_step_is_never_skipped(self):
        chain = asb.build_approval_chain('zahtev', 'direktor')
        self.assertIn('direktor', [s['role'] for s in chain])

    def test_finance_chain_order(self):
        chain = asb.build_approval_chain('finansije', 'employee')
        self.assertEqual(
            [s['role'] for s in chain],
            ['sef_odeljenja', 'sef_racunovodstva', 'direktor'],
        )


class CanApproveRequestTests(unittest.TestCase):

    def test_head_of_same_department_can_approve(self):
        self.assertTrue(asb.can_approve_request(
            'sef_odeljenja', 'zahtev', 0,
            user_department=GEOLOGY, request_department=GEOLOGY,
        ))

    def test_head_of_other_department_cannot_approve(self):
        self.assertFalse(asb.can_approve_request(
            'sef_odeljenja', 'zahtev', 0,
            user_department=BIOLOGY, request_department=GEOLOGY,
        ))

    def test_department_scoping_tolerates_case_and_whitespace(self):
        self.assertTrue(asb.can_approve_request(
            'sef_odeljenja', 'zahtev', 0,
            user_department=f'  {GEOLOGY.lower()} ', request_department=GEOLOGY,
        ))

    def test_request_without_department_stays_with_admin(self):
        self.assertFalse(asb.can_approve_request(
            'sef_odeljenja', 'zahtev', 0,
            user_department=GEOLOGY, request_department='',
        ))
        self.assertTrue(asb.can_approve_request(
            'admin', 'zahtev', 0,
            user_department=None, request_department='',
        ))

    def test_director_cannot_cover_department_head_step(self):
        self.assertFalse(asb.can_approve_request(
            'direktor', 'zahtev', 0,
            user_department=None, request_department=GEOLOGY,
        ))

    def test_director_approves_director_step(self):
        self.assertTrue(asb.can_approve_request('direktor', 'zahtev', 1))

    def test_stored_chain_governs_step_resolution(self):
        # A head-created request stores a chain of just [direktor]: step 0 is
        # the director's, and the (any) department head has no say.
        stored = [{'role': 'direktor', 'label': 'Директор', 'order': 1}]
        self.assertTrue(asb.can_approve_request(
            'direktor', 'zahtev', 0, chain=stored,
        ))
        self.assertFalse(asb.can_approve_request(
            'sef_odeljenja', 'zahtev', 0, chain=stored,
            user_department=GEOLOGY, request_department=GEOLOGY,
        ))

    def test_empty_stored_chain_falls_back_to_constant(self):
        self.assertEqual(
            asb._effective_chain('zahtev', []),
            asb.APPROVAL_CHAINS['zahtev'],
        )
        self.assertEqual(
            asb._effective_chain('zahtev', None),
            asb.APPROVAL_CHAINS['zahtev'],
        )


# ---------------------------------------------------------------------------
# Client plumbing
# ---------------------------------------------------------------------------

class _ClientTestCase(unittest.TestCase):

    def setUp(self):
        museum_app.app.config['TESTING'] = True
        csrf_was_enabled = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.addCleanup(
            museum_app.app.config.__setitem__, 'WTF_CSRF_ENABLED', csrf_was_enabled
        )
        self.client = museum_app.app.test_client()

    def get(self, *args, **kwargs):
        kwargs.setdefault('base_url', 'https://localhost')
        return self.client.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        kwargs.setdefault('base_url', 'https://localhost')
        return self.client.post(*args, **kwargs)

    def login(self, who):
        with self.client.session_transaction() as sess:
            for key, value in who.items():
                sess[key] = value

    def use_db(self, script):
        cursor = FakeCursor(script)
        connection = FakeConnection(cursor)
        db_patch = patch.object(
            asb, 'get_postgres_connection', lambda **kwargs: connection
        )
        db_patch.start()
        self.addCleanup(db_patch.stop)
        return cursor


def _approve_row(*, request_type='zahtev', status='pending', step=0,
                 chain=None, creator='radnik@nhmbeo.rs', department=GEOLOGY,
                 request_data=None):
    # row: request_type, status, current_approval_step, approval_chain,
    #      created_by_email, title, created_by_department, request_data,
    #      created_by_name
    return (request_type, status, step,
            chain if chain is not None else list(ZAHTEV_CHAIN),
            creator, 'Тест захтев', department, request_data or {}, 'Радник')


# ---------------------------------------------------------------------------
# Approval flow: scoping, 403, auto-archive
# ---------------------------------------------------------------------------

class ApprovalFlowTests(_ClientTestCase):

    def _script(self, row):
        return [
            ("FROM archive_requests WHERE id = %s", row, None),
            ("UPDATE approval_signatures", None, None),
            ("UPDATE archive_requests", None, None),
            ("COALESCE(MAX(", (0,), None),
            ("INSERT INTO request_history", None, None),
            ("INSERT INTO user_notifications", None, None),
        ]

    def test_head_of_same_department_approves_first_step(self):
        cursor = self.use_db(self._script(_approve_row()))
        self.login(GEOLOGY_HEAD)
        response = self.post('/api/archive/requests/1/approve', json={'comments': ''})
        body = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertFalse(body['final'])
        update_sqls = [sql for sql, _ in cursor.executed if 'UPDATE archive_requests' in sql]
        self.assertTrue(any("status = 'in_review'" in s for s in update_sqls))

    def test_head_of_other_department_gets_403(self):
        cursor = self.use_db(self._script(_approve_row()))
        self.login(BIOLOGY_HEAD)
        response = self.post('/api/archive/requests/1/approve', json={'comments': ''})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(any('UPDATE archive_requests' in sql for sql, _ in cursor.executed))

    def test_employee_gets_403(self):
        self.use_db(self._script(_approve_row()))
        self.login(EMPLOYEE)
        response = self.post('/api/archive/requests/1/approve', json={'comments': ''})
        self.assertEqual(response.status_code, 403)

    def test_final_approval_auto_archives_with_reference(self):
        row = _approve_row(status='in_review', step=1)
        cursor = self.use_db(self._script(row))
        self.login(DIRECTOR)
        response = self.post('/api/archive/requests/1/approve', json={'comments': ''})
        body = response.get_json()
        self.assertTrue(body['success'])
        self.assertTrue(body['final'])
        self.assertTrue(body['archive_reference'].startswith('АРХ-'))
        archive_updates = [
            (sql, params) for sql, params in cursor.executed
            if "status = 'archived'" in sql
        ]
        self.assertEqual(len(archive_updates), 1)
        self.assertIn('archive_reference', archive_updates[0][0])
        self.assertIn(body['archive_reference'], archive_updates[0][1])

    def test_head_created_request_goes_straight_to_director(self):
        # Stored chain has only the director step: the director's approval of
        # step 0 finalizes the request.
        row = _approve_row(
            status='pending', step=0,
            chain=[{'role': 'direktor', 'label': 'Директор', 'order': 1}],
            creator='sef.geo@nhmbeo.rs',
        )
        cursor = self.use_db(self._script(row))
        self.login(DIRECTOR)
        response = self.post('/api/archive/requests/1/approve', json={'comments': ''})
        body = response.get_json()
        self.assertTrue(body['success'])
        self.assertTrue(body['final'])
        self.assertTrue(any("final_decision = 'approved'" in sql for sql, _ in cursor.executed))

    def test_reject_requires_reason_and_auto_archives_without_reference(self):
        row = _approve_row()
        cursor = self.use_db(self._script(row))
        self.login(GEOLOGY_HEAD)

        response = self.post('/api/archive/requests/1/reject', json={'comments': ''})
        self.assertEqual(response.status_code, 400)

        response = self.post('/api/archive/requests/1/reject', json={'comments': 'Непотпун захтев'})
        body = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        archive_updates = [
            sql for sql, _ in cursor.executed if "status = 'archived'" in sql
        ]
        self.assertEqual(len(archive_updates), 1)
        self.assertNotIn('archive_reference', archive_updates[0])

    def test_archived_request_is_read_only_for_approve_and_reject(self):
        row = _approve_row(status='archived', step=2)
        self.use_db(self._script(row))
        self.login(ADMIN)
        response = self.post('/api/archive/requests/1/approve', json={'comments': ''})
        self.assertEqual(response.status_code, 400)
        response = self.post('/api/archive/requests/1/reject', json={'comments': 'x'})
        self.assertEqual(response.status_code, 400)

    def test_archived_request_rejects_new_comments(self):
        comment_row = ('archived', 'radnik@nhmbeo.rs', 'zahtev', 2,
                       list(ZAHTEV_CHAIN), GEOLOGY)
        cursor = self.use_db([
            ("FROM archive_requests WHERE id = %s", comment_row, None),
        ])
        self.login(ADMIN)
        response = self.post('/api/archive/requests/1/comment', json={'comment': 'проба'})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(
            any('INSERT INTO request_comments' in sql for sql, _ in cursor.executed)
        )

    def test_final_approval_executes_business_trip_side_effects(self):
        field_trip = {
            'start_date': '2026-08-01', 'end_date': '2026-08-03',
            'location': 'Ђердап', 'purpose': 'Теренски рад',
            'vehicle_id': '2', 'update_timesheet': True,
        }
        row = _approve_row(
            request_type='terenska_aktivnost', status='in_review', step=2,
            chain=list(asb.APPROVAL_CHAINS['terenska_aktivnost']),
            request_data={'field_trip': field_trip},
        )
        cursor = self.use_db(self._script(row))
        self.login(ADMIN)
        with patch.object(
            travel_finance_views, 'execute_field_trip',
            return_value={'success': True, 'vehicle_reserved': True, 'timesheet_updated': True},
        ) as executor:
            response = self.post('/api/archive/requests/1/approve', json={'comments': ''})
        body = response.get_json()
        self.assertTrue(body['success'])
        self.assertTrue(body['final'])
        executor.assert_called_once_with(
            field_trip, user_name='Радник', user_email='radnik@nhmbeo.rs',
        )
        self.assertTrue(body['side_effects']['vehicle_reserved'])
        self.assertTrue(
            any("'executed'" in sql for sql, _ in cursor.executed),
            'side-effect outcome must be recorded in request_history',
        )

    def test_intermediate_approval_runs_no_side_effects(self):
        row = _approve_row(
            request_type='terenska_aktivnost', status='pending', step=0,
            chain=list(asb.APPROVAL_CHAINS['terenska_aktivnost']),
            request_data={'field_trip': {'vehicle_id': '2'}},
        )
        self.use_db(self._script(row))
        self.login(GEOLOGY_HEAD)
        with patch.object(travel_finance_views, 'execute_field_trip') as executor:
            response = self.post('/api/archive/requests/1/approve', json={'comments': ''})
        self.assertTrue(response.get_json()['success'])
        executor.assert_not_called()


# ---------------------------------------------------------------------------
# Creation: chain snapshot and department from session
# ---------------------------------------------------------------------------

class RequestCreationTests(_ClientTestCase):

    def _create(self, who, payload):
        cursor = self.use_db([
            ("INSERT INTO archive_requests", (7,), None),
            ("INSERT INTO approval_signatures", None, None),
            ("INSERT INTO request_history", None, None),
        ])
        self.login(who)
        response = self.post('/api/archive/requests', json=payload)
        return response, cursor

    def test_employee_request_stores_full_chain_and_session_department(self):
        response, cursor = self._create(EMPLOYEE, {
            'request_type': 'zahtev', 'subtype': 'godisnji_odmor',
            'title': 'Годишњи одмор', 'request_data': {'broj_dana': 5},
        })
        self.assertTrue(response.get_json()['success'])
        insert_params = next(
            params for sql, params in cursor.executed
            if 'INSERT INTO archive_requests' in sql
        )
        chain_json = insert_params[11]
        self.assertIn('sef_odeljenja', chain_json)
        self.assertIn('direktor', chain_json)
        self.assertEqual(insert_params[9], GEOLOGY)

    def test_department_head_request_skips_own_step(self):
        response, cursor = self._create(GEOLOGY_HEAD, {
            'request_type': 'zahtev', 'subtype': 'slobodan_dan',
            'title': 'Слободан дан',
        })
        self.assertTrue(response.get_json()['success'])
        insert_params = next(
            params for sql, params in cursor.executed
            if 'INSERT INTO archive_requests' in sql
        )
        chain_json = insert_params[11]
        self.assertNotIn('sef_odeljenja', chain_json)
        self.assertIn('direktor', chain_json)
        signature_inserts = [
            params for sql, params in cursor.executed
            if 'INSERT INTO approval_signatures' in sql
        ]
        self.assertEqual(len(signature_inserts), 1)
        self.assertEqual(signature_inserts[0][1], 'direktor')


# ---------------------------------------------------------------------------
# Pages: approval queue and archive with filters
# ---------------------------------------------------------------------------

def _pending_row(req_id, title, department, creator='radnik@nhmbeo.rs',
                 request_type='zahtev', step=0, chain=None):
    # row: id, title, request_type, subtype, created_by_name, created_at,
    #      priority, current_approval_step, approval_chain,
    #      created_by_department, created_by_email
    return (req_id, title, request_type, 'godisnji_odmor', 'Радник',
            datetime(2026, 7, 1, 10, 0), 'normal', step,
            chain if chain is not None else list(ZAHTEV_CHAIN),
            department, creator)


class ApprovalQueuePageTests(_ClientTestCase):

    def test_employee_is_redirected(self):
        self.login(EMPLOYEE)
        response = self.get('/zahtevi/odobravanje')
        self.assertEqual(response.status_code, 302)

    def test_department_head_sees_only_own_department(self):
        rows = [
            _pending_row(1, 'Захтев Гео', GEOLOGY),
            _pending_row(2, 'Захтев Био', BIOLOGY),
            _pending_row(3, 'Сопствени захтев', GEOLOGY, creator='sef.geo@nhmbeo.rs'),
        ]
        self.use_db([
            ("WHERE status IN ('pending', 'in_review')", None, rows),
        ])
        self.login(GEOLOGY_HEAD)
        response = self.get('/zahtevi/odobravanje')
        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn('Захтев Гео', page)
        self.assertNotIn('Захтев Био', page)
        self.assertNotIn('Сопствени захтев', page)

    def test_pending_api_scopes_by_department(self):
        rows = [
            _pending_row(1, 'Захтев Гео', GEOLOGY),
            _pending_row(2, 'Захтев Био', BIOLOGY),
        ]
        self.use_db([
            ("WHERE status IN ('pending', 'in_review')", None, rows),
        ])
        self.login(GEOLOGY_HEAD)
        response = self.get('/api/archive/pending')
        body = response.get_json()
        self.assertTrue(body['success'])
        self.assertEqual([req['id'] for req in body['pending']], [1])


class ArchivePageTests(_ClientTestCase):

    ARCHIVED_ROW = (
        5, 'zahtev', 'godisnji_odmor', 'Годишњи одмор', 'Радник',
        GEOLOGY, 'approved', datetime(2026, 7, 1, 12, 0), 'АРХ-2026-00001', 2026,
    )

    def _script(self, rows):
        return [
            ("SELECT DISTINCT archive_year", None, [(2026,)]),
            ("FROM archive_requests", None, rows),
        ]

    def test_archive_page_renders_for_employee(self):
        cursor = self.use_db(self._script([self.ARCHIVED_ROW]))
        self.login(EMPLOYEE)
        response = self.get('/zahtevi/arhiva')
        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn('АРХ-2026-00001', page)
        self.assertIn('Одобрен', page)
        main_sql, main_params = next(
            (sql, params) for sql, params in cursor.executed
            if "status = 'archived'" in sql and 'DISTINCT' not in sql
        )
        self.assertIn('created_by_email = %s', main_sql)
        self.assertIn(EMPLOYEE['user_email'], main_params)

    def test_archive_page_filters_by_type_year_and_submitter(self):
        cursor = self.use_db(self._script([]))
        self.login(ADMIN)
        response = self.get('/zahtevi/arhiva?tip=zahtev&godina=2026&podnosilac=Радник')
        self.assertEqual(response.status_code, 200)
        main_sql, main_params = next(
            (sql, params) for sql, params in cursor.executed
            if "status = 'archived'" in sql and 'DISTINCT' not in sql
        )
        self.assertIn('request_type = %s', main_sql)
        self.assertIn('archive_year = %s', main_sql)
        self.assertIn('ILIKE', main_sql)
        self.assertIn('zahtev', main_params)
        self.assertIn(2026, main_params)
        self.assertIn('%Радник%', main_params)

    def test_department_head_sees_department_archive(self):
        cursor = self.use_db(self._script([self.ARCHIVED_ROW]))
        self.login(GEOLOGY_HEAD)
        response = self.get('/zahtevi/arhiva')
        self.assertEqual(response.status_code, 200)
        main_sql, main_params = next(
            (sql, params) for sql, params in cursor.executed
            if "status = 'archived'" in sql and 'DISTINCT' not in sql
        )
        self.assertIn('created_by_department', main_sql)
        self.assertIn(GEOLOGY, main_params)


# ---------------------------------------------------------------------------
# Procurement enrollment and the restricted direct field-trip API
# ---------------------------------------------------------------------------

class ProcurementEnrollmentTests(_ClientTestCase):

    def test_nabavka_save_enrolls_into_framework(self):
        cursor = FakeCursor([
            ("INSERT INTO procurement_requests", {'id': 5}, None),
            ("INSERT INTO archive_requests", {'id': 9}, None),
            ("INSERT INTO approval_signatures", None, None),
            ("INSERT INTO request_history", None, None),
            ("UPDATE procurement_requests SET archive_request_id", None, None),
        ])
        connection = FakeConnection(cursor)
        self.login(EMPLOYEE)
        with patch.dict(os.environ, {'DATABASE_URL': 'postgresql://test/test'}), \
                patch('psycopg.connect', lambda *a, **kw: connection):
            response = self.post('/api/nabavka/save', json={
                'datum': '2026-07-07', 'podnosilac': 'Радник',
                'items': [{'description': 'Микроскоп', 'quantity': 1}],
                'totalEstimated': 120000,
            })
        body = response.get_json()
        self.assertTrue(body['success'])
        self.assertEqual(body['id'], 5)
        self.assertEqual(body['archive_request_id'], 9)

        archive_insert = next(
            params for sql, params in cursor.executed
            if 'INSERT INTO archive_requests' in sql
        )
        self.assertEqual(archive_insert[0], 'finansije')
        self.assertEqual(archive_insert[1], 'nabavka')
        self.assertEqual(archive_insert[9], GEOLOGY)

        fk_update = next(
            params for sql, params in cursor.executed
            if 'UPDATE procurement_requests SET archive_request_id' in sql
        )
        self.assertEqual(fk_update, (9, 5))


class DirectFieldTripApiTests(_ClientTestCase):

    def test_employee_cannot_create_field_trip_directly(self):
        self.login(EMPLOYEE)
        response = self.post('/api/field-trip/create', json={
            'vehicle_id': '2', 'start_date': '2026-08-01', 'end_date': '2026-08-02',
        })
        self.assertEqual(response.status_code, 403)
        self.assertFalse(response.get_json()['success'])


if __name__ == '__main__':
    unittest.main()
