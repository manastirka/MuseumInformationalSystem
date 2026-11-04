#!/usr/bin/env python3
"""Интерактивни уџбеник — до базе (`museum_system_test`).

Миграција 060 се примењује сама ако табела `udzbenik` не постоји (образац из
test_foto_veza_mineral_fk.py); тест брише само своје редове (zbirka
'minerali' из примера и 'udztest-*', минерал UDZTEST-*, фотографије
udztest-*).
"""
import importlib.util
import io
import json
import os
import re
import subprocess
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

import psycopg  # noqa: E402
import requests  # noqa: E402

import app as museum_app  # noqa: E402
import local_rruff_data  # noqa: E402
import pretraga  # noqa: E402
import scisearch_klijent  # noqa: E402
import udzbenik  # noqa: E402
from postgres_service import get_postgres_connection  # noqa: E402

KOREN = Path(__file__).resolve().parent
PRIMER = KOREN / 'udzbenik' / 'primer-minerali.json'
PRIMERI_ILUSTRACIJA = KOREN / 'udzbenik' / 'primeri-ilustracija.json'
ZBIRKA_ILUSTRACIJE = 'udztest-ilustracije'
BUNDLE_FAJLOVI = ('README.md', 'udzbenik.js', 'udzbenik-three.js', 'udzbenik-dijagrami.js', 'udzbenik.css',
                  'VERZIJA.txt')
if not PRIMER.exists():
    PRIMER = Path('/tmp/udzbenik/primer-minerali.json')
BAZA = 'https://localhost'
EMAIL = 'udztest@example.invalid'
TABELE = ('udzbenik', 'udzbenik_poglavlje', 'udzbenik_lekcija', 'udzbenik_lekcija_verzija', 'udzbenik_napredak')


def _ucitaj_uvoz():
    spec = importlib.util.spec_from_file_location('udzbenik_uvoz', KOREN / 'scripts' / 'udzbenik_uvoz.py')
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


uvoz = _ucitaj_uvoz()


def _osiguraj_semu():
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT to_regclass('public.udzbenik')")
            if cur.fetchone()[0] is None:
                cur.execute((KOREN / 'migration' / '060_udzbenik.sql').read_text(encoding='utf-8'))
        conn.commit()


def _ocisti():
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM udzbenik WHERE zbirka = 'minerali' OR zbirka LIKE 'udztest-%%'")
            cur.execute("DELETE FROM fotografije WHERE raw_putanja LIKE 'udztest/%%'")
            cur.execute("DELETE FROM minerals WHERE inventory_number LIKE 'UDZTEST-%%'")
        conn.commit()


def _brojevi():
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            out = {}
            for t in TABELE:
                cur.execute(f'SELECT COUNT(*) FROM {t}')
                out[t] = cur.fetchone()[0]
            return out


def _upit(sql, params=()):
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()


def _izvrsi(sql, params=()):
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
        conn.commit()


