#!/bin/bash
# Setup sudoers to allow control center to manage services without password

echo "Setting up passwordless sudo for museum services..."

# Create sudoers file
cat << 'EOF' | sudo tee /etc/sudoers.d/museum-control-center
# Allow user to control museum services without password
aleksandarlukovic ALL=(ALL) NOPASSWD: /usr/bin/systemctl start museum-system
aleksandarlukovic ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop museum-system
aleksandarlukovic ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart museum-system
aleksandarlukovic ALL=(ALL) NOPASSWD: /usr/bin/systemctl status museum-system
aleksandarlukovic ALL=(ALL) NOPASSWD: /usr/bin/systemctl is-active museum-system
aleksandarlukovic ALL=(ALL) NOPASSWD: /usr/bin/systemctl show museum-system
aleksandarlukovic ALL=(ALL) NOPASSWD: /usr/bin/systemctl start nginx
aleksandarlukovic ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop nginx
aleksandarlukovic ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
aleksandarlukovic ALL=(ALL) NOPASSWD: /usr/bin/systemctl status nginx
aleksandarlukovic ALL=(ALL) NOPASSWD: /usr/bin/systemctl is-active nginx
aleksandarlukovic ALL=(ALL) NOPASSWD: /usr/bin/systemctl show nginx
EOF

# Set correct permissions
sudo chmod 0440 /etc/sudoers.d/museum-control-center

# Verify sudoers syntax
sudo visudo -c

echo "✓ Done! You can now control services from the Control Center without password prompts."
