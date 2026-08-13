#!/usr/bin/env bash
#
# Mesečna proba vraćanja backupa (restore drill) — REPO KOPIJA.
#
# PAŽNJA: autoritativan primerak je /usr/local/bin/restore-proba.sh na
# nhmb-srv01. Ovaj fajl je rekonstruisan po ponašanju te skripte (2026-08-10)
# da bi proba bila vidljiva u izvornom kodu: najsvežiji noćni pg_dump se vrati
# u privremenu bazu (podrazumevano mis_restore_test), broj redova po tabeli
# se uporedi sa živom mis_db, pa se privremena baza obriše. Pre izmene uporedi sa prod primerkom.
#
# Svaka greška obara job (set -e, bez "|| true") — OnFailure= u jedinici
# šalje mejl.
#
set -euo pipefail

BACKUP_DB_DIR="${BACKUP_DB_DIR:-/backup/current/db}"
LIVE_DB="${LIVE_DB:-mis_db}"
TEST_DB="${TEST_DB:-mis_restore_test}"

log() { echo "[restore-proba $(date '+%H:%M:%S')] $*"; }

# Fail-closed: TEST_DB ide pravo u dropdb, pa pogrešan override (npr.
# TEST_DB=mis_db) ne sme ni da krene. Dozvoljen je samo prefiks
# mis_restore_test i ime različito od žive baze.
if [[ "$TEST_DB" != mis_restore_test* ]]; then
  log "GRESKA: TEST_DB='$TEST_DB' nije dozvoljeno — ime mora da počinje sa 'mis_restore_test'."
  exit 1
fi
if [[ "$TEST_DB" == "$LIVE_DB" ]]; then
  log "GRESKA: TEST_DB='$TEST_DB' je isto što i LIVE_DB — odbijam dropdb nad živom bazom."
  exit 1
fi

DUMP="$(ls -1t "$BACKUP_DB_DIR"/*.gz "$BACKUP_DB_DIR"/*.dump 2>/dev/null | head -1)"
[[ -n "$DUMP" ]] || { log "GRESKA: nema dump fajla u $BACKUP_DB_DIR"; exit 1; }
log "proba vracanja: $DUMP -> $TEST_DB"

dropdb --if-exists "$TEST_DB"
createdb "$TEST_DB"

case "$DUMP" in
  *.gz)   gunzip -c "$DUMP" | psql -q -v ON_ERROR_STOP=1 -d "$TEST_DB" >/dev/null ;;
  *.dump) pg_restore --no-owner --exit-on-error -d "$TEST_DB" "$DUMP" ;;
esac

# Broj redova po tabeli (tačan count(*), ne statistika) u obe baze.
count_sql="
  SELECT tablename || ' ' || (xpath('/row/c/text()',
           query_to_xml(format('SELECT count(*) AS c FROM %I.%I',
                               schemaname, tablename), false, true, '')))[1]::text
  FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename"
LIVE_COUNTS="$(psql -At -d "$LIVE_DB" -c "$count_sql")"
TEST_COUNTS="$(psql -At -d "$TEST_DB" -c "$count_sql")"

STATUS=0
if [[ "$LIVE_COUNTS" == "$TEST_COUNTS" ]]; then
  log "OK: broj redova po tabeli identican ($(wc -l <<<"$TEST_COUNTS") tabela)."
else
  # Živa baza radi i posle 02:30, pa mala razlika nije nužno korupcija —
  # ali mora da se vidi u logu; prazan restore ili razlika u tabelama obara.
  log "RAZLIKA u broju redova ($LIVE_DB naspram $TEST_DB):"
  diff <(echo "$LIVE_COUNTS") <(echo "$TEST_COUNTS") | sed 's/^/  /' || true
  if ! diff <(cut -d' ' -f1 <<<"$LIVE_COUNTS") <(cut -d' ' -f1 <<<"$TEST_COUNTS") >/dev/null; then
    log "GRESKA: skup tabela se razlikuje — restore nepotpun."
    STATUS=1
  fi
fi
TEST_TOTAL="$(awk '{s+=$2} END {print s+0}' <<<"$TEST_COUNTS")"
if [[ "$TEST_TOTAL" -eq 0 ]]; then
  log "GRESKA: $TEST_DB je prazna (0 redova) — dump neupotrebljiv."
  STATUS=1
fi

dropdb "$TEST_DB"
log "gotovo (ukupno $TEST_TOTAL redova u probi)."
exit "$STATUS"
