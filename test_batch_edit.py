#!/usr/bin/env python3
"""Tests for group editing of selected photos (batch edit).

Covers: per-item server-side permission (a curator may edit only their own +
public photos, an admin everything), the three tag actions (add / replace /
remove), description set vs append, visibility, linking many photos at once,
author change (admin only), skipping without failing, and the audit trail.
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


ADMIN = {'user_id': 1, 'user_email': 'admin@nhmbeo.rs', 'user_role': 'admin',
         'is_admin': True, 'is_department_head': False}
KUSTOS = {'user_id': 3, 'user_email': 'kustos@nhmbeo.rs', 'user_role': 'curator',
          'is_admin': False, 'is_department_head': False}


class _FakeCursor:
    def __init__(self, tagovi=None):
        self.executed = []
        self._tagovi = tagovi or []

    def execute(self, sql, params=None):
        self.executed.append((' '.join(sql.split()), params))

    def fetchall(self):
        return [(t,) for t in self._tagovi]

    def fetchone(self):
        return None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


def _foto(id=1, autor='kustos@nhmbeo.rs', vidljivost='javno', opis=''):
    return {'id': id, 'autor_email': autor, 'vidljivost': vidljivost, 'opis': opis}


# ---------------------------------------------------------------------------
# Prava — po stavci, na serveru
# ---------------------------------------------------------------------------

class PravaTests(unittest.TestCase):

    def test_kustos_sme_svoju(self):
        self.assertTrue(fototeka_views.can_edit_photo(KUSTOS, _foto(autor='kustos@nhmbeo.rs')))

    def test_kustos_ne_sme_tudju_privatnu(self):
        self.assertFalse(fototeka_views.can_edit_photo(
            KUSTOS, _foto(autor='drugi@nhmbeo.rs', vidljivost='privatno')))

    def test_admin_sme_sve(self):
        self.assertTrue(fototeka_views.can_edit_photo(
            ADMIN, _foto(autor='drugi@nhmbeo.rs', vidljivost='privatno')))


# ---------------------------------------------------------------------------
# Tagovi: dodaj / zameni / ukloni
# ---------------------------------------------------------------------------

class TagoviTests(unittest.TestCase):

    def _primeni(self, akcija, novi, postojeci):
        cur = _FakeCursor(tagovi=postojeci)
        upisani = []
        with patch.object(fototeka_views, '_replace_tags',
                          lambda c, i, tags: upisani.append(list(tags))):
            izmene = fototeka_views.primeni_batch_izmenu(
                cur, ADMIN, _foto(), {'tag_akcija': akcija, 'tagovi': novi})
        return (upisani[0] if upisani else None), izmene

    def test_dodaj_cuva_postojece(self):
        rezultat, izmene = self._primeni('dodaj', ['макро'], ['кварц'])
        self.assertEqual(sorted(rezultat), sorted(['кварц', 'макро']))
        self.assertEqual(izmene['tagovi']['akcija'], 'dodaj')

    def test_dodaj_ne_duplira(self):
        rezultat, izmene = self._primeni('dodaj', ['Кварц'], ['кварц'])
        self.assertIsNone(rezultat)      # ništa se nije promenilo
        self.assertEqual(izmene, {})

    def test_zameni_brise_stare(self):
        rezultat, _ = self._primeni('zameni', ['нов'], ['кварц', 'макро'])
        self.assertEqual(rezultat, ['нов'])

    def test_ukloni_samo_navedene(self):
        rezultat, _ = self._primeni('ukloni', ['макро'], ['кварц', 'макро'])
        self.assertEqual(rezultat, ['кварц'])

    def test_bez_akcije_ne_dira_tagove(self):
        rezultat, izmene = self._primeni(None, ['x'], ['кварц'])
        self.assertIsNone(rezultat)
        self.assertEqual(izmene, {})


# ---------------------------------------------------------------------------
# Opis, vidljivost, veza, autor
# ---------------------------------------------------------------------------

class OstaleAkcijeTests(unittest.TestCase):

    def test_opis_postavi_prepisuje(self):
        cur = _FakeCursor()
        izmene = fototeka_views.primeni_batch_izmenu(
            cur, ADMIN, _foto(opis='stari'), {'opis_akcija': 'postavi', 'opis': 'novi'})
        self.assertEqual(izmene['opis']['posle'], 'novi')

    def test_opis_dopisi_zadrzava_stari(self):
        cur = _FakeCursor()
        izmene = fototeka_views.primeni_batch_izmenu(
            cur, ADMIN, _foto(opis='stari'), {'opis_akcija': 'dopisi', 'opis': 'dodatak'})
        self.assertEqual(izmene['opis']['posle'], 'stari\ndodatak')

    def test_vidljivost_se_menja(self):
        cur = _FakeCursor()
        izmene = fototeka_views.primeni_batch_izmenu(
            cur, ADMIN, _foto(vidljivost='javno'), {'vidljivost': 'privatno'})
        self.assertEqual(izmene['vidljivost']['posle'], 'privatno')

    def test_veza_se_dodaje(self):
        cur = _FakeCursor()
        veza = {'tip': 'predmet', 'database_name': 'mineral', 'inventarni_broj': '28'}
        pozvano = []
        with patch.object(fototeka_views, '_insert_veza',
                          lambda c, i, v: pozvano.append((i, v))):
            izmene = fototeka_views.primeni_batch_izmenu(cur, ADMIN, _foto(id=9), {'veza': veza})
        self.assertEqual(pozvano, [(9, veza)])
        self.assertEqual(izmene['veza']['tip'], 'predmet')

    def test_autora_menja_samo_admin(self):
        cur = _FakeCursor()
        izmene = fototeka_views.primeni_batch_izmenu(
            cur, ADMIN, _foto(), {'autor_email': 'novi@nhmbeo.rs'})
        self.assertEqual(izmene['autor_email']['posle'], 'novi@nhmbeo.rs')

    def test_kustos_ne_moze_da_menja_autora(self):
        cur = _FakeCursor()
        izmene = fototeka_views.primeni_batch_izmenu(
            cur, KUSTOS, _foto(), {'autor_email': 'novi@nhmbeo.rs'})
        self.assertNotIn('autor_email', izmene)
        self.assertNotIn('UPDATE fotografije SET autor_email',
                         ' | '.join(s for s, _ in cur.executed))


# ---------------------------------------------------------------------------
# Preskakanje bez pada + audit
# ---------------------------------------------------------------------------

class PreskakanjeTests(unittest.TestCase):

    def test_audit_belezi_izmenu(self):
        cur = _FakeCursor()
        fototeka_views._audit_upisi(cur, 5, 'BATCH_EDIT', {'opis': {'posle': 'x'}}, 3)
        sql, params = cur.executed[0]
        self.assertIn('INSERT INTO audit_log', sql)
        self.assertIn("'fotografije'", sql)
        self.assertEqual(params[0], 5)
        self.assertEqual(params[1], 'BATCH_EDIT')
        self.assertEqual(params[3], 3)          # performed_by

    def test_nedozvoljena_se_preskace_a_dozvoljena_menja(self):
        """Izbor sa tuđom privatnom fotografijom NE sme da obori ceo posao."""
        fotografije = {
            1: _foto(id=1, autor='kustos@nhmbeo.rs'),                       # sme
            2: _foto(id=2, autor='drugi@nhmbeo.rs', vidljivost='privatno'), # NE sme
            3: _foto(id=3, autor='kustos@nhmbeo.rs'),                       # sme
        }
        primenjeno = []

        class _Cur(_FakeCursor):
            pass

        cur = _Cur()
        conn = type('C', (), {'cursor': lambda self: cur, 'commit': lambda self: None,
                              '__enter__': lambda self: self, '__exit__': lambda *a: False})()

        poruke = []
        with patch.object(fototeka_views, 'get_postgres_connection', lambda *a, **k: conn), \
             patch.object(fototeka_views, '_fetch_photo', lambda c, i: fotografije.get(i)), \
             patch.object(fototeka_views, '_parse_veza_form', lambda f, c: None), \
             patch.object(fototeka_views, 'primeni_batch_izmenu',
                          lambda c, s, p, a: primenjeno.append(p['id']) or {'opis': {'posle': 'x'}}), \
             patch.object(fototeka_views, '_audit_upisi', lambda *a: None), \
             patch.object(fototeka_views, 'flash', lambda poruka, kat: poruke.append((kat, poruka))), \
             patch.object(fototeka_views, 'redirect', lambda *a, **k: 'ok'), \
             patch.object(fototeka_views, 'url_for', lambda *a, **k: '/'), \
             patch.object(fototeka_views, 'session', KUSTOS), \
             patch.object(fototeka_views, 'request', type('R', (), {
                 'form': type('F', (), {
                     'getlist': lambda self, k: ['1', '2', '3'],
                     'get': lambda self, k, d=None: d,
                 })(),
                 'referrer': None,
             })()):
            fototeka_views.handle_batch_edit()

        self.assertEqual(primenjeno, [1, 3])            # tuđa privatna preskočena
        tekst = ' '.join(p for _, p in poruke)
        self.assertIn('2', tekst)                        # izmenjene 2
        self.assertTrue(any('Прескочено' in p for _, p in poruke))


if __name__ == '__main__':
    unittest.main()
