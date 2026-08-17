#!/bin/bash
# Постави дневну проверу продукције на dev машини.
# Покренути једном, на машини која има ssh алијас prod-nadzor и ради 24/7.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
PY="$(command -v python3)"
UNITS="$HOME/.config/systemd/user"
mkdir -p "$UNITS"

echo "=== 1. проба да прод уопште одговара ==="
ssh -T prod-nadzor >/dev/null

echo "=== 2. systemd јединице (корисник) ==="
cat > "$UNITS/mis-nadzor.service" <<SERVIS
[Unit]
Description=МИС — дневна провера продукције
After=network-online.target

[Service]
Type=oneshot
WorkingDirectory=$REPO
ExecStart=$PY $REPO/scripts/nadzor/provera_proda.py
SERVIS

cat > "$UNITS/mis-nadzor.timer" <<TAJMER
[Unit]
Description=МИС — провера продукције сваког јутра у 08:00

[Timer]
OnCalendar=*-*-* 08:00:00
# Ако је машина била угашена, провера се обави при паљењу — иначе би
# изостала баш оног јутра кад је највише треба.
Persistent=true

[Install]
WantedBy=timers.target
TAJMER

systemctl --user daemon-reload
systemctl --user enable --now mis-nadzor.timer

echo "=== 3. linger (да тајмер ради и кад ниси пријављен) ==="
if loginctl show-user "$USER" -p Linger 2>/dev/null | grep -q "Linger=yes"; then
    echo "    већ укључен"
else
    echo "    НИЈЕ укључен — без овога провера ради само док си пријављен."
    echo "    Покрени:  sudo loginctl enable-linger $USER"
fi

echo
systemctl --user list-timers mis-nadzor.timer --no-pager | head -3
echo
echo "Ручно:        python3 scripts/nadzor/provera_proda.py"
echo "Последње:     cat ~/nadzor/POSLEDNJE.md"
echo "Има проблема: test -f ~/nadzor/PROBLEM && cat ~/nadzor/PROBLEM"
