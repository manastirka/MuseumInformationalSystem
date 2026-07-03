"""Integration tests for the monthly report workflow against a REAL PostgreSQL.

SAFETY: these tests never touch the production museum_system database.
They run ONLY when TIMESHEET_TEST_DB_URL is set and points at a database
whose name contains '_test' (e.g. the schema-clone museum_system_test):

    TIMESHEET_TEST_DB_URL='postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system_test' \
        ./venv/bin/python -m pytest test_monthly_report_integration.py -q

Covers what mocks cannot: real column names, DB triggers (version bump,
entries sync, audit), unique constraints, editable_until semantics with DB
NOW(), and the real notification-routing SQL.
"""

import os
from contextlib import contextmanager
from datetime import datetime

import pytest

TEST_DB_URL = os.environ.get('TIMESHEET_TEST_DB_URL', '')

if '_test' not in TEST_DB_URL.rsplit('/', 1)[-1]:
    pytest.skip(
        'TIMESHEET_TEST_DB_URL nije postavljen na *_test bazu — preskačem '
        'integracione testove (zaštita produkcione baze)',
        allow_module_level=True,
    )

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-monthly-int')
os.environ['DATABASE_URL'] = TEST_DB_URL

import psycopg
from psycopg.rows import dict_row

import timesheet_postgres as tp

PLAIN_URL = TEST_DB_URL.replace('postgresql+psycopg://', 'postgresql://')


def _shift_month(year, month, delta):
    idx = year * 12 + (month - 1) + delta
    return idx // 12, idx % 12 + 1


# Testovi rade sa TEKUĆIM mesecom (uvek unutar roka za unos) i sa mesecom
# 4 meseca unazad (uvek van roka) — pa paket ne zavisi od kalendarskog datuma.
_NOW = datetime.now()
CUR_Y, CUR_M = _NOW.year, _NOW.month
PREV_Y, PREV_M = _shift_month(CUR_Y, CUR_M, -1)
PAST_Y, PAST_M = _shift_month(CUR_Y, CUR_M, -4)

ADMIN = 'admin@nhmbeo.rs'
DIREKTOR = 'direktor@nhmbeo.rs'
SEF_BIO = 'sef.bio@nhmbeo.rs'
ZAP_BIO = 'zaposleni.bio@nhmbeo.rs'
ZAP_EDU = 'zaposleni.edu@nhmbeo.rs'


def _connect():
    return psycopg.connect(PLAIN_URL, row_factory=dict_row)


@contextmanager
def db():
    conn = _connect()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


@pytest.fixture(scope='module', autouse=True)
def _point_module_at_test_db():
    """timesheet_postgres binds DATABASE_URL at import; u punom suite-u je
    modul možda već uvezen sa starim URL-om — preusmeri i resetuj pool."""
    tp.close_connection_pool()
    old_url = tp.DATABASE_URL
    tp.DATABASE_URL = TEST_DB_URL
    yield
    tp.close_connection_pool()
    tp.DATABASE_URL = old_url


