#!/usr/bin/env python3
"""Tests for Фототека batch import from the shared intake folder (Faza 1).

Covers: the PMB institution-prefix tolerance and date-from-filename fallback,
author resolution from the per-user Samba folder, dry-run purity (no DB writes,
no file moves), the move-after-success semantics (obradjeno/<mesec>,
obradjeno/duplikati, neuspesno) and the run/item logging.
"""

import os
import shutil
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

os.environ['FLASK_ENV'] = 'testing'
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

from PIL import Image

import fototeka_jobs
import fototeka_views


class _FakeCursor:
    def __init__(self, canned=None):
        self.canned = dict(canned or {})
        self._pending = None
        self.executed = []

    def execute(self, sql, params=None):
        self.executed.append((' '.join(sql.split()), params))
        for needle, row in self.canned.items():
            if needle in sql:
                value = row(params) if callable(row) else row
                self._pending = value
                return
        self._pending = None

    def fetchone(self):
        value = self._pending
        if isinstance(value, list):
            return value[0] if value else None
        return value

    def fetchall(self):
        value = self._pending
        if isinstance(value, list):
            return value
        return [value] if value else []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class _FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor
        self.commits = 0

    def cursor(self):
        return self._cursor

    def commit(self):
        self.commits += 1

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.commit()
        return False


def _write_jpeg(path, color=(120, 30, 30), size=(40, 30)):
    Image.new('RGB', size, color).save(path, 'JPEG')


# ---------------------------------------------------------------------------
# Konvencija: PMB prefiks + datum iz imena
# ---------------------------------------------------------------------------

class ConventionTests(unittest.TestCase):

    def test_pmb_prefix_is_tolerated(self):
        stripped = fototeka_views._strip_institution_prefix('PMB-M-01234_2026-07-02_01')
        self.assertEqual(stripped, 'M-01234_2026-07-02_01')
        result = fototeka_views.classify_import_filename(
            fototeka_views._strip_institution_prefix('PMB-M-01234_snimak.jpg'), 'mineral')
        self.assertEqual(result['klasa'], 'predmet')
        self.assertEqual(result['veza_meta']['inventarni_broj'], '01234')

    def test_cyrillic_pmb_prefix(self):
        self.assertEqual(
            fototeka_views._strip_institution_prefix('ПМБ-M-7_a'), 'M-7_a')

    def test_prefix_without_pmb_unchanged(self):
        self.assertEqual(
            fototeka_views._strip_institution_prefix('M-1234_x'), 'M-1234_x')

    def test_datum_iz_imena(self):
        self.assertEqual(
            fototeka_views.datum_iz_imena('M-01234_2026-07-02_01.tif'),
            date(2026, 7, 2))

    def test_datum_iz_imena_invalid_or_absent(self):
        self.assertIsNone(fototeka_views.datum_iz_imena('M-01234_2026-13-45.tif'))
        self.assertIsNone(fototeka_views.datum_iz_imena('DSC_0001.jpg'))

    def test_datum_iz_imena_requires_delimiters(self):
        # broj inventara ne sme slučajno da se protumači kao datum
        self.assertIsNone(fototeka_views.datum_iz_imena('M-20260702.tif'))


# ---------------------------------------------------------------------------
# Autorstvo iz korisničkog foldera
# ---------------------------------------------------------------------------

class AutorTests(unittest.TestCase):

    def test_unique_local_part_resolves(self):
        cur = _FakeCursor({'SPLIT_PART': [{'email': 'sjovanovic@nhmbeo.rs'}]})
        self.assertEqual(
            fototeka_views.autor_iz_foldera(cur, 'sjovanovic'),
            'sjovanovic@nhmbeo.rs')

    def test_unknown_folder_returns_none(self):
        cur = _FakeCursor({'SPLIT_PART': []})
        self.assertIsNone(fototeka_views.autor_iz_foldera(cur, 'nepoznat'))

    def test_ambiguous_folder_returns_none(self):
        cur = _FakeCursor({'SPLIT_PART': [
            {'email': 'ana@nhmbeo.rs'}, {'email': 'ana@drugidomen.rs'}]})
        self.assertIsNone(fototeka_views.autor_iz_foldera(cur, 'ana'))

    def test_empty_folder_returns_none(self):
        cur = _FakeCursor()
        self.assertIsNone(fototeka_views.autor_iz_foldera(cur, ''))


# ---------------------------------------------------------------------------
# run_batch_import — dry-run čistoća i premeštanje po ishodu
# ---------------------------------------------------------------------------

