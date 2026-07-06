"""Reproducing tests for the broken vehicle reservation PostgreSQL write path.

Bug report (2026-07-06): creating a vehicle reservation fails on deployed
databases. Root cause: the deployed vehicle_reservations table predates the
current schema and still carries the legacy
vehicle_reservations_status_check constraint (English statuses PENDING /
APPROVED / REJECTED / CANCELLED), while the application inserts the Serbian
status 'Активна' — so every INSERT dies with CheckViolation. The canonical
db/schema_vehicles.sql declares no status CHECK at all.

Secondary bug in the same flow: phase3a_databases.get_vehicle_reservations
returns 'reserved_by' while templates/vehicle_reservations.html renders
reservation.employee_name, so PostgreSQL-backed reservations display
'undefined' as the employee.

These tests run against the dev database (DATABASE_URL from .env) and are
skipped when it is unreachable. All writes are rolled back.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')

import pytest

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

psycopg = pytest.importorskip('psycopg')

DATABASE_URL = os.environ.get('DATABASE_URL', '').replace(
    'postgresql+psycopg://', 'postgresql://'
)


def _connect():
    if not DATABASE_URL:
        pytest.skip('DATABASE_URL is not configured')
    try:
        return psycopg.connect(DATABASE_URL)
    except Exception as exc:
        pytest.skip(f'PostgreSQL unreachable: {exc}')


@pytest.fixture
def db_conn():
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT to_regclass('public.vehicle_reservations')")
            if cur.fetchone()[0] is None:
                pytest.skip('vehicle_reservations table does not exist')
        yield conn
    finally:
        conn.rollback()
        conn.close()


def test_add_reservation_insert_with_serbian_status_succeeds(db_conn):
    """The exact INSERT handle_add_vehicle_reservation issues (status
    'Активна') must be accepted by the deployed table."""
    with db_conn.cursor() as cur:
        cur.execute("SELECT id FROM vehicles ORDER BY id LIMIT 1")
        row = cur.fetchone()
        if row is None:
            pytest.skip('no vehicles in database')
        vehicle_id = row[0]
        cur.execute(
            """
            INSERT INTO vehicle_reservations (
                vehicle_id, reserved_by, purpose, start_date, end_date,
                start_time, end_time, destination, estimated_km,
                driver_name, driver_license, passengers, notes, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, status
            """,
            (
                vehicle_id, 'test-suite', 'Terenski rad',
                '2026-07-10', '2026-07-11', '08:00', '16:00',
                'Fruška Gora', '120', 'Test Vozač', 'B', '2',
                'reproducing test — rolled back', 'Активна',
            ),
        )
        inserted = cur.fetchone()
        assert inserted is not None
        assert inserted[1] == 'Активна'
    db_conn.rollback()


def test_no_legacy_english_status_check_constraint(db_conn):
    """db/schema_vehicles.sql declares no status CHECK; a leftover legacy
    constraint rejecting 'Активна' must not exist on the deployed table."""
    with db_conn.cursor() as cur:
        cur.execute(
            """
            SELECT pg_get_constraintdef(oid)
            FROM pg_constraint
            WHERE conrelid = 'vehicle_reservations'::regclass
              AND conname = 'vehicle_reservations_status_check'
            """
        )
        row = cur.fetchone()
    assert row is None, (
        f'legacy status CHECK still present: {row[0]}'
    )


def test_no_rows_with_legacy_english_statuses(db_conn):
    """The application only understands 'Активна'/'Завршена'/'Отказана';
    legacy English statuses must be migrated so existing reservations stay
    visible to the calendar, views and the delete-vehicle guard."""
    with db_conn.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*) FROM vehicle_reservations
            WHERE status IN ('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED')
            """
        )
        count = cur.fetchone()[0]
    assert count == 0, f'{count} reservation(s) still carry legacy statuses'


def test_pg_reservations_expose_employee_name_for_template():
    """templates/vehicle_reservations.html renders
    reservation.employee_name; the PostgreSQL loader must provide it."""
    if not DATABASE_URL:
        pytest.skip('DATABASE_URL is not configured')
    import phase3a_databases
    try:
        reservations = phase3a_databases.get_vehicle_reservations()
    except Exception as exc:
        pytest.skip(f'PostgreSQL unreachable: {exc}')
    if not reservations:
        pytest.skip('no reservations in database')
    for reservation in reservations:
        assert 'employee_name' in reservation
        assert reservation['employee_name'] == reservation['reserved_by']
