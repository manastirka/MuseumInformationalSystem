## Phase 3A Migration Guide
**High-Priority Databases to PostgreSQL**

**Date**: December 25, 2025
**Status**: Ready to Execute

---

## Overview

This guide walks you through migrating 5 high-priority databases from JSON files and Python dictionaries to PostgreSQL.

### Databases Being Migrated:

1. **Library Database** (598 books) - from `library_database.json`
2. **Exhibitions Database** (~20 exhibitions) - from `exhibitions.json`
3. **Cultural Heritage** (~30 items) - from Python dict
4. **Meteorite Collection** (~15 specimens) - from Python dict
5. **Employees Database** (7 employees) - from `employee_directory.json`

**Total Records**: ~670

---

## Prerequisites

### 1. PostgreSQL Running

```bash
# Check PostgreSQL status
systemctl status postgresql

# If not running, start it
sudo systemctl start postgresql

# Enable auto-start
sudo systemctl enable postgresql
```

### 2. DATABASE_URL Set

Check that DATABASE_URL is in your .env file:

```bash
cat .env | grep DATABASE_URL

# Should show:
DATABASE_URL=postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system
```

### 3. Backup Current Data

**IMPORTANT**: Back up your JSON files before migration:

```bash
# Create backup directory
mkdir -p backups/phase3a_$(date +%Y%m%d)

# Backup JSON files
cp data/library_database.json backups/phase3a_$(date +%Y%m%d)/
cp data/exhibitions.json backups/phase3a_$(date +%Y%m%d)/
cp data/employee_directory.json backups/phase3a_$(date +%Y%m%d)/

echo "✓ Backups created"
```

---

## Migration Steps

### Quick Method (Recommended)

**One command does everything:**

```bash
cd /home/aleksandarlukovic/MuseumInfoSystem
./run_phase3a_migration.sh
```

This script will:
1. Check PostgreSQL is running
2. Apply the schema
3. Migrate all 5 databases
4. Offer to restart museum system

---

### Manual Method (Step-by-Step)

If you prefer to run each step manually:

#### Step 1: Apply Schema

```bash
cd /home/aleksandarlukovic/MuseumInfoSystem

# Apply Phase 3A schema to PostgreSQL
psql $DATABASE_URL -f db/schema_phase3a.sql
```

**Expected output**:
```
CREATE TABLE
CREATE TABLE
CREATE INDEX
...
COMMENT
```

**Verify schema**:
```bash
psql $DATABASE_URL -c "\dt" | grep -E "library|exhibition|heritage|meteorite|employee"
```

You should see:
- `library_books`
- `library_categories`
- `exhibitions`
- `exhibition_items`
- `heritage_items`
- `meteorite_specimens`
- `employee_profiles`

#### Step 2: Run Migration

```bash
# Run the all-in-one migration script
python3 scripts/migrate_phase3a_all.py
```

**Expected output**:
```
============================================================================
         PHASE 3A: ALL HIGH-PRIORITY DATABASES MIGRATION
============================================================================

🔌 Connecting to PostgreSQL...
✓ Connected to PostgreSQL

============================================================================
📚 1. LIBRARY DATABASE MIGRATION
============================================================================
📖 Found 598 books, X categories
   ... migrated 100 books
   ... migrated 200 books
   ...
✓ Library migration complete: 598 books, X categories

============================================================================
🎨 2. EXHIBITIONS DATABASE MIGRATION
============================================================================
...

============================================================================
✅ PHASE 3A MIGRATION COMPLETE
============================================================================
```

#### Step 3: Verify Migration

```bash
# Check record counts in PostgreSQL
psql $DATABASE_URL -c "
  SELECT 'library_books' as table, COUNT(*) FROM library_books
  UNION ALL SELECT 'exhibitions', COUNT(*) FROM exhibitions
  UNION ALL SELECT 'heritage_items', COUNT(*) FROM heritage_items
  UNION ALL SELECT 'meteorite_specimens', COUNT(*) FROM meteorite_specimens
  UNION ALL SELECT 'employee_profiles', COUNT(*) FROM employee_profiles
  ORDER BY table;
"
```

