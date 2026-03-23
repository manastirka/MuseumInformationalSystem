#!/usr/bin/env python3
import xlrd
import sqlite3
import sys
from datetime import datetime

def read_xls_file(filename):
    """Read the .xls file and return the data"""
    print(f"Reading file: {filename}")
    wb = xlrd.open_workbook(filename)
    sheet = wb.sheet_by_index(0)

    print(f"\nSheet name: {sheet.name}")
    print(f"Rows: {sheet.nrows}, Columns: {sheet.ncols}")

    # Define column mapping based on the actual structure
    # Headers are in row 2, data starts from row 4
    column_names = [
        'inventory_number',      # Col 0: редни број
        'date',                  # Col 1: датум
        'full_info',            # Col 2: Аутор, наслов, etc. (merged columns 2-5)
        '',                     # Col 3: empty
        '',                     # Col 4: empty
        'binding_type',         # Col 5: врста повеза
        'dimensions',           # Col 6: димензије
        'acquisition_legal',    # Col 7: обавезни примерак
        'acquisition_purchase', # Col 8: куповина
        'acquisition_exchange', # Col 9: размена
        'acquisition_gift',     # Col 10: поклон
        'price',                # Col 11: цена
        'signature',            # Col 12: сигнатура
        'notes'                 # Col 13: напомена
    ]

    print(f"\nParsing library records (starting from row 4)...")

    # Get all data rows (skip rows 0-3)
    data = []
    for row_idx in range(4, sheet.nrows):
        row_data = {}
        for col_idx in range(sheet.ncols):
            col_name = column_names[col_idx] if col_idx < len(column_names) else f'col_{col_idx}'
            if col_name:  # Skip empty column names
                value = sheet.cell_value(row_idx, col_idx)
                row_data[col_name] = value

        # Only add rows that have some data
        if any(str(v).strip() for v in row_data.values()):
            data.append(row_data)

    print(f"\nTotal records: {len(data)}")

    # Show first few records
    print("\nFirst 3 records:")
    for i, record in enumerate(data[:3]):
        print(f"\nRecord {i+1}:")
        for key, value in record.items():
            if value:  # Only show non-empty fields
                print(f"  {key}: {value}")

    return column_names, data

def insert_into_database(data):
    """Insert the library items into the database"""
    conn = sqlite3.connect('museum.db')
    cursor = conn.cursor()

    inserted_count = 0
    skipped_count = 0

    for idx, record in enumerate(data, 1):
        try:
            # Map the fields from the Excel file to database columns
            # You'll need to adjust this mapping based on the actual column names

            cursor.execute("""
                INSERT INTO library (
                    title, author, publisher, publication_year, isbn,
                    inventory_number, category, location, notes, date_added
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.get('Naslov', ''),
                record.get('Autor', record.get('Pisac', '')),
                record.get('Izdavač', record.get('Izdavac', '')),
                record.get('Godina izdanja', record.get('Godina', '')),
                record.get('ISBN', ''),
                record.get('Inventarni broj', record.get('Inv. broj', '')),
                record.get('Kategorija', 'Monografska publikacija'),
                record.get('Lokacija', ''),
                record.get('Napomena', record.get('Primedba', '')),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))

            inserted_count += 1
            if inserted_count % 10 == 0:
                print(f"Inserted {inserted_count} records...")

        except sqlite3.IntegrityError as e:
            print(f"Skipping record {idx} due to duplicate: {e}")
            skipped_count += 1
        except Exception as e:
            print(f"Error inserting record {idx}: {e}")
            print(f"Record data: {record}")
            skipped_count += 1

    conn.commit()
    conn.close()

    print(f"\n✓ Successfully inserted {inserted_count} records")
    print(f"✓ Skipped {skipped_count} records")

    return inserted_count, skipped_count

if __name__ == "__main__":
    xls_file = "Inventarni list za monografske publikacije.xls"

    # First, just read and display the structure
    headers, data = read_xls_file(xls_file)

    print("\n" + "="*60)
    print("PREVIEW MODE - Review the data above")
    print("="*60)

    response = input("\nDo you want to proceed with importing to database? (yes/no): ")

    if response.lower() in ['yes', 'y']:
        print("\nInserting data into database...")
        inserted, skipped = insert_into_database(data)
        print("\n✓ Import completed!")
    else:
        print("\nImport cancelled.")
