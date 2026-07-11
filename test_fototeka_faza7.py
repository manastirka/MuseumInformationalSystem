#!/usr/bin/env python3
"""Tests for Фототека access control (javno / privatno).

Rules: 'javno' photos are visible to every logged-in employee; 'privatno' only
to the author (plus admin/director for supervision). Enforcement is server-side
at every point — gallery list, photo page, both download routes and the ZIP —
so a direct URL to another user's private photo is 403, not merely hidden.
Only the author + admin/director may change visibility.
"""

import io
import os
import shutil
import tempfile
import unittest
from datetime import datetime
from unittest.mock import patch

os.environ['FLASK_ENV'] = 'testing'  # force: sibling modules may leak 'production'
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

from PIL import Image

import app as museum_app
import fototeka_views


def _jpeg_bytes(size=(64, 48)):
    buf = io.BytesIO()
    Image.new('RGB', size, (10, 20, 30)).save(buf, format='JPEG')
    buf.seek(0)
    return buf


def _insert_vidljivost(cur):
    """The vidljivost value carried by the INSERT INTO fotografije (it is the
    last positional parameter), or a sentinel if no insert happened."""
    for sql, params in cur.executed:
        if 'INSERT INTO fotografije' in sql and params:
            return params[-1]
    return '<no-insert>'


AUTHOR = {'user_id': 10, 'user_email': 'autor@nhmbeo.rs', 'user_name': 'Аутор',
          'user_role': 'employee', 'is_admin': False, 'user_department': 'ГЕО',
          'is_department_head': False}
OTHER = {'user_id': 11, 'user_email': 'drugi@nhmbeo.rs', 'user_name': 'Други',
         'user_role': 'employee', 'is_admin': False, 'user_department': 'ГЕО',
         'is_department_head': False}
HEAD = {'user_id': 12, 'user_email': 'sef@nhmbeo.rs', 'user_name': 'Шеф',
        'user_role': 'sef_odeljenja', 'is_admin': False, 'user_department': 'ГЕО',
        'is_department_head': True}
DIRECTOR = {'user_id': 30, 'user_email': 'direktor@nhmbeo.rs', 'user_name': 'Дир',
            'user_role': 'direktor', 'is_admin': False, 'user_department': None,
            'is_department_head': False}
ADMIN = {'user_id': 1, 'user_email': 'admin@nhmbeo.rs', 'user_name': 'Админ',
         'user_role': 'admin', 'is_admin': True, 'user_department': None,
         'is_department_head': False}

SHA = 'f' * 64


def _photo(**over):
    photo = {
        'id': 5, 'sha256': SHA, 'raw_putanja': 'razno/2026/x__ffffffff.jpg',
        'original_ime': 'x.jpg', 'ekstenzija': '.jpg', 'velicina_bajtova': 10,
        'width': 800, 'height': 600, 'autor_email': AUTHOR['user_email'],
        'datum_snimanja': None, 'exif': {}, 'opis': 'Опис', 'poreklo': 'upload',
        'status': 'spremna', 'u_prijemnom_redu': False, 'obrisana': False,
        'vidljivost': 'privatno',
        'fixity_proveren_at': None, 'fixity_ok': None,
        'created_at': datetime(2026, 7, 9, 8, 0), 'updated_at': None,
    }
    photo.update(over)
    return photo


class _FakeCursor:
    def __init__(self, canned=None):
        self.canned = dict(canned or {})
        self._pending = None
        self.executed = []

    def execute(self, sql, params=None):
        normalized = ' '.join(sql.split())
        self.executed.append((normalized, params))
        for needle, row in self.canned.items():
            if needle in normalized:
                self._pending = row
                return
        self._pending = None

    def fetchone(self):
        v = self._pending
        return (v[0] if v else None) if isinstance(v, list) else v

    def fetchall(self):
        v = self._pending
        return v if isinstance(v, list) else ([v] if v else [])

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
# Pure rules
# ---------------------------------------------------------------------------

