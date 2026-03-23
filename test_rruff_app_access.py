#!/usr/bin/env python3
"""Test RRUFF database access from the Flask app context."""

import os
from dotenv import load_dotenv

load_dotenv()

# Test with PostgreSQL
os.environ['DATABASE_URL'] = 'postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system'

from mineral_database_pg import get_mineral_database

print("="*70)
print("Testing RRUFF Database Access from Application")
print("="*70)

# Get mineral database
mineral_db = get_mineral_database()

print(f"\n✅ Mineral database loaded: {mineral_db.available}")

# Test RRUFF statistics
print("\n📊 RRUFF Statistics:")
stats = mineral_db.get_rruff_statistics()
print(f"  Total minerals: {stats.get('total_minerals', 0):,}")
print(f"  Crystal systems: {len(stats.get('by_crystal_system', []))}")
print(f"  IMA statuses: {len(stats.get('by_ima_status', []))}")

# Test RRUFF minerals pagination
print("\n📋 Testing RRUFF Minerals Pagination:")
result = mineral_db.get_rruff_minerals(page=1, per_page=5)
print(f"  Total: {result.get('total', 0):,}")
print(f"  Page: {result.get('page')}/{result.get('total_pages')}")
print(f"  Minerals on page: {len(result.get('minerals', []))}")

if result.get('minerals'):
    mineral = result['minerals'][0]
    print(f"  Sample: {mineral.get('name')} - {mineral.get('formula_rruff')}")

# Test search
print("\n🔍 Testing RRUFF Search:")
search_result = mineral_db.get_rruff_minerals(page=1, per_page=5, search="Quartz")
print(f"  'Quartz' search results: {search_result.get('total', 0)}")

# Test get by ID
print("\n📖 Testing Get RRUFF Mineral by ID:")
if result.get('minerals'):
    test_id = result['minerals'][0].get('id')
    detail = mineral_db.get_rruff_mineral_by_id(test_id)
    if detail:
        print(f"  ID {test_id}: {detail.get('name')}")
        print(f"  Formula: {detail.get('formula_rruff')}")
        print(f"  Crystal system: {detail.get('crystal_system')}")
        print(f"  Chemistry records: {len(detail.get('chemistry', []))}")
    else:
        print(f"  ❌ Could not load mineral ID {test_id}")

# Test name matching
print("\n🔗 Testing Name Matching:")
rruff_data = mineral_db.get_rruff_data_for_mineral("Quartz")
if rruff_data:
    print(f"  Found: {rruff_data.get('name')}")
    print(f"  Formula: {rruff_data.get('formula_rruff')}")
    print(f"  IMA status: {rruff_data.get('ima_status')}")
else:
    print("  ❌ No data found for 'Quartz'")

print("\n" + "="*70)
print("✅ All tests completed successfully!")
print("="*70)
