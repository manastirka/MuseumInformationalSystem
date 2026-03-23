"""
Locality Data Module
Provides locality information with geocoding support for accurate coordinates.
"""

import re
import json
import os
import urllib.request
import urllib.parse
from typing import Dict, Optional, List
import ssl
import time

# SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Cache file for geocoded locations
CACHE_FILE = os.path.join(os.path.dirname(__file__), 'data', 'locality_geocache.json')

# Geocoding cache (in memory)
_geocache = {}


def _load_geocache():
    """Load geocache from file."""
    global _geocache
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                _geocache = json.load(f)
        except:
            _geocache = {}
    return _geocache


def _save_geocache():
    """Save geocache to file."""
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(_geocache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving geocache: {e}")


def fetch_url(url: str, timeout: int = 10) -> Optional[str]:
    """Fetch URL content with error handling."""
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'MuseumInfoSystem/1.0 (Natural History Museum Belgrade; contact@nhmbeo.rs)'}
        )
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def geocode_locality(locality_name: str) -> Optional[Dict]:
    """
    Geocode a locality name using Nominatim (OpenStreetMap).
    Returns dict with lat, lon or None if not found.
    """
    global _geocache

    if not _geocache:
        _load_geocache()

    # Check cache first
    cache_key = locality_name.lower().strip()
    if cache_key in _geocache:
        cached = _geocache[cache_key]
        if cached:  # Valid cached result
            return cached
        # None means we tried and failed - don't retry
        return None

    # Parse locality name - try to extract useful parts
    # Format: "Place, Region, Country" or just "Place, Country"
    parts = [p.strip() for p in locality_name.split(',')]

    # Build search queries to try
    queries = []

    # Try full name first
    queries.append(locality_name)

    # If has country suffix, try with country
    if len(parts) >= 2:
        # Try first part + country
        queries.append(f"{parts[0]}, {parts[-1]}")
        # Try just first part
        queries.append(parts[0])

    # Nominatim API endpoint
    base_url = "https://nominatim.openstreetmap.org/search"

    for query in queries:
        # Add country context if Serbian locality
        search_query = query
        if not any(c in query.lower() for c in ['srbija', 'serbia', 'makedonija', 'macedonia',
                                                  'slovenija', 'slovenia', 'bosna', 'bosnia', 'bih',
                                                  'hrvatska', 'croatia', 'crna gora', 'montenegro']):
            # Try adding Serbia as context for unspecified localities
            search_query = f"{query}, Serbia"

        params = {
            'q': search_query,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1,
        }

        url = f"{base_url}?{urllib.parse.urlencode(params)}"

        try:
            # Rate limiting - Nominatim requires max 1 request per second
            time.sleep(1.1)

            content = fetch_url(url, timeout=15)
            if content:
                results = json.loads(content)
                if results and len(results) > 0:
                    result = results[0]
                    coords = {
                        'lat': float(result.get('lat', 0)),
                        'lon': float(result.get('lon', 0)),
                        'display_name': result.get('display_name', ''),
                        'type': result.get('type', ''),
                    }
                    # Cache the result
                    _geocache[cache_key] = coords
                    _save_geocache()
                    return coords
        except Exception as e:
            print(f"Geocoding error for {query}: {e}")

    # Cache the failure to avoid retrying
    _geocache[cache_key] = None
    _save_geocache()
    return None


