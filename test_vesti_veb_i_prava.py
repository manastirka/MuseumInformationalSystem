#!/usr/bin/env python3
"""Тестови за право уређивања вести и за претрагу вести на вебу.

Провере иду до базе (`museum_system_test`). Синтетички идентитети носе
ознаку у `upit` односно `keywords`, па чишћење не иде по префиксу наслова.
"""

import os
import unittest
from pathlib import Path
from datetime import datetime, timezone

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', 'logs/qa_flask_session')

import app as museum_app  # noqa: E402
import museum_news_store as skladiste  # noqa: E402
import museum_news_slike as slike  # noqa: E402
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


class SlikeTest(unittest.TestCase):
    """Слика мора да стигне из фида или са странице чланка — и да се упише."""

    def setUp(self):
        _ocisti()
        self.addCleanup(_ocisti)

    def _stavka(self, dodatno=''):
        return (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<rss xmlns:media="http://search.yahoo.com/mrss/"><channel><item>'
            '<title>Природњачки музеј у Београду добија нову зграду</title>'
            '<link>https://primer.invalid/vest-1</link>'
            '<description>Опис вести довољно дуг да прође проверу дужине.</description>'
            '<pubDate>Mon, 04 May 2026 10:00:00 GMT</pubDate>'
            + dodatno +
            '</item></channel></rss>').encode('utf-8')

    def test_slika_iz_media_content(self):
        nalazi = pretraga._razbori_odgovor(
            self._stavka('<media:content url="https://primer.invalid/s.jpg" '
                         'type="image/jpeg"/>'), 'medij', 'Тест')
        self.assertEqual(nalazi[0]['slika_url'], 'https://primer.invalid/s.jpg')

    def test_video_prilog_nije_slika(self):
        # Данас у media:content шаље YouTube везу — то није слика вести.
        nalazi = pretraga._razbori_odgovor(
            self._stavka('<media:content url="https://www.youtube.com/embed/x"/>'),
            'medij', 'Тест')
        self.assertIsNone(nalazi[0]['slika_url'])

    def test_slika_iz_html_opisa(self):
        nalazi = pretraga._razbori_odgovor(
            (self._stavka().decode('utf-8').replace(
                '<description>Опис',
                '<description>&lt;img src="https://primer.invalid/u.jpg"&gt;Опис')
             ).encode('utf-8'), 'medij', 'Тест')
        self.assertEqual(nalazi[0]['slika_url'], 'https://primer.invalid/u.jpg')

    def test_slika_se_upisuje_u_bazu(self):
        nalaz = {
            'kljuc': pretraga.kljuc_naslova('Вест о музеју са сликом'),
            'url': 'https://primer.invalid/a', 'naslov': 'Вест о музеју са сликом',
            'izvod': '', 'izvor_naziv': 'Тест', 'objavljeno': None,
            'slika_url': 'https://primer.invalid/slika.jpg',
            'upit': OZNAKA, 'pretrazivac': 'medij',
        }
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                self.assertTrue(pretraga._upisi_kandidata(cur, nalaz, 9, 'тест'))
                cur.execute('SELECT slika_url FROM news_web_kandidati '
                            'WHERE kljuc = %s', (nalaz['kljuc'],))
                self.assertEqual(cur.fetchone()['slika_url'],
                                 'https://primer.invalid/slika.jpg')
            conn.commit()

    def test_google_omot_se_ne_gadja_za_og_sliku(self):
        # Са Google омота се повуче Google-ов лого — горе од ниједне слике.
        self.assertIsNone(pretraga.preuzmi_og_sliku(
            'https://news.google.com/rss/articles/CBMiABC'))

    def test_odobrena_vest_nosi_sliku_dalje(self):
        kandidat_id = _ubaci_kandidata('Вест о музеју коју одобравам')
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute('UPDATE news_web_kandidati SET slika_url = %s '
                            'WHERE id = %s',
                            ('https://primer.invalid/foto.jpg', kandidat_id))
            conn.commit()

        _, _, vest_id = skladiste.odluci_o_kandidatu(
            kandidat_id, 'odobreno', ko=OZNAKA)

        self.assertEqual(skladiste.dohvati_vest(vest_id)['slika_url'],
                         'https://primer.invalid/foto.jpg')


class DopunaSlikaTest(unittest.TestCase):
    """Допуна слика мора да покрије и раније нађене кандидате."""

    def setUp(self):
        _ocisti()
        self.addCleanup(_ocisti)

    def test_dopuna_hvata_starog_kandidata_bez_nove_pretrage(self):
        # Кандидат нађен раније, без слике: следећа претрага не мора да
        # донесе ништа ново, а он свеједно мора да добије слику.
        kandidat_id = _ubaci_kandidata('Вест о музеју без слике',
                                       url='https://primer.invalid/clanak')

        # 1×1 PNG — довољно да pyvips направи стварну локалну копију.
        import base64
        PIKSEL = base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8'
            'z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==')

        class LaznaVeza:
            def get(self, url, **_kw):
                jeste_slika = url.endswith('.png')

                class O:
                    headers = {'Content-Type':
                               'image/png' if jeste_slika else 'text/html'}
                    content = (PIKSEL if jeste_slika else
                               b'<html><head><meta property="og:image" '
                               b'content="https://primer.invalid/og.png">'
                               b'</head></html>')

                    def raise_for_status(self):
                        return None

                    def iter_content(self, _n):
                        return iter([PIKSEL])

                o = O()
                o.url = url
                return o

        dopunjeno, pokusano = pretraga.dopuni_slike(session=LaznaVeza())

        self.assertEqual((dopunjeno, pokusano), (1, 1))
        self.assertEqual(_kandidat(kandidat_id)['slika_url'],
                         'https://primer.invalid/og.png')
        self.assertIsNotNone(_kandidat(kandidat_id)['slika_fajl'],
                             'без локалне копије CSP не приказује слику')

    def test_dopuna_preskace_google_omot(self):
        _ubaci_kandidata('Вест о музеју преко Google-а',
                         url='https://news.google.com/rss/articles/CBMiXYZ')

        class LaznaVeza:
            def get(self, *_a, **_kw):
                raise AssertionError('Google омот се не сме ни гађати')

        self.assertEqual(pretraga.dopuni_slike(session=LaznaVeza()), (0, 0))

    def test_pad_strane_ne_rusi_dopunu(self):
        kandidat_id = _ubaci_kandidata('Вест о музеју, страна не ради',
                                       url='https://primer.invalid/pukla')

        class LaznaVeza:
            def get(self, *_a, **_kw):
                raise RuntimeError('страна не одговара')

        dopunjeno, pokusano = pretraga.dopuni_slike(session=LaznaVeza())

        self.assertEqual((dopunjeno, pokusano), (0, 1))
        self.assertIsNone(_kandidat(kandidat_id)['slika_url'])


