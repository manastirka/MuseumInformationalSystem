"""Reproducing test for the collections-media cluster bug.

Bug: GET /api/images/<image_id> has three identical Werkzeug rules:
  - image_api.get_image      (@admin_required)  -- registered first
  - media.get_image_by_id    (@login_required)  -- shadowed
  - get_image_by_id (alias)  (@login_required)  -- shadowed

Because the rules are equal-weight, route resolution falls back to
registration order and the admin-only image_api.get_image handler always
wins. Non-admin curators/map users who legitimately consume the endpoint
(image upload modal preview, map field-data thumbnails — both built on
@login_required map routes) therefore receive 403, while the intended
@login_required media.get_image_by_id handler is never reachable via the URL.
"""

import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-collections-media')

import importlib.util
import sys
import unittest
from pathlib import Path


def _load_root_app_module():
    """Load the repository root app.py deterministically for tests."""
    module_name = 'museum_root_app_for_collections_media_tests'
    if module_name in sys.modules:
        return sys.modules[module_name]

    app_path = Path(__file__).resolve().parent / 'app.py'
    spec = importlib.util.spec_from_file_location(module_name, app_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ImageByIdRouteResolutionTests(unittest.TestCase):
    """The canonical GET /api/images/<id> route must be deterministic and
    reachable by the authorized non-admin consumers it was built for."""

    @classmethod
    def setUpClass(cls):
        os.environ['WTF_CSRF_ENABLED'] = 'False'
        museum_app = _load_root_app_module()
        cls.museum_app = museum_app
        cls.app = museum_app.app
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False
        if hasattr(museum_app, 'talisman'):
            museum_app.talisman.force_https = False
        for ext in cls.app.extensions.values():
            if hasattr(ext, 'force_https'):
                ext.force_https = False

    def setUp(self):
        self.base_url = 'https://localhost'
        self.client = self.app.test_client()

    def _login_as(self, role='employee'):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 'test@test.rs'
            sess['user_email'] = 'test@test.rs'
            sess['role'] = role
            sess['user_role'] = role

    def test_no_conflicting_get_handlers_for_image_by_id_path(self):
        """GET /api/images/<image_id> must resolve to a single view function.

        A benign backward-compat alias that points at the SAME view function is
        fine, but two DIFFERENT view functions with conflicting authorization
        (admin-only vs login-only) make resolution depend on registration order
        rather than intent.
        """
        view_funcs = {
            self.app.view_functions[rule.endpoint]
            for rule in self.app.url_map.iter_rules()
            if rule.rule == '/api/images/<image_id>' and 'GET' in rule.methods
        }
        endpoints = sorted(
            rule.endpoint
            for rule in self.app.url_map.iter_rules()
            if rule.rule == '/api/images/<image_id>' and 'GET' in rule.methods
        )
        self.assertEqual(
            len(view_funcs),
            1,
            f'Conflicting GET handlers for /api/images/<image_id>: {endpoints}',
        )

    def test_image_by_id_served_by_login_required_media_handler(self):
        """The surviving GET handler must be the @login_required media handler
        (authorized non-admins may view), NOT the admin-only image_api handler
        that previously shadowed it. Asserted at the routing layer so the policy
        is verified without executing the handler body."""
        rules = [
            rule for rule in self.app.url_map.iter_rules()
            if rule.rule == '/api/images/<image_id>' and 'GET' in rule.methods
        ]
        view_funcs = {self.app.view_functions[rule.endpoint] for rule in rules}
        self.assertEqual(len(view_funcs), 1, f'conflicting handlers: {[r.endpoint for r in rules]}')
        (view_func,) = view_funcs
        self.assertEqual(view_func.__module__, 'blueprints.media')
        self.assertEqual(view_func.__name__, 'get_image_by_id')


if __name__ == '__main__':
    unittest.main()
