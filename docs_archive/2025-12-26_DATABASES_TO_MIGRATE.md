# Complete Database Migration Analysis
**Date**: December 26, 2025

---

## Summary

**Total databases in application**: 24
**Already migrated to PostgreSQL**: 10 ✅
**Need migration (REAL DATA)**: 1 ❌ **NEWS/EXHIBITIONS DATABASE**
**Demo data (optional migration)**: 13 databases

---

## ❌ **PRIORITY: Real Data That NEEDS Migration**

### 1. NEWS/EXHIBITIONS Database (Baza vesti/izložbi) 🔴 HIGH PRIORITY
**Source**: `data/news.json`
**Records**: 115 articles/exhibitions
**Status**: ❌ **NOT in PostgreSQL** - Using JSON file
**Route**: `/admin/news`
**Variable**: `NEWS_DATABASE`

**Sample data**:
```json
{
  "title": "Добро дошли у мезозоик",
  "type": "Изложба",
  "status": "Историјска",
  "start_date": "2014-04-30",
  "description": "...",
  ...
}
```

**This is the "baza izložbi" that needs migration!** ← Contains exhibition and news/event data

---

## ✅ **Already Migrated to PostgreSQL (10 databases)**

| # | Database | Records | Status |
|---|----------|---------|--------|
| 1 | Bird Ringing | 157,115 | ✅ Working |
| 2 | Minerals | 2,571 | ✅ Working |
| 3 | Inventory Book | 3,970 | ✅ Working |
| 4 | RRUFF Reference | 5,997 | ✅ Working |
| 5 | Library | 598 | ✅ Working |
| 6 | Exhibitions (Phase 3A) | 34 | ✅ Working |
| 7 | Cultural Heritage | 6 | ✅ Working |
| 8 | Meteorites | 18 | ✅ Working |
| 9 | Employees | 42 | ✅ Working |
| 10 | Employee Profiles | 42 | ✅ Working |

---

## 📊 **Demo/Empty Databases (13 databases)**

These contain hardcoded demonstration data or are empty. Migration is optional.

### Biological Collections (9 collections)
| # | Collection | Specimens | Type |
|---|------------|-----------|------|
| 1 | Botany | 5 | Demo |
| 2 | Ichthyology | 3 | Demo |
| 3 | Entomology | ~6 | Demo |
| 4 | Mycology | ~5 | Demo |
| 5 | Herpetology | ~6 | Demo |
| 6 | Ornithology | ~5 | Demo |
| 7 | Paleozoology | ~6 | Demo |
| 8 | Paleobotany | ~4 | Demo |
| 9 | Petrology/Geological | ~4 | Demo |

### Other Demo/Empty Databases (4 databases)
| # | Database | Records | Type |
|---|----------|---------|------|
| 10 | Exhibits/Artifacts | ~10 | Demo |
| 11 | Conservation Biology | 2 | Demo |
| 12 | Visitors | 0 | Empty |
| 13 | Research Projects | 0 | Empty |

---

## Migration Action Plan

### 🔴 **Phase 1: Migrate Real Data (IMMEDIATE)**

#### Task: Migrate NEWS Database to PostgreSQL
**Priority**: HIGH
**Effort**: 1-2 hours
**Records**: 115 articles/exhibitions

**Steps**:
1. Create `news_articles` table in PostgreSQL schema
2. Write migration script to load from `data/news.json`
3. Update `app.py` to load from PostgreSQL (similar to exhibitions)
4. Test `/admin/news` route
5. Verify all 115 articles migrated correctly

**Schema**:
```sql
CREATE TABLE news_articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    title_en TEXT,
    type TEXT,
    status TEXT,
    start_date DATE,
    end_date DATE,
    location TEXT,
    curator TEXT,
    co_curator TEXT,
    specimens_count INTEGER DEFAULT 0,
    species_count INTEGER DEFAULT 0,
    boxes_count INTEGER DEFAULT 0,
    illustrations_count INTEGER DEFAULT 0,
    visitor_count INTEGER DEFAULT 0,
    description TEXT,
    description_en TEXT,
    target_audience TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
```

