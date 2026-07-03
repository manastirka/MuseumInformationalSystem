"""Support helpers for dashboard weather and website-news integrations."""

import logging
import os
import re
import threading
import tempfile
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import certifi
import requests
from bs4 import BeautifulSoup

from runtime_lock_utils import load_json_file, write_json_file

logger = logging.getLogger(__name__)

DEFAULT_WEATHER_CONDITION = os.environ.get('WEATHER_FALLBACK_CONDITION', 'none').strip().lower() or 'none'
FORCED_WEATHER_CONDITION = os.environ.get('WEATHER_FORCE_CONDITION', '').strip().lower()

RHMZ_WARNING_URL = 'https://www.hidmet.gov.rs/ciril/upozorenja/index.php'
RHMZ_FORECAST_URL = 'https://www.hidmet.gov.rs/latin/prognoza/stanica.php?mp_id=13274'
RHMZ_OBSERVED_URL = 'https://www.hidmet.gov.rs/latin/osmotreni/index.php'

_weather_cache = {
    'data': None,
    'timestamp': None,
    'cache_date': None,
}
_weather_cache_lock = threading.Lock()
_weather_forecast_cache = {
    'data': None,
    'timestamp': None,
    'cache_date': None,
}
_weather_forecast_cache_lock = threading.Lock()
_weather_daily_bundle_cache = {
    'data': None,
    'timestamp': None,
    'cache_date': None,
}
_weather_daily_bundle_lock = threading.Lock()
_rhmz_warning_cache = {
    'data': None,
    'timestamp': None,
}
_rhmz_warning_cache_lock = threading.Lock()
_website_news_cache = {
    'data': None,
    'timestamp': None,
}
_website_news_cache_lock = threading.Lock()
_website_news_refresh_lock = threading.Lock()
_WEBSITE_NEWS_CACHE_TTL_SECONDS = int(os.environ.get('WEBSITE_NEWS_CACHE_TTL_SECONDS', '300'))
_WEBSITE_NEWS_CONNECT_TIMEOUT_SECONDS = float(os.environ.get('WEBSITE_NEWS_CONNECT_TIMEOUT_SECONDS', '2'))
_WEBSITE_NEWS_READ_TIMEOUT_SECONDS = float(os.environ.get('WEBSITE_NEWS_READ_TIMEOUT_SECONDS', '3'))


def _default_weather_cache_path():
    """Return a runtime-writable weather cache path outside the repository tree."""
    configured_path = os.environ.get('WEATHER_FORECAST_CACHE_PATH', '').strip()
    if configured_path:
        return Path(configured_path)

    runtime_root = Path(
        os.environ.get(
            'MUSEUM_RUNTIME_CACHE_DIR',
            os.path.join(tempfile.gettempdir(), 'museum_info_system_runtime'),
        )
    )
    return runtime_root / 'weather_forecast_daily_cache.json'


_WEATHER_FORECAST_CACHE_PATH = _default_weather_cache_path()

_WMO_DESCRIPTIONS = {
    0: 'Ведро', 1: 'Претежно ведро', 2: 'Делимично облачно', 3: 'Облачно',
    45: 'Магла', 48: 'Магла са мразом',
    51: 'Слаба роса', 53: 'Умерена роса', 55: 'Густа роса',
    56: 'Ледена роса', 57: 'Густа ледена роса',
    61: 'Слаба киша', 63: 'Умерена киша', 65: 'Јака киша',
    66: 'Ледена киша', 67: 'Јака ледена киша',
    71: 'Слаб снег', 73: 'Умерен снег', 75: 'Јак снег',
    77: 'Снежна зрна', 80: 'Слаби пљускови', 81: 'Умерени пљускови',
    82: 'Јаки пљускови', 85: 'Слаби снежни пљускови', 86: 'Јаки снежни пљускови',
    95: 'Грмљавина', 96: 'Грмљавина са градом', 99: 'Јака грмљавина са градом',
}

_SR_WEEKDAYS_SHORT = ['Пон', 'Уто', 'Сре', 'Чет', 'Пет', 'Суб', 'Нед']
_SR_WEEKDAYS_FULL = ['Понедељак', 'Уторак', 'Среда', 'Четвртак', 'Петак', 'Субота', 'Недеља']
_RHMZ_SECTION_META = [
    {'key': 'meteorological', 'title': 'Метеоролошка упозорења'},
]
_RHMZ_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'sr,en;q=0.8',
}
# RHMZ (hidmet.gov.rs) now serves certificates that chain to Let's Encrypt's
# new 'ISRG Root YR', which is missing from older system / certifi CA bundles
# and causes SSLError on every weather fetch. The bundled gen-y roots are merged
# into the standard trust store so verification succeeds without disabling it.
_ISRG_GEN_Y_ROOTS_PATH = Path(__file__).resolve().parent / 'certs' / 'isrg_gen_y_roots.pem'
_rhmz_ca_bundle_lock = threading.Lock()
_rhmz_ca_bundle_state = {'path': None}


