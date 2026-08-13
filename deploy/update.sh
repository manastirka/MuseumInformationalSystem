#!/usr/bin/env bash
#
# One-command UPDATE of MuseumInfoSystem on a server from git.
# Pulls the latest code, installs pinned deps, applies any new DB migrations,
# restarts the service, and health-checks. Use this for every update AFTER the
# initial install. Re-running with no new commits is a safe no-op.
#
# (The FIRST install is different: git clone -> create .env -> restore the DB
#  from a pg_dump -> run_migrations.py baseline -> systemctl enable --now. See
#  README.md "Cutover checklist".)
#
set -euo pipefail

APP_DIR="${MUSEUM_APP_DIR:-/home/aleksandarlukovic/MuseumInfoSystem}"
BRANCH="${MUSEUM_GIT_BRANCH:-main}"
VENV="${MUSEUM_VENV:-$APP_DIR/venv}"
SERVICE="${MUSEUM_SERVICE:-museum-system}"
HEALTH_URL="${MUSEUM_HEALTH_URL:-https://localhost/healthz}"

cd "$APP_DIR"
log() { echo "[update $(date '+%H:%M:%S')] $*"; }

# Refuse to run on a dirty tree so a pull can never clobber local edits.
if ! git diff --quiet || ! git diff --cached --quiet; then
  log "ERROR: working tree has uncommitted changes; commit/stash them first."
  exit 1
fi

PREV="$(git rev-parse HEAD)"
log "git fetch + fast-forward $BRANCH"
git fetch --prune origin
git checkout "$BRANCH"
git pull --ff-only origin "$BRANCH"
NEW="$(git rev-parse HEAD)"

if [[ "$PREV" == "$NEW" ]]; then
  log "already up to date ($NEW); nothing to do."
  exit 0
fi
log "updating $PREV -> $NEW"

log "installing pinned dependencies"
"$VENV/bin/pip" install -q -r requirements.lock

log "applying any new database migrations"
"$VENV/bin/python" deploy/run_migrations.py apply --execute \
    --database "${MUSEUM_DB_NAME:-museum_system}"

log "restarting $SERVICE"
sudo systemctl restart "$SERVICE"

log "health check"
for _ in $(seq 1 15); do
  if curl -fsS -k "$HEALTH_URL" >/dev/null 2>&1; then
    log "healthy — update to $NEW complete."
    exit 0
  fi
  sleep 2
done

log "WARNING: health check did not pass. Inspect 'journalctl -u $SERVICE -n 50'."
log "To roll back the code: git reset --hard $PREV && sudo systemctl restart $SERVICE"
exit 1
