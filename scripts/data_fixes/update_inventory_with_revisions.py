#!/usr/bin/env python3
"""
Update Mineralogical Inventory Book with Revisited Data
- Add revisited status field
- Mark inventory numbers 1-76 as revisited
- Update entries from combined_inventory.csv with location data
"""

import sqlite3
import csv
from datetime import datetime

INVENTORY_DB = 'data/inventory_book.db'
COMBINED_CSV = 'combined_inventory.csv'

def add_revisited_field():
    """Add revisited field to inventory_book if it doesn't exist."""
    conn = sqlite3.connect(INVENTORY_DB)
    cursor = conn.cursor()

    # Check if revisited field exists
    cursor.execute("PRAGMA table_info(inventory_book)")
    columns = [row[1] for row in cursor.fetchall()]

    if 'revisited' not in columns:
        print("Adding 'revisited' field to inventory_book...")
        cursor.execute("""
            ALTER TABLE inventory_book
            ADD COLUMN revisited INTEGER DEFAULT 0
        """)
        conn.commit()
        print("✓ Field 'revisited' added")
    else:
        print("✓ Field 'revisited' already exists")

    # Check if physical_location field exists
    if 'physical_location' not in columns:
        print("Adding 'physical_location' field to inventory_book...")
        cursor.execute("""
            ALTER TABLE inventory_book
            ADD COLUMN physical_location TEXT
        """)
        conn.commit()
        print("✓ Field 'physical_location' added")
    else:
        print("✓ Field 'physical_location' already exists")

    # Check if revision_date field exists
    if 'revision_date' not in columns:
        print("Adding 'revision_date' field to inventory_book...")
        cursor.execute("""
            ALTER TABLE inventory_book
            ADD COLUMN revision_date TIMESTAMP
        """)
        conn.commit()
        print("✓ Field 'revision_date' added")
    else:
        print("✓ Field 'revision_date' already exists")

    conn.close()

def mark_1_76_as_revisited():
    """Mark inventory numbers 1-76 as revisited."""
    conn = sqlite3.connect(INVENTORY_DB)
    cursor = conn.cursor()

    print("\nMarking inventory numbers 1-76 as revisited...")

    cursor.execute("""
        UPDATE inventory_book
        SET revisited = 1,
            revision_date = ?
        WHERE inventory_number BETWEEN 1 AND 76
    """, (datetime.now().isoformat(),))

    updated_count = cursor.rowcount
    conn.commit()
    conn.close()

    print(f"✓ Marked {updated_count} entries (inv #1-76) as revisited")
    return updated_count