class RuleTests(unittest.TestCase):

    def test_private_visible_only_to_author_admin_director(self):
        priv = _photo(vidljivost='privatno')
        self.assertTrue(fototeka_views.can_view_photo(AUTHOR, priv))
        self.assertTrue(fototeka_views.can_view_photo(ADMIN, priv))
        self.assertTrue(fototeka_views.can_view_photo(DIRECTOR, priv))
        self.assertFalse(fototeka_views.can_view_photo(OTHER, priv))
        self.assertFalse(fototeka_views.can_view_photo(HEAD, priv))  # head is not special here

    def test_public_visible_to_all(self):
        pub = _photo(vidljivost='javno')
        for who in (AUTHOR, OTHER, HEAD, DIRECTOR, ADMIN):
            self.assertTrue(fototeka_views.can_view_photo(who, pub))

    def test_missing_visibility_treated_public(self):
        self.assertTrue(fototeka_views.can_view_photo(OTHER, _photo(vidljivost=None)))

    def test_change_visibility_author_admin_director_only(self):
        p = _photo()
        self.assertTrue(fototeka_views.can_change_visibility(AUTHOR, p))
        self.assertTrue(fototeka_views.can_change_visibility(ADMIN, p))
        self.assertTrue(fototeka_views.can_change_visibility(DIRECTOR, p))
        self.assertFalse(fototeka_views.can_change_visibility(OTHER, p))
        self.assertFalse(fototeka_views.can_change_visibility(HEAD, p))

    def test_visibility_filter_admin_unrestricted(self):
        clause, params = fototeka_views._visibility_filter(ADMIN, 'f')
        self.assertIsNone(clause)
        clause, params = fototeka_views._visibility_filter(OTHER, 'f')
        self.assertIn('vidljivost', clause)
        self.assertEqual(params, ['javno', 'drugi@nhmbeo.rs'])


# ---------------------------------------------------------------------------
# Route enforcement
# ---------------------------------------------------------------------------

class _RouteTestCase(unittest.TestCase):

    def setUp(self):
        museum_app.app.config['TESTING'] = True
        csrf_was = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.addCleanup(museum_app.app.config.__setitem__, 'WTF_CSRF_ENABLED', csrf_was)
        mp = patch.object(museum_app.app, 'user_has_module_access', lambda *a, **k: True)
        mp.start()
        self.addCleanup(mp.stop)
        self.arhiva = tempfile.mkdtemp(prefix='fototeka7-a-')
        self.media = tempfile.mkdtemp(prefix='fototeka7-m-')
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
        cur = _FakeCursor(canned)
        p = patch.object(fototeka_views, 'get_postgres_connection', lambda **k: _FakeConnection(cur))
        p.start()
        self.addCleanup(p.stop)
        return cur


class PhotoPageAccessTests(_RouteTestCase):

    def test_other_curator_gets_403_on_private_page(self):
        self.use_db({'FROM fotografije WHERE id': _photo(vidljivost='privatno')})
        self.login(OTHER)
        self.assertEqual(self.get('/fototeka/5').status_code, 403)

    def test_author_sees_own_private_page(self):
        self.use_db({'FROM fotografije WHERE id': _photo(vidljivost='privatno')})
        self.login(AUTHOR)
        self.assertEqual(self.get('/fototeka/5').status_code, 200)

    def test_public_page_visible_to_other(self):
        self.use_db({'FROM fotografije WHERE id': _photo(vidljivost='javno')})
        self.login(OTHER)
        self.assertEqual(self.get('/fototeka/5').status_code, 200)

    def test_admin_sees_private_page(self):
        self.use_db({'FROM fotografije WHERE id': _photo(vidljivost='privatno')})
        self.login(ADMIN)
        self.assertEqual(self.get('/fototeka/5').status_code, 200)


