"""Revizija 2026-08 (batch 6, stavka 5 + krug revizije, stavka 2): pad
spoljnog commit-a ne sme trajno da zarobi write-once RAW putanju.

Scenario iz nalaza: _intake_photo_from_path postavi RAW, vrati se, a commit
ManagedPostgresConnection konteksta padne — nema DB reda, RAW ostaje, ponovni
upload istog sadržaja dobija lažnu "koliziju". Protokol namere (fototeka_
intake_pending, migration/047): namera PRE fajla u sopstvenoj transakciji,
finalizacija u transakciji reda; zauzeta putanja bez DB reda a sa namerom je
dokazano siroče i sme da se preuzme; reconciler periodično čisti ostatke.

IntakePendingProtocolTests i ConcurrentIntakeRealDbTests rade nad stvarnim
PostgreSQL-om (museum_system_test): baš MVCC/commit ponašanje je predmet
ovih testova (siroče vs. pravi write-once original, konkurentni unos), a
fake kursor bez pravih transakcija ne bi to dokazao. ReconcileIntakePendingTests
i dalje koristi fake DB sloj jer testira čistu orkestraciju
reconcile_intake_pending nad tmp arhivom, bez transakcione semantike.
"""

import os
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

import tempfile

from PIL import Image

import fototeka_jobs
import fototeka_views


TEST_DB_URL = os.environ.get(
    'MIS_TEST_DB_URL',
    'postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system_test',
)
PLAIN_URL = TEST_DB_URL.replace('postgresql+psycopg://', 'postgresql://')


def _write_jpeg(path):
    Image.new('RGB', (40, 30), (120, 30, 30)).save(path, 'JPEG')


class _RealDbFototekaTestCase(unittest.TestCase):
    """Zajednička plumbing za testove nad stvarnim museum_system_test:
    dostupnost baze, primena migracija koje protokol namere zahteva, tmp
    arhiva/media, čišćenje po sintetičkom identitetu."""

    NAMERA_EMAIL = 'namera.protokol@example.invalid'
    NAMERA_IME = 'NAMERA_PROTOKOL.jpg'

    @classmethod
    def setUpClass(cls):
        if '_test' not in PLAIN_URL.rsplit('/', 1)[-1]:
            raise unittest.SkipTest(
                'MIS_TEST_DB_URL ne pokazuje na *_test bazu — zaštita produkcije')
        try:
            import psycopg
        except ImportError:
            raise unittest.SkipTest('psycopg nije instaliran')
        cls.psycopg = psycopg
        try:
            with psycopg.connect(PLAIN_URL, connect_timeout=3) as conn:
                conn.execute('SELECT 1')
        except Exception:
            raise unittest.SkipTest('museum_system_test nije dostupan')
        with psycopg.connect(PLAIN_URL) as conn:
            for fname in ('047_fototeka_intake_pending.sql',
                          '052_fototeka_intent_claim.sql'):
                sql = (Path(__file__).parent / 'migration' / fname
                       ).read_text(encoding='utf-8')
                conn.execute(sql)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.arhiva = base / 'arhiva'
        self.media = base / 'media'
        self.arhiva.mkdir()
        self.media.mkdir()
        self.patchers = [
            patch.object(fototeka_jobs, 'get_arhiva_path', lambda: self.arhiva),
            patch.object(fototeka_jobs, 'get_media_path', lambda: self.media),
            patch.object(fototeka_jobs, 'enqueue_job', lambda cur, fid, tip: None),
            # Intent-transakcija fototeka_views ide na test bazu, ne kroz
            # pool vezan za .env bazu.
            patch.object(fototeka_views, 'get_postgres_connection',
                         lambda: self.psycopg.connect(PLAIN_URL)),
        ]
        for p in self.patchers:
            p.start()
        self.addCleanup(self.tmp.cleanup)
        for p in self.patchers:
            self.addCleanup(p.stop)
        self.addCleanup(self._ocisti_bazu)
        # I na ulazu: namera se commit-uje autonomno, pa prekinut raniji run
        # ostavlja redove koje cleanup nije stigao da ukloni.
        self._ocisti_bazu()

    def _ocisti_bazu(self):
        with self.psycopg.connect(PLAIN_URL) as conn:
            conn.execute(
                """
                DELETE FROM foto_poslovi WHERE fotografija_id IN
                    (SELECT id FROM fotografije WHERE autor_email = %s)
                """, (self.NAMERA_EMAIL,))
            conn.execute(
                """
                DELETE FROM fotografija_tagovi WHERE fotografija_id IN
                    (SELECT id FROM fotografije WHERE autor_email = %s)
                """, (self.NAMERA_EMAIL,))
            conn.execute('DELETE FROM fotografije WHERE autor_email = %s',
                         (self.NAMERA_EMAIL,))
            conn.execute(
                'DELETE FROM fototeka_intake_pending WHERE original_ime = %s',
                (self.NAMERA_IME,))

    def _intake(self, cur):
        temp_path = self.media / 'temp_upload.jpg'
        _write_jpeg(temp_path)
        size = temp_path.stat().st_size
        return fototeka_views._intake_photo_from_path(
            cur, temp_path, self.NAMERA_IME, size, '.jpg',
            autor_email=self.NAMERA_EMAIL, opis=None, tags=[],
            datum_override=None, veza=None,
            u_prijemnom_redu=False, poreklo='upload',
        )


