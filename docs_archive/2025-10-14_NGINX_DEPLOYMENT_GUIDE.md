# Museum Information System - Nginx & Gunicorn Deployment Guide

## Overview

This guide will help you deploy the Museum Information System on your local LAN using Nginx as a reverse proxy and Gunicorn as the WSGI application server.

## Architecture

```
Internet/LAN → Nginx (Port 80) → Gunicorn (Unix Socket) → Flask Application
```

- **Nginx**: Handles incoming HTTP requests, serves static files, and proxies dynamic requests to Gunicorn
- **Gunicorn**: Production-grade WSGI server running the Flask application
- **Unix Socket**: Secure communication between Nginx and Gunicorn (faster than TCP)

## Files Created

1. **nginx_museum.conf** - Nginx server configuration
2. **museum-system.service** - Systemd service for Gunicorn
3. **setup_nginx_gunicorn.sh** - Automated setup script
4. **gunicorn.conf.py** - Gunicorn configuration (updated)

## Quick Setup (Recommended)

Run the automated setup script:

```bash
sudo bash setup_nginx_gunicorn.sh
```

This script will:
- Install Nginx and dependencies
- Install Python packages
- Configure Nginx
- Set up systemd service
- Configure firewall
- Start all services

## Manual Setup

If you prefer to set up manually or need to troubleshoot:

### 1. Install Dependencies

```bash
# Install system packages
sudo dnf install -y nginx python3-pip python3-devel gcc

# Install Python dependencies
pip3 install --user -r requirements.txt
```

### 2. Configure Nginx

```bash
# Create necessary directories
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled

# Copy nginx configuration
sudo cp nginx_museum.conf /etc/nginx/sites-available/museum

# Create symlink
sudo ln -s /etc/nginx/sites-available/museum /etc/nginx/sites-enabled/museum

# Update nginx.conf to include sites-enabled
# Add this line inside the http block if not present:
# include /etc/nginx/sites-enabled/*;

# Test configuration
sudo nginx -t
```

### 3. Set Up Systemd Service

```bash
# Copy service file
sudo cp museum-system.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable museum-system.service

# Start the service
sudo systemctl start museum-system.service
```

### 4. Start Nginx

```bash
# Enable nginx to start on boot
sudo systemctl enable nginx

# Start nginx
sudo systemctl start nginx
```

### 5. Configure Firewall

```bash
# Allow HTTP traffic
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
```

## Accessing the Application

Once deployed, you can access the application at:

- **Local machine**: http://localhost
- **From LAN**: http://192.168.144.48
- **By hostname**: http://your-hostname (if DNS is configured)

## Service Management

### Check Service Status

```bash
# Check Gunicorn service
sudo systemctl status museum-system

# Check Nginx status
sudo systemctl status nginx
```

### Start/Stop/Restart Services

```bash
# Museum system
sudo systemctl start museum-system
sudo systemctl stop museum-system
sudo systemctl restart museum-system

# Nginx
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
```

### View Logs

```bash
# Gunicorn logs (via systemd)
sudo journalctl -u museum-system -f

# Gunicorn logs (file)
tail -f logs/gunicorn_access.log
tail -f logs/gunicorn_error.log

# Nginx logs
sudo tail -f /var/log/nginx/museum_access.log
sudo tail -f /var/log/nginx/museum_error.log
```

## Troubleshooting

### Service won't start

```bash
# Check service status and logs
sudo systemctl status museum-system
sudo journalctl -u museum-system -xe

# Check if socket file is created
ls -la /tmp/museum_info_system.sock

# Check socket permissions
sudo chmod 755 /tmp
```

### Nginx 502 Bad Gateway

This usually means Gunicorn is not running or the socket connection failed:

```bash
# Restart Gunicorn
sudo systemctl restart museum-system

# Check if socket exists
ls -la /tmp/museum_info_system.sock

# Check Nginx error log
sudo tail -f /var/log/nginx/museum_error.log
```

### Static files not loading

