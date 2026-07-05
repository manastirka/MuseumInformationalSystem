"""Reproducing tests for admin-users cluster (Phase B medium bugs).

Covers the stale-reference persistence bug in:
- grant_module_access / revoke_module_access
- customize_dashboard_preferences

Root cause: the view receives `module_access` / `dashboard_preferences` as a
parameter captured BEFORE the loader runs. The loader reassigns the backing
global and returns the fresh object. `save_*()` persists the fresh global, but
the view mutated the stale parameter, so the change is silently dropped.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-admin-users')

import flask
import pytest

import admin_user_management_views as views


@pytest.fixture
def app():
    application = flask.Flask(__name__)
    application.secret_key = 'test-secret'
    application.add_url_rule('/manage', 'manage_user_access', lambda: '', methods=['GET'])
    application.add_url_rule('/dashboard', 'dashboard', lambda: '', methods=['GET'])
    return application


def _make_module_access_state():
    """Return (persisted, loader, saver, captured_param).

    Simulates app.py semantics:
    - The 'global' lives in a dict cell.
    - loader() reassigns the global to a FRESH deep-equal object and returns it.
    - saver() persists whatever the global currently references.
    - captured_param is the object captured BEFORE the loader runs (what the
      blueprint binds as module_access=museum_app.MODULE_ACCESS).
    """
    initial = {
        'minerali': {
            'name': 'Минерали',
            'default_access': False,
            'authorized_users': ['admin'],
        }
    }
    import copy

    cell = {'global': initial}
    persisted = {'value': None}
    captured_param = cell['global']

    def loader(force=False):
        # Mirror load_module_access: reassign global to a fresh object, return it.
        cell['global'] = copy.deepcopy(cell['global'])
        return cell['global']

    def saver():
        persisted['value'] = copy.deepcopy(cell['global'])
        return True

    return persisted, loader, saver, captured_param, cell


def test_grant_module_access_persists_change(app):
    persisted, loader, saver, captured_param, cell = _make_module_access_state()

    with app.test_request_context(
        '/manage', method='POST',
        data={'user_email': 'pera@nhmbeo.rs', 'module_key': 'minerali'},
    ):
        views.grant_module_access(
            load_module_access=loader,
            save_module_access=saver,
            module_access=captured_param,
        )

    # The grant must be present in what was actually persisted.
    assert persisted['value'] is not None, "save was never called"
    assert 'pera@nhmbeo.rs' in persisted['value']['minerali']['authorized_users'], (
        "grant was lost: change applied to stale param, not the persisted global"
    )


def test_revoke_module_access_persists_change(app):
    persisted, loader, saver, captured_param, cell = _make_module_access_state()
    # Pre-grant pera so we can revoke.
    captured_param['minerali']['authorized_users'].append('pera@nhmbeo.rs')
    cell['global'] = captured_param  # keep them aligned at start

    with app.test_request_context(
        '/manage', method='POST',
        data={'user_email': 'pera@nhmbeo.rs', 'module_key': 'minerali'},
    ):
        views.revoke_module_access(
            load_module_access=loader,
            save_module_access=saver,
            module_access=captured_param,
        )

    assert persisted['value'] is not None, "save was never called"
    assert 'pera@nhmbeo.rs' not in persisted['value']['minerali']['authorized_users'], (
        "revoke was lost: change applied to stale param, not the persisted global"
    )


def test_customize_dashboard_persists_widgets(app):
    saved = {'value': None}

    def save_user_elements(user_email, elements):
        saved['value'] = (user_email, list(elements))
        return True

    module_access = {
        'museum_databases': {'name': 'Базе', 'description': 'опис', 'icon': 'bi-database'},
        'maps': {'name': 'Карте', 'description': 'опис', 'icon': 'bi-map'},
    }

    with app.test_request_context(
        '/dashboard/customize', method='POST',
        data={'widgets': ['museum_databases', 'maps']},
    ):
        flask.session['user_email'] = 'pera@nhmbeo.rs'
        flask.session['user_role'] = 'employee'
        views.customize_dashboard_preferences(
            load_dashboard_preferences=lambda force=False: {},
            load_module_access=lambda force=False: module_access,
            user_has_module_access=lambda *a, **k: True,
            load_saved_elements=lambda email: None,
            save_user_elements=save_user_elements,
            dashboard_endpoint='dashboard',
        )

    assert saved['value'] == (
        'pera@nhmbeo.rs', ['museum_databases', 'maps']
    ), "widget selection was not persisted for the user"
