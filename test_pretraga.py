#!/usr/bin/env python3
"""Глобална претрага (Ctrl+K): нормализација, ILIKE ескејп, API са правима,
резултати из тест базе (`museum_system_test`): тест упише минерал са
инвентарним бројем PRETRAGATEST-… и очисти га."""
import os
import unittest
from unittest import mock

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', 'logs/qa_flask_session')

import app as museum_app  # noqa: E402
import pretraga  # noqa: E402
from postgres_service import get_postgres_connection  # noqa: E402

BAZA = 'https://localhost'
INV = 'PRETRAGATEST-77'


def _ocisti():
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM minerals WHERE inventory_number LIKE 'PRETRAGATEST-%%'")
        conn.commit()


def _ubaci_mineral():
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO minerals (inventory_number, item_name, card_locality) VALUES (%s, %s, %s) RETURNING id",
                        (INV, 'Тестни халкозин 100%_чист', 'Локалитет за претрагу'))
            mid = cur.fetchone()[0]
        conn.commit()
    return mid


class CisteFunkcijeTest(unittest.TestCase):
    def test_normalizacija_upita(self):
        self.assertIsNone(pretraga.normalizuj_upit(''))
        self.assertIsNone(pretraga.normalizuj_upit(' a '))
        self.assertEqual(pretraga.normalizuj_upit('  кварц   М123 '), 'кварц М123')
        self.assertEqual(len(pretraga.normalizuj_upit('x' * 200)), pretraga.NAJVISE_ZNAKOVA)

    def test_sablon_eskejpuje_dzokere(self):
        self.assertEqual(pretraga.sablon('100%_a\\b'), '%100\\%\\_a\\\\b%')

    def test_varijante_pisma(self):
        self.assertEqual(pretraga.varijante('кварц'), ['кварц', 'kvarc'])
        self.assertEqual(pretraga.varijante('Kvarc'), ['Kvarc', 'кварц'])
        self.assertEqual(pretraga.varijante('Ђорђе'), ['Ђорђе', 'Đorđe'])
        self.assertEqual(pretraga.varijante('Ljubljana'), ['Ljubljana', 'љубљана'])
        self.assertEqual(pretraga.varijante('MET-007'), ['MET-007', 'мет-007'])
        self.assertEqual(len(pretraga.sabloni('кварц')), 2)


class ApiTest(unittest.TestCase):
    def setUp(self):
        _ocisti()
        self.addCleanup(_ocisti)
        self.client = museum_app.app.test_client()

    def _prijavi(self, role='admin'):
        with self.client.session_transaction() as sess:
            sess.update({'user_id': 1, 'user_email': 'pretraga@example.invalid', 'user_name': 'Тест',
                         'user_role': role, 'is_admin': role == 'admin'})

    def test_bez_prijave_nema_pristupa(self):
        r = self.client.get('/api/pretraga?q=kvarc', base_url=BAZA)
        self.assertIn(r.status_code, (302, 401))

    def test_prekratak_upit(self):
        self._prijavi()
        r = self.client.get('/api/pretraga?q=a', base_url=BAZA)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.get_json()['prekratko'])
        self.assertEqual(r.get_json()['grupe'], [])

    def test_nalazi_mineral_po_inventarnom_broju_nazivu_lokalitetu_i_drugom_pismu(self):
        mid = _ubaci_mineral()
        self._prijavi()
        for q in ('PRETRAGATEST-7', 'халкозин', 'halkozin', 'за претрагу'):
            r = self.client.get('/api/pretraga?q=' + q, base_url=BAZA)
            self.assertEqual(r.status_code, 200, q)
            grupe = {g['kljuc']: g for g in r.get_json()['grupe']}
            self.assertIn('minerali', grupe, q)
            urlovi = [s['url'] for s in grupe['minerali']['stavke']]
            self.assertIn('/admin/mineral_detail/%d' % mid, urlovi, q)
            self.assertTrue(grupe['minerali']['jos'], 'линк „сви резултати“ за минерале')
        stavka = next(s for s in grupe['minerali']['stavke'] if s['url'].endswith('/%d' % mid))
        self.assertIn('M' + INV, stavka['naslov'])
        self.assertIn('Локалитет за претрагу', stavka['opis'])

    def test_dzoker_je_obican_tekst(self):
        _ubaci_mineral()
        self._prijavi()
        # '%_ч' постоји дословно у називу; голи '%%' не сме да врати „све“
        r = self.client.get('/api/pretraga?q=%25_ч', base_url=BAZA)
        grupe = {g['kljuc']: g for g in r.get_json()['grupe']}
        self.assertIn('minerali', grupe)
        r = self.client.get('/api/pretraga?q=%25%25%25', base_url=BAZA)
        self.assertNotIn('minerali', {g['kljuc'] for g in r.get_json()['grupe']})

    def test_korisnik_bez_modula_ne_vidi_grupu(self):
        _ubaci_mineral()
        self._prijavi(role='user')
        with mock.patch.object(museum_app, 'user_has_module_access', return_value=False):
            r = self.client.get('/api/pretraga?q=PRETRAGATEST', base_url=BAZA)
        self.assertEqual(r.status_code, 200)
        self.assertNotIn('minerali', {g['kljuc'] for g in r.get_json()['grupe']})

    def test_pad_jedne_baze_ne_rusi_pretragu(self):
        _ubaci_mineral()
        self._prijavi()

        def pukni(cur, s):
            raise RuntimeError('нема табеле')

        izvori = tuple((k, n, i, d, (pukni if k == 'knjige' else f), j) for k, n, i, d, f, j in pretraga.IZVORI)
        with mock.patch.object(pretraga, 'IZVORI', izvori):
            r = self.client.get('/api/pretraga?q=PRETRAGATEST', base_url=BAZA)
        self.assertEqual(r.status_code, 200)
        self.assertIn('minerali', {g['kljuc'] for g in r.get_json()['grupe']})


class UgradnjaTest(unittest.TestCase):
    def test_dugme_modal_i_skripta_u_base(self):
        base = open('templates/base.html', encoding='utf-8').read()
        self.assertIn('data-pretraga-otvori', base)
        self.assertIn('id="pretragaModal"', base)
        self.assertIn('js/pretraga.js', base)
        nav = open('templates/_navigacija.html', encoding='utf-8').read()
        self.assertIn('data-pretraga-otvori', nav)


if __name__ == '__main__':
    unittest.main()