@pytest.fixture(autouse=True)
def seed():
    """Sveže seme pre svakog testa: uloge, odseci, korisnici, profili."""
    with db() as conn:
        cur = conn.cursor()
        cur.execute("""
            TRUNCATE timesheet_status_history, timesheet_edit_requests,
                     timesheet_report_days, timesheet_entries,
                     timesheet_reports, user_notifications,
                     employee_profiles, users, departments
            RESTART IDENTITY CASCADE
        """)
        for role in ('admin', 'employee', 'direktor', 'sef_odeljenja'):
            cur.execute(
                "INSERT INTO roles (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                (role,))
        cur.execute("SELECT id, name FROM roles")
        roles = {r['name']: r['id'] for r in cur.fetchall()}
        cur.execute("INSERT INTO departments (name) VALUES ('Biologija') RETURNING id")
        bio_id = cur.fetchone()['id']
        cur.execute("INSERT INTO departments (name) VALUES ('Edukacija') RETURNING id")
        edu_id = cur.fetchone()['id']

        def add_user(email, name, role, dept_id):
            cur.execute("""
                INSERT INTO users (email, password_hash, salt, full_name,
                                   role_id, department_id, is_active)
                VALUES (%s, 'x', 'x', %s, %s, %s, TRUE)
            """, (email, name, roles[role], dept_id))

        def add_profile(email, name, dept, is_head):
            cur.execute("""
                INSERT INTO employee_profiles
                    (full_name, email, department, position, is_department_head)
                VALUES (%s, %s, %s, 'kustos', %s)
            """, (name, email, dept, is_head))

        add_user(ADMIN, 'Admin', 'admin', None)
        add_user(DIREKTOR, 'Direktor', 'direktor', None)
        add_user(SEF_BIO, 'Šef Biologije', 'sef_odeljenja', bio_id)
        add_user(ZAP_BIO, 'Zaposleni Bio', 'employee', bio_id)
        add_user(ZAP_EDU, 'Zaposleni Edu', 'employee', edu_id)
        add_profile(SEF_BIO, 'Šef Biologije', 'Biologija', True)
        add_profile(ZAP_BIO, 'Zaposleni Bio', 'Biologija', False)
        add_profile(ZAP_EDU, 'Zaposleni Edu', 'Edukacija', False)
    yield


def _report_row(email, month, year):
    with db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT *, (editable_until IS NOT NULL AND NOW() >= editable_until)
                       AS window_expired,
                   (editable_until IS NOT NULL AND NOW() < editable_until)
                       AS window_active
            FROM timesheet_reports
            WHERE employee_email = %s AND month = %s AND year = %s
        """, (email, month, year))
        return cur.fetchone()


def _history(report_id):
    with db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT old_status, new_status FROM timesheet_status_history
            WHERE report_id = %s ORDER BY changed_at, id
        """, (report_id,))
        return [(r['old_status'], r['new_status']) for r in cur.fetchall()]


def _save(email, name, month, year, hours=8, description='rad na zbirci'):
    return tp.save_timesheet_to_postgres(
        user_email=email, user_name=name, month=month, year=year,
        daily_data={'1': {'rad_na_mestu': hours}},
        work_description=description,
        organization_unit='Biologija', position='kustos',
    )


# =============================================================================
# Ceo životni ciklus: unos → podnošenje → overa
# =============================================================================

class TestLifecycle:
    def test_save_submit_approve_cycle(self):
        result = _save(ZAP_BIO, 'Zaposleni Bio', CUR_M, CUR_Y)
        assert result.success, result.error and result.error.message
        report_id = result.data['report_id']

        row = _report_row(ZAP_BIO, CUR_M, CUR_Y)
        assert row['status'] == 'DRAFT'
        assert row['is_locked'] is False

        with db() as conn:
            cur = conn.cursor()
            cur.execute(
                'SELECT day, work_in_museum FROM timesheet_report_days '
                'WHERE report_id = %s', (report_id,))
            days = cur.fetchall()
            assert len(days) == 1 and float(days[0]['work_in_museum']) == 8.0
            cur.execute(
                'SELECT COALESCE(SUM(hours), 0) AS total FROM timesheet_entries '
                'WHERE report_id = %s', (report_id,))
            synced = cur.fetchone()
            assert float(synced['total']) == 8.0, (
                'Trigger sync_timesheet_entries mora da agregira sate')

        submit = tp.submit_timesheet(report_id, ZAP_BIO)
        assert submit.success, submit.error and submit.error.message
        row = _report_row(ZAP_BIO, CUR_M, CUR_Y)
        assert row['status'] == 'SUBMITTED'
        assert row['is_locked'] is True
        assert row['submitted_at'] is not None
        assert row['editable_until'] is None

        blocked = _save(ZAP_BIO, 'Zaposleni Bio', CUR_M, CUR_Y, hours=4)
        assert not blocked.success
        assert blocked.error.error_type == tp.TimesheetErrorType.LOCKED

        approve = tp.approve_timesheet(report_id, SEF_BIO)
        assert approve.success
        row = _report_row(ZAP_BIO, CUR_M, CUR_Y)
        assert row['status'] == 'APPROVED'
        assert row['is_verified'] is True
        assert row['is_locked'] is True
        assert _history(report_id) == [
            ('DRAFT', 'SUBMITTED'), ('SUBMITTED', 'APPROVED')]

    def test_approve_requires_submitted(self):
        result = _save(ZAP_BIO, 'Zaposleni Bio', CUR_M, CUR_Y)
        approve = tp.approve_timesheet(result.data['report_id'], SEF_BIO)
        assert not approve.success

    def test_submit_ownership_enforced(self):
        result = _save(ZAP_BIO, 'Zaposleni Bio', CUR_M, CUR_Y)
        submit = tp.submit_timesheet(result.data['report_id'], ZAP_EDU)
        assert not submit.success
        assert submit.error.error_type == tp.TimesheetErrorType.PERMISSION_DENIED


