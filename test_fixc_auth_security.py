"""Focused tests for Phase-C LOW-severity auth-security hardening fixes.

Covers:
  * Finding (logic): _has_direct_module_access must compare emails
    case-insensitively so a user whose stored email contains uppercase
    characters still matches lowercase authorized_users / restricted_users.
  * Finding (csrf_exempt): the pass-through decorator must keep transparently
    calling the wrapped view (no behavior regression).
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-auth-security')

from app_access_support import _has_direct_module_access, user_has_module_access
from security_utils import csrf_exempt


def _load_module_access():
    return {}


class TestDirectModuleAccessCaseInsensitive:
    def test_authorized_user_with_uppercase_email_is_granted(self):
        module = {
            'default_access': False,
            'authorized_users': ['slavko.spasic@nhmbeo.rs'],
            'restricted_users': [],
        }
        assert _has_direct_module_access(module, 'Slavko.Spasic@nhmbeo.rs') is True

    def test_authorized_entry_with_uppercase_matches_lowercase_session(self):
        module = {
            'default_access': False,
            'authorized_users': ['Biljana.Mitrovic@NHMBEO.rs'],
            'restricted_users': [],
        }
        assert _has_direct_module_access(module, 'biljana.mitrovic@nhmbeo.rs') is True

    def test_restricted_user_with_uppercase_email_is_denied_on_default_access(self):
        module = {
            'default_access': True,
            'authorized_users': [],
            'restricted_users': ['slavko.spasic@nhmbeo.rs'],
        }
        # Case-mismatched stored email must still hit the restriction.
        assert _has_direct_module_access(module, 'Slavko.Spasic@nhmbeo.rs') is False

    def test_default_access_still_allows_unlisted_user(self):
        module = {
            'default_access': True,
            'authorized_users': [],
            'restricted_users': ['someone.else@nhmbeo.rs'],
        }
        assert _has_direct_module_access(module, 'Other.User@nhmbeo.rs') is True

    def test_non_member_still_denied(self):
        module = {
            'default_access': False,
            'authorized_users': ['slavko.spasic@nhmbeo.rs'],
            'restricted_users': [],
        }
        assert _has_direct_module_access(module, 'intruder@nhmbeo.rs') is False

    def test_user_has_module_access_grants_uppercase_authorized_user(self):
        module_access = {
            'library_database': {
                'default_access': False,
                'authorized_users': ['slavko.spasic@nhmbeo.rs'],
                'restricted_users': [],
            }
        }
        granted = user_has_module_access(
            'Slavko.Spasic@nhmbeo.rs',
            'user',
            'library_database',
            load_module_access=_load_module_access,
            module_access=module_access,
            resolved_module_access=module_access,
            resolved_employee_directory=[],
        )
        assert granted is True


class TestCsrfExemptPassthrough:
    def test_decorator_calls_wrapped_function(self):
        @csrf_exempt
        def view():
            return 'ok'

        assert view() == 'ok'

    def test_decorator_marks_attribute(self):
        @csrf_exempt
        def view():
            return 'ok'

        # Attribute preserved for discoverability / introspection.
        assert getattr(view, 'csrf_exempt', False) is True
