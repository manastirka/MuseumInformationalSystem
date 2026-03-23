# PostgreSQL Auto-Start Configuration

**Date**: December 25, 2025
**Purpose**: Ensure PostgreSQL starts automatically before the museum system

---

## Current Problem

The museum system has been successfully migrated to PostgreSQL, but PostgreSQL is not starting automatically. This causes the app to fall back to SQLite databases.

**Symptoms**:
```
○ PostgreSQL: inactive (dead)
⚠️ Using fallback authentication
⚠️ PostgreSQL bird ringing backend disabled: connection refused
ERROR - Failed to connect to PostgreSQL mineral database
```

---

## Solution Overview

Configure PostgreSQL to:
1. **Start on boot** - Enable PostgreSQL service
2. **Start before museum app** - Add service dependency
3. **Ensure museum app waits** - Add `Requires` and `After` directives

---

## What Will Be Changed

### 1. PostgreSQL Service
```bash
# Enable PostgreSQL to start on system boot
sudo systemctl enable postgresql

# Start PostgreSQL now
sudo systemctl start postgresql
```

### 2. Museum System Service File

**File**: `/etc/systemd/system/museum-system.service`

**Current Configuration**:
```ini
[Unit]
Description=Museum Information System - Gunicorn
After=network.target
```

**New Configuration**:
```ini
[Unit]
Description=Museum Information System - Gunicorn
After=network.target postgresql.service
Requires=postgresql.service
Wants=postgresql.service
```

**What This Does**:
- `After=postgresql.service` - Museum app starts AFTER PostgreSQL is ready
- `Requires=postgresql.service` - Museum app REQUIRES PostgreSQL to be running
- `Wants=postgresql.service` - Museum app wants PostgreSQL to start with it

---

## How to Apply

### Option 1: Automatic (Recommended)

Run the provided script:

```bash
cd /home/aleksandarlukovic/MuseumInfoSystem
./enable_postgres_autostart.sh
```

This script will:
- ✅ Enable PostgreSQL auto-start
- ✅ Start PostgreSQL now
- ✅ Backup current service file
- ✅ Update museum-system.service with PostgreSQL dependency
- ✅ Reload systemd
- ✅ Restart museum system
- ✅ Verify everything is working

### Option 2: Manual

If you prefer to do it manually:

```bash
# 1. Enable and start PostgreSQL
sudo systemctl enable postgresql
sudo systemctl start postgresql
sudo systemctl status postgresql

# 2. Backup current service file
sudo cp /etc/systemd/system/museum-system.service \
     /etc/systemd/system/museum-system.service.backup

# 3. Edit service file
sudo nano /etc/systemd/system/museum-system.service

# Add these lines in the [Unit] section:
After=network.target postgresql.service
Requires=postgresql.service
Wants=postgresql.service

# 4. Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart museum-system.service

# 5. Verify
systemctl status postgresql
systemctl status museum-system.service
```

---

## Verification

After running the setup, verify PostgreSQL is being used:

### 1. Check Services Are Running
```bash
systemctl status postgresql
# Should show: Active: active (running)

systemctl status museum-system.service
# Should show: Active: active (running)
```

### 2. Check Application Logs
```bash
journalctl -u museum-system.service -n 50 | grep -i "postgresql\|using"
```

**Expected Output**:
```
✓ Using PostgreSQL for mineral database
✓ Using PostgreSQL authentication
INFO - PostgresAuth: Connected successfully (7 users)
INFO - Timesheet repository connected to PostgreSQL
```

**NOT Expected** (these indicate fallback to SQLite):
```
⚠️ Using SQLite for mineral database
⚠️ Using fallback authentication
⚠️ PostgreSQL bird ringing backend disabled
```

### 3. Test Database Connection
```bash
# Connect to PostgreSQL
psql postgresql://aleksandarlukovic@localhost:5432/museum_system

# In psql, check tables:
\dt

# Check record counts:
SELECT 'bird_ringing' as table, COUNT(*) FROM bird_ringing_records
UNION ALL SELECT 'minerals', COUNT(*) FROM minerals
UNION ALL SELECT 'users', COUNT(*) FROM users;

# Exit:
\q
```

