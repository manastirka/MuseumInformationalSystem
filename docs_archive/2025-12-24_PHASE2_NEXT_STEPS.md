# Phase 2 Completion - Next Steps

**Date**: December 24, 2025
**Current Status**: 75% Complete (4/6 databases migrated)
**Estimated Time to Complete**: 4-5 hours

---

## Quick Status Overview

### ✅ What's Working
- PostgreSQL infrastructure fully operational
- Bird ringing database (157,115 records) - 100% migrated
- RRUFF reference database (5,997 minerals) - 100% migrated
- Inventory book (3,970 records) - 98.5% migrated
- Minerals (2,571 records) - 98.1% migrated
- Application using PostgreSQL for main features

### ❌ What Needs to Be Done
1. **Timesheet system** - Schema incomplete, migration not run
2. **User authentication** - Not migrated to PostgreSQL
3. **Minor data quality issues** - 111 records missing from inventory/minerals

---

## Priority 1: Fix Timesheet Schema (HIGH PRIORITY)

### Problem
The `db/promote_from_staging.sql` script references tables that don't exist in `db/schema.sql`:
- `timesheet_reports`
- `timesheet_report_days`
- Related staging tables

### Solution

#### Step 1: Update schema.sql
Add these tables to `/home/aleksandarlukovic/MuseumInfoSystem/db/schema.sql`:

```sql
-- Add after timesheet_entries table

CREATE TABLE timesheet_reports (
    id SERIAL PRIMARY KEY,
    legacy_radna_lista_id INTEGER UNIQUE,
    employee_name TEXT NOT NULL,
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    year INTEGER NOT NULL,
    organization_unit TEXT,
    position TEXT,
    special_scope TEXT,
    extraordinary_tasks TEXT,
    employee_signature TEXT,
    approver TEXT,
    manager_signature TEXT,
    director_signature TEXT,
    salary_adjustment TEXT,
    duties_summary TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX timesheet_reports_employee_idx ON timesheet_reports(employee_name);
CREATE INDEX timesheet_reports_period_idx ON timesheet_reports(year, month);

CREATE TABLE timesheet_report_days (
    id SERIAL PRIMARY KEY,
    report_id INTEGER NOT NULL REFERENCES timesheet_reports(id) ON DELETE CASCADE,
    day INTEGER NOT NULL CHECK (day BETWEEN 1 AND 31),
    work_in_museum NUMERIC(4,2) DEFAULT 0,
    work_outside NUMERIC(4,2) DEFAULT 0,
    vacation NUMERIC(4,2) DEFAULT 0,
    public_holiday NUMERIC(4,2) DEFAULT 0,
    paid_leave NUMERIC(4,2) DEFAULT 0,
    other_leave NUMERIC(4,2) DEFAULT 0,
    sick_leave_lt30 NUMERIC(4,2) DEFAULT 0,
    sick_leave_gte30 NUMERIC(4,2) DEFAULT 0,
    UNIQUE(report_id, day)
);

CREATE INDEX timesheet_report_days_report_idx ON timesheet_report_days(report_id);

-- Staging tables for timesheet migration
CREATE TABLE staging_timesheet_reports (
    radna_lista_id INTEGER,
    ime_prezime TEXT,
    mesec INTEGER,
    godina INTEGER,
    organizaciona_jedinica TEXT,
    radno_mesto TEXT,
    poseban_obim_posla TEXT,
    vanredni_poslovi TEXT,
    potpis_zaposlenog TEXT,
    nalogodavac TEXT,
    potpis_sefa TEXT,
    potpis_direktora TEXT,
    povecanje_umanjenje_zarade TEXT,
    o_posao TEXT,
    created_at TEXT
);

CREATE TABLE staging_timesheet_days (
    radna_lista_id INTEGER,
    dan INTEGER,
    rad_na_mestu NUMERIC,
    van_muzeja NUMERIC,
    godisnji_odmor NUMERIC,
    drzavni_praznik NUMERIC,
    placeno_odsustvo NUMERIC,
    ostalo_odsustvo NUMERIC,
    bolovanje_manje_30 NUMERIC,
    bolovanje_vece_30 NUMERIC
);
```

