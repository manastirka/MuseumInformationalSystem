"""Shared route implementations for user notification endpoints."""

import logging

from flask import jsonify, request, session
from psycopg.rows import dict_row

from postgres_service import get_postgres_connection

logger = logging.getLogger(__name__)


def api_get_notifications():
    """Return notifications for the logged-in user."""
    try:
        user_email = session.get('user_email')
        if not user_email:
            return jsonify({'success': True, 'notifications': [], 'unread_count': 0})

        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, title, message, icon, type, is_read,
                           to_char(created_at, 'DD.MM.YYYY HH24:MI') as time
                    FROM user_notifications
                    WHERE user_email = %s
                    ORDER BY created_at DESC
                    LIMIT 50
                    """,
                    (user_email,),
                )
                notifications = cur.fetchall()

                cur.execute(
                    """
                    SELECT COUNT(*) AS unread_count
                    FROM user_notifications
                    WHERE user_email = %s AND is_read = FALSE
                    """,
                    (user_email,),
                )
                unread_count = cur.fetchone()['unread_count']

        return jsonify(
            {
                'success': True,
                'notifications': [dict(notification) for notification in notifications],
                'unread_count': unread_count,
            }
        )
    except Exception as exc:
        logger.error("Error fetching notifications: %s", exc)
        return jsonify({'success': True, 'notifications': [], 'unread_count': 0})


def api_mark_notifications_read():
    """Mark one or all notifications as read for the current user."""
    try:
        user_email = session.get('user_email')
        if not user_email:
            return jsonify({'success': False})

        notification_id = (request.get_json(silent=True) or {}).get('id')

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                if notification_id:
                    cur.execute(
                        """
                        UPDATE user_notifications SET is_read = TRUE
                        WHERE id = %s AND user_email = %s
                        """,
                        (notification_id, user_email),
                    )
                else:
                    cur.execute(
                        """
                        UPDATE user_notifications SET is_read = TRUE
                        WHERE user_email = %s AND is_read = FALSE
                        """,
                        (user_email,),
                    )
                conn.commit()

        return jsonify({'success': True})
    except Exception as exc:
        logger.error("Error marking notifications read: %s", exc)
        return jsonify({'success': False})


def api_clear_notifications():
    """Delete all notifications for the current user."""
    try:
        user_email = session.get('user_email')
        if not user_email:
            return jsonify({'success': False})

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM user_notifications WHERE user_email = %s",
                    (user_email,),
                )
                conn.commit()

        return jsonify({'success': True})
    except Exception as exc:
        logger.error("Error clearing notifications: %s", exc)
        return jsonify({'success': False})
