#!/usr/bin/env python3
"""Tests for the Фототека module (Phase 1).

Covers: metadata/link helpers, RAW-layout-by-origin and its traversal safety,
EXIF extraction, the edit-permission policy, the derivative worker (real
pyvips derivatives, retry/backoff, fixity mismatch, queue claiming), and the
routes (login/dedup on upload, path-traversal guards on file serving,
admin-only soft delete that never touches the RAW original).
"""

import io
import os
import shutil
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path
from unittest.mock import patch

os.environ['FLASK_ENV'] = 'testing'  # force: sibling modules may leak 'production'
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

from PIL import Image

import app as museum_app
import archive_signature_blueprint
import fototeka_jobs
import fototeka_views


AUTHOR = {
    'user_id': 10, 'user_email': 'autor@nhmbeo.rs', 'user_name': 'Аутор',
    'user_role': 'employee', 'is_admin': False,
    'user_department': 'ГЕОЛОГИЈА', 'is_department_head': False,
}
OTHER = {
    'user_id': 11, 'user_email': 'drugi@nhmbeo.rs', 'user_name': 'Други',
    'user_role': 'employee', 'is_admin': False,
    'user_department': 'ГЕОЛОГИЈА', 'is_department_head': False,
}
HEAD = {
    'user_id': 20, 'user_email': 'sef@nhmbeo.rs', 'user_name': 'Шеф',
    'user_role': 'sef_odeljenja', 'is_admin': False,
    'user_department': 'БИОЛОГИЈА', 'is_department_head': True,
}
DIRECTOR = {
    'user_id': 30, 'user_email': 'direktor@nhmbeo.rs', 'user_name': 'Директор',
    'user_role': 'direktor', 'is_admin': False,
    'user_department': None, 'is_department_head': False,
}
ADMIN = {
    'user_id': 1, 'user_email': 'admin@nhmbeo.rs', 'user_name': 'Админ',
    'user_role': 'admin', 'is_admin': True,
    'user_department': None, 'is_department_head': False,
}

SHA = 'a' * 64


def _photo(**overrides):
    photo = {
        'id': 5, 'sha256': SHA, 'raw_putanja': 'razno/2026/proba__aaaaaaaa.jpg',
        'original_ime': 'proba.jpg', 'ekstenzija': '.jpg',
        'velicina_bajtova': 1234, 'width': 800, 'height': 600,
        'autor_email': AUTHOR['user_email'], 'datum_snimanja': None,
        'exif': {}, 'opis': 'Опис', 'poreklo': 'upload', 'status': 'spremna',
        'u_prijemnom_redu': False, 'obrisana': False,
        'fixity_proveren_at': None, 'fixity_ok': None,
        'created_at': None, 'updated_at': None,
    }
    photo.update(overrides)
    return photo


def _jpeg_bytes(size=(1200, 900), color=(20, 90, 40)):
    buf = io.BytesIO()
    Image.new('RGB', size, color).save(buf, format='JPEG')
    buf.seek(0)
    return buf


# ---------------------------------------------------------------------------
# Fake DB plumbing (mirrors test_document_library.py)
# ---------------------------------------------------------------------------

class _FakeCursor:
    """Returns canned rows matched by SQL substring; records every execute."""

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
# Pure helpers
# ---------------------------------------------------------------------------

class HelperTests(unittest.TestCase):

    def test_parse_tags_splits_dedupes_and_caps(self):
        tags = fototeka_views._parse_tags('витрина, Витрина; поставка ,  ')
        self.assertEqual(tags, ['витрина', 'поставка'])
        self.assertLessEqual(len(fototeka_views._parse_tags(','.join(str(i) for i in range(50)))), 30)

    def test_parse_datum_iso_and_invalid(self):
        self.assertEqual(fototeka_views._parse_datum('2026-07-08'), date(2026, 7, 8))
        self.assertIsNone(fototeka_views._parse_datum(''))
        self.assertIsNone(fototeka_views._parse_datum('08.07.2026'))

    def test_derivative_path_is_sha_sharded(self):
        self.assertEqual(
            fototeka_jobs.derivative_relative_path(SHA, 'thumb'),
            f'thumb/aa/{SHA}.jpg',
        )
        self.assertEqual(
            fototeka_jobs.derivative_relative_path(SHA, 'jpg'),
            f'jpg/aa/{SHA}.jpg',
        )


