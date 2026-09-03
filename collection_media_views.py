"""Shared route implementations for specimen media views."""

import logging
import os
from datetime import datetime
from urllib.parse import unquote

from flask import current_app, flash, jsonify, redirect, render_template, request, send_file, session, url_for

logger = logging.getLogger(__name__)

PUBLIC_SPECIMEN_MEDIA_TARGETS = {
    ('meteorites', 'meteorite'),
    ('botany', 'botany'),
    ('paleozoology', 'paleozoology'),
}


def _is_public_specimen_media_target(database, entity_type):
    """Allow anonymous media access only for explicitly public QR collections."""
    normalized_database = str(database or '').strip().lower()
    normalized_entity_type = str(entity_type or '').strip().lower()
    return (normalized_database, normalized_entity_type) in PUBLIC_SPECIMEN_MEDIA_TARGETS


def _authorize_specimen_media_request(database, entity_type):
    """Require collection access unless the request targets a public QR collection."""
    if _is_public_specimen_media_target(database, entity_type):
        return None

    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Морате бити пријављени'}), 401

    access_checker = getattr(current_app, 'user_has_module_access', None)
    module_key_getter = getattr(current_app, 'get_image_upload_module_key', None)
    if access_checker is None or module_key_getter is None:
        current_app.logger.error('Specimen media access helpers are not configured on the Flask app')
        return jsonify({'success': False, 'message': 'Грешка у конфигурацији апликације'}), 500

    user_email = session.get('user_email', '')
    user_role = session.get('user_role', '')
    module_key = module_key_getter(database)
    if not module_key or not access_checker(user_email, user_role, module_key):
        return jsonify({'success': False, 'message': 'Немате дозволу за приступ овој слици'}), 403

    return None


def _send_placeholder(*placeholder_candidates):
    for placeholder_path in placeholder_candidates:
        if os.path.exists(placeholder_path):
            return send_file(
                placeholder_path,
                mimetype='image/png' if placeholder_path.endswith('.png') else 'image/jpeg',
            )
    return "No image available", 404


# Збирке чије предмете Фототека везује (foto_veza_predmet.database_name):
# назив из URL-а -> (database_name у вези, табела предмета, колона броја).
_FOTOTEKA_ZBIRKE = {
    'mineral': ('mineral', 'minerals', 'inventory_number'),
    'minerals': ('mineral', 'minerals', 'inventory_number'),
    'meteorite': ('meteorite', 'meteorite_specimens', 'catalog_number'),
    'meteorites': ('meteorite', 'meteorite_specimens', 'catalog_number'),
}


def _fototeka_entity_response(database, entity_type, entity_id, size):
    """Serve a Фототека derivative for this entity (minerals and meteorites —
    the linked set). Only 'javno' photos are served here: this route authorizes
    on collection access, not photo authorship, so it must never expose a photo
    the author flipped to 'privatno'. Returns a Flask response, or None when the
    item has no usable Фототека photo — the caller then serves a placeholder."""
    zbirka = _FOTOTEKA_ZBIRKE.get(str(database).lower())
    if not zbirka:
        return None
    database_name, tabela, kolona = zbirka
    try:
        import fototeka_jobs
        from postgres_service import get_postgres_connection

        predmet_id = int(str(entity_id).strip())
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT f.sha256
                    FROM fotografije f
                    JOIN foto_veza_predmet v ON v.fotografija_id = f.id
                    JOIN {tabela} m ON btrim(m.{kolona}) = btrim(v.inventarni_broj)
                    WHERE v.database_name = %s AND m.id = %s
                      AND f.obrisana = FALSE AND f.status = 'spremna'
                      AND f.vidljivost = 'javno'
                    ORDER BY f.id
                    LIMIT 1
                    """,
                    (database_name, predmet_id),
                )
                row = cur.fetchone()
        if not row:
            return None
        sha256 = (row['sha256'] if isinstance(row, dict) else row[0]).strip()
        kind = 'thumb' if size in ('small', 'thumb') else 'jpg'
        media_root = fototeka_jobs.get_media_path().resolve()
        full_path = (media_root / fototeka_jobs.derivative_relative_path(
            sha256, kind)).resolve()
        if not str(full_path).startswith(str(media_root) + os.sep):
            return None
        if not full_path.is_file():
            return None
        return send_file(full_path, mimetype='image/jpeg')
    except Exception as exc:  # noqa: BLE001 - a broken photo must not 500 the page
        logger.warning('Фототека слика није послужена (иде плацехолдер): %s', exc)
        return None


def _send_entity_image(database, entity_type, entity_id, size):
    """Фототека је једини извор слика предмета; без ње иде плацехолдер."""
    return _fototeka_entity_response(database, entity_type, entity_id, size)


def get_specimen_image(database, entity_type, entity_id):
    """Get specimen image or placeholder."""
    auth_response = _authorize_specimen_media_request(database, entity_type)
    if auth_response is not None:
        return auth_response

    response = _send_entity_image(database, entity_type, entity_id, 'medium')
    if response is not None:
        return response
    return _send_placeholder(os.path.join('static', 'images', 'specimen-placeholder.png'))


def get_specimen_image_full(database, entity_type, entity_id):
    """Get full-size specimen image."""
    auth_response = _authorize_specimen_media_request(database, entity_type)
    if auth_response is not None:
        return auth_response

    response = _send_entity_image(database, entity_type, entity_id, 'original')
    if response is not None:
        return response
    return get_specimen_image(database, entity_type, entity_id)


def get_specimen_thumbnail(database, entity_type, entity_id):
    """Get specimen thumbnail or small placeholder."""
    auth_response = _authorize_specimen_media_request(database, entity_type)
    if auth_response is not None:
        return auth_response

    response = _send_entity_image(database, entity_type, entity_id, 'small')
    if response is not None:
        return response
    return _send_placeholder(
        os.path.join('static', 'images', 'specimen-placeholder-thumb.png'),
        os.path.join('static', 'images', 'specimen-placeholder.png'),
    )


def get_image_by_id(image_id, *, get_image_storage):
    """Serve an image directly by image id."""
    size = request.args.get('size', 'original').strip().lower()
    if size not in {'original', 'small', 'medium', 'large'}:
        size = 'original'

    try:
        image_storage = get_image_storage()
        metadata = image_storage.get_image_metadata(image_id)
        if not metadata:
            return "No image available", 404

        auth_response = _authorize_specimen_media_request(
            metadata.get('database_name'), metadata.get('entity_type')
        )
        if auth_response is not None:
            return auth_response

        image_path = image_storage.get_image_path(image_id, size)
        if image_path and image_path.exists():
            suffix = image_path.suffix.lower()
            mimetype = 'image/png' if suffix == '.png' else 'image/jpeg'
            return send_file(image_path, mimetype=mimetype)
    except Exception as exc:
        logger.error("Error loading image %s: %s", image_id, exc)

    return "No image available", 404
