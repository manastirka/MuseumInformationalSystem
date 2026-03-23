# Museum Control Center - PostgreSQL Integration

**Date**: December 25, 2025
**Status**: ✅ Complete

---

## Summary

The Museum Control Center has been updated to include full PostgreSQL service management. You can now start, stop, restart, and monitor PostgreSQL directly from the GUI, as well as enable automatic startup.

---

## What's New

### 1. PostgreSQL Service in Services Tab

PostgreSQL is now listed as the **first service** in the control center with:

- **Icon**: 🐘 (PostgreSQL elephant)
- **Name**: PostgreSQL База података
- **Port**: 5432
- **Service Type**: systemd (postgresql)
- **Order**: 1 (starts first when using "Start All Services")

### 2. Service Control Features

You can now:

- ✅ **Start PostgreSQL** - Start the PostgreSQL service
- ✅ **Stop PostgreSQL** - Stop the PostgreSQL service
- ✅ **Restart PostgreSQL** - Restart the PostgreSQL service
- ✅ **View Logs** - View PostgreSQL logs via journalctl
- ✅ **Auto Status** - Real-time status updates every 2 seconds

### 3. Enhanced Database Tab

The "Базе података" (Databases) tab now includes:

#### New Button: 🐘 Омогући PostgreSQL ауто-старт

This button performs the complete PostgreSQL auto-start setup:

**What it does:**
1. Enables PostgreSQL to start on system boot
2. Starts PostgreSQL now
3. Backs up museum-system.service
4. Updates museum-system.service with PostgreSQL dependency
5. Reloads systemd configuration
6. Restarts museum system
7. Verifies everything is working

**Service Configuration Applied:**
```ini
[Unit]
Description=Museum Information System - Gunicorn
After=network.target postgresql.service
Requires=postgresql.service
Wants=postgresql.service
```

#### Enhanced Status Check

The "📊 Провери статус база података" button now shows:

**For PostgreSQL:**
- ✅ Service status (Active/Inactive)
- ✅ PostgreSQL version
- ✅ Database size
- ✅ Record counts for all tables:
  - bird_ringing records
  - minerals
  - inventory entries
  - users
- ✅ Auto-start status (Enabled/Disabled)

**For SQLite (Legacy):**
- ⚠️ Marked as "Застарело - само за fallback"
- Shows that SQLite is only used when PostgreSQL is inactive

---

## How to Use

### Option 1: Quick Setup (Recommended)

1. **Launch Museum Control Center**
   ```bash
   cd /home/aleksandarlukovic/MuseumInfoSystem
   python3 museum_control_center.py
   ```

2. **Go to "Базе података" tab**

3. **Click "🐘 Омогући PostgreSQL ауто-старт"**
   - Enter your sudo password when prompted
   - Wait for all steps to complete
   - Verify success message

4. **Done!** PostgreSQL is now auto-starting

### Option 2: Manual Service Control

1. **Go to "Сервиси" tab**

2. **Find "🐘 PostgreSQL База података"** (first in the list)

3. **Click "▶️ Покрени"** to start PostgreSQL
   - Enter sudo password
   - Wait for confirmation

4. **Monitor Status**
   - Status updates automatically every 2 seconds
   - Green 🟢 = Running
   - Red 🔴 = Stopped

### Option 3: Start All Services in Correct Order

1. **Click "🚀 Покрени све сервисе"** at the bottom

Services will start in this order:
1. **PostgreSQL** (order: 1) - Database first
2. **Museum System** (order: 2) - Application second
3. **Nginx** (order: 3) - Web server last

---

## Service Startup Order

The control center now respects service dependencies:

```
System Boot
    ↓
🐘 PostgreSQL (order: 1)
    ↓
🏛️ Museum System (order: 2)
    ↓
🌐 Nginx (order: 3)
    ↓
System Ready
```

This ensures:
- Database is available before app starts
- App is running before web server starts
- Proper dependency chain

---

## Log Viewing

PostgreSQL logs are now available in the "Логови" tab:

1. **Go to "Логови" tab**
2. **Select "postgresql"** from dropdown
3. **Click "🔄 Освежи"** to view logs
4. **Enable "Аутоматско освежавање"** for live logs

Logs are retrieved using `journalctl -u postgresql -n 500`

---

## Verification

### Check PostgreSQL Status

**In Control Center:**
1. Go to "Базе података" tab
2. Click "📊 Провери статус база података"
3. Look for:
   ```
   🐘 PostgreSQL (Главна база података - Phase 2):
      ✅ Сервис: Активан
      ✅ Верзија: PostgreSQL 16.x
      ✅ Величина базе: XX MB
      📊 Број записа:
         • bird_ringing: 157115
         • minerals: 2571
         • inventory: 3970
         • users: 7
      ✅ Аутоматски старт: Омогућен
   ```

**In Services Tab:**
- PostgreSQL status should show: `● Статус: 🟢 Активан`

**In System:**
```bash
systemctl status postgresql
systemctl is-enabled postgresql  # Should show "enabled"
```

### Check Museum System Using PostgreSQL