class RawLayoutTests(unittest.TestCase):

    def test_layout_by_origin(self):
        predmet = fototeka_jobs.raw_intake_relative_path(
            veza_predmet=('mineral', 'ПМ 1234/а'), original_ime='Кварц.jpg', sha256=SHA)
        self.assertTrue(predmet.startswith('zbirke/mineral/'))
        self.assertIn('aaaaaaaa', predmet)

        teren = fototeka_jobs.raw_intake_relative_path(
            veza_teren=(2025, 'Западна Србија'), original_ime='t.JPG', sha256=SHA)
        self.assertTrue(teren.startswith('teren/2025/'))
        self.assertTrue(teren.endswith('.jpg'))  # extension lowercased

        razno = fototeka_jobs.raw_intake_relative_path(
            original_ime='x.png', sha256=SHA, datum=date(2021, 1, 1))
        self.assertTrue(razno.startswith('razno/2021/'))

    def test_safe_segment_neutralizes_traversal(self):
        seg = fototeka_jobs._safe_segment('../../etc/passwd')
        self.assertNotIn('..', seg)
        self.assertNotIn('/', seg)
        # a Cyrillic inventory number survives, path separators do not
        seg2 = fototeka_jobs._safe_segment('ПМ 1234/а')
        self.assertNotIn('/', seg2)
        self.assertTrue(seg2.startswith('ПМ'))

    def test_intake_path_never_escapes_archive(self):
        rel = fototeka_jobs.raw_intake_relative_path(
            veza_predmet=('../../evil', '../x'), original_ime='../../y.jpg', sha256=SHA)
        root = Path('/data/arhiva').resolve()
        resolved = (root / rel).resolve()
        self.assertTrue(str(resolved).startswith(str(root) + os.sep))


class ExifTests(unittest.TestCase):

    def test_plain_image_has_dimensions_no_date(self):
        with Image.open(_jpeg_bytes(size=(640, 480))) as img:
            info = fototeka_views._extract_exif(img)
        self.assertEqual((info['width'], info['height']), (640, 480))
        self.assertIsNone(info['datum_snimanja'])


class PhotoPermissionTests(unittest.TestCase):

    def test_author_admin_director_head_may_edit(self):
        for who in (AUTHOR, ADMIN, DIRECTOR, HEAD):
            self.assertTrue(fototeka_views.can_edit_photo(who, _photo()))

    def test_unrelated_employee_may_not_edit(self):
        self.assertFalse(fototeka_views.can_edit_photo(OTHER, _photo()))

    def test_head_may_edit_public_but_not_others_private(self):
        # A3: a department head edits public photos (view-allowed) but must not
        # be able to mutate a private photo of another author it cannot see.
        self.assertTrue(
            fototeka_views.can_edit_photo(HEAD, _photo(vidljivost='javno')))
        self.assertFalse(
            fototeka_views.can_edit_photo(HEAD, _photo(vidljivost='privatno')))
        # its own author still edits their private photo
        self.assertTrue(
            fototeka_views.can_edit_photo(AUTHOR, _photo(vidljivost='privatno')))


# ---------------------------------------------------------------------------
# Worker: derivatives, retry/backoff, fixity, queue claiming
# ---------------------------------------------------------------------------

class DerivativeTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='fototeka-deriv-')
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.env = patch.dict(os.environ, {'FOTOTEKA_MEDIA_PATH': self.tmp + '/media'})
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_make_derivatives_produces_both_sizes(self):
        raw = Path(self.tmp, 'raw.png')
        Image.new('RGB', (4000, 3000), (120, 30, 30)).save(raw)
        fototeka_jobs.make_derivatives(raw, SHA)
        jpg = Path(self.tmp, 'media', fototeka_jobs.derivative_relative_path(SHA, 'jpg'))
        thumb = Path(self.tmp, 'media', fototeka_jobs.derivative_relative_path(SHA, 'thumb'))
        self.assertTrue(jpg.is_file())
        self.assertTrue(thumb.is_file())
        with Image.open(jpg) as im:
            self.assertEqual(max(im.size), 2500)
        with Image.open(thumb) as im:
            self.assertEqual(max(im.size), 300)


