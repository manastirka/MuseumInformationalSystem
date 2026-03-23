# Full Timesheet System Integration - 2026-01-08

## Implementation Plan

### Phase 1: Core Functionality (IMPLEMENTING NOW)
1. ✅ Create `/timesheet/entry` route with full calendar interface
2. ✅ Implement PostgreSQL queries (migrated from MySQL)
3. ✅ Add `/api/timesheet/load` - AJAX data loading
4. ✅ Add `/api/timesheet/save` - AJAX data saving
5. ✅ Copy and adapt employee_timesheet.html template
6. ✅ Serbian holidays integration
7. ✅ Weekend/holiday coloring
8. ✅ 8 work categories
9. ✅ Auto-calculation of totals

### Phase 2: Advanced Features (NEXT)
10. ⏳ Word export functionality
11. ⏳ Admin approval workflow
12. ⏳ Edit restriction logic (1st-7th of month)
13. ⏳ Analytics dashboard

### Phase 3: Polish & Testing
14. ⏳ Styling to match main app
15. ⏳ Comprehensive testing
16. ⏳ Bug fixes

## Key Changes from localSQLtesting

### Database Migration: MySQL → PostgreSQL

**MySQL (Old):**
```python
cursor.execute("SELECT ... FROM radna_lista WHERE ...")
```

**PostgreSQL (New):**
```python
cursor.execute(text("SELECT ... FROM timesheet_reports WHERE ..."))
```

### Table Mappings:
- `radna_lista` → `timesheet_reports`
- `radna_lista_dan` → `timesheet_entries`
- `radna_lista_id` → `id`
- `mesec`/`godina` → `month`/`year`
- `ime_prezime` → `employee_name`
- `OPosao` → (stored in JSON or text field)
- `IsVerify` → `is_approved`

### Authentication Integration

**Old System:**
```python
if 'user_id' not in session:
    return redirect(url_for('login'))
user_full_name = session['full_name']
```

**New System:**
```python
@app.route('/timesheet/entry')
@login_required  # Uses main app decorator
def timesheet_entry():
    user_name = session.get('user_name')
    user_email = session.get('user_email')
```

## Files to Create/Modify

### 1. app.py - Add Routes
```python
@app.route('/timesheet/entry')
@login_required
def timesheet_entry():
    # Full implementation with PostgreSQL

@app.route('/api/timesheet/load')
@login_required
def api_timesheet_load():
    # AJAX load from PostgreSQL

@app.route('/api/timesheet/save', methods=['POST'])
@login_required
def api_timesheet_save():
    # AJAX save to PostgreSQL
```

### 2. templates/employee_timesheet.html
- Copy from localSQLtesting
- Adapt for main app layout (extend base.html)
- Update all references to work with PostgreSQL schema
- Integrate with main app session variables

### 3. serbian_holidays.py (Already exists)
- Use existing implementation
- No changes needed

## PostgreSQL Schema Usage

### timesheet_reports (Header Data)
```sql
CREATE TABLE timesheet_reports (
    id SERIAL PRIMARY KEY,
    employee_name VARCHAR(255),
    employee_email VARCHAR(255),
    month INTEGER,
    year INTEGER,
    organization_unit VARCHAR(255),
    position VARCHAR(255),
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### timesheet_entries (Daily Data)
```sql
CREATE TABLE timesheet_entries (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES timesheet_reports(id),
    day INTEGER,
    category VARCHAR(50),
    hours DECIMAL(4,2),
    created_at TIMESTAMP
);
```

## Implementation Status

### Completed ✅
- [x] Research existing system
- [x] Understand PostgreSQL schema
- [x] Plan migration strategy
- [x] Create documentation

### In Progress 🔄
- [ ] Create `/timesheet/entry` route
- [ ] Implement PostgreSQL queries
- [ ] Add API endpoints
- [ ] Copy/adapt template

### Pending ⏳
- [ ] Word export
- [ ] Approval workflow
- [ ] Testing
- [ ] Bug fixes

## Timeline

- **Phase 1** (NOW): 2 hours - Core functional entry system
- **Phase 2** (LATER): 2 hours - Advanced features
- **Phase 3** (FINAL): 1 hour - Polish & test

**Total: ~5 hours for complete replication**

## Notes

- Using existing PostgreSQL tables from Phase 2 migration
- Main app authentication already integrated
- Serbian holidays module ready to use
- Template needs adaptation but core structure preserved
- All queries adapted for PostgreSQL syntax

Starting implementation NOW...
