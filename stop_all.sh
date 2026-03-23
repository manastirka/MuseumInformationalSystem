#!/bin/bash

# Museum Information System - Stop Script
# Stops main application

echo "🛑 Stopping Museum Information System..."
echo ""

# Kill process by PID if file exists
if [ -f logs/main_app.pid ]; then
    MAIN_PID=$(cat logs/main_app.pid)
    echo "   Stopping Main Application (PID: $MAIN_PID)..."
    kill $MAIN_PID 2>/dev/null
    rm logs/main_app.pid
fi

# Cleanup any remaining process on port 5000
echo "   Cleaning up any remaining processes..."
pkill -f "python.*app.py.*5000" 2>/dev/null

sleep 2

echo ""
echo "✅ Museum system stopped"
echo "ℹ️  NOTE: Mineral database is now part of the main app (no separate service)"