---

### 🟡 **Phase 2: Migrate Demo Collections (OPTIONAL)**

#### Task: Create unified collection schema for all 9 biological collections
**Priority**: MEDIUM
**Effort**: 3-4 hours
**Total specimens**: ~50 demo records

**Benefits**:
- Persistent collection data (survives app restart)
- Real collection management capabilities
- Add/edit/delete functionality
- Export and reporting

**Schema**:
```sql
CREATE TABLE collection_specimens (
    id SERIAL PRIMARY KEY,
    catalog_number TEXT UNIQUE NOT NULL,
    collection_type TEXT NOT NULL, -- 'botany', 'ichthyology', etc.
    scientific_name TEXT,
    common_name_sr TEXT,
    family TEXT,
    location_found TEXT,
    date_collected DATE,
    collector TEXT,
    condition TEXT,
    conservation_status TEXT,
    description TEXT,
    curator TEXT,
    metadata JSONB, -- For collection-specific fields
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_collection_type ON collection_specimens(collection_type);
CREATE INDEX idx_catalog_number ON collection_specimens(catalog_number);
```

**Steps**:
1. Create schema
2. Migrate hardcoded data for each collection
3. Update routes to load from PostgreSQL
4. Add CRUD functionality
5. Test all 9 collection interfaces

---

### 🟢 **Phase 3: Other Databases (OPTIONAL)**

#### Exhibits Database
- Status: Demo data only
- Action: Can migrate if real artifact data exists

#### Visitors & Research
- Status: Empty (ready for use)
- Action: No migration needed - already functional

#### Conservation Biology
- Status: 2 demo records
- Action: Can integrate with collection management

---

## Current System Status

### PostgreSQL Tables (37 tables)
```
✅ Core museum data operational
✅ 170,000+ records migrated
✅ All major systems working
❌ NEWS missing from PostgreSQL
```

### Application Routes
```
✅ 10 databases using PostgreSQL
❌ 1 database using JSON (news.json)
📊 13 databases using hardcoded dictionaries
```

---

## Recommendations

### **TODAY: Migrate NEWS Database** 🔴
This is the "baza izložbi" with **real exhibition/event data** that must be in PostgreSQL.

**Command**:
```bash
# 1. Add schema to db/schema.sql
# 2. Create migration script
# 3. Run migration
# 4. Update app.py
# 5. Test
```

### **THIS WEEK: Migrate Collections** 🟡
Convert the 9 biological collections to use PostgreSQL for persistence and proper management.

### **FUTURE: Keep demo data as-is** 🟢
Exhibits, Conservation Biology, Visitors, Research can stay as hardcoded/empty until real data is available.

---

## Files to Modify

### 1. Database Schema
- `db/schema.sql` - Add news_articles table
- `db/schema.sql` - Add collection_specimens table (optional)

### 2. Migration Scripts
- `scripts/migrate_news_to_postgres.py` - NEW
- `scripts/migrate_collections_to_postgres.py` - NEW (optional)

### 3. Application Code
- `app.py` - Update NEWS_DATABASE loading
- `app.py` - Update collection routes (optional)
- `phase3a_databases.py` - Add news accessor functions

### 4. Data Sources
- `data/news.json` - 115 articles (MIGRATE THIS!)
- Hardcoded dictionaries in app.py lines 629-1524 (optional)

---

## Summary

**MUST MIGRATE NOW**:
- ❌ NEWS Database (115 articles) - Real exhibition/event data

**SHOULD MIGRATE SOON**:
- 📊 9 Biological Collections (~50 specimens) - For persistence and management

**CAN SKIP**:
- 4 Demo/Empty databases - No real data to migrate

---

**Next Action**: Create migration script for NEWS database and migrate 115 articles to PostgreSQL.