def _rhmz_ca_bundle():
    """Return a CA bundle path that also trusts Let's Encrypt's gen-y roots."""
    with _rhmz_ca_bundle_lock:
        cached = _rhmz_ca_bundle_state.get('path')
        if cached and os.path.exists(cached):
            return cached

        base_bundle = certifi.where()
        try:
            extra_roots = _ISRG_GEN_Y_ROOTS_PATH.read_text()
        except OSError as exc:
            logger.warning("ISRG gen-y roots unavailable (%s); using stock CA bundle.", exc)
            _rhmz_ca_bundle_state['path'] = base_bundle
            return base_bundle

        try:
            base_text = Path(base_bundle).read_text()
        except OSError as exc:
            logger.warning("Base CA bundle unreadable (%s); using bundled roots only.", exc)
            base_text = ''

        runtime_root = _WEATHER_FORECAST_CACHE_PATH.parent
        try:
            runtime_root.mkdir(parents=True, exist_ok=True)
            combined_path = runtime_root / 'rhmz_ca_bundle.pem'
            combined_path.write_text(base_text + '\n' + extra_roots)
            resolved = str(combined_path)
        except OSError as exc:
            logger.warning("Combined CA bundle write failed (%s); using stock CA bundle.", exc)
            resolved = base_bundle

        _rhmz_ca_bundle_state['path'] = resolved
        return resolved
_RHMZ_FORECAST_RULES = [
    (('vedro', 'suncan', 'sunčan', 'ведро', 'сунчан'), 'clear', 'Ведро'),
    (('nepogod', 'grmljav', 'olu', 'непогод', 'грмљав', 'олу'), 'thunderstorm', 'Грмљавина'),
    (('slab sneg', 'sneg', 'susnez', 'vejav', 'снег', 'суснеж', 'вејав'), 'snow', 'Снег'),
    (
        ('kisa koja se ledi', 'ledena kisa', 'slaba kisa', 'kisa', 'pljus', 'rosulj', 'киша', 'пљус', 'росуљ'),
        'rain',
        'Киша',
    ),
    (('magla', 'магла'), 'fog', 'Магла'),
    (
        ('oblac', 'obla', 'delimicno', 'delimično', 'promenljivo', 'pretežno', 'pretezn', 'umereno', 'jak vetar', 'облач', 'делимично', 'променљиво', 'претежно', 'умерено', 'јак ветар'),
        'cloudy',
        'Облачно',
    ),
]
# RHMZ forecast icons are numeric GIFs (repository/ikonice/prognoza/<N>.gif) and
# the forecast row carries only a generic alt="Pojava". This legend maps each
# icon code to (animation condition, Serbian-Cyrillic description); it was
# harvested from RHMZ's own descriptive alt text across station pages.
_RHMZ_FORECAST_ICON_CODES = {
    1: ('clear', 'Ведро'),
    2: ('clear', 'Сунчано'),
    3: ('clear', 'Претежно сунчано'),
    4: ('cloudy', 'Мало и умерено облачно'),
    5: ('rain', 'Послеподневни пљускови'),
    6: ('rain', 'Могући пљускови'),
    7: ('cloudy', 'Облачно'),
    8: ('rain', 'Слаба киша'),
    9: ('rain', 'Киша'),
    10: ('cloudy', 'Променљиво облачно'),
    11: ('rain', 'Пљусак'),
    12: ('thunderstorm', 'Пљусак и грмљавина'),
    13: ('snow', 'Суснежица'),
    14: ('snow', 'Слаб снег'),
    15: ('snow', 'Снег'),
    16: ('rain', 'Киша која се леди'),
    17: ('fog', 'Магла'),
    18: ('cloudy', 'Јак ветар'),
    19: ('rain', 'Могући краткотрајни пљускови'),
    20: ('thunderstorm', 'Непогоде'),
}


def _normalize_space(value):
    """Collapse whitespace into a single-space string."""
    if value is None:
        return ''
    return re.sub(r'\s+', ' ', str(value)).strip()


def _weather_condition_from_wmo(code):
    """Map WMO weather code to the internal animation condition."""
    if code in (0, 1):
        return 'clear'
    if code in (2, 3):
        return 'cloudy'
    if code in (45, 48):
        return 'fog'
    if code in (51, 53, 55, 56, 57):
        return 'drizzle'
    if code in (61, 63, 65, 66, 67, 80, 81, 82):
        return 'rain'
    if code in (71, 73, 75, 77, 85, 86):
        return 'snow'
    if code in (95, 96, 99):
        return 'thunderstorm'
    return DEFAULT_WEATHER_CONDITION


