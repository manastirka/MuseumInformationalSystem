#!/usr/bin/env python3
"""Regression tests for PostgreSQL connection pooling and safe wrappers."""

import importlib
import unittest
from unittest.mock import patch

import image_database_manager
import image_storage_engine
import postgres_service


class FakeConn:
    def __init__(self, *, autocommit=False):
        self.autocommit = autocommit
        self.commit_calls = 0
        self.rollback_calls = 0
        self.close_calls = 0

    def commit(self):
        self.commit_calls += 1

    def rollback(self):
        self.rollback_calls += 1

    def close(self):
        self.close_calls += 1


class FakePool:
    min_size = 1
    max_size = 10

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.conn = FakeConn()
        self.getconn_calls = 0
        self.putconn_calls = 0
        self.closed = False

    def getconn(self):
        self.getconn_calls += 1
        return self.conn

    def putconn(self, conn):
        self.putconn_calls += 1
        self.returned_conn = conn

    def close(self):
        self.closed = True


class PostgresConnectionPoolingTests(unittest.TestCase):
    def setUp(self):
        postgres_service.close_connection_pools()

    def tearDown(self):
        postgres_service.close_connection_pools()

    def test_get_connection_pool_reuses_pool_for_same_kwargs(self):
        with patch.object(postgres_service, 'POOL_AVAILABLE', True), patch.object(
            postgres_service,
            'ConnectionPool',
            FakePool,
        ), patch.dict(
            'os.environ',
            {
                'DATABASE_URL': 'postgresql+psycopg://user@localhost/db',
                'POSTGRES_POOL_ENABLED': 'true',
            },
            clear=False,
        ):
            first = postgres_service.get_connection_pool(row_factory='dict')
            second = postgres_service.get_connection_pool(row_factory='dict')

        self.assertIs(first, second)

    def test_get_connection_pool_applies_default_connect_timeout(self):
        with patch.object(postgres_service, 'POOL_AVAILABLE', True), patch.object(
            postgres_service,
            'ConnectionPool',
            FakePool,
        ), patch.dict(
            'os.environ',
            {
                'DATABASE_URL': 'postgresql+psycopg://user@localhost/db',
                'POSTGRES_POOL_ENABLED': 'true',
                'POSTGRES_CONNECT_TIMEOUT': '3',
            },
            clear=False,
        ):
            pool = postgres_service.get_connection_pool(row_factory='dict')

        self.assertEqual(pool.kwargs['kwargs']['connect_timeout'], 3)

    def test_direct_postgres_connection_applies_default_connect_timeout(self):
        fake_conn = FakeConn()

        with patch.object(postgres_service, 'POOL_AVAILABLE', False), patch.object(
            postgres_service.psycopg,
            'connect',
            return_value=fake_conn,
        ) as mocked_connect, patch.dict(
            'os.environ',
            {
                'DATABASE_URL': 'postgresql+psycopg://user@localhost/db',
                'POSTGRES_CONNECT_TIMEOUT': '4',
            },
            clear=False,
        ):
            wrapped = postgres_service.get_postgres_connection()

        self.assertIsInstance(wrapped, postgres_service.ManagedPostgresConnection)
        mocked_connect.assert_called_once()
        self.assertEqual(mocked_connect.call_args.kwargs['connect_timeout'], 4)

    def test_managed_connection_returns_pooled_connection_on_close(self):
        fake_pool = FakePool()
        wrapped = postgres_service.ManagedPostgresConnection(fake_pool.getconn(), pool=fake_pool)

        wrapped.close()

        self.assertEqual(fake_pool.putconn_calls, 1)
        self.assertEqual(fake_pool.conn.close_calls, 0)

    def test_managed_connection_rolls_back_on_error_and_returns_to_pool(self):
        fake_pool = FakePool()
        wrapped = postgres_service.ManagedPostgresConnection(fake_pool.getconn(), pool=fake_pool)

        with self.assertRaises(RuntimeError):
            with wrapped:
                raise RuntimeError('boom')

        self.assertEqual(fake_pool.conn.rollback_calls, 1)
        self.assertEqual(fake_pool.putconn_calls, 1)

    def test_managed_connection_commits_on_successful_context_exit(self):
        fake_pool = FakePool()
        wrapped = postgres_service.ManagedPostgresConnection(fake_pool.getconn(), pool=fake_pool)

        with wrapped:
            pass

        self.assertEqual(fake_pool.conn.commit_calls, 1)
        self.assertEqual(fake_pool.putconn_calls, 1)

    def test_image_helpers_use_shared_postgres_service(self):
        fake_conn = object()

        with patch.object(image_database_manager, 'get_postgres_connection', return_value=fake_conn):
            self.assertIs(image_database_manager._get_db_connection(), fake_conn)

        with patch.object(image_storage_engine, 'get_postgres_connection', return_value=fake_conn):
            self.assertIs(image_storage_engine._get_db_connection(), fake_conn)


if __name__ == '__main__':
    unittest.main()
