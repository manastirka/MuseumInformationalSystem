#!/bin/bash
# deploy.sh — MIS deploy na produkciju (nhmb-srv01)
# Poziv: sudo /usr/local/bin/deploy.sh
# Na neuspeh bilo kog koraka posle povlačenja koda: automatski rollback na
# prethodni commit + restart servisa (trap ERR).
set -euo pipefail

APP=/opt/mis/app
VENV=/opt/mis/venv
HEALTH_URL="${MIS_HEALTH_URL:-https://localhost/healthz}"
NGINX_CONF="${MIS_NGINX_CONF:-/etc/nginx/conf.d/mis.conf}"
DB_NAME="${MIS_DB_NAME:-mis_db}"
BACKUP_DIR="${MIS_PREDEPLOY_BACKUP_DIR:-/backup}"
PRE_DUMP=""
MIG_LOG=""

echo "== 1/7 Backup pre deploja =="
systemctl start backup-nhmb.service

echo "== 2/7 Povlačenje koda (samo fast-forward) =="
PREV="$(sudo -u mis git -C "$APP" rev-parse HEAD)"

# Snimak živog nginx konfiga pre deploja — rollback vraća i njega ako ga je
# deploj u međuvremenu menjao (ne samo kod).
NGINX_PRE=""
if [[ -f "$NGINX_CONF" ]]; then
    NGINX_PRE="$(mktemp /tmp/mis-nginx-pre.XXXXXX)"
    cp "$NGINX_CONF" "$NGINX_PRE"
fi

rollback() {
    echo "!! DEPLOY PAO — vraćam kod na ${PREV:0:12} i restartujem servis"
    sudo -u mis git -C "$APP" reset --hard "$PREV"
    sudo -u mis "$VENV/bin/pip" install -q -r "$APP/requirements.lock" || true
    # Kod je vraćen. Migracije idu u JEDNOJ transakciji (run_migrations.py):
    # ako je pao sam korak migracija, MIG_LOG je prazan i šema je netaknuta;
    # ako je pao neki KASNIJI korak (smoke), migracije su već commit-ovane
    # i šema je ispred koda. Restore baze je Aleksandrova odluka, deploy ga
    # NIKAD ne radi sam.
    if [[ -n "${MIG_LOG:-}" && -s "$MIG_LOG" ]]; then
        echo "!! ======================================================="
        echo "!! PAŽNJA: ŠEMA BAZE JE ISPRED KODA. U ovom pokušaju su"
        echo "!! primenjene (i commit-ovane) sledeće migracije:"
        sed 's/^/!!     /' "$MIG_LOG"
        echo "!! Baza NIJE automatski vraćena. Ako je restore potreban,"
        echo "!! ručno (posle provere šta je smoke oborio):"
        echo "!!     sudo -u postgres pg_restore --clean --if-exists -d $DB_NAME $PRE_DUMP"
        echo "!! Snimak stanja pre migracija: $PRE_DUMP"
        echo "!! ======================================================="
    elif [[ -n "${PRE_DUMP:-}" && -f "$PRE_DUMP" ]]; then
        echo "!! Nijedna migracija nije primenjena u ovom pokušaju — šema"
        echo "!! odgovara vraćenom kodu (snimak: $PRE_DUMP)."
    fi
    if [[ -n "$NGINX_PRE" && -f "$NGINX_PRE" && -f "$NGINX_CONF" ]] \
            && ! diff -q "$NGINX_PRE" "$NGINX_CONF" >/dev/null 2>&1; then
        echo "!! vraćam nginx konfig na stanje pre deploja"
        install -m 644 "$NGINX_PRE" "$NGINX_CONF"
        if nginx -t; then
            systemctl reload nginx || true
        fi
    fi
    systemctl restart mis || true
    if systemctl cat mis-fototeka-worker.service >/dev/null 2>&1; then
        systemctl restart mis-fototeka-worker || true
    fi
}
trap rollback ERR

sudo -u mis git -C "$APP" pull --ff-only

echo "== 3/7 Zavisnosti (pinovane, requirements.lock) =="
sudo -u mis "$VENV/bin/pip" install -r "$APP/requirements.lock" -q

echo "== 3a/7 Snimak baze pre migracija (pg_dump) =="
# Migracije se commit-uju pojedinačno i nemaju undo — ovaj snimak je jedini
# put nazad ako migracija prođe a smoke test padne.
NEW_SHA="$(sudo -u mis git -C "$APP" rev-parse HEAD)"
PRE_DUMP="$BACKUP_DIR/pre-deploy-${NEW_SHA:0:12}.dump"
install -d -m 755 "$BACKUP_DIR"
sudo -u postgres pg_dump -Fc "$DB_NAME" > "$PRE_DUMP"
echo "  snimak: $PRE_DUMP"

