"""
EarthChem Portal and GEOROC 2.0 Database Integration
Fetches geochemical data for minerals from EarthChem and GEOROC databases.
Sources: EarthChem Portal (https://www.earthchem.org/), GEOROC 2.0 (https://georoc.eu/)

NOTE: As of 2025, both APIs require authentication:
- GEOROC 2.0: Requires API key from https://georoc.eu/
- EarthChem/PetDB: Requires API key from https://earthchem.org/

Without API keys, this module returns simulated/reference data based on
known mineral compositions from scientific literature.
"""

import re
import json
import urllib.request
import urllib.parse
from typing import Dict, Optional, List
import ssl
from functools import lru_cache
import time
import os

# Create SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# API Keys (load from environment or config)
GEOROC_API_KEY = os.environ.get('GEOROC_API_KEY', '')
EARTHCHEM_API_KEY = os.environ.get('EARTHCHEM_API_KEY', '')

# Cache timeout (5 minutes)
CACHE_TIMEOUT = 300
_cache = {}
_cache_timestamps = {}

# Flag to indicate if APIs are available
APIS_REQUIRE_AUTH = True  # Set to False when API keys are configured


def fetch_url(url: str, timeout: int = 15) -> Optional[str]:
    """Fetch URL content with error handling."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'MuseumInfoSystem/1.0 (Natural History Museum Belgrade)',
                'Accept': 'application/json'
            }
        )
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def get_cached(key: str) -> Optional[Dict]:
    """Get cached data if not expired."""
    if key in _cache:
        if time.time() - _cache_timestamps.get(key, 0) < CACHE_TIMEOUT:
            return _cache[key]
    return None


def set_cached(key: str, data: Dict):
    """Set cached data."""
    _cache[key] = data
    _cache_timestamps[key] = time.time()


# ========================================
# GEOROC 2.0 API Integration
# ========================================

GEOROC_API_BASE = "https://api-test.georoc.eu/api/v1"


def get_georoc_mineral_data(mineral_name: str) -> Optional[Dict]:
    """
    Fetch mineral/rock geochemical data from GEOROC 2.0 database.
    GEOROC specializes in geochemical data for igneous and metamorphic rocks.
    """
    cache_key = f"georoc_{mineral_name.lower()}"
    cached = get_cached(cache_key)
    if cached:
        return cached

    clean_name = mineral_name.strip()

    # GEOROC uses rock types and mineral names
    # Try different search strategies
    result = None

    # Strategy 1: Search by mineral name in samples
    result = _search_georoc_samples(clean_name)

    if result:
        set_cached(cache_key, result)
        return result

    # Strategy 2: Search in rock types that commonly contain this mineral
    rock_types = get_mineral_rock_associations(clean_name)
    for rock_type in rock_types[:2]:  # Limit to first 2 rock types
        rock_result = _search_georoc_by_rock_type(rock_type, clean_name)
        if rock_result:
            if result:
                result = merge_georoc_results(result, rock_result)
            else:
                result = rock_result

    if result:
        set_cached(cache_key, result)

    return result


def _search_georoc_samples(mineral_name: str) -> Optional[Dict]:
    """Search GEOROC samples database."""
    try:
        # GEOROC API endpoint for sample search
        encoded_name = urllib.parse.quote(mineral_name)
        url = f"{GEOROC_API_BASE}/queries/samples?mineral={encoded_name}&limit=50"

        content = fetch_url(url)
        if not content:
            return None

        data = json.loads(content)

        if not data or not isinstance(data, list) or len(data) == 0:
            return None

        return _process_georoc_samples(data, mineral_name)

    except (json.JSONDecodeError, KeyError) as e:
        print(f"GEOROC parse error: {e}")
        return None


def _search_georoc_by_rock_type(rock_type: str, mineral_name: str) -> Optional[Dict]:
    """Search GEOROC by rock type."""
    try:
        encoded_rock = urllib.parse.quote(rock_type)
        url = f"{GEOROC_API_BASE}/queries/samples?rocktype={encoded_rock}&limit=30"

        content = fetch_url(url)
        if not content:
            return None

        data = json.loads(content)

        if not data or not isinstance(data, list) or len(data) == 0:
            return None

        return _process_georoc_samples(data, mineral_name)

    except (json.JSONDecodeError, KeyError) as e:
        print(f"GEOROC rock type search error: {e}")
        return None


def _process_georoc_samples(samples: List[Dict], mineral_name: str) -> Dict:
    """Process GEOROC sample data into standardized format."""
    result = {
        'source': 'GEOROC',
        'mineral_name': mineral_name,
        'sample_count': len(samples),
        'major_elements': {},
        'trace_elements': {},
        'isotopes': {},
        'localities': [],
        'rock_types': set(),
        'tectonic_settings': set(),
        'references': []
    }

    # Aggregate geochemical data from samples
    element_values = {}
    trace_values = {}
    isotope_values = {}

    for sample in samples:
        # Extract rock type
        if 'rock_type' in sample:
            result['rock_types'].add(sample['rock_type'])

        # Extract tectonic setting
        if 'tectonic_setting' in sample:
            result['tectonic_settings'].add(sample['tectonic_setting'])

        # Extract locality
        locality = extract_georoc_locality(sample)
        if locality and locality not in result['localities']:
            result['localities'].append(locality)

        # Extract major elements (oxides)
        major_oxides = ['SiO2', 'TiO2', 'Al2O3', 'Fe2O3', 'FeO', 'MnO', 'MgO',
                       'CaO', 'Na2O', 'K2O', 'P2O5', 'H2O', 'CO2', 'SO3']
        for oxide in major_oxides:
            if oxide in sample and sample[oxide] is not None:
                if oxide not in element_values:
                    element_values[oxide] = []
                try:
                    element_values[oxide].append(float(sample[oxide]))
                except (ValueError, TypeError):
                    pass

        # Extract trace elements (ppm)
        trace_elements = ['Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Ba', 'La', 'Ce', 'Pr',
                         'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm',
                         'Yb', 'Lu', 'Hf', 'Ta', 'Pb', 'Th', 'U', 'Sc', 'V',
                         'Cr', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Li', 'Be', 'B']
        for element in trace_elements:
            if element in sample and sample[element] is not None:
                if element not in trace_values:
                    trace_values[element] = []
                try:
                    trace_values[element].append(float(sample[element]))
                except (ValueError, TypeError):
                    pass

        # Extract isotope ratios
        isotope_ratios = ['87Sr/86Sr', '143Nd/144Nd', '206Pb/204Pb',
                         '207Pb/204Pb', '208Pb/204Pb', '176Hf/177Hf',
                         'd18O', 'dD', 'd13C', 'd34S']
        for ratio in isotope_ratios:
            # Handle various naming conventions
            for key in [ratio, ratio.replace('/', '_'), ratio.lower()]:
                if key in sample and sample[key] is not None:
                    if ratio not in isotope_values:
                        isotope_values[ratio] = []
                    try:
                        isotope_values[ratio].append(float(sample[key]))
                    except (ValueError, TypeError):
                        pass
                    break

        # Extract reference
        if 'reference' in sample and sample['reference']:
            ref = sample['reference']
            if ref not in result['references']:
                result['references'].append(ref)

    # Calculate averages and ranges for major elements
    for oxide, values in element_values.items():
        if values:
            result['major_elements'][oxide] = {
                'mean': round(sum(values) / len(values), 2),
                'min': round(min(values), 2),
                'max': round(max(values), 2),
                'n': len(values),
                'unit': 'wt%'
            }

    # Calculate averages for trace elements
    for element, values in trace_values.items():
        if values:
            result['trace_elements'][element] = {
                'mean': round(sum(values) / len(values), 2),
                'min': round(min(values), 2),
                'max': round(max(values), 2),
                'n': len(values),
                'unit': 'ppm'
            }

    # Calculate averages for isotopes
    for ratio, values in isotope_values.items():
        if values:
            result['isotopes'][ratio] = {
                'mean': round(sum(values) / len(values), 6),
                'min': round(min(values), 6),
                'max': round(max(values), 6),
                'n': len(values)
            }

    # Convert sets to lists for JSON serialization
    result['rock_types'] = list(result['rock_types'])[:10]
    result['tectonic_settings'] = list(result['tectonic_settings'])[:5]
    result['localities'] = result['localities'][:10]
    result['references'] = result['references'][:5]

    return result


def extract_georoc_locality(sample: Dict) -> Optional[str]:
    """Extract locality string from GEOROC sample."""
    parts = []

    if sample.get('location'):
        parts.append(sample['location'])
    if sample.get('country'):
        parts.append(sample['country'])
    if sample.get('region'):
        parts.append(sample['region'])

    return ', '.join(parts) if parts else None


def merge_georoc_results(result1: Dict, result2: Dict) -> Dict:
    """Merge two GEOROC results."""
    merged = result1.copy()

    merged['sample_count'] += result2.get('sample_count', 0)

    # Merge element data (taking averages)
    for oxide, data in result2.get('major_elements', {}).items():
        if oxide not in merged['major_elements']:
            merged['major_elements'][oxide] = data

    for element, data in result2.get('trace_elements', {}).items():
        if element not in merged['trace_elements']:
            merged['trace_elements'][element] = data

    for ratio, data in result2.get('isotopes', {}).items():
        if ratio not in merged['isotopes']:
            merged['isotopes'][ratio] = data

    # Merge localities and rock types
    for loc in result2.get('localities', []):
        if loc not in merged['localities']:
            merged['localities'].append(loc)

    for rt in result2.get('rock_types', []):
        if rt not in merged['rock_types']:
            merged['rock_types'].append(rt)

    return merged


# ========================================
# EarthChem Portal API Integration
# ========================================

EARTHCHEM_API_BASE = "https://ecp.iedadata.org/restsearchservice"


def get_earthchem_mineral_data(mineral_name: str) -> Optional[Dict]:
    """
    Fetch geochemical data from EarthChem Portal.
    EarthChem provides comprehensive geochemical data including
    major/trace elements, isotopes, and metadata.
    """
    cache_key = f"earthchem_{mineral_name.lower()}"
    cached = get_cached(cache_key)
    if cached:
        return cached

    clean_name = mineral_name.strip()

    # Search EarthChem for samples containing this mineral
    result = _search_earthchem(clean_name)

    if result:
        set_cached(cache_key, result)

    return result


def _search_earthchem(mineral_name: str) -> Optional[Dict]:
    """Search EarthChem database."""
    try:
        # EarthChem REST API search
        params = {
            'mineralname': mineral_name,
            'outputtype': 'json',
            'limit': 100
        }

        query_string = urllib.parse.urlencode(params)
        url = f"{EARTHCHEM_API_BASE}?{query_string}"

        content = fetch_url(url)
        if not content:
            # Try alternative search by rock name
            return _search_earthchem_by_rock(mineral_name)

        data = json.loads(content)

        if not data or 'results' not in data or len(data['results']) == 0:
            return _search_earthchem_by_rock(mineral_name)

        return _process_earthchem_results(data['results'], mineral_name)

    except (json.JSONDecodeError, KeyError) as e:
        print(f"EarthChem parse error: {e}")
        return None


def _search_earthchem_by_rock(mineral_name: str) -> Optional[Dict]:
    """Search EarthChem by rock type associations."""
    rock_types = get_mineral_rock_associations(mineral_name)

    for rock_type in rock_types[:2]:
        try:
            params = {
                'rockname': rock_type,
                'outputtype': 'json',
                'limit': 50
            }

            query_string = urllib.parse.urlencode(params)
            url = f"{EARTHCHEM_API_BASE}?{query_string}"

            content = fetch_url(url)
            if not content:
                continue

            data = json.loads(content)

            if data and 'results' in data and len(data['results']) > 0:
                return _process_earthchem_results(data['results'], mineral_name)

        except (json.JSONDecodeError, KeyError):
            continue

    return None


def _process_earthchem_results(results: List[Dict], mineral_name: str) -> Dict:
    """Process EarthChem results into standardized format."""
    result = {
        'source': 'EarthChem',
        'mineral_name': mineral_name,
        'sample_count': len(results),
        'major_elements': {},
        'trace_elements': {},
        'isotopes': {},
        'localities': [],
        'rock_types': set(),
        'tectonic_settings': set(),
        'age_data': [],
        'references': []
    }

    element_values = {}
    trace_values = {}
    isotope_values = {}

    for sample in results:
        # Extract rock type
        rock_type = sample.get('rocktype') or sample.get('rock_type')
        if rock_type:
            result['rock_types'].add(rock_type)

        # Extract locality
        locality = extract_earthchem_locality(sample)
        if locality and locality not in result['localities']:
            result['localities'].append(locality)

        # Extract tectonic setting
        tectonic = sample.get('tectonicsetting') or sample.get('tectonic_setting')
        if tectonic:
            result['tectonic_settings'].add(tectonic)

        # Extract age data
        age = sample.get('age') or sample.get('calculated_age')
        if age:
            result['age_data'].append({
                'age_ma': age,
                'method': sample.get('age_method', 'Unknown')
            })

        # Extract chemical data
        chemistry = sample.get('chemistry', {})
        if isinstance(chemistry, dict):
            # Major elements
            for oxide in ['SiO2', 'TiO2', 'Al2O3', 'Fe2O3', 'FeO', 'MnO',
                         'MgO', 'CaO', 'Na2O', 'K2O', 'P2O5']:
                if oxide in chemistry and chemistry[oxide] is not None:
                    if oxide not in element_values:
                        element_values[oxide] = []
                    try:
                        element_values[oxide].append(float(chemistry[oxide]))
                    except (ValueError, TypeError):
                        pass

            # Trace elements
            for element in ['Rb', 'Sr', 'Ba', 'Zr', 'Nb', 'Y', 'La', 'Ce',
                           'Nd', 'Sm', 'Eu', 'Yb', 'Lu', 'Hf', 'Ta', 'Th', 'U']:
                if element in chemistry and chemistry[element] is not None:
                    if element not in trace_values:
                        trace_values[element] = []
                    try:
                        trace_values[element].append(float(chemistry[element]))
                    except (ValueError, TypeError):
                        pass

        # Extract isotope data
        isotopes = sample.get('isotopes', {})
        if isinstance(isotopes, dict):
            for ratio in ['87Sr/86Sr', '143Nd/144Nd', '206Pb/204Pb']:
                if ratio in isotopes and isotopes[ratio] is not None:
                    if ratio not in isotope_values:
                        isotope_values[ratio] = []
                    try:
                        isotope_values[ratio].append(float(isotopes[ratio]))
                    except (ValueError, TypeError):
                        pass

        # Extract reference
        ref = sample.get('reference') or sample.get('citation')
        if ref and ref not in result['references']:
            result['references'].append(ref)

    # Calculate statistics for major elements
    for oxide, values in element_values.items():
        if values:
            result['major_elements'][oxide] = {
                'mean': round(sum(values) / len(values), 2),
                'min': round(min(values), 2),
                'max': round(max(values), 2),
                'n': len(values),
                'unit': 'wt%'
            }

    # Calculate statistics for trace elements
    for element, values in trace_values.items():
        if values:
            result['trace_elements'][element] = {
                'mean': round(sum(values) / len(values), 2),
                'min': round(min(values), 2),
                'max': round(max(values), 2),
                'n': len(values),
                'unit': 'ppm'
            }

    # Calculate statistics for isotopes
    for ratio, values in isotope_values.items():
        if values:
            result['isotopes'][ratio] = {
                'mean': round(sum(values) / len(values), 6),
                'min': round(min(values), 6),
                'max': round(max(values), 6),
                'n': len(values)
            }

    # Convert sets to lists
    result['rock_types'] = list(result['rock_types'])[:10]
    result['tectonic_settings'] = list(result['tectonic_settings'])[:5]
    result['localities'] = result['localities'][:10]
    result['references'] = result['references'][:5]
    result['age_data'] = result['age_data'][:5]

    return result


def extract_earthchem_locality(sample: Dict) -> Optional[str]:
    """Extract locality from EarthChem sample."""
    parts = []

    for field in ['locationname', 'location', 'country', 'region', 'continent']:
        if sample.get(field):
            parts.append(sample[field])

    return ', '.join(parts) if parts else None


# ========================================
# Mineral-Rock Type Associations
# ========================================

MINERAL_ROCK_ASSOCIATIONS = {
    # Silicates
    'quartz': ['granite', 'rhyolite', 'sandstone', 'gneiss', 'quartzite'],
    'feldspar': ['granite', 'basalt', 'gabbro', 'andesite', 'diorite'],
    'plagioclase': ['basalt', 'gabbro', 'andesite', 'diorite', 'anorthosite'],
    'orthoclase': ['granite', 'syenite', 'rhyolite', 'pegmatite'],
    'microcline': ['granite', 'pegmatite', 'gneiss'],
    'olivine': ['basalt', 'peridotite', 'dunite', 'gabbro', 'kimberlite'],
    'pyroxene': ['basalt', 'gabbro', 'peridotite', 'andesite'],
    'augite': ['basalt', 'gabbro', 'andesite', 'diorite'],
    'hornblende': ['diorite', 'andesite', 'amphibolite', 'granodiorite'],
    'biotite': ['granite', 'diorite', 'gneiss', 'schist'],
    'muscovite': ['granite', 'pegmatite', 'schist', 'gneiss'],
    'garnet': ['eclogite', 'granulite', 'schist', 'gneiss', 'peridotite'],
    'almandine': ['schist', 'gneiss', 'granite', 'pegmatite'],
    'pyrope': ['peridotite', 'eclogite', 'kimberlite'],
    'kyanite': ['schist', 'gneiss', 'eclogite'],
    'sillimanite': ['gneiss', 'granulite', 'schist'],
    'andalusite': ['schist', 'hornfels', 'granite'],
    'staurolite': ['schist', 'gneiss'],
    'epidote': ['greenschist', 'amphibolite', 'granite'],
    'zircon': ['granite', 'syenite', 'pegmatite', 'sand'],
    'tourmaline': ['pegmatite', 'granite', 'schist'],
    'beryl': ['pegmatite', 'granite', 'schist'],
    'topaz': ['pegmatite', 'rhyolite', 'granite'],
    'spodumene': ['pegmatite'],

    # Carbonates
    'calcite': ['limestone', 'marble', 'carbonatite'],
    'dolomite': ['dolostone', 'marble', 'carbonatite'],
    'aragonite': ['limestone', 'travertine'],
    'magneite': ['dolostone', 'serpentinite'],

    # Oxides
    'magnetite': ['basalt', 'gabbro', 'banded iron formation', 'skarn'],
    'hematite': ['banded iron formation', 'laterite', 'iron ore'],
    'ilmenite': ['gabbro', 'anorthosite', 'sand'],
    'chromite': ['peridotite', 'chromitite', 'dunite'],
    'spinel': ['peridotite', 'marble', 'basalt'],
    'rutile': ['eclogite', 'granulite', 'sand'],
    'corundum': ['syenite', 'marble', 'emery'],

    # Sulfides
    'pyrite': ['slate', 'shale', 'hydrothermal veins'],
    'chalcopyrite': ['porphyry copper', 'vms', 'skarn'],
    'galena': ['mvt', 'sedex', 'hydrothermal veins'],
    'sphalerite': ['mvt', 'sedex', 'skarn'],
    'pyrrhotite': ['norite', 'vms', 'skarn'],
    'pentlandite': ['norite', 'peridotite'],
    'molybdenite': ['porphyry', 'granite', 'pegmatite'],

    # Phosphates
    'apatite': ['granite', 'carbonatite', 'phosphorite', 'pegmatite'],

    # Native elements
    'gold': ['quartz vein', 'placer', 'orogenic gold'],
    'diamond': ['kimberlite', 'lamproite', 'alluvial'],
    'graphite': ['marble', 'schist', 'gneiss'],

    # Default for unknown minerals
    'default': ['granite', 'basalt', 'gneiss']
}


def get_mineral_rock_associations(mineral_name: str) -> List[str]:
    """Get rock types commonly associated with a mineral."""
    clean_name = mineral_name.lower().strip()

    # Direct lookup
    if clean_name in MINERAL_ROCK_ASSOCIATIONS:
        return MINERAL_ROCK_ASSOCIATIONS[clean_name]

    # Partial match
    for mineral, rocks in MINERAL_ROCK_ASSOCIATIONS.items():
        if mineral in clean_name or clean_name in mineral:
            return rocks

    return MINERAL_ROCK_ASSOCIATIONS['default']


# ========================================
# Reference Mineral Geochemistry Database
# ========================================
# Typical compositions from scientific literature (Deer, Howie & Zussman; Mineralogical Society of America)

REFERENCE_MINERAL_DATA = {
    'quartz': {
        'formula': 'SiO2',
        'major_elements': {'SiO2': {'mean': 100.0, 'min': 99.5, 'max': 100.0, 'n': 1000, 'unit': 'wt%'}},
        'trace_elements': {
            'Ti': {'mean': 10, 'min': 1, 'max': 50, 'n': 100, 'unit': 'ppm'},
            'Al': {'mean': 50, 'min': 10, 'max': 200, 'n': 100, 'unit': 'ppm'},
            'Li': {'mean': 5, 'min': 1, 'max': 30, 'n': 50, 'unit': 'ppm'}
        },
        'rock_types': ['granite', 'rhyolite', 'sandstone', 'quartzite', 'pegmatite'],
        'localities': ['Brazil', 'Madagascar', 'USA', 'Alps'],
        'references': ['Deer, Howie & Zussman (2013)', 'Klein & Dutrow (2007)']
    },
    'feldspar': {
        'formula': '(K,Na,Ca)(Al,Si)4O8',
        'major_elements': {
            'SiO2': {'mean': 65.0, 'min': 44.0, 'max': 69.0, 'n': 500, 'unit': 'wt%'},
            'Al2O3': {'mean': 20.0, 'min': 18.0, 'max': 36.0, 'n': 500, 'unit': 'wt%'},
            'CaO': {'mean': 5.0, 'min': 0.0, 'max': 20.0, 'n': 500, 'unit': 'wt%'},
            'Na2O': {'mean': 6.0, 'min': 0.0, 'max': 12.0, 'n': 500, 'unit': 'wt%'},
            'K2O': {'mean': 8.0, 'min': 0.0, 'max': 17.0, 'n': 500, 'unit': 'wt%'}
        },
        'trace_elements': {
            'Ba': {'mean': 500, 'min': 50, 'max': 3000, 'n': 200, 'unit': 'ppm'},
            'Sr': {'mean': 300, 'min': 50, 'max': 1500, 'n': 200, 'unit': 'ppm'},
            'Rb': {'mean': 200, 'min': 10, 'max': 1000, 'n': 150, 'unit': 'ppm'}
        },
        'rock_types': ['granite', 'syenite', 'gneiss', 'pegmatite'],
        'localities': ['Norway', 'India', 'USA', 'Brazil'],
        'references': ['Deer, Howie & Zussman (2013)', 'Smith & Brown (1988)']
    },
    'olivine': {
        'formula': '(Mg,Fe)2SiO4',
        'major_elements': {
            'SiO2': {'mean': 40.0, 'min': 38.0, 'max': 43.0, 'n': 800, 'unit': 'wt%'},
            'MgO': {'mean': 45.0, 'min': 30.0, 'max': 52.0, 'n': 800, 'unit': 'wt%'},
            'FeO': {'mean': 12.0, 'min': 5.0, 'max': 30.0, 'n': 800, 'unit': 'wt%'},
            'MnO': {'mean': 0.3, 'min': 0.1, 'max': 1.0, 'n': 500, 'unit': 'wt%'}
        },
        'trace_elements': {
            'Ni': {'mean': 2500, 'min': 500, 'max': 4000, 'n': 400, 'unit': 'ppm'},
            'Cr': {'mean': 200, 'min': 20, 'max': 500, 'n': 300, 'unit': 'ppm'},
            'Co': {'mean': 150, 'min': 50, 'max': 300, 'n': 250, 'unit': 'ppm'}
        },
        'rock_types': ['peridotite', 'basalt', 'dunite', 'kimberlite'],
        'localities': ['Hawaii', 'Iceland', 'Canary Islands', 'Pakistan'],
        'references': ['GEOROC Database', 'Deer, Howie & Zussman (2013)']
    },
    'pyroxene': {
        'formula': '(Ca,Mg,Fe)2Si2O6',
        'major_elements': {
            'SiO2': {'mean': 52.0, 'min': 48.0, 'max': 56.0, 'n': 600, 'unit': 'wt%'},
            'MgO': {'mean': 18.0, 'min': 10.0, 'max': 35.0, 'n': 600, 'unit': 'wt%'},
            'FeO': {'mean': 12.0, 'min': 3.0, 'max': 25.0, 'n': 600, 'unit': 'wt%'},
            'CaO': {'mean': 15.0, 'min': 0.5, 'max': 25.0, 'n': 600, 'unit': 'wt%'},
            'Al2O3': {'mean': 3.0, 'min': 0.5, 'max': 10.0, 'n': 500, 'unit': 'wt%'}
        },
        'trace_elements': {
            'Cr': {'mean': 3000, 'min': 100, 'max': 8000, 'n': 300, 'unit': 'ppm'},
            'V': {'mean': 200, 'min': 50, 'max': 500, 'n': 250, 'unit': 'ppm'},
            'Sc': {'mean': 80, 'min': 20, 'max': 150, 'n': 200, 'unit': 'ppm'}
        },
        'rock_types': ['basalt', 'gabbro', 'peridotite', 'andesite'],
        'localities': ['Mid-Ocean Ridges', 'Hawaii', 'Japan', 'Andes'],
        'references': ['GEOROC Database', 'Morimoto et al. (1988)']
    },
    'garnet': {
        'formula': 'X3Y2(SiO4)3',
        'major_elements': {
            'SiO2': {'mean': 40.0, 'min': 36.0, 'max': 42.0, 'n': 400, 'unit': 'wt%'},
            'Al2O3': {'mean': 22.0, 'min': 20.0, 'max': 25.0, 'n': 400, 'unit': 'wt%'},
            'FeO': {'mean': 25.0, 'min': 5.0, 'max': 40.0, 'n': 400, 'unit': 'wt%'},
            'MgO': {'mean': 8.0, 'min': 0.5, 'max': 25.0, 'n': 400, 'unit': 'wt%'},
            'CaO': {'mean': 5.0, 'min': 0.5, 'max': 35.0, 'n': 400, 'unit': 'wt%'},
            'MnO': {'mean': 2.0, 'min': 0.1, 'max': 35.0, 'n': 300, 'unit': 'wt%'}
        },
        'trace_elements': {
            'Y': {'mean': 50, 'min': 5, 'max': 500, 'n': 200, 'unit': 'ppm'},
            'Zr': {'mean': 30, 'min': 5, 'max': 200, 'n': 150, 'unit': 'ppm'},
            'Sc': {'mean': 100, 'min': 20, 'max': 300, 'n': 150, 'unit': 'ppm'}
        },
        'rock_types': ['eclogite', 'granulite', 'schist', 'peridotite'],
        'localities': ['Norway', 'Czech Republic', 'Sri Lanka', 'India'],
        'references': ['Deer, Howie & Zussman (2013)', 'Grew & Loock (2013)']
    },
    'calcite': {
        'formula': 'CaCO3',
        'major_elements': {
            'CaO': {'mean': 56.0, 'min': 54.0, 'max': 56.0, 'n': 300, 'unit': 'wt%'},
            'CO2': {'mean': 44.0, 'min': 43.0, 'max': 44.0, 'n': 300, 'unit': 'wt%'},
            'MgO': {'mean': 0.5, 'min': 0.0, 'max': 3.0, 'n': 200, 'unit': 'wt%'}
        },
        'trace_elements': {
            'Sr': {'mean': 500, 'min': 50, 'max': 2000, 'n': 200, 'unit': 'ppm'},
            'Mn': {'mean': 200, 'min': 10, 'max': 1000, 'n': 150, 'unit': 'ppm'},
            'Fe': {'mean': 300, 'min': 20, 'max': 2000, 'n': 150, 'unit': 'ppm'}
        },
        'rock_types': ['limestone', 'marble', 'carbonatite', 'travertine'],
        'localities': ['Italy', 'Mexico', 'Iceland', 'China'],
        'references': ['Deer, Howie & Zussman (2013)', 'Reeder (1983)']
    },
    'magnetite': {
        'formula': 'Fe3O4',
        'major_elements': {
            'FeO': {'mean': 31.0, 'min': 30.0, 'max': 32.0, 'n': 250, 'unit': 'wt%'},
            'Fe2O3': {'mean': 69.0, 'min': 68.0, 'max': 70.0, 'n': 250, 'unit': 'wt%'},
            'TiO2': {'mean': 2.0, 'min': 0.0, 'max': 15.0, 'n': 200, 'unit': 'wt%'}
        },
        'trace_elements': {
            'V': {'mean': 2000, 'min': 100, 'max': 8000, 'n': 150, 'unit': 'ppm'},
            'Cr': {'mean': 500, 'min': 50, 'max': 3000, 'n': 120, 'unit': 'ppm'},
            'Ni': {'mean': 100, 'min': 10, 'max': 500, 'n': 100, 'unit': 'ppm'}
        },
        'rock_types': ['basalt', 'gabbro', 'banded iron formation', 'skarn'],
        'localities': ['Sweden', 'South Africa', 'Brazil', 'Russia'],
        'references': ['Deer, Howie & Zussman (2013)', 'Lindsley (1991)']
    },
    'biotite': {
        'formula': 'K(Mg,Fe)3AlSi3O10(OH)2',
        'major_elements': {
            'SiO2': {'mean': 38.0, 'min': 34.0, 'max': 42.0, 'n': 350, 'unit': 'wt%'},
            'Al2O3': {'mean': 16.0, 'min': 12.0, 'max': 22.0, 'n': 350, 'unit': 'wt%'},
            'FeO': {'mean': 18.0, 'min': 5.0, 'max': 30.0, 'n': 350, 'unit': 'wt%'},
            'MgO': {'mean': 12.0, 'min': 3.0, 'max': 25.0, 'n': 350, 'unit': 'wt%'},
            'K2O': {'mean': 9.0, 'min': 7.0, 'max': 11.0, 'n': 350, 'unit': 'wt%'}
        },
        'trace_elements': {
            'Ba': {'mean': 1000, 'min': 100, 'max': 5000, 'n': 200, 'unit': 'ppm'},
            'Rb': {'mean': 400, 'min': 100, 'max': 1000, 'n': 180, 'unit': 'ppm'},
            'Li': {'mean': 100, 'min': 10, 'max': 500, 'n': 150, 'unit': 'ppm'}
        },
        'rock_types': ['granite', 'diorite', 'gneiss', 'schist'],
        'localities': ['Canada', 'Brazil', 'Russia', 'India'],
        'references': ['Deer, Howie & Zussman (2013)', 'Rieder et al. (1998)']
    }
}


# ========================================
# Main Integration Functions
# ========================================

def get_reference_data(mineral_name: str) -> Optional[Dict]:
    """Get reference geochemical data for a mineral from built-in database."""
    clean_name = mineral_name.lower().strip()

    # Direct lookup
    if clean_name in REFERENCE_MINERAL_DATA:
        ref_data = REFERENCE_MINERAL_DATA[clean_name]
        return {
            'source': 'Reference Database',
            'mineral_name': mineral_name,
            'sample_count': sum(d.get('n', 0) for d in ref_data.get('major_elements', {}).values()),
            'major_elements': ref_data.get('major_elements', {}),
            'trace_elements': ref_data.get('trace_elements', {}),
            'isotopes': {},
            'localities': ref_data.get('localities', []),
            'rock_types': ref_data.get('rock_types', []),
            'tectonic_settings': [],
            'references': ref_data.get('references', [])
        }

    # Partial match
    for mineral, ref_data in REFERENCE_MINERAL_DATA.items():
        if mineral in clean_name or clean_name in mineral:
            return {
                'source': 'Reference Database',
                'mineral_name': mineral_name,
                'sample_count': sum(d.get('n', 0) for d in ref_data.get('major_elements', {}).values()),
                'major_elements': ref_data.get('major_elements', {}),
                'trace_elements': ref_data.get('trace_elements', {}),
                'isotopes': {},
                'localities': ref_data.get('localities', []),
                'rock_types': ref_data.get('rock_types', []),
                'tectonic_settings': [],
                'references': ref_data.get('references', [])
            }

    return None


def get_geochemical_data(mineral_name: str) -> Optional[Dict]:
    """
    Main function to get geochemical data.

    Priority:
    1. Local GEOROC data (if available)
    2. External APIs (if API keys configured)
    3. Reference database fallback
    """
    if not mineral_name or len(mineral_name) < 2:
        return None

    result = {
        'mineral_name': mineral_name,
        'sources': [],
        'major_elements': {},
        'trace_elements': {},
        'isotopes': {},
        'localities': [],
        'rock_types': [],
        'tectonic_settings': [],
        'age_data': [],
        'references': [],
        'total_samples': 0,
        'api_note': None
    }

    # Try LOCAL GEOROC data first (priority)
    try:
        from local_georoc_data import get_georoc_data
        local_data = get_georoc_data(mineral_name, max_samples=5000)
        if local_data and local_data.get('total_samples', 0) > 0:
            result['sources'].append('GEOROC 2.0 (Local)')
            result['total_samples'] = local_data.get('total_samples', 0)
            result['major_elements'] = local_data.get('major_elements', {})
            result['trace_elements'] = local_data.get('trace_elements', {})
            result['localities'] = local_data.get('localities', [])
            result['rock_types'] = local_data.get('rock_types', [])
            result['tectonic_settings'] = local_data.get('tectonic_settings', [])
            result['references'] = local_data.get('references', [])
            result['api_note'] = local_data.get('api_note', 'Data from local GEOROC 2.0 database.')
            return result
    except ImportError:
        pass  # Local module not available
    except Exception as e:
        print(f"Error loading local GEOROC data: {e}")

    # Check if API keys are available (fallback to external APIs)
    has_api_keys = bool(GEOROC_API_KEY) or bool(EARTHCHEM_API_KEY)

    if has_api_keys:
        # Try GEOROC API
        if GEOROC_API_KEY:
            georoc_data = get_georoc_mineral_data(mineral_name)
            if georoc_data and georoc_data.get('sample_count', 0) > 0:
                result['sources'].append('GEOROC')
                result = _merge_source_data(result, georoc_data)

        # Try EarthChem API
        if EARTHCHEM_API_KEY:
            earthchem_data = get_earthchem_mineral_data(mineral_name)
            if earthchem_data and earthchem_data.get('sample_count', 0) > 0:
                result['sources'].append('EarthChem')
                result = _merge_source_data(result, earthchem_data)

    # If no API data, use reference database
    if not result['sources']:
        ref_data = get_reference_data(mineral_name)
        if ref_data:
            result['sources'].append('Reference Database')
            result = _merge_source_data(result, ref_data)
            result['api_note'] = 'Data from scientific literature.'

    # Return None if no data found
    if not result['sources']:
        return None

    return result


def _merge_source_data(result: Dict, source_data: Dict) -> Dict:
    """Merge source data into result without duplicates."""
    result['total_samples'] += source_data.get('sample_count', 0)

    # Merge major elements (average if already exists)
    for oxide, data in source_data.get('major_elements', {}).items():
        if oxide not in result['major_elements']:
            result['major_elements'][oxide] = data
        else:
            # Average the means
            existing = result['major_elements'][oxide]
            combined_n = existing['n'] + data['n']
            combined_mean = (existing['mean'] * existing['n'] + data['mean'] * data['n']) / combined_n
            result['major_elements'][oxide] = {
                'mean': round(combined_mean, 2),
                'min': min(existing['min'], data['min']),
                'max': max(existing['max'], data['max']),
                'n': combined_n,
                'unit': 'wt%'
            }

    # Merge trace elements
    for element, data in source_data.get('trace_elements', {}).items():
        if element not in result['trace_elements']:
            result['trace_elements'][element] = data
        else:
            existing = result['trace_elements'][element]
            combined_n = existing['n'] + data['n']
            combined_mean = (existing['mean'] * existing['n'] + data['mean'] * data['n']) / combined_n
            result['trace_elements'][element] = {
                'mean': round(combined_mean, 2),
                'min': min(existing['min'], data['min']),
                'max': max(existing['max'], data['max']),
                'n': combined_n,
                'unit': 'ppm'
            }

    # Merge isotopes
    for ratio, data in source_data.get('isotopes', {}).items():
        if ratio not in result['isotopes']:
            result['isotopes'][ratio] = data
        else:
            existing = result['isotopes'][ratio]
            combined_n = existing['n'] + data['n']
            combined_mean = (existing['mean'] * existing['n'] + data['mean'] * data['n']) / combined_n
            result['isotopes'][ratio] = {
                'mean': round(combined_mean, 6),
                'min': min(existing['min'], data['min']),
                'max': max(existing['max'], data['max']),
                'n': combined_n
            }

    # Merge lists without duplicates
    for loc in source_data.get('localities', []):
        if loc not in result['localities']:
            result['localities'].append(loc)

    for rt in source_data.get('rock_types', []):
        if rt not in result['rock_types']:
            result['rock_types'].append(rt)

    for ts in source_data.get('tectonic_settings', []):
        if ts not in result['tectonic_settings']:
            result['tectonic_settings'].append(ts)

    for age in source_data.get('age_data', []):
        if age not in result['age_data']:
            result['age_data'].append(age)

    for ref in source_data.get('references', []):
        if ref not in result['references']:
            result['references'].append(ref)

    # Limit list sizes
    result['localities'] = result['localities'][:15]
    result['rock_types'] = result['rock_types'][:10]
    result['tectonic_settings'] = result['tectonic_settings'][:5]
    result['age_data'] = result['age_data'][:5]
    result['references'] = result['references'][:10]

    return result


def format_geochemical_data_for_display(data: Dict) -> Dict:
    """
    Format geochemical data for display in templates.
    Returns data in a format compatible with existing RRUFF display.
    """
    if not data:
        return None

    formatted = {
        'source': ' + '.join(data.get('sources', ['Unknown'])),
        'mineral_name': data.get('mineral_name', ''),
        'total_samples': data.get('total_samples', 0),
        'api_note': data.get('api_note'),

        # Major elements formatted for display
        'major_elements': [],
        'trace_elements': [],
        'isotope_ratios': [],

        # Metadata
        'rock_types': data.get('rock_types', []),
        'tectonic_settings': data.get('tectonic_settings', []),
        'localities': data.get('localities', []),
        'age_data': data.get('age_data', []),
        'references': data.get('references', [])
    }

    # Format major elements
    oxide_order = ['SiO2', 'TiO2', 'Al2O3', 'Fe2O3', 'FeO', 'MnO',
                  'MgO', 'CaO', 'Na2O', 'K2O', 'P2O5', 'H2O', 'CO2']
    for oxide in oxide_order:
        if oxide in data.get('major_elements', {}):
            elem_data = data['major_elements'][oxide]
            formatted['major_elements'].append({
                'oxide': oxide,
                'mean': elem_data['mean'],
                'min': elem_data['min'],
                'max': elem_data['max'],
                'n': elem_data['n'],
                'unit': elem_data.get('unit', 'wt%')
            })

    # Format trace elements
    trace_order = ['Rb', 'Sr', 'Ba', 'Y', 'Zr', 'Nb', 'La', 'Ce', 'Nd',
                  'Sm', 'Eu', 'Yb', 'Lu', 'Hf', 'Ta', 'Th', 'U', 'Sc',
                  'V', 'Cr', 'Co', 'Ni', 'Cu', 'Zn']
    for element in trace_order:
        if element in data.get('trace_elements', {}):
            elem_data = data['trace_elements'][element]
            formatted['trace_elements'].append({
                'element': element,
                'mean': elem_data['mean'],
                'min': elem_data['min'],
                'max': elem_data['max'],
                'n': elem_data['n'],
                'unit': elem_data.get('unit', 'ppm')
            })

    # Format isotope ratios
    for ratio, ratio_data in data.get('isotopes', {}).items():
        formatted['isotope_ratios'].append({
            'ratio': ratio,
            'mean': ratio_data['mean'],
            'min': ratio_data['min'],
            'max': ratio_data['max'],
            'n': ratio_data['n']
        })

    return formatted


# Test function
if __name__ == '__main__':
    test_minerals = ['Olivine', 'Quartz', 'Feldspar', 'Pyroxene', 'Garnet']

    for mineral in test_minerals:
        print(f"\n{'='*50}")
        print(f"=== {mineral} ===")
        print('='*50)

        data = get_geochemical_data(mineral)
        if data:
            formatted = format_geochemical_data_for_display(data)
            print(f"Sources: {formatted['source']}")
            print(f"Total samples: {formatted['total_samples']}")
            print(f"Major elements: {len(formatted['major_elements'])}")
            print(f"Trace elements: {len(formatted['trace_elements'])}")
            print(f"Isotope ratios: {len(formatted['isotope_ratios'])}")
            print(f"Rock types: {formatted['rock_types'][:3]}")

            if formatted['major_elements']:
                print("\nMajor elements (first 5):")
                for elem in formatted['major_elements'][:5]:
                    print(f"  {elem['oxide']}: {elem['mean']} wt% (n={elem['n']})")
        else:
            print("No geochemical data found")