def _weather_snapshot_from_wmo(code, temperature=None, windspeed=None):
    """Build a normalized weather payload from a WMO code and measurements."""
    condition = _weather_condition_from_wmo(code)
    description = _WMO_DESCRIPTIONS.get(code, condition.capitalize())
    return {
        'condition': condition,
        'temperature': temperature,
        'windspeed': windspeed,
        'description': description,
    }


def _weather_fallback_snapshot():
    """Return the configured fallback weather payload."""
    return {
        'condition': DEFAULT_WEATHER_CONDITION,
        'temperature': None,
        'windspeed': None,
        'description': '',
    }


def _parse_float(value):
    """Convert a dashboard numeric string to float when possible."""
    normalized = _normalize_space(value).replace(',', '.')
    if not normalized or normalized == '-':
        return None

    match = re.search(r'-?\d+(?:\.\d+)?', normalized)
    if not match:
        return None

    try:
        return float(match.group(0))
    except ValueError:
        return None


def _format_display_number(value):
    """Return an int when the float is whole, otherwise keep one decimal."""
    if value is None:
        return None
    rounded = round(float(value), 1)
    if float(rounded).is_integer():
        return int(rounded)
    return rounded


def _rhmz_description_to_snapshot(description, *, temperature=None, windspeed=None):
    """Map RHMZ textual descriptions to dashboard weather conditions."""
    normalized = _normalize_space(description).lower()
    if not normalized or normalized == '-':
        return _weather_fallback_snapshot() | {
            'temperature': temperature,
            'windspeed': windspeed,
            'description': '',
        }

    for keywords, condition, label in _RHMZ_FORECAST_RULES:
        if any(keyword in normalized for keyword in keywords):
            return {
                'condition': condition,
                'temperature': temperature,
                'windspeed': windspeed,
                'description': label,
            }

    return {
        'condition': DEFAULT_WEATHER_CONDITION,
        'temperature': temperature,
        'windspeed': windspeed,
        'description': description,
    }


def _rhmz_icon_to_description(img):
    """Infer a forecast description from an RHMZ icon tag."""
    candidates = [
        img.get('title'),
        img.get('alt'),
        Path(urlparse(img.get('src') or '').path).stem,
    ]
    normalized = _normalize_space(' '.join(filter(None, candidates))).lower()
    normalized = normalized.replace('_', ' ').replace('-', ' ')

    if not normalized or normalized == 'pojava':
        return ''

    if 'pretezno vedro' in normalized or 'pretežno vedro' in normalized:
        return 'Претежно ведро'
    if 'pretezno suncano' in normalized or 'pretežno sunčano' in normalized:
        return 'Претежно сунчано'
    if 'vedro' in normalized:
        return 'Ведро'
    if 'suncano' in normalized or 'sunčano' in normalized:
        return 'Сунчано'
    if 'malo i umereno oblacno' in normalized or 'malo i umereno oblačno' in normalized:
        return 'Мало и умерено облачно'
    if 'promenljivo oblacno' in normalized or 'promenljivo oblačno' in normalized:
        return 'Променљиво облачно'
    if 'delimicno oblacno' in normalized or 'delimično oblačno' in normalized:
        return 'Делимично облачно'
    if 'oblacno' in normalized or 'oblačno' in normalized:
        return 'Облачно'
    if 'slaba kisa' in normalized or 'slaba kiša' in normalized:
        return 'Слаба киша'
    if 'kisa koja se ledi' in normalized or 'kiša koja se ledi' in normalized:
        return 'Киша која се леди'
    if 'poslepodnevni pljuskovi' in normalized:
        return 'Послеподневни пљускови'
    if 'moguci kratkotrajni pljuskovi' in normalized or 'mogući kratkotrajni pljuskovi' in normalized:
        return 'Могући краткотрајни пљускови'
    if 'moguci pljuskovi' in normalized or 'mogući pljuskovi' in normalized:
        return 'Могући пљускови'
    if 'pljusak i grmljavina' in normalized:
        return 'Пљусак и грмљавина'
    if 'pljusak' in normalized:
        return 'Пљусак'
    if 'kisa' in normalized or 'kiša' in normalized:
        return 'Киша'
    if 'susnezica' in normalized or 'susnežica' in normalized:
        return 'Суснежица'
    if 'slab sneg' in normalized:
        return 'Слаб снег'
    if 'sneg' in normalized:
        return 'Снег'
    if 'magla' in normalized:
        return 'Магла'
    if 'jak vetar' in normalized:
        return 'Јак ветар'
    if 'nepogode' in normalized:
        return 'Непогоде'

    return ''


