"""Collection media routes extracted from app.py (QR routes live in blueprints/qr.py)."""

from flask import Blueprint, send_from_directory

import collection_media_views
from rate_limit_ext import limiter
from security_utils import login_required


media_bp = Blueprint('media', __name__)


@media_bp.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory('static', filename)


@media_bp.route('/api/specimen_image/<database>/<entity_type>/<entity_id>')
@limiter.limit("600 per minute")
def get_specimen_image(database, entity_type, entity_id):
    """Get specimen image or placeholder."""
    return collection_media_views.get_specimen_image(
        database,
        entity_type,
        entity_id,
    )


@media_bp.route('/api/specimen_image_full/<database>/<entity_type>/<entity_id>')
@limiter.limit("600 per minute")
def get_specimen_image_full(database, entity_type, entity_id):
    """Get full-size specimen image."""
    return collection_media_views.get_specimen_image_full(
        database,
        entity_type,
        entity_id,
    )


@media_bp.route('/api/specimen_thumbnail/<database>/<entity_type>/<entity_id>')
@limiter.limit("600 per minute")
def get_specimen_thumbnail(database, entity_type, entity_id):
    """Get specimen thumbnail or small placeholder."""
    return collection_media_views.get_specimen_thumbnail(
        database,
        entity_type,
        entity_id,
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
