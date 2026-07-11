#!/usr/bin/env python3
"""Tests for the three live-upload findings:

1. RAW / archival formats: camera RAW accepted without PIL validation; a photo
   whose format libvips can't decode becomes 'bez_derivata' (no retry storm),
   and a JPG preview can be attached afterwards.
2. Sequential single-file upload endpoint returns JSON per file.
3. Exhibition not in the list: a new exhibition is created and linked.
"""

import io
import os
import shutil
import tempfile
import unittest
from datetime import date
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


AUTHOR = {
    'user_id': 10, 'user_email': 'autor@nhmbeo.rs', 'user_name': 'Аутор',
    'user_role': 'employee', 'is_admin': False,
    'user_department': 'ГЕОЛОГИЈА', 'is_department_head': False,
}
SHA = 'e' * 64


def _photo(**over):
    photo = {
        'id': 5, 'sha256': SHA, 'raw_putanja': 'razno/2026/x__eeeeeeee.cr2',
        'original_ime': 'x.cr2', 'ekstenzija': '.cr2', 'velicina_bajtova': 10,
        'width': None, 'height': None, 'autor_email': AUTHOR['user_email'],
        'datum_snimanja': None, 'exif': {}, 'opis': 'Опис', 'poreklo': 'upload',
        'status': 'bez_derivata', 'u_prijemnom_redu': False, 'obrisana': False,
        'fixity_proveren_at': None, 'fixity_ok': None,
        'created_at': None, 'updated_at': None,
    }
    photo.update(over)
    return photo


def _jpeg_bytes(size=(600, 400)):
    buf = io.BytesIO()
    Image.new('RGB', size, (20, 90, 40)).save(buf, format='JPEG')
    buf.seek(0)
    return buf


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


# ---------------------------------------------------------------------------
# Finding 1: RAW / bez_derivata
# ---------------------------------------------------------------------------

class NoDerivativeWorkerTests(unittest.TestCase):

    def test_undecodable_format_marks_bez_derivata_no_retry(self):
        with patch.object(fototeka_jobs, 'make_derivatives',
                          side_effect=RuntimeError('not a known file format')), \
             patch.object(fototeka_jobs, '_mark_no_derivative') as mark, \
             patch.object(fototeka_jobs, '_fail_job') as fail:
            job = {'id': 1, 'fotografija_id': 5, 'tip': 'derivati', 'pokusaji': 0,
                   'sha256': SHA, 'raw_putanja': 'razno/2026/x.cr2', 'ekstenzija': '.cr2'}
            # returns True (success) and never enters the retry path
            self.assertTrue(fototeka_jobs.process_job(job))
            mark.assert_called_once()
            fail.assert_not_called()

    def test_decodable_format_still_retries_on_failure(self):
        with patch.object(fototeka_jobs, 'make_derivatives',
                          side_effect=RuntimeError('transient')), \
             patch.object(fototeka_jobs, '_mark_no_derivative') as mark, \
             patch.object(fototeka_jobs, '_fail_job') as fail:
            job = {'id': 1, 'fotografija_id': 5, 'tip': 'derivati', 'pokusaji': 0,
                   'sha256': SHA, 'raw_putanja': 'razno/2026/x.jpg', 'ekstenzija': '.jpg'}
            self.assertFalse(fototeka_jobs.process_job(job))
            fail.assert_called_once()
            mark.assert_not_called()


class RawIntakeTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='fototeka5-raw-')
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.arhiva = Path(self.tmp, 'arhiva')
        env = patch.dict(os.environ, {'FOTOTEKA_ARHIVA_PATH': str(self.arhiva),
                                      'FOTOTEKA_MEDIA_PATH': str(Path(self.tmp, 'media'))})
        env.start()
        self.addCleanup(env.stop)

    def test_raw_accepted_without_pil_validation(self):
        # a .cr2 with a valid RAW/TIFF signature is archived without PIL
        raw = Path(self.tmp, 'src.cr2')
        raw.write_bytes(b'II\x2a\x00' + b'\x00\x01RAWDATA' * 100)
        cursor = _FakeCursor({'INSERT INTO fotografije': {'id': 9}})
        fid, reason = fototeka_views._intake_photo_from_path(
            cursor, raw, 'photo.cr2', raw.stat().st_size, '.cr2',
            autor_email='a@b.rs', opis=None, tags=[], datum_override=None,
            veza=None, u_prijemnom_redu=False, poreklo='upload')
        self.assertEqual(fid, 9)
        self.assertIsNone(reason)
        self.assertTrue(list(self.arhiva.rglob('*.cr2')))  # archived

    def test_raw_with_bogus_signature_is_refused(self):
        # B3: arbitrary content merely renamed to .cr2 must be refused, not
        # silently archived forever (deletes are soft, the RAW stays).
        raw = Path(self.tmp, 'fake.cr2')
        raw.write_bytes(b'this is definitely not a raw image ' * 20)
        cursor = _FakeCursor({'INSERT INTO fotografije': {'id': 9}})
        fid, reason = fototeka_views._intake_photo_from_path(
            cursor, raw, 'fake.cr2', raw.stat().st_size, '.cr2',
            autor_email='a@b.rs', opis=None, tags=[], datum_override=None,
            veza=None, u_prijemnom_redu=False, poreklo='upload')
        self.assertIsNone(fid)
        self.assertIsNotNone(reason)
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertNotIn('INSERT INTO fotografije', joined)
        self.assertEqual(list(self.arhiva.rglob('*.cr2')), [])  # not archived

    def test_full_sha_in_path_avoids_prefix_collision(self):
        # B1: two different files sharing the first 8 sha hex must NOT map to
        # the same archive path (the old sha[:8] scheme let them collide).
        sha_a = 'a' * 64
        sha_b = 'a' * 8 + 'b' * 56
        path_a = fototeka_jobs.raw_intake_relative_path(
            original_ime='x.cr2', sha256=sha_a, datum=date(2026, 1, 1))
        path_b = fototeka_jobs.raw_intake_relative_path(
            original_ime='x.cr2', sha256=sha_b, datum=date(2026, 1, 1))
        self.assertNotEqual(path_a, path_b)
        self.assertIn(sha_a, path_a)  # full sha, not a truncated prefix

    def test_intake_refuses_to_overwrite_existing_raw(self):
        # B1: if the target archive path is already occupied, intake must skip
        # and leave the existing original byte-for-byte intact (write-once).
        raw = Path(self.tmp, 'src.cr2')
        raw.write_bytes(b'II\x2a\x00' + b'NEWDATA' * 50)
        sha = fototeka_jobs.sha256_of_file(raw)
        raw_rel = fototeka_jobs.raw_intake_relative_path(
            original_ime='photo.cr2', sha256=sha, datum=date(2026, 1, 1))
        raw_full = self.arhiva / raw_rel
        raw_full.parent.mkdir(parents=True, exist_ok=True)
        raw_full.write_bytes(b'ORIGINAL-KEEP-ME')  # a pre-existing occupant
        cursor = _FakeCursor({'INSERT INTO fotografije': {'id': 9}})
        fid, reason = fototeka_views._intake_photo_from_path(
            cursor, raw, 'photo.cr2', raw.stat().st_size, '.cr2',
            autor_email='a@b.rs', opis=None, tags=[],
            datum_override=date(2026, 1, 1),
            veza=None, u_prijemnom_redu=False, poreklo='upload')
        self.assertIsNone(fid)
        self.assertIsNotNone(reason)
        self.assertEqual(raw_full.read_bytes(), b'ORIGINAL-KEEP-ME')  # not overwritten
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertNotIn('INSERT INTO fotografije', joined)

    def test_intake_removes_raw_when_db_insert_fails(self):
        # B1: a DB failure after the file is placed must leave NO orphan in the
        # write-once archive (compensating unlink of exactly the placed file).
        class _FailingInsertCursor(_FakeCursor):
            def execute(self, sql, params=None):
                if 'INSERT INTO fotografije' in sql:
                    raise RuntimeError('DB boom')
                return super().execute(sql, params)

        raw = Path(self.tmp, 'boom.cr2')
        raw.write_bytes(b'II\x2a\x00' + b'RAWCONTENT' * 20)
        with self.assertRaises(RuntimeError):
            fototeka_views._intake_photo_from_path(
                _FailingInsertCursor(), raw, 'boom.cr2', raw.stat().st_size, '.cr2',
                autor_email='a@b.rs', opis=None, tags=[],
                datum_override=date(2026, 1, 1),
                veza=None, u_prijemnom_redu=False, poreklo='upload')
        orphans = [p for p in self.arhiva.rglob('*') if p.is_file()]
        self.assertEqual(orphans, [])


