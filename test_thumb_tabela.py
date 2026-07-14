#!/usr/bin/env python3
"""Tests for the specimen thumbnail column in the collection table.

Covers: the batch (no N+1) main-photo lookup, the server-side visibility filter
(another curator's private photo must not surface in the table), specimens
without a photo (placeholder, never an empty cell), the 'main photo' rule
(oldest = lowest id, same as the detail page) and resilience (a Фототека
failure must not break the specimen list).
"""

import os
import unittest
from unittest.mock import patch

os.environ['FLASK_ENV'] = 'testing'
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

import collection_management_views
import fototeka_views


ADMIN = {'user_id': 1, 'user_email': 'admin@nhmbeo.rs', 'user_role': 'admin',
         'is_admin': True}
KUSTOS = {'user_id': 3, 'user_email': 'kustos@nhmbeo.rs', 'user_role': 'curator',
          'is_admin': False}


class _FakeCursor:
    def __init__(self, rows=None):
        self.rows = rows or []
        self.executed = []

    def execute(self, sql, params=None):
        self.executed.append((' '.join(sql.split()), params))

    def fetchall(self):
        return self.rows

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


def _patch_db(testcase, rows):
    cur = _FakeCursor(rows)
    conn = _FakeConnection(cur)
    patcher = patch.object(
        fototeka_views, 'get_postgres_connection', lambda *a, **k: conn)
    patcher.start()
    testcase.addCleanup(patcher.stop)
    return cur


class BatchLookupTests(unittest.TestCase):

    def test_one_query_for_the_whole_page(self):
        """Bez N+1: jedna strana = jedan upit, bez obzira na broj predmeta."""
        cur = _patch_db(self, [('101', 7), ('102', 9)])

        mapa = fototeka_views.glavne_fotografije_predmeta(
            ADMIN, 'mineral', ['101', '102', '103'])

        self.assertEqual(mapa, {'101': 7, '102': 9})
        self.assertEqual(len(cur.executed), 1)

    def test_main_photo_is_the_oldest(self):
        """'Glavna' = najstarija (najmanji id) — ista konvencija kao detalj."""
        cur = _patch_db(self, [('101', 7)])
        fototeka_views.glavne_fotografije_predmeta(ADMIN, 'mineral', ['101'])
        sql = cur.executed[0][0]
        self.assertIn('DISTINCT ON (v.inventarni_broj)', sql)
        self.assertIn('ORDER BY v.inventarni_broj, f.id', sql)
        self.assertNotIn('f.id DESC', sql)

    def test_only_ready_and_not_deleted_photos(self):
        cur = _patch_db(self, [])
        fototeka_views.glavne_fotografije_predmeta(ADMIN, 'mineral', ['101'])
        sql = cur.executed[0][0]
        self.assertIn('f.obrisana = FALSE', sql)
        self.assertIn("f.status = 'spremna'", sql)

    def test_empty_input_makes_no_query(self):
        cur = _patch_db(self, [])
        self.assertEqual(fototeka_views.glavne_fotografije_predmeta(ADMIN, 'mineral', []), {})
        self.assertEqual(
            fototeka_views.glavne_fotografije_predmeta(ADMIN, 'mineral', [None, '  ']), {})
        self.assertEqual(cur.executed, [])


class VisibilityTests(unittest.TestCase):

    def test_curator_query_filters_private_photos(self):
        """Tuđa privatna fotografija ne sme da procuri u tabelu zbirke."""
        cur = _patch_db(self, [])

        fototeka_views.glavne_fotografije_predmeta(KUSTOS, 'mineral', ['101'])

        sql, params = cur.executed[0]
        self.assertIn("f.vidljivost = %s OR LOWER(f.autor_email) = %s", sql)
        self.assertIn('javno', params)
        self.assertIn('kustos@nhmbeo.rs', params)

    def test_admin_sees_everything(self):
        cur = _patch_db(self, [])
        fototeka_views.glavne_fotografije_predmeta(ADMIN, 'mineral', ['101'])
        sql, params = cur.executed[0]
        self.assertNotIn('vidljivost', sql)
        self.assertNotIn('javno', params)


class AttachToRowsTests(unittest.TestCase):

    def test_specimen_without_photo_gets_none(self):
        """Predmet bez fotografije -> foto_id None (šablon crta placeholder)."""
        minerals = [
            {'id': 1, 'inventarni_broj': '101'},
            {'id': 2, 'inventarni_broj': '102'},   # nema fotografiju
            {'id': 3, 'inventarni_broj': None},    # nema ni inv. broj
        ]
        with patch.object(fototeka_views, 'glavne_fotografije_predmeta',
                          lambda *a, **k: {'101': 7}):
            with patch.object(collection_management_views, 'session', ADMIN):
                collection_management_views._priloži_foto_id(minerals)

        self.assertEqual(minerals[0]['foto_id'], 7)
        self.assertIsNone(minerals[1]['foto_id'])
        self.assertIsNone(minerals[2]['foto_id'])

    def test_fototeka_failure_does_not_break_the_list(self):
        """Ako Фototeka pukne, lista predmeta se i dalje renderuje."""
        minerals = [{'id': 1, 'inventarni_broj': '101'}]

        def eksplodira(*a, **k):
            raise RuntimeError('baza nedostupna')

        with patch.object(fototeka_views, 'glavne_fotografije_predmeta', eksplodira):
            with patch.object(collection_management_views, 'session', ADMIN):
                collection_management_views._priloži_foto_id(minerals)  # ne sme da baci

        self.assertNotIn('foto_id', minerals[0])  # red preživeo, bez slike

    def test_empty_page_is_noop(self):
        with patch.object(collection_management_views, 'session', ADMIN):
            collection_management_views._priloži_foto_id([])  # bez izuzetka


if __name__ == '__main__':
    unittest.main()


class DetaljKarticeTests(unittest.TestCase):
    """BUG 2: kartica predmeta je gledala SAMO staru images putanju, pa je
    predmet sa fototeka fotografijom prikazivao placeholder."""

    def test_detalj_dobija_foto_id(self):
        mineral = {'id': 11, 'inventarni_broj': '42'}
        with patch.object(fototeka_views, 'glavne_fotografije_predmeta',
                          lambda *a, **k: {'42': 13}):
            with patch.object(collection_management_views, 'session', ADMIN):
                collection_management_views._priloži_foto_id([mineral])
        self.assertEqual(mineral['foto_id'], 13)

    def test_detalj_bez_fototeke_ostaje_na_legacy(self):
        mineral = {'id': 11, 'inventarni_broj': '42'}
        with patch.object(fototeka_views, 'glavne_fotografije_predmeta',
                          lambda *a, **k: {}):
            with patch.object(collection_management_views, 'session', ADMIN):
                collection_management_views._priloži_foto_id([mineral])
        self.assertIsNone(mineral['foto_id'])
