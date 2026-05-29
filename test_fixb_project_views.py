"""Reproducing tests for confirmed medium-severity bugs in project_views.py.

Covers:
- Curator assignment silently dropped on save (sanitize_project_space allow-list).
- last_active_view wiped from disk during the auto-layout re-sync save.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-project-views')

import json
from pathlib import Path

import project_views


def test_sanitize_preserves_curator():
    """A curator value posted back from the client must survive sanitize."""
    raw_space = {
        'id': 'depot-6.4',
        'name': '6.4 Depo minerala i meteorita',
        'room_type': 'specimen_storage',
        'x': 10.0,
        'y': 10.0,
        'width': 5.0,
        'height': 5.0,
        'area_m2': 194.27,
        'specs': {
            'purpose': 'Чување збирке минерала',
            'curator': 'Александар Луковић',
        },
    }
    sanitized = project_views.sanitize_project_space(
        raw_space, project_space_library=project_views.PROJECT_SPACE_LIBRARY
    )
    assert sanitized is not None
    assert sanitized['specs'].get('curator') == 'Александар Луковић'


def test_resync_save_preserves_last_active_view(tmp_path, monkeypatch):
    """Auto-layout re-sync must not wipe last_active_view from disk."""
    planner_file = tmp_path / 'space_planner_state.json'

    # Persist a state at an OLD auto_layout_version that carries a real
    # last_active_view and one stored (depot) space so the sync branch runs.
    stored = {
        'version': 1,
        'auto_layout_version': 0,
        'plan': {'filename': project_views.PROJECT_SPACE_PLAN_FILE, 'title': 'x'},
        'spaces': [
            {
                'id': 'depot-6.4',
                'name': '6.4 Depo minerala i meteorita',
                'room_type': 'specimen_storage',
                'x': 12.0,
                'y': 12.0,
                'width': 6.0,
                'height': 9.0,
                'area_m2': 194.27,
                'specs': {'purpose': 'Чување збирке минерала'},
            }
        ],
        'last_active_view': 'depot',
        'last_updated_at': None,
        'last_updated_by': 'tester',
    }
    planner_file.write_text(json.dumps(stored), encoding='utf-8')

    state = project_views.load_project_space_planner_state(
        planner_file=planner_file,
        auto_layout_version=project_views.PROJECT_AUTO_LAYOUT_VERSION,
        project_space_plan_file=project_views.PROJECT_SPACE_PLAN_FILE,
        project_space_library=project_views.PROJECT_SPACE_LIBRARY,
        project_space_plan_image_size=project_views.PROJECT_SPACE_PLAN_IMAGE_SIZE,
        project_auto_detected_spaces=project_views.PROJECT_DEPOT_AUTO_DETECTED_SPACES,
        project_depot_auto_detected_spaces=project_views.PROJECT_DEPOT_AUTO_DETECTED_SPACES,
    )

    # Sanity: the sync branch ran and bumped the version.
    assert state['auto_layout_version'] == project_views.PROJECT_AUTO_LAYOUT_VERSION

    # The bug: the re-sync save wrote last_active_view=None to disk, so the
    # NEXT read from disk loses the view.
    on_disk = json.loads(planner_file.read_text(encoding='utf-8'))
    assert on_disk.get('last_active_view') == 'depot'
