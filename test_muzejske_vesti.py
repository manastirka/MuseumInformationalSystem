#!/usr/bin/env python3
"""Тестови за музејске вести: увоз са сајта, читање из базе и границе.

Свака провера иде до базе (`museum_system_test`), не до статуса 200.
Синтетички идентитети носе ознаку у `keywords` и `spoljni_id`, па чишћење
никад не иде по префиксу наслова.
"""

import os
import unittest

import requests

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', 'logs/qa_flask_session')

import app as museum_app  # noqa: E402
import museum_news_importer as uvoznik  # noqa: E402
import museum_news_store as skladiste  # noqa: E402
from postgres_service import get_postgres_connection  # noqa: E402
from psycopg.rows import dict_row  # noqa: E402

OZNAKA = 'test-muzejske-vesti@example.invalid'
TEST_SPOLJNI = ['900001', '900002', '900003']


def _post(spoljni_id, *, naslov, sadrzaj=None, izvod=None, izmenjen=None,
          slika=None, kategorija=None):
    """Минималан облик WordPress одговора какав уозник добија."""
    telo = sadrzaj if sadrzaj is not None else '<p>%s</p>' % naslov
    return {
        'id': spoljni_id,
        'date': '2026-03-04T10:00:00',
        'modified': izmenjen or '2026-03-04T10:00:00',
        'link': 'https://nhmbeo.rs/%s/' % spoljni_id,
        'author_name': 'Уредник сајта',
        'title': {'rendered': naslov},
        'excerpt': {'rendered': izvod if izvod is not None else telo},
        'content': {'rendered': telo},
        'categories_detail': ([{'slug': kategorija}] if kategorija else []),
        '_embedded': ({'wp:featuredmedia': [{'source_url': slika}]}
                      if slika else {}),
    }


class LaznaSesija:
    """Стоји уместо ``requests``: враћа припремљене одговоре по редоследу."""

    class _Odgovor:
        def __init__(self, podaci):
            self._podaci = podaci

        def raise_for_status(self):
            return None

        def json(self):
            return self._podaci

    def __init__(self, po_strani=None, greske_na=(), izuzetak=None):
        self.po_strani = po_strani or {}
        self.greske_na = set(greske_na)
        self.izuzetak = izuzetak
        self.pozivi = []

    def get(self, url, params=None, headers=None, timeout=None):
        parametri = params or {}
        self.pozivi.append(parametri)
        if self.izuzetak is not None:
            raise self.izuzetak
        kljuc = ('pomak', parametri['offset']) if 'offset' in parametri \
            else ('strana', parametri.get('page', 1))
        if kljuc in self.greske_na:
            # HTTPError = сајт је одговорио, само лоше; спасавање има смисла.
            raise requests.HTTPError('500 са сајта за %s' % (kljuc,))
        return self._Odgovor(self.po_strani.get(kljuc, []))


def _ocisti():
    with get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                'DELETE FROM news_articles WHERE spoljni_id = ANY(%s) '
                'OR keywords = %s', (TEST_SPOLJNI, OZNAKA))
            cur.execute('DELETE FROM news_import_log WHERE pokrenuo = %s',
                        (OZNAKA,))
        conn.commit()


def _red(spoljni_id):
    with get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT * FROM news_articles WHERE izvor = %s AND spoljni_id = %s',
                (uvoznik.IZVOR, str(spoljni_id)))
            return cur.fetchone()


def _poslednji_log():
    with get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT * FROM news_import_log WHERE pokrenuo = %s '
                'ORDER BY id DESC LIMIT 1', (OZNAKA,))
            return cur.fetchone()


def _ubaci_rucnu(naslov, *, tip='Вест', datum='2026-02-02'):
    with get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO news_articles (title, description, type, "
                "start_date, keywords, izvor) VALUES (%s, %s, %s, %s, %s, "
                "'rucni') RETURNING id",
                (naslov, 'Опис ручне вести', tip, datum, OZNAKA))
            vest_id = cur.fetchone()['id']
        conn.commit()
    return vest_id


class NormalizacijaTest(unittest.TestCase):
    """Оно што уђе са сајта мора да изађе као чист, употребљив текст."""

    def test_skida_tagove_i_ponovljen_naslov(self):
        naslov = 'Отворена изложба „Минерали Трепче“'
        post = _post('900001', naslov=naslov, sadrzaj=(
            '<p>%s Јуче је свечано отворена изложба у Крушевцу.</p>' % naslov))
        red = uvoznik.normalizuj(post)

        self.assertEqual(red['title'], naslov)
        self.assertNotIn('<p>', red['sadrzaj_tekst'])
        self.assertFalse(red['sadrzaj_tekst'].startswith(naslov),
                         'наслов се понавља на почетку текста')
        self.assertTrue(red['sadrzaj_tekst'].startswith('Јуче'))

    def test_izbacuje_gole_url_ove_medija(self):
        post = _post('900001', naslov='Вест са видеом', sadrzaj=(
            '<p>Увод https://nhmbeo.rs/wp-content/uploads/x.mp4 наставак.</p>'))
        red = uvoznik.normalizuj(post)

        self.assertNotIn('http', red['sadrzaj_tekst'])
        self.assertIn('Увод', red['sadrzaj_tekst'])
        self.assertIn('наставак', red['sadrzaj_tekst'])

    def test_mapira_tip_i_sliku(self):
        post = _post('900001', naslov='Изложба', kategorija='izlozbe',
                     slika='https://nhmbeo.rs/slika.jpg')
        red = uvoznik.normalizuj(post)

        self.assertEqual(red['type'], 'Изложба')
        self.assertEqual(red['slika_url'], 'https://nhmbeo.rs/slika.jpg')

    def test_bez_naslova_se_preskace(self):
        self.assertIsNone(uvoznik.normalizuj(_post('900001', naslov='   ')))


