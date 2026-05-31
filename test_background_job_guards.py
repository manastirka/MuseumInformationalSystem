#!/usr/bin/env python3
"""Regression tests for background job ownership and atomic JSON writes."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')

import app as museum_app
import runtime_lock_utils
import science_news_updater
import map_feature_paper_enricher


class BackgroundJobGuardTests(unittest.TestCase):
    def setUp(self):
        self.original_env = os.environ.get(museum_app.BACKGROUND_WORKER_ROLE_ENV)
        museum_app._background_jobs_started = False
        museum_app._background_jobs_lock_fd = None

    def tearDown(self):
        if self.original_env is None:
            os.environ.pop(museum_app.BACKGROUND_WORKER_ROLE_ENV, None)
        else:
            os.environ[museum_app.BACKGROUND_WORKER_ROLE_ENV] = self.original_env

    def test_start_background_jobs_refuses_non_worker_process(self):
        os.environ.pop(museum_app.BACKGROUND_WORKER_ROLE_ENV, None)

        with patch.object(museum_app, 'update_science_news_background') as news_mock, patch.object(
            museum_app.map_feature_paper_enricher,
            'start_enrichment_background',
        ) as enrich_mock:
            started = museum_app.start_background_jobs()

        self.assertFalse(started)
        news_mock.assert_not_called()
        enrich_mock.assert_not_called()

    def test_start_background_jobs_requires_cross_process_lock(self):
        os.environ[museum_app.BACKGROUND_WORKER_ROLE_ENV] = '1'

        with patch.object(museum_app, 'try_acquire_process_lock', return_value=None), patch.object(
            museum_app,
            'update_science_news_background',
        ) as news_mock, patch.object(
            museum_app.map_feature_paper_enricher,
            'start_enrichment_background',
        ) as enrich_mock:
            started = museum_app.start_background_jobs()

        self.assertFalse(started)
        news_mock.assert_not_called()
        enrich_mock.assert_not_called()

    def test_start_background_jobs_runs_once_when_worker_owns_lock(self):
        os.environ[museum_app.BACKGROUND_WORKER_ROLE_ENV] = '1'

        with patch.object(museum_app, 'try_acquire_process_lock', return_value=123), patch.object(
            museum_app,
            'update_science_news_background',
        ) as news_mock, patch.object(
            museum_app.map_feature_paper_enricher,
            'start_enrichment_background',
        ) as enrich_mock:
            first = museum_app.start_background_jobs()
            second = museum_app.start_background_jobs()

        self.assertTrue(first)
        self.assertFalse(second)
        news_mock.assert_called_once()
        enrich_mock.assert_called_once()


class AtomicJsonWriteTests(unittest.TestCase):
    def test_atomic_write_json_persists_valid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'state.json'
            payload = {'status': 'ok', 'items': [1, 2, 3]}

            runtime_lock_utils.atomic_write_json(target, payload)

            self.assertEqual(json.loads(target.read_text('utf-8')), payload)

    def test_science_news_save_uses_atomic_writer(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'science_news.json'
            payload = [{'id': 'n1', 'title': 'News'}]

            self.assertTrue(science_news_updater.save_news(str(target), payload))
            self.assertEqual(json.loads(target.read_text('utf-8')), payload)

    def test_enricher_state_save_uses_atomic_writer(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / 'map_feature_papers_fetch_state.json'
            payload = {'completed_features': {'x': True}, 'completed_queries': {}}

            with patch.object(map_feature_paper_enricher, 'STATE_PATH', str(state_path)):
                map_feature_paper_enricher._save_state(payload)

            self.assertEqual(json.loads(state_path.read_text('utf-8')), payload)


if __name__ == '__main__':
    unittest.main()
