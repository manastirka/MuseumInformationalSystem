"""Regression tests for the exhibitions database view (fix/ui-doterivanje-avg).

Reproduces the production 500 on /admin/exhibitions_database: when any
exhibition row has a NULL start_date (left as None by the PostgreSQL loader),
sorting the exhibitions by ``exhibition['start_date']`` raised
``TypeError: '<' not supported between instances of 'NoneType' and 'str'``.
"""

from unittest import mock

import museum_content_views as content_views


def _fake_stats():
    return {
        'total_exhibitions': 0,
        'active_exhibitions': 0,
        'completed_exhibitions': 0,
        'planned_exhibitions': 0,
        'total_visitors': 0,
        'annual_exhibitions': 0,
    }


def test_render_exhibitions_with_null_start_date_no_500():
    """An exhibition whose start_date is None must not crash the sort."""
    exhibitions_database = {
        'exhibitions': [
            {'id': 1, 'title': 'Са датумом', 'start_date': '2026-01-01', 'status': 'Активна'},
            {'id': 2, 'title': 'Без датума', 'start_date': None, 'status': 'Планирана'},
        ],
        'types': ['Изложба'],
    }

    with mock.patch.object(content_views, 'render_template', return_value='OK') as render:
        result = content_views.render_exhibitions_database(
            exhibitions_database=exhibitions_database,
            get_exhibition_statistics=_fake_stats,
        )

    assert result == 'OK'
    # Exhibition with a real date sorts ahead of the date-less one.
    passed = render.call_args.kwargs['exhibitions']
    assert [item['id'] for item in passed] == [1, 2]
