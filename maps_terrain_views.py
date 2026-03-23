"""Shared route implementations for terrain and KMZ tile map views."""

import base64
import gzip
import io
import json
import logging
import os
import re

import numpy as np
import rasterio
from flask import jsonify, make_response, send_from_directory
from PIL import Image
from rasterio.windows import from_bounds
from scipy.ndimage import zoom as ndzoom

logger = logging.getLogger(__name__)


def api_balkans_terrain(*, dem_dir):
    """Full Serbia DEM at reduced resolution for geological timeline 3D view."""
    south, north = 42.0, 46.0
    west, east = 19.0, 23.0
    max_grid = 300

    dem_files = []
    for lat_floor in range(int(np.floor(south)), int(np.floor(north)) + 1):
        for lon_floor in range(int(np.floor(west)), int(np.floor(east)) + 1):
            fname = f"Copernicus_DSM_COG_10_N{lat_floor:02d}_00_E{lon_floor:03d}_00_DEM.tif"
            fpath = os.path.join(dem_dir, fname)
            if os.path.exists(fpath):
                dem_files.append(fpath)

    if not dem_files:
        return jsonify({'error': 'No DEM data'}), 404

    elevation_arrays = []
    for dem_path in dem_files:
        try:
            with rasterio.open(dem_path) as src:
                bounds = src.bounds
                win_south = max(south, bounds.bottom)
                win_north = min(north, bounds.top)
                win_west = max(west, bounds.left)
                win_east = min(east, bounds.right)
                if win_south >= win_north or win_west >= win_east:
                    continue
                window = from_bounds(win_west, win_south, win_east, win_north, src.transform)
                data = src.read(1, window=window)
                elevation_arrays.append(
                    {
                        'data': data,
                        'south': win_south,
                        'north': win_north,
                        'west': win_west,
                        'east': win_east,
                    }
                )
        except Exception:
            continue

    if not elevation_arrays:
        return jsonify({'error': 'No elevation data'}), 500

    lat_range = north - south
    lon_range = east - west
    aspect = lon_range / lat_range
    grid_cols = max_grid
    grid_rows = max(10, int(max_grid / aspect))

    elevation = np.full((grid_rows, grid_cols), np.nan, dtype=np.float32)
    for entry in elevation_arrays:
        row_start = int((north - entry['north']) / lat_range * grid_rows)
        row_end = int((north - entry['south']) / lat_range * grid_rows)
        col_start = int((entry['west'] - west) / lon_range * grid_cols)
        col_end = int((entry['east'] - west) / lon_range * grid_cols)
        row_start = max(0, min(row_start, grid_rows - 1))
        row_end = max(row_start + 1, min(row_end, grid_rows))
        col_start = max(0, min(col_start, grid_cols - 1))
        col_end = max(col_start + 1, min(col_end, grid_cols))
        target_rows = row_end - row_start
        target_cols = col_end - col_start
        if target_rows < 1 or target_cols < 1:
            continue
        src_data = entry['data'].astype(np.float32)
        if src_data.shape[0] != target_rows or src_data.shape[1] != target_cols:
            src_data = ndzoom(src_data, (target_rows / src_data.shape[0], target_cols / src_data.shape[1]), order=1)
            src_data = src_data[:target_rows, :target_cols]
        elevation[row_start:row_start + src_data.shape[0], col_start:col_start + src_data.shape[1]] = src_data

    nan_mask = np.isnan(elevation)
    if nan_mask.any():
        if nan_mask.all():
            return jsonify({'error': 'No valid data'}), 500
        from scipy.ndimage import distance_transform_edt

        indices = distance_transform_edt(nan_mask, return_distances=False, return_indices=True)
        elevation = elevation[tuple(indices)]

    elevation = np.round(elevation, 0).astype(np.int16)
    body = json.dumps(
        {
            'elevation': elevation.tolist(),
            'bounds': {'south': south, 'north': north, 'west': west, 'east': east},
            'grid': {'rows': grid_rows, 'cols': grid_cols},
        },
        separators=(',', ':'),
    )
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode='wb', compresslevel=4) as gz:
        gz.write(body.encode())
    response = make_response(buffer.getvalue())
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'public, max-age=86400'
    return response


