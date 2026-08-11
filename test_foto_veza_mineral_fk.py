"""Revizija 2026-08 (batch 6, stavka 7): veza fotografija↔predmet dobija
stabilan strani ključ za mineralošku zbirku.

Nalaz: foto_veza_predmet cilja predmet tekstualnim parom (database_name,
inventarni_broj); ispravka inventarnog broja M-123 -> M-124 ili brisanje
minerala ostavlja vezu da visi na starom broju. Migracija 048 dodaje
nullable mineral_id FK (ON UPDATE/DELETE CASCADE) + backfill, a
update_mineral/delete_mineral sinhronizuju vezu u ISTOJ transakciji.

Integracioni testovi (obrazac iz test_postgres_implementation): šemu
obezbeđuju sami (migracija 048 je idempotentna), seed čiste po sebi;
preskaču se ako baza nije dostupna.
"""

import os
import unittest
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / '.env')

# psycopg.connect traži 'postgresql://', SQLAlchemy (MineralDatabase) traži
# '+psycopg' dijalekt — čuvamo obe varijante istog URL-a.
SQLALCHEMY_URL = os.environ.get('DATABASE_URL', '')
DATABASE_URL = SQLALCHEMY_URL.replace('postgresql+psycopg://', 'postgresql://')

SEED_SHA = 'f' * 60 + 'ba71'  # jedinstven, prepoznatljiv test sha
SEED_INV = 'PYTEST-FK-99991'
SEED_INV_NEW = 'PYTEST-FK-99992'


def _connect():
    import psycopg
    if not DATABASE_URL:
        raise unittest.SkipTest('DATABASE_URL is not configured')
    try:
        return psycopg.connect(DATABASE_URL, connect_timeout=5)
    except Exception as exc:
        raise unittest.SkipTest(f'PostgreSQL unreachable: {exc}')


