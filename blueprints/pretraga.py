"""Глобална претрага — API за Ctrl+K поље (pretraga.py ради посао)."""
from flask import Blueprint, jsonify, request

import pretraga
from rate_limit_ext import limiter
from security_utils import login_required

pretraga_bp = Blueprint('pretraga', __name__)


@pretraga_bp.route('/api/pretraga')
@login_required
@limiter.limit("120 per minute")
def api_pretraga():
    """JSON: {upit, grupe:[{kljuc, naziv, ikona, stavke:[{naslov, opis, url}], jos}], prekratko}."""
    return jsonify(pretraga.pretrazi(request.args.get('q', '')))
