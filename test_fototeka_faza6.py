#!/usr/bin/env python3
"""Tests for the gallery improvement package:

1. Sorting: whitelisted sort column + direction reach the ORDER BY.
2. View mode: purely client-side (localStorage) — the gallery renders the
   toggle and a single item container that the JS reclasses.
3. ZIP download: selected photos stream as a ZIP (JPG derivative or original),
   built to a temp file; bad/empty selection and path safety are handled.
4. Bug: the original/RAW download button appears only when the archival file
   really exists, and is labelled 'RAW' only for actual camera RAW.
"""

import io
import os
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

os.environ['FLASK_ENV'] = 'testing'  # force: sibling modules may leak 'production'
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

from datetime import datetime

from PIL import Image

import app as museum_app
import fototeka_jobs
import fototeka_views


AUTHOR = {
    'user_id': 10, 'user_email': 'autor@nhmbeo.rs', 'user_name': 'Аутор',
    'user_role': 'employee', 'is_admin': False,
    'user_department': 'ГЕОЛОГИЈА', 'is_department_head': False,
}
SHA = 'd' * 64


def _photo(**over):
    photo = {
        'id': 5, 'sha256': SHA, 'raw_putanja': 'razno/2026/x__dddddddd.jpg',
        'original_ime': 'x.jpg', 'ekstenzija': '.jpg', 'velicina_bajtova': 10,
        'width': 800, 'height': 600, 'autor_email': AUTHOR['user_email'],
        'datum_snimanja': None, 'exif': {}, 'opis': 'Опис', 'poreklo': 'upload',
        'status': 'spremna', 'u_prijemnom_redu': False, 'obrisana': False,
        'fixity_proveren_at': None, 'fixity_ok': None,
        'created_at': datetime(2026, 7, 9, 8, 0), 'updated_at': None,
    }
    photo.update(over)
    return photo


def _write_jpeg(path, size=(300, 200)):
    Image.new('RGB', size, (30, 90, 40)).save(path, format='JPEG')
    return path


class _FakeCursor:
    def __init__(self, canned=None):
        self.canned = dict(canned or {})
        self._pending = None
        self.executed = []

    def execute(self, sql, params=None):
        normalized = ' '.join(sql.split())
        self.executed.append((normalized, params))
        for needle, row in self.canned.items():
            if needle in normalized:  # match whitespace-normalized SQL
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

        self.arhiva = tempfile.mkdtemp(prefix='fototeka6-arhiva-')
        self.media = tempfile.mkdtemp(prefix='fototeka6-media-')
        self.addCleanup(shutil.rmtree, self.arhiva, True)
        self.addCleanup(shutil.rmtree, self.media, True)
        env = patch.dict(os.environ, {'FOTOTEKA_ARHIVA_PATH': self.arhiva,
                                      'FOTOTEKA_MEDIA_PATH': self.media})
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
        db_patch = patch.object(fototeka_views, 'get_postgres_connection', lambda **k: conn)
        db_patch.start()
        self.addCleanup(db_patch.stop)
        return cursor

    def _raw_file(self, photo):
        path = Path(self.arhiva) / photo['raw_putanja']
        path.parent.mkdir(parents=True, exist_ok=True)
        _write_jpeg(path)
        return path

    def _derivative_file(self, sha, kind='jpg'):
        path = Path(self.media) / fototeka_jobs.derivative_relative_path(sha, kind)
        path.parent.mkdir(parents=True, exist_ok=True)
        _write_jpeg(path)
        return path


# ---------------------------------------------------------------------------
# 1. Sorting
# ---------------------------------------------------------------------------

class SortTests(_RouteTestCase):

    def _gallery_db(self):
        return self.use_db({
            'SELECT COUNT(*)': {'total': 0},
            'ORDER BY': [],  # photo list
        })

    def test_sort_by_name_ascending_reaches_order_by(self):
        cursor = self._gallery_db()
        self.login(AUTHOR)
        self.get('/fototeka?sort=naziv&smer=asc')
        order = [sql for sql, _ in cursor.executed if 'ORDER BY' in sql][0]
        self.assertIn('lower(f.original_ime) ASC', order)

    def test_invalid_sort_falls_back_to_capture_date(self):
        cursor = self._gallery_db()
        self.login(AUTHOR)
        self.get('/fototeka?sort=DROP&smer=weird')
        order = [sql for sql, _ in cursor.executed if 'ORDER BY' in sql][0]
        self.assertIn('datum_snimanja', order)   # snimak fallback
        self.assertIn('DESC', order)              # smer fallback


