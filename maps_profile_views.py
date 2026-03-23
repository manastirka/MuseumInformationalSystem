"""Shared route implementations for map elevation and digitized profile endpoints."""

import json
import logging
import os
from datetime import datetime

from flask import jsonify, request, session

logger = logging.getLogger(__name__)


def load_digitized_profiles(profiles_path):
    """Load digitized profiles from JSON file."""
    if not os.path.isfile(profiles_path):
        return []
    try:
        with open(profiles_path, 'r', encoding='utf-8') as handle:
            return json.load(handle)
    except Exception:
        return []


def save_digitized_profiles(profiles_path, profiles):
    """Save digitized profiles to JSON file."""
    with open(profiles_path, 'w', encoding='utf-8') as handle:
        json.dump(profiles, handle, ensure_ascii=False, indent=2)


def api_map_elevation(*, sample_elevation_at_point):
    """Return terrain elevation for a single lat/lon point."""
    try:
        lat = float(request.args.get('lat', 0))
        lon = float(request.args.get('lon', 0))
    except (TypeError, ValueError):
        return jsonify({'elevation': None})

    elevation = sample_elevation_at_point(lat, lon)
    return jsonify({'elevation': round(elevation, 1) if elevation is not None else None})


def api_map_cross_profile(
    *,
    app_root,
    haversine,
    batch_sample_elevations,
    interpolate_subsurface,
):
    """Generate a cross-section profile between two points."""
    try:
        lat1 = float(request.args.get('lat1', 0))
        lon1 = float(request.args.get('lon1', 0))
        lat2 = float(request.args.get('lat2', 0))
        lon2 = float(request.args.get('lon2', 0))
        samples = min(int(request.args.get('samples', 300)), 1000)
        subsurface = request.args.get('subsurface', 'false').lower() == 'true'
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Неважећи параметри'}), 400

    if samples < 2:
        return jsonify({'success': False, 'message': 'Потребно минимум 2 тачке'}), 400

    for lat, lon in ((lat1, lon1), (lat2, lon2)):
        if lat < 41 or lat > 47 or lon < 18 or lon > 24:
            return jsonify({'success': False, 'message': 'Координате изван покривености ДЕМ података'}), 400

    total_distance = haversine(lat1, lon1, lat2, lon2)
    if total_distance < 0.01:
        return jsonify({'success': False, 'message': 'Тачке су сувише близу'}), 400

    try:
        sheets_path = os.path.join(app_root, 'data', 'geological_map_sheets.json')
        with open(sheets_path, 'r', encoding='utf-8') as handle:
            geo_sheets = json.load(handle)
    except Exception:
        geo_sheets = []

    sample_points = []
    for idx in range(samples):
        frac = idx / (samples - 1) if samples > 1 else 0
        sample_points.append((lat1 + (lat2 - lat1) * frac, lon1 + (lon2 - lon1) * frac))

    elevations = batch_sample_elevations(sample_points)

    profile_points = []
    for idx, (lat, lon) in enumerate(sample_points):
        dist_km = 0 if idx == 0 else haversine(lat1, lon1, lat, lon)
        elevation = elevations[idx]
        if elevation is None:
            for offset in (1, -1, 2, -2):
                neighbor_idx = idx + offset
                if 0 <= neighbor_idx < len(elevations) and elevations[neighbor_idx] is not None:
                    elevation = elevations[neighbor_idx]
                    break
            if elevation is None:
                elevation = 0

        profile_points.append(
            {
                'dist_km': round(dist_km, 3),
                'lat': round(lat, 6),
                'lon': round(lon, 6),
                'elevation': round(elevation, 1),
            }
        )

    elevs = [point['elevation'] for point in profile_points]
    elev_min = min(elevs) if elevs else 0
    elev_max = max(elevs) if elevs else 0
    gain = 0
    loss = 0
    for idx in range(1, len(elevs)):
        diff = elevs[idx] - elevs[idx - 1]
        if diff > 0:
            gain += diff
        else:
            loss += abs(diff)

    crossing_sheets = []
    seen_folders = set()
    for sheet in geo_sheets:
        bounds = sheet.get('bounds', {})
        folder = sheet.get('folder', '')
        if not folder or folder in seen_folders:
            continue
        south = bounds.get('south', 99)
        north = bounds.get('north', -99)
        west = bounds.get('west', 99)
        east = bounds.get('east', -99)
        for lat, lon in sample_points:
            if south <= lat <= north and west <= lon <= east:
                crossing_sheets.append(folder)
                seen_folders.add(folder)
                break

    nearest_profiles = []
    mid_lat = (lat1 + lat2) / 2
    mid_lon = (lon1 + lon2) / 2
    for sheet in geo_sheets:
        center = sheet.get('center', {})
        if center.get('lat') and center.get('lon'):
            distance = haversine(mid_lat, mid_lon, center['lat'], center['lon'])
            if sheet.get('files', {}).get('profili'):
                nearest_profiles.append(
                    {
                        'sheet': sheet.get('name', ''),
                        'folder': sheet.get('folder', ''),
                        'profile_file': 'profili',
                        'distance_km': round(distance, 1),
                    }
                )
    nearest_profiles.sort(key=lambda item: item['distance_km'])
    nearest_profiles = nearest_profiles[:3]

    response = {
        'success': True,
        'profile': {
            'points': profile_points,
            'total_distance_km': round(total_distance, 2),
            'elevation_min': round(elev_min, 1),
            'elevation_max': round(elev_max, 1),
            'elevation_gain': round(gain, 0),
            'elevation_loss': round(loss, 0),
            'crossing_sheets': crossing_sheets,
            'nearest_profiles': nearest_profiles,
        },
    }

    if subsurface:
        subsurface_data = interpolate_subsurface(lat1, lon1, lat2, lon2, profile_points, total_distance)
        if subsurface_data:
            response['profile']['subsurface'] = subsurface_data

    return jsonify(response)


