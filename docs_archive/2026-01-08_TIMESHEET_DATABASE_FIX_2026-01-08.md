# Timesheet Database Column Mismatch - FIXED ✅
## Date: 2026-01-08

## Problem

The timesheet system was loading but showing error:
```
Упозорење: Грешка при учитавању података: column "work_description" does not exist
```

The queries were using incorrect column names that didn't match the actual PostgreSQL schema.

## Root Cause

**Assumed schema** (from agent implementation):
- `timesheet_entries` table with columns like `work_at_museum`, `outside_museum`, `annual_leave`, etc.
- `work_description` and `is_verified` columns in `timesheet_reports`

**Actual PostgreSQL schema**:
- `timesheet_report_days` table (not `timesheet_entries`) with columns:
  - `work_in_museum` (not `work_at_museum`)
  - `work_outside` (not `outside_museum`)
  - `vacation` (not `annual_leave`)
  - `public_holiday` (not `state_holiday`)
  - `sick_leave_lt30` (not `sick_leave_under_30`)
  - `sick_leave_gte30` (not `sick_leave_30_plus`)
- `extraordinary_tasks` and `duties_summary` (not `work_description`)
- NO `is_verified` column
- NO `employee_email` column in old records

## Solution

Fixed ALL queries in 3 routes to use correct PostgreSQL schema.

### 1. Fixed `/timesheet/entry` Route (Lines 2218-2426)

**Changed queries:**

**Header data:**
```python
# OLD (WRONG):
SELECT id, employee_name, work_description, is_verified FROM timesheet_reports

# NEW (CORRECT):
SELECT id, employee_name, extraordinary_tasks, duties_summary FROM timesheet_reports
```

**Daily data:**
```python
# OLD (WRONG):
SELECT day, work_at_museum, outside_museum, annual_leave, state_holiday,
       paid_leave, other_leave, sick_leave_under_30, sick_leave_30_plus
FROM timesheet_entries WHERE report_id = %s

# NEW (CORRECT):
SELECT day, work_in_museum, work_outside, vacation, public_holiday,
       paid_leave, other_leave, sick_leave_lt30, sick_leave_gte30
FROM timesheet_report_days WHERE report_id = %s
```

**Data mapping:**
```python
# OLD (WRONG):
'rad_na_mestu': row['work_at_museum']
'van_muzeja': row['outside_museum']
'godisnji_odmor': row['annual_leave']
'drzavni_praznik': row['state_holiday']
'bolovanje_manje_30': row['sick_leave_under_30']
'bolovanje_vece_30': row['sick_leave_30_plus']

# NEW (CORRECT):
'rad_na_mestu': row['work_in_museum']
'van_muzeja': row['work_outside']
'godisnji_odmor': row['vacation']
'drzavni_praznik': row['public_holiday']
'bolovanje_manje_30': row['sick_leave_lt30']
'bolovanje_vece_30': row['sick_leave_gte30']
```

### 2. Fixed `/api/timesheet/load` Route (Lines 2429-2492)

**Changed queries:**

**Header:**
```python
# OLD:
SELECT id, work_description FROM timesheet_reports

# NEW:
SELECT id, extraordinary_tasks, duties_summary FROM timesheet_reports
```

**Daily data:**
```python
# OLD:
FROM timesheet_entries

# NEW:
FROM timesheet_report_days
```

**Column names:** Same mappings as above

### 3. Fixed `/api/timesheet/save` Route (Lines 2495-2595)

**Check existing:**
```python
# OLD:
SELECT id, is_verified FROM timesheet_reports
if is_verified:
    # Block editing

# NEW:
SELECT id FROM timesheet_reports
# Removed is_verified check for now
```

**Update existing:**
```python
# OLD:
UPDATE timesheet_reports SET work_description = %s
DELETE FROM timesheet_entries WHERE report_id = %s

# NEW:
UPDATE timesheet_reports SET extraordinary_tasks = %s
DELETE FROM timesheet_report_days WHERE report_id = %s
```

**Create new:**
```python
# OLD:
INSERT INTO timesheet_reports
(employee_name, employee_email, month, year, work_description, is_verified, created_at, updated_at)
VALUES (%s, %s, %s, %s, %s, FALSE, NOW(), NOW())

# NEW:
INSERT INTO timesheet_reports
(employee_name, month, year, extraordinary_tasks)
VALUES (%s, %s, %s, %s)
```

**Insert daily data:**
```python
# OLD:
INSERT INTO timesheet_entries
(report_id, day, work_at_museum, outside_museum, annual_leave,
 state_holiday, paid_leave, other_leave,
 sick_leave_under_30, sick_leave_30_plus)

# NEW:
INSERT INTO timesheet_report_days
(report_id, day, work_in_museum, work_outside, vacation,
 public_holiday, paid_leave, other_leave,
 sick_leave_lt30, sick_leave_gte30)
```

## Actual PostgreSQL Schema

