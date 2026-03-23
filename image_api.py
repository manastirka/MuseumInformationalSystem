#!/usr/bin/env python3
"""
Museum Image API
Flask endpoints for image management and server backup
"""

import os
import re
import logging
import uuid
from pathlib import Path
from flask import Blueprint, request, jsonify, send_file, current_app, session
from werkzeug.utils import secure_filename
from image_storage_engine import get_image_storage
from security_utils import login_required, admin_required

logger = logging.getLogger(__name__)

# Create Blueprint
image_api = Blueprint('image_api', __name__, url_prefix='/api/images')

# Allowed backup root — all restore paths must resolve inside this directory
_BACKUP_ROOT = Path('./storage/backups').resolve()

# Backup name must be a safe slug (alphanumeric, dash, underscore only)
_SAFE_BACKUP_NAME = re.compile(r'^[a-zA-Z0-9_-]{1,64}$')


def _can_upload_to_database(database: str) -> bool:
    """Return True when the current user can upload images to the target database."""
    user_role = session.get('user_role', '')
    if user_role == 'admin':
        return True

    module_key_getter = getattr(current_app, 'get_image_upload_module_key', None)
    access_checker = getattr(current_app, 'user_has_module_access', None)
    if module_key_getter is None or access_checker is None:
        current_app.logger.error("Image upload access helpers are not configured on the Flask app")
        return False

    module_key = module_key_getter(database)
    if not module_key:
        return False

    return access_checker(session.get('user_email', ''), user_role, module_key)


