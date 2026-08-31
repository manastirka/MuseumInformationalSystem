#!/usr/bin/env python3
"""Тестови за право уређивања вести и за претрагу вести на вебу.

Провере иду до базе (`museum_system_test`). Синтетички идентитети носе
ознаку у `upit` односно `keywords`, па чишћење не иде по префиксу наслова.
"""

import os
import unittest
from datetime import datetime, timezone

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', 'logs/qa_flask_session')

import app as museum_app  # noqa: E402
import museum_news_store as skladiste  # noqa: E402
import museum_news_web_search as pretraga  # noqa: E402
from postgres_service import get_postgres_connection  # noqa: E402
from psycopg.rows import dict_row  # noqa: E402

OZNAKA = 'test-vesti-veb@example.invalid'


def _ocisti():
    with get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                'DELETE FROM news_articles WHERE id IN ('
                '  SELECT vest_id FROM news_web_kandidati '
                '  WHERE upit = %s AND vest_id IS NOT NULL)', (OZNAKA,))
            cur.execute('DELETE FROM news_web_kandidati WHERE upit = %s',
                        (OZNAKA,))
            cur.execute('DELETE FROM news_articles WHERE keywords = %s',
                        (OZNAKA,))
            cur.execute('DELETE FROM news_import_log WHERE pokrenuo = %s',
                        (OZNAKA,))
        conn.commit()


def _ubaci_kandidata(naslov, *, ocena=9, url='https://primer.invalid/vest',
                     izvor_naziv='Тест медиј'):
    with get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO news_web_kandidati (kljuc, url, naslov, izvod, '
                'izvor_naziv, objavljeno, upit, pretrazivac, ocena, razlog) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
                (pretraga.kljuc_naslova(naslov), url, naslov, 'Извод вести',
                 izvor_naziv, datetime(2026, 5, 5, tzinfo=timezone.utc),
                 OZNAKA, 'test', ocena, 'тест'))
            return cur.fetchone()['id']


def _kandidat(kandidat_id):
    with get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM news_web_kandidati WHERE id = %s',
                        (kandidat_id,))
            return cur.fetchone()


class OcenaRelevantnostiTest(unittest.TestCase):
    """Оцена мора да пусти наш музеј, а да одбије истоимене музеје."""

    def test_pusta_nas_muzej(self):
        ocena, _ = pretraga.oceni(
            'Природњачки музеј у Београду прославио 129 година', '', '')
        self.assertGreaterEqual(ocena, pretraga.PRAG)

    def test_hvata_i_deklinirane_oblike(self):
        # Google даје само наслов; „Природњачког музеја" мора да прође исто
        # као и „Природњачки музеј", иначе пола вести не стигне до кустоса.
        for naslov in ('Отворена изложба Природњачког музеја у Београду',
                       'Гости у Природњачком музеју',
                       'Prirodnjackog muzeja nova zgrada'):
            with self.subTest(naslov=naslov):
                ocena, _ = pretraga.oceni(naslov, '', '')
                self.assertGreaterEqual(ocena, pretraga.PRAG, naslov)

    def test_odbija_muzej_u_svilajncu(self):
        ocena, razlog = pretraga.oceni(
            'Природњачки музеј у Свилајнцу обара рекорде посећености, '
            'бољи и од Београда', '', '')
        self.assertLess(ocena, pretraga.PRAG)
        self.assertIn('Свилајнцу', razlog)

    def test_odbija_strane_muzeje(self):
        for naslov in ('Prirodnjački muzej u Londonu otvara novu galeriju',
                       'Природњачки музеј у Њујорку добија донацију'):
            with self.subTest(naslov=naslov):
                ocena, _ = pretraga.oceni(naslov, '', '')
                self.assertLess(ocena, pretraga.PRAG, naslov)

    def test_beograd_bez_muzeja_ne_prolazi(self):
        ocena, _ = pretraga.oceni('Београд добија нови кеј и аквaријум', '', '')
        self.assertLess(ocena, pretraga.PRAG)

    def test_kljuc_zanemaruje_ime_medija(self):
        # Исти чланак преко Google-а („… - Данас") и Bing-а мора да добије
        # исти кључ, иначе се у реду за преглед појави двапут.
        a = pretraga.kljuc_naslova('Нова зграда музеја - Данас')
        b = pretraga.kljuc_naslova('Нова зграда музеја')
        self.assertEqual(a, b)


