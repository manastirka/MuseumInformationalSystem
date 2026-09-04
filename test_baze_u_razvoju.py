#!/usr/bin/env python3
"""Мени „Базе података": база без стварних података иде у подмени „У развоју"
и сама се враћа у свој одељак чим добије први стварни запис."""

import os
import unittest
from unittest import mock

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', 'logs/qa_flask_session')

import app as museum_app  # noqa: E402
import museum_baze_stanje as stanje  # noqa: E402
from postgres_service import get_postgres_connection  # noqa: E402

BAZA = 'https://localhost'
KATALOG = 'RAZVOJTEST-BOT-1'


def _ocisti():
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM collection_specimens WHERE catalog_number LIKE 'RAZVOJTEST-%%'")
        conn.commit()
    stanje.osvezi()


def _ubaci_botaniku(katalog=KATALOG):
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            # тест база нема шифарник типова збирки; FK тражи ред
            cur.execute("INSERT INTO collection_types (code, name_sr) VALUES (%s, %s) "
                        "ON CONFLICT DO NOTHING", ('botany', 'Ботаника'))
            cur.execute(
                "INSERT INTO collection_specimens (catalog_number, collection_type, scientific_name) "
                "VALUES (%s, 'botany', 'Testus realis')", (katalog,))
        conn.commit()
    stanje.osvezi()


class LogikaTest(unittest.TestCase):
    def tearDown(self):
        stanje.osvezi()

    def test_pad_baze_nista_ne_skriva(self):
        with mock.patch.object(stanje, 'izbroj_stvarne_redove', return_value={}):
            stanje.osvezi()
            self.assertFalse(stanje.u_razvoju('botany_collection'))
            self.assertEqual(stanje.stavke_u_razvoju(), [])
        with mock.patch.object(stanje, 'izbroj_stvarne_redove',
                               return_value={'botany_collection': None, 'exhibits_database': 0}):
            stanje.osvezi()
            self.assertFalse(stanje.u_razvoju('botany_collection'))
            self.assertTrue(stanje.u_razvoju('exhibits_database'))
            self.assertEqual([s['kljuc'] for s in stanje.stavke_u_razvoju()], ['exhibits_database'])

    def test_kes_ne_ide_u_bazu_pre_isteka(self):
        with mock.patch.object(stanje, 'izbroj_stvarne_redove', return_value={'exhibits_database': 0}) as brojac:
            stanje.osvezi()
            stanje.u_razvoju('exhibits_database')
            stanje.u_razvoju('exhibits_database')
            stanje.stavke_u_razvoju()
            self.assertEqual(brojac.call_count, 1)

    def test_seme_nije_stvaran_podatak(self):
        # Демо каталошки бројеви из децембра 2025. не смеју да „оживе" базу.
        self.assertIn('BOT-2024-001', stanje._SEME_ZBIRKI['botany'])
        self.assertFalse(hasattr(stanje, '_SEME_METEORITI'), 'метеорити су стварна збирка — без семена')
        for s in stanje.NAV_BAZE:
            self.assertIn(s['modul'], museum_app.MODULE_ACCESS, s['kljuc'])


class BazaIMeniTest(unittest.TestCase):
    def setUp(self):
        _ocisti()
        self.addCleanup(_ocisti)
        self.client = museum_app.app.test_client()
        with self.client.session_transaction() as sess:
            sess.update({'user_id': 1, 'user_email': 'admin@example.invalid', 'user_name': 'Тест',
                         'user_role': 'admin', 'is_admin': True})

    def _meni(self):
        odgovor = self.client.get('/dashboard', base_url=BAZA)
        self.assertEqual(odgovor.status_code, 200)
        telo = odgovor.get_data(as_text=True)
        # Лева трака (без префикса) — мобилна фиока понавља исто стабло са „m-“ префиксом.
        poc = telo.index('id="databasesDropdown"')
        kraj = telo.find('id="m-databasesDropdown"', poc + 1)
        return telo[poc:kraj if kraj > 0 else None]

    def test_prazna_zbirka_je_u_razvoju_a_sa_zapisom_se_vraca(self):
        # тест база: collection_specimens празна → ботаника у развоју
        self.assertTrue(stanje.u_razvoju('botany_collection'))
        meni = self._meni()
        self.assertIn('id="uRazvojuSubmenu"', meni)
        razvoj = meni.index('id="uRazvojuSubmenu"')
        biologija = meni.index('id="biologySubmenu"')
        prva_botanika = meni.index('Ботаничка збирка')
        self.assertGreater(prva_botanika, razvoj, 'ботаника без података не сме у одељак Биологија')
        self.assertLess(biologija, razvoj)

        _ubaci_botaniku()
        self.assertFalse(stanje.u_razvoju('botany_collection'))
        meni = self._meni()
        razvoj = meni.index('id="uRazvojuSubmenu"')
        prva_botanika = meni.index('Ботаничка збирка')
        self.assertLess(prva_botanika, razvoj, 'са стварним записом ботаника мора назад у Биологију')
        self.assertEqual(meni.count('Ботаничка збирка'), 1)

    def test_seme_ne_vraca_zbirku_iz_razvoja(self):
        _ubaci_botaniku('BOT-2024-001')
        self.assertTrue(stanje.u_razvoju('botany_collection'))
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM collection_specimens WHERE catalog_number = 'BOT-2024-001' "
                            "AND scientific_name = 'Testus realis'")
            conn.commit()
        stanje.osvezi()


if __name__ == '__main__':
    unittest.main()
