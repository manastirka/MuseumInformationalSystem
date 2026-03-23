#!/bin/bash

# Museum Information System Startup Script
# Starts the main application and integrated subsystems

echo "🏛️ Starting Museum Information System"
echo "======================================"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Create logs directory
mkdir -p logs

# Check dependencies
echo "🔍 Checking dependencies..."
if ! python -c "import flask" &> /dev/null; then
    echo "⚠️  Flask not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Check database connectivity
echo "🗄️ Checking database connectivity..."
python -c "
import sys
sys.path.insert(0, 'localSQLtesting')
try:
    from database import db_manager
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        print('✅ Database connection successful')
except Exception as e:
    print(f'⚠️  Database connection failed: {e}')
    print('   Please check your database configuration in .env')
"

# Set environment variables if .env exists
if [ -f ".env" ]; then
    echo "📋 Loading environment configuration..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  .env file not found. Using defaults..."
    echo "   Copy .env.example to .env and configure your settings"
fi

# Default values
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-"5555"}
FLASK_DEBUG=${FLASK_DEBUG:-"True"}

echo ""
echo "🚀 Starting Museum Information System"
echo "   Main System: http://${HOST}:${PORT}"
echo "   Debug Mode: ${FLASK_DEBUG}"
echo ""
echo "📊 Integrated Systems:"
echo "   • Timesheet System (localSQLtesting)"
echo "   • Mineral Database (PrirodnjackiMuzej)"
echo ""
echo "🔐 Default Login:"
echo "   Admin: admin / admin123"
echo "   Employee: [museum-email] / user"
echo ""
echo "Press Ctrl+C to stop the server"
echo "======================================"

# Start the main application
python app.py --host "$HOST" --port "$PORT" $([ "$FLASK_DEBUG" = "True" ] && echo "--debug")