def _pokreni_uvoz(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        kod = uvoz.main(list(argv))
    return kod, out.getvalue(), err.getvalue()


def _uvezi_primer():
    kod, out, err = _pokreni_uvoz('--fajl', str(PRIMER), '--execute', 'mis_db', '--autor', EMAIL)
    assert kod == 0, err + out
    return out


def _primer_sa_izmenom(izmeni):
    podaci = json.loads(PRIMER.read_text(encoding='utf-8'))
    izmeni(podaci)
    f = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8')
    json.dump(podaci, f, ensure_ascii=False)
    f.close()
    return f.name


def _ubaci_mineral(inv='UDZTEST-1'):
    return _upit("INSERT INTO minerals (inventory_number, item_name, card_locality) VALUES (%s, %s, %s) RETURNING id",
                 (inv, 'Тестни пирит', 'Бор'))[0][0]


def _ubaci_fotografiju(sha, vidljivost='javno', autor=EMAIL):
    return _upit(
        """INSERT INTO fotografije (sha256, raw_putanja, original_ime, autor_email, poreklo, status,
                                    vidljivost, width, height)
           VALUES (%s, %s, %s, %s, 'upload', 'spremna', %s, 2400, 1600) RETURNING id""",
        (sha * 64, 'udztest/' + sha, 'udztest-' + sha + '.jpg', autor, vidljivost))[0][0]


class _Osnova(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _osiguraj_semu()

    def setUp(self):
        _ocisti()
        self.addCleanup(_ocisti)
        self.client = museum_app.app.test_client()

    def _prijava(self, role='user', email=EMAIL):
        with self.client.session_transaction() as sess:
            sess.clear()
            sess.update({'user_id': 1, 'user_email': email, 'user_name': 'Тест',
                         'user_role': role, 'is_admin': role == 'admin'})

    def get(self, url, **k):
        k.setdefault('base_url', BAZA)
        return self.client.get(url, **k)

    def post_json(self, url, telo, **k):
        k.setdefault('base_url', BAZA)
        return self.client.post(url, data=json.dumps(telo), content_type='application/json', **k)


# ---------------------------------------------------------------------------
# 1. Миграција
# ---------------------------------------------------------------------------

class MigracijaTest(_Osnova):
    def test_tabele_postoje(self):
        for t in TABELE:
            self.assertIsNotNone(_upit("SELECT to_regclass(%s)", ('public.' + t,))[0][0], t)

    def test_check_statusa_i_sluga(self):
        with self.assertRaises(psycopg.errors.CheckViolation):
            _izvrsi("INSERT INTO udzbenik (zbirka, naslov, status) VALUES ('udztest-x', 'X', 'pogresan')")
        uid = _upit("INSERT INTO udzbenik (zbirka, naslov) VALUES ('udztest-y', 'Y') RETURNING id")[0][0]
        with self.assertRaises(psycopg.errors.CheckViolation):
            _izvrsi("INSERT INTO udzbenik_poglavlje (udzbenik_id, redosled, slug, naslov) "
                    "VALUES (%s, 1, 'Велики Slug', 'P')", (uid,))

    def test_migracija_bez_sopstvene_transakcije(self):
        sql = (KOREN / 'migration' / '060_udzbenik.sql').read_text(encoding='utf-8')
        spec = importlib.util.spec_from_file_location('run_migrations', KOREN / 'deploy' / 'run_migrations.py')
        rm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rm)
        self.assertEqual(rm.problemi_za_transakciju(sql), [])


# ---------------------------------------------------------------------------
# 2. Увоз
# ---------------------------------------------------------------------------

class UvozTest(_Osnova):
    def test_dry_run_ne_menja_tabele(self):
        pre = _brojevi()
        kod, out, err = _pokreni_uvoz('--fajl', str(PRIMER), '--dry-run')
        self.assertEqual(kod, 0, err)
        self.assertEqual(_brojevi(), pre)
        self.assertIn('dry-run', out)
        self.assertIn('+ lekcija kristalografija/kristalni-sistemi (dodaje → verzija 1)', out)
        self.assertIn('2 поглавља, 4 лекција, 4 нових верзија', out)

    def test_execute_zahteva_potvrdu(self):
        pre = _brojevi()
        kod, _, err = _pokreni_uvoz('--fajl', str(PRIMER), '--execute', 'da')
        self.assertEqual(kod, 2)
        self.assertIn('mis_db', err)
        self.assertEqual(_brojevi(), pre)

    def test_execute_upisuje_i_ponovni_uvoz_je_idempotentan(self):
        pre = _brojevi()
        out = _uvezi_primer()
        posle = _brojevi()
        self.assertEqual(posle['udzbenik'] - pre['udzbenik'], 1)
        self.assertEqual(posle['udzbenik_poglavlje'] - pre['udzbenik_poglavlje'], 2)
        self.assertEqual(posle['udzbenik_lekcija'] - pre['udzbenik_lekcija'], 4)
        self.assertEqual(posle['udzbenik_lekcija_verzija'] - pre['udzbenik_lekcija_verzija'], 4)
        self.assertIn('Урађено', out)
        self.assertEqual(_upit("SELECT autor_email FROM udzbenik WHERE zbirka = 'minerali'")[0][0], EMAIL)
        self.assertEqual(_upit("SELECT DISTINCT napomena FROM udzbenik_lekcija_verzija"), [('uvoz: primer-minerali.json',)])

        out2 = _uvezi_primer()
        self.assertEqual(_brojevi(), posle)
        self.assertIn('(isto)', out2)
        self.assertIn('0 нових верзија', out2)

    def test_izmenjen_markdown_pravi_verziju_2(self):
        _uvezi_primer()
        pre = _brojevi()

        def izmeni(p):
            p['poglavlja'][0]['lekcije'][0]['sadrzaj']['blokovi'][0]['markdown'] = 'Измењен уводни текст.'
        putanja = _primer_sa_izmenom(izmeni)
        self.addCleanup(os.unlink, putanja)
        kod, out, err = _pokreni_uvoz('--fajl', putanja, '--execute', 'mis_db')
        self.assertEqual(kod, 0, err)
        posle = _brojevi()
        self.assertEqual(posle['udzbenik_lekcija'], pre['udzbenik_lekcija'])
        self.assertEqual(posle['udzbenik_lekcija_verzija'] - pre['udzbenik_lekcija_verzija'], 1)
        self.assertIn('(menja sadrzaj → verzija 2)', out)
        red = _upit("""SELECT l.verzija, l.sadrzaj->'blokovi'->0->>'markdown',
                              (SELECT COUNT(*) FROM udzbenik_lekcija_verzija v WHERE v.lekcija_id = l.id)
                       FROM udzbenik_lekcija l WHERE l.slug = 'kristalni-sistemi'""")[0]
        self.assertEqual(red, (2, 'Измењен уводни текст.', 2))

    def test_nepoznata_scena_nista_ne_upisuje(self):
        pre = _brojevi()

        def izmeni(p):
            p['poglavlja'][0]['lekcije'][0]['sadrzaj']['blokovi'][1]['scena'] = 'nepostojeca'
        putanja = _primer_sa_izmenom(izmeni)
        self.addCleanup(os.unlink, putanja)
        kod, out, err = _pokreni_uvoz('--fajl', putanja, '--execute', 'mis_db')
        self.assertEqual(kod, 1)
        self.assertEqual(_brojevi(), pre)
        self.assertIn('poglavlja[0].lekcije[0].sadrzaj.blokovi[1].scena', err)
        self.assertIn('nepostojeca', err)

    def test_poluprecnici_scene_kristalna_struktura(self):
        """Шема: опционо ``poluprecnici`` ∈ {jonski, kovalentni}; пример (без
        поља) и вредност kovalentni пролазе, непозната вредност пада с путањом."""
        def parametri(p):
            return p['poglavlja'][1]['lekcije'][1]['sadrzaj']['blokovi'][3]['parametri']
        self.assertNotIn('poluprecnici', parametri(json.loads(PRIMER.read_text(encoding='utf-8'))))
        self.assertEqual(_pokreni_uvoz('--fajl', str(PRIMER), '--dry-run')[0], 0)

        def kovalentni(p):
            parametri(p)['poluprecnici'] = 'kovalentni'
        putanja = _primer_sa_izmenom(kovalentni)
        self.addCleanup(os.unlink, putanja)
        kod, _, err = _pokreni_uvoz('--fajl', putanja, '--dry-run')
        self.assertEqual(kod, 0, err)

        def pogresno(p):
            parametri(p)['poluprecnici'] = 'metalni'
        putanja = _primer_sa_izmenom(pogresno)
        self.addCleanup(os.unlink, putanja)
        pre = _brojevi()
        kod, _, err = _pokreni_uvoz('--fajl', putanja, '--execute', 'mis_db')
        self.assertEqual(kod, 1)
        self.assertEqual(_brojevi(), pre)
        self.assertIn('poglavlja[1].lekcije[1].sadrzaj.blokovi[3].parametri.poluprecnici', err)
        self.assertIn('metalni', err)

    def test_sve_greske_odjednom_sa_putanjom(self):
        def izmeni(p):
            blokovi = p['poglavlja'][1]['lekcije'][0]['sadrzaj']['blokovi']
            blokovi[1]['id'] = blokovi[0]['id']                       # дупликат id
            blokovi.append({'id': 'slika-x', 'tip': 'slika', 'fotografija_id': 999999999})
            blokovi.append({'id': 'prim-x', 'tip': 'primerak', 'zbirka': 'minerali', 'objekat_id': 999999999})
            blokovi.append({'id': 'bez-tipa', 'tip': 'video'})
        putanja = _primer_sa_izmenom(izmeni)
        self.addCleanup(os.unlink, putanja)
        kod, _, err = _pokreni_uvoz('--fajl', putanja, '--dry-run')
        self.assertEqual(kod, 1)
        for deo in ('poglavlja[1].lekcije[0].sadrzaj.blokovi[1].id', 'blokovi[5].fotografija_id',
                    'blokovi[6].objekat_id', 'blokovi[7].tip'):
            self.assertIn(deo, err)

    def test_kolizija_redosleda_sa_bazom_jasna_greska(self):
        """Поглавље/лекција у бази а не у фајлу задржава redosled; ново са истим
        redosled-ом мора пасти јасном поруком (и у dry-run), не UniqueViolation."""
        _uvezi_primer()
        pre = _brojevi()

        def izmeni(p):
            p['poglavlja'][0]['slug'] = 'novo-poglavlje'          # redosled 1 држи kristalografija
            p['poglavlja'][1]['lekcije'][0]['slug'] = 'nova-lekcija'  # redosled 1 држи mohsova-skala
        putanja = _primer_sa_izmenom(izmeni)
        self.addCleanup(os.unlink, putanja)
        for rezim in (('--dry-run',), ('--execute', 'mis_db')):
            kod, out, err = _pokreni_uvoz('--fajl', putanja, *rezim)
            self.assertEqual(kod, 1, rezim)
            self.assertIn('poglavlja[0].redosled: redosled 1', err)
            self.assertIn("'kristalografija'", err)
            self.assertIn('poglavlja[1].lekcije[0].redosled: redosled 1', err)
            self.assertIn('fizicke-osobine/mohsova-skala', err)
            self.assertNotIn('UniqueViolation', err)
            self.assertEqual(_brojevi(), pre, rezim)

    def test_upozorenje_za_lekciju_koje_nema_u_fajlu(self):
        _uvezi_primer()

        def izmeni(p):
            del p['poglavlja'][1]['lekcije'][1]
        putanja = _primer_sa_izmenom(izmeni)
        self.addCleanup(os.unlink, putanja)
        pre = _brojevi()
        kod, out, _ = _pokreni_uvoz('--fajl', putanja, '--execute', 'mis_db')
        self.assertEqual(kod, 0)
        self.assertEqual(_brojevi(), pre, 'лекција која није у фајлу се НЕ брише')
        self.assertIn('упозорење: лекција fizicke-osobine/cepljivost-i-prelom', out)


# ---------------------------------------------------------------------------
# 3–4. API
# ---------------------------------------------------------------------------

class ApiTest(_Osnova):
    def setUp(self):
        super().setUp()
        _uvezi_primer()
        self._prijava()

    def test_struktura_po_brifu(self):
        r = self.get('/api/udzbenik/minerali')
        self.assertEqual(r.status_code, 200)
        d = r.get_json()
        self.assertEqual(set(d), {'udzbenik', 'poglavlja', 'korisnik'})
        self.assertEqual(set(d['udzbenik']), {'zbirka', 'naslov', 'opis', 'status', 'javno', 'azurirano'})
        self.assertEqual(d['udzbenik']['zbirka'], 'minerali')
        self.assertEqual([p['slug'] for p in d['poglavlja']], ['kristalografija', 'fizicke-osobine'])
        self.assertEqual(set(d['poglavlja'][0]), {'slug', 'naslov', 'redosled', 'opis', 'lekcije'})
        self.assertEqual([x['slug'] for x in d['poglavlja'][0]['lekcije']], ['kristalni-sistemi', 'kristalni-oblici'])
        self.assertEqual(set(d['poglavlja'][0]['lekcije'][0]), {'slug', 'naslov', 'redosled', 'sazetak', 'zavrseno'})
        self.assertEqual(d['korisnik'], {'prijavljen': True, 'moze_da_uredjuje': False})

    def test_lekcija_susedi_preko_granice_poglavlja(self):
        r = self.get('/api/udzbenik/minerali/lekcija/kristalografija/kristalni-oblici')
        self.assertEqual(r.status_code, 200)
        lek = r.get_json()['lekcija']
        self.assertEqual(lek['poglavlje'], {'slug': 'kristalografija', 'naslov': 'Kristalografija'})
        self.assertEqual(lek['prethodna']['lekcija'], 'kristalni-sistemi')
        self.assertEqual(lek['sledeca'], {'poglavlje': 'fizicke-osobine', 'lekcija': 'mohsova-skala',
                                          'naslov': 'Tvrdoća — Mohsova skala'})
        self.assertEqual(lek['verzija'], 1)
        self.assertFalse(lek['zavrseno'])
        self.assertEqual([b['tip'] for b in lek['blokovi']], ['tekst', 'scena', 'tekst', 'napomena', 'pitanje'])
        prva = self.get('/api/udzbenik/minerali/lekcija/kristalografija/kristalni-sistemi').get_json()['lekcija']
        self.assertIsNone(prva['prethodna'])
        poslednja = self.get('/api/udzbenik/minerali/lekcija/fizicke-osobine/cepljivost-i-prelom').get_json()['lekcija']
        self.assertIsNone(poslednja['sledeca'])
        self.assertEqual(poslednja['prethodna']['poglavlje'], 'fizicke-osobine')

    def test_nepostojeca_lekcija_404_json(self):
        r = self.get('/api/udzbenik/minerali/lekcija/kristalografija/nema')
        self.assertEqual(r.status_code, 404)
        self.assertIn('greska', r.get_json())
        self.assertEqual(self.get('/api/udzbenik/nema-zbirke').status_code, 404)

    def _lekcija_sa_slikom_i_primerkom(self, foto_id, mineral_id):
        lekcija_id = _upit("SELECT id FROM udzbenik_lekcija WHERE slug = 'kristalni-sistemi'")[0][0]
        sadrzaj = {'verzija': 1, 'blokovi': [
            {'id': 'slika-1', 'tip': 'slika', 'fotografija_id': foto_id, 'potpis': 'Пирит', 'alt': 'Пирит'},
            {'id': 'prim-1', 'tip': 'primerak', 'zbirka': 'minerali', 'objekat_id': mineral_id, 'napomena': 'Коцке'},
            {'id': 'cudan', 'tip': 'video', 'url': 'x'},
        ]}
        _izvrsi("UPDATE udzbenik_lekcija SET sadrzaj = %s WHERE id = %s", (json.dumps(sadrzaj), lekcija_id))

    def test_slika_i_primerak_razreseni(self):
        mineral_id = _ubaci_mineral()
        foto = _ubaci_fotografiju('a')
        foto_primerka = _ubaci_fotografiju('b')
        privatna = _ubaci_fotografiju('c', vidljivost='privatno', autor='neko-drugi@example.invalid')
        _izvrsi("INSERT INTO foto_veza_predmet (fotografija_id, database_name, inventarni_broj, mineral_id) "
                "VALUES (%s, 'mineral', 'UDZTEST-1', %s), (%s, 'mineral', 'UDZTEST-1', %s)",
                (foto_primerka, mineral_id, privatna, mineral_id))
        self._lekcija_sa_slikom_i_primerkom(foto, mineral_id)
        # корисник СА правом на збирку минерала (mineral_database је ограничен модул)
        with mock.patch.object(museum_app, 'user_has_module_access', lambda *a: True):
            r = self.get('/api/udzbenik/minerali/lekcija/kristalografija/kristalni-sistemi')
        self.assertEqual(r.status_code, 200)
        slika, primerak, cudan = r.get_json()['lekcija']['blokovi']
        self.assertEqual(slika['url'], '/fototeka/media/%d/jpg' % foto)
        self.assertEqual(slika['url_mala'], '/fototeka/media/%d/thumb' % foto)
        self.assertEqual((slika['sirina_px'], slika['visina_px']), (2400, 1600))
        self.assertEqual(slika['potpis'], 'Пирит', 'ауторова поља остају')
        self.assertTrue(slika['autor'])
        self.assertNotIn('nedostupan', slika)
        self.assertEqual(primerak['naziv'], 'Тестни пирит')
        self.assertEqual(primerak['inventarni_broj'], 'UDZTEST-1')
        self.assertEqual(primerak['lokalitet'], 'Бор')
        self.assertEqual(primerak['url_kartica'], '/admin/mineral_detail/%d' % mineral_id)
        self.assertEqual([f['id'] for f in primerak['fotografije']], [foto_primerka], 'приватна туђа фотографија се не види')
        self.assertEqual(primerak['fotografije'][0]['url_mala'], '/fototeka/media/%d/thumb' % foto_primerka)
        self.assertTrue(cudan['nepoznat'])
        self.assertEqual(cudan['url'], 'x')

    def test_nedostupan_bez_prava_na_zbirku_i_privatna_slika(self):
        mineral_id = _ubaci_mineral()
        privatna = _ubaci_fotografiju('d', vidljivost='privatno', autor='neko-drugi@example.invalid')
        self._lekcija_sa_slikom_i_primerkom(privatna, mineral_id)
        samo_udzbenik = lambda email, role, modul: modul == 'udzbenik'  # noqa: E731
        with mock.patch.object(museum_app, 'user_has_module_access', samo_udzbenik):
            r = self.get('/api/udzbenik/minerali/lekcija/kristalografija/kristalni-sistemi')
        self.assertEqual(r.status_code, 200, 'цела лекција не пада због једног блока')
        slika, primerak, _ = r.get_json()['lekcija']['blokovi']
        self.assertTrue(slika['nedostupan'])
        self.assertEqual(primerak, {'id': 'prim-1', 'tip': 'primerak', 'zbirka': 'minerali', 'objekat_id': mineral_id,
                                    'napomena': 'Коцке', 'nedostupan': True, 'razlog': 'nema prava na zbirku'})

    def test_bez_modula_fototeka_slike_nedostupne(self):
        """Медиј служи /fototeka/media под модулом fototeka — без њега блок
        мора поштено рећи „недоступан“, а не дати URL који пуца на 302/403."""
        mineral_id = _ubaci_mineral()
        foto = _ubaci_fotografiju('e')
        foto_primerka = _ubaci_fotografiju('f')
        _izvrsi("INSERT INTO foto_veza_predmet (fotografija_id, database_name, inventarni_broj, mineral_id) "
                "VALUES (%s, 'mineral', 'UDZTEST-1', %s)", (foto_primerka, mineral_id))
        self._lekcija_sa_slikom_i_primerkom(foto, mineral_id)
        bez_fototeke = lambda email, role, modul: modul != 'fototeka'  # noqa: E731
        with mock.patch.object(museum_app, 'user_has_module_access', bez_fototeke):
            r = self.get('/api/udzbenik/minerali/lekcija/kristalografija/kristalni-sistemi')
        self.assertEqual(r.status_code, 200)
        slika, primerak, _ = r.get_json()['lekcija']['blokovi']
        self.assertEqual(slika, {'id': 'slika-1', 'tip': 'slika', 'fotografija_id': foto, 'potpis': 'Пирит',
                                 'alt': 'Пирит', 'nedostupan': True, 'razlog': 'nema prava na Фототеку'})
        self.assertNotIn('url', slika)
        self.assertEqual(primerak['naziv'], 'Тестни пирит', 'примерак се разрешава, само без фотографија')
        self.assertEqual(primerak['fotografije'], [])
        self.assertEqual(primerak['fotografije_razlog'], 'nema prava na Фототеку')
        self.assertNotIn('/fototeka/media', r.get_data(as_text=True))

    def test_anonimni_javni_citalac_bez_slika(self):
        mineral_id = _ubaci_mineral()
        foto = _ubaci_fotografiju('g')
        self._lekcija_sa_slikom_i_primerkom(foto, mineral_id)
        _izvrsi("UPDATE udzbenik SET javno = TRUE, status = 'objavljen' WHERE zbirka = 'minerali'")
        _izvrsi("UPDATE udzbenik_lekcija SET status = 'objavljen'")
        with self.client.session_transaction() as sess:
            sess.clear()
        r = self.get('/api/udzbenik/minerali/lekcija/kristalografija/kristalni-sistemi')
        self.assertEqual(r.status_code, 200)
        slika, primerak, _ = r.get_json()['lekcija']['blokovi']
        self.assertTrue(slika['nedostupan'])
        self.assertEqual(slika['razlog'], 'nema prava na Фототеку')
        self.assertTrue(primerak['nedostupan'], 'анонимни нема право ни на збирку')
        self.assertNotIn('/fototeka/media', r.get_data(as_text=True))

    def test_obrisan_primerak_nedostupan(self):
        self._lekcija_sa_slikom_i_primerkom(999999999, 999999999)
        with mock.patch.object(museum_app, 'user_has_module_access', lambda *a: True):
            r = self.get('/api/udzbenik/minerali/lekcija/kristalografija/kristalni-sistemi')
        slika, primerak, _ = r.get_json()['lekcija']['blokovi']
        self.assertTrue(slika['nedostupan'] and primerak['nedostupan'])
        self.assertEqual(primerak['razlog'], 'примерак не постоји')


# ---------------------------------------------------------------------------
# 5. Права
# ---------------------------------------------------------------------------

class PravaTest(_Osnova):
    def setUp(self):
        super().setUp()
        _uvezi_primer()

    def _objavi(self):
        _izvrsi("UPDATE udzbenik SET javno = TRUE, status = 'objavljen' WHERE zbirka = 'minerali'")
        _izvrsi("UPDATE udzbenik_lekcija SET status = 'objavljen'")

    def test_anonimni_html_na_prijavu_api_401(self):
        for url in ('/udzbenik', '/udzbenik/minerali', '/udzbenik/minerali/kristalografija/kristalni-sistemi'):
            r = self.get(url)
            self.assertEqual(r.status_code, 302, url)
            self.assertIn('/login', r.headers['Location'])
        for url in ('/api/udzbenik/minerali', '/api/udzbenik/minerali/lekcija/kristalografija/kristalni-sistemi',
                    '/api/udzbenik/struktura/halit'):
            r = self.get(url)
            self.assertEqual(r.status_code, 401, url)
            self.assertIn('greska', r.get_json())
        r = self.post_json('/api/udzbenik/napredak', {'zbirka': 'minerali', 'poglavlje': 'kristalografija',
                                                      'lekcija': 'kristalni-sistemi', 'zavrseno': True})
        self.assertEqual(r.status_code, 401)

    def test_prijavljen_bez_modula_403(self):
        self._prijava('user')
        with mock.patch.dict(museum_app.MODULE_ACCESS['udzbenik'], {'default_access': False}), \
                mock.patch.dict(museum_app.MODULE_ACCESS_DEFAULTS['udzbenik'], {'default_access': False}):
            self.assertEqual(self.get('/udzbenik').status_code, 403)
            self.assertEqual(self.get('/udzbenik/minerali').status_code, 403)
            r = self.get('/api/udzbenik/minerali')
            self.assertEqual(r.status_code, 403)
            self.assertIn('greska', r.get_json())
            self.assertEqual(self.get('/api/udzbenik/struktura/halit').status_code, 403)
            r = self.post_json('/api/udzbenik/napredak', {'zbirka': 'minerali', 'poglavlje': 'kristalografija',
                                                          'lekcija': 'kristalni-sistemi', 'zavrseno': True})
            self.assertEqual(r.status_code, 403)
            self.assertEqual(_upit('SELECT COUNT(*) FROM udzbenik_napredak')[0][0], 0)

    def test_javno_objavljeno_cita_anonimni(self):
        self._objavi()
        r = self.get('/api/udzbenik/minerali')
        self.assertEqual(r.status_code, 200)
        d = r.get_json()
        self.assertEqual(d['korisnik'], {'prijavljen': False, 'moze_da_uredjuje': False})
        self.assertEqual(len(d['poglavlja']), 2)
        r = self.get('/udzbenik/minerali')
        self.assertEqual(r.status_code, 200)
        self.assertIn('id="udzbenik-app"', r.get_data(as_text=True))
        r = self.get('/api/udzbenik/minerali/lekcija/fizicke-osobine/mohsova-skala')
        self.assertEqual(r.status_code, 200)

    def test_anonimni_vidi_samo_objavljene_lekcije(self):
        self._objavi()
        _izvrsi("UPDATE udzbenik_lekcija SET status = 'nacrt' WHERE slug = 'kristalni-oblici'")
        d = self.get('/api/udzbenik/minerali').get_json()
        self.assertEqual([x['slug'] for x in d['poglavlja'][0]['lekcije']], ['kristalni-sistemi'])
        self.assertEqual(self.get('/api/udzbenik/minerali/lekcija/kristalografija/kristalni-oblici').status_code, 404)
        # прелаз претходна/следећа прескаче невидљиву лекцију
        lek = self.get('/api/udzbenik/minerali/lekcija/kristalografija/kristalni-sistemi').get_json()['lekcija']
        self.assertEqual(lek['sledeca']['lekcija'], 'mohsova-skala')
        self._prijava()
        d = self.get('/api/udzbenik/minerali').get_json()
        self.assertEqual(len(d['poglavlja'][0]['lekcije']), 2, 'пријављени види и нацрт')

    def test_admin_i_direktor_isto_kao_korisnik(self):
        ocekivano = None
        for role in ('user', 'admin', 'direktor'):
            self._prijava(role, email='%s@example.invalid' % role)
            r = self.get('/api/udzbenik/minerali')
            self.assertEqual(r.status_code, 200, role)
            d = r.get_json()
            self.assertEqual(d['korisnik'], {'prijavljen': True, 'moze_da_uredjuje': False}, role)
            if ocekivano is None:
                ocekivano = d['poglavlja']
            self.assertEqual(d['poglavlja'], ocekivano, role)
            self.assertEqual(self.get('/udzbenik/minerali').status_code, 200, role)
            self.assertEqual(self.get('/udzbenik').status_code, 200, role)

    def test_sme_da_cita_je_jedino_pravilo(self):
        with museum_app.app.test_request_context('/'):
            self.assertFalse(udzbenik.sme_da_cita(None))
            self.assertFalse(udzbenik.sme_da_cita({'javno': True, 'status': 'nacrt'}))
            self.assertFalse(udzbenik.sme_da_cita({'javno': False, 'status': 'objavljen'}))
            self.assertTrue(udzbenik.sme_da_cita({'javno': True, 'status': 'objavljen'}))


# ---------------------------------------------------------------------------
# 6. Напредак
# ---------------------------------------------------------------------------

class NapredakTest(_Osnova):
    TELO = {'zbirka': 'minerali', 'poglavlje': 'kristalografija', 'lekcija': 'kristalni-sistemi',
            'zavrseno': True, 'rezultat': {'tacno': 3, 'ukupno': 4, 'odgovori': {'pitanje-1': [1]}}}

    def setUp(self):
        super().setUp()
        _uvezi_primer()
        self._prijava()

    def _redovi(self):
        return _upit("""SELECT n.user_email, l.slug, n.zavrseno, n.rezultat FROM udzbenik_napredak n
                        JOIN udzbenik_lekcija l ON l.id = n.lekcija_id ORDER BY l.slug""")

    def test_bez_csrf_400(self):
        bilo = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = True
        self.addCleanup(museum_app.app.config.__setitem__, 'WTF_CSRF_ENABLED', bilo)
        r = self.post_json('/api/udzbenik/napredak', self.TELO)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(self._redovi(), [])

    def test_ispravan_post_upisuje_pa_vraca_ok(self):
        r = self.post_json('/api/udzbenik/napredak', self.TELO)
        self.assertEqual(r.status_code, 200, r.get_data(as_text=True))
        redovi = self._redovi()
        self.assertEqual(len(redovi), 1)
        self.assertEqual(redovi[0][:3], (EMAIL, 'kristalni-sistemi', True))
        self.assertEqual(redovi[0][3], {'tacno': 3, 'ukupno': 4, 'odgovori': {'pitanje-1': [1]}})
        self.assertEqual(r.get_json(), {'ok': True})
        # upsert: други POST мења исти ред
        telo = dict(self.TELO, zavrseno=False, rezultat=None)
        self.assertEqual(self.post_json('/api/udzbenik/napredak', telo).status_code, 200)
        redovi = self._redovi()
        self.assertEqual(len(redovi), 1)
        self.assertEqual(redovi[0][2:], (False, None))
        # структура враћа zavrseno из базе
        self.assertEqual(self.post_json('/api/udzbenik/napredak', self.TELO).status_code, 200)
        d = self.get('/api/udzbenik/minerali').get_json()
        self.assertTrue(d['poglavlja'][0]['lekcije'][0]['zavrseno'])
        self.assertFalse(d['poglavlja'][0]['lekcije'][1]['zavrseno'])
        lista = self.get('/udzbenik').get_data(as_text=True)
        self.assertIn('25% завршено', lista)

    def test_tacno_vece_od_ukupno_400_bez_reda(self):
        telo = dict(self.TELO, rezultat={'tacno': 5, 'ukupno': 4, 'odgovori': {}})
        r = self.post_json('/api/udzbenik/napredak', telo)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.get_json()['ok'], False)
        self.assertIn('greska', r.get_json())
        self.assertEqual(self._redovi(), [])

    def test_nepostojeca_lekcija_404_i_lose_telo_400(self):
        r = self.post_json('/api/udzbenik/napredak', dict(self.TELO, lekcija='nema'))
        self.assertEqual(r.status_code, 404)
        r = self.post_json('/api/udzbenik/napredak', dict(self.TELO, zbirka='nema'))
        self.assertEqual(r.status_code, 404)
        r = self.client.post('/api/udzbenik/napredak', data='nije json', content_type='text/plain', base_url=BAZA)
        self.assertEqual(r.status_code, 400)
        r = self.post_json('/api/udzbenik/napredak', dict(self.TELO, zavrseno='da'))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(self._redovi(), [])


