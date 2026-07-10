#!/usr/bin/env python3
"""Tests for Фототека Phase 4: legacy images migration + flag-gated serving.

Covers the migration planner (mineral entity_id -> inventory link vs unlinked
reception queue, RAW layout, missing file), the migration write path and its
sha256 idempotency, and the flag-gated legacy-image redirect
(_fototeka_entity_response): off by default, mineral-only, safe fallback.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ['FLASK_ENV'] = 'testing'  # force: sibling modules may leak 'production'
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

from PIL import Image

import app as museum_app
import collection_media_views
import fototeka_jobs
import migrate_images_to_fototeka as migrator
import postgres_service


def _write_jpeg(path):
    Image.new('RGB', (500, 400), (30, 90, 40)).save(path, format='JPEG')
    return path


class _FakeCursor:
    def __init__(self, canned=None):
        self.canned = dict(canned or {})
        self._pending = None
        self.executed = []

    def execute(self, sql, params=None):
        self.executed.append((' '.join(sql.split()), params))
        for needle, row in self.canned.items():
            if needle in sql:
                self._pending = row
                return
        self._pending = None

    def fetchone(self):
        value = self._pending
        if isinstance(value, list):
            return value[0] if value else None
        return value

    def fetchall(self):
        value = self._pending
        if isinstance(value, list):
            return value
        return [value] if value else []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class _FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor

    def cursor(self):
        return self._cursor

    def commit(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class MigrationPlannerTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='fototeka4-plan-')
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.original = _write_jpeg(Path(self.tmp, 'legacy.jpg'))

    def _image(self, **over):
        img = {'image_id': 'x1', 'database_name': 'mineral', 'entity_type': 'mineral',
               'entity_id': '5', 'file_path': str(self.original),
               'original_filename': 'legacy.jpg', 'file_size': 111,
               'width': 500, 'height': 400, 'created_at': None}
        img.update(over)
        return img

    def test_resolved_mineral_links_predmet(self):
        cursor = _FakeCursor({'FROM minerals WHERE id': {'inventory_number': '123', 'item_name': 'Kvarc'}})
        plan = migrator._plan_row(cursor, self._image())
        self.assertEqual(plan['veza']['tip'], 'predmet')
        self.assertEqual(plan['veza']['inventarni_broj'], '123')
        self.assertFalse(plan['u_prijemnom_redu'])
        self.assertTrue(plan['raw_rel'].startswith('zbirke/mineral/123/'))
        self.assertEqual(len(plan['sha256']), 64)

    def test_unresolved_entity_goes_unlinked(self):
        cursor = _FakeCursor({})  # minerals lookup returns nothing
        plan = migrator._plan_row(cursor, self._image(entity_id='999'))
        self.assertIsNone(plan['veza'])
        self.assertTrue(plan['u_prijemnom_redu'])
        self.assertTrue(plan['raw_rel'].startswith('razno/'))

    def test_missing_file_reported(self):
        cursor = _FakeCursor({})
        result = migrator._plan_row(cursor, self._image(file_path='/nema/ovaj.jpg'))
        self.assertIsInstance(result, str)
        self.assertIn('missing', result)


class MigrationWritePathTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='fototeka4-write-')
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.original = _write_jpeg(Path(self.tmp, 'legacy.jpg'))
        self.arhiva = Path(self.tmp, 'arhiva')
        env = patch.dict(os.environ, {'FOTOTEKA_ARHIVA_PATH': str(self.arhiva)})
        env.start()
        self.addCleanup(env.stop)

    def _image_row(self):
        return {'image_id': 'x1', 'database_name': 'mineral', 'entity_type': 'mineral',
                'entity_id': '5', 'file_path': str(self.original),
                'original_filename': 'legacy.jpg', 'file_size': 111,
                'width': 500, 'height': 400, 'created_at': None}

    def test_commit_copies_file_and_inserts(self):
        cursor = _FakeCursor({
            'FROM images': [self._image_row()],
            'FROM minerals WHERE id': {'inventory_number': '123', 'item_name': 'Kvarc'},
            'INSERT INTO fotografije': {'id': 1},
        })
        conn = _FakeConnection(cursor)
        with patch.object(migrator, 'get_postgres_connection', lambda **k: conn):
            stats = migrator.migrate(commit=True, limit=None)
        self.assertEqual(stats['migrated'], 1)
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertIn('INSERT INTO fotografije', joined)
        self.assertIn('INSERT INTO foto_veza_predmet', joined)
        self.assertIn('INSERT INTO foto_poslovi', joined)  # derivative enqueued
        # the RAW original was copied into the archive
        copied = list(self.arhiva.rglob('*.jpg'))
        self.assertEqual(len(copied), 1)
        self.assertTrue(self.original.is_file())  # source untouched

    def test_dedup_skips_already_migrated(self):
        cursor = _FakeCursor({
            'FROM images': [self._image_row()],
            'FROM minerals WHERE id': {'inventory_number': '123', 'item_name': 'Kvarc'},
            'SELECT id FROM fotografije WHERE sha256': {'id': 7},
        })
        conn = _FakeConnection(cursor)
        with patch.object(migrator, 'get_postgres_connection', lambda **k: conn):
            stats = migrator.migrate(commit=True, limit=None)
        self.assertEqual(stats['dedup'], 1)
        self.assertEqual(stats['migrated'], 0)
        self.assertEqual(list(self.arhiva.rglob('*.jpg')), [])

    def test_dry_run_writes_nothing(self):
        cursor = _FakeCursor({
            'FROM images': [self._image_row()],
            'FROM minerals WHERE id': {'inventory_number': '123', 'item_name': 'Kvarc'},
        })
        conn = _FakeConnection(cursor)
        with patch.object(migrator, 'get_postgres_connection', lambda **k: conn):
            stats = migrator.migrate(commit=False, limit=None)
        self.assertEqual(stats['planned'], 1)
        self.assertEqual(stats['migrated'], 0)
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertNotIn('INSERT INTO fotografije', joined)
        self.assertEqual(list(self.arhiva.rglob('*.jpg')), [])


class LegacyServingRedirectTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='fototeka4-serve-')
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.media = Path(self.tmp, 'media')
        env = patch.dict(os.environ, {'FOTOTEKA_MEDIA_PATH': str(self.media)})
        env.start()
        self.addCleanup(env.stop)

    def _make_derivative(self, sha256):
        rel = fototeka_jobs.derivative_relative_path(sha256, 'jpg')
        path = self.media / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        _write_jpeg(path)
        return path

    def test_flag_off_returns_none(self):
        # default: flag not set -> legacy path is used, no Фототека lookup
        with patch.dict(os.environ, {'FOTOTEKA_SERVE_LEGACY_IMAGES': 'false'}):
            self.assertIsNone(
                collection_media_views._fototeka_entity_response('minerals', 'mineral', '5', 'medium'))

    def test_flag_on_serves_migrated_derivative(self):
        sha = 'c' * 64
        self._make_derivative(sha)
        cursor = _FakeCursor({'FROM fotografije f': {'sha256': sha}})
        conn = _FakeConnection(cursor)
        with patch.dict(os.environ, {'FOTOTEKA_SERVE_LEGACY_IMAGES': 'true'}), \
             patch.object(postgres_service, 'get_postgres_connection', lambda **k: conn), \
             museum_app.app.test_request_context('/'):
            response = collection_media_views._fototeka_entity_response(
                'minerals', 'mineral', '5', 'medium')
        self.assertIsNotNone(response)

    def test_flag_on_no_photo_falls_back(self):
        cursor = _FakeCursor({})  # no fotografije row
        conn = _FakeConnection(cursor)
        with patch.dict(os.environ, {'FOTOTEKA_SERVE_LEGACY_IMAGES': 'true'}), \
             patch.object(postgres_service, 'get_postgres_connection', lambda **k: conn), \
             museum_app.app.test_request_context('/'):
            self.assertIsNone(collection_media_views._fototeka_entity_response(
                'minerals', 'mineral', '5', 'medium'))

    def test_flag_on_non_mineral_falls_back(self):
        with patch.dict(os.environ, {'FOTOTEKA_SERVE_LEGACY_IMAGES': 'true'}):
            self.assertIsNone(collection_media_views._fototeka_entity_response(
                'botany', 'collection_item', '5', 'medium'))

    def test_flag_on_query_restricts_to_public_only(self):
        # A2: the legacy specimen route authorizes on collection access, not
        # photo authorship — so it must select only 'javno' photos, never a
        # private one the author flipped after migration.
        sha = 'c' * 64
        self._make_derivative(sha)
        cursor = _FakeCursor({'FROM fotografije f': {'sha256': sha}})
        conn = _FakeConnection(cursor)
        with patch.dict(os.environ, {'FOTOTEKA_SERVE_LEGACY_IMAGES': 'true'}), \
             patch.object(postgres_service, 'get_postgres_connection', lambda **k: conn), \
             museum_app.app.test_request_context('/'):
            collection_media_views._fototeka_entity_response(
                'minerals', 'mineral', '5', 'medium')
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertIn('vidljivost', joined)
        self.assertIn("'javno'", joined)


if __name__ == '__main__':
    unittest.main()