def _rhmz_forecast_icon_snapshot(img):
    """Resolve an RHMZ forecast icon to {'condition', 'description'} or None."""
    stem = Path(urlparse(img.get('src') or '').path).stem
    if stem.isdigit():
        mapping = _RHMZ_FORECAST_ICON_CODES.get(int(stem))
        if mapping:
            return {'condition': mapping[0], 'description': mapping[1]}

    # Fall back to descriptive alt/title text when the numeric code is unknown.
    description = _rhmz_icon_to_description(img)
    if description:
        snapshot = _rhmz_description_to_snapshot(description)
        return {
            'condition': snapshot['condition'],
            'description': snapshot['description'] or description,
        }
    return None


def _extract_current_weather_payload(data):
    """Normalize current weather payloads from legacy and current Open-Meteo formats."""
    current = data.get('current') or {}
    if current:
        return {
            'code': current.get('weather_code', current.get('weathercode', -1)),
            'temperature': current.get('temperature_2m', current.get('temperature')),
            'windspeed': current.get('wind_speed_10m', current.get('windspeed')),
        }

    current_weather = data.get('current_weather') or {}
    return {
        'code': current_weather.get('weathercode', current_weather.get('weather_code', -1)),
        'temperature': current_weather.get('temperature', current_weather.get('temperature_2m')),
        'windspeed': current_weather.get('windspeed', current_weather.get('wind_speed_10m')),
    }


def _format_weather_day_label(date_value):
    """Return Serbian display labels for one ISO date string."""
    try:
        dt = datetime.strptime(date_value, '%Y-%m-%d')
    except (TypeError, ValueError):
        return {
            'date': date_value,
            'short_label': date_value,
            'day_name': date_value,
            'date_label': date_value,
        }

    return {
        'date': date_value,
        'short_label': _SR_WEEKDAYS_SHORT[dt.weekday()],
        'day_name': _SR_WEEKDAYS_FULL[dt.weekday()],
        'date_label': dt.strftime('%d.%m.'),
    }


def _warning_has_content(message):
    """Heuristic for whether an RHMZ section contains an active warning."""
    normalized = _normalize_space(message).lower()
    if not normalized:
        return False

    no_warning_markers = (
        'тренутно нема',
        'нема актуелног',
        'нема важећег',
        'без упозорења',
    )
    return not any(marker in normalized for marker in no_warning_markers)


def _get_cached_weather_snapshot():
    """Return the current-weather snapshot for the active day when available."""
    with _weather_cache_lock:
        cached_data = _weather_cache['data']
        cached_date = _weather_cache.get('cache_date')

    if not cached_data or cached_date != datetime.now().strftime('%Y-%m-%d'):
        return None, False

    return cached_data, True


def _today_weather_cache_key():
    """Return the daily cache key for the current local date."""
    return datetime.now().strftime('%Y-%m-%d')


def _extract_numeric_series(cells):
    """Extract a row of numeric values from a mixed RHMZ table row."""
    values = []
    for cell in cells[1:]:
        parsed = _parse_float(cell)
        if parsed is not None:
            values.append(_format_display_number(parsed))
    if values:
        return values

    row_text = ' '.join(cells)
    for match in re.findall(r'-?\d+(?:[.,]\d+)?', row_text):
        parsed = _parse_float(match)
        if parsed is not None:
            values.append(_format_display_number(parsed))
    return values


def _extract_forecast_dates_and_days(soup):
    """Collect forecast dates from the RHMZ 5-day page."""
    text = soup.get_text(' ', strip=True)
    dates = re.findall(r'\d{2}\.\d{2}\.\d{4}\.', text)
    unique_dates = []
    for date_value in dates:
        if date_value not in unique_dates:
            unique_dates.append(date_value)
        if len(unique_dates) == 5:
            break
    return unique_dates


