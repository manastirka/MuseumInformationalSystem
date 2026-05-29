"""Archive and digital signature routes extracted from the main app."""

import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path

import psycopg
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from observability import add_sentry_breadcrumb, capture_observability_exception
from postgres_service import get_postgres_connection
from security_utils import admin_required, login_required

logger = logging.getLogger(__name__)

APP_ROOT = Path(__file__).resolve().parent
SIGNATURE_DOCUMENT_ROOTS = (
    APP_ROOT / 'exports',
    APP_ROOT / 'storage' / 'uploads',
)

archive_signature_bp = Blueprint('archive_signature', __name__)

# Distinct namespaces for per-year pg_advisory_xact_lock keys so the archive
# reference and delovodni number generators never contend on the same lock.
_ARCHIVE_REF_LOCK_NS = 0x4152
_REGISTRATION_LOCK_NS = 0x5245


def _server_error_response():
    """Return a sanitized 500 payload while details stay in server logs."""
    return jsonify({'success': False, 'message': 'Дошло је до грешке на серверу.'}), 500

# Approval chain configurations
APPROVAL_CHAINS = {
    'zahtev': [
        {'role': 'sef_odeljenja', 'label': 'Шеф одељења', 'order': 1},
        {'role': 'direktor', 'label': 'Директор', 'order': 2},
    ],
    'finansije': [
        {'role': 'sef_racunovodstva', 'label': 'Шеф рачуноводства', 'order': 1},
        {'role': 'sef_odeljenja', 'label': 'Шеф одељења', 'order': 2},
        {'role': 'direktor', 'label': 'Директор', 'order': 3},
    ],
    'terenska_aktivnost': [
        {'role': 'sef_odeljenja', 'label': 'Шеф одељења', 'order': 1},
        {'role': 'direktor', 'label': 'Директор', 'order': 2},
        {'role': 'sef_racunovodstva', 'label': 'Шеф рачуноводства', 'order': 3},
    ],
}

REQUEST_SUBTYPES = {
    'zahtev': [
        {'value': 'godisnji_odmor', 'label': 'Годишњи одмор'},
        {'value': 'slobodan_dan', 'label': 'Слободан дан'},
        {'value': 'bolovanje', 'label': 'Боловање'},
        {'value': 'sluzbeni_put', 'label': 'Службени пут'},
        {'value': 'nabavka_materijala', 'label': 'Набавка материјала'},
        {'value': 'oprema', 'label': 'Опрема'},
        {'value': 'edukacija', 'label': 'Едукација'},
        {'value': 'ostalo', 'label': 'Остало'},
    ],
    'finansije': [
        {'value': 'fakture', 'label': 'Фактуре'},
        {'value': 'isplate', 'label': 'Исплате'},
        {'value': 'budzet', 'label': 'Буџет'},
        {'value': 'finansijski_plan', 'label': 'Финансијски план'},
        {'value': 'refundacija', 'label': 'Рефундација'},
        {'value': 'ostalo', 'label': 'Остало'},
    ],
    'terenska_aktivnost': [
        {'value': 'putni_nalog', 'label': 'Путни налог'},
        {'value': 'dnevnice', 'label': 'Дневнице'},
        {'value': 'gorivo', 'label': 'Гориво'},
        {'value': 'terenski_izvestaj', 'label': 'Теренски извештај'},
        {'value': 'troskovi', 'label': 'Трошкови'},
        {'value': 'ostalo', 'label': 'Остало'},
    ],
}


def can_approve_request(user_role, request_type, current_step):
    """Check if user can approve at current step."""
    chain = APPROVAL_CHAINS.get(request_type, [])
    if current_step < len(chain):
        required_role = chain[current_step]['role']
        if required_role == 'direktor' and user_role in ['admin', 'direktor']:
            return True
        if user_role == required_role:
            return True
        if user_role == 'admin':
            return True
    return False


def can_view_archive_request(created_by_email, user_email, user_role, request_type, current_step):
    """Allow archive request access to owners, admins/direktor, and current approvers."""
    if user_role in ['admin', 'direktor']:
        return True
    if created_by_email == user_email:
        return True
    return can_approve_request(user_role, request_type, current_step)


def resolve_signature_document_path(raw_path):
    """Resolve a signature document path to an allowed app-local file and safe relative path."""
    if not raw_path:
        return None, None, None

    try:
        candidate = Path(str(raw_path).strip())
        if not str(candidate):
            return None, None, None

        if candidate.is_absolute():
            resolved = candidate.resolve(strict=True)
        else:
            resolved = (APP_ROOT / candidate).resolve(strict=True)

        if not resolved.is_file():
            return None, None, 'Документ није пронађен'

        for allowed_root in SIGNATURE_DOCUMENT_ROOTS:
            try:
                relative_to_root = resolved.relative_to(allowed_root)
                safe_relative = (allowed_root.relative_to(APP_ROOT) / relative_to_root).as_posix()
                return resolved, safe_relative, None
            except ValueError:
                continue

        return None, None, 'Путања документа није дозвољена'
    except (OSError, RuntimeError, ValueError):
        return None, None, 'Путања документа није валидна'


@archive_signature_bp.route('/admin/archive')
@login_required
def admin_archive_dashboard():
    """Main archive and verification dashboard."""
    return render_template(
        'admin_archive_dashboard.html',
        subtypes=REQUEST_SUBTYPES,
        approval_chains=APPROVAL_CHAINS,
    )


@archive_signature_bp.route('/admin/archive/zahtevi')
@login_required
def admin_archive_zahtevi():
    """Zahtevi (requests) management page."""
    return render_template(
        'admin_archive_zahtevi.html',
        subtypes=REQUEST_SUBTYPES.get('zahtev', []),
        approval_chain=APPROVAL_CHAINS.get('zahtev', []),
    )


@archive_signature_bp.route('/admin/archive/finansije')
@login_required
def admin_archive_finansije():
    """Finansije (finances) management page."""
    return render_template(
        'admin_archive_finansije.html',
        subtypes=REQUEST_SUBTYPES.get('finansije', []),
        approval_chain=APPROVAL_CHAINS.get('finansije', []),
    )


@archive_signature_bp.route('/admin/archive/approvals')
@login_required
@admin_required
def admin_archive_approvals():
    """Central approvals page for admins."""
    return render_template('admin_archive_approvals.html')


