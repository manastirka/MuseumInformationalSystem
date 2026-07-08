#!/usr/bin/env python3
"""Tests for `flask reset-test-data` (praznjenje probnih podataka).

Covers: dry-run report that names every table and changes nothing, execute
that truncates exactly the confirmed tables inside one transaction, the
interactive database-name confirmation, the missing-table guard, file cleanup
(dokumenta 017 + chat prilozi) and the EXPLICIT guard that institutional and
library tables are never touched.
"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

import app as museum_app
import reset_test_data

TEST_DB_URL = 'postgresql://tester@localhost:5432/testdb'
TEST_DB_NAME = 'testdb'

# Eksplicitan spisak institucionalnih tabela koje execute NE SME da dira —
# zbirke/nauka, BIBLIOTEKA kao ustanova (poimence, zahtev korisnika
# 2026-07-08), zaposleni/nalozi/role/odeljenja, entiteti i podesavanja.
INSTITUTIONAL_TABLES = [
    'bilja_hydrobioidea_radoman',
    'bilja_kenozojske_invertebrate',
    'bilja_opsta_zbirka_mollusca',
    'bilja_recentni_morski_mekusci',
    'bilja_skoljke_tadic',
    'bilja_suvozemni_puzevi_pavlovic',
    'sanja_paleogene_neogene_mammals',
    'minerals',
    'mineral_references',
    'mineral_rruff_matches',
    'rruff_chemistry',
    'rruff_localities',
    'rruff_minerals',
    'rruff_references',
    'meteorite_specimens',
    'collection_specimens',
    'collection_types',
    'inventory_entries',
    'bird_ringing_records',
    'bird_species',
    'digitized_profiles',
    'images',
    'heritage_categories',
    'heritage_items',
    'heritage_types',
    'library_books',
    'library_categories',
    'library_loans',
    'employee_publications',
    'scientific_papers',
    'paper_locality_links',
    'paper_feature_links',
    'users',
    'roles',
    'departments',
    'employee_profiles',
    'user_module_permissions',
    'vehicles',
    'signature_templates',
    'app_shared_settings',
    'mail_user_settings',
    'schema_migrations',
    'news_articles',
    'exhibitions',
    'exhibition_items',
    'exhibition_events',
]


class _FakeCursor:
    """Records normalized SQL and answers the two queries the command runs."""

    def __init__(self, tables, executed):
        self._tables = tables
        self.executed = executed
        self._last = ''

    def execute(self, sql, params=None):
        normalized = ' '.join(sql.split())
        self.executed.append(normalized)
        self._last = normalized

    def fetchall(self):
        if 'pg_tables' in self._last:
            return [(name,) for name in self._tables]
        return []

    def fetchone(self):
        if 'count(*)' in self._last:
            return (3,)
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class _FakeConnection:
    """Mimics ManagedPostgresConnection: commit on clean context exit."""

    def __init__(self, tables, executed, commits):
        self._tables = tables
        self.executed = executed
        self.commits = commits

    def cursor(self):
        return _FakeCursor(self._tables, self.executed)

    def commit(self):
        self.commits.append('commit')

    def rollback(self):
        self.commits.append('rollback')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        return False


class ResetTestDataCliTests(unittest.TestCase):
    def setUp(self):
        self.executed = []
        self.commits = []
        self.tables = list(reset_test_data.RESET_TABLES)
        self.runner = museum_app.app.test_cli_runner()

        self._tmp = tempfile.TemporaryDirectory()
        self.docs_dir = Path(self._tmp.name) / 'dokumenti'
        self.chat_dir = Path(self._tmp.name) / 'chat_files'
        self.docs_dir.mkdir()
        self.chat_dir.mkdir()
        (self.docs_dir / 'proba').mkdir()
        (self.docs_dir / 'proba' / 'v01_test.pdf').write_bytes(b'pdf')
        (self.chat_dir / 'slika.png').write_bytes(b'png')

        patchers = [
            patch.object(
                reset_test_data, 'get_postgres_connection',
                lambda **kwargs: _FakeConnection(
                    self.tables, self.executed, self.commits
                ),
            ),
            patch.object(
                reset_test_data, 'get_database_url', lambda: TEST_DB_URL
            ),
            patch.dict(
                os.environ, {'DOCUMENTS_STORAGE_PATH': str(self.docs_dir)}
            ),
            patch('chat_room.CHAT_FILES_DIR', self.chat_dir),
        ]
        for patcher in patchers:
            patcher.start()
            self.addCleanup(patcher.stop)
        self.addCleanup(self._tmp.cleanup)

    def _invoke(self, *args, **kwargs):
        return self.runner.invoke(args=['reset-test-data', *args], **kwargs)

    def _write_statements(self):
        return [
            sql for sql in self.executed
            if not sql.upper().startswith('SELECT')
        ]

    def test_dry_run_imenuje_tabele_i_ne_menja_nista(self):
        result = self._invoke()
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(self._write_statements(), [])
        self.assertIn('DRY-RUN', result.output)
        self.assertIn('nista nije izmenjeno', result.output)
        for table in reset_test_data.RESET_TABLES:
            self.assertIn(table, result.output)

    def test_dry_run_ne_dira_fajlove(self):
        result = self._invoke()
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertTrue((self.docs_dir / 'proba' / 'v01_test.pdf').exists())
        self.assertTrue((self.chat_dir / 'slika.png').exists())

    def test_execute_trunkira_tacno_oznacene_tabele(self):
        result = self._invoke('--execute', input=TEST_DB_NAME + '\n')
        self.assertEqual(result.exit_code, 0, result.output)
        truncates = [
            sql for sql in self.executed if sql.startswith('TRUNCATE')
        ]
        self.assertEqual(len(truncates), 1)
        self.assertIn('RESTART IDENTITY', truncates[0])
        for table in reset_test_data.RESET_TABLES:
            self.assertIn(f'"{table}"', truncates[0])
        self.assertEqual(self._write_statements(), truncates)
        self.assertIn('commit', self.commits)
        self.assertNotIn('rollback', self.commits)
        self.assertIn('GOTOVO', result.output)

    def test_execute_odbija_pogresno_ime_baze(self):
        result = self._invoke('--execute', input='pogresna_baza\n')
        self.assertNotEqual(result.exit_code, 0)
        self.assertEqual(self._write_statements(), [])
        self.assertIn('ne poklapa', result.output)
        self.assertTrue((self.docs_dir / 'proba' / 'v01_test.pdf').exists())

    def test_execute_prekida_ako_tabela_nedostaje(self):
        self.tables.remove('archive_requests')
        result = self._invoke('--execute', input=TEST_DB_NAME + '\n')
        self.assertNotEqual(result.exit_code, 0)
        self.assertEqual(self._write_statements(), [])
        self.assertIn('archive_requests', result.output)

    def test_execute_brise_fajlove_dokumenata_i_chata(self):
        result = self._invoke('--execute', input=TEST_DB_NAME + '\n')
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertTrue(self.docs_dir.is_dir())
        self.assertTrue(self.chat_dir.is_dir())
        self.assertEqual(list(self.docs_dir.iterdir()), [])
        self.assertEqual(list(self.chat_dir.iterdir()), [])

    def test_institucionalne_i_bibliotecke_tabele_netaknute(self):
        """EKSPLICITNI zastitni test: execute ne sme da pomene nijednu
        institucionalnu tabelu — zbirke, biblioteku (poimence), zaposlene,
        naloge, role, odeljenja, vozila kao entitete ni podesavanja."""
        result = self._invoke('--execute', input=TEST_DB_NAME + '\n')
        self.assertEqual(result.exit_code, 0, result.output)

        for table in INSTITUTIONAL_TABLES:
            self.assertNotIn(table, reset_test_data.RESET_TABLES)
            self.assertIn(table, reset_test_data.PROTECTED_TABLES)
            for sql in self._write_statements():
                self.assertNotIn(f'"{table}"', sql)

    def test_biblioteka_poimence_u_zastiti(self):
        for table in (
            'library_books', 'library_categories', 'library_loans',
            'employee_publications', 'scientific_papers',
            'paper_locality_links', 'paper_feature_links',
        ):
            self.assertIn(table, reset_test_data.PROTECTED_TABLES)
            self.assertNotIn(table, reset_test_data.RESET_TABLES)

    def test_spisak_za_brisanje_ne_sece_zastitu(self):
        self.assertEqual(
            set(reset_test_data.RESET_TABLES)
            & set(reset_test_data.PROTECTED_TABLES),
            set(),
        )


if __name__ == '__main__':
    unittest.main()