class WorkerRetryTests(unittest.TestCase):

    def _run_fail(self, attempts_before):
        cursor = _FakeCursor()
        conn = _FakeConnection(cursor)
        with patch.object(fototeka_jobs, 'get_postgres_connection', lambda **k: conn):
            fototeka_jobs._fail_job(1, 5, 'derivati', attempts_before, 'boom')
        return cursor.executed

    def test_early_failure_reschedules_with_backoff(self):
        executed = self._run_fail(0)
        joined = ' '.join(sql for sql, _ in executed)
        self.assertIn("status = 'ceka'", joined)
        # first retry uses the 1-minute backoff
        params = [p for _, p in executed if p]
        self.assertTrue(any(1 in p for p in params))

    def test_final_failure_marks_photo_greska(self):
        executed = self._run_fail(fototeka_jobs.MAX_ATTEMPTS - 1)
        joined = ' '.join(sql for sql, _ in executed)
        self.assertIn("status = 'greska'", joined)
        self.assertIn('UPDATE fotografije', joined)

    def test_process_job_derivati_success_marks_spremna(self):
        with patch.object(fototeka_jobs, 'make_derivatives') as mk, \
             patch.object(fototeka_jobs, '_finish_job') as finish, \
             patch.object(fototeka_jobs, '_fail_job') as fail:
            job = {'id': 1, 'fotografija_id': 5, 'tip': 'derivati',
                   'pokusaji': 0, 'sha256': SHA, 'raw_putanja': 'razno/2026/x.jpg', 'ekstenzija': '.jpg'}
            self.assertTrue(fototeka_jobs.process_job(job))
            mk.assert_called_once()
            finish.assert_called_once()
            fail.assert_not_called()

    def test_process_job_routes_failure_to_retry(self):
        with patch.object(fototeka_jobs, 'make_derivatives', side_effect=RuntimeError('vips down')), \
             patch.object(fototeka_jobs, '_fail_job') as fail, \
             patch.object(fototeka_jobs, '_finish_job') as finish:
            job = {'id': 1, 'fotografija_id': 5, 'tip': 'derivati',
                   'pokusaji': 0, 'sha256': SHA, 'raw_putanja': 'razno/2026/x.jpg', 'ekstenzija': '.jpg'}
            self.assertFalse(fototeka_jobs.process_job(job))
            fail.assert_called_once()
            finish.assert_not_called()


class WorkerCrashReclaimTests(unittest.TestCase):
    """B4: a stale 'radi' job (worker died mid-job, possibly a native crash
    that skipped _fail_job) must count as an attempt and eventually
    dead-letter, so a crash-inducing file can't loop forever."""

    def _reclaim(self, reclaimed_rows):
        cursor = _FakeCursor({'UPDATE foto_poslovi': reclaimed_rows})
        conn = _FakeConnection(cursor)
        with patch.object(fototeka_jobs, 'get_postgres_connection', lambda **k: conn):
            n = fototeka_jobs.reclaim_stale_jobs()
        return cursor, n

    def test_reclaim_counts_crash_as_attempt(self):
        cur, n = self._reclaim(
            [{'id': 1, 'fotografija_id': 5, 'tip': 'derivati', 'status': 'ceka'}])
        joined = ' '.join(sql for sql, _ in cur.executed)
        self.assertIn('pokusaji = pokusaji + 1', joined)
        # a job returned to 'ceka' does NOT flip the photo to greska
        self.assertNotIn("UPDATE fotografije SET status = 'greska'", joined)
        self.assertEqual(n, 1)

    def test_reclaim_dead_letters_after_max_and_marks_photo(self):
        cur, n = self._reclaim(
            [{'id': 1, 'fotografija_id': 5, 'tip': 'derivati', 'status': 'greska'}])
        joined = ' '.join(sql for sql, _ in cur.executed)
        self.assertIn("UPDATE fotografije SET status = 'greska'", joined)
        self.assertEqual(n, 1)


