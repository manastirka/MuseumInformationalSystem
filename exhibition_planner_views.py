"""Shared route implementations for exhibition planner views."""

import json
import logging

from flask import jsonify, render_template, request, session
from psycopg.rows import dict_row

from postgres_service import get_postgres_connection
import audit_support

logger = logging.getLogger(__name__)

_DATE_FIELDS = ['start_date', 'end_date', 'opening_date', 'created_at', 'updated_at']
_UPDATE_FIELD_MAPPING = {
    'name': 'title',
    'title': 'title',
    'description': 'description',
    'type': 'exhibition_type',
    'exhibition_type': 'exhibition_type',
    'location': 'location',
    'venue': 'venue',
    'startDate': 'start_date',
    'start_date': 'start_date',
    'endDate': 'end_date',
    'end_date': 'end_date',
    'curator': 'curator',
    'status': 'status',
    'budget': 'budget',
    'progress': 'progress',
    'planning_phase': 'planning_phase',
    'notes': 'notes',
}


def render_museum_terminology():
    """Display museum terminology page."""
    return render_template('museum_terminology.html')


def render_exhibition_planner():
    """Display exhibition planning tool."""
    return render_template('exhibition_planner.html')


def _normalize_exhibition_row(row, user_email):
    exhibition = dict(row)
    for field in _DATE_FIELDS:
        if exhibition.get(field):
            exhibition[field] = str(exhibition[field])
    if exhibition.get('co_curators') is None:
        exhibition['co_curators'] = []
    if exhibition.get('sponsors') is None:
        exhibition['sponsors'] = []
    exhibition['is_owner'] = exhibition.get('created_by_email') == user_email
    return exhibition


def _get_exhibition_owner(cur, exhibition_id):
    cur.execute("SELECT id, created_by_email FROM exhibitions WHERE id = %s", (exhibition_id,))
    return cur.fetchone()


