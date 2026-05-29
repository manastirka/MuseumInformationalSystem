"""Support helpers and shared state for geological profile and sampling logic."""

import json
import logging
import math
import os
import time

import maps_terrain_support
from runtime_lock_utils import load_json_file, write_json_file

logger = logging.getLogger(__name__)

APP_ROOT = os.path.dirname(__file__)
DIGITIZED_PROFILES_PATH = os.path.join(APP_ROOT, 'data', 'digitized_profiles.json')

_zone_map_cache = {}
_ZONE_MAP_CACHE_MAX = 10


def load_zone_map_cached(folder_name, sheet_bounds):
    """Load zone group image/metadata for a sheet, with simple LRU eviction."""
    from PIL import Image

    now = time.time()
    if folder_name in _zone_map_cache:
        _zone_map_cache[folder_name]['atime'] = now
        return _zone_map_cache[folder_name]

    zone_dir = os.path.join(APP_ROOT, 'data', 'geo_zones', folder_name)
    map_path = os.path.join(zone_dir, 'zone_group_map.png')
    meta_path = os.path.join(zone_dir, 'zone_groups_meta.json')

    if not os.path.isfile(map_path) or not os.path.isfile(meta_path):
        return None

    try:
        image = Image.open(map_path)
        meta = load_json_file(meta_path, default=[])

        legend_path = os.path.join(zone_dir, 'enhanced_legend.json')
        legend = []
        if os.path.isfile(legend_path):
            legend = load_json_file(legend_path, default=[])

        calib_path = os.path.join(zone_dir, 'manual_calibration.json')
        calibration = []
        if os.path.isfile(calib_path):
            calib_data = load_json_file(calib_path, default={})
            calibration = calib_data.get('entries', [])

        groups = meta.get('groups', meta) if isinstance(meta, dict) else meta
        id_to_group = {}
        for group in groups:
            id_to_group[group.get('group_id', 0)] = group

        entry = {
            'image': image,
            'meta': groups,
            'legend': legend,
            'calibration': calibration,
            'id_to_group': id_to_group,
            'bounds': sheet_bounds,
            'width': image.width,
            'height': image.height,
            'atime': now,
        }

        if len(_zone_map_cache) >= _ZONE_MAP_CACHE_MAX:
            oldest_key = min(_zone_map_cache, key=lambda key: _zone_map_cache[key]['atime'])
            old_entry = _zone_map_cache.pop(oldest_key)
            old_entry['image'].close()

        _zone_map_cache[folder_name] = entry
        return entry
    except Exception as exc:
        logger.warning("Error loading zone map for %s: %s", folder_name, exc)
        return None


def haversine_km(lat1, lon1, lat2, lon2):
    """Haversine distance in km between two lat/lon points."""
    radius_km = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return radius_km * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def sample_tile_color_at_point(lat, lon):
    """Sample RGB color from the geological map tile set at one point."""
    from PIL import Image

    tile_index = maps_terrain_support.build_tile_index()
    levels = tile_index.get('levels', {})

    for level in [4, 3, 2, 1]:
        if level not in levels:
            continue
        for tile in levels[level]:
            if not (tile['south'] <= lat <= tile['north'] and tile['west'] <= lon <= tile['east']):
                continue

            filename = tile['filename'].replace('.tif', '')
            png_path = maps_terrain_support.extract_tile_to_cache(filename)
            if not png_path:
                continue

            try:
                image = Image.open(png_path)
                px_x = int((lon - tile['west']) / (tile['east'] - tile['west']) * image.width)
                px_y = int((tile['north'] - lat) / (tile['north'] - tile['south']) * image.height)
                px_x = max(0, min(px_x, image.width - 1))
                px_y = max(0, min(px_y, image.height - 1))
                pixel = image.getpixel((px_x, px_y))
                image.close()
                if len(pixel) >= 3:
                    if len(pixel) == 4 and pixel[3] < 50:
                        continue
                    return (pixel[0], pixel[1], pixel[2])
            except Exception:
                continue
    return None


