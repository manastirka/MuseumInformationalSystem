#!/usr/bin/env python3
"""
Batch geocode all localities from the mineral database.
This script pre-populates the geocache so coordinates are available immediately.
"""

import sys
import time

def main():
    from mineral_database_pg import get_mineral_database
    from locality_data import geocode_locality, _geocache, _load_geocache, _save_geocache

    # Load existing cache
    _load_geocache()
    print(f"Loaded {len(_geocache)} cached localities")

    # Get all minerals
    mineral_db = get_mineral_database()
    result = mineral_db.get_all_minerals(page=1, per_page=10000)
    minerals = result.get('minerals', [])

    # Get unique localities
    localities = set()
    for m in minerals:
        loc = m.get('lokalitet') or ''
        if loc and loc.strip():
            localities.add(loc.strip())

    print(f"Found {len(localities)} unique localities")

    # Filter out already cached localities
    to_geocode = []
    for loc in localities:
        cache_key = loc.lower().strip()
        if cache_key not in _geocache:
            to_geocode.append(loc)

    print(f"Need to geocode {len(to_geocode)} new localities")

    if not to_geocode:
        print("All localities already cached!")
        return

    # Geocode in batches
    success = 0
    failed = 0

    for i, loc in enumerate(to_geocode):
        print(f"[{i+1}/{len(to_geocode)}] Geocoding: {loc[:50]}...", end=" ", flush=True)

        try:
            coords = geocode_locality(loc)
            if coords:
                print(f"OK ({coords['lat']:.4f}, {coords['lon']:.4f})")
                success += 1
            else:
                print("NOT FOUND")
                failed += 1
        except Exception as e:
            print(f"ERROR: {e}")
            failed += 1

        # Save periodically
        if (i + 1) % 10 == 0:
            _save_geocache()
            print(f"  [Saved cache: {len(_geocache)} entries]")

    # Final save
    _save_geocache()

    print(f"\nDone!")
    print(f"  Success: {success}")
    print(f"  Failed: {failed}")
    print(f"  Total cached: {len(_geocache)}")


if __name__ == '__main__':
    main()
