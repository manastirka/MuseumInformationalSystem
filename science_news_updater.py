#!/usr/bin/env python3
"""
Science News Updater - Fetches and updates geology/mineralogy news on app startup
Aggregates news from scientific RSS feeds and web sources
"""

import os
import re
import json
import logging
import hashlib
import threading
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from runtime_lock_utils import load_json_file, write_json_file

logger = logging.getLogger(__name__)

# RSS Feed sources for geology and mineralogy
RSS_FEEDS = [
    {
        'url': 'https://www.sciencedaily.com/rss/earth_climate/geology.xml',
        'category': 'geology',
        'categoryName': 'Геологија',
        'source': 'ScienceDaily',
        'region': 'world'
    },
    {
        'url': 'https://www.sciencedaily.com/rss/earth_climate/earthquakes.xml',
        'category': 'seismology',
        'categoryName': 'Сеизмологија',
        'source': 'ScienceDaily',
        'region': 'world'
    },
    {
        'url': 'https://www.sciencedaily.com/rss/earth_climate/volcanoes.xml',
        'category': 'geology',
        'categoryName': 'Геологија',
        'source': 'ScienceDaily',
        'region': 'world'
    },
    {
        'url': 'https://www.sciencedaily.com/rss/fossils_ruins.xml',
        'category': 'paleontology',
        'categoryName': 'Палеонтологија',
        'source': 'ScienceDaily',
        'region': 'world'
    },
    {
        'url': 'https://phys.org/rss-feed/earth-news/',
        'category': 'geology',
        'categoryName': 'Геологија',
        'source': 'Phys.org',
        'region': 'world'
    },
    {
        'url': 'https://www.egu.eu/news/feed/',
        'category': 'research',
        'categoryName': 'Истраживање',
        'source': 'EGU',
        'region': 'europe'
    }
]

# Regional keywords for classification
BALKAN_KEYWORDS = [
    'serbia', 'srbija', 'serbian', 'croatia', 'croatian', 'hrvatska',
    'bosnia', 'herzegovina', 'montenegro', 'crna gora', 'macedonia',
    'north macedonia', 'makedonija', 'slovenia', 'slovenija', 'albania',
    'albanian', 'kosovo', 'balkan', 'balkans', 'dinaric', 'dinarides',
    'pannonian', 'carpathian', 'rhodope', 'morava', 'danube', 'dunav',
    'sava', 'adriatic', 'belgrade', 'beograd', 'zagreb', 'sarajevo',
    'skopje', 'ljubljana', 'podgorica', 'tirana', 'pristina',
    'kopaonik', 'tara', 'zlatibor', 'rtanj', 'avala', 'fruska gora',
    'bor', 'timok', 'jadar', 'loznica', 'vardar', 'ohrid'
]

EUROPE_KEYWORDS = [
    'europe', 'european', 'eu ', 'alps', 'alpine', 'mediterranean',
    'germany', 'german', 'france', 'french', 'italy', 'italian',
    'spain', 'spanish', 'poland', 'polish', 'czech', 'austria',
    'austrian', 'hungary', 'hungarian', 'romania', 'romanian',
    'bulgaria', 'bulgarian', 'greece', 'greek', 'turkey', 'turkish',
    'ukraine', 'ukrainian', 'scandinavia', 'norway', 'norwegian',
    'sweden', 'swedish', 'finland', 'finnish', 'denmark', 'danish',
    'uk ', 'britain', 'british', 'england', 'scotland', 'ireland',
    'switzerland', 'swiss', 'portugal', 'portuguese', 'netherlands',
    'belgium', 'vesuvius', 'etna', 'iceland', 'icelandic'
]


def _compile_region_pattern(keywords: List[str]) -> 're.Pattern':
    """Compile a word-boundary regex from a keyword list (whitespace-trimmed)."""
    terms = sorted({kw.strip() for kw in keywords if kw.strip()}, key=len, reverse=True)
    return re.compile(r'\b(?:' + '|'.join(map(re.escape, terms)) + r')\b')


