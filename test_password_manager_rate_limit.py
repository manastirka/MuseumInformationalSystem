#!/usr/bin/env python3
"""Regression tests for password manager route throttling."""

import unittest

from flask_limiter.util import get_qualified_name

import app as museum_app
from rate_limit_ext import limiter


class PasswordManagerRateLimitTests(unittest.TestCase):
    def test_reset_route_has_rate_limit(self):
        view = museum_app.app.view_functions.get('admin.api_password_manager_reset')
        self.assertIsNotNone(view, 'admin.api_password_manager_reset route is missing')

        qualified_name = get_qualified_name(view)
        self.assertIn(qualified_name, limiter._marked_for_limiting)

        groups = limiter.limit_manager._decorated_limits.get(qualified_name)
        self.assertTrue(groups, 'no decorated limits registered for password reset')
        self.assertIn('5 per minute', [group.limit_provider for group in groups])


if __name__ == '__main__':
    unittest.main()
