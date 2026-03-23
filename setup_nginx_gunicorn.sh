#!/bin/bash
# Setup script for Museum Information System with Nginx and Gunicorn

set -e

echo "🏛️  Museum Information System - Nginx & Gunicorn Setup"
echo "========================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}This script needs to be run with sudo for some operations${NC}"
    echo "Usage: sudo bash setup_nginx_gunicorn.sh"
    exit 1
fi

echo ""
echo "Step 1: Installing required packages..."
echo "----------------------------------------"
dnf install -y nginx python3-pip python3-devel gcc

echo ""
echo "Step 2: Installing Python dependencies..."
echo "-----------------------------------------"
# Use the actual user (not root) to install pip packages
ACTUAL_USER=$(logname)
sudo -u $ACTUAL_USER pip3 install --user -r requirements.txt

echo ""
echo "Step 3: Creating logs directory..."
echo "----------------------------------"
mkdir -p logs
chown -R $ACTUAL_USER:$ACTUAL_USER logs

echo ""
echo "Step 4: Setting up Nginx configuration..."
echo "-----------------------------------------"
# Copy nginx config to sites-available
mkdir -p /etc/nginx/sites-available
mkdir -p /etc/nginx/sites-enabled

cp nginx_museum.conf /etc/nginx/sites-available/museum

# Create symlink to sites-enabled
if [ ! -L /etc/nginx/sites-enabled/museum ]; then
    ln -s /etc/nginx/sites-available/museum /etc/nginx/sites-enabled/museum
    echo -e "${GREEN}✓ Nginx configuration linked${NC}"
else
    echo -e "${YELLOW}⚠ Nginx configuration already linked${NC}"
fi

# Update nginx.conf to include sites-enabled if not already done
if ! grep -q "include /etc/nginx/sites-enabled" /etc/nginx/nginx.conf; then
    sed -i '/http {/a \    include /etc/nginx/sites-enabled/*;' /etc/nginx/nginx.conf
    echo -e "${GREEN}✓ Updated nginx.conf to include sites-enabled${NC}"
fi

# Test nginx configuration
echo ""
echo "Testing Nginx configuration..."
nginx -t

echo ""
echo "Step 5: Setting up systemd service..."
echo "-------------------------------------"
# Copy systemd service file
cp museum-system.service /etc/systemd/system/

# Reload systemd
systemctl daemon-reload
echo -e "${GREEN}✓ Systemd service installed${NC}"

echo ""
echo "Step 6: Setting permissions for socket..."
echo "-----------------------------------------"
# Set permissions for the socket directory
chmod 755 /tmp
echo -e "${GREEN}✓ Socket permissions set${NC}"

echo ""
echo "Step 7: Configuring firewall..."
echo "-------------------------------"
if systemctl is-active --quiet firewalld; then
    firewall-cmd --permanent --add-service=http
    firewall-cmd --reload
    echo -e "${GREEN}✓ Firewall configured to allow HTTP${NC}"
else
    echo -e "${YELLOW}⚠ Firewalld not running, skipping firewall configuration${NC}"
fi

echo ""
echo "Step 8: Starting services..."
echo "---------------------------"
# Enable and start the museum service
systemctl enable museum-system.service
systemctl start museum-system.service

# Enable and start nginx
systemctl enable nginx
systemctl restart nginx

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Setup completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Service Status:"
echo "---------------"
systemctl status museum-system.service --no-pager -l || true
echo ""
systemctl status nginx --no-pager -l || true

echo ""
echo "Access your application at:"
echo "  Local:   http://localhost"
echo "  LAN:     http://192.168.144.48"
echo ""
echo "Useful commands:"
echo "  Check service status:  sudo systemctl status museum-system"
echo "  View logs:            sudo journalctl -u museum-system -f"
echo "  Restart service:      sudo systemctl restart museum-system"
echo "  Restart nginx:        sudo systemctl restart nginx"
echo "  Check nginx logs:     sudo tail -f /var/log/nginx/museum_*.log"
echo ""
