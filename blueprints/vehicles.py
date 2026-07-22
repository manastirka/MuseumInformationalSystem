"""Vehicle and virtual depot routes extracted from app.py."""

from flask import Blueprint

import vehicle_depot_views
from security_utils import admin_required, login_required, module_access_required


vehicles_bp = Blueprint('vehicles', __name__)


@vehicles_bp.route('/vehicle_reservations')
@login_required
def vehicle_reservations():
    """Display vehicle reservation calendar."""
    from app import get_museum_vehicles, get_vehicle_reservations

    return vehicle_depot_views.render_vehicle_reservations(
        get_museum_vehicles=get_museum_vehicles,
        get_vehicle_reservations=get_vehicle_reservations,
    )


@vehicles_bp.route('/add_vehicle_reservation', methods=['POST'])
@login_required
def add_vehicle_reservation():
    """Add new vehicle reservation."""
    import app as museum_app

    return vehicle_depot_views.handle_add_vehicle_reservation(
        phase3a_databases=getattr(museum_app, 'phase3a_databases', None),
        get_vehicle_reservations=museum_app.get_vehicle_reservations,
    )


@vehicles_bp.route('/vehicle_management')
@admin_required
def vehicle_management():
    """Display vehicle management page."""
    from app import get_museum_vehicles, get_vehicle_reservations

    return vehicle_depot_views.render_vehicle_management(
        get_museum_vehicles=get_museum_vehicles,
        get_vehicle_reservations=get_vehicle_reservations,
    )


@vehicles_bp.route('/add_vehicle', methods=['POST'])
@admin_required
def add_vehicle():
    """Add new vehicle."""
    import app as museum_app

    return vehicle_depot_views.handle_add_vehicle(
        phase3a_databases=getattr(museum_app, 'phase3a_databases', None),
        get_museum_vehicles=museum_app.get_museum_vehicles,
    )


@vehicles_bp.route('/edit_vehicle', methods=['POST'])
@admin_required
def edit_vehicle():
    """Edit existing vehicle."""
    import app as museum_app

    return vehicle_depot_views.handle_edit_vehicle(
        phase3a_databases=getattr(museum_app, 'phase3a_databases', None),
        get_museum_vehicles=museum_app.get_museum_vehicles,
    )


@vehicles_bp.route('/delete_vehicle', methods=['POST'])
@admin_required
def delete_vehicle():
    """Delete vehicle."""
    import app as museum_app

    return vehicle_depot_views.handle_delete_vehicle(
        phase3a_databases=getattr(museum_app, 'phase3a_databases', None),
        get_museum_vehicles=museum_app.get_museum_vehicles,
    )


@vehicles_bp.route('/admin/virtual_depot')
@module_access_required('mineral_database')
def virtual_depot():
    """3D Virtual Mineral Depot - Three.js visualization of mineral storage."""
    return vehicle_depot_views.render_virtual_depot()


@vehicles_bp.route('/api/depot/boxes', methods=['GET'])
@login_required
def api_get_depot_boxes():
    """Get all boxes with mineral counts for 3D depot."""
    return vehicle_depot_views.api_get_depot_boxes()


@vehicles_bp.route('/api/depot/box/<box_id>', methods=['GET'])
@login_required
def api_get_box_contents(box_id):
    """Get contents of a specific box."""
    return vehicle_depot_views.api_get_box_contents(box_id)
