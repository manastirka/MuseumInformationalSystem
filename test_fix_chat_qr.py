"""Reproducing tests for the chat-qr cluster bug.

Bug: chat_room.py functions borrow a (potentially pooled) DB connection via
_get_db() and call db.close() at the END of the function with NO try/finally
and NO context manager. If any db.execute(...) raises, db.close() is skipped,
so a pooled connection is never returned to the pool (putconn) and leaks.
After enough leaks the pool is exhausted.

These tests prove that the connection is always returned (close() is called)
even when a query raises, by counting acquire vs. close on a fake connection.
"""

import os
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-chat-qr')

import pytest  # noqa: E402

import chat_room  # noqa: E402


class FakeCursor:
    def fetchone(self):
        return None

    def fetchall(self):
        return []


class FakeConnection:
    """Stand-in for ManagedPostgresConnection that records close()/commit().

    execute() raises on the call indicated by raise_on_call (1-based) to
    simulate a query failing mid-function.
    """

    def __init__(self, raise_on_call=None):
        self.execute_calls = 0
        self.raise_on_call = raise_on_call
        self.closed = False
        self.committed = False

    def execute(self, *args, **kwargs):
        self.execute_calls += 1
        if self.raise_on_call is not None and self.execute_calls == self.raise_on_call:
            raise RuntimeError('simulated DB failure')
        return FakeCursor()

    def commit(self):
        self.committed = True

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if exc_type is None:
                self.commit()
        finally:
            self.close()
        return False


@pytest.fixture(autouse=True)
def _schema_ready():
    # Avoid running the schema SQL path inside _get_db during these unit tests.
    chat_room._schema_ready = True
    yield


def _patch_db(fake):
    return patch.object(chat_room, 'get_postgres_connection', return_value=fake)


def test_touch_presence_returns_connection_on_query_error():
    fake = FakeConnection(raise_on_call=1)
    with _patch_db(fake):
        with pytest.raises(RuntimeError):
            chat_room.touch_presence(1, 'Тест', 'test@museum.rs')
    assert fake.closed, 'connection leaked: close() never called when execute() raised'


def test_get_online_users_returns_connection_on_query_error():
    fake = FakeConnection(raise_on_call=1)
    with _patch_db(fake):
        with pytest.raises(RuntimeError):
            chat_room.get_online_users()
    assert fake.closed, 'connection leaked: close() never called when execute() raised'


def test_send_message_returns_connection_on_query_error():
    fake = FakeConnection(raise_on_call=1)
    with _patch_db(fake):
        with pytest.raises(RuntimeError):
            chat_room.send_message(1, 'Тест', 'test@museum.rs', 'Dept', message='hi')
    assert fake.closed, 'connection leaked: close() never called when execute() raised'


def test_get_user_channels_returns_connection_on_query_error():
    fake = FakeConnection(raise_on_call=1)
    with _patch_db(fake):
        with pytest.raises(RuntimeError):
            chat_room.get_user_channels(5)
    assert fake.closed, 'connection leaked: close() never called when execute() raised'


def test_get_messages_returns_connection_on_query_error():
    fake = FakeConnection(raise_on_call=1)
    with _patch_db(fake):
        with pytest.raises(RuntimeError):
            chat_room.get_messages()
    assert fake.closed, 'connection leaked: close() never called when execute() raised'


def test_mark_channel_read_returns_connection_on_query_error():
    fake = FakeConnection(raise_on_call=1)
    with _patch_db(fake):
        with pytest.raises(RuntimeError):
            chat_room.mark_channel_read(1, 'general')
    assert fake.closed, 'connection leaked: close() never called when execute() raised'


def test_set_user_status_returns_connection_on_query_error():
    fake = FakeConnection(raise_on_call=1)
    with _patch_db(fake):
        with pytest.raises(RuntimeError):
            chat_room.set_user_status(1, 'busy')
    assert fake.closed, 'connection leaked: close() never called when execute() raised'


def test_clear_presence_returns_connection_on_query_error():
    fake = FakeConnection(raise_on_call=1)
    with _patch_db(fake):
        with pytest.raises(RuntimeError):
            chat_room.clear_presence(1)
    assert fake.closed, 'connection leaked: close() never called when execute() raised'


def test_get_user_channels_returns_connection_on_malformed_channel():
    """The int(parts[1]) parse on a malformed dm channel raises mid-loop;
    the connection must still be returned."""
    fake = FakeConnection()

    def execute(sql, params=None):
        fake.execute_calls += 1
        # First call is the DISTINCT channel listing; return a malformed dm row.
        if fake.execute_calls == 1:
            cur = FakeCursor()
            cur.fetchall = lambda: [{'channel': 'dm:abc:5'}]
            return cur
        return FakeCursor()

    fake.execute = execute
    with _patch_db(fake):
        with pytest.raises(ValueError):
            chat_room.get_user_channels(5)
    assert fake.closed, 'connection leaked: close() never called when int() parse raised'


def test_touch_presence_commits_and_closes_on_success():
    fake = FakeConnection()
    with _patch_db(fake):
        chat_room.touch_presence(1, 'Тест', 'test@museum.rs', status='online')
    assert fake.committed, 'success path must commit'
    assert fake.closed, 'success path must return the connection'
