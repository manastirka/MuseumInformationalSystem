"""Shared route implementations for depot locality and science news APIs."""

import hashlib
import json
import logging
import os
from datetime import datetime

from flask import current_app, jsonify, request, session
from runtime_lock_utils import load_json_file, update_json_file
from postgres_service import get_postgres_connection

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


def _registry_localities(cur):
    """Rows of the standalone registry (migration 027), newest names last."""
    cur.execute(
        """
        SELECT id, name, country, note, source
        FROM localities
        ORDER BY name
        """
    )
    polja = ('id', 'name', 'country', 'note', 'source')
    return [dict(zip(polja, row)) for row in cur.fetchall()]


def api_get_localities(*, get_mineral_database):
    """Localities for the collection tool.

    Source of truth is the standalone registry (`localities`, migration 027) —
    a locality may exist with zero specimens (field site, future find). Specimen
    counts are still derived from the free-text `minerals.card_locality`.
    While the registry is still empty (before the seed runs) the tool falls back
    to the old runtime aggregate so it never shows an empty screen.
    """
    try:
        from locality_data import get_locality_data_local_only

        mineral_db = get_mineral_database()
        result = mineral_db.get_all_minerals(page=1, per_page=10000)
        minerals = result.get('minerals', [])

        localities = {}
        registry = []
        try:
            with get_postgres_connection() as conn:
                with conn.cursor() as cur:
                    registry = _registry_localities(cur)
        except Exception as exc:  # sifarnik nedostupan -> stari agregat
            logger.warning('Locality registry unavailable, falling back: %s', exc)

        for row in registry:
            localities[row['name']] = {
                'name': row['name'],
                'count': 0,
                'minerals': set(),
                'source': row['source'],
                'country': row['country'],
                'note': row['note'],
            }

        for mineral in minerals:
            locality_name = (mineral.get('lokalitet') or '').strip()
            if not locality_name:
                continue

            # Registry is the list; a specimen whose free-text locality is not
            # in it yet still gets counted (it is real data), so nothing is lost
            # before/without the seed.
            locality_entry = localities.setdefault(
                locality_name,
                {
                    'name': locality_name,
                    'count': 0,
                    'minerals': set(),
                    'source': 'zbirka',
                    'country': None,
                    'note': None,
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
                    'source': locality_data.get('source', 'zbirka'),
                    'country': locality_data.get('country'),
                    'note': locality_data.get('note'),
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

        # Najpre po broju predmeta, pa azbucno — lokaliteti bez predmeta
        # (rucno dodati, teren) ostaju na spisku, na kraju.
        response_data.sort(key=lambda item: (-item['count'], item['name']))
        return jsonify(
            {
                'success': True,
                'localities': response_data,
                'total': len(response_data),
                'registry_count': len(registry),
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


def api_add_locality():
    """Add a locality to the standalone registry (no specimen required)."""
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    country = (data.get('country') or '').strip() or None
    note = (data.get('note') or '').strip() or None

    if not name:
        return jsonify({'success': False, 'message': 'Назив локалитета је обавезан.'}), 400
    if len(name) > 300:
        return jsonify({'success': False, 'message': 'Назив је предугачак.'}), 400

    try:
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO localities (name, country, note, source, created_by_email)
                    VALUES (%s, %s, %s, 'rucno', %s)
                    ON CONFLICT (name) DO NOTHING
                    RETURNING id
                    """,
                    (name, country, note, session.get('user_email', 'system')),
                )
                row = cur.fetchone()
            conn.commit()

        if not row:
            return jsonify({'success': False,
                            'message': 'Локалитет са тим називом већ постоји.'}), 409
        return jsonify({'success': True, 'id': row[0], 'name': name})
    except Exception as exc:
        logger.error('Error adding locality: %s', exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_delete_locality(locality_id):
    """Delete a registry entry. Specimens are never touched — but a locality
    that still has specimens attached by name is refused, so the list cannot
    silently lose a place the collection references."""
    try:
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT name FROM localities WHERE id = %s', (locality_id,))
                row = cur.fetchone()
                if not row:
                    return jsonify({'success': False,
                                    'message': 'Локалитет не постоји.'}), 404
                name = row[0]

                cur.execute(
                    "SELECT count(*) FROM minerals WHERE btrim(coalesce(card_locality,'')) = %s",
                    (name,),
                )
                broj = cur.fetchone()[0]
                if broj:
                    return jsonify({
                        'success': False,
                        'message': f'Локалитет има {broj} везаних предмета — не може се обрисати.',
                    }), 409

                cur.execute('DELETE FROM localities WHERE id = %s', (locality_id,))
            conn.commit()
        return jsonify({'success': True})
    except Exception as exc:
        logger.error('Error deleting locality %s: %s', locality_id, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500
