#!/bin/bash

set -euo pipefail
set +H

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

QA_SERVER_MODE="${QA_SERVER_MODE:-flask}"
QA_SERVER_HOST="${QA_SERVER_HOST:-127.0.0.1}"
QA_SERVER_PORT="${QA_SERVER_PORT:-}"
if [ -z "$QA_SERVER_PORT" ]; then
  if [ "$QA_SERVER_MODE" = "gunicorn" ]; then
    QA_SERVER_PORT="5051"
  else
    QA_SERVER_PORT="5050"
  fi
fi

BASE_URL="${CYPRESS_BASE_URL:-http://${QA_SERVER_HOST}:${QA_SERVER_PORT}}"
SERVER_LOG="logs/qa_server.log"
QA_SESSION_DIR="${QA_SESSION_DIR:-${ROOT_DIR}/logs/qa_flask_session}"
SERVER_PID=""
SERVER_STARTED="0"
SERVER_PIDFILE=""
REDIS_CONTAINER_NAME=""
REDIS_STARTED="0"
QA_INCLUDE_LINT="${QA_INCLUDE_LINT:-1}"
QA_INCLUDE_CYPRESS="${QA_INCLUDE_CYPRESS:-1}"
QA_INCLUDE_PLAYWRIGHT="${QA_INCLUDE_PLAYWRIGHT:-1}"
QA_INCLUDE_K6="${QA_INCLUDE_K6:-0}"
QA_GUNICORN_WORKERS="${QA_GUNICORN_WORKERS:-4}"
QA_REDIS_URL="${QA_REDIS_URL:-${REDIS_URL:-}}"
QA_USE_REDIS="${QA_USE_REDIS:-0}"
QA_REDIS_MODE="${QA_REDIS_MODE:-podman}"
QA_REDIS_HOST="${QA_REDIS_HOST:-127.0.0.1}"
QA_REDIS_PORT="${QA_REDIS_PORT:-6379}"
QA_REDIS_IMAGE="${QA_REDIS_IMAGE:-docker.io/library/redis:7-alpine}"
QA_K6_BIN="${QA_K6_BIN:-}"

cleanup() {
  if [ "$SERVER_STARTED" = "1" ] && [ -n "$SERVER_PID" ]; then
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
  if [ -n "$SERVER_PIDFILE" ] && [ -f "$SERVER_PIDFILE" ]; then
    rm -f "$SERVER_PIDFILE"
  fi
  if [ "$REDIS_STARTED" = "1" ] && [ -n "$REDIS_CONTAINER_NAME" ]; then
    podman rm -f "$REDIS_CONTAINER_NAME" >/dev/null 2>&1 || true
  fi
}

trap cleanup EXIT

echo "QA wrapper"
echo "=========="
echo "Server mode: ${QA_SERVER_MODE}"
echo "Base URL: ${BASE_URL}"

run_with_browser_log_filter() {
  local command_status=0

  set +e
  "$@" 2>&1 | grep -vE 'gles2_cmd_decoder_passthrough\.cc|gl_utils\.cc.*GPU stall due to ReadPixels'
  command_status=${PIPESTATUS[0]}
  set -e

  return "$command_status"
}

prepare_gunicorn_pidfile() {
  local pidfile="$1"

  if [ ! -f "$pidfile" ]; then
    return
  fi

  local existing_pid=""
  existing_pid="$(cat "$pidfile" 2>/dev/null || true)"

  if [ -n "$existing_pid" ] && kill -0 "$existing_pid" 2>/dev/null; then
    local command_name=""
    command_name="$(ps -p "$existing_pid" -o comm= 2>/dev/null || true)"
    if printf '%s' "$command_name" | grep -qi 'gunicorn'; then
      echo "Stopping stale QA gunicorn process on PID ${existing_pid}"
      kill "$existing_pid" 2>/dev/null || true
      wait "$existing_pid" 2>/dev/null || true
      sleep 1
    fi
  fi

  rm -f "$pidfile"
}

