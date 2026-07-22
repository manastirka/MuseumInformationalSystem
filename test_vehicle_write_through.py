"""Write-through tests for the vehicle module (ZADATAK #3, jul 2026).

PostgreSQL je jedini izvor istine za vozila i rezervacije. Ovi testovi dokazuju:

1. Pad baze se NE maskira tihim JSON fallback-om — greška se propagira
   (``load_vehicles`` / ``load_reservations`` dižu izuzetak umesto praznog niza).
2. CRUD (dodavanje / izmena / brisanje) ide isključivo kroz bazu, a in-memory
   keš se invalidira posle svakog upisa (``force_reload=True``).
3. INSERT novog vozila upisuje sve kolone koje obrazac prikuplja.

Unit deo (1) radi bez baze. Integracioni deo (2, 3) traži dev bazu
(``DATABASE_URL`` iz .env) i preskače se kad nije dostupna; svi upisi se čiste.
"""

import os
from unittest import mock

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-vehicle-write-through')

import flask
import pytest

import vehicle_data_support
import vehicle_depot_views


# ---------------------------------------------------------------------------
# 1. Pad baze -> jasna greška, nikad tihi fallback
# ---------------------------------------------------------------------------

def test_load_vehicles_raises_when_backend_missing():
    with pytest.raises(vehicle_data_support.VehicleStoreUnavailable):
        vehicle_data_support.load_vehicles(phase3a_databases=None)


def test_load_reservations_raises_when_backend_missing():
    with pytest.raises(vehicle_data_support.VehicleStoreUnavailable):
        vehicle_data_support.load_reservations(phase3a_databases=None)


def test_load_vehicles_propagates_db_error_not_silent():
    backend = mock.MagicMock()
    backend.get_vehicles_list.side_effect = RuntimeError('db down')
    # No silent [] fallback — the error must surface to the caller.
    with pytest.raises(RuntimeError):
        vehicle_data_support.load_vehicles(phase3a_databases=backend)


def test_load_reservations_propagates_db_error_not_silent():
    backend = mock.MagicMock()
    backend.get_vehicle_reservations.side_effect = RuntimeError('db down')
    with pytest.raises(RuntimeError):
        vehicle_data_support.load_reservations(phase3a_databases=backend)


# ---------------------------------------------------------------------------
# 2. + 3. CRUD kroz bazu i potpun INSERT (integracioni, protiv dev baze)
# ---------------------------------------------------------------------------

psycopg = pytest.importorskip('psycopg')

DATABASE_URL = os.environ.get('DATABASE_URL', '').replace(
    'postgresql+psycopg://', 'postgresql://'
)

TEST_REGISTRATION = 'TEST-WT-0001'


def _connect():
    if not DATABASE_URL:
        pytest.skip('DATABASE_URL is not configured')
    try:
        return psycopg.connect(DATABASE_URL, connect_timeout=5)
    except Exception as exc:
        pytest.skip(f'PostgreSQL unreachable: {exc}')


class _RealBackend:
    """Minimal phase3a_databases stand-in: hands the handlers a real
    connection so the write path is exercised end-to-end against Postgres."""

    def get_db_connection(self):
        return psycopg.connect(DATABASE_URL)


def _delete_test_vehicle(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM vehicles WHERE registration = %s", (TEST_REGISTRATION,))
    conn.commit()


@pytest.fixture
def db_conn():
    conn = _connect()
    with conn.cursor() as cur:
        cur.execute("SELECT to_regclass('public.vehicles')")
        if cur.fetchone()[0] is None:
            conn.close()
            pytest.skip('vehicles table does not exist')
    _delete_test_vehicle(conn)
    try:
        yield conn
    finally:
        _delete_test_vehicle(conn)
        conn.close()


@pytest.fixture
def app():
    application = flask.Flask(__name__)
    application.secret_key = 'test-secret'
    application.add_url_rule(
        '/vehicle_management', 'vehicles.vehicle_management', lambda: '', methods=['GET']
    )
    application.add_url_rule(
        '/vehicle_reservations', 'vehicles.vehicle_reservations', lambda: '', methods=['GET']
    )
    return application


def _add_form():
    return {
        'name': 'Тест Возило',
        'registration': TEST_REGISTRATION,
        'type': 'Комби',
        'capacity': '7',
        'status': 'Активно',
        'year': '2021',
        'make_model': 'Тест 1.6',
        'notes': 'напомена',
    }


def test_add_vehicle_writes_all_form_columns_to_db(app, db_conn):
    reloads = []

    with app.test_request_context('/add_vehicle', method='POST', data=_add_form()):
        vehicle_depot_views.handle_add_vehicle(
            phase3a_databases=_RealBackend(),
            get_museum_vehicles=lambda force_reload=False: reloads.append(force_reload),
        )

    # Write-through: the in-memory cache is invalidated after the write.
    assert reloads == [True]

    with db_conn.cursor() as cur:
        cur.execute(
            """
            SELECT name, registration, type, capacity, status, year,
                   make_model, notes, image_ids, created_at, updated_at
            FROM vehicles WHERE registration = %s
            """,
            (TEST_REGISTRATION,),
        )
        row = cur.fetchone()

    assert row is not None, 'vehicle must be persisted to the database'
    (name, registration, vtype, capacity, status, year,
     make_model, notes, image_ids, created_at, updated_at) = row
    assert name == 'Тест Возило'
    assert registration == TEST_REGISTRATION
    assert vtype == 'Комби'
    assert capacity == '7'
    assert status == 'Активно'
    assert year == '2021'
    assert make_model == 'Тест 1.6'
    assert notes == 'напомена'
    assert image_ids == []
    # Schema-managed columns must be populated by DEFAULT now().
    assert created_at is not None
    assert updated_at is not None


def test_vehicle_crud_roundtrip_through_db(app, db_conn):
    # CREATE
    with app.test_request_context('/add_vehicle', method='POST', data=_add_form()):
        vehicle_depot_views.handle_add_vehicle(
            phase3a_databases=_RealBackend(),
            get_museum_vehicles=lambda force_reload=False: None,
        )
    with db_conn.cursor() as cur:
        cur.execute("SELECT id, status FROM vehicles WHERE registration = %s", (TEST_REGISTRATION,))
        created = cur.fetchone()
    assert created is not None
    vehicle_id = created[0]

    # UPDATE
    edit_form = dict(_add_form())
    edit_form['vehicle_id'] = str(vehicle_id)
    edit_form['status'] = 'У сервису'
    edit_form['capacity'] = '9'
    with app.test_request_context('/edit_vehicle', method='POST', data=edit_form):
        vehicle_depot_views.handle_edit_vehicle(
            phase3a_databases=_RealBackend(),
            get_museum_vehicles=lambda force_reload=False: None,
        )
    with db_conn.cursor() as cur:
        cur.execute("SELECT status, capacity FROM vehicles WHERE id = %s", (vehicle_id,))
        updated = cur.fetchone()
    assert updated == ('У сервису', '9')

    # DELETE
    with app.test_request_context('/delete_vehicle', method='POST', data={'vehicle_id': str(vehicle_id)}):
        vehicle_depot_views.handle_delete_vehicle(
            phase3a_databases=_RealBackend(),
            get_museum_vehicles=lambda force_reload=False: None,
        )
    with db_conn.cursor() as cur:
        cur.execute("SELECT id FROM vehicles WHERE id = %s", (vehicle_id,))
        assert cur.fetchone() is None, 'vehicle must be deleted from the database'
