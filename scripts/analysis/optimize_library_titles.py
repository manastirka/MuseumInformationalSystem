#!/usr/bin/env python3
"""
Script to optimize library database titles:
- Extract clean, short titles
- Move detailed bibliographic info to a structured info field
- Preserve all data for search functionality
"""
import json
import re

def extract_short_title(full_title, author_name=''):
    """
    Extract a clean, short title from the full bibliographic entry.
    Rules:
    1. Remove subtitle after colon or slash
    2. Remove editor/translator info
    3. Remove publication place
    4. Keep main title only
    """
    # Remove common patterns that indicate extra info
    short_title = full_title

    # Remove patterns like "/ editor name" or "/ translator"
    short_title = re.split(r'\s*/\s*[\[\(]?(?:уредник|приредио|преводилац|илустровао)', short_title)[0]
    short_title = re.split(r'\s*/\s*[A-Z][a-z]+\s+[A-Z]', short_title)[0]

    # Remove ". - Place : Publisher" pattern
    short_title = re.split(r'\.\s*-\s*[A-Z]', short_title)[0]

    # Remove ", Place, Publisher" at end
    short_title = re.split(r',\s+[A-Z][a-z]+(?:,|\s*:)', short_title)[0]

    # Remove subtitle after colon (but keep if it's part of main title)
    # Only remove if there's significant text before the colon
    if ':' in short_title:
        parts = short_title.split(':')
        if len(parts[0].strip()) > 10:  # Main title has substance
            short_title = parts[0]

    # Clean up extra whitespace and punctuation
    short_title = short_title.strip(' .,;-/')

    # If title is still too long, try to find just the main part
    if len(short_title) > 100:
        # Look for common patterns
        match = re.match(r'^([^=/\(]+)', short_title)
        if match:
            short_title = match.group(1).strip(' .,;-/')

    # If author name is in the title (bad parsing), remove it
    if author_name and author_name in short_title:
        short_title = short_title.replace(author_name, '').strip(' .,;-/')

    return short_title.strip()

def create_detailed_info(book):
    """
    Create a comprehensive info field with all bibliographic details.
    """
    info_parts = []

    # Author
    if book.get('author'):
        info_parts.append(f"Аутор: {book['author']}")

    # Title (original full bibliographic entry)
    if book.get('description'):
        # The description field contains the original full entry
        info_parts.append(f"\nПун наслов:\n{book['description']}")

    # Publisher and place
    pub_info = []
    if book.get('place'):
        pub_info.append(book['place'])
    if book.get('publisher'):
        pub_info.append(book['publisher'])
    if pub_info:
        info_parts.append(f"\nИздавач: {', '.join(pub_info)}")

    # Year
    if book.get('year') and book['year'] != 0:
        info_parts.append(f"Година издања: {book['year']}")

    # Physical description
    phys_info = []
    if book.get('binding_type'):
        phys_info.append(f"Повез: {book['binding_type']}")
    if book.get('dimensions'):
        phys_info.append(f"Димензије: {book['dimensions']}")
    if book.get('pages') and book['pages'] > 0:
        phys_info.append(f"{book['pages']} стр.")
    if phys_info:
        info_parts.append(f"\nФизички опис: {', '.join(phys_info)}")

    # Location and inventory
    if book.get('location'):
        info_parts.append(f"\nСигнатура: {book['location']}")
    if book.get('inventory_number'):
        info_parts.append(f"Инвентарни број: {book['inventory_number']}")

    # Acquisition
    if book.get('acquisition_method'):
        info_parts.append(f"\nНачин набавке: {book['acquisition_method']}")
    if book.get('date_added'):
        info_parts.append(f"Датум уноса: {book['date_added']}")
    if book.get('price'):
        info_parts.append(f"Цена: {book['price']}")

    # Status and category
    if book.get('status'):
        info_parts.append(f"\nСтатус: {book['status']}")
    if book.get('category'):
        info_parts.append(f"Категорија: {book['category']}")
    if book.get('language'):
        info_parts.append(f"Језик: {book['language']}")

    # ISBN
    if book.get('isbn'):
        info_parts.append(f"\nISBN: {book['isbn']}")

    # Notes
    if book.get('notes'):
        info_parts.append(f"\nНапомена: {book['notes']}")

    return '\n'.join(info_parts)

def optimize_library_database():
    """Process the entire library database and optimize titles."""
    # Load current database
    with open('data/library_database.json', 'r', encoding='utf-8') as f:
        library_data = json.load(f)

    print(f"Processing {len(library_data['books'])} books...")
    print("="*80)

    # Statistics
    titles_shortened = 0
    unchanged = 0

    # Process each book
    for book in library_data['books']:
        original_title = book['title']

        # Extract short title
        short_title = extract_short_title(original_title, book.get('author', ''))

        # Create detailed info
        detailed_info = create_detailed_info(book)

        # Update book entry
        book['title'] = short_title
        book['detailed_info'] = detailed_info

        # Keep original title in description for search
        if not book.get('description'):
            book['description'] = original_title

        # Track statistics
        if short_title != original_title:
            titles_shortened += 1
        else:
            unchanged += 1

    print(f"\n✓ Processed {len(library_data['books'])} books")
    print(f"  - Titles shortened: {titles_shortened}")
    print(f"  - Unchanged: {unchanged}")

    # Save optimized database
    with open('data/library_database.json', 'w', encoding='utf-8') as f:
        json.dump(library_data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Saved optimized database to data/library_database.json")

    # Show examples
    print("\n" + "="*80)
    print("EXAMPLES OF OPTIMIZED TITLES:")
    print("="*80)

    for i, book in enumerate(library_data['books'][:5], 1):
        print(f"\n{i}. Short Title: {book['title']}")
        print(f"   Original: {book['description'][:100]}...")
        print(f"   Author: {book['author']}")
        print(f"   Detailed info preview: {book['detailed_info'][:150]}...")

if __name__ == "__main__":
    optimize_library_database()
    print("\n✓ Library database optimization complete!")