class RunBatchImportTests(unittest.TestCase):

    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix='uvoz-ulaz-'))
        self.media = Path(tempfile.mkdtemp(prefix='uvoz-media-'))
        self.arhiva = Path(tempfile.mkdtemp(prefix='uvoz-arhiva-'))
        self.addCleanup(shutil.rmtree, self.root, True)
        self.addCleanup(shutil.rmtree, self.media, True)
        self.addCleanup(shutil.rmtree, self.arhiva, True)
        self.env = patch.dict(os.environ, {
            'FOTOTEKA_IMPORT_PATH': str(self.root),
            'FOTOTEKA_MEDIA_PATH': str(self.media),
            'FOTOTEKA_ARHIVA_PATH': str(self.arhiva),
        })
        self.env.start()
        self.addCleanup(self.env.stop)

        self.kustos = self.root / 'sjovanovic'
        self.kustos.mkdir()

    def _patch_db(self, canned=None):
        cur = _FakeCursor(canned)
        conn = _FakeConnection(cur)
        patcher = patch.object(
            fototeka_views, 'get_postgres_connection', lambda: conn)
        patcher.start()
        self.addCleanup(patcher.stop)
        return cur

    def test_dry_run_writes_nothing(self):
        _write_jpeg(self.kustos / 'M-77_2026-07-02_01.jpg')
        _write_jpeg(self.kustos / 'DSC_0001.jpg', color=(10, 90, 40))
        cur = self._patch_db({
            'SPLIT_PART': [{'email': 'sjovanovic@nhmbeo.rs'}],
            'WHERE sha256': [],
        })

        rezime = fototeka_views.run_batch_import(dry_run=True)

        self.assertEqual(rezime['ukupno'], 2)
        self.assertEqual(rezime['uvezeno'], 2)
        self.assertEqual(rezime['u_prijemni_red'], 1)
        self.assertEqual(rezime['po_klasi']['predmet'], 1)
        self.assertEqual(rezime['po_klasi']['prijemni_red'], 1)
        self.assertIsNone(rezime['run_id'])
        # fajlovi netaknuti na share-u
        self.assertTrue((self.kustos / 'M-77_2026-07-02_01.jpg').exists())
        self.assertTrue((self.kustos / 'DSC_0001.jpg').exists())
        # nikakav INSERT nije izvršen
        inserts = [sql for sql, _ in cur.executed if sql.startswith('INSERT')]
        self.assertEqual(inserts, [])
        # arhiva prazna
        self.assertEqual(list(self.arhiva.rglob('*')), [])

    def test_dry_run_reports_existing_duplicate(self):
        _write_jpeg(self.kustos / 'M-77.jpg')
        self._patch_db({
            'SPLIT_PART': [{'email': 'sjovanovic@nhmbeo.rs'}],
            'WHERE sha256': [{'id': 42}],
        })

        rezime = fototeka_views.run_batch_import(dry_run=True)

        self.assertEqual(rezime['duplikata'], 1)
        self.assertEqual(rezime['uvezeno'], 0)
        self.assertTrue((self.kustos / 'M-77.jpg').exists())  # dry-run ne pomera

    def test_real_run_moves_by_outcome_and_logs(self):
        _write_jpeg(self.kustos / 'M-77_2026-07-02_01.jpg')
        _write_jpeg(self.kustos / 'duplikat.jpg', color=(1, 2, 3))
        (self.kustos / 'prazan.jpg').touch()  # 0 bajtova -> neuspesno

        sha_dup = fototeka_jobs.sha256_of_file(self.kustos / 'duplikat.jpg')

        def sha_lookup(params):
            return [{'id': 42}] if params and params[0] == sha_dup else []

        intake_calls = []

        def fake_intake(cur, temp_path, original_ime, file_size, ext, **kw):
            intake_calls.append({'ime': original_ime, **kw})
            return 101, None

        cur = self._patch_db({
            'SPLIT_PART': [{'email': 'sjovanovic@nhmbeo.rs'}],
            'WHERE sha256': sha_lookup,
            'INSERT INTO fototeka_uvoz_run': {'id': 7},
        })
        patcher = patch.object(fototeka_views, '_intake_photo_from_path', fake_intake)
        patcher.start()
        self.addCleanup(patcher.stop)

        rezime = fototeka_views.run_batch_import(
            dry_run=False, izvor='cli', pokrenuo_email='admin@nhmbeo.rs')

        self.assertEqual(rezime['uvezeno'], 1)
        self.assertEqual(rezime['duplikata'], 1)
        self.assertEqual(rezime['neuspesno'], 1)
        self.assertEqual(rezime['run_id'], 7)

        # premeštanje po ishodu
        mesec_dir = self.kustos / 'obradjeno'
        self.assertTrue(any(mesec_dir.rglob('M-77_2026-07-02_01.jpg')))
        self.assertTrue((self.kustos / 'obradjeno' / 'duplikati' / 'duplikat.jpg').exists())
        self.assertTrue((self.kustos / 'neuspesno' / 'prazan.jpg').exists())
        self.assertFalse((self.kustos / 'M-77_2026-07-02_01.jpg').exists())

        # intake dobio autora iz foldera, datum iz imena i poreklo import
        self.assertEqual(len(intake_calls), 1)
        poziv = intake_calls[0]
        self.assertEqual(poziv['autor_email'], 'sjovanovic@nhmbeo.rs')
        self.assertEqual(poziv['datum_override'], date(2026, 7, 2))
        self.assertEqual(poziv['poreklo'], 'import')
        self.assertEqual(poziv['tags'], [])

        # log: run + 3 stavke
        run_inserts = [p for sql, p in cur.executed
                       if sql.startswith('INSERT INTO fototeka_uvoz_run')]
        stavka_inserts = [p for sql, p in cur.executed
                          if sql.startswith('INSERT INTO fototeka_uvoz_stavka')]
        self.assertEqual(len(run_inserts), 1)
        self.assertEqual(len(stavka_inserts), 3)
        ishodi = sorted(p[3] for p in stavka_inserts)
        self.assertEqual(ishodi, ['duplikat', 'neuspesno', 'uvezeno'])

    def test_unknown_folder_falls_back_with_tag(self):
        _write_jpeg(self.kustos / 'M-5.jpg')
        self._patch_db({
            'SPLIT_PART': [],  # folder se ne mapira ni na jednog korisnika
            'WHERE sha256': [],
        })
        intake_calls = []

        def fake_intake(cur, temp_path, original_ime, file_size, ext, **kw):
            intake_calls.append(kw)
            return 55, None

        patcher = patch.object(fototeka_views, '_intake_photo_from_path', fake_intake)
        patcher.start()
        self.addCleanup(patcher.stop)

        fototeka_views.run_batch_import(
            dry_run=False, fallback_autor_email='fototeka@nhmbeo.rs')

        self.assertEqual(intake_calls[0]['autor_email'], 'fototeka@nhmbeo.rs')
        self.assertEqual(intake_calls[0]['tags'], ['uvoz-nepoznat-autor'])

    def test_obradjeno_and_neuspesno_dirs_are_not_rescanned(self):
        (self.kustos / 'obradjeno' / '2026-07').mkdir(parents=True)
        (self.kustos / 'neuspesno').mkdir()
        _write_jpeg(self.kustos / 'obradjeno' / '2026-07' / 'staro.jpg')
        _write_jpeg(self.kustos / 'neuspesno' / 'los.jpg')
        self._patch_db({'SPLIT_PART': [{'email': 'sjovanovic@nhmbeo.rs'}]})

        rezime = fototeka_views.run_batch_import(dry_run=True)

        self.assertEqual(rezime['ukupno'], 0)

    def test_teren_import_works_without_request_context(self):
        """Regresija: headless uvoz TEREN fajla ne sme da dira Flask sesiju
        (autor terena dolazi iz korisničkog foldera, ne iz sesije)."""
        _write_jpeg(self.kustos / 'TEREN_2026_Kopaonik_01.jpg')
        cur = self._patch_db({
            'SPLIT_PART': [{'email': 'sjovanovic@nhmbeo.rs'}],
            'WHERE sha256': [],
            'INSERT INTO fototeka_tereni': {'id': 9},
            'INSERT INTO fototeka_uvoz_run': {'id': 3},
        })
        intake_veze = []

        def fake_intake(cur, temp_path, original_ime, file_size, ext, **kw):
            intake_veze.append(kw['veza'])
            return 77, None

        patcher = patch.object(fototeka_views, '_intake_photo_from_path', fake_intake)
        patcher.start()
        self.addCleanup(patcher.stop)

        rezime = fototeka_views.run_batch_import(dry_run=False)

        self.assertEqual(rezime['uvezeno'], 1)
        self.assertEqual(intake_veze[0]['tip'], 'teren')
        teren_insert = [p for sql, p in cur.executed
                        if 'INSERT INTO fototeka_tereni' in sql][0]
        self.assertEqual(teren_insert[2], 'sjovanovic@nhmbeo.rs')

    def test_name_collision_in_target_gets_suffix(self):
        odrediste = self.kustos / 'obradjeno' / 'duplikati'
        odrediste.mkdir(parents=True)
        _write_jpeg(odrediste / 'ista.jpg')
        _write_jpeg(self.kustos / 'ista.jpg', color=(9, 9, 9))

        nova = fototeka_views._premesti_original(self.kustos / 'ista.jpg', odrediste)

        self.assertEqual(nova.name, 'ista__1.jpg')
        self.assertTrue((odrediste / 'ista.jpg').exists())
        self.assertTrue(nova.exists())


class IstorijaTests(unittest.TestCase):
    """Regresija: psycopg vraća TUPLE redove (ne dict) — mapiranje istorije
    mora da radi po poziciji kolona, ne preko _scalar."""

    def test_istorija_maps_tuple_rows(self):
        from datetime import datetime as dt
        red = (3, dt(2026, 7, 12, 22, 18), 'ui', 'qa@x', 1, 1, 0, 0, 0)
        cur = _FakeCursor({'FROM fototeka_uvoz_run': [red]})
        conn = _FakeConnection(cur)
        with patch.object(fototeka_views, 'get_postgres_connection', lambda: conn):
            istorija = fototeka_views._uvoz_istorija()
        self.assertEqual(istorija[0]['id'], 3)
        self.assertEqual(istorija[0]['izvor'], 'ui')
        self.assertEqual(istorija[0]['uvezeno'], 1)
        self.assertEqual(istorija[0]['pokrenut_at'].year, 2026)


if __name__ == '__main__':
    unittest.main()