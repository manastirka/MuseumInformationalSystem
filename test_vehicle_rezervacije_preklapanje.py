"""Revizija 2026-08 (batch 6, stavka 9): dvostruko rezervisanje vozila.

Nalaz: vehicle_reservations ima samo CHECK (end_date >= start_date); upis je
običan INSERT bez provere dostupnosti — dvoje zaposlenih rezerviše isto
vozilo za isti datum i oboje vide uspeh. Migracija 049 dodaje
EXCLUDE USING gist (vehicle_id WITH =, daterange(start_date, end_date, '[]')
WITH &&) WHERE (status = 'Активна') uz btree_gist.

Integracioni testovi: šemu obezbeđuju sami (migracija je idempotentna),
seed čiste po sebi; preskaču se bez baze.
"""

import os
import unittest
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / '.env')

DATABASE_URL = os.environ.get('DATABASE_URL', '').replace(
    'postgresql+psycopg://', 'postgresql://')

SEED_REG = 'PYTEST-PREKLOP-01'
SEED_BY = 'pytest-preklapanje@example.com'


def _connect():
    import psycopg
    if not DATABASE_URL:
        raise unittest.SkipTest('DATABASE_URL is not configured')
    try:
        return psycopg.connect(DATABASE_URL, connect_timeout=5)
    except Exception as exc:
        raise unittest.SkipTest(f'PostgreSQL unreachable: {exc}')


class VehicleRezervacijePreklapanjeTests(unittest.TestCase):
    def setUp(self):
        self.conn = _connect()
        with self.conn.cursor() as cur:
            cur.execute("SELECT to_regclass('public.vehicle_reservations')")
            if cur.fetchone()[0] is None:
                self.conn.close()
                self.skipTest('vehicle_reservations ne postoji')
        sql = (Path(__file__).parent / 'migration'
               / '049_vehicle_rezervacije_preklapanje.sql').read_text(encoding='utf-8')
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql)
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            self.conn.close()
            self.skipTest(f'migracija 049 nije primenljiva ovde: {exc}')
        self._cleanup()
        self.addCleanup(self._teardown)
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO vehicles (name, registration)
                VALUES ('Тест возило (pytest)', %s) RETURNING id
                """,
                (SEED_REG,),
            )
            self.vehicle_id = cur.fetchone()[0]
        self.conn.commit()

    def _teardown(self):
        self.conn.rollback()
        self._cleanup()
        self.conn.close()

    def _cleanup(self):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM vehicle_reservations WHERE reserved_by = %s",
                        (SEED_BY,))
            cur.execute("DELETE FROM vehicles WHERE registration = %s", (SEED_REG,))
        self.conn.commit()

    def _rezervisi(self, start, end, status='Активна'):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO vehicle_reservations
                    (vehicle_id, reserved_by, purpose, start_date, end_date, status)
                VALUES (%s, %s, 'pytest preklapanje', %s, %s, %s)
                RETURNING id
                """,
                (self.vehicle_id, SEED_BY, start, end, status),
            )
            rid = cur.fetchone()[0]
        self.conn.commit()
        return rid

    def test_preklopljena_aktivna_rezervacija_se_odbija(self):
        """Nalaz iz revizije: isti datum + isto vozilo = druga rezervacija
        mora pasti na nivou baze."""
        from psycopg import errors as pg_errors
        self._rezervisi('2030-05-10', '2030-05-12')
        with self.assertRaises(pg_errors.ExclusionViolation):
            self._rezervisi('2030-05-12', '2030-05-14')  # granični dan se seče
        self.conn.rollback()

    def test_uzastopni_periodi_bez_preklapanja_prolaze(self):
        self._rezervisi('2030-06-01', '2030-06-05')
        rid = self._rezervisi('2030-06-06', '2030-06-08')
        self.assertIsInstance(rid, int)

    def test_otkazana_rezervacija_ne_blokira(self):
        """Samo AKTIVNE rezervacije se isključuju — otkazana ne blokira novu."""
        self._rezervisi('2030-07-01', '2030-07-05', status='Отказана')
        rid = self._rezervisi('2030-07-01', '2030-07-05')
        self.assertIsInstance(rid, int)


if __name__ == '__main__':
    unittest.main()
