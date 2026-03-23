#!/usr/bin/env python3
"""
Analyze coordinates that failed to convert to identify missing patterns
"""

import sqlite3
from collections import Counter

DB_PATH = 'data/bird_ringing.db'

def analyze_failed_coordinates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get non-standardized coordinates (those NOT in "XX.XXXXXX, YY.YYYYYY" format)
    cursor.execute('''
        SELECT coordinates
        FROM bird_ringing
        WHERE coordinates IS NOT NULL
        AND coordinates != ""
        AND coordinates NOT LIKE "%.%, %"
    ''')

    failed_coords = [row[0] for row in cursor.fetchall()]

    print(f"Total non-standard coordinates: {len(failed_coords):,}")
    print("=" * 80)

    # Analyze patterns
    print("\nSample non-standard coordinates (first 50):")
    print("-" * 80)
    for i, coord in enumerate(failed_coords[:50], 1):
        print(f"{i:3d}. '{coord}'")

    # Look for common characteristics
    print("\n" + "=" * 80)
    print("Pattern Analysis:")
    print("-" * 80)

    has_degree_symbol = sum(1 for c in failed_coords if '°' in c)
    has_minutes_symbol = sum(1 for c in failed_coords if "'" in c or '´' in c)
    has_seconds_symbol = sum(1 for c in failed_coords if '"' in c or '´´' in c)
    has_nsew = sum(1 for c in failed_coords if any(x in c.upper() for x in ['N', 'S', 'E', 'W']))
    has_semicolon = sum(1 for c in failed_coords if ';' in c)
    has_space_only = sum(1 for c in failed_coords if ' ' in c and ',' not in c and ';' not in c)

    print(f"Contains degree symbol (°):     {has_degree_symbol:6,} ({has_degree_symbol/len(failed_coords)*100:.1f}%)")
    print(f"Contains minutes symbol (' ´):  {has_minutes_symbol:6,} ({has_minutes_symbol/len(failed_coords)*100:.1f}%)")
    print(f"Contains seconds symbol (\" ´´): {has_seconds_symbol:6,} ({has_seconds_symbol/len(failed_coords)*100:.1f}%)")
    print(f"Contains N/S/E/W:                {has_nsew:6,} ({has_nsew/len(failed_coords)*100:.1f}%)")
    print(f"Contains semicolon (;):          {has_semicolon:6,} ({has_semicolon/len(failed_coords)*100:.1f}%)")
    print(f"Space-separated (no , or ;):     {has_space_only:6,} ({has_space_only/len(failed_coords)*100:.1f}%)")

    conn.close()

if __name__ == '__main__':
    analyze_failed_coordinates()
