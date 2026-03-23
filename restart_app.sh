#!/bin/bash
# Quick restart script for museum system

echo "🔄 Restarting Museum Information System..."
echo ""

# Try systemctl first
echo "Attempting systemctl restart..."
sudo systemctl restart museum-system 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ System restarted via systemctl"
    sudo systemctl status museum-system --no-pager
else
    echo "⚠️  Systemctl failed, trying manual restart..."

    # Kill existing processes
    echo "Killing existing processes..."
    pkill -f "gunicorn.*museum" || true
    pkill -f "python.*app.py" || true

    sleep 2

    # Start manually
    echo "Starting application..."
    cd /home/aleksandarlukovic/MuseumInfoSystem
    source venv/bin/activate 2>/dev/null || true
    nohup gunicorn -c gunicorn.conf.py wsgi:application > logs/gunicorn.log 2>&1 &

    echo "✓ Application restarted manually"
fi

echo ""
echo "Waiting for application to start..."
sleep 3

# Check if running
if pgrep -f "gunicorn.*museum" > /dev/null || pgrep -f "python.*app.py" > /dev/null; then
    echo "✓ Application is running"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Clear your browser cookies"
    echo "   2. Refresh the login page"
    echo "   3. Try logging in again"
else
    echo "✗ Application failed to start"
    echo "   Check logs: tail -f logs/gunicorn_error.log"
fi
