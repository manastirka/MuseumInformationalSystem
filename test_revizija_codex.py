#!/usr/bin/env python3
"""Reprodukcioni testovi за ДРУГУ независну ревизију (Codex/GPT) — 6 налаза
које прва ревизија (Grok) није нашла. Сваки тест закључава ТАЧНО ЈЕДНУ
поправку; ако падне, регресирала је нека од затворених рупа.

Налази:
  #1  Модул службених путовања више НЕ пише у timesheet_report_days
      (аутоматски упис у радну листу потпуно уклоњен).
  #2  force_edit_timesheet re-проверава статус+ауторизацију под FOR UPDATE
      (нема TOCTOU трке око откључавања одобрене листе).
  #3  Месечни/укупни сажеци поштују department scope (шеф не види цео музеј).
  #4  Обичан запослени не може self-save за текући/будући месец без
      активног откључавања или враћене (REJECTED) листе.
  #5  timesheet_reports.employee_email је NOT NULL (name-collision грана мртва).
  #6  Пропали упис се не пријављује као success=true (парцијални неуспех видљив).

DB делови се прескачу без PostgreSQL-а.
"""

import os
import unittest
from datetime import datetime, timedelta

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-codex')
os.environ.setdefault('WTF_CSRF_ENABLED', 'False')

import timesheet_postgres as tp

_HERE = os.path.dirname(os.path.abspath(__file__))
# Модул службених путовања чита DATABASE_URL директно из окружења; тестови
# морају да га поставе да би DB гране (резервација/некадашњи упис у листу)
# уопште биле активне и проверљиве.
_DSN = tp.DATABASE_URL


def _pg_available():
    try:
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT 1')
                cur.fetchone()
        return True
    except Exception:
        return False


_DB = unittest.skipUnless(_pg_available(), 'PostgreSQL nije dostupan')


# ---------------------------------------------------------------------------
# Заједнички DB алат
# ---------------------------------------------------------------------------
def _delete_by_email(email):
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM timesheet_report_days WHERE report_id IN "
                "(SELECT id FROM timesheet_reports WHERE employee_email=%s)", (email,))
            cur.execute("DELETE FROM timesheet_reports WHERE employee_email=%s", (email,))
            conn.commit()


def _seed_report(email, name, month, year, status='SUBMITTED', is_locked=None):
    if is_locked is None:
        is_locked = status in ('SUBMITTED', 'APPROVED')
    verified = status == 'APPROVED'
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO timesheet_reports "
                "(employee_name, employee_email, month, year, status, is_locked, is_verified) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id",
                (name, email, month, year, status, is_locked, verified))
            rid = cur.fetchone()['id']
            conn.commit()
            return rid


def _insert_day(report_id, day, work_in_museum=0, work_outside=0):
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO timesheet_report_days (report_id, day, work_in_museum, work_outside) "
                "VALUES (%s,%s,%s,%s)",
                (report_id, day, work_in_museum, work_outside))
            conn.commit()


def _day_row(report_id, day):
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT work_in_museum, work_outside FROM timesheet_report_days "
                "WHERE report_id=%s AND day=%s", (report_id, day))
            return cur.fetchone()


def _status_of(report_id):
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COALESCE(status,'DRAFT') AS s FROM timesheet_reports WHERE id=%s",
                        (report_id,))
            return cur.fetchone()['s']


