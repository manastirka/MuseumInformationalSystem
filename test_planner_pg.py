"""Revizija 2026-08 (batch 6, stavka 10): planer prostora u PostgreSQL.

Nalaz: operativno stanje planera (admin/projekti/space-planner) živelo je
isključivo u data/project_space_planner.json — kršenje pravila da je
PostgreSQL jedini izvor istine. Migracija 050: singleton red (id=1, JSONB);
JSON fajl služi samo za jednokratni uvoz pri prvom čitanju.
"""

import json
import os
import unittest
from pathlib import Path

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-planner-pg')

import pytest
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / '.env')

import project_views

DATABASE_URL = os.environ.get('DATABASE_URL', '').replace(
    'postgresql+psycopg://', 'postgresql://')


@pytest.fixture
def store(monkeypatch):
    """In-memory zamena za singleton red u bazi."""
    memory = {}
    monkeypatch.setattr(project_views, '_planner_state_read_db',
                        lambda: memory.get('state'))

    def _write(state, user):
        memory['state'] = state
        memory['user'] = user

    monkeypatch.setattr(project_views, '_planner_state_write_db', _write)
    return memory


def _load(planner_file):
    return project_views.load_project_space_planner_state(
        planner_file=planner_file,
        auto_layout_version=project_views.PROJECT_AUTO_LAYOUT_VERSION,
        project_space_plan_file=project_views.PROJECT_SPACE_PLAN_FILE,
        project_space_library=project_views.PROJECT_SPACE_LIBRARY,
        project_space_plan_image_size=project_views.PROJECT_SPACE_PLAN_IMAGE_SIZE,
        project_auto_detected_spaces=project_views.PROJECT_AUTO_DETECTED_SPACES,
        project_depot_auto_detected_spaces=project_views.PROJECT_DEPOT_AUTO_DETECTED_SPACES,
    )


def _state(spaces=None, view='depot'):
    return {
        'version': 1,
        'auto_layout_version': project_views.PROJECT_AUTO_LAYOUT_VERSION,
        'plan': {'filename': project_views.PROJECT_SPACE_PLAN_FILE, 'title': 't'},
        'spaces': spaces or [],
        'last_active_view': view,
        'last_updated_at': '2026-08-11T00:00:00Z',
        'last_updated_by': 'tester',
    }


def test_save_pise_u_bazu_a_ne_na_disk(tmp_path, store):
    planner_file = tmp_path / 'planner.json'
    state = project_views.save_project_space_planner_state(
        {'spaces': [], 'last_active_view': 'depot'}, 'tester',
        planner_file=planner_file,
        auto_layout_version=project_views.PROJECT_AUTO_LAYOUT_VERSION,
        project_space_plan_file=project_views.PROJECT_SPACE_PLAN_FILE,
    )
    assert store['state']['last_active_view'] == 'depot'
    assert store['user'] == 'tester'
    assert not planner_file.exists(), 'JSON fajl se više ne piše (samo uvoz)'
    assert state['last_updated_by'] == 'tester'


def test_load_cita_iz_baze_ne_sa_diska(tmp_path, store):
    planner_file = tmp_path / 'planner.json'
    planner_file.write_text(json.dumps(_state(view='sa-diska')), encoding='utf-8')
    store['state'] = _state(view='iz-baze')

    state = _load(planner_file)
    assert state['last_active_view'] == 'iz-baze', \
        'baza je izvor istine kad red postoji — fajl se ignoriše'


def test_prvi_load_uvozi_json_jednokratno(tmp_path, store):
    """Nema reda u bazi + postoji JSON → sadržaj se uveze u bazu i vrati."""
    planner_file = tmp_path / 'planner.json'
    planner_file.write_text(json.dumps(_state(view='uvezeno')), encoding='utf-8')

    state = _load(planner_file)
    assert state['last_active_view'] == 'uvezeno'
    assert store.get('state', {}).get('last_active_view') == 'uvezeno', \
        'jednokratni uvoz mora da upiše stanje u bazu'


def test_bez_baze_i_bez_fajla_vraca_default(tmp_path, store):
    state = _load(tmp_path / 'nema.json')
    assert state['spaces'] == []
    assert state['last_active_view'] is None


class PlannerPgIntegrationTests(unittest.TestCase):
    """Pravi singleton red: šemu obezbeđuje test (migracija 050), zatečeni
    sadržaj se čuva i vraća u teardown-u."""

    def setUp(self):
        import psycopg
        if not DATABASE_URL:
            self.skipTest('DATABASE_URL is not configured')
        try:
            self.conn = psycopg.connect(DATABASE_URL, connect_timeout=5)
        except Exception as exc:
            self.skipTest(f'PostgreSQL unreachable: {exc}')
        sql = (Path(__file__).parent / 'migration'
               / '050_project_space_planner_state.sql').read_text(encoding='utf-8')
        with self.conn.cursor() as cur:
            cur.execute(sql)
            cur.execute('SELECT state, updated_by FROM project_space_planner_state '
                        'WHERE id = 1')
            self.prethodno = cur.fetchone()
        self.conn.commit()
        self.addCleanup(self._restore)

    def _restore(self):
        with self.conn.cursor() as cur:
            if self.prethodno is None:
                cur.execute('DELETE FROM project_space_planner_state WHERE id = 1')
            else:
                cur.execute(
                    """
                    INSERT INTO project_space_planner_state (id, state, updated_by)
                    VALUES (1, %s::jsonb, %s)
                    ON CONFLICT (id) DO UPDATE
                    SET state = EXCLUDED.state, updated_by = EXCLUDED.updated_by
                    """,
                    (json.dumps(self.prethodno[0]), self.prethodno[1]),
                )
        self.conn.commit()
        self.conn.close()

    def test_upsert_i_citanje_singleton_reda(self):
        marker = {'spaces': [], 'last_active_view': 'pytest-pg-proba'}
        project_views._planner_state_write_db(marker, 'pytest@example.com')
        project_views._planner_state_write_db(
            {'spaces': [], 'last_active_view': 'pytest-pg-proba-2'}, 'pytest@example.com')
        procitano = project_views._planner_state_read_db()
        self.assertEqual(procitano['last_active_view'], 'pytest-pg-proba-2')


if __name__ == '__main__':
    unittest.main()
