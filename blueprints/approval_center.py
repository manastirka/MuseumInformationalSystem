"""Unified approval center routes (Центар за одобравање и Архива)."""

from flask import Blueprint

import approval_center_views
from security_utils import admin_or_department_head_required, login_required


approval_center_bp = Blueprint('approval_center', __name__)


@approval_center_bp.after_request
def _disable_caching(response):
    """Decision pages must never come back stale from the cache or bfcache
    (same hardening as the vehicle reservations list): a cached queue makes
    an already-decided request look pending again."""
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@approval_center_bp.route('/odobravanje')
@login_required
@admin_or_department_head_required
def centar_odobravanje():
    """Requests and document versions waiting on the caller, in tabs."""
    return approval_center_views.render_approval_center()


@approval_center_bp.route('/arhiva')
@login_required
def arhiva():
    """Read-only archive of processed requests and archived documents."""
    return approval_center_views.render_archive_center()
