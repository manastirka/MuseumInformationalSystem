#!/usr/bin/env python3
"""Automated PostgreSQL connection smoke tests."""

import os
import unittest
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv(Path(__file__).resolve().parent / '.env')


class PostgresConnectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            raise unittest.SkipTest('DATABASE_URL is not configured')
        try:
            cls.engine = create_engine(database_url)
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

    def test_core_tables_are_reachable(self):
        expected_tables = {
            'bird_ringing_records': 1,
            'minerals': 1,
            'inventory_entries': 1,
        }

        with self.engine.connect() as conn:
            for table_name, min_rows in expected_tables.items():
                with self.subTest(table=table_name):
                    count = conn.execute(text(f'SELECT COUNT(*) FROM {table_name}')).scalar()
                    self.assertIsNotNone(count)
                    self.assertGreaterEqual(count, min_rows)


if __name__ == '__main__':
    unittest.main(verbosity=2)
