"""Read-only admin viewer za globalni audit trag (ZADATAK #4).

Odgovara na pitanje „ko je ovo obrisao / promenio?" — lista `audit_log` sa
filterima (entitet, korisnik, akcija, opseg datuma) i paginacijom. Samo
čitanje; upis ide isključivo kroz audit_support.record_audit.
"""

import logging

from flask import render_template, request
from psycopg.rows import dict_row

from postgres_service import get_postgres_connection

logger = logging.getLogger(__name__)

PER_PAGE = 50
MAX_PER_PAGE = 200


def _int_arg(name, default):
    try:
        return int(request.args.get(name, default))
    except (TypeError, ValueError):
        return default


def render_audit_log():
    """Render the global audit-log page with filters + pagination."""
    entity = (request.args.get('entity') or '').strip()
    actor = (request.args.get('actor') or '').strip()
    action = (request.args.get('action') or '').strip()
    date_from = (request.args.get('date_from') or '').strip()
    date_to = (request.args.get('date_to') or '').strip()
    query = (request.args.get('q') or '').strip()

    page = max(1, _int_arg('page', 1))
    per_page = min(MAX_PER_PAGE, max(1, _int_arg('per_page', PER_PAGE)))
    offset = (page - 1) * per_page

    # WHERE se gradi od belih-listi kolona; vrednosti idu isključivo kroz %s.
    where = []
    params = []
    if entity:
        where.append('a.table_name = %s')
        params.append(entity)
    if actor:
        where.append('(a.changed_by ILIKE %s OR u.email ILIKE %s)')
        params.extend([f'%{actor}%', f'%{actor}%'])
    if action:
        where.append('a.action = %s')
        params.append(action)
    if date_from:
        where.append('a.performed_at >= %s')
        params.append(date_from)
    if date_to:
        # uključi ceo dan: < (date_to + 1 dan)
        where.append("a.performed_at < (%s::date + INTERVAL '1 day')")
        params.append(date_to)
    if query:
        where.append('a.change_summary ILIKE %s')
        params.append(f'%{query}%')

    where_sql = ('WHERE ' + ' AND '.join(where)) if where else ''

    entries = []
    total = 0
    entity_types = []
    actions = []
    try:
        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT count(*) AS n
                    FROM audit_log a
                    LEFT JOIN users u ON u.id = a.performed_by
                    {where_sql}
                    """,
                    params,
                )
                total = cur.fetchone()['n']

                cur.execute(
                    f"""
                    SELECT
                        a.id,
                        a.performed_at,
                        a.action,
                        a.table_name,
                        a.record_id,
                        a.record_ref,
                        a.change_summary,
                        a.ip_address,
                        COALESCE(a.changed_by, u.email, a.performed_by::text) AS actor
                    FROM audit_log a
                    LEFT JOIN users u ON u.id = a.performed_by
                    {where_sql}
                    ORDER BY a.performed_at DESC, a.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    params + [per_page, offset],
                )
                entries = cur.fetchall()

                # Vrednosti za filter padajuće liste.
                cur.execute('SELECT DISTINCT table_name FROM audit_log ORDER BY table_name')
                entity_types = [r['table_name'] for r in cur.fetchall()]
                cur.execute('SELECT DISTINCT action FROM audit_log ORDER BY action')
                actions = [r['action'] for r in cur.fetchall()]
    except Exception as exc:
        logger.error("Error loading audit log: %s", exc)

    total_pages = max(1, (total + per_page - 1) // per_page)

    return render_template(
        'admin_audit_log.html',
        entries=entries,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        entity_types=entity_types,
        actions=actions,
        filters={
            'entity': entity,
            'actor': actor,
            'action': action,
            'date_from': date_from,
            'date_to': date_to,
            'q': query,
        },
    )
