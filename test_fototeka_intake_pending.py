"""Revizija 2026-08 (batch 6, stavka 5): pad spoljnog commit-a ne sme trajno
da zarobi write-once RAW putanju.

Scenario iz nalaza: _intake_photo_from_path postavi RAW, vrati se, a commit
ManagedPostgresConnection konteksta padne — nema DB reda, RAW ostaje, ponovni
upload istog sadržaja dobija lažnu "koliziju". Protokol namere (fototeka_
intake_pending, migration/047): namera PRE fajla u sopstvenoj transakciji,
finalizacija u transakciji reda; zauzeta putanja bez DB reda a sa namerom je
dokazano siroče i sme da se preuzme; reconciler periodično čisti ostatke.

Testovi koriste fake DB sloj (obrazac iz test_fototeka_uvoz.py) i stvarne
fajlove u tmp arhivi — commit-fail se simulira odbacivanjem svih DB efekata
glavne transakcije uz zadržavanje fajla i (posebno commit-ovane) namere.
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


class _PendingStore:
    """Simulira fototeka_intake_pending: upisi preko sopstvene konekcije se
    'commit-uju' odmah (kao u produkciji); DELETE kroz glavnu transakciju
    primenjuje se samo ako glavna transakcija 'prođe'."""

    def __init__(self):
        self.rows = {}


class _IntentCursor:
    def __init__(self, store):
        self.store = store

    def execute(self, sql, params=None):
        assert 'fototeka_intake_pending' in sql
        sha256, raw_rel, original_ime = params
        self.store.rows[raw_rel] = sha256

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class _IntentConnection:
    def __init__(self, store):
        self.store = store

    def cursor(self):
        return _IntentCursor(self.store)

    def commit(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class _MainCursor:
    """Glavna transakcija: fotografije + tagovi + veza + posao + finalizacija.
    Efekti se skupljaju u staged_* i primenjuju tek na apply() ('commit')."""

    def __init__(self, store, committed_photos):
        self.store = store
        self.committed_photos = committed_photos  # set raw_putanja sa redom
        self.staged_pending_deletes = []
        self._pending = None
        self.next_id = 100

    def execute(self, sql, params=None):
        squashed = ' '.join(sql.split())
        self._pending = None
        if 'SELECT id FROM fotografije WHERE sha256' in squashed:
            self._pending = None
        elif 'SELECT 1 FROM fotografije WHERE raw_putanja' in squashed:
            self._pending = (1,) if params[0] in self.committed_photos else None
        elif 'SELECT 1 FROM fototeka_intake_pending' in squashed:
            self._pending = (1,) if params[0] in self.store.rows else None
        elif 'INSERT INTO fotografije' in squashed:
            self._pending = {'id': self.next_id}
        elif 'DELETE FROM fototeka_intake_pending' in squashed:
            self.staged_pending_deletes.append(params[0])

    def fetchone(self):
        return self._pending

    def apply_commit(self, raw_rel):
        self.committed_photos.add(raw_rel)
        for deleted in self.staged_pending_deletes:
            self.store.rows.pop(deleted, None)


def _write_jpeg(path):
    Image.new('RGB', (40, 30), (120, 30, 30)).save(path, 'JPEG')


class IntakePendingProtocolTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.arhiva = base / 'arhiva'
        self.media = base / 'media'
        self.arhiva.mkdir()
        self.media.mkdir()
        self.store = _PendingStore()
        self.committed = set()
        self.patchers = [
            patch.object(fototeka_jobs, 'get_arhiva_path', lambda: self.arhiva),
            patch.object(fototeka_jobs, 'get_media_path', lambda: self.media),
            patch.object(fototeka_jobs, 'enqueue_job', lambda cur, fid, tip: None),
            patch.object(fototeka_views, 'get_postgres_connection',
                         lambda: _IntentConnection(self.store)),
        ]
        for p in self.patchers:
            p.start()
        self.addCleanup(self.tmp.cleanup)
        for p in self.patchers:
            self.addCleanup(p.stop)

    def _intake(self, cur):
        temp_path = self.media / 'temp_upload.jpg'
        _write_jpeg(temp_path)
        size = temp_path.stat().st_size
        return fototeka_views._intake_photo_from_path(
            cur, temp_path, 'IMG_0001.jpg', size, '.jpg',
            autor_email='qa@example.com', opis=None, tags=[],
            datum_override=None, veza=None,
            u_prijemnom_redu=False, poreklo='upload',
        )

    def test_pad_commita_pa_ponovni_upload_uspeva(self):
        """Nalaz iz revizije: posle propalog commit-a ponovni upload istog
        sadržaja MORA da uspe, ne da prijavi lažnu koliziju."""
        # 1. prvi intake: fajl postavljen, ali commit "padne" — DB efekti se
        #    NE primenjuju (apply_commit se ne zove); namera je već upisana.
        cur1 = _MainCursor(self.store, self.committed)
        foto_id, reason = self._intake(cur1)
        self.assertIsNotNone(foto_id)
        raw_files = list(self.arhiva.rglob('*.jpg'))
        self.assertEqual(len(raw_files), 1, 'RAW mora biti postavljen')
        raw_rel = str(raw_files[0].relative_to(self.arhiva))
        self.assertIn(raw_rel, self.store.rows,
                      'namera mora biti upisana pre fajla i preživeti pad commit-a')

        # 2. ponovni upload: putanja je zauzeta siročetom, ali bez DB reda i
        #    sa zabeleženom namerom — intake je preuzima i uspeva.
        cur2 = _MainCursor(self.store, self.committed)
        foto_id2, reason2 = self._intake(cur2)
        self.assertIsNone(reason2, f'lažna kolizija: {reason2}')
        self.assertIsNotNone(foto_id2)
        cur2.apply_commit(raw_rel)
        self.assertNotIn(raw_rel, self.store.rows,
                         'uspešan commit briše nameru (finalizacija)')
        self.assertEqual(len(list(self.arhiva.rglob('*.jpg'))), 1)

    def test_pravi_original_se_nikad_ne_preuzima(self):
        """Zauzeta putanja SA postojećim DB redom je pravi write-once original
        — kolizija se i dalje odbija, fajl se ne dira."""
        cur1 = _MainCursor(self.store, self.committed)
        foto_id, _ = self._intake(cur1)
        self.assertIsNotNone(foto_id)
        raw_files = list(self.arhiva.rglob('*.jpg'))
        raw_rel = str(raw_files[0].relative_to(self.arhiva))
        cur1.apply_commit(raw_rel)  # commit PROŠAO — pravi original
        original_bytes = raw_files[0].read_bytes()

        cur2 = _MainCursor(self.store, self.committed)
        foto_id2, reason2 = self._intake(cur2)
        self.assertIsNone(foto_id2)
        self.assertIn('већ постоји у', reason2 or '')
        self.assertEqual(raw_files[0].read_bytes(), original_bytes)

    def test_namera_se_upisuje_pre_fajla(self):
        """Redosled: namera -> fajl. Ako upis namere padne, fajl se ne sme
        postaviti (radnja bez traga se ne izvršava)."""
        def boom():
            raise RuntimeError('baza nedostupna')

        with patch.object(fototeka_views, 'get_postgres_connection', boom):
            cur = _MainCursor(self.store, self.committed)
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


if __name__ == '__main__':
    unittest.main()