@image_api.route('/upload', methods=['POST'])
@login_required
def upload_image():
    """
    Upload an image.

    Expected form data:
        - file: Image file
        - database: Database name
        - entity_type: Entity type
        - entity_id: Entity ID
        - description: (optional) Image description
        - metadata: (optional) JSON string of additional metadata
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Get required parameters
        database = request.form.get('database')
        entity_type = request.form.get('entity_type')
        entity_id = request.form.get('entity_id')

        if not all([database, entity_type, entity_id]):
            return jsonify({'error': 'Missing required parameters'}), 400

        if not _can_upload_to_database(database):
            return jsonify({'error': 'You do not have permission to upload images for this collection'}), 403

        # Optional parameters
        description = request.form.get('description', '')
        metadata = request.form.get('metadata', {})

        # Save file to a unique temp path to prevent concurrent overwrites
        storage = get_image_storage()
        safe_name = secure_filename(file.filename)
        temp_name = f"{uuid.uuid4().hex}_{safe_name}"
        temp_path = storage.base_path / 'temp' / temp_name
        try:
            file.save(temp_path)

            # Store image
            image_id = storage.store_image(
                file_path=str(temp_path),
                database=database,
                entity_type=entity_type,
                entity_id=entity_id,
                description=description,
                metadata=metadata
            )
        finally:
            # Always clean up temp file
            if temp_path.exists():
                temp_path.unlink()

        if image_id:
            return jsonify({
                'success': True,
                'image_id': image_id,
                'message': 'Image uploaded successfully'
            }), 201
        else:
            return jsonify({'error': 'Failed to store image'}), 500

    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        return jsonify({'error': str(e)}), 500


@image_api.route('/<image_id>', methods=['GET'])
@admin_required
def get_image(image_id):
    """
    Get an image file.

    Query parameters:
        - size: 'original', 'small', 'medium', or 'large' (default: 'original')
    """
    try:
        size = request.args.get('size', 'original')
        storage = get_image_storage()

        image_path = storage.get_image_path(image_id, size)
        if not image_path:
            return jsonify({'error': 'Image not found'}), 404

        return send_file(image_path, mimetype='image/jpeg')

    except Exception as e:
        logger.error(f"Error retrieving image: {e}")
        return jsonify({'error': str(e)}), 500


@image_api.route('/<image_id>/metadata', methods=['GET'])
@admin_required
def get_image_metadata(image_id):
    """Get image metadata. Admin-only to prevent path/metadata leakage."""
    try:
        storage = get_image_storage()
        metadata = storage.get_image_metadata(image_id)

        if metadata:
            return jsonify({
                'success': True,
                'image_id': image_id,
                'metadata': metadata
            }), 200
        else:
            return jsonify({'error': 'Image not found'}), 404

    except Exception as e:
        logger.error(f"Error retrieving metadata: {e}")
        return jsonify({'error': str(e)}), 500


@image_api.route('/entity/<database>/<entity_type>/<entity_id>', methods=['GET'])
@admin_required
def get_entity_images(database, entity_type, entity_id):
    """Get all images for a specific entity."""
    try:
        storage = get_image_storage()
        images = storage.get_images_for_entity(database, entity_type, entity_id)

        return jsonify({
            'success': True,
            'count': len(images),
            'images': images
        }), 200

    except Exception as e:
        logger.error(f"Error retrieving entity images: {e}")
        return jsonify({'error': str(e)}), 500


@image_api.route('/<image_id>', methods=['DELETE'])
@admin_required
def delete_image(image_id):
    """Delete an image. Admin-only — destructive action."""
    try:
        storage = get_image_storage()
        success = storage.delete_image(image_id)

        if success:
            return jsonify({
                'success': True,
                'message': 'Image deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to delete image'}), 500

    except Exception as e:
        logger.error(f"Error deleting image: {e}")
        return jsonify({'error': str(e)}), 500


@image_api.route('/backup/create', methods=['POST'])
@admin_required
def create_backup():
    """Create a local backup of all images."""
    try:
        backup_name = request.json.get('backup_name') if request.json else None

        # Sanitize backup_name to prevent path traversal
        if backup_name and not _SAFE_BACKUP_NAME.match(backup_name):
            return jsonify({'error': 'Invalid backup name — use only letters, numbers, dash, underscore'}), 400

        storage = get_image_storage()
        backup_path = storage.create_local_backup(backup_name)

        if backup_path:
            return jsonify({
                'success': True,
                'backup_path': str(backup_path),
                'message': 'Backup created successfully'
            }), 201
        else:
            return jsonify({'error': 'Failed to create backup'}), 500

    except Exception as e:
        logger.error(f"Error creating backup: {e}")
        return jsonify({'error': str(e)}), 500


def _validate_backup_path(backup_path):
    """Validate that a backup path resolves inside the allowed backup root."""
    try:
        resolved = Path(backup_path).resolve()
        # Use is_relative_to for proper containment check (not string prefix)
        if not resolved.is_relative_to(_BACKUP_ROOT):
            return None
        return resolved
    except (ValueError, OSError):
        return None


@image_api.route('/backup/restore', methods=['POST'])
@admin_required
def restore_backup():
    """Restore images from a backup."""
    try:
        if not request.json or 'backup_path' not in request.json:
            return jsonify({'error': 'backup_path required'}), 400

        raw_path = request.json['backup_path']
        safe_path = _validate_backup_path(raw_path)
        if safe_path is None:
            return jsonify({'error': 'Invalid backup path'}), 400

        storage = get_image_storage()
        success = storage.restore_from_backup(str(safe_path))

        if success:
            return jsonify({
                'success': True,
                'message': 'Backup restored successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to restore backup'}), 500

    except Exception as e:
        logger.error(f"Error restoring backup: {e}")
        return jsonify({'error': str(e)}), 500


@image_api.route('/backup/server', methods=['POST'])
@admin_required
def backup_to_server():
    """Backup images to server."""
    try:
        image_id = request.json.get('image_id') if request.json else None
        storage = get_image_storage()

        success = storage.backup_to_server(image_id)

        if success:
            return jsonify({
                'success': True,
                'message': 'Backup to server completed'
            }), 200
        else:
            return jsonify({'error': 'Server backup failed'}), 500

    except Exception as e:
        logger.error(f"Error backing up to server: {e}")
        return jsonify({'error': str(e)}), 500


@image_api.route('/stats', methods=['GET'])
@admin_required
def get_storage_stats():
    """Get storage statistics. Admin-only because it exposes internal paths."""
    try:
        storage = get_image_storage()
        stats = storage.get_storage_stats()

        return jsonify({
            'success': True,
            'stats': stats
        }), 200

    except Exception as e:
        logger.error(f"Error retrieving stats: {e}")
        return jsonify({'error': str(e)}), 500


def _check_backup_token():
    """Verify X-Backup-Token header for service-to-service backup auth."""
    expected = os.environ.get('IMAGE_BACKUP_TOKEN')
    if not expected:
        return False
    return request.headers.get('X-Backup-Token') == expected


# Server-side backup receiver endpoint
@image_api.route('/backup/receive', methods=['POST'])
def receive_backup():
    """
    Receive image backup from another instance.
    Service-to-service endpoint authenticated via X-Backup-Token.
    """
    has_token = _check_backup_token()
    if not has_token:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        image_id = request.form.get('image_id')
        metadata = request.form.get('metadata')

        if not image_id:
            return jsonify({'error': 'image_id required'}), 400

        # Use a dedicated backup storage path (not the singleton main storage)
        backup_base = Path('./storage/backups/server')
        backup_base.mkdir(parents=True, exist_ok=True)
        backup_storage = get_image_storage(base_path=str(backup_base))

        # Save to unique temp path
        safe_name = secure_filename(file.filename)
        temp_name = f"{uuid.uuid4().hex}_{safe_name}"
        temp_dir = backup_base / 'temp'
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_path = temp_dir / temp_name

        try:
            file.save(temp_path)

            import json
            meta_dict = json.loads(metadata) if metadata else {}

            backup_id = backup_storage.store_image(
                file_path=str(temp_path),
                database=meta_dict.get('database_name', meta_dict.get('database', 'unknown')),
                entity_type=meta_dict.get('entity_type', 'backup'),
                entity_id=str(meta_dict.get('entity_id', image_id)),
                description=f"Backup of {image_id}",
                metadata=meta_dict
            )
        finally:
            if temp_path.exists():
                temp_path.unlink()

        if backup_id:
            return jsonify({
                'success': True,
                'backup_id': backup_id,
                'message': 'Backup received successfully'
            }), 201
        else:
            return jsonify({'error': 'Failed to store backup'}), 500

    except Exception as e:
        logger.error(f"Error receiving backup: {e}")
        return jsonify({'error': str(e)}), 500


def init_image_api(app, storage_path=None, server_backup_url=None):
    """
    Initialize image API with Flask app.

    Args:
        app: Flask application
        storage_path: Path for image storage
        server_backup_url: URL for server backups
    """
    # Initialize storage engine
    get_image_storage(storage_path, server_backup_url)

    # Register blueprint
    app.register_blueprint(image_api)

    logger.info("Image API initialized")
