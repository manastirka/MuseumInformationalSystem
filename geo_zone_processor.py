#!/usr/bin/env python3
"""
Geological Zone Processor — Pre-processes OGK map sheet images into zone maps.

For each of the 65 OGK geological map sheets, generates:
  - zone_group_map.png: uint8 PNG at half-resolution (~200-400KB) where each pixel value
    is a zone group ID
  - zone_groups_meta.json: metadata for each zone group (color, unit, pattern, etc.)
  - enhanced_legend.json: extracted legend swatches with color, HSV, and unit info

Uses Pillow + NumPy + SciPy + scikit-learn (for K-means clustering).
"""

import os
import sys
import json
import math
import logging
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
from scipy.ndimage import binary_opening, binary_closing, binary_dilation
from sklearn.cluster import MiniBatchKMeans
from runtime_lock_utils import load_json_file, write_json_file

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SHEETS_JSON = os.path.join(BASE_DIR, 'data', 'geological_map_sheets.json')
KARTE_DIR = os.path.join(BASE_DIR, 'Karte', 'Final - Srbija')
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'geo_zones')

# HSV-based geological era classification (mirrors client-side classifyGeoColor logic)
GEO_HSV_FAMILIES = [
    {'hMin': 38, 'hMax': 65, 'era': 'Kvartar', 'eraColor': '#8d6e63',
     'families': ['Kvartar', 'Pleistocen', 'Holocen', 'Neogen']},
    {'hMin': 13, 'hMax': 38, 'era': 'Neogen', 'eraColor': '#f9a825',
     'families': ['Paleogen', 'Neogen']},
    {'hMin': 68, 'hMax': 158, 'era': 'Kreda', 'eraColor': '#2e7d32',
     'families': ['Kreda', 'Paleozoik']},
    {'hMin': 195, 'hMax': 265, 'era': 'Jura', 'eraColor': '#1565c0',
     'families': ['Jura']},
    {'hMin': 265, 'hMax': 345, 'era': 'Trijas', 'eraColor': '#9c27b0',
     'families': ['Trijas', 'Prekambrijum']},
    {'hMin': 345, 'hMax': 375, 'era': 'Perm', 'eraColor': '#e65100',
     'families': ['Perm', 'Магматити']},
    {'hMin': 0, 'hMax': 15, 'era': 'Магматити', 'eraColor': '#d32f2f',
     'families': ['Магматити', 'Perm']},
    {'hMin': 155, 'hMax': 195, 'era': 'Офиолити', 'eraColor': '#00695c',
     'families': ['Офиолити', 'Jura', 'Kreda']},
]


