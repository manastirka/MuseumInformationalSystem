#!/usr/bin/env python3
"""Regression tests for specimen media access control and error sanitization."""

import json
import os
import tempfile
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
import image_api as image_api_mod


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
    def test_send_entity_image_uses_bounded_primary_path_lookup(self):
        class FastPathStorage:
            def __init__(self, image_path):
                self.image_path = image_path
                self.slow_lookup_called = False

            def get_primary_entity_image_path(self, database, entity_type, entity_id, size):
                self.fast_lookup_args = (database, entity_type, entity_id, size)
                return self.image_path

            def get_images_for_entity(self, database, entity_type, entity_id):
                self.slow_lookup_called = True
                return []

        with tempfile.TemporaryDirectory() as tmp_dir:
            image_path = Path(tmp_dir) / 'thumb.jpg'
            image_path.write_bytes(b'placeholder')
            storage = FastPathStorage(image_path)

            with museum_app.app.test_request_context('/'):
                response = museum_app.collection_media_views._send_entity_image(
                    lambda: storage,
                    'minerals',
                    'mineral',
                    '151',
                    'small',
                )

        self.assertEqual(response.status_code, 200)
        response.close()
        self.assertEqual(storage.fast_lookup_args, ('minerals', 'mineral', '151', 'small'))
        self.assertFalse(storage.slow_lookup_called)

    def test_mineral_table_uses_local_placeholder_instead_of_thumbnail_storm(self):
        template = Path('templates/admin_mineral_collection.html').read_text(encoding='utf-8')

        # Placeholder is still used as the fallback for minerals without an image,
        # and lazy/async attributes still defer rendering to avoid a thumbnail storm.
        self.assertIn("url_for('static', filename='images/specimen-placeholder-thumb.png')", template)
        self.assertIn('loading="lazy"', template)
        self.assertIn('decoding="async"', template)

    def test_mineral_table_shows_thumbnail_when_has_image(self):
        """Minerals with has_image=True must render the real thumbnail endpoint,
        not the static placeholder. The placeholder is only for minerals without
        an image, so we avoid an HTTP request per empty row while still showing
        real images when they exist."""
        template = Path('templates/admin_mineral_collection.html').read_text(encoding='utf-8')

        # The template must branch on mineral.has_image.
        self.assertIn('mineral.has_image', template)

        # When has_image is true, the row must point at the thumbnail endpoint
        # with the correct database/entity_type/entity_id parameters.
        self.assertIn(
            "url_for('get_specimen_thumbnail', database='minerals',"
            " entity_type='mineral', entity_id=mineral.id)",
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

    def test_image_api_hides_internal_exception_details(self):
        self._login(role='admin')

        with patch.object(
            image_api_mod,
            'get_image_storage',
            side_effect=RuntimeError('/srv/secret/path'),
        ):
            response = self.client.get('/api/images/stats', base_url=self.base_url)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), {'error': 'Internal server error'})

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
