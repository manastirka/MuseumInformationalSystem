# Timesheet System - Quick Start Guide
## Updated: 2026-01-05

## ✅ What Changed?

The timesheet system is now **fully integrated** into the main application.

**Before:** Separate app on port 5003 with its own login
**Now:** Unified system with single login

---

## How to Access Timesheets

### 1. Login Once
```
URL: http://localhost:5555/login

Admin Users:
- admin / admin123
- slavko.spasic@nhmbeo.rs / user
- biljana.mitrovic@nhmbeo.rs / user
- verica.stojanovic@nhmbeo.rs / user

Employees:
- [their-email]@nhmbeo.rs / user
```

### 2. Navigate to Timesheets
```
Dashboard → Систем за радне листе
```

### 3. View Reports
```
Click: "Преглед радних листи"
You'll see all timesheet reports with filtering options
```

---

## Current User Identity

When you access the timesheet system, you'll see:

```
Већ сте пријављени као: [Your Name]
[your.email@nhmbeo.rs]
```

This confirms your identity is preserved throughout the application.

---

## Key Features

✅ **Single Login** - Log in once, access everything
✅ **User Consistency** - Your identity never changes
✅ **No Port 5003** - Everything on main port 5555
✅ **PostgreSQL Data** - All data in one database
✅ **Seamless Navigation** - No new windows/tabs

---

## Available Reports

Current timesheet data in system:
- **9 reports** from **3 employees**
- All stored in PostgreSQL
- Accessible through integrated interface

---

## For Admins Only

### Admin Features:
- View all employee timesheets
- Filter by month, year, employee
- Access detailed report breakdowns
- View summary statistics

### Admin Routes:
- `/timesheet` - Timesheet overview
- `/admin/timesheet_reports` - All reports
- `/admin/timesheet_reports/<id>` - Report details

---

## Troubleshooting

### "I see a different user"
**Solution:** This should no longer happen! If it does:
1. Log out completely
2. Clear browser cache
3. Log in again
4. Contact admin if issue persists

### "Can't access timesheets"
**Solution:** Verify you're logged in and have permissions:
1. Check you see your name on dashboard
2. Verify "Систем за радне листе" module is visible
3. Contact admin to verify your role

### "No data showing"
**Solution:** Confirm PostgreSQL is running:
```bash
systemctl status postgresql
```

---

## What's Deprecated

❌ **Do NOT use:**
- Port 5003 (no longer exists)
- Separate timesheet login
- localSQLtesting standalone app
- SQLite timesheet database

✅ **USE instead:**
- Main application (port 5555)
- Unified login
- Integrated timesheet routes
- PostgreSQL database

---

## Quick Reference

| Task | Action |
|------|--------|
| Login | Go to http://localhost:5555/login |
| View Timesheets | Dashboard → Систем за радне листе → Преглед радних листи |
| Check Your Identity | Look for "Већ сте пријављени као: [Your Name]" |
| Access Admin | Login with admin credentials, access admin panel |

---

## Need Help?

1. Check your login credentials
2. Verify you're on port 5555 (not 5003)
3. Confirm your user is active in PostgreSQL
4. Review logs: `/home/aleksandarlukovic/MuseumInfoSystem/logs/`
5. Contact system administrator

---

**System Status:** ✅ Operational
**Database:** PostgreSQL (unified)
**Authentication:** Single sign-on
**Session:** Persistent across modules

---

**Last Updated: 2026-01-05**