# Known Serbian/Balkan mining localities with verified scientific data
# Coordinates will be supplemented by geocoding
LOCALITY_DATABASE = {
    # === SERBIA ===
    'stari trg': {
        'name': 'Stari Trg, Trepča',
        'name_sr': 'Стари Трг, Трепча',
        'country': 'Srbija',
        'type': 'Pb-Zn-Ag rudnik',
        'mindat': 'https://www.mindat.org/loc-5589.html',
    },
    'trepča': {
        'name': 'Trepča Mine Complex',
        'name_sr': 'Рудник Трепча',
        'country': 'Srbija',
        'type': 'Pb-Zn-Ag rudnik',
        'mindat': 'https://www.mindat.org/loc-5589.html',
    },
    'bor': {
        'name': 'Bor Copper Mine',
        'name_sr': 'Рудник Бор',
        'country': 'Srbija',
        'type': 'Cu-Au rudnik',
        'mindat': 'https://www.mindat.org/loc-5562.html',
    },
    'majdanpek': {
        'name': 'Majdanpek Copper Mine',
        'name_sr': 'Рудник Мајданпек',
        'country': 'Srbija',
        'type': 'Cu rudnik',
        'mindat': 'https://www.mindat.org/loc-17549.html',
    },
    'rudnik': {
        'name': 'Rudnik Mine',
        'name_sr': 'Рудник',
        'country': 'Srbija',
        'type': 'Pb-Zn-Ag rudnik',
        'mindat': 'https://www.mindat.org/loc-25898.html',
    },
    'kopaonik': {
        'name': 'Kopaonik',
        'name_sr': 'Копаоник',
        'country': 'Srbija',
        'type': 'Rudno područje',
        'mindat': 'https://www.mindat.org/loc-211440.html',
    },
    'suvo rudište': {
        'name': 'Suvo Rudište, Kopaonik',
        'name_sr': 'Суво Рудиште',
        'country': 'Srbija',
        'type': 'Pb-Zn rudnik',
        'mindat': 'https://www.mindat.org/loc-211440.html',
    },
    'lece': {
        'name': 'Lece',
        'name_sr': 'Леце',
        'country': 'Srbija',
        'type': 'Au-Ag rudnik',
        'mindat': 'https://www.mindat.org/loc-17613.html',
    },
    'zajača': {
        'name': 'Zajača',
        'name_sr': 'Зајача',
        'country': 'Srbija',
        'type': 'Sb rudnik',
        'mindat': 'https://www.mindat.org/loc-32276.html',
    },
    'stolice': {
        'name': 'Stolice, Krupanj',
        'name_sr': 'Столице',
        'country': 'Srbija',
        'type': 'Sb rudnik',
        'mindat': 'https://www.mindat.org/loc-251920.html',
    },
    'avala': {
        'name': 'Avala',
        'name_sr': 'Авала',
        'country': 'Srbija',
        'type': 'Hg nalazište',
        'mindat': 'https://www.mindat.org/loc-205433.html',
    },
    'bukulja': {
        'name': 'Bukulja',
        'name_sr': 'Букуља',
        'country': 'Srbija',
        'type': 'Pegmatiti',
        'mindat': 'https://www.mindat.org/loc-205442.html',
    },
    'kosmaj': {
        'name': 'Kosmaj',
        'name_sr': 'Космај',
        'country': 'Srbija',
        'type': 'Magmatski kompleks',
    },
    'fruška gora': {
        'name': 'Fruška Gora',
        'name_sr': 'Фрушка Гора',
        'country': 'Srbija',
        'type': 'Planina',
    },
    'zlatibor': {
        'name': 'Zlatibor',
        'name_sr': 'Златибор',
        'country': 'Srbija',
        'type': 'Ultramafiti',
    },
    'novo brdo': {
        'name': 'Novo Brdo',
        'name_sr': 'Ново Брдо',
        'country': 'Srbija',
        'type': 'Pb-Zn-Ag rudnik',
        'mindat': 'https://www.mindat.org/loc-245099.html',
    },

    # === SLOVENIA ===
    'mežica': {
        'name': 'Mežica',
        'name_sr': 'Межица',
        'country': 'Slovenija',
        'type': 'Pb-Zn rudnik',
        'mindat': 'https://www.mindat.org/loc-7308.html',
    },
    'mezice': {
        'name': 'Mežica',
        'name_sr': 'Межица',
        'country': 'Slovenija',
        'type': 'Pb-Zn rudnik',
        'mindat': 'https://www.mindat.org/loc-7308.html',
    },
    'idrija': {
        'name': 'Idrija',
        'name_sr': 'Идрија',
        'country': 'Slovenija',
        'type': 'Hg rudnik',
        'mindat': 'https://www.mindat.org/loc-7304.html',
    },

    # === NORTH MACEDONIA ===
    'alšar': {
        'name': 'Alšar',
        'name_sr': 'Алшар',
        'country': 'Makedonija',
        'type': 'Tl-As-Sb nalazište',
        'mindat': 'https://www.mindat.org/loc-3174.html',
    },
    'prilep': {
        'name': 'Prilep',
        'name_sr': 'Прилеп',
        'country': 'Makedonija',
        'type': 'Mermer',
        'mindat': 'https://www.mindat.org/loc-23066.html',
    },

    # === BOSNIA ===
    'busovača': {
        'name': 'Busovača',
        'name_sr': 'Бусовача',
        'country': 'BiH',
        'type': 'Kvarc, hijalofan',
        'mindat': 'https://www.mindat.org/loc-7843.html',
    },
    'busovaca': {
        'name': 'Busovača',
        'name_sr': 'Бусовача',
        'country': 'BiH',
        'type': 'Kvarc, hijalofan',
        'mindat': 'https://www.mindat.org/loc-7843.html',
    },
    'vareš': {
        'name': 'Vareš',
        'name_sr': 'Вареш',
        'country': 'BiH',
        'type': 'Fe rudnik',
        'mindat': 'https://www.mindat.org/loc-7836.html',
    },
}


