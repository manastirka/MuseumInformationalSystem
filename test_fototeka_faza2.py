#!/usr/bin/env python3
"""Tests for Фототека Phase 2: reception queue + reverse linking (entitet->foto).

Covers: the entity-reference parser (and that its output is a valid `veza` for
_insert_veza), the entity link filter, the reception-queue flag on upload and
its dedicated screen, the reverse-linking JSON API (linked photos, candidate
search, link, unlink), and route login enforcement.
"""

import io
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

os.environ['FLASK_ENV'] = 'testing'  # force: sibling modules may leak 'production'
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

from PIL import Image

import app as museum_app
import fototeka_views


AUTHOR = {
    'user_id': 10, 'user_email': 'autor@nhmbeo.rs', 'user_name': 'Аутор',
    'user_role': 'employee', 'is_admin': False,
    'user_department': 'ГЕОЛОГИЈА', 'is_department_head': False,
}
ADMIN = {
    'user_id': 1, 'user_email': 'admin@nhmbeo.rs', 'user_name': 'Админ',
    'user_role': 'admin', 'is_admin': True,
    'user_department': None, 'is_department_head': False,
}
OTHER = {
    'user_id': 11, 'user_email': 'drugi@nhmbeo.rs', 'user_name': 'Други',
    'user_role': 'employee', 'is_admin': False,
    'user_department': 'ГЕОЛОГИЈА', 'is_department_head': False,
}

SHA = 'b' * 64


def _photo(**overrides):
    photo = {
        'id': 5, 'sha256': SHA, 'raw_putanja': 'razno/2026/x__bbbbbbbb.jpg',
        'original_ime': 'x.jpg', 'ekstenzija': '.jpg', 'velicina_bajtova': 10,
        'width': 100, 'height': 80, 'autor_email': AUTHOR['user_email'],
        'datum_snimanja': None, 'exif': {}, 'opis': 'Опис', 'poreklo': 'upload',
        'status': 'spremna', 'u_prijemnom_redu': False, 'obrisana': False,
        'fixity_proveren_at': None, 'fixity_ok': None,
        'created_at': None, 'updated_at': None,
    }
    photo.update(overrides)
    return photo


def _jpeg_bytes():
    buf = io.BytesIO()
    Image.new('RGB', (400, 300), (20, 90, 40)).save(buf, format='JPEG')
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
# Pure: entity-reference parser and filter
# ---------------------------------------------------------------------------

class EntityRefTests(unittest.TestCase):

    def test_predmet_ref_is_valid_veza(self):
        ref = fototeka_views._parse_entity_ref(
            {'tip': 'predmet', 'database': 'mineral', 'broj': ' ПМ 12 '})
        self.assertEqual(ref['tip'], 'predmet')
        self.assertEqual(ref['database_name'], 'mineral')
        self.assertEqual(ref['inventarni_broj'], 'ПМ 12')
        # the parser output must be a valid veza for _insert_veza
        cursor = _FakeCursor()
        fototeka_views._insert_veza(cursor, 5, ref)
        sql, params = cursor.executed[-1]
        self.assertIn('INSERT INTO foto_veza_predmet', sql)
        # migr. 048: uz tekstualni par ide i rezolucija mineral_id (database_name
        # + inventarni broj se ponavljaju u CASE podupitu za FK).
        self.assertEqual(params, (5, 'mineral', 'ПМ 12', 'mineral', 'ПМ 12'))

    def test_teren_projekat_izlozba_refs(self):
        self.assertEqual(
            fototeka_views._parse_entity_ref({'tip': 'teren', 'teren_id': '3'}),
            {'tip': 'teren', 'teren_id': 3})
        self.assertEqual(
            fototeka_views._parse_entity_ref({'tip': 'projekat', 'projekat_id': '4'}),
            {'tip': 'projekat', 'projekat_id': 4})
        self.assertEqual(
            fototeka_views._parse_entity_ref({'tip': 'izlozba', 'izlozba_id': '7'}),
            {'tip': 'izlozba', 'izlozba_id': 7})

    def test_invalid_refs_raise(self):
        for bad in (
            {'tip': 'predmet', 'database': 'nema', 'broj': '1'},
            {'tip': 'predmet', 'database': 'mineral', 'broj': ''},
            {'tip': 'teren', 'teren_id': 'x'},
            {'tip': 'nepostojeci'},
        ):
            with self.assertRaises(ValueError):
                fototeka_views._parse_entity_ref(bad)

    def test_entity_filter_is_table_qualified(self):
        table, cond, params = fototeka_views._entity_photo_filter(
            {'tip': 'predmet', 'database_name': 'mineral', 'inventarni_broj': '9'})
        self.assertEqual(table, 'foto_veza_predmet')
        self.assertIn('foto_veza_predmet.database_name', cond)
        self.assertEqual(params, ('mineral', '9'))
        table, cond, params = fototeka_views._entity_photo_filter(
            {'tip': 'izlozba', 'izlozba_id': 7})
        self.assertIn('foto_veza_izlozba.exhibition_id', cond)
        self.assertEqual(params, (7,))


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

        self.arhiva = tempfile.mkdtemp(prefix='fototeka2-arhiva-')
        self.media = tempfile.mkdtemp(prefix='fototeka2-media-')
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


