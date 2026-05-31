"""Read-only map routes extracted from app.py."""

import os
import sys

from flask import Blueprint, current_app

import maps_biodiversity_views
import maps_field_data_views
import maps_geo_zone_views
import maps_layer_views
import maps_profile_views
import maps_terrain_views
from security_utils import admin_required, login_required, module_access_required


maps_bp = Blueprint('maps', __name__)


def _app_root():
    """Return the MuseumInfoSystem application root for map data files."""
    return current_app.root_path


def _museum_app_module():
    """Return the already-loaded MuseumInfoSystem app module without importing by name.

    Running ``python app.py`` loads this project as ``__main__``. Importing
    ``app`` inside a route can instead resolve to the nested PrirodnjackiMuzej
    package because app.py extends sys.path. That breaks map APIs with 500s.
    """
    for module_name in ('app', '__main__'):
        module = sys.modules.get(module_name)
        if module is not None and hasattr(module, '_build_tile_index'):
            return module
    raise RuntimeError('MuseumInfoSystem app module is not loaded')


@maps_bp.route('/admin/maps')
@module_access_required('maps_karte')
def admin_maps():
    """Interactive geological map of Serbia."""
    return maps_layer_views.render_admin_maps()


@maps_bp.route('/admin/geological-timeline')
@module_access_required('maps_karte')
def admin_geological_timeline():
    """Animated geological/tectonic timeline of the Balkans."""
    return maps_layer_views.render_admin_geological_timeline()


@maps_bp.route('/api/map/balkans-terrain')
@login_required
def api_balkans_terrain():
    """Full Serbia DEM at reduced resolution for geological timeline 3D view."""
    museum_app = _museum_app_module()

    return maps_terrain_views.api_balkans_terrain(
        dem_dir=museum_app._DEM_DIR,
    )


@maps_bp.route('/api/map/tile-index')
@login_required
def api_map_tile_index():
    """Return JSON tile index (zoom levels + bounds)."""
    museum_app = _museum_app_module()

    return maps_terrain_views.api_map_tile_index(
        build_tile_index=museum_app._build_tile_index,
    )


@maps_bp.route('/api/map/tile/<filename>')
@login_required
def api_map_tile(filename):
    """Serve individual tile PNG (extract from KMZ on first request, cache)."""
    museum_app = _museum_app_module()

    return maps_terrain_views.api_map_tile(
        filename=filename,
        extract_tile_to_cache=museum_app._extract_tile_to_cache,
        tile_cache_dir=museum_app._TILE_CACHE_DIR,
    )


@maps_bp.route('/api/map/3d-terrain')
@login_required
def api_map_3d_terrain():
    """Return elevation grid + geological texture for 3D terrain rendering."""
    museum_app = _museum_app_module()

    return maps_terrain_views.api_map_3d_terrain(
        dem_dir=museum_app._DEM_DIR,
        build_tile_index=museum_app._build_tile_index,
        extract_tile_to_cache=museum_app._extract_tile_to_cache,
    )


@maps_bp.route('/api/map/field-data', methods=['POST'])
@login_required
def api_create_field_data():
    """Create a new geological field observation."""
    return maps_field_data_views.api_create_field_data()


@maps_bp.route('/api/map/field-data', methods=['GET'])
@login_required
def api_list_field_data():
    """List all geological field observations, with optional bounding box filter."""
    return maps_field_data_views.api_list_field_data()


@maps_bp.route('/api/map/field-data/<int:item_id>', methods=['GET'])
@login_required
def api_get_field_data(item_id):
    """Get a single field observation with images."""
    museum_app = _museum_app_module()

    return maps_field_data_views.api_get_field_data(
        item_id,
        image_storage_factory=museum_app.get_image_storage,
    )


@maps_bp.route('/api/map/field-data/<int:item_id>', methods=['PUT'])
@login_required
def api_update_field_data(item_id):
    """Update a field observation (owner or admin only)."""
    return maps_field_data_views.api_update_field_data(item_id)


@maps_bp.route('/api/map/field-data/<int:item_id>', methods=['DELETE'])
@login_required
def api_delete_field_data(item_id):
    """Delete a field observation (owner or admin only)."""
    museum_app = _museum_app_module()

    return maps_field_data_views.api_delete_field_data(
        item_id,
        image_storage_factory=museum_app.get_image_storage,
    )


@maps_bp.route('/api/map/ore-deposits')
@login_required
def api_ore_deposits():
    """Serve ore deposit data from JSON for the map layer."""
    return maps_layer_views.api_ore_deposits(_app_root())


@maps_bp.route('/api/map/stratigraphy')
@login_required
def api_stratigraphy_localities():
    """Serve stratigraphy locality data from JSON for the map layer."""
    return maps_layer_views.api_stratigraphy_localities(_app_root())