def _parse_rhmz_forecast_page(html):
    """Parse the official RHMZ 5-day forecast page for Belgrade."""
    soup = BeautifulSoup(html, 'lxml')
    rows = []
    for row in soup.find_all('tr'):
        cells = [_normalize_space(cell.get_text(' ', strip=True)) for cell in row.find_all(['td', 'th'])]
        if cells:
            rows.append((cells, row))

    if not rows:
        raise ValueError('RHMZ forecast table not found')

    updated_match = re.search(r'Prognoza ažurirana:\s*([0-9.: ]+)', soup.get_text(' ', strip=True))
    updated_at = _normalize_space(updated_match.group(1)) if updated_match else datetime.now().strftime('%d.%m.%Y. %H:%M')
    date_tokens = _extract_forecast_dates_and_days(soup)

    max_values = []
    min_values = []
    condition_snapshots = []

    for cells, row in rows:
        row_label = cells[0].lower()
        if 'maks. temperatura' in row_label:
            max_values = _extract_numeric_series(cells)
        elif 'min. temperatura' in row_label:
            min_values = _extract_numeric_series(cells)
        elif 'pojava' in row_label:
            for img in row.find_all('img'):
                snapshot = _rhmz_forecast_icon_snapshot(img)
                if snapshot:
                    condition_snapshots.append(snapshot)

    if not date_tokens or not max_values or not min_values:
        raise ValueError('RHMZ forecast values are incomplete')

    fallback_condition = _weather_fallback_snapshot()['condition']
    forecast_days = []
    limit = min(len(date_tokens), len(max_values), len(min_values), 5)
    for idx in range(limit):
        iso_date = datetime.strptime(date_tokens[idx], '%d.%m.%Y.').strftime('%Y-%m-%d')
        snapshot = condition_snapshots[idx] if idx < len(condition_snapshots) else None
        condition = snapshot['condition'] if snapshot else fallback_condition
        description = snapshot['description'] if snapshot else ''
        labels = _format_weather_day_label(iso_date)
        forecast_days.append(
            {
                **labels,
                'condition': condition,
                'description': description or 'Без детаљног описа',
                'temp_max': max_values[idx],
                'temp_min': min_values[idx],
                'precipitation_probability': None,
                'windspeed': None,
            }
        )

    return {
        'updated_at': updated_at,
        'days': forecast_days,
    }


def _find_station_cells(rows, station_name):
    """Return the first parsed table row that matches a station name."""
    target = station_name.lower()
    for cells in rows:
        if cells and _normalize_space(cells[0]).lower() == target:
            return cells
    return None


def _parse_rhmz_observed_page(html):
    """Parse official RHMZ observed weather rows for Belgrade and Kosutnjak."""
    soup = BeautifulSoup(html, 'lxml')
    rows = []
    for row in soup.find_all('tr'):
        cells = [_normalize_space(cell.get_text(' ', strip=True)) for cell in row.find_all(['td', 'th'])]
        if cells:
            rows.append(cells)

    if not rows:
        raise ValueError('RHMZ observed table not found')

    text = soup.get_text(' ', strip=True)
    updated_match = re.search(r'Podaci ažurirani:\s*([0-9.: ]+)', text)
    updated_at = _normalize_space(updated_match.group(1)) if updated_match else datetime.now().strftime('%d.%m.%Y. %H:%M')

    beograd = _find_station_cells(rows, 'Beograd')
    kosutnjak = _find_station_cells(rows, 'Košutnjak') or _find_station_cells(rows, 'Kosutnjak')

    if not beograd and not kosutnjak:
        raise ValueError('RHMZ Belgrade stations not found')

    beograd_temp = _parse_float(beograd[1]) if beograd and len(beograd) > 1 else None
    beograd_wind = _parse_float(beograd[4]) if beograd and len(beograd) > 4 else None
    beograd_description = beograd[-1] if beograd else ''

    kosutnjak_temp = _parse_float(kosutnjak[2]) if kosutnjak and len(kosutnjak) > 2 else None
    kosutnjak_wind = _parse_float(kosutnjak[6]) if kosutnjak and len(kosutnjak) > 6 else None

    current_temperature = beograd_temp if beograd_temp is not None else kosutnjak_temp
    # RHMZ observed tables publish wind in m/s; convert to km/h for the existing UI.
    wind_mps = beograd_wind if beograd_wind is not None else kosutnjak_wind
    current_wind = _format_display_number(wind_mps * 3.6) if wind_mps is not None else None

    return {
        'updated_at': updated_at,
        'temperature': _format_display_number(current_temperature),
        'windspeed': current_wind,
        'description': '' if beograd_description == '-' else beograd_description,
    }


def _build_forecast_days_from_payload(daily, *, limit=7):
    """Normalize Open-Meteo daily arrays into dashboard forecast entries."""
    date_values = daily.get('time') or []
    weather_codes = daily.get('weather_code') or daily.get('weathercode') or []
    temp_max_values = daily.get('temperature_2m_max') or []
    temp_min_values = daily.get('temperature_2m_min') or []
    precipitation_values = daily.get('precipitation_probability_max') or []
    wind_values = daily.get('wind_speed_10m_max') or daily.get('windspeed_10m_max') or []

    forecast_days = []
    for idx, date_value in enumerate(date_values[:limit]):
        code = weather_codes[idx] if idx < len(weather_codes) else None
        weather = _weather_snapshot_from_wmo(code)
        labels = _format_weather_day_label(date_value)
        forecast_days.append(
            {
                **labels,
                'condition': weather['condition'],
                'description': weather['description'],
                'temp_max': temp_max_values[idx] if idx < len(temp_max_values) else None,
                'temp_min': temp_min_values[idx] if idx < len(temp_min_values) else None,
                'precipitation_probability': precipitation_values[idx] if idx < len(precipitation_values) else None,
                'windspeed': wind_values[idx] if idx < len(wind_values) else None,
            }
        )

    return forecast_days


