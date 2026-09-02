#!/usr/bin/env python3
"""QR ознаке: резолвер, кутије, налепнице, права и API за телефон.

Провере иду до базе (`museum_system_test`). Тест упише један минерал у
`minerals` са инвентарним бројем QRTEST-… и чисти све што је направио; ознаке
се препознају по `napravio`.
"""

import os
import unittest
from unittest import mock

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', 'logs/qa_flask_session')

import app as museum_app  # noqa: E402
import museum_qr  # noqa: E402
from postgres_service import get_postgres_connection  # noqa: E402

KO = 'qr-test@example.invalid'
KUTIJA = 'QRTEST-KUTIJA 7, polica 2'
BAZA = 'https://localhost'


def _ocisti():
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM qr_oznake WHERE napravio = %s OR objekat_id LIKE 'QRTEST-%%' "
                        "OR objekat_id IN (SELECT id::text FROM minerals WHERE inventory_number LIKE 'QRTEST-%%')",
                        (KO,))
            cur.execute("DELETE FROM minerals WHERE inventory_number LIKE 'QRTEST-%%'")
        conn.commit()


def _ubaci_mineral(inv='QRTEST-1', naziv='Кварц тестни', kutija=KUTIJA):
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO minerals (inventory_number, item_name, storage_location, card_locality) "
                "VALUES (%s, %s, %s, %s) RETURNING id",
                (inv, naziv, kutija, 'Тестни локалитет'))
            mineral_id = cur.fetchone()[0]
        conn.commit()
    return mineral_id


class OznakaTest(unittest.TestCase):
    def test_normalizacija_tolerise_citanje_sa_nalepnice(self):
        self.assertEqual(museum_qr.normalizuj_oznaku(' 7k3m9q2h '), '7K3M9Q2H')
        self.assertEqual(museum_qr.normalizuj_oznaku('7K3MOQ2I'), '7K3M0Q21')
        self.assertIsNone(museum_qr.normalizuj_oznaku('7K3M9Q2'))
        self.assertIsNone(museum_qr.normalizuj_oznaku('UUUUUUUU'))
        self.assertIsNone(museum_qr.normalizuj_oznaku(None))

    def test_svg_bez_xml_prologa(self):
        svg = museum_qr.svg_kod('https://192.168.144.194/q/7K3M9Q2H')
        self.assertTrue(svg.startswith('<svg'), svg[:40])
        self.assertIn('</svg>', svg)

    def test_sadrzaj_kutije_isti_kao_zalepljena_nalepnica(self):
        red = {'vrsta': 'kutija', 'zbirka': 'minerals', 'objekat_id': '7, polica 2', 'oznaka': 'AAAAAAAA'}
        with mock.patch.object(museum_qr, 'bazna_adresa', return_value='https://192.168.144.194'):
            self.assertEqual(museum_qr.sadrzaj_koda(red),
                             'https://192.168.144.194/qr_box/minerals/7%2C%20polica%202')
            red['vrsta'] = 'primerak'
            self.assertEqual(museum_qr.sadrzaj_koda(red), 'https://192.168.144.194/q/AAAAAAAA')

    def test_bazna_adresa_bez_kose_crte_na_kraju(self):
        with mock.patch.dict(os.environ, {'QR_BAZNA_ADRESA': 'https://primer.invalid/'}):
            with mock.patch('admin_system_views.load_saved_settings', return_value={}):
                self.assertEqual(museum_qr.bazna_adresa(), 'https://primer.invalid')


