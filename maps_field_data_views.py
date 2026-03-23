"""Shared route implementations for geological field-data views."""

import logging

from flask import jsonify, request, session
from psycopg.rows import dict_row

from postgres_service import get_postgres_connection

logger = logging.getLogger(__name__)

_VALID_CATEGORIES = ('rock', 'mineral', 'fossil', 'outcrop', 'formation', 'other')
_geo_field_table_ready = False


def _ensure_geo_field_table():
    """Create the geo field observations table if needed."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS geo_field_data (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    latitude DOUBLE PRECISION NOT NULL,
                    longitude DOUBLE PRECISION NOT NULL,
                    category VARCHAR(50) DEFAULT 'other',
                    rock_mineral_type VARCHAR(255),
                    geological_period VARCHAR(255),
                    formation_name VARCHAR(255),
                    field_notes TEXT,
                    created_by VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                );
                CREATE INDEX IF NOT EXISTS idx_geo_field_data_coords ON geo_field_data(latitude, longitude);
                CREATE INDEX IF NOT EXISTS idx_geo_field_data_user ON geo_field_data(created_by);
                """
            )
            conn.commit()


def _get_geo_field_conn():
    """Return a PostgreSQL connection after ensuring the table exists."""
    global _geo_field_table_ready
    if not _geo_field_table_ready:
        _ensure_geo_field_table()
        _geo_field_table_ready = True
    return get_postgres_connection(row_factory=dict_row)


def _normalize_category(category):
    """Return a safe category value."""
    if category in _VALID_CATEGORIES:
        return category
    return 'other'