# ---------------------------------------------------------------------------
# 7. Структура минерала (CIF)
# ---------------------------------------------------------------------------

CIF_HALIT = """data_Halite
_cell_length_a 5.6402
_cell_length_b 5.6402
_cell_length_c 5.6402
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90
_symmetry_space_group_name_H-M 'P 1'
_symmetry_Int_Tables_number 1
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
Na1 Na 0.0 0.0 0.0
Cl1 Cl 0.5 0.5 0.5
"""


class _LazniRruff:
    available = True
    pozivi = []

    def __init__(self, *a, **k):
        pass

    def generate_cif_from_dif(self, ime, expand_unitcell=False, supercell=None):
        _LazniRruff.pozivi.append((ime, expand_unitcell, supercell))
        return CIF_HALIT if ime.lower() == 'halite' else None


class _NemaRruff:
    available = False

    def __init__(self, *a, **k):
        pass


class StrukturaTest(_Osnova):
    def setUp(self):
        super().setUp()
        self._prijava()
        _LazniRruff.pozivi.clear()

    def test_halit_i_halite_daju_cif_p1(self):
        with mock.patch.object(local_rruff_data, 'LocalRRUFFData', _LazniRruff):
            for ime in ('halit', 'halite', 'Халит'):
                r = self.get('/api/udzbenik/struktura/' + ime)
                self.assertEqual(r.status_code, 200, ime)
                self.assertEqual(r.headers['Content-Type'], 'text/plain; charset=utf-8')
                self.assertEqual(r.headers['Cache-Control'], 'private, max-age=3600')
                telo = r.get_data(as_text=True)
                self.assertIn('_atom_site_fract_x', telo)
                self.assertIn("'P 1'", telo)
            self.assertTrue(_LazniRruff.pozivi)
            self.assertTrue(all(p[1] is True and p[2] is None for p in _LazniRruff.pozivi),
                            'API тражи САМО јединичну ћелију (без supercell): %r' % _LazniRruff.pozivi)

    def test_parametar_prikaz_je_ukinut_400(self):
        with mock.patch.object(local_rruff_data, 'LocalRRUFFData', _LazniRruff):
            for vrednost in ('celija', 'supercelija', 'nesto', ''):
                r = self.get('/api/udzbenik/struktura/halit?prikaz=' + vrednost)
                self.assertEqual(r.status_code, 400, vrednost)
                greska = r.get_json()['greska']
                self.assertIn('prikaz', greska)
                self.assertIn('мотору', greska)
                self.assertIn('P1', greska)
        self.assertEqual(_LazniRruff.pozivi, [], 'уз prikaz се RRUFF ни не пита')

    def test_nepostojeci_mineral_404_json(self):
        with mock.patch.object(local_rruff_data, 'LocalRRUFFData', _LazniRruff):
            r = self.get('/api/udzbenik/struktura/nepostojecit')
        self.assertEqual(r.status_code, 404)
        self.assertIn('greska', r.get_json())
        with mock.patch.object(local_rruff_data, 'LocalRRUFFData', _LazniRruff):
            self.assertEqual(self.get('/api/udzbenik/struktura/h').status_code, 400, 'прекратак назив')

    def test_rruff_nedostupan_503(self):
        with mock.patch.object(local_rruff_data, 'LocalRRUFFData', _NemaRruff):
            r = self.get('/api/udzbenik/struktura/halit')
        self.assertEqual(r.status_code, 503)
        self.assertIn('RRUFF', r.get_json()['greska'])

    def test_pravo_je_modul_udzbenik_ne_mineral_database(self):
        samo_udzbenik = lambda email, role, modul: modul == 'udzbenik'  # noqa: E731
        with mock.patch.object(museum_app, 'user_has_module_access', samo_udzbenik), \
                mock.patch.object(local_rruff_data, 'LocalRRUFFData', _LazniRruff):
            self.assertEqual(self.get('/api/udzbenik/struktura/halit').status_code, 200)


