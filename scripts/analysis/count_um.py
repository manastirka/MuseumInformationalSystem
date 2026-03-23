#!/usr/bin/env python3
"""
Count U.M. entries vs actual coordinates that failed
"""

import sqlite3

DB_PATH = 'data/bird_ringing.db'

def count_um():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get non-standardized coordinates
    cursor.execute('''
        SELECT coordinates
        FROM bird_ringing
        WHERE coordinates IS NOT NULL
        AND coordinates != ""
        AND coordinates NOT LIKE "%.%, %"
    ''')

    failed_coords = [row[0] for row in cursor.fetchall()]

    # Count U.M.
    um_count = sum(1 for c in failed_coords if c.strip().upper() == 'U.M.')
    actual_coords = len(failed_coords) - um_count

    print(f"Total non-standard: {len(failed_coords):,}")
    print(f"  U.M. entries:     {um_count:,} ({um_count/len(failed_coords)*100:.1f}%)")
    print(f"  Actual coordinates: {actual_coords:,} ({actual_coords/len(failed_coords)*100:.1f}%)")

    # Show non-U.M. examples
    print(f"\nNon-U.M. coordinates that failed (first 30):")
    print("-" * 80)
    count = 0
    seen = set()
    for coord in failed_coords:
        if coord.strip().upper() != 'U.M.' and coord not in seen:
            seen.add(coord)
            print(f"  '{coord}'")
            count += 1
            if count >= 30:
                break

    conn.close()

if __name__ == '__main__':
    count_um()
