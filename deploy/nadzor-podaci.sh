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
          restore-proba.timer fototeka-import.timer"

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

echo "###PROBA"
systemctl show restore-proba.service -p ExecMainStartTimestamp --value

echo "###KRAJ"
