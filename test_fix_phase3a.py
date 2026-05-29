#!/usr/bin/env python3
"""Regression tests for phase3a_databases connection-leak fixes.

These tests verify that every accessor in phase3a_databases.py returns its
borrowed pooled connection (i.e. calls conn.close(), which maps to
pool.putconn) on the exception path, not only on the success path. A leaked
connection permanently consumes a pool slot and eventually exhausts the pool.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-phase3a')
os.environ.setdefault('DATABASE_URL', 'postgresql://user@localhost/db')

import unittest
from unittest.mock import patch

import phase3a_databases


class FakeCursor:
    """Cursor whose execute() raises after the first call to simulate a
    mid-operation DB error (malformed row, missing column, transient error)."""

    def __init__(self, fail_after=0):
        self.fail_after = fail_after
        self.execute_calls = 0
        self.closed = False
        self.description = [('id',)]

    def execute(self, *args, **kwargs):
        self.execute_calls += 1
        if self.execute_calls > self.fail_after:
            raise RuntimeError('simulated DB failure mid-operation')

    def fetchall(self):
        return []

    def fetchone(self):
        return None

    def close(self):
        self.closed = True


class FakeConn:
    """Tracks whether the borrowed connection was returned via close()."""

    def __init__(self, fail_after=0):
        self.autocommit = False
        self.cursor_obj = FakeCursor(fail_after=fail_after)
        self.close_calls = 0
        self.commit_calls = 0
        self.rollback_calls = 0

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.commit_calls += 1

    def rollback(self):
        self.rollback_calls += 1

    def close(self):
        self.close_calls += 1


class Phase3AConnectionLeakTests(unittest.TestCase):
    """Each read accessor must close the connection even when a query fails."""

    def _run_and_assert_closed(self, func, *args, **kwargs):
        fake_conn = FakeConn(fail_after=0)
        with patch.object(phase3a_databases, 'get_postgres_connection', return_value=fake_conn):
            func(*args, **kwargs)
        self.assertEqual(
            fake_conn.close_calls,
            1,
            f"{func.__name__} leaked its pooled connection on the error path",
        )

    def test_get_library_database_closes_on_error(self):
        self._run_and_assert_closed(phase3a_databases.get_library_database)

    def test_load_exhibitions_data_closes_on_error(self):
        self._run_and_assert_closed(phase3a_databases.load_exhibitions_data)

    def test_get_cultural_heritage_database_closes_on_error(self):
        self._run_and_assert_closed(phase3a_databases.get_cultural_heritage_database)

    def test_get_meteorite_collection_database_closes_on_error(self):
        self._run_and_assert_closed(phase3a_databases.get_meteorite_collection_database)

    def test_load_employee_directory_closes_on_error(self):
        self._run_and_assert_closed(phase3a_databases.load_employee_directory)

    def test_get_news_database_closes_on_error(self):
        self._run_and_assert_closed(phase3a_databases.get_news_database)

    def test_get_collection_by_type_closes_on_error(self):
        self._run_and_assert_closed(phase3a_databases.get_collection_by_type, 'botany')

    def test_test_connection_closes_on_error(self):
        self._run_and_assert_closed(phase3a_databases.test_connection)


class Phase3AVehicleLeakTests(unittest.TestCase):
    """Vehicle accessors re-raise on error; they must still close the conn."""

    def _run_and_assert_closed(self, func, *args, **kwargs):
        fake_conn = FakeConn(fail_after=0)
        with patch.object(phase3a_databases, 'get_postgres_connection', return_value=fake_conn):
            with self.assertRaises(RuntimeError):
                func(*args, **kwargs)
        self.assertEqual(
            fake_conn.close_calls,
            1,
            f"{func.__name__} leaked its pooled connection on the error path",
        )

    def test_get_vehicles_list_closes_on_error(self):
        self._run_and_assert_closed(phase3a_databases.get_vehicles_list)

    def test_get_vehicle_by_id_closes_on_error(self):
        self._run_and_assert_closed(phase3a_databases.get_vehicle_by_id, 1)

    def test_get_vehicle_reservations_closes_on_error(self):
        self._run_and_assert_closed(phase3a_databases.get_vehicle_reservations)

    def test_get_active_vehicle_reservations_closes_on_error(self):
        self._run_and_assert_closed(phase3a_databases.get_active_vehicle_reservations)

    def test_get_vehicle_availability_closes_on_error(self):
        self._run_and_assert_closed(phase3a_databases.get_vehicle_availability)

    def test_get_vehicle_usage_stats_closes_on_error(self):
        self._run_and_assert_closed(phase3a_databases.get_vehicle_usage_stats)


class Phase3ASuccessPathTests(unittest.TestCase):
    """The finally-based close must not break the normal success path."""

    def test_get_library_database_success_closes_once(self):
        fake_conn = FakeConn(fail_after=99)
        with patch.object(phase3a_databases, 'get_postgres_connection', return_value=fake_conn):
            result = phase3a_databases.get_library_database()
        self.assertIn('books', result)
        self.assertEqual(result['books'], [])
        # Success path calls conn.close() once; the finally close is a no-op
        # because ManagedPostgresConnection.close() is idempotent. The fake
        # here is not idempotent, so it records the explicit + finally close.
        self.assertGreaterEqual(fake_conn.close_calls, 1)


class Phase3ASaveLibraryBookTests(unittest.TestCase):
    """save_library_book must roll back AND close on the error path."""

    def test_save_library_book_rolls_back_and_closes_on_error(self):
        fake_conn = FakeConn(fail_after=0)
        with patch.object(phase3a_databases, 'get_postgres_connection', return_value=fake_conn):
            result = phase3a_databases.save_library_book({'title': 'X'})
        self.assertIsNone(result)
        self.assertEqual(
            fake_conn.close_calls,
            1,
            "save_library_book leaked its pooled connection on the error path",
        )
        self.assertEqual(
            fake_conn.rollback_calls,
            1,
            "save_library_book did not roll back the aborted transaction",
        )
        self.assertEqual(fake_conn.commit_calls, 0)


if __name__ == '__main__':
    unittest.main()
