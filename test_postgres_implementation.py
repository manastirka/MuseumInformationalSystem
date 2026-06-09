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

    @classmethod
    def tearDownClass(cls):
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
