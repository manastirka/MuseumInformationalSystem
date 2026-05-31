"""Project-related routes extracted from app.py."""

from pathlib import Path

from flask import Blueprint, current_app

import project_views
from security_utils import login_required


projects_bp = Blueprint('projects', __name__)

PROJECT_SPACE_PLANNER_RELATIVE_PATH = Path('data') / 'project_space_planner.json'
PROJECT_SPACE_PLAN_FILE = project_views.PROJECT_SPACE_PLAN_FILE
PROJECT_SPACE_PLAN_IMAGE_SIZE = project_views.PROJECT_SPACE_PLAN_IMAGE_SIZE
PROJECT_SPACE_DEPOT_PLAN_FILE = project_views.PROJECT_SPACE_DEPOT_PLAN_FILE
PROJECT_SPACE_DEPOT_PLAN_IMAGE_SIZE = project_views.PROJECT_SPACE_DEPOT_PLAN_IMAGE_SIZE
PROJECT_DEPOT_PLAN_AREA_ANNOTATIONS = project_views.PROJECT_DEPOT_PLAN_AREA_ANNOTATIONS
PROJECT_DEPOT_AUTO_DETECTED_SPACES = project_views.PROJECT_DEPOT_AUTO_DETECTED_SPACES
PROJECT_AUTO_LAYOUT_VERSION = project_views.PROJECT_AUTO_LAYOUT_VERSION
PROJECT_SPACE_PLAN_VIEWS = project_views.PROJECT_SPACE_PLAN_VIEWS
PROJECT_SPACE_LIBRARY = project_views.PROJECT_SPACE_LIBRARY
PROJECT_COMMON_TERMS = project_views.PROJECT_COMMON_TERMS
PROJECT_AUTO_DETECTED_SPACES = project_views.PROJECT_AUTO_DETECTED_SPACES


def _project_space_planner_file():
    return Path(current_app.root_path) / PROJECT_SPACE_PLANNER_RELATIVE_PATH


@projects_bp.route('/admin/projekti')
@login_required
def admin_projekti():
    """View the new museum building project page."""
    return project_views.render_projects_page()


@projects_bp.route('/admin/projekti/dokumentacija')
@login_required
def admin_projekti_dokumentacija():
    """Read project documentation inline inside the application."""
    return project_views.render_project_documentation(
        app_root_path=current_app.root_path,
    )


@projects_bp.route('/admin/projekti/space-planner')
@login_required
def admin_projekti_space_planner():
    """Interactive editor for plan -5 room specifications."""
    return project_views.render_project_space_planner()


@projects_bp.route('/api/projekti/space-planner')
@login_required
def api_projekti_space_planner_get():
    """Return stored room zones and terminology for the -5 plan editor."""
    return project_views.api_project_space_planner_get(
        planner_file=_project_space_planner_file(),
        auto_layout_version=PROJECT_AUTO_LAYOUT_VERSION,
        project_space_plan_views=PROJECT_SPACE_PLAN_VIEWS,
        project_space_plan_file=PROJECT_SPACE_PLAN_FILE,
        project_space_plan_image_size=PROJECT_SPACE_PLAN_IMAGE_SIZE,
        project_space_library=PROJECT_SPACE_LIBRARY,
        project_common_terms=PROJECT_COMMON_TERMS,
        project_auto_detected_spaces=PROJECT_AUTO_DETECTED_SPACES,
        project_depot_auto_detected_spaces=PROJECT_DEPOT_AUTO_DETECTED_SPACES,
    )


@projects_bp.route('/api/projekti/space-planner', methods=['POST'])
@login_required
def api_projekti_space_planner_save():
    """Persist room zones and room specifications for the -5 plan editor."""
    return project_views.api_project_space_planner_save(
        planner_file=_project_space_planner_file(),
        auto_layout_version=PROJECT_AUTO_LAYOUT_VERSION,
        project_space_plan_file=PROJECT_SPACE_PLAN_FILE,
        project_space_library=PROJECT_SPACE_LIBRARY,
    )


@projects_bp.route('/projekti_files/<path:filename>')
@login_required
def projekti_file(filename):
    """Serve files from the Projekti folder."""
    return project_views.serve_project_file(
        filename,
        project_directory='Projekti',
    )
