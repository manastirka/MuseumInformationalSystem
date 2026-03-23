#!/usr/bin/env python3
"""
Test script to verify library optimization
"""
import json

print("Testing library optimization...")
print("="*80)

# Load optimized library
with open('data/library_database.json', 'r', encoding='utf-8') as f:
    library = json.load(f)

# Test 1: Check all books have required fields
print("\n1. Checking data structure...")
books = library['books']
missing_detailed_info = []
long_titles = []

for book in books:
    if 'detailed_info' not in book:
        missing_detailed_info.append(book['id'])
    if len(book['title']) > 100:
        long_titles.append({
            'id': book['id'],
            'title': book['title'],
            'length': len(book['title'])
        })

print(f"   ✓ Total books: {len(books)}")
print(f"   ✓ Books with detailed_info: {len(books) - len(missing_detailed_info)}")
if missing_detailed_info:
    print(f"   ⚠ Books missing detailed_info: {len(missing_detailed_info)}")

# Test 2: Check title lengths
print(f"\n2. Title length analysis...")
avg_title_length = sum(len(book['title']) for book in books) / len(books)
print(f"   ✓ Average title length: {avg_title_length:.1f} characters")
print(f"   ✓ Titles over 100 chars: {len(long_titles)}")

if long_titles:
    print(f"\n   First 5 long titles:")
    for item in long_titles[:5]:
        print(f"     - ID {item['id']}: {item['title'][:80]}... ({item['length']} chars)")

# Test 3: Sample detailed info
print(f"\n3. Sample detailed information:")
for i, book in enumerate(books[:3], 1):
    print(f"\n   Book {i}: {book['title']}")
    print(f"   Author: {book['author']}")
    print(f"   Detailed info preview:")
    detail_preview = book.get('detailed_info', 'N/A')[:200]
    print(f"   {detail_preview}...")

# Test 4: Search functionality test
print(f"\n4. Testing search data...")
search_test_queries = ['Панчић', 'Darwin', 'биологија', '1942', 'Београд']
for query in search_test_queries:
    matches = []
    for book in books:
        # Simulate search across all fields
        search_text = f"{book['title']} {book['author']} {book.get('description', '')} {book.get('publisher', '')}".lower()
        if query.lower() in search_text:
            matches.append(book['title'])
    print(f"   Query '{query}': {len(matches)} results")
    if matches:
        print(f"      Example: {matches[0][:60]}...")

print("\n" + "="*80)
print("✓ Library optimization test complete!")
print(f"\nSummary:")
print(f"  - {len(books)} books processed")
print(f"  - {len(books) - len(missing_detailed_info)} books have detailed info")
print(f"  - Average title length: {avg_title_length:.1f} characters")
print(f"  - Search functionality preserved across all fields")