@archive_signature_bp.route('/admin/archive/terenska')
@login_required
def admin_archive_terenska():
    """Terenska aktivnost (field activity) management page."""
    return render_template(
        'admin_archive_terenska.html',
        subtypes=REQUEST_SUBTYPES.get('terenska_aktivnost', []),
        approval_chain=APPROVAL_CHAINS.get('terenska_aktivnost', []),
    )


@archive_signature_bp.route('/api/archive/requests', methods=['GET'])
@login_required
def api_get_archive_requests():
    """Get archive requests with filtering."""
    try:
        user_email = session.get('user_email', '')
        user_role = session.get('user_role', 'employee')

        request_type = request.args.get('type', '')
        status = request.args.get('status', '')
        subtype = request.args.get('subtype', '')
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 20))
        except (TypeError, ValueError):
            return jsonify({'success': False, 'message': 'Неисправни параметри странице'}), 400
        page = max(1, page)
        per_page = max(1, min(per_page, 100))

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                conditions = []
                params = []

                if request_type:
                    conditions.append("request_type = %s")
                    params.append(request_type)

                if status:
                    conditions.append("status = %s")
                    params.append(status)

                if subtype:
                    conditions.append("subtype = %s")
                    params.append(subtype)

                if user_role not in ['admin', 'direktor']:
                    conditions.append("""(
                        created_by_email = %s
                        OR (
                            status = 'pending'
                            AND EXISTS (
                                SELECT 1 FROM approval_signatures
                                WHERE request_id = archive_requests.id
                                AND approver_role = %s
                                AND decision = 'pending'
                                AND signature_order = archive_requests.current_approval_step
                            )
                        )
                    )""")
                    params.extend([user_email, user_role])

                where_clause = " AND ".join(conditions) if conditions else "1=1"

                cur.execute(
                    "SELECT COUNT(*) FROM archive_requests WHERE " + where_clause,
                    params,
                )
                total = cur.fetchone()[0]

                offset = (page - 1) * per_page
                cur.execute(
                    "SELECT "
                    "id, request_type, subtype, title, description, "
                    "request_data, status, priority, "
                    "created_by_email, created_by_name, created_by_department, "
                    "created_at, updated_at, attachments, approval_chain, "
                    "current_approval_step, final_decision, final_decision_by_name, "
                    "final_decision_at, archived_at, archive_reference "
                    "FROM archive_requests "
                    "WHERE " + where_clause + " "
                    "ORDER BY created_at DESC "
                    "LIMIT %s OFFSET %s",
                    params + [per_page, offset],
                )

                requests_list = []
                for row in cur.fetchall():
                    req = {
                        'id': row[0],
                        'request_type': row[1],
                        'subtype': row[2],
                        'title': row[3],
                        'description': row[4],
                        'request_data': row[5] or {},
                        'status': row[6],
                        'priority': row[7],
                        'created_by_email': row[8],
                        'created_by_name': row[9],
                        'created_by_department': row[10],
                        'created_at': row[11].isoformat() if row[11] else None,
                        'updated_at': row[12].isoformat() if row[12] else None,
                        'attachments': row[13] or [],
                        'approval_chain': row[14] or [],
                        'current_approval_step': row[15],
                        'final_decision': row[16],
                        'final_decision_by_name': row[17],
                        'final_decision_at': row[18].isoformat() if row[18] else None,
                        'archived_at': row[19].isoformat() if row[19] else None,
                        'archive_reference': row[20],
                        'is_owner': row[8] == user_email,
                        'can_approve': can_approve_request(user_role, row[1], row[15]),
                    }

                    cur.execute(
                        """
                        SELECT approver_role, approver_name, decision, comments, signed_at, signature_order
                        FROM approval_signatures
                        WHERE request_id = %s
                        ORDER BY signature_order
                        """,
                        (row[0],),
                    )
                    req['signatures'] = [
                        {
                            'role': signature[0],
                            'name': signature[1],
                            'decision': signature[2],
                            'comments': signature[3],
                            'signed_at': signature[4].isoformat() if signature[4] else None,
                            'order': signature[5],
                        }
                        for signature in cur.fetchall()
                    ]

                    requests_list.append(req)

                return jsonify(
                    {
                        'success': True,
                        'requests': requests_list,
                        'total': total,
                        'page': page,
                        'per_page': per_page,
                        'total_pages': (total + per_page - 1) // per_page,
                    }
                )
    except Exception:
        logger.exception("Error getting archive requests")
        return _server_error_response()


