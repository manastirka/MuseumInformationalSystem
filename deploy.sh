#!/bin/bash
# deploy.sh — MIS deploy na produkciju (nhmb-srv01)
# Poziv: sudo /usr/local/bin/deploy.sh
set -euo pipefail

APP=/opt/mis/app
VENV=/opt/mis/venv

echo "== 1/5 Backup pre deploja =="
systemctl start backup-nhmb.service

echo "== 2/5 Povlačenje koda (samo fast-forward) =="
sudo -u mis git -C "$APP" pull --ff-only

echo "== 3/5 Zavisnosti =="
sudo -u mis "$VENV/bin/pip" install -r "$APP/requirements.txt" -q

echo "== 3b/5 Migracije šeme (SQL fajlovi iz migration/) =="
sudo -u mis bash -c "cd $APP && $VENV/bin/python deploy/run_migrations.py apply"

echo "== 4/5 Restart aplikacije =="
systemctl restart mis
sleep 2

echo "== 4b/5 Restart Fototeka worker =="
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
        exit 1
    fi
else
    echo "  (mis-fototeka-worker nije instaliran — preskacem)"
fi

echo "== 5/5 Smoke test =="
curl -sfI http://127.0.0.1:8000 > /dev/null
echo "DEPLOY OK — $(sudo -u mis git -C "$APP" log -1 --oneline)"
