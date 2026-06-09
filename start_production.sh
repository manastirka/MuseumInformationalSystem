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

# Safely parse .env assignments without executing the file as shell code.
load_env_file() {
    python3 - <<'PY'
import shlex
import sys
from pathlib import Path

try:
    from dotenv import dotenv_values
except ImportError as exc:
    print(f"python-dotenv is required to load .env safely: {exc}", file=sys.stderr)
    sys.exit(1)

env_path = Path('.env')
for key, value in dotenv_values(env_path).items():
    if not key or value is None:
        continue
    print(f"export {key}={shlex.quote(str(value))}")
PY
}

# Load environment variables
if [ -f ".env" ]; then
    echo "📋 Loading environment configuration..."
    if ! eval "$(load_env_file)"; then
        echo "❌ Failed to load .env: Malformed .env entry detected"
        exit 1
    fi
else
    echo "⚠️  .env file not found. Using production defaults..."
fi

# Production defaults — must match nginx_museum.conf proxy_pass (127.0.0.1:8000)
HOST=${HOST:-"127.0.0.1"}
PORT=${PORT:-"8000"}
WORKERS=${WORKERS:-"1"}
BACKGROUND_WORKER_ENABLED=${BACKGROUND_WORKER_ENABLED:-"false"}
SESSION_TYPE=${SESSION_TYPE:-"redis"}
SESSION_INVALIDATE_ON_RESTART=${SESSION_INVALIDATE_ON_RESTART:-"false"}
if [ "${SESSION_INVALIDATE_ON_RESTART}" = "true" ] && [ -z "${SESSION_BOOT_ID}" ]; then
    SESSION_BOOT_ID="$(date +%s%N)"
fi

if [ -z "${REDIS_URL}" ]; then
    echo "❌ REDIS_URL must be set for production shared state"
    exit 1
fi

if [ "${SESSION_TYPE}" != "redis" ]; then
    echo "❌ Production startup requires SESSION_TYPE=redis"
    exit 1
fi

if [ -z "${SECRET_KEY}" ]; then
    echo "❌ SECRET_KEY must be set for production"
    exit 1
fi

case "${SECRET_KEY}" in
    "dev-secret-key"|"dev-only-secret-key"|"test-secret-key")
        echo "❌ SECRET_KEY uses an insecure placeholder value and must be rotated before production startup"
        exit 1
        ;;
esac

if [ -z "${MAIL_SETTINGS_ENCRYPTION_KEY}" ]; then
    echo "⚠️  MAIL_SETTINGS_ENCRYPTION_KEY is not set; encrypted mail credential features will remain unavailable until the key is configured"
fi

RATELIMIT_STORAGE_URL=${RATELIMIT_STORAGE_URL:-"${REDIS_URL}"}

echo ""
echo "🚀 Starting Production Server"
echo "   Host: ${HOST}"
echo "   Port: ${PORT}"
echo "   Workers: ${WORKERS}"
echo "   Session Type: ${SESSION_TYPE}"
echo "   Keep Login Across Restart: $( [ "${SESSION_INVALIDATE_ON_RESTART}" = "true" ] && printf no || printf yes )"
echo "   Background Worker: ${BACKGROUND_WORKER_ENABLED}"
PID_FILE=${PID_FILE:-"/run/museum/museum_info_system.pid"}
echo "   PID File: ${PID_FILE}"
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
echo "To stop: kill \$(cat ${PID_FILE})"
echo "================================================="

if [ "${BACKGROUND_WORKER_ENABLED}" = "true" ]; then
    echo "🔁 Starting background worker..."
    nohup python background_worker.py > logs/background_worker.log 2>&1 &
    echo $! > /tmp/museum_background_worker.pid
fi

mkdir -p storage/uploads
rm -f "${PID_FILE}"

GUNICORN_CMD=(
    gunicorn
    --config gunicorn.conf.py
    --bind "${HOST}:${PORT}"
    --workers "${WORKERS}"
    --pid "${PID_FILE}"
    --daemon
    --env "SESSION_TYPE=${SESSION_TYPE}"
    --env "SESSION_INVALIDATE_ON_RESTART=${SESSION_INVALIDATE_ON_RESTART}"
    --env "RATELIMIT_STORAGE_URL=${RATELIMIT_STORAGE_URL}"
    wsgi:application
)

if [ -n "${SESSION_BOOT_ID:-}" ]; then
    GUNICORN_CMD+=(--env "SESSION_BOOT_ID=${SESSION_BOOT_ID}")
fi

exec "${GUNICORN_CMD[@]}"
