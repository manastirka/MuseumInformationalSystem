"""Document library routes (складиштење, преглед и одобравање докумената)."""

from flask import Blueprint, redirect, url_for

import document_library_views
from security_utils import (
    admin_or_department_head_required,
    admin_or_director_required,
    login_required,
    module_access_required,
)


documents_bp = Blueprint('documents', __name__)


@documents_bp.route('/dokumenti')
@login_required
@module_access_required('dokumenti')
def dokumenti_lista():
    """Approved documents per category + the caller's own uploads."""
    return document_library_views.render_documents_list()


@documents_bp.route('/dokumenti/<int:document_id>')
@login_required
@module_access_required('dokumenti')
def dokumenti_detalj(document_id):
    """Document page with the visible version history."""
    return document_library_views.render_document_detail(document_id)


@documents_bp.route('/dokumenti/odobravanje')
@login_required
@admin_or_department_head_required
def dokumenti_odobravanje():
    """Legacy URL: the queue lives in the unified approval center now."""
    return redirect(url_for('approval_center.centar_odobravanje', tab='dokumenta'))


@documents_bp.route('/dokumenti/upload', methods=['POST'])
@login_required
@module_access_required('dokumenti')
def dokumenti_upload():
    """Every employee may upload; the new version starts as a draft."""
    return document_library_views.handle_document_upload()


@documents_bp.route('/dokumenti/verzija/<int:version_id>/posalji', methods=['POST'])
@login_required
@module_access_required('dokumenti')
def dokumenti_posalji(version_id):
    """Send a draft version to the approval queue."""
    return document_library_views.handle_submit_for_approval(version_id)


@documents_bp.route('/dokumenti/verzija/<int:version_id>/odobri', methods=['POST'])
@login_required
@admin_or_department_head_required
def dokumenti_odobri(version_id):
    """Approve a pending version (self-approval is refused in the view)."""
    return document_library_views.handle_approve_version(version_id)


@documents_bp.route('/dokumenti/verzija/<int:version_id>/odbij', methods=['POST'])
@login_required
@admin_or_department_head_required
def dokumenti_odbij(version_id):
    """Reject a pending version back to draft with a comment."""
    return document_library_views.handle_reject_version(version_id)


@documents_bp.route('/dokumenti/verzija/<int:version_id>/arhiviraj', methods=['POST'])
@login_required
@admin_or_director_required
def dokumenti_arhiviraj(version_id):
    """Manually archive an approved version."""
    return document_library_views.handle_archive_version(version_id)


@documents_bp.route('/dokumenti/fajl/<int:version_id>')
@login_required
@module_access_required('dokumenti')
def dokumenti_fajl(version_id):
    """Serve the file: PDF inline, other formats as attachment."""
    return document_library_views.serve_document_version(version_id)