class RedZaPregledTest(unittest.TestCase):
    """Одлука кустоса мора да буде трајна и атомична."""

    def setUp(self):
        _ocisti()
        self.addCleanup(_ocisti)

    def test_odobravanje_pravi_vest(self):
        kandidat_id = _ubaci_kandidata('Вест о музеју за одобравање')
        uspelo, _, vest_id = skladiste.odluci_o_kandidatu(
            kandidat_id, 'odobreno', ko=OZNAKA)

        self.assertTrue(uspelo)
        vest = skladiste.dohvati_vest(vest_id)
        self.assertIsNotNone(vest)
        self.assertEqual(vest['izvor'], 'veb')
        self.assertEqual(vest['source_link'], 'https://primer.invalid/vest')
        self.assertEqual(_kandidat(kandidat_id)['status'], 'odobreno')

    def test_odbacivanje_ne_pravi_vest(self):
        kandidat_id = _ubaci_kandidata('Вест о музеју за одбацивање')
        uspelo, _, vest_id = skladiste.odluci_o_kandidatu(
            kandidat_id, 'odbaceno', ko=OZNAKA)

        self.assertTrue(uspelo)
        self.assertIsNone(vest_id)
        self.assertEqual(_kandidat(kandidat_id)['status'], 'odbaceno')

    def test_druga_odluka_o_istoj_vesti_se_odbija(self):
        kandidat_id = _ubaci_kandidata('Вест о музеју, двострука одлука')
        skladiste.odluci_o_kandidatu(kandidat_id, 'odobreno', ko=OZNAKA)
        uspelo, poruka, _ = skladiste.odluci_o_kandidatu(
            kandidat_id, 'odbaceno', ko=OZNAKA)

        self.assertFalse(uspelo)
        self.assertIn('већ', poruka)
        self.assertEqual(_kandidat(kandidat_id)['status'], 'odobreno')

    def test_odbacena_vest_se_ne_nudi_ponovo(self):
        naslov = 'Вест о музеју коју кустос не жели'
        kandidat_id = _ubaci_kandidata(naslov)
        skladiste.odluci_o_kandidatu(kandidat_id, 'odbaceno', ko=OZNAKA)

        # Иста вест стигне у следећој претрази: upsert не сме да је врати
        # на чекање, иначе кустос сваки дан одбацује исто.
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                nov = pretraga._upisi_kandidata(
                    cur,
                    {'kljuc': pretraga.kljuc_naslova(naslov),
                     'url': 'https://primer.invalid/vest',
                     'naslov': naslov, 'izvod': '', 'izvor_naziv': 'Тест',
                     'objavljeno': None, 'upit': OZNAKA,
                     'pretrazivac': 'test'},
                    9, 'тест')
            conn.commit()

        self.assertFalse(nov)
        self.assertEqual(_kandidat(kandidat_id)['status'], 'odbaceno')

    def test_nepoznata_odluka_ne_menja_nista(self):
        kandidat_id = _ubaci_kandidata('Вест о музеју, погрешна одлука')
        uspelo, _, _ = skladiste.odluci_o_kandidatu(
            kandidat_id, 'obrisi', ko=OZNAKA)

        self.assertFalse(uspelo)
        self.assertEqual(_kandidat(kandidat_id)['status'], 'na_cekanju')


class PravoUredjivanjaTest(unittest.TestCase):
    """`news_edit` дели читање вести од уређивања."""

    def setUp(self):
        _ocisti()
        self.addCleanup(_ocisti)
        self.client = museum_app.app.test_client()

    def _prijava(self, role, email):
        with self.client.session_transaction() as sess:
            sess.clear()
            sess.update({'user_id': 1, 'user_email': email,
                         'user_name': 'Тест', 'user_role': role,
                         'is_admin': role == 'admin'})

    def test_kljuc_postoji_medju_modulima(self):
        # Екран „Управљање приступом" исцртава модуле из овог речника; без
        # кључа админ нема где да дода корисника.
        self.assertIn('news_edit', museum_app.MODULE_ACCESS)
        self.assertFalse(
            museum_app.MODULE_ACCESS['news_edit']['default_access'])

    def test_zaposleni_vidi_vesti_ali_ne_sme_da_ih_menja(self):
        self._prijava('employee', 'obican@example.invalid')

        prikaz = self.client.get('/admin/news', base_url='https://localhost')
        self.assertEqual(prikaz.status_code, 200)
        self.assertNotIn('dugmeNovaVest', prikaz.get_data(as_text=True))

        upis = self.client.post(
            '/api/news/save',
            json={'title': 'Подметнута вест', 'description': 'Опис'},
            base_url='https://localhost')
        self.assertEqual(upis.status_code, 403)

        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT count(*) AS broj FROM news_articles '
                            'WHERE title = %s', ('Подметнута вест',))
                self.assertEqual(cur.fetchone()['broj'], 0,
                                 'одбијен упис не сме да остави ред у бази')

    def test_zaposleni_ne_moze_da_odlucuje_o_nadjenim_vestima(self):
        kandidat_id = _ubaci_kandidata('Вест о музеју, покушај без права')
        self._prijava('employee', 'obican@example.invalid')

        odgovor = self.client.post(
            '/api/news/web/%d/odluka' % kandidat_id,
            json={'odluka': 'odobreno'}, base_url='https://localhost')

        self.assertEqual(odgovor.status_code, 403)
        self.assertEqual(_kandidat(kandidat_id)['status'], 'na_cekanju')

    def test_admin_sme_sve(self):
        self._prijava('admin', 'admin@nhmbeo.rs')

        prikaz = self.client.get('/admin/news', base_url='https://localhost')
        self.assertIn('dugmeNovaVest', prikaz.get_data(as_text=True))
        self.assertEqual(
            self.client.get('/admin/news/sa-veba',
                            base_url='https://localhost').status_code, 200)

    def test_direktor_sme_da_uredjuje(self):
        # Parity одлука 06/2026: изузеци су само password manager, SMTP,
        # системска подешавања и DB — вести нису међу њима.
        self._prijava('direktor', 'direktor@example.invalid')
        self.assertEqual(
            self.client.get('/admin/news/sa-veba',
                            base_url='https://localhost').status_code, 200)


if __name__ == '__main__':
    unittest.main()
