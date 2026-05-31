#!/usr/bin/env python3
"""Regression tests for locked JSON reads and atomic read-modify-write updates."""

import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

import fetch_scientific_papers
import locality_data
import map_feature_paper_enricher
import runtime_lock_utils
import science_news_updater


class JsonLockingTests(unittest.TestCase):
    def test_update_json_file_preserves_concurrent_increments(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'counter.json'
            runtime_lock_utils.write_json_file(target, {'count': 0})

            def increment():
                runtime_lock_utils.update_json_file(
                    target,
                    lambda payload: {'count': int((payload or {}).get('count', 0)) + 1},
                    default={'count': 0},
                )

            threads = [threading.Thread(target=increment) for _ in range(40)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            self.assertEqual(runtime_lock_utils.load_json_file(target, default={}), {'count': 40})

    def test_write_json_file_round_trips_valid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'state.json'
            payload = {'items': [1, 2, 3], 'status': 'ok'}

            runtime_lock_utils.write_json_file(target, payload)

            self.assertEqual(json.loads(target.read_text('utf-8')), payload)
            self.assertEqual(runtime_lock_utils.load_json_file(target, default={}), payload)

    def test_write_json_file_supports_custom_json_encoder_options(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'export.json'
            payload = {'created_at': object()}

            runtime_lock_utils.write_json_file(target, payload, default=str)

            stored = runtime_lock_utils.load_json_file(target, default={})
            self.assertIsInstance(stored.get('created_at'), str)

    def test_json_lock_path_falls_back_to_tmp_when_target_dir_is_not_writable(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'ore_deposits.json'
            target.write_text('[]', encoding='utf-8')

            with patch.object(runtime_lock_utils.os, 'access', return_value=False):
                lock_path = runtime_lock_utils._json_lock_path(target)
                self.assertTrue(str(lock_path).startswith(tempfile.gettempdir()))
                self.assertIn(target.name, lock_path.name)

                loaded = runtime_lock_utils.load_json_file(target, default=[])

            self.assertEqual(loaded, [])
            self.assertTrue(lock_path.exists())

            try:
                lock_path.unlink()
            except FileNotFoundError:
                pass


class JsonModuleStateTests(unittest.TestCase):
    def test_fetch_scientific_papers_state_uses_locked_helpers(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / 'scientific_papers_fetch_state.json'
            payload = {'completed_localities': ['Bor'], 'completed_queries': {'Bor': ['query']}, 'stats': {'queries': 1}}

            with patch.object(fetch_scientific_papers, 'STATE_PATH', str(state_path)):
                fetch_scientific_papers.save_state(payload)
                self.assertEqual(fetch_scientific_papers.load_state(), payload)

    def test_map_feature_enricher_state_uses_locked_helpers(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / 'map_feature_state.json'
            payload = {'completed_features': {'ore::Bor': True}, 'completed_queries': {'ore::Bor||q': True}}

            with patch.object(map_feature_paper_enricher, 'STATE_PATH', str(state_path)):
                map_feature_paper_enricher._save_state(payload)
                self.assertEqual(map_feature_paper_enricher._load_state(), payload)

    def test_locality_geocache_save_and_load_uses_locked_helpers(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / 'locality_geocache.json'
            payload = {'bor': {'lat': 44.0, 'lon': 22.0}}

            original_cache = locality_data._geocache
            try:
                locality_data._geocache = dict(payload)
                with patch.object(locality_data, 'CACHE_FILE', str(cache_path)):
                    locality_data._save_geocache()
                    locality_data._geocache = {}
                    self.assertEqual(locality_data._load_geocache(), payload)
            finally:
                locality_data._geocache = original_cache

    def test_locality_geocache_load_does_not_swallow_keyboard_interrupt(self):
        with patch.object(locality_data, 'CACHE_FILE', '/tmp/locality_geocache.json'), patch.object(
            locality_data.os.path,
            'exists',
            return_value=True,
        ), patch.object(
            locality_data,
            'load_json_file',
            side_effect=KeyboardInterrupt(),
        ):
            with self.assertRaises(KeyboardInterrupt):
                locality_data._load_geocache()

    def test_science_news_should_update_does_not_swallow_keyboard_interrupt(self):
        with patch.object(
            science_news_updater.os.path,
            'getmtime',
            side_effect=KeyboardInterrupt(),
        ), patch.object(
            science_news_updater.os.path,
            'exists',
            return_value=True,
        ):
            with self.assertRaises(KeyboardInterrupt):
                science_news_updater.should_update('/tmp/science_news.json')


if __name__ == '__main__':
    unittest.main()
