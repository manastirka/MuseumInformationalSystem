"""Shared route implementations for geological zone map endpoints."""

import json
import logging
import os
from datetime import datetime

from flask import jsonify, request, send_file

logger = logging.getLogger(__name__)


def _is_invalid_folder_name(folder_name):
    """Reject path traversal in geological sheet folder names."""
    return '..' in folder_name or '/' in folder_name or '\\' in folder_name


def _load_geological_sheets(app_root):
    """Load geological sheet metadata from disk."""
    sheets_path = os.path.join(app_root, 'data', 'geological_map_sheets.json')
    with open(sheets_path, 'r', encoding='utf-8') as handle:
        return json.load(handle)


def api_geo_zone_map(folder_name, *, app_root):
    """Serve pre-computed zone group map PNG for a geological sheet."""
    if _is_invalid_folder_name(folder_name):
        return jsonify({'success': False, 'message': 'Неважећи назив'}), 400

    file_path = os.path.join(app_root, 'data', 'geo_zones', folder_name, 'zone_group_map.png')
    if not os.path.isfile(file_path):
        return jsonify({'success': False, 'message': 'Зонска карта није доступна'}), 404

    return send_file(file_path, mimetype='image/png', max_age=86400)


def api_geo_zone_metadata(folder_name, *, app_root):
    """Serve zone groups metadata JSON for a geological sheet."""
    if _is_invalid_folder_name(folder_name):
        return jsonify({'success': False, 'message': 'Неважећи назив'}), 400

    file_path = os.path.join(app_root, 'data', 'geo_zones', folder_name, 'zone_groups_meta.json')
    if not os.path.isfile(file_path):
        return jsonify({'success': False, 'message': 'Метаподаци нису доступни'}), 404

    try:
        with open(file_path, 'r', encoding='utf-8') as handle:
            data = json.load(handle)
        return jsonify({'success': True, 'data': data})
    except Exception as exc:
        logger.error("Error loading zone metadata for %s: %s", folder_name, exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању'}), 500


def api_geo_zone_legend(folder_name, *, app_root):
    """Serve enhanced legend JSON for a geological sheet."""
    if _is_invalid_folder_name(folder_name):
        return jsonify({'success': False, 'message': 'Неважећи назив'}), 400

    file_path = os.path.join(app_root, 'data', 'geo_zones', folder_name, 'enhanced_legend.json')
    if not os.path.isfile(file_path):
        return jsonify({'success': False, 'message': 'Легенда није доступна'}), 404

    try:
        with open(file_path, 'r', encoding='utf-8') as handle:
            data = json.load(handle)
        return jsonify({'success': True, 'data': data})
    except Exception as exc:
        logger.error("Error loading enhanced legend for %s: %s", folder_name, exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању'}), 500


def api_geo_zone_process(*, app_root):
    """Trigger zone map processing for a sheet."""
    import geo_zone_processor

    folder = request.json.get('folder') if request.is_json else request.form.get('folder')
    force = (
        request.json.get('force', False)
        if request.is_json
        else request.form.get('force', 'false').lower() == 'true'
    )

    if not folder:
        return jsonify({'success': False, 'message': 'Потребан је назив фасцикле (folder)'}), 400
    if _is_invalid_folder_name(folder):
        return jsonify({'success': False, 'message': 'Неважећи назив фасцикле'}), 400

    try:
        sheets = _load_geological_sheets(app_root)
    except Exception:
        return jsonify({'success': False, 'message': 'Грешка при учитавању'}), 500

    sheet_data = next((sheet for sheet in sheets if sheet['folder'] == folder), None)
    result = geo_zone_processor.process_sheet(folder, sheet_data=sheet_data, force=force)
    if result and result.get('status') in ('ok', 'exists'):
        return jsonify({'success': True, 'data': result})
    return jsonify({'success': False, 'message': 'Обрада неуспешна', 'data': result}), 500


def api_geo_zone_legend_update(folder_name, *, app_root):
    """Update enhanced legend with unit code assignments."""
    if _is_invalid_folder_name(folder_name):
        return jsonify({'success': False, 'message': 'Неважећи назив'}), 400

    legend_dir = os.path.join(app_root, 'data', 'geo_zones', folder_name)
    legend_path = os.path.join(legend_dir, 'enhanced_legend.json')
    if not os.path.isfile(legend_path):
        return jsonify({'success': False, 'message': 'Легенда није пронађена'}), 404

    try:
        updates = request.get_json()
        if not updates or 'swatches' not in updates:
            return jsonify({'success': False, 'message': 'Недостају подаци'}), 400

        with open(legend_path, 'r', encoding='utf-8') as handle:
            legend = json.load(handle)

        for update in updates['swatches']:
            idx = update.get('band_index')
            if idx is not None and 0 <= idx < len(legend):
                for key in ('unit_code', 'unit_name_sr', 'unit_name_en', 'era', 'pattern'):
                    if key in update:
                        legend[idx][key] = update[key]

        with open(legend_path, 'w', encoding='utf-8') as handle:
            json.dump(legend, handle, ensure_ascii=False, indent=2)

        return jsonify({'success': True, 'message': 'Легенда ажурирана'})
    except Exception as exc:
        logger.error("Error updating legend for %s: %s", folder_name, exc)
        return jsonify({'success': False, 'message': 'Грешка при чувању'}), 500


def api_geo_manual_calibration_get(folder_name, *, app_root):
    """Load manual color calibration for a geological sheet."""
    if _is_invalid_folder_name(folder_name):
        return jsonify({'success': False, 'message': 'Неважећи назив'}), 400

    file_path = os.path.join(app_root, 'data', 'geo_zones', folder_name, 'manual_calibration.json')
    if not os.path.isfile(file_path):
        return jsonify({'success': True, 'data': None})

    try:
        with open(file_path, 'r', encoding='utf-8') as handle:
            data = json.load(handle)
        return jsonify({'success': True, 'data': data})
    except Exception as exc:
        logger.error("Error loading manual calibration for %s: %s", folder_name, exc)
        return jsonify({'success': False, 'message': 'Грешка при учитавању'}), 500


def api_geo_manual_calibration_save(folder_name, *, app_root):
    """Save manual color calibration for a geological sheet."""
    if _is_invalid_folder_name(folder_name):
        return jsonify({'success': False, 'message': 'Неважећи назив'}), 400

    cal_dir = os.path.join(app_root, 'data', 'geo_zones', folder_name)
    if not os.path.isdir(cal_dir):
        return jsonify({'success': False, 'message': 'Фасцикла не постоји'}), 404

    try:
        payload = request.get_json()
        if not payload or 'entries' not in payload:
            return jsonify({'success': False, 'message': 'Недостају подаци'}), 400

        data = {
            'folder': folder_name,
            'calibrated_at': datetime.now().isoformat(),
            'entries': payload['entries'],
        }
        cal_path = os.path.join(cal_dir, 'manual_calibration.json')
        with open(cal_path, 'w', encoding='utf-8') as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)

        return jsonify(
            {
                'success': True,
                'message': 'Калибрација сачувана',
                'count': len(payload['entries']),
            }
        )
    except Exception as exc:
        logger.error("Error saving manual calibration for %s: %s", folder_name, exc)
        return jsonify({'success': False, 'message': 'Грешка при чувању'}), 500


def api_geo_manual_calibration_patch_entry(folder_name, *, app_root):
    """Update or add a single calibration entry by color match."""
    if _is_invalid_folder_name(folder_name):
        return jsonify({'success': False, 'message': 'Неважећи назив'}), 400

    cal_dir = os.path.join(app_root, 'data', 'geo_zones', folder_name)
    cal_path = os.path.join(cal_dir, 'manual_calibration.json')

    try:
        payload = request.get_json()
        if not payload or 'color' not in payload:
            return jsonify({'success': False, 'message': 'Недостају подаци'}), 400

        data = {'folder': folder_name, 'entries': []}
        if os.path.isfile(cal_path):
            with open(cal_path, 'r', encoding='utf-8') as handle:
                data = json.load(handle)

        entries = data.get('entries', [])
        new_entry = payload

        def hsv_dist(h1, s1, v1, h2, s2, v2):
            dh = abs(h1 - h2)
            if dh > 180:
                dh = 360 - dh
            return ((dh / 180) ** 2 + ((s1 - s2) / 100) ** 2 + ((v1 - v2) / 100) ** 2) ** 0.5

        hsv = new_entry.get('hsv', [0, 0, 0])
        best_idx = -1
        best_dist = 999
        for idx, entry in enumerate(entries):
            existing_hsv = entry.get('hsv', [0, 0, 0])
            dist = hsv_dist(hsv[0], hsv[1], hsv[2], existing_hsv[0], existing_hsv[1], existing_hsv[2])
            if dist < best_dist:
                best_dist = dist
                best_idx = idx

        if best_dist < 0.15 and best_idx >= 0:
            entry_id = entries[best_idx].get('id', best_idx + 1)
            entries[best_idx] = {
                'id': entry_id,
                'color': new_entry['color'],
                'hsv': new_entry['hsv'],
                'unit_code': new_entry.get('unit_code', ''),
                'unit_name_sr': new_entry.get('unit_name_sr', ''),
                'unit_name_en': new_entry.get('unit_name_en', ''),
                'era': new_entry.get('era', ''),
                'era_color': new_entry.get('era_color', '#9e9e9e'),
            }
            action = 'updated'
        else:
            max_id = max((entry.get('id', 0) for entry in entries), default=0)
            entries.append(
                {
                    'id': max_id + 1,
                    'color': new_entry['color'],
                    'hsv': new_entry['hsv'],
                    'unit_code': new_entry.get('unit_code', ''),
                    'unit_name_sr': new_entry.get('unit_name_sr', ''),
                    'unit_name_en': new_entry.get('unit_name_en', ''),
                    'era': new_entry.get('era', ''),
                    'era_color': new_entry.get('era_color', '#9e9e9e'),
                }
            )
            action = 'added'

        data['entries'] = entries
        data['calibrated_at'] = datetime.now().isoformat()
        if not os.path.isdir(cal_dir):
            os.makedirs(cal_dir, exist_ok=True)
        with open(cal_path, 'w', encoding='utf-8') as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)

        return jsonify({'success': True, 'action': action, 'count': len(entries)})
    except Exception as exc:
        logger.error("Error patching calibration entry for %s: %s", folder_name, exc)
        return jsonify({'success': False, 'message': 'Грешка при чувању'}), 500


def api_geo_manual_calibration_delete(folder_name, *, app_root):
    """Delete manual calibration for a geological sheet."""
    if _is_invalid_folder_name(folder_name):
        return jsonify({'success': False, 'message': 'Неважећи назив'}), 400

    cal_path = os.path.join(app_root, 'data', 'geo_zones', folder_name, 'manual_calibration.json')
    if os.path.isfile(cal_path):
        os.remove(cal_path)
    return jsonify({'success': True, 'message': 'Калибрација обрисана'})
