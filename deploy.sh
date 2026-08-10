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

echo "== 1/7 Backup pre deploja =="
systemctl start backup-nhmb.service

echo "== 2/7 Povlačenje koda (samo fast-forward) =="
PREV="$(sudo -u mis git -C "$APP" rev-parse HEAD)"

rollback() {
    echo "!! DEPLOY PAO — vraćam kod na ${PREV:0:12} i restartujem servis"
    sudo -u mis git -C "$APP" reset --hard "$PREV"
    sudo -u mis "$VENV/bin/pip" install -q -r "$APP/requirements.lock" || true
    systemctl restart mis || true
    if systemctl cat mis-fototeka-worker.service >/dev/null 2>&1; then
        systemctl restart mis-fototeka-worker || true
    fi
}
trap rollback ERR

sudo -u mis git -C "$APP" pull --ff-only

echo "== 3/7 Zavisnosti (pinovane, requirements.lock) =="
sudo -u mis "$VENV/bin/pip" install -r "$APP/requirements.lock" -q

echo "== 3b/7 Migracije šeme (SQL fajlovi iz migration/) =="
# Neinteraktivno, ali --database mora da se poklopi sa current_database() —
# runner odbija ako .env pokazuje na pogrešnu bazu.
sudo -u mis bash -c "cd $APP && $VENV/bin/python deploy/run_migrations.py apply --execute --database ${MIS_DB_NAME:-mis_db}"

echo "== 4/7 Sistemski fajlovi (systemd/nginx/logrotate) =="
install -m 755 "$APP/deploy/backup-nhmb.sh" /usr/local/bin/backup-nhmb.sh
install -m 755 "$APP/deploy/restore-proba.sh" /usr/local/bin/restore-proba.sh
for unit in backup-nhmb.service backup-nhmb.timer \
            restore-proba.service restore-proba.timer mis-alarm@.service \
            fototeka-import.service fototeka-import.timer \
            fototeka-fixity.service fototeka-fixity.timer \
            mis-fototeka-worker.service; do
    install -m 644 "$APP/deploy/$unit" "/etc/systemd/system/$unit"
done
systemctl daemon-reload
install -m 644 "$APP/deploy/logrotate-museum" /etc/logrotate.d/museum-info-system
if [[ -f "$NGINX_CONF" ]]; then
    install -m 644 "$APP/deploy/nginx_museum_prod.conf" "$NGINX_CONF"
    # nginx -t PRE reload-a: pokvaren konfig obara deploy (rollback), a živi
    # nginx nastavlja sa starim učitanim konfigom.
    nginx -t
    systemctl reload nginx
else
    echo "  (nginx: $NGINX_CONF ne postoji — prvo ručno usvajanje konfiga," \
         "vidi deploy/README.md; preskačem)"
fi

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
