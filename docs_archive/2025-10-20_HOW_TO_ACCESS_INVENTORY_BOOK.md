# How to Access the Inventory Book System

## ✅ The inventory book is now fully integrated and visible!

## 4 Ways to Access the Inventory Book

### 1. From Museum Databases Page (Main Entry Point)

**Path**: Admin Panel → Museum Databases

You'll see **two new database cards**:

```
┌──────────────────────────────────────┐
│  📖 Књига Инвентара                 │
│  4044                                │
│  Физичка књига инвентара - 4.044    │
│  археолошких записа                  │
│  (под Минералошком базом)            │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│  📋 Упоређивање инвентара            │
│  ✓                                   │
│  Алат за упоређивање књиге          │
│  инвентара са ревидираном базом      │
└──────────────────────────────────────┘
```

Click on either card to access that feature.

### 2. From Mineral Collection Page (Quick Access Buttons)

**Path**: Admin Panel → Mineral Collection (База минерала)

At the top of the page, you'll see **two new prominent buttons**:

```
┌──────────────────────────────────────────────────────────┐
│  Минералошка збирка                                      │
│                                                          │
│  [Књига Инвентара] [Упоређивање] [Додај слике] [PDF]  │
└──────────────────────────────────────────────────────────┘
```

**Plus** a yellow alert banner below:

```
⚠️ Књига Инвентара доступна: Приступите физичкој књизи
   инвентара са 4.044 историјских записа или користите алат
   за упоређивање са ревидираном базом.
   [Отвори књигу] | [Упоређивање]
```

### 3. Direct URL Access

Simply navigate to:

**Inventory Book**:
```
http://your-museum-url/admin/inventory_book
```

**Reconciliation Tool**:
```
http://your-museum-url/admin/inventory_reconciliation
```

### 4. From Navigation Between Tools

Once you're in either tool, you can navigate:

**From Inventory Book page**:
- Button: "Алат за упоређивање" → Goes to reconciliation
- Button: "Минералошка база" → Goes back to mineral collection

**From Reconciliation page**:
- Button: "Књига инвентара" → Goes to inventory book
- Button: "Минералошка база" → Goes to mineral collection

## What You'll See

### Inventory Book Page (`/admin/inventory_book`)

```
┌────────────────────────────────────────────────────────┐
│ 📖 Књига Инвентара                                    │
│ Физичка књига инвентара - археолошки запис музејске   │
│ збирке                                                 │
│                                        [4044 Ставки]   │
├────────────────────────────────────────────────────────┤
│                                                        │
│ Statistics:                                            │
│ [3956 Јединствени инв. бр.] [1-3961 Опсег] [4 Листа] │
│                                                        │
│ Actions:                                               │
│ [Алат за упоређивање] [Минералошка база]              │
│                                                        │
│ Search & Filters:                                      │
│ Инв. број: [_____]  Назив: [_____]                    │
│ Локалитет: [_____]  Лист: [Dropdown]                  │
│ [Претражи] [Ресетуј]                                   │
│                                                        │
│ Results Table:                                         │
│ ┌───┬─────────┬────────────┬───────────┬──────────┐  │
│ │Инв│ Назив   │ Локалитет  │ Количина  │ Лист     │  │
│ ├───┼─────────┼────────────┼───────────┼──────────┤  │
│ │ 1 │Melanit  │            │           │Main Inv. │  │
│ │ 2 │Topaz    │            │           │Main Inv. │  │
│ │ 3 │Topaz    │Ural        │           │Main Inv. │  │
│ └───┴─────────┴────────────┴───────────┴──────────┘  │
│                                                        │
│ Pagination: [◀] 1 2 3 ... 41 [▶]                      │
└────────────────────────────────────────────────────────┘
```

### Reconciliation Page (`/admin/inventory_reconciliation`)

```
┌────────────────────────────────────────────────────────┐
│ 📋 Упоређивање инвентара                              │
│ Алат за упоређивање физичке књиге инвентара са        │
│ стварном ревидираном базом података                    │
├────────────────────────────────────────────────────────┤
│                                                        │
│ Actions:                                               │
│ [Књига инвентара] [Минералошка база]                  │
│                                                        │
│ Statistics:                                            │
│ [4044 Ставки у књизи] [0 Ставки у бази]              │
│ [0 Упарено] [0 Неслагања]                            │
│                                                        │
│ Distribution:                                          │
│ ┌───────────────────────┬───────────────────────────┐ │
│ │ По листовима:         │ Посебне категорије:       │ │
│ │ • Main Inventory: 3975│ • Meteorit: 19           │ │
│ │ • Meteoriti: 19       │ • Azbest: 30             │ │
│ │ • Lista AZBESTA: 30   │ • Radioaktivni: 20       │ │
│ │ • Lista Radio...: 20  │                           │ │
│ └───────────────────────┴───────────────────────────┘ │
│                                                        │
│ Inventory Range: 1 - 3961 (3956 јединствених)        │
└────────────────────────────────────────────────────────┘
```

## Quick Navigation Map

```
Admin Panel
    │
    ├─ Museum Databases
    │       │
    │       ├─ База минерала (2621)
    │       ├─ 📖 Књига Инвентара (4044) ← NEW!
    │       └─ 📋 Упоређивање инвентара (✓) ← NEW!
    │
    └─ Mineral Collection
            │
            ├─ [Књига Инвентара] button ← NEW!
            └─ [Упоређивање] button ← NEW!
```

## Search Examples

Once in the Inventory Book page, try these searches:

1. **Find minerals from Trepča**:
   - Локалитет: "Trepča"
   - Click Претражи
   - Result: 768 items

2. **Find Calcite specimens**:
   - Назив: "Kalcit"
   - Click Претражи
   - Result: 638 items

3. **View meteorites only**:
   - Лист: Select "Meteoriti"
   - Click Претражи
   - Result: 19 items

4. **Look up specific inventory number**:
   - Инв. број: "1"
   - Click Претражи
   - Result: First item (Melanit)

## Features Available

✅ **Inventory Book View**:
- Browse all 4,044 records
- Search by name, locality, inventory number
- Filter by sheet type
- Paginated display (100 items/page)
- Statistics overview

✅ **Reconciliation Tool**:
- View inventory statistics
- See distribution across sheets
- Category breakdowns
- Ready for comparison (when revision data available)

## Troubleshooting

**Q: I don't see the inventory book cards**
A: Make sure you're logged in as admin and navigate to `/admin/museum_databases`

**Q: The buttons don't appear on mineral collection page**
A: Refresh the page (Ctrl+F5) to clear cache

**Q: I get an error when clicking**
A: Ensure the database files exist:
   - `data/inventory_book.db`
   - `data/inventory_book.json`

**Q: Direct URL doesn't work**
A: Make sure you're logged in as admin user first

## Support

If you still can't see the inventory book:

1. Check that these files exist:
   ```bash
   ls -la data/inventory_book.db
   ls -la data/inventory_book.json
   ```

2. Verify routes are registered:
   ```bash
   python3 -c "from app import app; print(app.url_map)"
   ```

3. Restart the app:
   ```bash
   pkill -f "python.*app.py"
   python3 app.py
   ```

---
**Last Updated**: October 20, 2025
**Status**: ✅ Fully Integrated and Visible
