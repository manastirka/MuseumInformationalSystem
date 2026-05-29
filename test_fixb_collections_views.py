"""Reproducing tests for collections-views medium-severity fixes (phase B)."""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-collections-views')

import json
from pathlib import Path
from unittest import mock

import pytest
from flask import Flask

import collection_management_views as cmv


def _make_app():
    app = Flask(__name__)
    app.secret_key = 'test-secret'

    # Register the endpoints the handlers redirect to so url_for resolves.
    app.add_url_rule('/heritage', 'cultural_heritage_database', lambda: '')
    app.add_url_rule(
        '/sanja', 'sanja_paleogene_neogene_mammals', lambda: ''
    )
    app.add_url_rule('/museum', 'museum_databases', lambda: '')
    return app


def _get_flashes():
    from flask import get_flashed_messages
    return get_flashed_messages(with_categories=True)


# ---------------------------------------------------------------------------
# Finding 1: handle_add_heritage_item never persists, reports bogus success.
# ---------------------------------------------------------------------------

def test_add_heritage_item_does_not_report_bogus_success():
    app = _make_app()

    heritage_db = {'heritage_items': [{'id': 1}]}

    with app.test_request_context(
        '/admin/add_heritage_item',
        method='POST',
        data={'name': 'Test', 'registry_number': 'R-1'},
    ):
        resp = cmv.handle_add_heritage_item(
            get_cultural_heritage_database=lambda: heritage_db
        )
        flashes = _get_flashes()

    # The new item must NOT be silently appended to the in-memory cache,
    # and the user must NOT be told it succeeded.
    categories = {cat for cat, _ in flashes}
    assert 'success' not in categories, (
        'Bogus success flashed even though item was never persisted'
    )
    assert 'error' in categories, 'Honest error message expected'
    assert len(heritage_db['heritage_items']) == 1, (
        'Item must not be appended to the cached dict'
    )
    # Should redirect back to the form/listing, not raise.
    assert resp.status_code in (301, 302)


# ---------------------------------------------------------------------------
# Finding 2: Sanja JSON written non-atomically (truncate-then-write).
# ---------------------------------------------------------------------------

def test_sanja_save_is_atomic(tmp_path, monkeypatch):
    target = tmp_path / 'sanja.json'
    target.write_text(
        json.dumps({'specimens': [{'id': 1, 'specimen_name': 'old'}]}),
        encoding='utf-8',
    )
    monkeypatch.setattr(cmv, '_SANJA_DATABASE_PATH', target)

    original_replace = os.replace
    seen = {'replace': False}

    def tracking_replace(src, dst):
        seen['replace'] = True
        return original_replace(src, dst)

    payload = {'specimens': [{'id': 1, 'specimen_name': 'new'}], 'metadata': {}}

    # Atomic write must go through a temp file + os.replace, never truncate
    # the live file in place.
    with mock.patch('os.replace', side_effect=tracking_replace):
        with mock.patch.object(
            Path, 'write_text',
            side_effect=AssertionError('non-atomic write_text used'),
        ):
            cmv._save_sanja_database_payload(payload)

    assert seen['replace'], 'Save must use os.replace for atomicity'
    data = json.loads(target.read_text(encoding='utf-8'))
    assert data['specimens'][0]['specimen_name'] == 'new'


# ---------------------------------------------------------------------------
# Finding 3: Sanja save can wipe DB after a swallowed read error.
# ---------------------------------------------------------------------------

def test_sanja_load_raises_on_corrupt_file(tmp_path, monkeypatch):
    target = tmp_path / 'sanja.json'
    target.write_text('{ this is : not valid json', encoding='utf-8')
    monkeypatch.setattr(cmv, '_SANJA_DATABASE_PATH', target)

    # A corrupt/parse-failing file must NOT be silently treated as empty.
    with pytest.raises(Exception):
        cmv._load_sanja_database_payload()


def test_sanja_load_missing_file_returns_empty(tmp_path, monkeypatch):
    target = tmp_path / 'does_not_exist.json'
    monkeypatch.setattr(cmv, '_SANJA_DATABASE_PATH', target)

    payload = cmv._load_sanja_database_payload()
    assert payload['specimens'] == []


def test_sanja_add_aborts_without_wiping_on_corrupt_db(tmp_path, monkeypatch):
    app = _make_app()
    target = tmp_path / 'sanja.json'
    good_payload = {
        'specimens': [{'id': i, 'specimen_name': f's{i}'} for i in range(1, 11)],
        'metadata': {},
    }
    target.write_text(json.dumps(good_payload), encoding='utf-8')
    monkeypatch.setattr(cmv, '_SANJA_DATABASE_PATH', target)

    # Simulate a transient read failure (locked/partial read) on load.
    real_read_text = Path.read_text

    def boom(self, *args, **kwargs):
        if Path(self) == target:
            raise OSError('transient read failure')
        return real_read_text(self, *args, **kwargs)

    collection_info = {
        'name': 'Крупни сисари палеогена и неогена',
        'route': 'sanja_paleogene_neogene_mammals',
    }

    with app.test_request_context(
        '/admin/add_sanja',
        method='POST',
        data={'specimen_name': 'new specimen'},
    ):
        with mock.patch.object(Path, 'read_text', boom):
            resp = cmv._handle_sanja_paleogene_neogene_mammal_form(collection_info)
        flashes = _get_flashes()

    # The on-disk file must NOT be overwritten with a single-record payload.
    data = json.loads(target.read_text(encoding='utf-8'))
    assert len(data['specimens']) == 10, 'Existing records must not be wiped'
    categories = {cat for cat, _ in flashes}
    assert 'success' not in categories
    assert resp.status_code in (301, 302)