@maps_bp.route('/api/map/paleontology')
@login_required
def api_paleo_localities():
    """Serve paleontological locality data from JSON for the map layer."""
    return maps_layer_views.api_paleo_localities(_app_root())


@maps_bp.route('/api/map/mining-operations')
@login_required
def api_mining_operations():
    """Serve mining operations data from JSON for the map layer."""
    return maps_layer_views.api_mining_operations(_app_root())


@maps_bp.route('/api/map/exploration-licenses')
@login_required
def api_exploration_licenses():
    """Serve exploration license data from JSON for the map layer."""
    return maps_layer_views.api_exploration_licenses(_app_root())


@maps_bp.route('/api/map/sanja-mammals-localities')
@login_required
def api_sanja_mammals_localities():
    """Serve Sanja mammals locality + specimen data for the map layer."""
    return maps_layer_views.api_sanja_mammals_localities(_app_root())


@maps_bp.route('/api/map/geological-sheets')
@login_required
def api_geological_sheets():
    """Serve geological map sheet metadata (bounds, files) for the map layer."""
    return maps_layer_views.api_geological_sheets(_app_root())


@maps_bp.route('/api/map/geological-sheet-image/<folder_name>/<image_type>')
@login_required
def api_geological_sheet_image(folder_name, image_type):
    """Serve individual JPG images from OGK map sheet folders."""
    return maps_layer_views.api_geological_sheet_image(
        folder_name,
        image_type,
        _app_root(),
    )


@maps_bp.route('/api/map/geological-sheet-tumac/<folder_name>')
@login_required
def api_geological_sheet_tumac(folder_name):
    """Serve tumac PDF/DOC file for a geological map sheet."""
    return maps_layer_views.api_geological_sheet_tumac(
        folder_name,
        _app_root(),
    )


@maps_bp.route('/api/map/elevation')
@login_required
def api_map_elevation():
    """Return terrain elevation for a single lat/lon point."""
    museum_app = _museum_app_module()

    return maps_profile_views.api_map_elevation(
        sample_elevation_at_point=museum_app._sample_elevation_at_point,
    )


@maps_bp.route('/api/map/cross-profile')
@login_required
def api_map_cross_profile():
    """Generate a cross-section profile between two points with elevation and geology."""
    museum_app = _museum_app_module()

    return maps_profile_views.api_map_cross_profile(
        app_root=_app_root(),
        haversine=museum_app._haversine_py,
        batch_sample_elevations=museum_app._batch_sample_elevations,
        interpolate_subsurface=museum_app._interpolate_subsurface,
    )


@maps_bp.route('/api/map/digitized-profiles')
@login_required
def api_digitized_profiles_list():
    """List all digitized cross-section profiles."""
    museum_app = _museum_app_module()

    return maps_profile_views.api_digitized_profiles_list(
        profiles_path=museum_app._DIGITIZED_PROFILES_PATH,
    )


@maps_bp.route('/api/map/digitized-profiles/<profile_id>')
@login_required
def api_digitized_profile_get(profile_id):
    """Get a single digitized profile with full layer data."""
    museum_app = _museum_app_module()

    return maps_profile_views.api_digitized_profile_get(
        profile_id,
        profiles_path=museum_app._DIGITIZED_PROFILES_PATH,
    )


@maps_bp.route('/api/map/digitized-profiles', methods=['POST'])
@login_required
def api_digitized_profile_create():
    """Create a new digitized profile."""
    museum_app = _museum_app_module()

    return maps_profile_views.api_digitized_profile_create(
        profiles_path=museum_app._DIGITIZED_PROFILES_PATH,
    )


@maps_bp.route('/api/map/digitized-profiles/<profile_id>', methods=['PUT'])
@login_required
def api_digitized_profile_update(profile_id):
    """Update an existing digitized profile."""
    museum_app = _museum_app_module()

    return maps_profile_views.api_digitized_profile_update(
        profile_id,
        profiles_path=museum_app._DIGITIZED_PROFILES_PATH,
    )


@maps_bp.route('/api/map/digitized-profiles/<profile_id>', methods=['DELETE'])
@login_required
def api_digitized_profile_delete(profile_id):
    """Delete a digitized profile."""
    museum_app = _museum_app_module()

    return maps_profile_views.api_digitized_profile_delete(
        profile_id,
        profiles_path=museum_app._DIGITIZED_PROFILES_PATH,
    )


@maps_bp.route('/api/map/geo-zones/<folder_name>/zone-map')
@login_required
def api_geo_zone_map(folder_name):
    """Serve pre-computed zone group map PNG for a geological sheet."""
    return maps_geo_zone_views.api_geo_zone_map(
        folder_name,
        app_root=_app_root(),
    )


