"""Phase C low-severity hardening tests for the image-api cluster.

Focus: Serbian Cyrillic filenames must keep a valid extension after
secure_filename so image_storage_engine._validate_image accepts the upload.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-image-api')

import io
import uuid
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from flask import Flask
from werkzeug.utils import secure_filename

import image_api as image_api_mod


def _make_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret'
    app.register_blueprint(image_api_mod.image_api)
    return app


class _FakeStorage:
    """Records the temp file_path handed to store_image and the saved file."""

    def __init__(self):
        self.base_path = Path('/tmp/museum-test-c-image-api/storage')
        (self.base_path / 'temp').mkdir(parents=True, exist_ok=True)
        self.last_file_path = None

    def store_image(self, file_path=None, **kwargs):
        self.last_file_path = file_path
        # Mimic _validate_image: reject when the temp path lacks a valid suffix.
        if Path(file_path).suffix.lower() not in {
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'
        }:
            return None
        return 'img-123'


class CyrillicUploadExtensionTests(unittest.TestCase):
    """Cyrillic filenames must not lose their extension during temp naming."""

    def setUp(self):
        self.app = _make_app()
        # secure_filename drops the dot for Cyrillic names: 'Минерал.jpg' -> 'jpg'
        self.cyrillic_name = 'Минерал.jpg'
        self.assertEqual(Path(secure_filename(self.cyrillic_name)).suffix, '')

    def _patch_login(self):
        # Bypass auth decorators which are imported at module load.
        return patch.dict(
            image_api_mod.session, {}, clear=False
        )

    @patch.object(image_api_mod, 'get_image_storage')
    @patch('image_api.secure_filename', side_effect=secure_filename)
    def test_upload_route_preserves_cyrillic_extension(self, _sf, mock_get_storage):
        fake = _FakeStorage()
        mock_get_storage.return_value = fake

        # Patch the auth decorator's permission gate and login session.
        with patch.object(image_api_mod, '_can_upload_to_database', return_value=True):
            client = self.app.test_client()
            with client.session_transaction() as sess:
                sess['logged_in'] = True
                sess['user_id'] = 1
                sess['user_role'] = 'admin'
                sess['user_email'] = 'a@b.c'
            data = {
                'database': 'mineral',
                'entity_type': 'collection_item',
                'entity_id': '7',
                'file': (io.BytesIO(b'fakejpeg'), self.cyrillic_name),
            }
            resp = client.post('/api/images/upload', data=data,
                               content_type='multipart/form-data')

        self.assertIsNotNone(fake.last_file_path,
                             "store_image was never reached")
        suffix = Path(fake.last_file_path).suffix.lower()
        self.assertIn(suffix,
                      {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'},
                      f"temp path lost its extension: {fake.last_file_path!r}")
        self.assertEqual(resp.status_code, 201)

    @patch('werkzeug.datastructures.FileStorage.save', autospec=True)
    @patch('pathlib.Path.mkdir')
    @patch.object(image_api_mod, 'get_image_storage')
    @patch.object(image_api_mod, '_check_backup_token', return_value=True)
    def test_receive_backup_preserves_cyrillic_extension(
        self, _tok, mock_get_storage, _mkdir, _save
    ):
        # receive_backup writes to a hardcoded ./storage/backups/server path
        # that is not writable in the sandbox; the suffix logic under test runs
        # before any disk I/O, so stub mkdir/save and assert on the temp path.
        fake = _FakeStorage()
        mock_get_storage.return_value = fake

        client = self.app.test_client()
        data = {
            'image_id': 'abc',
            'metadata': '{}',
            'file': (io.BytesIO(b'fakejpeg'), self.cyrillic_name),
        }
        resp = client.post('/api/images/backup/receive', data=data,
                           content_type='multipart/form-data',
                           headers={'X-Backup-Token': 'x'})

        self.assertIsNotNone(fake.last_file_path,
                             "store_image was never reached")
        suffix = Path(fake.last_file_path).suffix.lower()
        self.assertIn(suffix,
                      {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'},
                      f"backup temp path lost its extension: {fake.last_file_path!r}")
        self.assertEqual(resp.status_code, 201)


if __name__ == '__main__':
    unittest.main()