@archive_signature_bp.route('/api/archive/requests', methods=['POST'])
@login_required
def api_create_archive_request():
    """Create new archive request."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Нема података'}), 400

        request_type = data.get('request_type', '')
        if request_type not in APPROVAL_CHAINS:
            return jsonify({'success': False, 'message': 'Непознат тип захтева'}), 400

        user_email = session.get('user_email', '')
        user_name = session.get('user_name', '')
        approval_chain = APPROVAL_CHAINS.get(request_type, [])
        add_sentry_breadcrumb(
            category='archive',
            message='Archive request creation started',
            data={'request_type': request_type, 'subtype': data.get('subtype', '')},
        )

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO archive_requests (
                        request_type, subtype, title, description, request_data,
                        status, priority, created_by_email, created_by_name,
                        created_by_department, attachments, approval_chain, current_approval_step
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        request_type,
                        data.get('subtype', ''),
                        data.get('title', ''),
                        data.get('description', ''),
                        json.dumps(data.get('request_data', {})),
                        'pending',
                        data.get('priority', 'normal'),
                        user_email,
                        user_name,
                        data.get('department', ''),
                        json.dumps(data.get('attachments', [])),
                        json.dumps(approval_chain),
                        0,
                    ),
                )
                request_id = cur.fetchone()[0]

                for order, approver in enumerate(approval_chain):
                    cur.execute(
                        """
                        INSERT INTO approval_signatures (
                            request_id, approver_role, decision, signature_order
                        ) VALUES (%s, %s, 'pending', %s)
                        """,
                        (request_id, approver['role'], order),
                    )

                cur.execute(
                    """
                    INSERT INTO request_history (
                        request_id, action, action_by_email, action_by_name, new_values
                    ) VALUES (%s, 'created', %s, %s, %s)
                    """,
                    (request_id, user_email, user_name, json.dumps(data)),
                )
                conn.commit()

        return jsonify(
            {
                'success': True,
                'message': 'Захтев је успешно креиран',
                'id': request_id,
            }
        )
    except Exception as exc:
        logger.exception("Error creating archive request")
        capture_observability_exception(
            exc,
            tags={'component': 'archive', 'operation': 'create_request'},
            extra={
                'user_email': session.get('user_email'),
                'request_type': (request.get_json(silent=True) or {}).get('request_type'),
            },
            user={'email': session.get('user_email')},
        )
        return _server_error_response()


@archive_signature_bp.route('/api/archive/requests/<int:request_id>', methods=['GET'])
@login_required
def api_get_archive_request(request_id):
    """Get single archive request with full details."""
    try:
        user_email = session.get('user_email', '')
        user_role = session.get('user_role', 'employee')

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id, request_type, subtype, title, description,
                        request_data, status, priority,
                        created_by_email, created_by_name, created_by_department,
                        created_at, updated_at, attachments, approval_chain,
                        current_approval_step, final_decision, final_decision_by_email,
                        final_decision_by_name, final_decision_at, final_notes,
                        archived_at, archive_reference
                    FROM archive_requests
                    WHERE id = %s
                    """,
                    (request_id,),
                )
                row = cur.fetchone()
                if not row:
                    return jsonify({'success': False, 'message': 'Захтев није пронађен'}), 404

                if not can_view_archive_request(row[8], user_email, user_role, row[1], row[15]):
                    return jsonify({'success': False, 'message': 'Немате приступ овом захтеву'}), 403

                req = {
                    'id': row[0],
                    'request_type': row[1],
                    'subtype': row[2],
                    'title': row[3],
                    'description': row[4],
                    'request_data': row[5] or {},
                    'status': row[6],
                    'priority': row[7],
                    'created_by_email': row[8],
                    'created_by_name': row[9],
                    'created_by_department': row[10],
                    'created_at': row[11].isoformat() if row[11] else None,
                    'updated_at': row[12].isoformat() if row[12] else None,
                    'attachments': row[13] or [],
                    'approval_chain': row[14] or [],
                    'current_approval_step': row[15],
                    'final_decision': row[16],
                    'final_decision_by_email': row[17],
                    'final_decision_by_name': row[18],
                    'final_decision_at': row[19].isoformat() if row[19] else None,
                    'final_notes': row[20],
                    'archived_at': row[21].isoformat() if row[21] else None,
                    'archive_reference': row[22],
                    'is_owner': row[8] == user_email,
                    'can_approve': can_approve_request(user_role, row[1], row[15]),
                }

                cur.execute(
                    """
                    SELECT approver_role, approver_email, approver_name, decision, comments, signed_at, signature_order
                    FROM approval_signatures
                    WHERE request_id = %s
                    ORDER BY signature_order
                    """,
                    (request_id,),
                )
                req['signatures'] = [
                    {
                        'role': signature[0],
                        'email': signature[1],
                        'name': signature[2],
                        'decision': signature[3],
                        'comments': signature[4],
                        'signed_at': signature[5].isoformat() if signature[5] else None,
                        'order': signature[6],
                    }
                    for signature in cur.fetchall()
                ]

                cur.execute(
                    """
                    SELECT id, author_email, author_name, comment, created_at
                    FROM request_comments
                    WHERE request_id = %s
                    ORDER BY created_at
                    """,
                    (request_id,),
                )
                req['comments'] = [
                    {
                        'id': comment[0],
                        'author_email': comment[1],
                        'author_name': comment[2],
                        'comment': comment[3],
                        'created_at': comment[4].isoformat() if comment[4] else None,
                    }
                    for comment in cur.fetchall()
                ]

                cur.execute(
                    """
                    SELECT action, action_by_email, action_by_name, notes, created_at
                    FROM request_history
                    WHERE request_id = %s
                    ORDER BY created_at DESC
                    """,
                    (request_id,),
                )
                req['history'] = [
                    {
                        'action': item[0],
                        'by_email': item[1],
                        'by_name': item[2],
                        'notes': item[3],
                        'created_at': item[4].isoformat() if item[4] else None,
                    }
                    for item in cur.fetchall()
                ]

        return jsonify({'success': True, 'request': req})
    except Exception:
        logger.exception("Error getting archive request")
        return _server_error_response()