def _forced_weather_snapshot():
    """Return the configured forced current-weather payload when enabled."""
    if FORCED_WEATHER_CONDITION and FORCED_WEATHER_CONDITION != 'auto':
        return {
            'condition': FORCED_WEATHER_CONDITION,
            'temperature': None,
            'windspeed': None,
            'description': FORCED_WEATHER_CONDITION.capitalize(),
        }
    return None


def _cache_weather_bundle(bundle, *, cache_date):
    """Mirror the shared daily weather bundle into memory caches."""
    now_ts = time.time()
    current_snapshot = bundle.get('current') or _weather_fallback_snapshot()
    forecast_snapshot = {
        'location': bundle.get('location', 'Београд'),
        'days': bundle.get('days', []),
        'updated_at': bundle.get('updated_at'),
        'source': bundle.get('source', 'RHMZ Србије'),
    }

    with _weather_daily_bundle_lock:
        _weather_daily_bundle_cache['data'] = bundle
        _weather_daily_bundle_cache['timestamp'] = now_ts
        _weather_daily_bundle_cache['cache_date'] = cache_date

    with _weather_cache_lock:
        _weather_cache['data'] = current_snapshot
        _weather_cache['timestamp'] = now_ts
        _weather_cache['cache_date'] = cache_date

    with _weather_forecast_cache_lock:
        _weather_forecast_cache['data'] = forecast_snapshot
        _weather_forecast_cache['timestamp'] = now_ts
        _weather_forecast_cache['cache_date'] = cache_date


def _read_weather_bundle_from_disk(cache_date=None, *, allow_stale=False):
    """Load the persisted daily weather bundle from disk when it is usable."""
    try:
        payload = load_json_file(_WEATHER_FORECAST_CACHE_PATH, default={}) or {}
    except (OSError, ValueError) as exc:
        logger.warning("Weather disk cache read failed: %s", exc)
        return None, False

    bundle = payload.get('data')
    bundle_date = payload.get('cache_date')
    if not bundle or not bundle_date:
        return None, False
    if not allow_stale and cache_date and bundle_date != cache_date:
        return None, False
    _cache_weather_bundle(bundle, cache_date=bundle_date)
    return bundle, bundle_date != cache_date


def _fetch_daily_weather_bundle(cache_date):
    """Fetch current weather and forecast from official RHMZ sources."""
    forced_current = _forced_weather_snapshot()

    try:
        ca_bundle = _rhmz_ca_bundle()
        forecast_response = requests.get(RHMZ_FORECAST_URL, headers=_RHMZ_HEADERS, timeout=10, verify=ca_bundle)
        forecast_response.raise_for_status()
        forecast_payload = _parse_rhmz_forecast_page(forecast_response.text)

        observed_response = requests.get(RHMZ_OBSERVED_URL, headers=_RHMZ_HEADERS, timeout=10, verify=ca_bundle)
        observed_response.raise_for_status()
        observed_payload = _parse_rhmz_observed_page(observed_response.text)

        observed_description = observed_payload.get('description')
        fallback_description = (
            forecast_payload['days'][0]['description']
            if forecast_payload.get('days')
            else ''
        )
        current_snapshot = forced_current or _rhmz_description_to_snapshot(
            observed_description or fallback_description,
            temperature=observed_payload.get('temperature'),
            windspeed=observed_payload.get('windspeed'),
        )
        bundle = {
            'location': 'Београд',
            'current': current_snapshot,
            'days': forecast_payload.get('days', []),
            'updated_at': forecast_payload.get('updated_at') or observed_payload.get('updated_at') or datetime.now().strftime('%d.%m.%Y. %H:%M'),
            'source': 'RHMZ Србије',
        }
        _cache_weather_bundle(bundle, cache_date=cache_date)
        try:
            write_json_file(
                _WEATHER_FORECAST_CACHE_PATH,
                {
                    'cache_date': cache_date,
                    'saved_at': datetime.now().isoformat(timespec='seconds'),
                    'data': bundle,
                },
            )
        except OSError as exc:
            logger.warning("Weather disk cache write failed: %s", exc)
        return bundle
    except Exception as exc:
        logger.warning("Daily weather fetch failed: %s", exc)
        if forced_current:
            return {
                'location': 'Београд',
                'current': forced_current,
                'days': [],
                'updated_at': datetime.now().strftime('%d.%m.%Y. %H:%M'),
                'source': 'RHMZ Србије',
            }
        raise


