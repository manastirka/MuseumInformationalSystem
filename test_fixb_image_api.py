"""Phase B regression tests for image_api.py (cluster: image-api).

Bug under test: the /upload route forwards the raw `metadata` form value
(a JSON *string*) straight into storage.store_image, which then does
json.dumps(metadata or {}). For a client-supplied JSON object string this
double-encodes the value, storing an opaque escaped string in the JSONB
`custom_metadata` column instead of a queryable object.
"""

import io
import os
import json

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-b-image-api')

import unittest
from unittest import mock

from flask import Flask

import image_api as image_api_mod


def _make_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret'
    app.config['WTF_CSRF_ENABLED'] = False
    app.register_blueprint(image_api_mod.image_api)
    return app


class _RecordingStorage:
    """Stand-in for the storage engine that records store_image kwargs."""

    def __init__(self):
        self.base_path = None
        self.captured = {}

    def store_image(self, **kwargs):
        self.captured = kwargs
        return 'img_123'


class UploadMetadataTests(unittest.TestCase):
    def setUp(self):
        self.app = _make_app()
        self.client = self.app.test_client()
        self.storage = _RecordingStorage()

        # base_path/temp must be writable; point at a temp dir.
        import tempfile
        from pathlib import Path
        self._tmp = tempfile.mkdtemp(prefix='fixb-image-')
        (Path(self._tmp) / 'temp').mkdir(parents=True, exist_ok=True)
        self.storage.base_path = Path(self._tmp)

    def _post_upload(self, metadata_value):
        data = {
            'database': 'mineral',
            'entity_type': 'collection_item',
            'entity_id': '42',
            'file': (io.BytesIO(b'fake-image-bytes'), 'photo.jpg'),
        }
        if metadata_value is not None:
            data['metadata'] = metadata_value

        with mock.patch.object(image_api_mod, 'get_image_storage', return_value=self.storage), \
                mock.patch.object(image_api_mod, '_can_upload_to_database', return_value=True):
            # login_required checks session['user_id']; seed it so it passes.
            with self.client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['user_email'] = 'tester@example.com'
                sess['user_role'] = 'admin'
            return self.client.post(
                '/api/images/upload',
                data=data,
                content_type='multipart/form-data',
            )

    def test_object_metadata_passed_as_dict(self):
        """A JSON-object metadata string must reach store_image as a dict."""
        resp = self._post_upload('{"foo": "bar", "n": 3}')
        self.assertEqual(resp.status_code, 201, resp.get_data(as_text=True))
        passed = self.storage.captured.get('metadata')
        # Root cause: must be a dict so json.dumps serializes exactly once.
        self.assertIsInstance(
            passed, dict,
            f"metadata forwarded to store_image was {type(passed).__name__}: {passed!r}",
        )
        self.assertEqual(passed, {'foo': 'bar', 'n': 3})

    def test_absent_metadata_defaults_to_empty_dict(self):
        resp = self._post_upload(None)
        self.assertEqual(resp.status_code, 201, resp.get_data(as_text=True))
        passed = self.storage.captured.get('metadata')
        self.assertEqual(passed, {})

    def test_empty_metadata_defaults_to_empty_dict(self):
        resp = self._post_upload('')
        self.assertEqual(resp.status_code, 201, resp.get_data(as_text=True))
        passed = self.storage.captured.get('metadata')
        self.assertEqual(passed, {})

    def test_invalid_json_metadata_rejected(self):
        resp = self._post_upload('{not valid json')
        self.assertEqual(resp.status_code, 400, resp.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
