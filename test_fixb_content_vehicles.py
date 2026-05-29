import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-content-vehicles')

import museum_content_support


def test_exhibition_statistics_handles_null_start_date_and_visitor_count():
    # Mirrors the PostgreSQL path where start_date may be NULL (None) and
    # visitor_count may be NULL, per phase3a_databases.load_exhibitions_data
    # ordering by `start_date DESC NULLS LAST`.
    exhibitions_database = {
        'exhibitions': [
            {
                'status': 'Активна',
                'visitor_count': 100,
                'start_date': '2026-01-01',
                'category': 'gallery',
            },
            {
                'status': 'Завршена',
                'visitor_count': None,
                'start_date': None,
                'category': 'gallery',
            },
            {
                'status': 'Планирана',
                'category': 'gallery',
                # visitor_count and start_date keys missing entirely
            },
        ]
    }

    stats = museum_content_support.get_exhibition_statistics(
        exhibitions_database=exhibitions_database,
        current_year=2026,
    )

    assert stats['total_exhibitions'] == 3
    assert stats['active_exhibitions'] == 1
    assert stats['completed_exhibitions'] == 1
    assert stats['planned_exhibitions'] == 1
    # 100 + None(->0) + missing(->0)
    assert stats['total_visitors'] == 100
    # Only the record with a 2026 start_date counts.
    assert stats['annual_exhibitions'] == 1


def test_exhibition_statistics_normal_records_unaffected():
    exhibitions_database = {
        'exhibitions': [
            {
                'status': 'Активна',
                'visitor_count': 50,
                'start_date': '2026-03-01',
                'category': 'gallery',
            },
            {
                'status': 'Историјска',
                'visitor_count': 75,
                'start_date': '2019-05-01',
                'category': 'gallery',
            },
            {
                'status': 'Активна',
                'visitor_count': 25,
                'start_date': '2025-01-01',
                'category': 'touring',
            },
        ]
    }

    stats = museum_content_support.get_exhibition_statistics(
        exhibitions_database=exhibitions_database,
        current_year=2026,
    )

    # touring excluded
    assert stats['total_exhibitions'] == 2
    assert stats['active_exhibitions'] == 1
    assert stats['completed_exhibitions'] == 1
    assert stats['total_visitors'] == 125
    assert stats['annual_exhibitions'] == 1