# =============================================================================
# Vraćanje na doradu + extra dan (pravila 4 i 5)
# =============================================================================

class TestReturnForRework:
    def _submitted_report(self, month=CUR_M, year=CUR_Y):
        result = _save(ZAP_BIO, 'Zaposleni Bio', month, year)
        report_id = result.data['report_id']
        assert tp.submit_timesheet(report_id, ZAP_BIO).success
        return report_id

    def test_reject_opens_24h_window_and_resubmit_closes_it(self):
        report_id = self._submitted_report()
        reject = tp.reject_timesheet(report_id, SEF_BIO, 'Dopuniti opis rada')
        assert reject.success

        row = _report_row(ZAP_BIO, CUR_M, CUR_Y)
        assert row['status'] == 'REJECTED'
        assert row['is_locked'] is False
        assert row['rejection_note'] == 'Dopuniti opis rada'
        assert row['window_active'] is True, 'editable_until mora biti u budućnosti'

        with db() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT (editable_until BETWEEN NOW() + INTERVAL '23 hours'
                                           AND NOW() + INTERVAL '25 hours')
                       AS about_24h
                FROM timesheet_reports WHERE id = %s
            """, (report_id,))
            assert cur.fetchone()['about_24h'] is True, (
                'Prozor mora biti ~24 časa od vraćanja')

        fix = _save(ZAP_BIO, 'Zaposleni Bio', CUR_M, CUR_Y, hours=6,
                    description='dopunjen opis')
        assert fix.success, (
            'U aktivnom 24h prozoru zaposleni mora moći da menja vraćeni '
            'izveštaj: ' + (fix.error.message if fix.error else ''))

        resubmit = tp.submit_timesheet(report_id, ZAP_BIO)
        assert resubmit.success
        assert resubmit.data.get('was_rejected') is True
        row = _report_row(ZAP_BIO, CUR_M, CUR_Y)
        assert row['status'] == 'SUBMITTED'
        assert row['editable_until'] is None, (
            'Ponovno podnošenje mora da zatvori prozor')

    def test_reject_requires_submitted_status(self):
        result = _save(ZAP_BIO, 'Zaposleni Bio', CUR_M, CUR_Y)
        reject = tp.reject_timesheet(result.data['report_id'], SEF_BIO, 'x')
        assert not reject.success

    def test_expired_window_blocks_save_and_materializes_lock(self):
        report_id = self._submitted_report()
        assert tp.reject_timesheet(report_id, SEF_BIO, 'Ispravka').success

        with db() as conn:
            conn.cursor().execute("""
                UPDATE timesheet_reports
                SET editable_until = NOW() - INTERVAL '1 minute'
                WHERE id = %s
            """, (report_id,))

        late = _save(ZAP_BIO, 'Zaposleni Bio', CUR_M, CUR_Y, hours=2)
        assert not late.success
        assert late.error.error_type == tp.TimesheetErrorType.LOCKED

        row = _report_row(ZAP_BIO, CUR_M, CUR_Y)
        assert row['is_locked'] is True, (
            'Posle isteka prozora izveštaj mora biti stvarno zaključan u bazi')
        assert row['editable_until'] is None

    def test_window_is_scoped_to_returned_month_only(self):
        returned_id = self._submitted_report()
        assert tp.reject_timesheet(returned_id, SEF_BIO, 'Dopuna').success

        with db() as conn:
            conn.cursor().execute("""
                INSERT INTO timesheet_reports
                    (employee_email, employee_name, month, year, version, status)
                VALUES (%s, 'Zaposleni Bio', %s, %s, 1, 'DRAFT')
            """, (ZAP_BIO, PREV_M, PREV_Y))

        returned_row = _report_row(ZAP_BIO, CUR_M, CUR_Y)
        other_row = _report_row(ZAP_BIO, PREV_M, PREV_Y)
        assert returned_row['window_active'] is True
        assert other_row['editable_until'] is None, (
            'Extra dan važi SAMO za vraćeni mesec')


# =============================================================================
# Optimistički lock, trigeri, ograničenja
# =============================================================================

class TestConcurrencyAndConstraints:
    def test_version_trigger_bumps_and_stale_version_conflicts(self):
        first = _save(ZAP_BIO, 'Zaposleni Bio', CUR_M, CUR_Y)
        v1 = first.data['version']

        second = tp.save_timesheet_to_postgres(
            user_email=ZAP_BIO, user_name='Zaposleni Bio', month=CUR_M, year=CUR_Y,
            daily_data={'2': {'van_muzeja': 4}},
            work_description='izmena', organization_unit='Biologija',
            position='kustos', expected_version=v1,
        )
        assert second.success
        v2 = second.data['version']
        assert v2 > v1, 'Trigger mora da povećava version pri svakoj izmeni'

        stale = tp.save_timesheet_to_postgres(
            user_email=ZAP_BIO, user_name='Zaposleni Bio', month=CUR_M, year=CUR_Y,
            daily_data={'3': {'godisnji_odmor': 8}},
            work_description='stara verzija', organization_unit='Biologija',
            position='kustos', expected_version=v1,
        )
        assert not stale.success
        assert stale.error.error_type == tp.TimesheetErrorType.CONCURRENT_MODIFICATION

    def test_unique_constraint_blocks_duplicate_month(self):
        _save(ZAP_BIO, 'Zaposleni Bio', CUR_M, CUR_Y)
        with pytest.raises(psycopg.errors.UniqueViolation):
            with db() as conn:
                conn.cursor().execute("""
                    INSERT INTO timesheet_reports
                        (employee_email, employee_name, month, year, version)
                    VALUES (%s, 'Duplikat', %s, %s, 1)
                """, (ZAP_BIO, CUR_M, CUR_Y))

    def test_case_insensitive_duplicate_also_blocked(self):
        _save(ZAP_BIO, 'Zaposleni Bio', CUR_M, CUR_Y)
        with pytest.raises(psycopg.errors.UniqueViolation):
            with db() as conn:
                conn.cursor().execute("""
                    INSERT INTO timesheet_reports
                        (employee_email, employee_name, month, year, version)
                    VALUES (%s, 'Duplikat', %s, %s, 1)
                """, (ZAP_BIO.upper(), CUR_M, CUR_Y))


# =============================================================================
# Pravilo 2 — stvarno rutiranje obaveštenja kroz pravi SQL
# =============================================================================

class TestNotificationRouting:
    def _notified_for(self, submitter_email, submitter_dept, submitter_name):
        import timesheet_employee_views as ev

        @contextmanager
        def test_db_conn(row_factory=None):
            conn = psycopg.connect(PLAIN_URL, row_factory=dict_row)
            try:
                yield conn
            finally:
                conn.close()

        original = ev.get_postgres_connection
        ev.get_postgres_connection = test_db_conn
        try:
            ev._notify_verifiers_about_submission(
                submitter_name, submitter_email, submitter_dept)
        finally:
            ev.get_postgres_connection = original

        with db() as conn:
            cur = conn.cursor()
            cur.execute('SELECT user_email FROM user_notifications')
            return {r['user_email'] for r in cur.fetchall()}

    def test_bio_employee_notifies_admin_and_bio_head(self):
        got = self._notified_for(ZAP_BIO, 'Biologija', 'Zaposleni Bio')
        assert got == {ADMIN, SEF_BIO}, (
            f'Očekivano: admin + šef Biologije; dobijeno: {got}')

    def test_bio_head_notifies_admin_and_director(self):
        got = self._notified_for(SEF_BIO, 'Biologija', 'Šef Biologije')
        assert got == {ADMIN, DIREKTOR}

    def test_edu_employee_notifies_admin_and_director(self):
        got = self._notified_for(ZAP_EDU, 'Edukacija', 'Zaposleni Edu')
        assert got == {ADMIN, DIREKTOR}


# =============================================================================
# Pravilo 1 — rok u bazi (SPEC-RED dok se rok ne uključi)
# =============================================================================

class TestDeadlineInDatabase:
    def test_save_for_long_past_month_is_rejected(self):
        result = _save(ZAP_BIO, 'Zaposleni Bio', PAST_M, PAST_Y,
                       description='zakasneli unos za davno prošli mesec')
        assert not result.success, (
            'Unos za mesec od pre 4 meseca mora biti odbijen (rok je 10. u '
            'narednom mesecu)')

    def test_submit_for_long_past_month_is_rejected(self):
        with db() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO timesheet_reports
                    (employee_email, employee_name, month, year, version, status)
                VALUES (%s, 'Zaposleni Bio', %s, %s, 1, 'DRAFT')
                RETURNING id
            """, (ZAP_BIO, PAST_M, PAST_Y))
            report_id = cur.fetchone()['id']
        submit = tp.submit_timesheet(report_id, ZAP_BIO)
        assert not submit.success, (
            'Podnošenje izveštaja od pre 4 meseca mora biti odbijeno')

    def test_returned_report_with_active_window_can_save_and_resubmit_past_deadline(self):
        """Pravila 4+5 zajedno: kada šef vrati izveštaj POSLE roka, aktivni
        24h prozor mora da dozvoli i izmenu I ponovno podnošenje — inače je
        vraćanje na doradu mrtvo slovo čim rok prođe."""
        with db() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO timesheet_reports
                    (employee_email, employee_name, month, year, version,
                     status, is_locked, rejection_note, editable_until)
                VALUES (%s, 'Zaposleni Bio', %s, %s, 1,
                        'REJECTED', FALSE, 'Dopuniti', NOW() + INTERVAL '12 hours')
                RETURNING id
            """, (ZAP_BIO, PAST_M, PAST_Y))
            report_id = cur.fetchone()['id']

        fix = _save(ZAP_BIO, 'Zaposleni Bio', PAST_M, PAST_Y, hours=5,
                    description='dopuna po vraćanju (posle roka)')
        assert fix.success, (
            'Aktivni 24h prozor mora da dozvoli izmenu vraćenog izveštaja i '
            'posle roka: ' + (fix.error.message if fix.error else ''))

        resubmit = tp.submit_timesheet(report_id, ZAP_BIO)
        assert resubmit.success, (
            'Aktivni 24h prozor mora da dozvoli ponovno podnošenje i posle '
            'roka: ' + (resubmit.error.message if resubmit.error else ''))
        row = _report_row(ZAP_BIO, PAST_M, PAST_Y)
        assert row['status'] == 'SUBMITTED'
        assert row['editable_until'] is None
