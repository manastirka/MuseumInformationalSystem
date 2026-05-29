# Gunicorn configuration file for Museum Information System

import os
import multiprocessing

LOG_DIR = os.path.abspath(os.environ.get('LOG_DIR', 'logs'))

# Server socket
# Keep Gunicorn private behind nginx by default; allow explicit override via env.
bind = os.environ.get('GUNICORN_BIND', '127.0.0.1:8000')
backlog = 2048

# Worker processes
# NOTE: with in-memory rate limiting (default), login throttling is per-worker.
# Set RATELIMIT_STORAGE_URL to a Redis URL if using multiple workers.
workers = int(os.environ.get('WORKERS', '1'))
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
loglevel = 'info'
accesslog = os.path.join(LOG_DIR, 'gunicorn_access.log')
errorlog = os.path.join(LOG_DIR, 'gunicorn_error.log')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'museum_info_system'

# Server mechanics
daemon = False
pidfile = os.environ.get('GUNICORN_PIDFILE', '/run/museum/museum_info_system.pid')
user = os.environ.get('GUNICORN_RUN_USER') or None
group = os.environ.get('GUNICORN_RUN_GROUP') or None
tmp_upload_dir = None

# SSL (for production)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'

# Environment
# Don't override environment variables - let systemd service file control them
# raw_env = [
#     'FLASK_ENV=production',
# ]

# Preload application
preload_app = True

# Worker timeout (single definition - removed duplicate from line 15)
graceful_timeout = 120

# Server hooks
def on_starting(server):
    server.log.info("🏛️ Museum Information System starting...")

def on_reload(server):
    server.log.info("🔄 Museum Information System reloading...")

def when_ready(server):
    server.log.info("✅ Museum Information System ready to serve requests")

def on_exit(server):
    server.log.info("👋 Museum Information System shutting down")


# Create log directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)
