# Phase 3: Complete Database Migration to PostgreSQL

**Date**: December 25, 2025
**Status**: 📋 Planning
**Current Progress**: 6/26 databases migrated (23%)

---

## Executive Summary

Phase 2 successfully migrated **6 core databases** to PostgreSQL. However, analysis reveals that **20 additional databases** are still using in-memory Python dictionaries or JSON files. This document provides a complete inventory and migration plan for Phase 3.

---

## Current Database Inventory

### ✅ Phase 2 - MIGRATED TO POSTGRESQL (6 databases)

| Database | Storage | Records | Status |
|----------|---------|---------|--------|
| **Bird Ringing** | PostgreSQL | 157,115 | ✅ Complete |
| **Minerals Collection** | PostgreSQL | 2,571 | ✅ Complete |
| **RRUFF Reference** | PostgreSQL | 5,997 | ✅ Complete |
| **Inventory Book** | PostgreSQL | 3,970 | ✅ Complete |
| **Users/Authentication** | PostgreSQL | 7 | ✅ Complete |
| **Timesheet** | PostgreSQL | 0 (schema ready) | ✅ Complete |

**Total Migrated**: ~170,000 records

---

### ❌ Phase 3 - NEEDS MIGRATION (20 databases)

#### Category 1: Administrative Databases (5)

| # | Database | Current Storage | Estimated Records | Priority |
|---|----------|-----------------|-------------------|----------|
| 1 | **Library Database** | JSON file (1.1 MB) | ~598 books | HIGH |
| 2 | **Employees Database** | Python dict | ~7 | HIGH |
| 3 | **Employee Profiles** | JSON file (34 KB) | ~7 | MEDIUM |
| 4 | **Visitors Database** | Python list `[]` | 0 | LOW |
| 5 | **Research Projects** | Python dict | ~3 | MEDIUM |

#### Category 2: Exhibition & Display (3)

| # | Database | Current Storage | Estimated Records | Priority |
|---|----------|-----------------|-------------------|----------|
| 6 | **Exhibits Database** | Python dict | ~50 | MEDIUM |
| 7 | **Exhibitions Database** | JSON (33 KB) | ~20 | HIGH |
| 8 | **News Database** | JSON (154 KB) | ~30 | MEDIUM |

#### Category 3: Cultural Heritage (1)

| # | Database | Current Storage | Estimated Records | Priority |
|---|----------|-----------------|-------------------|----------|
| 9 | **Cultural Heritage** | Python dict | ~30 items | HIGH |

#### Category 4: Biology Collections (7)

| # | Database | Current Storage | Estimated Records | Priority |
|---|----------|-----------------|-------------------|----------|
| 10 | **Botany Collection** | Python dict | ~85 specimens | MEDIUM |
| 11 | **Ichthyology** | Python dict | ~45 specimens | LOW |
| 12 | **Entomology** | Python dict | ~12 specimens | LOW |
| 13 | **Mycology** | Python dict | ~8 specimens | LOW |
| 14 | **Herpetology** | Python dict | ~22 specimens | LOW |
| 15 | **Ornithology** | Python dict | ~35 specimens | LOW |
| 16 | **Conservation Biology** | Python dict | ~12 records | LOW |

#### Category 5: Geology Collections (4)

| # | Database | Current Storage | Estimated Records | Priority |
|---|----------|-----------------|-------------------|----------|
| 17 | **Paleozoology** | Python dict | ~48 specimens | MEDIUM |
| 18 | **Paleobotany** | Python dict | ~18 specimens | LOW |
| 19 | **Petrology** | Python dict | ~28 specimens | LOW |
| 20 | **Meteorite Collection** | Python dict | ~15 specimens | HIGH |

**Total to Migrate**: ~1,100 records (estimated)

---

## Current Storage Methods

### Python Dictionaries (In-Memory)
**Problem**: Data is lost on app restart unless manually saved
**Files**: Defined in `app.py` lines 481-1587

