import unittest

from inventory_reconciliation import InventoryReconciliation
from mineral_search_utils import build_search_specs


class MineralSearchUtilsTests(unittest.TestCase):
    def test_multi_term_inventory_search_marks_inventory_only_terms(self):
        specs = build_search_specs("M123, 456, Quartz, BEZ-0001")

        self.assertEqual([spec["term"] for spec in specs], ["M123", "456", "Quartz", "BEZ-0001"])
        self.assertTrue(specs[0]["inventory_only"])
        self.assertEqual(specs[0]["inv_num"], "123")
        self.assertTrue(specs[1]["inventory_only"])
        self.assertEqual(specs[1]["inv_num"], "456")
        self.assertFalse(specs[2]["inventory_only"])
        self.assertEqual(specs[3]["inv_prefix"], "BEZ-0001%")

    def test_single_term_numeric_search_keeps_general_behavior(self):
        specs = build_search_specs("123")

        self.assertEqual(len(specs), 1)
        self.assertFalse(specs[0]["inventory_only"])
        self.assertEqual(specs[0]["inv_num"], "123")


class InventoryReconciliationSearchTests(unittest.TestCase):
    def setUp(self):
        self.reconciliation = InventoryReconciliation(inventory_db="unused.db")
        self.reconciliation._inventory_cache = [
            {"inventory_number": 101, "name": "Kalcit", "locality": "Trepca", "category": "Mineral", "sheet": "A1"},
            {"inventory_number": 202, "name": "Kvarc", "locality": "Bor", "category": "Mineral", "sheet": "A2"},
            {"inventory_number": 303, "name": "Pirit", "locality": "Majdanpek", "category": "Mineral", "sheet": "A3"},
        ]

    def test_search_inventory_matches_comma_separated_names(self):
        results = self.reconciliation.search_inventory(name="kalcit, kvarc")

        self.assertEqual([item["inventory_number"] for item in results], [101, 202])

    def test_search_inventory_matches_comma_separated_inventory_numbers(self):
        results = self.reconciliation.search_inventory(inv_number="101, M202")

        self.assertEqual([item["inventory_number"] for item in results], [101, 202])

    def test_search_inventory_invalid_inventory_filter_returns_no_matches(self):
        results = self.reconciliation.search_inventory(inv_number="abc")

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
