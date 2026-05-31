#!/usr/bin/env python3
"""Regression tests for mineralogical database local sub navigation."""

from pathlib import Path
import unittest


class MineralSubnavTests(unittest.TestCase):
    def setUp(self):
        self.mineral_template = Path('templates/admin_mineral_collection.html').read_text(encoding='utf-8')
        self.base_template = Path('templates/base.html').read_text(encoding='utf-8')

    def test_mineral_tools_are_grouped_in_local_subnav(self):
        self.assertIn('class="mineral-subnav"', self.mineral_template)
        self.assertIn('Музејска збирка', self.mineral_template)
        self.assertIn('RRUFF база', self.mineral_template)
        self.assertIn('Научне вести', self.mineral_template)
        self.assertIn('id="mineralToolsDropdown"', self.mineral_template)
        rendered_subnav = self.mineral_template.split('<nav class="mineral-subnav"', 1)[1].split('</nav>', 1)[0]
        self.assertIn('RRUFF база', rendered_subnav)
        self.assertIn("search_mode='rruff'", rendered_subnav)
        self.assertIn('Научне вести', rendered_subnav)
        self.assertIn("url_for('science.admin_science_news')", rendered_subnav)
        self.assertNotIn("url_for('museum_news')", rendered_subnav)

        for label in (
            '3D Депо',
            'Локалитети',
            'Инвентар',
            'Упоређивање',
            'QR примерци',
            'QR кутије',
            'Слике',
            'Извоз',
        ):
            self.assertIn(label, self.mineral_template)

    def test_old_quick_action_strip_is_removed(self):
        self.assertNotIn('quick-actions-row', self.mineral_template)
        self.assertNotIn('quick-action-card', self.mineral_template)

    def test_header_does_not_show_decorative_rruff_stat(self):
        header = self.mineral_template.split('<!-- Mineralogical Database Sub Navigation -->', 1)[0]
        self.assertNotIn('<span class="stat-label">RRUFF база</span>', header)
        self.assertIn('<span class="stat-label">Примерака</span>', header)
        self.assertIn('<span class="stat-label">Локалитета</span>', header)

    def test_rruff_is_not_in_global_external_database_menu(self):
        self.assertNotIn('RRUFF минерали', self.base_template)
        self.assertNotIn("url_for('rruff_minerals')", self.base_template)
        self.assertIn('NHM London Data Portal', self.base_template)

    def test_mineral_tool_links_use_registered_blueprint_endpoints(self):
        self.assertIn("url_for('vehicles.virtual_depot')", self.mineral_template)
        self.assertIn("url_for('collections.inventory_book')", self.mineral_template)
        self.assertIn("url_for('collections.inventory_reconciliation')", self.mineral_template)
        self.assertIn("url_for('collections.export_collection_to_pdf', collection_type='mineral')", self.mineral_template)

    def test_large_science_news_panel_is_not_rendered(self):
        self.assertIn('{% if false and not is_rruff_mode %}', self.mineral_template)
        self.assertIn('{% elif is_rruff_mode %}', self.mineral_template)
        disabled_news_block = self.mineral_template.split('{% if false and not is_rruff_mode %}', 1)[1].split('{% else %}', 1)[0]
        self.assertIn('id="science-news-shell"', disabled_news_block)

    def test_mineral_search_uses_professional_aligned_grid(self):
        self.assertIn('.mineral-search-form .search-grid', self.mineral_template)
        self.assertIn('grid-template-columns: minmax(280px, 1fr) auto auto auto;', self.mineral_template)
        self.assertIn('<div class="search-grid">', self.mineral_template)
        self.assertIn('<div class="search-control">', self.mineral_template)
        self.assertIn('Подржани су зарезом раздвојени појмови', self.mineral_template)


if __name__ == '__main__':
    unittest.main()
