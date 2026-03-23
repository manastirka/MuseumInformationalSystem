#!/usr/bin/env python3
"""Generate data/geological_map_sheets.json from Karte/Final - Srbija/ directories."""
import json
import os
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KARTE_DIR = os.path.join(BASE_DIR, 'Karte', 'Final - Srbija')
OUTPUT_FILE = os.path.join(BASE_DIR, 'data', 'geological_map_sheets.json')

# Approximate city coordinates (lat, lon) for all 65 OGK sheets
CITY_COORDS = {
    'aleksinac':            (43.538, 21.705),
    'ali bunar':            (45.081, 20.970),
    'backa palanka':        (45.250, 19.392),
    'bela crkva':           (44.898, 21.417),
    'bela palanka':         (43.223, 22.307),
    'beograd':              (44.787, 20.449),
    'bijeljina':            (44.757, 19.214),
    'bijelo polje':         (43.029, 19.748),
    'boljevac':             (43.826, 21.951),
    'bor':                  (44.075, 22.100),
    'breznik':              (42.739, 22.904),
    'cacak':                (43.891, 20.349),
    'donji milanovac':      (44.463, 22.150),
    'gornji milanovac':     (44.014, 20.461),
    'ivanjica':             (43.581, 20.229),
    'Jasa Tomic':           (45.043, 20.850),
    'K34-22 Belogradcik':   (43.623, 22.684),
    'K34-30 Novi Pazar':    (43.137, 20.512),
    'kacanik':              (42.233, 21.253),
    'knjazevac':            (43.566, 22.257),
    'kragujevac':           (44.013, 20.911),
    'kraljevo':             (43.726, 20.689),
    'krusevac':             (43.582, 21.326),
    'kucevo':               (44.483, 21.668),
    'kumanovo':             (42.132, 21.714),
    'kursumlija':           (43.141, 21.269),
    'L34-130 Turnu Severin': (44.631, 22.656),
    'L34-64 Subotica':      (46.101, 19.665),
    'lapovo':               (44.186, 21.095),
    'leskovac':             (42.998, 21.946),
    'negotin':              (44.226, 22.531),
    'nis':                  (43.321, 21.896),
    'novi sad':             (45.252, 19.837),
    'obrenovac':            (44.654, 20.201),
    'Odzaci':               (45.509, 19.262),
    'orahovac':             (42.395, 20.661),
    'pancevo':              (44.871, 20.640),
    'paracin':              (43.859, 21.405),
    'pec i kukes':          (42.659, 20.289),
    'pirot':                (43.153, 22.586),
    'pljevlja':             (43.357, 19.357),
    'podujevo':             (42.909, 21.193),
    'pozarevac':            (44.622, 21.186),
    'prijepolje':           (43.387, 19.650),
    'Prizren':              (42.209, 20.741),
    'rozaje':               (42.839, 20.167),
    'sabac':                (44.755, 19.690),
    'sjenica':              (43.272, 20.005),
    'smederevo':            (44.663, 20.924),
    'Sombor':               (45.774, 19.113),
    'Srbobran':             (45.555, 19.796),
    'titova mitrovica':     (42.883, 20.867),
    'trgoviste':            (42.352, 22.085),
    'Urosevac':             (42.370, 21.155),
    'uzice':                (43.859, 19.849),
    'valjevo':              (44.275, 19.892),
    'visegrad':             (43.786, 19.292),
    'vladimirci':           (44.615, 19.785),
    'vlasotince':           (42.964, 22.131),
    'vranje':               (42.551, 21.889),
    'vrnjci':               (43.618, 20.892),
    'Vrsac':                (45.118, 21.299),
    'zagubica':             (44.197, 21.788),
    'zajecar':              (43.904, 22.288),
    'zvornik':              (44.386, 19.102),
}

# Display names (proper capitalization with Serbian conventions)
DISPLAY_NAMES = {
    'aleksinac':            'Aleksinac',
    'ali bunar':            'Alibunar',
    'backa palanka':        'Backa Palanka',
    'bela crkva':           'Bela Crkva',
    'bela palanka':         'Bela Palanka',
    'beograd':              'Beograd',
    'bijeljina':            'Bijeljina',
    'bijelo polje':         'Bijelo Polje',
    'boljevac':             'Boljevac',
    'bor':                  'Bor',
    'breznik':              'Breznik',
    'cacak':                'Cacak',
    'donji milanovac':      'Donji Milanovac',
    'gornji milanovac':     'Gornji Milanovac',
    'ivanjica':             'Ivanjica',
    'Jasa Tomic':           'Jasa Tomic',
    'K34-22 Belogradcik':   'Belogradcik',
    'K34-30 Novi Pazar':    'Novi Pazar',
    'kacanik':              'Kacanik',
    'knjazevac':            'Knjazevac',
    'kragujevac':           'Kragujevac',
    'kraljevo':             'Kraljevo',
    'krusevac':             'Krusevac',
    'kucevo':               'Kucevo',
    'kumanovo':             'Kumanovo',
    'kursumlija':           'Kursumlija',
    'L34-130 Turnu Severin': 'Turnu Severin',
    'L34-64 Subotica':      'Subotica',
    'lapovo':               'Lapovo',
    'leskovac':             'Leskovac',
    'negotin':              'Negotin',
    'nis':                  'Nis',
    'novi sad':             'Novi Sad',
    'obrenovac':            'Obrenovac',
    'Odzaci':               'Odzaci',
    'orahovac':             'Orahovac',
    'pancevo':              'Pancevo',
    'paracin':              'Paracin',
    'pec i kukes':          'Pec i Kukes',
    'pirot':                'Pirot',
    'pljevlja':             'Pljevlja',
    'podujevo':             'Podujevo',
    'pozarevac':            'Pozarevac',
    'prijepolje':           'Prijepolje',
    'Prizren':              'Prizren',
    'rozaje':               'Rozaje',
    'sabac':                'Sabac',
    'sjenica':              'Sjenica',
    'smederevo':            'Smederevo',
    'Sombor':               'Sombor',
    'Srbobran':             'Srbobran',
    'titova mitrovica':     'Kosovska Mitrovica',
    'trgoviste':            'Trgoviste',
    'Urosevac':             'Urosevac',
    'uzice':                'Uzice',
    'valjevo':              'Valjevo',
    'visegrad':             'Visegrad',
    'vladimirci':           'Vladimirci',
    'vlasotince':           'Vlasotince',
    'vranje':               'Vranje',
    'vrnjci':               'Vrnjci',
    'Vrsac':                'Vrsac',
    'zagubica':             'Zagubica',
    'zajecar':              'Zajecar',
    'zvornik':              'Zvornik',
}