ensure_qa_redis() {
  if [ -n "$QA_REDIS_URL" ]; then
    echo "Using configured Redis at ${QA_REDIS_URL}"
    return
  fi

  if [ "$QA_USE_REDIS" != "1" ]; then
    return
  fi

  if [ "$QA_REDIS_MODE" != "podman" ]; then
    echo "Unsupported QA_REDIS_MODE: ${QA_REDIS_MODE}" >&2
    exit 1
  fi

  if ! command -v podman >/dev/null 2>&1; then
    echo "podman is required for QA_USE_REDIS=1" >&2
    exit 1
  fi

  REDIS_CONTAINER_NAME="museum-info-system-qa-redis"
  echo "Starting local QA Redis via podman on ${QA_REDIS_HOST}:${QA_REDIS_PORT}"
  podman rm -f "$REDIS_CONTAINER_NAME" >/dev/null 2>&1 || true
  podman run -d \
    --name "$REDIS_CONTAINER_NAME" \
    -p "${QA_REDIS_HOST}:${QA_REDIS_PORT}:6379" \
    "$QA_REDIS_IMAGE" >/dev/null
  REDIS_STARTED="1"
  QA_REDIS_URL="redis://${QA_REDIS_HOST}:${QA_REDIS_PORT}/0"

  for _ in $(seq 1 30); do
    if podman exec "$REDIS_CONTAINER_NAME" redis-cli ping >/dev/null 2>&1; then
      break
    fi
    sleep 1
  done

  if ! podman exec "$REDIS_CONTAINER_NAME" redis-cli ping >/dev/null 2>&1; then
    echo "QA Redis did not become healthy" >&2
    exit 1
  fi
}

if [ "$QA_INCLUDE_CYPRESS" = "1" ]; then
  required_vars=(
    CYPRESS_ADMIN_EMAIL
    CYPRESS_ADMIN_PASSWORD
    CYPRESS_EMPLOYEE_EMAIL
    CYPRESS_EMPLOYEE_PASSWORD
  )

  for var_name in "${required_vars[@]}"; do
    if [ -z "${!var_name:-}" ]; then
      echo "Missing required environment variable: $var_name" >&2
      exit 1
    fi
  done
fi

mkdir -p logs
mkdir -p "$QA_SESSION_DIR"
ensure_qa_redis

if [ -z "$QA_K6_BIN" ]; then
  if command -v k6 >/dev/null 2>&1; then
    QA_K6_BIN="$(command -v k6)"
  elif [ -x "/tmp/k6-v0.49.0-linux-amd64/k6" ]; then
    QA_K6_BIN="/tmp/k6-v0.49.0-linux-amd64/k6"
  fi
fi

if [ -n "$QA_K6_BIN" ]; then
  export PATH="$(dirname "$QA_K6_BIN"):$PATH"
fi

SESSION_INVALIDATE_ON_RESTART="${SESSION_INVALIDATE_ON_RESTART:-false}"
if [ "${SESSION_INVALIDATE_ON_RESTART}" = "true" ] && [ -z "${SESSION_BOOT_ID:-}" ]; then
  SESSION_BOOT_ID="$(date +%s%N)"
fi

if curl -sf "${BASE_URL}/login" >/dev/null 2>&1; then
  echo "Using existing app server at ${BASE_URL}"
