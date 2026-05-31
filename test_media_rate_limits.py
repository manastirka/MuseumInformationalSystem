#!/usr/bin/env python3
"""Regression tests for specimen media route throttling."""

import re
import unittest
from pathlib import Path


class MediaRateLimitTests(unittest.TestCase):
    def test_specimen_media_routes_keep_high_page_safe_rate_limit(self):
        app_text = Path('app.py').read_text(encoding='utf-8')

        for route_name in (
            'get_specimen_image',
            'get_specimen_image_full',
            'get_specimen_thumbnail',
        ):
            pattern = (
                r'@app\.route\([^\n]+\)\n'
                r'(?:#.*\n)*'
                r'@limiter\.limit\("600 per minute"\)\n'
                rf'def {route_name}\('
            )
            self.assertRegex(app_text, pattern)


if __name__ == '__main__':
    unittest.main()
