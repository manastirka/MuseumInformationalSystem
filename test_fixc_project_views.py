"""Focused tests for LOW-severity hardening fixes in project_views.py (cluster: project-views)."""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-project-views')

import json
from unittest.mock import patch

import project_views

import pytest


@pytest.fixture(autouse=True)
def _planner_db_u_memoriji(monkeypatch):
    """Stavka 10 (revizija 2026-08): planer je prešao na PostgreSQL — unit
    testovi rade nad in-memory zamenom da ne diraju pravu bazu."""
    store = {}
    monkeypatch.setattr(project_views, '_planner_state_read_db',
                        lambda: store.get('state'))
    monkeypatch.setattr(project_views, '_planner_state_write_db',
                        lambda state, user: store.__setitem__('state', state))
    yield store


LIBRARY = project_views.PROJECT_SPACE_LIBRARY


# ---------------------------------------------------------------------------
# Finding 1: duplicate generated ids for multiple id-less spaces in one request
# ---------------------------------------------------------------------------
def test_idless_spaces_get_unique_generated_ids():
    """Two id-less spaces sanitized in the same millisecond must get distinct ids."""
    fixed_ms = 1_716_998_400.0
    with patch.object(project_views.time, 'time', return_value=fixed_ms):
        first = project_views.sanitize_project_space(
            {'name': 'A', 'width': 10, 'height': 10}, project_space_library=LIBRARY
        )
        second = project_views.sanitize_project_space(
            {'name': 'B', 'width': 10, 'height': 10}, project_space_library=LIBRARY
        )

    assert first['id'] and second['id']
    assert first['id'].startswith('space-')
    assert second['id'].startswith('space-')
    # Pre-fix both ids were f"space-{int(time.time()*1000)}" -> identical. Now unique.
    assert first['id'] != second['id']


def test_explicit_id_is_preserved():
    """An explicitly supplied id must be kept verbatim (no spurious suffix)."""
    space = project_views.sanitize_project_space(
        {'id': 'room-7', 'name': 'A', 'width': 10, 'height': 10},
        project_space_library=LIBRARY,
    )
    assert space['id'] == 'room-7'


# ---------------------------------------------------------------------------
# Finding 2: auto-sync must honor a user-stored edge coordinate of 0
# ---------------------------------------------------------------------------
def _detected_id_with_nonzero_xy():
    """Pick a depot detected space id whose template x and y are both > 0."""
    for raw in project_views.PROJECT_DEPOT_AUTO_DETECTED_SPACES:
        if float(raw.get('x', 0)) > 0 and float(raw.get('y', 0)) > 0:
            return raw['id'], float(raw['x']), float(raw['y'])
    raise AssertionError('no suitable detected space found')


def test_autosync_preserves_zero_edge_coordinate(tmp_path):
    """A room a user moved to x=0 / y=0 must not snap back to the template position."""
    space_id, tmpl_x, tmpl_y = _detected_id_with_nonzero_xy()
    assert tmpl_x > 0 and tmpl_y > 0

    planner_file = tmp_path / 'space_planner.json'
    stored = {
        'version': 1,
        'auto_layout_version': 0,  # forces auto-sync (mismatch with current version)
        'plan': {'filename': project_views.PROJECT_SPACE_PLAN_FILE, 'title': 't'},
        'spaces': [
            {
                'id': space_id,
                'name': 'Moved room',
                'room_type': 'specimen_storage',
                'x': 0.0,
                'y': 0.0,
                'width': 5.0,
                'height': 5.0,
                'area_m2': 12.0,
            }
        ],
        'last_active_view': None,
        'last_updated_at': None,
        'last_updated_by': 'tester',
    }
    planner_file.write_text(json.dumps(stored), encoding='utf-8')

    state = project_views.load_project_space_planner_state(
        planner_file=planner_file,
        auto_layout_version=project_views.PROJECT_AUTO_LAYOUT_VERSION,
        project_space_plan_file=project_views.PROJECT_SPACE_PLAN_FILE,
        project_space_library=LIBRARY,
        project_space_plan_image_size=project_views.PROJECT_SPACE_PLAN_IMAGE_SIZE,
        project_auto_detected_spaces=project_views.PROJECT_AUTO_DETECTED_SPACES,
        project_depot_auto_detected_spaces=project_views.PROJECT_DEPOT_AUTO_DETECTED_SPACES,
    )

    synced = {s['id']: s for s in state['spaces']}
    assert space_id in synced
    moved = synced[space_id]
    # Pre-fix: value > 0 guard reverted x/y to template (tmpl_x / tmpl_y).
    assert moved['x'] == 0.0
    assert moved['y'] == 0.0