class BazaTest(unittest.TestCase):
    def setUp(self):
        _ocisti()
        self.addCleanup(_ocisti)
        self.client = museum_app.app.test_client()
        self.mineral_id = _ubaci_mineral()

    def _prijava(self, role, email):
        with self.client.session_transaction() as sess:
            sess.clear()
            sess.update({'user_id': 1, 'user_email': email, 'user_name': 'Тест',
                         'user_role': role, 'is_admin': role == 'admin'})

    def test_dodela_je_idempotentna_i_broji_stampu(self):
        prvi = museum_qr.dodeli_oznaku('primerak', 'minerals', self.mineral_id, KO)
        drugi = museum_qr.dodeli_oznaku('primerak', 'minerals', self.mineral_id, KO)
        self.assertEqual(prvi['oznaka'], drugi['oznaka'])
        self.assertRegex(prvi['oznaka'], r'^[0-9A-HJKMNP-TV-Z]{8}$')
        self.assertEqual(prvi['stampano_puta'], 0)
        posle = museum_qr.zabelezi_stampu(prvi['oznaka'], KO)
        self.assertEqual(posle['stampano_puta'], 1)
        self.assertEqual(posle['poslednje_stampao'], KO)
        self.assertEqual(museum_qr.oznaka_za_objekat('primerak', 'minerals', self.mineral_id)['oznaka'],
                         prvi['oznaka'])

    def test_stara_ruta_kutije_javna_i_nepromenjena(self):
        # Облик залепљен на кутијама: без пријаве, са размацима и зарезом у имену.
        odgovor = self.client.get('/qr_box/minerals/QRTEST-KUTIJA%207%2C%20polica%202', base_url=BAZA)
        self.assertEqual(odgovor.status_code, 200)
        telo = odgovor.get_data(as_text=True)
        self.assertIn('Кварц тестни', telo)
        self.assertIn('QRTEST-1', telo)
        self.assertEqual(self.client.get('/qr_box/minerals/NEMA-TAKVE', base_url=BAZA).status_code, 404)

    def test_api_kutije_za_telefon(self):
        odgovor = self.client.get('/api/q/kutija/minerali/QRTEST-KUTIJA%207%2C%20polica%202', base_url=BAZA)
        self.assertEqual(odgovor.status_code, 200)
        podaci = odgovor.get_json()
        self.assertTrue(podaci['ok'])
        self.assertEqual(podaci['vrsta'], 'kutija')
        self.assertEqual(podaci['broj_minerala'], 1)
        self.assertEqual(podaci['minerali'][0]['inventarni_broj'], 'QRTEST-1')
        self.assertEqual(self.client.get('/api/q/kutija/minerali/NEMA', base_url=BAZA).status_code, 404)

    def test_nepoznata_oznaka(self):
        self.assertEqual(self.client.get('/q/ZZZZZZZZ', base_url=BAZA).status_code, 404)
        self.assertEqual(self.client.get('/q/nije-oznaka', base_url=BAZA).status_code, 404)
        odgovor = self.client.get('/api/q/ZZZZZZZZ', base_url=BAZA)
        self.assertEqual(odgovor.status_code, 404)
        self.assertFalse(odgovor.get_json()['ok'])

    def test_stari_qr_sistem_je_uklonjen(self):
        for putanja in ('/admin/qr_generator', '/admin/qr_select/botany',
                        '/admin/qr_boxes/minerals', '/qr_view/botany/BOT-1'):
            self._prijava('admin', 'admin@example.invalid')
            self.assertEqual(self.client.get(putanja, base_url=BAZA).status_code, 404, putanja)

    def test_dugme_dodeljuje_oznaku_pa_nalepnica_pa_resolver(self):
        self._prijava('admin', 'admin@example.invalid')
        odgovor = self.client.post('/api/qr/dodeli', json={
            'vrsta': 'primerak', 'zbirka': 'minerals', 'objekat_id': self.mineral_id,
        }, base_url=BAZA)
        self.assertEqual(odgovor.status_code, 200, odgovor.get_data(as_text=True))
        podaci = odgovor.get_json()
        oznaka = podaci['oznaka']
        self.assertTrue(podaci['sadrzaj'].endswith('/q/' + oznaka))
        # исти објекат → иста ознака
        ponovo = self.client.post('/api/qr/dodeli', json={
            'zbirka': 'mineral', 'objekat_id': str(self.mineral_id),
        }, base_url=BAZA).get_json()
        self.assertEqual(ponovo['oznaka'], oznaka)

        # налепница: SVG + бројач
        nalepnica = self.client.get(podaci['url_nalepnice'], base_url=BAZA)
        self.assertEqual(nalepnica.status_code, 200)
        telo = nalepnica.get_data(as_text=True)
        self.assertIn('<svg', telo)
        self.assertIn(oznaka, telo)
        self.assertIn('Кварц тестни', telo)
        self.assertEqual(museum_qr.dohvati_oznaku(oznaka)['stampano_puta'], 1)
        self.assertEqual(self.client.get(podaci['url_nalepnice'] + '?format=nema', base_url=BAZA).status_code, 400)

        # API за телефон
        api = self.client.get('/api/q/' + oznaka.lower(), base_url=BAZA).get_json()
        self.assertEqual(api['zbirka'], 'minerals')
        self.assertEqual(api['objekat_id'], str(self.mineral_id))
        self.assertEqual(api['url_detalja'], f'/admin/mineral_detail/{self.mineral_id}')

        # пријављен са приступом → детаљи
        skok = self.client.get('/q/' + oznaka, base_url=BAZA)
        self.assertEqual(skok.status_code, 302)
        self.assertTrue(skok.headers['Location'].endswith(f'/admin/mineral_detail/{self.mineral_id}'))

        # непријављен → јавна картица без депоа
        with self.client.session_transaction() as sess:
            sess.clear()
        kartica = self.client.get('/q/' + oznaka, base_url=BAZA)
        self.assertEqual(kartica.status_code, 200)
        telo = kartica.get_data(as_text=True)
        self.assertIn('Кварц тестни', telo)
        self.assertIn('Пријава', telo)
        self.assertNotIn(KUTIJA, telo, 'јавна картица не сме да открије кутију/депо')
        self.assertEqual(self.client.get(podaci['url_nalepnice'], base_url=BAZA).status_code, 302)

    def test_dodela_bez_prava_ne_ostavlja_red(self):
        self._prijava('employee', 'obican@example.invalid')
        sme = museum_app.user_has_module_access('obican@example.invalid', 'employee', 'mineral_database')
        odgovor = self.client.post('/api/qr/dodeli', json={
            'zbirka': 'minerals', 'objekat_id': self.mineral_id}, base_url=BAZA)
        if sme:
            self.assertEqual(odgovor.status_code, 200)
        else:
            self.assertEqual(odgovor.status_code, 403)
            self.assertIsNone(museum_qr.oznaka_za_objekat('primerak', 'minerals', self.mineral_id))
        self.assertEqual(self.client.post('/api/qr/dodeli', json={
            'zbirka': 'minerals', 'objekat_id': 999999999}, base_url=BAZA).status_code,
            404 if sme else 403)
        self.assertEqual(self.client.post('/api/qr/dodeli', json={
            'zbirka': 'nepostojeca', 'objekat_id': 1}, base_url=BAZA).status_code, 400)

    def test_genericka_strana_detalja_i_kartica_za_zbirku(self):
        zapis = {'id': 777, 'catalog_number': 'QRTEST-BOT-777', 'scientific_name': 'Testus botanicus',
                 'family': 'Testaceae', 'storage_location': 'Депо Б, орман 3', 'collector': 'Тест'}
        with mock.patch.object(museum_app, 'get_qr_collection_records',
                               side_effect=lambda z: [zapis] if z == 'botany' else []):
            self._prijava('admin', 'admin@example.invalid')
            strana = self.client.get('/zbirka/botany/777', base_url=BAZA)
            self.assertEqual(strana.status_code, 200)
            telo = strana.get_data(as_text=True)
            self.assertIn('Testus botanicus', telo)
            self.assertIn('QR налепница', telo)
            self.assertEqual(self.client.get('/zbirka/botany/778', base_url=BAZA).status_code, 404)
            self.assertEqual(self.client.get('/zbirka/nema/1', base_url=BAZA).status_code, 404)

            red = museum_qr.dodeli_oznaku('primerak', 'botany', 777, KO)
            with self.client.session_transaction() as sess:
                sess.clear()
            kartica = self.client.get('/q/' + red['oznaka'], base_url=BAZA)
            self.assertEqual(kartica.status_code, 200)
            telo = kartica.get_data(as_text=True)
            self.assertIn('Testus botanicus', telo)
            self.assertIn('Testaceae', telo)
            self.assertNotIn('Депо Б', telo)
            self.assertEqual(self.client.get('/zbirka/botany/777', base_url=BAZA).status_code, 302)

    def test_nalepnice_kutija_dodeljuju_oznake(self):
        self._prijava('admin', 'admin@example.invalid')
        strana = self.client.get('/admin/qr/kutije/minerali', base_url=BAZA)
        self.assertEqual(strana.status_code, 200)
        self.assertIn(KUTIJA, strana.get_data(as_text=True))
        odgovor = self.client.post('/admin/qr/kutije/minerali/nalepnice',
                                   data={'kutije': [KUTIJA]}, base_url=BAZA)
        self.assertEqual(odgovor.status_code, 200)
        telo = odgovor.get_data(as_text=True)
        self.assertIn('<svg', telo)
        self.assertIn('/qr_box/minerals/QRTEST-KUTIJA%207%2C%20polica%202', telo)
        red = museum_qr.oznaka_za_objekat('kutija', 'minerals', KUTIJA)
        self.assertIsNotNone(red)
        self.assertEqual(red['stampano_puta'], 1)
        # и /q/<ознака> кутије води на садржај кутије, без пријаве
        with self.client.session_transaction() as sess:
            sess.clear()
        self.assertIn('Кварц тестни', self.client.get('/q/' + red['oznaka'], base_url=BAZA).get_data(as_text=True))

    def test_detalji_minerala_nude_dugme_pa_znacku(self):
        self._prijava('admin', 'admin@example.invalid')
        pre = self.client.get(f'/admin/mineral_detail/{self.mineral_id}', base_url=BAZA)
        self.assertEqual(pre.status_code, 200)
        self.assertIn('id="qr-dodeli"', pre.get_data(as_text=True))
        red = museum_qr.dodeli_oznaku('primerak', 'minerals', self.mineral_id, KO)
        posle = self.client.get(f'/admin/mineral_detail/{self.mineral_id}', base_url=BAZA).get_data(as_text=True)
        self.assertNotIn('id="qr-dodeli"', posle)
        self.assertIn(red['oznaka'], posle)
        self.assertIn(f"/q/{red['oznaka']}/nalepnica", posle)


if __name__ == '__main__':
    unittest.main()
