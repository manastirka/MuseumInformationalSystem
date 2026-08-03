"""Regression tests for the exhibitions database view (fix/ui-doterivanje).

Two production 500s on /admin/exhibitions_database, both triggered by NULL
columns the PostgreSQL loader leaves as None:

1. Sorting by ``exhibition['start_date']`` raised TypeError when start_date was
   None (fixed by a null-safe sort key).
2. The template rendered ``exhibition.description[:150]`` and
   ``"{:,}".format(exhibition.visitor_count)`` — both raise (TypeError /
   ValueError) when the column is None. Dev data had these populated, so the
   crash only showed with production rows that have NULL description or
   visitor_count. Fixed by defaulting them in the loader + guarding the template.
"""

import os
import unittest
from unittest import mock

for _k, _v in {
    'FLASK_ENV': 'testing',
    'SECRET_KEY': 'test-secret',
    'REDIS_URL': '',
    'SESSION_TYPE': 'filesystem',
    'SESSION_FILE_DIR': '/tmp/museum-test-flask-session',
}.items():
    os.environ.setdefault(_k, _v)

import app as museum_app
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


# --- Finding 1: null start_date breaks the sort ---------------------------

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
    passed = render.call_args.kwargs['exhibitions']
    assert [item['id'] for item in passed] == [1, 2]


# --- Finding 2: null description / visitor_count break the real template ---

class ExhibitionsRouteNullDataTests(unittest.TestCase):
    """Render the REAL template through the REAL route with NULL columns."""

    def setUp(self):
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = 'admin@example.com'
            sess['user_name'] = 'Admin'
            sess['user_role'] = 'admin'
            sess['is_admin'] = True

    def test_null_description_and_visitor_count_render_200(self):
        """A row with description=None and visitor_count=None (as PostgreSQL
        returns for NULL) must not 500 the exhibitions page."""
        crafted = {
            'exhibitions': [
                {
                    'id': 42,
                    'title': 'Проблематична изложба',
                    'description': None,       # NULL in prod -> None[:150] TypeError
                    'visitor_count': None,     # NULL in prod -> format(None) ValueError
                    'status': 'Активна',
                    'start_date': None,
                    'end_date': None,
                    'curator': None,
                    'location': None,
                    'category': 'gallery',
                    'type': 'Изложба',
                },
            ],
            'types': ['Изложба'],
        }

        with mock.patch.object(museum_app, 'EXHIBITIONS_DATABASE', crafted), \
                mock.patch.object(museum_app, 'get_exhibition_statistics', _fake_stats):
            response = self.client.get('/admin/exhibitions_database', base_url=self.base_url)

        self.assertEqual(
            response.status_code, 200,
            msg='exhibitions page 500s on NULL description/visitor_count',
        )