def rgb_to_hsv(r, g, b):
    """Convert RGB (0-255) to HSV (h=0-360, s=0-100, v=0-100)."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    d = mx - mn
    v = mx
    s = 0 if mx == 0 else d / mx
    if d == 0:
        h = 0
    elif mx == r:
        h = ((g - b) / d + (6 if g < b else 0)) * 60
    elif mx == g:
        h = ((b - r) / d + 2) * 60
    else:
        h = ((r - g) / d + 4) * 60
    return h, s * 100, v * 100


def hsv_distance(h1, s1, v1, h2, s2, v2):
    """Weighted HSV distance matching client-side matchToLegend logic."""
    dh = min(abs(h1 - h2), 360 - abs(h1 - h2))
    ds = abs(s1 - s2)
    dv = abs(v1 - v2)
    return (dh / 180) * 4 + (ds / 100) * 3 + (dv / 100) * 1.5


def classify_era(h, s, v):
    """Classify an HSV color into a geological era family."""
    for fam in GEO_HSV_FAMILIES:
        hmin, hmax = fam['hMin'], fam['hMax']
        if hmax > 360:
            if h >= hmin or h <= (hmax - 360):
                return fam
        elif h >= hmin and h < hmax:
            return fam
    return None


def analyze_texture(gray_patch):
    """Analyze a grayscale patch to classify its texture pattern.

    Returns one of: 'solid', 'horizontal_lines', 'vertical_lines', 'dots', 'cross_hatch'
    """
    if gray_patch.size < 100:
        return 'solid'

    variance = np.var(gray_patch)
    if variance < 100:
        return 'solid'

    # Edge density: horizontal vs vertical differences
    h_edges = np.abs(np.diff(gray_patch.astype(np.float32), axis=1))
    v_edges = np.abs(np.diff(gray_patch.astype(np.float32), axis=0))

    h_density = np.mean(h_edges > 20)
    v_density = np.mean(v_edges > 20)

    if h_density > 0.15 and v_density > 0.15:
        return 'cross_hatch'
    elif h_density > 0.12 and h_density > v_density * 2:
        return 'vertical_lines'  # vertical lines create horizontal edges
    elif v_density > 0.12 and v_density > h_density * 2:
        return 'horizontal_lines'  # horizontal lines create vertical edges

    # Check for dots: high variance but low directional edge density
    if variance > 200 and h_density < 0.1 and v_density < 0.1:
        return 'dots'

    if variance > 300:
        return 'cross_hatch'

    return 'solid'


def extract_legend_swatches_server(legend_path):
    """Server-side legend swatch extraction (port of client-side extractLegendSwatches).

    Returns list of swatch dicts with color, HSV, position info.
    """
    img = Image.open(legend_path).convert('RGB')
    w, h = img.size
    pixels = np.array(img)

    # Step 1: Find swatch columns by scanning for non-white vertical stripes
    scan_ys = list(range(int(h * 0.05), int(h * 0.9), max(1, h // 20)))

    all_runs = []
    for sy in scan_ys:
        row = pixels[sy, :, :]
        # Convert to HSV-like check: is this pixel colored?
        run_start = -1
        for x in range(w):
            r, g, b = int(row[x, 0]), int(row[x, 1]), int(row[x, 2])
            ph, ps, pv = rgb_to_hsv(r, g, b)
            is_colored = pv < 90 or ps > 12
            if is_colored:
                if run_start < 0:
                    run_start = x
            else:
                if run_start >= 0:
                    run_w = x - run_start
                    if run_w >= 20:
                        all_runs.append({'xStart': run_start, 'xEnd': x - 1, 'y': sy})
                    run_start = -1
        if run_start >= 0 and (w - run_start) >= 20:
            all_runs.append({'xStart': run_start, 'xEnd': w - 1, 'y': sy})

    # Cluster into swatch columns (10px bins)
    x_bins = {}
    for run in all_runs:
        run_center = round((run['xStart'] + run['xEnd']) / 2)
        run_width = run['xEnd'] - run['xStart']
        if run_width < 20 or run_width > 200:
            continue
        bin_key = round(run_center / 10) * 10
        if bin_key not in x_bins:
            x_bins[bin_key] = {'xMin': run['xStart'], 'xMax': run['xEnd'], 'count': 0}
        x_bins[bin_key]['xMin'] = min(x_bins[bin_key]['xMin'], run['xStart'])
        x_bins[bin_key]['xMax'] = max(x_bins[bin_key]['xMax'], run['xEnd'])
        x_bins[bin_key]['count'] += 1

    bin_list = [v for v in x_bins.values() if v['count'] >= len(scan_ys) * 0.2]
    bin_list.sort(key=lambda b: -b['count'])

    # Merge overlapping bins into at most 2 columns
    columns = []
    for bn in bin_list:
        if len(columns) >= 2:
            break
        merged = False
        for col in columns:
            if bn['xMin'] <= col['xMax'] + 20 and bn['xMax'] >= col['xMin'] - 20:
                col['xMin'] = min(col['xMin'], bn['xMin'])
                col['xMax'] = max(col['xMax'], bn['xMax'])
                col['count'] += bn['count']
                merged = True
                break
        if not merged:
            columns.append(dict(bn))

    if not columns:
        columns.append({'xMin': round(w * 0.08), 'xMax': round(w * 0.18)})

    # Step 2: Extract color bands from each column
    all_bands = []
    for col in columns:
        col_left = col['xMin'] + 3
        col_right = col['xMax'] - 3
        if col_right <= col_left:
            continue
        bands = _extract_bands_from_column(pixels, col_left, col_right, w, h)
        all_bands.extend(bands)

    all_bands.sort(key=lambda b: b['y'])

    # Assign band indices
    for i, band in enumerate(all_bands):
        band['band_index'] = i

    return all_bands


def _extract_bands_from_column(pixels, col_left, col_right, img_w, img_h):
    """Extract color bands from a vertical column region of the legend."""
    col_mid = round((col_left + col_right) / 2)
    col_w = col_right - col_left
    sample_w = max(4, round(col_w * 0.4))
    sample_x = col_mid - round(sample_w / 2)

    # Scan vertically: classify each row as colored or gap
    row_is_colored = []
    for y in range(img_h):
        strip = pixels[y, sample_x:sample_x + sample_w, :]
        if strip.shape[0] == 0:
            row_is_colored.append(False)
            continue
        # Median color of the strip
        strip_sorted = strip[np.argsort(np.sum(strip, axis=1))]
        med = strip_sorted[len(strip_sorted) // 2]
        mh, ms, mv = rgb_to_hsv(int(med[0]), int(med[1]), int(med[2]))
        is_colored = (ms > 10 or mv < 93) and not (ms < 5 and mv > 90)
        row_is_colored.append(is_colored)

    # Group consecutive colored rows into bands
    bands = []
    band_start = -1
    gap_count = 0
    MIN_GAP = 8

    for y in range(img_h):
        if row_is_colored[y]:
            if band_start < 0:
                band_start = y
            gap_count = 0
        else:
            if band_start >= 0:
                gap_count += 1
                if gap_count >= MIN_GAP:
                    band_end = y - gap_count
                    if band_end - band_start >= 12:
                        _finalize_band(pixels, band_start, band_end, col_left, col_right, col_mid, bands)
                    band_start = -1
                    gap_count = 0

    if band_start >= 0:
        band_end = img_h - 1 - gap_count
        if band_end - band_start >= 12:
            _finalize_band(pixels, band_start, band_end, col_left, col_right, col_mid, bands)

    return bands


def _finalize_band(pixels, y_start, y_end, col_left, col_right, col_mid, bands):
    """Finalize a color band by sampling its interior."""
    height = y_end - y_start + 1
    col_w = col_right - col_left
    y_mid = round((y_start + y_end) / 2)

    x_offsets = [-round(col_w * 0.25), 0, round(col_w * 0.25)]
    y_offsets = [y_start + round(height * 0.25), y_mid, y_start + round(height * 0.75)]

    sample_points = []
    img_h, img_w = pixels.shape[:2]
    for yo in y_offsets:
        for xo in x_offsets:
            sx = col_mid + xo
            sy = yo
            if 0 <= sx < img_w and 0 <= sy < img_h:
                r, g, b = int(pixels[sy, sx, 0]), int(pixels[sy, sx, 1]), int(pixels[sy, sx, 2])
                if r < 30 and g < 30 and b < 30:
                    continue
                ph, ps, pv = rgb_to_hsv(r, g, b)
                if ps < 5 and pv > 90:
                    continue
                sample_points.append((r, g, b))

    if len(sample_points) < 2:
        return

    sample_points.sort(key=lambda p: sum(p))
    med = sample_points[len(sample_points) // 2]
    avg_r, avg_g, avg_b = med
    h, s, v = rgb_to_hsv(avg_r, avg_g, avg_b)

    bands.append({
        'color': [avg_r, avg_g, avg_b],
        'hsv': [round(h, 1), round(s, 1), round(v, 1)],
        'y': y_mid,
        'height': height,
        'col_left': col_left,
        'col_right': col_right,
        'band_index': len(bands),
        'unit_code': '',
        'unit_name_sr': '',
        'unit_name_en': '',
        'era': '',
        'pattern': 'solid'
    })


def process_sheet(folder, sheet_data=None, force=False):
    """Process a single OGK map sheet into a zone group map.

    Args:
        folder: Sheet folder name (e.g. 'bor')
        sheet_data: Optional sheet metadata dict from geological_map_sheets.json
        force: If True, re-process even if output already exists

    Returns:
        dict with processing results or None on error
    """
    output_dir = os.path.join(OUTPUT_DIR, folder)
    zone_map_path = os.path.join(output_dir, 'zone_group_map.png')
    meta_path = os.path.join(output_dir, 'zone_groups_meta.json')

    if not force and os.path.exists(zone_map_path) and os.path.exists(meta_path):
        logger.info(f"Sheet '{folder}' already processed, skipping (use force=True to reprocess)")
        return {'status': 'exists', 'folder': folder}

    # Find karta image
    sheet_dir = os.path.join(KARTE_DIR, folder)
    if not os.path.isdir(sheet_dir):
        logger.error(f"Sheet directory not found: {sheet_dir}")
        return None

    # Find karta file
    karta_file = None
    if sheet_data and 'files' in sheet_data and 'karta' in sheet_data['files']:
        karta_file = os.path.join(sheet_dir, sheet_data['files']['karta'])
    else:
        # Auto-detect
        for f in os.listdir(sheet_dir):
            if 'karta' in f.lower() and f.lower().endswith('.jpg'):
                karta_file = os.path.join(sheet_dir, f)
                break

    if not karta_file or not os.path.isfile(karta_file):
        logger.error(f"Karta image not found for sheet '{folder}'")
        return None

    logger.info(f"Processing sheet '{folder}': {karta_file}")

    try:
        # Step 1: Load image
        img = Image.open(karta_file).convert('RGB')
        orig_w, orig_h = img.size
        arr = np.array(img)

        # Step 2: Bilateral-style blur (Gaussian preserving color transitions)
        # Use median filter (better for JPEG block artifacts than Gaussian)
        blurred = img.filter(ImageFilter.MedianFilter(size=5))
        blurred_arr = np.array(blurred)

        # Step 3: K-means color clustering (better than MEDIANCUT quantization)
        # Reshape to (N_pixels, 3) for clustering
        h_img, w_img = blurred_arr.shape[:2]
        pixels_flat = blurred_arr.reshape(-1, 3).astype(np.float32)

        n_clusters = 40  # more clusters than before (32) for finer distinctions
        kmeans = MiniBatchKMeans(
            n_clusters=n_clusters,
            batch_size=4096,
            n_init=3,
            random_state=42,
        )
        cluster_labels = kmeans.fit_predict(pixels_flat)
        quant_indices = cluster_labels.reshape(h_img, w_img)

        # Step 4: Detect boundaries (adjacent pixels with different cluster IDs)
        boundary_h = quant_indices[:, :-1] != quant_indices[:, 1:]
        boundary_v = quant_indices[:-1, :] != quant_indices[1:, :]
        boundary = np.zeros(quant_indices.shape, dtype=bool)
        boundary[:, :-1] |= boundary_h
        boundary[:, 1:] |= boundary_h
        boundary[:-1, :] |= boundary_v
        boundary[1:, :] |= boundary_v

        # Step 4b: Morphological cleanup — remove thin noise boundaries,
        # close small gaps in real boundaries
        # Use cross-shaped structuring element (less aggressive than full 3x3)
        struct_cross = ndimage.generate_binary_structure(2, 1)  # 3x3 cross
        # Opening removes thin spurious boundary pixels (JPEG block artifacts)
        boundary = binary_opening(boundary, structure=struct_cross, iterations=1)
        # Closing fills small gaps in real geological boundaries
        boundary = binary_closing(boundary, structure=struct_cross, iterations=1)

        # Step 5: Label connected non-boundary regions
        non_boundary = ~boundary
        labeled, num_features = ndimage.label(non_boundary)
        logger.info(f"  Found {num_features} raw zones")

        # Step 6: Compute zone properties using fully vectorized operations
        flat_labels = labeled.ravel()
        n_labels = num_features + 1
        zone_areas = np.bincount(flat_labels, minlength=n_labels)
        min_area = 500

        # Vectorized mean color computation using bincount
        flat_r = arr[:, :, 0].ravel().astype(np.float64)
        flat_g = arr[:, :, 1].ravel().astype(np.float64)
        flat_b = arr[:, :, 2].ravel().astype(np.float64)
        sum_r = np.bincount(flat_labels, weights=flat_r, minlength=n_labels)
        sum_g = np.bincount(flat_labels, weights=flat_g, minlength=n_labels)
        sum_b = np.bincount(flat_labels, weights=flat_b, minlength=n_labels)

        # Vectorized centroid computation
        ys_all, xs_all = np.mgrid[0:orig_h, 0:orig_w]
        flat_ys = ys_all.ravel().astype(np.float64)
        flat_xs = xs_all.ravel().astype(np.float64)
        sum_y = np.bincount(flat_labels, weights=flat_ys, minlength=n_labels)
        sum_x = np.bincount(flat_labels, weights=flat_xs, minlength=n_labels)

        # Pre-compute grayscale for texture analysis
        gray = np.mean(arr, axis=2).astype(np.uint8)

        # Filter to zones with sufficient area and build zone_data
        valid_ids = np.where(zone_areas[1:] >= min_area)[0] + 1
        logger.info(f"  {len(valid_ids)} zones with area >= {min_area}px (of {num_features} total)")

        # Compute bounding boxes for valid zones using ndimage
        # This is much faster than per-zone np.where
        all_slices = ndimage.find_objects(labeled)

        zone_data = {}
        for zone_id in valid_ids:
            area = int(zone_areas[zone_id])
            mean_r = int(round(sum_r[zone_id] / area))
            mean_g = int(round(sum_g[zone_id] / area))
            mean_b = int(round(sum_b[zone_id] / area))
            cy = int(round(sum_y[zone_id] / area))
            cx = int(round(sum_x[zone_id] / area))

            # Bounding box from find_objects
            slc = all_slices[zone_id - 1]  # 0-indexed
            bbox = [slc[0].start, slc[1].start, slc[0].stop - 1, slc[1].stop - 1]

            # Step 7: Texture analysis on a patch at centroid
            patch_half = 25
            py_s = max(0, cy - patch_half)
            py_e = min(orig_h, cy + patch_half)
            px_s = max(0, cx - patch_half)
            px_e = min(orig_w, cx + patch_half)
            gray_patch = gray[py_s:py_e, px_s:px_e]
            pattern = analyze_texture(gray_patch)

            h, s, v = rgb_to_hsv(mean_r, mean_g, mean_b)
            era_fam = classify_era(h, s, v)

            zone_data[zone_id] = {
                'zone_id': int(zone_id),
                'area': area,
                'centroid': [cy, cx],
                'bbox': bbox,
                'color': [mean_r, mean_g, mean_b],
                'hsv': [round(h, 1), round(s, 1), round(v, 1)],
                'pattern': pattern,
                'era': era_fam['era'] if era_fam else '',
                'era_color': era_fam['eraColor'] if era_fam else '#757575',
            }

        # Step 8: Match zones to legend (if legend available)
        legend_path = None
        if sheet_data and 'files' in sheet_data and 'legenda' in sheet_data['files']:
            legend_path = os.path.join(sheet_dir, sheet_data['files']['legenda'])
        else:
            for f in os.listdir(sheet_dir):
                if 'legenda' in f.lower() and f.lower().endswith('.jpg'):
                    legend_path = os.path.join(sheet_dir, f)
                    break

        legend_swatches = []
        if legend_path and os.path.isfile(legend_path):
            try:
                legend_swatches = extract_legend_swatches_server(legend_path)
                logger.info(f"  Extracted {len(legend_swatches)} legend swatches")
            except Exception as e:
                logger.warning(f"  Legend extraction failed: {e}")

        # Match each zone to best legend swatch
        for zid, zd in zone_data.items():
            zh, zs, zv = zd['hsv']
            best_swatch = None
            best_dist = float('inf')
            for sw in legend_swatches:
                sh, ss, sv = sw['hsv']
                dist = hsv_distance(zh, zs, zv, sh, ss, sv)
                if dist < best_dist:
                    best_dist = dist
                    best_swatch = sw
            if best_swatch and best_dist < 0.5:
                zd['legend_band'] = best_swatch['band_index']
                zd['legend_dist'] = round(best_dist, 3)
                if best_swatch.get('unit_code'):
                    zd['unit_code'] = best_swatch['unit_code']
            else:
                zd['legend_band'] = -1
                zd['legend_dist'] = round(best_dist, 3) if best_dist < float('inf') else -1

        # Step 9: Merge zones with the same geological unit (same legend band + same era)
        # Group by (legend_band, era) — zones matching the same legend entry
        merge_groups = {}
        for zid, zd in zone_data.items():
            key = (zd.get('legend_band', -1), zd.get('era', ''))
            if key not in merge_groups:
                merge_groups[key] = []
            merge_groups[key].append(zid)

        # Assign group IDs (1-based, 0=unclassified, max 254 groups for uint8)
        zone_groups = {}
        group_meta = []
        group_id = 1
        for key, zone_ids in merge_groups.items():
            if group_id > 254:
                break
            # Compute merged properties (area-weighted averages)
            total_area = sum(zone_data[z]['area'] for z in zone_ids)
            wr = sum(zone_data[z]['color'][0] * zone_data[z]['area'] for z in zone_ids) / total_area
            wg = sum(zone_data[z]['color'][1] * zone_data[z]['area'] for z in zone_ids) / total_area
            wb = sum(zone_data[z]['color'][2] * zone_data[z]['area'] for z in zone_ids) / total_area
            mean_color = [int(round(wr)), int(round(wg)), int(round(wb))]

            h, s, v = rgb_to_hsv(mean_color[0], mean_color[1], mean_color[2])

            # Most common pattern
            patterns = [zone_data[z]['pattern'] for z in zone_ids]
            pattern = Counter(patterns).most_common(1)[0][0]

            era = zone_data[zone_ids[0]]['era']
            era_color = zone_data[zone_ids[0]]['era_color']
            legend_band = zone_data[zone_ids[0]].get('legend_band', -1)
            legend_dist = min(zone_data[z].get('legend_dist', 999) for z in zone_ids)
            unit_code = zone_data[zone_ids[0]].get('unit_code', '')

            # Confidence based on legend match distance
            if legend_dist < 0.15:
                confidence = 'high'
            elif legend_dist < 0.35:
                confidence = 'medium'
            else:
                confidence = 'low'

            group_entry = {
                'group_id': group_id,
                'color': mean_color,
                'hsv': [round(h, 1), round(s, 1), round(v, 1)],
                'area': total_area,
                'zone_count': len(zone_ids),
                'pattern': pattern,
                'era': era,
                'era_color': era_color,
                'legend_band': legend_band,
                'legend_dist': round(legend_dist, 3) if legend_dist < 999 else -1,
                'unit_code': unit_code,
                'unit_name_sr': '',
                'unit_name_en': '',
                'confidence': confidence,
            }
            group_meta.append(group_entry)

            for zid in zone_ids:
                zone_groups[zid] = group_id
            group_id += 1

        logger.info(f"  Merged into {len(group_meta)} zone groups")

        # Step 10: Build zone group map at half resolution (vectorized)
        half_h = orig_h // 2
        half_w = orig_w // 2

        # Build a lookup table: zone_id -> group_id (vectorized mapping)
        max_label = num_features + 1
        zone_to_group = np.zeros(max_label, dtype=np.uint8)
        for zid, gid in zone_groups.items():
            if zid < max_label:
                zone_to_group[zid] = gid

        # Downsample labeled array by taking every 2nd pixel, then map
        downsampled = labeled[::2, ::2][:half_h, :half_w]
        group_map = zone_to_group[downsampled]

        # Save outputs
        os.makedirs(output_dir, exist_ok=True)

        # Save zone group map as PNG
        group_img = Image.fromarray(group_map)
        group_img.save(zone_map_path, 'PNG', optimize=True)
        map_size = os.path.getsize(zone_map_path)

        # Save zone groups metadata
        meta = {
            'folder': folder,
            'sheet_name': sheet_data['name'] if sheet_data else folder,
            'original_size': [orig_w, orig_h],
            'zone_map_size': [half_w, half_h],
            'total_zones': len(zone_data),
            'total_groups': len(group_meta),
            'groups': group_meta,
        }
        write_json_file(meta_path, meta)

        # Save enhanced legend
        if legend_swatches:
            # Augment swatches with era classification
            for sw in legend_swatches:
                sh, ss, sv = sw['hsv']
                era_fam = classify_era(sh, ss, sv)
                if era_fam and not sw.get('era'):
                    sw['era'] = era_fam['era']

            legend_path_out = os.path.join(output_dir, 'enhanced_legend.json')
            write_json_file(legend_path_out, legend_swatches)

        logger.info(f"  Done: {len(group_meta)} groups, map={map_size//1024}KB")
        return {
            'status': 'ok',
            'folder': folder,
            'total_zones': len(zone_data),
            'total_groups': len(group_meta),
            'map_size_kb': map_size // 1024,
        }

    except Exception as e:
        logger.error(f"Error processing sheet '{folder}': {e}", exc_info=True)
        return {'status': 'error', 'folder': folder, 'error': str(e)}


def process_all_sheets(force=False):
    """Process all 65 OGK map sheets."""
    sheets = load_json_file(SHEETS_JSON, default=[])

    results = []
    for i, sheet in enumerate(sheets):
        folder = sheet['folder']
        logger.info(f"[{i+1}/{len(sheets)}] Processing {folder}...")
        result = process_sheet(folder, sheet_data=sheet, force=force)
        results.append(result)

    # Summary
    ok = sum(1 for r in results if r and r.get('status') == 'ok')
    exists = sum(1 for r in results if r and r.get('status') == 'exists')
    errors = sum(1 for r in results if r is None or (r and r.get('status') == 'error'))
    logger.info(f"\nDone: {ok} processed, {exists} already existed, {errors} errors")
    return results


if __name__ == '__main__':
    import argparse

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    parser = argparse.ArgumentParser(description='Process OGK geological map sheets into zone maps')
    parser.add_argument('--folder', '-f', help='Process a single sheet folder')
    parser.add_argument('--force', action='store_true', help='Re-process even if output exists')
    parser.add_argument('--all', '-a', action='store_true', help='Process all sheets')
    args = parser.parse_args()

    if args.folder:
        # Load sheet data
        sheets = load_json_file(SHEETS_JSON, default=[])
        sheet_data = next((s for s in sheets if s['folder'] == args.folder), None)
        result = process_sheet(args.folder, sheet_data=sheet_data, force=args.force)
        if result:
            print(json.dumps(result, indent=2))
        else:
            print("Processing failed")
            sys.exit(1)
    elif args.all:
        results = process_all_sheets(force=args.force)
        ok = sum(1 for r in results if r and r.get('status') in ('ok', 'exists'))
        print(f"\nCompleted: {ok}/{len(results)} sheets")
    else:
        parser.print_help()
