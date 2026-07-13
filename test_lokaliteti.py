#!/usr/bin/env python3
"""Tests for the standalone locality registry (migration 027).

Covers: the seed source (DISTINCT card_locality, trimmed, no blanks, NO merging
of similar names), CSV parsing, idempotent insert, the registry-first API with
its fallback while the table is still empty, manual add (curator+), and the
refusal to delete a locality that specimens still reference.
"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ['FLASK_ENV'] = 'testing'
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

import app as museum_app
import depot_science_views
import lokaliteti_cli


ADMIN = {
    'user_id': 1, 'user_email': 'admin@nhmbeo.rs', 'user_name': 'Админ',
    'user_role': 'admin', 'is_admin': True,
    'user_department': None, 'is_department_head': False,
}
CURATOR = {
    'user_id': 3, 'user_email': 'kustos@nhmbeo.rs', 'user_name': 'Кустос',
    'user_role': 'curator', 'is_admin': False,
    'user_department': 'ГЕОЛОГИЈА', 'is_department_head': False,
}
EMPLOYEE = {
    'user_id': 10, 'user_email': 'radnik@nhmbeo.rs', 'user_name': 'Радник',
    'user_role': 'employee', 'is_admin': False,
    'user_department': 'ГЕОЛОГИЈА', 'is_department_head': False,
}


class _FakeCursor:
    def __init__(self, canned=None):
        self.canned = dict(canned or {})
        self._pending = None
        self.executed = []

    def execute(self, sql, params=None):
        self.executed.append((' '.join(sql.split()), params))
        for needle, row in self.canned.items():
            if needle in sql:
                self._pending = row(params) if callable(row) else row
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
        return False


# ---------------------------------------------------------------------------
# Seed izvor + CSV
# ---------------------------------------------------------------------------

class SeedSourceTests(unittest.TestCase):

    def test_zbirka_query_trims_and_skips_blanks(self):
        cur = _FakeCursor({'SELECT DISTINCT': [('Stari Trg, Trepča, Srbija',), ('Rudnik, Srbija',)]})
        nazivi = lokaliteti_cli.nazivi_iz_zbirke(cur)
        self.assertEqual(nazivi, ['Stari Trg, Trepča, Srbija', 'Rudnik, Srbija'])
        sql = cur.executed[0][0]
        self.assertIn('btrim(card_locality)', sql)
        self.assertIn("btrim(card_locality) <> ''", sql)

    def test_csv_keeps_commas_in_names(self):
        """Regresija: nazivi imaju zareze — slepo CSV-parsiranje bi 'Stari Trg,
        Trepča, Srbija' odseklo na 'Stari Trg'."""
        with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False,
                                         encoding='utf-8', newline='') as handle:
            handle.write('name\n"Stari Trg, Trepča, Srbija"\nRudnik, Srbija\n')
            putanja = handle.name
        self.addCleanup(os.unlink, putanja)

        nazivi = lokaliteti_cli.nazivi_iz_csv(putanja)

        # i navodnikovan (iz export-a) i go red (rucno kucan) ostaju celi
        self.assertEqual(nazivi, ['Stari Trg, Trepča, Srbija', 'Rudnik, Srbija'])

    def test_csv_skips_header_blanks_and_duplicates(self):
        with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False,
                                         encoding='utf-8', newline='') as handle:
            handle.write('name\nStari Trg, Trepča, Srbija\n\n  Rudnik, Srbija  \n'
                         'Stari Trg, Trepča, Srbija\n')  # duplikat i prazan red
            putanja = handle.name
        self.addCleanup(os.unlink, putanja)

        nazivi = lokaliteti_cli.nazivi_iz_csv(putanja)

        self.assertEqual(nazivi, ['Stari Trg, Trepča, Srbija', 'Rudnik, Srbija'])

    def test_similar_names_are_never_merged(self):
        """Naučni nazivi se ne diraju: 'Trepča' i 'Stari Trg, Trepča, Srbija'
        su i dalje DVA zapisa (nikakvo fuzzy spajanje)."""
        with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False,
                                         encoding='utf-8', newline='') as handle:
            handle.write('name\nTrepča\nStari Trg, Trepča, Srbija\ntrepča\n')
            putanja = handle.name
        self.addCleanup(os.unlink, putanja)

        nazivi = lokaliteti_cli.nazivi_iz_csv(putanja)

        self.assertEqual(len(nazivi), 3)
        self.assertIn('Trepča', nazivi)
        self.assertIn('trepča', nazivi)  # ni case-folding nije spajanje


class IdempotentInsertTests(unittest.TestCase):

    def test_insert_uses_on_conflict_do_nothing(self):
        cur = _FakeCursor({'INSERT INTO localities': {'id': 1}})
        ubaceno = lokaliteti_cli.upisi_nove(cur, ['A', 'B'], 'cli@nhmbeo.rs')
        self.assertEqual(ubaceno, 2)
        sql = cur.executed[0][0]
        self.assertIn('ON CONFLICT (name) DO NOTHING', sql)
        self.assertIn("'seed'", sql)

    def test_second_run_inserts_nothing(self):
        """Idempotentnost: kad INSERT ne vrati red (naziv postoji), broj je 0."""
        cur = _FakeCursor({'INSERT INTO localities': []})
        ubaceno = lokaliteti_cli.upisi_nove(cur, ['A', 'B'], 'cli@nhmbeo.rs')
        self.assertEqual(ubaceno, 0)


