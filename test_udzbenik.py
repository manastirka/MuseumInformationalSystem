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
import shutil
import subprocess
import tempfile
import unittest
import uuid
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


def _ucitaj_ai_slike():
    spec = importlib.util.spec_from_file_location('udzbenik_ai_slike', KOREN / 'scripts' / 'udzbenik_ai_slike.py')
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


ai_slike = _ucitaj_ai_slike()


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
            cur.execute("DELETE FROM fotografije WHERE raw_putanja LIKE 'udztest/%%' OR original_ime LIKE 'udztest-ai-%%'")
            cur.execute("DELETE FROM fototeka_intake_pending WHERE original_ime LIKE 'udztest-ai-%%'")
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


_IME_BAZE = []


def _ime_baze():
    """Потврда за ``--execute`` = име базе на коју је свита стварно повезана (тест база)."""
    if not _IME_BAZE:
        _IME_BAZE.append(_upit('SELECT current_database()')[0][0])
    return _IME_BAZE[0]


def _pokreni_uvoz(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        kod = uvoz.main(list(argv))
    return kod, out.getvalue(), err.getvalue()


def _uvezi_primer():
    kod, out, err = _pokreni_uvoz('--fajl', str(PRIMER), '--execute', _ime_baze(), '--autor', EMAIL)
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

    def test_execute_trazi_ime_baze(self):
        # Потврда је име базе на коју је скрипта стварно повезана (као udzbenik_ai_slike.py),
        # а не дословно „mis_db“ — на dev-у је база museum_system, на тестовима *_test.
        pre = _brojevi()
        baza = _ime_baze()
        self.assertTrue(baza.endswith('_test'), baza)
        for pogresno in ('da', 'mis_db'):
            kod, _, err = _pokreni_uvoz('--fajl', str(PRIMER), '--execute', pogresno)
            self.assertEqual(kod, 2, err)
            self.assertIn(f'дословно име базе „{baza}“', err)
            self.assertIn(repr(pogresno), err)
            self.assertEqual(_brojevi(), pre)
        kod, out, err = _pokreni_uvoz('--fajl', str(PRIMER), '--execute', baza)
        self.assertEqual(kod, 0, err + out)
        self.assertNotEqual(_brojevi(), pre)

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
        kod, out, err = _pokreni_uvoz('--fajl', putanja, '--execute', _ime_baze())
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
        kod, out, err = _pokreni_uvoz('--fajl', putanja, '--execute', _ime_baze())
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
        kod, _, err = _pokreni_uvoz('--fajl', putanja, '--execute', _ime_baze())
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
        for rezim in (('--dry-run',), ('--execute', _ime_baze())):
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
        kod, out, _ = _pokreni_uvoz('--fajl', putanja, '--execute', _ime_baze())
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
        kod, out, err = _pokreni_uvoz('--fajl', putanja, '--execute', _ime_baze(), '--autor', EMAIL)
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
        kod, _, err = _pokreni_uvoz('--fajl', putanja, '--execute', _ime_baze(), '--autor', EMAIL)
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
        kod, _, err = _pokreni_uvoz('--fajl', putanja, '--execute', _ime_baze())
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
            kod, _, err = _pokreni_uvoz('--fajl', putanja, '--execute', _ime_baze(), '--proveri-literaturu')
        self.assertEqual(kod, 1)
        self.assertIn('SciSearch није подешен', err)
        self.assertEqual(_brojevi(), pre, 'ништа није уписано')
        with mock.patch.dict(os.environ, SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent, 'pretrazi',
                                  side_effect=scisearch_klijent.SciSearchGreska('timeout после 4 s')):
            kod, _, err = _pokreni_uvoz('--fajl', putanja, '--execute', _ime_baze(), '--proveri-literaturu')
        self.assertEqual(kod, 1)
        self.assertIn('blokovi[5]: SciSearch није одговорио (timeout после 4 s)', err)
        self.assertEqual(_brojevi(), pre)


# ---------------------------------------------------------------------------
# 11. Слике из литературе (MIS-UGOVOR-SLIKE.md §2) — лажни SciSearch
# ---------------------------------------------------------------------------

FIGURA_SCISEARCH = {
    'id': 5175, 'doc_id': 442, 'strana': 12, 'sirina': 800, 'visina': 600, 'vrsta': 'thin_section',
    'potpis': 'Figure 17 <b>Backscattered</b> electron image<script>x</script> of pyrite',
    'naslov': 'Ore Microscopy', 'autor': 'Craig & Vaughan', 'godina': 1999,
    'slika': '/svc/figure/5175.jpg', 'sicicka': '/svc/figure/5175/thumb.jpg',
}
JPEG_BAJTOVI = b'\xff\xd8\xff\xe0' + b'J' * 300 + b'\xff\xd9'
PNG_BAJTOVI = b'\x89PNG\r\n\x1a\n' + b'P' * 100


class _SlikaOdgovor:
    """Стримовани одговор requests-а: iter_content, headers, close."""

    def __init__(self, status_code=200, bajtovi=JPEG_BAJTOVI, tip='image/jpeg', duzina=None, komad=None):
        self.status_code = status_code
        self.headers = {'Content-Type': tip}
        if duzina is not None:
            self.headers['Content-Length'] = str(duzina)
        self._bajtovi = bajtovi
        self._komad = komad
        self.zatvoren = False
        self.procitano = 0

    def iter_content(self, velicina):
        velicina = self._komad or velicina
        for i in range(0, len(self._bajtovi), velicina):
            deo = self._bajtovi[i:i + velicina]
            self.procitano += len(deo)
            yield deo

    def close(self):
        self.zatvoren = True


def _lazni_scisearch(figura=None, slika=None):
    """requests.get по URL-у: /svc/figure/<id> → JSON, .jpg/thumb.jpg → слика."""
    figura = FIGURA_SCISEARCH if figura is None else figura
    pozivi = []

    def get(url, **k):
        pozivi.append((url, k))
        if url.endswith('.jpg'):
            if slika is None:
                return _SlikaOdgovor(bajtovi=PNG_BAJTOVI if 'thumb' in url else JPEG_BAJTOVI,
                                     tip='image/png' if 'thumb' in url else 'image/jpeg')
            return slika() if callable(slika) else slika
        if figura == 404:
            return _Odgovor(404, {'greska': 'nema'})
        return _Odgovor(200, dict(figura))
    get.pozivi = pozivi
    return get


class SlikaLiteraturaKlijentTest(unittest.TestCase):
    """scisearch_klijent.figura / preuzmi_sliku без мреже."""

    def setUp(self):
        scisearch_klijent.ocisti_kes()
        self.addCleanup(scisearch_klijent.ocisti_kes)

    def test_bez_env_nije_podesen(self):
        with mock.patch.dict(os.environ, BEZ_SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent.requests, 'get') as get:
            with self.assertRaises(scisearch_klijent.SciSearchNijePodesen):
                scisearch_klijent.figura(5175)
            with self.assertRaises(scisearch_klijent.SciSearchNijePodesen):
                scisearch_klijent.preuzmi_sliku(5175)
            get.assert_not_called()

    def test_figura_oblik_potpis_cist_i_kes(self):
        get = _lazni_scisearch()
        with mock.patch.dict(os.environ, SCISEARCH_ENV), mock.patch.object(scisearch_klijent.requests, 'get', get):
            fig = scisearch_klijent.figura(5175)
            self.assertEqual(get.pozivi, [('https://192.168.144.194/nauka/svc/figure/5175',
                                           {'headers': {'X-Svc-Token': 'test-token'}, 'timeout': 4})])
            self.assertEqual(fig, {
                'id': 5175, 'doc_id': 442, 'strana': 12, 'sirina': 800, 'visina': 600, 'vrsta': 'thin_section',
                'potpis': 'Figure 17 Backscattered electron imagex of pyrite',
                'naslov': 'Ore Microscopy', 'autor': 'Craig & Vaughan', 'godina': 1999,
            }, 'само позната поља; потпис без тагова; без slika/sicicka SciSearch-а')
            fig['naslov'] = 'измењено'
            self.assertEqual(scisearch_klijent.figura(5175)['naslov'], 'Ore Microscopy', 'кеш враћа копије')
            self.assertEqual(len(get.pozivi), 1, 'други позив из кеша')
            with mock.patch.object(scisearch_klijent.time, 'monotonic',
                                   return_value=scisearch_klijent.time.monotonic() + 601):
                scisearch_klijent.figura(5175)
            self.assertEqual(len(get.pozivi), 2, 'после 10 минута поново пита')

    def test_figura_404_timeout_los_id(self):
        with mock.patch.dict(os.environ, SCISEARCH_ENV):
            with mock.patch.object(scisearch_klijent.requests, 'get', _lazni_scisearch(figura=404)):
                with self.assertRaises(scisearch_klijent.SciSearchNemaFigure) as cm:
                    scisearch_klijent.figura(5175)
                self.assertIsInstance(cm.exception, scisearch_klijent.SciSearchGreska)
                self.assertEqual(cm.exception.razlog, 'figura 5175 ne postoji')
            with mock.patch.object(scisearch_klijent.requests, 'get', side_effect=requests.Timeout()):
                with self.assertRaises(scisearch_klijent.SciSearchGreska) as cm:
                    scisearch_klijent.figura(5175)
                self.assertIn('timeout', cm.exception.razlog)
                self.assertNotIn('test-token', str(cm.exception))
            with mock.patch.object(scisearch_klijent.requests, 'get', return_value=_Odgovor(200, {'nema': 1})):
                with self.assertRaises(scisearch_klijent.SciSearchGreska):
                    scisearch_klijent.figura(5175)
            with mock.patch.object(scisearch_klijent.requests, 'get') as get:
                for los in (0, -1, '5175', True, None):
                    with self.assertRaises(scisearch_klijent.SciSearchGreska):
                        scisearch_klijent.figura(los)
                get.assert_not_called()

    def test_preuzmi_sliku_stream_timeout_8_tip_i_lru_kes(self):
        get = _lazni_scisearch()
        with mock.patch.dict(os.environ, SCISEARCH_ENV), mock.patch.object(scisearch_klijent.requests, 'get', get):
            bajtovi, tip = scisearch_klijent.preuzmi_sliku(5175)
            self.assertEqual((bajtovi, tip), (JPEG_BAJTOVI, 'image/jpeg'))
            self.assertEqual(get.pozivi[-1], ('https://192.168.144.194/nauka/svc/figure/5175.jpg',
                                              {'headers': {'X-Svc-Token': 'test-token'}, 'timeout': 8, 'stream': True}))
            mala, tip_male = scisearch_klijent.preuzmi_sliku(5175, mala=True)
            self.assertEqual((mala, tip_male), (PNG_BAJTOVI, 'image/png'))
            self.assertEqual(get.pozivi[-1][0], 'https://192.168.144.194/nauka/svc/figure/5175/thumb.jpg')
            self.assertEqual(len(get.pozivi), 2)
            scisearch_klijent.preuzmi_sliku(5175)
            scisearch_klijent.preuzmi_sliku(5175, mala=True)
            self.assertEqual(len(get.pozivi), 2, 'друго читање из LRU кеша, SciSearch се не зове')
            self.assertEqual(scisearch_klijent.velicina_kesa_slika(), len(JPEG_BAJTOVI) + len(PNG_BAJTOVI))

    def test_preuzmi_sliku_odbija_tip_velicinu_i_404(self):
        with mock.patch.dict(os.environ, SCISEARCH_ENV):
            html = _SlikaOdgovor(tip='text/html; charset=utf-8', bajtovi=b'<html>')
            with mock.patch.object(scisearch_klijent.requests, 'get', return_value=html):
                with self.assertRaises(scisearch_klijent.SciSearchGreska) as cm:
                    scisearch_klijent.preuzmi_sliku(5175)
                self.assertIn('text/html', cm.exception.razlog)
                self.assertTrue(html.zatvoren)
            prevelika = _SlikaOdgovor(duzina=16 * 1024 * 1024)
            with mock.patch.object(scisearch_klijent.requests, 'get', return_value=prevelika):
                with self.assertRaises(scisearch_klijent.SciSearchGreska) as cm:
                    scisearch_klijent.preuzmi_sliku(5175)
                self.assertIn('15 MB', cm.exception.razlog)
                self.assertEqual(prevelika.procitano, 0, 'прекид пре читања тела')
            # без Content-Length: прекид чим стрим пређе 15 MB, не чита се до краја
            lazljiva = _SlikaOdgovor(bajtovi=b'x' * (16 * 1024 * 1024), komad=1024 * 1024)
            with mock.patch.object(scisearch_klijent.requests, 'get', return_value=lazljiva):
                with self.assertRaises(scisearch_klijent.SciSearchGreska):
                    scisearch_klijent.preuzmi_sliku(5175)
                self.assertEqual(lazljiva.procitano, 16 * 1024 * 1024, 'стаје на првом комаду преко границе')
                self.assertTrue(lazljiva.zatvoren)
            with mock.patch.object(scisearch_klijent.requests, 'get', return_value=_SlikaOdgovor(404)):
                with self.assertRaises(scisearch_klijent.SciSearchNemaFigure):
                    scisearch_klijent.preuzmi_sliku(5175)
            with mock.patch.object(scisearch_klijent.requests, 'get', return_value=_SlikaOdgovor(bajtovi=b'')):
                with self.assertRaises(scisearch_klijent.SciSearchGreska):
                    scisearch_klijent.preuzmi_sliku(5175)
            with mock.patch.object(scisearch_klijent.requests, 'get', side_effect=requests.Timeout()):
                with self.assertRaises(scisearch_klijent.SciSearchGreska) as cm:
                    scisearch_klijent.preuzmi_sliku(5175)
                self.assertEqual(cm.exception.razlog, 'timeout после 8 s')
            self.assertEqual(scisearch_klijent.velicina_kesa_slika(), 0, 'грешка се не кешира')

    def test_lru_kes_izbacuje_najstarije(self):
        get = _lazni_scisearch(slika=lambda: _SlikaOdgovor(bajtovi=b'j' * 100))
        with mock.patch.dict(os.environ, SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent, 'SLIKA_KES_NAJVISE_BAJTOVA', 250), \
                mock.patch.object(scisearch_klijent.requests, 'get', get):
            scisearch_klijent.preuzmi_sliku(1)
            scisearch_klijent.preuzmi_sliku(2)
            scisearch_klijent.preuzmi_sliku(1)  # 1 је сад „свежија“ од 2
            scisearch_klijent.preuzmi_sliku(3)  # 300 > 250 → избацује 2
            self.assertEqual(len(get.pozivi), 3)
            self.assertEqual(scisearch_klijent.velicina_kesa_slika(), 200)
            scisearch_klijent.preuzmi_sliku(1)
            scisearch_klijent.preuzmi_sliku(3)
            self.assertEqual(len(get.pozivi), 3, '1 и 3 су у кешу')
            scisearch_klijent.preuzmi_sliku(2)
            self.assertEqual(len(get.pozivi), 4, '2 је избачена')


class SlikaLiteraturaApiTest(_Osnova):
    URL = '/api/udzbenik/minerali/lekcija/kristalografija/kristalni-sistemi'
    SLIKA = '/api/udzbenik/literatura-slika/5175'
    MALA = '/api/udzbenik/literatura-slika/5175/thumb'

    def setUp(self):
        super().setUp()
        _uvezi_primer()
        scisearch_klijent.ocisti_kes()
        self.addCleanup(scisearch_klijent.ocisti_kes)
        self.lekcija_id = _upit("SELECT id FROM udzbenik_lekcija WHERE slug = 'kristalni-sistemi'")[0][0]
        self.blok = {'id': 'fig-1', 'tip': 'slika-literatura', 'figura_id': 5175, 'sirina': 'pola',
                     'potpis': 'Пирит у одбијеној светлости.', 'napomena': 'Зашто је слика ту.'}
        sadrzaj = {'verzija': 1, 'blokovi': [
            {'id': 'uvod', 'tip': 'tekst', 'markdown': 'Пирит.'}, dict(self.blok),
            {'id': 'kraj', 'tip': 'tekst', 'markdown': 'Крај.'},
        ]}
        _izvrsi("UPDATE udzbenik_lekcija SET sadrzaj = %s WHERE id = %s", (json.dumps(sadrzaj), self.lekcija_id))

    def _objavi_javno(self):
        _izvrsi("UPDATE udzbenik SET javno = TRUE, status = 'objavljen' WHERE zbirka = 'minerali'")
        _izvrsi("UPDATE udzbenik_lekcija SET status = 'objavljen'")
        with self.client.session_transaction() as sess:
            sess.clear()

    def _blokovi(self):
        r = self.get(self.URL)
        self.assertEqual(r.status_code, 200, 'лекција се увек враћа')
        return r.get_json()['lekcija']['blokovi']

    def test_prijavljen_izvor_i_proxy_slika(self):
        self._prijava()
        get = _lazni_scisearch()
        with mock.patch.dict(os.environ, SCISEARCH_ENV), mock.patch.object(scisearch_klijent.requests, 'get', get):
            uvod, fig, kraj = self._blokovi()
            self.assertEqual((uvod['id'], kraj['id']), ('uvod', 'kraj'))
            self.assertEqual({k: fig[k] for k in self.blok}, self.blok, 'ауторова поља остају')
            self.assertNotIn('nedostupan', fig)
            self.assertEqual(fig['izvor'], {
                'naslov': 'Ore Microscopy', 'autor': 'Craig & Vaughan', 'godina': 1999, 'strana': 12,
                'potpis_izvora': 'Figure 17 Backscattered electron imagex of pyrite'})
            self.assertEqual((fig['slika'], fig['sicicka']), (self.SLIKA, self.MALA), 'МИС-ове руте, не SciSearch')
            self.assertEqual((fig['sirina_px'], fig['visina_px']), (800, 600))
            self.assertEqual([u for u, _ in get.pozivi], ['https://192.168.144.194/nauka/svc/figure/5175'])
            telo = self.get(self.URL).get_data(as_text=True)
            self.assertNotIn('test-token', telo)
            self.assertNotIn('/svc/', telo, 'клијент не сазнаје SciSearch путање')

            r = self.get(self.SLIKA)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'image/jpeg')
            self.assertEqual(r.data, JPEG_BAJTOVI)
            self.assertEqual(r.headers['Cache-Control'], 'private, max-age=604800')
            self.assertEqual(get.pozivi[-1], ('https://192.168.144.194/nauka/svc/figure/5175.jpg',
                                              {'headers': {'X-Svc-Token': 'test-token'}, 'timeout': 8, 'stream': True}))
            r = self.get(self.MALA)
            self.assertEqual((r.status_code, r.mimetype, r.data), (200, 'image/png', PNG_BAJTOVI))
            self.assertNotIn('test-token', str(r.headers) + str(r.data))
            n = len(get.pozivi)
            self.assertEqual(self.get(self.SLIKA).status_code, 200)
            self.assertEqual(len(get.pozivi), n, 'други приказ из кеша, SciSearch се не зове')

    def test_anonimni_blok_izostavljen_ruta_404(self):
        self._objavi_javno()
        get = _lazni_scisearch()
        with mock.patch.dict(os.environ, SCISEARCH_ENV), mock.patch.object(scisearch_klijent.requests, 'get', get):
            blokovi = self._blokovi()
            self.assertEqual([b['id'] for b in blokovi], ['uvod', 'kraj'], 'блок потпуно изостављен')
            telo = self.get(self.URL).get_data(as_text=True)
            for trag in ('slika-literatura', '5175', 'Ore Microscopy', 'Пирит у одбијеној'):
                self.assertNotIn(trag, telo, 'ни слика ни навод за анонимног')
            for url in (self.SLIKA, self.MALA):
                r = self.get(url)
                self.assertEqual(r.status_code, 404, url)
                self.assertIn('greska', r.get_json())
            self.assertEqual(get.pozivi, [], 'SciSearch се за анонимног не зове')

    def test_prijavljen_bez_modula_403(self):
        self._prijava('user')
        get = _lazni_scisearch()
        with mock.patch.dict(museum_app.MODULE_ACCESS['udzbenik'], {'default_access': False}), \
                mock.patch.dict(museum_app.MODULE_ACCESS_DEFAULTS['udzbenik'], {'default_access': False}), \
                mock.patch.dict(os.environ, SCISEARCH_ENV), mock.patch.object(scisearch_klijent.requests, 'get', get):
            for url in (self.SLIKA, self.MALA):
                self.assertEqual(self.get(url).status_code, 403, url)
            self.assertEqual(get.pozivi, [])

    def test_admin_i_direktor_isto_kao_korisnik(self):
        for role in ('user', 'admin', 'direktor'):
            self._prijava(role, email='%s@example.invalid' % role)
            scisearch_klijent.ocisti_kes()
            get = _lazni_scisearch()
            with mock.patch.dict(os.environ, SCISEARCH_ENV), mock.patch.object(scisearch_klijent.requests, 'get', get):
                _, fig, _ = self._blokovi()
                self.assertEqual(fig['izvor']['naslov'], 'Ore Microscopy', role)
                self.assertEqual(self.get(self.SLIKA).status_code, 200, role)

    def test_scisearch_pao_nedostupan_lekcija_zivi(self):
        self._prijava()
        with mock.patch.dict(os.environ, SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent.requests, 'get', side_effect=requests.Timeout()):
            uvod, fig, kraj = self._blokovi()
            self.assertEqual({k: fig[k] for k in self.blok}, self.blok)
            self.assertEqual((fig['nedostupan'], fig['razlog']), (True, 'biblioteka trenutno nije dostupna'))
            for polje in ('izvor', 'slika', 'sicicka'):
                self.assertNotIn(polje, fig)
            r = self.get(self.SLIKA)
            self.assertEqual(r.status_code, 503)
            self.assertIn('greska', r.get_json())
        with mock.patch.dict(os.environ, SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent.requests, 'get', return_value=_Odgovor(500, {'greska': 'x'})):
            _, fig, _ = self._blokovi()
            self.assertEqual(fig['razlog'], 'biblioteka trenutno nije dostupna')
        with mock.patch.dict(os.environ, SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent, 'figura', side_effect=RuntimeError('пукло')):
            _, fig, _ = self._blokovi()
            self.assertTrue(fig['nedostupan'])

    def test_figura_ne_postoji_i_nepodesen_env(self):
        self._prijava()
        with mock.patch.dict(os.environ, SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent.requests, 'get', _lazni_scisearch(figura=404)):
            _, fig, _ = self._blokovi()
            self.assertEqual((fig['nedostupan'], fig['razlog']), (True, 'slika ne postoji u biblioteci'))
            with mock.patch.object(scisearch_klijent.requests, 'get', return_value=_SlikaOdgovor(404)):
                self.assertEqual(self.get(self.SLIKA).status_code, 404)
        with mock.patch.dict(os.environ, BEZ_SCISEARCH_ENV), \
                mock.patch.object(scisearch_klijent.requests, 'get') as get:
            _, fig, _ = self._blokovi()
            self.assertEqual((fig['nedostupan'], fig['razlog']), (True, 'biblioteka nije povezana'))
            self.assertEqual(self.get(self.SLIKA).status_code, 503)
            get.assert_not_called()

    def test_uvoz_validira_blok_slika_literatura(self):
        def pokvari(podaci):
            podaci['poglavlja'][0]['lekcije'][0]['sadrzaj']['blokovi'].extend([
                {'id': 'fig-a', 'tip': 'slika-literatura'},
                {'id': 'fig-b', 'tip': 'slika-literatura', 'figura_id': 0, 'sirina': 'mala'},
                {'id': 'fig-c', 'tip': 'slika-literatura', 'figura_id': 5175, 'slika': '/svc/figure/5175.jpg'},
                {'id': 'fig-d', 'tip': 'slika-literatura', 'figura_id': 5175, 'potpis': 'x' * 501},
            ])
        putanja = _primer_sa_izmenom(pokvari)
        self.addCleanup(os.unlink, putanja)
        pre = _brojevi()
        kod, _, err = _pokreni_uvoz('--fajl', putanja, '--execute', _ime_baze())
        self.assertEqual(kod, 1)
        self.assertEqual(_brojevi(), pre)
        n = len(json.loads(PRIMER.read_text(encoding='utf-8'))['poglavlja'][0]['lekcije'][0]['sadrzaj']['blokovi'])
        koren = 'poglavlja[0].lekcije[0].sadrzaj.blokovi'
        self.assertIn(f"{koren}[{n}]: 'figura_id' is a required property", err)
        self.assertIn(f'{koren}[{n + 1}].figura_id: 0 is less than the minimum of 1', err)
        self.assertIn(f"{koren}[{n + 1}].sirina: 'mala' is not one of ['puna', 'pola']", err)
        self.assertIn(f"{koren}[{n + 2}]: Additional properties are not allowed ('slika' was unexpected)", err)
        self.assertIn(f'{koren}[{n + 3}].potpis:', err)

    def test_uvoz_ispravan_blok_prolazi_i_proveri_figuru(self):
        def dodaj(podaci):
            podaci['poglavlja'][0]['lekcije'][0]['sadrzaj']['blokovi'].extend([
                {'id': 'fig-a', 'tip': 'slika-literatura', 'figura_id': 5175, 'potpis': 'Пирит.'},
                {'id': 'fig-b', 'tip': 'slika-literatura', 'figura_id': 999999, 'sirina': 'pola'},
            ])
        putanja = _primer_sa_izmenom(dodaj)
        self.addCleanup(os.unlink, putanja)
        kod, out, err = _pokreni_uvoz('--fajl', putanja, '--dry-run')
        self.assertEqual(kod, 0, err)

        def lazna_figura(figura_id):
            if figura_id == 5175:
                return dict(FIGURA_SCISEARCH)
            raise scisearch_klijent.SciSearchNemaFigure(figura_id)
        pre = _brojevi()
        with mock.patch.dict(os.environ, SCISEARCH_ENV), mock.patch.object(scisearch_klijent, 'figura', lazna_figura), \
                mock.patch.object(scisearch_klijent, 'pretrazi', side_effect=AssertionError('нема literatura блока')):
            kod, out, err = _pokreni_uvoz('--fajl', putanja, '--execute', _ime_baze(), '--proveri-literaturu')
        self.assertEqual(kod, 1)
        self.assertIn('blokovi[6].figura_id: фигура 999999 не постоји у SciSearch-у', err)
        self.assertNotIn('blokovi[5]', err)
        self.assertEqual(_brojevi(), pre, 'ништа није уписано')

        def sve_postoje(figura_id):
            return dict(FIGURA_SCISEARCH, id=figura_id)
        with mock.patch.dict(os.environ, SCISEARCH_ENV), mock.patch.object(scisearch_klijent, 'figura', sve_postoje):
            kod, out, err = _pokreni_uvoz('--fajl', putanja, '--execute', _ime_baze(), '--proveri-literaturu')
        self.assertEqual(kod, 0, err)
        self.assertIn('0 упозорења', out)
        sadrzaj = _upit("SELECT sadrzaj FROM udzbenik_lekcija WHERE slug = 'kristalni-sistemi'")[0][0]
        if isinstance(sadrzaj, str):
            sadrzaj = json.loads(sadrzaj)
        self.assertEqual([b['figura_id'] for b in sadrzaj['blokovi'] if b['tip'] == 'slika-literatura'],
                         [5175, 999999])