# ---------------------------------------------------------------------------
# 8. Љуска
# ---------------------------------------------------------------------------

class LjuskaTest(_Osnova):
    def setUp(self):
        super().setUp()
        _uvezi_primer()
        self._prijava()

    def test_data_atributi_dubokog_linka(self):
        r = self.get('/udzbenik/minerali/fizicke-osobine/mohsova-skala')
        self.assertEqual(r.status_code, 200)
        html = r.get_data(as_text=True)
        app_deo = html[html.index('id="udzbenik-app"'):html.index('</div>', html.index('id="udzbenik-app"'))]
        self.assertIn('data-api="/api/udzbenik/minerali"', app_deo)
        self.assertIn('data-api-koren="/api/udzbenik"', app_deo)
        self.assertIn('data-zbirka="minerali"', app_deo)
        self.assertIn('data-poglavlje="fizicke-osobine"', app_deo)
        self.assertIn('data-lekcija="mohsova-skala"', app_deo)
        self.assertIn('data-pismo="cyrl"', app_deo)
        self.assertIn('data-moze-uredjuje="false"', app_deo)
        self.assertIn('Учитавање уџбеника', app_deo)
        self.assertIn('udzbenik/udzbenik.js?v=', html)
        self.assertIn('udzbenik/udzbenik.css?v=', html)
        self.assertIn("css/strane/udzbenik.css", html)
        self.assertIn('class="zaglavlje page-hero"', html)
        self.assertNotIn('Kristal je čvrsto telo', html, 'љуска не носи садржај лекције')

    def test_koren_udzbenika_prazni_atributi_i_404(self):
        html = self.get('/udzbenik/minerali').get_data(as_text=True)
        self.assertIn('data-poglavlje=""', html)
        self.assertIn('data-lekcija=""', html)
        self.assertEqual(self.get('/udzbenik/minerali/kristalografija/nema').status_code, 404)
        self.assertEqual(self.get('/udzbenik/minerali/nema/kristalni-sistemi').status_code, 404)
        self.assertEqual(self.get('/udzbenik/nema-zbirke').status_code, 404)

    def test_latinica_iz_sesije(self):
        with self.client.session_transaction() as sess:
            sess['museum_lang'] = 'sr-Latn'
        self.assertIn('data-pismo="lat"', self.get('/udzbenik/minerali').get_data(as_text=True))

    def test_lista_i_navigacija(self):
        html = self.get('/udzbenik').get_data(as_text=True)
        self.assertIn('Mineralogija — interaktivni udžbenik', html)
        self.assertIn('4 лекција', html)
        self.assertIn('href="/udzbenik/minerali"', html)
        self.assertIn('Уџбеник</span>', html, 'ставка у навигацији')

    def test_sablon_bez_inline_js_i_statika_pracena(self):
        t = (KOREN / 'templates' / 'udzbenik.html').read_text(encoding='utf-8')
        self.assertEqual(t.count('<script'), 1)
        self.assertIn('type="module"', t)
        for ime in BUNDLE_FAJLOVI:
            self.assertTrue((KOREN / 'static' / 'udzbenik' / ime).exists(), ime)
        self.assertIn('!static/udzbenik/', (KOREN / '.gitignore').read_text(encoding='utf-8'))
        verzija = (KOREN / 'static' / 'udzbenik' / 'VERZIJA.txt').read_text(encoding='utf-8').splitlines()[0]
        self.assertRegex(verzija, r'^(nema|mis-udzbenik [0-9a-f]{7,40})$', verzija)

    def test_bundle_motora_je_u_gitu(self):
        """Bundle (README списак + све rezerve/*.png које мотор испоручује) мора
        бити праћен у git-у — глобално *.png је 2026-10-29 тихо прогутало
        резервне слике, па свеж клон/прод не би имао пад без WebGL-a. Шема сме
        да предњачи мотору (фаза 2: нове сцене пре bundle-а), па се тражене
        слике читају са диска, а .gitignore се проверава за СВЕ сцене из шеме."""
        readme = (KOREN / 'static' / 'udzbenik' / 'README.md').read_text(encoding='utf-8')
        iz_readme = sorted(set(re.findall(r'`([\w-]+\.(?:js|css|txt))`', readme)))
        self.assertIn('udzbenik-three.js', iz_readme)
        self.assertIn('udzbenik-dijagrami.js', iz_readme)
        sema = json.loads((KOREN / 'udzbenik' / 'schema' / 'lekcija.schema.json').read_text(encoding='utf-8'))
        scene = sema['$defs']['scena']['properties']['scena']['enum']
        self.assertGreaterEqual(len(scene), 5)
        # Фаза 2: мотор за сваки дијаграм тражи rezerve/dijagram-<dijagram>.png
        dijagrami = sema['$defs']['dijagram']['properties']['dijagram']['enum']
        self.assertGreaterEqual(len(dijagrami), 5)
        scene = scene + ['dijagram-' + d for d in dijagrami]
        rezerve = sorted(p.name for p in (KOREN / 'static' / 'udzbenik' / 'rezerve').glob('*.png'))
        self.assertGreaterEqual(len(rezerve), 5)
        self.assertEqual([r for r in rezerve if r[:-4] not in scene], [], 'резерва за сцену/дијаграм којих нема у шеми')
        ocekivani = ['static/udzbenik/' + ime for ime in iz_readme]
        ocekivani += ['static/udzbenik/rezerve/' + ime for ime in rezerve]
        praceni = set(subprocess.run(['git', 'ls-files', '--', 'static/udzbenik'], cwd=KOREN, check=True,
                                     capture_output=True, text=True).stdout.split())
        self.assertEqual([f for f in ocekivani if f not in praceni], [], 'нису у git-у')
        za_ignore = ocekivani + ['static/udzbenik/rezerve/%s.png' % scena for scena in scene]
        ignorisani = subprocess.run(['git', 'check-ignore', '--no-index', '--', *za_ignore], cwd=KOREN,
                                    capture_output=True, text=True).stdout.split()
        self.assertEqual(ignorisani, [], '.gitignore их искључује')


