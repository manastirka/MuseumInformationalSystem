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

import app as museum_app  # noqa: E402
import local_rruff_data  # noqa: E402
import pretraga  # noqa: E402
import udzbenik  # noqa: E402
from postgres_service import get_postgres_connection  # noqa: E402

KOREN = Path(__file__).resolve().parent
PRIMER = KOREN / 'udzbenik' / 'primer-minerali.json'
BUNDLE_FAJLOVI = ('README.md', 'udzbenik.js', 'udzbenik-three.js', 'udzbenik.css', 'VERZIJA.txt')
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
        """Bundle (README списак + rezerve/<scena>.png за сваку сцену из шеме)
        мора бити праћен у git-у — глобално *.png је 2026-10-29 тихо
        прогутало резервне слике, па свеж клон/прод не би имао пад без WebGL-a."""
        readme = (KOREN / 'static' / 'udzbenik' / 'README.md').read_text(encoding='utf-8')
        iz_readme = sorted(set(re.findall(r'`([\w-]+\.(?:js|css|txt))`', readme)))
        self.assertIn('udzbenik-three.js', iz_readme)
        sema = json.loads((KOREN / 'udzbenik' / 'schema' / 'lekcija.schema.json').read_text(encoding='utf-8'))
        scene = sema['$defs']['scena']['properties']['scena']['enum']
        self.assertGreaterEqual(len(scene), 5)
        ocekivani = ['static/udzbenik/' + ime for ime in iz_readme]
        ocekivani += ['static/udzbenik/rezerve/%s.png' % scena for scena in scene]
        praceni = set(subprocess.run(['git', 'ls-files', '--', 'static/udzbenik'], cwd=KOREN, check=True,
                                     capture_output=True, text=True).stdout.split())
        self.assertEqual([f for f in ocekivani if f not in praceni], [], 'нису у git-у')
        ignorisani = subprocess.run(['git', 'check-ignore', '--no-index', '--', *ocekivani], cwd=KOREN,
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


if __name__ == '__main__':
    unittest.main()