# ===========================================================================
# #1  Модул службених путовања НЕ пише у радну листу
# ===========================================================================
class TravelNeverWritesTimesheet(unittest.TestCase):
    def test_travel_source_has_no_timesheet_day_writes(self):
        """Ниједна рута/функција службеног пута не сме да дира
        timesheet_report_days — статичка провера извора."""
        for fname in ('travel_finance_views.py', 'archive_signature_blueprint.py'):
            with open(os.path.join(_HERE, fname), encoding='utf-8') as fh:
                src = fh.read()
            self.assertNotIn(
                'timesheet_report_days', src,
                f'{fname} и даље референцира timesheet_report_days — радна листа '
                f'се сме мењати ИСКЉУЧИВО кроз свој ток.')

    @_DB
    def test_execute_field_trip_does_not_touch_days(self):
        """Позив execute_field_trip са update_timesheet=True НЕ мења дане
        већ поднете листе и не пријављује timesheet_updated."""
        import importlib
        email = 'codex.trip@example.invalid'
        name = 'Codex Trip'
        month, year = datetime.now().month, datetime.now().year
        prev = os.environ.get('DATABASE_URL')
        os.environ['DATABASE_URL'] = _DSN
        _delete_by_email(email)
        try:
            rid = _seed_report(email, name, month, year, status='SUBMITTED')
            _insert_day(rid, 15, work_in_museum=8, work_outside=0)

            import travel_finance_views as tfv
            importlib.reload(tfv)
            day_iso = f'{year:04d}-{month:02d}-15'
            result = tfv.execute_field_trip(
                {'update_timesheet': True, 'start_date': day_iso, 'end_date': day_iso,
                 'vehicle_id': 'sopstveni', 'location': 'X', 'purpose': 'Y'},
                user_name=name, user_email=email)

            row = _day_row(rid, 15)
            self.assertEqual(float(row['work_in_museum']), 8.0,
                             'дан радне листе је измењен из модула службеног пута')
            self.assertEqual(float(row['work_outside']), 0.0,
                             'службени пут је уписао work_outside у радну листу')
            self.assertNotEqual(result.get('timesheet_updated'), True,
                                'модул службеног пута тврди да је ажурирао радну листу')
        finally:
            _delete_by_email(email)
            if prev is None:
                os.environ.pop('DATABASE_URL', None)
            else:
                os.environ['DATABASE_URL'] = prev


# ===========================================================================
# #2  force_edit_timesheet: провера статуса+ауторизације под FOR UPDATE
# ===========================================================================
class ForceEditReauthUnderLock(unittest.TestCase):
    EMAIL = 'codex.race@example.invalid'
    NAME = 'Codex Race'

    def tearDown(self):
        if _pg_available():
            _delete_by_email(self.EMAIL)

    @_DB
    def test_head_cannot_reopen_approved_report(self):
        """Кад је листа APPROVED, позивалац без права на поновно отварање
        (шеф) добија одбијање, а статус остаје APPROVED — провера је ПОД
        истим локом као UPDATE, па нема TOCTOU трке."""
        _delete_by_email(self.EMAIL)
        month, year = datetime.now().month, datetime.now().year
        rid = _seed_report(self.EMAIL, self.NAME, month, year, status='APPROVED')

        res = tp.force_edit_timesheet(rid, 'sef@example.invalid',
                                      allow_approved_reopen=False)
        self.assertFalse(res.success, 'шеф је успео да отвори ОВЕРЕНУ листу')
        self.assertEqual(_status_of(rid), 'APPROVED',
                         'оверена листа је враћена на DRAFT упркос одбијању')

    @_DB
    def test_admin_may_reopen_approved_report(self):
        """Админ/директор (allow_approved_reopen=True) сме да отвори оверену
        листу — регуларан оператерски пут остаје."""
        _delete_by_email(self.EMAIL)
        month, year = datetime.now().month, datetime.now().year
        rid = _seed_report(self.EMAIL, self.NAME, month, year, status='APPROVED')

        res = tp.force_edit_timesheet(rid, 'admin@example.invalid',
                                      allow_approved_reopen=True)
        self.assertTrue(res.success, res.error.message if res.error else res)
        self.assertEqual(_status_of(rid), 'DRAFT')


