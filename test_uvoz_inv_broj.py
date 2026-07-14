#!/usr/bin/env python3
"""Tests for flexible inventory-number matching on import (bug: run 71).

'M 028.JPG' produced the number '028' while the collection stores '28', so the
link pointed at a specimen that does not exist — 125 photos were reported as
linked while NOTHING was. Covered here: normalization of every filename shape,
the existence check (a number that is not in the collection is NO LINK, not a
silent dangling link), the explicit report counters, and the retroactive
`povezi-fotografije` command.
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
import povezi_fotografije_cli


class _FakeCursor:
    def __init__(self, canned=None):
        self.canned = dict(canned or {})
        self._pending = None
        self.executed = []
        self.rowcount = 0

    def execute(self, sql, params=None):
        self.executed.append((' '.join(sql.split()), params))
        for needle, rows in self.canned.items():
            if needle in sql:
                self._pending = rows(params) if callable(rows) else rows
                return
        self._pending = []

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
        return False


# ---------------------------------------------------------------------------
# Normalizacija inventarskog broja
# ---------------------------------------------------------------------------

class NormalizacijaTests(unittest.TestCase):

    def test_sve_varijante_daju_isti_broj(self):
        """M 028 == M-28 == M028 == M_28 == 028 == 28 -> '28'"""
        for ulaz in ('M 028', 'M-28', 'M028', 'M_28', 'm 28', '028', '28', ' M  028 '):
            self.assertEqual(fototeka_views.normalizuj_inv_broj(ulaz), '28', ulaz)

    def test_institucijski_i_zbirni_prefiks_zajedno(self):
        self.assertEqual(fototeka_views.normalizuj_inv_broj('PMB-M-01234'), '1234')
        self.assertEqual(fototeka_views.normalizuj_inv_broj('ПМБ-М-28'), '28')

    def test_druge_zbirke(self):
        self.assertEqual(fototeka_views.normalizuj_inv_broj('MET-012'), '12')
        self.assertEqual(fototeka_views.normalizuj_inv_broj('PAL 007'), '7')

    def test_sve_nule_ostaju_nula(self):
        self.assertEqual(fototeka_views.normalizuj_inv_broj('000'), '0')
        self.assertEqual(fototeka_views.normalizuj_inv_broj('M 000'), '0')

    def test_prazno_i_besmisleno(self):
        self.assertEqual(fototeka_views.normalizuj_inv_broj(''), '')
        self.assertEqual(fototeka_views.normalizuj_inv_broj(None), '')

    def test_broj_iz_baze_se_normalizuje_isto(self):
        """Baza je nekonzistentna ('42' ali i 'M4301') — obe strane se poklope."""
        self.assertEqual(fototeka_views.normalizuj_inv_broj('M4301'),
                         fototeka_views.normalizuj_inv_broj('4301'))


class ClassifyTests(unittest.TestCase):

    def test_ime_sa_vodecim_nulama_daje_broj_bez_nula(self):
        rezultat = fototeka_views.classify_import_filename('M 028.JPG', 'mineral')
        self.assertEqual(rezultat['klasa'], 'predmet')
        self.assertEqual(rezultat['veza_meta']['inventarni_broj'], '28')

    def test_razmak_crtica_donja_crta_isto(self):
        for ime in ('M 028.JPG', 'M-028.jpg', 'M_028.jpg', 'M028.jpg'):
            rezultat = fototeka_views.classify_import_filename(ime, 'mineral')
            self.assertEqual(rezultat['veza_meta']['inventarni_broj'], '28', ime)


# ---------------------------------------------------------------------------
# Postojanje predmeta — srž buga
# ---------------------------------------------------------------------------

class NadjiPredmetTests(unittest.TestCase):

    def test_broj_koji_postoji(self):
        cur = _FakeCursor({'FROM minerals': [('28',)]})
        nadjen, status = fototeka_views.nadji_predmet(cur, 'mineral', 'M 028')
        self.assertEqual((nadjen, status), ('28', 'ok'))
        self.assertEqual(cur.executed[0][1], ('28',))   # traži normalizovano

    def test_broj_koji_NE_postoji_je_bez_veze(self):
        """Srž buga: nepostojeći broj više nije tiha veza u prazno."""
        cur = _FakeCursor({'FROM minerals': []})
        nadjen, status = fototeka_views.nadji_predmet(cur, 'mineral', 'M 999999')
        self.assertIsNone(nadjen)
        self.assertEqual(status, 'nema')

    def test_dvosmislen_broj(self):
        cur = _FakeCursor({'FROM minerals': [('28',), ('M28',)]})
        nadjen, status = fototeka_views.nadji_predmet(cur, 'mineral', '28')
        self.assertIsNone(nadjen)
        self.assertEqual(status, 'dvosmisleno')

    def test_nepoznata_zbirka_se_ne_proverava(self):
        cur = _FakeCursor({})
        nadjen, status = fototeka_views.nadji_predmet(cur, 'entomology', 'ENT-5')
        self.assertEqual(status, 'neprovereno')
        self.assertEqual(cur.executed, [])

    def test_vraca_zapis_iz_baze_ne_iz_imena(self):
        """Veza mora da nosi broj onako kako STOJI u bazi ('M4301'), ne iz imena."""
        cur = _FakeCursor({'FROM minerals': [('M4301',)]})
        nadjen, _ = fototeka_views.nadji_predmet(cur, 'mineral', 'M 4301')
        self.assertEqual(nadjen, 'M4301')


# ---------------------------------------------------------------------------
# Retroaktivno povezivanje
# ---------------------------------------------------------------------------

class RetroTests(unittest.TestCase):

    def test_kandidati_upit_hvata_i_veze_u_prazno(self):
        """Veza '001' dok predmet stoji kao '1' je prazna ljuska: aplikacija
        poredi TACAN string, pa je fotografija i dalje nepovezana."""
        cur = _FakeCursor({'FROM fotografije f': [(1, 'M 028.JPG')]})
        kandidati = povezi_fotografije_cli.fotografije_bez_veze(cur)
        self.assertEqual(kandidati, [(1, 'M 028.JPG')])
        sql = cur.executed[0][0]
        self.assertIn('NOT EXISTS', sql)
        self.assertIn('btrim(m.inventory_number) = btrim(v.inventarni_broj)', sql)

    def test_predlozi_samo_za_postojece_predmete(self):
        cur = _FakeCursor({'FROM minerals': lambda p: [('28',)] if p == ('28',) else []})
        predlozi = povezi_fotografije_cli.predlozi_veze(
            cur, [(1, 'M 028.JPG'), (2, 'M 999999.JPG'), (3, 'DSC_1.jpg')], 'mineral')
        self.assertEqual(predlozi, [(1, 'M 028.JPG', '28')])

    def test_primeni_veze_je_idempotentno_i_skida_prijemni_red(self):
        cur = _FakeCursor({'INSERT INTO foto_veza_predmet': [(1,)]})
        povezano, _ = povezi_fotografije_cli.primeni_veze(
            cur, [(1, 'M 028.JPG', '28')], 'mineral')
        self.assertEqual(povezano, 1)
        sqlovi = ' | '.join(sql for sql, _ in cur.executed)
        self.assertIn('ON CONFLICT DO NOTHING', sqlovi)
        self.assertIn('UPDATE fotografije SET u_prijemnom_redu = FALSE', sqlovi)

    def test_drugi_run_ne_pravi_nove_veze(self):
        cur = _FakeCursor({'INSERT INTO foto_veza_predmet': []})   # ON CONFLICT
        povezano, _ = povezi_fotografije_cli.primeni_veze(
            cur, [(1, 'M 028.JPG', '28')], 'mineral')
        self.assertEqual(povezano, 0)

    def test_prazna_ljuska_se_brise(self):
        """Stara veza koja ne pokazuje ni na jedan predmet se cisti."""
        cur = _FakeCursor({'INSERT INTO foto_veza_predmet': [(1,)]})
        povezi_fotografije_cli.primeni_veze(cur, [(1, 'M 028.JPG', '28')], 'mineral')
        sqlovi = [sql for sql, _ in cur.executed]
        self.assertTrue(any(s.startswith('DELETE FROM foto_veza_predmet') for s in sqlovi))

    def test_ne_dira_datoteke_ni_derivate(self):
        """Komanda sme da dira SAMO veze i zastavicu prijemnog reda: nikakav
        DELETE nad fotografijama/poslovima, nikakvo diranje RAW putanje."""
        cur = _FakeCursor({'INSERT INTO foto_veza_predmet': [(1,)]})
        povezi_fotografije_cli.primeni_veze(cur, [(1, 'M 028.JPG', '28')], 'mineral')
        sqlovi = [sql for sql, _ in cur.executed]
        spojeno = ' | '.join(sqlovi)
        for zabranjeno in ('raw_putanja', 'sha256', 'foto_poslovi', 'DROP', 'TRUNCATE'):
            self.assertNotIn(zabranjeno, spojeno)
        # jedini DELETE sme biti nad foto_veza_predmet (prazne ljuske)
        for sql in sqlovi:
            if sql.startswith('DELETE'):
                self.assertTrue(sql.startswith('DELETE FROM foto_veza_predmet'), sql)
        self.assertFalse(any(s.startswith('DELETE FROM fotografije') for s in sqlovi))


if __name__ == '__main__':
    unittest.main()