class FileServeAccessTests(_RouteTestCase):

    def test_derivat_403_for_other_on_private(self):
        self.use_db({'FROM fotografije WHERE id': _photo(vidljivost='privatno')})
        self.login(OTHER)
        self.assertEqual(self.get('/fototeka/media/5/jpg').status_code, 403)

    def test_raw_403_for_other_on_private(self):
        self.use_db({'FROM fotografije WHERE id': _photo(vidljivost='privatno')})
        self.login(OTHER)
        self.assertEqual(self.get('/fototeka/raw/5').status_code, 403)

    def test_derivat_public_ok_for_other(self):
        self.use_db({'FROM fotografije WHERE id': _photo(vidljivost='javno', status='obrada')})
        self.login(OTHER)
        # public: not 403 (serves placeholder while processing)
        self.assertNotEqual(self.get('/fototeka/media/5/jpg').status_code, 403)

    def _write_derivative(self, sha, kind='jpg'):
        import fototeka_jobs
        rel = fototeka_jobs.derivative_relative_path(sha, kind)
        path = os.path.join(self.media, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        Image.new('RGB', (40, 30), (10, 20, 30)).save(path, format='JPEG')
        return path

    def test_private_derivat_is_not_shared_cacheable(self):
        # A6: a private photo's derivative must never carry `public` cache and
        # must be `no-store` so a javno->privatno flip is effective immediately.
        self._write_derivative(SHA, 'jpg')
        self.use_db({'FROM fotografije WHERE id': _photo(vidljivost='privatno')})
        self.login(AUTHOR)
        r = self.get('/fototeka/media/5/jpg')
        self.assertEqual(r.status_code, 200)
        cc = r.headers.get('Cache-Control', '')
        self.assertNotIn('public', cc)
        self.assertIn('no-store', cc)
        self.assertIn('Cookie', r.headers.get('Vary', ''))

    def test_public_derivat_is_private_not_public_cache(self):
        self._write_derivative(SHA, 'jpg')
        self.use_db({'FROM fotografije WHERE id': _photo(vidljivost='javno')})
        self.login(OTHER)
        r = self.get('/fototeka/media/5/jpg')
        self.assertEqual(r.status_code, 200)
        cc = r.headers.get('Cache-Control', '')
        self.assertNotIn('public', cc)  # behind login → never a shared cache
        self.assertIn('private', cc)


class ZipAccessTests(_RouteTestCase):

    def test_other_curator_403_zip_with_private(self):
        self.use_db({'FROM fotografije WHERE obrisana = FALSE AND id':
                     [_photo(vidljivost='privatno')]})
        self.login(OTHER)
        r = self.post('/fototeka/preuzmi-zip', data={'ids': ['5'], 'sloj': 'jpg'})
        self.assertEqual(r.status_code, 403)

    def test_author_zip_not_forbidden(self):
        self.use_db({'FROM fotografije WHERE obrisana = FALSE AND id':
                     [_photo(vidljivost='privatno')]})
        self.login(AUTHOR)
        r = self.post('/fototeka/preuzmi-zip', data={'ids': ['5'], 'sloj': 'jpg'})
        self.assertNotEqual(r.status_code, 403)  # allowed (no files -> 302, but not 403)


class VisibilityChangeTests(_RouteTestCase):

    def test_author_may_change(self):
        cur = self.use_db({'FROM fotografije WHERE id': _photo(vidljivost='javno')})
        self.login(AUTHOR)
        r = self.post('/fototeka/5/vidljivost', data={'vidljivost': 'privatno'})
        self.assertEqual(r.status_code, 302)
        joined = ' '.join(sql for sql, _ in cur.executed)
        self.assertIn('SET vidljivost', joined)

    def test_other_cannot_change(self):
        self.use_db({'FROM fotografije WHERE id': _photo(vidljivost='javno')})
        self.login(OTHER)
        self.assertEqual(self.post('/fototeka/5/vidljivost',
                                   data={'vidljivost': 'privatno'}).status_code, 403)

    def test_department_head_cannot_change(self):
        self.use_db({'FROM fotografije WHERE id': _photo(vidljivost='javno')})
        self.login(HEAD)
        self.assertEqual(self.post('/fototeka/5/vidljivost',
                                   data={'vidljivost': 'privatno'}).status_code, 403)


class UploadVisibilityTests(_RouteTestCase):
    """Regression for K1: the 'privatno' choice must survive BOTH upload paths.

    The classic multi-POST (handle_upload) is only the no-JS fallback; the
    per-file JSON endpoint (handle_upload_jedan) is the path the browser
    actually uses, so a regression there silently makes every 'privatno'
    upload public."""

    def test_classic_multipost_private_stays_private(self):
        cur = self.use_db({'INSERT INTO fotografije': {'id': 21}})
        self.login(AUTHOR)
        r = self.post('/fototeka/upload',
                      data={'files': (_jpeg_bytes(), 'a.jpg'),
                            'veza_tip': 'bez', 'vidljivost': 'privatno'},
                      content_type='multipart/form-data')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(_insert_vidljivost(cur), 'privatno')

    def test_sequential_single_private_stays_private(self):
        cur = self.use_db({'INSERT INTO fotografije': {'id': 22}})
        self.login(AUTHOR)
        r = self.post('/fototeka/upload/jedan',
                      data={'file': (_jpeg_bytes(), 'a.jpg'),
                            'veza_tip': 'bez', 'vidljivost': 'privatno'},
                      content_type='multipart/form-data')
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.get_json()['ok'])
        self.assertEqual(_insert_vidljivost(cur), 'privatno')

    def test_sequential_single_default_is_public(self):
        cur = self.use_db({'INSERT INTO fotografije': {'id': 23}})
        self.login(AUTHOR)
        self.post('/fototeka/upload/jedan',
                  data={'file': (_jpeg_bytes(), 'a.jpg'), 'veza_tip': 'bez'},
                  content_type='multipart/form-data')
        self.assertEqual(_insert_vidljivost(cur), 'javno')


