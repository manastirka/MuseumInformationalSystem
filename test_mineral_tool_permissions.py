#!/usr/bin/env python3
"""Regression tests for mineral subnav tool route permissions."""

from pathlib import Path
import unittest


class MineralToolPermissionTests(unittest.TestCase):
    def setUp(self):
        self.collections_routes = Path('blueprints/collections.py').read_text(encoding='utf-8')
        self.vehicle_routes = Path('blueprints/vehicles.py').read_text(encoding='utf-8')

    def test_mineral_collection_type_maps_to_mineral_module(self):
        self.assertIn("'mineral': 'mineral_database'", self.collections_routes)

    def test_mineral_tools_are_available_to_mineral_module_users(self):
        self.assertIn("@collections_bp.route('/admin/inventory_book')\n@module_access_required('mineral_database')", self.collections_routes)
        self.assertIn("@collections_bp.route('/admin/inventory_reconciliation', endpoint='inventory_reconciliation')\n@module_access_required('mineral_database')", self.collections_routes)
        self.assertIn("@vehicles_bp.route('/admin/virtual_depot')\n@module_access_required('mineral_database')", self.vehicle_routes)

    def test_pdf_export_checks_requested_collection_access(self):
        self.assertIn("@collections_bp.route('/admin/export_collection_to_pdf/<collection_type>')\n@login_required", self.collections_routes)
        self.assertIn('access_denied = _ensure_collection_type_access(collection_type)', self.collections_routes)


if __name__ == '__main__':
    unittest.main()