@archive_signature_bp.route('/api/archive/requests/<int:request_id>/approve', methods=['POST'])
@login_required
def api_approve_archive_request(request_id):
    """Approve request at current step."""
    try:
        data = request.get_json() or {}
        comments = data.get('comments', '')

        user_email = session.get('user_email', '')
        user_name = session.get('user_name', '')
        user_role = session.get('user_role', 'employee')
        add_sentry_breadcrumb(
            category='archive',
            message='Archive request approval started',
            data={'request_id': request_id, 'user_role': user_role},
        )

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT request_type, status, current_approval_step, approval_chain,
                           created_by_email, title
                    FROM archive_requests WHERE id = %s
                    FOR UPDATE
                    """,
                    (request_id,),
                )
                row = cur.fetchone()

                if not row:
                    return jsonify({'success': False, 'message': 'Захтев није пронађен'}), 404

                request_type = row[0]
                status = row[1]
                current_step = row[2]
                creator_email = row[4] if len(row) > 4 else None
                req_title = row[5] if len(row) > 5 else ''

                if status not in ['pending', 'in_review']:
                    return jsonify({'success': False, 'message': 'Захтев није у статусу чекања'}), 400

                if creator_email and creator_email == user_email:
                    return jsonify({'success': False, 'message': 'Не можете одобрити сопствени захтев'}), 403

                if not can_approve_request(user_role, request_type, current_step):
                    return jsonify({'success': False, 'message': 'Немате дозволу за одобрење у овој фази'}), 403

                # Derive the chain from the authoritative APPROVAL_CHAINS constant
                # (the same source used for authorization) so the finalize/advance
                # decision and the notification label never drift from the stored,
                # per-row approval_chain snapshot.
                chain = APPROVAL_CHAINS.get(request_type, [])
                cur.execute(
                    """
                    UPDATE approval_signatures
                    SET decision = 'approved', approver_email = %s, approver_name = %s,
                        comments = %s, signed_at = NOW()
                    WHERE request_id = %s AND signature_order = %s
                    """,
                    (user_email, user_name, comments, request_id, current_step),
                )

                next_step = current_step + 1
                if next_step >= len(chain):
                    cur.execute(
                        """
                        UPDATE archive_requests
                        SET status = 'approved', current_approval_step = %s,
                            final_decision = 'approved', final_decision_by_email = %s,
                            final_decision_by_name = %s, final_decision_at = NOW(),
                            updated_at = NOW()
                        WHERE id = %s
                        """,
                        (next_step, user_email, user_name, request_id),
                    )
                else:
                    cur.execute(
                        """
                        UPDATE archive_requests
                        SET current_approval_step = %s, status = 'in_review', updated_at = NOW()
                        WHERE id = %s
                        """,
                        (next_step, request_id),
                    )

                cur.execute(
                    """
                    INSERT INTO request_history (
                        request_id, action, action_by_email, action_by_name, notes
                    ) VALUES (%s, 'approved', %s, %s, %s)
                    """,
                    (request_id, user_email, user_name, f"Одобрено у кораку {current_step + 1}. {comments}"),
                )

                # Notify request creator about approval
                if creator_email:
                    step_label = chain[current_step].get('label', '') if current_step < len(chain) else ''
                    if next_step >= len(chain):
                        notif_title = 'Захтев одобрен'
                        notif_msg = f'Ваш захтев „{req_title or ""}" је потпуно одобрен.'
                        notif_icon = 'bi-check-circle-fill'
                        notif_type = 'success'
                    else:
                        notif_title = 'Захтев одобрен у кораку'
                        notif_msg = f'{step_label} је одобрио/ла ваш захтев „{req_title or ""}". Чека се следећи ниво одобрења.'
                        notif_icon = 'bi-check-circle'
                        notif_type = 'info'
                    cur.execute(
                        """
                        INSERT INTO user_notifications (user_email, title, message, icon, type)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (creator_email, notif_title, notif_msg, notif_icon, notif_type),
                    )

                conn.commit()

        return jsonify(
            {
                'success': True,
                'message': 'Захтев је успешно одобрен',
                'final': next_step >= len(chain),
            }
        )
    except Exception as exc:
        logger.exception("Error approving request")
        capture_observability_exception(
            exc,
            tags={'component': 'archive', 'operation': 'approve_request'},
            extra={'request_id': request_id, 'user_role': session.get('user_role')},
            user={'email': session.get('user_email')},
        )
        return _server_error_response()


@archive_signature_bp.route('/api/archive/requests/<int:request_id>/reject', methods=['POST'])
@login_required
def api_reject_archive_request(request_id):
    """Reject request."""
    try:
        data = request.get_json() or {}
        comments = data.get('comments', '')
        if not comments:
            return jsonify({'success': False, 'message': 'Молимо унесите разлог одбијања'}), 400

        user_email = session.get('user_email', '')
        user_name = session.get('user_name', '')
        user_role = session.get('user_role', 'employee')

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT request_type, status, current_approval_step,
                           approval_chain, created_by_email, title
                    FROM archive_requests WHERE id = %s
                    FOR UPDATE
                    """,
                    (request_id,),
                )
                row = cur.fetchone()

                if not row:
                    return jsonify({'success': False, 'message': 'Захтев није пронађен'}), 404

                request_type = row[0]
                status = row[1]
                current_step = row[2]
                creator_email = row[4] if len(row) > 4 else None
                req_title = row[5] if len(row) > 5 else ''

                if status not in ['pending', 'in_review']:
                    return jsonify({'success': False, 'message': 'Захтев није у статусу чекања'}), 400

                if creator_email and creator_email == user_email:
                    return jsonify({'success': False, 'message': 'Не можете одбити сопствени захтев'}), 403

                if not can_approve_request(user_role, request_type, current_step):
                    return jsonify({'success': False, 'message': 'Немате дозволу за одбијање'}), 403

                cur.execute(
                    """
                    UPDATE approval_signatures
                    SET decision = 'rejected', approver_email = %s, approver_name = %s,
                        comments = %s, signed_at = NOW()
                    WHERE request_id = %s AND signature_order = %s
                    """,
                    (user_email, user_name, comments, request_id, current_step),
                )

                cur.execute(
                    """
                    UPDATE archive_requests
                    SET status = 'rejected', final_decision = 'rejected',
                        final_decision_by_email = %s, final_decision_by_name = %s,
                        final_decision_at = NOW(), final_notes = %s, updated_at = NOW()
                    WHERE id = %s
                    """,
                    (user_email, user_name, comments, request_id),
                )

                cur.execute(
                    """
                    INSERT INTO request_history (
                        request_id, action, action_by_email, action_by_name, notes
                    ) VALUES (%s, 'rejected', %s, %s, %s)
                    """,
                    (request_id, user_email, user_name, comments),
                )

                # Notify request creator about rejection
                if creator_email:
                    chain = APPROVAL_CHAINS.get(request_type, [])
                    step_label = chain[current_step].get('label', '') if current_step < len(chain) else ''
                    cur.execute(
                        """
                        INSERT INTO user_notifications (user_email, title, message, icon, type)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            creator_email,
                            'Захтев одбијен',
                            f'{step_label} је одбио/ла ваш захтев „{req_title or ""}". Разлог: {comments}',
                            'bi-x-circle-fill',
                            'error',
                        ),
                    )

                conn.commit()

        return jsonify({'success': True, 'message': 'Захтев је одбијен'})
    except Exception:
        logger.exception("Error rejecting request")
        return _server_error_response()


@archive_signature_bp.route('/api/archive/requests/<int:request_id>/comment', methods=['POST'])
@login_required
def api_add_request_comment(request_id):
    """Add comment to request."""
    try:
        data = request.get_json() or {}
        comment = data.get('comment', '').strip()
        if not comment:
            return jsonify({'success': False, 'message': 'Молимо унесите коментар'}), 400

        user_email = session.get('user_email', '')
        user_name = session.get('user_name', '')

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO request_comments (request_id, author_email, author_name, comment)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (request_id, user_email, user_name, comment),
                )
                comment_id = cur.fetchone()[0]

                cur.execute(
                    """
                    INSERT INTO request_history (
                        request_id, action, action_by_email, action_by_name, notes
                    ) VALUES (%s, 'commented', %s, %s, %s)
                    """,
                    (request_id, user_email, user_name, comment[:100]),
                )
                conn.commit()

        return jsonify(
            {
                'success': True,
                'message': 'Коментар је додат',
                'comment_id': comment_id,
            }
        )
    except Exception:
        logger.exception("Error adding comment")
        return _server_error_response()


