"""Collection management routes extracted from app.py."""

from flask import Blueprint, current_app, flash, redirect, session, url_for

import collection_management_views
import museum_content_views
import museum_overview_views
from collection_registry import (
    COLLECTION_LIST_ENTRIES,
    COLLECTION_TYPE_MODULE_MAP,
    build_collection_database_map,
)
from security_utils import admin_required, login_required, module_access_required


collections_bp = Blueprint('collections', __name__)


def _ensure_collection_type_access(collection_type):
    module_key = COLLECTION_TYPE_MODULE_MAP.get(collection_type)
    if not module_key:
        flash('Непозната збирка.', 'danger')
        return redirect(url_for('museum_databases'))

    access_checker = getattr(current_app, 'user_has_module_access', None)
    user_email = session.get('user_email', '')
    user_role = session.get('user_role', '')

    if access_checker is None or not access_checker(user_email, user_role, module_key):
        flash('Немате дозволу за приступ овој збирци.', 'danger')
        return redirect(url_for('dashboard'))

    return None


def _render_collection_list(entry):
    """Render a registered collection list view."""
    import app as museum_app

    if entry.render_mode == 'meteorite':
        return collection_management_views.render_meteorite_collection(
            get_meteorite_collection_database=museum_app.get_meteorite_collection_database,
            prepare_collection_records_for_display=museum_app.prepare_collection_records_for_display,
            get_qr_collection_action_url=museum_app.get_qr_collection_action_url,
        )

    database = getattr(museum_app, entry.database_attr)
    records = database['specimens']
    if entry.strip_source_file:
        records = [
            {key: value for key, value in record.items() if key != 'source_file'}
            for record in records
        ]

    kwargs = {
        'collection_name': entry.collection_name,
        'collection_icon': entry.collection_icon,
        'collection_type': entry.collection_type,
        'records': records,
        'statistics': database['statistics'],
        'prepare_collection_records_for_display': museum_app.prepare_collection_records_for_display,
        'get_qr_collection_action_url': museum_app.get_qr_collection_action_url,
    }
    if (
        not entry.collection_actions_enabled
        or not entry.collection_add_enabled
        or not entry.collection_export_enabled
    ):
        kwargs['collection_actions_enabled'] = entry.collection_actions_enabled
        kwargs['collection_add_enabled'] = entry.collection_add_enabled
        kwargs['collection_export_enabled'] = entry.collection_export_enabled

    return collection_management_views.render_standard_collection_database(**kwargs)


def _register_collection_list_routes(blueprint):
    """Register list-view routes from the central collection registry."""
    for entry in COLLECTION_LIST_ENTRIES:
        def make_view(collection_entry=entry):
            @module_access_required(collection_entry.module_key)
            def view():
                return _render_collection_list(collection_entry)

            view.__name__ = collection_entry.route_slug
            view.__doc__ = f'{collection_entry.collection_name} collection database.'
            return view

        blueprint.add_url_rule(
            f'/admin/{entry.route_slug}',
            endpoint=entry.route_slug,
            view_func=make_view(),
        )


_register_collection_list_routes(collections_bp)


@collections_bp.route('/admin/mineral_collection')
@module_access_required('mineral_database')
def admin_mineral_collection():
    """Mineral collection database."""
    import app as museum_app

    return collection_management_views.render_mineral_collection(
        get_mineral_database=museum_app.get_mineral_database,
    )


@collections_bp.route('/admin/mineral_detail/<int:mineral_id>')
@module_access_required('mineral_database')
def admin_mineral_detail(mineral_id):
    """Mineral detail view."""
    import app as museum_app

    return collection_management_views.render_mineral_detail(
        mineral_id,
        get_mineral_database=museum_app.get_mineral_database,
    )


@collections_bp.route('/admin/rruff_minerals')
@module_access_required('mineral_database')
def admin_rruff_minerals():
    """Redirect to mineral collection in RRUFF mode."""
    return collection_management_views.redirect_rruff_minerals()


@collections_bp.route('/admin/rruff/detail/<int:mineral_id>')
@module_access_required('mineral_database')
def admin_rruff_detail(mineral_id):
    """RRUFF mineral detail view."""
    import app as museum_app

    return collection_management_views.render_rruff_detail(
        mineral_id,
        get_mineral_database=museum_app.get_mineral_database,
    )


@collections_bp.route('/admin/add_mineral', methods=['GET', 'POST'])
@module_access_required('mineral_database')
def add_mineral():
    """Add a new mineral to the collection."""
    import app as museum_app

    return collection_management_views.handle_add_mineral(
        get_mineral_database=museum_app.get_mineral_database,
    )


