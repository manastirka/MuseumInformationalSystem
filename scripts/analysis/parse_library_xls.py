#!/usr/bin/env python3
import xlrd
import re
import json

def parse_full_info(full_info):
    """
    Parse the combined author/title/publisher/year field.
    Format: AUTHOR\nTitle, Place, Publisher, Year
    """
    lines = [line.strip() for line in full_info.strip().split('\n') if line.strip()]

    author = ''
    title = ''
    publisher = ''
    year = ''
    place = ''
    description = full_info  # Keep original as description

    if len(lines) >= 1:
        # First line is usually the author
        author = lines[0].strip()

    if len(lines) >= 2:
        # Second line contains title, place, publisher, year
        second_line = lines[1].strip()

        # Extract year (4 digits) - look for patterns like "1942" or "2009"
        year_match = re.search(r'\b(1[0-9]{3}|20[0-2][0-9])\b', second_line)
        if year_match:
            year = year_match.group(1)
            # Remove year from second_line for further processing
            second_line_no_year = second_line.replace(year, '').strip(', .')
        else:
            second_line_no_year = second_line

        # Split by commas
        parts = [p.strip() for p in second_line_no_year.split(',') if p.strip()]

        if len(parts) >= 1:
            # First part after author is the title
            title = parts[0]

        # Try to identify place and publisher
        # Common pattern: Title, Place, Publisher or Title / subtitle. - Place : Publisher
        if len(parts) >= 2:
            place = parts[1] if len(parts) == 2 else parts[1]

        if len(parts) >= 3:
            publisher = parts[2]

    # If title is empty, use the entire second line
    if not title and len(lines) >= 2:
        title = lines[1]

    return {
        'author': author,
        'title': title,
        'publisher': publisher,
        'year': year,
        'place': place,
        'description': description
    }

def parse_acquisition_method(record):
    """Determine acquisition method from the checkboxes."""
    methods = []
    if record.get('acquisition_legal'):
        methods.append('обавезни примерак')
    if record.get('acquisition_purchase'):
        methods.append('куповина')
    if record.get('acquisition_exchange'):
        methods.append('размена')
    if record.get('acquisition_gift') or 'Poklon' in str(record.get('notes', '')):
        methods.append('поклон')

    return ', '.join(methods) if methods else 'непознато'

def read_and_parse_xls(filename):
    """Read and parse the XLS file."""
    print(f"Reading file: {filename}")
    wb = xlrd.open_workbook(filename)
    sheet = wb.sheet_by_index(0)

    column_names = [
        'inventory_number',      # Col 0
        'date',                  # Col 1
        'full_info',            # Col 2
        '',                     # Col 3
        '',                     # Col 4
        'binding_type',         # Col 5
        'dimensions',           # Col 6
        'acquisition_legal',    # Col 7
        'acquisition_purchase', # Col 8
        'acquisition_exchange', # Col 9
        'acquisition_gift',     # Col 10
        'price',                # Col 11
        'signature',            # Col 12
        'notes'                 # Col 13
    ]

    books = []
    skipped = []

    # Start from row 4 (data rows)
    for row_idx in range(4, sheet.nrows):
        row_data = {}
        for col_idx in range(min(len(column_names), sheet.ncols)):
            col_name = column_names[col_idx]
            if col_name:
                value = sheet.cell_value(row_idx, col_idx)
                row_data[col_name] = value

        # Skip empty rows
        if not any(str(v).strip() for v in row_data.values()):
            continue

        # Skip rows without inventory number
        inv_num = str(row_data.get('inventory_number', '')).strip()
        if not inv_num or inv_num.lower() in ['prazno', '', 'редни \nброј']:
            skipped.append(f"Row {row_idx}: No inventory number")
            continue

        # Parse the full info field
        full_info = str(row_data.get('full_info', '')).strip()
        if not full_info:
            skipped.append(f"Row {row_idx}: No book info")
            continue

        parsed = parse_full_info(full_info)

        # Create book entry
        book = {
            'inventory_number': inv_num,
            'title': parsed['title'] or full_info.split('\n')[1] if len(full_info.split('\n')) > 1 else full_info,
            'author': parsed['author'],
            'publisher': parsed['publisher'],
            'year': parsed['year'],
            'place': parsed['place'],
            'binding_type': str(row_data.get('binding_type', '')).strip(),
            'dimensions': str(row_data.get('dimensions', '')).strip(),
            'signature': str(row_data.get('signature', '')).strip(),
            'acquisition_method': parse_acquisition_method(row_data),
            'price': str(row_data.get('price', '')).strip(),
            'date_added': str(row_data.get('date', '')).strip(),
            'notes': str(row_data.get('notes', '')).strip(),
            'description': parsed['description'],
            'category': 'Монографска публикација',
            'status': 'доступна',
            'language': 'српски',  # Default, could be improved with detection
        }

        books.append(book)

    print(f"\nTotal books parsed: {len(books)}")
    print(f"Skipped entries: {len(skipped)}")

    if skipped:
        print("\nFirst 10 skipped entries:")
        for s in skipped[:10]:
            print(f"  - {s}")

    return books, skipped

def display_sample_books(books, count=5):
    """Display sample books for verification."""
    print(f"\nFirst {count} books:")
    for i, book in enumerate(books[:count], 1):
        print(f"\n{i}. Inventory: {book['inventory_number']}")
        print(f"   Author: {book['author']}")
        print(f"   Title: {book['title']}")
        print(f"   Publisher: {book['publisher']}, {book['place']}, {book['year']}")
        print(f"   Signature: {book['signature']}")
        print(f"   Acquisition: {book['acquisition_method']}")
        if book['notes']:
            print(f"   Notes: {book['notes']}")

def save_to_json(books, filename='library_books_import.json'):
    """Save parsed books to JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Saved to {filename}")

if __name__ == "__main__":
    xls_file = "Inventarni list za monografske publikacije.xls"

    books, skipped = read_and_parse_xls(xls_file)

    display_sample_books(books, 10)

    save_to_json(books)

    print(f"\n✓ Successfully parsed {len(books)} books from Excel file")
    print(f"✓ Data saved to library_books_import.json")
    print(f"\nNext steps:")
    print(f"1. Review the JSON file to verify the data is correct")
    print(f"2. The data can then be imported into the app.py LIBRARY_DATABASE")
