#!/bin/bash
# Постави окидач рецензије: git кука + systemd тајмер.
# Покренути једном, на машини где су CLI-ји рецензената (dev).
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO"

echo "=== 1. git кука после merge-а ==="
cat > .git/hooks/post-merge <<'KUKA'
#!/bin/bash
# МИС: сваки merge иде у ред за рецензију. Не рецензира одмах — тајмер
# то ради кад рецензент буде слободан, па merge никад не чека.
h="$(git rev-parse HEAD)"
if git rev-parse -q --verify "$h^2" >/dev/null 2>&1; then
    python3 "$(git rev-parse --show-toplevel)/scripts/review/red.py" dodaj "$h" || true
fi
KUKA
chmod +x .git/hooks/post-merge
echo "    .git/hooks/post-merge постављена"

echo "=== 2. systemd тајмер (корисник, на сваких 15 min) ==="
UNITS="$HOME/.config/systemd/user"
mkdir -p "$UNITS"

PY="$REPO/venv/bin/python"
[ -x "$PY" ] || PY="$(command -v python3)"

cat > "$UNITS/mis-recenzija.service" <<SERVIS
[Unit]
Description=МИС — обрада реда рецензија
After=network-online.target

[Service]
Type=oneshot
WorkingDirectory=$REPO
ExecStart=$PY $REPO/scripts/review/red.py obradi
SERVIS

cat > "$UNITS/mis-recenzija.timer" <<TAJMER
[Unit]
Description=МИС — покушај рецензије на сваких 15 минута

[Timer]
OnBootSec=5min
OnUnitActiveSec=15min
Persistent=true

[Install]
WantedBy=timers.target
TAJMER

systemctl --user daemon-reload
systemctl --user enable --now mis-recenzija.timer
echo "    тајмер укључен"

echo "=== 3. linger (да тајмер ради и кад ниси пријављен) ==="
if loginctl show-user "$USER" -p Linger 2>/dev/null | grep -q "Linger=yes"; then
    echo "    већ укључен"
else
    sudo loginctl enable-linger "$USER" && echo "    укључен"
fi

echo
echo "=== стање ==="
systemctl --user list-timers mis-recenzija.timer --no-pager | head -3
echo
echo "Провера реда:  python3 scripts/review/red.py pregled"
