"""Document library: storage, review and approval workflow for museum documents.

Files live on disk under DOCUMENTS_STORAGE_PATH (production: /data/mis/dokumenti);
PostgreSQL stores only the relative path, metadata and a sha256 checksum.
Workflow per version: nacrt -> na_odobrenju -> odobreno -> arhivirano
(rejection returns the version to nacrt with a review comment).

Approval policy mirrors the timesheet module: every employee may upload,
department heads approve documents from their own department, the director
approves everything (including heads' uploads), and nobody approves a version
they uploaded themselves.
"""

import hashlib
import mimetypes
import os
import uuid
from pathlib import Path

from flask import (
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

from postgres_service import get_postgres_connection


DOCUMENT_CATEGORIES = {
    'obrasci_zahtevi': 'Обрасци и захтеви',
    'uputstva': 'Упутства',
    'pravilnici': 'Правилници',
    'finansije': 'Финансије',
    'izvestaji': 'Извештаји',
    'organizacija': 'Организација',
    'ostalo': 'Остало',
}

DOCUMENT_STATUS_LABELS = {
    'nacrt': 'Нацрт',
    'na_odobrenju': 'На одобрењу',
    'odobreno': 'Одобрено',
    'arhivirano': 'Архивирано',
}

ALLOWED_DOCUMENT_EXTENSIONS = {
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.odt', '.ods', '.rtf', '.txt', '.jpg', '.jpeg', '.png',
}

MAX_DOCUMENT_SIZE = 25 * 1024 * 1024  # 25MB, comfortably under MAX_CONTENT_LENGTH

INLINE_EXTENSIONS = {'.pdf'}

VERSION_COLUMNS = (
    'v.id, v.document_id, v.version_no, v.file_path, v.original_filename, '
    'v.mime_type, v.file_size, v.sha256, v.status, v.uploaded_by_email, '
    'v.uploaded_at, v.submitted_at, v.reviewed_by_email, v.reviewed_at, '
    'v.review_comment'
)


def get_documents_storage_path() -> Path:
    return Path(os.environ.get('DOCUMENTS_STORAGE_PATH', './data/dokumenti'))


def _norm_dept(name) -> str:
    """Same normalization policy as timesheet: department names are maintained
    by hand and can drift in case/whitespace."""
    return (name or '').strip().casefold()


def _session_is_admin(session_data) -> bool:
    return session_data.get('user_role') == 'admin'


def _session_is_director(session_data) -> bool:
    return session_data.get('user_role') == 'direktor'


def _session_is_department_head(session_data) -> bool:
    return bool(session_data.get('is_department_head', False))


def _session_email(session_data) -> str:
    return (session_data.get('user_email') or '').strip().lower()


def can_view_document_version(session_data, document, version) -> bool:
    """Approved versions are visible to every logged-in user. Drafts, pending
    and archived versions are visible only to the uploader, admins, the
    director, and the head of the document's department."""
    if version.get('status') == 'odobreno':
        return True
    if _session_is_admin(session_data) or _session_is_director(session_data):
        return True
    user_email = _session_email(session_data)
    uploader = (version.get('uploaded_by_email') or '').strip().lower()
    if user_email and user_email == uploader:
        return True
    if _session_is_department_head(session_data):
        doc_dept = _norm_dept(document.get('department'))
        return bool(doc_dept) and doc_dept == _norm_dept(session_data.get('user_department'))
    return False


def can_approve_document_version(session_data, document, version) -> bool:
    """Self-approval is forbidden for everyone. Admins and the director
    approve any department; a department head only documents from their own
    department. Documents without a department fall to the director/admin."""
    user_email = _session_email(session_data)
    uploader = (version.get('uploaded_by_email') or '').strip().lower()
    if not user_email or (uploader and user_email == uploader):
        return False
    if _session_is_admin(session_data) or _session_is_director(session_data):
        return True
    if not _session_is_department_head(session_data):
        return False
    doc_dept = _norm_dept(document.get('department'))
    return bool(doc_dept) and doc_dept == _norm_dept(session_data.get('user_department'))


def _log_document_action(cursor, document_id, version_id, action, actor_email, note=None):
    cursor.execute(
        """
        INSERT INTO document_audit_log (document_id, version_id, action, actor_email, note)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (document_id, version_id, action, actor_email, note),
    )


def _fetch_version_with_document(cursor, version_id):
    """Return `(document_row, version_row)` as dicts, or `(None, None)`."""
    cursor.execute(
        f"""
        SELECT {VERSION_COLUMNS},
               d.id AS d_id, d.title AS d_title, d.description AS d_description,
               d.category AS d_category, d.department AS d_department,
               d.created_by_email AS d_created_by_email, d.is_active AS d_is_active
        FROM document_versions v
        JOIN documents d ON d.id = v.document_id
        WHERE v.id = %s
        """,
        (version_id,),
    )
    row = cursor.fetchone()
    if not row:
        return None, None
    row = _row_to_dict(cursor, row)
    document = {
        'id': row['d_id'],
        'title': row['d_title'],
        'description': row['d_description'],
        'category': row['d_category'],
        'department': row['d_department'],
        'created_by_email': row['d_created_by_email'],
        'is_active': row['d_is_active'],
    }
    version = {key: value for key, value in row.items() if not key.startswith('d_')}
    return document, version


def _row_to_dict(cursor, row):
    if isinstance(row, dict):
        return row
    columns = [column.name for column in cursor.description]
    return dict(zip(columns, row))


def _rows_to_dicts(cursor, rows):
    return [_row_to_dict(cursor, row) for row in rows]


def _safe_document_filename(original_filename: str) -> str:
    """`secure_filename` strips Cyrillic characters entirely, so keep the
    extension by hand (same approach as image_api.py)."""
    ext = Path(original_filename or '').suffix.lower()
    safe_name = secure_filename(original_filename or '') or 'dokument'
    if not Path(safe_name).suffix:
        safe_name = f"{safe_name}{ext}"
    return safe_name


def _sha256_of_file(file_path: Path) -> str:
    digest = hashlib.sha256()
    with open(file_path, 'rb') as handle:
        for block in iter(lambda: handle.read(65536), b''):
            digest.update(block)
    return digest.hexdigest()


def render_documents_list():
    """Landing page: approved documents per category + the caller's own
    uploads with their workflow status."""
    selected_category = (request.args.get('kategorija') or '').strip()
    if selected_category and selected_category not in DOCUMENT_CATEGORIES:
        selected_category = ''
    search_term = (request.args.get('q') or '').strip()

    user_email = _session_email(session)
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            params = []
            filters = ['d.is_active = TRUE', "v.status = 'odobreno'"]
            if selected_category:
                filters.append('d.category = %s')
                params.append(selected_category)
            if search_term:
                filters.append('d.title ILIKE %s')
                params.append(f'%{search_term}%')
            cur.execute(
                f"""
                SELECT DISTINCT ON (d.id)
                       d.id, d.title, d.description, d.category, d.department,
                       v.id AS version_id, v.version_no, v.original_filename,
                       v.file_size, v.reviewed_at
                FROM documents d
                JOIN document_versions v ON v.document_id = d.id
                WHERE {' AND '.join(filters)}
                ORDER BY d.id, v.version_no DESC
                """,
                params,
            )
            approved_documents = _rows_to_dicts(cur, cur.fetchall())

            cur.execute(
                f"""
                SELECT {VERSION_COLUMNS}, d.title AS document_title, d.category
                FROM document_versions v
                JOIN documents d ON d.id = v.document_id
                WHERE LOWER(v.uploaded_by_email) = %s AND d.is_active = TRUE
                ORDER BY v.uploaded_at DESC
                LIMIT 50
                """,
                (user_email,),
            )
            my_versions = _rows_to_dicts(cur, cur.fetchall())

    approved_documents.sort(key=lambda doc: (doc.get('title') or '').casefold())
    return render_template(
        'dokumenti_lista.html',
        categories=DOCUMENT_CATEGORIES,
        status_labels=DOCUMENT_STATUS_LABELS,
        selected_category=selected_category,
        search_term=search_term,
        approved_documents=approved_documents,
        my_versions=my_versions,
    )


def render_document_detail(document_id):
    """Document page with the version history the caller may see."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, description, category, department,
                       created_by_email, created_at, is_active
                FROM documents WHERE id = %s
                """,
                (document_id,),
            )
            row = cur.fetchone()
            if not row:
                abort(404)
            document = _row_to_dict(cur, row)
            if not document['is_active'] and not (
                _session_is_admin(session) or _session_is_director(session)
            ):
                abort(404)
            cur.execute(
                f"""
                SELECT {VERSION_COLUMNS}
                FROM document_versions v
                WHERE v.document_id = %s
                ORDER BY v.version_no DESC
                """,
                (document_id,),
            )
            versions = _rows_to_dicts(cur, cur.fetchall())

    visible_versions = [
        version for version in versions
        if can_view_document_version(session, document, version)
    ]
    if not visible_versions:
        abort(404)
    user_email = _session_email(session)
    for version in visible_versions:
        version['can_approve'] = (
            version['status'] == 'na_odobrenju'
            and can_approve_document_version(session, document, version)
        )
        version['can_submit'] = (
            version['status'] == 'nacrt'
            and (version.get('uploaded_by_email') or '').strip().lower() == user_email
        )
    return render_template(
        'dokumenti_detalj.html',
        document=document,
        versions=visible_versions,
        categories=DOCUMENT_CATEGORIES,
        status_labels=DOCUMENT_STATUS_LABELS,
    )


def get_pending_document_versions():
    """Versions waiting for approval, scoped like timesheet verification:
    admins and the director see everything, a department head only their
    own department. Rendered by the unified approval center."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT {VERSION_COLUMNS}, d.title AS document_title,
                       d.category, d.department
                FROM document_versions v
                JOIN documents d ON d.id = v.document_id
                WHERE v.status = 'na_odobrenju' AND d.is_active = TRUE
                ORDER BY v.submitted_at ASC NULLS LAST
                """,
            )
            pending = _rows_to_dicts(cur, cur.fetchall())

    if not (_session_is_admin(session) or _session_is_director(session)):
        user_dept = _norm_dept(session.get('user_department'))
        pending = [row for row in pending if _norm_dept(row.get('department')) == user_dept]
    for row in pending:
        row['can_approve'] = can_approve_document_version(
            session,
            {'department': row.get('department')},
            row,
        )
    return pending


def get_archived_document_versions():
    """Archived versions the caller may see, mirroring
    can_view_document_version: admins and the director everything, a
    department head their department plus own uploads, everyone else only
    versions they uploaded themselves. Rendered by the unified archive."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT {VERSION_COLUMNS}, d.title AS document_title,
                       d.category, d.department
                FROM document_versions v
                JOIN documents d ON d.id = v.document_id
                WHERE v.status = 'arhivirano'
                ORDER BY v.reviewed_at DESC NULLS LAST
                """,
            )
            archived = _rows_to_dicts(cur, cur.fetchall())

    if _session_is_admin(session) or _session_is_director(session):
        return archived
    user_email = _session_email(session)
    user_dept = _norm_dept(session.get('user_department'))
    is_head = _session_is_department_head(session)
    return [
        row for row in archived
        if (row.get('uploaded_by_email') or '').strip().lower() == user_email
        or (is_head and bool(user_dept) and _norm_dept(row.get('department')) == user_dept)
    ]


def handle_document_upload():
    """Create a new document (first version) or add a version to an existing
    one. The uploaded version always starts as `nacrt`."""
    uploaded = request.files.get('file')
    if uploaded is None or not (uploaded.filename or '').strip():
        flash('Изаберите датотеку за отпремање.', 'warning')
        return redirect(url_for('documents.dokumenti_lista'))

    original_filename = uploaded.filename
    ext = Path(original_filename).suffix.lower()
    if ext not in ALLOWED_DOCUMENT_EXTENSIONS:
        flash('Тип датотеке није дозвољен.', 'danger')
        return redirect(url_for('documents.dokumenti_lista'))

    uploaded.stream.seek(0, os.SEEK_END)
    file_size = uploaded.stream.tell()
    uploaded.stream.seek(0)
    if file_size <= 0:
        flash('Датотека је празна.', 'danger')
        return redirect(url_for('documents.dokumenti_lista'))
    if file_size > MAX_DOCUMENT_SIZE:
        flash('Датотека је већа од дозвољених 25 MB.', 'danger')
        return redirect(url_for('documents.dokumenti_lista'))

    document_id_raw = (request.form.get('document_id') or '').strip()
    title = (request.form.get('title') or '').strip()
    description = (request.form.get('description') or '').strip()
    category = (request.form.get('category') or '').strip()
    user_email = _session_email(session)

    if not document_id_raw:
        if not title:
            flash('Наслов документа је обавезан.', 'warning')
            return redirect(url_for('documents.dokumenti_lista'))
        if category not in DOCUMENT_CATEGORIES:
            flash('Изаберите важећу категорију.', 'warning')
            return redirect(url_for('documents.dokumenti_lista'))

    storage_root = get_documents_storage_path()
    temp_dir = storage_root / 'temp'
    temp_dir.mkdir(parents=True, exist_ok=True)
    safe_name = _safe_document_filename(original_filename)
    temp_path = temp_dir / f"{uuid.uuid4().hex}_{safe_name}"

    try:
        uploaded.save(temp_path)
        file_hash = _sha256_of_file(temp_path)
        mime_type = mimetypes.guess_type(safe_name)[0] or 'application/octet-stream'

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                if document_id_raw:
                    cur.execute(
                        """
                        SELECT id, title, category, department, is_active
                        FROM documents WHERE id = %s
                        """,
                        (int(document_id_raw),),
                    )
                    row = cur.fetchone()
                    if not row:
                        flash('Документ није пронађен.', 'danger')
                        return redirect(url_for('documents.dokumenti_lista'))
                    document = _row_to_dict(cur, row)
                    if not document['is_active']:
                        flash('Документ је деактивиран.', 'danger')
                        return redirect(url_for('documents.dokumenti_lista'))
                    document_id = document['id']
                    category = document['category']
                    cur.execute(
                        """
                        SELECT 1 FROM document_versions
                        WHERE document_id = %s AND sha256 = %s
                        """,
                        (document_id, file_hash),
                    )
                    if cur.fetchone():
                        flash('Идентична датотека већ постоји као верзија овог документа.', 'warning')
                        return redirect(url_for('documents.dokumenti_detalj', document_id=document_id))
                    cur.execute(
                        """
                        SELECT COALESCE(MAX(version_no), 0) AS max_version
                        FROM document_versions
                        WHERE document_id = %s
                        """,
                        (document_id,),
                    )
                    max_row = cur.fetchone()
                    max_version = (
                        max_row.get('max_version') if isinstance(max_row, dict) else max_row[0]
                    ) or 0
                    version_no = int(max_version) + 1
                else:
                    department = (session.get('user_department') or '').strip() or None
                    cur.execute(
                        """
                        INSERT INTO documents (title, description, category, department, created_by_email)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (title, description or None, category, department, user_email),
                    )
                    inserted = cur.fetchone()
                    document_id = (
                        inserted.get('id') if isinstance(inserted, dict) else inserted[0]
                    )
                    version_no = 1

                relative_path = f"{category}/{document_id}/v{version_no:02d}_{uuid.uuid4().hex[:8]}_{safe_name}"
                final_path = storage_root / relative_path
                final_path.parent.mkdir(parents=True, exist_ok=True)
                os.replace(temp_path, final_path)

                cur.execute(
                    """
                    INSERT INTO document_versions
                        (document_id, version_no, file_path, original_filename,
                         mime_type, file_size, sha256, uploaded_by_email)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (document_id, version_no, relative_path, original_filename,
                     mime_type, file_size, file_hash, user_email),
                )
                inserted = cur.fetchone()
                version_id = (
                    inserted.get('id') if isinstance(inserted, dict) else inserted[0]
                )
                _log_document_action(
                    cur, document_id, version_id, 'upload', user_email,
                    f'Верзија {version_no}: {original_filename}',
                )
    finally:
        if temp_path.exists():
            temp_path.unlink()

    flash('Датотека је отпремљена као нацрт. Пошаљите је на одобрење када будете спремни.', 'success')
    return redirect(url_for('documents.dokumenti_detalj', document_id=document_id))


def handle_submit_for_approval(version_id):
    """nacrt -> na_odobrenju, allowed to the uploader (or admin/direktor)."""
    user_email = _session_email(session)
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            document, version = _fetch_version_with_document(cur, version_id)
            if not version:
                abort(404)
            uploader = (version.get('uploaded_by_email') or '').strip().lower()
            if uploader != user_email and not (
                _session_is_admin(session) or _session_is_director(session)
            ):
                abort(403)
            cur.execute(
                """
                UPDATE document_versions
                SET status = 'na_odobrenju', submitted_at = now()
                WHERE id = %s AND status = 'nacrt'
                RETURNING id
                """,
                (version_id,),
            )
            if not cur.fetchone():
                flash('Верзија није у статусу нацрта.', 'warning')
                return redirect(url_for('documents.dokumenti_detalj', document_id=version['document_id']))
            _log_document_action(cur, version['document_id'], version_id, 'submit', user_email)
    flash('Верзија је послата на одобрење.', 'success')
    return redirect(url_for('documents.dokumenti_detalj', document_id=version['document_id']))


def handle_approve_version(version_id):
    """na_odobrenju -> odobreno; the previously approved version of the same
    document is automatically archived."""
    user_email = _session_email(session)
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            document, version = _fetch_version_with_document(cur, version_id)
            if not version:
                abort(404)
            if not can_approve_document_version(session, document, version):
                abort(403)
            cur.execute(
                """
                UPDATE document_versions
                SET status = 'odobreno', reviewed_by_email = %s,
                    reviewed_at = now(), review_comment = NULL
                WHERE id = %s AND status = 'na_odobrenju'
                RETURNING id
                """,
                (user_email, version_id),
            )
            if not cur.fetchone():
                flash('Верзија није на одобрењу.', 'warning')
                return redirect(url_for('documents.dokumenti_detalj', document_id=version['document_id']))
            cur.execute(
                """
                UPDATE document_versions
                SET status = 'arhivirano'
                WHERE document_id = %s AND status = 'odobreno' AND id <> %s
                """,
                (version['document_id'], version_id),
            )
            _log_document_action(cur, version['document_id'], version_id, 'approve', user_email)
    flash('Верзија је одобрена.', 'success')
    return redirect(request.referrer or url_for('documents.dokumenti_detalj', document_id=version['document_id']))


def handle_reject_version(version_id):
    """na_odobrenju -> nacrt, with a mandatory review comment."""
    user_email = _session_email(session)
    comment = (request.form.get('comment') or '').strip()
    if not comment:
        flash('Разлог одбијања је обавезан.', 'warning')
        return redirect(request.referrer or url_for('documents.dokumenti_lista'))
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            document, version = _fetch_version_with_document(cur, version_id)
            if not version:
                abort(404)
            if not can_approve_document_version(session, document, version):
                abort(403)
            cur.execute(
                """
                UPDATE document_versions
                SET status = 'nacrt', reviewed_by_email = %s,
                    reviewed_at = now(), review_comment = %s
                WHERE id = %s AND status = 'na_odobrenju'
                RETURNING id
                """,
                (user_email, comment, version_id),
            )
            if not cur.fetchone():
                flash('Верзија није на одобрењу.', 'warning')
                return redirect(url_for('documents.dokumenti_detalj', document_id=version['document_id']))
            _log_document_action(cur, version['document_id'], version_id, 'reject', user_email, comment)
    flash('Верзија је враћена у нацрт.', 'success')
    return redirect(request.referrer or url_for('documents.dokumenti_detalj', document_id=version['document_id']))


def handle_archive_version(version_id):
    """odobreno -> arhivirano, manual archiving (admin/direktor only —
    enforced by the route decorator)."""
    user_email = _session_email(session)
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            document, version = _fetch_version_with_document(cur, version_id)
            if not version:
                abort(404)
            cur.execute(
                """
                UPDATE document_versions
                SET status = 'arhivirano'
                WHERE id = %s AND status = 'odobreno'
                RETURNING id
                """,
                (version_id,),
            )
            if not cur.fetchone():
                flash('Само одобрене верзије се архивирају.', 'warning')
                return redirect(url_for('documents.dokumenti_detalj', document_id=version['document_id']))
            _log_document_action(cur, version['document_id'], version_id, 'archive', user_email)
    flash('Верзија је архивирана.', 'success')
    return redirect(url_for('documents.dokumenti_detalj', document_id=version['document_id']))


def serve_document_version(version_id):
    """Login-protected file download; PDF opens inline, everything else is an
    attachment named after the original (Cyrillic-safe) filename."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            document, version = _fetch_version_with_document(cur, version_id)
    if not version:
        abort(404)
    if not can_view_document_version(session, document, version):
        abort(403)

    storage_root = get_documents_storage_path().resolve()
    full_path = (storage_root / version['file_path']).resolve()
    if not str(full_path).startswith(str(storage_root) + os.sep):
        abort(404)
    if not full_path.is_file():
        abort(404)

    ext = Path(version['file_path']).suffix.lower()
    mime_type = version.get('mime_type') or 'application/octet-stream'
    return send_file(
        full_path,
        mimetype=mime_type,
        as_attachment=ext not in INLINE_EXTENSIONS,
        download_name=version.get('original_filename') or full_path.name,
        max_age=0,
    )
