#!/usr/bin/env python3
"""Regression tests for nhm-portal cluster crashes on CKAN null fields.

CKAN returns JSON null (Python None) for present-but-empty fields such as
notes, author and resource format. dict.get(key, '') only substitutes the
default when the KEY is absent, so a present null value flows through as None
and later .lower()/.upper()/len() calls raise. These tests reproduce those
crashes and lock in the coercion fixes.
"""

import os
import unittest
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-nhm-portal')

from nhm_data_portal_api import NHMDataPortalAPI
from nhm_dataset_downloader import NHMDatasetDownloader


class TestFormatDatasetNullNotes(unittest.TestCase):
    """Finding 2: _format_dataset crashes on notes:null (TypeError len(None))."""

    def test_summary_handles_null_notes(self):
        api = NHMDataPortalAPI()
        pkg = {
            'id': 'abc',
            'name': 'mineral-data',
            'title': 'Mineral Data',
            'notes': None,
            'author': None,
        }
        result = api._format_dataset(pkg)
        self.assertEqual(result['notes'], '')
        self.assertEqual(result['author'], '')

    def test_search_datasets_handles_null_notes(self):
        api = NHMDataPortalAPI()
        ckan_result = {
            'count': 1,
            'results': [{
                'id': 'abc',
                'name': 'mineral-data',
                'title': 'Mineral Data',
                'notes': None,
            }],
        }
        with patch.object(api, '_make_request', return_value=ckan_result):
            out = api.search_datasets('minerals')
        self.assertEqual(out['count'], 1)
        self.assertEqual(out['results'][0]['notes'], '')


class TestFormatResourceNullFormat(unittest.TestCase):
    """Finding 3: _format_resource crashes on format:null (None.upper())."""

    def test_resource_handles_null_format(self):
        api = NHMDataPortalAPI()
        res = {
            'id': 'res-1',
            'name': 'Specimens',
            'format': None,
        }
        result = api._format_resource(res)
        self.assertEqual(result['format'], '')

    def test_full_dataset_with_null_format_resource(self):
        api = NHMDataPortalAPI()
        pkg = {
            'id': 'abc',
            'name': 'mineral-data',
            'title': 'Mineral Data',
            'resources': [{'id': 'res-1', 'name': 'Specimens', 'format': None}],
        }
        with patch.object(api, '_make_request', return_value=pkg):
            full = api.get_dataset('mineral-data')
        self.assertIsNotNone(full)
        self.assertEqual(full['resources'][0]['format'], '')


class TestBuildSearchIndexNullFields(unittest.TestCase):
    """Finding 1: _build_search_index crashes on null title/notes/author."""

    def test_index_handles_null_fields(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            downloader = NHMDatasetDownloader(data_dir=tmp)
            datasets = [{
                'id': 'abc',
                'name': 'mineral-data',
                'title': None,
                'notes': None,
                'author': None,
                'tags': [],
                'resources': [],
            }]
            downloader._build_search_index(datasets)
            self.assertTrue(os.path.exists(downloader.index_file))


if __name__ == '__main__':
    unittest.main()