def api_create_field_data():
    """Create a new geological field observation."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Нема података'}), 400

        title = (data.get('title') or '').strip()
        if not title:
            return jsonify({'success': False, 'message': 'Наслов је обавезан'}), 400

        lat = data.get('latitude')
        lng = data.get('longitude')
        if lat is None or lng is None:
            return jsonify({'success': False, 'message': 'Координате су обавезне'}), 400

        try:
            lat = float(lat)
            lng = float(lng)
        except (TypeError, ValueError):
            return jsonify({'success': False, 'message': 'Неважеће координате'}), 400

        with _get_geo_field_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO geo_field_data
                        (title, description, latitude, longitude, category,
                         rock_mineral_type, geological_period, formation_name,
                         field_notes, created_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        title,
                        data.get('description', ''),
                        lat,
                        lng,
                        _normalize_category(data.get('category', 'other')),
                        data.get('rock_mineral_type', ''),
                        data.get('geological_period', ''),
                        data.get('formation_name', ''),
                        data.get('field_notes', ''),
                        session['user_email'],
                    ),
                )
                row = cur.fetchone()
                new_id = row['id']
                conn.commit()

        return jsonify({'success': True, 'id': new_id})
    except Exception as exc:
        logger.error("Error creating field data: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при чувању'}), 500


def api_list_field_data():
    """List geological field observations, optionally filtered by bounding box."""
    try:
        north = request.args.get('north', type=float)
        south = request.args.get('south', type=float)
        east = request.args.get('east', type=float)
        west = request.args.get('west', type=float)

        with _get_geo_field_conn() as conn:
            with conn.cursor() as cur:
                if all(v is not None for v in (north, south, east, west)):
                    cur.execute(
                        """
                        SELECT id, title, description, latitude, longitude,
                               category, rock_mineral_type, geological_period,
                               formation_name, field_notes, created_by,
                               created_at, updated_at
                        FROM geo_field_data
                        WHERE latitude BETWEEN %s AND %s
                          AND longitude BETWEEN %s AND %s
                        ORDER BY created_at DESC
                        """,
                        (south, north, west, east),
                    )
                else:
                    cur.execute(
                        """
                        SELECT id, title, description, latitude, longitude,
                               category, rock_mineral_type, geological_period,
                               formation_name, field_notes, created_by,
                               created_at, updated_at
                        FROM geo_field_data
                        ORDER BY created_at DESC
                        """
                    )
                rows = cur.fetchall()

        data = []
        for row in rows:
            item = dict(row)
            item['created_at'] = item['created_at'].isoformat() if item['created_at'] else None
            item['updated_at'] = item['updated_at'].isoformat() if item['updated_at'] else None
            data.append(item)

        return jsonify({'success': True, 'data': data})
    except Exception as exc:
        logger.error("Error listing field data: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању'}), 500


def api_get_field_data(item_id, *, image_storage_factory):
    """Get a single field observation with images."""
    try:
        with _get_geo_field_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, title, description, latitude, longitude,
                           category, rock_mineral_type, geological_period,
                           formation_name, field_notes, created_by,
                           created_at, updated_at
                    FROM geo_field_data WHERE id = %s
                    """,
                    (item_id,),
                )
                row = cur.fetchone()

        if not row:
            return jsonify({'success': False, 'message': 'Није пронађено'}), 404

        item = dict(row)
        item['created_at'] = item['created_at'].isoformat() if item['created_at'] else None
        item['updated_at'] = item['updated_at'].isoformat() if item['updated_at'] else None

        images = []
        try:
            storage = image_storage_factory()
            img_list = storage.get_images_for_entity('geo_field', 'observation', str(item_id))
            for img in img_list:
                image_id = img.get('image_id', '')
                images.append(
                    {
                        'image_id': image_id,
                        'description': img.get('description', ''),
                        'url': f"/api/images/{image_id}",
                        'thumbnail': f"/api/images/{image_id}?size=medium",
                    }
                )
        except Exception as exc:
            logger.warning("Error fetching images for field data %s: %s", item_id, exc)

        item['images'] = images
        return jsonify({'success': True, 'data': item})
    except Exception as exc:
        logger.error("Error getting field data %s: %s", item_id, exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању'}), 500


def api_update_field_data(item_id):
    """Update a field observation for its owner or an admin."""
    try:
        with _get_geo_field_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT created_by FROM geo_field_data WHERE id = %s", (item_id,))
                row = cur.fetchone()

        if not row:
            return jsonify({'success': False, 'message': 'Није пронађено'}), 404

        user_email = session.get('user_email', '')
        user_role = session.get('user_role', '')
        if row['created_by'] != user_email and user_role != 'admin':
            return jsonify({'success': False, 'message': 'Немате дозволу'}), 403

        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Нема података'}), 400

        title = (data.get('title') or '').strip()
        if not title:
            return jsonify({'success': False, 'message': 'Наслов је обавезан'}), 400

        try:
            lat = float(data.get('latitude'))
            lng = float(data.get('longitude'))
        except (TypeError, ValueError):
            return jsonify({'success': False, 'message': 'Неважеће координате'}), 400

        with _get_geo_field_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE geo_field_data SET
                        title = %s, description = %s,
                        latitude = %s, longitude = %s,
                        category = %s, rock_mineral_type = %s,
                        geological_period = %s, formation_name = %s,
                        field_notes = %s, updated_at = NOW()
                    WHERE id = %s
                    """,
                    (
                        title,
                        data.get('description', ''),
                        lat,
                        lng,
                        _normalize_category(data.get('category', 'other')),
                        data.get('rock_mineral_type', ''),
                        data.get('geological_period', ''),
                        data.get('formation_name', ''),
                        data.get('field_notes', ''),
                        item_id,
                    ),
                )
                conn.commit()

        return jsonify({'success': True})
    except Exception as exc:
        logger.error("Error updating field data %s: %s", item_id, exc)
        return jsonify({'success': False, 'message': 'Грешка при ажурирању'}), 500


def api_delete_field_data(item_id, *, image_storage_factory):
    """Delete a field observation for its owner or an admin."""
    try:
        with _get_geo_field_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT created_by FROM geo_field_data WHERE id = %s", (item_id,))
                row = cur.fetchone()

        if not row:
            return jsonify({'success': False, 'message': 'Није пронађено'}), 404

        user_email = session.get('user_email', '')
        user_role = session.get('user_role', '')
        if row['created_by'] != user_email and user_role != 'admin':
            return jsonify({'success': False, 'message': 'Немате дозволу'}), 403

        try:
            storage = image_storage_factory()
            images = storage.get_images_for_entity('geo_field', 'observation', str(item_id))
            for img in images:
                storage.delete_image(img.get('image_id', ''))
        except Exception as exc:
            logger.warning("Error deleting images for field data %s: %s", item_id, exc)

        with _get_geo_field_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM geo_field_data WHERE id = %s", (item_id,))
                conn.commit()

        return jsonify({'success': True})
    except Exception as exc:
        logger.error("Error deleting field data %s: %s", item_id, exc)
        return jsonify({'success': False, 'message': 'Грешка при брисању'}), 500
