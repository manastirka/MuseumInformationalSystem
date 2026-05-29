#!/usr/bin/env python3
"""Reproducing tests for maps-1: IDOR on digitized profile update/delete.

Any authenticated user must not be able to update or delete a digitized
profile owned by a different user unless they are an admin.
"""

import json
import os
import tempfile
import unittest

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-maps-1')

from flask import Flask

import maps_profile_views


def _make_app():
    app = Flask(__name__)
    app.secret_key = 'test-secret'
    return app


def _seed_profile(profiles_path, owner='owner@example.com'):
    profile = {
        'id': 'sheet1_AB',
        'sheet_folder': 'sheet1',
        'profile_id': 'AB',
        'endpoint_a': {'lat': 44.0, 'lon': 20.0},
        'endpoint_b': {'lat': 44.1, 'lon': 20.1},
        'image_bounds': {},
        'layers': [{'name': 'orig'}],
        'faults': [],
        'digitized_by': owner,
        'digitized_at': '2026-01-01T00:00:00',
    }
    with open(profiles_path, 'w', encoding='utf-8') as fh:
        json.dump([profile], fh)
    return profile


class DigitizedProfileAuthTests(unittest.TestCase):
    def setUp(self):
        self.app = _make_app()
        fd, self.profiles_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        _seed_profile(self.profiles_path)

    def tearDown(self):
        if os.path.isfile(self.profiles_path):
            os.remove(self.profiles_path)

    def test_update_by_non_owner_non_admin_is_forbidden(self):
        with self.app.test_request_context(
            '/api/map/digitized-profiles/sheet1_AB',
            method='PUT',
            json={'layers': [{'name': 'hacked'}]},
        ) as ctx:
            ctx.session['user_email'] = 'attacker@example.com'
            ctx.session['user_role'] = 'user'
            resp = maps_profile_views.api_digitized_profile_update(
                'sheet1_AB', profiles_path=self.profiles_path
            )

        body = resp[0] if isinstance(resp, tuple) else resp
        status = resp[1] if isinstance(resp, tuple) else 200
        payload = body.get_json()

        self.assertEqual(status, 403, f"expected 403, got {status}: {payload}")
        self.assertFalse(payload.get('success'))

        with open(self.profiles_path, encoding='utf-8') as fh:
            saved = json.load(fh)
        self.assertEqual(saved[0]['layers'], [{'name': 'orig'}])
        self.assertEqual(saved[0]['digitized_by'], 'owner@example.com')

    def test_delete_by_non_owner_non_admin_is_forbidden(self):
        with self.app.test_request_context(
            '/api/map/digitized-profiles/sheet1_AB', method='DELETE'
        ) as ctx:
            ctx.session['user_email'] = 'attacker@example.com'
            ctx.session['user_role'] = 'user'
            resp = maps_profile_views.api_digitized_profile_delete(
                'sheet1_AB', profiles_path=self.profiles_path
            )

        status = resp[1] if isinstance(resp, tuple) else 200
        body = resp[0] if isinstance(resp, tuple) else resp
        payload = body.get_json()

        self.assertEqual(status, 403, f"expected 403, got {status}: {payload}")
        self.assertFalse(payload.get('success'))

        with open(self.profiles_path, encoding='utf-8') as fh:
            saved = json.load(fh)
        self.assertEqual(len(saved), 1)

    def test_update_by_owner_succeeds(self):
        with self.app.test_request_context(
            '/api/map/digitized-profiles/sheet1_AB',
            method='PUT',
            json={'layers': [{'name': 'updated'}]},
        ) as ctx:
            ctx.session['user_email'] = 'owner@example.com'
            ctx.session['user_role'] = 'user'
            resp = maps_profile_views.api_digitized_profile_update(
                'sheet1_AB', profiles_path=self.profiles_path
            )

        body = resp[0] if isinstance(resp, tuple) else resp
        payload = body.get_json()
        self.assertTrue(payload.get('success'), payload)

        with open(self.profiles_path, encoding='utf-8') as fh:
            saved = json.load(fh)
        self.assertEqual(saved[0]['layers'], [{'name': 'updated'}])

    def test_delete_by_admin_succeeds(self):
        with self.app.test_request_context(
            '/api/map/digitized-profiles/sheet1_AB', method='DELETE'
        ) as ctx:
            ctx.session['user_email'] = 'someone-else@example.com'
            ctx.session['user_role'] = 'admin'
            resp = maps_profile_views.api_digitized_profile_delete(
                'sheet1_AB', profiles_path=self.profiles_path
            )

        body = resp[0] if isinstance(resp, tuple) else resp
        payload = body.get_json()
        self.assertTrue(payload.get('success'), payload)

        with open(self.profiles_path, encoding='utf-8') as fh:
            saved = json.load(fh)
        self.assertEqual(len(saved), 0)


if __name__ == '__main__':
    unittest.main()
