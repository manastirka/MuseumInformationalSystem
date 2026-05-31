import sys
import types

import observability


class _FakeScope:
    def __init__(self):
        self.tags = {}
        self.extras = {}
        self.user = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def set_tag(self, key, value):
        self.tags[key] = value

    def set_extra(self, key, value):
        self.extras[key] = value

    def set_user(self, user):
        self.user = user


def test_sentry_helpers_capture_and_breadcrumb(monkeypatch):
    calls = {
        'breadcrumbs': [],
        'captured': [],
        'users': [],
        'scopes': [],
    }

    fake_sdk = types.SimpleNamespace()

    def add_breadcrumb(**kwargs):
        calls['breadcrumbs'].append(kwargs)

    def set_user(user):
        calls['users'].append(user)

    def push_scope():
        scope = _FakeScope()
        calls['scopes'].append(scope)
        return scope

    def capture_exception(exc):
        calls['captured'].append(str(exc))

    fake_sdk.add_breadcrumb = add_breadcrumb
    fake_sdk.set_user = set_user
    fake_sdk.push_scope = push_scope
    fake_sdk.capture_exception = capture_exception

    monkeypatch.setitem(sys.modules, 'sentry_sdk', fake_sdk)

    observability.add_sentry_breadcrumb(
        category='auth',
        message='Login started',
        data={'password': 'secret', 'email': 'user@example.com'},
    )
    observability.capture_observability_exception(
        RuntimeError('boom'),
        tags={'component': 'auth'},
        extra={'token': 'abc', 'email': 'user@example.com'},
        user={'email': 'user@example.com'},
    )

    assert calls['breadcrumbs'][0]['data']['password'] == '[Filtered]'
    assert calls['users'] == []
    assert calls['scopes'][0].user['email'] == 'user@example.com'
    assert calls['captured'] == ['boom']
    assert calls['scopes'][0].tags['component'] == 'auth'
    assert calls['scopes'][0].extras['token'] == '[Filtered]'
