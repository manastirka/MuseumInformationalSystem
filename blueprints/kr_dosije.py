"""Конзерваторско-рестаураторски досије — routes.

Логика је у `kr_dosije_views.py`; овде само рутирање и капије приступа
(`module_access_required('kr_dosije')` + `login_required`).
"""

from flask import Blueprint

import kr_dosije_views
from security_utils import login_required, module_access_required


kr_dosije_bp = Blueprint('kr_dosije', __name__)

_GATE = module_access_required('kr_dosije')


@kr_dosije_bp.route('/kr-dosije')
@login_required
@_GATE
def lista():
    return kr_dosije_views.render_lista()


@kr_dosije_bp.route('/kr-dosije/novi', methods=['GET', 'POST'])
@login_required
@_GATE
def novi():
    from flask import request
    if request.method == 'POST':
        return kr_dosije_views.handle_create()
    return kr_dosije_views.render_forma()


@kr_dosije_bp.route('/kr-dosije/<int:dosije_id>')
@login_required
@_GATE
def detalj(dosije_id):
    return kr_dosije_views.render_detalj(dosije_id)


@kr_dosije_bp.route('/kr-dosije/<int:dosije_id>/izmena', methods=['GET', 'POST'])
@login_required
@_GATE
def izmena(dosije_id):
    from flask import request
    if request.method == 'POST':
        return kr_dosije_views.handle_update(dosije_id)
    return kr_dosije_views.render_forma(dosije_id)


@kr_dosije_bp.route('/kr-dosije/<int:dosije_id>/brisanje', methods=['POST'])
@login_required
@_GATE
def brisanje(dosije_id):
    return kr_dosije_views.handle_delete(dosije_id)


@kr_dosije_bp.route('/kr-dosije/<int:dosije_id>/pdf')
@login_required
@_GATE
def pdf(dosije_id):
    return kr_dosije_views.handle_pdf(dosije_id)


# --- фотографије по фази ---
@kr_dosije_bp.route('/kr-dosije/<int:dosije_id>/foto', methods=['POST'])
@login_required
@_GATE
def foto_upload(dosije_id):
    return kr_dosije_views.handle_foto_upload(dosije_id)


@kr_dosije_bp.route('/kr-dosije/<int:dosije_id>/foto/<int:veza_id>/ukloni',
                    methods=['POST'])
@login_required
@_GATE
def foto_ukloni(dosije_id, veza_id):
    return kr_dosije_views.handle_foto_detach(dosije_id, veza_id)


# --- autocomplete предмета ---
@kr_dosije_bp.route('/kr-dosije/api/predmet')
@login_required
@_GATE
def api_predmet():
    return kr_dosije_views.api_predmet_search()


# --- предлошци поступака (CRUD) ---
@kr_dosije_bp.route('/kr-dosije/predlosci')
@login_required
@_GATE
def predlosci():
    return kr_dosije_views.render_predlosci()


@kr_dosije_bp.route('/kr-dosije/api/predlosci')
@login_required
@_GATE
def api_predlosci():
    return kr_dosije_views.api_predlosci()


@kr_dosije_bp.route('/kr-dosije/predlosci/novi', methods=['POST'])
@login_required
@_GATE
def predlozak_novi():
    return kr_dosije_views.handle_predlozak_create()


@kr_dosije_bp.route('/kr-dosije/predlosci/<int:predlozak_id>/izmena', methods=['POST'])
@login_required
@_GATE
def predlozak_izmena(predlozak_id):
    return kr_dosije_views.handle_predlozak_update(predlozak_id)


@kr_dosije_bp.route('/kr-dosije/predlosci/<int:predlozak_id>/brisanje', methods=['POST'])
@login_required
@_GATE
def predlozak_brisanje(predlozak_id):
    return kr_dosije_views.handle_predlozak_delete(predlozak_id)