# ===========================================================================
# #3  Сажеци поштују department scope
# ===========================================================================
class SummaryDepartmentScope(unittest.TestCase):
    DEPT_A = '__CodexDeptA__'
    DEPT_B = '__CodexDeptB__'
    EMAIL_A = 'codex.deptA@example.invalid'
    EMAIL_B = 'codex.deptB@example.invalid'

    def _seed_profile(self, email, name, dept):
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM employee_profiles WHERE email=%s", (email,))
                cur.execute(
                    "INSERT INTO employee_profiles (full_name, email, position, department) "
                    "VALUES (%s,%s,%s,%s)", (name, email, 'кустос', dept))
                conn.commit()

    def _cleanup(self):
        _delete_by_email(self.EMAIL_A)
        _delete_by_email(self.EMAIL_B)
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM employee_profiles WHERE email IN (%s,%s)",
                            (self.EMAIL_A, self.EMAIL_B))
                conn.commit()

    def tearDown(self):
        if _pg_available():
            self._cleanup()

    @_DB
    def test_month_and_overall_summary_respect_department(self):
        from timesheet_repository import TimesheetRepository
        self._cleanup()
        month, year = datetime.now().month, datetime.now().year
        self._seed_profile(self.EMAIL_A, 'Codex A', self.DEPT_A)
        self._seed_profile(self.EMAIL_B, 'Codex B', self.DEPT_B)
        rid_a = _seed_report(self.EMAIL_A, 'Codex A', month, year, status='DRAFT')
        rid_b = _seed_report(self.EMAIL_B, 'Codex B', month, year, status='DRAFT')
        _insert_day(rid_a, 3, work_in_museum=8)   # dept A: 8h
        _insert_day(rid_b, 4, work_in_museum=5)   # dept B: 5h

        repo = TimesheetRepository(_DSN)  # SQLAlchemy psycopg3 dialect URL as-is
        if not repo.available:
            self.skipTest('repository nije dostupan')

        scoped = repo.get_month_summary(month=month, year=year, department=self.DEPT_A)
        self.assertIsNotNone(scoped)
        self.assertEqual(scoped['totals']['reports_count'], 1,
                         'месечни сажетак броји листе изван одељења')
        self.assertEqual(scoped['totals']['rad_na_mestu'], 8.0,
                         'месечни сажетак сабира сате изван одељења')

        overall = repo.get_overall_summary(department=self.DEPT_A)
        self.assertIsNotNone(overall)
        self.assertEqual(overall['employees'], 1,
                         'укупни сажетак види запослене изван одељења')
        self.assertEqual(overall['category_totals']['rad_na_mestu'], 8.0)


# ===========================================================================
# #4  Self-save за текући/будући месец блокиран без откључавања
# ===========================================================================
class CurrentMonthSelfSaveBlocked(unittest.TestCase):
    def setUp(self):
        import app as museum_app
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.app = museum_app.app
        self.client = self.app.test_client()
        self.base_url = 'https://localhost'
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT email, full_name FROM users "
                            "WHERE email IS NOT NULL AND full_name IS NOT NULL "
                            "ORDER BY id LIMIT 1")
                self.emp = cur.fetchone()
        self._cleanup()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        if not self.emp:
            return
        for m, y in ((datetime.now().month, datetime.now().year),):
            with tp.get_pg_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM timesheet_report_days WHERE report_id IN "
                                "(SELECT id FROM timesheet_reports WHERE employee_email=%s AND month=%s AND year=%s)",
                                (self.emp['email'], m, y))
                    cur.execute("DELETE FROM timesheet_reports WHERE employee_email=%s AND month=%s AND year=%s",
                                (self.emp['email'], m, y))
                    conn.commit()

    def _login_employee(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 999
            sess['user_email'] = self.emp['email']
            sess['user_name'] = self.emp['full_name']
            sess['user_role'] = 'employee'
            sess['is_admin'] = False

    @_DB
    def test_current_month_save_blocked_for_employee(self):
        if not self.emp:
            self.skipTest('нема запосленог у users')
        self._login_employee()
        now = datetime.now()
        payload = {'month': now.month, 'year': now.year,
                   'daily_data': {'5': {'rad_na_mestu': 8}}, 'obavljeni_poslovi': ''}
        resp = self.client.post('/api/timesheet/save', json=payload, base_url=self.base_url)
        self.assertEqual(resp.status_code, 423,
                         'текући месец је сачуван без откључавања '
                         f'(HTTP {resp.status_code}: {resp.get_data(as_text=True)[:200]})')

    @_DB
    def test_unlocked_current_month_allowed(self):
        """Активно откључавање (editable_until у будућности) отвара текући
        месец — тестирање корисника се НЕ сме блокирати."""
        if not self.emp:
            self.skipTest('нема запосленог у users')
        now = datetime.now()
        rid = _seed_report(self.emp['email'], self.emp['full_name'], now.month, now.year,
                           status='DRAFT', is_locked=False)
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE timesheet_reports SET editable_until = NOW() + INTERVAL '2 days' "
                            "WHERE id=%s", (rid,))
                conn.commit()
        self._login_employee()
        payload = {'month': now.month, 'year': now.year,
                   'daily_data': {'5': {'rad_na_mestu': 8}}, 'obavljeni_poslovi': ''}
        resp = self.client.post('/api/timesheet/save', json=payload, base_url=self.base_url)
        self.assertNotEqual(resp.status_code, 423,
                            'откључан текући месец је погрешно блокиран (тестирање)')


