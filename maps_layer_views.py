"""Shared route implementations for map pages and JSON-backed map layers."""

import json
import logging
import os

from flask import jsonify, render_template, send_file

logger = logging.getLogger(__name__)

_ore_deposits_cache = None
_stratigraphy_cache = None
_paleo_localities_cache = None
_mining_operations_cache = None
_exploration_licenses_cache = None
_geo_sheets_cache = None
_sanja_mammals_localities_cache = None


def render_admin_maps():
    """Render the interactive geological map page."""
    return render_template('admin_maps.html')


def render_admin_geological_timeline():
    """Render the geological timeline page."""
    return render_template('admin_geological_timeline.html')


def _load_json_cached(cache_name, file_path):
    """Load read-only map JSON into a module-level cache and return it.

    These map datasets are static layer sources. Avoid runtime lock sidecars here:
    production serves this code as a restricted user that can read data/*.json
    but must not need write permission to create hidden .*.lock files.
    """
    global _ore_deposits_cache
    global _stratigraphy_cache
    global _paleo_localities_cache
    global _mining_operations_cache
    global _exploration_licenses_cache
    global _geo_sheets_cache
    global _sanja_mammals_localities_cache

    cache_value = globals()[cache_name]
    if cache_value is None:
        if not os.path.exists(file_path):
            cache_value = []
        else:
            with open(file_path, 'r', encoding='utf-8') as handle:
                cache_value = json.load(handle)
        globals()[cache_name] = cache_value
    return cache_value