class HeadBlindWriteTests(_RouteTestCase):
    """A3: a department head may read+edit public photos, but a direct POST
    must not mutate a private photo of another author (GET is already 403)."""

    def test_head_cannot_azuriraj_others_private(self):
        cur = self.use_db({'FROM fotografije WHERE id': _photo(vidljivost='privatno')})
        self.login(HEAD)
        r = self.post('/fototeka/5/azuriraj', data={'opis': 'провала'})
        self.assertEqual(r.status_code, 403)
        joined = ' '.join(sql for sql, _ in cur.executed)
        self.assertNotIn('UPDATE fotografije SET opis', joined)

    def test_head_cannot_add_veza_to_others_private(self):
        self.use_db({'FROM fotografije WHERE id': _photo(vidljivost='privatno')})
        self.login(HEAD)
        r = self.post('/fototeka/5/veza',
                      data={'veza_tip': 'projekat', 'veza_projekat_naziv': 'X'})
        self.assertEqual(r.status_code, 403)

    def test_head_may_azuriraj_public(self):
        cur = self.use_db({'FROM fotografije WHERE id': _photo(vidljivost='javno')})
        self.login(HEAD)
        r = self.post('/fototeka/5/azuriraj', data={'opis': 'легитимно'})
        self.assertEqual(r.status_code, 302)
        joined = ' '.join(sql for sql, _ in cur.executed)
        self.assertIn('UPDATE fotografije SET opis', joined)


class GalleryFilterTests(_RouteTestCase):

    def test_regular_user_gallery_query_filters_visibility(self):
        cur = self.use_db({'SELECT COUNT(*)': {'total': 0}, 'ORDER BY': []})
        self.login(OTHER)
        self.get('/fototeka')
        self.assertTrue(any('vidljivost' in sql for sql, _ in cur.executed))

    def test_admin_gallery_query_unrestricted(self):
        cur = self.use_db({'SELECT COUNT(*)': {'total': 0}, 'ORDER BY': []})
        self.login(ADMIN)
        self.get('/fototeka')
        self.assertFalse(any('vidljivost' in sql for sql, _ in cur.executed))


