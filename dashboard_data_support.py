"""Support helpers for dashboard weather and website-news integrations."""

import logging
import os
import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

DEFAULT_WEATHER_CONDITION = os.environ.get('WEATHER_FALLBACK_CONDITION', 'none').strip().lower() or 'none'
FORCED_WEATHER_CONDITION = os.environ.get('WEATHER_FORCE_CONDITION', '').strip().lower()

RHMZ_WARNING_URL = 'https://www.hidmet.gov.rs/ciril/upozorenja/index.php'

_weather_cache = {
    'data': None,
    'timestamp': None,
}
_weather_forecast_cache = {
    'data': None,
    'timestamp': None,
}
_rhmz_warning_cache = {
    'data': None,
    'timestamp': None,
}
_website_news_cache = {
    'data': None,
    'timestamp': None,
}

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


def get_current_weather():
    """Fetch current weather for Belgrade from Open-Meteo."""
    if FORCED_WEATHER_CONDITION and FORCED_WEATHER_CONDITION != 'auto':
        return {
            'condition': FORCED_WEATHER_CONDITION,
            'temperature': None,
            'windspeed': None,
            'description': FORCED_WEATHER_CONDITION.capitalize(),
        }

    if _weather_cache['data'] and _weather_cache['timestamp']:
        if time.time() - _weather_cache['timestamp'] < 1800:
            return _weather_cache['data']

    try:
        response = requests.get(
            'https://api.open-meteo.com/v1/forecast',
            params={
                'latitude': 44.8178,
                'longitude': 20.4568,
                'current_weather': 'true',
            },
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        current_weather = data.get('current_weather', {})
        code = current_weather.get('weathercode', -1)
        temperature = current_weather.get('temperature')
        windspeed = current_weather.get('windspeed')

        result = _weather_snapshot_from_wmo(code, temperature=temperature, windspeed=windspeed)
        _weather_cache['data'] = result
        _weather_cache['timestamp'] = time.time()
        return result
    except Exception as exc:
        logger.warning("Weather fetch failed, using fallback '%s': %s", DEFAULT_WEATHER_CONDITION, exc)
        fallback = {
            'condition': DEFAULT_WEATHER_CONDITION,
            'temperature': None,
            'windspeed': None,
            'description': '',
        }
        _weather_cache['data'] = fallback
        _weather_cache['timestamp'] = time.time()
        return fallback


def get_weather_forecast(days=7):
    """Fetch daily weather forecast for Belgrade."""
    days = max(1, min(days, 7))
    cached_data = _weather_forecast_cache.get('data')
    if cached_data and _weather_forecast_cache.get('timestamp'):
        if time.time() - _weather_forecast_cache['timestamp'] < 10800:
            return {
                **cached_data,
                'days': cached_data.get('days', [])[:days],
            }

    try:
        response = requests.get(
            'https://api.open-meteo.com/v1/forecast',
            params={
                'latitude': 44.8178,
                'longitude': 20.4568,
                'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max',
                'forecast_days': days,
                'timezone': 'Europe/Belgrade',
            },
            timeout=6,
        )
        response.raise_for_status()
        data = response.json()
        daily = data.get('daily', {})

        date_values = daily.get('time') or []
        weather_codes = daily.get('weather_code') or daily.get('weathercode') or []
        temp_max_values = daily.get('temperature_2m_max') or []
        temp_min_values = daily.get('temperature_2m_min') or []
        precipitation_values = daily.get('precipitation_probability_max') or []
        wind_values = daily.get('wind_speed_10m_max') or daily.get('windspeed_10m_max') or []

        forecast_days = []
        for idx, date_value in enumerate(date_values[:days]):
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

        result = {
            'location': 'Београд',
            'days': forecast_days,
            'updated_at': datetime.now().strftime('%d.%m.%Y. %H:%M'),
            'source': 'Open-Meteo',
        }
        _weather_forecast_cache['data'] = result
        _weather_forecast_cache['timestamp'] = time.time()
        return result
    except Exception as exc:
        logger.warning("Weather forecast fetch failed: %s", exc)
        if cached_data:
            return {
                **cached_data,
                'days': cached_data.get('days', [])[:days],
                'stale': True,
            }
        return {
            'location': 'Београд',
            'days': [],
            'updated_at': datetime.now().strftime('%d.%m.%Y. %H:%M'),
            'source': 'Open-Meteo',
            'error': 'Прогноза тренутно није доступна.',
        }


def get_rhmz_weather_warnings():
    """Fetch and parse the primary official RHMZ meteorological warning."""
    cached_data = _rhmz_warning_cache.get('data')
    if cached_data and _rhmz_warning_cache.get('timestamp'):
        if time.time() - _rhmz_warning_cache['timestamp'] < 86400:
            return cached_data

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept-Language': 'sr,en;q=0.8',
        }
        response = requests.get(RHMZ_WARNING_URL, headers=headers, timeout=10)
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
    if _website_news_cache['data'] and _website_news_cache['timestamp']:
        if time.time() - _website_news_cache['timestamp'] < 300:
            return _website_news_cache['data'][:limit]

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'sr,en-US;q=0.7,en;q=0.3',
        }

        response = requests.get('https://nhmbeo.rs/vesti/', headers=headers, timeout=10)
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

        _website_news_cache['data'] = news_items
        _website_news_cache['timestamp'] = time.time()
        return news_items[:limit]
    except Exception as exc:
        logger.error("Error fetching website news: %s", exc)
        return []