class FormatBadgeTests(_RouteTestCase):
    """Each thumbnail carries a small format badge (JPG/TIFF/CR2/NEF...)."""

    def _gallery_with(self, photos):
        # 'f.ekstenzija' uniquely matches the photo-list SELECT (not the facet
        # queries), so facets stay empty while the list returns these photos.
        return self.use_db({'SELECT COUNT(*)': {'total': len(photos)},
                            'f.ekstenzija': photos})

    def test_format_badge_shows_uppercase_label(self):
        self._gallery_with([_photo(id=5, ekstenzija='.cr2'),
                            _photo(id=6, ekstenzija='.tiff'),
                            _photo(id=7, ekstenzija='.jpeg')])
        self.login(AUTHOR)
        r = self.get('/fototeka')
        self.assertEqual(r.status_code, 200)
        html = r.data.decode('utf-8')
        self.assertIn('class="foto-format"', html)
        self.assertIn('>CR2</span>', html)     # RAW kept as-is
        self.assertIn('>TIFF</span>', html)    # .tiff normalized
        self.assertIn('>JPG</span>', html)     # .jpeg normalized to JPG

    def test_format_label_helper(self):
        self.assertEqual(fototeka_views._format_label('.NEF'), 'NEF')
        self.assertEqual(fototeka_views._format_label('.jpeg'), 'JPG')
        self.assertEqual(fototeka_views._format_label('.tif'), 'TIFF')
        self.assertEqual(fototeka_views._format_label(None), '—')


class DownloadModalTests(_RouteTestCase):
    """The jpg/original choice moved out of the toolbar into a modal opened by
    the download button; the modal carries the size/warning wiring."""

    def _render(self):
        self.use_db({'SELECT COUNT(*)': {'total': 1},
                     'f.ekstenzija': [_photo(id=5, ekstenzija='.cr2',
                                             velicina_bajtova=1234)]})
        self.login(AUTHOR)
        r = self.get('/fototeka')
        self.assertEqual(r.status_code, 200)
        return r.data.decode('utf-8')

    def test_modal_and_radios_present(self):
        html = self._render()
        self.assertIn('id="fototekaDownloadModal"', html)
        self.assertIn('name="fototekaSlojChoice"', html)
        self.assertIn('value="jpg"', html)
        self.assertIn('value="original"', html)
        self.assertIn('id="fototekaDownloadOpen"', html)

    def test_old_inline_layer_select_removed(self):
        html = self._render()
        # the old toolbar <select name="sloj"> is gone; sloj is now a hidden input
        self.assertNotIn('<option value="jpg">JPG преглед</option>', html)
        self.assertIn('id="fototekaSloj"', html)
        self.assertIn('name="sloj"', html)

    def test_zip_limits_and_byte_data_present(self):
        html = self._render()
        # JS needs the ZIP limits and per-photo bytes to compute size + warning
        self.assertIn('data-zip-max-bytes="{}"'.format(
            fototeka_views.ZIP_MAX_TOTAL_BYTES), html)
        self.assertIn('data-zip-max-count="{}"'.format(
            fototeka_views.DOWNLOAD_ZIP_MAX), html)
        self.assertIn('data-bytes="1234"', html)


# ---------------------------------------------------------------------------
# 4. Conditional original/RAW button
# ---------------------------------------------------------------------------

class OriginalButtonTests(_RouteTestCase):

    def test_button_hidden_when_original_missing(self):
        # DB row exists but no file on disk -> no download button
        self.use_db({'FROM fotografije WHERE id': _photo()})
        self.login(AUTHOR)
        response = self.get('/fototeka/5')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Преузми'.encode('utf-8'), response.data)

    def test_jpeg_original_labelled_original_not_raw(self):
        photo = _photo(ekstenzija='.jpg')
        self._raw_file(photo)
        self.use_db({'FROM fotografije WHERE id': photo})
        self.login(AUTHOR)
        response = self.get('/fototeka/5')
        self.assertIn('Преузми оригинал'.encode('utf-8'), response.data)
        self.assertNotIn('RAW оригинал'.encode('utf-8'), response.data)

    def test_camera_raw_labelled_raw(self):
        photo = _photo(ekstenzija='.cr2', raw_putanja='razno/2026/x__dddddddd.cr2',
                       status='bez_derivata')
        self._raw_file(photo)
        self.use_db({'FROM fotografije WHERE id': photo})
        self.login(AUTHOR)
        response = self.get('/fototeka/5')
        self.assertIn('RAW оригинал'.encode('utf-8'), response.data)

    def test_archival_path_helper_rejects_traversal(self):
        with museum_app.app.test_request_context():
            self.assertIsNone(fototeka_views._archival_original_path(
                _photo(raw_putanja='../secret.jpg')))

    def test_filename_and_email_marked_no_translate(self):
        # D5: naturally-Latin identifiers (filename, author email) must be
        # marked data-no-translate so the Latin<->Cyrillic transliterator does
        # not corrupt them in the display.
        self.use_db({'FROM fotografije WHERE id': _photo()})
        self.login(AUTHOR)
        response = self.get('/fototeka/5')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('<td data-no-translate>autor@nhmbeo.rs</td>', html)
        self.assertIn('<td data-no-translate>x.jpg</td>', html)


