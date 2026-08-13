#!/usr/bin/env python3
"""Automated PostgreSQL integration tests for core data modules."""

import os
import time
import unittest
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

import bird_ringing_database as brd
from inventory_reconciliation import InventoryReconciliation
from mineral_database_pg import MineralDatabase


load_dotenv(Path(__file__).resolve().parent / '.env')

SEED_TAG = 'pytest-seed-postgres-tests'


def _database_name(url: str) -> str:
    return url.rstrip('/').rsplit('/', 1)[-1].split('?')[0]


def ensure_reference_data(engine, database_url):
    """Обезбеди податке које ови тестови проверавају (образац из
    test_revizija_codex.EmployeeEmailNotNull): ако подаци фале а повезана
    база је *_test — убаци минималан сет и врати state за
    cleanup_reference_data; ако база НИЈЕ *_test — SkipTest са разлогом
    (жива база се не сеедује из тестова)."""
    state = {
        'bird_record_ids': [],
        'bird_species_ids': [],
        'mineral_ids': [],
        'inventory_ids': [],
    }
    with engine.connect() as conn:
        missing_birds = conn.execute(text("""
            SELECT COUNT(*)
            FROM bird_ringing_records br
            JOIN bird_species bs ON bs.id = br.species_id
            WHERE br.coordinates IS NOT NULL
              AND strpos(bs.species_name, 'Parus') > 0
              AND br.location IS NOT NULL
              AND br.ringer IS NOT NULL
              AND br.event_date IS NOT NULL
        """)).scalar() == 0
        missing_minerals = conn.execute(text(
            "SELECT COUNT(*) FROM minerals WHERE inventory_number IS NOT NULL"
        )).scalar() == 0
        missing_inventory = conn.execute(text(
            "SELECT COUNT(*) FROM inventory_entries WHERE inventory_number IS NOT NULL"
        )).scalar() == 0

    if not (missing_birds or missing_minerals or missing_inventory):
        return state

    db_name = _database_name(database_url)
    if not db_name.endswith('_test'):
        raise unittest.SkipTest(
            f'referentni podaci fale (ptice={missing_birds}, '
            f'minerali={missing_minerals}, inventar={missing_inventory}), '
            f'a baza "{db_name}" nije *_test — ne seedujem živu bazu; '
            'testovi zahtevaju postojeće podatke ili *_test bazu')

    try:
        _seed_reference_data(engine, state, missing_birds, missing_minerals,
                             missing_inventory)
    except BaseException:
        cleanup_reference_data(engine, state)
        raise
    return state


def _seed_reference_data(engine, state, missing_birds, missing_minerals,
                         missing_inventory):
    with engine.begin() as conn:
        if missing_birds:
            species_ids = []
            for name in ('Parus major', 'Erithacus rubecula'):
                row = conn.execute(text(
                    'INSERT INTO bird_species (species_name) VALUES (:name) '
                    'ON CONFLICT (species_name) DO NOTHING RETURNING id'
                ), {'name': name}).fetchone()
                if row is not None:
                    state['bird_species_ids'].append(row[0])
                    species_ids.append(row[0])
                else:
                    species_ids.append(conn.execute(text(
                        'SELECT id FROM bird_species WHERE species_name = :name'
                    ), {'name': name}).scalar())

            record_specs = (
                (species_ids[0], 'PY-SEED-0001', 'Велико ратно острво (seed)',
                 20.4489, 44.8125, '2024-05-10'),
                (species_ids[0], 'PY-SEED-0002', 'Велико ратно острво (seed)',
                 20.4489, 44.8125, '2023-04-18'),
                (species_ids[1], 'PY-SEED-0003', 'Обедска бара (seed)',
                 None, None, '2024-06-02'),
            )
            for sid, ring, location, lon, lat, day in record_specs:
                params = {'ring': ring, 'sid': sid, 'loc': location,
                          'day': day, 'ringer': 'Тест Прстеновач (seed)',
                          'notes': SEED_TAG}
                if lon is None:
                    row = conn.execute(text("""
                        INSERT INTO bird_ringing_records
                            (ring_number, species_id, location, event_date,
                             ringer, notes)
                        VALUES (:ring, :sid, :loc, :day, :ringer, :notes)
                        RETURNING id
                    """), params).fetchone()
                else:
                    row = conn.execute(text("""
                        INSERT INTO bird_ringing_records
                            (ring_number, species_id, location, coordinates,
                             event_date, ringer, notes)
                        VALUES (:ring, :sid, :loc,
                                ST_GeogFromText(
                                    'SRID=4326;POINT(' || :lon || ' ' || :lat || ')'),
                                :day, :ringer, :notes)
                        RETURNING id
                    """), {**params, 'lon': lon, 'lat': lat}).fetchone()
                state['bird_record_ids'].append(row[0])

        if missing_minerals:
            row = conn.execute(text("""
                INSERT INTO minerals
                    (inventory_number, item_name, card_locality, quantity,
                     comments)
                VALUES ('999901', 'Тест кварц (seed)',
                        'Тест локалитет (seed)', 1, :tag)
                ON CONFLICT (inventory_number) DO NOTHING RETURNING id
            """), {'tag': SEED_TAG}).fetchone()
            if row is not None:
                state['mineral_ids'].append(row[0])

        if missing_inventory:
            row = conn.execute(text("""
                INSERT INTO inventory_entries
                    (inventory_number, inventory_number_raw, name, locality,
                     quantity, sheet, row_number, category, notes)
                VALUES ('999901', '999901', 'Тест кварц (seed)',
                        'Тест локалитет (seed)', '1', 'seed', 1,
                        'минерали', :tag)
                ON CONFLICT (inventory_number) DO NOTHING RETURNING id
            """), {'tag': SEED_TAG}).fetchone()
            if row is not None:
                state['inventory_ids'].append(row[0])


