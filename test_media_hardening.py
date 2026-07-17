#!/usr/bin/env python3
"""Regression tests for specimen media access control and error sanitization."""

import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-flask-session')

import app as museum_app
import archive_signature_blueprint


class MediaAccessHardeningTests(unittest.TestCase):
    def setUp(self):
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def _login(self, *, email='user@example.com', role='employee'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = email
            sess['user_name'] = 'Test User'
            sess['user_role'] = role
            sess['is_admin'] = role == 'admin'

    def test_anonymous_restricted_specimen_image_requires_auth(self):
        response = self.client.get(
            '/api/specimen_image/minerals/mineral/1',
            base_url=self.base_url,
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.get_json(),
            {'success': False, 'message': 'Морате бити пријављени'},
        )

    def test_logged_in_user_without_collection_access_gets_forbidden(self):
        self._login(role='employee')

        response = self.client.get(
            '/api/specimen_thumbnail/minerals/mineral/1',
            base_url=self.base_url,
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.get_json(),
            {'success': False, 'message': 'Немате дозволу за приступ овој слици'},
        )

    def test_public_qr_collection_image_remains_available_anonymously(self):
        with patch.object(
            museum_app.collection_media_views,
            '_send_entity_image',
            return_value=museum_app.app.response_class('ok', status=200),
        ) as mocked_sender:
            response = self.client.get(
                '/api/specimen_image/botany/botany/BOT-1',
                base_url=self.base_url,
            )

        self.assertEqual(response.status_code, 200)
        mocked_sender.assert_called_once()


class ThumbnailPerformanceHardeningTests(unittest.TestCase):
    def test_mineral_table_uses_local_placeholder_instead_of_thumbnail_storm(self):
        template = Path('templates/admin_mineral_collection.html').read_text(encoding='utf-8')

        # Placeholder is still used as the fallback for minerals without an image,
        # and lazy/async attributes still defer rendering to avoid a thumbnail storm.
        self.assertIn("url_for('static', filename='images/specimen-placeholder-thumb.png')", template)
        self.assertIn('loading="lazy"', template)
        self.assertIn('decoding="async"', template)

    def test_mineral_table_shows_fototeka_thumbnail_when_photo_linked(self):
        """Minerals with a Фототека photo must render its derivative, not the
        placeholder. The placeholder is only for minerals without a photo, so we
        avoid an HTTP request per empty row while still showing real images."""
        template = Path('templates/admin_mineral_collection.html').read_text(encoding='utf-8')

        self.assertIn('mineral.foto_id', template)
        self.assertIn(
            "url_for('fototeka.fototeka_media', fotografija_id=mineral.foto_id, kind='thumb')",
            template,
        )


class ErrorSanitizationTests(unittest.TestCase):
    def setUp(self):
        self.client = museum_app.app.test_client()
        self.base_url = 'https://localhost'

    def _login(self, *, email='user@example.com', role='employee'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_email'] = email
            sess['user_name'] = 'Test User'
            sess['user_role'] = role
            sess['is_admin'] = role == 'admin'

    def test_archive_api_hides_internal_exception_details(self):
        self._login(role='employee')

        with patch.object(
            archive_signature_blueprint,
            'get_postgres_connection',
            side_effect=RuntimeError('postgresql://secret-host/museum'),
        ):
            response = self.client.get('/api/archive/requests', base_url=self.base_url)

        self.assertEqual(response.status_code, 500)
        body = response.get_json()
        self.assertEqual(
            body,
            {'success': False, 'message': 'Дошло је до грешке на серверу.'},
        )
        self.assertNotIn('secret-host', json.dumps(body, ensure_ascii=False))


if __name__ == '__main__':
    unittest.main()