- `EXHIBITS_DATABASE`
- `EXHIBITIONS_DATABASE`
- `NEWS_DATABASE`
- `BOTANY_COLLECTION_DATABASE`
- `ICHTHYOLOGY_COLLECTION_DATABASE`
- `ENTOMOLOGY_COLLECTION_DATABASE`
- `MYCOLOGY_COLLECTION_DATABASE`
- `HERPETOLOGY_COLLECTION_DATABASE`
- `ORNITHOLOGY_COLLECTION_DATABASE`
- `PALEOZOOLOGY_COLLECTION_DATABASE`
- `PALEOBOTANY_COLLECTION_DATABASE`
- `PETROLOGY_COLLECTION_DATABASE`
- `METEORITE_COLLECTION_DATABASE`
- `CONSERVATION_BIOLOGY_DATABASE`
- `CULTURAL_HERITAGE_DATABASE`

### JSON Files (Persistent but not database)
**Problem**: No ACID guarantees, no relationships, no concurrent access control

- `data/library_database.json` (1.1 MB) - Library books
- `data/employee_directory.json` (34 KB) - Employee profiles
- `data/exhibitions.json` (33 KB) - Exhibition records
- `data/news.json` (154 KB) - News articles
- `data/museum_vehicles.json` (1.3 KB) - Vehicles (optional)

### Python Lists (In-Memory, Volatile)
**Problem**: Always starts empty, no persistence

- `VISITOR_RECORDS = []`
- `RESEARCH_PROJECTS` (dict but starts empty)

---

## Migration Priority Levels

### HIGH Priority (Immediate - Phase 3A)

**Why**: Active use, significant data, business critical

1. **Library Database** (598 books) - Actively used, has real data
2. **Exhibitions Database** (~20 exhibitions) - Public-facing, historical records
3. **Cultural Heritage** (~30 items) - Protected cultural items, legal importance
4. **Meteorite Collection** (~15 specimens) - Real scientific data
5. **Employees Database** (7 employees) - Core administrative data

**Estimated Time**: 1-2 weeks
**Records**: ~670

### MEDIUM Priority (Phase 3B)

**Why**: Some real data, moderate importance

6. **Exhibits Database** (~50 artifacts) - Display management
7. **News Database** (~30 articles) - Content management
8. **Research Projects** (~3 projects) - Academic tracking
9. **Employee Profiles** (7 profiles) - Biographical data
10. **Botany Collection** (~85 specimens) - Largest biology collection
11. **Paleozoology** (~48 specimens) - Significant geology collection

**Estimated Time**: 1-2 weeks
**Records**: ~223

### LOW Priority (Phase 3C - Optional)

**Why**: Minimal data, demo/placeholder collections

12-20. **Remaining Collections** - Mostly placeholder/demo data
   - Ichthyology, Entomology, Mycology, Herpetology
   - Ornithology, Conservation Biology
   - Paleobotany, Petrology
   - Visitors Database (empty)

**Estimated Time**: 1 week
**Records**: ~160

---

## Migration Strategy

### Approach 1: Generic Collection Migration (Recommended)

Create a **generic collections table** structure that can handle all curator collections:

```sql
-- Generic collections schema
CREATE TABLE collections (
    id SERIAL PRIMARY KEY,
    collection_type VARCHAR(50) NOT NULL,  -- 'botany', 'meteorite', etc.
    catalog_number VARCHAR(100) NOT NULL,
    specimen_name TEXT,
    scientific_name TEXT,
    common_name TEXT,
    description TEXT,
    collection_date DATE,
    collector TEXT,
    location TEXT,
    coordinates GEOGRAPHY(POINT, 4326),
    habitat TEXT,
    notes TEXT,
    dimensions JSONB,  -- Flexible field for measurements
    metadata JSONB,    -- Collection-specific fields
    images JSONB,      -- Image references
    status VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(collection_type, catalog_number)
);

CREATE INDEX collections_type_idx ON collections(collection_type);
CREATE INDEX collections_catalog_idx ON collections(catalog_number);
CREATE INDEX collections_name_idx ON collections(specimen_name);
CREATE INDEX collections_sci_name_idx ON collections(scientific_name);
```

