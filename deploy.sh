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

# == Migracije šeme (odkomentarisati ako/kad projekat koristi Flask-Migrate) ==
# sudo -u mis bash -c "cd $APP && $VENV/bin/flask db upgrade"

echo "== 4/5 Restart aplikacije =="
systemctl restart mis
sleep 2

echo "== 5/5 Smoke test =="
curl -sfI http://127.0.0.1:8000 > /dev/null
echo "DEPLOY OK — $(sudo -u mis git -C "$APP" log -1 --oneline)"