# ---------------------------------------------------------------------------
# 9. Претрага
# ---------------------------------------------------------------------------

class PretragaTest(_Osnova):
    def setUp(self):
        super().setUp()
        _uvezi_primer()
        self._prijava()

    def test_nalazi_lekciju_u_oba_pisma(self):
        for q in ('Mohsova', 'Мохсова', 'habitus', 'хабитус'):
            r = self.get('/api/pretraga?q=' + q)
            self.assertEqual(r.status_code, 200, q)
            grupe = {g['kljuc']: g for g in r.get_json()['grupe']}
            self.assertIn('udzbenik', grupe, q)
            self.assertEqual(grupe['udzbenik']['naziv'], 'Уџбеник')
            urlovi = [s['url'] for s in grupe['udzbenik']['stavke']]
            ocekivan = ('/udzbenik/minerali/fizicke-osobine/mohsova-skala' if 'ohsova' in q.lower() or 'охсова' in q.lower()
                        else '/udzbenik/minerali/kristalografija/kristalni-oblici')
            self.assertIn(ocekivan, urlovi, q)

    def test_bez_modula_nema_grupe(self):
        with mock.patch.object(museum_app, 'user_has_module_access', lambda e, r, m: m != 'udzbenik'):
            r = self.get('/api/pretraga?q=Mohsova')
        self.assertNotIn('udzbenik', {g['kljuc'] for g in r.get_json()['grupe']})
        self.assertIn('udzbenik', dict((i[0], i) for i in pretraga.IZVORI))


