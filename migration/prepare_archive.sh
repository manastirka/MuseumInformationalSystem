#!/usr/bin/env bash
# =============================================================================
# Museum Information System - Prepare Deployment Archive
# =============================================================================
# Run this on the SOURCE machine to create a complete deployment package.
# The output archive can then be transferred to the target Fedora system
# and deployed using deploy.sh.
#
# Usage: bash migration/prepare_archive.sh [output_directory]
# =============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err()  { echo -e "${RED}[✗]${NC} $1"; }
info() { echo -e "${BLUE}[i]${NC} $1"; }
step() { echo -e "\n${CYAN}=== $1 ===${NC}"; }

# Resolve paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="${1:-$HOME}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
ARCHIVE_NAME="museum_system_deploy_${TIMESTAMP}"
WORK_DIR="$(mktemp -d)"

trap 'rm -rf "$WORK_DIR"' EXIT

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     Museum Information System - Archive Builder             ║"
echo "║     Preparing deployment package from: $APP_DIR             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ── Step 1: Validate source ──────────────────────────────────────────────────

step "Step 1/5: Validating source installation"

if [[ ! -f "$APP_DIR/app.py" ]]; then
    err "app.py not found in $APP_DIR — are you in the right directory?"
    exit 1
fi
log "Application directory: $APP_DIR"

if [[ ! -d "$APP_DIR/db" ]]; then
    err "db/ schema directory not found"
    exit 1
fi
log "Schema files found: $(ls "$APP_DIR"/db/*.sql 2>/dev/null | wc -l) SQL files"

if [[ ! -f "$APP_DIR/requirements.txt" ]]; then
    err "requirements.txt not found"
    exit 1
fi
log "requirements.txt found"

# ── Step 2: Export PostgreSQL database ───────────────────────────────────────

step "Step 2/5: Exporting PostgreSQL database"

PG_DUMP_FILE="$WORK_DIR/museum_system_full.sql"

if command -v pg_dump &>/dev/null; then
    # Try to detect the database URL
    if [[ -f "$APP_DIR/.env" ]]; then
        DB_URL=$(grep -oP 'DATABASE_URL=\K.*' "$APP_DIR/.env" 2>/dev/null || true)
    fi

    # Extract database name from URL (default: museum_system)
    # URL format: postgresql+psycopg://user@localhost:5432/dbname
    DB_NAME="museum_system"
    if [[ -n "${DB_URL:-}" ]]; then
        DB_NAME=$(echo "$DB_URL" | sed -E 's|.*/([^?]+)$|\1|' || echo "museum_system")
    fi

    info "Dumping PostgreSQL database: $DB_NAME"

    if pg_dump "$DB_NAME" > "$PG_DUMP_FILE" 2>/dev/null; then
        DUMP_SIZE=$(du -h "$PG_DUMP_FILE" | cut -f1)
        log "PostgreSQL dump created: $DUMP_SIZE"
    else
        warn "pg_dump failed — trying with sudo -u postgres..."
        if sudo -u postgres pg_dump "$DB_NAME" > "$PG_DUMP_FILE" 2>/dev/null; then
            DUMP_SIZE=$(du -h "$PG_DUMP_FILE" | cut -f1)
            log "PostgreSQL dump created: $DUMP_SIZE"
        else
            warn "Could not dump PostgreSQL. Schemas will still be included."
            warn "You will need to manually export: pg_dump $DB_NAME > museum_system_full.sql"
            rm -f "$PG_DUMP_FILE"
        fi
    fi
else
    warn "pg_dump not found — skipping database export"
    warn "Install postgresql and run: pg_dump museum_system > museum_system_full.sql"
fi

# ── Step 3: Build the archive file list ──────────────────────────────────────

step "Step 3/5: Building file list"

STAGING="$WORK_DIR/staging"
mkdir -p "$STAGING/museum_deploy"
DEST="$STAGING/museum_deploy"

