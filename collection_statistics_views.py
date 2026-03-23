"""Shared route implementations for collection statistics views."""

import logging

from flask import flash, redirect, render_template, url_for

logger = logging.getLogger(__name__)


def render_admin_statistics(
    *,
    get_mineral_database,
    get_meteorite_collection_database,
    botany_collection_database,
    paleozoology_collection_database,
    paleobotany_collection_database,
    petrology_collection_database,
    get_cultural_heritage_database,
    get_image_storage,
):
    """Render the collection statistics dashboard."""
    try:
        mineral_db = get_mineral_database()
        mineral_stats = mineral_db.get_statistics() if mineral_db.available else {}
        rruff_stats = mineral_db.get_rruff_statistics() if mineral_db.available else {}

        meteorite_count = len(get_meteorite_collection_database()['specimens'])
        botany_count = len(botany_collection_database['specimens'])
        paleozoology_count = len(paleozoology_collection_database['specimens'])
        paleobotany_count = len(paleobotany_collection_database['specimens'])
        geology_count = len(petrology_collection_database['specimens'])
        heritage_count = len(get_cultural_heritage_database().get('heritage_items', []))

        total_specimens = (
            mineral_stats.get('total_minerals', 0)
            + meteorite_count
            + botany_count
            + paleozoology_count
            + paleobotany_count
            + geology_count
            + heritage_count
        )

        image_storage = get_image_storage()
        image_stats = image_storage.get_storage_stats()
        total_images = image_stats.get('total_images', 0)

        try:
            from image_database_manager import get_image_db_manager

            img_db = get_image_db_manager()
            img_statistics = img_db.get_statistics()
            specimens_with_images = img_statistics.get('total_items_with_images', 0)
        except Exception:
            specimens_with_images = 0

        image_coverage = (specimens_with_images / total_specimens * 100) if total_specimens > 0 else 0

        stats = {
            'total_specimens': total_specimens,
            'total_images': total_images,
            'specimens_with_images': specimens_with_images,
            'image_coverage': round(image_coverage, 1),
            'recent_additions': 12,
            'collections': {
                'minerals': {
                    'name': 'Минералошка збирка',
                    'count': mineral_stats.get('total_minerals', 0),
                    'icon': 'bi-gem',
                    'color': 'primary',
                    'url': '/admin/mineral_collection',
                },
                'meteorites': {
                    'name': 'Метеорити',
                    'count': meteorite_count,
                    'icon': 'bi-moon-stars',
                    'color': 'warning',
                    'url': '/admin/collection_database/meteorites',
                },
                'botany': {
                    'name': 'Ботаника',
                    'count': botany_count,
                    'icon': 'bi-flower3',
                    'color': 'success',
                    'url': '/admin/collection_database/botany',
                },
                'paleozoology': {
                    'name': 'Палеозоологија',
                    'count': paleozoology_count,
                    'icon': 'bi-bones',
                    'color': 'secondary',
                    'url': '/admin/collection_database/paleozoology',
                },
                'paleobotany': {
                    'name': 'Палеоботаника',
                    'count': paleobotany_count,
                    'icon': 'bi-tree',
                    'color': 'info',
                    'url': '/admin/collection_database/paleobotany',
                },
                'geology': {
                    'name': 'Геологија',
                    'count': geology_count,
                    'icon': 'bi-hexagon',
                    'color': 'dark',
                    'url': '/admin/collection_database/geology',
                },
                'heritage': {
                    'name': 'Културно наслеђе',
                    'count': heritage_count,
                    'icon': 'bi-bank',
                    'color': 'danger',
                    'url': '/admin/collection_database/cultural_heritage',
                },
            },
            'mineral_details': {
                'with_inventory': mineral_stats.get('with_inventory', 0),
                'with_locality': mineral_stats.get('with_locality', 0),
                'top_localities': mineral_stats.get('top_localities', [])[:5],
            },
            'rruff_details': {
                'total': rruff_stats.get('total_minerals', 0),
                'by_crystal_system': rruff_stats.get('by_crystal_system', [])[:7],
            },
        }

        return render_template('admin_statistics.html', stats=stats)
    except Exception as exc:
        logger.error("Error generating statistics: %s", exc)
        flash('Грешка при учитавању статистике.', 'error')
        return redirect(url_for('admin_panel'))
