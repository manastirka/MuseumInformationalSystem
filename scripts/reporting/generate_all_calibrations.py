#!/usr/bin/env python3
"""
Generate manual_calibration.json for all geo zones from enhanced_legend.json data.
This creates basic calibration entries with colors and auto-classified eras.
Descriptions will be filled in from legend images separately.
"""
import json
import os
from datetime import datetime

GEO_ZONES_DIR = os.path.join(os.path.dirname(__file__), 'data', 'geo_zones')

ERA_COLORS = {
    'Kvartar': '#8d6e63',
    'Holocen': '#8d6e63',
    'Pleistocen': '#8d6e63',
    'Neogen': '#f9a825',
    'Paleogen': '#ff8f00',
    'Kreda': '#2e7d32',
    'Jura': '#1565c0',
    'Trijas': '#9c27b0',
    'Perm': '#e65100',
    'Karbon': '#607d8b',
    'Devon': '#795548',
    'Paleozoik': '#795548',
    'Офиолити': '#00695c',
    'Магматити': '#d32f2f',
    'Метаморфити': '#78909c',
    '': '#9e9e9e'
}

ERA_NAMES_SR = {
    'Kvartar': 'Квартарне наслаге',
    'Holocen': 'Холоценске наслаге',
    'Pleistocen': 'Плеистоценске наслаге',
    'Neogen': 'Неогене наслаге',
    'Paleogen': 'Палеогене наслаге',
    'Kreda': 'Кредне творевине',
    'Jura': 'Јурске творевине',
    'Trijas': 'Тријаске творевине',
    'Perm': 'Пермске творевине',
    'Karbon': 'Карбонске творевине',
    'Devon': 'Девонске творевине',
    'Paleozoik': 'Палеозојске творевине',
    'Офиолити': 'Офиолитски комплекс',
    'Магматити': 'Магматске стене',
    'Метаморфити': 'Метаморфне стене',
    '': 'Некласификовано'
}

ERA_NAMES_EN = {
    'Kvartar': 'Quaternary deposits',
    'Holocen': 'Holocene deposits',
    'Pleistocen': 'Pleistocene deposits',
    'Neogen': 'Neogene deposits',
    'Paleogen': 'Paleogene deposits',
    'Kreda': 'Cretaceous formations',
    'Jura': 'Jurassic formations',
    'Trijas': 'Triassic formations',
    'Perm': 'Permian formations',
    'Karbon': 'Carboniferous formations',
    'Devon': 'Devonian formations',
    'Paleozoik': 'Paleozoic formations',
    'Офиолити': 'Ophiolite complex',
    'Магматити': 'Magmatic rocks',
    'Метаморфити': 'Metamorphic rocks',
    '': 'Unclassified'
}


def generate_calibration(folder_path, folder_name):
    """Generate manual_calibration.json from enhanced_legend.json."""
    enhanced_path = os.path.join(folder_path, 'enhanced_legend.json')
    calib_path = os.path.join(folder_path, 'manual_calibration.json')

    if os.path.exists(calib_path):
        return None  # Skip already calibrated

    if not os.path.exists(enhanced_path):
        return None

    with open(enhanced_path, 'r', encoding='utf-8') as f:
        bands = json.load(f)

    if not bands:
        return None

    # Filter out near-white/near-black bands (likely artifacts)
    valid_bands = []
    for band in bands:
        hsv = band.get('hsv', [0, 0, 0])
        s = hsv[1]  # saturation
        v = hsv[2]  # value
        # Skip very low saturation + very high value (near white)
        # or very low value (near black) - these are likely scan artifacts
        if s < 5 and v > 90:
            continue  # Near white
        if v < 15:
            continue  # Near black
        valid_bands.append(band)

    if not valid_bands:
        return None

    # Track era counters for unit code generation
    era_counters = {}
    entries = []

    for i, band in enumerate(valid_bands):
        era = band.get('era', '')
        color = band.get('color', [128, 128, 128])
        hsv = band.get('hsv', [0, 0, 0])

        # Generate sequential unit code per era
        if era not in era_counters:
            era_counters[era] = 0
        era_counters[era] += 1
        idx = era_counters[era]

        # Create abbreviated code
        era_abbr = {
            'Kvartar': 'Q', 'Holocen': 'Q', 'Pleistocen': 'Q',
            'Neogen': 'N', 'Paleogen': 'Pg',
            'Kreda': 'K', 'Jura': 'J', 'Trijas': 'T',
            'Perm': 'P', 'Karbon': 'C', 'Devon': 'D',
            'Paleozoik': 'Pz',
            'Офиолити': 'Of', 'Магматити': 'Mg', 'Метаморфити': 'Mt',
            '': 'X'
        }.get(era, 'X')

        unit_code = f"{era_abbr}{idx}"

        entries.append({
            'id': i + 1,
            'color': color,
            'hsv': hsv,
            'unit_code': unit_code,
            'unit_name_sr': ERA_NAMES_SR.get(era, 'Некласификовано'),
            'unit_name_en': ERA_NAMES_EN.get(era, 'Unclassified'),
            'era': era,
            'era_color': ERA_COLORS.get(era, '#9e9e9e')
        })

    calibration = {
        'folder': folder_name,
        'calibrated_at': datetime.now().isoformat(),
        'entries': entries
    }

    with open(calib_path, 'w', encoding='utf-8') as f:
        json.dump(calibration, f, ensure_ascii=False, indent=2)

    return len(entries)


def main():
    total_created = 0
    total_entries = 0
    skipped = []

    for folder_name in sorted(os.listdir(GEO_ZONES_DIR)):
        folder_path = os.path.join(GEO_ZONES_DIR, folder_name)
        if not os.path.isdir(folder_path):
            continue

        calib_path = os.path.join(folder_path, 'manual_calibration.json')
        if os.path.exists(calib_path):
            skipped.append(folder_name)
            continue

        count = generate_calibration(folder_path, folder_name)
        if count:
            total_created += 1
            total_entries += count
            print(f"  Created {folder_name}: {count} entries")

    print(f"\nDone. Created {total_created} calibration files with {total_entries} total entries.")
    print(f"Skipped (already calibrated): {', '.join(skipped)}")


if __name__ == '__main__':
    main()