# ---------------------------------------------------------------------------
# AI илустрације → Фототека → лекције (scripts/udzbenik_ai_slike.py)
# ---------------------------------------------------------------------------

AI_MAPA = [
    {'slika': 'udztest-ai-komora', 'lekcija': '01-kristalni-sistemi', 'posle_bloka': 'uvod',
     'potpis': 'Магматска комора. (AI ilustracija, šematski)', 'alt': 'Пресек магматске коморе.'},
    {'slika': 'udztest-ai-rečni', 'lekcija': 'kristalni-sistemi', 'posle_bloka': 'tabela',
     'potpis': 'Речни плацер. (AI ilustracija, šematski)', 'alt': 'Речно корито са златом.'},
    {'slika': 'udztest-ai-laguna', 'lekcija': 'kristalni-sistemi', 'posle_bloka': 'tabela',
     'potpis': 'Евапоритна лагуна. (AI ilustracija, šematski)', 'alt': 'Плитка лагуна са кристалима соли.'},
    {'slika': 'udztest-ai-komora', 'lekcija': 'mohsova-skala', 'posle_bloka': 'uvod',
     'potpis': 'Иста слика у другој лекцији.', 'alt': 'Пресек магматске коморе.'},
]
AI_IDS_SISTEMI = ['uvod', 'ai-udztest-ai-komora', 'scena-sistemi', 'tabela', 'ai-udztest-ai-recni',
                  'ai-udztest-ai-laguna', 'napomena-simetrija', 'pitanje-1']


