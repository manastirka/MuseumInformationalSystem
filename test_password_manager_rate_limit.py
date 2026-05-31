#!/usr/bin/env python3
"""Regression tests for password manager route throttling."""

import re
import unittest
from pathlib import Path


class PasswordManagerRateLimitTests(unittest.TestCase):
    def test_reset_route_has_rate_limit(self):
        app_source = Path(__file__).resolve().parent / 'app.py'
        content = app_source.read_text(encoding='utf-8')

        pattern = re.compile(
            r"@app\.route\('/api/admin/password_manager/reset', methods=\['POST'\]\)\n"
            r"@admin_required\n"
            r'@limiter\.limit\("5 per minute"\)\n'
            r"def api_password_manager_reset\(",
        )

        self.assertRegex(content, pattern)


if __name__ == '__main__':
    unittest.main()
