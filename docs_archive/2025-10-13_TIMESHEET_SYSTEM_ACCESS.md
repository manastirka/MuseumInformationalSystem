# Timesheet System Access Guide

## Current Status: ✅ WORKING

The timesheet system (radnih lista) is **working correctly** but runs as a **separate application** on port 5003.

## How to Access

### From Main Museum System (Port 5000)

1. **Login** to main system at `http://localhost:5000/login`
2. Go to **Dashboard**
3. Click on **"Систем за радне листе"** (Timesheet System) widget
4. You'll see an integration page with two buttons:
   - **"Отвори систем радних листи"** - Opens user timesheet interface
   - **"Администрација"** - Opens admin panel

### Direct Access URLs

If you prefer direct access without going through the main system:

- **User Interface**: `http://localhost:5003`
- **Admin Panel**: `http://localhost:5003/admin`

## System Architecture

```
Main Museum System (Port 5000)
    ↓
Dashboard → Timesheet Integration Page
    ↓
Opens in new tab/window → Timesheet System (Port 5003)
```

The timesheet system is **intentionally separate** for the following reasons:
1. Independent functionality
2. Can run on different server if needed
3. Separate authentication/session management
4. Better performance isolation

## Troubleshooting

### Issue: "Timesheet admin won't work"

**Solution**: The timesheet admin is accessed through the **separate timesheet application** on port 5003, not through the main app's admin panel.

Access it at: `http://localhost:5003/admin`

### Check if Timesheet System is Running

```bash
# Run the status check script
./check_status.sh

# Or manually check port 5003
netstat -tuln | grep 5003
# or
ss -tuln | grep 5003
```

### Start Timesheet System if Not Running

The timesheet system should be running separately. It's currently running from:
```
/home/aleksandarlukovic/Mesečni_app/localSQLtesting/
```

## Port Summary

| Service | Port | Purpose |
|---------|------|---------|
| **Main Museum System** | 5000 | Central dashboard, authentication, databases |
| **Mineral Database** | 5001 | Mineral collection management |
| **Timesheet System** | 5003 | Employee work timesheets (separate app) |

## Integration Features

The integration page at `/timesheet` provides:
- ✅ Status checking for timesheet system
- ✅ Direct links to open timesheet system
- ✅ Instructions for users and admins
- ✅ System startup functionality (if not running)

## Login Credentials

### Main System (Port 5000)
- Admin: `admin` / `admin123`
- Employees: Use museum email address / `user`

### Timesheet System (Port 5003)
- Uses the **same authentication** as main system
- Employee database is shared

## Notes

- The timesheet system integration is by design - it's not broken
- The `/timesheet/admin` route doesn't exist because admin functions are on port 5003
- The integration page serves as a convenient launcher and status monitor
- For full timesheet functionality, use the application on port 5003 directly

## Future Improvements

Possible enhancements (not currently needed):
- Embed timesheet system in iframe (less secure, more complex)
- Proxy requests through main app (adds latency)
- Full integration into main codebase (loses modularity)

**Current setup is intentional and working as designed!**
