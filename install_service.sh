#!/bin/bash
# Quick install script for museum-system service

echo "Installing Museum System Service..."

# Copy service file
sudo cp /home/aleksandarlukovic/MuseumInfoSystem/museum-system.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

echo "✓ Service installed!"
echo ""
echo "Now you can:"
echo "  Start:   sudo systemctl start museum-system"
echo "  Stop:    sudo systemctl stop museum-system"
echo "  Status:  sudo systemctl status museum-system"
echo "  Enable:  sudo systemctl enable museum-system"
echo ""