def api_get_exhibitions():
    """Get exhibitions for the planner based on user role."""
    try:
        user_email = session.get('user_email', '')
        user_role = session.get('user_role', 'employee')

        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                if user_role in ['admin', 'direktor']:
                    cur.execute(
                        """
                        SELECT
                            id, title, subtitle, description, exhibition_type,
                            location, venue, start_date, end_date, opening_date,
                            curator, co_curators, organizer, sponsors, status,
                            visitor_count, budget, notes, progress, planning_phase,
                            checklist_data, team_members, created_at, updated_at,
                            created_by_email, created_by_name
                        FROM exhibitions
                        ORDER BY created_at DESC
                        """
                    )
                else:
                    cur.execute(
                        """
                        SELECT
                            id, title, subtitle, description, exhibition_type,
                            location, venue, start_date, end_date, opening_date,
                            curator, co_curators, organizer, sponsors, status,
                            visitor_count, budget, notes, progress, planning_phase,
                            checklist_data, team_members, created_at, updated_at,
                            created_by_email, created_by_name
                        FROM exhibitions
                        WHERE created_by_email = %s
                           OR status IN ('active', 'completed', 'активна', 'завршена')
                        ORDER BY created_at DESC
                        """,
                        (user_email,),
                    )

                exhibitions = [_normalize_exhibition_row(row, user_email) for row in cur.fetchall()]

        return jsonify(
            {
                'success': True,
                'exhibitions': exhibitions,
                'user_role': user_role,
                'can_see_all': user_role in ['admin', 'direktor'],
            }
        )
    except Exception as exc:
        logger.error("Error fetching exhibitions: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_create_exhibition():
    """Create a new exhibition."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Нема података'}), 400

        title = (data.get('name') or '').strip() or (data.get('title') or '').strip()
        if not title:
            return jsonify({'success': False, 'message': 'Назив изложбе је обавезан'}), 400

        user_email = session.get('user_email', '')
        user_name = session.get('user_name', '')

        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO exhibitions (
                        title, description, exhibition_type, location,
                        start_date, end_date, curator, status, budget,
                        progress, planning_phase, checklist_data, team_members,
                        created_by_email, created_by_name
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    RETURNING id, title, status, progress, created_at
                    """,
                    (
                        title,
                        data.get('description', ''),
                        data.get('type', 'temporary'),
                        data.get('location', ''),
                        data.get('startDate') or data.get('start_date') or None,
                        data.get('endDate') or data.get('end_date') or None,
                        data.get('curator', ''),
                        data.get('status', 'planning'),
                        data.get('budget') or None,
                        data.get('progress', 0),
                        data.get('planning_phase', 'conceptual'),
                        json.dumps(data.get('checklist_data', {})),
                        json.dumps(data.get('team_members', [])),
                        user_email,
                        user_name,
                    ),
                )
                result = cur.fetchone()
                conn.commit()

        return jsonify(
            {
                'success': True,
                'message': 'Изложба је успешно креирана',
                'exhibition': {
                    'id': result['id'],
                    'title': result['title'],
                    'status': result['status'],
                    'progress': result['progress'],
                    'created_at': str(result['created_at']),
                },
            }
        )
    except Exception as exc:
        logger.error("Error creating exhibition: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_update_exhibition(exhibition_id):
    """Update an existing exhibition."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Нема података'}), 400

        user_email = session.get('user_email', '')
        user_role = session.get('user_role', 'employee')

        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                exhibition = _get_exhibition_owner(cur, exhibition_id)
                if not exhibition:
                    return jsonify({'success': False, 'message': 'Изложба није пронађена'}), 404

                is_owner = exhibition.get('created_by_email') == user_email
                is_admin_or_direktor = user_role in ['admin', 'direktor']
                if not is_owner and not is_admin_or_direktor:
                    return jsonify(
                        {
                            'success': False,
                            'message': 'Немате дозволу за измену ове изложбе',
                        }
                    ), 403

                update_fields = []
                params = []
                seen_db_fields = set()
                for key, db_field in _UPDATE_FIELD_MAPPING.items():
                    if key in data:
                        if db_field in seen_db_fields:
                            continue
                        seen_db_fields.add(db_field)
                        value = data[key]
                        if db_field in ['start_date', 'end_date'] and value == '':
                            value = None
                        update_fields.append(f"{db_field} = %s")
                        params.append(value)

                if 'checklist_data' in data:
                    update_fields.append("checklist_data = %s")
                    params.append(json.dumps(data['checklist_data']))

                if 'team_members' in data:
                    update_fields.append("team_members = %s")
                    params.append(json.dumps(data['team_members']))

                if not update_fields:
                    return jsonify({'success': False, 'message': 'Нема поља за ажурирање'}), 400

                update_fields.append("updated_at = NOW()")
                params.append(exhibition_id)

                query = f"""
                    UPDATE exhibitions
                    SET {', '.join(update_fields)}
                    WHERE id = %s
                    RETURNING id, title, status, progress
                """
                cur.execute(query, params)
                result = cur.fetchone()
                if not result:
                    return jsonify({'success': False, 'message': 'Изложба није пронађена'}), 404
                conn.commit()

        return jsonify(
            {
                'success': True,
                'message': 'Изложба је успешно ажурирана',
                'exhibition': dict(result),
            }
        )
    except Exception as exc:
        logger.error("Error updating exhibition: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_delete_exhibition(exhibition_id):
    """Delete an exhibition."""
    try:
        user_email = session.get('user_email', '')
        user_role = session.get('user_role', 'employee')

        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                exhibition = _get_exhibition_owner(cur, exhibition_id)
                if not exhibition:
                    return jsonify({'success': False, 'message': 'Изложба није пронађена'}), 404

                is_owner = exhibition.get('created_by_email') == user_email
                is_admin_or_direktor = user_role in ['admin', 'direktor']
                if not is_owner and not is_admin_or_direktor:
                    return jsonify(
                        {
                            'success': False,
                            'message': 'Немате дозволу за брисање ове изложбе',
                        }
                    ), 403

                cur.execute("DELETE FROM exhibitions WHERE id = %s RETURNING id", (exhibition_id,))
                # Audit у истој трансакцији — брисање без трага се не commit-ује.
                audit_support.record_audit(
                    action=audit_support.ACTION_DELETE,
                    entity_type='exhibition',
                    entity_id=exhibition_id,
                    summary=f'Обрисана изложба #{exhibition_id}'
                            + (f' — {exhibition.get("title")}' if exhibition.get('title') else ''),
                    old_values=dict(exhibition) if isinstance(exhibition, dict) else None,
                    changed_by=user_email or None,
                    cursor=cur,
                )
                conn.commit()
        return jsonify({'success': True, 'message': 'Изложба је успешно обрисана'})
    except Exception as exc:
        logger.error("Error deleting exhibition: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_update_exhibition_checklist(exhibition_id):
    """Update exhibition checklist data."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Нема података'}), 400

        user_email = session.get('user_email', '')
        user_role = session.get('user_role', 'employee')

        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                exhibition = _get_exhibition_owner(cur, exhibition_id)
                if not exhibition:
                    return jsonify({'success': False, 'message': 'Изложба није пронађена'}), 404

                is_owner = exhibition.get('created_by_email') == user_email
                is_admin_or_direktor = user_role in ['admin', 'direktor']
                if not is_owner and not is_admin_or_direktor:
                    return jsonify(
                        {
                            'success': False,
                            'message': 'Немате дозволу за измену ове изложбе',
                        }
                    ), 403

                cur.execute(
                    """
                    UPDATE exhibitions
                    SET checklist_data = %s, updated_at = NOW()
                    WHERE id = %s
                    RETURNING id
                    """,
                    (json.dumps(data), exhibition_id),
                )
                result = cur.fetchone()
                if not result:
                    return jsonify({'success': False, 'message': 'Изложба није пронађена'}), 404
                conn.commit()

        return jsonify({'success': True, 'message': 'Чеклиста је успешно ажурирана'})
    except Exception as exc:
        logger.error("Error updating checklist: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500
