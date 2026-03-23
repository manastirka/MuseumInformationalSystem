"""
Local GEOROC Data Manager
Reads and parses local GEOROC CSV files for geochemical data.
Data source: GEOROC 2.0 (https://georoc.eu/) - December 2024 export
"""

import os
import csv
import re
from typing import Dict, List, Optional, Tuple
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

# Path to GEOROC data folder
GEOROC_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'GEROC')

# Mapping of mineral categories to their CSV files
MINERAL_CATEGORIES = {
    'amphibole': '2024-12-SGFTFN_AMPHIBOLES.csv',
    'hornblende': '2024-12-SGFTFN_AMPHIBOLES.csv',
    'actinolite': '2024-12-SGFTFN_AMPHIBOLES.csv',
    'tremolite': '2024-12-SGFTFN_AMPHIBOLES.csv',
    'apatite': '2024-12-SGFTFN_APATITES.csv',
    'carbonate': '2024-12-SGFTFN_CARBONATES.csv',
    'calcite': '2024-12-SGFTFN_CARBONATES.csv',
    'dolomite': '2024-12-SGFTFN_CARBONATES.csv',
    'aragonite': '2024-12-SGFTFN_CARBONATES.csv',
    'siderite': '2024-12-SGFTFN_CARBONATES.csv',
    'magnesite': '2024-12-SGFTFN_CARBONATES.csv',
    'chalcogenide': '2024-12-SGFTFN_CHALCOGENIDES.csv',
    'sulfide': '2024-12-SGFTFN_CHALCOGENIDES.csv',
    'pyrite': '2024-12-SGFTFN_CHALCOGENIDES.csv',
    'galena': '2024-12-SGFTFN_CHALCOGENIDES.csv',
    'sphalerite': '2024-12-SGFTFN_CHALCOGENIDES.csv',
    'chalcopyrite': '2024-12-SGFTFN_CHALCOGENIDES.csv',
    'clay': '2024-12-SGFTFN_CLAY_MINERALS.csv',
    'kaolinite': '2024-12-SGFTFN_CLAY_MINERALS.csv',
    'montmorillonite': '2024-12-SGFTFN_CLAY_MINERALS.csv',
    'illite': '2024-12-SGFTFN_CLAY_MINERALS.csv',
    'clinopyroxene': '2024-12-SGFTFN_CLINOPYROXENES.csv',
    'augite': '2024-12-SGFTFN_CLINOPYROXENES.csv',
    'diopside': '2024-12-SGFTFN_CLINOPYROXENES.csv',
    'hedenbergite': '2024-12-SGFTFN_CLINOPYROXENES.csv',
    'feldspar': '2024-12-SGFTFN_FELDSPARS.csv',
    'plagioclase': '2024-12-SGFTFN_FELDSPARS.csv',
    'orthoclase': '2024-12-SGFTFN_FELDSPARS.csv',
    'albite': '2024-12-SGFTFN_FELDSPARS.csv',
    'anorthite': '2024-12-SGFTFN_FELDSPARS.csv',
    'microcline': '2024-12-SGFTFN_FELDSPARS.csv',
    'sanidine': '2024-12-SGFTFN_FELDSPARS.csv',
    'feldspathoid': '2024-12-SGFTFN_FELDSPATHOIDES.csv',
    'nepheline': '2024-12-SGFTFN_FELDSPATHOIDES.csv',
    'leucite': '2024-12-SGFTFN_FELDSPATHOIDES.csv',
    'sodalite': '2024-12-SGFTFN_FELDSPATHOIDES.csv',
    'garnet': '2024-12-SGFTFN_GARNETS.csv',
    'almandine': '2024-12-SGFTFN_GARNETS.csv',
    'pyrope': '2024-12-SGFTFN_GARNETS.csv',
    'grossular': '2024-12-SGFTFN_GARNETS.csv',
    'andradite': '2024-12-SGFTFN_GARNETS.csv',
    'spessartine': '2024-12-SGFTFN_GARNETS.csv',
    'ilmenite': '2024-12-SGFTFN_ILMENITES.csv',
    'mica': '2024-12-SGFTFN_MICA.csv',
    'biotite': '2024-12-SGFTFN_MICA.csv',
    'muscovite': '2024-12-SGFTFN_MICA.csv',
    'phlogopite': '2024-12-SGFTFN_MICA.csv',
    'lepidolite': '2024-12-SGFTFN_MICA.csv',
    'olivine': '2024-12-SGFTFN_OLIVINES.csv',
    'forsterite': '2024-12-SGFTFN_OLIVINES.csv',
    'fayalite': '2024-12-SGFTFN_OLIVINES.csv',
    'orthopyroxene': '2024-12-SGFTFN_ORTHOPYROXENES.csv',
    'enstatite': '2024-12-SGFTFN_ORTHOPYROXENES.csv',
    'hypersthene': '2024-12-SGFTFN_ORTHOPYROXENES.csv',
    'perovskite': '2024-12-SGFTFN_PEROVSKITES.csv',
    'pyroxene': '2024-12-SGFTFN_PYROXENES.csv',
    'quartz': '2024-12-SGFTFN_QUARTZ.csv',
    'spinel': '2024-12-SGFTFN_SPINELS.csv',
    'magnetite': '2024-12-SGFTFN_SPINELS.csv',
    'chromite': '2024-12-SGFTFN_SPINELS.csv',
    'titanite': '2024-12-SGFTFN_TITANITES.csv',
    'sphene': '2024-12-SGFTFN_TITANITES.csv',
    'zircon': '2024-12-SGFTFN_ZIRCONS.csv',
}

