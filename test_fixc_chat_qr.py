"""Phase C low-severity hardening tests for the chat-qr cluster.

Covers:
- qr_label_views: label-format routes enforce minerals access for mineral_boxes.
- chat_room.mark_channel_read: marks read up to a caller-supplied timestamp.
- chat_views.api_chat_messages: cursor not advanced past messages fetched.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-chat-qr')

import time
from unittest import mock

import pytest

import qr_label_views


class _StopRedirect(Exception):
    """Sentinel raised by the access-check mock to prove it was invoked."""


def _noop(*_args, **_kwargs):
    return ''


# --- Finding 1: mineral_boxes must enforce 'minerals' collection access ---

def test_label_format_enforces_minerals_access_for_mineral_boxes():
    calls = []

    def fake_access(collection_type):
        calls.append(collection_type)
        # Simulate a denied user: return a truthy redirect.
        return 'REDIRECT'

    result = qr_label_views.render_admin_qr_label_format(
        'mineral_boxes',
        normalize_qr_collection_type=lambda c: c,
        ensure_qr_collection_access=fake_access,
        get_qr_collection_name=_noop,
        get_qr_collection_url=_noop,
    )

    assert calls == ['minerals'], (
        'mineral_boxes must be access-checked against the minerals collection'
    )
    assert result == 'REDIRECT'


def test_labels_with_format_enforces_minerals_access_for_mineral_boxes():
    calls = []

    def fake_access(collection_type):
        calls.append(collection_type)
        return 'REDIRECT'

    result = qr_label_views.handle_admin_qr_labels_with_format(
        'mineral_boxes',
        normalize_qr_collection_type=lambda c: c,
        ensure_qr_collection_access=fake_access,
        get_qr_collection_url=_noop,
    )

    assert calls == ['minerals']
    assert result == 'REDIRECT'


def test_label_format_still_checks_non_box_collection_directly():
    calls = []

    def fake_access(collection_type):
        calls.append(collection_type)
        return 'REDIRECT'

    result = qr_label_views.render_admin_qr_label_format(
        'meteorite',
        normalize_qr_collection_type=lambda c: c,
        ensure_qr_collection_access=fake_access,
        get_qr_collection_name=_noop,
        get_qr_collection_url=_noop,
    )

    assert calls == ['meteorite']
    assert result == 'REDIRECT'


# --- Finding 2: mark_channel_read must not advance past fetched messages ---

def test_mark_channel_read_accepts_up_to_epoch():
    import chat_room

    captured = {}

    class _FakeDB:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def execute(self, sql, params):
            captured['params'] = params
            return self

    with mock.patch.object(chat_room, '_get_db', return_value=_FakeDB()):
        chat_room.mark_channel_read(42, 'general', up_to_epoch=123.5)

    assert captured['params'] == (42, 'general', 123.5)


def test_mark_channel_read_defaults_to_now_when_not_supplied():
    import chat_room

    captured = {}

    class _FakeDB:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def execute(self, sql, params):
            captured['params'] = params
            return self

    before = time.time()
    with mock.patch.object(chat_room, '_get_db', return_value=_FakeDB()):
        chat_room.mark_channel_read(7, 'general')
    after = time.time()

    user_id, channel, epoch = captured['params']
    assert user_id == 7
    assert channel == 'general'
    assert before <= epoch <= after


def test_api_chat_messages_marks_read_no_later_than_fetch_start():
    """A message arriving after the fetch must not be silently marked read."""
    import app as museum_app
    import chat_views

    recorded = {}

    def fake_get_messages(since_epoch=0, limit=100, channel='general'):
        # Simulate a message inserted concurrently AFTER the fetch began.
        time.sleep(0.02)
        return []

    def fake_mark_channel_read(user_id, channel, up_to_epoch=None):
        recorded['up_to_epoch'] = up_to_epoch
        recorded['mark_time'] = time.time()

    with museum_app.app.test_request_context('/api/chat/messages?channel=general'):
        from flask import session

        session['user_id'] = 1
        session['user_name'] = 'Tester'
        session['user_email'] = 'tester@example.com'

        with mock.patch('chat_room.get_messages', side_effect=fake_get_messages), \
             mock.patch('chat_room.get_online_users', return_value=[]), \
             mock.patch('chat_room.get_user_channels', return_value=[]), \
             mock.patch('chat_room.mark_channel_read', side_effect=fake_mark_channel_read), \
             mock.patch('chat_room.touch_presence'):
            fetch_start = time.time()
            chat_views.api_chat_messages()

    assert recorded['up_to_epoch'] is not None
    # The cursor must be stamped no later than the moment the fetch started,
    # i.e. strictly before the post-fetch wall clock.
    assert recorded['up_to_epoch'] <= recorded['mark_time']
    assert recorded['up_to_epoch'] <= fetch_start + 0.005


if __name__ == '__main__':
    raise SystemExit(pytest.main([__file__, '-q']))
