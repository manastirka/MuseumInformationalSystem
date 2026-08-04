#!/usr/bin/env python3
"""
Inventory Reconciliation Tool
Compares physical inventory book data with actual revisioned database data
"""
import os
import logging
import json
from collections import defaultdict
from difflib import SequenceMatcher
from datetime import datetime
from typing import Dict, Iterable, List, Optional

from dotenv import load_dotenv
from runtime_lock_utils import write_json_file

try:
    import psycopg
    from psycopg.rows import dict_row as pg_dict_row
except ImportError:  # pragma: no cover - optional dependency
    psycopg = None
    pg_dict_row = None


logger = logging.getLogger(__name__)
load_dotenv()

class InventoryReconciliation:
    """Tool to compare inventory book with actual mineral database."""

    def __init__(self, inventory_db='data/inventory_book.db', mineral_db=None, database_url: Optional[str] = None):
        self.inventory_db = inventory_db
        # Default to revised mineralogical database
        self.mineral_db = mineral_db or 'PrirodnjackiMuzej/prirodnjacki_muzej.sqlite'
        self._collection_cache: Optional[Dict[str, List[Dict]]] = None
        self._inventory_cache: Optional[List[Dict]] = None

        # Optional PostgreSQL backend (Phase 2)
        self.database_url = database_url or os.environ.get('DATABASE_URL')
        self._postgres_enabled = bool(self.database_url and psycopg)
        if self.database_url and not psycopg:
            logger.warning("DATABASE_URL set but psycopg driver missing; PostgreSQL access unavailable.")

    # ------------------------------------------------------------------
    # Inventory loading helpers
    # ------------------------------------------------------------------

    def refresh_inventory_cache(self):
        """Force reloading inventory data (used after migrations)."""
        self._inventory_cache = None

    def _load_inventory_items(self) -> List[Dict]:
        """Load inventory entries from PostgreSQL."""
        if self._inventory_cache is not None:
            return self._inventory_cache

        if self._postgres_enabled:
            try:
                rows = self._load_inventory_from_postgres()
            except Exception as exc:  # pragma: no cover - depends on DB connectivity
                logger.error("PostgreSQL inventory load failed: %s.", exc)
                rows = []
                self._postgres_enabled = False
        else:
            logger.error("Inventory reconciliation requires PostgreSQL access.")
            rows = []

        self._inventory_cache = rows
        return self._inventory_cache

    def _load_inventory_from_postgres(self) -> List[Dict]:
        if not psycopg:  # pragma: no cover - guarded earlier
            raise RuntimeError("psycopg driver is required for PostgreSQL inventory access.")

        # Convert sqlalchemy-style URL to psycopg format if needed
        db_url = self.database_url.replace('postgresql+psycopg://', 'postgresql://')

        query = """
            SELECT
                id,
                inventory_number,
                inventory_number_raw,
                name,
                locality,
                quantity,
                acquisition_info,
                collector,
                notes,
                sheet,
                row_number,
                category,
                revisited,
                physical_location,
                revision_date,
                in_printed_book
            FROM inventory_entries
            ORDER BY inventory_number
        """

        with psycopg.connect(db_url, row_factory=pg_dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = [self._normalize_inventory_row(row) for row in cur.fetchall()]

        return rows

    def _normalize_inventory_row(self, row: Dict) -> Dict:
        """Normalize inventory rows so downstream code works uniformly."""
        normalized = dict(row)
        normalized['inventory_number_raw'] = normalized.get('inventory_number_raw') or normalized.get('inventory_number')
        normalized['inventory_number'] = self._normalize_inventory_number(normalized.get('inventory_number'))
        normalized['name'] = (normalized.get('name') or '').strip()
        normalized['locality'] = (normalized.get('locality') or '').strip()
        normalized['category'] = (normalized.get('category') or '').strip()
        normalized['sheet'] = (normalized.get('sheet') or '').strip()
        normalized['acquisition_info'] = (normalized.get('acquisition_info') or '').strip()
        normalized['collector_donator'] = normalized.get('collector_donator') or normalized.get('collector')
        normalized['collector'] = (normalized.get('collector') or normalized.get('collector_donator') or '').strip()
        normalized['notes'] = (normalized.get('notes') or '').strip()
        normalized['physical_location'] = (normalized.get('physical_location') or '').strip()
        normalized['quantity'] = (normalized.get('quantity') or '').strip()
        normalized['in_printed_book'] = bool(row.get('in_printed_book'))

        revisited = normalized.get('revisited')
        if isinstance(revisited, bool):
            normalized['revisited'] = revisited
        elif isinstance(revisited, (int, float)):
            normalized['revisited'] = revisited != 0
        elif isinstance(revisited, str):
            normalized['revisited'] = revisited.strip().lower() in ('1', 'true', 'да')

        row_number = normalized.get('row_number')
        if isinstance(row_number, str) and row_number.strip().isdigit():
            normalized['row_number'] = int(row_number.strip())

        return normalized

    # ------------------------------------------------------------------
    # Inventory-facing helpers
    # ------------------------------------------------------------------

    def get_inventory_book_items(self, force_refresh: bool = False):
        """Get all items from inventory book."""
        if force_refresh:
            self.refresh_inventory_cache()
        return [dict(item) for item in self._load_inventory_items()]

    def get_inventory_by_number(self, inv_number):
        """Get specific inventory item by number."""
        normalized = self._normalize_inventory_number(inv_number)
        for item in self._load_inventory_items():
            if item.get('inventory_number') == normalized:
                return dict(item)
        return None

    def get_inventory_summary(self):
        """Get summary statistics from inventory book."""
        items = self._load_inventory_items()
        total = len(items)
        unique_numbers = {
            item['inventory_number'] for item in items if item.get('inventory_number') is not None
        }

        by_category: Dict[str, int] = defaultdict(int)
        by_sheet: Dict[str, int] = defaultdict(int)
        inventory_numbers = []

        for item in items:
            category = item.get('category')
            if category:
                by_category[category] += 1

            sheet = item.get('sheet')
            if sheet:
                by_sheet[sheet] += 1

            inv = item.get('inventory_number')
            if inv is not None:
                inventory_numbers.append(inv)

        inv_min = min(inventory_numbers) if inventory_numbers else None
        inv_max = max(inventory_numbers) if inventory_numbers else None

        return {
            'total_items': total,
            'unique_inventory_numbers': len(unique_numbers),
            'by_category': dict(by_category),
            'by_sheet': dict(by_sheet),
            'inventory_range': {
                'min': inv_min,
                'max': inv_max
            }
        }

    def find_similar_names(self, name, threshold=0.6):
        """Find similar mineral names in inventory."""
        all_names = [item['name'] for item in self._load_inventory_items() if item.get('name')]

        matches = []
        for inv_name in all_names:
            ratio = SequenceMatcher(None, name.lower(), inv_name.lower()).ratio()
            if ratio >= threshold:
                matches.append({
                    'name': inv_name,
                    'similarity': ratio
                })

        matches.sort(key=lambda x: x['similarity'], reverse=True)
        return matches[:10]  # Top 10 matches

    @staticmethod
    def _normalize_inventory_number(value) -> Optional[int]:
        """Normalize inventory numbers from various formats to integers."""
        if value is None:
            return None

        if isinstance(value, int):
            return value if value > 0 else None

        if isinstance(value, float):
            # Inventory numbers are stored as floats (e.g., 42.0)
            normalized = int(round(value))
            return normalized if normalized > 0 else None

        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return None

            # Remove common prefixes like "M1234" or extra characters
            digits = ''.join(ch for ch in stripped if ch.isdigit())
            if digits:
                normalized = int(digits)
                return normalized if normalized > 0 else None

        return None

    @staticmethod
    def _split_search_terms(value) -> List[str]:
        """Split comma-separated user input into normalized lowercase terms."""
        if value is None:
            return []

        if isinstance(value, (list, tuple, set)):
            raw_terms = [str(item).strip() for item in value]
        else:
            raw_terms = [term.strip() for term in str(value).split(',')]

        return [term.lower() for term in raw_terms if term]

    def _normalize_inventory_numbers(self, value) -> List[int]:
        """Normalize one or more comma-separated inventory numbers."""
        numbers: List[int] = []
        seen = set()

        for term in self._split_search_terms(value):
            normalized = self._normalize_inventory_number(term)
            if normalized is not None and normalized not in seen:
                seen.add(normalized)
                numbers.append(normalized)

        return numbers

    def get_mineral_collection_data(self, force_refresh: bool = False) -> Dict[str, List[Dict]]:
        """Load mineral collection data from revised database.

        Returns a dictionary with two lists:
            - with_inventory: Records that have inventory numbers
            - without_inventory: Records missing inventory numbers
        """
        if self._collection_cache is not None and not force_refresh:
            return self._collection_cache

        collection_with_inventory: List[Dict] = []
        collection_without_inventory: List[Dict] = []

        if not self._postgres_enabled:
            logger.error("Mineral collection reconciliation requires PostgreSQL access.")
        else:
            try:
                db_url = self.database_url.replace('postgresql+psycopg://', 'postgresql://')
                with psycopg.connect(db_url, row_factory=pg_dict_row) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("""
                            SELECT
                                id,
                                inventory_number,
                                item_name AS name,
                                card_locality AS locality,
                                item_name AS predmet,
                                storage_location AS location,
                                acquisition_method,
                                acquisition_date,
                                donor AS legator,
                                identifier AS identifikovao,
                                quantity
                            FROM minerals
                        """)

                        for row in cursor.fetchall():
                            normalized_inv = self._normalize_inventory_number(row['inventory_number'])

                            record = {
                                'id': row['id'],
                                'inventory_number': normalized_inv,
                                'inventory_number_raw': row['inventory_number'],
                                'name': (row['name'] or '').strip(),
                                'locality': (row['locality'] or '').strip(),
                                'category': (row['predmet'] or '').strip(),
                                'location': (row['location'] or '').strip(),
                                'acquisition_method': (row['acquisition_method'] or '').strip(),
                                'acquisition_date': row['acquisition_date'],
                                'legator': (row['legator'] or '').strip(),
                                'identified_by': (row['identifikovao'] or '').strip(),
                                'quantity': row['quantity']
                            }

                            if normalized_inv is None:
                                collection_without_inventory.append(record)
                            else:
                                collection_with_inventory.append(record)
            except Exception as exc:
                logger.error("Неуспело учитавање минералошке базе из PostgreSQL: %s", exc)

        self._collection_cache = {
            'with_inventory': collection_with_inventory,
            'without_inventory': collection_without_inventory
        }
        return self._collection_cache

    def _group_by_inventory_number(self, records: Iterable[Dict]) -> Dict[int, List[Dict]]:
        """Group records by normalized inventory number."""
        grouped: Dict[int, List[Dict]] = defaultdict(list)
        for record in records:
            inv = record.get('inventory_number')
            if inv is not None:
                grouped[inv].append(record)
        return grouped

    def get_collection_index(self, force_refresh: bool = False) -> Dict[int, List[Dict]]:
        """Return collection data grouped by inventory number."""
        data = self.get_mineral_collection_data(force_refresh=force_refresh)
        return self._group_by_inventory_number(data.get('with_inventory', []))

    def search_inventory(self, **kwargs):
        """
        Search inventory book by various criteria.

        Args:
            name: Mineral name (partial match)
            locality: Locality (partial match)
            inv_number: Specific inventory number
            inv_range: Tuple of (min, max) inventory numbers
            category: Category
            sheet: Sheet name
        """
        items = self._load_inventory_items()
        results = []

        name_terms = self._split_search_terms(kwargs.get('name', ''))
        locality_terms = self._split_search_terms(kwargs.get('locality', ''))
        inv_number = kwargs.get('inv_number')
        inv_range = kwargs.get('inv_range')
        category = (kwargs.get('category') or '').strip().lower()
        sheet = (kwargs.get('sheet') or '').strip().lower()
        normalized_inventories = self._normalize_inventory_numbers(inv_number)
        has_inventory_filter = bool(str(inv_number).strip()) if inv_number is not None else False

        for item in items:
            match = True
            if name_terms:
                item_name = (item.get('name') or '').lower()
                match = any(term in item_name for term in name_terms)

            if match and locality_terms:
                item_locality = (item.get('locality') or '').lower()
                match = any(term in item_locality for term in locality_terms)

            if match and has_inventory_filter:
                match = bool(normalized_inventories) and item.get('inventory_number') in normalized_inventories

            if match and inv_range and all(inv_range):
                min_inv, max_inv = inv_range
                normalized_min = self._normalize_inventory_number(min_inv)
                normalized_max = self._normalize_inventory_number(max_inv)
                inv_value = item.get('inventory_number')
                if inv_value is None or normalized_min is None or normalized_max is None:
                    match = False
                else:
                    match = normalized_min <= inv_value <= normalized_max

            if match and category:
                match = (item.get('category') or '').lower() == category

            if match and sheet:
                match = (item.get('sheet') or '').lower() == sheet

            if match:
                results.append(dict(item))

        results.sort(key=lambda x: (x.get('inventory_number') is None, x.get('inventory_number')))
        return results

    def get_available_sheets(self) -> List[str]:
        """Return sorted list of available sheets for UI filters."""
        items = self._load_inventory_items()
        sheets = {item.get('sheet') for item in items if item.get('sheet')}
        return sorted(sheets)

    def generate_discrepancy_report(self, mineral_collection_data=None):
        """
        Generate a report of discrepancies between inventory book and actual collection.

        Args:
            mineral_collection_data: List of dictionaries with actual collection data
                                     Each should have: inventory_number, name, locality, etc.
        """
        report = {
            'inventory_book_summary': self.get_inventory_summary(),
            'timestamp': None,
            'discrepancies': {
                'missing_in_collection': [],
                'missing_in_inventory_book': [],
                'name_mismatches': [],
                'locality_mismatches': [],
                'additional_info': []
            },
            'statistics': {
                'total_in_book': 0,
                'total_in_collection': 0,
                'total_collection_records': 0,
                'matched': 0,
                'missing_from_collection': 0,
                'missing_from_book': 0,
                'name_differences': 0,
                'locality_differences': 0,
                'collection_without_inventory': 0,
                'book_duplicate_numbers': 0,
                'collection_duplicate_numbers': 0
            }
        }

        if mineral_collection_data is None:
            collection_bundle = self.get_mineral_collection_data()
            mineral_collection_data = collection_bundle.get('with_inventory', [])
            collection_without_inventory = collection_bundle.get('without_inventory', [])
        else:
            collection_without_inventory = []

        if not mineral_collection_data and not collection_without_inventory:
            print("⚠ Нема доступних ревидираних података минералошке базе за упоређивање")
            print("   Извештај ће садржати само податке из књиге инвентара")
            return report

        # Get all inventory book items
        book_items = self.get_inventory_book_items()
        book_by_inv = self._group_by_inventory_number(book_items)
        collection_by_inv = self._group_by_inventory_number(mineral_collection_data)

        # Statistics
        book_numbers = set(book_by_inv.keys())
        collection_numbers = set(collection_by_inv.keys())

        report['statistics']['total_in_book'] = len(book_numbers)
        report['statistics']['total_in_collection'] = len(collection_numbers)
        report['statistics']['total_collection_records'] = len(mineral_collection_data) + len(collection_without_inventory)
        report['statistics']['collection_without_inventory'] = len(collection_without_inventory)
        report['statistics']['book_duplicate_numbers'] = sum(1 for inv in book_by_inv if len(book_by_inv[inv]) > 1)
        report['statistics']['collection_duplicate_numbers'] = sum(1 for inv in collection_by_inv if len(collection_by_inv[inv]) > 1)

        # Missing items analysis
        missing_in_collection_numbers = sorted(book_numbers - collection_numbers)
        missing_in_inventory_numbers = sorted(collection_numbers - book_numbers)

        for inv_num in missing_in_collection_numbers:
            book_records = book_by_inv[inv_num]
            report['discrepancies']['missing_in_collection'].append({
                'inventory_number': inv_num,
                'name': '; '.join(sorted({(item.get('name') or '').strip() for item in book_records if item.get('name')})),
                'locality': '; '.join(sorted({(item.get('locality') or '').strip() for item in book_records if item.get('locality')})),
                'sheet': '; '.join(sorted({(item.get('sheet') or '').strip() for item in book_records if item.get('sheet')})),
                'count': len(book_records)
            })

        for inv_num in missing_in_inventory_numbers:
            collection_records = collection_by_inv[inv_num]
            report['discrepancies']['missing_in_inventory_book'].append({
                'inventory_number': inv_num,
                'name': '; '.join(sorted({(item.get('name') or '').strip() for item in collection_records if item.get('name')})),
                'locality': '; '.join(sorted({(item.get('locality') or '').strip() for item in collection_records if item.get('locality')})),
                'count': len(collection_records)
            })

        report['statistics']['missing_from_collection'] = len(missing_in_collection_numbers)
        report['statistics']['missing_from_book'] = len(missing_in_inventory_numbers)

        # Check for mismatches in matched items
        matched_numbers = sorted(book_numbers & collection_numbers)
        report['statistics']['matched'] = len(matched_numbers)

        for inv_num in matched_numbers:
            book_records = book_by_inv[inv_num]
            collection_records = collection_by_inv[inv_num]

            # Note duplicate counts for additional info
            if len(book_records) != len(collection_records) or len(book_records) > 1 or len(collection_records) > 1:
                report['discrepancies']['additional_info'].append({
                    'type': 'duplicate_or_count_mismatch',
                    'inventory_number': inv_num,
                    'book_count': len(book_records),
                    'collection_count': len(collection_records)
                })

            # Evaluate name similarity using primary names
            book_names = [item.get('name', '').strip() for item in book_records if item.get('name')]
            collection_names = [item.get('name', '').strip() for item in collection_records if item.get('name')]

            primary_book_name = max(book_names, key=len) if book_names else ''
            primary_collection_name = max(collection_names, key=len) if collection_names else ''

            if primary_book_name and primary_collection_name:
                similarity = SequenceMatcher(None, primary_book_name.lower(), primary_collection_name.lower()).ratio()
                if similarity < 0.8:
                    report['discrepancies']['name_mismatches'].append({
                        'inventory_number': inv_num,
                        'book_name': primary_book_name,
                        'collection_name': primary_collection_name,
                        'similarity': similarity,
                        'collection_ids': [item['id'] for item in collection_records]
                    })
                    report['statistics']['name_differences'] += 1

            # Evaluate locality differences
            book_localities = {item.get('locality', '').strip() for item in book_records if item.get('locality')}
            collection_localities = {item.get('locality', '').strip() for item in collection_records if item.get('locality')}

            if book_localities and collection_localities:
                normalized_book_localities = {loc.lower() for loc in book_localities}
                normalized_collection_localities = {loc.lower() for loc in collection_localities}

                if normalized_book_localities.isdisjoint(normalized_collection_localities):
                    report['discrepancies']['locality_mismatches'].append({
                        'inventory_number': inv_num,
                        'book_locality': '; '.join(sorted(book_localities)),
                        'collection_locality': '; '.join(sorted(collection_localities)),
                        'collection_ids': [item['id'] for item in collection_records]
                    })
                    report['statistics']['locality_differences'] += 1

        report['timestamp'] = datetime.now().isoformat()

        return report

    def export_report(self, report, output_path='data/inventory_reconciliation_report.json'):
        """Export reconciliation report to JSON."""
        write_json_file(output_path, report)

        print(f"✓ Report exported to {output_path}")

    def print_report_summary(self, report):
        """Print a summary of the reconciliation report."""
        print("\n" + "="*80)
        print("INVENTORY RECONCILIATION REPORT SUMMARY")
        print("="*80)

        stats = report['statistics']
        print(f"\nOverall Statistics:")
        print(f"  Total in inventory book: {stats['total_in_book']}")
        print(f"  Total in collection: {stats['total_in_collection']}")
        print(f"  Matched items: {stats['matched']}")

        print(f"\nDiscrepancies:")
        print(f"  Missing from physical collection: {stats['missing_from_collection']}")
        print(f"  Missing from inventory book: {stats['missing_from_book']}")
        print(f"  Name differences: {stats['name_differences']}")

        # Show sample discrepancies
        disc = report['discrepancies']

        if disc['missing_in_collection']:
            print(f"\n  Sample items missing from collection (first 5):")
            for item in disc['missing_in_collection'][:5]:
                print(f"    - Inv #{item['inventory_number']}: {item['name']}")

        if disc['missing_in_inventory_book']:
            print(f"\n  Sample items missing from inventory book (first 5):")
            for item in disc['missing_in_inventory_book'][:5]:
                print(f"    - Inv #{item['inventory_number']}: {item['name']}")

        if disc['name_mismatches']:
            print(f"\n  Sample name mismatches (first 5):")
            for item in disc['name_mismatches'][:5]:
                print(f"    - Inv #{item['inventory_number']}:")
                print(f"      Book: {item['book_name']}")
                print(f"      Collection: {item['collection_name']}")
                print(f"      Similarity: {item['similarity']:.1%}")

        print("\n" + "="*80)


def main():
    """Main function for testing."""
    print("Inventory Reconciliation Tool")
    print("="*80)

    reconciliation = InventoryReconciliation()

    # Get summary
    print("\nInventory Book Summary:")
    summary = reconciliation.get_inventory_summary()
    print(f"  Total items: {summary['total_items']}")
    print(f"  Unique inventory numbers: {summary['unique_inventory_numbers']}")
    print(f"  Inventory range: {summary['inventory_range']['min']} - {summary['inventory_range']['max']}")

    print(f"\n  By sheet:")
    for sheet, count in summary['by_sheet'].items():
        print(f"    - {sheet}: {count}")

    if summary['by_category']:
        print(f"\n  By category:")
        for category, count in summary['by_category'].items():
            print(f"    - {category}: {count}")

    # Test search
    print(f"\n" + "="*80)
    print("Sample search: minerals from Trepča")
    results = reconciliation.search_inventory(locality='Trepča')
    print(f"Found {len(results)} items")
    for item in results[:5]:
        print(f"  - Inv #{item['inventory_number']}: {item['name']}")

    # Generate reconciliation report using revised collection data
    print(f"\n" + "="*80)
    print("Generating reconciliation report...")
    report = reconciliation.generate_discrepancy_report()
    reconciliation.print_report_summary(report)
    reconciliation.export_report(report)

    print(f"\n✓ Reconciliation tool test complete!")


if __name__ == "__main__":
    main()
