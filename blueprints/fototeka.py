"""Фототека routes (самосталне фотографије са таговима и опционим везама)."""

from flask import Blueprint

import fototeka_views
from security_utils import (
    admin_required,
    login_required,
    module_access_required,
)


fototeka_bp = Blueprint('fototeka', __name__)


@fototeka_bp.route('/fototeka')
@login_required
@module_access_required('fototeka')
def fototeka_galerija():
    """Gallery with filters (tag, author, year, link type, search)."""
    return fototeka_views.render_galerija()


@fototeka_bp.route('/fototeka/upload')
@login_required
@module_access_required('fototeka')
def fototeka_upload():
    """Upload form; every employee with module access may add photos."""
    return fototeka_views.render_upload_form()


@fototeka_bp.route('/fototeka/upload', methods=['POST'])
@login_required
@module_access_required('fototeka')
def fototeka_upload_post():
    return fototeka_views.handle_upload()


@fototeka_bp.route('/fototeka/<int:fotografija_id>')
@login_required
@module_access_required('fototeka')
def fototeka_fotografija(fotografija_id):
    """Photo page: metadata, tags, links, processing history."""
    return fototeka_views.render_fotografija(fotografija_id)


@fototeka_bp.route('/fototeka/<int:fotografija_id>/azuriraj', methods=['POST'])
@login_required
@module_access_required('fototeka')
def fototeka_azuriraj(fotografija_id):
    """Description/date/tags; author, heads, director and admin (view checks)."""
    return fototeka_views.handle_azuriraj(fotografija_id)


@fototeka_bp.route('/fototeka/<int:fotografija_id>/veza', methods=['POST'])
@login_required
@module_access_required('fototeka')
def fototeka_dodaj_vezu(fotografija_id):
    return fototeka_views.handle_dodaj_vezu(fotografija_id)


@fototeka_bp.route(
    '/fototeka/<int:fotografija_id>/veza/<tip>/<int:veza_id>/ukloni',
    methods=['POST'],
)
@login_required
@module_access_required('fototeka')
def fototeka_ukloni_vezu(fotografija_id, tip, veza_id):
    return fototeka_views.handle_ukloni_vezu(fotografija_id, tip, veza_id)


@fototeka_bp.route('/fototeka/<int:fotografija_id>/ponovi-obradu', methods=['POST'])
@login_required
@module_access_required('fototeka')
def fototeka_ponovi_obradu(fotografija_id):
    """Re-enqueue derivative processing after a failure."""
    return fototeka_views.handle_ponovi_obradu(fotografija_id)


@fototeka_bp.route('/fototeka/<int:fotografija_id>/obrisi', methods=['POST'])
@login_required
@admin_required
def fototeka_obrisi(fotografija_id):
    """Soft delete (admin only); the RAW original always stays in the archive."""
    return fototeka_views.handle_obrisi(fotografija_id)


@fototeka_bp.route('/fototeka/media/<int:fotografija_id>/<kind>')
@login_required
@module_access_required('fototeka')
def fototeka_media(fotografija_id, kind):
    """Serve a derivative ('jpg' ~2500px or 'thumb' ~300px); placeholder
    while processing is still running."""
    return fototeka_views.serve_derivat(fotografija_id, kind)


@fototeka_bp.route('/fototeka/raw/<int:fotografija_id>')
@login_required
@module_access_required('fototeka')
def fototeka_raw(fotografija_id):
    """Download the untouched RAW original as an attachment."""
    return fototeka_views.serve_raw(fotografija_id)


@fototeka_bp.route('/fototeka/api/tagovi')
@login_required
@module_access_required('fototeka')
def fototeka_api_tagovi():
    return fototeka_views.api_tagovi()


@fototeka_bp.route('/fototeka/api/predmeti')
@login_required
@module_access_required('fototeka')
def fototeka_api_predmeti():
    return fototeka_views.api_predmeti()