# ---------------------------------------------------------------------------
# API: šifarnik je izvor spiska, sa fallbackom dok je prazan
# ---------------------------------------------------------------------------

class _ApiTestCase(unittest.TestCase):

    def setUp(self):
        museum_app.app.config['TESTING'] = True
        csrf_was = museum_app.app.config.get('WTF_CSRF_ENABLED', False)
        museum_app.app.config['WTF_CSRF_ENABLED'] = False
        self.addCleanup(museum_app.app.config.__setitem__, 'WTF_CSRF_ENABLED', csrf_was)
        self.client = museum_app.app.test_client()

    def login(self, who):
        with self.client.session_transaction() as sess:
            sess.update(who)

    def use_db(self, canned):
        cursor = _FakeCursor(canned)
        conn = _FakeConnection(cursor)
        patcher = patch.object(
            depot_science_views, 'get_postgres_connection', lambda *a, **k: conn)
        patcher.start()
        self.addCleanup(patcher.stop)
        return cursor

    def use_minerals(self, minerals):
        class FakeDB:
            def get_all_minerals(self, page=1, per_page=50, **kw):
                return {'minerals': minerals, 'total': len(minerals)}

        patcher = patch.object(museum_app.app, 'get_mineral_database', lambda: FakeDB())
        patcher.start()
        self.addCleanup(patcher.stop)


class LocalityListTests(_ApiTestCase):

    def test_registry_locality_without_specimens_is_listed(self):
        self.use_db({'FROM localities': [(1, 'Терен Копаоник 2026', 'Србија', None, 'rucno')]})
        self.use_minerals([{'lokalitet': 'Rudnik, Srbija', 'naziv': 'Kvarc'}])
        self.login(ADMIN)

        response = self.client.get('/api/depot/localities', base_url='https://localhost')
        data = response.get_json()

        imena = {l['name']: l for l in data['localities']}
        self.assertIn('Терен Копаоник 2026', imena)          # bez ijednog predmeta
        self.assertEqual(imena['Терен Копаоник 2026']['count'], 0)
        self.assertEqual(imena['Терен Копаоник 2026']['source'], 'rucno')
        self.assertEqual(imena['Rudnik, Srbija']['count'], 1)  # iz zbirke, još nije u šifarniku
        self.assertEqual(data['registry_count'], 1)

    def test_empty_registry_falls_back_to_collection_aggregate(self):
        """Pre seed-a (i na produkciji) alat ne sme da bude prazan."""
        self.use_db({'FROM localities': []})
        self.use_minerals([
            {'lokalitet': 'Rudnik, Srbija', 'naziv': 'Kvarc'},
            {'lokalitet': 'Rudnik, Srbija', 'naziv': 'Galenit'},
            {'lokalitet': '   ', 'naziv': 'Bez lokaliteta'},
        ])
        self.login(ADMIN)

        data = self.client.get('/api/depot/localities',
                               base_url='https://localhost').get_json()

        self.assertTrue(data['success'])
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['localities'][0]['count'], 2)
        self.assertEqual(data['registry_count'], 0)


class LocalityCrudTests(_ApiTestCase):

    def test_curator_can_add_locality(self):
        cursor = self.use_db({'INSERT INTO localities': (7,)})
        self.login(CURATOR)

        response = self.client.post(
            '/api/depot/localities', json={'name': 'Рудник Благодат, Србија'},
            base_url='https://localhost')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['id'], 7)
        sql, params = cursor.executed[0]
        self.assertIn('ON CONFLICT (name) DO NOTHING', sql)
        self.assertIn("'rucno'", sql)
        self.assertEqual(params[0], 'Рудник Благодат, Србија')

    def test_plain_employee_cannot_add(self):
        self.login(EMPLOYEE)
        response = self.client.post('/api/depot/localities', json={'name': 'X'},
                                    base_url='https://localhost')
        self.assertIn(response.status_code, (302, 403))

    def test_empty_name_refused(self):
        self.use_db({})
        self.login(CURATOR)
        response = self.client.post('/api/depot/localities', json={'name': '   '},
                                    base_url='https://localhost')
        self.assertEqual(response.status_code, 400)

    def test_duplicate_name_conflicts(self):
        self.use_db({'INSERT INTO localities': []})   # ON CONFLICT -> nema RETURNING
        self.login(CURATOR)
        response = self.client.post('/api/depot/localities', json={'name': 'Rudnik, Srbija'},
                                    base_url='https://localhost')
        self.assertEqual(response.status_code, 409)

    def test_delete_refused_while_specimens_reference_it(self):
        self.use_db({
            'SELECT name FROM localities': ('Rudnik, Srbija',),
            'FROM minerals WHERE': (5,),
        })
        self.login(ADMIN)

        response = self.client.delete('/api/depot/localities/3', base_url='https://localhost')

        self.assertEqual(response.status_code, 409)
        self.assertIn('5', response.get_json()['message'])

    def test_delete_allowed_when_no_specimens(self):
        cursor = self.use_db({
            'SELECT name FROM localities': ('Терен Копаоник 2026',),
            'FROM minerals WHERE': (0,),
        })
        self.login(ADMIN)

        response = self.client.delete('/api/depot/localities/4', base_url='https://localhost')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(any('DELETE FROM localities' in sql for sql, _ in cursor.executed))


if __name__ == '__main__':
    unittest.main()