# ---------------------------------------------------------------------------
# 10. Илустрације (фаза 2): блок dijagram + нове сцене
# ---------------------------------------------------------------------------

def _lekcija_ilustracija(izmeni=None):
    """primeri-ilustracija.json као једна лекција уџбеника udztest-ilustracije;
    ``izmeni(blokovi_po_id)`` квари садржај пре уписа у привремени фајл."""
    sadrzaj = json.loads(PRIMERI_ILUSTRACIJA.read_text(encoding='utf-8'))
    if izmeni is not None:
        izmeni({b['id']: b for b in sadrzaj['blokovi']})
    podaci = {
        'udzbenik': {'zbirka': ZBIRKA_ILUSTRACIJE, 'naslov': 'Ilustracije', 'status': 'nacrt', 'javno': False},
        'poglavlja': [{'slug': 'ilustracije', 'naslov': 'Ilustracije', 'redosled': 1, 'lekcije': [
            {'slug': 'sve', 'naslov': 'Sve ilustracije', 'redosled': 1, 'status': 'nacrt', 'sadrzaj': sadrzaj}]}],
    }
    f = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8')
    json.dump(podaci, f, ensure_ascii=False)
    f.close()
    return f.name, sadrzaj


class IlustracijeTest(_Osnova):
    def test_primeri_prolaze_uvoz_i_api_vraca_sve_blokove(self):
        putanja, sadrzaj = _lekcija_ilustracija()
        self.addCleanup(os.unlink, putanja)
        self.assertEqual(len(sadrzaj['blokovi']), 29)
        kod, out, err = _pokreni_uvoz('--fajl', putanja, '--execute', 'mis_db', '--autor', EMAIL)
        self.assertEqual(kod, 0, err + out)

        self._prijava()
        r = self.get(f'/api/udzbenik/{ZBIRKA_ILUSTRACIJE}/lekcija/ilustracije/sve')
        self.assertEqual(r.status_code, 200)
        blokovi = r.get_json()['lekcija']['blokovi']
        self.assertEqual(len(blokovi), 29)
        self.assertEqual([b for b in blokovi if 'nepoznat' in b], [])
        self.assertEqual(blokovi, sadrzaj['blokovi'])

        sema = udzbenik.ucitaj_semu()
        self.assertEqual({b['dijagram'] for b in blokovi if b['tip'] == 'dijagram'},
                         set(sema['$defs']['dijagram']['properties']['dijagram']['enum']))
        self.assertLessEqual({'bravaisova-resetka', 'opticka-indikatrisa', 'blizanac', 'koordinacioni-poliedar',
                              'silikatna-struktura', 'habitus'},
                             {b['scena'] for b in blokovi if b['tip'] == 'scena'})
        self.assertIn('dijagram', udzbenik.POZNATI_TIPOVI)

    def test_los_dijagram_pada_sa_putanjom_i_nista_se_ne_upisuje(self):
        def pokvari(b):
            b['d-bowen']['dijagram'] = 'nepostojeci'                       # непозната врста
            b['d-sio2']['parametri']['sistem'] = 'H2O'                     # лош систем
            b['d-karta']['parametri']['lokaliteti'][1]['lat'] = 48.2       # тачка ван Србије
            b['d-par']['parametri']['minerali'][1].update(od=2, do=1)      # od > do
            b['d-par']['parametri']['minerali'][2]['do'] = 7               # do ≥ број фаза
            b['s-kvarc']['parametri']['forme'][0]['hkl'] = [1, 0, -2, 0]   # i ≠ −(h+k)
        putanja, sadrzaj = _lekcija_ilustracija(pokvari)
        self.addCleanup(os.unlink, putanja)
        indeks = {b['id']: i for i, b in enumerate(sadrzaj['blokovi'])}
        pre = _brojevi()
        kod, _, err = _pokreni_uvoz('--fajl', putanja, '--execute', 'mis_db', '--autor', EMAIL)
        self.assertEqual(kod, 1)
        self.assertEqual(_brojevi(), pre)
        self.assertEqual(_upit('SELECT 1 FROM udzbenik WHERE zbirka = %s', (ZBIRKA_ILUSTRACIJE,)), [])
        koren = 'poglavlja[0].lekcije[0].sadrzaj.blokovi'
        for deo in (f"{koren}[{indeks['d-bowen']}].dijagram: 'nepostojeci'",
                    f"{koren}[{indeks['d-sio2']}].parametri.sistem: 'H2O'",
                    f"{koren}[{indeks['d-karta']}].parametri.lokaliteti[1].lat: 48.2",
                    f"{koren}[{indeks['d-par']}].parametri.minerali[1]: od=2",
                    f"{koren}[{indeks['d-par']}].parametri.minerali[2].do: 7",
                    f"{koren}[{indeks['s-kvarc']}].parametri.forme[0].hkl: i=-2"):
            self.assertIn(deo, err)

    def test_karta_van_srbije_dozvoljena_za_drugu_oblast(self):
        def izmeni(b):
            b['d-karta']['parametri']['oblast'] = 'evropa'
            b['d-karta']['parametri']['lokaliteti'][1]['lat'] = 48.2
            del b['d-karta']['parametri']['prikazi_jedinice']
        putanja, _ = _lekcija_ilustracija(izmeni)
        self.addCleanup(os.unlink, putanja)
        kod, _, err = _pokreni_uvoz('--fajl', putanja, '--dry-run')
        self.assertEqual(kod, 0, err)


# ---------------------------------------------------------------------------
# 10. Литература из SciSearch-а (уговор LITERATURA.md §2) — лажни SciSearch
# ---------------------------------------------------------------------------

