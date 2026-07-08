#!/usr/bin/env python3
"""Tests for Фототека Phase 3: Samba import + monthly fixity enqueue.

Covers: the filename-convention classifier (predmet / teren / reception
queue), the import-path traversal guard, the scan preview and confirm-intake
routes (admin-only, share original preserved), and the fixity batch enqueue.
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
import fototeka_jobs
import fototeka_views


ADMIN = {
    'user_id': 1, 'user_email': 'admin@nhmbeo.rs', 'user_name': 'Админ',
    'user_role': 'admin', 'is_admin': True,
    'user_department': None, 'is_department_head': False,
}
EMPLOYEE = {
    'user_id': 10, 'user_email': 'radnik@nhmbeo.rs', 'user_name': 'Радник',
    'user_role': 'employee', 'is_admin': False,
    'user_department': 'ГЕОЛОГИЈА', 'is_department_head': False,
}


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
        self.commits = 0

    def cursor(self):
        return self._cursor

    def commit(self):
        self.commits += 1

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.commit()
        return False


# ---------------------------------------------------------------------------
# Pure: classification + path guard
# ---------------------------------------------------------------------------

class ClassificationTests(unittest.TestCase):

    def test_inventory_number_maps_to_predmet_prefix_stripped(self):
        result = fototeka_views.classify_import_filename('M-1234_kvarc.jpg', 'mineral')
        self.assertEqual(result['klasa'], 'predmet')
        self.assertEqual(result['veza_meta']['database_name'], 'mineral')
        # 'M-1234' -> '1234' so it matches the numeric DB inventory_number
        self.assertEqual(result['veza_meta']['inventarni_broj'], '1234')
        self.assertFalse(result['u_prijemnom_redu'])

    def test_teren_prefix_with_year(self):
        result = fototeka_views.classify_import_filename(
            'TEREN_2025_Zapadna_Srbija_01.jpg', 'mineral')
        self.assertEqual(result['klasa'], 'teren')
        self.assertEqual(result['veza_meta']['godina'], 2025)
        self.assertIn('Zapadna', result['veza_meta']['naziv'])

    def test_teren_without_year_goes_to_queue(self):
        result = fototeka_views.classify_import_filename('TEREN_kopaonik.jpg', 'mineral')
        self.assertEqual(result['klasa'], 'prijemni_red')
        self.assertTrue(result['u_prijemnom_redu'])

    def test_unmatched_name_goes_to_queue_not_generic_number(self):
        # a bare number must NOT be auto-linked (honors "ostalo -> prijemni red")
        result = fototeka_views.classify_import_filename('DSC_0001.jpg', 'mineral')
        self.assertEqual(result['klasa'], 'prijemni_red')
        self.assertIsNone(result['veza_meta'])

    def test_extract_broj_unknown_collection_is_none(self):
        self.assertIsNone(fototeka_views._extract_predmet_broj('M-1.jpg', 'nepostojeca'))


class ImportPathGuardTests(unittest.TestCase):

    def setUp(self):
        self.root = tempfile.mkdtemp(prefix='fototeka-import-root-')
        self.addCleanup(shutil.rmtree, self.root, True)
        env = patch.dict(os.environ, {'FOTOTEKA_IMPORT_PATH': self.root})
        env.start()
        self.addCleanup(env.stop)

    def test_traversal_is_refused(self):
        self.assertIsNone(fototeka_views._safe_import_dir('../../etc'))

    def test_normal_subdir_resolves_under_root(self):
        target = fototeka_views._safe_import_dir('2026_jun')
        self.assertIsNotNone(target)
        self.assertTrue(str(target).startswith(str(Path(self.root).resolve())))

    def test_empty_subdir_is_root(self):
        target = fototeka_views._safe_import_dir('')
        self.assertEqual(target, Path(self.root).resolve())


# ---------------------------------------------------------------------------
# Fixity enqueue
# ---------------------------------------------------------------------------

class FixityEnqueueTests(unittest.TestCase):

    def test_enqueue_returns_count(self):
        cursor = _FakeCursor({'INSERT INTO foto_poslovi': [{'id': 1}, {'id': 2}, {'id': 3}]})
        conn = _FakeConnection(cursor)
        with patch.object(fototeka_jobs, 'get_postgres_connection', lambda **k: conn):
            self.assertEqual(fototeka_jobs.enqueue_fixity_batch(), 3)
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertIn("'fixity'", joined)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

class _RouteTestCase(unittest.TestCase):

    def setUp(self):
        museum_app.app.config['TESTING'] = True
        csrf_was = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.addCleanup(museum_app.app.config.__setitem__, 'WTF_CSRF_ENABLED', csrf_was)

        self.import_root = tempfile.mkdtemp(prefix='fototeka3-import-')
        self.arhiva = tempfile.mkdtemp(prefix='fototeka3-arhiva-')
        self.media = tempfile.mkdtemp(prefix='fototeka3-media-')
        for d in (self.import_root, self.arhiva, self.media):
            self.addCleanup(shutil.rmtree, d, True)
        env = patch.dict(os.environ, {
            'FOTOTEKA_IMPORT_PATH': self.import_root,
            'FOTOTEKA_ARHIVA_PATH': self.arhiva,
            'FOTOTEKA_MEDIA_PATH': self.media,
        })
        env.start()
        self.addCleanup(env.stop)

        self.client = museum_app.app.test_client()

    def get(self, *a, **k):
        k.setdefault('base_url', 'https://localhost')
        return self.client.get(*a, **k)

    def post(self, *a, **k):
        k.setdefault('base_url', 'https://localhost')
        return self.client.post(*a, **k)

    def login(self, who):
        with self.client.session_transaction() as sess:
            for key, value in who.items():
                sess[key] = value

    def use_db(self, canned):
        cursor = _FakeCursor(canned)
        conn = _FakeConnection(cursor)
        db_patch = patch.object(
            fototeka_views, 'get_postgres_connection', lambda **k: conn)
        db_patch.start()
        self.addCleanup(db_patch.stop)
        return cursor

    def _make_image(self, name):
        path = Path(self.import_root, name)
        Image.new('RGB', (400, 300), (30, 90, 40)).save(path)
        return path


class ImportRouteTests(_RouteTestCase):

    def test_import_screen_is_admin_only(self):
        self.login(EMPLOYEE)
        response = self.get('/fototeka/uvoz')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard', response.headers['Location'])

    def test_import_requires_login(self):
        response = self.get('/fototeka/uvoz')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_scan_preview_classifies_files(self):
        self._make_image('M-77.jpg')
        self._make_image('TEREN_2024_kopaonik.jpg')
        self._make_image('nasumicno.jpg')
        self.login(ADMIN)
        response = self.post('/fototeka/uvoz/skeniraj',
                             data={'subdir': '', 'zbirka': 'mineral'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Преглед'.encode('utf-8'), response.data)
        self.assertIn('M-77.jpg'.encode('utf-8'), response.data)

    def test_confirm_intakes_and_keeps_share_original(self):
        share_file = self._make_image('M-77.jpg')
        cursor = self.use_db({'INSERT INTO fotografije': {'id': 1}})
        self.login(ADMIN)
        response = self.post('/fototeka/uvoz/potvrdi',
                             data={'subdir': '', 'zbirka': 'mineral'})
        self.assertEqual(response.status_code, 302)
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertIn('INSERT INTO fotografije', joined)
        # imported as 'import', linked as a mineral predmet
        insert = [p for sql, p in cursor.executed if 'INSERT INTO fotografije' in sql][0]
        self.assertIn('import', insert)
        self.assertIn('INSERT INTO foto_veza_predmet', joined)
        # the share original is copied, never moved
        self.assertTrue(share_file.is_file())

    def test_confirm_rejects_traversal_subdir(self):
        self.use_db({})
        self.login(ADMIN)
        response = self.post('/fototeka/uvoz/potvrdi',
                             data={'subdir': '../../etc', 'zbirka': 'mineral'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/fototeka/uvoz', response.headers['Location'])


if __name__ == '__main__':
    unittest.main()