def normalize_locality_name(name: str) -> str:
    """Normalize locality name for lookup."""
    if not name:
        return ''
    # Lowercase and remove extra spaces
    normalized = ' '.join(name.lower().split())
    # Remove common suffixes
    normalized = re.sub(r',\s*(srbija|serbia|makedonija|macedonia|slovenija|slovenia|bih|bosna|bosnia).*$', '', normalized)
    # Remove diacritics for matching
    normalized = normalized.replace('č', 'c').replace('ć', 'c').replace('š', 's').replace('ž', 'z').replace('đ', 'dj')
    return normalized.strip()


def find_locality_info(locality_name: str) -> Optional[Dict]:
    """Find locality information from local database."""
    if not locality_name:
        return None

    normalized = normalize_locality_name(locality_name)

    # Direct match
    for key, data in LOCALITY_DATABASE.items():
        key_normalized = normalize_locality_name(key)
        if key_normalized in normalized or normalized in key_normalized:
            return data

    # Try to match parts
    parts = normalized.replace(',', ' ').split()
    for part in parts:
        if len(part) > 3:
            for key, data in LOCALITY_DATABASE.items():
                key_normalized = normalize_locality_name(key)
                if part == key_normalized or (len(part) > 5 and part in key_normalized):
                    return data

    return None


def get_locality_data(locality_name: str, include_coordinates: bool = True) -> Optional[Dict]:
    """
    Get locality data with optional geocoding.
    Returns basic info from database + geocoded coordinates.
    """
    if not locality_name:
        return None

    # Try local database first
    local_data = find_locality_info(locality_name)

    result = {}
    if local_data:
        result = {**local_data, 'source': 'database'}

    # Get coordinates via geocoding if requested
    if include_coordinates:
        coords = geocode_locality(locality_name)
        if coords:
            result['coordinates'] = {
                'lat': coords['lat'],
                'lon': coords['lon'],
            }
            result['geocoded_name'] = coords.get('display_name', '')
            if not result.get('source'):
                result['source'] = 'geocoded'

    return result if result else None


def get_locality_data_local_only(locality_name: str) -> Optional[Dict]:
    """
    Get locality data without making HTTP requests.
    Only returns data from local database + cached geocoding results.
    """
    if not locality_name:
        return None

    # Load cache
    if not _geocache:
        _load_geocache()

    # Try local database
    local_data = find_locality_info(locality_name)

    result = {}
    if local_data:
        result = {**local_data, 'source': 'database'}

    # Check geocache for coordinates
    cache_key = locality_name.lower().strip()
    if cache_key in _geocache and _geocache[cache_key]:
        coords = _geocache[cache_key]
        result['coordinates'] = {
            'lat': coords['lat'],
            'lon': coords['lon'],
        }
        if not result.get('source'):
            result['source'] = 'geocoded'

    return result if result else None


def batch_geocode_localities(localities: List[str], progress_callback=None) -> Dict[str, Dict]:
    """
    Geocode multiple localities.
    Returns dict of locality_name -> coordinates.
    """
    results = {}
    total = len(localities)

    for i, loc in enumerate(localities):
        if progress_callback:
            progress_callback(i + 1, total, loc)

        coords = geocode_locality(loc)
        if coords:
            results[loc] = coords

    return results


# Initialize cache on module load
_load_geocache()


# Test
if __name__ == '__main__':
    test_localities = [
        'Stari Trg, Trepča, Srbija',
        'Majdanpek, Srbija',
        'Mežice, Slovenija',
        'Alšar, Makedonija',
        'Bor, Srbija',
        'Busovača, BiH',
    ]

    for loc in test_localities:
        print(f"\n=== {loc} ===")
        data = get_locality_data(loc)
        if data:
            print(f"  Name: {data.get('name', loc)}")
            print(f"  Type: {data.get('type', 'N/A')}")
            if data.get('coordinates'):
                print(f"  Coordinates: {data['coordinates']['lat']:.4f}, {data['coordinates']['lon']:.4f}")
            print(f"  Source: {data.get('source')}")
        else:
            print("  No data found")