**Expected output**:
```
       table        | count
--------------------+-------
 employee_profiles  |     7
 exhibitions        |    20
 heritage_items     |    30
 library_books      |   598
 meteorite_specimens|    15
```

#### Step 4: Restart Museum System

```bash
# Restart to load new PostgreSQL data
sudo systemctl restart museum-system

# Check status
systemctl status museum-system

# View logs
journalctl -u museum-system -n 50
```

---

## Verification & Testing

### 1. Test Library Database

```bash
# Open in browser
http://localhost/admin/library_database

# Or test with curl
curl http://localhost/admin/library_database | grep "598"
```

**Expected**: Should show 598 books from PostgreSQL (not JSON)

### 2. Test Exhibitions

```bash
http://localhost/admin/exhibitions_database
```

**Expected**: Should show exhibitions from PostgreSQL

### 3. Test Cultural Heritage

```bash
http://localhost/admin/cultural_heritage_database
```

**Expected**: Should show heritage items from PostgreSQL

### 4. Test Meteorites

```bash
http://localhost/admin/meteorite_collection
```

**Expected**: Should show meteorite specimens from PostgreSQL

### 5. Test Employees

```bash
http://localhost/admin/employees_database
```

**Expected**: Should show 7 employees from PostgreSQL

### 6. Check App Logs

```bash
# Look for PostgreSQL usage (not JSON loading)
journalctl -u museum-system -n 100 | grep -i "library\|exhibition\|heritage\|meteorite\|employee"
```

**Good signs**:
- No errors about missing JSON files
- Database queries working
- No fallback to Python dicts

**Bad signs**:
- "Library file not found" errors
- Still loading from JSON
- Database connection errors

---

## Troubleshooting

### Issue: Schema Application Fails

**Error**: `ERROR: relation "library_books" already exists`

**Solution**: Tables already exist, you can skip schema step or drop them first:

```bash
psql $DATABASE_URL -c "
  DROP TABLE IF EXISTS library_loans CASCADE;
  DROP TABLE IF EXISTS library_books CASCADE;
  DROP TABLE IF EXISTS library_categories CASCADE;
  -- ... repeat for other tables
"

# Then reapply schema
psql $DATABASE_URL -f db/schema_phase3a.sql
```

### Issue: Migration Script Fails

**Error**: `Could not import CULTURAL_HERITAGE_DATABASE from app.py`

**Solution**: Make sure you're running from the correct directory:

```bash
cd /home/aleksandarlukovic/MuseumInfoSystem
python3 scripts/migrate_phase3a_all.py
```

### Issue: No Records Migrated

**Error**: `⚠️  Library file not found: data/library_database.json`

**Solution**: Check that JSON files exist:

```bash
ls -lh data/library_database.json
ls -lh data/exhibitions.json
ls -lh data/employee_directory.json
```

If files are missing, restore from backups or check file paths.

### Issue: PostgreSQL Connection Failed

**Error**: `Failed to connect to PostgreSQL: connection refused`

**Solution**:

```bash
# Start PostgreSQL
sudo systemctl start postgresql

# Check it's running
systemctl status postgresql

# Verify DATABASE_URL
echo $DATABASE_URL
```

---

## After Migration

### 1. Update App Code (Optional for now)

The app should automatically use PostgreSQL because we kept the same data structures. But eventually you'll want to:

1. Remove old `load_library_database()` function
2. Remove JSON file loading code
3. Remove Python dict definitions
4. Create dedicated PostgreSQL query modules

**Don't do this yet** - first verify everything works!

### 2. Monitor Performance

