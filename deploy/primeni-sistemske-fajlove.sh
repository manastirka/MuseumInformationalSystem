#!/bin/bash
# Усклађивање системских јединица на продукцији + провера аларма.
#
# ПОКРЕНУТИ КАО ROOT, на nhmb-srv01:
#     sudo bash /opt/mis/app/deploy/primeni-sistemske-fajlove.sh
#
# Claude ово не може сам: `sudo -n` му покрива само `deploy.sh` и `psql`.
#
# Шта ради:
#   1. снима затечене јединице (повратак у једном потезу)
#   2. инсталира репо верзије и проверава их `systemd-analyze verify`
#   3. ДОКАЗУЈЕ да аларм ради — намерно обори тест-јединицу и тражи маркер
#   4. одговара на отворено питање: да ли је /data/mis/media намерно
#      изостављен из бекапа
#
# Ништа не рестартује апликацију. Ако било шта пукне — стаје и каже шта.
set -uo pipefail

SNIMAK=/root/pre-uskladjivanja-$(date +%Y%m%d)
REPO=/opt/mis/app/deploy
JEDINICE=(backup-nhmb.service backup-nhmb.timer
          restore-proba.service restore-proba.timer
          mis-alarm@.service mis-fototeka-worker.service
          mis-vesti-uvoz.service mis-vesti-uvoz.timer
          mis-vesti-veb.service mis-vesti-veb.timer)

# Тајмери које треба укључити после инсталације (сервиси су oneshot и
# покрећу их тајмери, не systemctl enable на сервису).
TAJMERI_ZA_UKLJUCITI=(mis-vesti-uvoz.timer mis-vesti-veb.timer)

if [ "$(id -u)" -ne 0 ]; then
    echo "ОДБИЈЕНО: покрени као root (sudo bash $0)" >&2
    exit 1
fi

echo "=== 1/4 снимак затеченог стања → $SNIMAK ==="
mkdir -p "$SNIMAK"
for j in "${JEDINICE[@]}"; do
    if [ -f "/etc/systemd/system/$j" ]; then
        cp -a "/etc/systemd/system/$j" "$SNIMAK/" && echo "    сачувано: $j"
    fi
done
echo "    повратак:  cp -a $SNIMAK/. /etc/systemd/system/ && systemctl daemon-reload"

echo
echo "=== 2/4 инсталација репо верзија ==="
for j in "${JEDINICE[@]}"; do
    if [ ! -f "$REPO/$j" ]; then
        echo "    ПРЕСКАЧЕМ $j — нема га у репоу" >&2
        continue
    fi
    cp "$REPO/$j" /etc/systemd/system/ && echo "    инсталирано: $j"
done
systemctl daemon-reload

echo
echo "--- systemd-analyze verify ---"
for j in backup-nhmb.service restore-proba.service mis-alarm@.service; do
    izlaz=$(systemd-analyze verify "/etc/systemd/system/$j" 2>&1)
    if [ -n "$izlaz" ]; then
        echo "    $j: $izlaz"
    else
        echo "    $j: ОК"
    fi
done

echo
echo "=== 3/4 ДОКАЗ да аларм оставља траг ==="
rm -f /var/lib/mis/alarm/*proba-alarma* 2>/dev/null
systemctl start 'mis-alarm@proba-alarma.service' 2>&1 | sed 's/^/    /'
sleep 2
if ls /var/lib/mis/alarm/*proba-alarma* >/dev/null 2>&1; then
    echo "    МАРКЕР НАПРАВЉЕН:"
    ls -l /var/lib/mis/alarm/ | tail -3 | sed 's/^/      /'
    echo "    → јутарња провера са dev-а ће ово пријавити као нов аларм."
    echo "    → уклони пробни маркер ако не желиш да звони:"
    echo "      rm /var/lib/mis/alarm/*proba-alarma*"
else
    echo "    МАРКЕР НИЈЕ НАПРАВЉЕН — аларм не ради како треба." >&2
    systemctl status 'mis-alarm@proba-alarma.service' --no-pager --lines=15 | sed 's/^/      /'
fi

echo
echo "=== 4/4 одговор на отворено питање: /data/mis/media и бекап ==="
echo "Провером 17.08. утврђено да те гране НЕМА у /backup/current/data/mis,"
echo "док су cif_files, arhiva, share и fototeka_ulaz сви ту. Ево зашто:"
echo
if grep -nE "media|exclude|--exclude" /usr/local/bin/backup-nhmb.sh 2>/dev/null; then
    echo
    echo "→ Ако изнад стоји изричито искључење — намерно је, ништа не треба мењати."
    echo "  Ако не стоји ништа, `media` испада неким другим путем и то ваља погледати."
else
    echo "    (у скрипти нема ниједног помена 'media' ни 'exclude')"
    echo
    echo "→ Значи да изостанак НИЈЕ изричит. Погледај шта скрипта уопште копира:"
    echo "     grep -nE 'rsync|btrfs|cp |snapshot' /usr/local/bin/backup-nhmb.sh"
fi

echo
echo "=== стање тајмера ==="
echo
echo "=== укључивање тајмера за вести ==="
for t in "${TAJMERI_ZA_UKLJUCITI[@]}"; do
    if [ -f "/etc/systemd/system/$t" ]; then
        systemctl enable --now "$t" 2>&1 | sed 's/^/    /'
    else
        echo "    ПРЕСКАЧЕМ $t — није инсталиран" >&2
    fi
done

systemctl list-timers backup-nhmb.timer restore-proba.timer \
    mis-vesti-uvoz.timer mis-vesti-veb.timer --no-pager | head -6
echo
echo "Готово. Апликација није рестартована."