# ---------------------------------------------------------------------------
# Route-level: attach preview, single upload, exhibition create
# ---------------------------------------------------------------------------

class _RouteTestCase(unittest.TestCase):

    def setUp(self):
        museum_app.app.config['TESTING'] = True
        csrf_was = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.addCleanup(museum_app.app.config.__setitem__, 'WTF_CSRF_ENABLED', csrf_was)
        module_patch = patch.object(
            museum_app.app, 'user_has_module_access', lambda *a, **k: True)
        module_patch.start()
        self.addCleanup(module_patch.stop)

        self.arhiva = tempfile.mkdtemp(prefix='fototeka5-arhiva-')
        self.media = tempfile.mkdtemp(prefix='fototeka5-media-')
        self.addCleanup(shutil.rmtree, self.arhiva, True)
        self.addCleanup(shutil.rmtree, self.media, True)
        env = patch.dict(os.environ, {'FOTOTEKA_ARHIVA_PATH': self.arhiva,
                                      'FOTOTEKA_MEDIA_PATH': self.media})
        env.start()
        self.addCleanup(env.stop)
        self.client = museum_app.app.test_client()

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
        db_patch = patch.object(fototeka_views, 'get_postgres_connection', lambda **k: conn)
        db_patch.start()
        self.addCleanup(db_patch.stop)
        return cursor


class AttachPreviewTests(_RouteTestCase):

    def test_attach_jpg_generates_derivatives_and_marks_spremna(self):
        cursor = self.use_db({'FROM fotografije WHERE id': _photo(status='bez_derivata')})
        self.login(AUTHOR)
        response = self.post(
            '/fototeka/5/derivat',
            data={'preview': (_jpeg_bytes(), 'preview.jpg')},
            content_type='multipart/form-data')
        self.assertEqual(response.status_code, 302)
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertIn("status = 'spremna'", joined)
        # both derivatives were written under the photo's sha
        for kind in ('jpg', 'thumb'):
            rel = fototeka_jobs.derivative_relative_path(SHA, kind)
            self.assertTrue((Path(self.media) / rel).is_file())

    def test_attach_rejects_non_preview_extension(self):
        self.use_db({'FROM fotografije WHERE id': _photo(status='bez_derivata')})
        self.login(AUTHOR)
        response = self.post(
            '/fototeka/5/derivat',
            data={'preview': (io.BytesIO(b'x'), 'file.cr2')},
            content_type='multipart/form-data')
        self.assertEqual(response.status_code, 302)  # rejected, redirected back
        # no derivative was written for a rejected extension
        self.assertEqual(list(Path(self.media).rglob('*.jpg')), [])

    def test_attach_rejected_for_spremna_photo(self):
        # A5: a 'spremna' photo's derivative (built from the RAW original) must
        # not be silently overwritten by an unrelated preview upload.
        cursor = self.use_db({'FROM fotografije WHERE id': _photo(status='spremna')})
        self.login(AUTHOR)
        response = self.post(
            '/fototeka/5/derivat',
            data={'preview': (_jpeg_bytes(), 'preview.jpg')},
            content_type='multipart/form-data')
        self.assertEqual(response.status_code, 302)
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertNotIn("status = 'spremna'", joined)
        # nothing was written/overwritten under the media root
        self.assertEqual(list(Path(self.media).rglob('*.jpg')), [])

    def test_reprocess_rejected_for_spremna_photo(self):
        cursor = self.use_db({'FROM fotografije WHERE id': _photo(status='spremna')})
        self.login(AUTHOR)
        response = self.post('/fototeka/5/ponovi-obradu', data={})
        self.assertEqual(response.status_code, 302)
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertNotIn('INSERT INTO foto_poslovi', joined)

    def test_reprocess_allowed_for_greska(self):
        cursor = self.use_db({'FROM fotografije WHERE id': _photo(status='greska')})
        self.login(AUTHOR)
        response = self.post('/fototeka/5/ponovi-obradu', data={})
        self.assertEqual(response.status_code, 302)
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertIn('INSERT INTO foto_poslovi', joined)