class CspSlikeTest(unittest.TestCase):
    """Слика мора да се сервира са НАШЕГ порекла — CSP блокира туђе домене."""

    def test_csp_ne_dozvoljava_domene_medija(self):
        # Ово је разлог зашто уопште чувамо локалну копију. Ако неко једног
        # дана дода домене медија у img-src, овај тест пада и натера га да
        # прочита зашто то није било решење.
        dozvoljeni = museum_app.app.config.get('SECURITY_HEADERS', {})
        import app as _a
        izvor = Path(_a.__file__).read_text(encoding='utf-8')
        pocetak = izvor.index("'img-src'")
        odeljak = izvor[pocetak:pocetak + 800]
        for domen in ('politika.rs', 'b92.net', 'ocdn.eu', 'rts.rs'):
            self.assertNotIn(domen, odeljak,
                             'домен медија у img-src — уместо тога се чува '
                             'локална копија, види museum_news_slike.py')
        del dozvoljeni

    def test_sablon_koristi_lokalnu_kopiju(self):
        strana = Path('templates/admin_news.html').read_text(encoding='utf-8')
        self.assertIn("vesti_slike/' ~ vest.slika_fajl", strana)
        pregled = Path('templates/news_review.html').read_text(encoding='utf-8')
        self.assertIn("vesti_slike/' ~ k.slika_fajl", pregled)

    def test_ime_fajla_stabilno_po_adresi(self):
        a = slike.ime_fajla('https://primer.invalid/x.jpg')
        self.assertEqual(a, slike.ime_fajla('https://primer.invalid/x.jpg'))
        self.assertNotEqual(a, slike.ime_fajla('https://primer.invalid/y.jpg'))
        self.assertTrue(a.endswith('.jpg'))

    def test_nije_slika_se_odbija(self):
        class LaznaVeza:
            def get(self, *_a, **_kw):
                class O:
                    headers = {'Content-Type': 'text/html'}
                    def raise_for_status(self): return None
                    def iter_content(self, _n): return iter([b'<html>'])
                return O()

        self.assertIsNone(slike.preuzmi('https://primer.invalid/strana.html',
                                        session=LaznaVeza()))

    def test_odobrena_vest_nosi_lokalnu_kopiju(self):
        kandidat_id = _ubaci_kandidata('Вест о музеју, локална копија')
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute('UPDATE news_web_kandidati SET slika_url = %s, '
                            'slika_fajl = %s WHERE id = %s',
                            ('https://primer.invalid/a.jpg', 'abc123.jpg',
                             kandidat_id))
            conn.commit()
        self.addCleanup(_ocisti)

        _, _, vest_id = skladiste.odluci_o_kandidatu(
            kandidat_id, 'odobreno', ko=OZNAKA)

        self.assertEqual(skladiste.dohvati_vest(vest_id)['slika_fajl'],
                         'abc123.jpg')


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


class FilterIzvoraTest(unittest.TestCase):
    """Филтер по извору мора да зна за сва три извора, не за два."""

    def setUp(self):
        _ocisti()
        self.addCleanup(_ocisti)
        kandidat_id = _ubaci_kandidata('Вест о музеју из медија')
        _, _, self.vest_id = skladiste.odluci_o_kandidatu(
            kandidat_id, 'odobreno', ko=OZNAKA)
        self.client = museum_app.app.test_client()
        with self.client.session_transaction() as sess:
            sess.update({'user_id': 1, 'user_email': 'admin@nhmbeo.rs',
                         'user_name': 'Тест', 'user_role': 'admin',
                         'is_admin': True})

    def test_skladiste_filtrira_veb(self):
        vesti, ukupno = skladiste.dohvati_vesti(izvor='veb', limit=100)
        self.assertGreaterEqual(ukupno, 1)
        self.assertTrue(all(v['izvor'] == 'veb' for v in vesti))
        self.assertIn(self.vest_id, [v['id'] for v in vesti])

    def test_ruta_ne_odbacuje_veb_kao_nepoznat_izvor(self):
        odgovor = self.client.get('/admin/news?izvor=veb',
                                  base_url='https://localhost')
        telo = odgovor.get_data(as_text=True)

        self.assertEqual(odgovor.status_code, 200)
        # Кад би 'veb' пао на None, страна би приказала и ручне вести.
        self.assertIn('Вест о музеју из медија', telo)
        self.assertIn('одговара филтеру', telo)


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