class UvozTest(unittest.TestCase):
    """Увоз пише у базу, понавља се без дупликата и никад не ћути о квару."""

    def setUp(self):
        _ocisti()
        self.addCleanup(_ocisti)

    def test_upisuje_u_bazu_i_belezi_uspeh(self):
        sesija = LaznaSesija(po_strani={
            ('strana', 1): [_post('900001', naslov='Прва вест'),
                            _post('900002', naslov='Друга вест')],
        })
        ishod = uvoznik.uvezi_vesti(strana_do=1, pokrenuo=OZNAKA,
                                    session=sesija)

        self.assertEqual(ishod['status'], 'uspeh')
        self.assertEqual(ishod['novih'], 2)
        self.assertIsNotNone(_red('900001'))
        self.assertEqual(_red('900002')['izvor'], 'nhmbeo')
        self.assertEqual(_poslednji_log()['status'], 'uspeh')

    def test_ponovljen_uvoz_ne_pravi_duplikate(self):
        strane = {('strana', 1): [_post('900001', naslov='Прва вест')]}
        uvoznik.uvezi_vesti(strana_do=1, pokrenuo=OZNAKA,
                            session=LaznaSesija(po_strani=strane))
        drugi = uvoznik.uvezi_vesti(strana_do=1, pokrenuo=OZNAKA,
                                    session=LaznaSesija(po_strani=strane))

        self.assertEqual(drugi['novih'], 0)
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT count(*) AS broj FROM news_articles '
                    'WHERE izvor = %s AND spoljni_id = %s',
                    (uvoznik.IZVOR, '900001'))
                self.assertEqual(cur.fetchone()['broj'], 1)

    def test_izmena_na_sajtu_azurira_red(self):
        uvoznik.uvezi_vesti(strana_do=1, pokrenuo=OZNAKA, session=LaznaSesija(
            po_strani={('strana', 1): [_post('900001', naslov='Стари наслов')]}))
        uvoznik.uvezi_vesti(strana_do=1, pokrenuo=OZNAKA, session=LaznaSesija(
            po_strani={('strana', 1): [
                _post('900001', naslov='Нови наслов',
                      izmenjen='2026-05-05T08:00:00')]}))

        self.assertEqual(_red('900001')['title'], 'Нови наслов')

    def test_pad_mreze_ne_prolazi_tiho(self):
        sesija = LaznaSesija(izuzetak=RuntimeError('мрежа не ради'))

        with self.assertRaises(RuntimeError):
            uvoznik.uvezi_vesti(strana_do=1, pokrenuo=OZNAKA, session=sesija)

        log = _poslednji_log()
        self.assertEqual(log['status'], 'greska')
        self.assertIn('мрежа не ради', log['poruka'])

    def test_pala_strana_se_spasava_objavu_po_objavu(self):
        # Страна 2 враћа 500, али појединачне објаве са ње се могу повући —
        # једна покварена објава не сме да однесе целу страну вести.
        pocetak = uvoznik.PER_PAGE
        po_strani = {
            ('pomak', pocetak): [_post('900002', naslov='Друга вест')],
            ('pomak', pocetak + 1): [_post('900003', naslov='Трећа вест')],
        }
        greske = {('strana', 2)}
        greske.update(('pomak', pocetak + k)
                      for k in range(2, uvoznik.PER_PAGE))
        sesija = LaznaSesija(po_strani=po_strani, greske_na=greske)

        ishod = uvoznik.uvezi_vesti(strana_od=2, strana_do=2, pokrenuo=OZNAKA,
                                    session=sesija)

        self.assertEqual(ishod['status'], 'delimicno',
                         'делимичан увоз не сме да се пријави као успех')
        self.assertEqual(ishod['preskoceno'], uvoznik.PER_PAGE - 2)
        self.assertIsNotNone(_red('900002'))
        self.assertIsNotNone(_red('900003'))
        self.assertEqual(_poslednji_log()['status'], 'delimicno')

    def test_potpun_pad_sajta_ne_daje_delimican_uspeh(self):
        # Сваки покушај пада: ниједна објава није стигла — то је грешка,
        # никад „делимично", и изузетак иде даље.
        pocetak = uvoznik.PER_PAGE
        greske = {('strana', 2)}
        greske.update(('pomak', pocetak + k) for k in range(uvoznik.PER_PAGE))

        with self.assertRaises(Exception):
            uvoznik.uvezi_vesti(strana_od=2, strana_do=2, pokrenuo=OZNAKA,
                                session=LaznaSesija(greske_na=greske))

        self.assertEqual(_poslednji_log()['status'], 'greska')