**Benefits**:
- Single migration script for all 14 collections
- Consistent structure
- Easy to add new collections
- Metadata JSONB for collection-specific fields

### Approach 2: Dedicated Tables per Category

Create specific tables for each category:

```sql
-- Library
CREATE TABLE library_books (...);

-- Exhibitions
CREATE TABLE exhibitions (...);
CREATE TABLE exhibition_items (...);

-- Cultural Heritage
CREATE TABLE heritage_items (...);

-- News
CREATE TABLE news_articles (...);
```

**Benefits**:
- Optimized schema per category
- Type-safe fields
- Better for complex relationships

### Recommended: Hybrid Approach

- **Generic collections table** for all curator collections (14 databases)
- **Dedicated tables** for administrative data (library, exhibitions, heritage, news)

---

## Phase 3 Implementation Plan

### Phase 3A: High Priority Migration

**Duration**: 1-2 weeks

#### Week 1: Schema Design & Administrative Data

**Days 1-2: Schema Design**
```sql
-- Create schemas for:
CREATE SCHEMA IF NOT EXISTS library;
CREATE SCHEMA IF NOT EXISTS exhibitions;
CREATE SCHEMA IF NOT EXISTS collections;
CREATE SCHEMA IF NOT EXISTS heritage;
```

**Days 3-4: Library Database Migration**
- Parse `library_database.json`
- Migrate 598 books to PostgreSQL
- Update `app.py` to use PostgreSQL
- Test library features

**Days 5-7: Exhibitions & Heritage**
- Migrate exhibitions.json
- Migrate cultural heritage items
- Create relationships (exhibition → items)
- Test public-facing exhibitions page

#### Week 2: Collections & Employees

**Days 1-3: Meteorite Collection**
- Migrate meteorite specimens (highest scientific value)
- Add detailed scientific fields
- Test QR code generation

**Days 4-5: Employees Database**
- Migrate employee directory
- Merge with existing users table
- Update authentication

**Days 6-7: Testing & Verification**
- End-to-end testing
- Data integrity checks
- Performance benchmarks

### Phase 3B: Medium Priority

**Duration**: 1-2 weeks

- Migrate exhibits database
- Migrate news articles
- Migrate research projects
- Migrate employee profiles
- Migrate botany collection
- Migrate paleozoology collection

### Phase 3C: Low Priority

**Duration**: 1 week

- Migrate remaining 8 curator collections
- Implement visitors database (currently empty)
- Performance optimization
- Final cleanup

---

## Migration Scripts Needed

### 1. Library Migration
```python
# scripts/migrate_library_to_postgres.py
import json
import psycopg

# Load library_database.json
# Create library schema
# Migrate books, categories, statistics
```

### 2. Exhibitions Migration
```python
# scripts/migrate_exhibitions_to_postgres.py
# Load exhibitions.json
# Create exhibitions and exhibition_items tables
# Migrate with relationships
```

### 3. Collections Migration (Generic)
```python
# scripts/migrate_collections_to_postgres.py
# Migrate all 14 curator collections using generic schema
# Handle JSONB metadata for collection-specific fields
```

### 4. Cultural Heritage Migration
```python
# scripts/migrate_heritage_to_postgres.py
# Migrate CULTURAL_HERITAGE_DATABASE
# Preserve legal/protection data
```

---

## Database Schema Updates Needed

### File: `db/schema_phase3.sql`