@maps_bp.route('/api/map/geo-zones/<folder_name>/metadata')
@login_required
def api_geo_zone_metadata(folder_name):
    """Serve zone groups metadata JSON for a geological sheet."""
    return maps_geo_zone_views.api_geo_zone_metadata(
        folder_name,
        app_root=_app_root(),
    )


@maps_bp.route('/api/map/geo-zones/<folder_name>/legend')
@login_required
def api_geo_zone_legend(folder_name):
    """Serve enhanced legend JSON for a geological sheet."""
    return maps_geo_zone_views.api_geo_zone_legend(
        folder_name,
        app_root=_app_root(),
    )


@maps_bp.route('/api/map/geo-zones/process', methods=['POST'])
@admin_required
def api_geo_zone_process():
    """Admin: trigger zone map processing for a sheet or all sheets."""
    return maps_geo_zone_views.api_geo_zone_process(
        app_root=_app_root(),
    )


@maps_bp.route('/api/map/geo-zones/<folder_name>/legend', methods=['POST'])
@admin_required
def api_geo_zone_legend_update(folder_name):
    """Admin: update enhanced legend with unit code assignments."""
    return maps_geo_zone_views.api_geo_zone_legend_update(
        folder_name,
        app_root=_app_root(),
    )


@maps_bp.route('/api/map/geo-zones/<folder_name>/calibration')
@login_required
def api_geo_manual_calibration_get(folder_name):
    """Load manual color calibration for a geological sheet."""
    return maps_geo_zone_views.api_geo_manual_calibration_get(
        folder_name,
        app_root=_app_root(),
    )


@maps_bp.route('/api/map/geo-zones/<folder_name>/calibration', methods=['POST'])
@admin_required
def api_geo_manual_calibration_save(folder_name):
    """Save manual color calibration for a geological sheet."""
    return maps_geo_zone_views.api_geo_manual_calibration_save(
        folder_name,
        app_root=_app_root(),
    )


@maps_bp.route('/api/map/geo-zones/<folder_name>/calibration/entry', methods=['PATCH'])
@admin_required
def api_geo_manual_calibration_patch_entry(folder_name):
    """Update or add a single calibration entry by color match."""
    return maps_geo_zone_views.api_geo_manual_calibration_patch_entry(
        folder_name,
        app_root=_app_root(),
    )


@maps_bp.route('/api/map/geo-zones/<folder_name>/calibration', methods=['DELETE'])
@admin_required
def api_geo_manual_calibration_delete(folder_name):
    """Delete manual calibration for a geological sheet (reset)."""
    return maps_geo_zone_views.api_geo_manual_calibration_delete(
        folder_name,
        app_root=_app_root(),
    )


@maps_bp.route('/admin/biodiversity-map')
@module_access_required('biodiversity_map')
def admin_biodiversity_map():
    """Interactive biodiversity map of Serbia — bird ringing localities."""
    return maps_biodiversity_views.render_admin_biodiversity_map()


@maps_bp.route('/api/map/bird-ringing-localities')
@login_required
def api_bird_ringing_localities():
    """Serve bird ringing locality data for the biodiversity map layer."""
    museum_app = _museum_app_module()

    return maps_biodiversity_views.api_bird_ringing_localities(
        app_root=_app_root(),
        bird_ringing_database=museum_app.bird_ringing_database,
    )


@maps_bp.route('/api/map/bird-ringing-filters')
@login_required
def api_bird_ringing_filters():
    """Return available filter values for the biodiversity map."""
    museum_app = _museum_app_module()

    return maps_biodiversity_views.api_bird_ringing_filters(
        bird_ringing_database=museum_app.bird_ringing_database,
    )


@maps_bp.route('/api/map/collection-localities')
@login_required
def api_collection_localities():
    """Serve collection specimen localities for the biodiversity map."""
    museum_app = _museum_app_module()

    return maps_biodiversity_views.api_collection_localities(
        app_root=_app_root(),
        botany_collection_database=museum_app.BOTANY_COLLECTION_DATABASE,
        ornithology_collection_database=museum_app.ORNITHOLOGY_COLLECTION_DATABASE,
        ichthyology_collection_database=museum_app.ICHTHYOLOGY_COLLECTION_DATABASE,
        herpetology_collection_database=museum_app.HERPETOLOGY_COLLECTION_DATABASE,
        entomology_collection_database=museum_app.ENTOMOLOGY_COLLECTION_DATABASE,
        mycology_collection_database=museum_app.MYCOLOGY_COLLECTION_DATABASE,
    )