class ApiPredmetiAccessTests(_RouteTestCase):
    """D4: mineral inventory autocomplete must honour the mineral database's
    own (narrower) access control, not just Фototeka module access."""

    def test_denied_without_mineral_access_returns_empty(self):
        # fototeka module allowed (route passes), mineral_database denied
        with patch.object(museum_app.app, 'user_has_module_access',
                          lambda email, role, key: key != 'mineral_database'):
            self.login(AUTHOR)
            r = self.get('/fototeka/api/predmeti?zbirka=mineral&q=12')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.get_json(), [])

    def test_allowed_with_mineral_access_queries(self):
        cur = self.use_db({'FROM minerals':
                           [{'inventory_number': '123', 'item_name': 'Кварц'}]})
        with patch.object(museum_app.app, 'user_has_module_access',
                          lambda *a, **k: True):
            self.login(AUTHOR)
            r = self.get('/fototeka/api/predmeti?zbirka=mineral&q=12')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(len(r.get_json()), 1)
        self.assertTrue(any('FROM minerals' in sql for sql, _ in cur.executed))


class RequestTooLargeTests(_RouteTestCase):
    """C1: a request over MAX_CONTENT_LENGTH must give the JSON uploader a
    clean message, not an HTML page it would surface as 'server error'."""

    def test_oversized_upload_jedan_returns_json_413(self):
        prev = museum_app.app.config.get('MAX_CONTENT_LENGTH')
        museum_app.app.config['MAX_CONTENT_LENGTH'] = 64
        self.addCleanup(museum_app.app.config.__setitem__, 'MAX_CONTENT_LENGTH', prev)
        self.login(AUTHOR)
        r = self.post('/fototeka/upload/jedan',
                      data={'file': (io.BytesIO(b'x' * 4096), 'big.jpg')},
                      content_type='multipart/form-data')
        self.assertEqual(r.status_code, 413)
        body = r.get_json()
        self.assertIsNotNone(body)
        self.assertFalse(body['ok'])


class FacetLeakTests(_RouteTestCase):
    """A7: author dropdown, tag list and the tag autocomplete must be drawn
    from the same visible set as the gallery — a private photo's author/tag
    must not leak to users who cannot see the photo."""

    def _facet_sqls(self, cur):
        return [sql for sql, _ in cur.executed
                if 'DISTINCT autor_email' in sql or 'DISTINCT t.tag' in sql]

    def test_gallery_facets_filter_visibility_for_regular_user(self):
        cur = self.use_db({'SELECT COUNT(*)': {'total': 0}, 'ORDER BY': []})
        self.login(OTHER)
        self.get('/fototeka')
        facets = self._facet_sqls(cur)
        self.assertEqual(len(facets), 2)  # autori + tagovi
        for sql in facets:
            self.assertIn('vidljivost', sql)

    def test_gallery_facets_unrestricted_for_admin(self):
        cur = self.use_db({'SELECT COUNT(*)': {'total': 0}, 'ORDER BY': []})
        self.login(ADMIN)
        self.get('/fototeka')
        for sql in self._facet_sqls(cur):
            self.assertNotIn('vidljivost', sql)

    def test_api_tagovi_joins_photos_and_filters_visibility(self):
        cur = self.use_db({'fotografija_tagovi': []})
        self.login(OTHER)
        self.get('/fototeka/api/tagovi?q=a')
        sql = [s for s, _ in cur.executed if 'fotografija_tagovi' in s][0]
        self.assertIn('JOIN fotografije', sql)
        self.assertIn('obrisana = FALSE', sql)
        self.assertIn('vidljivost', sql)


if __name__ == '__main__':
    unittest.main()