def test_autosync_still_applies_positive_overrides(tmp_path):
    """Sanity: a positive stored coordinate is still honored after the fix."""
    space_id, tmpl_x, tmpl_y = _detected_id_with_nonzero_xy()
    planner_file = tmp_path / 'space_planner.json'
    stored = {
        'auto_layout_version': 0,
        'spaces': [
            {
                'id': space_id,
                'name': 'Moved room',
                'room_type': 'specimen_storage',
                'x': 42.5,
                'y': 17.25,
                'width': 5.0,
                'height': 5.0,
                'area_m2': 99.0,
            }
        ],
    }
    planner_file.write_text(json.dumps(stored), encoding='utf-8')

    state = project_views.load_project_space_planner_state(
        planner_file=planner_file,
        auto_layout_version=project_views.PROJECT_AUTO_LAYOUT_VERSION,
        project_space_plan_file=project_views.PROJECT_SPACE_PLAN_FILE,
        project_space_library=LIBRARY,
        project_space_plan_image_size=project_views.PROJECT_SPACE_PLAN_IMAGE_SIZE,
        project_auto_detected_spaces=project_views.PROJECT_AUTO_DETECTED_SPACES,
        project_depot_auto_detected_spaces=project_views.PROJECT_DEPOT_AUTO_DETECTED_SPACES,
    )
    moved = {s['id']: s for s in state['spaces']}[space_id]
    assert moved['x'] == 42.5
    assert moved['y'] == 17.25
    assert moved['area_m2'] == 99.0


# ---------------------------------------------------------------------------
# Finding 3: save must record a meaningful last_updated_by, never None/''
# ---------------------------------------------------------------------------
def _import_flask_app():
    import app as museum_app

    return museum_app.app


def test_save_falls_back_to_email_when_user_name_empty(tmp_path):
    """An empty (present-but-falsy) user_name must fall through to user_email."""
    flask_app = _import_flask_app()
    planner_file = tmp_path / 'space_planner.json'
    captured = {}

    def fake_save(payload, user_name, **kwargs):
        captured['user_name'] = user_name
        return {'spaces': payload.get('spaces', []), 'last_updated_by': user_name}

    with flask_app.test_request_context(
        '/api/project/space-planner/save',
        method='POST',
        json={'spaces': [{'id': 'r1', 'name': 'A', 'width': 10, 'height': 10}]},
    ):
        from flask import session

        session['user_name'] = ''  # present but empty -> the bug
        session['user_email'] = 'curator@example.com'
        with patch.object(project_views, 'save_project_space_planner_state', side_effect=fake_save):
            project_views.api_project_space_planner_save(
                planner_file=planner_file,
                auto_layout_version=project_views.PROJECT_AUTO_LAYOUT_VERSION,
                project_space_plan_file=project_views.PROJECT_SPACE_PLAN_FILE,
                project_space_library=LIBRARY,
            )

    # Pre-fix: session.get('user_name', default) returned '' (falsy present value).
    assert captured['user_name'] == 'curator@example.com'


def test_save_falls_back_to_unknown_when_no_identity(tmp_path):
    """With neither name nor email, last_updated_by becomes the 'unknown' sentinel."""
    flask_app = _import_flask_app()
    planner_file = tmp_path / 'space_planner.json'
    captured = {}

    def fake_save(payload, user_name, **kwargs):
        captured['user_name'] = user_name
        return {'spaces': payload.get('spaces', []), 'last_updated_by': user_name}

    with flask_app.test_request_context(
        '/api/project/space-planner/save',
        method='POST',
        json={'spaces': [{'id': 'r1', 'name': 'A', 'width': 10, 'height': 10}]},
    ):
        with patch.object(project_views, 'save_project_space_planner_state', side_effect=fake_save):
            project_views.api_project_space_planner_save(
                planner_file=planner_file,
                auto_layout_version=project_views.PROJECT_AUTO_LAYOUT_VERSION,
                project_space_plan_file=project_views.PROJECT_SPACE_PLAN_FILE,
                project_space_library=LIBRARY,
            )

    assert captured['user_name'] == 'unknown'