class SkladisteTest(unittest.TestCase):
    """Читање иде у базу и филтери раде над стварним редовима."""

    def setUp(self):
        _ocisti()
        self.addCleanup(_ocisti)
        uvoznik.uvezi_vesti(strana_do=1, pokrenuo=OZNAKA, session=LaznaSesija(
            po_strani={('strana', 1): [
                _post('900001', naslov='Уве3ена вест о минералима',
                      kategorija='izlozbe'),
                _post('900002', naslov='Увезена вест о фосилима'),
            ]}))
        self.rucna_id = _ubaci_rucnu('Ручна вест о инсектима')

    def test_filtrira_po_izvoru(self):
        sa_sajta, _ = skladiste.dohvati_vesti(izvor='nhmbeo', limit=100)
        self.assertTrue(all(v['izvor'] == 'nhmbeo' for v in sa_sajta))
        self.assertNotIn(self.rucna_id, [v['id'] for v in sa_sajta])

    def test_pretraga_nalazi_deo_reci(self):
        nadjene, ukupno = skladiste.dohvati_vesti(upit='минерал', limit=100)
        self.assertGreaterEqual(ukupno, 1)
        self.assertTrue(any('минерал' in v['title'].lower()
                            for v in nadjene))

    def test_stranicenje_vraca_ukupan_broj(self):
        prva, ukupno = skladiste.dohvati_vesti(limit=1, pomak=0)
        self.assertEqual(len(prva), 1)
        self.assertGreater(ukupno, 1, 'ukupno mora da broji sve, ne stranicu')

    def test_uvezena_vest_se_ne_brise_kroz_aplikaciju(self):
        vest = _red('900001')
        obrisano, poruka = skladiste.obrisi_vest(vest['id'])

        self.assertFalse(obrisano)
        self.assertIn('сајт', poruka)
        self.assertIsNotNone(_red('900001'), 'ред мора да остане у бази')

    def test_rucna_vest_se_brise(self):
        obrisano, _ = skladiste.obrisi_vest(self.rucna_id)

        self.assertTrue(obrisano)
        self.assertIsNone(skladiste.dohvati_vest(self.rucna_id))


class RuteTest(unittest.TestCase):
    """Стране се исцртавају, а границе враћају одбијање уместо тихог успеха."""

    def setUp(self):
        _ocisti()
        self.addCleanup(_ocisti)
        self.client = museum_app.app.test_client()
        uvoznik.uvezi_vesti(strana_do=1, pokrenuo=OZNAKA, session=LaznaSesija(
            po_strani={('strana', 1): [
                _post('900001', naslov='Увезена вест за приказ',
                      slika='https://nhmbeo.rs/slika.jpg')]}))

    def _prijava(self, role='admin'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = OZNAKA
            sess['user_name'] = 'Тест Кустос'
            sess['user_role'] = role
            sess['is_admin'] = role == 'admin'

    def test_strana_vesti_prikazuje_uvezenu_vest(self):
        self._prijava()
        odgovor = self.client.get('/admin/news',
                                  base_url='https://localhost')

        self.assertEqual(odgovor.status_code, 200)
        self.assertIn('Увезена вест за приказ', odgovor.get_data(as_text=True))

    def test_strana_citanja_radi(self):
        self._prijava()
        vest = _red('900001')
        odgovor = self.client.get('/admin/news/%d' % vest['id'],
                                  base_url='https://localhost')

        self.assertEqual(odgovor.status_code, 200)
        self.assertIn('Увезена вест за приказ', odgovor.get_data(as_text=True))

    def test_nepostojeca_vest_daje_404(self):
        self._prijava()
        odgovor = self.client.get('/admin/news/99999999',
                                  base_url='https://localhost')
        self.assertEqual(odgovor.status_code, 404)

    def test_izmena_uvezene_vesti_se_odbija_i_red_ostaje_isti(self):
        self._prijava()
        vest = _red('900001')

        odgovor = self.client.post(
            '/api/news/save',
            json={'id': vest['id'], 'title': 'Подметнут наслов',
                  'description': 'Подметнут опис'},
            base_url='https://localhost')

        self.assertEqual(odgovor.status_code, 409)
        self.assertFalse(odgovor.get_json()['success'])
        self.assertEqual(_red('900001')['title'], 'Увезена вест за приказ')

    def test_xss_u_naslovu_izlazi_escape_ovan(self):
        self._prijava()
        napad = '<img src=x onerror=alert(1)>'
        vest_id = _ubaci_rucnu('Вест %s' % napad)

        odgovor = self.client.get('/admin/news/%d' % vest_id,
                                  base_url='https://localhost')
        telo = odgovor.get_data(as_text=True)

        self.assertEqual(odgovor.status_code, 200)
        self.assertNotIn(napad, telo)
        self.assertIn('&lt;img src=x onerror=alert(1)&gt;', telo)


if __name__ == '__main__':
    unittest.main()
