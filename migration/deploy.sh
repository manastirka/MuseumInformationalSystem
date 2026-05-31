#!/usr/bin/env bash
# =============================================================================
# Museum Information System - Automated Deployment Script for Fedora
# =============================================================================
# This script fully automates the deployment of the Museum Information System
# on a fresh Fedora installation. It will:
#
#   1.  Ask for the system username and password (only interactive part)
#   2.  Install all system packages (dnf)
#   3.  Create the application user (if needed)
#   4.  Initialize PostgreSQL and create the database
#   5.  Apply all database schemas and import data
#   6.  Set up Python virtual environment and install dependencies
#   7.  Generate .env configuration
#   8.  Configure Gunicorn
#   9.  Generate self-signed SSL certificates
#   10. Configure Nginx
#   11. Install and enable the systemd service
#   12. Configure SELinux and firewall
#   13. Start all services and verify
#
# Usage:
#   sudo bash migration/deploy.sh
#
# Requirements:
#   - Fedora Linux (tested on 39-41)
#   - Root/sudo access
#   - The extracted deployment archive (run prepare_archive.sh first)
# =============================================================================

set -euo pipefail

# ── Colors and logging ───────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

log()     { echo -e "${GREEN}[✓]${NC} $1"; }
warn()    { echo -e "${YELLOW}[!]${NC} $1"; }
err()     { echo -e "${RED}[✗]${NC} $1"; }
info()    { echo -e "${BLUE}[i]${NC} $1"; }
step()    { echo -e "\n${CYAN}${BOLD}═══ $1 ═══${NC}"; }
substep() { echo -e "  ${BLUE}→${NC} $1"; }

# Track errors for final summary
WARNINGS=()
add_warning() { WARNINGS+=("$1"); }

# ── Pre-flight checks ───────────────────────────────────────────────────────

if [[ $EUID -ne 0 ]]; then
    err "This script must be run as root (use: sudo bash migration/deploy.sh)"
    exit 1
fi

# Detect script and app location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ ! -f "$SOURCE_DIR/app.py" ]]; then
    err "app.py not found in $SOURCE_DIR"
    err "Run this script from inside the extracted deployment archive."
    exit 1
fi

# Check we're on Fedora
if [[ ! -f /etc/fedora-release ]]; then
    warn "This doesn't look like Fedora. The script may still work on RHEL/CentOS."
    read -rp "Continue anyway? [y/N]: " CONTINUE
    [[ "$CONTINUE" =~ ^[Yy]$ ]] || exit 0
fi

FEDORA_VERSION=$(rpm -E %fedora 2>/dev/null || echo "unknown")

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║       Museum Information System - Automated Deployment      ║"
echo "║       Target: Fedora $FEDORA_VERSION                                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ── Step 1: Ask for username and password ────────────────────────────────────

step "Step 1/13: User Configuration"

echo ""
echo -e "${BOLD}Enter the system username that will run the Museum application.${NC}"
echo "If the user doesn't exist, it will be created."
echo ""

read -rp "Username: " APP_USER

if [[ -z "$APP_USER" ]]; then
    err "Username cannot be empty"
    exit 1
fi

# Validate username format
if ! [[ "$APP_USER" =~ ^[a-z_][a-z0-9_-]*$ ]]; then
    err "Invalid username. Use lowercase letters, numbers, hyphens, underscores."
    exit 1
fi

echo ""
echo -e "${BOLD}Enter a password for the PostgreSQL database and the admin web account.${NC}"
echo "Requirements: 12+ chars, uppercase, lowercase, number, special char (!@#\$%^&*)"
echo ""

