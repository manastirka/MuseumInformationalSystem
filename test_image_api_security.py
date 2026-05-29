"""Tests for image API authentication, authorization, and CSRF behavior."""

import unittest
import os
import sys
import io
import importlib.util
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
import image_api as image_api_mod
import image_storage_engine as image_storage_mod


def _load_root_app_module():
    """Load the repository root app.py deterministically for tests."""
    os.environ['SECRET_KEY'] = 'test-key'
    os.environ['FLASK_ENV'] = 'development'
    module_name = 'museum_root_app_for_tests'
    if module_name in sys.modules:
        return sys.modules[module_name]

    app_path = Path(__file__).resolve().parent / 'app.py'
    spec = importlib.util.spec_from_file_location(module_name, app_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ImageAPIAuthTests(unittest.TestCase):
    """Ensure every image API route rejects anonymous requests."""

    @classmethod
    def setUpClass(cls):
        os.environ['WTF_CSRF_ENABLED'] = 'False'
        museum_app = _load_root_app_module()
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

    def test_upload_requires_collection_access(self):
        self._login_as('employee')
        resp = self._post(
            '/api/images/upload',
            data={
                'database': 'x',
                'entity_type': 'collection_item',
                'entity_id': '1',
                'file': (io.BytesIO(b'not-an-image'), 'test.jpg'),
            },
            content_type='multipart/form-data',
        )
        self.assertEqual(resp.status_code, 403)

    def test_get_image_requires_auth(self):
        resp = self._get('/api/images/test-id')
        self.assertEqual(resp.status_code, 401)

    def test_http_login_cookie_respects_non_secure_session_config(self):
        resp = self.client.get('/login', base_url='http://localhost')
        set_cookie = resp.headers.get('Set-Cookie', '')
        self.assertNotIn('Secure;', set_cookie)
        self.assertIn('HttpOnly', set_cookie)

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

    def test_backup_receive_requires_token(self):
        self._login_as('employee')
        resp = self._post('/api/images/backup/receive',
                          data={'image_id': '1'})
        self.assertEqual(resp.status_code, 401)

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

    def test_restore_rejects_sibling_prefix_path(self):
        """Sibling path with same prefix should not pass validation."""
        self._login_as('admin')
        # If backup root is /x/storage/backups, then /x/storage/backups_evil should fail
        resp = self._post('/api/images/backup/restore',
                          json={'backup_path': str(image_api_mod._BACKUP_ROOT) + '_evil/data'})
        self.assertEqual(resp.status_code, 400)

    # --- Delete and metadata require admin (object-level auth) ---

    def test_delete_requires_admin(self):
        self._login_as('employee')
        resp = self._delete('/api/images/test-id')
        self.assertEqual(resp.status_code, 403)

    def test_metadata_requires_admin(self):
        self._login_as('employee')
        resp = self._get('/api/images/test-id/metadata')
        self.assertEqual(resp.status_code, 403)

    def test_get_image_served_by_login_required_media_handler(self):
        # Policy: GET image-by-id is served by the @login_required media handler
        # so authorized non-admins (curators, map users) can view images; it is
        # NOT admin-only. Verified at the routing layer (the deferred `import app`
        # in the handler body is not exercisable under this test bootstrap).
        rules = [
            rule for rule in self.app.url_map.iter_rules()
            if rule.rule == '/api/images/<image_id>' and 'GET' in rule.methods
        ]
        view_funcs = {self.app.view_functions[rule.endpoint] for rule in rules}
        self.assertEqual(len(view_funcs), 1, f'conflicting handlers: {[r.endpoint for r in rules]}')
        (view_func,) = view_funcs
        self.assertEqual(view_func.__module__, 'blueprints.media')
        self.assertEqual(view_func.__name__, 'get_image_by_id')

    def test_entity_images_requires_admin(self):
        self._login_as('employee')
        resp = self._get('/api/images/entity/db/type/1')
        self.assertEqual(resp.status_code, 403)

    def test_stats_requires_admin(self):
        self._login_as('employee')
        resp = self._get('/api/images/stats')
        self.assertEqual(resp.status_code, 403)

    # --- Backup name sanitization ---

    def test_backup_create_rejects_unsafe_name(self):
        self._login_as('admin')
        resp = self._post('/api/images/backup/create',
                          json={'backup_name': '../etc/evil'})
        self.assertEqual(resp.status_code, 400)

    def test_backup_create_rejects_spaces_in_name(self):
        self._login_as('admin')
        resp = self._post('/api/images/backup/create',
                          json={'backup_name': 'my backup name'})
        self.assertEqual(resp.status_code, 400)

    def test_backup_create_accepts_safe_name(self):
        """A safe alphanumeric name should not be rejected at validation."""
        self._login_as('admin')
        resp = self._post('/api/images/backup/create',
                          json={'backup_name': 'daily-2026-03-23'})
        # May fail for other reasons (no storage), but should NOT be 400
        self.assertNotEqual(resp.status_code, 400)


class ImageAPICsrfTests(unittest.TestCase):
    """Verify only intended image routes are exempt from CSRF."""

    @classmethod
    def setUpClass(cls):
        museum_app = _load_root_app_module()
        cls.app = museum_app.app
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = True

    def setUp(self):
        self.base_url = 'https://localhost'
        self.client = self.app.test_client()

    def _login_as(self, role='employee'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 'test@test.rs'
            sess['user_email'] = 'test@test.rs'
            sess['role'] = role
            sess['user_role'] = role

    def test_backup_create_enforces_csrf(self):
        self._login_as('admin')
        resp = self.client.post(
            '/api/images/backup/create',
            base_url=self.base_url,
            json={'backup_name': 'safe_name'},
        )
        self.assertEqual(resp.status_code, 400)

    def test_backup_server_enforces_csrf(self):
        self._login_as('admin')
        resp = self.client.post(
            '/api/images/backup/server',
            base_url=self.base_url,
            json={'image_id': 'test-id'},
        )
        self.assertEqual(resp.status_code, 400)

    def test_upload_route_is_still_csrf_exempt(self):
        self._login_as('employee')
        resp = self.client.post(
            '/api/images/upload',
            base_url=self.base_url,
            data={'database': 'x', 'entity_type': 'y', 'entity_id': '1'},
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json(), {'error': 'No file provided'})

    def test_backup_receive_route_is_token_based_and_csrf_exempt(self):
        resp = self.client.post(
            '/api/images/backup/receive',
            base_url=self.base_url,
            data={'image_id': '1'},
        )
        self.assertEqual(resp.status_code, 401)


class ImageStorageFactoryTests(unittest.TestCase):
    """Ensure different storage paths receive isolated storage instances."""

    def setUp(self):
        image_storage_mod._image_storage_instances.clear()

    def test_storage_instances_are_isolated_by_path(self):
        storage_a = image_storage_mod.get_image_storage('/tmp/image-store-a')
        storage_b = image_storage_mod.get_image_storage('/tmp/image-store-b')
        storage_a_again = image_storage_mod.get_image_storage('/tmp/image-store-a')

        self.assertIsNot(storage_a, storage_b)
        self.assertIs(storage_a, storage_a_again)


if __name__ == '__main__':
    unittest.main()
