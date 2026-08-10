#!/usr/bin/env python3
"""Regression tests for specimen media route throttling."""

import unittest

from flask_limiter.util import get_qualified_name

import app as museum_app
from rate_limit_ext import limiter


class MediaRateLimitTests(unittest.TestCase):
    def test_specimen_media_routes_keep_high_page_safe_rate_limit(self):
        for route_name in (
            'get_specimen_image',
            'get_specimen_image_full',
            'get_specimen_thumbnail',
        ):
            with self.subTest(route=route_name):
                view = museum_app.app.view_functions.get(f'media.{route_name}')
                self.assertIsNotNone(view, f'media.{route_name} route is missing')

                qualified_name = get_qualified_name(view)
                self.assertIn(qualified_name, limiter._marked_for_limiting)

                groups = limiter.limit_manager._decorated_limits.get(qualified_name)
                self.assertTrue(groups, f'no decorated limits registered for {route_name}')
                self.assertIn(
                    '600 per minute',
                    [group.limit_provider for group in groups],
                )


if __name__ == '__main__':
    unittest.main()
