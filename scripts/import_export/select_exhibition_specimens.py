#!/usr/bin/env python3
"""
Select 80 mineral specimens for permanent exhibition
Focus on Balkans/Yugoslavia specimens and worldwide representatives
"""

import sqlite3
import sys

DB_PATH = 'PrirodnjackiMuzej/prirodnjacki_muzej.sqlite'

def get_connection():
    return sqlite3.connect(DB_PATH)

# Get top localities
conn = get_connection()
cursor = conn.cursor()

print("Top localities in database:")
cursor.execute("""
    SELECT "Lokalitet sa kartice", COUNT(*) as count
    FROM minerali
    WHERE "Lokalitet sa kartice" IS NOT NULL AND "Lokalitet sa kartice" != ''
    GROUP BY "Lokalitet sa kartice"
    ORDER BY count DESC
    LIMIT 40
""")

localities = cursor.fetchall()
for loc, count in localities:
    print(f"{loc}: {count}")

print("\n" + "="*80)

# Balkans/Yugoslavia keywords for filtering
balkan_keywords = [
    'srbij', 'serbia', 'bosn', 'hrvatska', 'crna gora', 'montenegro',
    'slovenij', 'sloveni', 'makedon', 'kosovo', 'jugoslavij', 'yugoslav',
    'kopaonik', 'rtanj', 'jastrebac', 'bor', 'majdanpek', 'rudnik',
    'balkan', 'beograd', 'belgrade', 'trepča', 'trepca'
]

# Get minerals from Balkans/Yugoslavia regions
cursor.execute("""
    SELECT
        id,
        "Inv. broj" as inv_broj,
        "Naziv" as naziv,
        "Lokalitet sa kartice" as lokalitet,
        "Predmet" as predmet,
        "Napomena/opis" as opis,
        "Komentar/napomena" as komentar
    FROM minerali
    WHERE "Lokalitet sa kartice" IS NOT NULL
    AND "Lokalitet sa kartice" != ''
    AND "Naziv" IS NOT NULL
    AND "Naziv" != ''
    ORDER BY "Inv. broj"
""")

all_minerals = cursor.fetchall()

# Filter Balkans specimens
balkan_specimens = []
world_specimens = []

for mineral in all_minerals:
    mid, inv, naziv, lokalitet, predmet, opis, komentar = mineral
    lokalitet_lower = lokalitet.lower() if lokalitet else ''

    is_balkan = any(keyword in lokalitet_lower for keyword in balkan_keywords)

    if is_balkan:
        balkan_specimens.append(mineral)
    else:
        world_specimens.append(mineral)

print(f"\nFound {len(balkan_specimens)} Balkan specimens")
print(f"Found {len(world_specimens)} World specimens")

# Select diverse specimens - aim for variety in mineral types
selected_balkan = []
selected_world = []

# Track mineral names to ensure diversity
seen_balkan_names = {}
seen_world_names = {}

# Select from Balkans - aim for 50-60 specimens
for mineral in balkan_specimens:
    mid, inv, naziv, lokalitet, predmet, opis, komentar = mineral

    # Ensure diversity - limit duplicates
    if naziv not in seen_balkan_names or seen_balkan_names[naziv] < 2:
        selected_balkan.append(mineral)
        seen_balkan_names[naziv] = seen_balkan_names.get(naziv, 0) + 1

        if len(selected_balkan) >= 55:
            break

# Select from World - aim for 20-30 specimens
for mineral in world_specimens:
    mid, inv, naziv, lokalitet, predmet, opis, komentar = mineral

    # Ensure diversity
    if naziv not in seen_world_names or seen_world_names[naziv] < 1:
        selected_world.append(mineral)
        seen_world_names[naziv] = seen_world_names.get(naziv, 0) + 1

        if len(selected_world) >= 25:
            break

print(f"\nSelected {len(selected_balkan)} Balkan specimens")
print(f"Selected {len(selected_world)} World specimens")
print(f"Total: {len(selected_balkan) + len(selected_world)} specimens")

# Save to file for document generation
import json

output_data = {
    'balkan_specimens': [
        {
            'id': m[0],
            'inv_broj': int(m[1]) if m[1] else None,
            'naziv': m[2],
            'lokalitet': m[3],
            'predmet': m[4],
            'opis': m[5],
            'komentar': m[6]
        }
        for m in selected_balkan
    ],
    'world_specimens': [
        {
            'id': m[0],
            'inv_broj': int(m[1]) if m[1] else None,
            'naziv': m[2],
            'lokalitet': m[3],
            'predmet': m[4],
            'opis': m[5],
            'komentar': m[6]
        }
        for m in selected_world
    ]
}

with open('exhibition_specimens.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("\nData saved to exhibition_specimens.json")

# Display sample
print("\n" + "="*80)
print("SAMPLE - First 5 Balkan specimens:")
for i, m in enumerate(selected_balkan[:5], 1):
    mid, inv, naziv, lokalitet, predmet, opis, komentar = m
    inv_display = f"M{int(inv)}" if inv else "N/A"
    print(f"\n{i}. {naziv}")
    print(f"   Inv: {inv_display}")
    print(f"   Lokalitet: {lokalitet}")
    if predmet:
        print(f"   Predmet: {predmet}")

print("\n" + "="*80)
print("SAMPLE - First 5 World specimens:")
for i, m in enumerate(selected_world[:5], 1):
    mid, inv, naziv, lokalitet, predmet, opis, komentar = m
    inv_display = f"M{int(inv)}" if inv else "N/A"
    print(f"\n{i}. {naziv}")
    print(f"   Inv: {inv_display}")
    print(f"   Lokalitet: {lokalitet}")
    if predmet:
        print(f"   Predmet: {predmet}")

conn.close()