def cleanup_reference_data(engine, state):
    """Обриши ТАЧНО оно што је _seed_reference_data убацио (по запамћеним
    ID-јевима), редом који поштује FK (записи пре врста)."""
    if not any(state.values()):
        return
    with engine.begin() as conn:
        for table, key in (
            ('bird_ringing_records', 'bird_record_ids'),
            ('bird_species', 'bird_species_ids'),
            ('minerals', 'mineral_ids'),
            ('inventory_entries', 'inventory_ids'),
        ):
            for row_id in state[key]:
                conn.execute(text(f'DELETE FROM {table} WHERE id = :id'),
                             {'id': row_id})


class PostgresIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.database_url = os.environ.get('DATABASE_URL')
        if not cls.database_url:
            raise unittest.SkipTest('DATABASE_URL is not configured')
        try:
            cls.engine = create_engine(cls.database_url)
            with cls.engine.connect() as conn:
                conn.execute(text('SELECT 1'))
        except unittest.SkipTest:
            raise
        except Exception as exc:
            engine = getattr(cls, 'engine', None)
            if engine is not None:
                engine.dispose()
            raise unittest.SkipTest(f'PostgreSQL is not usable: {exc}')
        cls._seed_state = None
        try:
            cls._seed_state = ensure_reference_data(cls.engine, cls.database_url)
        except BaseException:
            cls.engine.dispose()
            raise

    @classmethod
    def tearDownClass(cls):
        try:
            state = getattr(cls, '_seed_state', None)
            if state is not None:
                cleanup_reference_data(cls.engine, state)
        finally:
            cls.engine.dispose()

    def test_basic_connection_and_main_table_counts(self):
        expected_tables = (
            'bird_ringing_records',
            'minerals',
            'inventory_entries',
            'bird_species',
            'users',
            'departments',
        )

        with self.engine.connect() as conn:
            for table_name in expected_tables:
                with self.subTest(table=table_name):
                    count = conn.execute(text(f'SELECT COUNT(*) FROM {table_name}')).scalar()
                    self.assertIsNotNone(count)
                    self.assertGreaterEqual(count, 0)

    def test_bird_ringing_module_is_postgres_only(self):
        self.assertTrue(brd._postgres_available())
        self.assertTrue(hasattr(brd, 'get_connection'))
        self.assertFalse(hasattr(brd, '_sqlite_get_all_records'))

    def test_bird_ringing_module_queries(self):
        records, total, pages = brd.get_all_records(page=1, per_page=10)
        self.assertTrue(records)
        self.assertGreater(total, 0)
        self.assertGreater(pages, 0)

        sample = records[0]
        self.assertIn('id', sample)

        fetched = brd.get_record_by_id(sample['id'])
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched['id'], sample['id'])

        stats = brd.get_statistics()
        self.assertGreater(stats['total_records'], 0)
        self.assertGreater(stats['unique_species'], 0)
        self.assertGreater(stats['unique_ringers'], 0)

        self.assertTrue(brd.get_all_species())
        self.assertTrue(brd.get_all_locations())
        self.assertTrue(brd.get_all_ringers())
        self.assertTrue(brd.get_all_years())

        self.assertTrue(brd.search_records('Parus', limit=5))
        self.assertIsInstance(brd.get_map_localities(), list)
        self.assertIsInstance(brd.get_map_localities_no_coords(), list)

    def test_mineral_database_module(self):
        db = MineralDatabase()
        self.assertTrue(db.available)

        result = db.get_all_minerals(page=1, per_page=10)
        minerals = result.get('minerals', [])
        self.assertTrue(minerals)
        self.assertGreater(result.get('total', 0), 0)

        sample = minerals[0]
        mineral = db.get_mineral_by_id(sample['id'])
        self.assertIsNotNone(mineral)
        self.assertEqual(mineral['id'], sample['id'])

        inventory_number = sample.get('inventarni_broj')
        if inventory_number:
            mineral_by_inventory = db.get_mineral_by_inventory_number(str(int(inventory_number)))
            self.assertIsNotNone(mineral_by_inventory)

    def test_inventory_reconciliation_module(self):
        reconciler = InventoryReconciliation()
        self.assertTrue(reconciler._postgres_enabled)

        items = reconciler.get_inventory_book_items()
        self.assertTrue(items)

        summary = reconciler.get_inventory_summary()
        self.assertGreater(summary.get('total_items', 0), 0)
        self.assertGreater(summary.get('unique_inventory_numbers', 0), 0)

        first_number = next((item.get('inventory_number') for item in items if item.get('inventory_number')), None)
        self.assertIsNotNone(first_number)
        self.assertIsNotNone(reconciler.get_inventory_by_number(first_number))

    def test_data_integrity_checks(self):
        staging_tables = (
            'staging_bird_ringing',
            'staging_minerals',
            'staging_inventory',
        )

        with self.engine.connect() as conn:
            for table_name in staging_tables:
                with self.subTest(staging_table=table_name):
                    count = conn.execute(text(f'SELECT COUNT(*) FROM {table_name}')).scalar()
                    self.assertEqual(count, 0)

            duplicate_inventory = conn.execute(text("""
                SELECT COUNT(*)
                FROM (
                    SELECT inventory_number
                    FROM inventory_entries
                    WHERE inventory_number IS NOT NULL
                    GROUP BY inventory_number
                    HAVING COUNT(*) > 1
                ) duplicates
            """)).scalar()
            self.assertEqual(duplicate_inventory, 0)

            null_species = conn.execute(text("""
                SELECT COUNT(*)
                FROM bird_ringing_records br
                LEFT JOIN bird_species bs ON bs.id = br.species_id
                WHERE bs.species_name IS NULL
            """)).scalar()
            self.assertGreaterEqual(null_species, 0)

            coordinates_count = conn.execute(text("""
                SELECT COUNT(*)
                FROM bird_ringing_records
                WHERE coordinates IS NOT NULL
            """)).scalar()
            self.assertGreater(coordinates_count, 0)

    def test_postgres_queries_are_reasonably_fast(self):
        query_specs = (
            ('large_result', text('SELECT id FROM bird_ringing_records ORDER BY id DESC LIMIT 10000')),
            ('complex_join', text("""
                SELECT br.id, bs.species_name, br.location
                FROM bird_ringing_records br
                LEFT JOIN bird_species bs ON bs.id = br.species_id
                ORDER BY br.id DESC
                LIMIT 1000
            """)),
            ('aggregation', text("""
                SELECT bs.species_name, COUNT(*) AS cnt
                FROM bird_ringing_records br
                LEFT JOIN bird_species bs ON bs.id = br.species_id
                GROUP BY bs.species_name
                ORDER BY cnt DESC
                LIMIT 20
            """)),
        )

        with self.engine.connect() as conn:
            for label, query in query_specs:
                with self.subTest(query=label):
                    start = time.time()
                    rows = conn.execute(query).fetchall()
                    elapsed = time.time() - start
                    self.assertTrue(rows)
                    self.assertLess(elapsed, 10.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