def compute_ogk_bounds(lat, lon):
    """Compute OGK 1:100,000 grid cell bounds for given coordinates.
    Each sheet covers 20' latitude (1/3 degree) x 30' longitude (1/2 degree)."""
    south = math.floor(lat * 3) / 3.0
    north = south + 1.0 / 3.0
    west = math.floor(lon * 2) / 2.0
    east = west + 0.5
    return {
        'south': round(south, 6),
        'north': round(north, 6),
        'west': round(west, 6),
        'east': round(east, 6)
    }


def compute_ogk_code(lat, lon):
    """Compute OGK sheet code (e.g. L34-113) from coordinates."""
    bounds = compute_ogk_bounds(lat, lon)

    # Determine 1:1,000,000 sheet band (4-degree latitude bands)
    # K = 40-44N, L = 44-48N
    band_index = int(lat) // 4
    band_letter = chr(ord('A') + band_index)

    # Determine 1:1,000,000 sheet column (6-degree longitude zones)
    # Zone 34 = 18-24E
    zone_number = int(lon) // 6 + 31  # Adjusted for European convention

    # Determine sheet number within the 1:1,000,000 sheet
    band_south = band_index * 4
    band_west = (zone_number - 31) * 6

    # Row from top (0-indexed), each row = 1/3 degree
    row_from_top = int(round((band_south + 4 - bounds['north']) * 3))
    # Column from left (0-indexed), each col = 1/2 degree
    col_from_left = int(round((bounds['west'] - band_west) * 2))

    sheet_number = row_from_top * 12 + col_from_left + 1

    return f"{band_letter}{zone_number}-{sheet_number}"


def classify_file(filename):
    """Classify a JPG file as karta, legenda, profili, or stub."""
    fn_lower = filename.lower()
    if not fn_lower.endswith('.jpg'):
        return None

    if 'karta' in fn_lower or 'geolkarta' in fn_lower:
        return 'karta'
    elif 'legend' in fn_lower or 'legedn' in fn_lower:
        return 'legenda'
    elif 'profil' in fn_lower:
        return 'profili'
    elif 'stub' in fn_lower:
        return 'stub'
    return None


def scan_directory(dir_path):
    """Scan a directory and return dict of file type -> filename."""
    files = {}
    for f in os.listdir(dir_path):
        file_type = classify_file(f)
        if file_type:
            files[file_type] = f
    return files


def main():
    sheets = []

    for folder_name in sorted(os.listdir(KARTE_DIR)):
        folder_path = os.path.join(KARTE_DIR, folder_name)
        if not os.path.isdir(folder_path):
            continue

        if folder_name not in CITY_COORDS:
            print(f"WARNING: No coordinates for '{folder_name}', skipping")
            continue

        lat, lon = CITY_COORDS[folder_name]
        bounds = compute_ogk_bounds(lat, lon)
        ogk_code = compute_ogk_code(lat, lon)
        display_name = DISPLAY_NAMES.get(folder_name, folder_name)
        files = scan_directory(folder_path)

        sheet = {
            'name': display_name,
            'folder': folder_name,
            'ogk_code': ogk_code,
            'center': {
                'lat': round((bounds['south'] + bounds['north']) / 2, 6),
                'lon': round((bounds['west'] + bounds['east']) / 2, 6)
            },
            'bounds': bounds,
            'files': files
        }
        sheets.append(sheet)

    # Sort by name
    sheets.sort(key=lambda s: s['name'])

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(sheets, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(sheets)} map sheets -> {OUTPUT_FILE}")

    # Verify known codes
    for s in sheets:
        if s['folder'].startswith(('K34-', 'L34-')):
            expected_code = s['folder'].split(' ')[0]
            if s['ogk_code'] != expected_code:
                print(f"  CODE MISMATCH: {s['folder']} -> computed {s['ogk_code']}, expected {expected_code}")
            else:
                print(f"  CODE OK: {s['folder']} -> {s['ogk_code']}")


if __name__ == '__main__':
    main()