@archive_signature_bp.route('/api/archive/pending', methods=['GET'])
@login_required
def api_get_pending_approvals():
    """Get pending approvals for current user."""
    try:
        user_role = session.get('user_role', 'employee')

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                pending_requests = []

                for request_type, chain in APPROVAL_CHAINS.items():
                    for step_index, approver in enumerate(chain):
                        if can_approve_request(user_role, request_type, step_index):
                            cur.execute(
                                """
                                SELECT ar.id, ar.title, ar.request_type, ar.subtype,
                                       ar.created_by_name, ar.created_at, ar.priority
                                FROM archive_requests ar
                                WHERE ar.request_type = %s
                                AND ar.current_approval_step = %s
                                AND ar.status IN ('pending', 'in_review')
                                ORDER BY
                                    CASE ar.priority
                                        WHEN 'urgent' THEN 1
                                        WHEN 'high' THEN 2
                                        WHEN 'normal' THEN 3
                                        WHEN 'low' THEN 4
                                    END,
                                    ar.created_at
                                """,
                                (request_type, step_index),
                            )

                            for row in cur.fetchall():
                                pending_requests.append(
                                    {
                                        'id': row[0],
                                        'title': row[1],
                                        'request_type': row[2],
                                        'subtype': row[3],
                                        'created_by_name': row[4],
                                        'created_at': row[5].isoformat() if row[5] else None,
                                        'priority': row[6],
                                        'approval_role': approver['label'],
                                    }
                                )

        return jsonify(
            {
                'success': True,
                'pending': pending_requests,
                'count': len(pending_requests),
            }
        )
    except Exception:
        logger.exception("Error getting pending approvals")
        return _server_error_response()


@archive_signature_bp.route('/api/archive/statistics', methods=['GET'])
@login_required
def api_get_archive_statistics():
    """Get archive statistics for dashboard."""
    try:
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                stats = {
                    'total': 0,
                    'pending': 0,
                    'approved': 0,
                    'rejected': 0,
                    'by_type': {},
                    'recent_activity': [],
                }

                cur.execute("SELECT status, COUNT(*) FROM archive_requests GROUP BY status")
                for row in cur.fetchall():
                    stats[row[0]] = row[1]
                    stats['total'] += row[1]

                cur.execute("SELECT request_type, COUNT(*) FROM archive_requests GROUP BY request_type")
                for row in cur.fetchall():
                    stats['by_type'][row[0]] = row[1]

                cur.execute(
                    """
                    SELECT ar.id, ar.title, ar.request_type, rh.action,
                           rh.action_by_name, rh.created_at
                    FROM request_history rh
                    JOIN archive_requests ar ON ar.id = rh.request_id
                    ORDER BY rh.created_at DESC
                    LIMIT 10
                    """
                )
                for row in cur.fetchall():
                    stats['recent_activity'].append(
                        {
                            'request_id': row[0],
                            'title': row[1],
                            'request_type': row[2],
                            'action': row[3],
                            'by_name': row[4],
                            'created_at': row[5].isoformat() if row[5] else None,
                        }
                    )

        return jsonify({'success': True, 'statistics': stats})
    except Exception:
        logger.exception("Error getting statistics")
        return _server_error_response()


@archive_signature_bp.route('/api/archive/requests/<int:request_id>/archive', methods=['POST'])
@login_required
@admin_required
def api_archive_request(request_id):
    """Move approved request to archive."""
    try:
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT status FROM archive_requests WHERE id = %s", (request_id,))
                row = cur.fetchone()

                if not row:
                    return jsonify({'success': False, 'message': 'Захтев није пронађен'}), 404

                if row[0] != 'approved':
                    return jsonify({'success': False, 'message': 'Само одобрени захтеви могу бити архивирани'}), 400

                year = datetime.now().year
                # Serialize reference allocation for this year within the
                # transaction so concurrent archivings cannot mint duplicates.
                cur.execute(
                    "SELECT pg_advisory_xact_lock(%s, %s)",
                    (_ARCHIVE_REF_LOCK_NS, year),
                )
                # Derive the next sequence from the highest existing reference
                # for the year (not COUNT(*), which drifts if a row is later
                # un-archived or deleted).
                cur.execute(
                    """
                    SELECT COALESCE(MAX(
                        CAST(SUBSTRING(archive_reference FROM '([0-9]+)$') AS INTEGER)
                    ), 0)
                    FROM archive_requests
                    WHERE archive_year = %s AND archive_reference IS NOT NULL
                    """,
                    (year,),
                )
                count = cur.fetchone()[0] + 1
                archive_ref = f"АРХ-{year}-{count:05d}"

                cur.execute(
                    """
                    UPDATE archive_requests
                    SET status = 'archived', archived_at = NOW(),
                        archive_reference = %s, archive_year = %s
                    WHERE id = %s
                    """,
                    (archive_ref, year, request_id),
                )

                user_email = session.get('user_email', '')
                user_name = session.get('user_name', '')
                cur.execute(
                    """
                    INSERT INTO request_history (
                        request_id, action, action_by_email, action_by_name, notes
                    ) VALUES (%s, 'archived', %s, %s, %s)
                    """,
                    (request_id, user_email, user_name, f"Архивирано под бројем {archive_ref}"),
                )
                conn.commit()

        return jsonify(
            {
                'success': True,
                'message': f'Захтев је архивиран под бројем {archive_ref}',
                'archive_reference': archive_ref,
            }
        )
    except Exception:
        logger.exception("Error archiving request")
        return _server_error_response()


@archive_signature_bp.route('/admin/digital-signatures')
@login_required
def admin_digital_signatures():
    """Digital signature management dashboard."""
    user_role = session.get('user_role', '')
    if user_role not in ['admin', 'direktor', 'sef_pravne_sluzbe']:
        flash('Немате приступ овој страници.', 'error')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_digital_signatures.html')


