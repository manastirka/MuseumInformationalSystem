#!/usr/bin/env python3
"""
Script to integrate parsed library books into app.py's LIBRARY_DATABASE
"""
import json
import re

def load_parsed_books():
    """Load the parsed books from JSON."""
    with open('library_books_import.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def convert_to_app_format(parsed_books, start_id=6):
    """
    Convert parsed books to app.py LIBRARY_DATABASE format.

    Maps:
    - inventory_number -> id (using start_id + index)
    - title -> title
    - author -> author
    - publisher -> publisher
    - year -> year
    - signature -> location
    - description -> description
    - category -> category
    - status -> status
    - language -> language
    """
    app_books = []

    for idx, book in enumerate(parsed_books):
        # Clean up year - convert to int if possible
        year = book.get('year', '')
        try:
            year_int = int(year) if year and str(year).isdigit() else None
        except (ValueError, TypeError):
            year_int = None

        # Determine language based on author/title content
        text_sample = f"{book.get('author', '')} {book.get('title', '')}"
        # Simple heuristic: if contains Cyrillic, it's Serbian
        has_cyrillic = bool(re.search(r'[а-яА-ЯёЁ]', text_sample))
        language = 'српски' if has_cyrillic else 'енглески'

        app_book = {
            'id': start_id + idx,
            'inventory_number': book.get('inventory_number', ''),
            'title': book.get('title', 'Без наслова'),
            'author': book.get('author', 'Непознат аутор'),
            'isbn': '',  # Not available in Excel file
            'category': 'Монографска публикација',
            'year': year_int if year_int else 0,
            'location': book.get('signature', ''),
            'status': 'доступна',
            'description': book.get('description', ''),
            'pages': 0,  # Not available
            'publisher': book.get('publisher', ''),
            'language': language,
            'binding_type': book.get('binding_type', ''),
            'dimensions': book.get('dimensions', ''),
            'acquisition_method': book.get('acquisition_method', ''),
            'price': book.get('price', ''),
            'date_added': book.get('date_added', ''),
            'notes': book.get('notes', ''),
        }

        app_books.append(app_book)

    return app_books

def generate_library_database_json(app_books):
    """Generate a complete LIBRARY_DATABASE JSON file."""

    # Calculate statistics
    total_books = len(app_books)
    available_books = len([b for b in app_books if b['status'] == 'доступна'])
    borrowed_books = len([b for b in app_books if b['status'] == 'позајмљена'])

    # Extract unique categories
    categories = list(set(book['category'] for book in app_books))
    categories.sort()

    library_database = {
        'books': app_books,
        'categories': categories,
        'statistics': {
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books,
            'total_categories': len(categories)
        }
    }

    return library_database

def save_library_json(library_database, filename='data/library_database.json'):
    """Save library database to JSON file."""
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(library_database, f, ensure_ascii=False, indent=2)

    print(f"✓ Saved library database to {filename}")

def display_stats(library_database):
    """Display statistics about the library database."""
    print("\n" + "="*60)
    print("LIBRARY DATABASE STATISTICS")
    print("="*60)
    print(f"Total books: {library_database['statistics']['total_books']}")
    print(f"Available: {library_database['statistics']['available_books']}")
    print(f"Borrowed: {library_database['statistics']['borrowed_books']}")
    print(f"Categories: {library_database['statistics']['total_categories']}")
    print(f"\nCategories list:")
    for cat in library_database['categories']:
        count = len([b for b in library_database['books'] if b['category'] == cat])
        print(f"  - {cat}: {count} books")

    print(f"\nFirst 5 books:")
    for i, book in enumerate(library_database['books'][:5], 1):
        print(f"\n{i}. {book['title']}")
        print(f"   Author: {book['author']}")
        print(f"   Year: {book['year']}, Location: {book['location']}")
        print(f"   Inventory: {book['inventory_number']}")

if __name__ == "__main__":
    print("Loading parsed books from library_books_import.json...")
    parsed_books = load_parsed_books()
    print(f"✓ Loaded {len(parsed_books)} books")

    print("\nConverting to app.py format...")
    app_books = convert_to_app_format(parsed_books, start_id=1)
    print(f"✓ Converted {len(app_books)} books")

    print("\nGenerating library database...")
    library_database = generate_library_database_json(app_books)

    display_stats(library_database)

    print("\n" + "="*60)
    save_library_json(library_database)

    print("\n✓ Library database integration complete!")
    print("\nNext steps:")
    print("1. Review data/library_database.json")
    print("2. Update app.py to load library data from this JSON file")
    print("3. Add persistence when books are added/modified")
