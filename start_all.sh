#!/bin/bash

# Museum Information System - Startup Script
# Starts main museum application (mineral database is now integrated)

echo "🏛️  Museum Information System - Starting services..."
echo ""

# Set working directory
cd "$(dirname "$0")"

# Load environment variables from .env file
if [ -f .env ]; then
    set -a
    source .env 2>/dev/null
    set +a
    echo "✓ Loaded environment variables from .env"
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Kill any existing processes on port 5000
echo "🧹 Cleaning up existing processes..."
fuser -k 5000/tcp 2>/dev/null || lsof -ti:5000 | xargs kill -9 2>/dev/null
sleep 2

# Start main application (port 5000)
echo "🏛️  Starting Museum Information System on port 5000..."
nohup python3 app.py > logs/main_app.log 2>&1 &
MAIN_PID=$!
echo "   ✓ Main Application started (PID: $MAIN_PID)"
echo "$MAIN_PID" > logs/main_app.pid

echo ""
echo "✅ Museum system started successfully!"
echo ""
echo "📋 Access URL:"
echo "   Museum System:       http://localhost:5000"
echo "   Production (Nginx):  http://192.168.144.48"
echo ""
echo "📊 Process ID:"
echo "   Main App:            $MAIN_PID"
echo ""
echo "📁 Log file:"
echo "   Main App:            logs/main_app.log"
echo ""
echo "ℹ️  NOTE: Mineral database is now integrated into the main app"
echo "   Access at: http://localhost:5000/admin/mineral_collection"
echo ""
echo "⚠️  To stop service, run: ./stop_all.sh"
echo "   Or manually: pkill -f 'python.*app.py'"
echo ""
echo "📜 To view logs, run:"
echo "   tail -f logs/main_app.log"
