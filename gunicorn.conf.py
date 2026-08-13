# Gunicorn configuration file for Museum Information System

import os
import multiprocessing

LOG_DIR = os.path.abspath(os.environ.get('LOG_DIR', 'logs'))

# Server socket
# Keep Gunicorn private behind nginx by default; allow explicit override via env.
bind = os.environ.get('GUNICORN_BIND', '127.0.0.1:8000')
backlog = 2048

# Worker processes
# NOTE: rate limiting prati REDIS_URL čim je podešen (deljen preko svih
# workera); memory:// (per-worker) važi samo bez Redisa — sa WORKERS > 1
# ProductionConfig to odbija na startu.
workers = int(os.environ.get('WORKERS', '1'))
# gthread umesto sync: rute za slike (serve_derivat/serve_raw) su kratke -
# provera prava + DB upit, a sam prenos fajla ide preko nginx X-Accel-Redirect
# (FOTOTEKA_XACCEL). Sa sync worker-om jedna galerija (do 60 thumbnaila) drzi
# sve workere zauzete dok se fajlovi strimuju; gthread dozvoljava da jedan
# worker paralelno servisira vise takvih kratkih zahteva bez cene dodatnih
# procesa (preload deli kod, ali svaki proces ipak nosi svoj overhead).
# threads=4 x WORKERS=4 = 16 istovremenih slotova; DB pool (max 10/worker)
# pokriva 4 niti po worker-u. Broj niti je konzervativan - I/O-vezane kratke
# rute, ne CPU-vezan posao (obrada slika je u zasebnom fototeka_worker-u).
worker_class = os.environ.get('GUNICORN_WORKER_CLASS', 'gthread')
threads = int(os.environ.get('GUNICORN_THREADS', '4'))
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
