#!/usr/bin/env python3
"""Regression tests for geological raster tile support helpers."""

import tempfile
import unittest
from unittest.mock import patch

import maps_terrain_support


class MapsTerrainSupportTests(unittest.TestCase):
    def test_resolve_tile_cache_dir_uses_static_cache_when_parent_is_writable(self):
        with patch.object(maps_terrain_support.os, 'access', return_value=True):
            resolved = maps_terrain_support.resolve_tile_cache_dir()

        self.assertEqual(
            resolved,
            maps_terrain_support.os.path.join(maps_terrain_support.APP_ROOT, 'static', 'map_tiles'),
        )

    def test_resolve_tile_cache_dir_falls_back_to_tmp_when_static_parent_not_writable(self):
        with patch.object(maps_terrain_support.os, 'access', return_value=False), patch.dict(
            maps_terrain_support.os.environ,
            {},
            clear=False,
        ):
            resolved = maps_terrain_support.resolve_tile_cache_dir()

        self.assertEqual(
            resolved,
            maps_terrain_support.os.path.join(tempfile.gettempdir(), 'museum_info_system_map_tiles'),
        )


if __name__ == '__main__':
    unittest.main()