def _get_or_fetch_daily_weather_bundle():
    """Return today's shared weather bundle, falling back to stale disk data on failure."""
    today_key = _today_weather_cache_key()

    with _weather_daily_bundle_lock:
        cached_bundle = _weather_daily_bundle_cache.get('data')
        cached_date = _weather_daily_bundle_cache.get('cache_date')
        if cached_bundle and cached_date == today_key:
            return cached_bundle, False

    disk_bundle, disk_is_stale = _read_weather_bundle_from_disk(today_key, allow_stale=False)
    if disk_bundle:
        return disk_bundle, disk_is_stale

    try:
        return _fetch_daily_weather_bundle(today_key), False
    except Exception:
        stale_bundle, _ = _read_weather_bundle_from_disk(today_key, allow_stale=True)
        if stale_bundle:
            return stale_bundle, True
        return None, True


def get_current_weather():
    """Return current weather from the shared daily weather bundle."""
    cached_data, is_fresh = _get_cached_weather_snapshot()
    if cached_data and is_fresh:
        return cached_data

    bundle, _ = _get_or_fetch_daily_weather_bundle()
    if bundle and bundle.get('current'):
        return bundle['current']

    forced_current = _forced_weather_snapshot()
    return forced_current or _weather_fallback_snapshot()


def get_current_weather_quick():
    """Return the currently cached snapshot without triggering new weather traffic."""
    cached_data, is_fresh = _get_cached_weather_snapshot()
    if cached_data and is_fresh:
        return cached_data

    bundle, _ = _read_weather_bundle_from_disk(_today_weather_cache_key(), allow_stale=False)
    if bundle and bundle.get('current'):
        return bundle['current']

    forced_current = _forced_weather_snapshot()
    return forced_current or cached_data or _weather_fallback_snapshot()


def get_weather_forecast(days=7):
    """Return the shared RHMZ forecast from the daily weather bundle."""
    days = max(1, min(days, 7))
    bundle, is_stale = _get_or_fetch_daily_weather_bundle()
    if bundle:
        result = {
            'location': bundle.get('location', 'Београд'),
            'days': bundle.get('days', [])[:days],
            'updated_at': bundle.get('updated_at'),
            'source': bundle.get('source', 'RHMZ Србије'),
        }
        if is_stale:
            result['stale'] = True
        return result

    return {
        'location': 'Београд',
        'days': [],
        'updated_at': datetime.now().strftime('%d.%m.%Y. %H:%M'),
        'source': 'RHMZ Србије',
        'error': 'Прогноза тренутно није доступна.',
    }


def get_rhmz_weather_warnings():
    """Fetch and parse the primary official RHMZ meteorological warning."""
    with _rhmz_warning_cache_lock:
        cached_data = _rhmz_warning_cache.get('data')
        cached_timestamp = _rhmz_warning_cache.get('timestamp')
    if cached_data and cached_timestamp:
        if time.time() - cached_timestamp < 86400:
            return cached_data

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept-Language': 'sr,en;q=0.8',
        }
        response = requests.get(RHMZ_WARNING_URL, headers=headers, timeout=10, verify=_rhmz_ca_bundle())
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        lines = [_normalize_space(text) for text in soup.stripped_strings]
        lines = [line for line in lines if line]

        title_index = next((idx for idx, line in enumerate(lines) if 'УПОЗОРЕЊА РХМЗ СРБИЈЕ' in line.upper()), None)
        if title_index is not None:
            lines = lines[title_index + 1:]

        filtered_lines = []
        footer_markers = ('Контакт', 'Република Србија', 'Републички хидрометеоролошки завод', '©')
        for line in lines:
            if any(marker in line for marker in footer_markers):
                break
            if line in ('Ћир', 'Lat', 'Eng', 'Srbija'):
                continue
            filtered_lines.append(line)

        section_blocks = []
        current_date = None
        current_lines = []
        date_pattern = re.compile(r'^РХМЗ Србије\s+(\d{2}\.\d{2}\.\d{4})(?:\.)?$')
        for line in filtered_lines:
            match = date_pattern.match(line)
            if match:
                if current_date is not None or current_lines:
                    section_blocks.append((current_date, current_lines))
                current_date = match.group(1)
                current_lines = []
                continue
            current_lines.append(line)

        if current_date is not None or current_lines:
            section_blocks.append((current_date, current_lines))

        if not section_blocks:
            raise ValueError('RHMZ warning sections not found')

        date_text, section_lines = section_blocks[0]
        meta = _RHMZ_SECTION_META[0]
        message = _normalize_space(' '.join(section_lines)) or 'Нема доступних података.'
        has_warning = _warning_has_content(message)
        primary_section = {
            'key': meta['key'],
            'title': meta['title'],
            'date': date_text,
            'message': message,
            'has_warning': has_warning,
            'status': 'warning' if has_warning else 'clear',
        }

        result = {
            'source': 'РХМЗ Србије',
            'source_url': RHMZ_WARNING_URL,
            'checked_at': datetime.now().strftime('%d.%m.%Y. %H:%M'),
            'has_warning': has_warning,
            'has_meteorological_warning': has_warning,
            'primary_section': primary_section,
            'sections': [primary_section],
        }
        with _rhmz_warning_cache_lock:
            _rhmz_warning_cache['data'] = result
            _rhmz_warning_cache['timestamp'] = time.time()
        return result
    except Exception as exc:
        logger.warning("RHMZ warning fetch failed: %s", exc)
        if cached_data:
            return {
                **cached_data,
                'stale': True,
            }
        return {
            'source': 'РХМЗ Србије',
            'source_url': RHMZ_WARNING_URL,
            'checked_at': datetime.now().strftime('%d.%m.%Y. %H:%M'),
            'has_warning': False,
            'has_meteorological_warning': False,
            'primary_section': None,
            'sections': [],
            'error': 'RHMZ упозорења тренутно нису доступна.',
        }


