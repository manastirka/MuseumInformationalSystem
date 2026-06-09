#!/usr/bin/env python3
"""Test meteorite collection data loading and display"""

import os
import sys

# Set DATABASE_URL
os.environ.setdefault('DATABASE_URL', 'postgresql://aleksandarlukovic@localhost:5432/museum_system')

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import phase3a module
import phase3a_databases

# Load meteorite collection
print("🧪 Testing Meteorite Collection Database\n")
print("="*60)

data = phase3a_databases.get_meteorite_collection_database()

print(f"\n📊 Total specimens loaded: {len(data['specimens'])}")
print(f"\n📈 Statistics:")
for key, value in data['statistics'].items():
    if key == 'total_mass_grams':
        print(f"   {key}: {value:.2f} g ({value/1000:.2f} kg)")
    else:
        print(f"   {key}: {value}")

print(f"\n🇷🇸 Serbian Meteorites:")
serbian_count = 0
for spec in data['specimens']:
    if spec.get('serbian_meteorite'):
        serbian_count += 1
        print(f"   ✓ {spec['catalog_number']}: {spec['specimen_name']}")
        if spec.get('fall_type'):
            print(f"      Fall type: {spec['fall_type']}")
        if spec.get('meteorite_class'):
            print(f"      Class: {spec['meteorite_class']}")

print(f"\n🌍 Foreign Meteorites: {len(data['specimens']) - serbian_count}")

print("\n" + "="*60)
print("✅ Test complete!")