@archive_signature_bp.route('/api/digital-signatures', methods=['GET'])
@login_required
def api_get_digital_signatures():
    """Get all digital signatures with filters."""
    try:
        user_role = session.get('user_role', '')
        user_email = session.get('user_email', '')
        can_see_all = user_role in ['admin', 'direktor', 'sef_pravne_sluzbe']

        status_filter = request.args.get('status', 'all')
        doc_type_filter = request.args.get('document_type', 'all')

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT id, document_type, document_id, document_title, document_pdf_path,
                           requester_email, requester_name, requester_department,
                           status, requester_signed_at, requester_signature_valid,
                           legal_verified_at, legal_verified_by_name, legal_verification_notes,
                           approver_signed_at, approver_name,
                           registration_number, registered_at,
                           created_at, updated_at, notes
                    FROM document_signatures
                    WHERE 1=1
                """
                params = []

                if not can_see_all:
                    query += " AND requester_email = %s"
                    params.append(user_email)

                if status_filter != 'all':
                    query += " AND status = %s"
                    params.append(status_filter)

                if doc_type_filter != 'all':
                    query += " AND document_type = %s"
                    params.append(doc_type_filter)

                query += " ORDER BY created_at DESC"
                cur.execute(query, params)

                signatures = []
                for row in cur.fetchall():
                    _, safe_document_path, _ = resolve_signature_document_path(row[4])
                    signatures.append(
                        {
                            'id': row[0],
                            'document_type': row[1],
                            'document_id': row[2],
                            'document_title': row[3],
                            'document_pdf_path': safe_document_path,
                            'requester_email': row[5],
                            'requester_name': row[6],
                            'requester_department': row[7],
                            'status': row[8],
                            'requester_signed_at': row[9].isoformat() if row[9] else None,
                            'requester_signature_valid': row[10],
                            'legal_verified_at': row[11].isoformat() if row[11] else None,
                            'legal_verified_by_name': row[12],
                            'legal_verification_notes': row[13],
                            'approver_signed_at': row[14].isoformat() if row[14] else None,
                            'approver_name': row[15],
                            'registration_number': row[16],
                            'registered_at': row[17].isoformat() if row[17] else None,
                            'created_at': row[18].isoformat() if row[18] else None,
                            'updated_at': row[19].isoformat() if row[19] else None,
                            'notes': row[20],
                        }
                    )

        return jsonify({'success': True, 'signatures': signatures})
    except Exception:
        logger.exception("Error fetching digital signatures")
        return _server_error_response()


@archive_signature_bp.route('/api/digital-signatures/templates', methods=['GET'])
@login_required
def api_get_signature_templates():
    """Get all signature templates."""
    try:
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, document_type, document_type_label,
                           requires_requester_signature, requires_legal_verification,
                           requires_approver_signature, approver_roles, instructions
                    FROM signature_templates
                    WHERE is_active = TRUE
                    ORDER BY document_type_label
                    """
                )

                templates = [
                    {
                        'id': row[0],
                        'document_type': row[1],
                        'document_type_label': row[2],
                        'requires_requester_signature': row[3],
                        'requires_legal_verification': row[4],
                        'requires_approver_signature': row[5],
                        'approver_roles': row[6] if row[6] else [],
                        'instructions': row[7],
                    }
                    for row in cur.fetchall()
                ]

        return jsonify({'success': True, 'templates': templates})
    except Exception:
        logger.exception("Error fetching signature templates")
        return _server_error_response()


@archive_signature_bp.route('/api/digital-signatures', methods=['POST'])
@login_required
def api_create_digital_signature():
    """Create a new document signature request."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Нема података'}), 400

        document_type = data.get('document_type')
        document_id = data.get('document_id')
        document_title = data.get('document_title')
        document_pdf_path = data.get('document_pdf_path')

        if not document_type or not document_title:
            return jsonify({'success': False, 'message': 'Недостају обавезна поља'}), 400

        user_email = session.get('user_email', '')
        user_name = session.get('user_name', '')
        user_department = session.get('user_department', '')

        document_hash = None
        stored_document_path = None
        if document_pdf_path:
            resolved_document_path, stored_document_path, path_error = resolve_signature_document_path(document_pdf_path)
            if path_error:
                return jsonify({'success': False, 'message': path_error}), 400
            with open(resolved_document_path, 'rb') as file_handle:
                document_hash = hashlib.sha256(file_handle.read()).hexdigest()

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO document_signatures (
                        document_type, document_id, document_title, document_pdf_path,
                        requester_email, requester_name, requester_department,
                        status, document_hash
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending_signature', %s)
                    RETURNING id
                    """,
                    (
                        document_type,
                        document_id,
                        document_title,
                        stored_document_path,
                        user_email,
                        user_name,
                        user_department,
                        document_hash,
                    ),
                )
                sig_id = cur.fetchone()[0]

                cur.execute(
                    """
                    INSERT INTO signature_audit_log (
                        document_signature_id, action, action_by_email, action_by_name,
                        action_details
                    ) VALUES (%s, 'created', %s, %s, %s)
                    """,
                    (
                        sig_id,
                        user_email,
                        user_name,
                        psycopg.types.json.Json(
                            {'document_type': document_type, 'document_title': document_title}
                        ),
                    ),
                )
                conn.commit()

        return jsonify(
            {
                'success': True,
                'message': 'Захтев за потпис је креиран',
                'signature_id': sig_id,
            }
        )
    except Exception:
        logger.exception("Error creating digital signature")
        return _server_error_response()


