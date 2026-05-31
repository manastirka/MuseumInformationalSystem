#!/usr/bin/env python3
"""Regression tests for the dedicated scientific news page."""

from pathlib import Path
import unittest


class ScienceNewsPageTests(unittest.TestCase):
    def setUp(self):
        self.routes = Path('blueprints/science.py').read_text(encoding='utf-8')
        self.template = Path('templates/admin_science_news.html').read_text(encoding='utf-8')

    def test_scientific_news_page_route_exists_for_mineral_users(self):
        self.assertIn("@science_bp.route('/admin/science_news')", self.routes)
        self.assertIn("@module_access_required('mineral_database')", self.routes)
        self.assertIn("def admin_science_news():", self.routes)
        self.assertIn("render_template('admin_science_news.html')", self.routes)

    def test_scientific_news_page_uses_science_news_api(self):
        self.assertIn('Научне вести', self.template)
        self.assertIn("fetch(`/api/science-news?", self.template)
        self.assertIn("secureFetch('/api/science-news'", self.template)
        self.assertIn("secureFetch(`/api/science-news/${encodeURIComponent(newsId)}`", self.template)
        self.assertNotIn("url_for('museum_news')", self.template)


if __name__ == '__main__':
    unittest.main()
