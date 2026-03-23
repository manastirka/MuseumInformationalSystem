#!/usr/bin/env python3
"""
Fix Meteorite Migration - Add All Missing Fields
Re-migrates meteorite collection with complete data
"""

import os
import sys
import psycopg
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("❌ DATABASE_URL not set")
    sys.exit(1)

# Convert URL format
DB_URL = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')

def migrate_meteorites():
    """Re-migrate meteorite collection with ALL fields."""
    print("\n" + "="*70)
    print("☄️  METEORITE COLLECTION - COMPLETE RE-MIGRATION")
    print("="*70)

    # Import original data
    try:
        from app import METEORITE_COLLECTION_DATABASE
    except Exception as e:
        print(f"❌ Could not import meteorite data: {e}")
        return 1

    specimens = METEORITE_COLLECTION_DATABASE.get('specimens', [])
    print(f"\n☄️  Found {len(specimens)} meteorite specimens to migrate")

    # Connect to PostgreSQL
    try:
        conn = psycopg.connect(DB_URL)
        cur = conn.cursor()
        print("✓ Connected to PostgreSQL")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return 1

    try:
        # Delete existing records
        cur.execute("DELETE FROM meteorite_specimens")
        deleted = cur.rowcount
        print(f"\n🗑️  Deleted {deleted} existing records")

        # Migrate all specimens with COMPLETE data
        migrated = 0
        errors = []

        for spec in specimens:
            try:
                catalog = spec.get('catalog_number', '').strip()
                name = spec.get('meteorite_name', spec.get('name', '')).strip()

                if not catalog or not name:
                    print(f"⚠️  Skipping specimen with missing catalog or name")
                    continue

                # Handle mass fields
                specimen_mass = spec.get('specimen_mass', spec.get('mass'))
                total_mass_kg = spec.get('total_mass_kg')
                total_mass_g = spec.get('total_mass_g')

                # Determine mass and unit
                mass = specimen_mass
                mass_unit = 'kg'

                # Total mass
                total_mass = None
                total_mass_unit = 'kg'
                if total_mass_kg and isinstance(total_mass_kg, (int, float)):
                    total_mass = total_mass_kg
                    total_mass_unit = 'kg'
                elif total_mass_g and isinstance(total_mass_g, (int, float)):
                    total_mass = total_mass_g
                    total_mass_unit = 'g'

                # Insert with ALL fields
                cur.execute("""
                    INSERT INTO meteorite_specimens (
                        catalog_number, specimen_name, meteorite_class,
                        meteorite_type, mass, mass_unit,
                        total_mass, total_mass_unit, quantity,
                        fall_location, fall_country, fall_type,
                        fall_date_text, fall_witnessed,
                        collector, acquisition_method, acquisition_date_text,
                        shock_stage, weathering_grade, texture,
                        chemical_composition, mineralogy,
                        parent_body, cosmic_ray_exposure,
                        widmanstatten_pattern, fusion_crust,
                        meteorite_bulletin_number, serbian_meteorite,
                        storage_location, condition, description, notes,
                        status
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s
                    )
                    ON CONFLICT (catalog_number) DO UPDATE SET
                        specimen_name = EXCLUDED.specimen_name,
                        meteorite_class = EXCLUDED.meteorite_class,
                        meteorite_type = EXCLUDED.meteorite_type,
                        mass = EXCLUDED.mass,
                        mass_unit = EXCLUDED.mass_unit,
                        total_mass = EXCLUDED.total_mass,
                        total_mass_unit = EXCLUDED.total_mass_unit,
                        quantity = EXCLUDED.quantity,
                        fall_location = EXCLUDED.fall_location,
                        fall_country = EXCLUDED.fall_country,
                        fall_type = EXCLUDED.fall_type,
                        fall_date_text = EXCLUDED.fall_date_text,
                        fall_witnessed = EXCLUDED.fall_witnessed,
                        collector = EXCLUDED.collector,
                        acquisition_method = EXCLUDED.acquisition_method,
                        acquisition_date_text = EXCLUDED.acquisition_date_text,
                        shock_stage = EXCLUDED.shock_stage,
                        weathering_grade = EXCLUDED.weathering_grade,
                        texture = EXCLUDED.texture,
                        chemical_composition = EXCLUDED.chemical_composition,
                        mineralogy = EXCLUDED.mineralogy,
                        parent_body = EXCLUDED.parent_body,
                        cosmic_ray_exposure = EXCLUDED.cosmic_ray_exposure,
                        widmanstatten_pattern = EXCLUDED.widmanstatten_pattern,
                        fusion_crust = EXCLUDED.fusion_crust,
                        meteorite_bulletin_number = EXCLUDED.meteorite_bulletin_number,
                        serbian_meteorite = EXCLUDED.serbian_meteorite,
                        storage_location = EXCLUDED.storage_location,
                        condition = EXCLUDED.condition,
                        description = EXCLUDED.description,
                        notes = EXCLUDED.notes,
                        status = EXCLUDED.status
                """, (
                    catalog,
                    name,
                    spec.get('classification') or spec.get('class') or spec.get('meteorite_class'),
                    spec.get('type') or spec.get('meteorite_type'),
                    mass,
                    mass_unit,
                    total_mass,
                    total_mass_unit,
                    spec.get('quantity', 1),
                    spec.get('location_found') or spec.get('fall_location') or spec.get('location'),
                    spec.get('fall_country') or spec.get('country'),
                    spec.get('fall_type'),  # "Пад (посматран)", "Налаз", etc.
                    spec.get('fall_date'),  # Keep original Serbian date format
                    spec.get('fall_type', '').lower().startswith('пад') if spec.get('fall_type') else False,
                    spec.get('curator') or spec.get('collector') or spec.get('finder'),
                    spec.get('source') or spec.get('acquisition_method'),
                    spec.get('acquisition_date'),  # Keep original format
                    spec.get('shock_stage'),
                    spec.get('weathering_grade'),
                    spec.get('texture'),
                    spec.get('chemical_composition'),
                    spec.get('mineralogy'),
                    spec.get('parent_body'),
                    spec.get('cosmic_ray_exposure'),
                    spec.get('widmanstatten_pattern'),
                    spec.get('fusion_crust'),
                    spec.get('meteorite_bulletin_number'),
                    spec.get('serbian_meteorite', False),
                    spec.get('storage_location') or spec.get('storage'),
                    spec.get('condition'),
                    spec.get('description'),
                    spec.get('notes'),
                    'у збирци'
                ))

                migrated += 1

                if migrated % 5 == 0:
                    print(f"   ... migrated {migrated} specimens")

            except Exception as e:
                error_msg = f"Error migrating {spec.get('catalog_number', 'UNKNOWN')}: {e}"
                errors.append(error_msg)
                print(f"   ❌ {error_msg}")
                continue

        # Commit transaction
        conn.commit()

        print(f"\n✓ Migration complete: {migrated} specimens")

        if errors:
            print(f"\n⚠️  {len(errors)} errors occurred:")
            for err in errors[:5]:  # Show first 5 errors
                print(f"   - {err}")

        # Verification
        cur.execute("SELECT COUNT(*) FROM meteorite_specimens")
        count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM meteorite_specimens WHERE serbian_meteorite = TRUE")
        serbian_count = cur.fetchone()[0]

        print(f"\n📊 Verification:")
        print(f"   • Total specimens: {count}")
        print(f"   • Serbian meteorites: {serbian_count}")
        print(f"   • Foreign meteorites: {count - serbian_count}")

        # Sample data check
        print(f"\n🔍 Sample data (first 3 specimens):")
        cur.execute("""
            SELECT
                catalog_number,
                specimen_name,
                fall_type,
                quantity,
                shock_stage,
                mineralogy,
                serbian_meteorite
            FROM meteorite_specimens
            ORDER BY catalog_number
            LIMIT 3
        """)

        for row in cur.fetchall():
            print(f"   • {row[0]}: {row[1]}")
            print(f"      Fall type: {row[2]}")
            print(f"      Quantity: {row[3]}")
            print(f"      Shock stage: {row[4]}")
            print(f"      Mineralogy: {row[5][:50] if row[5] else 'N/A'}{'...' if row[5] and len(row[5]) > 50 else ''}")
            print(f"      Serbian: {row[6]}")

        cur.close()
        conn.close()

        return 0

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        return 1

if __name__ == '__main__':
    sys.exit(migrate_meteorites())
