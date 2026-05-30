"""Tests for the digitized-profiles PostgreSQL migration (dual-mode dispatch).

The live PostgreSQL path needs a DB + the digitized_profiles table (migration 011);
here we verify the dispatch: Postgres is used (with the same ownership rules) when
available, and the JSON fallback is preserved otherwise.
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-profiles-pg')

import flask  # noqa: E402
import app as museum_app  # noqa: E402
import maps_profile_views as mp  # noqa: E402

DUMMY = '/nonexistent-profiles.json'


def _body(resp):
    return (resp[0] if isinstance(resp, tuple) else resp).get_json()


def _status(resp):
    return resp[1] if isinstance(resp, tuple) else 200


class TestDigitizedProfilesPG:
    def test_list_uses_postgres(self):
        fake = MagicMock()
        fake.get_digitized_profiles.return_value = [
            {'id': 'p1', 'digitized_by': 'u@x.rs', 'layers': [1, 2], 'faults': []},
        ]
        with patch.object(mp, '_profiles_pg', return_value=fake):
            with museum_app.app.test_request_context('/api/map/profiles'):
                resp = mp.api_digitized_profiles_list(profiles_path=DUMMY)
        data = resp.get_json()
        assert data['success'] is True
        assert data['data'][0]['id'] == 'p1'
        assert data['data'][0]['layer_count'] == 2

    def test_create_uses_postgres_and_rejects_duplicate(self):
        fake = MagicMock()
        fake.get_digitized_profile.return_value = None
        with patch.object(mp, '_profiles_pg', return_value=fake):
            with museum_app.app.test_request_context(
                '/api/map/profiles', method='POST',
                json={'id': 'p9', 'sheet_folder': 's', 'profile_id': 'AB'},
            ):
                flask.session['user_email'] = 'u@x.rs'
                resp = mp.api_digitized_profile_create(profiles_path=DUMMY)
        assert _body(resp)['success'] is True
        fake.upsert_digitized_profile.assert_called_once()

        dup = MagicMock()
        dup.get_digitized_profile.return_value = {'id': 'p9'}
        with patch.object(mp, '_profiles_pg', return_value=dup):
            with museum_app.app.test_request_context(
                '/api/map/profiles', method='POST', json={'id': 'p9'},
            ):
                flask.session['user_email'] = 'u@x.rs'
                resp = mp.api_digitized_profile_create(profiles_path=DUMMY)
        assert _status(resp) == 409
        dup.upsert_digitized_profile.assert_not_called()

    def test_update_postgres_enforces_ownership(self):
        fake = MagicMock()
        fake.get_digitized_profile.return_value = {'id': 'p1', 'digitized_by': 'owner@x.rs'}
        # non-owner, non-admin -> 403, no write
        with patch.object(mp, '_profiles_pg', return_value=fake):
            with museum_app.app.test_request_context('/x', method='PUT', json={'layers': [1]}):
                flask.session['user_email'] = 'intruder@x.rs'
                flask.session['user_role'] = 'employee'
                resp = mp.api_digitized_profile_update('p1', profiles_path=DUMMY)
        assert _status(resp) == 403
        fake.upsert_digitized_profile.assert_not_called()
        # owner -> ok, writes
        fake.reset_mock()
        fake.get_digitized_profile.return_value = {'id': 'p1', 'digitized_by': 'owner@x.rs'}
        with patch.object(mp, '_profiles_pg', return_value=fake):
            with museum_app.app.test_request_context('/x', method='PUT', json={'layers': [1, 2]}):
                flask.session['user_email'] = 'owner@x.rs'
                flask.session['user_role'] = 'employee'
                resp = mp.api_digitized_profile_update('p1', profiles_path=DUMMY)
        assert _body(resp)['success'] is True
        fake.upsert_digitized_profile.assert_called_once()

    def test_delete_postgres_missing_returns_404(self):
        fake = MagicMock()
        fake.get_digitized_profile.return_value = None
        with patch.object(mp, '_profiles_pg', return_value=fake):
            with museum_app.app.test_request_context('/x', method='DELETE'):
                flask.session['user_email'] = 'u@x.rs'
                flask.session['user_role'] = 'employee'
                resp = mp.api_digitized_profile_delete('pX', profiles_path=DUMMY)
        assert _status(resp) == 404
        fake.delete_digitized_profile.assert_not_called()

    def test_list_falls_back_to_json(self):
        tmp = Path(tempfile.mkdtemp()) / 'profiles.json'
        tmp.write_text(json.dumps([{'id': 'j1', 'layers': [], 'faults': []}]), encoding='utf-8')
        with patch.object(mp, '_profiles_pg', return_value=None):
            with museum_app.app.test_request_context('/x'):
                resp = mp.api_digitized_profiles_list(profiles_path=str(tmp))
        assert resp.get_json()['data'][0]['id'] == 'j1'