@archive_signature_bp.route('/api/digital-signatures/<int:sig_id>/sign', methods=['POST'])
@login_required
def api_sign_document(sig_id):
    """Mark document as signed by requester."""
    try:
        user_email = session.get('user_email', '')
        user_name = session.get('user_name', '')
        certificate_info = (request.get_json() or {}).get('certificate_info', {})

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT requester_email, status FROM document_signatures WHERE id = %s",
                    (sig_id,),
                )
                row = cur.fetchone()

                if not row:
                    return jsonify({'success': False, 'message': 'Документ није пронађен'}), 404

                if row[0] != user_email:
                    return jsonify({'success': False, 'message': 'Само подносилац може потписати документ'}), 403

                if row[1] != 'pending_signature':
                    return jsonify({'success': False, 'message': 'Документ није у статусу за потписивање'}), 400

                cur.execute(
                    """
                    UPDATE document_signatures
                    SET requester_signed_at = NOW(),
                        requester_signature_valid = TRUE,
                        requester_certificate_info = %s,
                        status = 'pending_legal_verification',
                        updated_at = NOW()
                    WHERE id = %s
                    """,
                    (psycopg.types.json.Json(certificate_info), sig_id),
                )

                cur.execute(
                    """
                    INSERT INTO signature_audit_log (
                        document_signature_id, action, action_by_email, action_by_name,
                        action_details
                    ) VALUES (%s, 'signed', %s, %s, %s)
                    """,
                    (
                        sig_id,
                        user_email,
                        user_name,
                        psycopg.types.json.Json({'certificate_info': certificate_info}),
                    ),
                )
                conn.commit()

        return jsonify(
            {
                'success': True,
                'message': 'Документ је потписан и прослеђен на верификацију',
            }
        )
    except Exception:
        logger.exception("Error signing document")
        return _server_error_response()


@archive_signature_bp.route('/api/digital-signatures/<int:sig_id>/verify', methods=['POST'])
@login_required
def api_verify_signature(sig_id):
    """Legal verification of signature by sef_pravne_sluzbe."""
    try:
        user_role = session.get('user_role', '')
        user_email = session.get('user_email', '')
        user_name = session.get('user_name', '')

        if user_role not in ['sef_pravne_sluzbe', 'admin']:
            return jsonify({'success': False, 'message': 'Немате овлашћење за верификацију'}), 403

        data = request.get_json() or {}
        verification_notes = data.get('notes', '')
        certificate_info = data.get('certificate_info', {})

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT status, document_type FROM document_signatures WHERE id = %s",
                    (sig_id,),
                )
                row = cur.fetchone()

                if not row:
                    return jsonify({'success': False, 'message': 'Документ није пронађен'}), 404

                if row[0] != 'pending_legal_verification':
                    return jsonify({'success': False, 'message': 'Документ није у статусу за верификацију'}), 400

                cur.execute(
                    """
                    SELECT requires_approver_signature FROM signature_templates
                    WHERE document_type = %s
                    """,
                    (row[1],),
                )
                template_row = cur.fetchone()
                requires_approver = template_row[0] if template_row else False
                new_status = 'pending_approval' if requires_approver else 'verified'

                cur.execute(
                    """
                    UPDATE document_signatures
                    SET legal_verified_at = NOW(),
                        legal_verified_by_email = %s,
                        legal_verified_by_name = %s,
                        legal_verification_notes = %s,
                        legal_certificate_info = %s,
                        status = %s,
                        updated_at = NOW()
                    WHERE id = %s
                    """,
                    (
                        user_email,
                        user_name,
                        verification_notes,
                        psycopg.types.json.Json(certificate_info),
                        new_status,
                        sig_id,
                    ),
                )

                cur.execute(
                    """
                    INSERT INTO signature_audit_log (
                        document_signature_id, action, action_by_email, action_by_name,
                        action_details
                    ) VALUES (%s, 'verified', %s, %s, %s)
                    """,
                    (
                        sig_id,
                        user_email,
                        user_name,
                        psycopg.types.json.Json({'notes': verification_notes, 'new_status': new_status}),
                    ),
                )
                conn.commit()

        message = 'Потпис је верификован'
        if new_status != 'verified':
            message = 'Потпис је верификован и прослеђен на одобрење'
        return jsonify({'success': True, 'message': message, 'new_status': new_status})
    except Exception:
        logger.exception("Error verifying signature")
        return _server_error_response()


@archive_signature_bp.route('/api/digital-signatures/<int:sig_id>/reject', methods=['POST'])
@login_required
def api_reject_signature(sig_id):
    """Reject a signature request."""
    try:
        user_role = session.get('user_role', '')
        user_email = session.get('user_email', '')
        user_name = session.get('user_name', '')

        if user_role not in ['sef_pravne_sluzbe', 'direktor', 'admin']:
            return jsonify({'success': False, 'message': 'Немате овлашћење за одбијање'}), 403

        rejection_reason = (request.get_json() or {}).get('reason', '')
        if not rejection_reason:
            return jsonify({'success': False, 'message': 'Разлог одбијања је обавезан'}), 400

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE document_signatures
                    SET status = 'rejected',
                        notes = %s,
                        updated_at = NOW()
                    WHERE id = %s
                    """,
                    (rejection_reason, sig_id),
                )

                cur.execute(
                    """
                    INSERT INTO signature_audit_log (
                        document_signature_id, action, action_by_email, action_by_name,
                        action_details
                    ) VALUES (%s, 'rejected', %s, %s, %s)
                    """,
                    (
                        sig_id,
                        user_email,
                        user_name,
                        psycopg.types.json.Json({'reason': rejection_reason}),
                    ),
                )
                conn.commit()

        return jsonify({'success': True, 'message': 'Захтев је одбијен'})
    except Exception:
        logger.exception("Error rejecting signature")
        return _server_error_response()


@archive_signature_bp.route('/api/digital-signatures/<int:sig_id>/approve', methods=['POST'])
@login_required
def api_approve_signature(sig_id):
    """Final approval by approver (direktor, sef_odeljenja, etc.)."""
    try:
        user_role = session.get('user_role', '')
        user_email = session.get('user_email', '')
        user_name = session.get('user_name', '')
        certificate_info = (request.get_json() or {}).get('certificate_info', {})

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT ds.status, ds.document_type, st.approver_roles
                    FROM document_signatures ds
                    LEFT JOIN signature_templates st ON st.document_type = ds.document_type
                    WHERE ds.id = %s
                    """,
                    (sig_id,),
                )
                row = cur.fetchone()

                if not row:
                    return jsonify({'success': False, 'message': 'Документ није пронађен'}), 404

                status, _document_type, approver_roles = row
                if status != 'pending_approval':
                    return jsonify({'success': False, 'message': 'Документ није у статусу за одобрење'}), 400

                allowed_roles = approver_roles if approver_roles else []
                if user_role not in allowed_roles and user_role not in ['admin', 'direktor']:
                    return jsonify({'success': False, 'message': 'Немате овлашћење за одобрење овог документа'}), 403

                cur.execute(
                    """
                    UPDATE document_signatures
                    SET approver_signed_at = NOW(),
                        approver_email = %s,
                        approver_name = %s,
                        approver_certificate_info = %s,
                        status = 'verified',
                        updated_at = NOW()
                    WHERE id = %s
                    """,
                    (user_email, user_name, psycopg.types.json.Json(certificate_info), sig_id),
                )

                cur.execute(
                    """
                    INSERT INTO signature_audit_log (
                        document_signature_id, action, action_by_email, action_by_name,
                        action_details
                    ) VALUES (%s, 'approved', %s, %s, %s)
                    """,
                    (
                        sig_id,
                        user_email,
                        user_name,
                        psycopg.types.json.Json({'certificate_info': certificate_info}),
                    ),
                )
                conn.commit()

        return jsonify({'success': True, 'message': 'Документ је одобрен и верификован'})
    except Exception:
        logger.exception("Error approving signature")
        return _server_error_response()