# Major element columns in GEOROC CSVs (wt%)
MAJOR_ELEMENT_COLUMNS = [
    'SIO2(WT%)', 'TIO2(WT%)', 'AL2O3(WT%)', 'FE2O3(WT%)', 'FE2O3T(WT%)',
    'FEO(WT%)', 'FEOT(WT%)', 'MNO(WT%)', 'MGO(WT%)', 'CAO(WT%)',
    'NA2O(WT%)', 'K2O(WT%)', 'P2O5(WT%)', 'H2O(WT%)', 'CO2(WT%)',
    'CR2O3(WT%)', 'NIO(WT%)', 'ZNO(WT%)', 'PBO(WT%)', 'CUO(WT%)',
    'BAO(WT%)', 'SRO(WT%)', 'ZRO2(WT%)', 'V2O5(WT%)'
]

# Trace element columns in GEOROC CSVs (ppm)
TRACE_ELEMENT_COLUMNS = [
    'LI(PPM)', 'BE(PPM)', 'B(PPM)', 'SC(PPM)', 'V(PPM)', 'CR(PPM)',
    'CO(PPM)', 'NI(PPM)', 'CU(PPM)', 'ZN(PPM)', 'GA(PPM)', 'GE(PPM)',
    'AS(PPM)', 'SE(PPM)', 'RB(PPM)', 'SR(PPM)', 'Y(PPM)', 'ZR(PPM)',
    'NB(PPM)', 'MO(PPM)', 'AG(PPM)', 'CD(PPM)', 'SN(PPM)', 'SB(PPM)',
    'CS(PPM)', 'BA(PPM)', 'LA(PPM)', 'CE(PPM)', 'PR(PPM)', 'ND(PPM)',
    'SM(PPM)', 'EU(PPM)', 'GD(PPM)', 'TB(PPM)', 'DY(PPM)', 'HO(PPM)',
    'ER(PPM)', 'TM(PPM)', 'YB(PPM)', 'LU(PPM)', 'HF(PPM)', 'TA(PPM)',
    'W(PPM)', 'TL(PPM)', 'PB(PPM)', 'BI(PPM)', 'TH(PPM)', 'U(PPM)'
]

# Cache for parsed data
_data_cache = {}
_cache_max_samples = 10000  # Max samples to keep in cache per mineral


def get_csv_file_for_mineral(mineral_name: str) -> Optional[str]:
    """Get the CSV file path for a mineral."""
    mineral_lower = mineral_name.lower().strip()

    # Direct match
    if mineral_lower in MINERAL_CATEGORIES:
        csv_file = MINERAL_CATEGORIES[mineral_lower]
        full_path = os.path.join(GEOROC_DATA_PATH, csv_file)
        if os.path.exists(full_path):
            return full_path

    # Partial match
    for key, csv_file in MINERAL_CATEGORIES.items():
        if key in mineral_lower or mineral_lower in key:
            full_path = os.path.join(GEOROC_DATA_PATH, csv_file)
            if os.path.exists(full_path):
                return full_path

    return None