class IntakePendingProtocolTests(_RealDbFototekaTestCase):
    """Stvarni PostgreSQL: pad commit-a i write-once kolizija zavise od
    pravog MVCC ponašanja (nekomitovan red je nevidljiv drugoj konekciji,
    fajl na disku nije transakcion) — fake kursor to ne modeluje verno."""

    def test_pad_commita_pa_ponovni_upload_uspeva(self):
        """Nalaz iz revizije: posle propalog commit-a ponovni upload istog
        sadržaja MORA da uspe, ne da prijavi lažnu koliziju."""
        # 1. prvi intake: fajl postavljen, ali commit "padne" — rollback na
        #    sopstvenoj konekciji; namera je već commit-ovana (sopstvena
        #    transakcija) i preživljava.
        conn1 = self.psycopg.connect(PLAIN_URL)
        self.addCleanup(conn1.close)
        cur1 = conn1.cursor()
        foto_id, reason = self._intake(cur1)
        self.assertIsNone(reason)
        self.assertIsNotNone(foto_id)
        raw_files = list(self.arhiva.rglob('*.jpg'))
        self.assertEqual(len(raw_files), 1, 'RAW mora biti postavljen')
        raw_rel = str(raw_files[0].relative_to(self.arhiva))
        conn1.rollback()

        with self.psycopg.connect(PLAIN_URL) as verify_conn:
            namera = verify_conn.execute(
                'SELECT 1 FROM fototeka_intake_pending WHERE raw_putanja = %s',
                (raw_rel,)).fetchone()
        self.assertIsNotNone(
            namera, 'namera mora biti upisana pre fajla i preživeti pad commit-a')

        # 2. ponovni upload POSLE isteka INTAKE_CLAIM_STALE_MINUTES (svežu
        #    tuđu nameru niko ne sme da preuzme — krug 4, stavka 2): putanja
        #    je zauzeta siročetom, bez DB reda, bajata namera se preuzima.
        with self.psycopg.connect(PLAIN_URL) as age_conn:
            age_conn.execute(
                """
                UPDATE fototeka_intake_pending
                SET created_at = now() - interval '31 minutes'
                WHERE raw_putanja = %s
                """, (raw_rel,))
            age_conn.commit()

        conn2 = self.psycopg.connect(PLAIN_URL)
        self.addCleanup(conn2.close)
        cur2 = conn2.cursor()
        foto_id2, reason2 = self._intake(cur2)
        self.assertIsNone(reason2, f'lažna kolizija: {reason2}')
        self.assertIsNotNone(foto_id2)
        conn2.commit()

        with self.psycopg.connect(PLAIN_URL) as verify_conn:
            namera = verify_conn.execute(
                'SELECT 1 FROM fototeka_intake_pending WHERE raw_putanja = %s',
                (raw_rel,)).fetchone()
        self.assertIsNone(namera, 'uspešan commit briše nameru (finalizacija)')
        self.assertEqual(len(list(self.arhiva.rglob('*.jpg'))), 1)

    def test_pravi_original_se_nikad_ne_preuzima(self):
        """Zauzeta putanja SA postojećim DB redom je pravi write-once
        original — _reclaim_orphan_raw je nikad ne preuzima, fajl se ne
        dira. (Sha256 je deo imena RAW fajla, pa isti sadržaj kroz javni
        _intake_photo_from_path prvo pada na dedup pre sha256 provere;
        _reclaim_orphan_raw se testira direktno, kao što ga interno zove
        _intake_photo_from_path posle FileExistsError.)"""
        conn1 = self.psycopg.connect(PLAIN_URL)
        self.addCleanup(conn1.close)
        cur1 = conn1.cursor()
        foto_id, reason = self._intake(cur1)
        self.assertIsNone(reason)
        self.assertIsNotNone(foto_id)
        conn1.commit()  # commit PROŠAO — pravi original

        raw_files = list(self.arhiva.rglob('*.jpg'))
        raw_rel = str(raw_files[0].relative_to(self.arhiva))
        original_bytes = raw_files[0].read_bytes()

        with self.psycopg.connect(PLAIN_URL) as conn2:
            cur2 = conn2.cursor()
            preuzeto = fototeka_views._reclaim_orphan_raw(
                cur2, raw_rel, raw_files[0], 'ma-koji-token')
        self.assertFalse(
            preuzeto, 'putanja sa postojećim DB redom se nikad ne preuzima')
        self.assertEqual(raw_files[0].read_bytes(), original_bytes)

    def test_namera_se_upisuje_pre_fajla(self):
        """Redosled: namera -> fajl. Ako upis namere padne, fajl se ne sme
        postaviti (radnja bez traga se ne izvršava)."""
        def boom():
            raise RuntimeError('baza nedostupna')

        with patch.object(fototeka_views, 'get_postgres_connection', boom):
            conn = self.psycopg.connect(PLAIN_URL)
            self.addCleanup(conn.close)
            cur = conn.cursor()
            with self.assertRaises(RuntimeError):
                self._intake(cur)
        self.assertEqual(list(self.arhiva.rglob('*.jpg')), [],
                         'fajl ne sme biti postavljen bez upisane namere')