SCISEARCH_ENV = {'SCISEARCH_URL': 'https://192.168.144.194/nauka/', 'SCISEARCH_SVC_TOKEN': 'test-token'}
BEZ_SCISEARCH_ENV = {'SCISEARCH_URL': '', 'SCISEARCH_SVC_TOKEN': ''}
REZULTAT_SCISEARCH = {
    'doc_id': 812, 'naslov': 'Минерали Србије', 'autor': 'Петровић', 'godina': 1987, 'vrsta': 'book',
    'izvor': 'geolosko', 'poglavlje': {'naslov': 'Сулфиди', 'autori': 'Петровић', 'strana_od': 12, 'strana_do': 30},
    'strana': 47, 'isecak': 'Кристали <mark>пирита</mark> су <b>кубични</b><script>alert(1)</script>.',
    'url': '/nauka/doc/812?page=47&q=пирит',
}


class _Odgovor:
    def __init__(self, status_code=200, telo=None, tekst='nije json'):
        self.status_code = status_code
        self._telo = telo
        self._tekst = tekst

    def json(self):
        if self._telo is None:
            raise ValueError(self._tekst)
        return self._telo


def _scisearch_odgovor(rezultati, status=200):
    return _Odgovor(status, {'upit': 'пирит', 'ukupno': len(rezultati), 'ms': 12, 'rezultati': rezultati})


class LiteraturaKlijentTest(unittest.TestCase):
    """scisearch_klijent без мреже: env, timeout, кеш, чишћење исечка."""

    def setUp(self):
        scisearch_klijent.ocisti_kes()
        self.addCleanup(scisearch_klijent.ocisti_kes)

    def test_bez_env_nije_podesen(self):
        with mock.patch.dict(os.environ, BEZ_SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent.requests, 'get') as get:
            self.assertFalse(scisearch_klijent.podesen())
            with self.assertRaises(scisearch_klijent.SciSearchNijePodesen) as cm:
                scisearch_klijent.pretrazi('пирит', 3)
            self.assertEqual(cm.exception.razlog, 'biblioteka nije povezana')
            self.assertIsInstance(cm.exception, scisearch_klijent.SciSearchGreska)
            get.assert_not_called()

    def test_poziv_sa_tokenom_as_user_i_timeoutom(self):
        with mock.patch.dict(os.environ, SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent.requests, 'get',
                                  return_value=_scisearch_odgovor([REZULTAT_SCISEARCH])) as get:
            rezultati = scisearch_klijent.pretrazi('  пирит   Бор ', 20, as_user=EMAIL)
        get.assert_called_once_with(
            'https://192.168.144.194/nauka/svc/search',
            params={'q': 'пирит Бор', 'n': 8, 'mode': 'hybrid', 'as_user': EMAIL},
            headers={'X-Svc-Token': 'test-token'}, timeout=4)
        self.assertEqual(len(rezultati), 1)
        r = rezultati[0]
        self.assertEqual(r['isecak'], 'Кристали <mark>пирита</mark> су кубичниalert(1).',
                         '<mark> остаје, други тагови не')
        self.assertEqual(r['url'], '/nauka/doc/812?page=47&q=пирит', 'url остаје релативан — исти хост')
        self.assertEqual((r['doc_id'], r['naslov'], r['autor'], r['godina'], r['strana']),
                         (812, 'Минерали Србије', 'Петровић', 1987, 47))
        self.assertEqual(r['poglavlje']['strana_do'], 30)
        self.assertEqual(set(r), {'doc_id', 'naslov', 'autor', 'godina', 'vrsta', 'izvor', 'poglavlje',
                                  'strana', 'isecak', 'url'})

    def test_timeout_i_los_odgovor_dizu_gresku_sa_razlogom(self):
        with mock.patch.dict(os.environ, SCISEARCH_ENV):
            with mock.patch.object(scisearch_klijent.requests, 'get', side_effect=requests.Timeout()):
                with self.assertRaises(scisearch_klijent.SciSearchGreska) as cm:
                    scisearch_klijent.pretrazi('пирит')
                self.assertIn('timeout', cm.exception.razlog)
            with mock.patch.object(scisearch_klijent.requests, 'get', return_value=_Odgovor(401, {'greska': 'x'})):
                with self.assertRaises(scisearch_klijent.SciSearchGreska) as cm:
                    scisearch_klijent.pretrazi('пирит')
                self.assertEqual(cm.exception.razlog, 'HTTP 401')
            with mock.patch.object(scisearch_klijent.requests, 'get', return_value=_Odgovor(200, None)):
                with self.assertRaises(scisearch_klijent.SciSearchGreska):
                    scisearch_klijent.pretrazi('пирит')
            with mock.patch.object(scisearch_klijent.requests, 'get', return_value=_Odgovor(200, {'nema': 1})):
                with self.assertRaises(scisearch_klijent.SciSearchGreska):
                    scisearch_klijent.pretrazi('пирит')
            with mock.patch.object(scisearch_klijent.requests, 'get',
                                   side_effect=requests.ConnectionError('odbijeno')):
                with self.assertRaises(scisearch_klijent.SciSearchGreska) as cm:
                    scisearch_klijent.pretrazi('пирит')
                self.assertIn('odbijeno', cm.exception.razlog)

    def test_kes_10_minuta_po_upitu_i_broju(self):
        with mock.patch.dict(os.environ, SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent.requests, 'get',
                                  return_value=_scisearch_odgovor([REZULTAT_SCISEARCH])) as get:
            prvi = scisearch_klijent.pretrazi('пирит', 3)
            drugi = scisearch_klijent.pretrazi('пирит', 3, as_user='drugi@example.invalid')
            self.assertEqual(get.call_count, 1, 'други позив из кеша')
            self.assertEqual(prvi, drugi)
            drugi[0]['naslov'] = 'измењено'
            self.assertEqual(scisearch_klijent.pretrazi('пирит', 3)[0]['naslov'], 'Минерали Србије',
                             'кеш враћа копије')
            scisearch_klijent.pretrazi('пирит', 5)
            self.assertEqual(get.call_count, 2, 'други broj = други кључ')
            with mock.patch.object(scisearch_klijent.time, 'monotonic',
                                   return_value=scisearch_klijent.time.monotonic() + 601):
                scisearch_klijent.pretrazi('пирит', 3)
            self.assertEqual(get.call_count, 3, 'после 10 минута поново пита')
            get.side_effect = requests.Timeout()
            with self.assertRaises(scisearch_klijent.SciSearchGreska):
                scisearch_klijent.pretrazi('нови упит', 3)
            self.assertEqual(get.call_count, 4)
            with self.assertRaises(scisearch_klijent.SciSearchGreska):
                scisearch_klijent.pretrazi('нови упит', 3)
            self.assertEqual(get.call_count, 5, 'грешка се не кешира')

    def test_prazan_upit_ne_zove_servis(self):
        with mock.patch.dict(os.environ, SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent.requests, 'get') as get:
            self.assertEqual(scisearch_klijent.pretrazi('   ', 3), [])
            get.assert_not_called()

    def test_ocisti_isecak(self):
        self.assertEqual(scisearch_klijent.ocisti_isecak('a <MARK>b</MARK> <img src=x onerror=1> <mark x="y">c'),
                         'a <mark>b</mark>  c')
        self.assertEqual(scisearch_klijent.ocisti_isecak(None), '')
        self.assertEqual(len(scisearch_klijent.ocisti_isecak('x' * 1000)), 400)


