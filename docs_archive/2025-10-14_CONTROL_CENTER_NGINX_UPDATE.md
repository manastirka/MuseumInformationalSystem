# Museum Control Center - Nginx Integration Update

## Overview

The Museum Control Center has been updated to manage nginx and the gunicorn-based museum system service alongside the existing development services.

## Changes Made

### 1. Added New Services

Two new services have been added to the control center:

#### Nginx Web Server
- **Name**: Nginx Web Server
- **Type**: Systemd service
- **Port**: 80
- **Control**: Via systemctl
- **Logs**: Uses journalctl for viewing system logs
- **URL**: http://localhost (LAN: http://192.168.144.48)

#### Museum System (Gunicorn)
- **Name**: Музејски систем (Gunicorn)
- **Type**: Systemd service
- **Socket**: /tmp/museum_info_system.sock
- **Control**: Via systemctl
- **Logs**: Uses journalctl for viewing system logs

### 2. Service Types

The control center now supports two types of services:

#### Process Services (Existing)
- Started directly as Python processes
- Controlled via process signals (SIGTERM/SIGKILL)
- Port-based status checking
- File-based logs
- Examples: main_app, mineral_db, timesheet

#### Systemd Services (New)
- Managed by systemd
- Controlled via systemctl (start/stop/restart)
- Status checked via `systemctl is-active`
- Logs viewed via journalctl
- Examples: nginx, museum-system

### 3. New Features

#### Systemd Integration
- **Service Control**: Uses `pkexec` to request admin privileges for systemctl commands
- **Status Checking**: Real-time status monitoring via `systemctl is-active`
- **PID Retrieval**: Gets process IDs from systemd for running services
- **Log Viewing**: Integrates journalctl for systemd service logs (last 500 lines)

#### Enhanced UI
- **Socket Display**: Shows Unix socket paths for services that don't use TCP ports
- **Systemd Indicator**: Displays systemd service name for system services
- **Smart URL Display**: Shows both localhost and LAN IP for port 80 services
- **Service Type Detection**: Automatically handles different service types

#### Improved Log Management
- **Dual Log Support**: File-based logs for processes, journalctl for systemd
- **Auto-refresh**: Works with both log types
- **Clear Logs**: Prevents accidental deletion of system logs (journalctl)

### 4. Permission Handling

Systemd service control requires root privileges. The control center uses `pkexec` to:
- Request user authentication via PolicyKit
- Execute systemctl commands with appropriate permissions
- Provide clear error messages if authentication fails

## Usage

### Starting Services

1. **Launch Control Center**:
   ```bash
   python3 museum_control_center.py
   ```

2. **Start Individual Services**:
   - Click the "▶️ Покрени" button for the desired service
   - For systemd services, you'll be prompted for your password

3. **Start All Services**:
   - Click "🚀 Покрени све сервисе" at the bottom

### Service Control

Each service panel shows:
- **Status**: Real-time status indicator (🟢 Active / 🔴 Stopped)
- **Connection Info**: Port number or Unix socket path
- **URL**: Clickable link to open in browser (for web services)
- **Systemd Info**: Service name (for systemd services)

Control buttons:
- **▶️ Покрени**: Start the service
- **⏹️ Заустави**: Stop the service
- **🔄 Рестарт**: Restart the service
- **📋 Логови**: View service logs

### Viewing Logs

1. Go to the "Логови" tab
2. Select a service from the dropdown (now includes nginx and museum_system)
3. Click "🔄 Освежи" to refresh logs
4. Enable "Аутоматско освежавање" for real-time updates

**Note**: Systemd services show the last 500 lines from journalctl.

### System Information

The "Системске информације" tab displays:
- System resource usage (CPU, memory, disk)
- Status of all services
- Port numbers and URLs
- Socket paths for Unix socket services
- Systemd service names

## Service Startup Order

For production deployment, recommended startup order:

1. **nginx** - Start nginx first to listen on port 80
2. **museum_system** - Start gunicorn service (connects to nginx via socket)
3. **mineral_db** (optional) - If using standalone mineral database
4. **timesheet** (optional) - If using standalone timesheet system

**Note**: The dev server (main_app on port 5000) should NOT be running when using the production nginx/gunicorn setup, as they serve the same application.

## Architecture

### Development Mode
```
Browser → Flask Dev Server (port 5000)
```

### Production Mode (Nginx + Gunicorn)
```
Browser → Nginx (port 80) → Gunicorn (unix socket) → Flask Application
```

## Troubleshooting

### Service Won't Start

**Systemd Services**:
- Check service status: `sudo systemctl status nginx`
- View detailed logs: `sudo journalctl -u nginx -n 50`
- Ensure service files are installed (see NGINX_DEPLOYMENT_GUIDE.md)

**Process Services**:
- Check if port is already in use
- View log files in the logs directory
- Ensure no other instance is running

### Permission Denied

If you get permission errors when controlling systemd services:
- Ensure you're in the right user groups: `groups`
- PolicyKit should prompt for password - if not, check PolicyKit configuration
- Try running manually: `sudo systemctl start nginx`

### Logs Not Showing

**Systemd Services**:
- Verify journalctl access: `journalctl -u nginx --no-pager`
- Check if service is registered: `systemctl list-units | grep nginx`

**Process Services**:
- Check if log file exists in the logs directory
- Verify file permissions: `ls -la logs/`

## Files Modified

- **museum_control_center.py**: Updated to support nginx and systemd services

## Related Documentation

- **NGINX_DEPLOYMENT_GUIDE.md**: Complete nginx and gunicorn deployment guide
- **nginx_museum.conf**: Nginx configuration file
- **museum-system.service**: Systemd service file for gunicorn
- **setup_nginx_gunicorn.sh**: Automated setup script

## Security Notes

- Systemd service control requires sudo/admin privileges
- PolicyKit (pkexec) is used for secure privilege escalation
- Only specific systemctl commands are allowed (start, stop, restart, is-active, show)
- No direct root access is granted to the control center application

## Future Enhancements

Potential improvements:
- Add service dependency checking (start nginx before museum-system)
- Real-time log streaming for systemd services
- Service health checks beyond simple status
- Auto-restart failed services
- Notification system for service failures
- Resource usage graphs per service