class FotoVezaMineralFkTests(unittest.TestCase):
    def setUp(self):
        self.conn = _connect()
        with self.conn.cursor() as cur:
            cur.execute("SELECT to_regclass('public.foto_veza_predmet'), "
                        "to_regclass('public.minerals')")
            veza_t, minerals_t = cur.fetchone()
            if veza_t is None or minerals_t is None:
                self.conn.close()
                self.skipTest('foto_veza_predmet/minerals ne postoje (migracija 024)')
        # Šema stavke 7 — idempotentna migracija 048 (uključuje i backfill).
        sql = (Path(__file__).parent / 'migration'
               / '048_foto_veza_predmet_mineral_fk.sql').read_text(encoding='utf-8')
        with self.conn.cursor() as cur:
            cur.execute(sql)
        self.conn.commit()
        self._cleanup()
        self.addCleanup(self._teardown)

    def _teardown(self):
        self._cleanup()
        self.conn.close()

    def _cleanup(self):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM foto_veza_predmet WHERE inventarni_broj LIKE 'PYTEST-FK-%'")
            cur.execute("DELETE FROM fotografije WHERE sha256 = %s", (SEED_SHA,))
            cur.execute("DELETE FROM minerals WHERE inventory_number LIKE 'PYTEST-FK-%'")
        self.conn.commit()

    def _seed(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO minerals (inventory_number, item_name)
                VALUES (%s, 'Тест минерал (pytest)') RETURNING id
                """,
                (SEED_INV,),
            )
            mineral_id = cur.fetchone()[0]
            cur.execute(
                """
                INSERT INTO fotografije (sha256, raw_putanja, original_ime,
                                         autor_email, poreklo)
                VALUES (%s, %s, 'pytest-fk.jpg', 'pytest@example.com', 'upload')
                RETURNING id
                """,
                (SEED_SHA, f'pytest/fk/{SEED_SHA}.jpg'),
            )
            foto_id = cur.fetchone()[0]
            cur.execute(
                """
                INSERT INTO foto_veza_predmet
                    (fotografija_id, database_name, inventarni_broj, mineral_id)
                VALUES (%s, 'mineral', %s, %s) RETURNING id
                """,
                (foto_id, SEED_INV, mineral_id),
            )
            veza_id = cur.fetchone()[0]
        self.conn.commit()
        return mineral_id, foto_id, veza_id

    def _veza(self, veza_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT inventarni_broj, mineral_id FROM foto_veza_predmet "
                        "WHERE id = %s", (veza_id,))
            return cur.fetchone()

    def test_preimenovanje_minerala_prati_vezu(self):
        """M-123 -> M-124: veza mora da pređe na novi broj (ista transakcija)."""
        from mineral_database_pg import MineralDatabase
        mineral_id, _, veza_id = self._seed()

        # Eksplicitan URL: puna svita ume da preusmeri DATABASE_URL u env-u,
        # a seed ide kroz psycopg na URL uhvaćen pri importu ovog modula.
        db = MineralDatabase(SQLALCHEMY_URL)
        if not db.available:
            self.skipTest('MineralDatabase nije dostupna')
        ok = db.update_mineral(mineral_id, {
            'inventory_number': SEED_INV_NEW,
            'item_name': 'Тест минерал (pytest, преименован)',
        })
        self.assertTrue(ok)

        row = self._veza(veza_id)
        self.assertIsNotNone(row, 'veza ne sme da nestane pri preimenovanju')
        self.assertEqual(row[0], SEED_INV_NEW,
                         'veza mora da prati novi inventarni broj')
        self.assertEqual(row[1], mineral_id)

    def test_brisanje_minerala_uklanja_vezu(self):
        """ON DELETE CASCADE: brisanje minerala čisti vezu, fotografija ostaje."""
        from mineral_database_pg import MineralDatabase
        mineral_id, foto_id, veza_id = self._seed()

        # Eksplicitan URL: puna svita ume da preusmeri DATABASE_URL u env-u,
        # a seed ide kroz psycopg na URL uhvaćen pri importu ovog modula.
        db = MineralDatabase(SQLALCHEMY_URL)
        if not db.available:
            self.skipTest('MineralDatabase nije dostupna')
        self.assertTrue(db.delete_mineral(mineral_id))

        self.assertIsNone(self._veza(veza_id), 'veza mora pasti uz mineral')
        with self.conn.cursor() as cur:
            cur.execute('SELECT 1 FROM fotografije WHERE id = %s', (foto_id,))
            self.assertIsNotNone(cur.fetchone(), 'fotografija ostaje')

    def test_backfill_uparuje_postojece_veze(self):
        """Zatečena veza bez mineral_id (tačan broj) dobija FK kroz backfill."""
        mineral_id, foto_id, veza_id = self._seed()
        with self.conn.cursor() as cur:
            cur.execute('UPDATE foto_veza_predmet SET mineral_id = NULL '
                        'WHERE id = %s', (veza_id,))
        self.conn.commit()

        sql = (Path(__file__).parent / 'migration'
               / '048_foto_veza_predmet_mineral_fk.sql').read_text(encoding='utf-8')
        with self.conn.cursor() as cur:
            cur.execute(sql)
        self.conn.commit()

        self.assertEqual(self._veza(veza_id)[1], mineral_id,
                         'backfill mora da upari vezu sa mineralom')

    def test_novi_insert_veze_postavlja_mineral_id(self):
        """_insert_veza za database_name='mineral' odmah rezolvuje FK."""
        import fototeka_views
        mineral_id, foto_id, veza_id = self._seed()
        with self.conn.cursor() as cur:
            cur.execute('DELETE FROM foto_veza_predmet WHERE id = %s', (veza_id,))
            fototeka_views._insert_veza(cur, foto_id, {
                'tip': 'predmet', 'database_name': 'mineral',
                'inventarni_broj': SEED_INV,
            })
            cur.execute('SELECT mineral_id FROM foto_veza_predmet '
                        'WHERE fotografija_id = %s', (foto_id,))
            self.assertEqual(cur.fetchone()[0], mineral_id)
        self.conn.rollback()


if __name__ == '__main__':
    unittest.main()