#### Step 2: Apply schema update
```bash
cd /home/aleksandarlukovic/MuseumInfoSystem
psql postgresql://aleksandarlukovic@localhost:5432/museum_system -f db/schema_updates_timesheet.sql
```

#### Step 3: Verify timesheet data exists
```bash
sqlite3 localSQLtesting/museum_timesheet.db "SELECT COUNT(*) FROM radna_lista;"
sqlite3 localSQLtesting/museum_timesheet.db "SELECT COUNT(*) FROM radna_lista_dan;"
```

#### Step 4: Run migration
```bash
python scripts/migrate_to_postgres.py --dataset timesheet --batch-size 1000
```

#### Step 5: Verify migration
```bash
psql postgresql://aleksandarlukovic@localhost:5432/museum_system -c \
  "SELECT COUNT(*) FROM timesheet_reports;"
psql postgresql://aleksandarlukovic@localhost:5432/museum_system -c \
  "SELECT COUNT(*) FROM timesheet_entries;"
```

---

## Priority 2: Migrate User Authentication (HIGH PRIORITY)

### Problem
- User table in PostgreSQL is empty (0 records)
- App currently uses fallback authentication
- 7 users exist in SQLite that need migration

### Solution

#### Step 1: Check existing users in SQLite
```bash
sqlite3 localSQLtesting/museum_timesheet.db "SELECT email, password, salt, is_active FROM users;"
```

#### Step 2: Create user migration script

Create `/home/aleksandarlukovic/MuseumInfoSystem/migrate_users.py`:

```python
#!/usr/bin/env python3
"""Migrate users from SQLite to PostgreSQL"""
import os
import sqlite3
from dotenv import load_dotenv
import psycopg

load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL'].replace('postgresql+psycopg://', 'postgresql://')
SQLITE_PATH = 'localSQLtesting/museum_timesheet.db'

# Extract from SQLite
sqlite_conn = sqlite3.connect(SQLITE_PATH)
sqlite_conn.row_factory = sqlite3.Row
users = sqlite_conn.execute("SELECT * FROM users").fetchall()
sqlite_conn.close()

# Insert into PostgreSQL
with psycopg.connect(DATABASE_URL) as pg_conn:
    with pg_conn.cursor() as cur:
        # First, ensure admin role exists
        cur.execute("""
            INSERT INTO roles (name, description)
            VALUES ('admin', 'Administrator with full access')
            ON CONFLICT (name) DO NOTHING
        """)

        # Insert users
        for user in users:
            cur.execute("""
                INSERT INTO users (
                    email, password_hash, salt, full_name,
                    role_id, is_active, created_at
                )
                VALUES (
                    %s, %s, %s, %s,
                    (SELECT id FROM roles WHERE name = 'admin'),
                    %s, now()
                )
                ON CONFLICT (email) DO NOTHING
            """, (
                user['email'],
                user['password'],  # Already hashed
                user['salt'],
                user['email'].split('@')[0],  # Use email prefix as name
                user['is_active']
            ))

        pg_conn.commit()

        # Verify
        cur.execute("SELECT COUNT(*) FROM users")
        count = cur.fetchone()[0]
        print(f"✓ Migrated {count} users to PostgreSQL")
```

#### Step 3: Run user migration
```bash
python3 migrate_users.py
```

#### Step 4: Verify migration
```bash
psql postgresql://aleksandarlukovic@localhost:5432/museum_system -c \
  "SELECT email, full_name, is_active FROM users;"
```

#### Step 5: Test authentication
```bash
# Restart the application and test login
python3 app.py --port 5555
# Try logging in with existing credentials
```

---

## Priority 3: Resolve Missing Records (MEDIUM PRIORITY)

### Problem
- Inventory: 61 records missing (3,970 vs 4,031)
- Minerals: 50 records missing (2,571 vs 2,621)

### Root Cause
Records with NULL inventory numbers are excluded due to UNIQUE constraint.

### Solution