echo "== 3b/7 Migracije šeme (SQL fajlovi iz migration/) =="
# Neinteraktivno, ali --database mora da se poklopi sa current_database() —
# runner odbija ako .env pokazuje na pogrešnu bazu. --applied-log pamti šta
# je ovaj pokušaj stvarno primenio, za rollback poruku.
MIG_LOG="$(mktemp /tmp/mis-migracije-primenjene.XXXXXX)"
chown mis "$MIG_LOG"
sudo -u mis bash -c "cd $APP && $VENV/bin/python deploy/run_migrations.py apply --execute --database $DB_NAME --applied-log $MIG_LOG"

echo "== 4/7 Sistemski fajlovi (systemd/nginx/logrotate) =="
# PROD primerak je AUTORITATIVAN za backup-nhmb.sh, restore-proba.sh i
# $NGINX_CONF — repo kopije su rekonstrukcije po opisu (referenca, ne izvor;
# vidi deploy/README.md). Deploy ih zato NE prepisuje: samo prijavi razliku,
# bez izmene i bez prekida deploja.
warn_if_differs() {
    local repo="$1" live="$2"
    if [[ ! -f "$repo" ]]; then
        echo "  UPOZORENJE: $repo ne postoji u repou — nema reference za poređenje"
    elif [[ ! -f "$live" ]]; then
        echo "  UPOZORENJE: $live ne postoji — repo referenca: $repo" \
             "(ručno usvajanje, vidi deploy/README.md)"
    elif ! diff -q "$repo" "$live" >/dev/null; then
        echo "  UPOZORENJE: $live se razlikuje od repo kopije ($repo) —" \
             "NE prepisujem, prod primerak je autoritativan"
    fi
}
warn_if_differs "$APP/deploy/backup-nhmb.sh"          /usr/local/bin/backup-nhmb.sh
warn_if_differs "$APP/deploy/restore-proba.sh"        /usr/local/bin/restore-proba.sh
warn_if_differs "$APP/deploy/nginx_museum_prod.conf"  "$NGINX_CONF"

# Systemd jedinice: instaliraju se samo kad nema šta da se pregazi — nova
# jedinica (živi fajl ne postoji) ili identičan sadržaj. Razišla živa
# jedinica se NE prepisuje, samo upozorenje.
for unit in backup-nhmb.service backup-nhmb.timer \
            restore-proba.service restore-proba.timer mis-alarm@.service \
            fototeka-import.service fototeka-import.timer \
            fototeka-fixity.service fototeka-fixity.timer \
            mis-vesti-uvoz.service mis-vesti-uvoz.timer \
            mis-vesti-veb.service mis-vesti-veb.timer \
            mis-fototeka-worker.service; do
    repo_unit="$APP/deploy/$unit"
    live_unit="/etc/systemd/system/$unit"
    if [[ ! -f "$repo_unit" ]]; then
        echo "  UPOZORENJE: $repo_unit ne postoji u repou — preskačem"
    elif [[ ! -f "$live_unit" ]]; then
        install -m 644 "$repo_unit" "$live_unit"
        echo "  instalirana nova jedinica: $unit"
    elif diff -q "$repo_unit" "$live_unit" >/dev/null; then
        install -m 644 "$repo_unit" "$live_unit"
    else
        echo "  UPOZORENJE: $live_unit se razlikuje od repo kopije —" \
             "NE prepisujem, prod primerak je autoritativan"
    fi
done
systemctl daemon-reload
install -m 644 "$APP/deploy/logrotate-museum" /etc/logrotate.d/museum-info-system

echo "== 5/7 Restart aplikacije =="
systemctl restart mis

echo "== 5b/7 Restart Fototeka worker =="
# The Фototeka worker is a long-lived sibling service; without restarting it,
# it keeps running the previous code after a deploy (derivati/fixity logic can
# silently lag the web app). Guarded so a host without the unit still deploys.
if systemctl cat mis-fototeka-worker.service >/dev/null 2>&1; then
    systemctl restart mis-fototeka-worker
    sleep 1
    if systemctl is-active --quiet mis-fototeka-worker; then
        echo "  fototeka worker: aktivan"
    else
        echo "  GRESKA: mis-fototeka-worker nije aktivan posle restarta"
        journalctl -u mis-fototeka-worker -n 20 --no-pager || true
        false
    fi
else
    echo "  (mis-fototeka-worker nije instaliran — preskacem)"
fi

echo "== 6/7 Smoke test (/healthz kroz nginx, do 30 s) =="
# /healthz dira PostgreSQL i Redis — za razliku od "/", pada kad je baza
# mrtva. Petlja retrija umesto fiksnog sleep-a: gunicorn radnicima treba
# promenljivo vreme da se podignu.
HEALTHY=0
for _ in $(seq 1 15); do
    if curl -fsS -k "$HEALTH_URL" > /dev/null 2>&1; then
        HEALTHY=1
        break
    fi
    sleep 2
done
if [[ "$HEALTHY" != "1" ]]; then
    echo "GRESKA: $HEALTH_URL nije prošao — pokrećem rollback"
    false
fi

trap - ERR
echo "== 7/7 Gotovo =="
echo "DEPLOY OK — $(sudo -u mis git -C "$APP" log -1 --oneline)"
