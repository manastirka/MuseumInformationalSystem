#!/bin/bash
# Постави окидач рецензије: git кука + systemd тајмер.
# Покренути једном, на машини где су CLI-ји рецензената (dev).
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO"

echo "=== 1. git куке ==="
# ДВЕ куке, не једна. `post-merge` се пали само кад merge прође аутоматски;
# merge са конфликтом корисник завршава са `git commit`, што пали `post-commit`.
# Управо ти merge-еви — где је ручно спајање најризичније — иначе би
# систематски пролазили без рецензије и без трага.
# `red.py dodaj` је идемпотентан, па двострука пријава не смета.
TELO='#!/bin/bash
# МИС: сваки merge иде у ред за рецензију. Не рецензира одмах — тајмер то
# ради кад рецензент буде слободан, па merge никад не чека.
h="$(git rev-parse HEAD)"
if git rev-parse -q --verify "$h^2" >/dev/null 2>&1; then
    koren="$(git rev-parse --show-toplevel)"
    if ! python3 "$koren/scripts/review/red.py" dodaj "$h"; then
        # Неуспех уписа у ред се НЕ гута — иначе merge прође, рецензија
        # никад не буде заказана, и нигде нема трага.
        echo "УПОЗОРЕЊЕ: $h није уписан у ред за рецензију!" >&2
        echo "  Упиши ручно: python3 scripts/review/red.py dodaj $h" >&2
    fi
fi'

for kuka in post-merge post-commit; do
    printf '%s\n' "$TELO" > ".git/hooks/$kuka"
    chmod +x ".git/hooks/$kuka"
    echo "    .git/hooks/$kuka постављена"
done

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