def api_map_tile_index(*, build_tile_index):
    """Return tile index JSON."""
    index = build_tile_index()
    result = {'bounds': index.get('bounds', {}), 'levels': {}}
    for level, tiles in index.get('levels', {}).items():
        result['levels'][str(level)] = tiles
    return jsonify(result)


def api_map_tile(*, filename, extract_tile_to_cache, tile_cache_dir):
    """Serve an extracted KMZ tile PNG."""
    if not re.match(r'^kml_image_L\d+_\d+_\d+$', filename):
        return jsonify({'error': 'Invalid filename'}), 400

    png_name = filename + '.png'
    png_path = extract_tile_to_cache(filename)
    if png_path is None:
        return jsonify({'error': 'Tile not found in archive'}), 404

    return send_from_directory(tile_cache_dir, png_name, mimetype='image/png', max_age=86400)


def api_map_3d_terrain(*, dem_dir, build_tile_index, extract_tile_to_cache):
    """Return elevation grid plus geological texture for 3D terrain rendering."""
    from flask import request

    try:
        south = float(request.args.get('south', 0))
        north = float(request.args.get('north', 0))
        west = float(request.args.get('west', 0))
        east = float(request.args.get('east', 0))
        max_grid = min(int(request.args.get('max_grid', 800)), 2400)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid parameters'}), 400

    if south >= north or west >= east:
        return jsonify({'error': 'Invalid bounds: south must be < north, west must be < east'}), 400
    if (north - south) > 2.0 or (east - west) > 2.0:
        return jsonify({'error': 'Selection too large (max 2° x 2°)'}), 400
    if south < 41 or north > 47 or west < 18 or east > 24:
        return jsonify({'error': 'Selection outside Serbia DEM coverage'}), 400

    dem_files = []
    for lat_floor in range(int(np.floor(south)), int(np.floor(north)) + 1):
        for lon_floor in range(int(np.floor(west)), int(np.floor(east)) + 1):
            fname = f"Copernicus_DSM_COG_10_N{lat_floor:02d}_00_E{lon_floor:03d}_00_DEM.tif"
            fpath = os.path.join(dem_dir, fname)
            if os.path.exists(fpath):
                dem_files.append(fpath)

    if not dem_files:
        return jsonify({'error': 'No DEM data for selected area'}), 404

    elevation_arrays = []
    for dem_path in dem_files:
        try:
            with rasterio.open(dem_path) as src:
                bounds = src.bounds
                win_south = max(south, bounds.bottom)
                win_north = min(north, bounds.top)
                win_west = max(west, bounds.left)
                win_east = min(east, bounds.right)
                if win_south >= win_north or win_west >= win_east:
                    continue
                window = from_bounds(win_west, win_south, win_east, win_north, src.transform)
                data = src.read(1, window=window)
                elevation_arrays.append(
                    {
                        'data': data,
                        'south': win_south,
                        'north': win_north,
                        'west': win_west,
                        'east': win_east,
                    }
                )
        except Exception as exc:
            logger.warning("Error reading DEM %s: %s", dem_path, exc)
            continue

    if not elevation_arrays:
        return jsonify({'error': 'Could not read DEM data for area'}), 500

    lat_range = north - south
    lon_range = east - west
    aspect = lon_range / lat_range if lat_range > 0 else 1.0
    if aspect >= 1.0:
        grid_cols = max_grid
        grid_rows = max(10, int(max_grid / aspect))
    else:
        grid_rows = max_grid
        grid_cols = max(10, int(max_grid * aspect))

    elevation = np.full((grid_rows, grid_cols), np.nan, dtype=np.float32)
    for entry in elevation_arrays:
        row_start = int((north - entry['north']) / lat_range * grid_rows)
        row_end = int((north - entry['south']) / lat_range * grid_rows)
        col_start = int((entry['west'] - west) / lon_range * grid_cols)
        col_end = int((entry['east'] - west) / lon_range * grid_cols)
        row_start = max(0, min(row_start, grid_rows - 1))
        row_end = max(row_start + 1, min(row_end, grid_rows))
        col_start = max(0, min(col_start, grid_cols - 1))
        col_end = max(col_start + 1, min(col_end, grid_cols))

        target_rows = row_end - row_start
        target_cols = col_end - col_start
        if target_rows < 1 or target_cols < 1:
            continue

        src_data = entry['data'].astype(np.float32)
        if src_data.shape[0] != target_rows or src_data.shape[1] != target_cols:
            zoom_r = target_rows / src_data.shape[0]
            zoom_c = target_cols / src_data.shape[1]
            src_data = ndzoom(src_data, (zoom_r, zoom_c), order=1)
            src_data = src_data[:target_rows, :target_cols]

        elevation[row_start:row_start + src_data.shape[0], col_start:col_start + src_data.shape[1]] = src_data

    nan_mask = np.isnan(elevation)
    if nan_mask.any():
        if nan_mask.all():
            return jsonify({'error': 'No valid elevation data in area'}), 500
        from scipy.ndimage import distance_transform_edt

        indices = distance_transform_edt(nan_mask, return_distances=False, return_indices=True)
        elevation = elevation[tuple(indices)]

    tile_index = build_tile_index()
    levels = tile_index.get('levels', {})
    preferred_levels = [4, 3, 2, 1]
    geo_texture = None

    for level in preferred_levels:
        if level not in levels:
            continue
        overlapping = [
            tile
            for tile in levels[level]
            if tile['south'] < north and tile['north'] > south and tile['west'] < east and tile['east'] > west
        ]
        if not overlapping:
            continue

        tex_scale = min(4, 4800 / max(grid_cols, grid_rows))
        tex_w = int(grid_cols * tex_scale)
        tex_h = int(grid_rows * tex_scale)
        canvas = Image.new('RGBA', (tex_w, tex_h), (0, 0, 0, 0))

        for tile in overlapping:
            fname = tile['filename'].replace('.tif', '')
            png_path = extract_tile_to_cache(fname)
            if not png_path:
                continue
            try:
                tile_img = Image.open(png_path).convert('RGBA')
            except Exception:
                continue

            tx_start = int((tile['west'] - west) / lon_range * tex_w)
            ty_start = int((north - tile['north']) / lat_range * tex_h)
            tx_end = int((tile['east'] - west) / lon_range * tex_w)
            ty_end = int((north - tile['south']) / lat_range * tex_h)
            tw = max(1, tx_end - tx_start)
            th = max(1, ty_end - ty_start)
            tile_resized = tile_img.resize((tw, th), Image.LANCZOS)

            paste_x = max(0, tx_start)
            paste_y = max(0, ty_start)
            crop_x = max(0, -tx_start)
            crop_y = max(0, -ty_start)
            crop_r = tw - max(0, (tx_start + tw) - tex_w)
            crop_b = th - max(0, (ty_start + th) - tex_h)

            if crop_r > crop_x and crop_b > crop_y:
                region = tile_resized.crop((crop_x, crop_y, crop_r, crop_b))
                canvas.paste(region, (paste_x, paste_y), region)

        arr = np.array(canvas)
        if arr[:, :, 3].sum() > 0:
            geo_texture = canvas
            break

    geo_texture_b64 = None
    if geo_texture is not None:
        buffer = io.BytesIO()
        geo_texture.save(buffer, 'PNG', optimize=True)
        geo_texture_b64 = base64.b64encode(buffer.getvalue()).decode('ascii')

    lats = np.linspace(north, south, grid_rows).tolist()
    lons = np.linspace(west, east, grid_cols).tolist()
    elevation = np.round(elevation, 1)

    response_data = json.dumps(
        {
            'elevation': elevation.tolist(),
            'lats': lats,
            'lons': lons,
            'geo_texture_b64': geo_texture_b64,
            'bounds': {'south': south, 'north': north, 'west': west, 'east': east},
            'grid_size': {'rows': grid_rows, 'cols': grid_cols},
        }
    )

    gz_level = 3 if max_grid >= 1200 else 6
    compressed = gzip.compress(response_data.encode('utf-8'), compresslevel=gz_level)
    response = make_response(compressed)
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Length'] = len(compressed)
    return response