class LiteraturaApiTest(_Osnova):
    def setUp(self):
        super().setUp()
        _uvezi_primer()
        scisearch_klijent.ocisti_kes()
        self.addCleanup(scisearch_klijent.ocisti_kes)
        self.lekcija_id = _upit("SELECT id FROM udzbenik_lekcija WHERE slug = 'kristalni-sistemi'")[0][0]
        self.blok = {'id': 'lit-1', 'tip': 'literatura', 'upit': 'пирит', 'naslov': 'Из библиотеке',
                     'napomena': 'Опис кристала пирита у старијој литератури'}
        sadrzaj = {'verzija': 1, 'blokovi': [
            {'id': 'uvod', 'tip': 'tekst', 'markdown': 'Пирит.'}, dict(self.blok),
            {'id': 'lit-2', 'tip': 'literatura', 'upit': 'нема ничега', 'broj': 2},
        ]}
        _izvrsi("UPDATE udzbenik_lekcija SET sadrzaj = %s WHERE id = %s", (json.dumps(sadrzaj), self.lekcija_id))

    URL = '/api/udzbenik/minerali/lekcija/kristalografija/kristalni-sistemi'

    def _blokovi(self):
        r = self.get(self.URL)
        self.assertEqual(r.status_code, 200, 'лекција се увек враћа')
        return r.get_json()['lekcija']['blokovi']

    def test_rezultati_prolaze_isecak_samo_mark(self):
        self._prijava()

        def lazni_get(url, params, headers, timeout):
            if params['q'] == 'пирит':
                return _scisearch_odgovor([REZULTAT_SCISEARCH])
            return _scisearch_odgovor([])
        with mock.patch.dict(os.environ, SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent.requests, 'get', side_effect=lazni_get) as get:
            tekst, lit, prazan = self._blokovi()
        self.assertEqual(tekst['tip'], 'tekst')
        self.assertEqual([c.kwargs['params'] for c in get.call_args_list],
                         [{'q': 'пирит', 'n': 3, 'mode': 'hybrid', 'as_user': EMAIL},
                          {'q': 'нема ничега', 'n': 2, 'mode': 'hybrid', 'as_user': EMAIL}],
                         'подразумевани broj 3, as_user = пријављени')
        self.assertEqual({k: lit[k] for k in self.blok}, self.blok, 'ауторова поља остају')
        self.assertNotIn('nedostupan', lit)
        self.assertEqual(len(lit['rezultati']), 1)
        r = lit['rezultati'][0]
        self.assertEqual(r['isecak'], 'Кристали <mark>пирита</mark> су кубичниalert(1).')
        self.assertEqual(r['url'], '/nauka/doc/812?page=47&q=пирит')
        self.assertEqual(r['naslov'], 'Минерали Србије')
        self.assertEqual(prazan, {'id': 'lit-2', 'tip': 'literatura', 'upit': 'нема ничега', 'broj': 2,
                                  'nedostupan': True, 'razlog': 'nema rezultata'})
        self.assertNotIn('<script', self.get(self.URL).get_data(as_text=True))

    def test_izuzetak_klijenta_ne_obara_lekciju(self):
        self._prijava()
        with mock.patch.dict(os.environ, SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent, 'pretrazi', side_effect=RuntimeError('пукло')):
            _, lit, lit2 = self._blokovi()
        self.assertEqual({k: lit[k] for k in ('nedostupan', 'razlog')},
                         {'nedostupan': True, 'razlog': 'biblioteka trenutno nije dostupna'})
        self.assertEqual(lit['napomena'], self.blok['napomena'])
        self.assertNotIn('rezultati', lit)
        self.assertTrue(lit2['nedostupan'])

    def test_timeout_i_http_greska_nedostupan(self):
        self._prijava()
        with mock.patch.dict(os.environ, SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent.requests, 'get', side_effect=requests.Timeout()):
            _, lit, _ = self._blokovi()
        self.assertEqual(lit['razlog'], 'biblioteka trenutno nije dostupna')
        with mock.patch.dict(os.environ, SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent.requests, 'get', return_value=_Odgovor(504, {'greska': 't'})):
            _, lit, _ = self._blokovi()
        self.assertTrue(lit['nedostupan'])
        self.assertEqual(lit['razlog'], 'biblioteka trenutno nije dostupna')

    def test_nepodesen_env_biblioteka_nije_povezana(self):
        self._prijava()
        with mock.patch.dict(os.environ, BEZ_SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent.requests, 'get') as get:
            _, lit, _ = self._blokovi()
        get.assert_not_called()
        self.assertEqual((lit['nedostupan'], lit['razlog']), (True, 'biblioteka nije povezana'))

    def test_anonimni_samo_za_prijavljene(self):
        _izvrsi("UPDATE udzbenik SET javno = TRUE, status = 'objavljen' WHERE zbirka = 'minerali'")
        _izvrsi("UPDATE udzbenik_lekcija SET status = 'objavljen'")
        with self.client.session_transaction() as sess:
            sess.clear()
        with mock.patch.dict(os.environ, SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent.requests, 'get') as get:
            tekst, lit, lit2 = self._blokovi()
        get.assert_not_called()
        self.assertEqual(tekst['markdown'], 'Пирит.')
        for b in (lit, lit2):
            self.assertEqual((b['nedostupan'], b['razlog']), (True, 'samo za prijavljene korisnike'))
            self.assertNotIn('rezultati', b)

    def test_uvoz_validira_blok_literatura(self):
        def pokvari(podaci):
            podaci['poglavlja'][0]['lekcije'][0]['sadrzaj']['blokovi'].extend([
                {'id': 'lit-a', 'tip': 'literatura'},
                {'id': 'lit-b', 'tip': 'literatura', 'upit': 'x' * 201, 'broj': 9},
                {'id': 'lit-c', 'tip': 'literatura', 'upit': 'пирит', 'url': '/nauka/doc/1'},
            ])
        putanja = _primer_sa_izmenom(pokvari)
        self.addCleanup(os.unlink, putanja)
        pre = _brojevi()
        kod, _, err = _pokreni_uvoz('--fajl', putanja, '--execute', 'mis_db')
        self.assertEqual(kod, 1)
        self.assertEqual(_brojevi(), pre)
        n = len(json.loads(PRIMER.read_text(encoding='utf-8'))['poglavlja'][0]['lekcije'][0]['sadrzaj']['blokovi'])
        koren = 'poglavlja[0].lekcije[0].sadrzaj.blokovi'
        self.assertIn(f"{koren}[{n}]: 'upit' is a required property", err)
        self.assertIn(f'{koren}[{n + 1}].broj: 9 is greater than the maximum of 8', err)
        self.assertIn(f'{koren}[{n + 1}].upit:', err)
        self.assertIn(f"{koren}[{n + 2}]: Additional properties are not allowed ('url' was unexpected)", err)

    def _primer_sa_literaturom(self):
        def dodaj(podaci):
            podaci['poglavlja'][0]['lekcije'][0]['sadrzaj']['blokovi'].extend([
                {'id': 'lit-a', 'tip': 'literatura', 'upit': 'пирит'},
                {'id': 'lit-b', 'tip': 'literatura', 'upit': 'нема ничега', 'broj': 2},
            ])
        putanja = _primer_sa_izmenom(dodaj)
        self.addCleanup(os.unlink, putanja)
        return putanja

    def test_uvoz_proveri_literaturu_upozorava_na_0_rezultata(self):
        putanja = self._primer_sa_literaturom()

        def lazni(upit, broj=3, as_user=None):
            return [dict(REZULTAT_SCISEARCH)] if upit == 'пирит' else []
        pre = _brojevi()
        with mock.patch.dict(os.environ, SCISEARCH_ENV), mock.patch.object(scisearch_klijent, 'pretrazi', lazni):
            kod, out, err = _pokreni_uvoz('--fajl', putanja, '--dry-run', '--proveri-literaturu')
        self.assertEqual(kod, 0, err)
        self.assertEqual(_brojevi(), pre)
        self.assertIn("! упозорење: poglavlja[0].lekcije[0].sadrzaj.blokovi[6].upit: 'нема ничега' даје 0 резултата", out)
        self.assertNotIn("'пирит' даје 0", out)
        self.assertIn('1 упозорења', out)
        # без заставице SciSearch се не пита
        with mock.patch.dict(os.environ, SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent, 'pretrazi', side_effect=AssertionError('не сме')):
            kod, out, err = _pokreni_uvoz('--fajl', putanja, '--dry-run')
        self.assertEqual(kod, 0, err)
        self.assertIn('0 упозорења', out)

    def test_uvoz_proveri_literaturu_bez_servisa_je_greska(self):
        putanja = self._primer_sa_literaturom()
        pre = _brojevi()
        with mock.patch.dict(os.environ, BEZ_SCISEARCH_ENV):
            kod, _, err = _pokreni_uvoz('--fajl', putanja, '--execute', 'mis_db', '--proveri-literaturu')
        self.assertEqual(kod, 1)
        self.assertIn('SciSearch није подешен', err)
        self.assertEqual(_brojevi(), pre, 'ништа није уписано')
        with mock.patch.dict(os.environ, SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent, 'pretrazi',
                                  side_effect=scisearch_klijent.SciSearchGreska('timeout после 4 s')):
            kod, _, err = _pokreni_uvoz('--fajl', putanja, '--execute', 'mis_db', '--proveri-literaturu')
        self.assertEqual(kod, 1)
        self.assertIn('blokovi[5]: SciSearch није одговорио (timeout после 4 s)', err)
        self.assertEqual(_brojevi(), pre)


if __name__ == '__main__':
    unittest.main()
