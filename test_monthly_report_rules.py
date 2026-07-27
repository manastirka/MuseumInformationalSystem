"""Bullet-proof spec tests for the monthly report (radna lista) workflow.

Encodes the five business rules for mesečni izveštaji:

1. ROK: the report for month M is filled during M and until the 10th of
   month M+1 at 23:59; after that entry LOCKS (date-based, on top of the
   existing status locks).
2. RUTIRANJE: on submission the report reaches the department head of the
   employee's department and (where the policy says so) the director; both
   see submitted reports in their accounts.
3. VIDLJIVOST/OVLAŠĆENJA: verification is department-scoped — a head only
   verifies their own department and never their own report; the director
   verifies head reports and head-less departments; admin verifies all.
   EVERY approve path must obey the same policy.
4. VRAĆANJE NA DORADU: a bad SUBMITTED report is returned (REJECTED) with a
   note; the employee fixes and resubmits without an unlock request.
5. EXTRA DAN: after a return the employee gets a 24h window, only for that
   returned month; when it expires the report locks again and an unlock
   request is required.

Tests marked SPEC-RED document behavior that is REQUIRED but not yet
implemented (they are the reproducing tests for the fix wave). The rest
lock in behavior that already works so regressions cannot sneak in.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-monthly-rules')
os.environ.setdefault('DATABASE_URL', 'postgresql://test:test@localhost:5432/test')

import unittest
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import flask


# =============================================================================
# Shared fakes (repo idiom: recording cursor + context-manager connection)
# =============================================================================

class RecordingCursor:
    """Cursor that records executed SQL and replays queued fetch results."""

    def __init__(self, fetchone_queue=None, fetchall_queue=None):
        self.executed = []
        self._fetchone = list(fetchone_queue or [])
        self._fetchall = list(fetchall_queue or [])
        self.rowcount = 1

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchone(self):
        return self._fetchone.pop(0) if self._fetchone else None

    def fetchall(self):
        return self._fetchall.pop(0) if self._fetchall else []

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def conn_cm_for(cursor):
    conn = MagicMock()
    conn.cursor.return_value = cursor

    @contextmanager
    def _cm(*args, **kwargs):
        yield conn

    return _cm


def executed_sql(cursor):
    return '\n'.join(q for q, _ in cursor.executed)


@contextmanager
def request_ctx(path='/', method='GET', json_body=None):
    app = flask.Flask(__name__)
    app.secret_key = 'test-secret'
    kwargs = {'method': method}
    if json_body is not None:
        kwargs['json'] = json_body
    with app.test_request_context(path, **kwargs):
        yield


def fixed_now(year, month, day, hour=12, minute=0):
    return datetime(year, month, day, hour, minute, 0)


class _FixedDatetime(datetime):
    """datetime subclass whose now() is frozen (repo idiom from
    test_timesheet_status.py — timesheet_postgres calls datetime.now())."""

    _frozen = None

    @classmethod
    def freeze(cls, value):
        cls._frozen = value
        return cls

    @classmethod
    def now(cls, tz=None):
        if tz is not None:
            return cls._frozen.replace(tzinfo=tz)
        return cls._frozen


# =============================================================================
# PRAVILO 1 — ROK: unos/podnošenje do 10. sledećeg meseca  [SPEC-RED]
# =============================================================================

class TestDeadlineSubmitRule(unittest.TestCase):
    """can_submit_for_review: dozvoljeno tokom meseca M i 1-10. u M+1."""

    def _can_submit(self, today, month, year):
        import timesheet_postgres as tp
        with patch.object(tp, 'datetime', _FixedDatetime.freeze(today)):
            return tp.can_submit_for_review(month, year)

    def test_allowed_during_report_month(self):
        ok, _ = self._can_submit(fixed_now(2026, 6, 20), 6, 2026)
        self.assertTrue(ok)

    def test_allowed_first_of_next_month(self):
        ok, _ = self._can_submit(fixed_now(2026, 7, 1), 6, 2026)
        self.assertTrue(ok)

    def test_allowed_on_the_10th_of_next_month(self):
        ok, _ = self._can_submit(fixed_now(2026, 7, 10, 23, 59), 6, 2026)
        self.assertTrue(ok)

    def test_blocked_on_the_11th_of_next_month(self):
        # SPEC-RED: enforcement is currently disabled (always True).
        ok, msg = self._can_submit(fixed_now(2026, 7, 11, 0, 5), 6, 2026)
        self.assertFalse(ok, 'Podnošenje 11. u sledećem mesecu mora biti blokirano')
        self.assertTrue(msg)

    def test_blocked_months_later(self):
        ok, _ = self._can_submit(fixed_now(2026, 7, 3), 4, 2026)
        self.assertFalse(ok, 'Izveštaj za april ne sme da se podnosi u julu')

    def test_blocked_for_future_month(self):
        ok, _ = self._can_submit(fixed_now(2026, 7, 3), 9, 2026)
        self.assertFalse(ok, 'Izveštaj za budući mesec ne sme da se podnosi')

    def test_december_rollover_allowed_until_jan_10(self):
        ok, _ = self._can_submit(fixed_now(2027, 1, 10), 12, 2026)
        self.assertTrue(ok)

    def test_december_rollover_blocked_jan_11(self):
        ok, _ = self._can_submit(fixed_now(2027, 1, 11), 12, 2026)
        self.assertFalse(ok)


class TestDeadlineEditRule(unittest.TestCase):
    """can_edit_timesheet_by_status: status blokade + datumski prozor."""

    def _can_edit(self, today, month, year, status):
        import timesheet_postgres as tp
        with patch.object(tp, 'datetime', _FixedDatetime.freeze(today)):
            return tp.can_edit_timesheet_by_status(month, year, status)

    def test_submitted_always_blocked(self):
        ok, _ = self._can_edit(fixed_now(2026, 6, 5), 6, 2026, 'SUBMITTED')
        self.assertFalse(ok)

    def test_approved_always_blocked(self):
        ok, _ = self._can_edit(fixed_now(2026, 6, 5), 6, 2026, 'APPROVED')
        self.assertFalse(ok)

    def test_draft_editable_during_month(self):
        ok, _ = self._can_edit(fixed_now(2026, 6, 5), 6, 2026, 'DRAFT')
        self.assertTrue(ok)

    def test_draft_editable_until_10th_next_month(self):
        ok, _ = self._can_edit(fixed_now(2026, 7, 10), 6, 2026, 'DRAFT')
        self.assertTrue(ok)

    def test_draft_blocked_11th_next_month(self):
        # SPEC-RED: date window is currently disabled.
        ok, msg = self._can_edit(fixed_now(2026, 7, 11), 6, 2026, 'DRAFT')
        self.assertFalse(ok, 'Unos 11. u sledećem mesecu mora biti zaključan')
        self.assertTrue(msg)

    def test_rejected_blocked_after_deadline_without_window(self):
        # Vraćeni izveštaj van 24h prozora podleže istom roku (prozor se
        # proverava na save-sloju preko editable_until).
        ok, _ = self._can_edit(fixed_now(2026, 7, 20), 5, 2026, 'REJECTED')
        self.assertFalse(ok)

    def test_december_rollover(self):
        ok, _ = self._can_edit(fixed_now(2027, 1, 9), 12, 2026, 'DRAFT')
        self.assertTrue(ok)


class TestSaveEnforcesDeadline(unittest.TestCase):
    """save_timesheet_to_postgres mora da poštuje rok — direktan POST na
    /api/timesheet/save ne sme da zaobiđe pravilo 1.  [SPEC-RED]"""

    def _save(self, today, existing_row, month, year):
        import timesheet_postgres as tp
        cursor = RecordingCursor(fetchone_queue=[existing_row])
        with patch.object(tp, 'get_pg_connection', conn_cm_for(cursor)), \
                patch.object(tp, 'datetime', _FixedDatetime.freeze(today)):
            result = tp.save_timesheet_to_postgres(
                user_email='zaposleni@nhmbeo.rs',
                user_name='Test Zaposleni',
                month=month,
                year=year,
                daily_data={'1': {'rad_na_mestu': 8}},
                work_description='opis',
                organization_unit='Biologija',
                position='kustos',
            )
        return result, cursor

    def test_save_existing_draft_blocked_after_deadline(self):
        row = {
            'id': 10, 'version': 1, 'is_locked': False, 'is_verified': False,
            'status': 'DRAFT', 'editable_until': None, 'edit_window_expired': False,
        }
        result, cursor = self._save(fixed_now(2026, 7, 15), row, 5, 2026)
        self.assertFalse(
            result.success,
            'Snimanje DRAFT izveštaja za maj 15. jula mora biti odbijeno (rok 10.)',
        )
        self.assertNotIn('UPDATE timesheet_reports', executed_sql(cursor).replace('\n', ' '),
                         'Posle isteka roka ne sme biti UPDATE-a podataka')

    def test_save_new_report_blocked_after_deadline(self):
        result, cursor = self._save(fixed_now(2026, 7, 15), None, 4, 2026)
        self.assertFalse(
            result.success,
            'Kreiranje izveštaja za april u julu mora biti odbijeno',
        )
        self.assertNotIn('INSERT INTO timesheet_reports', executed_sql(cursor),
                         'Posle isteka roka ne sme biti INSERT-a')

    def test_save_rejected_with_active_window_allowed_after_deadline(self):
        """Pravilo 5: extra dan (editable_until) nadjačava rok za TAJ mesec."""
        future = datetime.now(timezone.utc) + timedelta(hours=12)
        row = {
            'id': 11, 'version': 3, 'is_locked': False, 'is_verified': False,
            'status': 'REJECTED', 'editable_until': future,
            'edit_window_expired': False,
        }
        cursor = RecordingCursor(fetchone_queue=[
            row,
            {'version': 4},  # UPDATE ... RETURNING version
        ])
        import timesheet_postgres as tp
        with patch.object(tp, 'get_pg_connection', conn_cm_for(cursor)), \
                patch.object(tp, 'datetime', _FixedDatetime.freeze(fixed_now(2026, 7, 15))):
            result = tp.save_timesheet_to_postgres(
                user_email='zaposleni@nhmbeo.rs',
                user_name='Test Zaposleni',
                month=5, year=2026,
                daily_data={'1': {'rad_na_mestu': 8}},
                work_description='dopuna po vraćanju',
                organization_unit='Biologija',
                position='kustos',
            )
        self.assertTrue(
            result.success,
            'Vraćeni izveštaj sa aktivnim 24h prozorom mora biti izmenjiv i posle roka: '
            + (result.error.message if result.error else ''),
        )

    def test_save_current_month_allowed(self):
        cursor = RecordingCursor(fetchone_queue=[
            None,
            {'id': 12, 'version': 1},  # INSERT ... RETURNING id, version
        ])
        import timesheet_postgres as tp
        with patch.object(tp, 'get_pg_connection', conn_cm_for(cursor)), \
                patch.object(tp, 'datetime', _FixedDatetime.freeze(fixed_now(2026, 7, 3))):
            result = tp.save_timesheet_to_postgres(
                user_email='zaposleni@nhmbeo.rs',
                user_name='Test Zaposleni',
                month=7, year=2026,
                daily_data={'1': {'rad_na_mestu': 8}},
                work_description='tekući mesec',
                organization_unit='Biologija',
                position='kustos',
            )
        self.assertTrue(result.success)

    def test_save_previous_month_before_deadline_allowed(self):
        cursor = RecordingCursor(fetchone_queue=[
            None,
            {'id': 13, 'version': 1},
        ])
        import timesheet_postgres as tp
        with patch.object(tp, 'get_pg_connection', conn_cm_for(cursor)), \
                patch.object(tp, 'datetime', _FixedDatetime.freeze(fixed_now(2026, 7, 9))):
            result = tp.save_timesheet_to_postgres(
                user_email='zaposleni@nhmbeo.rs',
                user_name='Test Zaposleni',
                month=6, year=2026,
                daily_data={'1': {'rad_na_mestu': 8}},
                work_description='jun pre roka',
                organization_unit='Biologija',
                position='kustos',
            )
        self.assertTrue(result.success)


# =============================================================================
# PRAVILA 2 i 3 — matrica ovlašćenja za verifikaciju (lock-in postojećeg)
# =============================================================================

HEADS = {'Biologija': 'sef.bio@nhmbeo.rs', 'Pravna služba': 'sef.pravna@nhmbeo.rs'}


def _sess(role, email, department='', is_head=False):
    return {
        'user_role': role,
        'user_email': email,
        'user_department': department,
        'is_department_head': is_head,
    }


class TestVerificationMatrix(unittest.TestCase):
    def _can(self, sess, dept, target_email, heads=HEADS):
        import timesheet_admin_views as av
        return av.can_user_verify_report_for_department(
            sess, dept, target_employee_email=target_email, department_heads=heads,
        )

    def test_admin_verifies_everything(self):
        self.assertTrue(self._can(
            _sess('admin', 'admin@nhmbeo.rs'), 'Biologija', 'x@nhmbeo.rs'))

    def test_head_verifies_own_department_employee(self):
        self.assertTrue(self._can(
            _sess('sef_odeljenja', 'sef.bio@nhmbeo.rs', 'Biologija', True),
            'Biologija', 'zaposleni@nhmbeo.rs'))

    def test_head_cannot_verify_other_department(self):
        self.assertFalse(self._can(
            _sess('sef_odeljenja', 'sef.bio@nhmbeo.rs', 'Biologija', True),
            'Pravna služba', 'pravnik@nhmbeo.rs'))

    def test_head_cannot_verify_own_report(self):
        self.assertFalse(self._can(
            _sess('sef_odeljenja', 'sef.bio@nhmbeo.rs', 'Biologija', True),
            'Biologija', 'sef.bio@nhmbeo.rs'))

    def test_director_verifies_headless_department(self):
        self.assertTrue(self._can(
            _sess('direktor', 'direktor@nhmbeo.rs'), 'Edukacija', 'edu@nhmbeo.rs'))

    def test_director_cannot_verify_employee_of_headed_department(self):
        self.assertFalse(self._can(
            _sess('direktor', 'direktor@nhmbeo.rs'), 'Biologija', 'zaposleni@nhmbeo.rs'))

    def test_director_verifies_heads_own_report(self):
        self.assertTrue(self._can(
            _sess('direktor', 'direktor@nhmbeo.rs'), 'Biologija', 'sef.bio@nhmbeo.rs'))

    def test_director_cannot_verify_own_report(self):
        self.assertFalse(self._can(
            _sess('direktor', 'direktor@nhmbeo.rs'), 'Edukacija', 'direktor@nhmbeo.rs'))

    def test_plain_employee_never_verifies(self):
        self.assertFalse(self._can(
            _sess('employee', 'zaposleni@nhmbeo.rs', 'Biologija'),
            'Biologija', 'kolega@nhmbeo.rs'))

    def test_director_denied_without_heads_context(self):
        self.assertFalse(self._can(
            _sess('direktor', 'direktor@nhmbeo.rs'), 'Biologija', 'x@nhmbeo.rs',
            heads=None))


class TestHeadsMapNormalization(unittest.TestCase):
    """Ime odseka ne sme da zavisi od velikih/malih slova ili razmaka —
    inače direktor 'ne vidi' šefa i preuzima tuđe izveštaje.  [SPEC-RED]"""

    def test_department_name_case_mismatch_still_finds_head(self):
        import timesheet_admin_views as av
        # employee_profiles.department = 'BIOLOGIJA', users/departments = 'Biologija'
        allowed = av.can_user_verify_report_for_department(
            _sess('direktor', 'direktor@nhmbeo.rs'),
            'BIOLOGIJA',
            target_employee_email='zaposleni@nhmbeo.rs',
            department_heads={'Biologija': 'sef.bio@nhmbeo.rs'},
        )
        self.assertFalse(
            allowed,
            'Direktor ne sme da overi zaposlenog iz odseka sa šefom samo zato '
            'što se ime odseka razlikuje u velikim/malim slovima',
        )

    def test_head_scope_survives_case_mismatch(self):
        import timesheet_admin_views as av
        allowed = av.can_user_verify_report_for_department(
            _sess('sef_odeljenja', 'sef.bio@nhmbeo.rs', 'Biologija', True),
            'BIOLOGIJA',
            target_employee_email='zaposleni@nhmbeo.rs',
            department_heads={'Biologija': 'sef.bio@nhmbeo.rs'},
        )
        self.assertTrue(
            allowed,
            'Šef mora da overi svoj odsek i kada se ime razlikuje u case-u',
        )


# =============================================================================
# PRAVILO 3 — sekundarna approve ruta mora da poštuje istu politiku [SPEC-RED]
# =============================================================================

class TestSecondaryApproveWritesVerifierColumns(unittest.TestCase):
    """timesheet_postgres.approve_timesheet mora da upiše verified_by /
    verified_at / verified_role i očisti editable_until — kao primarna ruta."""

    def test_approve_sets_verified_columns_and_clears_window(self):
        import timesheet_postgres as tp
        cursor = RecordingCursor(fetchone_queue=[
            {'id': 5, 'status': 'SUBMITTED'},
        ])
        with patch.object(tp, 'get_pg_connection', conn_cm_for(cursor)):
            result = tp.approve_timesheet(5, 'admin@nhmbeo.rs')
        self.assertTrue(result.success)
        sql = executed_sql(cursor)
        self.assertIn('verified_by', sql,
                      'approve_timesheet mora da upiše verified_by (Word izvoz i '
                      'audit čitaju te kolone)')
        self.assertIn('verified_at', sql)
        self.assertIn('editable_until', sql,
                      'approve_timesheet mora da očisti editable_until da odobren '
                      'izveštaj ne zadrži stari 24h prozor')


class TestSecondaryApproveRoutePolicy(unittest.TestCase):
    """POST /api/timesheet/<id>/approve (direktor) mora da prođe kroz
    can_user_verify_report_for_department, ne sme da zaobiđe podelu
    šef-vs-direktor.  [SPEC-RED]"""

    def _post_as_director(self):
        import app as museum_app
        import timesheet_postgres as tp
        import timesheet_admin_views as av

        client = museum_app.app.test_client()
        with client.session_transaction() as sess:
            sess['user_id'] = 601
            sess['user'] = 'direktor@nhmbeo.rs'
            sess['user_email'] = 'direktor@nhmbeo.rs'
            sess['user_name'] = 'Direktor'
            sess['user_role'] = 'direktor'
            sess['user_department'] = ''
            sess['is_department_head'] = False

        approve_spy = MagicMock(return_value=tp.TimesheetResult.ok({
            'report_id': 7, 'status': 'APPROVED', 'message': 'ok'}))

        lookup_cursor = RecordingCursor(fetchone_queue=[
            # _lookup_report_department → (department, employee_email)
            {'employee_department': 'Biologija',
             'employee_email': 'zaposleni@nhmbeo.rs'},
        ], fetchall_queue=[
            # _get_department_heads
            [{'department': 'Biologija', 'head_email': 'sef.bio@nhmbeo.rs'}],
        ])

        with patch.object(tp, 'approve_timesheet', approve_spy), \
                patch.object(av, 'get_postgres_connection',
                             conn_cm_for(lookup_cursor), create=True), \
                patch('timesheet_employee_views.get_postgres_connection',
                      conn_cm_for(lookup_cursor)), \
                patch('timesheet_employee_views.approve_timesheet',
                      approve_spy, create=True):
            resp = client.post('/api/timesheet/7/approve',
                               base_url='https://localhost')
        return resp, approve_spy

    def test_director_cannot_approve_headed_department_employee_via_secondary_route(self):
        resp, approve_spy = self._post_as_director()
        payload = resp.get_json(silent=True) or {}
        approved = approve_spy.called and (resp.status_code == 200
                                           and payload.get('success', True))
        self.assertFalse(
            approved,
            'Sekundarna approve ruta je dozvolila direktoru da overi zaposlenog '
            'iz odseka koji ima šefa — mora da važi ista politika kao na '
            'primarnoj ruti',
        )


# =============================================================================
# PRAVILO 4 — vraćanje na doradu + poništavanje overe
# =============================================================================

class TestRejectFlow(unittest.TestCase):
    def test_reject_submitted_opens_24h_window(self):
        import timesheet_postgres as tp
        cursor = RecordingCursor(fetchone_queue=[
            {'id': 5, 'status': 'SUBMITTED'},
        ])
        with patch.object(tp, 'get_pg_connection', conn_cm_for(cursor)):
            result = tp.reject_timesheet(5, 'sef.bio@nhmbeo.rs', 'Dopuniti opis')
        self.assertTrue(result.success)
        sql = executed_sql(cursor)
        self.assertIn("status = 'REJECTED'", sql)
        self.assertIn('is_locked = FALSE', sql)
        self.assertIn("editable_until = NOW() + INTERVAL '24 hours'", sql)
        self.assertIn('rejection_note', sql)
        self.assertIn('timesheet_status_history', sql)

    def test_reject_requires_submitted_status(self):
        import timesheet_postgres as tp
        for status in ('DRAFT', 'APPROVED', 'REJECTED'):
            cursor = RecordingCursor(fetchone_queue=[{'id': 5, 'status': status}])
            with patch.object(tp, 'get_pg_connection', conn_cm_for(cursor)):
                result = tp.reject_timesheet(5, 'sef.bio@nhmbeo.rs', 'x')
            self.assertFalse(result.success, f'reject iz statusa {status} mora pasti')

    def test_reject_requires_note(self):
        """Vraćanje bez obrazloženja je zabranjeno — zaposleni mora da zna
        šta da ispravi.  [SPEC-RED ako prolazi bez napomene]"""
        import timesheet_postgres as tp
        cursor = RecordingCursor(fetchone_queue=[{'id': 5, 'status': 'SUBMITTED'}])
        with patch.object(tp, 'get_pg_connection', conn_cm_for(cursor)):
            result = tp.reject_timesheet(5, 'sef.bio@nhmbeo.rs', '   ')
        self.assertFalse(result.success,
                         'Vraćanje bez napomene mora biti odbijeno')


class TestRevokeVerificationHonest(unittest.TestCase):
    """Poništavanje overe (APPROVED → SUBMITTED) ne sme da otvori 'mrtav'
    24h prozor: save blokira SUBMITTED, pa je poruka o izmenama lažna, a
    editable_until ostaje kao tempirana rupa.  [SPEC-RED]"""

    def _revoke(self):
        import timesheet_admin_views as av
        cursor = RecordingCursor(fetchone_queue=[
            {'id': 7, 'status': 'APPROVED', 'employee_email': 'zaposleni@nhmbeo.rs',
             'employee_name': 'Test Zaposleni', 'month': 5, 'year': 2026,
             'is_verified': True, 'is_locked': True},
            {'employee_department': 'Biologija',
             'employee_email': 'zaposleni@nhmbeo.rs'},
        ], fetchall_queue=[
            [{'department': 'Biologija', 'head_email': 'sef.bio@nhmbeo.rs'}],
        ])
        with request_ctx('/api/admin/timesheet/report/7/approve', 'POST',
                         json_body={'approve': False}):
            flask.session.update(_sess('admin', 'admin@nhmbeo.rs'))
            with patch.object(av, 'get_postgres_connection',
                              conn_cm_for(cursor), create=True):
                resp = av.api_admin_approve_timesheet_report(7)
        return resp, cursor

    def test_revoke_does_not_open_edit_window(self):
        resp, cursor = self._revoke()
        sql = executed_sql(cursor)
        self.assertNotIn(
            "editable_until = NOW() + INTERVAL", sql,
            'Poništavanje overe vraća izveštaj u SUBMITTED (zaključan za unos) '
            '— otvaranje editable_until prozora je mrtva/pogrešna semantika',
        )

    def test_revoke_message_does_not_promise_editing(self):
        resp, _ = self._revoke()
        body = resp[0].get_json() if isinstance(resp, tuple) else resp.get_json()
        message = (body or {}).get('message', '')
        self.assertNotIn(
            '24', message,
            'Poruka ne sme da obećava 24h izmena — SUBMITTED se ne može menjati',
        )


class TestForceEditStatusGuard(unittest.TestCase):
    """Šef ne sme force-edit da primeni na APPROVED izveštaj (zaobilazi
    zaključavanje overenog dokumenta); admin/direktor smeju.  [SPEC-RED]"""

    def _force_edit(self, role_sess, report_status):
        import timesheet_employee_views as ev
        import timesheet_postgres as tp
        spy = MagicMock(return_value=tp.TimesheetResult.ok({
            'report_id': 7, 'status': 'DRAFT', 'message': 'ok'}))
        cursor = RecordingCursor(fetchone_queue=[
            {'employee_department': 'Biologija',
             'employee_email': 'zaposleni@nhmbeo.rs'},
            {'id': 7, 'status': report_status},
        ], fetchall_queue=[
            [{'department': 'Biologija', 'head_email': 'sef.bio@nhmbeo.rs'}],
        ])
        with request_ctx('/api/timesheet/7/force-edit', 'POST', json_body={}):
            flask.session.update(role_sess)
            with patch.object(ev, 'get_postgres_connection', conn_cm_for(cursor)), \
                    patch.object(ev, 'force_edit_timesheet', spy, create=True), \
                    patch('timesheet_postgres.force_edit_timesheet', spy), \
                    patch('timesheet_postgres.get_pg_connection', conn_cm_for(cursor)):
                resp = ev.api_timesheet_force_edit(7)
        return resp, spy

    def test_head_cannot_force_edit_approved_report(self):
        sess = _sess('sef_odeljenja', 'sef.bio@nhmbeo.rs', 'Biologija', True)
        resp, spy = self._force_edit(sess, 'APPROVED')
        body = resp[0].get_json() if isinstance(resp, tuple) else resp.get_json()
        succeeded = (body or {}).get('success', False)
        self.assertFalse(
            succeeded,
            'Šef odseka ne sme da vrati APPROVED (overen) izveštaj u DRAFT — '
            'za overene izveštaje ide zahtev za otključavanje / admin',
        )

    def test_head_can_force_edit_submitted_report(self):
        sess = _sess('sef_odeljenja', 'sef.bio@nhmbeo.rs', 'Biologija', True)
        resp, spy = self._force_edit(sess, 'SUBMITTED')
        body = resp[0].get_json() if isinstance(resp, tuple) else resp.get_json()
        self.assertTrue((body or {}).get('success', False),
                        'Vraćanje SUBMITTED izveštaja na unos mora da radi')


# =============================================================================
# PRAVILO 5 — istekli prozor se svuda vidi kao zaključan  [SPEC-RED]
# =============================================================================

class TestStaleLockReaders(unittest.TestCase):
    def test_check_lock_status_treats_expired_window_as_locked(self):
        import timesheet_postgres as tp
        cursor = RecordingCursor(fetchone_queue=[
            {'is_locked': False, 'is_verified': False,
             'edit_window_expired': True},
        ])
        with patch.object(tp, 'get_pg_connection', conn_cm_for(cursor)):
            is_locked, _ = tp.check_timesheet_lock_status(
                'zaposleni@nhmbeo.rs', 5, 2026)
        self.assertTrue(
            is_locked,
            'Istekao editable_until mora da se prijavljuje kao zaključano — '
            'lenjo zaključavanje ostavlja is_locked=FALSE u bazi',
        )


# =============================================================================
# Vlasništvo i podnošenje (lock-in postojećeg ponašanja)
# =============================================================================

class TestSubmitOwnership(unittest.TestCase):
    def _submit(self, report_email, submitter):
        import timesheet_postgres as tp
        cursor = RecordingCursor(fetchone_queue=[
            {'id': 5, 'month': 6, 'year': 2026, 'status': 'DRAFT',
             'employee_email': report_email},
        ])
        with patch.object(tp, 'get_pg_connection', conn_cm_for(cursor)):
            return tp.submit_timesheet(5, submitter)

    def test_cannot_submit_someone_elses_report(self):
        result = self._submit('zaposleni@nhmbeo.rs', 'napadac@nhmbeo.rs')
        self.assertFalse(result.success)

    def test_cannot_submit_report_without_email(self):
        result = self._submit(None, 'zaposleni@nhmbeo.rs')
        self.assertFalse(result.success)

    def test_owner_can_submit_and_lock_happens(self):
        import timesheet_postgres as tp
        cursor = RecordingCursor(fetchone_queue=[
            {'id': 5, 'month': 6, 'year': 2026, 'status': 'DRAFT',
             'employee_email': 'zaposleni@nhmbeo.rs'},
        ])
        with patch.object(tp, 'get_pg_connection', conn_cm_for(cursor)):
            result = tp.submit_timesheet(5, 'zaposleni@nhmbeo.rs')
        self.assertTrue(result.success)
        sql = executed_sql(cursor)
        self.assertIn("status = 'SUBMITTED'", sql)
        self.assertIn('is_locked = TRUE', sql)
        self.assertIn('editable_until = NULL', sql,
                      'Podnošenje mora da zatvori raniji 24h prozor')

    def test_submit_only_from_draft_or_rejected(self):
        import timesheet_postgres as tp
        for status in ('SUBMITTED', 'APPROVED'):
            cursor = RecordingCursor(fetchone_queue=[
                {'id': 5, 'month': 6, 'year': 2026, 'status': status,
                 'employee_email': 'zaposleni@nhmbeo.rs'},
            ])
            with patch.object(tp, 'get_pg_connection', conn_cm_for(cursor)):
                result = tp.submit_timesheet(5, 'zaposleni@nhmbeo.rs')
            self.assertFalse(result.success,
                             f'submit iz statusa {status} mora pasti')


# =============================================================================
# PRAVILO 2 — politika obaveštavanja (šef + direktor + admin, bez podnosioca)
# =============================================================================

class TestNotifyPolicy(unittest.TestCase):
    CANDIDATES = [
        {'email': 'admin@nhmbeo.rs', 'role': 'admin', 'department': None},
        {'email': 'direktor@nhmbeo.rs', 'role': 'direktor', 'department': None},
        {'email': 'sef.bio@nhmbeo.rs', 'role': 'sef_odeljenja',
         'department': 'Biologija'},
        {'email': 'sef.pravna@nhmbeo.rs', 'role': 'sef_pravne_sluzbe',
         'department': 'Pravna služba'},
    ]
    HEAD_ROWS = [
        {'department': 'Biologija', 'head_email': 'sef.bio@nhmbeo.rs'},
        {'department': 'Pravna služba', 'head_email': 'sef.pravna@nhmbeo.rs'},
    ]

    def _notified(self, submitter_email, submitter_dept):
        import timesheet_employee_views as ev
        cursor = RecordingCursor(
            fetchall_queue=[self.CANDIDATES, self.HEAD_ROWS])
        with patch.object(ev, 'get_postgres_connection', conn_cm_for(cursor)):
            ev._notify_verifiers_about_submission(
                'Test', submitter_email, submitter_dept)
        return {params[0] for q, params in cursor.executed
                if 'INSERT INTO user_notifications' in q}

    def test_regular_employee_notifies_admin_and_own_head_only(self):
        got = self._notified('zaposleni@nhmbeo.rs', 'Biologija')
        self.assertEqual(
            got, {'admin@nhmbeo.rs', 'sef.bio@nhmbeo.rs'},
            'Za zaposlenog iz odseka sa šefom: obaveštavaju se admin i NJEGOV '
            'šef; direktor i tuđi šefovi ne',
        )

    def test_head_submission_notifies_admin_and_director(self):
        got = self._notified('sef.bio@nhmbeo.rs', 'Biologija')
        self.assertEqual(got, {'admin@nhmbeo.rs', 'direktor@nhmbeo.rs'},
                         'Izveštaj šefa overava direktor (+admin)')

    def test_headless_department_notifies_admin_and_director(self):
        got = self._notified('edu@nhmbeo.rs', 'Edukacija')
        self.assertEqual(got, {'admin@nhmbeo.rs', 'direktor@nhmbeo.rs'})


if __name__ == '__main__':
    unittest.main()