def parse_float(value: str) -> Optional[float]:
    """Parse a float from string, handling empty and invalid values."""
    if not value or value.strip() == '':
        return None
    try:
        return float(value.strip().replace(',', '.'))
    except (ValueError, TypeError):
        return None


def calculate_statistics(values: List[float]) -> Dict:
    """Calculate mean, min, max, stdev for a list of values."""
    if not values:
        return {'mean': None, 'min': None, 'max': None, 'stdev': None, 'n': 0}

    n = len(values)
    mean = sum(values) / n
    min_val = min(values)
    max_val = max(values)

    if n > 1:
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        stdev = variance ** 0.5
    else:
        stdev = 0

    return {
        'mean': round(mean, 4),
        'min': round(min_val, 4),
        'max': round(max_val, 4),
        'stdev': round(stdev, 4),
        'n': n
    }


def get_georoc_data(mineral_name: str, max_samples: int = 5000) -> Optional[Dict]:
    """
    Get geochemical data for a mineral from local GEOROC CSV files.

    Args:
        mineral_name: Name of the mineral
        max_samples: Maximum number of samples to process (for performance)

    Returns:
        Dictionary with geochemical data or None if not found
    """
    cache_key = mineral_name.lower().strip()

    # Check cache
    if cache_key in _data_cache:
        return _data_cache[cache_key]

    csv_path = get_csv_file_for_mineral(mineral_name)
    if not csv_path:
        logger.debug(f"No GEOROC data file found for mineral: {mineral_name}")
        return None

    logger.info(f"Loading GEOROC data for {mineral_name} from {os.path.basename(csv_path)}")

    try:
        # Collect element values
        major_elements = {col: [] for col in MAJOR_ELEMENT_COLUMNS}
        trace_elements = {col: [] for col in TRACE_ELEMENT_COLUMNS}

        locations = set()
        rock_types = set()
        tectonic_settings = set()
        references = set()
        sample_count = 0

        mineral_lower = mineral_name.lower()

        with open(csv_path, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Filter by mineral name if specific mineral requested
                mineral_col = (row.get('MINERAL') or '').lower()
                if mineral_lower not in mineral_col and mineral_col not in mineral_lower:
                    # For generic category searches, include all
                    if mineral_lower not in ['amphibole', 'carbonate', 'feldspar', 'garnet',
                                             'mica', 'olivine', 'pyroxene', 'spinel', 'zircon',
                                             'clinopyroxene', 'orthopyroxene', 'chalcogenide',
                                             'sulfide', 'chalcogenide', 'clay']:
                        continue

                sample_count += 1

                # Collect metadata (handle None values)
                loc = row.get('LOCATION')
                if loc:
                    locations.add(str(loc)[:100])  # Limit length
                rock = row.get('ROCK NAME')
                if rock:
                    rock_types.add(str(rock)[:50])
                tect = row.get('TECTONIC SETTING')
                if tect:
                    tectonic_settings.add(str(tect)[:50])
                cite = row.get('CITATION')
                if cite and str(cite).startswith('['):
                    references.add(str(cite)[:100])

                # Collect major element values
                for col in MAJOR_ELEMENT_COLUMNS:
                    val = parse_float(row.get(col, ''))
                    if val is not None and 0 <= val <= 100:  # Valid wt% range
                        major_elements[col].append(val)

                # Collect trace element values
                for col in TRACE_ELEMENT_COLUMNS:
                    val = parse_float(row.get(col, ''))
                    if val is not None and val >= 0:  # Valid ppm
                        trace_elements[col].append(val)

                # Limit samples for performance
                if sample_count >= max_samples:
                    break

        if sample_count == 0:
            logger.debug(f"No matching samples found for {mineral_name}")
            return None

        # Calculate statistics for each element
        major_stats = {}

        # Mapping of column names to proper oxide names
        oxide_names = {
            'SIO2': 'SiO2', 'TIO2': 'TiO2', 'ZRO2': 'ZrO2', 'THO2': 'ThO2', 'UO2': 'UO2',
            'AL2O3': 'Al2O3', 'CR2O3': 'Cr2O3', 'LA2O3': 'La2O3', 'CE2O3': 'Ce2O3',
            'ND2O3': 'Nd2O3', 'SM2O3': 'Sm2O3', 'V2O5': 'V2O5', 'P2O5': 'P2O5',
            'FE2O3T': 'Fe2O3(T)', 'FE2O3': 'Fe2O3', 'FEOT': 'FeO(T)', 'FEO': 'FeO',
            'CAO': 'CaO', 'MGO': 'MgO', 'MNO': 'MnO', 'BAO': 'BaO', 'SRO': 'SrO',
            'PBO': 'PbO', 'NIO': 'NiO', 'ZNO': 'ZnO', 'ZNO2': 'ZnO2', 'CUO': 'CuO',
            'K2O': 'K2O', 'NA2O': 'Na2O', 'H2O': 'H2O', 'CO2': 'CO2'
        }

        for col, values in major_elements.items():
            if values:
                # Clean column name: SIO2(WT%) -> SIO2
                raw_name = col.replace('(WT%)', '').replace('(wt%)', '').strip().upper()
                element_name = oxide_names.get(raw_name, raw_name)

                stats = calculate_statistics(values)
                stats['unit'] = 'wt%'
                major_stats[element_name] = stats

        trace_stats = {}
        for col, values in trace_elements.items():
            if values:
                element_name = col.replace('(PPM)', '').replace('(ppm)', '')
                stats = calculate_statistics(values)
                stats['unit'] = 'ppm'
                trace_stats[element_name] = stats

        result = {
            'mineral_name': mineral_name,
            'source': 'GEOROC 2.0 (Local)',
            'source_file': os.path.basename(csv_path),
            'total_samples': sample_count,
            'major_elements': major_stats,
            'trace_elements': trace_stats,
            'localities': list(locations)[:20],  # Limit to 20
            'rock_types': list(rock_types)[:15],
            'tectonic_settings': list(tectonic_settings)[:10],
            'references': list(references)[:10],
            'api_note': f'Data from GEOROC 2.0 database (December 2024). Processed {sample_count} samples.'
        }

        # Cache result
        _data_cache[cache_key] = result

        return result

    except Exception as e:
        logger.error(f"Error reading GEOROC data for {mineral_name}: {e}")
        return None


def get_available_minerals() -> List[str]:
    """Get list of minerals available in local GEOROC data."""
    available = []
    for mineral, csv_file in MINERAL_CATEGORIES.items():
        full_path = os.path.join(GEOROC_DATA_PATH, csv_file)
        if os.path.exists(full_path):
            available.append(mineral)
    return sorted(set(available))


def format_for_display(data: Dict) -> Dict:
    """Format GEOROC data for display in the UI."""
    if not data:
        return None

    return {
        'source': data.get('source', 'GEOROC'),
        'total_samples': data.get('total_samples', 0),
        'major_elements': data.get('major_elements', {}),
        'trace_elements': data.get('trace_elements', {}),
        'localities': data.get('localities', []),
        'rock_types': data.get('rock_types', []),
        'tectonic_settings': data.get('tectonic_settings', []),
        'references': data.get('references', []),
        'api_note': data.get('api_note', '')
    }


# Singleton instance
_instance = None

def get_local_georoc():
    """Get singleton instance of local GEOROC data manager."""
    global _instance
    if _instance is None:
        # Check if data folder exists
        if os.path.exists(GEOROC_DATA_PATH):
            _instance = True
            logger.info(f"Local GEOROC data available at {GEOROC_DATA_PATH}")
        else:
            _instance = False
            logger.warning(f"GEOROC data folder not found: {GEOROC_DATA_PATH}")
    return _instance


if __name__ == '__main__':
    # Test
    logging.basicConfig(level=logging.INFO)

    print("Available minerals:", get_available_minerals()[:10])

    test_minerals = ['quartz', 'olivine', 'garnet', 'dolomite', 'magnetite']
    for mineral in test_minerals:
        data = get_georoc_data(mineral, max_samples=1000)
        if data:
            print(f"\n{mineral}: {data['total_samples']} samples")
            print(f"  Major elements: {list(data['major_elements'].keys())[:5]}")
            print(f"  Trace elements: {list(data['trace_elements'].keys())[:5]}")
        else:
            print(f"\n{mineral}: No data found")
