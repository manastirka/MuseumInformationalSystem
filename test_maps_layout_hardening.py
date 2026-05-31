#!/usr/bin/env python3
"""Regression tests for geological map control layout hardening."""

from pathlib import Path
import unittest


class GeologicalMapLayoutHardeningTests(unittest.TestCase):
    def setUp(self):
        self.template = Path('templates/admin_maps.html').read_text(encoding='utf-8')
        self.routes = Path('blueprints/maps.py').read_text(encoding='utf-8')
        self.base_template = Path('templates/base.html').read_text(encoding='utf-8')
        self.layer_views = Path('maps_layer_views.py').read_text(encoding='utf-8')

    def test_right_layer_controls_are_static_and_self_healing(self):
        self.assertIn('id="map-right-col"', self.template)
        self.assertIn('class="map-controls"', self.template)
        self.assertIn('id="toggle-overlay"', self.template)
        self.assertIn('id="toggle-map-sheets"', self.template)
        self.assertIn('function hardenMapLayerControls()', self.template)
        self.assertIn('window.addEventListener(\'resize\', hardenMapLayerControls);', self.template)

    def test_map_columns_do_not_wrap_right_controls_away_on_desktop(self):
        self.assertIn('#map-row {\n        flex-wrap: nowrap;', self.template)
        self.assertIn('#map-wrapper {\n        min-width: 0;', self.template)
        self.assertIn('.map-right-col {\n        position: relative;', self.template)
        self.assertIn('flex: 0 0 auto;', self.template)
        self.assertIn('@media (max-width: 991.98px)', self.template)

    def test_map_routes_do_not_import_app_by_name(self):
        self.assertNotIn('import app as museum_app', self.routes)
        self.assertIn('def _museum_app_module():', self.routes)
        self.assertIn('current_app.root_path', self.routes)

    def test_alpine_navbar_components_exist_before_alpine_loads(self):
        notification_def = self.base_template.index('window.notificationBell = function()')
        mail_def = self.base_template.index('window.mailNotifier = function()')
        alpine_load = self.base_template.index('cdn.min.js')

        self.assertLess(notification_def, alpine_load)
        self.assertLess(mail_def, alpine_load)

    def test_static_map_layer_json_reads_do_not_require_lock_files(self):
        self.assertNotIn('load_json_file', self.layer_views)
        self.assertIn("with open(file_path, 'r', encoding='utf-8') as handle:", self.layer_views)
        self.assertNotIn("'.paleo_localities.json.lock'", self.layer_views)


if __name__ == '__main__':
    unittest.main()