while true; do
    read -rsp "Password: " APP_PASSWORD
    echo ""

    # Validate password
    PW_ERRORS=()
    if [[ ${#APP_PASSWORD} -lt 12 ]]; then
        PW_ERRORS+=("Must be at least 12 characters")
    fi
    if ! [[ "$APP_PASSWORD" =~ [A-Z] ]]; then
        PW_ERRORS+=("Must contain an uppercase letter")
    fi
    if ! [[ "$APP_PASSWORD" =~ [a-z] ]]; then
        PW_ERRORS+=("Must contain a lowercase letter")
    fi
    if ! [[ "$APP_PASSWORD" =~ [0-9] ]]; then
        PW_ERRORS+=("Must contain a number")
    fi
    if ! [[ "$APP_PASSWORD" =~ [^a-zA-Z0-9] ]]; then
        PW_ERRORS+=("Must contain a special character")
    fi

    if [[ ${#PW_ERRORS[@]} -gt 0 ]]; then
        err "Password does not meet requirements:"
        for e in "${PW_ERRORS[@]}"; do
            echo -e "    ${RED}•${NC} $e"
        done
        echo ""
        continue
    fi

    read -rsp "Confirm password: " APP_PASSWORD_CONFIRM
    echo ""

    if [[ "$APP_PASSWORD" != "$APP_PASSWORD_CONFIRM" ]]; then
        err "Passwords do not match. Try again."
        echo ""
        continue
    fi

    break
done

log "Username: $APP_USER"
log "Password: validated"

# Derived paths
APP_HOME="/home/$APP_USER"
APP_DIR="$APP_HOME/MuseumInfoSystem"
VENV_DIR="$APP_DIR/venv"
DB_NAME="museum_system"

echo ""
info "Application will be installed to: $APP_DIR"
info "PostgreSQL database: $DB_NAME"
echo ""
read -rp "Proceed with installation? [Y/n]: " PROCEED
[[ "$PROCEED" =~ ^[Nn]$ ]] && { echo "Aborted."; exit 0; }

# ── Step 2: Install System Packages ─────────────────────────────────────────

step "Step 2/13: Installing System Packages"

substep "Updating package cache..."
dnf makecache --quiet 2>/dev/null || true

PACKAGES=(
    # Python
    python3 python3-pip python3-devel

    # Build tools
    gcc gcc-c++ make redhat-rpm-config

    # PostgreSQL
    postgresql-server postgresql-contrib postgresql-devel

    # Nginx
    nginx

    # Libraries for Python packages
    libjpeg-turbo-devel zlib-devel libffi-devel
    libxml2-devel libxslt-devel
    openssl-devel

    # GDAL for rasterio/GIS
    gdal gdal-devel

    # Utilities
    openssl curl policycoreutils-python-utils
)

substep "Installing packages (this may take a few minutes)..."
dnf install -y "${PACKAGES[@]}" 2>&1 | tail -1
log "System packages installed"

# ── Step 3: Create Application User ─────────────────────────────────────────

step "Step 3/13: Setting Up Application User"

if id "$APP_USER" &>/dev/null; then
    log "User '$APP_USER' already exists"
else
    substep "Creating user '$APP_USER'..."
    useradd -m -s /bin/bash "$APP_USER"
    log "User '$APP_USER' created"
fi

# Ensure home directory exists and has correct permissions
chmod 755 "$APP_HOME"

# ── Step 4: Deploy Application Files ────────────────────────────────────────

step "Step 4/13: Deploying Application Files"

if [[ -d "$APP_DIR" ]]; then
    warn "Directory $APP_DIR already exists"
    BACKUP_SUFFIX="backup_$(date +%Y%m%d_%H%M%S)"
    substep "Backing up existing installation to ${APP_DIR}.${BACKUP_SUFFIX}"
    mv "$APP_DIR" "${APP_DIR}.${BACKUP_SUFFIX}"
fi

substep "Copying application files to $APP_DIR..."
cp -r "$SOURCE_DIR" "$APP_DIR"

# Create required directories
mkdir -p "$APP_DIR/logs"
mkdir -p "$APP_DIR/flask_session"
mkdir -p "$APP_DIR/exports/timesheets"
mkdir -p "$APP_DIR/storage/uploads"
mkdir -p "$APP_DIR/static/uploads"
mkdir -p "$APP_DIR/data"

# Set ownership
chown -R "$APP_USER:$APP_USER" "$APP_DIR"
log "Application files deployed to $APP_DIR"

# ── Step 5: Initialize PostgreSQL ────────────────────────────────────────────

step "Step 5/13: Initializing PostgreSQL"

# Check if PostgreSQL is already initialized
PG_DATA="/var/lib/pgsql/data"
if [[ ! -f "$PG_DATA/PG_VERSION" ]]; then
    substep "Initializing PostgreSQL data directory..."
    postgresql-setup --initdb 2>/dev/null || {
        # Fedora 40+ uses a different method
        postgresql-setup --initdb --unit postgresql 2>/dev/null || true
    }
    log "PostgreSQL initialized"
else
    log "PostgreSQL already initialized"
fi

# Configure PostgreSQL authentication
PG_HBA="$PG_DATA/pg_hba.conf"
if [[ -f "$PG_HBA" ]]; then
    substep "Configuring PostgreSQL authentication..."

    # Back up original
    cp "$PG_HBA" "${PG_HBA}.backup.$(date +%Y%m%d)"

    # Replace ident/peer with md5 for local connections, keep peer for postgres user
    # This allows password-based auth for our app user
    cat > "$PG_HBA" <<'PGHBA'
# PostgreSQL Client Authentication Configuration
# TYPE  DATABASE    USER            ADDRESS         METHOD

# "local" is for Unix domain socket connections only
local   all         postgres                        peer
local   all         all                             md5

# IPv4 local connections
host    all         all             127.0.0.1/32    md5

# IPv6 local connections
host    all         all             ::1/128         md5
PGHBA

    log "PostgreSQL authentication configured (md5)"
fi

# Start PostgreSQL
substep "Starting PostgreSQL..."
systemctl enable postgresql
systemctl restart postgresql

# Wait for PostgreSQL to be ready
for i in $(seq 1 15); do
    if sudo -u postgres pg_isready -q 2>/dev/null; then
        break
    fi
    sleep 1
done

if ! sudo -u postgres pg_isready -q 2>/dev/null; then
    err "PostgreSQL failed to start"
    journalctl -u postgresql --no-pager -n 20
    exit 1
fi
log "PostgreSQL is running"

# ── Step 6: Create Database and Import Data ──────────────────────────────────

step "Step 6/13: Setting Up Database"

# Create PostgreSQL user
substep "Creating PostgreSQL user '$APP_USER'..."
sudo -u postgres psql -c "
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$APP_USER') THEN
            CREATE ROLE $APP_USER WITH LOGIN PASSWORD '$(echo "$APP_PASSWORD" | sed "s/'/''/g")' CREATEDB;
            RAISE NOTICE 'Role created';
        ELSE
            ALTER ROLE $APP_USER WITH PASSWORD '$(echo "$APP_PASSWORD" | sed "s/'/''/g")';
            RAISE NOTICE 'Role updated';
        END IF;
    END
    \$\$;
" 2>/dev/null
log "PostgreSQL user configured"

# Create database
substep "Creating database '$DB_NAME'..."
if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    warn "Database '$DB_NAME' already exists — skipping creation"
else
    sudo -u postgres createdb -O "$APP_USER" "$DB_NAME"
    log "Database '$DB_NAME' created"
fi

# Grant permissions
sudo -u postgres psql -d "$DB_NAME" -c "GRANT ALL ON SCHEMA public TO $APP_USER;" 2>/dev/null

# Install PostgreSQL extensions (need superuser)
substep "Installing PostgreSQL extensions..."
sudo -u postgres psql -d "$DB_NAME" <<'EXTSQL'
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;
-- PostGIS is optional: it may not be installed on all systems
DO $$
BEGIN
    CREATE EXTENSION IF NOT EXISTS postgis;
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'PostGIS not available — geographic features will be limited';
END $$;
EXTSQL
log "PostgreSQL extensions installed"

# Check if we have a full database dump (with data)
if [[ -f "$APP_DIR/museum_system_full.sql" ]]; then
    substep "Importing full database dump (schemas + data)..."
    sudo -u postgres psql -d "$DB_NAME" -f "$APP_DIR/museum_system_full.sql" 2>&1 | tail -5
    log "Full database dump imported"
else
    # Apply schemas one by one
    substep "Applying database schemas..."

    SCHEMA_ORDER=(
        "db/schema.sql"
        "db/schema_phase3a.sql"
        "db/rruff_schema.sql"
        "db/schema_collections.sql"
        "db/schema_vehicles.sql"
        "db/schema_timesheet_complete.sql"
        "db/schema_news_articles.sql"
    )

    for schema_file in "${SCHEMA_ORDER[@]}"; do
        if [[ -f "$APP_DIR/$schema_file" ]]; then
            substep "Applying $schema_file..."
            # Use the app user for schemas since extensions are already created
            PGPASSWORD="$APP_PASSWORD" psql -U "$APP_USER" -h 127.0.0.1 -d "$DB_NAME" \
                -f "$APP_DIR/$schema_file" 2>&1 | grep -E "^(ERROR|NOTICE)" | head -5 || true
        else
            warn "Schema file not found: $schema_file"
        fi
    done

    log "Database schemas applied"

    # Insert default roles (required by the auth system)
    substep "Inserting default roles..."
    PGPASSWORD="$APP_PASSWORD" psql -U "$APP_USER" -h 127.0.0.1 -d "$DB_NAME" <<'ROLESQL'
INSERT INTO roles (name, description) VALUES
    ('admin', 'System administrator with full access'),
    ('employee', 'Museum employee with standard access'),
    ('curator', 'Collection curator with extended access'),
    ('viewer', 'Read-only viewer')
ON CONFLICT (name) DO NOTHING;
ROLESQL
    log "Default roles created"
fi

# Apply incremental migration scripts (001_*, 002_*, etc.)
MIGRATION_SQL_FILES=$(find "$APP_DIR/migration" -maxdepth 1 -name '*.sql' -type f 2>/dev/null | sort)
if [[ -n "$MIGRATION_SQL_FILES" ]]; then
    substep "Applying incremental migration scripts..."
    while IFS= read -r sql_file; do
        substep "Applying $(basename "$sql_file")..."
        PGPASSWORD="$APP_PASSWORD" psql -U "$APP_USER" -h 127.0.0.1 -d "$DB_NAME" \
            -f "$sql_file" 2>&1 | grep -E "^(ERROR|NOTICE)" | head -3 || true
    done <<< "$MIGRATION_SQL_FILES"
    log "Incremental migrations applied"
else
    info "No incremental migration SQL files found — skipping"
fi

# Grant all table permissions to app user
substep "Granting table permissions..."
sudo -u postgres psql -d "$DB_NAME" -c "
    GRANT ALL ON ALL TABLES IN SCHEMA public TO $APP_USER;
    GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO $APP_USER;
    GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO $APP_USER;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $APP_USER;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $APP_USER;
" 2>/dev/null
log "Database permissions granted"

# ── Step 7: Python Virtual Environment ───────────────────────────────────────

step "Step 7/13: Setting Up Python Environment"

substep "Creating virtual environment..."
sudo -u "$APP_USER" python3 -m venv "$VENV_DIR"

substep "Upgrading pip..."
sudo -u "$APP_USER" "$VENV_DIR/bin/pip" install --upgrade pip setuptools wheel 2>&1 | tail -1

substep "Installing Python dependencies (this may take a few minutes)..."

# Try full install first; if rasterio fails, install without it then retry
if sudo -u "$APP_USER" "$VENV_DIR/bin/pip" install -r "$APP_DIR/requirements.txt" 2>&1 | tail -3; then
    log "All Python dependencies installed"
else
    warn "Some packages failed. Retrying without rasterio..."
    grep -v rasterio "$APP_DIR/requirements.txt" > "$APP_DIR/requirements_minimal.txt"
    sudo -u "$APP_USER" "$VENV_DIR/bin/pip" install -r "$APP_DIR/requirements_minimal.txt" 2>&1 | tail -3

    # Try rasterio separately with --no-binary
    substep "Attempting rasterio with system GDAL..."
    if sudo -u "$APP_USER" "$VENV_DIR/bin/pip" install --no-binary rasterio rasterio 2>/dev/null; then
        log "rasterio installed with system GDAL"
    else
        add_warning "rasterio could not be installed — GIS/terrain features will be unavailable"
        warn "rasterio not installed (GIS features will be limited)"
    fi

    rm -f "$APP_DIR/requirements_minimal.txt"
    log "Python dependencies installed (with fallbacks)"
fi

# Verify critical packages
CRITICAL_PKGS=(flask psycopg gunicorn bcrypt)
MISSING_PKGS=()
for pkg in "${CRITICAL_PKGS[@]}"; do
    if ! sudo -u "$APP_USER" "$VENV_DIR/bin/python3" -c "import $pkg" 2>/dev/null; then
        MISSING_PKGS+=("$pkg")
    fi
done

if [[ ${#MISSING_PKGS[@]} -gt 0 ]]; then
    err "Critical packages missing: ${MISSING_PKGS[*]}"
    err "Try installing manually: $VENV_DIR/bin/pip install ${MISSING_PKGS[*]}"
    exit 1
fi
log "Critical packages verified: ${CRITICAL_PKGS[*]}"

# ── Step 8: Generate .env Configuration ──────────────────────────────────────

step "Step 8/13: Generating Configuration"

SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

cat > "$APP_DIR/.env" <<ENVFILE
# Museum Information System Configuration
# Generated by deploy.sh on $(date '+%Y-%m-%d %H:%M:%S')

# Flask
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=$SECRET_KEY

# PostgreSQL Database
DATABASE_URL=postgresql+psycopg://$APP_USER:$APP_PASSWORD@localhost:5432/$DB_NAME

# Legacy MySQL settings (unused when DATABASE_URL is set)
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=museum_timesheet_local
DB_CHARSET=utf8mb4

# Security
WTF_CSRF_ENABLED=True
WTF_CSRF_TIME_LIMIT=3600
SESSION_TYPE=filesystem
SESSION_PERMANENT=False
SESSION_USE_SIGNER=True
SESSION_KEY_PREFIX=museum:
PERMANENT_SESSION_LIFETIME=28800
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# Rate Limiting
RATELIMIT_ENABLED=True
RATELIMIT_STORAGE_URL=memory://

# Password Policy
PASSWORD_MIN_LENGTH=12
PASSWORD_REQUIRE_UPPERCASE=True
PASSWORD_REQUIRE_LOWERCASE=True
PASSWORD_REQUIRE_NUMBERS=True
PASSWORD_REQUIRE_SPECIAL=True

# Account Security
MAX_LOGIN_ATTEMPTS=5
ACCOUNT_LOCKOUT_DURATION=1800
SESSION_TIMEOUT_WARNING=300

# Auth
AUTH_SYSTEM_ENABLED=True
ENABLE_FALLBACK_AUTH=False
REQUIRE_PASSWORD_CHANGE_ON_FIRST_LOGIN=True
ADMIN_EMAIL=admin@nhmbeo.rs
ADMIN_DEFAULT_PASSWORD=$APP_PASSWORD

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/museum_info_system.log
LOG_FORMAT=json
LOG_MAX_BYTES=10485760
LOG_BACKUP_COUNT=10

# Server
HOST=0.0.0.0
PORT=5555
WORKERS=4

# File Upload
MAX_CONTENT_LENGTH=52428800
UPLOAD_FOLDER=storage/uploads
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,pdf,xlsx,csv

# Redis/Caching (optional)
REDIS_URL=redis://localhost:6379/0
CACHE_TYPE=simple
CACHE_DEFAULT_TIMEOUT=300
CACHE_KEY_PREFIX=museum_cache:

# Email (configure for your SMTP server)
MAIL_SERVER=
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=

# Sentry (optional)
SENTRY_DSN=

# Backup
BACKUP_ENABLED=True
BACKUP_DIRECTORY=/var/backups/museum
BACKUP_RETENTION_DAYS=30
ENVFILE

# Secure the .env file
chown "$APP_USER:$APP_USER" "$APP_DIR/.env"
chmod 600 "$APP_DIR/.env"

log ".env configuration generated"

# ── Step 9: Configure Gunicorn ───────────────────────────────────────────────

step "Step 9/13: Configuring Gunicorn"

cat > "$APP_DIR/gunicorn.conf.py" <<GUNICORN
# Gunicorn configuration - Generated by deploy.sh
import os
import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = min(4, multiprocessing.cpu_count() * 2 + 1)
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 2

# Restart workers to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
loglevel = 'info'
accesslog = 'logs/gunicorn_access.log'
errorlog = 'logs/gunicorn_error.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'museum_info_system'

# Server mechanics
daemon = False
pidfile = '/tmp/museum_info_system.pid'
user = '$APP_USER'
group = '$APP_USER'
tmp_upload_dir = None

# Preload application
preload_app = True
graceful_timeout = 120

# Server hooks
def on_starting(server):
    server.log.info("Museum Information System starting...")

def on_reload(server):
    server.log.info("Museum Information System reloading...")

def when_ready(server):
    server.log.info("Museum Information System ready to serve requests")

def on_exit(server):
    server.log.info("Museum Information System shutting down")

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)
GUNICORN

chown "$APP_USER:$APP_USER" "$APP_DIR/gunicorn.conf.py"
log "Gunicorn configured (workers: auto-detected based on CPU count)"

# ── Step 10: Generate SSL Certificates ───────────────────────────────────────

step "Step 10/13: Setting Up SSL Certificates"

SSL_CERT="/etc/ssl/certs/museum_cert.pem"
SSL_KEY="/etc/ssl/private/museum_key.pem"

if [[ -f "$SSL_CERT" && -f "$SSL_KEY" ]]; then
    log "SSL certificates already exist — keeping existing"
else
    substep "Generating self-signed SSL certificate..."
    mkdir -p /etc/ssl/private

    # Get the machine's IP address for the certificate
    MACHINE_IP=$(hostname -I | awk '{print $1}' || echo "127.0.0.1")
    MACHINE_HOSTNAME=$(hostname -f 2>/dev/null || hostname)

    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "$SSL_KEY" \
        -out "$SSL_CERT" \
        -subj "/C=RS/ST=Belgrade/L=Belgrade/O=Museum/CN=$MACHINE_HOSTNAME" \
        -addext "subjectAltName=IP:$MACHINE_IP,IP:127.0.0.1,DNS:localhost,DNS:$MACHINE_HOSTNAME" \
        2>/dev/null

    chmod 600 "$SSL_KEY"
    chmod 644 "$SSL_CERT"

    log "Self-signed SSL certificate generated for $MACHINE_IP"
    add_warning "Using self-signed SSL certificate. Replace with a proper certificate for production."
fi

# ── Step 11: Configure Nginx ─────────────────────────────────────────────────

step "Step 11/13: Configuring Nginx"

# Detect machine IP
MACHINE_IP=$(hostname -I | awk '{print $1}' || echo "127.0.0.1")

cat > /etc/nginx/conf.d/museum.conf <<NGINX
# Museum Information System - Nginx Configuration
# Generated by deploy.sh on $(date '+%Y-%m-%d %H:%M:%S')

upstream museum_app {
    server 127.0.0.1:8000 fail_timeout=0;
}

# Rate limiting zones
limit_req_zone \$binary_remote_addr zone=museum_limit:10m rate=10r/s;
limit_req_zone \$binary_remote_addr zone=login_limit:10m rate=1r/s;

# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name $MACHINE_IP localhost;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name $MACHINE_IP localhost;

    # SSL Configuration
    ssl_certificate     $SSL_CERT;
    ssl_certificate_key $SSL_KEY;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5:!RC4;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    server_tokens off;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    client_max_body_size 50M;

    root $APP_DIR;

    access_log /var/log/nginx/museum_access.log;
    error_log  /var/log/nginx/museum_error.log;

    # Static files
    location /static {
        alias $APP_DIR/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
        add_header X-Content-Type-Options "nosniff" always;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    # Rate limit login endpoint
    location /login {
        limit_req zone=login_limit burst=3 nodelay;
        proxy_pass http://museum_app;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Main application
    location / {
        limit_req zone=museum_limit burst=20 nodelay;
        proxy_pass http://museum_app;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_connect_timeout 60s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;

        proxy_buffering on;
        proxy_buffer_size 16k;
        proxy_buffers 16 64k;
        proxy_busy_buffers_size 128k;
    }

    # Deny access to hidden files and sensitive paths
    location ~ /\\. { deny all; access_log off; log_not_found off; }
    location ~ \\.(env|json|py|pyc|ini|cfg|conf|log|sql|db|sqlite)\$ {
        deny all; access_log off; log_not_found off;
    }
}
NGINX

# Remove default nginx page if it conflicts
rm -f /etc/nginx/conf.d/default.conf 2>/dev/null || true

# Test nginx configuration
if nginx -t 2>&1 | grep -q "successful"; then
    log "Nginx configuration valid"
else
    err "Nginx configuration test failed:"
    nginx -t
    exit 1
fi

# ── Step 12: Systemd Service & SELinux & Firewall ────────────────────────────

step "Step 12/13: Installing Systemd Service, SELinux, Firewall"

# Write systemd service file
substep "Installing systemd service..."
cat > /etc/systemd/system/museum-system.service <<SERVICE
[Unit]
Description=Museum Information System - Gunicorn
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=exec
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin:$APP_HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"
Environment="FLASK_ENV=production"
Environment="PYTHONPATH=$APP_DIR"
ExecStartPre=/bin/mkdir -p /run/museum
ExecStart=$VENV_DIR/bin/python3 -m gunicorn --config gunicorn.conf.py wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=35
Restart=always
RestartSec=10

# Security hardening
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
NoNewPrivileges=true
ReadWritePaths=$APP_DIR/data
ReadWritePaths=$APP_DIR/logs
ReadWritePaths=$APP_DIR/exports
ReadWritePaths=$APP_DIR/static/uploads
ReadWritePaths=$APP_DIR/flask_session
ReadWritePaths=$APP_DIR/storage
ReadWritePaths=/run/museum
RuntimeDirectory=museum

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable museum-system
log "Systemd service installed and enabled"

# SELinux
substep "Configuring SELinux..."
if command -v getenforce &>/dev/null && [[ "$(getenforce)" != "Disabled" ]]; then
    # Allow nginx to proxy to gunicorn
    setsebool -P httpd_can_network_connect 1 2>/dev/null || true

    # Label static files for nginx
    semanage fcontext -a -t httpd_sys_content_t "$APP_DIR/static(/.*)?" 2>/dev/null || true
    restorecon -Rv "$APP_DIR/static" 2>/dev/null || true

    # Allow reading from the app home
    setsebool -P httpd_read_user_content 1 2>/dev/null || true

    log "SELinux configured"
else
    info "SELinux is disabled or not installed — skipping"
fi

# Firewall
substep "Configuring firewall..."
if command -v firewall-cmd &>/dev/null && systemctl is-active --quiet firewalld; then
    firewall-cmd --permanent --add-service=http  2>/dev/null || true
    firewall-cmd --permanent --add-service=https 2>/dev/null || true
    firewall-cmd --reload 2>/dev/null || true
    log "Firewall: HTTP and HTTPS ports opened"
else
    info "firewalld not running — skipping firewall configuration"
    add_warning "Firewall not configured. Open ports 80/443 manually if needed."
fi

# Create backup directory
mkdir -p /var/backups/museum
chown "$APP_USER:$APP_USER" /var/backups/museum

# ── Step 13: Create Admin User and Start Services ────────────────────────────

step "Step 13/13: Creating Admin User and Starting Services"

# Create the admin user in PostgreSQL using the app's own Python code
substep "Creating admin user in database..."
sudo -u "$APP_USER" bash -c "
    cd '$APP_DIR'
    source '$VENV_DIR/bin/activate'
    python3 -c \"
import os, sys
os.environ['DATABASE_URL'] = 'postgresql+psycopg://$APP_USER:$(echo "$APP_PASSWORD" | sed "s/'/\\\\'/g")@localhost:5432/$DB_NAME'

# Check if users table has any rows
import psycopg
from psycopg.rows import dict_row

pg_url = os.environ['DATABASE_URL'].replace('postgresql+psycopg://', 'postgresql://')

try:
    with psycopg.connect(pg_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) as cnt FROM users')
            count = cur.fetchone()['cnt']
            if count > 0:
                print(f'Users table already has {count} users — skipping admin creation')
                sys.exit(0)
except Exception as e:
    print(f'Note: {e}')

# Create admin user using the app auth system
try:
    from security_utils import PasswordHasher
    hasher = PasswordHasher()
    pw_hash, salt = hasher.hash_password('$APP_PASSWORD')

    with psycopg.connect(pg_url) as conn:
        with conn.cursor() as cur:
            # Ensure admin role exists
            cur.execute(\\\"SELECT id FROM roles WHERE name = 'admin'\\\")
            role = cur.fetchone()
            if role is None:
                cur.execute(\\\"INSERT INTO roles (name, description) VALUES ('admin', 'System administrator') RETURNING id\\\")
                role_id = cur.fetchone()[0]
            else:
                role_id = role[0]

            cur.execute('''
                INSERT INTO users (email, password_hash, salt, full_name, role_id, position, is_active, is_first_login, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, TRUE, TRUE, NOW(), NOW())
                ON CONFLICT (email) DO NOTHING
            ''', ('admin@nhmbeo.rs', pw_hash, salt, 'System Administrator', role_id, 'Administrator'))
            conn.commit()
            print('Admin user created: admin@nhmbeo.rs')
except Exception as e:
    print(f'Warning: Could not create admin user: {e}')
    print('You can create it manually after deployment.')
\"
" 2>&1 | while read -r line; do substep "$line"; done

# Start services
substep "Starting museum-system service..."
systemctl start museum-system

substep "Starting nginx..."
systemctl enable nginx
systemctl restart nginx

# Wait a moment and verify
sleep 3

# ── Final Verification ───────────────────────────────────────────────────────

echo ""
echo -e "${CYAN}${BOLD}═══ Verification ═══${NC}"

CHECKS_PASSED=0
CHECKS_TOTAL=4

# Check PostgreSQL
if sudo -u postgres pg_isready -q 2>/dev/null; then
    log "PostgreSQL: running"
    ((CHECKS_PASSED++))
else
    err "PostgreSQL: not running"
fi

# Check museum-system service
if systemctl is-active --quiet museum-system; then
    log "Museum service: running"
    ((CHECKS_PASSED++))
else
    err "Museum service: not running"
    warn "Check logs: journalctl -u museum-system -n 30"
fi

# Check Gunicorn listening
if ss -tlnp 2>/dev/null | grep -q ":8000"; then
    log "Gunicorn: listening on port 8000"
    ((CHECKS_PASSED++))
else
    err "Gunicorn: not listening on port 8000"
fi

# Check Nginx
if systemctl is-active --quiet nginx; then
    log "Nginx: running"
    ((CHECKS_PASSED++))
else
    err "Nginx: not running"
fi

# Detect IP
MACHINE_IP=$(hostname -I | awk '{print $1}' || echo "127.0.0.1")

# ── Summary ──────────────────────────────────────────────────────────────────

echo ""
echo -e "${GREEN}${BOLD}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              DEPLOYMENT COMPLETE ($CHECKS_PASSED/$CHECKS_TOTAL checks passed)               ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                                                             ║"
printf "║  URL:       %-46s ║\n" "https://$MACHINE_IP/"
printf "║  Login:     %-46s ║\n" "admin@nhmbeo.rs"
printf "║  Password:  %-46s ║\n" "(the password you entered)"
echo "║                                                             ║"
printf "║  App dir:   %-46s ║\n" "$APP_DIR"
printf "║  Database:  %-46s ║\n" "postgresql://$APP_USER@localhost/$DB_NAME"
printf "║  Logs:      %-46s ║\n" "$APP_DIR/logs/"
echo "║                                                             ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  Useful commands:                                           ║"
echo "║                                                             ║"
echo "║  sudo systemctl status museum-system    # App status        ║"
echo "║  sudo systemctl restart museum-system   # Restart app       ║"
echo "║  sudo journalctl -u museum-system -f    # Live logs         ║"
echo "║  sudo systemctl status nginx            # Nginx status      ║"
echo "║  sudo systemctl status postgresql       # DB status         ║"
echo "║                                                             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Print warnings if any
if [[ ${#WARNINGS[@]} -gt 0 ]]; then
    echo -e "${YELLOW}${BOLD}Warnings:${NC}"
    for w in "${WARNINGS[@]}"; do
        echo -e "  ${YELLOW}!${NC} $w"
    done
    echo ""
fi
