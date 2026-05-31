#!/usr/bin/env python3
"""Regression tests for LAN-only nginx exposure."""

import re
import unittest
from pathlib import Path


class NginxLanRestrictionsTests(unittest.TestCase):
    def test_nginx_config_restricts_http_and_https_to_private_networks(self):
        config_text = Path('nginx_museum.conf').read_text(encoding='utf-8')

        http_server = re.search(
            r"server\s*\{\s*listen 80;.*?deny all;\s*return 301 https://\$host\$request_uri;\s*\}",
            config_text,
            re.DOTALL,
        )
        https_server = re.search(
            r"server\s*\{\s*listen 443 ssl;\s*listen \[::\]:443 ssl;\s*http2 on;.*?deny all;",
            config_text,
            re.DOTALL,
        )

        self.assertIsNotNone(http_server)
        self.assertIsNotNone(https_server)

        for needle in (
            'allow 127.0.0.1;',
            'allow ::1;',
            'allow 192.168.144.0/24;',
            'deny all;',
        ):
            self.assertGreaterEqual(config_text.count(needle), 2, needle)

        for broad_private_range in (
            'allow 10.0.0.0/8;',
            'allow 172.16.0.0/12;',
            'allow 192.168.0.0/16;',
            'allow fc00::/7;',
            'allow fe80::/10;',
        ):
            self.assertNotIn(broad_private_range, config_text)


if __name__ == '__main__':
    unittest.main()
