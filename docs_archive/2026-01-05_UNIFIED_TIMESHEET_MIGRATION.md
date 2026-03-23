# Unified Timesheet System Migration Plan
## Date: 2026-01-05

## Problem Identified

When users log into the main system (e.g., slavko.spasic@nhmbeo.rs) and then access the timesheet system, they see a different user (e.g., aleksandar lukovic).

### Root Cause:
- The timesheet system currently runs as a **separate application on port 5003**
- It has its own **separate session management and SQLite authentication**
- When users click "Open Timesheet System", it opens `http://localhost:5003` in a new window
- This separate app uses old SQLite sessions, causing user mismatch

## Solution

Integrate the timesheet system into the main application to use:
1. **Single authentication system** (PostgreSQL only)
2. **Unified session management** (Flask sessions from main app)
3. **Single application** (no separate port 5003)

## Implementation Steps

### Phase 1: Create Integrated Timesheet Routes ✓

Add timesheet management routes to main app.py:
- `/timesheet/create` - Create new timesheet
- `/timesheet/edit/<id>` - Edit existing timesheet
- `/timesheet/view/<id>` - View timesheet details
- `/timesheet/list` - List user's timesheets
- `/timesheet/delete/<id>` - Delete timesheet

All routes will:
- Use `@login_required` decorator
- Access user info from `session.get('user_email')` and `session.get('user_name')`
- Use PostgreSQL timesheet_reports tables
- No separate authentication needed

### Phase 2: Update Templates

Modify `templates/timesheet_integration.html`:
- Replace `window.open('http://localhost:5003')` with internal routes
- Update buttons to redirect to `/timesheet/list` instead
- Remove port 5003 references
- Keep unified session throughout

### Phase 3: Decommission Separate App

- Stop any running instance on port 5003
- Document that localSQLtesting app is deprecated
- All timesheet access through main app only

### Phase 4: Database Confirmation

- Verify PostgreSQL has all timesheet data (✓ Already migrated - 9 reports)
- SQLite has 0 records (✓ Confirmed)
- Remove SQLite dependency from timesheet access

## Benefits

✅ **Single authentication** - User logs in once, stays logged in everywhere
✅ **Consistent user identity** - No more session confusion
✅ **PostgreSQL only** - Unified database backend
✅ **Better security** - One session to manage and secure
✅ **Simpler architecture** - No multi-port complexity
✅ **Better UX** - Seamless navigation without new windows

## Current Status

- PostgreSQL timesheet tables: ✓ Exist
- Timesheet data migrated: ✓ Complete (9 reports)
- SQLite users: ✓ Deactivated
- PostgreSQL users: ✓ Active (40 users)
- Separate app running: ✗ Not running

## Next Steps

1. Implement integrated timesheet routes in app.py
2. Update timesheet_integration.html template
3. Test with admin users (admin, slavko.spasic, biljana.mitrovic, verica.stojanovic)
4. Verify session persistence and user identity
5. Document new timesheet access workflow

---

**Migration Target Date: 2026-01-05**
