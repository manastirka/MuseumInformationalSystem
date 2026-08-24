#!/usr/bin/env python3
"""Regression tests for geological map control layout hardening."""

from pathlib import Path
import unittest


# Прекидачи слојева које постојећи JS адресира по id-у. Преуређење бочног
# менија у склопиве групе сме да их премести, али ниједан не сме да нестане
# нити да промени id — иначе addEventListener пуца на null.
POSTOJECI_PREKIDACI = (
    'toggle-overlay',
    'toggle-basemap',
    'toggle-field-markers',
    'toggle-ore-deposits',
    'toggle-stratigraphy',
    'toggle-paleontology',
    'toggle-sanja-mammals',
    'toggle-mining-operations',
    'toggle-exploration-licenses',
    'toggle-map-sheets',
    'toggle-geo-hover',
    'toggle-calibration',
)


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

    def test_every_existing_layer_toggle_id_survives_the_menu_regroup(self):
        for toggle_id in POSTOJECI_PREKIDACI:
            with self.subTest(toggle=toggle_id):
                self.assertEqual(
                    self.template.count('id="{}"'.format(toggle_id)), 1,
                    'прекидач {} мора да постоји тачно једном'.format(toggle_id),
                )

    def test_layer_menu_is_five_collapsible_groups(self):
        for grupa in ('podloga', 'geologija', 'rudarstvo', 'zbirke', 'alati'):
            with self.subTest(grupa=grupa):
                self.assertIn('data-map-group="{}"'.format(grupa), self.template)
                self.assertIn('data-map-group-badge="{}"'.format(grupa), self.template)
        self.assertIn('id="btn-ugasi-sve-slojeve"', self.template)
        self.assertIn("'mis.maps.grupe'", self.template)
        # Гашење мора да иде кроз прави change догађај, не кроз директан позив.
        self.assertIn("new Event('change', { bubbles: true })", self.template)
        # Основна карта (OSM) и алати остају упаљени.
        self.assertIn('id="toggle-basemap" data-map-layer="1" data-map-keep="1"',
                      self.template)

    def test_ogk_layers_use_theme_tokens_and_lazy_loading(self):
        for grupa in ('rudnici', 'kamenolomi', 'busotine', 'izvori',
                      'fosili', 'rasedi', 'jedinice', 'ostalo'):
            with self.subTest(grupa=grupa):
                self.assertIn('id="toggle-ogk-{}"'.format(grupa), self.template)
        self.assertIn('L.canvas({ pane: \'thematic-vector-pane\'', self.template)
        # markercluster се НЕ додаје (CSP + нова зависност) — само canvas.
        self.assertNotIn('L.markerClusterGroup', self.template)
        self.assertNotIn('leaflet.markercluster', self.template)
        self.assertIn('getComputedStyle(document.documentElement)', self.template)
        self.assertIn("fetch('/api/map/ogk-points?grupe='", self.template)
        # Пад fetch-а мора да се види у менију, не само у конзоли.
        self.assertIn('data-ogk-greska=', self.template)
        self.assertIn('function ogkGreska(', self.template)

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
