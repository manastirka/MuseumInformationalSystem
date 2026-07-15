#!/usr/bin/env python3
"""Regression: the module-access card grid must render from the FRESHLY loaded
module_access, not from the reference captured before load_module_access() runs.

Production bug (2026-07): a user (Nenad) had a per-user module (Baza minerala)
and access worked, yet its card still showed "+" (not assigned). The blueprint
passes `module_access=MODULE_ACCESS` — a dict captured before the view runs —
while load_module_access() rebinds that global to a NEW dict (shared-settings
DB, 60s TTL, multiple workers). The grid was painted from the stale reference,
so a module the user really had appeared unassigned.

The fix reloads inside the view (force=True) and renders from that return value.
"""

import os
import unittest
from unittest.mock import patch

os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

import admin_user_management_views as views


def _module(name, default_access=False, authorized=None):
    return {
        'name': name,
        'description': name,
        'icon': 'bi-x',
        'default_access': default_access,
        'authorized_users': list(authorized or []),
        'restricted_users': [],
    }


class _FakeCursor:
    def __init__(self, users):
        self._users = users

    def execute(self, *a, **k):
        pass

    def fetchall(self):
        return self._users

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class _FakeConn:
    def __init__(self, users):
        self._users = users

    def cursor(self, *a, **k):
        return _FakeCursor(self._users)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class ManageAccessFreshDictTests(unittest.TestCase):
    def setUp(self):
        # STALE: the reference the blueprint would capture — no mineral module.
        self.stale = {'timesheet': _module('Радне листе', default_access=True)}
        # FRESH: what load_module_access() returns — mineral added, Nenad on it.
        self.fresh = {
            'timesheet': _module('Радне листе', default_access=True),
            'mineral_database': _module(
                'База минерала', authorized=['nenad.mladenovic@nhmbeo.rs']),
        }
        self.nenad = {
            'email': 'nenad.mladenovic@nhmbeo.rs',
            'full_name': 'Ненад Младеновић',
            'position': 'конзерватор',
            'department': 'Геолошко одељење',
            'role': 'employee',
        }

    def _load_module_access(self, force=False):
        # Mimics the real function: force must be honoured; return the fresh dict.
        self._load_called_with_force = force
        return self.fresh

    def _user_has_module_access(self, email, role, key):
        module = self.fresh.get(key) or {}
        if module.get('default_access'):
            return True
        return email in module.get('authorized_users', [])

    def _render(self):
        captured = {}

        def fake_render_template(template, **ctx):
            captured.update(ctx)
            return ''

        with patch.object(views, 'render_template', fake_render_template), \
             patch.object(views, 'get_postgres_connection',
                          lambda **k: _FakeConn([self.nenad])), \
             patch.object(views, 'request',
                          type('R', (), {'args': type('A', (), {
                              'get': lambda self, k, d='': d})()})()):
            views.render_manage_user_access(
                load_module_access=self._load_module_access,
                user_has_module_access=self._user_has_module_access,
                module_access=self.stale,  # blueprint passes the STALE reference
                get_museum_employees=lambda: {},
            )
        return captured

    def test_grid_uses_fresh_dict_not_stale_param(self):
        ctx = self._render()
        # The card grid (all_modules) must include the freshly added module.
        self.assertIn('mineral_database', ctx['all_modules'],
                      "grid rendered from stale param — mineral card is missing")

    def test_forces_fresh_reload(self):
        self._render()
        self.assertTrue(self._load_called_with_force,
                        "view must force a fresh load to defeat the TTL cache")

    def test_user_module_reflects_real_permission(self):
        ctx = self._render()
        nenad = next(u for u in ctx['users'] if u['email'] == self.nenad['email'])
        keys = {m['key'] for m in nenad['modules']}
        self.assertIn('mineral_database', keys,
                      "card would show '+' though the user has access")


if __name__ == '__main__':
    unittest.main()
