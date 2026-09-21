#!/bin/bash
# Сакупљач стања продукције — ЈЕДИНА наредба коју надзорни кључ сме да покрене.
#
# У ~alukovic/.ssh/authorized_keys тај кључ стоји са
#   command="/home/alukovic/bin/nadzor-podaci.sh",restrict
# па dev машина, чак и ако јој неко узме кључ, не може да уради ништа друго
# на проду — ни шел, ни прослеђивање портова, ни сопствену наредбу.
#
# Правило за овај фајл: САМО читање. Ниједна наредба овде не сме да мења
# стање продукције. Ако икад затреба измена — не иде овуда.
#
# Излаз чита scripts/nadzor/provera_proda.py на dev-у.
set -u

JEDINICE="mis.service mis-fototeka-worker.service nginx.service postgresql.service
          backup-nhmb.service backup-nhmb.timer restore-proba.service
          restore-proba.timer fototeka-import.timer scisearch-web.service"

echo "###VREME"
date +%s

echo "###BEKAP"
ls -t /backup/current/db/*.sql.gz 2>/dev/null | head -1 | xargs -r stat -c '%Y %n'

echo "###PALE"
for j in $JEDINICE; do
    printf '%s %s\n' "$j" "$(systemctl is-failed "$j" 2>&1)"
done

echo "###MARKERI"
ls -1 /var/lib/mis/alarm/*.txt 2>/dev/null | tail -20

echo "###DISK"
df --output=target,pcent / /backup 2>/dev/null | tail -n +2

echo "###ZDRAVLJE"
curl -sk --max-time 10 https://127.0.0.1/healthz 2>/dev/null || echo NEDOSTUPNO

echo "###STABLA_PROD"
cd /data 2>/dev/null && find . -mindepth 1 -maxdepth 2 -type d -printf '%P\n' 2>/dev/null | sort

echo "###STABLA_BEKAP"
cd /backup/current/data 2>/dev/null && find . -mindepth 1 -maxdepth 2 -type d -printf '%P\n' 2>/dev/null | sort

echo "###GRESKE5XX"
# Одговори 5xx у последња 24 h. Грешка коју нико не гледа не постоји —
# 21.09.2026 је /admin/library_database враћао 500 а то се сазнало случајно.
for j in mis scisearch-web; do
    printf '%s %s\n' "$j" "$(journalctl -u "$j" --since '-24 hours' --no-pager 2>/dev/null | grep -cE '" 5[0-9][0-9] ')"
done

echo "###GRESKE5XX_PRIMERI"
journalctl -u mis --since '-24 hours' --no-pager 2>/dev/null | grep -oE '"[A-Z]+ [^"?]+[^"]*" 5[0-9][0-9]' | sed -E 's/\?[^"]*//' | sort | uniq -c | sort -rn | head -5

echo "###PROBA"
systemctl show restore-proba.service -p ExecMainStartTimestamp --value

echo "###KRAJ"
