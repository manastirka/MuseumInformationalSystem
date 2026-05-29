#!/usr/bin/env python3
"""Phase B regression tests for collection_media_views authorization fixes."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-collections-media')

import app as museum_app
import collection_media_views


class _FakeStorage:
    """Minimal image storage stub returning metadata + an on-disk image path."""

    def __init__(self, metadata, image_path):
        self._metadata = metadata
        self._image_path = image_path

    def get_image_metadata(self, image_id):
        return self._metadata

    def get_image_path(self, image_id, size='original'):
        return self._image_path


class GetImageByIdAuthorizationTests(unittest.TestCase):
    """get_image_by_id must enforce per-collection authorization, not just login."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.image_path = Path(self._tmp.name) / 'img.jpg'
        self.image_path.write_bytes(b'binarydata')

    def tearDown(self):
        self._tmp.cleanup()

    def _storage_for(self, database_name, entity_type):
        metadata = {
            'image_id': 'x',
            'database_name': database_name,
            'entity_type': entity_type,
            'entity_id': '1',
        }
        return _FakeStorage(metadata, self.image_path)

    def test_logged_in_user_without_module_access_is_forbidden(self):
        """A logged-in user lacking access to the owning collection must be 403,
        not served the raw image by id."""
        storage = self._storage_for('minerals', 'mineral')

        with museum_app.app.test_request_context('/api/images/minerals_mineral_1_x'):
            from flask import session

            session['user_id'] = 7
            session['user_email'] = 'nobody@example.com'
            session['user_role'] = 'employee'

            with patch.object(
                museum_app.app, 'user_has_module_access', return_value=False
            ):
                result = collection_media_views.get_image_by_id(
                    'minerals_mineral_1_x',
                    get_image_storage=lambda: storage,
                )

        # Tuple form -> (response, status_code)
        status = result[1] if isinstance(result, tuple) else result.status_code
        self.assertEqual(status, 403)

    def test_anonymous_user_for_non_public_collection_requires_auth(self):
        """Anonymous request for a non-public collection image must be 401."""
        storage = self._storage_for('minerals', 'mineral')

        with museum_app.app.test_request_context('/api/images/minerals_mineral_1_x'):
            result = collection_media_views.get_image_by_id(
                'minerals_mineral_1_x',
                get_image_storage=lambda: storage,
            )

        status = result[1] if isinstance(result, tuple) else result.status_code
        self.assertEqual(status, 401)

    def test_logged_in_user_with_module_access_is_served(self):
        """A user with module access to the owning collection still gets the image."""
        storage = self._storage_for('minerals', 'mineral')

        with museum_app.app.test_request_context('/api/images/minerals_mineral_1_x'):
            from flask import session

            session['user_id'] = 7
            session['user_email'] = 'curator@example.com'
            session['user_role'] = 'employee'

            with patch.object(
                museum_app.app, 'user_has_module_access', return_value=True
            ):
                response = collection_media_views.get_image_by_id(
                    'minerals_mineral_1_x',
                    get_image_storage=lambda: storage,
                )

        self.assertEqual(response.status_code, 200)
        response.close()

    def test_public_qr_collection_image_served_anonymously(self):
        """Images owned by a public QR collection remain anonymously accessible."""
        storage = self._storage_for('botany', 'botany')

        with museum_app.app.test_request_context('/api/images/botany_botany_1_x'):
            response = collection_media_views.get_image_by_id(
                'botany_botany_1_x',
                get_image_storage=lambda: storage,
            )

        self.assertEqual(response.status_code, 200)
        response.close()


if __name__ == '__main__':
    unittest.main()
