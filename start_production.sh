#!/bin/bash

# Museum Information System Production Startup Script
# Uses Gunicorn for production deployment

echo "🏛️ Starting Museum Information System (Production)"
echo "================================================="

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Create necessary directories
mkdir -p logs
mkdir -p tmp

# Check dependencies
echo "🔍 Checking production dependencies..."
if ! python -c "import gunicorn" &> /dev/null; then
    echo "⚠️  Gunicorn not found. Installing..."
    pip install gunicorn
fi

# Set production environment
export FLASK_ENV=production
export FLASK_DEBUG=False

# Load environment variables
if [ -f ".env" ]; then
    echo "📋 Loading environment configuration..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  .env file not found. Using production defaults..."
fi

# Production defaults — must match nginx_museum.conf proxy_pass (127.0.0.1:8000)
HOST=${HOST:-"127.0.0.1"}
PORT=${PORT:-"8000"}
WORKERS=${WORKERS:-"1"}
BACKGROUND_WORKER_ENABLED=${BACKGROUND_WORKER_ENABLED:-"false"}
SESSION_TYPE=${SESSION_TYPE:-"redis"}

if [ -z "${REDIS_URL}" ]; then
    echo "❌ REDIS_URL must be set for production shared state"
    exit 1
fi

if [ -z "${MAIL_SETTINGS_ENCRYPTION_KEY}" ]; then
    echo "❌ MAIL_SETTINGS_ENCRYPTION_KEY must be set for shared mail credential encryption"
    exit 1
fi

RATELIMIT_STORAGE_URL=${RATELIMIT_STORAGE_URL:-"${REDIS_URL}"}

echo ""
echo "🚀 Starting Production Server"
echo "   Host: ${HOST}"
echo "   Port: ${PORT}"
echo "   Workers: ${WORKERS}"
echo "   Session Type: ${SESSION_TYPE}"
echo "   Background Worker: ${BACKGROUND_WORKER_ENABLED}"
echo "   PID File: /tmp/museum_info_system.pid"
echo ""
echo "📊 Integrated Systems:"
echo "   • Timesheet System (localSQLtesting)"
echo "   • Mineral Database (PrirodnjackiMuzej)"
echo ""
echo "📋 Logs:"
echo "   • Access: logs/gunicorn_access.log"
echo "   • Error: logs/gunicorn_error.log"
echo "   • App: logs/museum_info_system.log"
echo ""
echo "To stop: kill \$(cat /tmp/museum_info_system.pid)"
echo "================================================="

if [ "${BACKGROUND_WORKER_ENABLED}" = "true" ]; then
    echo "🔁 Starting background worker..."
    nohup python background_worker.py > logs/background_worker.log 2>&1 &
    echo $! > /tmp/museum_background_worker.pid
fi

# Start production server
exec gunicorn \
    --config gunicorn.conf.py \
    --bind "${HOST}:${PORT}" \
    --workers "${WORKERS}" \
    --pid /tmp/museum_info_system.pid \
    --daemon \
    --env "SESSION_TYPE=${SESSION_TYPE}" \
    --env "RATELIMIT_STORAGE_URL=${RATELIMIT_STORAGE_URL}" \
    wsgi:application

echo "✅ Production server started successfully!"
echo "📊 Server status: http://${HOST}:${PORT}"