#### Option A: Allow NULL inventory numbers (Recommended)
```sql
-- Modify constraint to allow multiple NULLs
ALTER TABLE minerals DROP CONSTRAINT IF EXISTS minerals_inventory_number_key;
CREATE UNIQUE INDEX minerals_inventory_number_idx
  ON minerals(inventory_number)
  WHERE inventory_number IS NOT NULL;

ALTER TABLE inventory_entries DROP CONSTRAINT IF EXISTS inventory_entries_inventory_number_key;
CREATE UNIQUE INDEX inventory_entries_inventory_number_idx
  ON inventory_entries(inventory_number)
  WHERE inventory_number IS NOT NULL;
```

#### Option B: Generate synthetic inventory numbers
```sql
-- Add prefix for records without inventory numbers
UPDATE staging_minerals
SET inventory_number = 'UNKNOWN-' || row_number
WHERE inventory_number IS NULL OR inventory_number = '';
```

#### Re-run migration after fix
```bash
python scripts/migrate_to_postgres.py --dataset minerals --batch-size 1000
python scripts/migrate_to_postgres.py --dataset inventory --batch-size 1000
```

---

## Quick Command Reference

### Check Migration Status
```bash
# Run validation script
python3 validate_phase2_migration.py

# Check record counts
psql postgresql://aleksandarlukovic@localhost:5432/museum_system -c "
  SELECT 'bird_ringing' as db, COUNT(*) FROM bird_ringing_records
  UNION ALL SELECT 'inventory', COUNT(*) FROM inventory_entries
  UNION ALL SELECT 'minerals', COUNT(*) FROM minerals
  UNION ALL SELECT 'users', COUNT(*) FROM users
  UNION ALL SELECT 'timesheet', COUNT(*) FROM timesheet_entries;
"
```

### Restart Application with PostgreSQL
```bash
# Ensure DATABASE_URL is set
grep DATABASE_URL .env

# Start application
python3 app.py --port 5555
```

### Backup PostgreSQL Database
```bash
pg_dump postgresql://aleksandarlukovic@localhost:5432/museum_system \
  > backups/museum_system_$(date +%Y%m%d_%H%M%S).sql
```

---

## Testing Checklist

After completing migrations, test:

- [ ] User login works with PostgreSQL credentials
- [ ] Timesheet reports load and display correctly
- [ ] Bird ringing search and display
- [ ] Mineral database search and display
- [ ] Inventory book search and display
- [ ] RRUFF reference lookups
- [ ] Cross-database features (if any)
- [ ] Performance is acceptable
- [ ] No SQLite fallback warnings in logs

---

## Expected Timeline

| Task | Estimated Time | Priority |
|------|----------------|----------|
| Fix timesheet schema | 30 min | HIGH |
| Migrate timesheet data | 30 min | HIGH |
| Migrate users | 30 min | HIGH |
| Test authentication | 30 min | HIGH |
| Fix missing records | 1 hour | MEDIUM |
| Full application testing | 1 hour | MEDIUM |
| Documentation updates | 30 min | LOW |

**Total**: 4-5 hours

---

## Success Criteria

Phase 2 is complete when:

1. ✅ All 6 databases migrated (>99% data integrity)
2. ✅ No SQLite dependencies in application
3. ✅ User authentication works with PostgreSQL
4. ✅ Timesheet system fully functional
5. ✅ All tests passing
6. ✅ Documentation updated

---

## Get Help

If you encounter issues:

1. **Check logs**: `logs/museum_info_system.log`
2. **Run validation**: `python3 validate_phase2_migration.py`
3. **Check PostgreSQL**: `psql postgresql://aleksandarlukovic@localhost:5432/museum_system`
4. **Review migration scripts**: `scripts/migrate_to_postgres.py`

---

## After Phase 2 Completion

Once Phase 2 is complete, you can:

1. **Remove SQLite databases** (after backup)
2. **Optimize PostgreSQL** (indexes, vacuum, analyze)
3. **Setup automated backups**
4. **Begin Phase 3** (advanced features, API, monitoring)

---

**Let's complete Phase 2!**
Start with the timesheet schema fix - that's the biggest blocker.
