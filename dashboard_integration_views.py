"""Shared route implementations for dashboard integrations and library views."""

import logging
from datetime import datetime

from flask import jsonify, render_template, request

logger = logging.getLogger(__name__)


def api_website_news(*, fetch_website_news):
    """Return cached website news items for the dashboard."""
    try:
        limit = request.args.get('limit', 6, type=int)
        news = fetch_website_news(limit=min(limit, 12))
        return jsonify({'success': True, 'news': news})
    except Exception as exc:
        logger.error("Error in website news API: %s", exc)
        return jsonify({'success': False, 'message': str(exc), 'news': []})


def api_weather_details(
    *,
    get_current_weather,
    get_weather_forecast,
    get_rhmz_weather_warnings,
    rhmz_warning_url,
):
    """Return current weather, forecast, and RHMZ warning status."""
    try:
        forecast_days = request.args.get('days', 7, type=int)
        current_weather = get_current_weather()
        forecast = get_weather_forecast(days=forecast_days)
        rhmz_warnings = get_rhmz_weather_warnings()

        return jsonify(
            {
                'success': True,
                'location': forecast.get('location', 'Београд'),
                'current': current_weather,
                'forecast': forecast.get('days', []),
                'forecast_updated_at': forecast.get('updated_at'),
                'forecast_source': forecast.get('source'),
                'forecast_stale': forecast.get('stale', False),
                'rhmz': rhmz_warnings,
            }
        )
    except Exception as exc:
        logger.error("Weather details API failed: %s", exc)
        return (
            jsonify(
                {
                    'success': False,
                    'message': 'Није могуће учитати временске податке.',
                    'location': 'Београд',
                    'current': get_current_weather(),
                    'forecast': [],
                    'rhmz': {
                        'source': 'РХМЗ Србије',
                        'source_url': rhmz_warning_url,
                        'checked_at': datetime.now().strftime('%d.%m.%Y. %H:%M'),
                        'has_warning': False,
                        'has_meteorological_warning': False,
                        'sections': [],
                    },
                }
            ),
            500,
        )


def render_library_database(*, get_library_database):
    """Render the library database management view."""
    library_database = get_library_database()
    books = library_database['books']
    categories = library_database['categories']
    statistics = library_database['statistics'].copy()

    statistics['total_books'] = len(books)
    statistics['available_books'] = len([book for book in books if book['status'] == 'доступна'])
    statistics['borrowed_books'] = len([book for book in books if book['status'] == 'позајмљена'])
    statistics['total_categories'] = len({book['category'] for book in books})

    return render_template(
        'admin_library_database.html',
        books=books,
        categories=categories,
        statistics=statistics,
        total_books=len(books),
    )
