"""Shared route implementations for biodiversity map views."""

import json
import logging
import os
import time

from flask import jsonify, render_template, request
from psycopg.rows import dict_row
from runtime_lock_utils import load_json_file

from postgres_service import get_postgres_connection

logger = logging.getLogger(__name__)

_bird_ringing_map_cache = None
_bird_ringing_map_cache_time = 0
_locality_geocache = None
_COLLECTION_MAP_WHITELIST = {
    'botany',
    'ornithology',
    'ichthyology',
    'herpetology',
    'entomology',
    'mycology',
}


def render_admin_biodiversity_map():
    """Render the biodiversity map page."""
    return render_template('admin_biodiversity_map.html')


def _get_locality_geocache(app_root):
    """Load locality geocache once."""
    global _locality_geocache
    if _locality_geocache is not None:
        return _locality_geocache

    geocache_path = os.path.join(app_root, 'data', 'locality_geocache.json')
    if os.path.exists(geocache_path):
        try:
            _locality_geocache = load_json_file(geocache_path, default={})
        except Exception:
            _locality_geocache = {}
    else:
        _locality_geocache = {}
    return _locality_geocache


def api_bird_ringing_localities(*, app_root, bird_ringing_database):
    """Serve bird ringing locality data for the biodiversity map."""
    global _bird_ringing_map_cache, _bird_ringing_map_cache_time

    species = request.args.get('species', '').strip() or None
    year = request.args.get('year', '').strip()
    location = request.args.get('location', '').strip() or None

    year_int = None
    if year:
        try:
            year_int = int(year)
        except ValueError:
            pass

    try:
        if not species and not year_int and not location:
            now = time.time()
            if _bird_ringing_map_cache is not None and (now - _bird_ringing_map_cache_time) < 300:
                gps_data = _bird_ringing_map_cache
            else:
                gps_data = bird_ringing_database.get_map_localities()
                _bird_ringing_map_cache = gps_data
                _bird_ringing_map_cache_time = now
        else:
            gps_data = bird_ringing_database.get_map_localities(species, year_int, location)

        for entry in gps_data:
            entry['geocoded'] = False

        no_gps = bird_ringing_database.get_map_localities_no_coords(species, year_int, location)
        gps_location_names = {entry['location'].lower().strip() for entry in gps_data if entry.get('location')}

        geocache = _get_locality_geocache(app_root)
        geocoded_data = []
        for entry in no_gps:
            loc_name = entry.get('location', '')
            cache_key = loc_name.lower().strip()
            if cache_key in gps_location_names:
                continue
            coords = geocache.get(cache_key)
            if not coords or not coords.get('lat') or not coords.get('lon'):
                continue
            entry['latitude'] = coords['lat']
            entry['longitude'] = coords['lon']
            entry['geocoded'] = True
            geocoded_data.append(entry)

        return jsonify({'success': True, 'data': gps_data + geocoded_data})
    except Exception as exc:
        logger.error("Error loading bird ringing localities: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању локалитета прстеновања'}), 500


def api_bird_ringing_filters(*, bird_ringing_database):
    """Return available filter values for the biodiversity map."""
    try:
        species_list = bird_ringing_database.get_all_species()
        years_list = bird_ringing_database.get_all_years()
        locations_list = bird_ringing_database.get_all_locations()
        stats = bird_ringing_database.get_statistics()
        return jsonify(
            {
                'success': True,
                'species': species_list,
                'years': years_list,
                'locations': locations_list,
                'stats': {
                    'total_records': stats.get('total_records', 0),
                    'unique_species': stats.get('unique_species', 0),
                    'unique_locations': stats.get('unique_locations', 0),
                },
            }
        )
    except Exception as exc:
        logger.error("Error loading bird ringing filters: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању филтера'}), 500


def api_collection_localities(
    *,
    app_root,
    botany_collection_database,
    ornithology_collection_database,
    ichthyology_collection_database,
    herpetology_collection_database,
    entomology_collection_database,
    mycology_collection_database,
):
    """Serve collection specimen localities for the biodiversity map."""
    collection_type = request.args.get('type', '').strip().lower()
    if collection_type not in _COLLECTION_MAP_WHITELIST:
        return jsonify({'success': False, 'message': 'Непознат тип збирке'}), 400

    try:
        if os.environ.get('DATABASE_URL'):
            try:
                with get_postgres_connection(row_factory=dict_row) as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            """
                            SELECT
                                catalog_number, scientific_name, common_name_sr,
                                family, conservation_status, location_found,
                                collector, date_collected,
                                ROUND(ST_Y(coordinates::geometry)::numeric, 5) AS latitude,
                                ROUND(ST_X(coordinates::geometry)::numeric, 5) AS longitude
                            FROM collection_specimens
                            WHERE collection_type = %s
                              AND coordinates IS NOT NULL
                            """,
                            (collection_type,),
                        )
                        rows = cur.fetchall()

                data = []
                for row in rows:
                    rec = dict(row)
                    if rec.get('date_collected'):
                        rec['date_collected'] = str(rec['date_collected'])
                    if rec['latitude'] is not None and rec['longitude'] is not None:
                        rec['latitude'] = float(rec['latitude'])
                        rec['longitude'] = float(rec['longitude'])
                        rec['location'] = rec.pop('location_found') or ''
                        data.append(rec)
                if data:
                    return jsonify({'success': True, 'data': data})
            except Exception as exc:
                logger.warning("PostGIS query failed for %s, using fallback: %s", collection_type, exc)

        db_map = {
            'botany': botany_collection_database,
            'ornithology': ornithology_collection_database,
            'ichthyology': ichthyology_collection_database,
            'herpetology': herpetology_collection_database,
            'entomology': entomology_collection_database,
            'mycology': mycology_collection_database,
        }
        collection = db_map.get(collection_type, {})
        specimens = collection.get('specimens', [])
        geocache = _get_locality_geocache(app_root)
        data = []
        for spec in specimens:
            loc_name = spec.get('location_found', '')
            if not loc_name:
                continue
            coords = geocache.get(loc_name.lower().strip())
            if not coords or not coords.get('lat') or not coords.get('lon'):
                continue
            data.append(
                {
                    'location': loc_name,
                    'latitude': coords['lat'],
                    'longitude': coords['lon'],
                    'catalog_number': spec.get('catalog_number', ''),
                    'scientific_name': spec.get('scientific_name', ''),
                    'common_name_sr': spec.get('common_name_sr', ''),
                    'family': spec.get('family', ''),
                    'conservation_status': spec.get('conservation_status', ''),
                    'date_collected': spec.get('date_collected', ''),
                    'collector': spec.get('collector', ''),
                }
            )

        return jsonify({'success': True, 'data': data})
    except Exception as exc:
        logger.error("Error loading collection localities for %s: %s", collection_type, exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању локалитета збирке'}), 500
