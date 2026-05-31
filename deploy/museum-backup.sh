#!/usr/bin/env bash
#
# Nightly backup for MuseumInfoSystem:
#   * PostgreSQL database (custom-format dump)
#   * flat-file domain data still on disk + schema/migrations
#   * (optional) secrets: .env and data/.mail_key
# then copies everything OFF-BOX to your personal Google Drive (rclone 'gdrive:')
# and prunes old copies by age.
#
# Portable: every path/target is an env var with a sensible default, so the SAME
# script runs on this machine now and on the new server. Run it as the user that
# owns the rclone config (here: aleksandarlukovic) so Google Drive is reachable.
#
set -euo pipefail

APP_DIR="${MUSEUM_APP_DIR:-$HOME/MuseumInfoSystem}"
BACKUP_DIR="${MUSEUM_BACKUP_DIR:-$APP_DIR/backups}"
GDRIVE_REMOTE="${MUSEUM_BACKUP_GDRIVE_REMOTE:-gdrive:MuseumBackups}"
LOCAL_KEEP_DAYS="${MUSEUM_BACKUP_LOCAL_KEEP_DAYS:-7}"
DRIVE_KEEP_DAYS="${MUSEUM_BACKUP_DRIVE_KEEP_DAYS:-30}"
INCLUDE_SECRETS="${MUSEUM_BACKUP_INCLUDE_SECRETS:-0}"

STAMP="$(date +%Y%m%d_%H%M%S)"
log() { echo "[museum-backup $(date '+%H:%M:%S')] $*"; }

mkdir -p "$BACKUP_DIR"

# --- load DATABASE_URL from .env (only what we need; safe against spaces/globs) ---
if [[ -f "$APP_DIR/.env" ]] && [[ -z "${DATABASE_URL:-}" ]]; then
  DATABASE_URL="$(grep -m1 '^DATABASE_URL=' "$APP_DIR/.env" \
    | sed 's/^DATABASE_URL=//; s/\r$//; s/^["'\'']//; s/["'\'']$//')"
  export DATABASE_URL
fi
: "${DATABASE_URL:?DATABASE_URL is not set (check $APP_DIR/.env)}"

# psycopg-style URL -> libpq URL that pg_dump understands
PG_URL="${DATABASE_URL/postgresql+psycopg:\/\//postgresql:\/\/}"

# --- 1) PostgreSQL dump (custom format = compressed + selective restore) ---
DUMP="$BACKUP_DIR/museum_db_${STAMP}.dump"
log "pg_dump -> $DUMP"
pg_dump --format=custom --no-owner --dbname="$PG_URL" --file="$DUMP"

# --- 2) flat-file domain data still on disk + schema/migrations (small) ---
DATA_TAR="$BACKUP_DIR/museum_files_${STAMP}.tar.gz"
log "files -> $DATA_TAR"
tar -czf "$DATA_TAR" -C "$APP_DIR" \
  --ignore-failed-read \
  Sanja/sanja_paleogene_neogene_mammals.json \
  data/digitized_profiles.json \
  data/geo_zones \
  db migration 2>/dev/null || true

# --- 3) optional secrets (sensitive!) — only when explicitly enabled ---
if [[ "$INCLUDE_SECRETS" == "1" ]]; then
  SECRETS_TAR="$BACKUP_DIR/museum_secrets_${STAMP}.tar.gz"
  log "secrets -> $SECRETS_TAR"
  tar -czf "$SECRETS_TAR" -C "$APP_DIR" --ignore-failed-read .env data/.mail_key 2>/dev/null || true
fi

# --- 4) copy this run off-box to personal Google Drive ---
log "rclone copy -> $GDRIVE_REMOTE"
rclone mkdir "$GDRIVE_REMOTE" 2>/dev/null || true
rclone copy "$BACKUP_DIR" "$GDRIVE_REMOTE" --include "museum_*_${STAMP}.*" --transfers 2

# --- 5) prune old copies (local + drive) by age ---
find "$BACKUP_DIR" -name 'museum_*' -type f -mtime +"$LOCAL_KEEP_DAYS" -delete 2>/dev/null || true
rclone delete "$GDRIVE_REMOTE" --min-age "${DRIVE_KEEP_DAYS}d" --include 'museum_*' 2>/dev/null || true

log "done ($STAMP). DB=$(du -h "$DUMP" | cut -f1), files=$(du -h "$DATA_TAR" | cut -f1)"
