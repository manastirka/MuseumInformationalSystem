#!/usr/bin/env bash
#
# Noćni backup MIS-a na nhmb-srv01 (pokreće backup-nhmb.timer u 02:30).
# Instalacija: deploy/RUNBOOK-backup-nhmb.md (kopija u /usr/local/bin).
#
# Radi tri stvari, tim redom:
#   1. pg_dump žive baze (gz) u /backup/current/db/ + čišćenje starih dump-ova;
#   2. rsync OSVEŽAVANJE fajl-stabala u /backup/current/data/ i koda u
#      /backup/current/app/ — ovo je korak koji drži novu fototeku na DVA
#      diska (/data je /dev/sda1, /backup je /dev/sdb1); bez njega sve posle
#      poslednjeg ručnog rsync-a postoji samo na jednom disku;
#   3. btrfs readonly snimak /backup/current u /backup/.snapshots/<datum>.
#
# Posle rsync-a se piše MANIFEST.sha256 (broj fajlova + SHA-256 svakog fajla)
# — dokaz šta je te noći stvarno bilo u kopiji, i osnova za restore-probu.
#
# NAMERNO nema "|| true" na koracima koji čuvaju podatke: nepostojeći izvor,
# pukao rsync ili pg_dump OBARAJU job, a OnFailure= u jedinici šalje mejl.
#
set -euo pipefail

BACKUP_ROOT="${BACKUP_ROOT:-/backup}"
CURRENT="$BACKUP_ROOT/current"
SNAP_DIR="$BACKUP_ROOT/.snapshots"
LIVE_DB="${LIVE_DB:-mis_db}"
APP_DIR="${APP_DIR:-/opt/mis/app}"
DB_KEEP_DAYS="${DB_KEEP_DAYS:-14}"
SNAP_KEEP_DAYS="${SNAP_KEEP_DAYS:-30}"

# Fajl-stabla koja se preslikavaju u $CURRENT/data/ (putanja bez vodećeg /data).
SOURCES=(/data/arhiva /data/mis/dokumenti /data/mis/media /data/fototeka_ulaz)

STAMP="$(date +%Y-%m-%d)"
log() { echo "[backup-nhmb $(date '+%H:%M:%S')] $*"; }

mkdir -p "$CURRENT/db" "$CURRENT/data" "$CURRENT/app"

# --- 1) pg_dump ---------------------------------------------------------------
DUMP="$CURRENT/db/${LIVE_DB}_$(date +%Y%m%d).sql.gz"
log "pg_dump $LIVE_DB -> $DUMP"
pg_dump --no-owner "$LIVE_DB" | gzip > "$DUMP.tmp"
mv "$DUMP.tmp" "$DUMP"
find "$CURRENT/db" -name "${LIVE_DB}_*.sql.gz" -mtime +"$DB_KEEP_DAYS" -delete

# --- 2) rsync osvežavanje fajl-stabala ---------------------------------------
for src in "${SOURCES[@]}"; do
    if [[ ! -d "$src" ]]; then
        log "GRESKA: izvor $src ne postoji — backup NEPOTPUN, obaram job."
        exit 1
    fi
    dest="$CURRENT/data${src#/data}"
    mkdir -p "$dest"
    log "rsync $src/ -> $dest/"
    rsync -a --delete "$src/" "$dest/"
    src_count="$(find "$src" -type f | wc -l)"
    dest_count="$(find "$dest" -type f | wc -l)"
    log "  fajlova: izvor=$src_count kopija=$dest_count"
    if [[ "$src_count" != "$dest_count" ]]; then
        log "GRESKA: broj fajlova se ne poklapa za $src — obaram job."
        exit 1
    fi
done

log "rsync $APP_DIR/ -> $CURRENT/app/"
rsync -a --delete --exclude 'venv' --exclude '__pycache__' --exclude '.git' \
    "$APP_DIR/" "$CURRENT/app/"

# --- 2b) manifest (broj fajlova + SHA-256; traje par minuta na ~20 GB) -------
MANIFEST="$CURRENT/data/MANIFEST.sha256"
log "manifest -> $MANIFEST"
(cd "$CURRENT/data" \
    && find . -type f ! -name 'MANIFEST.sha256*' -print0 | sort -z \
     | xargs -0 -r sha256sum > MANIFEST.sha256.tmp)
MANIFEST_COUNT="$(wc -l < "$MANIFEST.tmp")"
{ echo "# backup-nhmb $STAMP — $MANIFEST_COUNT fajlova"; cat "$MANIFEST.tmp"; } > "$MANIFEST"
rm -f "$MANIFEST.tmp"
log "  manifest: $MANIFEST_COUNT fajlova"

# --- 3) btrfs readonly snimak -------------------------------------------------
mkdir -p "$SNAP_DIR"
if [[ -e "$SNAP_DIR/$STAMP" ]]; then
    log "snimak $SNAP_DIR/$STAMP već postoji — preskačem snapshot korak."
else
    log "btrfs snapshot -r $CURRENT -> $SNAP_DIR/$STAMP"
    btrfs subvolume snapshot -r "$CURRENT" "$SNAP_DIR/$STAMP"
fi
# Čišćenje snimaka starijih od $SNAP_KEEP_DAYS dana (imena su YYYY-MM-DD).
CUTOFF="$(date -d "-$SNAP_KEEP_DAYS days" +%Y-%m-%d)"
for snap in "$SNAP_DIR"/????-??-??; do
    [[ -e "$snap" ]] || continue
    if [[ "$(basename "$snap")" < "$CUTOFF" ]]; then
        log "brišem stari snimak $snap"
        btrfs subvolume delete "$snap"
    fi
done

log "gotovo: db=$(du -h "$DUMP" | cut -f1), data=$(du -sh "$CURRENT/data" | cut -f1)"