def api_ore_deposits(app_root):
    """Serve ore deposit data from JSON."""
    try:
        data = _load_json_cached(
            '_ore_deposits_cache',
            os.path.join(app_root, 'data', 'ore_deposits.json'),
        )
        return jsonify({'success': True, 'data': data})
    except Exception as exc:
        logger.error("Error loading ore deposits: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању рудних лежишта'}), 500


def api_stratigraphy_localities(app_root):
    """Serve stratigraphy locality data from JSON."""
    try:
        data = _load_json_cached(
            '_stratigraphy_cache',
            os.path.join(app_root, 'data', 'stratigraphy_localities.json'),
        )
        return jsonify({'success': True, 'data': data})
    except Exception as exc:
        logger.error("Error loading stratigraphy localities: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању стратиграфских локалитета'}), 500


def api_paleo_localities(app_root):
    """Serve paleontological locality data from JSON."""
    try:
        data = _load_json_cached(
            '_paleo_localities_cache',
            os.path.join(app_root, 'data', 'paleo_localities.json'),
        )
        return jsonify({'success': True, 'data': data})
    except Exception as exc:
        logger.error("Error loading paleontological localities: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању палеонтолошких локалитета'}), 500


def api_mining_operations(app_root):
    """Serve mining operations data from JSON."""
    try:
        data = _load_json_cached(
            '_mining_operations_cache',
            os.path.join(app_root, 'data', 'mining_operations_serbia.json'),
        )
        return jsonify({'success': True, 'data': data})
    except Exception as exc:
        logger.error("Error loading mining operations: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању рударских операција'}), 500


def api_exploration_licenses(app_root):
    """Serve exploration license data from JSON."""
    try:
        data = _load_json_cached(
            '_exploration_licenses_cache',
            os.path.join(app_root, 'data', 'exploration_licenses_map.json'),
        )
        return jsonify({'success': True, 'data': data})
    except Exception as exc:
        logger.error("Error loading exploration licenses: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању истражних лиценци'}), 500


def _get_geological_sheets(app_root):
    """Return geological map sheet metadata."""
    return _load_json_cached(
        '_geo_sheets_cache',
        os.path.join(app_root, 'data', 'geological_map_sheets.json'),
    )


def api_geological_sheets(app_root):
    """Serve geological map sheet metadata."""
    try:
        return jsonify({'success': True, 'data': _get_geological_sheets(app_root)})
    except Exception as exc:
        logger.error("Error loading geological sheets: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању листова карте'}), 500


def api_sanja_mammals_localities(app_root):
    """Serve Sanja mammals locality data enriched with linked specimens.

    Each locality gets a ``specimens`` array built by matching the first
    3 digits of each specimen's ``catalog_number`` to the locality ``code``.
    """
    try:
        localities = _load_json_cached(
            '_sanja_mammals_localities_cache',
            os.path.join(app_root, 'Sanja', 'sanja_mammals_localities.json'),
        )

        # Build a code→specimens index from the live Sanja database.
        import app as museum_app
        db = museum_app.SANJA_PALEOGENE_NEOGENE_MAMMALS_DATABASE
        specimens = db.get('specimens', [])

        from collections import defaultdict
        by_code = defaultdict(list)
        for s in specimens:
            cn = (s.get('catalog_number') or '').strip()
            if len(cn) >= 3:
                by_code[cn[:3]].append({
                    'id': s.get('id'),
                    'catalog_number': cn,
                    'specimen_name': s.get('specimen_name', ''),
                    'material': s.get('material', ''),
                    'identified_by': s.get('identified_by', ''),
                    'description': s.get('description', ''),
                    'location_found': s.get('location_found', ''),
                    'quantity': s.get('quantity', ''),
                    'uncertain_determination': s.get('uncertain_determination', ''),
                })

        result = []
        for loc in localities:
            code = loc.get('code', '')
            entry = dict(loc)
            entry['specimens'] = by_code.get(code, [])
            entry['specimen_count'] = len(entry['specimens'])
            result.append(entry)

        return jsonify({'success': True, 'data': result})
    except Exception as exc:
        logger.error("Error loading Sanja mammals localities: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању локалитета крупних сисара'}), 500


def api_geological_sheet_image(folder_name, image_type, app_root):
    """Serve individual JPG images from geological map sheet folders."""
    if image_type not in ('karta', 'legenda', 'profili', 'stub'):
        return jsonify({'success': False, 'message': 'Непознат тип слике'}), 400
    if '..' in folder_name or '/' in folder_name or '\\' in folder_name:
        return jsonify({'success': False, 'message': 'Неважећи назив фасцикле'}), 400

    try:
        sheets = _get_geological_sheets(app_root)
    except Exception:
        return jsonify({'success': False, 'message': 'Грешка при учитавању података'}), 500

    sheet = next((item for item in sheets if item['folder'] == folder_name), None)
    if not sheet:
        return jsonify({'success': False, 'message': 'Лист карте није пронађен'}), 404
    if image_type not in sheet.get('files', {}):
        return jsonify({'success': False, 'message': 'Слика није доступна за овај лист'}), 404

    filename = sheet['files'][image_type]
    file_path = os.path.join(app_root, 'Karte', 'Final - Srbija', folder_name, filename)
    if not os.path.isfile(file_path):
        return jsonify({'success': False, 'message': 'Датотека није пронађена'}), 404

    return send_file(file_path, mimetype='image/jpeg', max_age=86400)


def api_geological_sheet_tumac(folder_name, app_root):
    """Serve tumac PDF/DOC file for a geological map sheet."""
    if '..' in folder_name or '/' in folder_name or '\\' in folder_name:
        return jsonify({'success': False, 'message': 'Неважећи назив'}), 400

    try:
        sheets = _get_geological_sheets(app_root)
    except Exception:
        return jsonify({'success': False, 'message': 'Грешка при учитавању'}), 500

    sheet = next((item for item in sheets if item['folder'] == folder_name), None)
    if not sheet or 'tumac' not in sheet:
        return jsonify({'success': False, 'message': 'Тумач није пронађен'}), 404

    tumac_file = sheet['tumac']['tumac_file']
    file_path = os.path.join(app_root, 'Karte', 'Tumaci Srbija', tumac_file)
    if not os.path.isfile(file_path):
        return jsonify({'success': False, 'message': 'Датотека није пронађена'}), 404

    mimetype = 'application/pdf' if tumac_file.lower().endswith('.pdf') else 'application/msword'
    return send_file(file_path, mimetype=mimetype, max_age=86400)
