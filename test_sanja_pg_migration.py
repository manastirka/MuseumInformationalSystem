"""Tests for the Sanja collection PostgreSQL migration (dual-mode dispatch).

The live PostgreSQL path needs a DB + the sanja table (applied via migration 010),
so here we verify the dispatch logic: Postgres is used when available, and the
JSON fallback is preserved (unchanged behaviour) when it is not.
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-sanja-pg')

import collection_management_views as cmv


class TestSanjaBackendSelection:
    def test_pg_backend_is_none_without_database_url(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop('DATABASE_URL', None)
            assert cmv._sanja_pg() is None

    def test_pg_backend_is_none_when_table_missing(self):
        fake = MagicMock()
        fake.sanja_table_exists.return_value = False
        with patch.dict(os.environ, {'DATABASE_URL': 'postgresql://x'}, clear=False), \
             patch.dict('sys.modules', {'phase3a_databases': fake}):
            assert cmv._sanja_pg() is None


class TestSanjaLoad:
    def test_load_uses_postgres_when_available(self):
        fake_pg = MagicMock()
        fake_pg.get_sanja_specimens.return_value = [
            {'id': 1, 'specimen_name': 'Mammuthus', 'location_found': 'Kostolac', 'identified_by': 'А.Б.'},
            {'id': 2, 'specimen_name': 'Mammuthus', 'location_found': 'Виминацијум', 'identified_by': 'А.Б.'},
        ]
        with patch.object(cmv, '_sanja_pg', return_value=fake_pg):
            payload = cmv._load_sanja_database_payload()
        assert payload['specimens'] == fake_pg.get_sanja_specimens.return_value
        # statistics are recomputed from the PG specimens
        assert payload['statistics']['total_specimens'] == 2
        assert payload['statistics']['total_taxa'] == 1          # one distinct specimen_name
        assert payload['statistics']['total_localities'] == 2    # two distinct localities

    def test_load_falls_back_to_json_when_no_pg(self):
        tmp = Path(tempfile.mkdtemp()) / 'sanja.json'
        tmp.write_text(json.dumps({
            'metadata': {'name': 'X'},
            'specimens': [{'id': 7, 'specimen_name': 'Bos'}],
            'statistics': {},
        }), encoding='utf-8')
        with patch.object(cmv, '_sanja_pg', return_value=None), \
             patch.object(cmv, '_SANJA_DATABASE_PATH', tmp):
            payload = cmv._load_sanja_database_payload()
        assert [s['id'] for s in payload['specimens']] == [7]


class TestSanjaSave:
    def test_save_writes_to_postgres_when_available(self):
        fake_pg = MagicMock()
        with patch.object(cmv, '_sanja_pg', return_value=fake_pg):
            cmv._save_sanja_database_payload({'specimens': [{'id': 1, 'specimen_name': 'M'}], 'metadata': {}})
        fake_pg.replace_sanja_specimens.assert_called_once()
        saved = fake_pg.replace_sanja_specimens.call_args[0][0]
        assert [s['id'] for s in saved] == [1]

    def test_save_falls_back_to_json_when_no_pg(self):
        tmp = Path(tempfile.mkdtemp()) / 'sanja.json'
        with patch.object(cmv, '_sanja_pg', return_value=None), \
             patch.object(cmv, '_SANJA_DATABASE_PATH', tmp):
            cmv._save_sanja_database_payload({'specimens': [{'id': 1, 'specimen_name': 'M'}], 'metadata': {}})
        assert tmp.exists()
        data = json.loads(tmp.read_text(encoding='utf-8'))
        assert data['specimens'][0]['id'] == 1
        assert data['statistics']['total_specimens'] == 1