# ---------------------------------------------------------------------------
# 3. ZIP download
# ---------------------------------------------------------------------------

class ZipDownloadTests(_RouteTestCase):

    def test_zip_of_originals(self):
        photo = _photo()
        self._raw_file(photo)
        self.use_db({'FROM fotografije WHERE obrisana = FALSE AND id': [photo]})
        self.login(AUTHOR)
        response = self.post('/fototeka/preuzmi-zip',
                             data={'ids': ['5'], 'sloj': 'original'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/zip')
        names = zipfile.ZipFile(io.BytesIO(response.data)).namelist()
        self.assertEqual(names, ['x.jpg'])

    def test_zip_of_jpg_derivatives(self):
        photo = _photo()
        self._derivative_file(SHA, 'jpg')
        self.use_db({'FROM fotografije WHERE obrisana = FALSE AND id': [photo]})
        self.login(AUTHOR)
        response = self.post('/fototeka/preuzmi-zip',
                             data={'ids': ['5'], 'sloj': 'jpg'})
        self.assertEqual(response.status_code, 200)
        names = zipfile.ZipFile(io.BytesIO(response.data)).namelist()
        self.assertEqual(names, ['x.jpg'])

    def test_empty_selection_redirects(self):
        self.use_db({})
        self.login(AUTHOR)
        response = self.post('/fototeka/preuzmi-zip', data={'ids': []})
        self.assertEqual(response.status_code, 302)

    def test_missing_files_yield_no_download(self):
        # rows exist but neither derivative nor original on disk
        photo = _photo()
        self.use_db({'FROM fotografije WHERE obrisana = FALSE AND id': [photo]})
        self.login(AUTHOR)
        response = self.post('/fototeka/preuzmi-zip',
                             data={'ids': ['5'], 'sloj': 'original'})
        self.assertEqual(response.status_code, 302)  # nothing to zip -> back

    def test_zip_requires_login(self):
        response = self.post('/fototeka/preuzmi-zip', data={'ids': ['5']})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_zip_stops_at_total_byte_cap(self):
        # B2: a selection whose running size exceeds the archive byte budget is
        # truncated (keeps one file + a note) instead of building an unbounded
        # archive that could fill the disk / hang the worker.
        p5 = _photo(id=5, raw_putanja='razno/2026/a__dddddddd.jpg', original_ime='a.jpg')
        p6 = _photo(id=6, raw_putanja='razno/2026/b__dddddddd.jpg', original_ime='b.jpg')
        for p in (p5, p6):
            self._raw_file(p)
        self.use_db({'FROM fotografije WHERE obrisana = FALSE AND id': [p5, p6]})
        self.login(AUTHOR)
        with patch.object(fototeka_views, 'ZIP_MAX_TOTAL_BYTES', 1):
            response = self.post('/fototeka/preuzmi-zip',
                                 data={'ids': ['5', '6'], 'sloj': 'original'})
        self.assertEqual(response.status_code, 200)
        names = zipfile.ZipFile(io.BytesIO(response.data)).namelist()
        self.assertIn('NAPOMENA.txt', names)
        self.assertEqual(len([n for n in names if n != 'NAPOMENA.txt']), 1)

    def test_zip_temp_built_on_data_partition_not_tmp(self):
        # B2: the archive is built under the media temp dir (data partition),
        # not the default /tmp (tmpfs/RAM on this host).
        photo = _photo()
        self._raw_file(photo)
        self.use_db({'FROM fotografije WHERE obrisana = FALSE AND id': [photo]})
        self.login(AUTHOR)
        seen = {}
        real_ntf = tempfile.NamedTemporaryFile

        def _spy(*a, **k):
            seen['dir'] = k.get('dir')
            return real_ntf(*a, **k)

        with patch.object(tempfile, 'NamedTemporaryFile', _spy):
            response = self.post('/fototeka/preuzmi-zip',
                                 data={'ids': ['5'], 'sloj': 'original'})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(seen.get('dir'))
        self.assertTrue(str(seen['dir']).startswith(self.media))


if __name__ == '__main__':
    unittest.main()
