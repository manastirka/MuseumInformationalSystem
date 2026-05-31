"""Mineral science API routes extracted from app.py."""

from flask import Blueprint

import mineral_science_views
from security_utils import login_required


mineral_science_bp = Blueprint('mineral_science', __name__)


@mineral_science_bp.route('/api/rruff/mineral/<mineral_name>', methods=['GET'])
@login_required
def api_get_rruff_data(mineral_name):
    """Get RRUFF scientific data for mineral(s) by name."""
    return mineral_science_views.api_get_rruff_data(mineral_name)


@mineral_science_bp.route('/api/cod/search/<mineral_name>', methods=['GET'])
@login_required
def api_cod_search(mineral_name):
    """Search COD for crystal structure data by mineral name."""
    return mineral_science_views.api_cod_search(mineral_name)


@mineral_science_bp.route('/api/cod/cif/<entry_id>', methods=['GET'])
@login_required
def api_cod_get_cif(entry_id):
    """Get CIF file content for a database entry."""
    return mineral_science_views.api_cod_get_cif(entry_id)


@mineral_science_bp.route('/api/crystal/cif', methods=['GET'])
@login_required
def api_crystal_get_cif_by_url():
    """Get CIF file content by direct URL."""
    return mineral_science_views.api_crystal_get_cif_by_url()


@mineral_science_bp.route('/api/crystal/local/<entry_id>', methods=['GET'])
@login_required
def api_crystal_get_local_cif(entry_id):
    """Get CIF file content from local storage or download on demand."""
    return mineral_science_views.api_crystal_get_local_cif(entry_id)


@mineral_science_bp.route('/api/cod/structure/<mineral_name>', methods=['GET'])
@login_required
def api_cod_get_structure(mineral_name):
    """Get complete crystal structure data for a mineral including CIF."""
    return mineral_science_views.api_cod_get_structure(mineral_name)


@mineral_science_bp.route('/api/geochemical/<mineral_name>', methods=['GET'])
@login_required
def api_get_geochemical_data(mineral_name):
    """Get geochemical data for a mineral."""
    return mineral_science_views.api_get_geochemical_data(mineral_name)


@mineral_science_bp.route('/api/local_rruff/<mineral_name>', methods=['GET'])
@login_required
def api_get_local_rruff_data(mineral_name):
    """Get all local RRUFF data for a mineral."""
    return mineral_science_views.api_get_local_rruff_data(mineral_name)


@mineral_science_bp.route('/api/local_rruff/dif/<mineral_name>', methods=['GET'])
@login_required
def api_get_local_rruff_dif(mineral_name):
    """Get DIF crystal structure data for 3D visualization."""
    return mineral_science_views.api_get_local_rruff_dif(mineral_name)


@mineral_science_bp.route('/api/local_rruff/cif/<mineral_name>', methods=['GET'])
@login_required
def api_get_local_rruff_cif(mineral_name):
    """Generate CIF file content from DIF data."""
    return mineral_science_views.api_get_local_rruff_cif(mineral_name)


@mineral_science_bp.route('/api/local_rruff/spectrum/<spectrum_type>/<mineral_name>', methods=['GET'])
@login_required
def api_get_local_rruff_spectrum(spectrum_type, mineral_name):
    """Get Raman or infrared spectrum data for a mineral."""
    return mineral_science_views.api_get_local_rruff_spectrum(spectrum_type, mineral_name)


@mineral_science_bp.route('/api/local_rruff/powder_xy/<mineral_name>', methods=['GET'])
@login_required
def api_get_local_rruff_powder_xy(mineral_name):
    """Get powder diffraction XY profile data."""
    return mineral_science_views.api_get_local_rruff_powder_xy(mineral_name)


@mineral_science_bp.route('/api/local_rruff/image/<path:image_path>')
@login_required
def api_serve_local_rruff_image(image_path):
    """Serve RRUFF image files."""
    return mineral_science_views.api_serve_local_rruff_image(image_path)


@mineral_science_bp.route('/api/local_rruff/microprobe/<mineral_name>', methods=['GET'])
@login_required
def api_get_local_rruff_microprobe(mineral_name):
    """Get microprobe data for a mineral from local RRUFF chemistry files."""
    return mineral_science_views.api_get_local_rruff_microprobe(mineral_name)
