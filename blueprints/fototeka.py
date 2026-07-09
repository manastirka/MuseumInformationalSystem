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


@fototeka_bp.route('/fototeka/upload/jedan', methods=['POST'])
@login_required
@module_access_required('fototeka')
def fototeka_upload_jedan():
    """One file at a time (JSON) — the browser sends a multi-select set
    sequentially so no request exceeds the size limit."""
    return fototeka_views.handle_upload_jedan()


@fototeka_bp.route('/fototeka/prijemni-red')
@login_required
@module_access_required('fototeka')
def fototeka_prijemni_red():
    """Curation queue: photos flagged for follow-up (tags/links), oldest first."""
    return fototeka_views.render_prijemni_red()


@fototeka_bp.route('/fototeka/<int:fotografija_id>')
@login_required
@module_access_required('fototeka')
def fototeka_fotografija(fotografija_id):
    """Photo page: metadata, tags, links, processing history."""
    return fototeka_views.render_fotografija(fotografija_id)


@fototeka_bp.route('/fototeka/<int:fotografija_id>/skini-sa-reda', methods=['POST'])
@login_required
@module_access_required('fototeka')
def fototeka_skini_sa_reda(fotografija_id):
    """Clear the reception-queue flag without adding a link."""
    return fototeka_views.handle_skini_sa_reda(fotografija_id)


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


@fototeka_bp.route('/fototeka/<int:fotografija_id>/vidljivost', methods=['POST'])
@login_required
@module_access_required('fototeka')
def fototeka_vidljivost(fotografija_id):
    """Change visibility (javno/privatno); author + admin/director only."""
    return fototeka_views.handle_promeni_vidljivost(fotografija_id)


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


@fototeka_bp.route('/fototeka/<int:fotografija_id>/derivat', methods=['POST'])
@login_required
@module_access_required('fototeka')
def fototeka_prilozi_derivat(fotografija_id):
    """Attach a JPG/PNG preview for a photo with no auto-derivative (RAW)."""
    return fototeka_views.handle_prilozi_derivat(fotografija_id)


@fototeka_bp.route('/fototeka/<int:fotografija_id>/obrisi', methods=['POST'])
@login_required
@admin_required
def fototeka_obrisi(fotografija_id):
    """Soft delete (admin only); the RAW original always stays in the archive."""
    return fototeka_views.handle_obrisi(fotografija_id)


@fototeka_bp.route('/fototeka/uvoz')
@login_required
@admin_required
def fototeka_import():
    """Samba-share import screen (admin/director only)."""
    return fototeka_views.render_import_form()


@fototeka_bp.route('/fototeka/uvoz/skeniraj', methods=['POST'])
@login_required
@admin_required
def fototeka_import_scan():
    """Dry-run preview of the filename-convention classification."""
    return fototeka_views.handle_import_scan()


@fototeka_bp.route('/fototeka/uvoz/potvrdi', methods=['POST'])
@login_required
@admin_required
def fototeka_import_confirm():
    """Intake every scanned file (poreklo='import')."""
    return fototeka_views.handle_import_confirm()


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


@fototeka_bp.route('/fototeka/preuzmi-zip', methods=['POST'])
@login_required
@module_access_required('fototeka')
def fototeka_preuzmi_zip():
    """Download the selected photos as a ZIP (JPG derivative or original)."""
    return fototeka_views.handle_preuzmi_zip()


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


@fototeka_bp.route('/fototeka/api/entitet/fotografije')
@login_required
@module_access_required('fototeka')
def fototeka_api_entitet_fotografije():
    """Photos already linked to an entity (reverse-linking widget load)."""
    return fototeka_views.api_entitet_fotografije()


@fototeka_bp.route('/fototeka/api/entitet/pretraga')
@login_required
@module_access_required('fototeka')
def fototeka_api_entitet_pretraga():
    """Candidate photos to link to an entity."""
    return fototeka_views.api_entitet_pretraga()


@fototeka_bp.route('/fototeka/api/entitet/veza', methods=['POST'])
@login_required
@module_access_required('fototeka')
def fototeka_api_entitet_veza():
    """Link an existing photo to an entity (non-destructive cross-reference)."""
    return fototeka_views.handle_entitet_veza()


@fototeka_bp.route('/fototeka/api/entitet/veza/ukloni', methods=['POST'])
@login_required
@module_access_required('fototeka')
def fototeka_api_entitet_ukloni():
    return fototeka_views.handle_entitet_ukloni()
