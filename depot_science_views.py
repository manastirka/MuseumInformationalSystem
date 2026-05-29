"""Shared route implementations for depot locality and science news APIs."""

import hashlib
import json
import logging
import os
from datetime import datetime

from flask import current_app, jsonify, request, session
from runtime_lock_utils import load_json_file, update_json_file

logger = logging.getLogger(__name__)

_CATEGORY_NAMES = {
    'geology': 'Геологија',
    'mineralogy': 'Минералогија',
    'paleontology': 'Палеонтологија',
    'research': 'Истраживање',
    'petrology': 'Петрологија',
    'seismology': 'Сеизмологија',
}

_REGION_NAMES = {
    'balkans': 'Балкан',
    'europe': 'Европа',
    'world': 'Свет',
}


def _science_news_file():
    return os.path.join(current_app.root_path, 'data', 'science_news.json')


def _load_science_news():
    news_file = _science_news_file()
    try:
        if os.path.exists(news_file):
            return load_json_file(news_file, default=[])
    except Exception as exc:
        logger.error("Error loading science news: %s", exc)
    return []


def _save_science_news(all_news):
    news_file = _science_news_file()
    update_json_file(news_file, lambda _current: list(all_news), default=[])


def api_get_localities(*, get_mineral_database):
    """Get all unique localities from the mineral collection with counts and info."""
    try:
        from locality_data import get_locality_data_local_only

        mineral_db = get_mineral_database()
        result = mineral_db.get_all_minerals(page=1, per_page=10000)
        minerals = result.get('minerals', [])

        localities = {}
        for mineral in minerals:
            locality_name = (mineral.get('lokalitet') or '').strip()
            if not locality_name:
                continue

            locality_entry = localities.setdefault(
                locality_name,
                {
                    'name': locality_name,
                    'count': 0,
                    'minerals': set(),
                },
            )
            locality_entry['count'] += 1

            mineral_name = mineral.get('naziv') or mineral.get('predmet') or ''
            if mineral_name:
                locality_entry['minerals'].add(mineral_name)

        response_data = []
        for locality_name, locality_data in localities.items():
            info = get_locality_data_local_only(locality_name)
            description = (info or {}).get('description', '')
            response_data.append(
                {
                    'name': locality_data['name'],
                    'count': locality_data['count'],
                    'minerals': list(locality_data['minerals'])[:10],
                    'has_info': info is not None,
                    'info': {
                        'type': info.get('type', '') if info else '',
                        'geology': info.get('geology', '') if info else '',
                        'description': description[:200],
                        'country': info.get('country', '') if info else '',
                        'coordinates': info.get('coordinates', {}) if info else {},
                        'references': info.get('references', [])[:3] if info else [],
                        'wikipedia': info.get('wikipedia', '') if info else '',
                        'mindat': info.get('mindat', '') if info else '',
                    }
                    if info
                    else None,
                }
            )

        response_data.sort(key=lambda item: -item['count'])
        return jsonify(
            {
                'success': True,
                'localities': response_data[:100],
                'total': len(response_data),
            }
        )
    except Exception as exc:
        logger.error("Error fetching localities: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_get_science_news():
    """Get curated science news from JSON storage with optional filters."""
    search_query = request.args.get('q', '').strip().lower()
    category_filter = request.args.get('category', '').strip()
    region_filter = request.args.get('region', '').strip()

    all_news = _load_science_news()

    if category_filter:
        all_news = [item for item in all_news if item.get('category') == category_filter]

    if region_filter:
        all_news = [item for item in all_news if item.get('region') == region_filter]

    if search_query:
        all_news = [
            item
            for item in all_news
            if search_query in f"{item.get('title', '')} {item.get('summary', '')}".lower()
        ]

    def sort_key(item):
        region_priority = {'balkans': 0, 'europe': 1, 'world': 2}
        return (region_priority.get(item.get('region', 'world'), 2), item.get('date', ''))

    all_news.sort(key=lambda item: item.get('date', ''), reverse=True)
    all_news.sort(key=sort_key)

    return jsonify(
        {
            'success': True,
            'news': all_news[:12],
            'total': len(all_news),
            'fetched_at': datetime.now().isoformat(),
        }
    )


def api_add_science_news():
    """Add a new science news item."""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400

    for field in ['title', 'category', 'region']:
        if not data.get(field):
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400

    timestamp = datetime.now()
    news_id = hashlib.md5(f"{data['title']}{timestamp.isoformat()}".encode()).hexdigest()[:8]
    news_item = {
        'id': news_id,
        'title': str(data['title'])[:200],
        'summary': str(data.get('summary') or '')[:500],
        'category': data['category'],
        'categoryName': _CATEGORY_NAMES.get(data['category'], data['category']),
        'region': data['region'],
        'regionName': _REGION_NAMES.get(data['region'], data['region']),
        'source': data.get('source', ''),
        'url': data.get('url', ''),
        'date': data.get('date', timestamp.strftime('%Y-%m-%d')),
        'added_by': session.get('user_email', 'system'),
        'added_at': timestamp.isoformat(),
    }

    try:
        def _add_news(existing_news):
            payload = [item for item in list(existing_news or []) if item.get('id') != news_id]
            payload.insert(0, news_item)
            return payload[:100]

        update_json_file(_science_news_file(), _add_news, default=[])
        return jsonify({'success': True, 'news': news_item})
    except Exception as exc:
        logger.error("Error saving science news: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_delete_science_news(*, news_id):
    """Delete a science news item."""
    news_file = _science_news_file()
    if not os.path.exists(news_file):
        return jsonify({'success': False, 'message': 'News file not found'}), 404

    try:
        update_json_file(
            news_file,
            lambda all_news: [item for item in list(all_news or []) if item.get('id') != news_id],
            default=[],
        )
        return jsonify({'success': True})
    except Exception as exc:
        logger.error("Error deleting science news: %s", exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_get_locality_detail(locality_name, *, get_mineral_database):
    """Get detailed information about a specific locality."""
    try:
        from locality_data import get_locality_data

        info = get_locality_data(locality_name)
        mineral_db = get_mineral_database()
        result = mineral_db.get_all_minerals(page=1, per_page=10000)
        minerals = result.get('minerals', [])

        locality_minerals = []
        locality_name_lower = locality_name.lower()
        for mineral in minerals:
            locality = mineral.get('lokalitet') or ''
            if locality_name_lower in locality.lower():
                locality_minerals.append(
                    {
                        'name': mineral.get('naziv') or mineral.get('predmet') or '',
                        'inventory_number': mineral.get('inventarni_broj') or '',
                        'box': mineral.get('gde_se_nalazi') or '',
                    }
                )

        return jsonify(
            {
                'success': True,
                'locality': locality_name,
                'info': info,
                'minerals': locality_minerals[:50],
                'total_minerals': len(locality_minerals),
            }
        )
    except Exception as exc:
        logger.error("Error fetching locality detail for %s: %s", locality_name, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500