# Copy application code (Python files)
info "Copying application code..."
rsync -a --include='*.py' --include='*/' --exclude='__pycache__' \
    --exclude='venv/' --exclude='.venv/' --exclude='*.pyc' \
    --exclude='localSQLtesting/' \
    "$APP_DIR"/*.py "$DEST/" 2>/dev/null || true

# Copy key config files
info "Copying configuration files..."
for f in requirements.txt .env.example .gitignore gunicorn.conf.py wsgi.py; do
    [[ -f "$APP_DIR/$f" ]] && cp "$APP_DIR/$f" "$DEST/"
done

# Copy DB schemas
info "Copying database schemas..."
cp -r "$APP_DIR/db" "$DEST/db"

# Copy migration scripts (ourselves)
cp -r "$APP_DIR/migration" "$DEST/migration"

# Copy templates
if [[ -d "$APP_DIR/templates" ]]; then
    info "Copying templates..."
    cp -r "$APP_DIR/templates" "$DEST/templates"
fi

# Copy static files
if [[ -d "$APP_DIR/static" ]]; then
    info "Copying static assets..."
    cp -r "$APP_DIR/static" "$DEST/static"
fi

# Copy nginx and service configs
for f in nginx_museum.conf museum-system.service; do
    [[ -f "$APP_DIR/$f" ]] && cp "$APP_DIR/$f" "$DEST/"
done

# Copy data directory (JSON files and SQLite databases, skip huge CIF data)
if [[ -d "$APP_DIR/data" ]]; then
    info "Copying data directory (excluding cif_files, mail_cache)..."
    rsync -a \
        --exclude='cif_files/' \
        --exclude='mail_cache/' \
        --exclude='dem_serbia/' \
        "$APP_DIR/data/" "$DEST/data/"
fi

# Copy PrirodnjackiMuzej (mineral database subsystem)
if [[ -d "$APP_DIR/PrirodnjackiMuzej" ]]; then
    info "Copying PrirodnjackiMuzej subsystem..."
    rsync -a \
        --exclude='venv/' \
        --exclude='__pycache__/' \
        --exclude='logs/' \
        "$APP_DIR/PrirodnjackiMuzej/" "$DEST/PrirodnjackiMuzej/"
fi

# Copy storage (uploaded images)
if [[ -d "$APP_DIR/storage" ]]; then
    info "Copying storage directory..."
    cp -r "$APP_DIR/storage" "$DEST/storage"
fi

# Copy exports structure
mkdir -p "$DEST/exports/timesheets"

# Copy PostgreSQL dump into archive
if [[ -f "$PG_DUMP_FILE" ]]; then
    cp "$PG_DUMP_FILE" "$DEST/museum_system_full.sql"
fi

# Create empty required directories
mkdir -p "$DEST/logs"
mkdir -p "$DEST/flask_session"

# ── Step 4: Calculate sizes ──────────────────────────────────────────────────

step "Step 4/5: Archive summary"

TOTAL_FILES=$(find "$DEST" -type f | wc -l)
TOTAL_SIZE=$(du -sh "$DEST" | cut -f1)

log "Total files: $TOTAL_FILES"
log "Total size (uncompressed): $TOTAL_SIZE"

echo ""
info "Directory breakdown:"
du -sh "$DEST"/*/ 2>/dev/null | sort -rh | head -15

# ── Step 5: Create compressed archive ────────────────────────────────────────

step "Step 5/5: Creating compressed archive"

ARCHIVE_PATH="$OUTPUT_DIR/${ARCHIVE_NAME}.tar.gz"

info "Compressing to: $ARCHIVE_PATH"
tar czf "$ARCHIVE_PATH" -C "$STAGING" museum_deploy

ARCHIVE_SIZE=$(du -h "$ARCHIVE_PATH" | cut -f1)

echo ""
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ARCHIVE READY                            ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                                                             ║"
printf "║  File: %-52s ║\n" "$ARCHIVE_PATH"
printf "║  Size: %-52s ║\n" "$ARCHIVE_SIZE"
printf "║  Files: %-51s ║\n" "$TOTAL_FILES"
echo "║                                                             ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  Next steps:                                                ║"
echo "║                                                             ║"
echo "║  1. Copy archive to target machine:                         ║"
echo "║     scp $ARCHIVE_NAME.tar.gz user@target:~/"
echo "║                                                             ║"
echo "║  2. On target machine, extract and run:                     ║"
echo "║     tar xzf $ARCHIVE_NAME.tar.gz"
echo "║     cd museum_deploy                                        ║"
echo "║     sudo bash migration/deploy.sh                           ║"
echo "║                                                             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
