#!/usr/bin/env python3
"""Regression tests for blueprint support helpers."""

import unittest

import app_blueprint_support


class _LimiterStub:
    def __init__(self):
        self.exempted = []
        self.limited = []

    def limit(self, rule):
        def decorator(view):
            self.limited.append((rule, view.__name__))
            return view
        return decorator

    def exempt(self, view):
        self.exempted.append(view.__name__)
        return view


class BlueprintRateLimitTests(unittest.TestCase):
    def test_map_tile_endpoints_are_rate_limit_exempt(self):
        class _App:
            view_functions = {
                'maps.api_map_tile_index': lambda: None,
                'maps.api_map_tile': lambda filename=None: None,
                'maps.api_geological_sheet_image': lambda folder_name=None, image_type=None: None,
                'maps.api_map_elevation': lambda: None,
            }

        limiter = _LimiterStub()
        app_blueprint_support.apply_endpoint_rate_limits(_App(), limiter)

        self.assertEqual(len(limiter.exempted), 4)


if __name__ == '__main__':
    unittest.main()
