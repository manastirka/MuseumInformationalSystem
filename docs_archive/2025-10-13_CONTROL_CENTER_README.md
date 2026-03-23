# Museum Control Center - Unified Control Panel

## Overview

The **Museum Control Center** is a comprehensive desktop application that provides unified control over all Museum Information System services from a single interface.

## What It Replaces

This unified control center replaces multiple individual control panels:
- ❌ `PrirodnjackiMuzej/museum_control_panel.py` - Delete this
- ❌ `PrirodnjackiMuzej/improved_control_panel.py` - Delete this  
- ❌ `localSQLtesting/desktop_web_admin.py` - Keep for now (has specific timesheet functions)

## Features

### 🎛️ **Tab 1: Service Control**
- Start/Stop/Restart individual services
- Real-time status monitoring with color indicators
- One-click access to service URLs
- Process ID (PID) tracking
- Service-specific log viewing

**Controlled Services:**
1. 🏛️ **Main Application** (Port 5000)
2. 💎 **Mineral Database** (Port 5001)
3. 📅 **Timesheet System** (Port 5003)

### 📋 **Tab 2: Logs Viewer**
- View logs from any service
- Auto-refresh capability
- Clear logs functionality
- Last 500 lines display
- Matrix-style green-on-black terminal theme

### 🖥️ **Tab 3: System Information**
- Real-time system stats (CPU, Memory, Disk)
- Operating system information
- Service status overview
- Process IDs and ports
- Direct URL access links

### 💾 **Tab 4: Database Management**
- Check database status (MySQL + SQLite)
- Database backup operations
- Statistics and optimization
- Database size monitoring

### 🚀 **Quick Actions (Bottom Bar)**
- **Start All Services** - Launch all services at once
- **Stop All Services** - Graceful shutdown of all services
- **Restart All** - Complete system restart

### 📊 **Real-time Status Bar**
Shows: `Status: X/3 services active | HH:MM:SS`

## How to Run

### From Terminal
```bash
cd /home/aleksandarlukovic/MuseumInfoSystem
python3 museum_control_center.py
```

### From Desktop
Double-click the desktop launcher:
```bash
museum-control-center.desktop
```

Or copy to desktop:
```bash
cp museum-control-center.desktop ~/Desktop/
chmod +x ~/Desktop/museum-control-center.desktop
```

## Requirements

The control center requires `psutil` for system monitoring:

```bash
pip install psutil
```

All other dependencies are standard Python libraries (tkinter, subprocess, etc.)

## Architecture

```
┌─────────────────────────────────────────────────────┐
│     Museum Control Center (Tkinter GUI)             │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │ Main App     │  │ Mineral DB   │  │Timesheet │ │
│  │ Port 5000    │  │ Port 5001    │  │Port 5003 │ │
│  └──────────────┘  └──────────────┘  └──────────┘ │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │  Real-time Status Monitoring (2s refresh)   │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │  Log Aggregation & Viewing                  │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## Key Advantages

### Unified Interface
- Single application for all service management
- No need to remember multiple control panels
- Consistent UI across all functions

### Auto-Discovery
- Automatically detects running services by port
- Shows real-time PID information
- No manual configuration needed

### Professional UI
- Clean, modern Tkinter interface
- Color-coded status indicators
- Tabbed organization
- Intuitive controls

### Service Management
- Start services with proper logging
- Graceful shutdowns with SIGTERM
- Force kill if necessary (SIGKILL)
- Proper error handling

### Monitoring
- Background thread for status updates (every 2 seconds)
- Log auto-refresh option
- System resource monitoring
- Database status checking

## Cleanup Instructions

### Files to Delete

Once you confirm the unified control center works, delete these old control panels:

```bash
cd /home/aleksandarlukovic/MuseumInfoSystem

# Delete mineral database control panels
rm PrirodnjackiMuzej/museum_control_panel.py
rm PrirodnjackiMuzej/improved_control_panel.py
rm PrirodnjackiMuzej/test_control_panel.py

# Delete backups
rm -rf PrirodnjackiMuzej/backups/*/museum_control_panel.py
rm -rf PrirodnjackiMuzej/backups/*/improved_control_panel.py
```

### Keep These Files

**DO NOT delete:**
- `localSQLtesting/desktop_web_admin.py` - Has timesheet-specific functionality (viewing/printing reports)
- The unified control center focuses on service management, not data management

## Usage Tips

### Starting the System
1. Open Control Center
2. Click "🚀 Покрени све сервисе" (Start All Services)
3. Wait 5-10 seconds for all services to initialize
4. Check status indicators turn green (🟢)

### Troubleshooting Services
1. Go to "Логови" (Logs) tab
2. Select problematic service from dropdown
3. Enable "Аутоматско освежавање" (Auto-refresh)
4. Watch logs in real-time

### Restarting a Service
1. Click "🔄 Рестарт" button for specific service
2. Or use "🔄 Рестартуј све" for all services

### Opening Service URLs
1. Click blue URL links in service panels
2. URLs open automatically in default browser

## Screenshots Description

The application has 4 main tabs:

**Сервиси** (Services)
- Large panels for each service
- Start/Stop/Restart/Logs buttons
- Real-time status with green/red indicators
- PID and port information

**Логови** (Logs)
- Black terminal-style log viewer
- Service selection dropdown
- Refresh and clear buttons
- Auto-refresh checkbox

**Системске информације** (System Info)
- CPU, memory, disk usage
- Service overview
- All ports and PIDs listed
- Refresh button

**Базе података** (Databases)
- Database status checker
- Backup, stats, optimize buttons
- Status display area

## Future Enhancements

Possible additions (not currently implemented):
- Database backup scheduling
- Email alerts for service failures
- Remote service management
- Service dependency visualization
- Performance graphing
- Configuration editor

## Support

For issues or questions:
1. Check logs in the Logs tab
2. Verify system requirements (psutil installed)
3. Ensure proper file permissions
4. Check that ports 5000, 5001, 5003 are available

## Summary

The Museum Control Center provides a professional, unified interface for managing all Museum Information System services. It consolidates multiple control panels into one application with real-time monitoring, log viewing, and comprehensive service management capabilities.

**One app to rule them all!** 🏛️