def api_digitized_profiles_list(*, profiles_path):
    """List all digitized cross-section profiles."""
    profiles = load_digitized_profiles(profiles_path)
    summary = []
    for profile in profiles:
        summary.append(
            {
                'id': profile['id'],
                'sheet_folder': profile.get('sheet_folder', ''),
                'profile_id': profile.get('profile_id', ''),
                'endpoint_a': profile.get('endpoint_a', {}),
                'endpoint_b': profile.get('endpoint_b', {}),
                'layer_count': len(profile.get('layers', [])),
                'fault_count': len(profile.get('faults', [])),
                'digitized_by': profile.get('digitized_by', ''),
                'digitized_at': profile.get('digitized_at', ''),
            }
        )
    return jsonify({'success': True, 'data': summary})


def api_digitized_profile_get(profile_id, *, profiles_path):
    """Get a single digitized profile."""
    profiles = load_digitized_profiles(profiles_path)
    profile = next((entry for entry in profiles if entry['id'] == profile_id), None)
    if not profile:
        return jsonify({'success': False, 'message': 'Профил није пронађен'}), 404
    return jsonify({'success': True, 'data': profile})


def api_digitized_profile_create(*, profiles_path):
    """Create a new digitized profile."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Недостају подаци'}), 400

        profiles = load_digitized_profiles(profiles_path)
        profile_id = data.get('id')
        if not profile_id:
            profile_id = f"{data.get('sheet_folder', 'unknown')}_{data.get('profile_id', 'AB')}"

        if any(profile['id'] == profile_id for profile in profiles):
            return jsonify({'success': False, 'message': 'Профил са овим ID-јем већ постоји'}), 409

        profile = {
            'id': profile_id,
            'sheet_folder': data.get('sheet_folder', ''),
            'profile_id': data.get('profile_id', ''),
            'endpoint_a': data.get('endpoint_a', {}),
            'endpoint_b': data.get('endpoint_b', {}),
            'image_bounds': data.get('image_bounds', {}),
            'layers': data.get('layers', []),
            'faults': data.get('faults', []),
            'digitized_by': session.get('user_email', ''),
            'digitized_at': datetime.now().isoformat(),
        }

        profiles.append(profile)
        save_digitized_profiles(profiles_path, profiles)
        return jsonify({'success': True, 'data': profile, 'message': 'Профил сачуван'})
    except Exception as exc:
        logger.error("Error creating digitized profile: %s", exc)
        return jsonify({'success': False, 'message': 'Грешка при чувању профила'}), 500


def api_digitized_profile_update(profile_id, *, profiles_path):
    """Update an existing digitized profile."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Недостају подаци'}), 400

        profiles = load_digitized_profiles(profiles_path)
        idx = next((i for i, profile in enumerate(profiles) if profile['id'] == profile_id), None)
        if idx is None:
            return jsonify({'success': False, 'message': 'Профил није пронађен'}), 404

        profile = profiles[idx]
        for key in ('endpoint_a', 'endpoint_b', 'image_bounds', 'layers', 'faults', 'profile_id', 'sheet_folder'):
            if key in data:
                profile[key] = data[key]
        profile['digitized_by'] = session.get('user_email', '')
        profile['digitized_at'] = datetime.now().isoformat()

        profiles[idx] = profile
        save_digitized_profiles(profiles_path, profiles)
        return jsonify({'success': True, 'data': profile, 'message': 'Профил ажуриран'})
    except Exception as exc:
        logger.error("Error updating digitized profile %s: %s", profile_id, exc)
        return jsonify({'success': False, 'message': 'Грешка при ажурирању'}), 500


def api_digitized_profile_delete(profile_id, *, profiles_path):
    """Delete a digitized profile."""
    try:
        profiles = load_digitized_profiles(profiles_path)
        new_profiles = [profile for profile in profiles if profile['id'] != profile_id]
        if len(new_profiles) == len(profiles):
            return jsonify({'success': False, 'message': 'Профил није пронађен'}), 404

        save_digitized_profiles(profiles_path, new_profiles)
        return jsonify({'success': True, 'message': 'Профил обрисан'})
    except Exception as exc:
        logger.error("Error deleting digitized profile %s: %s", profile_id, exc)
        return jsonify({'success': False, 'message': 'Грешка при брисању'}), 500
