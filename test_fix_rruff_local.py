"""Reproducing test for the rruff-local cluster bug.

Bug: LocalRRUFFData._load_or_build_index loads any valid JSON via
load_json_file and returns unconditionally without validating the
structure. A structurally-incomplete index file (e.g. {} or an old
format missing 'minerals'/'rruff_ids'/'stats') silently leaves
self._index without the required top-level keys, so every later
bare-keyed access (get_stats, search_minerals, get_mineral_data,
get_data_by_rruff_id) raises KeyError.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-rruff-local')

import json
import unittest

from local_rruff_data import LocalRRUFFData


class IncompleteIndexRecoveryTests(unittest.TestCase):
    """A structurally-incomplete index must not break RRUFF lookups."""

    def _make_manager(self, tmpdir, index_payload):
        index_file = os.path.join(tmpdir, 'rruff_file_index.json')
        with open(index_file, 'w', encoding='utf-8') as handle:
            json.dump(index_payload, handle)
        # data_path has no data subfolders/images, so a rebuild yields
        # an empty-but-well-formed index.
        return LocalRRUFFData(data_path=tmpdir)

    def test_empty_dict_index_does_not_break_stats(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = self._make_manager(tmpdir, {})
            # Before the fix this raises KeyError: 'minerals'
            stats = manager.get_stats()
            self.assertIn('total_minerals', stats)
            self.assertEqual(stats['total_minerals'], 0)
            self.assertIn('total_rruff_ids', stats)

    def test_partial_index_does_not_break_lookups(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            # Old/incomplete format: 'minerals' present but 'rruff_ids'
            # and 'stats' missing.
            manager = self._make_manager(tmpdir, {'minerals': {}})
            # Before the fix this raises KeyError: 'rruff_ids'
            self.assertIsNone(manager.get_data_by_rruff_id('R040063'))
            # Before the fix this raises KeyError: 'minerals'
            self.assertEqual(manager.search_minerals('quartz'), [])
            self.assertIsNone(manager.get_mineral_data('Quartz'))

    def test_index_has_required_keys_after_load(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = self._make_manager(tmpdir, {})
            for key in ('minerals', 'rruff_ids', 'stats'):
                self.assertIn(key, manager._index)


if __name__ == '__main__':
    unittest.main()