def rgb_to_hsv(r, g, b):
    """Convert RGB (0-255) to HSV (h=0-360, s=0-100, v=0-100)."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    delta = mx - mn
    value = mx
    saturation = 0 if mx == 0 else delta / mx
    if delta == 0:
        hue = 0
    elif mx == r:
        hue = ((g - b) / delta + (6 if g < b else 0)) * 60
    elif mx == g:
        hue = ((b - r) / delta + 2) * 60
    else:
        hue = ((r - g) / delta + 4) * 60
    return hue, saturation * 100, value * 100


def classify_geo_color(r, g, b, sheet_data=None):
    """Classify one geological map color into a unit/era payload."""
    hue, saturation, value = rgb_to_hsv(r, g, b)

    sheet_periods = None
    if sheet_data and sheet_data.get('tumac') and sheet_data['tumac'].get('geological_periods'):
        sheet_periods = set(sheet_data['tumac']['geological_periods'])

    def allowed(periods):
        if sheet_periods is None:
            return True
        return any(period in sheet_periods for period in periods)

    era_canonical_colors = {
        'Kvartar': '#c8b464',
        'Holocen': '#c8b464',
        'Pleistocen': '#d4c878',
        'Neogen': '#f9a825',
        'Paleogen': '#ff8f00',
        'Kreda': '#2e7d32',
        'Jura': '#1565c0',
        'Trijas': '#9c27b0',
        'Perm': '#e65100',
        'Karbon': '#5d4037',
        'Devon': '#0d47a1',
        'Paleozoik': '#795548',
        'Офиолити': '#00695c',
        'Магматити': '#d32f2f',
        'Метаморфити': '#7b1fa2',
        'Prekambrijum': '#880e4f',
    }

    def result(name_sr, name_en, code, era, era_color):
        return {
            'unit_code': code,
            'unit_name_sr': name_sr,
            'unit_name_en': name_en,
            'era': era,
            'era_color': era_color,
            'color': era_canonical_colors.get(era, era_color),
            'sheet_folder': sheet_data.get('folder', '') if sheet_data else '',
            'sheet_name': sheet_data.get('name', '') if sheet_data else '',
        }

    if saturation < 8 and 20 < value < 90:
        return None

    if 265 <= hue <= 345 and saturation > 12:
        if not allowed(['Trijas', 'Prekambrijum', 'Rifeo-kambrijum', 'Paleozoik']):
            return None
        if value < 30:
            return result('Прекамбријум', 'Precambrian', 'PR', 'Prekambrijum', '#880e4f')
        if saturation > 40:
            return result('Тријас', 'Triassic', 'T', 'Trijas', '#9c27b0')
        return result('Тријас - метаморфити', 'Triassic metamorphic', 'Tm', 'Trijas', '#9c27b0')

    if 195 <= hue <= 265 and saturation > 12:
        if not allowed(['Jura', 'Karbon']):
            return None
        if value > 60 and saturation < 35:
            return result('Горња јура', 'Upper Jurassic', 'J₃', 'Jura', '#1565c0')
        if value < 45:
            return result('Доња јура', 'Lower Jurassic', 'J₁', 'Jura', '#1565c0')
        return result('Јура', 'Jurassic', 'J', 'Jura', '#1565c0')

    if 155 <= hue <= 198 and saturation > 12:
        if not allowed(['Jura', 'Kreda', 'Trijas']):
            return None
        if value < 45:
            return result('Серпентинит', 'Serpentinite', 'Se', 'Офиолити', '#00695c')
        return result('Офиолитски комплекс', 'Ophiolite complex', 'of', 'Офиолити', '#00695c')

    if 68 <= hue <= 158 and saturation > 12:
        if value > 50 and allowed(['Kreda']):
            if hue > 100:
                return result('Кредни флиш', 'Cretaceous flysch', 'Kf', 'Kreda', '#2e7d32')
            if saturation > 60:
                return result('Горња креда', 'Upper Cretaceous', 'K₂', 'Kreda', '#2e7d32')
            return result('Креда', 'Cretaceous', 'K', 'Kreda', '#2e7d32')
        if value <= 50 or saturation <= 30:
            if allowed(['Paleozoik', 'Karbon', 'Devon', 'Silur', 'Ordovicijum', 'Kambrijum']):
                return result('Палеозоик', 'Paleozoic', 'Pz', 'Paleozoik', '#795548')
            if allowed(['Kreda']):
                return result('Доња креда', 'Lower Cretaceous', 'K₁', 'Kreda', '#2e7d32')
        if allowed(['Kreda']):
            return result('Креда', 'Cretaceous', 'K', 'Kreda', '#2e7d32')
        return None

    if 12 <= hue <= 52 and 18 <= saturation <= 75 and 20 <= value <= 62:
        if allowed(['Jura', 'Kreda', 'Trijas']):
            return result('Серпентинит', 'Serpentinite', 'Se', 'Офиолити', '#00695c')
        if allowed(['Devon', 'Paleozoik']):
            return result('Девон', 'Devonian', 'D', 'Devon', '#0d47a1')
        if allowed(['Perm']):
            return result('Перм', 'Permian', 'P', 'Perm', '#e65100')
        return None

    if (hue >= 345 or hue <= 15) and saturation > 45:
        if value > 60:
            if allowed(['Neogen', 'Paleogen', 'Kreda']):
                return result('Вулканити', 'Volcanic rocks', 'v', 'Магматити', '#d32f2f')
            if allowed(['Perm']):
                return result('Перм', 'Permian', 'P', 'Perm', '#e65100')
        if allowed(['Perm']):
            return result('Перм', 'Permian', 'P', 'Perm', '#e65100')
        return None

    if 13 <= hue <= 42 and saturation > 45 and value > 60:
        if saturation > 65:
            if allowed(['Neogen']):
                return result('Неоген - тортон (M₂)', 'Neogene - Tortonian', 'M₂', 'Neogen', '#f57f17')
            if allowed(['Paleogen']):
                return result('Палеоген', 'Paleogene', 'Pg', 'Paleogen', '#ff8f00')
        if allowed(['Paleogen']):
            return result('Палеоген', 'Paleogene', 'Pg', 'Paleogen', '#ff8f00')
        if allowed(['Neogen']):
            return result('Неоген - миоцен', 'Neogene - Miocene', 'M', 'Neogen', '#f9a825')
        return None

    if 0 <= hue <= 35 and 15 <= saturation <= 55 and value > 62:
        if allowed(['Trijas']):
            return result('Тријас - карбонати', 'Triassic carbonates', 'Tk', 'Trijas', '#e53935')
        if allowed(['Paleogen', 'Neogen', 'Kreda']):
            return result('Гранитоиди', 'Granitoids', 'γ', 'Магматити', '#d32f2f')
        if allowed(['Perm']):
            return result('Горњи перм', 'Upper Permian', 'P₂', 'Perm', '#e65100')
        return None

    if 58 <= hue < 68 and saturation > 15:
        if saturation > 50 and value > 80 and allowed(['Neogen']):
            return result('Неоген - понт (M₃³)', 'Neogene - Pontian', 'M₃³', 'Neogen', '#f9a825')
        if allowed(['Kreda']):
            return result('Горња креда', 'Upper Cretaceous', 'K₂', 'Kreda', '#2e7d32')
        if allowed(['Neogen']):
            return result('Неоген - понт (M₃³)', 'Neogene - Pontian', 'M₃³', 'Neogen', '#f9a825')
        return None

    if 38 <= hue < 58:
        if (
            hue < 48
            and value < 85
            and saturation > 45
            and allowed(['Paleozoik', 'Perm', 'Karbon', 'Devon', 'Silur', 'Ordovicijum', 'Kambrijum'])
            and not allowed(['Neogen'])
        ):
            return result('Палеозоик - седименти', 'Paleozoic sediments', 'Pzs', 'Paleozoik', '#795548')
        if saturation < 22:
            if allowed(['Kvartar', 'Holocen']):
                return result('Холоцен - алувијум', 'Holocene - Alluvium', 'al', 'Holocen', '#8d6e63')
            if allowed(['Neogen']):
                return result('Неоген', 'Neogene', 'N', 'Neogen', '#f9a825')
            return None
        if 22 <= saturation < 38:
            if allowed(['Kvartar', 'Holocen']):
                return result('Холоцен', 'Holocene', 'h', 'Holocen', '#8d6e63')
            if allowed(['Neogen']):
                return result('Неоген - горњи миоцен', 'Neogene - Upper Miocene', 'M₃', 'Neogen', '#f9a825')
            return None
        if 38 <= saturation < 50:
            if hue >= 52 and allowed(['Neogen']) and not allowed(['Kvartar', 'Pleistocen']):
                return result('Неоген - сармат (M₃¹)', 'Neogene - Sarmatian', 'M₃¹', 'Neogen', '#f9a825')
            if allowed(['Kvartar', 'Pleistocen']):
                return result('Плеистоцен', 'Pleistocene', 'Q₁', 'Pleistocen', '#00acc1')
            if allowed(['Neogen']):
                return result('Неоген - сармат (M₃¹)', 'Neogene - Sarmatian', 'M₃¹', 'Neogen', '#f9a825')
            return None
        if 50 <= saturation < 62:
            if hue < 52 and allowed(['Neogen']):
                return result('Неоген - плиоцен', 'Neogene - Pliocene', 'Pl', 'Neogen', '#f9a825')
            if allowed(['Neogen']):
                return result('Неоген - панон (M₃²)', 'Neogene - Pannonian', 'M₃²', 'Neogen', '#f9a825')
            if allowed(['Kvartar', 'Pleistocen']):
                return result('Плеистоцен', 'Pleistocene', 'Q₁', 'Pleistocen', '#00acc1')
            return None
        if saturation >= 62:
            if allowed(['Neogen']):
                return result('Неоген - миоцен', 'Neogene - Miocene', 'M', 'Neogen', '#f9a825')
            if allowed(['Paleozoik', 'Perm', 'Karbon', 'Devon']):
                return result('Палеозоик - седименти', 'Paleozoic sediments', 'Pzs', 'Paleozoik', '#795548')
            return None

    if 200 <= hue <= 280 and saturation < 15 and value > 80:
        if allowed(['Kvartar', 'Holocen']):
            return result('Језерско-речни седименти', 'Lake/river sediments', 'l-fl', 'Kvartar', '#00bcd4')
        return None

    return None


def sample_geology_at_point(lat, lon, sheets_data):
    """Determine geological unit at one point using zone maps, then HSV fallback."""
    for sheet in sheets_data:
        bounds = sheet.get('bounds', {})
        if not (
            bounds.get('south', 99) <= lat <= bounds.get('north', -99)
            and bounds.get('west', 99) <= lon <= bounds.get('east', -99)
        ):
            continue

        folder = sheet.get('folder', '')
        cached = load_zone_map_cached(folder, bounds)
        if not cached:
            continue

        img_w = cached['width']
        img_h = cached['height']
        south = bounds['south']
        north = bounds['north']
        west = bounds['west']
        east = bounds['east']

        px_x = int((lon - west) / (east - west) * img_w)
        px_y = int((north - lat) / (north - south) * img_h)
        px_x = max(0, min(px_x, img_w - 1))
        px_y = max(0, min(px_y, img_h - 1))

        try:
            pixel_val = cached['image'].getpixel((px_x, px_y))
            group_id = pixel_val if isinstance(pixel_val, int) else pixel_val[0]
        except Exception:
            continue

        if group_id == 0:
            continue

        best_group = cached.get('id_to_group', {}).get(group_id)
        if not best_group:
            continue

        era = best_group.get('era', '')
        era_color = best_group.get('era_color', '#9e9e9e')
        color = best_group.get('color', [128, 128, 128])

        if isinstance(color, (list, tuple)) and len(color) >= 3:
            for calib in cached.get('calibration', []):
                calib_color = calib.get('color', [0, 0, 0])
                delta_r = color[0] - calib_color[0]
                delta_g = color[1] - calib_color[1]
                delta_b = color[2] - calib_color[2]
                distance = math.sqrt(delta_r * delta_r + delta_g * delta_g + delta_b * delta_b)
                if distance < 30:
                    if calib.get('unit_code'):
                        best_group = dict(best_group)
                        best_group['unit_code'] = calib['unit_code']
                        best_group['unit_name_sr'] = calib.get('unit_name_sr', '')
                        best_group['unit_name_en'] = calib.get('unit_name_en', '')
                        if calib.get('era'):
                            era = calib['era']
                            era_color = calib.get('era_color', era_color)
                    break

        if isinstance(color, (list, tuple)):
            hex_color = '#{:02x}{:02x}{:02x}'.format(int(color[0]), int(color[1]), int(color[2]))
        else:
            hex_color = '#808080'

        return {
            'unit_code': best_group.get('unit_code', ''),
            'unit_name_sr': best_group.get('unit_name_sr', ''),
            'unit_name_en': best_group.get('unit_name_en', ''),
            'era': era,
            'era_color': era_color,
            'color': hex_color,
            'sheet_folder': folder,
            'sheet_name': sheet.get('name', ''),
        }

    rgb = sample_tile_color_at_point(lat, lon)
    if rgb:
        sheet_for_hsv = None
        for sheet in sheets_data:
            bounds = sheet.get('bounds', {})
            if (
                bounds.get('south', 99) <= lat <= bounds.get('north', -99)
                and bounds.get('west', 99) <= lon <= bounds.get('east', -99)
            ):
                sheet_for_hsv = sheet
                break
        classified = classify_geo_color(rgb[0], rgb[1], rgb[2], sheet_for_hsv)
        if classified:
            return classified

    return None


def sample_elevation_at_point(lat, lon):
    """Sample DEM elevation at a single lat/lon point."""
    import numpy as np
    import rasterio
    from rasterio.windows import from_bounds

    lat_floor = int(np.floor(lat))
    lon_floor = int(np.floor(lon))
    filename = f"Copernicus_DSM_COG_10_N{lat_floor:02d}_00_E{lon_floor:03d}_00_DEM.tif"
    dem_path = os.path.join(maps_terrain_support.DEM_DIR, filename)

    if not os.path.exists(dem_path):
        return None

    try:
        with rasterio.open(dem_path) as src:
            delta = 0.001
            window = from_bounds(lon - delta, lat - delta, lon + delta, lat + delta, src.transform)
            data = src.read(1, window=window)
            if data.size > 0:
                value = float(np.nanmean(data))
                if not np.isnan(value):
                    return value
    except Exception:
        pass
    return None


def batch_sample_elevations(points):
    """Batch sample DEM elevations for a list of ``(lat, lon)`` tuples."""
    import numpy as np
    import rasterio

    results = [None] * len(points)
    tile_groups = {}
    for idx, (lat, lon) in enumerate(points):
        lat_floor = int(np.floor(lat))
        lon_floor = int(np.floor(lon))
        tile_groups.setdefault((lat_floor, lon_floor), []).append(idx)

    for (lat_floor, lon_floor), indices in tile_groups.items():
        filename = f"Copernicus_DSM_COG_10_N{lat_floor:02d}_00_E{lon_floor:03d}_00_DEM.tif"
        dem_path = os.path.join(maps_terrain_support.DEM_DIR, filename)
        if not os.path.exists(dem_path):
            continue

        try:
            with rasterio.open(dem_path) as src:
                for idx in indices:
                    lat, lon = points[idx]
                    row, col = src.index(lon, lat)
                    row = max(0, min(row, src.height - 1))
                    col = max(0, min(col, src.width - 1))
                    window = rasterio.windows.Window(col, row, 1, 1)
                    data = src.read(1, window=window)
                    if data.size > 0:
                        value = float(data[0, 0])
                        if not np.isnan(value) and value > -500:
                            results[idx] = value
        except Exception as exc:
            logger.warning("Error batch-reading DEM tile N%sE%s: %s", lat_floor, lon_floor, exc)

    return results


def load_digitized_profiles(profiles_path=DIGITIZED_PROFILES_PATH):
    """Load digitized profiles from JSON."""
    if not os.path.isfile(profiles_path):
        return []
    try:
        return load_json_file(profiles_path, default=[])
    except Exception:
        return []


def save_digitized_profiles(profiles, profiles_path=DIGITIZED_PROFILES_PATH):
    """Save digitized profiles to JSON."""
    write_json_file(profiles_path, profiles)


def interpolate_subsurface(lat1, lon1, lat2, lon2, surface_points, total_distance_km):
    """Interpolate subsurface units from nearby digitized cross-sections."""
    profiles = load_digitized_profiles()
    if not profiles:
        return None

    mid_lat = (lat1 + lat2) / 2
    mid_lon = (lon1 + lon2) / 2
    nearby = []
    for profile in profiles:
        endpoint_a = profile.get('endpoint_a', {})
        endpoint_b = profile.get('endpoint_b', {})
        if None in (
            endpoint_a.get('lat'),
            endpoint_a.get('lon'),
            endpoint_b.get('lat'),
            endpoint_b.get('lon'),
        ):
            continue
        profile_mid_lat = (endpoint_a['lat'] + endpoint_b['lat']) / 2
        profile_mid_lon = (endpoint_a['lon'] + endpoint_b['lon']) / 2
        distance = haversine_km(mid_lat, mid_lon, profile_mid_lat, profile_mid_lon)
        if distance <= 50:
            nearby.append({'profile': profile, 'distance': distance})

    if not nearby:
        return None

    depth_levels = list(range(0, -2001, -50))
    subsurface_columns = []
    for surface_point in surface_points:
        column = {
            'dist_km': surface_point['dist_km'],
            'lat': surface_point['lat'],
            'lon': surface_point['lon'],
            'surface_elevation': surface_point['elevation'],
            'layers': [],
        }

        for depth in depth_levels:
            elevation = surface_point['elevation'] + depth
            unit_votes = {}
            total_weight = 0

            for nearby_profile in nearby:
                profile = nearby_profile['profile']
                profile_distance = nearby_profile['distance']
                image_bounds = profile.get('image_bounds', {})
                if not image_bounds.get('distance_km'):
                    continue

                frac = surface_point['dist_km'] / total_distance_km if total_distance_km > 0 else 0
                projected_distance = frac * image_bounds['distance_km']
                elevation_top = image_bounds.get('elevation_top_m', 1000)
                elevation_bottom = image_bounds.get('elevation_bottom_m', -1000)

                if elevation > elevation_top or elevation < elevation_bottom:
                    continue

                for layer in profile.get('layers', []):
                    points = layer.get('boundary_points', [])
                    if len(points) < 2:
                        continue

                    try:
                        layer_distances = [point[0] for point in points]
                        min_dist = min(layer_distances)
                        max_dist = max(layer_distances)
                        if projected_distance < min_dist or projected_distance > max_dist:
                            continue

                        boundary_elevation = None
                        for idx in range(len(points) - 1):
                            if points[idx][0] <= projected_distance <= points[idx + 1][0]:
                                denominator = points[idx + 1][0] - points[idx][0]
                                ratio = (projected_distance - points[idx][0]) / denominator if denominator != 0 else 0
                                boundary_elevation = points[idx][1] + ratio * (points[idx + 1][1] - points[idx][1])
                                break
                    except (TypeError, IndexError, KeyError):
                        continue

                    if boundary_elevation is not None and elevation <= boundary_elevation:
                        weight = 1.0 / max(profile_distance ** 2, 0.01)
                        unit_code = layer.get('unit_code', 'unknown')
                        unit_votes[unit_code] = unit_votes.get(unit_code, 0) + weight
                        total_weight += weight

            if unit_votes:
                winner = max(unit_votes, key=unit_votes.get)
                min_distance = min(item['distance'] for item in nearby) if nearby else 999
                if min_distance < 5:
                    confidence = 'high'
                elif min_distance < 20:
                    confidence = 'medium'
                else:
                    confidence = 'low'

                column['layers'].append(
                    {
                        'depth': depth,
                        'elevation': round(elevation, 1),
                        'unit_code': winner,
                        'confidence': confidence,
                    }
                )

        subsurface_columns.append(column)

    units = set()
    for column in subsurface_columns:
        for layer in column['layers']:
            units.add(layer['unit_code'])

    faults = []
    for nearby_profile in nearby:
        profile = nearby_profile['profile']
        for fault in profile.get('faults', []):
            faults.append(
                {
                    'distance_km': fault.get('distance_km', 0),
                    'points': fault.get('points', []),
                    'type': fault.get('type', 'normal'),
                    'source_profile': profile.get('id', ''),
                    'source_distance': nearby_profile['distance'],
                }
            )

    return {
        'columns': subsurface_columns,
        'depth_range': [0, -2000],
        'depth_step': 50,
        'nearby_profiles_count': len(nearby),
        'units': list(units),
        'faults': faults,
    }