class ReconcileIntakePendingTests(unittest.TestCase):
    """Orkestracija reconcile_intake_pending nad fake DB slojem + tmp arhivom."""

    class _Cur:
        def __init__(self, owner):
            self.owner = owner
            self._pending = []

        def execute(self, sql, params=None):
            squashed = ' '.join(sql.split())
            if 'SELECT id, raw_putanja FROM fototeka_intake_pending' in squashed:
                self._pending = [(pid, rel) for pid, rel in self.owner.pending]
            elif 'SELECT 1 FROM fotografije WHERE raw_putanja' in squashed:
                self._pending = [(1,)] if params[0] in self.owner.photos else []
            elif 'DELETE FROM fototeka_intake_pending' in squashed:
                self.owner.pending = [
                    (pid, rel) for pid, rel in self.owner.pending
                    if pid != params[0]
                ]
                self._pending = []

        def fetchone(self):
            return self._pending[0] if self._pending else None

        def fetchall(self):
            return list(self._pending)

        def __enter__(self):
            return self

        def __exit__(self, *_):
            return False

    class _Conn:
        def __init__(self, owner):
            self.owner = owner

        def cursor(self):
            return ReconcileIntakePendingTests._Cur(self.owner)

        def commit(self):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_):
            return False

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.arhiva = Path(self.tmp.name)
        self.pending = []
        self.photos = set()
        self.patchers = [
            patch.object(fototeka_jobs, 'get_arhiva_path', lambda: self.arhiva),
            patch.object(fototeka_jobs, 'get_postgres_connection',
                         lambda: ReconcileIntakePendingTests._Conn(self)),
        ]
        for p in self.patchers:
            p.start()
        self.addCleanup(self.tmp.cleanup)
        for p in self.patchers:
            self.addCleanup(p.stop)

    def test_reconcile_pokriva_sve_tri_grane(self):
        # 1: red postoji -> samo namera odlazi
        self.photos.add('a/finalizovana.jpg')
        # 2: reda nema, RAW postoji -> siroče se briše
        orphan = self.arhiva / 'b' / 'siroce.jpg'
        orphan.parent.mkdir(parents=True)
        orphan.write_bytes(b'x')
        # 3: reda nema, RAW ne postoji -> namera se čisti
        self.pending = [(1, 'a/finalizovana.jpg'),
                        (2, 'b/siroce.jpg'),
                        (3, 'c/nikad-postavljena.jpg')]

        stats = fototeka_jobs.reconcile_intake_pending(min_age_minutes=0)

        self.assertEqual(stats, {'finalized': 1, 'orphan_removed': 1,
                                 'stale_cleared': 1})
        self.assertFalse(orphan.exists())
        self.assertEqual(self.pending, [])

    def test_reconcile_je_idempotentan(self):
        self.pending = []
        stats = fototeka_jobs.reconcile_intake_pending(min_age_minutes=0)
        self.assertEqual(stats, {'finalized': 0, 'orphan_removed': 0,
                                 'stale_cleared': 0})


