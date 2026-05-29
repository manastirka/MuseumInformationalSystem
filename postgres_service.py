"""Shared PostgreSQL connection helpers."""

import atexit
import logging
import os
from pathlib import Path
from typing import Any

import psycopg
from dotenv import load_dotenv

try:
    from psycopg_pool import ConnectionPool

    POOL_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    ConnectionPool = None
    POOL_AVAILABLE = False


load_dotenv(Path(__file__).resolve().parent / '.env')

logger = logging.getLogger(__name__)
_connection_pools: dict[tuple[tuple[str, Any], ...], ConnectionPool] = {}


def _pool_key(kwargs: dict[str, Any]) -> tuple[tuple[str, Any], ...]:
    """Build a stable cache key for pool kwargs."""
    return tuple(sorted(kwargs.items(), key=lambda item: item[0]))


def pooling_enabled() -> bool:
    """Return whether connection pooling should be used in this process."""
    override = os.environ.get('POSTGRES_POOL_ENABLED')
    if override is not None:
        return override.strip().lower() == 'true'
    return os.environ.get('FLASK_ENV', 'production').strip().lower() == 'production'


def _with_default_connect_timeout(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Apply a short default connect timeout so failed DB attempts fail fast."""
    resolved = dict(kwargs)
    if 'connect_timeout' not in resolved:
        timeout_value = os.environ.get('POSTGRES_CONNECT_TIMEOUT', '2').strip()
        if timeout_value:
            resolved['connect_timeout'] = int(timeout_value)
    return resolved


def get_connection_pool(**kwargs):
    """Get or create a shared psycopg connection pool for the given kwargs."""
    kwargs = _with_default_connect_timeout(kwargs)
    if not POOL_AVAILABLE or not pooling_enabled():
        return None

    key = _pool_key(kwargs)
    pool = _connection_pools.get(key)
    if pool is None:
        pool = ConnectionPool(
            conninfo=get_database_url(),
            min_size=int(os.environ.get('POSTGRES_POOL_MIN_SIZE', '1')),
            max_size=int(os.environ.get('POSTGRES_POOL_MAX_SIZE', '10')),
            max_idle=int(os.environ.get('POSTGRES_POOL_MAX_IDLE', '300')),
            max_lifetime=int(os.environ.get('POSTGRES_POOL_MAX_LIFETIME', '3600')),
            kwargs=kwargs or None,
        )
        _connection_pools[key] = pool
        logger.info(
            "PostgreSQL connection pool initialized (min=%s, max=%s, kwargs=%s)",
            pool.min_size,
            pool.max_size,
            sorted(kwargs.keys()),
        )
    return pool


def close_connection_pools():
    """Close all cached pools on process shutdown."""
    for key, pool in list(_connection_pools.items()):
        try:
            pool.close()
        finally:
            _connection_pools.pop(key, None)


atexit.register(close_connection_pools)


class ManagedPostgresConnection:
    """Connection wrapper that returns pooled connections instead of closing them."""

    def __init__(self, conn, *, pool=None):
        self._conn = conn
        self._pool = pool
        self._closed = False

    def __getattr__(self, name):
        return getattr(self._conn, name)

    def close(self):
        """Return pooled connection to the pool or close the direct connection."""
        if self._closed:
            return
        self._closed = True
        if self._pool is not None:
            self._pool.putconn(self._conn)
        else:
            close_fn = getattr(self._conn, 'close', None)
            if callable(close_fn):
                close_fn()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if not getattr(self._conn, 'autocommit', False):
                if exc_type is None:
                    self._conn.commit()
                else:
                    self._conn.rollback()
        finally:
            self.close()
        return False


def get_database_url():
    """Return DATABASE_URL normalized for psycopg."""
    db_url = os.environ.get('DATABASE_URL', '')
    db_url = db_url.replace('postgresql+psycopg://', 'postgresql://')
    if not db_url:
        raise RuntimeError('DATABASE_URL is not configured')
    return db_url


def get_postgres_connection(**kwargs):
    """Create a psycopg connection using the configured database URL."""
    kwargs = _with_default_connect_timeout(kwargs)
    pool = get_connection_pool(**kwargs)
    if pool is not None:
        return ManagedPostgresConnection(pool.getconn(), pool=pool)
    return ManagedPostgresConnection(psycopg.connect(get_database_url(), **kwargs))