def load_combined_inventory():
    """Load data from combined_inventory.csv."""
    print(f"\nLoading data from {COMBINED_CSV}...")

    inventory_data = {}

    with open(COMBINED_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                inv_broj = row['Inv. broj'].strip()

                # Skip non-numeric inventory numbers
                if not inv_broj.isdigit():
                    continue

                inv_num = int(inv_broj)
                predmet = row['Predmet'].strip()
                gde_se_nalazi = row['Gde se nalazi'].strip()
                source = row['source'].strip()

                # Group by inventory number
                if inv_num not in inventory_data:
                    inventory_data[inv_num] = {
                        'names': set(),
                        'locations': set(),
                        'sources': set()
                    }

                if predmet:
                    inventory_data[inv_num]['names'].add(predmet)
                if gde_se_nalazi:
                    inventory_data[inv_num]['locations'].add(gde_se_nalazi)
                if source:
                    inventory_data[inv_num]['sources'].add(source)

            except (ValueError, KeyError) as e:
                # Skip malformed rows
                continue

    print(f"✓ Loaded data for {len(inventory_data)} unique inventory numbers")

    # Show range
    if inventory_data:
        min_inv = min(inventory_data.keys())
        max_inv = max(inventory_data.keys())
        print(f"  Inventory number range: {min_inv} - {max_inv}")

    return inventory_data

def update_inventory_with_combined_data(inventory_data):
    """Update inventory book with data from combined inventory."""
    conn = sqlite3.connect(INVENTORY_DB)
    cursor = conn.cursor()

    print("\nUpdating inventory book with combined inventory data...")

    updated_count = 0
    new_entries_count = 0
    skipped_count = 0

    revision_date = datetime.now().isoformat()

    for inv_num, data in sorted(inventory_data.items()):
        # Check if entry exists
        cursor.execute("""
            SELECT id, name, physical_location, revisited
            FROM inventory_book
            WHERE inventory_number = ?
        """, (inv_num,))

        existing = cursor.fetchone()

        # Prepare data
        names_str = '; '.join(sorted(data['names']))
        locations_str = ', '.join(sorted(data['locations']))
        sources_str = '; '.join(sorted(data['sources']))

        if existing:
            record_id, current_name, current_location, current_revisited = existing

            # Update existing entry
            # Add location info to notes if not already present
            notes_addition = f"Локација: {locations_str}. Извор: {sources_str}"

            cursor.execute("""
                UPDATE inventory_book
                SET physical_location = ?,
                    revisited = 1,
                    revision_date = ?,
                    notes = CASE
                        WHEN notes IS NULL OR notes = '' THEN ?
                        ELSE notes || ' | ' || ?
                    END
                WHERE id = ?
            """, (locations_str, revision_date, notes_addition, notes_addition, record_id))

            updated_count += 1

        else:
            # Insert new entry
            cursor.execute("""
                INSERT INTO inventory_book
                (inventory_number, name, physical_location, revisited, revision_date, notes, category)
                VALUES (?, ?, ?, 1, ?, ?, ?)
            """, (inv_num, names_str, locations_str, revision_date, f"Извор: {sources_str}", "Минералошка збирка"))

            new_entries_count += 1

    conn.commit()
    conn.close()

    print(f"✓ Updated {updated_count} existing entries")
    print(f"✓ Added {new_entries_count} new entries")
    if skipped_count > 0:
        print(f"⚠ Skipped {skipped_count} entries (errors)")

    return updated_count, new_entries_count

def get_revision_statistics():
    """Get statistics about revisited entries."""
    conn = sqlite3.connect(INVENTORY_DB)
    cursor = conn.cursor()

    # Total entries
    cursor.execute("SELECT COUNT(*) FROM inventory_book WHERE inventory_number IS NOT NULL")
    total = cursor.fetchone()[0]

    # Revisited entries
    cursor.execute("SELECT COUNT(*) FROM inventory_book WHERE revisited = 1")
    revisited = cursor.fetchone()[0]

    # Revisited with physical location
    cursor.execute("SELECT COUNT(*) FROM inventory_book WHERE revisited = 1 AND physical_location IS NOT NULL")
    with_location = cursor.fetchone()[0]

    # Range of revisited
    cursor.execute("""
        SELECT MIN(inventory_number), MAX(inventory_number)
        FROM inventory_book
        WHERE revisited = 1 AND inventory_number IS NOT NULL
    """)
    min_rev, max_rev = cursor.fetchone()

    conn.close()

    return {
        'total': total,
        'revisited': revisited,
        'with_location': with_location,
        'min_revisited': min_rev,
        'max_revisited': max_rev
    }

def main():
    print("="*80)
    print("MINERALOGICAL INVENTORY BOOK - REVISION UPDATE")
    print("="*80)

    # Step 1: Add revisited field
    add_revisited_field()

    # Step 2: Mark 1-76 as revisited
    mark_1_76_as_revisited()

    # Step 3: Load combined inventory data
    inventory_data = load_combined_inventory()

    # Step 4: Update inventory book
    if inventory_data:
        update_inventory_with_combined_data(inventory_data)
    else:
        print("⚠ No data loaded from combined inventory")

    # Step 5: Show statistics
    print("\n" + "="*80)
    print("REVISION STATISTICS")
    print("="*80)

    stats = get_revision_statistics()
    print(f"\nTotal inventory entries: {stats['total']}")
    print(f"Revisited entries: {stats['revisited']} ({stats['revisited']/stats['total']*100:.1f}%)")
    print(f"Revisited with physical location: {stats['with_location']}")
    print(f"Revisited inventory number range: {stats['min_revisited']} - {stats['max_revisited']}")

    not_revisited = stats['total'] - stats['revisited']
    print(f"\nStill to be revisited: {not_revisited} entries")

    print("\n" + "="*80)
    print("✓ Inventory book update complete!")
    print("="*80)

if __name__ == "__main__":
    main()