@archive_signature_bp.route('/api/digital-signatures/<int:sig_id>/register', methods=['POST'])
@login_required
def api_register_signature(sig_id):
    """Register document with delovodni broj."""
    try:
        user_role = session.get('user_role', '')
        user_email = session.get('user_email', '')
        user_name = session.get('user_name', '')

        if user_role not in ['sef_pravne_sluzbe', 'admin']:
            return jsonify({'success': False, 'message': 'Немате овлашћење за завођење'}), 403

        manual_number = (request.get_json() or {}).get('registration_number')

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT status FROM document_signatures WHERE id = %s", (sig_id,))
                row = cur.fetchone()

                if not row:
                    return jsonify({'success': False, 'message': 'Документ није пронађен'}), 404

                if row[0] != 'verified':
                    return jsonify({'success': False, 'message': 'Документ мора бити верификован пре завођења'}), 400

                if manual_number:
                    reg_number = manual_number
                else:
                    year = datetime.now().year
                    # Serialize delovodni-number allocation for this year within
                    # the transaction so concurrent registrations cannot collide.
                    cur.execute(
                        "SELECT pg_advisory_xact_lock(%s, %s)",
                        (_REGISTRATION_LOCK_NS, year),
                    )
                    # Derive the next sequence from the highest existing number
                    # for the year (not COUNT(*), which would reuse a number
                    # after any deletion).
                    cur.execute(
                        """
                        SELECT COALESCE(MAX(
                            CAST(SUBSTRING(registration_number FROM '-([0-9]+)/') AS INTEGER)
                        ), 0)
                        FROM document_signatures
                        WHERE registration_number IS NOT NULL
                        AND EXTRACT(YEAR FROM registered_at) = %s
                        """,
                        (year,),
                    )
                    reg_number = f"01-{cur.fetchone()[0] + 1:04d}/{year}"

                cur.execute(
                    """
                    UPDATE document_signatures
                    SET registration_number = %s,
                        registered_at = NOW(),
                        registered_by_email = %s,
                        status = 'archived',
                        updated_at = NOW()
                    WHERE id = %s
                    """,
                    (reg_number, user_email, sig_id),
                )

                cur.execute(
                    """
                    INSERT INTO signature_audit_log (
                        document_signature_id, action, action_by_email, action_by_name,
                        action_details
                    ) VALUES (%s, 'registered', %s, %s, %s)
                    """,
                    (
                        sig_id,
                        user_email,
                        user_name,
                        psycopg.types.json.Json({'registration_number': reg_number}),
                    ),
                )
                conn.commit()

        return jsonify(
            {
                'success': True,
                'message': f'Документ је заведен под бројем {reg_number}',
                'registration_number': reg_number,
            }
        )
    except Exception:
        logger.exception("Error registering signature")
        return _server_error_response()


@archive_signature_bp.route('/api/digital-signatures/<int:sig_id>/audit', methods=['GET'])
@login_required
def api_get_signature_audit(sig_id):
    """Get audit trail for a signature."""
    try:
        user_role = session.get('user_role', '')
        user_email = session.get('user_email', '')
        can_see_all = user_role in ['admin', 'direktor', 'sef_pravne_sluzbe']

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT requester_email FROM document_signatures WHERE id = %s", (sig_id,))
                signature_row = cur.fetchone()
                if not signature_row:
                    return jsonify({'success': False, 'message': 'Документ није пронађен'}), 404
                if not can_see_all and signature_row[0] != user_email:
                    return jsonify({'success': False, 'message': 'Немате приступ овом документу'}), 403

                cur.execute(
                    """
                    SELECT id, action, action_by_email, action_by_name,
                           action_details, created_at
                    FROM signature_audit_log
                    WHERE document_signature_id = %s
                    ORDER BY created_at ASC
                    """,
                    (sig_id,),
                )
                audit = [
                    {
                        'id': row[0],
                        'action': row[1],
                        'action_by_email': row[2],
                        'action_by_name': row[3],
                        'action_details': row[4] if row[4] else {},
                        'created_at': row[5].isoformat() if row[5] else None,
                    }
                    for row in cur.fetchall()
                ]

        return jsonify({'success': True, 'audit': audit})
    except Exception:
        logger.exception("Error fetching audit log")
        return _server_error_response()


@archive_signature_bp.route('/api/digital-signatures/statistics', methods=['GET'])
@login_required
def api_get_signature_statistics():
    """Get signature statistics for dashboard."""
    try:
        user_role = session.get('user_role', '')
        if user_role not in ['admin', 'direktor', 'sef_pravne_sluzbe']:
            return jsonify({'success': False, 'message': 'Немате приступ статистици'}), 403

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                stats = {
                    'total': 0,
                    'pending_signature': 0,
                    'pending_legal_verification': 0,
                    'pending_approval': 0,
                    'verified': 0,
                    'rejected': 0,
                    'archived': 0,
                    'by_type': {},
                }

                cur.execute(
                    """
                    SELECT status, COUNT(*) FROM document_signatures
                    GROUP BY status
                    """
                )
                for row in cur.fetchall():
                    stats[row[0]] = row[1]
                    stats['total'] += row[1]

                cur.execute(
                    """
                    SELECT document_type, COUNT(*) FROM document_signatures
                    GROUP BY document_type
                    """
                )
                for row in cur.fetchall():
                    stats['by_type'][row[0]] = row[1]

        return jsonify({'success': True, 'statistics': stats})
    except Exception:
        logger.exception("Error fetching statistics")
        return _server_error_response()
