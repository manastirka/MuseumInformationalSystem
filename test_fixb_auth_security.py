"""Reproducing tests for auth-security cluster medium bugs (phase B)."""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-auth-security')

import tempfile

import security_utils
import module_access_support


class FakeRedis:
    """Minimal in-memory stand-in for the subset of redis used by the tracker."""

    def __init__(self):
        self.lists = {}
        self.kv = {}

    def ttl(self, key):
        # -2 == no key; we model an active lockout key by presence in kv.
        return self.kv.get(key, (None, -2))[1] if key in self.kv else -2

    def setex(self, key, duration, value):
        self.kv[key] = (value, duration)

    def llen(self, key):
        return len(self.lists.get(key, []))

    def delete(self, *keys):
        for key in keys:
            self.lists.pop(key, None)
            self.kv.pop(key, None)


def _make_redis_tracker():
    tracker = security_utils.LoginAttemptTracker.__new__(
        security_utils.LoginAttemptTracker
    )
    tracker.use_redis = True
    tracker.redis_client = FakeRedis()
    tracker.attempts = {}
    tracker.lockouts = {}
    return tracker


def test_redis_lockout_does_not_relock_after_expiry():
    """After a Redis lockout expires, a stale attempts list must not re-lock.

    Reproduces: when the lockout is set, the attempts list is left in place
    (only its TTL eventually clears it), so once the 30-min lockout key
    expires the still-present attempts list immediately re-locks the account.
    """
    tracker = _make_redis_tracker()
    email = 'user@example.com'
    max_attempts = 5
    lockout_duration = 1800

    attempts_key = tracker._redis_key("attempts", email)

    # Simulate 5 failed attempts recorded in Redis.
    tracker.redis_client.lists[attempts_key] = ['t'] * max_attempts

    # First check trips the lockout.
    locked, _ = tracker.is_locked_out(email, max_attempts, lockout_duration)
    assert locked is True

    # Simulate the lockout key expiring (TTL lapses) while the attempts
    # list survives. With the bug, the attempts list was never cleared on
    # lock-out, so the very next check re-locks the account.
    lockout_key = tracker._redis_key("lockout", email)
    tracker.redis_client.delete(lockout_key)

    locked_again, _ = tracker.is_locked_out(email, max_attempts, lockout_duration)
    assert locked_again is False, (
        "Account re-locked after lockout expiry because the attempts list "
        "was not cleared when the lockout was set"
    )


def test_revoke_last_authorized_user_persists_empty_list():
    """Emptying authorized_users must persist as [] and not revert to defaults.

    Reproduces: save_module_access_data drops empty lists / empty module
    entries, so on reload the non-empty default authorized_users is restored,
    silently reinstating the revoked user's access.
    """
    default_access = {
        'mineral_db': {
            'default_access': False,
            'authorized_users': ['admin'],
            'restricted_users': [],
        }
    }

    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        access_file = tmp.name

    # Admin revoked the last authorized user -> empty list.
    current = module_access_support.deepcopy(default_access)
    current['mineral_db']['authorized_users'] = []

    saved = module_access_support.save_module_access_data(
        module_access_file=access_file,
        module_access=current,
        get_postgres_connection=None,
    )
    assert saved is True

    reloaded = module_access_support.load_module_access_data(
        module_access_file=access_file,
        current_mtime=1,
        default_access=default_access,
        get_postgres_connection=None,
    )

    os.remove(access_file)

    assert reloaded['mineral_db']['authorized_users'] == [], (
        "Revoked access reverted to default authorized_users after reload; "
        "empty list was not persisted"
    )


def test_revoke_keeps_restricted_users_round_trip():
    """A module reduced to only restricted_users should round-trip fully."""
    default_access = {
        'reports': {
            'default_access': True,
            'authorized_users': ['admin'],
            'restricted_users': [],
        }
    }

    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        access_file = tmp.name

    current = module_access_support.deepcopy(default_access)
    current['reports']['authorized_users'] = []
    current['reports']['restricted_users'] = ['blocked@example.com']

    module_access_support.save_module_access_data(
        module_access_file=access_file,
        module_access=current,
        get_postgres_connection=None,
    )

    reloaded = module_access_support.load_module_access_data(
        module_access_file=access_file,
        current_mtime=1,
        default_access=default_access,
        get_postgres_connection=None,
    )

    os.remove(access_file)

    assert reloaded['reports']['authorized_users'] == []
    assert reloaded['reports']['restricted_users'] == ['blocked@example.com']