@collections_bp.route('/admin/edit_mineral/<int:mineral_id>', methods=['GET', 'POST'])
@module_access_required('mineral_database')
def edit_mineral(mineral_id):
    """Edit an existing mineral."""
    import app as museum_app

    return collection_management_views.handle_edit_mineral(
        mineral_id,
        get_mineral_database=museum_app.get_mineral_database,
    )


@collections_bp.route('/admin/delete_mineral/<int:mineral_id>', methods=['POST'])
@module_access_required('mineral_database')
def delete_mineral(mineral_id):
    """Delete a mineral from the collection."""
    import app as museum_app

    return collection_management_views.handle_delete_mineral(
        mineral_id,
        get_mineral_database=museum_app.get_mineral_database,
    )


@collections_bp.route('/admin/inventory_book')
@module_access_required('mineral_database')
def inventory_book():
    """Inventory book records."""
    return collection_management_views.render_inventory_book()


@collections_bp.route('/admin/inventory_reconciliation', endpoint='inventory_reconciliation')
@module_access_required('mineral_database')
def inventory_reconciliation_view():
    """Inventory reconciliation tool."""
    return collection_management_views.render_inventory_reconciliation()


@collections_bp.route('/admin/conservation_biology')
@admin_required
def conservation_biology():
    """Conservation biology records database."""
    import app as museum_app

    return collection_management_views.render_conservation_biology(
        conservation_biology_database=museum_app.CONSERVATION_BIOLOGY_DATABASE,
    )


@collections_bp.route('/admin/export_collection_to_pdf/<collection_type>')
@login_required
def export_collection_to_pdf(collection_type):
    """Export collection to PDF."""
    access_denied = _ensure_collection_type_access(collection_type)
    if access_denied is not None:
        return access_denied
    return collection_management_views.export_collection_to_pdf(collection_type)


@collections_bp.route('/admin/museum_databases')
@module_access_required('museum_databases')
def museum_databases():
    """Overview of all museum databases."""
    import app as museum_app

    if museum_app.LIBRARY_DATABASE is None:
        museum_app.LIBRARY_DATABASE = museum_app.load_library_database()
    return museum_overview_views.render_museum_databases(
        library_database=museum_app.LIBRARY_DATABASE,
        get_employee_directory=museum_app.get_employee_directory,
        get_museum_employees=museum_app.get_museum_employees,
        get_mineral_database=museum_app.get_mineral_database,
        get_cultural_heritage_database=museum_app.get_cultural_heritage_database,
        get_exhibit_statistics=museum_app.get_exhibit_statistics,
        get_exhibition_statistics=museum_app.get_exhibition_statistics,
        bird_ringing_database=museum_app.bird_ringing_database,
        scientific_papers_database=museum_app.scientific_papers_database,
        collection_databases=build_collection_database_map(museum_app),
        conservation_biology_database=museum_app.CONSERVATION_BIOLOGY_DATABASE,
        visitor_records=museum_content_views.load_visitor_records(),
        research_projects=museum_content_views.load_research_projects(),
        get_qr_collection_action_url=museum_app.get_qr_collection_action_url,
        user_has_module_access=museum_app.user_has_module_access,
    )


@collections_bp.route('/admin/add_collection_item/<collection_type>', methods=['GET', 'POST'])
@module_access_required('museum_databases')
def add_collection_item(collection_type):
    """Add new item to a curator collection."""
    access_denied = _ensure_collection_type_access(collection_type)
    if access_denied is not None:
        return access_denied
    return collection_management_views.handle_add_collection_item(
        collection_type,
        museum_databases_endpoint='museum_databases',
    )


@collections_bp.route('/admin/edit_sanja_paleogene_neogene_mammal/<record_id>', methods=['GET', 'POST'])
@module_access_required('sanja_paleogene_neogene_mammals')
def edit_sanja_paleogene_neogene_mammal(record_id):
    """Edit an existing Sanja Paleogene/Neogene large mammal record."""
    return collection_management_views.handle_edit_sanja_paleogene_neogene_mammal_item(record_id)


@collections_bp.route('/admin/edit_bilja/<collection_key>/<int:record_id>', methods=['GET', 'POST'])
def edit_bilja_item(collection_key, record_id):
    """Edit (or delete on POST _action=delete) a Bilja specimen."""
    access_denied = _ensure_collection_type_access(collection_key)
    if access_denied is not None:
        return access_denied
    return collection_management_views.handle_edit_bilja_item(collection_key, record_id)