# --- Krug 4, stavka 2: konkurentni unos na STVARNOJ bazi ----------------------

KONKURENCIJA_EMAIL = 'konkurencija.krug4@example.invalid'
KONKURENCIJA_IME = 'KONKURENCIJA_KRUG4.jpg'


class ConcurrentIntakeRealDbTests(unittest.TestCase):
    """Dva ISTOVREMENA unosa iste fotografije (ista SHA) kroz stvarni
    PostgreSQL (MVCC, pravi commit): gubitnik ne sme ni da preuzme putanju ni
    da pri čišćenju obriše RAW pobednika. Pre isправke je gubitnik video
    zajednički red namere kao 'svoj', unlink-ovao pobednikov RAW i zaglavio
    na unique(sha256) čekajući pobednikov commit."""

    @classmethod
    def setUpClass(cls):
        if '_test' not in PLAIN_URL.rsplit('/', 1)[-1]:
            raise unittest.SkipTest(
                'MIS_TEST_DB_URL ne pokazuje na *_test bazu — zaštita produkcije')
        try:
            import psycopg
        except ImportError:
            raise unittest.SkipTest('psycopg nije instaliran')
        cls.psycopg = psycopg
        try:
            with psycopg.connect(PLAIN_URL, connect_timeout=3) as conn:
                conn.execute('SELECT 1')
        except Exception:
            raise unittest.SkipTest('museum_system_test nije dostupan')
        with psycopg.connect(PLAIN_URL) as conn:
            for fname in ('047_fototeka_intake_pending.sql',
                          '052_fototeka_intent_claim.sql'):
                sql = (Path(__file__).parent / 'migration' / fname
                       ).read_text(encoding='utf-8')
                conn.execute(sql)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.arhiva = base / 'arhiva'
        self.media = base / 'media'
        self.arhiva.mkdir()
        self.media.mkdir()
        self.patchers = [
            patch.object(fototeka_jobs, 'get_arhiva_path', lambda: self.arhiva),
            patch.object(fototeka_jobs, 'get_media_path', lambda: self.media),
            # Intent-transakcija fototeka_views ide na test bazu, ne kroz
            # pool vezan za .env bazu.
            patch.object(fototeka_views, 'get_postgres_connection',
                         lambda: self.psycopg.connect(PLAIN_URL)),
        ]
        for p in self.patchers:
            p.start()
        self.addCleanup(self.tmp.cleanup)
        for p in self.patchers:
            self.addCleanup(p.stop)
        self.addCleanup(self._ocisti_bazu)
        # I na ulazu: namera se commit-uje autonomno, pa prekinut raniji run
        # ostavlja redove koje cleanup nije stigao da ukloni.
        self._ocisti_bazu()

    def _ocisti_bazu(self):
        with self.psycopg.connect(PLAIN_URL) as conn:
            conn.execute(
                """
                DELETE FROM foto_poslovi WHERE fotografija_id IN
                    (SELECT id FROM fotografije WHERE autor_email = %s)
                """, (KONKURENCIJA_EMAIL,))
            conn.execute(
                """
                DELETE FROM fotografija_tagovi WHERE fotografija_id IN
                    (SELECT id FROM fotografije WHERE autor_email = %s)
                """, (KONKURENCIJA_EMAIL,))
            conn.execute('DELETE FROM fotografije WHERE autor_email = %s',
                         (KONKURENCIJA_EMAIL,))
            conn.execute(
                'DELETE FROM fototeka_intake_pending WHERE original_ime = %s',
                (KONKURENCIJA_IME,))

    def _intake(self, cur, temp_path):
        size = temp_path.stat().st_size
        return fototeka_views._intake_photo_from_path(
            cur, temp_path, KONKURENCIJA_IME, size, '.jpg',
            autor_email=KONKURENCIJA_EMAIL, opis=None, tags=[],
            datum_override=None, veza=None,
            u_prijemnom_redu=False, poreklo='upload',
        )

    def test_konkurentni_unos_iste_sha_ne_brise_raw_pobednika(self):
        # Jedinstven sadržaj po pokretanju testa da se ne sudara sa ostacima.
        import random
        boja = (random.randrange(256), random.randrange(256), random.randrange(256))
        temp_a = self.media / 'unos_a.jpg'
        temp_b = self.media / 'unos_b.jpg'
        Image.new('RGB', (40, 30), boja).save(temp_a, 'JPEG')
        temp_b.write_bytes(temp_a.read_bytes())

        conn_a = self.psycopg.connect(PLAIN_URL)
        conn_b = self.psycopg.connect(PLAIN_URL)
        self.addCleanup(conn_a.close)
        self.addCleanup(conn_b.close)
        cur_a = conn_a.cursor()
        cur_b = conn_b.cursor()

        # B (konkurent, ista SHA) ulazi u NAJGOREM prozoru: A je upisao i
        # commit-ovao nameru, postavio RAW i ubacio red fotografije (bez
        # commita), ali JOŠ NIJE finalizovao (DELETE namere). Pre isправke je
        # B tu video zajednički red namere kao 'svoj' i brisao A-ov RAW.
        rezultat_b = {}
        original_replace_tags = fototeka_views._replace_tags

        def replace_tags_sa_konkurentom(cur, foto_id, tags):
            if not rezultat_b:
                rezultat_b['vrednost'] = self._intake(cur_b, temp_b)
            return original_replace_tags(cur, foto_id, tags)

        with patch.object(fototeka_views, '_replace_tags',
                          replace_tags_sa_konkurentom):
            foto_id_a, reason_a = self._intake(cur_a, temp_a)
        self.assertIsNone(reason_a)
        self.assertIsNotNone(foto_id_a)
        raw_files = [p for p in self.arhiva.rglob('*') if p.is_file()]
        self.assertEqual(len(raw_files), 1, 'RAW pobednika mora biti postavljen')
        raw_bytes = raw_files[0].read_bytes()

        # B ne sme da preuzme svežu tuđu nameru, ne sme da dira fajl,
        # mora jasno da odbije.
        foto_id_b, reason_b = rezultat_b['vrednost']
        self.assertIsNone(foto_id_b)
        self.assertIn('управо додаје', reason_b or '',
                      f'očekivano odbijanje konkurentnog unosa, dobijeno: {reason_b}')

        conn_a.commit()
        conn_b.rollback()

        # RAW pobednika postoji posle OBA unosa, netaknut.
        self.assertTrue(raw_files[0].exists(),
                        'gubitnik je obrisao RAW pobednika')
        self.assertEqual(raw_files[0].read_bytes(), raw_bytes)

        # Red pobednika je u bazi i pokazuje na postojeći fajl; namera je
        # finalizovana (obrisana) u istom commit-u.
        with self.psycopg.connect(PLAIN_URL) as conn:
            row = conn.execute(
                'SELECT raw_putanja FROM fotografije WHERE id = %s',
                (foto_id_a,)).fetchone()
            self.assertIsNotNone(row)
            self.assertTrue((self.arhiva / row[0]).exists())
            ostale_namere = conn.execute(
                'SELECT count(*) FROM fototeka_intake_pending '
                'WHERE original_ime = %s', (KONKURENCIJA_IME,)).fetchone()[0]
            self.assertEqual(ostale_namere, 0)


if __name__ == '__main__':
    unittest.main()