_BALKAN_PATTERN = _compile_region_pattern(BALKAN_KEYWORDS)
_EUROPE_PATTERN = _compile_region_pattern(EUROPE_KEYWORDS)


def determine_region(text: str, default_region: str = 'world') -> tuple:
    """Determine the region based on text content."""
    text_lower = text.lower()

    # Check Balkans first (highest priority)
    if _BALKAN_PATTERN.search(text_lower):
        return 'balkans', 'Балкан'

    # Check Europe
    if _EUROPE_PATTERN.search(text_lower):
        return 'europe', 'Европа'

    return default_region, 'Свет' if default_region == 'world' else 'Европа'


def parse_rss_date(date_str: str) -> str:
    """Parse various RSS date formats."""
    if not date_str:
        return datetime.now().strftime('%Y-%m-%d')

    formats = [
        '%a, %d %b %Y %H:%M:%S %z',
        '%a, %d %b %Y %H:%M:%S %Z',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%d'
    ]

    for fmt in formats:
        try:
            parsed = datetime.strptime(date_str.strip()[:30], fmt)
            return parsed.strftime('%Y-%m-%d')
        except ValueError:
            continue

    # Fallback: try to extract date-like string
    try:
        return date_str[:10]
    except (TypeError, AttributeError, IndexError):
        return datetime.now().strftime('%Y-%m-%d')


def fetch_rss_news() -> List[Dict]:
    """Fetch news from RSS feeds."""
    news_items = []

    for feed in RSS_FEEDS:
        try:
            response = requests.get(
                feed['url'],
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0 (compatible; MuseumNewsBot/1.0)'}
            )

            if response.status_code != 200:
                continue

            root = ET.fromstring(response.content)

            # Handle standard RSS and Atom formats
            items = root.findall('.//item')
            if not items:
                items = root.findall('.//{http://www.w3.org/2005/Atom}entry')

            for item in items[:3]:  # Get top 3 from each feed
                # Extract title
                title_el = item.find('title')
                if title_el is None:
                    title_el = item.find('{http://www.w3.org/2005/Atom}title')
                title = title_el.text if title_el is not None else 'No title'

                # Extract description
                desc_el = item.find('description')
                if desc_el is None:
                    desc_el = item.find('{http://www.w3.org/2005/Atom}summary')
                desc = desc_el.text if desc_el is not None else ''

                # Clean HTML from description
                if desc:
                    soup = BeautifulSoup(desc, 'html.parser')
                    desc = soup.get_text()[:300]
                    if len(desc) >= 300:
                        desc += '...'

                # Extract link
                link_el = item.find('link')
                if link_el is not None:
                    link = link_el.text or link_el.get('href', '')
                else:
                    link_el = item.find('{http://www.w3.org/2005/Atom}link')
                    link = link_el.get('href', '') if link_el is not None else ''

                # Extract date
                date_el = item.find('pubDate')
                if date_el is None:
                    date_el = item.find('{http://www.w3.org/2005/Atom}published')
                if date_el is None:
                    date_el = item.find('{http://www.w3.org/2005/Atom}updated')
                date_str = parse_rss_date(date_el.text if date_el is not None else '')

                # Determine region
                full_text = f"{title} {desc}"
                region, region_name = determine_region(full_text, feed.get('region', 'world'))

                # Generate ID
                news_id = hashlib.md5(f"{title}{link}".encode()).hexdigest()[:10]

                news_items.append({
                    'id': f"rss_{news_id}",
                    'title': title[:150],
                    'summary': desc,
                    'category': feed['category'],
                    'categoryName': feed['categoryName'],
                    'region': region,
                    'regionName': region_name,
                    'source': feed['source'],
                    'url': link,
                    'date': date_str,
                    'auto_fetched': True
                })

        except Exception as e:
            logger.warning(f"Failed to fetch RSS feed {feed['url']}: {e}")
            continue

    return news_items


def load_existing_news(news_file: str) -> List[Dict]:
    """Load existing news from JSON file."""
    try:
        if os.path.exists(news_file):
            return load_json_file(news_file, default=[])
    except Exception as e:
        logger.error(f"Error loading existing news: {e}")
    return []


