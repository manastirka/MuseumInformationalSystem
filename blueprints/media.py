"""Collection media and public QR routes extracted from app.py."""

from flask import Blueprint, send_from_directory

import collection_media_views
from security_utils import login_required


media_bp = Blueprint('media', __name__)


@media_bp.route('/qr_box/minerals/<box_number>')
def qr_view_mineral_box(box_number):
    """Public mobile-optimized view for mineral box contents."""
    import app as museum_app

    return collection_media_views.render_qr_view_mineral_box(
        box_number,
        get_mineral_database=museum_app.get_mineral_database,
    )


@media_bp.route('/admin/batch_image_upload', methods=['GET', 'POST'])
@login_required
def batch_image_upload():
    """Batch image upload interface for museum collections."""
    import app as museum_app

    return collection_media_views.handle_batch_image_upload(
        get_accessible_image_upload_databases=museum_app.get_accessible_image_upload_databases,
        normalize_image_upload_database=museum_app.normalize_image_upload_database,
        ensure_image_upload_access=museum_app.ensure_image_upload_access,
        user_has_module_access=museum_app.user_has_module_access,
        get_image_upload_config=museum_app.get_image_upload_config,
        get_batch_uploader=museum_app.get_batch_uploader,
        get_image_upload_records=museum_app.get_image_upload_records,
        get_image_upload_collection_url=museum_app.get_image_upload_collection_url,
        get_image_upload_display_name=museum_app.get_image_upload_display_name,
    )


@media_bp.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory('static', filename)


@media_bp.route('/api/specimen_image/<database>/<entity_type>/<entity_id>')
def get_specimen_image(database, entity_type, entity_id):
    """Get specimen image or placeholder."""
    import app as museum_app

    return collection_media_views.get_specimen_image(
        database,
        entity_type,
        entity_id,
        get_image_storage=museum_app.get_image_storage,
    )


@media_bp.route('/api/specimen_image_full/<database>/<entity_type>/<entity_id>')
def get_specimen_image_full(database, entity_type, entity_id):
    """Get full-size specimen image."""
    import app as museum_app

    return collection_media_views.get_specimen_image_full(
        database,
        entity_type,
        entity_id,
        get_image_storage=museum_app.get_image_storage,
    )


@media_bp.route('/api/specimen_thumbnail/<database>/<entity_type>/<entity_id>')
def get_specimen_thumbnail(database, entity_type, entity_id):
    """Get specimen thumbnail or small placeholder."""
    import app as museum_app

    return collection_media_views.get_specimen_thumbnail(
        database,
        entity_type,
        entity_id,
        get_image_storage=museum_app.get_image_storage,
    )


@media_bp.route('/api/images/<image_id>')
@login_required
def get_image_by_id(image_id):
    """Serve an image directly by image_id."""
    import app as museum_app

    return collection_media_views.get_image_by_id(
        image_id,
        get_image_storage=museum_app.get_image_storage,
    )


@media_bp.route('/qr_view/<collection_type>/<catalog_number>')
def qr_view_specimen(collection_type, catalog_number):
    """Public mobile-optimized view for QR code scanned specimens."""
    import app as museum_app

    return collection_media_views.render_qr_view_specimen(
        collection_type,
        catalog_number,
        normalize_qr_collection_type=museum_app.normalize_qr_collection_type,
        get_meteorite_collection_database=museum_app.get_meteorite_collection_database,
        botany_collection_database=museum_app.BOTANY_COLLECTION_DATABASE,
        paleozoology_collection_database=museum_app.PALEOZOOLOGY_COLLECTION_DATABASE,
    )