```bash
# Check file permissions
ls -la /home/aleksandarlukovic/MuseumInfoSystem/static
ls -la /home/aleksandarlukovic/MuseumInfoSystem/data

# Ensure Nginx user can read files
sudo chmod 755 /home/aleksandarlukovic
sudo chmod 755 /home/aleksandarlukovic/MuseumInfoSystem
sudo chmod -R 755 /home/aleksandarlukovic/MuseumInfoSystem/static
sudo chmod -R 755 /home/aleksandarlukovic/MuseumInfoSystem/data
```

### Can't connect from other devices on LAN

```bash
# Check firewall
sudo firewall-cmd --list-all

# Add HTTP service if missing
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload

# Check if Nginx is listening on all interfaces
sudo ss -tlnp | grep :80
```

### Update application after code changes

```bash
# Restart Gunicorn to reload the application
sudo systemctl restart museum-system

# No need to restart Nginx unless you changed its config
```

## Performance Tuning

### Gunicorn Workers

The configuration automatically sets workers based on CPU cores:
```python
workers = multiprocessing.cpu_count() * 2 + 1
```

You can manually adjust in `gunicorn.conf.py`:
```python
workers = 4  # Set to desired number
```

### Nginx Connection Limits

Edit `nginx_museum.conf` to adjust:
```nginx
worker_connections 1024;  # Add this to nginx.conf
client_max_body_size 50M;  # Adjust file upload limit
```

## Security Considerations

### For Production Deployment

1. **Use HTTPS**: Obtain SSL certificate and configure HTTPS
2. **Change SECRET_KEY**: Set a strong secret key in environment variables
3. **Restrict access**: Use firewall rules to limit access
4. **Regular updates**: Keep system packages and Python dependencies updated
5. **Backup**: Regular backups of database and uploaded files

### Enable HTTPS (Optional)

```bash
# Install certbot
sudo dnf install certbot python3-certbot-nginx

# Obtain certificate (replace with your domain)
sudo certbot --nginx -d your-domain.com

# Auto-renewal is set up automatically
```

## Monitoring

### Set up log rotation

Create `/etc/logrotate.d/museum-system`:

```
/home/aleksandarlukovic/MuseumInfoSystem/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0644 aleksandarlukovic aleksandarlukovic
    sharedscripts
    postrotate
        systemctl reload museum-system > /dev/null 2>&1 || true
    endscript
}
```

### Monitor resource usage

```bash
# CPU and memory usage
htop

# Check process status
ps aux | grep gunicorn

# Check open connections
sudo ss -tunap | grep :80
```

## Backup and Recovery

### Backup important files

```bash
# Create backup directory
mkdir -p ~/backups/museum-system

# Backup database and uploads
tar -czf ~/backups/museum-system/backup-$(date +%Y%m%d).tar.gz \
    data/ \
    localSQLtesting/*.db \
    PrirodnjackiMuzej/*.db

# Backup configuration
cp nginx_museum.conf ~/backups/museum-system/
cp museum-system.service ~/backups/museum-system/
cp gunicorn.conf.py ~/backups/museum-system/
```

## Uninstall

To remove the installation:

```bash
# Stop and disable services
sudo systemctl stop museum-system
sudo systemctl disable museum-system
sudo systemctl stop nginx
sudo systemctl disable nginx

# Remove service files
sudo rm /etc/systemd/system/museum-system.service
sudo rm /etc/nginx/sites-available/museum
sudo rm /etc/nginx/sites-enabled/museum

# Reload systemd
sudo systemctl daemon-reload

# Remove socket file
rm -f /tmp/museum_info_system.sock
```

## Support

For issues or questions:
- Check logs: `sudo journalctl -u museum-system -f`
- Review Nginx logs: `sudo tail -f /var/log/nginx/museum_error.log`
- Verify configuration: `nginx -t` and `gunicorn --check-config gunicorn.conf.py`

## Additional Resources

- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Flask Deployment Options](https://flask.palletsprojects.com/en/latest/deploying/)
