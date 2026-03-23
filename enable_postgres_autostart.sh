#!/bin/bash
# Enable PostgreSQL to start automatically with the museum system

echo "================================================"
echo "PostgreSQL Auto-Start Configuration"
echo "================================================"
echo ""

# Step 1: Enable PostgreSQL to start on boot
echo "1. Enabling PostgreSQL to start on boot..."
sudo systemctl enable postgresql
if [ $? -eq 0 ]; then
    echo "   ✓ PostgreSQL enabled for auto-start"
else
    echo "   ❌ Failed to enable PostgreSQL"
    exit 1
fi
echo ""

# Step 2: Start PostgreSQL now
echo "2. Starting PostgreSQL service..."
sudo systemctl start postgresql
if [ $? -eq 0 ]; then
    echo "   ✓ PostgreSQL started successfully"
else
    echo "   ❌ Failed to start PostgreSQL"
    exit 1
fi
echo ""

# Step 3: Verify PostgreSQL is running
echo "3. Verifying PostgreSQL status..."
sudo systemctl is-active postgresql > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✓ PostgreSQL is active and running"
else
    echo "   ⚠️  PostgreSQL may not be running properly"
fi
echo ""

# Step 4: Update museum-system.service to depend on PostgreSQL
echo "4. Updating museum-system.service to depend on PostgreSQL..."
sudo cp /etc/systemd/system/museum-system.service /etc/systemd/system/museum-system.service.backup
echo "   ✓ Backup created: museum-system.service.backup"

# Create updated service file
sudo tee /etc/systemd/system/museum-system.service > /dev/null << 'EOF'
[Unit]
Description=Museum Information System - Gunicorn
After=network.target postgresql.service
Requires=postgresql.service
Wants=postgresql.service

[Service]
Type=exec
User=aleksandarlukovic
Group=aleksandarlukovic
WorkingDirectory=/home/aleksandarlukovic/MuseumInfoSystem
Environment="PATH=/home/aleksandarlukovic/.local/bin:/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONPATH=/home/aleksandarlukovic/MuseumInfoSystem"
Environment="ENABLE_FALLBACK_AUTH=True"
Environment="FLASK_ENV=development"
ExecStart=/usr/bin/python3 -m gunicorn --config gunicorn.conf.py wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=false
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "   ✓ Service file updated with PostgreSQL dependency"
echo ""

# Step 5: Reload systemd daemon
echo "5. Reloading systemd daemon..."
sudo systemctl daemon-reload
echo "   ✓ Systemd daemon reloaded"
echo ""

# Step 6: Restart museum-system service
echo "6. Restarting museum-system service..."
sudo systemctl restart museum-system.service
if [ $? -eq 0 ]; then
    echo "   ✓ Museum system restarted successfully"
else
    echo "   ⚠️  Museum system restart may have issues"
fi
echo ""

# Step 7: Verify both services are running
echo "7. Verifying services status..."
echo ""
echo "   PostgreSQL Status:"
systemctl is-active postgresql && echo "      ✓ Active" || echo "      ❌ Not Active"
echo ""
echo "   Museum System Status:"
systemctl is-active museum-system.service && echo "      ✓ Active" || echo "      ❌ Not Active"
echo ""

# Step 8: Check if app is using PostgreSQL
echo "8. Checking application database connection..."
sleep 2
journalctl -u museum-system.service -n 20 --no-pager | grep -i "postgresql\|sqlite" | tail -5
echo ""

echo "================================================"
echo "Configuration Complete!"
echo "================================================"
echo ""
echo "PostgreSQL is now configured to:"
echo "  • Start automatically on system boot"
echo "  • Start before the museum system service"
echo "  • Ensure museum system waits for PostgreSQL"
echo ""
echo "To verify the setup:"
echo "  systemctl status postgresql"
echo "  systemctl status museum-system.service"
echo ""