def merge_news(existing: List[Dict], new_items: List[Dict], max_items: int = 50) -> List[Dict]:
    """Merge new news items with existing, avoiding duplicates."""
    # Create set of existing IDs and titles for duplicate detection
    existing_ids = {n.get('id') for n in existing}
    existing_titles = {n.get('title', '').lower()[:50] for n in existing}

    merged = list(existing)

    for item in new_items:
        # Skip if ID already exists
        if item['id'] in existing_ids:
            continue

        # Skip if very similar title exists
        title_prefix = item.get('title', '').lower()[:50]
        if title_prefix in existing_titles:
            continue

        merged.append(item)
        existing_ids.add(item['id'])
        existing_titles.add(title_prefix)

    # Sort by date (newest first)
    merged.sort(key=lambda x: x.get('date', ''), reverse=True)

    # Keep manual entries (non auto-fetched) and recent auto-fetched
    manual = [n for n in merged if not n.get('auto_fetched')]
    auto = [n for n in merged if n.get('auto_fetched')]

    # Keep all manual + up to (max_items - len(manual)) auto
    max_auto = max(0, max_items - len(manual))
    result = manual + auto[:max_auto]

    # Re-sort
    result.sort(key=lambda x: x.get('date', ''), reverse=True)

    return result


def save_news(news_file: str, news_items: List[Dict]) -> bool:
    """Save news to JSON file."""
    try:
        write_json_file(news_file, news_items)
        return True
    except Exception as e:
        logger.error(f"Error saving news: {e}")
        return False


def should_update(news_file: str, min_hours: int = 6) -> bool:
    """Check if news should be updated based on last modification time."""
    try:
        if not os.path.exists(news_file):
            return True

        mtime = os.path.getmtime(news_file)
        last_modified = datetime.fromtimestamp(mtime)
        hours_since = (datetime.now() - last_modified).total_seconds() / 3600

        return hours_since >= min_hours
    except (OSError, ValueError) as exc:
        logger.warning("Could not determine science news freshness for %s: %s", news_file, exc)
        return True


def update_science_news(app_root: str, force: bool = False) -> Dict:
    """
    Update science news from RSS feeds.

    Args:
        app_root: Application root directory
        force: Force update even if recently updated

    Returns:
        Dict with update status
    """
    news_file = os.path.join(app_root, 'data', 'science_news.json')

    # Check if update is needed
    if not force and not should_update(news_file):
        logger.info("Science news recently updated, skipping")
        return {'status': 'skipped', 'reason': 'recently_updated'}

    logger.info("Starting science news update...")

    # Load existing news
    existing_news = load_existing_news(news_file)

    # Fetch new items from RSS
    new_items = fetch_rss_news()

    if not new_items:
        logger.warning("No new items fetched from RSS feeds")
        return {'status': 'no_new_items', 'existing_count': len(existing_news)}

    # Merge and save
    merged = merge_news(existing_news, new_items)

    if save_news(news_file, merged):
        logger.info(f"Science news updated: {len(merged)} total items ({len(new_items)} fetched)")
        return {
            'status': 'success',
            'total_items': len(merged),
            'new_items': len(new_items),
            'updated_at': datetime.now().isoformat()
        }
    else:
        return {'status': 'error', 'reason': 'save_failed'}


def update_science_news_background(app_root: str):
    """Run news update in background thread."""
    def _update():
        try:
            result = update_science_news(app_root)
            logger.info(f"Background news update completed: {result}")
        except Exception as e:
            logger.error(f"Background news update failed: {e}")

    thread = threading.Thread(target=_update, daemon=True)
    thread.start()
    logger.info("Science news background update started")


if __name__ == '__main__':
    # Test the updater
    logging.basicConfig(level=logging.INFO)
    app_root = os.path.dirname(os.path.abspath(__file__))
    result = update_science_news(app_root, force=True)
    print(f"Update result: {result}")