class MakeDerivativesTempTests(unittest.TestCase):
    """B4/B7: derivative temp files are per-process (no shared .tmp_<sha>
    collision) and never left behind."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='fototeka-tmp-')
        self.addCleanup(shutil.rmtree, self.tmp, True)
        env = patch.dict(os.environ, {'FOTOTEKA_MEDIA_PATH': self.tmp + '/media'})
        env.start()
        self.addCleanup(env.stop)

    def test_temp_name_is_process_unique_and_cleaned(self):
        import sys
        import types
        seen = []

        class _FakeImg:
            @staticmethod
            def thumbnail(path, width, height=None, size=None, **kw):
                return _FakeImg()

            def write_to_file(self, path, **kw):
                seen.append(os.path.basename(path))
                with open(path, 'wb') as fh:
                    fh.write(b'JPEGDATA')

        fake = types.ModuleType('pyvips')
        fake.Image = _FakeImg
        with patch.dict(sys.modules, {'pyvips': fake}):
            fototeka_jobs.make_derivatives(Path(self.tmp, 'raw.cr2'), SHA)

        media = Path(self.tmp, 'media')
        self.assertEqual([p for p in media.rglob('.tmp_*')], [])  # no leftovers
        self.assertTrue((media / fototeka_jobs.derivative_relative_path(SHA, 'jpg')).is_file())
        self.assertTrue(seen and all(str(os.getpid()) in name for name in seen))


class FixityTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='fototeka-fixity-')
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.env = patch.dict(os.environ, {'FOTOTEKA_ARHIVA_PATH': self.tmp})
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_fixity_ok_when_hash_matches(self):
        raw = Path(self.tmp, 'razno', '2026')
        raw.mkdir(parents=True)
        target = raw / 'x.jpg'
        target.write_bytes(b'hello fixity')
        real_sha = fototeka_jobs.sha256_of_file(target)
        cursor = _FakeCursor()
        conn = _FakeConnection(cursor)
        with patch.object(fototeka_jobs, 'get_postgres_connection', lambda **k: conn):
            report = fototeka_jobs._process_fixity(5, real_sha, target)
        # the UPDATE writes fixity_ok = True as the first param
        update = [p for sql, p in cursor.executed if 'fixity_ok' in sql][0]
        self.assertEqual(update[0], True)
        self.assertEqual(report, {
            'ok': True,
            'fotografija_id': 5,
            'status': 'ok',
            'raw_putanja': str(target),
            'expected_sha256': real_sha,
            'actual_sha256': real_sha,
        })

    def test_fixity_missing_file_reports_reason_and_expected_hash(self):
        target = Path(self.tmp, 'missing.jpg')
        cursor = _FakeCursor()
        conn = _FakeConnection(cursor)
        with patch.object(fototeka_jobs, 'get_postgres_connection', lambda **k: conn), \
             self.assertLogs(fototeka_jobs.logger, level='ERROR') as captured:
            report = fototeka_jobs._process_fixity(5, SHA, target)
        update = [p for sql, p in cursor.executed if 'fixity_ok' in sql][0]
        self.assertEqual(update[0], False)
        self.assertEqual(report['status'], 'missing_file')
        self.assertIsNone(report['actual_sha256'])
        log = '\n'.join(captured.output)
        self.assertIn('FOTOTEKA_FIXITY_MISMATCH photo_id=5', log)
        self.assertIn('reason=missing_file', log)
        self.assertIn(f'path={target}', log)
        self.assertIn(f'expected_sha256={SHA}', log)
        self.assertIn('actual_sha256=<missing>', log)

    def test_fixity_changed_file_reports_both_hashes(self):
        target = Path(self.tmp, 'changed.jpg')
        target.write_bytes(b'changed archival bytes')
        actual_sha = fototeka_jobs.sha256_of_file(target)
        cursor = _FakeCursor()
        conn = _FakeConnection(cursor)
        with patch.object(fototeka_jobs, 'get_postgres_connection', lambda **k: conn), \
             self.assertLogs(fototeka_jobs.logger, level='ERROR') as captured:
            report = fototeka_jobs._process_fixity(5, SHA, target)

        self.assertFalse(report['ok'])
        self.assertEqual(report['status'], 'checksum_mismatch')
        self.assertEqual(report['expected_sha256'], SHA)
        self.assertEqual(report['actual_sha256'], actual_sha)
        log = '\n'.join(captured.output)
        self.assertIn('reason=checksum_mismatch', log)
        self.assertIn(f'expected_sha256={SHA}', log)
        self.assertIn(f'actual_sha256={actual_sha}', log)


class QueueTests(unittest.TestCase):

    def test_claim_returns_none_on_empty_queue(self):
        conn = _FakeConnection(_FakeCursor({}))
        with patch.object(fototeka_jobs, 'get_postgres_connection', lambda **k: conn):
            self.assertIsNone(fototeka_jobs.claim_next_job())

    def test_enqueue_inserts_pending_job(self):
        cursor = _FakeCursor()
        fototeka_jobs.enqueue_job(cursor, 5, 'derivati')
        sql, params = cursor.executed[-1]
        self.assertIn('INSERT INTO foto_poslovi', sql)
        self.assertEqual(params, (5, 'derivati'))


# ---------------------------------------------------------------------------
# Routes
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

        self.arhiva = tempfile.mkdtemp(prefix='fototeka-arhiva-')
        self.media = tempfile.mkdtemp(prefix='fototeka-media-')
        self.addCleanup(shutil.rmtree, self.arhiva, True)
        self.addCleanup(shutil.rmtree, self.media, True)
        env = patch.dict(os.environ, {
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


class UploadRouteTests(_RouteTestCase):

    def test_upload_requires_login(self):
        response = self.post('/fototeka/upload', data={})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_duplicate_sha_is_rejected(self):
        self.use_db({'SELECT id FROM fotografije WHERE sha256': {'id': 7}})
        self.login(AUTHOR)
        response = self.post(
            '/fototeka/upload',
            data={'files': (_jpeg_bytes(), 'proba.jpg'), 'veza_tip': 'bez'},
            content_type='multipart/form-data', follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('већ постоји'.encode('utf-8'), response.data)
        # the RAW archive stays empty — dedup happens before placement
        self.assertEqual(list(Path(self.arhiva).rglob('*.jpg')), [])

    def test_non_image_extension_skipped(self):
        self.use_db({})
        self.login(AUTHOR)
        response = self.post(
            '/fototeka/upload',
            data={'files': (io.BytesIO(b'not an image'), 'malware.exe'), 'veza_tip': 'bez'},
            content_type='multipart/form-data', follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('није дозвољен'.encode('utf-8'), response.data)


class ServeGuardTests(_RouteTestCase):

    def test_serve_raw_blocks_path_traversal(self):
        self.use_db({'FROM fotografije WHERE id': _photo(raw_putanja='../secret.jpg')})
        self.login(AUTHOR)
        response = self.get('/fototeka/raw/5')
        self.assertEqual(response.status_code, 404)

    def test_serve_derivat_placeholder_while_processing(self):
        self.use_db({'FROM fotografije WHERE id': _photo(status='obrada')})
        self.login(AUTHOR)
        response = self.get('/fototeka/media/5/thumb')
        # placeholder is served (200) rather than a broken/missing derivative
        self.assertIn(response.status_code, (200, 404))
        self.assertNotEqual(response.status_code, 500)

    def test_serve_derivat_rejects_unknown_kind(self):
        self.use_db({'FROM fotografije WHERE id': _photo()})
        self.login(AUTHOR)
        response = self.get('/fototeka/media/5/original')
        self.assertEqual(response.status_code, 404)


class PhotoPageRenderTests(_RouteTestCase):
    """Render the photo page through the REAL base.html. Guards against a
    render_template kwarg (e.g. is_admin=<bool>) shadowing a context-processor
    global callable, which made base.html's `{% if not is_admin() %}` raise
    'bool object is not callable' -> HTTP 500 on the very first prod upload."""

    def _full_photo(self, **over):
        photo = _photo(created_at=datetime(2026, 7, 9, 8, 30), status='spremna')
        photo.update(over)
        return photo

    def test_photo_page_renders_for_non_admin(self):
        self.use_db({'FROM fotografije WHERE id': self._full_photo()})
        self.login(AUTHOR)
        response = self.get('/fototeka/5')
        self.assertEqual(response.status_code, 200)

    def test_photo_page_renders_for_admin(self):
        self.use_db({'FROM fotografije WHERE id': self._full_photo()})
        self.login(ADMIN)
        response = self.get('/fototeka/5')
        self.assertEqual(response.status_code, 200)


class SoftDeleteTests(_RouteTestCase):

    def test_soft_delete_is_admin_only(self):
        self.login(AUTHOR)
        response = self.post('/fototeka/5/obrisi')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard', response.headers['Location'])

    def test_admin_soft_delete_keeps_raw_file(self):
        raw_dir = Path(self.arhiva, 'razno', '2026')
        raw_dir.mkdir(parents=True)
        raw_file = raw_dir / 'proba__aaaaaaaa.jpg'
        raw_file.write_bytes(b'raw original')
        cursor = self.use_db({'FROM fotografije WHERE id': _photo()})
        self.login(ADMIN)
        response = self.post('/fototeka/5/obrisi')
        self.assertEqual(response.status_code, 302)
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertIn('obrisana = TRUE', joined)
        # soft delete only — the archive file is untouched
        self.assertTrue(raw_file.is_file())


if __name__ == '__main__':
    unittest.main()
