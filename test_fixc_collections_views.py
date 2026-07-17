"""Phase-C low-severity hardening tests for collection_management_views.

Focus: render_cultural_heritage_database must not crash with KeyError when a
heritage record omits optional classification keys (significance/category/
condition). This guards the statistics block against a future data source that
does not populate every key.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-collections-views')

from unittest.mock import patch

import app as museum_app
import collection_management_views as cmv


def _heritage_db_missing_keys():
    """A heritage DB whose item is missing significance/category/condition."""
    return {
        # Item deliberately lacks 'significance', 'category', and 'condition'.
        'heritage_items': [
            {
                'name': 'Тест предмет',
                'registry_number': 'Р-1',
                'location': 'Сала 1',
            }
        ],
        'statistics': {},
        'heritage_types': [],
        'categories': [],
        'subcategories': [],
        'significance_levels': [],
        'locations': [],
        'conditions': [],
        'protection_statuses': [],
    }


def test_heritage_statistics_resilient_to_missing_keys():
    """Statistics must use .get() so a missing key does not 500 the page."""
    with museum_app.app.test_request_context('/'):
        with patch.object(cmv, 'render_template', return_value='OK') as mock_render:
            result = cmv.render_cultural_heritage_database(
                get_cultural_heritage_database=_heritage_db_missing_keys,
                prepare_collection_records_for_display=lambda ct, records: (records, None),
                get_qr_collection_action_url=lambda ct: '/qr',
            )

    assert result == 'OK'
    stats = mock_render.call_args.kwargs['statistics']
    # Missing keys must count as zero, not raise.
    assert stats['exceptional_significance'] == 0
    assert stats['great_significance'] == 0
    assert stats['regular_significance'] == 0
    assert stats['natural_heritage'] == 0
    assert stats['excellent_condition'] == 0
    assert stats['good_condition'] == 0
    assert stats['total_heritage_items'] == 1


def test_heritage_statistics_still_count_present_keys():
    """Records that DO carry the keys are still counted correctly."""
    db = {
        'heritage_items': [
            {
                'name': 'А',
                'significance': 'Културно добро од изузетног значаја',
                'category': 'Природњачко наслеђе',
                'condition': 'Одлично',
                'location': 'Сала 1',
            },
            {
                'name': 'Б',
                'significance': 'Културно добро',
                'category': 'Природњачко наслеђе',
                'condition': 'Добро',
                'location': 'Депо А',
            },
        ],
        'statistics': {},
        'heritage_types': [],
        'categories': [],
        'subcategories': [],
        'significance_levels': [],
        'locations': [],
        'conditions': [],
        'protection_statuses': [],
    }
    with museum_app.app.test_request_context('/'):
        with patch.object(cmv, 'render_template', return_value='OK') as mock_render:
            cmv.render_cultural_heritage_database(
                get_cultural_heritage_database=lambda: db,
                prepare_collection_records_for_display=lambda ct, records: (records, None),
                get_qr_collection_action_url=lambda ct: '/qr',
            )

    stats = mock_render.call_args.kwargs['statistics']
    assert stats['exceptional_significance'] == 1
    assert stats['regular_significance'] == 1
    assert stats['great_significance'] == 0
    assert stats['natural_heritage'] == 2
    assert stats['excellent_condition'] == 1
    assert stats['good_condition'] == 1
    assert stats['displayed_items'] == 1
    assert stats['storage_items'] == 1