```sql
-- Library Schema
CREATE TABLE library_books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT,
    isbn VARCHAR(20),
    category VARCHAR(100),
    status VARCHAR(50) DEFAULT 'доступна',
    location TEXT,
    acquisition_date DATE,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Exhibitions Schema
CREATE TABLE exhibitions (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    exhibition_type VARCHAR(50),
    start_date DATE,
    end_date DATE,
    location TEXT,
    curator TEXT,
    status VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE exhibition_items (
    id SERIAL PRIMARY KEY,
    exhibition_id INTEGER REFERENCES exhibitions(id),
    item_type VARCHAR(50),
    item_id INTEGER,
    description TEXT
);

-- Cultural Heritage Schema
CREATE TABLE heritage_items (
    id SERIAL PRIMARY KEY,
    registry_number VARCHAR(100) UNIQUE,
    item_name TEXT NOT NULL,
    heritage_type VARCHAR(100),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    significance_level VARCHAR(100),
    description TEXT,
    location TEXT,
    protection_status VARCHAR(100),
    condition VARCHAR(50),
    dimensions JSONB,
    date_of_origin TEXT,
    creator TEXT,
    cultural_period TEXT,
    material TEXT,
    technique TEXT,
    provenance TEXT,
    legal_basis TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Generic Collections Schema
CREATE TABLE collections (
    id SERIAL PRIMARY KEY,
    collection_type VARCHAR(50) NOT NULL,
    catalog_number VARCHAR(100) NOT NULL,
    specimen_name TEXT,
    scientific_name TEXT,
    common_name TEXT,
    description TEXT,
    collection_date DATE,
    collector TEXT,
    location TEXT,
    coordinates GEOGRAPHY(POINT, 4326),
    habitat TEXT,
    notes TEXT,
    dimensions JSONB,
    metadata JSONB,
    images JSONB,
    status VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(collection_type, catalog_number)
);

-- News/Articles Schema
CREATE TABLE news_articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    subtitle TEXT,
    content TEXT,
    author TEXT,
    published_date DATE,
    category VARCHAR(100),
    tags TEXT[],
    featured BOOLEAN DEFAULT FALSE,
    status VARCHAR(50) DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Research Projects Schema
CREATE TABLE research_projects (
    id SERIAL PRIMARY KEY,
    project_title TEXT NOT NULL,
    principal_investigator TEXT,
    co_investigators TEXT[],
    start_date DATE,
    end_date DATE,
    status VARCHAR(50),
    funding_source TEXT,
    budget NUMERIC(12,2),
    description TEXT,
    objectives TEXT,
    methodology TEXT,
    findings TEXT,
    publications TEXT[],
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Visitors Database Schema
CREATE TABLE visitor_records (
    id SERIAL PRIMARY KEY,
    visit_date DATE NOT NULL,
    visitor_name TEXT,
    visitor_type VARCHAR(50),
    group_size INTEGER,
    purpose VARCHAR(100),
    contact_info TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Create indexes
CREATE INDEX library_books_category_idx ON library_books(category);
CREATE INDEX library_books_status_idx ON library_books(status);
CREATE INDEX exhibitions_dates_idx ON exhibitions(start_date, end_date);
CREATE INDEX heritage_type_idx ON heritage_items(heritage_type);
CREATE INDEX collections_type_idx ON collections(collection_type);
CREATE INDEX collections_catalog_idx ON collections(catalog_number);
CREATE INDEX news_published_idx ON news_articles(published_date);
CREATE INDEX research_status_idx ON research_projects(status);
```

---

## App Integration Changes

### Files to Modify

1. **`app.py`**
   - Remove Python dictionary definitions
   - Add PostgreSQL query functions
   - Update all route handlers

2. **Create new modules**:
   - `library_database_pg.py`
   - `exhibitions_database_pg.py`
   - `collections_database_pg.py`
   - `heritage_database_pg.py`

3. **Update templates** (if needed):
   - Most templates should work with minimal changes
   - Query results will be similar structure

---

