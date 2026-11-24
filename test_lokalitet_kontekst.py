#!/usr/bin/env python3
"""Контекст локалитета из GEE (миграција 066) и растерски слојеви карте.

До базе: CSV свески 12 и 13 → scripts/kontekst_lokaliteta_uvoz.py (dry-run,
--execute <име базе>) → lokalitet_kontekst → картица на детаљу примерка.
До фајла: плочица из MIS_SLOJEVI_PATH кроз /api/map/slojevi/… и прекидач на
карти само за слој који постоји на диску. Миграција 066 се примењује сама.
"""
import importlib.util
import io
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', 'logs/qa_flask_session')

import app as museum_app  # noqa: E402
import lokalitet_kontekst  # noqa: E402
from postgres_service import get_postgres_connection  # noqa: E402

KOREN = Path(__file__).resolve().parent
BAZA = 'https://localhost'
EMAIL = 'kontekst.test@example.invalid'
INV = 'KTXTEST-%'
LOKALITET = 'KTXTEST локалитет'

ZAGLAVLJE_12 = 'id,lat,lon,nadmorska_visina_m,nagib_stepeni,pokrivac_klasa,pokrivac_godina,ogk_list,izvor,datum_izracuna'
ZAGLAVLJE_13 = ('id,suma_2000_pct,gubitak_sume_ha,gubitak_sume_pct,gubitak_od,gubitak_do,dw_udeli,dw_godina,'
                'bio_izvor,bio_datum_izracuna')
IZVOR_12 = 'COPERNICUS/DEM/GLO30; GOOGLE/DYNAMICWORLD/V1 2024 (mode); OGK nominalna mreža'
UDELI = '"{""trees"": 61.5, ""crops"": 20.0, ""built"": 18.5}"'


def _ucitaj_uvoz():
    spec = importlib.util.spec_from_file_location('kontekst_lokaliteta_uvoz',
                                                  KOREN / 'scripts' / 'kontekst_lokaliteta_uvoz.py')
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


uvoz = _ucitaj_uvoz()


def _izvrsi(sql, params=()):
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            red = cur.fetchone() if cur.description else None
        conn.commit()
    return red


def _upit(sql, params=()):
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()


def _osiguraj_066():
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT to_regclass('public.lokalitet_kontekst')")
            if cur.fetchone()[0] is None:
                cur.execute((KOREN / 'migration' / '066_lokalitet_kontekst.sql').read_text(encoding='utf-8'))
        conn.commit()


def _ocisti():
    _izvrsi("DELETE FROM lokalitet_kontekst WHERE (vrsta = 'mineral' AND objekat_id IN "
            "(SELECT id FROM minerals WHERE inventory_number LIKE %s)) OR (vrsta = 'lokalitet' AND objekat_id IN "
            "(SELECT id FROM localities WHERE name = %s))", (INV, LOKALITET))
    _izvrsi('DELETE FROM minerals WHERE inventory_number LIKE %s', (INV,))
    _izvrsi('DELETE FROM localities WHERE name = %s', (LOKALITET,))


def _mineral(inv, lokalitet='Тестни локалитет'):
    return _izvrsi('INSERT INTO minerals (inventory_number, item_name, card_locality) VALUES (%s, %s, %s) '
                   'RETURNING id', (inv, 'Кварц тестни', lokalitet))[0]


def _ime_baze():
    return _upit('SELECT current_database()')[0][0]