```bash
# Watch database queries
psql $DATABASE_URL -c "
  SELECT query, calls, total_time
  FROM pg_stat_statements
  WHERE query LIKE '%library_books%'
  ORDER BY total_time DESC
  LIMIT 10;
"
```

### 3. Set Up Backups

```bash
# Create backup script
cat > backup_phase3a.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="backups/postgres_$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

pg_dump $DATABASE_URL \
  --table=library_books \
  --table=library_categories \
  --table=exhibitions \
  --table=heritage_items \
  --table=meteorite_specimens \
  --table=employee_profiles \
  > $BACKUP_DIR/phase3a_backup.sql

echo "✓ Backup saved to $BACKUP_DIR"
EOF

chmod +x backup_phase3a.sh
```

---

## Rollback (If Needed)

If something goes wrong and you need to rollback:

### Option 1: Drop PostgreSQL Tables

```bash
psql $DATABASE_URL -c "
  DROP TABLE IF EXISTS library_loans CASCADE;
  DROP TABLE IF EXISTS library_books CASCADE;
  DROP TABLE IF EXISTS library_categories CASCADE;
  DROP TABLE IF EXISTS exhibition_events CASCADE;
  DROP TABLE IF EXISTS exhibition_items CASCADE;
  DROP TABLE IF EXISTS exhibitions CASCADE;
  DROP TABLE IF EXISTS heritage_items CASCADE;
  DROP TABLE IF EXISTS meteorite_specimens CASCADE;
  DROP TABLE IF EXISTS employee_profiles CASCADE;
"
```

The app will fall back to JSON files and Python dicts.

### Option 2: Restore JSON Files

```bash
# Restore from backup
cp backups/phase3a_YYYYMMDD/library_database.json data/
cp backups/phase3a_YYYYMMDD/exhibitions.json data/
cp backups/phase3a_YYYYMMDD/employee_directory.json data/

# Restart app
sudo systemctl restart museum-system
```

---

## Success Criteria

Phase 3A migration is successful when:

- ✅ All 5 databases show data from PostgreSQL
- ✅ Library shows 598 books (not demo data)
- ✅ Exhibitions show historical records
- ✅ Cultural heritage shows protected items
- ✅ Meteorites show real specimens
- ✅ Employees show 7 staff members
- ✅ No errors in application logs
- ✅ All CRUD operations work (add/edit/delete)
- ✅ Search and filtering work
- ✅ QR code generation works

---

## Files Created

### Schema:
- `db/schema_phase3a.sql` - PostgreSQL schema for all 5 databases

### Migration Scripts:
- `scripts/migrate_phase3a_library.py` - Library-specific migration
- `scripts/migrate_phase3a_all.py` - All-in-one migration script

### Runner:
- `run_phase3a_migration.sh` - Automated migration runner

### Documentation:
- `PHASE3A_MIGRATION_GUIDE.md` - This file
- `PHASE3_COMPLETE_DATABASE_MIGRATION_PLAN.md` - Overall plan
- `PHASE2_VS_PHASE3_SUMMARY.md` - Comparison summary

---

## Next Steps After Phase 3A

Once Phase 3A is complete and verified:

1. **Monitor for 1-2 days** - Make sure everything is stable
2. **Plan Phase 3B** - Medium priority databases (Exhibits, News, Research, etc.)
3. **Remove old code** - Clean up JSON loading code
4. **Optimize queries** - Add indexes as needed
5. **Set up automated backups** - Daily PostgreSQL dumps

---

## Support

If you encounter issues:

1. Check logs: `journalctl -u museum-system -n 100`
2. Verify PostgreSQL: `systemctl status postgresql`
3. Check database: `psql $DATABASE_URL -c "\dt"`
4. Test queries: `psql $DATABASE_URL -c "SELECT COUNT(*) FROM library_books"`

---

**Ready to migrate?**

```bash
cd /home/aleksandarlukovic/MuseumInfoSystem
./run_phase3a_migration.sh
```

Good luck! 🚀
