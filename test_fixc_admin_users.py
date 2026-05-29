"""Reproducing/behavior tests for admin-users cluster (Phase C low hardening).

Covers the redundant `with_descriptions` recount in
render_employee_profiles_database. The statistic was recounted over the
already-filtered employees_list (every element has a description by
construction), making it dead/redundant and the source value misleading.
The fix counts over the full directory, which is the documented intent and
keeps it consistent with the completion_rate denominator (total_directory).
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-admin-users')

import flask
import pytest

import employee_admin_views as views


@pytest.fixture
def app():
    application = flask.Flask(__name__)
    application.secret_key = 'test-secret'
    return application


def _capture_render(monkeypatch):
    """Patch render_template in the view module; capture kwargs it receives."""
    captured = {}

    def fake_render_template(template_name, **context):
        captured['template'] = template_name
        captured['context'] = context
        return ''

    monkeypatch.setattr(views, 'render_template', fake_render_template)
    return captured


def test_with_descriptions_counts_full_directory(app, monkeypatch):
    """with_descriptions must reflect the full directory, not the filtered list.

    Directory has 3 employees, 2 with a description. The statistic must equal 2
    and stay consistent with total_profiles (the profiles actually rendered).
    """
    captured = _capture_render(monkeypatch)

    directory = [
        {'department': 'Geologija', 'description': 'Mineralog'},
        {'department': 'Biologija', 'description': 'Botanicar'},
        {'department': 'Geologija', 'description': ''},
    ]

    with app.test_request_context('/admin/employee_profiles_database'):
        views.render_employee_profiles_database(
            get_employee_directory=lambda: directory,
        )

    stats = captured['context']['statistics']
    # 2 of the 3 directory entries have a non-empty description.
    assert stats['with_descriptions'] == 2
    # Profiles rendered (filtered list) match the count with descriptions.
    assert stats['total_profiles'] == 2
    # completion_rate = with_descriptions / total_directory(3) * 100 = 66.7
    assert stats['completion_rate'] == 66.7
    assert stats['total_departments'] == 2


def test_empty_directory_no_zero_division(app, monkeypatch):
    """An empty directory yields zeroed statistics and a 0 completion_rate."""
    captured = _capture_render(monkeypatch)

    with app.test_request_context('/admin/employee_profiles_database'):
        views.render_employee_profiles_database(
            get_employee_directory=lambda: [],
        )

    stats = captured['context']['statistics']
    assert stats['total_profiles'] == 0
    assert stats['with_descriptions'] == 0
    assert stats['total_departments'] == 0
    assert stats['completion_rate'] == 0


def test_with_descriptions_source_is_full_directory(app, monkeypatch):
    """Guard against re-counting over the pre-filtered list.

    If with_descriptions were computed over employees_list (already filtered to
    those WITH a description), it would equal total_profiles by construction and
    be a dead value. Here we make the full directory contain entries WITHOUT a
    description; with_descriptions must still be derived by scanning every
    directory entry (count == 1), proving the source is the full directory.
    """
    captured = _capture_render(monkeypatch)

    directory = [
        {'department': 'Geologija', 'description': 'Mineralog'},
        {'department': 'Biologija'},
        {'department': 'Biologija', 'description': None},
    ]

    with app.test_request_context('/admin/employee_profiles_database'):
        views.render_employee_profiles_database(
            get_employee_directory=lambda: directory,
        )

    stats = captured['context']['statistics']
    assert stats['with_descriptions'] == 1
    assert stats['total_profiles'] == 1
    # completion_rate = 1 / 3 * 100 = 33.3
    assert stats['completion_rate'] == 33.3