**Look at museum system logs:**
1. Go to "Логови" tab
2. Select "museum_system"
3. Look for these lines:
   ```
   ✓ Using PostgreSQL for mineral database
   ✓ Using PostgreSQL authentication
   INFO - PostgresAuth: Connected successfully (7 users)
   ```

**NOT these (fallback mode):**
   ```
   ⚠️ Using SQLite for mineral database
   ⚠️ Using fallback authentication
   ```

---

## Troubleshooting

### PostgreSQL Won't Start

**Check from Control Center:**
1. Go to "Сервиси" tab
2. Try to start PostgreSQL
3. If it fails, click "📋 Логови" to see error

**Common fixes:**
```bash
# Initialize database (if first time)
sudo postgresql-setup --initdb --unit postgresql

# Check if port is in use
sudo ss -tlnp | grep 5432

# Check PostgreSQL logs
sudo journalctl -u postgresql -n 50
```

### Museum System Still Using SQLite

**Verify in Control Center:**
1. "Базе података" tab → "📊 Провери статус"
2. Check if PostgreSQL shows "Аутоматски старт: Онемогућен"
3. Click "🐘 Омогући PostgreSQL ауто-старт"

**Or manually:**
```bash
# Check DATABASE_URL is set
cat /home/aleksandarlukovic/MuseumInfoSystem/.env | grep DATABASE_URL

# Should show:
DATABASE_URL=postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system
```

### Auto-Start Button Fails

**Possible issues:**
1. **Wrong password** - Click "🔑 Ресетуј лозинку" and try again
2. **Service file missing** - Run install services first
3. **PostgreSQL not installed** - Install PostgreSQL 16

**Check error messages in the database status text area**

---

## Files Modified

### Updated
- **museum_control_center.py** - Added PostgreSQL support
  - Added `postgresql` service to services dict
  - Added `enable_postgresql_autostart()` function
  - Updated `check_database_status()` function
  - Updated `start_all_services()` to respect order
  - Updated log viewer to include PostgreSQL

### Created
- **MUSEUM_CONTROL_CENTER_POSTGRESQL.md** - This documentation

### Not Modified
- No changes to systemd files (done via control center)
- No changes to app.py
- No changes to database schema

---

## Benefits

### Before Update

- ❌ No PostgreSQL control from GUI
- ❌ Manual terminal commands required
- ❌ No visibility into PostgreSQL status
- ❌ No easy way to enable auto-start
- ❌ No service dependency management

### After Update

- ✅ Full PostgreSQL control from GUI
- ✅ One-click auto-start setup
- ✅ Real-time status monitoring
- ✅ Comprehensive database status
- ✅ Proper service dependency chain
- ✅ Live log viewing
- ✅ User-friendly interface

---

## Integration with Phase 2 Migration

This control center update **completes Phase 2** by providing:

1. **Easy PostgreSQL management** - Start/stop/restart from GUI
2. **Auto-start configuration** - One-click setup
3. **Status monitoring** - Real-time database status
4. **Service dependencies** - Ensures correct startup order
5. **User-friendly** - No need for terminal commands

Combined with the Phase 2 migration, you now have:
- ✅ All data migrated to PostgreSQL
- ✅ PostgreSQL auto-start configured
- ✅ Museum system using PostgreSQL
- ✅ GUI control center for management
- ✅ Complete monitoring and logging

---

## Quick Reference

### Common Actions

| Action | Steps |
|--------|-------|
| Enable auto-start | Базе података → 🐘 Омогући PostgreSQL ауто-старт |
| Start PostgreSQL | Сервиси → PostgreSQL → ▶️ Покрени |
| Check status | Базе података → 📊 Провери статус |
| View logs | Логови → Select "postgresql" → 🔄 Освежи |
| Start all services | Bottom → 🚀 Покрени све сервисе |
| Restart everything | Bottom → 🔄 Рестартуј све |

### Keyboard Shortcuts

- **Alt+Tab** - Switch between tabs
- **Enter** - Activate focused button
- **Esc** - Close dialog boxes

### Service Order

1. **PostgreSQL** (🐘) - Database layer
2. **Museum System** (🏛️) - Application layer
3. **Nginx** (🌐) - Web server layer

---

## Next Steps

After setting up PostgreSQL in the control center:

1. ✅ **Test the setup** - Reboot your system and verify everything starts automatically

2. ✅ **Access the museum system** - Go to http://localhost or http://192.168.144.48

3. ✅ **Login and verify** - Use admin/admin123 and check that databases work

4. ✅ **Change admin password** - Login → Change Password

5. ✅ **Monitor regularly** - Use control center to check status

---

## Support

If you encounter issues:

1. **Check logs in control center** - "Логови" tab
2. **Check database status** - "Базе података" tab
3. **Try restart** - Use "🔄 Рестарт" buttons
4. **Reset password cache** - Click "🔑 Ресетуј лозинку"
5. **Check systemd directly** - `systemctl status postgresql`

---

**Documentation Created**: December 25, 2025
**Version**: 1.0
**Status**: ✅ Production Ready
