"""QR admin routes extracted from app.py."""

from flask import Blueprint, current_app

import qr_label_views
import qr_management_views
from security_utils import login_required


qr_bp = Blueprint('qr', __name__)


@qr_bp.route('/admin/qr_generator')
@login_required
def admin_qr_generator():
    """Legacy QR generator entry point kept as a redirect to scoped collection pages."""
    return qr_management_views.render_admin_qr_generator(
        user_has_module_access=current_app.user_has_module_access,
    )


@qr_bp.route('/admin/qr_field_selection/<collection_type>', methods=['GET'])
@login_required
def admin_qr_field_selection(collection_type):
    """Field selection interface for QR code generation."""
    return qr_management_views.render_admin_qr_field_selection(
        collection_type,
        normalize_qr_collection_type=current_app.normalize_qr_collection_type,
        ensure_qr_collection_access=current_app.ensure_qr_collection_access,
    )


@qr_bp.route('/admin/qr_labels_with_fields/<collection_type>', methods=['POST'])
@login_required
def admin_qr_labels_with_fields(collection_type):
    """Generate QR codes with custom field selection."""
    return qr_management_views.handle_admin_qr_labels_with_fields(
        collection_type,
        normalize_qr_collection_type=current_app.normalize_qr_collection_type,
        ensure_qr_collection_access=current_app.ensure_qr_collection_access,
        get_meteorite_collection_database=current_app.get_meteorite_collection_database,
        botany_collection_database=current_app.botany_collection_database,
        paleozoology_collection_database=current_app.paleozoology_collection_database,
    )


@qr_bp.route('/admin/qr_boxes/minerals', methods=['GET'])
@login_required
def admin_qr_mineral_boxes():
    """Select mineral storage boxes for QR code generation."""
    return qr_management_views.render_admin_qr_mineral_boxes(
        ensure_qr_collection_access=current_app.ensure_qr_collection_access,
        get_mineral_database=current_app.get_mineral_database,
    )


@qr_bp.route('/admin/qr_boxes/minerals/generate', methods=['POST'])
@login_required
def admin_generate_box_qr_codes():
    """Generate QR codes for selected mineral boxes."""
    return qr_management_views.handle_admin_generate_box_qr_codes(
        ensure_qr_collection_access=current_app.ensure_qr_collection_access,
    )


@qr_bp.route('/admin/qr_select/<collection_type>', methods=['GET'])
@login_required
def admin_qr_select_specimens(collection_type):
    """Specimen selection interface with filters."""
    return qr_label_views.render_admin_qr_select_specimens(
        collection_type,
        normalize_qr_collection_type=current_app.normalize_qr_collection_type,
        ensure_qr_collection_access=current_app.ensure_qr_collection_access,
        get_qr_collection_name=current_app.get_qr_collection_name,
        get_qr_collection_url=current_app.get_qr_collection_url,
        get_mineral_database=current_app.get_mineral_database,
        get_qr_collection_records=current_app.get_qr_collection_records,
        get_qr_record_identifier=current_app.get_qr_record_identifier,
        get_qr_record_catalog_label=current_app.get_qr_record_catalog_label,
        get_qr_record_name=current_app.get_qr_record_name,
        get_qr_record_summary=current_app.get_qr_record_summary,
        get_qr_record_location=current_app.get_qr_record_location,
    )


@qr_bp.route('/admin/qr_labels_selected/<collection_type>', methods=['POST'])
@login_required
def admin_qr_labels_selected(collection_type):
    """Generate QR codes for selected specimens only."""
    return qr_label_views.handle_admin_qr_labels_selected(
        collection_type,
        normalize_qr_collection_type=current_app.normalize_qr_collection_type,
        ensure_qr_collection_access=current_app.ensure_qr_collection_access,
        get_mineral_database=current_app.get_mineral_database,
        get_qr_collection_records=current_app.get_qr_collection_records,
        get_qr_record_identifier=current_app.get_qr_record_identifier,
        get_qr_record_catalog_label=current_app.get_qr_record_catalog_label,
        get_qr_record_name=current_app.get_qr_record_name,
        build_collection_highlight_qr_url=current_app.build_collection_highlight_qr_url,
        get_qr_collection_name=current_app.get_qr_collection_name,
    )


@qr_bp.route('/admin/qr_label_format/<collection_type>')
@login_required
def admin_qr_label_format(collection_type):
    """Show label format selection for QR code generation."""
    return qr_label_views.render_admin_qr_label_format(
        collection_type,
        normalize_qr_collection_type=current_app.normalize_qr_collection_type,
        ensure_qr_collection_access=current_app.ensure_qr_collection_access,
        get_qr_collection_name=current_app.get_qr_collection_name,
        get_qr_collection_url=current_app.get_qr_collection_url,
    )


@qr_bp.route('/admin/qr_labels_with_format/<collection_type>', methods=['POST'])
@login_required
def admin_qr_labels_with_format(collection_type):
    """Generate QR codes with selected label format."""
    return qr_label_views.handle_admin_qr_labels_with_format(
        collection_type,
        normalize_qr_collection_type=current_app.normalize_qr_collection_type,
        ensure_qr_collection_access=current_app.ensure_qr_collection_access,
        get_qr_collection_url=current_app.get_qr_collection_url,
    )


@qr_bp.route('/admin/qr_labels/<collection_type>')
@login_required
def admin_qr_labels(collection_type):
    """Generate printable QR code labels for a collection."""
    return qr_label_views.render_admin_qr_labels(
        collection_type,
        normalize_qr_collection_type=current_app.normalize_qr_collection_type,
        ensure_qr_collection_access=current_app.ensure_qr_collection_access,
        get_mineral_database=current_app.get_mineral_database,
        get_qr_collection_records=current_app.get_qr_collection_records,
        get_qr_record_identifier=current_app.get_qr_record_identifier,
        get_qr_record_catalog_label=current_app.get_qr_record_catalog_label,
        get_qr_record_name=current_app.get_qr_record_name,
        build_collection_highlight_qr_url=current_app.build_collection_highlight_qr_url,
        get_qr_collection_name=current_app.get_qr_collection_name,
        get_qr_collection_url=current_app.get_qr_collection_url,
    )