### timesheet_reports Table
```sql
Column                | Type      | Description
----------------------|-----------|-------------
id                    | integer   | Primary key
legacy_radna_lista_id | integer   | Old MySQL ID reference
employee_name         | text      | Full name with titles
month                 | integer   | 1-12
year                  | integer   | Year
organization_unit     | text      | Department
position              | text      | Job title
special_scope         | text      | Special assignments
extraordinary_tasks   | text      | Work description (OPosao)
duties_summary        | text      | Summary of duties
employee_signature    | text      | Signature
approver              | text      | Approver name
manager_signature     | text      | Manager signature
director_signature    | text      | Director signature
salary_adjustment     | text      | Salary notes
created_at            | timestamp | Creation time
```

### timesheet_report_days Table
```sql
Column          | Type         | Description
----------------|--------------|-------------
id              | integer      | Primary key
report_id       | integer      | FK to timesheet_reports
day             | integer      | 1-31
work_in_museum  | numeric(4,2) | Hours at museum
work_outside    | numeric(4,2) | Hours outside
vacation        | numeric(4,2) | Vacation hours
public_holiday  | numeric(4,2) | Holiday hours
paid_leave      | numeric(4,2) | Paid leave hours
other_leave     | numeric(4,2) | Other leave hours
sick_leave_lt30 | numeric(4,2) | Sick leave < 30 days
sick_leave_gte30| numeric(4,2) | Sick leave >= 30 days
```

### timesheet_entries Table (Normalized View)
```sql
Column      | Type         | Description
------------|--------------|-------------
id          | integer      | Primary key
report_id   | integer      | FK to timesheet_reports
category    | text         | Category name
hours       | numeric(6,2) | Total hours for category
created_at  | timestamp    | Creation time

Categories: rad_na_mestu, van_muzeja, godisnji_odmor, drzavni_praznik,
           placeno_odsustvo, ostalo_odsustvo, bolovanje_manje_30, bolovanje_vece_30
```

**Note:** `timesheet_entries` is auto-synced from `timesheet_report_days` via trigger.

## Column Mapping Reference

| Template Variable | PostgreSQL Column (timesheet_report_days) |
|-------------------|-------------------------------------------|
| `rad_na_mestu` | `work_in_museum` |
| `van_muzeja` | `work_outside` |
| `godisnji_odmor` | `vacation` |
| `drzavni_praznik` | `public_holiday` |
| `placeno_odsustvo` | `paid_leave` |
| `ostalo_odsustvo` | `other_leave` |
| `bolovanje_manje_30` | `sick_leave_lt30` |
| `bolovanje_vece_30` | `sick_leave_gte30` |
| `OPosao` | `extraordinary_tasks` or `duties_summary` |

## Files Modified

- `app.py` - Fixed 3 routes with correct column names
  - Line 2289: timesheet_entry SELECT header
  - Line 2297: timesheet_entry SELECT header (fallback)
  - Line 2304-2309: timesheet_entry SELECT daily data
  - Line 2315-2325: Daily data mapping
  - Line 2330: Work description mapping
  - Line 2453: api_load SELECT header
  - Line 2462-2467: api_load SELECT daily data
  - Line 2474-2481: api_load data mapping
  - Line 2527: api_save SELECT existing
  - Line 2537: api_save UPDATE header
  - Line 2540: api_save DELETE daily data
  - Line 2544-2548: api_save INSERT new report
  - Line 2575-2579: api_save INSERT daily data

## Testing

### Test 1: Load Timesheet Entry Page ✅
```
URL: http://localhost:5555/timesheet/entry
Expected: No database errors, calendar loads
Result: SUCCESS - Page loads without "work_description" error
```

### Test 2: Load Existing Data ✅
```
Action: Navigate to existing timesheet month
Expected: Daily data loads from timesheet_report_days
Result: SUCCESS - Data loads correctly
```

### Test 3: Save New Timesheet ✅
```
Action: Enter data and click "Сачувај измене"
Expected: Saves to timesheet_report_days table
Result: SUCCESS - Data saved correctly
```

### Test 4: Update Existing Timesheet ✅
```
Action: Modify existing data and save
Expected: Updates timesheet_report_days
Result: SUCCESS - Updates correctly
```

## Status

✅ **FIXED** - All database column mismatches corrected
✅ **TESTED** - All queries now use correct schema
✅ **DEPLOYED** - Museum system restarted successfully
✅ **VERIFIED** - No errors in service logs

## Next Steps (Optional)

1. **Approval System**
   - Add approval tracking (maybe new column or separate table)
   - Implement approval workflow UI
   - Add email notifications

2. **User Department/Position Loading**
   - Currently shows "Није дефинисано" (Not defined)
   - Need to query from employee_profiles or users table
   - Add organization_unit and position to query

3. **Work Description Fields**
   - Map both `extraordinary_tasks` and `duties_summary`
   - Decide which field is primary
   - Maybe merge into single display

---

**Fixed by:** Claude (Agent)
**Date:** 2026-01-08 09:53
**Service restarted:** ✅
**Status:** Production Ready
**Error:** ❌ RESOLVED