class SingleUploadEndpointTests(_RouteTestCase):

    def test_single_upload_returns_json_id(self):
        self.use_db({'INSERT INTO fotografije': {'id': 12}})
        self.login(AUTHOR)
        response = self.post(
            '/fototeka/upload/jedan',
            data={'file': (_jpeg_bytes(), 'a.jpg'), 'veza_tip': 'bez'},
            content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['ok'])
        self.assertEqual(data['id'], 12)

    def test_single_upload_dedup_reports_json(self):
        self.use_db({'SELECT id FROM fotografije WHERE sha256': {'id': 7}})
        self.login(AUTHOR)
        response = self.post(
            '/fototeka/upload/jedan',
            data={'file': (_jpeg_bytes(), 'a.jpg'), 'veza_tip': 'bez'},
            content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.get_json()['ok'])

    def test_single_upload_requires_login(self):
        response = self.post('/fototeka/upload/jedan', data={})
        self.assertEqual(response.status_code, 302)


class ExhibitionCreateTests(_RouteTestCase):

    def test_new_exhibition_name_creates_and_links(self):
        cursor = self.use_db({
            'INSERT INTO fotografije': {'id': 3},
            'INSERT INTO exhibitions': {'id': 88},
        })
        self.login(AUTHOR)
        response = self.post(
            '/fototeka/upload/jedan',
            data={'file': (_jpeg_bytes(), 'a.jpg'),
                  'veza_tip': 'izlozba', 'veza_izlozba_id': '',
                  'veza_izlozba_naziv': 'Нова изложба минерала'},
            content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()['ok'])
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertIn('INSERT INTO exhibitions', joined)
        self.assertIn('INSERT INTO foto_veza_izlozba', joined)

    def test_existing_title_reused_not_duplicated(self):
        # C3 (#18): the sequential upload sends the same new-exhibition name in
        # N per-file requests; a same-titled exhibition must be reused, not
        # re-inserted, so N files do not create N duplicate exhibitions.
        cursor = self.use_db({
            'INSERT INTO fotografije': {'id': 4},
            'exhibitions WHERE title': {'id': 55},
        })
        self.login(AUTHOR)
        response = self.post(
            '/fototeka/upload/jedan',
            data={'file': (_jpeg_bytes(), 'b.jpg'),
                  'veza_tip': 'izlozba', 'veza_izlozba_id': '',
                  'veza_izlozba_naziv': 'Постојећа изложба'},
            content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()['ok'])
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertNotIn('INSERT INTO exhibitions', joined)  # reused, not duplicated
        veza_params = [p for sql, p in cursor.executed
                       if 'INSERT INTO foto_veza_izlozba' in sql]
        self.assertTrue(veza_params)
        self.assertIn(55, veza_params[0])

    def test_missing_exhibition_selection_errors(self):
        cursor = _FakeCursor()
        with patch.object(fototeka_views, 'get_postgres_connection',
                          lambda **k: _FakeConnection(cursor)):
            with museum_app.app.test_request_context(
                    '/', method='POST',
                    data={'veza_tip': 'izlozba', 'veza_izlozba_id': '',
                          'veza_izlozba_naziv': ''}):
                from flask import request
                with self.assertRaises(ValueError):
                    fototeka_views._parse_veza_form(request.form, cursor)


if __name__ == '__main__':
    unittest.main()