def fetch_website_news(limit=6):
    """Fetch news items from the public museum website."""
    def get_cached_snapshot(*, allow_stale):
        with _website_news_cache_lock:
            cached_data = list(_website_news_cache['data'] or [])
            cached_timestamp = _website_news_cache['timestamp']

        if not cached_data or not cached_timestamp:
            return None

        is_fresh = (time.time() - cached_timestamp) < _WEBSITE_NEWS_CACHE_TTL_SECONDS
        if is_fresh or allow_stale:
            return cached_data[:limit]
        return None

    fresh_cache = get_cached_snapshot(allow_stale=False)
    if fresh_cache is not None:
        return fresh_cache

    stale_cache = get_cached_snapshot(allow_stale=True)
    if not _website_news_refresh_lock.acquire(blocking=False):
        if stale_cache is not None:
            return stale_cache
        logger.info("Website news refresh already in progress; returning empty fallback.")
        return []

    try:
        fresh_cache = get_cached_snapshot(allow_stale=False)
        if fresh_cache is not None:
            return fresh_cache

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'sr,en-US;q=0.7,en;q=0.3',
        }

        response = requests.get(
            'https://nhmbeo.rs/vesti/',
            headers=headers,
            timeout=(_WEBSITE_NEWS_CONNECT_TIMEOUT_SECONDS, _WEBSITE_NEWS_READ_TIMEOUT_SECONDS),
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        news_items = []
        articles = soup.find_all('article') or soup.find_all('div', class_='post') or soup.find_all('div', class_='entry')
        if not articles:
            articles = soup.select('.type-post, .hentry, .blog-post, .news-item')

        for article in articles[:limit * 2]:
            try:
                title_elem = article.find(['h2', 'h3', 'h4'])
                if not title_elem:
                    title_elem = article.find('a', class_='entry-title') or article.find('a')

                title = title_elem.get_text(strip=True) if title_elem else None
                if not title:
                    continue

                link_elem = title_elem.find('a') if title_elem.name != 'a' else title_elem
                if not link_elem:
                    link_elem = article.find('a')
                link = link_elem.get('href', '') if link_elem else ''
                if link and not link.startswith('http'):
                    link = 'https://nhmbeo.rs' + link

                img_elem = article.find('img')
                image = img_elem.get('src', '') if img_elem else ''
                if not image and img_elem:
                    image = img_elem.get('data-src', '') or img_elem.get('data-lazy-src', '')
                if image and not image.startswith('http'):
                    image = 'https://nhmbeo.rs' + image

                date_elem = article.find('time') or article.find(class_=['date', 'entry-date', 'post-date'])
                date = date_elem.get_text(strip=True) if date_elem else ''

                excerpt_elem = article.find(['p', 'div'], class_=['excerpt', 'entry-summary', 'post-excerpt'])
                if not excerpt_elem:
                    excerpt_elem = article.find('p')
                excerpt = excerpt_elem.get_text(strip=True)[:200] if excerpt_elem else ''

                if title and link:
                    news_items.append(
                        {
                            'title': title,
                            'link': link,
                            'image': image,
                            'date': date,
                            'excerpt': excerpt,
                        }
                    )

                if len(news_items) >= limit:
                    break
            except Exception as exc:
                logger.warning("Error parsing article: %s", exc)
                continue

        with _website_news_cache_lock:
            _website_news_cache['data'] = news_items
            _website_news_cache['timestamp'] = time.time()
        return news_items[:limit]
    except Exception as exc:
        logger.error("Error fetching website news: %s", exc)
        if stale_cache is not None:
            return stale_cache
        return []
    finally:
        _website_news_refresh_lock.release()