## Data Persistence Risk Assessment

### Current Risks (Before Migration)

| Database | Risk Level | Data Loss Risk | Impact |
|----------|------------|----------------|---------|
| Python dicts | 🔴 CRITICAL | **100% on restart** | All collection data lost |
| JSON files | 🟡 MEDIUM | Low (but no ACID) | File corruption possible |
| Empty lists | 🔴 CRITICAL | **100% always** | No persistence at all |

### After Migration

| Database | Risk Level | Data Loss Risk | Impact |
|----------|------------|----------------|---------|
| PostgreSQL | 🟢 LOW | <0.01% with backups | Enterprise-grade reliability |

---

## Testing Requirements

### Phase 3A Testing

- [ ] Library books CRUD operations
- [ ] Exhibition creation and display
- [ ] Cultural heritage management
- [ ] Meteorite collection QR codes
- [ ] Employee authentication

### Phase 3B Testing

- [ ] News article publishing
- [ ] Research project tracking
- [ ] Collection searches across all types
- [ ] Image attachments

### Phase 3C Testing

- [ ] All collections accessible
- [ ] QR code generation for all
- [ ] Export functions
- [ ] Performance under load

---

## Success Criteria

**Phase 3 is complete when:**

1. ✅ All 26 databases using PostgreSQL
2. ✅ Zero Python dictionaries for data storage
3. ✅ JSON files converted to PostgreSQL
4. ✅ All CRUD operations functional
5. ✅ Data integrity validated (100% records migrated)
6. ✅ Performance acceptable (<100ms queries)
7. ✅ Backups automated
8. ✅ All tests passing

---

## Benefits of Complete Migration

### Before (Current State)

- ❌ 20/26 databases using volatile storage
- ❌ Data lost on restart (Python dicts)
- ❌ No relationships between collections
- ❌ No transaction support
- ❌ No concurrent access control
- ❌ Limited search capabilities
- ❌ No backup strategy for dicts

### After (Phase 3 Complete)

- ✅ 100% PostgreSQL (26/26 databases)
- ✅ Data persistent and ACID-compliant
- ✅ Relationships and foreign keys
- ✅ Transaction support
- ✅ Concurrent access safe
- ✅ Full-text search
- ✅ Point-in-time recovery
- ✅ Advanced queries (PostGIS, JSON aggregations)

---

## Estimated Timeline

| Phase | Duration | Databases | Priority |
|-------|----------|-----------|----------|
| **Phase 3A** | 1-2 weeks | 5 | HIGH |
| **Phase 3B** | 1-2 weeks | 6 | MEDIUM |
| **Phase 3C** | 1 week | 9 | LOW |
| **Testing & Optimization** | 1 week | All | - |
| **TOTAL** | **4-6 weeks** | **20** | - |

---

## Quick Start for Phase 3A

### Step 1: Create Schema

```bash
cd /home/aleksandarlukovic/MuseumInfoSystem
psql $DATABASE_URL -f db/schema_phase3.sql
```

### Step 2: Run Library Migration

```bash
python3 scripts/migrate_library_to_postgres.py
```

### Step 3: Update App

```python
# app.py - Replace
LIBRARY_DATABASE = load_library_database()

# With
from library_database_pg import get_library_database
library_db = get_library_database()
```

### Step 4: Test

```bash
# Restart museum system
sudo systemctl restart museum-system

# Check library page
curl http://localhost/admin/library_database
```

---

## Next Actions

1. **Review this plan** - Confirm priorities and timeline
2. **Create db/schema_phase3.sql** - Design PostgreSQL schema
3. **Start with Library migration** - Highest value, has real data
4. **Test incrementally** - One database at a time
5. **Update documentation** - Track progress

---

**Document Created**: December 25, 2025
**Phase**: 3 (Planning)
**Target**: Complete database migration to PostgreSQL
**Expected Completion**: 4-6 weeks from start
