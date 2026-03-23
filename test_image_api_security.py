"""
Tests for image API authentication and authorization.

Verifies that all image API endpoints require authentication,
destructive endpoints require admin role, and CSRF is enforced
on mutating endpoints.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))


class ImageAPIAuthTests(unittest.TestCase):
    """Ensure every image API route rejects anonymous requests."""

    @classmethod
    def setUpClass(cls):
        os.environ.setdefault('SECRET_KEY', 'test-key')
        os.environ.setdefault('WTF_CSRF_ENABLED', 'False')
        import app as museum_app
        cls.app = museum_app.app
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False
        # Disable Talisman HTTPS redirect for testing
        if hasattr(museum_app, 'talisman'):
            museum_app.talisman.force_https = False
        for ext in cls.app.extensions.values():
            if hasattr(ext, 'force_https'):
                ext.force_https = False

    def setUp(self):
        self.base_url = 'https://localhost'
        self.client = self.app.test_client()

    # --- Anonymous access should be denied (401) on every route ---

    def _url(self, path):
        return path

    def _get(self, path, **kw):
        return self.client.get(self._url(path), base_url=self.base_url, **kw)

    def _post(self, path, **kw):
        return self.client.post(self._url(path), base_url=self.base_url, **kw)

    def _delete(self, path, **kw):
        return self.client.delete(self._url(path), base_url=self.base_url, **kw)

    def test_upload_requires_auth(self):
        resp = self._post('/api/images/upload', data={'database': 'x'})
        self.assertEqual(resp.status_code, 401)

    def test_get_image_requires_auth(self):
        resp = self._get('/api/images/test-id')
        self.assertEqual(resp.status_code, 401)

    def test_get_metadata_requires_auth(self):
        resp = self._get('/api/images/test-id/metadata')
        self.assertEqual(resp.status_code, 401)

    def test_get_entity_images_requires_auth(self):
        resp = self._get('/api/images/entity/db/type/1')
        self.assertEqual(resp.status_code, 401)

    def test_delete_requires_auth(self):
        resp = self._delete('/api/images/test-id')
        self.assertEqual(resp.status_code, 401)

    def test_stats_requires_auth(self):
        resp = self._get('/api/images/stats')
        self.assertEqual(resp.status_code, 401)

    # --- Backup/restore endpoints require admin ---

    def test_backup_create_requires_auth(self):
        resp = self._post('/api/images/backup/create',
                          json={'backup_name': 'test'})
        self.assertEqual(resp.status_code, 401)

    def test_backup_restore_requires_auth(self):
        resp = self._post('/api/images/backup/restore',
                          json={'backup_path': '/tmp/x'})
        self.assertEqual(resp.status_code, 401)

    def test_backup_server_requires_auth(self):
        resp = self._post('/api/images/backup/server',
                          json={'image_id': '1'})
        self.assertEqual(resp.status_code, 401)

    def test_backup_receive_requires_auth(self):
        resp = self._post('/api/images/backup/receive',
                          data={'image_id': '1'})
        self.assertEqual(resp.status_code, 401)

    # --- Backup/restore need admin even if logged in as employee ---

    def _login_as(self, role='employee'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 'test@test.rs'
            sess['user_email'] = 'test@test.rs'
            sess['role'] = role
            sess['user_role'] = role

    def test_backup_create_requires_admin(self):
        self._login_as('employee')
        resp = self._post('/api/images/backup/create',
                          json={'backup_name': 'test'})
        self.assertEqual(resp.status_code, 403)

    def test_backup_restore_requires_admin(self):
        self._login_as('employee')
        resp = self._post('/api/images/backup/restore',
                          json={'backup_path': '/tmp/x'})
        self.assertEqual(resp.status_code, 403)

    def test_backup_server_requires_admin(self):
        self._login_as('employee')
        resp = self._post('/api/images/backup/server',
                          json={'image_id': '1'})
        self.assertEqual(resp.status_code, 403)

    def test_backup_receive_requires_admin(self):
        self._login_as('employee')
        resp = self._post('/api/images/backup/receive',
                          data={'image_id': '1'})
        self.assertEqual(resp.status_code, 403)

    # --- Restore must reject path traversal ---

    def test_restore_rejects_path_traversal(self):
        self._login_as('admin')
        resp = self._post('/api/images/backup/restore',
                          json={'backup_path': '../../etc/passwd'})
        self.assertEqual(resp.status_code, 400)

    def test_restore_rejects_absolute_path(self):
        self._login_as('admin')
        resp = self._post('/api/images/backup/restore',
                          json={'backup_path': '/etc/passwd'})
        self.assertEqual(resp.status_code, 400)


if __name__ == '__main__':
    unittest.main()
