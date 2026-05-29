"""Reproducing tests for chat-qr cluster crash bugs in chat_views.py.

These tests target three confirmed MEDIUM findings:
  1. Non-numeric DM channel segments -> ValueError -> HTTP 500
     (api_chat_messages, api_chat_send).
  2. Non-numeric ?since parameter -> ValueError -> HTTP 500
     (api_chat_messages).
  3. Non-object JSON body -> AttributeError -> HTTP 500
     (api_chat_send, api_chat_status).

The fix turns each of these into a clean 400 response instead of a crash.
"""

import os
import sys
import types

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-chat-qr')

import pytest
from flask import Flask


def _install_fake_chat_room():
    """Provide a stub chat_room module so chat_views imports succeed
    without touching the database/network. Records calls so we can assert
    that handler logic short-circuits before reaching them on bad input."""
    fake = types.ModuleType('chat_room')

    calls = {'send_message': 0, 'set_user_status': 0}

    class _Path:
        def __truediv__(self, other):
            return self

        def mkdir(self, *a, **k):
            pass

    fake.CHAT_FILES_DIR = _Path()
    fake.VALID_STATUSES = {'online', 'away', 'busy', 'offline'}

    def touch_presence(*a, **k):
        return None

    def get_messages(*a, **k):
        return []

    def get_online_users(*a, **k):
        return []

    def get_user_channels(*a, **k):
        return []

    def mark_channel_read(*a, **k):
        return None

    def send_message(*a, **k):
        calls['send_message'] += 1
        return {'id': 1}

    def set_user_status(*a, **k):
        calls['set_user_status'] += 1
        return None

    def clear_presence(*a, **k):
        return None

    fake.touch_presence = touch_presence
    fake.get_messages = get_messages
    fake.get_online_users = get_online_users
    fake.get_user_channels = get_user_channels
    fake.mark_channel_read = mark_channel_read
    fake.send_message = send_message
    fake.set_user_status = set_user_status
    fake.clear_presence = clear_presence
    fake._calls = calls

    sys.modules['chat_room'] = fake
    return fake


@pytest.fixture
def app_and_chat():
    import importlib

    prev_chat_room = sys.modules.get('chat_room')
    fake = _install_fake_chat_room()

    import chat_views as cv
    importlib.reload(cv)

    app = Flask(__name__)
    app.secret_key = 'test-secret'
    try:
        yield app, cv, fake
    finally:
        # Restore the real chat_room module (and rebind chat_views to it) so we
        # don't leave a stub in sys.modules that breaks other test files.
        if prev_chat_room is not None:
            sys.modules['chat_room'] = prev_chat_room
        else:
            sys.modules.pop('chat_room', None)
        importlib.reload(cv)


def _set_session(sess):
    sess['user_id'] = 5
    sess['user_name'] = 'Tester'
    sess['user_email'] = 'tester@example.com'
    sess['user_department'] = 'IT'


# --- Finding 1: non-numeric DM channel segment ---

def test_messages_non_numeric_dm_channel_returns_400(app_and_chat):
    app, cv, _fake = app_and_chat
    with app.test_request_context('/api/chat/messages?channel=dm:abc:1'):
        from flask import session
        _set_session(session)
        resp = cv.api_chat_messages()
        body = resp[0] if isinstance(resp, tuple) else resp
        status = resp[1] if isinstance(resp, tuple) else 200
        assert status == 400
        assert body.get_json()['success'] is False


def test_send_non_numeric_dm_channel_returns_400(app_and_chat):
    app, cv, fake = app_and_chat
    with app.test_request_context(
        '/api/chat/send',
        method='POST',
        json={'message': 'hi', 'channel': 'dm:abc:5'},
    ):
        from flask import session
        _set_session(session)
        resp = cv.api_chat_send()
        status = resp[1] if isinstance(resp, tuple) else 200
        assert status == 400
        # Must short-circuit before persisting.
        assert fake._calls['send_message'] == 0


# --- Finding 2: non-numeric ?since parameter ---

def test_messages_non_numeric_since_does_not_crash(app_and_chat):
    app, cv, _fake = app_and_chat
    with app.test_request_context('/api/chat/messages?since=abc&channel=general'):
        from flask import session
        _set_session(session)
        resp = cv.api_chat_messages()
        # Falls back to 0.0 and serves normally (200).
        status = resp[1] if isinstance(resp, tuple) else 200
        assert status == 200
        assert resp.get_json()['success'] is True


# --- Finding 3: non-object JSON body ---

def test_send_non_object_json_returns_400(app_and_chat):
    app, cv, fake = app_and_chat
    with app.test_request_context(
        '/api/chat/send',
        method='POST',
        data='null',
        content_type='application/json',
    ):
        from flask import session
        _set_session(session)
        resp = cv.api_chat_send()
        status = resp[1] if isinstance(resp, tuple) else 200
        assert status == 400
        assert fake._calls['send_message'] == 0


def test_send_scalar_json_returns_400(app_and_chat):
    app, cv, fake = app_and_chat
    with app.test_request_context(
        '/api/chat/send',
        method='POST',
        data='42',
        content_type='application/json',
    ):
        from flask import session
        _set_session(session)
        resp = cv.api_chat_send()
        status = resp[1] if isinstance(resp, tuple) else 200
        assert status == 400
        assert fake._calls['send_message'] == 0


def test_status_non_object_json_returns_400(app_and_chat):
    app, cv, fake = app_and_chat
    with app.test_request_context(
        '/api/chat/status',
        method='POST',
        data='null',
        content_type='application/json',
    ):
        from flask import session
        _set_session(session)
        resp = cv.api_chat_status()
        status = resp[1] if isinstance(resp, tuple) else 200
        assert status == 400
        assert fake._calls['set_user_status'] == 0


def test_status_list_json_returns_400(app_and_chat):
    app, cv, fake = app_and_chat
    with app.test_request_context(
        '/api/chat/status',
        method='POST',
        data='[]',
        content_type='application/json',
    ):
        from flask import session
        _set_session(session)
        resp = cv.api_chat_status()
        status = resp[1] if isinstance(resp, tuple) else 200
        assert status == 400
        assert fake._calls['set_user_status'] == 0
