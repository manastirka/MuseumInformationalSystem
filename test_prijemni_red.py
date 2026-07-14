#!/usr/bin/env python3
"""Tests: the reception queue is derived from the LINKS, not from a flag.

Production bug: the pre-fix import set `u_prijemnom_redu = FALSE` for every
filename that merely looked like it carried an inventory number, even when the
specimen did not exist. After the retroactive relink, the photos that still had
no link kept flag=FALSE — invisible in the queue, unreachable for a curator.
"""

import os
import unittest
from unittest.mock import patch

os.environ['FLASK_ENV'] = 'testing'
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

import fototeka_views


class BezIjedneVezeSqlTests(unittest.TestCase):

    def test_pokriva_sve_cetiri_vrste_veze(self):
        sql = fototeka_views.bez_ijedne_veze_sql('f')
        for tabela in ('foto_veza_predmet', 'foto_veza_teren',
                       'foto_veza_projekat', 'foto_veza_izlozba'):
            self.assertIn(tabela, sql)
        self.assertEqual(sql.count('NOT EXISTS'), 4)

    def test_ne_oslanja_se_na_zastavicu(self):
        """Zastavica ume da laze — uslov sme da gleda iskljucivo veze."""
        sql = fototeka_views.bez_ijedne_veze_sql('f')
        self.assertNotIn('u_prijemnom_redu', sql)

    def test_alias_se_postuje(self):
        self.assertIn('fotografije.id', fototeka_views.bez_ijedne_veze_sql('fotografije'))


class _FakeCursor:
    def __init__(self, rows=None):
        self.rows = rows or []
        self.executed = []
        self.description = [('id',), ('original_ime',), ('opis',), ('status',),
                            ('autor_email',), ('datum_snimanja',), ('created_at',)]

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


class RenderPrijemniRedTests(unittest.TestCase):

    def _run(self, session_data):
        cur = _FakeCursor([])
        conn = _FakeConnection(cur)
        with patch.object(fototeka_views, 'get_postgres_connection', lambda *a, **k: conn):
            with patch.object(fototeka_views, 'session', session_data):
                with patch.object(fototeka_views, 'render_template', lambda *a, **k: 'ok'):
                    fototeka_views.render_prijemni_red()
        return cur.executed[0]

    def test_upit_gleda_veze_a_ne_zastavicu(self):
        sql, _ = self._run({'user_email': 'admin@nhmbeo.rs', 'user_role': 'admin',
                            'is_admin': True})
        self.assertIn('NOT EXISTS', sql)
        self.assertIn('foto_veza_predmet', sql)
        self.assertNotIn('u_prijemnom_redu = TRUE', sql)   # srz buga
        self.assertIn('sklonjena_sa_reda = FALSE', sql)    # svesno sklonjene se ne vracaju

    def test_kustos_ne_vidi_tudju_privatnu(self):
        sql, params = self._run({'user_email': 'kustos@nhmbeo.rs',
                                 'user_role': 'curator', 'is_admin': False})
        self.assertIn('vidljivost', sql)
        self.assertIn('javno', params)
        self.assertIn('kustos@nhmbeo.rs', params)

    def test_admin_vidi_sve(self):
        sql, params = self._run({'user_email': 'admin@nhmbeo.rs',
                                 'user_role': 'admin', 'is_admin': True})
        self.assertNotIn('vidljivost', sql)
        self.assertEqual(list(params), [])


class SkiniSaRedaTests(unittest.TestCase):

    def test_belezi_svesnu_odluku_a_ne_laz_o_vezi(self):
        cur = _FakeCursor([])
        conn = _FakeConnection(cur)
        photo = {'id': 5, 'autor_email': 'kustos@nhmbeo.rs', 'vidljivost': 'javno'}
        with patch.object(fototeka_views, 'get_postgres_connection', lambda *a, **k: conn):
            with patch.object(fototeka_views, '_fetch_photo', lambda cur, i: photo):
                with patch.object(fototeka_views, 'can_edit_photo', lambda s, p: True):
                    with patch.object(fototeka_views, 'session',
                                      {'user_email': 'kustos@nhmbeo.rs', 'user_role': 'curator'}):
                        with patch.object(fototeka_views, 'flash', lambda *a, **k: None):
                            with patch.object(fototeka_views, 'redirect', lambda *a, **k: 'ok'):
                                with patch.object(fototeka_views, 'url_for', lambda *a, **k: '/'):
                                    fototeka_views.handle_skini_sa_reda(5)

        sql = ' | '.join(s for s, _ in cur.executed)
        self.assertIn('sklonjena_sa_reda = TRUE', sql)


if __name__ == '__main__':
    unittest.main()