# ===========================================================================
# #5  employee_email NOT NULL
# ===========================================================================
class EmployeeEmailNotNull(unittest.TestCase):
    @_DB
    def test_column_is_not_null(self):
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT is_nullable FROM information_schema.columns "
                            "WHERE table_name='timesheet_reports' AND column_name='employee_email'")
                row = cur.fetchone()
        self.assertEqual(row['is_nullable'], 'NO',
                         'employee_email није NOT NULL — name-collision грана остаје жива')


# ===========================================================================
# #6  Парцијални неуспех се пријављује (нема тихог success=true)
# ===========================================================================
class PartialFailureSurfaced(unittest.TestCase):
    def test_vehicle_reservation_error_flips_success_false(self):
        """Кад је резервација возила тражена (numeric vehicle_id) али падне,
        execute_field_trip мора вратити success=False + vehicle_error."""
        import importlib
        import travel_finance_views as tfv
        importlib.reload(tfv)
        prev = os.environ.get('DATABASE_URL')
        os.environ['DATABASE_URL'] = _DSN
        import psycopg
        orig_connect = psycopg.connect

        def _boom(*a, **k):
            raise RuntimeError('simulirani пад базе')

        psycopg.connect = _boom
        try:
            result = tfv.execute_field_trip(
                {'vehicle_id': '5', 'location': 'X', 'purpose': 'Y',
                 'start_date': '2026-06-01', 'end_date': '2026-06-01'},
                user_name='X', user_email='x@example.invalid')
        finally:
            psycopg.connect = orig_connect
            if prev is None:
                os.environ.pop('DATABASE_URL', None)
            else:
                os.environ['DATABASE_URL'] = prev
        self.assertIn('vehicle_error', result)
        self.assertFalse(result.get('success', True),
                         'резервација је пала, а success је остао True')

    @_DB
    def test_employee_save_surfaces_failed_auto_resubmit(self):
        """Страна запосленог (#6): кад сачувамо враћену листу, а аутоматско
        поновно подношење падне, одговор мора да НОСИ resubmit_failed и поруку
        да лист НИЈЕ поново поднет (ово је затворено још у ревизији ланца —
        овде само доказујемо да није регресирало)."""
        import app as museum_app
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        client = museum_app.app.test_client()
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT email, full_name FROM users "
                            "WHERE email IS NOT NULL AND full_name IS NOT NULL ORDER BY id LIMIT 1")
                emp = cur.fetchone()
        if not emp:
            self.skipTest('нема запосленог у users')
        now = datetime.now()
        _delete_by_email(emp['email'])
        # REJECTED листа са активним прозором → save пролази, па покушава resubmit.
        rid = _seed_report(emp['email'], emp['full_name'], now.month, now.year,
                           status='REJECTED', is_locked=False)
        with tp.get_pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE timesheet_reports SET editable_until = NOW() + INTERVAL '2 days' "
                            "WHERE id=%s", (rid,))
                conn.commit()

        orig_submit = tp.submit_timesheet
        tp.submit_timesheet = lambda *a, **k: tp.TimesheetResult.fail(
            tp.TimesheetErrorType.VALIDATION_ERROR, 'simulirani пад поновног подношења')
        try:
            with client.session_transaction() as sess:
                sess['user_id'] = 999
                sess['user_email'] = emp['email']
                sess['user_name'] = emp['full_name']
                sess['user_role'] = 'employee'
                sess['is_admin'] = False
            resp = client.post('/api/timesheet/save',
                               json={'month': now.month, 'year': now.year,
                                     'daily_data': {'5': {'rad_na_mestu': 8}},
                                     'obavljeni_poslovi': ''},
                               base_url='https://localhost')
            data = resp.get_json()
            self.assertTrue(data.get('resubmit_failed'),
                            'пали resubmit није пријављен као парцијални неуспех')
            self.assertIn('НИЈЕ поново поднет', data.get('message', ''),
                          'порука не саопштава да лист НИЈЕ поново поднет')
        finally:
            tp.submit_timesheet = orig_submit
            _delete_by_email(emp['email'])


if __name__ == '__main__':
    unittest.main()