class ReceptionQueueTests(_RouteTestCase):

    def test_upload_flag_sets_reception_queue(self):
        cursor = self.use_db({
            'INSERT INTO fototeka_intake_pending': {'claim_token': 'tok'},
            'INSERT INTO fotografije': {'id': 9},
        })
        self.login(AUTHOR)
        response = self.post(
            '/fototeka/upload',
            data={'files': (_jpeg_bytes(), 'x.jpg'), 'veza_tip': 'bez',
                  'u_prijemnom_redu': '1'},
            content_type='multipart/form-data', follow_redirects=False,
        )
        self.assertEqual(response.status_code, 302)
        insert = [p for sql, p in cursor.executed if 'INSERT INTO fotografije' in sql][0]
        # u_prijemnom_redu is the second-to-last param (vidljivost is last)
        self.assertIs(insert[-2], True)
        self.assertEqual(insert[-1], 'javno')

    def test_reception_queue_screen_lists_flagged(self):
        self.use_db({'u_prijemnom_redu = TRUE': []})
        self.login(AUTHOR)
        response = self.get('/fototeka/prijemni-red')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Пријемни ред'.encode('utf-8'), response.data)

    def test_skini_sa_reda_clears_flag(self):
        cursor = self.use_db({'FROM fotografije WHERE id': _photo(u_prijemnom_redu=True)})
        self.login(AUTHOR)
        response = self.post('/fototeka/5/skini-sa-reda')
        self.assertEqual(response.status_code, 302)
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertIn('u_prijemnom_redu = FALSE', joined)


class ReverseLinkingTests(_RouteTestCase):

    def _predmet_qs(self):
        return 'tip=predmet&database=mineral&broj=123'

    def test_linked_photos_returns_json(self):
        self.use_db({'JOIN foto_veza_predmet': [_photo(id=5), _photo(id=6)]})
        self.login(AUTHOR)
        response = self.get('/fototeka/api/entitet/fotografije?' + self._predmet_qs())
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['ok'])
        self.assertEqual(len(data['fotografije']), 2)
        self.assertIn('thumb_url', data['fotografije'][0])

    def test_search_candidates_returns_json(self):
        self.use_db({'FROM fotografije f WHERE': [_photo(id=8)]})
        self.login(AUTHOR)
        response = self.get(
            '/fototeka/api/entitet/pretraga?' + self._predmet_qs() + '&q=opis')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()['ok'])

    def test_link_existing_photo_inserts(self):
        cursor = self.use_db({'FROM fotografije WHERE id': _photo()})
        self.login(AUTHOR)
        response = self.post(
            '/fototeka/api/entitet/veza',
            data={'tip': 'predmet', 'database': 'mineral', 'broj': '123',
                  'fotografija_id': '5'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()['ok'])
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertIn('INSERT INTO foto_veza_predmet', joined)

    def test_unlink_deletes(self):
        cursor = self.use_db({'FROM fotografije WHERE id': _photo(),
                              'DELETE FROM foto_veza_predmet': {'id': 1}})
        self.login(AUTHOR)
        response = self.post(
            '/fototeka/api/entitet/veza/ukloni',
            data={'tip': 'predmet', 'database': 'mineral', 'broj': '123',
                  'fotografija_id': '5'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()['ok'])

    def test_link_others_private_is_404_no_insert(self):
        # A4/IDOR: another curator guesses a private photo's id and POSTs a
        # link — it must 404 (no existence leak) and perform no INSERT.
        cursor = self.use_db({'FROM fotografije WHERE id':
                              _photo(vidljivost='privatno')})
        self.login(OTHER)
        response = self.post(
            '/fototeka/api/entitet/veza',
            data={'tip': 'predmet', 'database': 'mineral', 'broj': '123',
                  'fotografija_id': '5'},
        )
        self.assertEqual(response.status_code, 404)
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertNotIn('INSERT INTO foto_veza_predmet', joined)

    def test_unlink_others_private_is_404_no_delete(self):
        cursor = self.use_db({'FROM fotografije WHERE id':
                              _photo(vidljivost='privatno'),
                              'DELETE FROM foto_veza_predmet': {'id': 1}})
        self.login(OTHER)
        response = self.post(
            '/fototeka/api/entitet/veza/ukloni',
            data={'tip': 'predmet', 'database': 'mineral', 'broj': '123',
                  'fotografija_id': '5'},
        )
        self.assertEqual(response.status_code, 404)
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertNotIn('DELETE FROM foto_veza_predmet', joined)

    def test_link_clears_reception_queue(self):
        # A4/D1: linking from the entity side also clears the reception queue,
        # mirroring the photo-page link handler.
        cursor = self.use_db({'FROM fotografije WHERE id':
                              _photo(u_prijemnom_redu=True)})
        self.login(AUTHOR)
        response = self.post(
            '/fototeka/api/entitet/veza',
            data={'tip': 'predmet', 'database': 'mineral', 'broj': '123',
                  'fotografija_id': '5'},
        )
        self.assertEqual(response.status_code, 200)
        joined = ' '.join(sql for sql, _ in cursor.executed)
        self.assertIn('SET u_prijemnom_redu = FALSE', joined)

    def test_bad_entity_ref_is_400(self):
        self.use_db({})
        self.login(AUTHOR)
        response = self.get('/fototeka/api/entitet/fotografije?tip=nepostojeci')
        self.assertEqual(response.status_code, 400)

    def test_link_requires_login(self):
        response = self.post('/fototeka/api/entitet/veza', data={})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])


if __name__ == '__main__':
    unittest.main()
