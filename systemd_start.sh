#!/bin/bash

set -euo pipefail

cd /home/aleksandarlukovic/MuseumInfoSystem

PYTHON_BIN="/usr/bin/python3"
if [ -x "venv/bin/python" ]; then
    PYTHON_BIN="$(pwd)/venv/bin/python"
fi

# Preserve service-level overrides so .env cannot accidentally redirect
# production runtime paths back into the developer workspace.
SERVICE_LOG_DIR="${LOG_DIR:-}"
SERVICE_LOG_FILE="${LOG_FILE:-}"
SERVICE_GUNICORN_BIND="${GUNICORN_BIND:-}"
SERVICE_GUNICORN_PIDFILE="${GUNICORN_PIDFILE:-}"
SERVICE_GUNICORN_RUN_USER="${GUNICORN_RUN_USER:-}"
SERVICE_GUNICORN_RUN_GROUP="${GUNICORN_RUN_GROUP:-}"

load_env_file() {
    "${PYTHON_BIN}" - <<'PY'
import re
import shlex
import sys
from pathlib import Path

env_path = Path('.env')
if not env_path.exists():
    sys.exit(0)

assignment_re = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

def strip_inline_comment(value: str) -> str:
    in_single = False
    in_double = False
    for idx, char in enumerate(value):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == '#' and not in_single and not in_double:
            if idx == 0 or value[idx - 1].isspace():
                return value[:idx].rstrip()
    return value.strip()

for raw_line in env_path.read_text(encoding='utf-8').splitlines():
    line = raw_line.strip()
    if not line or line.startswith('#'):
        continue
    if '=' not in line:
        continue
    key, value = line.split('=', 1)
    key = key.strip()
    if not assignment_re.match(key):
        continue
    value = strip_inline_comment(value.strip())
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        value = value[1:-1]
    print(f"export {key}={shlex.quote(value)}")
PY
}

if [ -f ".env" ]; then
    eval "$(load_env_file)"
fi

[ -n "${SERVICE_LOG_DIR}" ] && export LOG_DIR="${SERVICE_LOG_DIR}"
[ -n "${SERVICE_LOG_FILE}" ] && export LOG_FILE="${SERVICE_LOG_FILE}"
[ -n "${SERVICE_GUNICORN_BIND}" ] && export GUNICORN_BIND="${SERVICE_GUNICORN_BIND}"
[ -n "${SERVICE_GUNICORN_PIDFILE}" ] && export GUNICORN_PIDFILE="${SERVICE_GUNICORN_PIDFILE}"
[ -n "${SERVICE_GUNICORN_RUN_USER}" ] && export GUNICORN_RUN_USER="${SERVICE_GUNICORN_RUN_USER}"
[ -n "${SERVICE_GUNICORN_RUN_GROUP}" ] && export GUNICORN_RUN_GROUP="${SERVICE_GUNICORN_RUN_GROUP}"

export FLASK_ENV=production
export FLASK_DEBUG=False
export GUNICORN_BIND="${GUNICORN_BIND:-127.0.0.1:8000}"
export GUNICORN_PIDFILE="${GUNICORN_PIDFILE:-/run/museum/museum_info_system.pid}"
export LOG_DIR="${LOG_DIR:-/var/log/museum-info-system}"
export LOG_FILE="${LOG_FILE:-${LOG_DIR}/museum_info_system.log}"
export SESSION_TYPE=redis
export SESSION_INVALIDATE_ON_RESTART="${SESSION_INVALIDATE_ON_RESTART:-false}"
if [ "${SESSION_INVALIDATE_ON_RESTART}" = "true" ]; then
    export SESSION_BOOT_ID="${SESSION_BOOT_ID:-$(date +%s%N)}"
fi

if [ -z "${REDIS_URL:-}" ]; then
    echo "REDIS_URL must be set for production startup" >&2
    exit 1
fi

if [ -z "${SECRET_KEY:-}" ]; then
    echo "SECRET_KEY must be set for production startup" >&2
    exit 1
fi

if [ -z "${MAIL_SETTINGS_ENCRYPTION_KEY:-}" ] && [ -r "data/.mail_key" ]; then
    export MAIL_SETTINGS_ENCRYPTION_KEY="$(tr -d '\r\n' < data/.mail_key)"
fi

if [ -z "${MAIL_SETTINGS_ENCRYPTION_KEY:-}" ]; then
    echo "WARNING: MAIL_SETTINGS_ENCRYPTION_KEY is not set and data/.mail_key is missing; encrypted mail credential features will remain unavailable until the key is configured." >&2
fi

export RATELIMIT_STORAGE_URL="${RATELIMIT_STORAGE_URL:-${REDIS_URL}}"

mkdir -p "${LOG_DIR}"
rm -f "${GUNICORN_PIDFILE}"

exec "${PYTHON_BIN}" -m gunicorn --config gunicorn.conf.py wsgi:application