### 4. Test Museum App
```bash
# Navigate to the museum app
http://localhost:5555/login

# Login with:
Username: admin
Password: admin123

# Check that databases are accessible
```

---

## Benefits of This Setup

### Before (Current State)
- ❌ PostgreSQL not starting automatically
- ❌ Museum app uses SQLite fallback
- ❌ Manual intervention required after reboot
- ❌ Phase 2 migration not being utilized

### After (New State)
- ✅ PostgreSQL starts automatically on boot
- ✅ Museum app uses PostgreSQL (all migrated data)
- ✅ No manual intervention needed
- ✅ Full benefit of Phase 2 migration
- ✅ Proper service dependency management

---

## Service Dependency Chain

With the new configuration:

```
System Boot
    ↓
network.target (networking ready)
    ↓
postgresql.service (PostgreSQL starts)
    ↓
museum-system.service (Museum app starts)
```

If PostgreSQL fails to start, the museum system will:
- Wait for PostgreSQL to become available
- Retry automatically (due to `Restart=always` in service)
- Log the dependency issue in systemd journal

---

## Troubleshooting

### PostgreSQL Won't Start

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check PostgreSQL logs
sudo journalctl -u postgresql -n 50

# Check if PostgreSQL is listening
sudo ss -tlnp | grep 5432

# Try initializing database (if needed)
sudo postgresql-setup --initdb --unit postgresql
```

### Museum System Still Using SQLite

```bash
# Check if DATABASE_URL is set
grep DATABASE_URL /home/aleksandarlukovic/MuseumInfoSystem/.env

# Should show:
DATABASE_URL=postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system

# If missing, add it to .env
echo "DATABASE_URL=postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system" >> .env

# Restart museum system
sudo systemctl restart museum-system.service
```

### Dependency Not Working

```bash
# Check service dependencies
systemctl list-dependencies museum-system.service

# Should show postgresql.service in the tree

# If not, reload systemd
sudo systemctl daemon-reload
```

---

## Rollback (If Needed)

If something goes wrong:

```bash
# 1. Stop services
sudo systemctl stop museum-system.service

# 2. Restore backup
sudo cp /etc/systemd/system/museum-system.service.backup \
     /etc/systemd/system/museum-system.service

# 3. Reload and restart
sudo systemctl daemon-reload
sudo systemctl start museum-system.service

# App will work with SQLite (fallback mode)
```

---

## Files Modified

### Created
- `enable_postgres_autostart.sh` - Automated setup script
- `POSTGRES_AUTOSTART_SETUP.md` - This documentation

### Backed Up
- `/etc/systemd/system/museum-system.service.backup` - Original service file

### Modified
- `/etc/systemd/system/museum-system.service` - Updated with PostgreSQL dependency

---

## Next Steps After Setup

Once PostgreSQL auto-start is configured:

1. **Test Reboot Behavior**
   ```bash
   sudo reboot
   # After reboot, check:
   systemctl status postgresql
   systemctl status museum-system.service
   ```

2. **Change Default Admin Password**
   - Login: http://localhost:5555/login
   - Username: admin, Password: admin123
   - Go to profile → Change Password

3. **Monitor Performance**
   - Check query performance
   - Monitor PostgreSQL logs
   - Verify data integrity

4. **Setup Backups**
   ```bash
   # Create backup script
   pg_dump postgresql://aleksandarlukovic@localhost:5432/museum_system \
     > backups/museum_system_$(date +%Y%m%d).sql
   ```

5. **Consider Phase 3 Enhancements**
   - Advanced PostgreSQL features
   - Replication for high availability
   - Performance tuning
   - Full-text search

---

## Summary

This setup ensures that:
- PostgreSQL is always running when needed
- Museum system automatically uses PostgreSQL (not SQLite)
- All Phase 2 migration work is utilized
- System behaves correctly after reboots
- Proper service management is in place

**Run the script now to complete the setup!**

```bash
cd /home/aleksandarlukovic/MuseumInfoSystem
./enable_postgres_autostart.sh
```

---

**Documentation Created**: December 25, 2025
**Script**: `enable_postgres_autostart.sh`
**Status**: Ready to deploy