else
  echo "Starting local QA server at ${BASE_URL}"
  if [ "$QA_SERVER_MODE" = "gunicorn" ]; then
    SERVER_LOG="logs/qa_gunicorn.log"
    SERVER_PIDFILE="/tmp/museum_info_system_qa.pid"
    prepare_gunicorn_pidfile "$SERVER_PIDFILE"
    FLASK_ENV=testing \
    SECRET_KEY=test-secret \
    REDIS_URL="$QA_REDIS_URL" \
    SESSION_INVALIDATE_ON_RESTART="${SESSION_INVALIDATE_ON_RESTART:-false}" \
    SESSION_BOOT_ID="${SESSION_BOOT_ID:-}" \
    SESSION_TYPE="${SESSION_TYPE:-$( [ -n "$QA_REDIS_URL" ] && printf redis || printf filesystem )}" \
    SESSION_FILE_DIR="$QA_SESSION_DIR" \
    RATELIMIT_STORAGE_URL="${RATELIMIT_STORAGE_URL:-$( [ -n "$QA_REDIS_URL" ] && printf "%s" "$QA_REDIS_URL" || printf memory:// )}" \
    SESSION_COOKIE_SECURE=False \
    WORKERS="$QA_GUNICORN_WORKERS" \
    GUNICORN_RUN_USER="$(id -un)" \
    GUNICORN_RUN_GROUP="$(id -gn)" \
    gunicorn -c gunicorn.conf.py \
      --pid "$SERVER_PIDFILE" \
      --bind "${QA_SERVER_HOST}:${QA_SERVER_PORT}" \
      app:app >"$SERVER_LOG" 2>&1 &
    SERVER_PID="$!"
    SERVER_STARTED="1"
  elif [ "$QA_SERVER_MODE" = "flask" ]; then
    SERVER_LOG="logs/qa_server.log"
    FLASK_ENV=testing \
    SECRET_KEY=test-secret \
    REDIS_URL="$QA_REDIS_URL" \
    SESSION_INVALIDATE_ON_RESTART="${SESSION_INVALIDATE_ON_RESTART:-false}" \
    SESSION_BOOT_ID="${SESSION_BOOT_ID:-}" \
    SESSION_TYPE="${SESSION_TYPE:-$( [ -n "$QA_REDIS_URL" ] && printf redis || printf filesystem )}" \
    SESSION_FILE_DIR="$QA_SESSION_DIR" \
    RATELIMIT_STORAGE_URL="${RATELIMIT_STORAGE_URL:-$( [ -n "$QA_REDIS_URL" ] && printf "%s" "$QA_REDIS_URL" || printf memory:// )}" \
    SESSION_COOKIE_SECURE=False \
    python app.py --host "$QA_SERVER_HOST" --port "$QA_SERVER_PORT" >"$SERVER_LOG" 2>&1 &
    SERVER_PID="$!"
    SERVER_STARTED="1"
  else
    echo "Unsupported QA_SERVER_MODE: ${QA_SERVER_MODE}" >&2
    exit 1
  fi

  for _ in $(seq 1 60); do
    if curl -sf "${BASE_URL}/login" >/dev/null 2>&1; then
      break
    fi
    sleep 1
  done

  if ! curl -sf "${BASE_URL}/login" >/dev/null 2>&1; then
    echo "QA server did not become healthy. See ${SERVER_LOG}" >&2
    exit 1
  fi
fi

if [ "$QA_INCLUDE_LINT" = "1" ]; then
  echo "Running QA lint"
  npm run qa:lint
fi

echo "Running Python QA"
npm run qa:python

export CYPRESS_BASE_URL="${BASE_URL}"
export PLAYWRIGHT_BASE_URL="${BASE_URL}"

if [ "$QA_INCLUDE_CYPRESS" = "1" ]; then
  echo "Running browser E2E"
  run_with_browser_log_filter npm run e2e:all
fi

if [ "$QA_INCLUDE_PLAYWRIGHT" = "1" ]; then
  echo "Running Playwright E2E"
  run_with_browser_log_filter npm run e2e:playwright
fi

if [ "$QA_INCLUDE_K6" = "1" ]; then
  if [ -z "$QA_K6_BIN" ]; then
    echo "Skipping k6 load check: k6 is not installed or not configured on PATH"
  else
    echo "Running k6 load check"
    if [ -n "$QA_REDIS_URL" ] && [ -z "${QA_K6_ENABLE_AUTH:-}" ]; then
      export QA_K6_ENABLE_AUTH=1
    fi
    npm run perf:k6
  fi
fi

echo "QA run completed successfully"