def _pokreni_ai_slike(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        kod = ai_slike.main(list(argv))
    return kod, out.getvalue(), err.getvalue()


def _broj_fotografija():
    return _upit("SELECT COUNT(*) FROM fotografije WHERE original_ime LIKE 'udztest-ai-%%'")[0][0]


class AiSlikeTest(_Osnova):
    """До базе и до диска (привремени FOTOTEKA_ARHIVA_PATH / FOTOTEKA_MEDIA_PATH)."""

    def setUp(self):
        super().setUp()
        _uvezi_primer()
        from PIL import Image
        self.tmp = Path(tempfile.mkdtemp(prefix='udztest-ai-'))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.slike = self.tmp / 'slike'
        self.slike.mkdir()
        for ime, boja in (('udztest-ai-komora', (120, 40, 20)), ('udztest-ai-rečni', (20, 80, 140)),
                          ('udztest-ai-laguna', (200, 190, 90))):
            Image.new('RGB', (600, 448), boja).save(self.slike / f'{ime}.png', format='PNG')
        self.arhiva, self.media = self.tmp / 'arhiva', self.tmp / 'media'
        env = mock.patch.dict(os.environ, {'FOTOTEKA_ARHIVA_PATH': str(self.arhiva),
                                           'FOTOTEKA_MEDIA_PATH': str(self.media)})
        env.start()
        self.addCleanup(env.stop)
        self.mapa = self._mapa(AI_MAPA)
        self.baza = _upit('SELECT current_database()')[0][0]

    def _mapa(self, stavke):
        putanja = self.tmp / f'mapa-{uuid.uuid4().hex[:6]}.json'
        putanja.write_text(json.dumps(stavke, ensure_ascii=False), encoding='utf-8')
        return str(putanja)

    def _izvrsi(self, mapa=None):
        return _pokreni_ai_slike('--mapa', mapa or self.mapa, '--slike', str(self.slike),
                                 '--execute', self.baza, '--autor', EMAIL)

    def _lekcija(self, slug):
        red = _upit('SELECT id, verzija, sadrzaj FROM udzbenik_lekcija WHERE slug = %s', (slug,))[0]
        sadrzaj = json.loads(red[2]) if isinstance(red[2], str) else red[2]
        return red[0], red[1], sadrzaj

    def _raw_fajlovi(self):
        return sorted(p.name for p in self.arhiva.rglob('*') if p.is_file()) if self.arhiva.exists() else []

    def test_id_bloka_je_ascii(self):
        self.assertEqual(ai_slike.id_bloka('rečni-placer'), 'ai-recni-placer')
        self.assertEqual(ai_slike.id_bloka('Đerdap-šljunak-žica-ćup'), 'ai-djerdap-sljunak-zica-cup')

    def test_dry_run_ne_menja_nista(self):
        pre, pre_foto = _brojevi(), _broj_fotografija()
        kod, out, err = _pokreni_ai_slike('--mapa', self.mapa, '--slike', str(self.slike), '--dry-run',
                                          '--autor', EMAIL)
        self.assertEqual(kod, 0, err + out)
        self.assertEqual(_brojevi(), pre)
        self.assertEqual(_broj_fotografija(), pre_foto)
        self.assertEqual(self._raw_fajlovi(), [], 'dry-run не пише на диск')
        self.assertFalse(self.media.exists())
        self.assertIn('dry-run', out)
        self.assertIn('+ udztest-ai-komora (udztest-ai-komora.png', out)
        self.assertIn('~ kristalografija/kristalni-sistemi (мапа: 01-kristalni-sistemi): verzija 1 → 2, +3 блок(ова)',
                      out)
        self.assertIn('+ ai-udztest-ai-recni после tabela (нова фотографија)', out)
        self.assertIn('3 слика (3 нових), 2 лекција (2 нових верзија), 0 грешака', out)
        self.assertEqual(self._lekcija('kristalni-sistemi')[1], 1)

    def test_execute_trazi_ime_baze(self):
        kod, _, err = _pokreni_ai_slike('--mapa', self.mapa, '--slike', str(self.slike),
                                        '--execute', 'mis_db', '--autor', EMAIL)
        self.assertEqual(kod, 2)
        self.assertIn(f'дословно име базе „{self.baza}“', err)
        self.assertEqual(_broj_fotografija(), 0)

    def test_execute_pravi_fotografije_i_nove_verzije(self):
        pre = _brojevi()
        kod, out, err = self._izvrsi()
        self.assertEqual(kod, 0, err + out)
        self.assertIn('Урађено', out)
        # Фототека: 3 фотографије кроз intake (RAW на диску, ред за деривате, тагови, порекло у опису)
        foto = _upit("""SELECT id, original_ime, opis, poreklo, status, raw_putanja, u_prijemnom_redu,
                               sklonjena_sa_reda, autor_email, width, height
                        FROM fotografije WHERE original_ime LIKE 'udztest-ai-%%' ORDER BY id""")
        self.assertEqual([f[1] for f in foto],
                         ['udztest-ai-komora.png', 'udztest-ai-rečni.png', 'udztest-ai-laguna.png'])
        for f in foto:
            self.assertIn('Poreklo: AI ilustracija, šematski. Alat: Gemini (Antigravity).', f[2])
            self.assertEqual((f[3], f[4], f[6], f[7], f[8], f[9], f[10]),
                             ('import', 'primljena', False, True, EMAIL, 600, 448))
            self.assertTrue((self.arhiva / f[5]).is_file(), f[5])
            self.assertEqual(_upit("SELECT COUNT(*) FROM foto_poslovi WHERE fotografija_id = %s AND tip = 'derivati'",
                                   (f[0],))[0][0], 1)
            self.assertEqual(sorted(t[0] for t in _upit('SELECT tag FROM fotografija_tagovi WHERE fotografija_id = %s',
                                                        (f[0],))), ['ai-ilustracija', 'udzbenik'])
        self.assertTrue(foto[0][2].startswith('Пресек магматске коморе.'))
        ids = {f[1]: f[0] for f in foto}
        # Лекција: једна нова верзија, блокови одмах после posle_bloka, редослед из мапе
        lekcija_id, verzija, sadrzaj = self._lekcija('kristalni-sistemi')
        self.assertEqual(verzija, 2)
        self.assertEqual([b['id'] for b in sadrzaj['blokovi']], AI_IDS_SISTEMI)
        blok = sadrzaj['blokovi'][4]
        self.assertEqual(blok, {'id': 'ai-udztest-ai-recni', 'tip': 'slika',
                                'fotografija_id': ids['udztest-ai-rečni.png'],
                                'potpis': 'Речни плацер. (AI ilustracija, šematski)', 'alt': 'Речно корито са златом.',
                                'poreklo': 'ai-ilustracija', 'sirina': 'puna'})
        verzije = _upit("""SELECT verzija, autor_email, napomena FROM udzbenik_lekcija_verzija
                           WHERE lekcija_id = %s ORDER BY verzija""", (lekcija_id,))
        self.assertEqual(verzije[-1], (2, EMAIL, 'ai-slike: ' + os.path.basename(self.mapa)))
        self.assertEqual(len(verzije), 2)
        # иста слика у другој лекцији = исти fotografije.id, без дупликата
        _, verzija_mohs, sadrzaj_mohs = self._lekcija('mohsova-skala')
        self.assertEqual(verzija_mohs, 2)
        self.assertEqual(sadrzaj_mohs['blokovi'][1]['fotografija_id'], ids['udztest-ai-komora.png'])
        self.assertEqual(self._lekcija('kristalni-oblici')[1], 1, 'лекција ван мапе нетакнута')
        posle = _brojevi()
        self.assertEqual(posle['udzbenik_lekcija_verzija'], pre['udzbenik_lekcija_verzija'] + 2)
        self.assertEqual(posle['udzbenik_lekcija'], pre['udzbenik_lekcija'])

    def test_drugo_pokretanje_ne_pravi_nista_novo(self):
        kod, out, err = self._izvrsi()
        self.assertEqual(kod, 0, err + out)
        pre, pre_foto, pre_raw = _brojevi(), _broj_fotografija(), self._raw_fajlovi()
        kod, out, err = self._izvrsi()
        self.assertEqual(kod, 0, err + out)
        self.assertEqual(_brojevi(), pre)
        self.assertEqual(_broj_fotografija(), pre_foto)
        self.assertEqual(self._raw_fajlovi(), pre_raw)
        self.assertEqual(self._lekcija('kristalni-sistemi')[1], 2)
        self.assertIn('већ у Фототеци као fotografija #', out)
        self.assertIn('= kristalografija/kristalni-sistemi (мапа: 01-kristalni-sistemi): сви блокови већ постоје',
                      out)
        self.assertIn('3 слика (0 нових), 2 лекција (0 нових верзија), 0 грешака', out)
        # нова слика у већ обрађеној лекцији → само она се додаје, остале прескочене
        mapa = self._mapa(AI_MAPA + [{'slika': 'udztest-ai-laguna', 'lekcija': 'mohsova-skala', 'posle_bloka': 'uvod',
                                      'potpis': 'Лагуна.', 'alt': 'Лагуна.'}])
        kod, out, err = self._izvrsi(mapa)
        self.assertEqual(kod, 0, err + out)
        self.assertEqual(_broj_fotografija(), pre_foto)
        _, verzija, sadrzaj = self._lekcija('mohsova-skala')
        self.assertEqual(verzija, 3)
        self.assertEqual([b['id'] for b in sadrzaj['blokovi']][:3],
                         ['uvod', 'ai-udztest-ai-komora', 'ai-udztest-ai-laguna'])
        self.assertIn('= ai-udztest-ai-komora већ постоји, исти — прескочен', out)

    def test_nepostojeci_posle_bloka_je_greska_i_nista_se_ne_menja(self):
        mapa = self._mapa(AI_MAPA + [{'slika': 'udztest-ai-laguna', 'lekcija': 'mohsova-skala',
                                      'posle_bloka': 'nema-takvog', 'potpis': 'x', 'alt': 'x'}])
        pre = _brojevi()
        kod, out, err = self._izvrsi(mapa)
        self.assertEqual(kod, 1)
        self.assertIn("блок 'nema-takvog' (posle_bloka за 'udztest-ai-laguna') не постоји у лекцији "
                      'fizicke-osobine/mohsova-skala', out)
        self.assertIn('! fizicke-osobine/mohsova-skala: ГРЕШКА — остаје нетакнута', out)
        self.assertIn('ништа није уписано', err)
        self.assertEqual(_brojevi(), pre)
        self.assertEqual(_broj_fotografija(), 0)
        self.assertEqual(self._raw_fajlovi(), [])
        self.assertEqual(self._lekcija('mohsova-skala')[1], 1)
        self.assertEqual(self._lekcija('kristalni-sistemi')[1], 1)
        # непостојећа лекција и погрешан префикс редоследа су исто грешке
        mapa = self._mapa([dict(AI_MAPA[0], lekcija='02-kristalni-sistemi'), dict(AI_MAPA[0], lekcija='nema-lekcije')])
        kod, out, err = self._izvrsi(mapa)
        self.assertEqual(kod, 1)
        self.assertIn("slug 'kristalni-sistemi' постоји, али му redosled није 2", out)
        self.assertIn("лекција 'nema-lekcije' не постоји", out)
        self.assertEqual(_broj_fotografija(), 0)
        # фајл који недостаје се пријави пре него што се база и дира
        mapa = self._mapa([dict(AI_MAPA[0], slika='udztest-ai-nema')])
        kod, out, err = self._izvrsi(mapa)
        self.assertEqual(kod, 1)
        self.assertIn('нема фајла udztest-ai-nema.png', err)

    # --- замена слике/текста у постојећем блоку (поље ``fajl``) ---

    def _mapa_v2(self, **izmene):
        """Иста мапа, али прва ставка (udztest-ai-komora у kristalni-sistemi) са изменама."""
        return self._mapa([dict(AI_MAPA[0], **izmene)] + AI_MAPA[1:])

    def _verzije(self, lekcija_id):
        return _upit("""SELECT verzija, sadrzaj FROM udzbenik_lekcija_verzija WHERE lekcija_id = %s
                        ORDER BY verzija""", (lekcija_id,))

    def _blok(self, sadrzaj, bid):
        sadrzaj = json.loads(sadrzaj) if isinstance(sadrzaj, str) else sadrzaj
        return next(b for b in sadrzaj['blokovi'] if b.get('id') == bid)

    def test_fajl_menja_sliku_u_novoj_verziji_a_stara_ostaje(self):
        from PIL import Image
        kod, out, err = self._izvrsi()
        self.assertEqual(kod, 0, err + out)
        lekcija_id, _, sadrzaj = self._lekcija('kristalni-sistemi')
        stari_blok = self._blok(sadrzaj, 'ai-udztest-ai-komora')
        stara_foto = stari_blok['fotografija_id']
        (self.slike / 'v2').mkdir()
        Image.new('RGB', (600, 448), (10, 200, 60)).save(self.slike / 'v2' / 'udztest-ai-komora-v2.png', format='PNG')
        mapa = self._mapa_v2(fajl='v2/udztest-ai-komora-v2.png')
        # dry-run каже шта би било и ништа не мења
        pre, pre_foto = _brojevi(), _broj_fotografija()
        kod, out, err = _pokreni_ai_slike('--mapa', mapa, '--slike', str(self.slike), '--dry-run', '--autor', EMAIL)
        self.assertEqual(kod, 0, err + out)
        self.assertIn('+ udztest-ai-komora (udztest-ai-komora-v2.png', out)
        self.assertIn('~ kristalografija/kristalni-sistemi (мапа: 01-kristalni-sistemi): verzija 2 → 3, '
                      '+0 блок(ова), ~1 измењен(их)', out)
        self.assertIn(f'~ ai-udztest-ai-komora на истом месту: замена слике (fotografija #{stara_foto} → '
                      'нова фотографија)', out)
        self.assertIn('= ai-udztest-ai-recni већ постоји, исти — прескочен', out)
        self.assertIn('= fizicke-osobine/mohsova-skala: сви блокови већ постоје (ai-udztest-ai-komora) и исти су',
                      out)
        self.assertIn('4 слика (1 нових), 2 лекција (1 нових верзија), 0 грешака', out)
        self.assertEqual((_brojevi(), _broj_fotografija()), (pre, pre_foto))
        # execute: нова фотографија, нова верзија са истим id блока на истом месту
        kod, out, err = self._izvrsi(mapa)
        self.assertEqual(kod, 0, err + out)
        self.assertEqual(_broj_fotografija(), pre_foto + 1)
        nova_foto = _upit("SELECT id, opis FROM fotografije WHERE original_ime = 'udztest-ai-komora-v2.png'")[0]
        self.assertNotEqual(nova_foto[0], stara_foto)
        self.assertIn('Poreklo: AI ilustracija, šematski. Alat: Gemini (Antigravity).', nova_foto[1])
        self.assertEqual(sorted(t[0] for t in _upit('SELECT tag FROM fotografija_tagovi WHERE fotografija_id = %s',
                                                    (nova_foto[0],))), ['ai-ilustracija', 'udzbenik'])
        _, verzija, sadrzaj = self._lekcija('kristalni-sistemi')
        self.assertEqual(verzija, 3)
        self.assertEqual([b['id'] for b in sadrzaj['blokovi']], AI_IDS_SISTEMI, 'исти id и исто место')
        self.assertEqual(self._blok(sadrzaj, 'ai-udztest-ai-komora'), dict(stari_blok, fotografija_id=nova_foto[0]))
        verzije = self._verzije(lekcija_id)
        self.assertEqual([v[0] for v in verzije], [1, 2, 3])
        self.assertEqual(self._blok(verzije[1][1], 'ai-udztest-ai-komora')['fotografija_id'], stara_foto,
                         'стара верзија нетакнута')
        self.assertEqual(self._blok(verzije[2][1], 'ai-udztest-ai-komora')['fotografija_id'], nova_foto[0])
        # стара фотографија остаје у Фототеци; mohsova-skala (исти кључ, стари фајл) нетакнута
        self.assertEqual(_upit('SELECT obrisana FROM fotografije WHERE id = %s', (stara_foto,))[0][0], False)
        self.assertEqual(self._lekcija('mohsova-skala')[1], 2)
        # друго покретање исте мапе: ништа ново
        pre, pre_foto = _brojevi(), _broj_fotografija()
        kod, out, err = self._izvrsi(mapa)
        self.assertEqual(kod, 0, err + out)
        self.assertEqual((_brojevi(), _broj_fotografija()), (pre, pre_foto))
        self.assertEqual(self._lekcija('kristalni-sistemi')[1], 3)
        self.assertIn('4 слика (0 нових), 2 лекција (0 нових верзија), 0 грешака', out)

    def test_promena_samo_potpisa_pravi_novu_verziju_bez_nove_fotografije(self):
        kod, out, err = self._izvrsi()
        self.assertEqual(kod, 0, err + out)
        lekcija_id, _, sadrzaj = self._lekcija('kristalni-sistemi')
        stari_blok = self._blok(sadrzaj, 'ai-udztest-ai-komora')
        mapa = self._mapa_v2(potpis='Магматска комора, зонирана. (AI ilustracija, šematski)')
        pre, pre_foto = _brojevi(), _broj_fotografija()
        kod, out, err = self._izvrsi(mapa)
        self.assertEqual(kod, 0, err + out)
        self.assertIn('~ ai-udztest-ai-komora на истом месту: промена текста (potpis)', out)
        self.assertEqual(_broj_fotografija(), pre_foto)
        posle = _brojevi()
        self.assertEqual(posle['udzbenik_lekcija_verzija'], pre['udzbenik_lekcija_verzija'] + 1)
        _, verzija, sadrzaj = self._lekcija('kristalni-sistemi')
        self.assertEqual(verzija, 3)
        self.assertEqual(self._blok(sadrzaj, 'ai-udztest-ai-komora'),
                         dict(stari_blok, potpis='Магматска комора, зонирана. (AI ilustracija, šematski)'))
        self.assertEqual(self._blok(self._verzije(lekcija_id)[1][1], 'ai-udztest-ai-komora'), stari_blok)
        # поново иста мапа → идемпотентно
        kod, out, err = self._izvrsi(mapa)
        self.assertEqual(kod, 0, err + out)
        self.assertEqual(_brojevi(), posle)
        self.assertEqual(self._lekcija('kristalni-sistemi')[1], 3)

    def test_nepostojeci_fajl_je_greska_bez_delimicnog_upisa(self):
        from PIL import Image
        kod, out, err = self._izvrsi()
        self.assertEqual(kod, 0, err + out)
        (self.slike / 'v2').mkdir()
        Image.new('RGB', (600, 448), (10, 200, 60)).save(self.slike / 'v2' / 'udztest-ai-recni-v2.png', format='PNG')
        # у истој лекцији: једна исправна замена (rečni) + једна са непостојећим фајлом (komora)
        mapa = self._mapa([dict(AI_MAPA[0], fajl='v2/udztest-ai-nema.png'), dict(AI_MAPA[1], fajl='v2/udztest-ai-recni-v2.png')] + AI_MAPA[2:])
        pre, pre_foto, pre_raw = _brojevi(), _broj_fotografija(), self._raw_fajlovi()
        kod, out, err = self._izvrsi(mapa)
        self.assertEqual(kod, 1)
        self.assertIn(f'mapa[0].fajl: нема фајла v2/udztest-ai-nema.png у {self.slike}', err)
        self.assertIn('ништа није уписано', err)
        self.assertEqual((_brojevi(), _broj_fotografija(), self._raw_fajlovi()), (pre, pre_foto, pre_raw))
        self.assertEqual(self._lekcija('kristalni-sistemi')[1], 2)
        # fajl ван --slike и празан fajl су такође грешке
        for los in ('../udztest-ai-recni-v2.png', '/etc/passwd', ''):
            kod, out, err = self._izvrsi(self._mapa_v2(fajl=los))
            self.assertEqual(kod, 1, los)
            self.assertIn('mapa[0].fajl', err)
        self.assertEqual(_broj_fotografija(), pre_foto)

    def test_api_vraca_blok_slika_sa_poreklom_i_slika_se_sluzi(self):
        import fototeka_jobs
        kod, out, err = self._izvrsi()
        self.assertEqual(kod, 0, err + out)
        self._prijava()
        with mock.patch.object(museum_app, 'user_has_module_access', lambda *a, **k: True), \
                mock.patch.object(museum_app.app, 'user_has_module_access', lambda *a, **k: True):
            r = self.get('/api/udzbenik/minerali/lekcija/kristalografija/kristalni-sistemi')
            self.assertEqual(r.status_code, 200)
            lek = r.get_json()['lekcija']
            self.assertEqual(lek['verzija'], 2)
            self.assertEqual([b['id'] for b in lek['blokovi']], AI_IDS_SISTEMI)
            blok = lek['blokovi'][1]
            self.assertEqual(blok['tip'], 'slika')
            self.assertEqual(blok['poreklo'], 'ai-ilustracija')
            self.assertEqual(blok['sirina'], 'puna')
            self.assertEqual(blok['potpis'], 'Магматска комора. (AI ilustracija, šematski)')
            self.assertNotIn('nedostupan', blok)
            self.assertEqual((blok['sirina_px'], blok['visina_px']), (600, 448))
            # пре обраде: слика стиже као placeholder (image/*, 200)
            r = self.get(blok['url'])
            self.assertEqual(r.status_code, 200)
            self.assertTrue(r.mimetype.startswith('image/'), r.mimetype)
            # worker направи деривате → права слика (image/jpeg) из FOTOTEKA_MEDIA_PATH
            for _ in range(50):
                posao = fototeka_jobs.claim_next_job()
                if posao is None:
                    break
                fototeka_jobs.process_job(posao)
            self.assertEqual(_upit('SELECT status FROM fotografije WHERE id = %s', (blok['fotografija_id'],))[0][0],
                             'spremna')
            r = self.get(blok['url'])
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.mimetype, 'image/jpeg')
            self.assertGreater(len(r.data), 1000)
            r = self.get(blok['url_mala'])
            self.assertEqual((r.status_code, r.mimetype), (200, 'image/jpeg'))


if __name__ == '__main__':
    unittest.main()