class CistaValidacijaTest(unittest.TestCase):
    def test_csv_12_i_13_prepoznaje_kolone(self):
        kolone, redovi = lokalitet_kontekst.ucitaj_csv(ZAGLAVLJE_12 + '\n1,44.07,22.1,380.4,7.5,6,2024,L34-141,x,2026-11-24\n')
        self.assertEqual(kolone, lokalitet_kontekst.KOLONE_12)
        po_id, greske = lokalitet_kontekst.validiraj_redove(kolone, redovi)
        self.assertEqual(greske, [])
        self.assertEqual(po_id[1]['pokrivac_klasa'], 6)
        self.assertEqual(po_id[1]['datum_izracuna'].isoformat(), '2026-11-24')
        kolone, redovi = lokalitet_kontekst.ucitaj_csv(
            '﻿' + ZAGLAVLJE_13 + f'\n1,40.2,3.25,12.5,2001,2024,{UDELI},2024,UMD,2026-11-24\n')
        self.assertEqual(kolone, lokalitet_kontekst.KOLONE_13)
        po_id, greske = lokalitet_kontekst.validiraj_redove(kolone, redovi)
        self.assertEqual(greske, [])
        self.assertEqual(po_id[1]['dw_udeli'], {'trees': 61.5, 'crops': 20.0, 'built': 18.5})

    def test_prazno_je_null_a_ne_nula(self):
        kolone, redovi = lokalitet_kontekst.ucitaj_csv(ZAGLAVLJE_12 + '\n1,44.07,22.1,,,,,,,\n')
        po_id, greske = lokalitet_kontekst.validiraj_redove(kolone, redovi)
        self.assertEqual(greske, [])
        self.assertIsNone(po_id[1]['nadmorska_visina_m'])
        self.assertIsNone(po_id[1]['pokrivac_klasa'])

    def test_lose_vrednosti_su_greske(self):
        tekst = (ZAGLAVLJE_12 + '\n'
                 '1,95,22.1,,,,,,,\n'             # lat ван опсега
                 '2,44,22,,,9,,,,\n'              # класа DW 0–8
                 '3,44,22,,,,,K34-3,,\n'          # лист без водеће нуле
                 '3,44,22,,,,,,,\n'               # понављен id
                 'x,44,22,,,,,,,\n'               # id није број
                 '4,44,22,,,,,,,24.11.2026\n'     # датум није ISO
                 '5,,22,,,,,,,\n')                # lat обавезан
        po_id, greske = lokalitet_kontekst.validiraj_redove(*lokalitet_kontekst.ucitaj_csv(tekst))
        spojeno = '\n'.join(greske)
        for deo in ('lat: 95', 'pokrivac_klasa', 'ogk_list', 'се понавља', 'id „x“', 'ISO датум', 'обавезни'):
            self.assertIn(deo, spojeno)

    def test_dw_udeli_klase_i_zbir(self):
        def greske(udeli):
            tekst = ZAGLAVLJE_13 + f'\n1,,,,,,{udeli},,,\n'
            return lokalitet_kontekst.validiraj_redove(*lokalitet_kontekst.ucitaj_csv(tekst))[1]
        self.assertEqual(greske(UDELI), [])
        self.assertIn('непозната класа', greske('"{""forest"": 100}"')[0])
        self.assertIn('збир', greske('"{""trees"": 50}"')[0])
        self.assertIn('JSON', greske('nije-json')[0])

    def test_zaglavlje_bez_id_ili_kolona(self):
        with self.assertRaises(ValueError):
            lokalitet_kontekst.ucitaj_csv('lat,lon\n44,22\n')
        with self.assertRaises(ValueError):
            lokalitet_kontekst.ucitaj_csv('id,lat,lon_x\n1,44,22\n')
        with self.assertRaises(ValueError):
            lokalitet_kontekst.ucitaj_csv('id,lat\n1,44\n')

    def test_naziv_lista_bez_obzira_na_nulu(self):
        self.assertEqual(lokalitet_kontekst.naziv_lista('K34-03'), lokalitet_kontekst.naziv_lista('K34-3'))
        self.assertEqual(lokalitet_kontekst.naziv_lista('L34-141'), 'Bor')
        self.assertIsNone(lokalitet_kontekst.naziv_lista('K34-99'))


class UvozDoBazeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _osiguraj_066()

    def setUp(self):
        _ocisti()
        self.addCleanup(_ocisti)
        self.dir = Path(tempfile.mkdtemp(prefix='ktxtest-'))
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.mid = _mineral('KTXTEST-1')
        self.client = museum_app.app.test_client()

    def _csv(self, ime, tekst):
        putanja = self.dir / ime
        putanja.write_text(tekst, encoding='utf-8')
        return str(putanja)

    def _uvoz(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            kod = uvoz.main(list(argv))
        return kod, out.getvalue(), err.getvalue()

    def _red(self, vrsta='mineral', oid=None):
        redovi = _upit('SELECT nadmorska_visina_m, pokrivac_klasa, ogk_list, suma_2000_pct, dw_udeli, uvezao_email '
                       'FROM lokalitet_kontekst WHERE vrsta = %s AND objekat_id = %s', (vrsta, oid or self.mid))
        return redovi[0] if redovi else None

    def _csv12(self, visina='380.4', oid=None):
        return self._csv('12.csv', ZAGLAVLJE_12 + f'\n{oid or self.mid},44.07,22.1,{visina},7.5,6,2024,L34-141,'
                         f'"{IZVOR_12}",2026-11-24\n')

    def _prijava(self):
        with self.client.session_transaction() as s:
            s.update({'user_id': 1, 'user_email': EMAIL, 'user_name': 'Тест', 'user_role': 'admin',
                      'is_admin': True})

    def test_dry_run_ne_upisuje(self):
        kod, out, err = self._uvoz('--fajl', self._csv12())
        self.assertEqual(kod, 0, err)
        self.assertIn('(+1 ~0 =0)', out)
        self.assertIn('DRY-RUN', out)
        self.assertIsNone(self._red())

    def test_execute_trazi_doslovno_ime_baze(self):
        kod, _, err = self._uvoz('--fajl', self._csv12(), '--execute', 'pogresna_baza')
        self.assertEqual(kod, 2)
        self.assertIn('дословно име базе', err)
        self.assertIsNone(self._red())

    def test_12_pa_13_dopunjuje_a_ne_brise(self):
        kod, out, err = self._uvoz('--fajl', self._csv12(), '--execute', _ime_baze(), '--autor', EMAIL)
        self.assertEqual(kod, 0, err)
        self.assertEqual(self._red()[:3], (380.4, 6, 'L34-141'))
        csv13 = self._csv('13.csv', ZAGLAVLJE_13 + f'\n{self.mid},40.2,3.25,12.5,2001,2024,{UDELI},2024,UMD,2026-11-24\n')
        kod, out, err = self._uvoz('--fajl', csv13, '--execute', _ime_baze())
        self.assertEqual(kod, 0, err)
        self.assertIn('(+0 ~1 =0)', out)
        visina, klasa, lista, suma, udeli, autor = self._red()
        self.assertEqual((klasa, lista, autor), (6, 'L34-141', EMAIL), 'увоз 13 не сме да дира поља свеске 12')
        self.assertAlmostEqual(suma, 40.2, places=4)
        self.assertEqual(udeli, {'trees': 61.5, 'crops': 20.0, 'built': 18.5})
        # исти фајл поново — ништа за промену
        kod, out, _ = self._uvoz('--fajl', csv13)
        self.assertIn('(+0 ~0 =1)', out)
        kod, out, _ = self._uvoz('--fajl', self._csv12())
        self.assertIn('(+0 ~0 =1)', out)
        kod, out, _ = self._uvoz('--fajl', self._csv12(visina='381'))
        self.assertIn('(+0 ~1 =0)', out)

    def test_13_bez_reda_iz_12_je_greska(self):
        csv13 = self._csv('13.csv', ZAGLAVLJE_13 + f'\n{self.mid},40.2,,,,,,,,\n')
        kod, _, err = self._uvoz('--fajl', csv13, '--execute', _ime_baze())
        self.assertEqual(kod, 1)
        self.assertIn('прво увези CSV свеске 12', err)
        self.assertIsNone(self._red())

    def test_nepostojeci_objekat_rusi_ceo_uvoz(self):
        nepostojeci = _upit('SELECT COALESCE(MAX(id), 0) + 1000 FROM minerals')[0][0]
        tekst = (ZAGLAVLJE_12 + f'\n{self.mid},44.07,22.1,380,7.5,6,2024,L34-141,x,2026-11-24'
                 f'\n{nepostojeci},44.07,22.1,380,7.5,6,2024,L34-141,x,2026-11-24\n')
        kod, _, err = self._uvoz('--fajl', self._csv('12.csv', tekst), '--execute', _ime_baze())
        self.assertEqual(kod, 1)
        self.assertIn(f'id {nepostojeci}: нема га у minerals', err)
        self.assertIsNone(self._red(), 'грешка у једном реду — ништа се не уписује')

    def test_kartica_na_detalju_primerka(self):
        self._prijava()
        prazno = self.client.get(f'/admin/mineral_detail/{self.mid}', base_url=BAZA)
        self.assertEqual(prazno.status_code, 200)
        self.assertNotIn('id="kontekstLokaliteta"', prazno.get_data(as_text=True))
        self._uvoz('--fajl', self._csv12(), '--execute', _ime_baze())
        html = self.client.get(f'/admin/mineral_detail/{self.mid}', base_url=BAZA).get_data(as_text=True)
        self.assertIn('id="kontekstLokaliteta"', html)
        for deo in ('380 m', '7.5°', 'Изграђено', 'L34-141 Bor', '24.11.2026.', 'Copernicus DEM GLO-30'):
            self.assertIn(deo, html)
        self.assertNotIn('Global Forest Change', html, 'без података свеске 13 нема ни атрибуције Hansen-а')

    def test_lokalitet_iz_sifarnika_vazi_za_primerak_sa_tim_lokalitetom(self):
        lok_id = _izvrsi("INSERT INTO localities (name, source) VALUES (%s, 'rucno') RETURNING id", (LOKALITET,))[0]
        mid2 = _mineral('KTXTEST-2', lokalitet=LOKALITET)
        kod, _, err = self._uvoz('--fajl', self._csv12(oid=lok_id), '--vrsta', 'lokalitet', '--execute', _ime_baze())
        self.assertEqual(kod, 0, err)
        self._prijava()
        html = self.client.get(f'/admin/mineral_detail/{mid2}', base_url=BAZA).get_data(as_text=True)
        self.assertIn('id="kontekstLokaliteta"', html)
        self.assertIn(f'за локалитет „{LOKALITET}“ из шифарника', html)
        html = self.client.get(f'/admin/mineral_detail/{self.mid}', base_url=BAZA).get_data(as_text=True)
        self.assertNotIn('id="kontekstLokaliteta"', html, 'други локалитет — без картице')


# Најмањи исправан PNG (1×1, провидан).
PNG = bytes.fromhex('89504e470d0a1a0a0000000d4948445200000001000000010806000000'
                    '1f15c4890000000d49444154789c6360000002000154a24f5d0000000049454e44ae426082')


class SlojeviKarteTest(unittest.TestCase):
    def setUp(self):
        self.koren = Path(tempfile.mkdtemp(prefix='ktxtest-slojevi-'))
        self.addCleanup(shutil.rmtree, self.koren, True)
        okruzenje = mock.patch.dict(os.environ, {'MIS_SLOJEVI_PATH': str(self.koren)})
        okruzenje.start()
        self.addCleanup(okruzenje.stop)
        self.client = museum_app.app.test_client()

    def _prijava(self):
        with self.client.session_transaction() as s:
            s.update({'user_id': 990610, 'user_email': EMAIL, 'user_name': 'Тест', 'user_role': 'admin',
                      'user_department': 'Природњачки музеј', 'is_admin': True})

    def _plocica(self, sloj='reljef', z=8, x=142, y=93):
        putanja = self.koren / sloj / str(z) / str(x)
        putanja.mkdir(parents=True, exist_ok=True)
        (putanja / f'{y}.png').write_bytes(PNG)

    def test_plocica_se_sluzi_samo_prijavljenom(self):
        self._plocica()
        anonimno = self.client.get('/api/map/slojevi/reljef/8/142/93.png', base_url=BAZA)
        self.assertNotEqual(anonimno.status_code, 200)
        self._prijava()
        odgovor = self.client.get('/api/map/slojevi/reljef/8/142/93.png', base_url=BAZA)
        self.assertEqual(odgovor.status_code, 200)
        self.assertEqual(odgovor.mimetype, 'image/png')
        self.assertEqual(odgovor.get_data(), PNG)
        ponovo = self.client.get('/api/map/slojevi/reljef/8/142/93.png', base_url=BAZA,
                                 headers={'If-None-Match': odgovor.headers['ETag']})
        self.assertEqual(ponovo.status_code, 304)

    def test_nepostojeca_ili_nedozvoljena_plocica_je_404(self):
        self._plocica()
        self._prijava()
        for url in ('/api/map/slojevi/reljef/8/142/94.png',      # нема фајла
                    '/api/map/slojevi/nepoznat/8/142/93.png',    # непознат слој
                    '/api/map/slojevi/reljef/8/256/93.png',      # x ван мреже зума 8
                    '/api/map/slojevi/..%2Freljef/8/142/93.png'):
            self.assertEqual(self.client.get(url, base_url=BAZA).status_code, 404, url)

    def test_prekidac_na_karti_samo_za_sloj_na_disku(self):
        self._prijava()
        html = self.client.get('/admin/maps', base_url=BAZA).get_data(as_text=True)
        self.assertNotIn('data-mis-sloj=', html)
        self._plocica(z=6, x=35, y=23)
        self._plocica(z=12)
        html = self.client.get('/admin/maps', base_url=BAZA).get_data(as_text=True)
        self.assertIn('data-mis-sloj="reljef" data-min-zoom="6" data-max-zoom="12"', html)
        self.assertIn('Copernicus DEM GLO-30', html)
        self.assertNotIn('data-mis-sloj="pokrivac-2024"', html)
        self._plocica(sloj='pokrivac-2024')
        html = self.client.get('/admin/maps', base_url=BAZA).get_data(as_text=True)
        self.assertIn('data-mis-sloj-legenda="pokrivac-2024"', html)
        self.assertIn('data-boja="#419bdf"', html)


if __name__ == '__main__':
    unittest.main()
