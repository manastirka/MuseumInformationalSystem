# Inventory Book System - Quick Start Guide

## Overview
This system provides digital access to the physical inventory book ("Knjiga Inventara") with 4,044 historical records, and tools to compare it with the actual mineral collection database.

## Quick Access

### 1. View Inventory Book
```
URL: /admin/inventory_book
```

What you can do:
- Browse all 4,044 inventory records
- Search by mineral name, locality, or inventory number
- Filter by sheet type (Main Inventory, Meteorites, etc.)
- See acquisition history and notes

### 2. Reconciliation Tool
```
URL: /admin/inventory_reconciliation
```

What you can do:
- View statistics and summaries
- See distribution across sheets
- Compare book vs database (when data available)
- Identify discrepancies

## Common Tasks

### Search for a Specific Mineral

1. Go to `/admin/inventory_book`
2. Enter mineral name in "Назив минерала" field
3. Click "Претражи" (Search)

Example: Search for "Калцит" finds 638 items

### Find Items from a Locality

1. Go to `/admin/inventory_book`
2. Enter locality in "Локалитет" field
3. Click "Претражи"

Example: Search for "Трепча" finds 768 items

### Look Up by Inventory Number

1. Go to `/admin/inventory_book`
2. Enter number in "Инв. број" field
3. Click "Претражи"

Example: Search for "1" finds the first inventory item (Melanit)

### Filter by Sheet Type

1. Go to `/admin/inventory_book`
2. Select sheet from "Лист" dropdown:
   - Main Inventory (3,975 items)
   - Meteoriti (19 items)
   - Lista AZBESTA (30 items)
   - Lista Radioaktivnih (20 items)
3. Click "Претражи"

## Data Structure

Each inventory record contains:

| Field | Description |
|-------|-------------|
| **Инв. број** | Inventory number (1-3,961) |
| **Назив** | Mineral name |
| **Локалитет** | Locality where found |
| **Количина** | Quantity/pieces |
| **Начин набавке** | How acquired (purchase, donation, etc.) |
| **Колектор** | Who collected/donated |
| **Лист** | Which sheet in the book |
| **Напомене** | Additional notes |

## Special Collections

### Meteorites (19 items)
Famous specimens including:
- **Sokobanjski meteorit** - 16.286 kg, fell 1877
- **Jelički meteorit** - 7.380 kg, fell 1889
- International specimens from Australia

Access: Filter by sheet "Meteoriti"

### Asbestos Collection (30 items)
Historical asbestos specimens from various localities

Access: Filter by sheet "Lista AZBESTA"

### Radioactive Minerals (20 items)
Including Uraninit, Torbernit, and others

Access: Filter by sheet "Lista Radioaktivnih"

## Historical Context

### Acquisition Sources
The inventory book documents minerals acquired from:
- **Dr. Pavle Ivić** (1955) - Major collection purchase
- **Milan Ristić** (1947)
- **Narodna biblioteka Srbije** - Donations
- Various collectors and donations

### Time Period
Records span from 1950s to present, with inventory numbers 1-3,961

### Notable Localities
- **Trepča**: 768 specimens (major Serbian mining site)
- **Bor**: Multiple copper-related specimens
- **International**: Ural, Germany, Czechoslovakia, Australia

## Statistics at a Glance

```
Total Items:          4,044
Unique Inv. Numbers:  3,956
Inventory Range:      1 - 3,961
Sheets:               4

Breakdown:
  Main Inventory:     3,975 items
  Meteorites:            19 items
  Asbestos:              30 items
  Radioactive:           20 items
```

## Comparison Tool

The reconciliation tool (`/admin/inventory_reconciliation`) now compares the physical inventory book with the revised mineralogical database in real time.

✅ **Current Features**:
- Automated comparison between book records and the revised collection
- Detection of items missing from either source
- Name similarity checks with percentage scoring
- Locality mismatch detection
- Duplicate inventory number tracking (book vs database)
- Collection statistics, including items without inventory numbers

📄 **Planned Enhancements**:
- Export discrepancy reports to PDF/Excel

## Tips & Tricks

### 1. Broad Search
Leave all fields empty and click search to see all records (paginated)

### 2. Combined Filters
You can combine multiple search criteria:
- Name: "Galenit"
- Locality: "Trepča"
- Sheet: "Main Inventory"

### 3. Partial Matching
Searches use partial matching:
- "Kvar" finds "Kvarc", "Kvarcit", etc.
- "Trep" finds "Trepča", "Trepcit", etc.

### 4. Navigation
Use the sheet breakdown at the bottom to quickly see distribution of items

### 5. Export Data
Future feature: Export search results to CSV/PDF

## Troubleshooting

**Q: Page loads slowly**
A: Large datasets are paginated. Use filters to narrow results.

**Q: Can't find an item**
A: Try:
- Partial name search
- Check different spelling variants
- Look in different sheets
- Search by inventory number

**Q: Reconciliation shows no comparison data**
A: Ensure the revised mineral database (`PrirodnjackiMuzej/prirodnjacki_muzej.sqlite`) is accessible and restart the application if the connection was established while the server was running.

## Data Quality Notes

- Some entries may have incomplete locality information
- Historical spelling variations exist
- Some inventory numbers may have gaps
- Acquisition dates are as recorded in the original book

## Support

For technical issues or questions about the inventory book system:
- Check the full documentation: `INVENTORY_BOOK_SYSTEM_SUMMARY.md`
- Review the source code: `parse_inventory_book.py`, `inventory_reconciliation.py`

---
**Last Updated**: October 20, 2025
**Version**: 1.0
**Records**: 4,044 items from physical inventory book
