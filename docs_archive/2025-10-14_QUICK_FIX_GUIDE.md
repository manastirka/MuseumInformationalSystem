# Quick Fix Guide - Nginx & Gunicorn Issues

## Problems Identified

### 1. Gunicorn Won't Start from Control Center
**Cause**: The `museum-system.service` file was never installed to `/etc/systemd/system/`

**Symptom**: Control center shows error when trying to start museum_system service

### 2. Remote Machines Only See Timesheet (Radne Liste)
**Cause**: Multiple conflicting nginx configurations in `/etc/nginx/conf.d/`:
- `museum-timesheet.conf` - Redirects all port 80 traffic to HTTPS and serves timesheet
- `museum-app.conf` - Also tries to serve on port 80, conflicts with timesheet config
- Both configs point to port 5003 (timesheet) instead of the main museum app

**Symptom**: When accessing http://192.168.144.48 from LAN, only timesheet system appears

## The Fix

### Automated Fix (Recommended)

Run the fix script:

```bash
sudo bash fix_nginx_gunicorn.sh
```

This script will:
1. Backup old nginx configurations to `/etc/nginx/conf.d/backup/`
2. Install the new nginx configuration (`museum-system.conf`)
3. Install the systemd service file for gunicorn
4. Reload systemd and nginx
5. Start the museum-system service
6. Verify everything is working

### Manual Fix (If Needed)

If you prefer to fix manually:

#### Step 1: Install Systemd Service
```bash
sudo cp museum-system.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable museum-system
```

#### Step 2: Fix Nginx Configuration
```bash
# Backup old configs
sudo mkdir -p /etc/nginx/conf.d/backup
sudo mv /etc/nginx/conf.d/museum-*.conf /etc/nginx/conf.d/backup/

# Install new config
sudo cp nginx_museum.conf /etc/nginx/conf.d/museum-system.conf

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

#### Step 3: Start Gunicorn
```bash
sudo systemctl start museum-system
sudo systemctl status museum-system
```

## Verification

After running the fix:

### 1. Check Services
```bash
# Check gunicorn
sudo systemctl status museum-system

# Check nginx
sudo systemctl status nginx

# Check socket file
ls -la /tmp/museum_info_system.sock
```

### 2. Test Access

**Local machine**:
```bash
curl http://localhost
```

**From LAN**: Open browser to http://192.168.144.48

You should now see the full Museum Information System, not just the timesheet.

### 3. Control Center

Open the Museum Control Center:
```bash
python3 museum_control_center.py
```

You should now be able to:
- See nginx and museum_system services
- Start/stop both services
- View logs via journalctl

## Architecture After Fix

```
Browser (LAN) → http://192.168.144.48:80
                     ↓
                   Nginx
                     ↓
        Unix Socket: /tmp/museum_info_system.sock
                     ↓
                  Gunicorn (4 workers)
                     ↓
           Flask Museum Application
```

## Troubleshooting

### Gunicorn Won't Start

Check logs:
```bash
sudo journalctl -u museum-system -n 50
```

Common issues:
- Socket permission denied: `sudo chmod 755 /tmp`
- Python path wrong: Check ExecStart in service file
- Module not found: `pip3 install --user -r requirements.txt`

### Still Seeing Only Timesheet

Check what's serving port 80:
```bash
sudo ss -tlnp | grep :80
curl -I http://localhost
```

Check nginx configuration:
```bash
sudo nginx -t
ls -la /etc/nginx/conf.d/
cat /etc/nginx/conf.d/museum-system.conf
```

Make sure old configs are backed up:
```bash
sudo mv /etc/nginx/conf.d/museum-timesheet.conf /etc/nginx/conf.d/backup/
sudo systemctl restart nginx
```

### Socket File Not Created

Check gunicorn logs:
```bash
sudo journalctl -u museum-system -n 100
```

Verify gunicorn config:
```bash
cat gunicorn.conf.py | grep bind
```

Should show: `bind = "unix:/tmp/museum_info_system.sock"`

### Permission Errors

```bash
# Set correct ownership
sudo chown aleksandarlukovic:aleksandarlukovic -R /home/aleksandarlukovic/MuseumInfoSystem/logs

# Set socket directory permissions
sudo chmod 755 /tmp

# Restart services
sudo systemctl restart museum-system
sudo systemctl restart nginx
```

## Rolling Back

If you need to restore the old configuration:

```bash
# Stop new service
sudo systemctl stop museum-system
sudo systemctl disable museum-system

# Restore old nginx configs
sudo mv /etc/nginx/conf.d/backup/* /etc/nginx/conf.d/
sudo rm /etc/nginx/conf.d/museum-system.conf

# Restart nginx
sudo systemctl restart nginx
```

## What Changed

### Before
- Port 80: Timesheet app (via old nginx config)
- Port 5000: Museum app (Flask dev server)
- Port 5001: Mineral database (Flask dev server)
- Port 5003: Timesheet (Flask dev server)

### After
- Port 80: Full Museum Information System (via nginx → gunicorn)
- Port 5000: Museum app dev server (for development, optional)
- Port 5001: Mineral database (unchanged)
- Port 5003: Timesheet (unchanged)

The main museum app is now served professionally via nginx and gunicorn on port 80, accessible from the entire LAN.

## Next Steps

After fixing:

1. **Test thoroughly**: Access from multiple devices on your LAN
2. **Update firewall**: Ensure port 80 is allowed
3. **Set up SSL** (optional): Use certbot for HTTPS
4. **Monitor logs**: Check `/var/log/nginx/museum_*.log`
5. **Performance tuning**: Adjust gunicorn workers if needed

## Support

If issues persist:
```bash
# Collect diagnostic info
sudo journalctl -u museum-system -n 100 > museum-system.log
sudo journalctl -u nginx -n 100 > nginx.log
sudo nginx -T > nginx-config.log
systemctl status museum-system > status.log
```

Then review these log files for error messages.
