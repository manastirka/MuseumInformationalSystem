# MuseumInfoSystem — Operations & Deploy Kit

Small, portable ops tooling. Everything is env-driven so it runs **on this
machine now** and on the **new server** unchanged. Anything that touches the
database or the server must be run by you (the sandbox can't reach the live DB).

---

## 1. Database migration runner — `deploy/run_migrations.py`

Applies `migration/NNN_*.sql` in order, once each, tracked in a
`schema_migrations` table. Requires `DATABASE_URL`.

```bash
python deploy/run_migrations.py status     # show applied vs pending
python deploy/run_migrations.py apply       # run all pending, in order
python deploy/run_migrations.py baseline     # mark ALL files applied WITHOUT running
python deploy/run_migrations.py mark '001_*.sql'   # mark some applied, don't run
python deploy/run_migrations.py remap            # dry-run: old->new filename rows
python deploy/run_migrations.py remap --execute  # rewrite them in schema_migrations
```

> 2026-08: duplicate `NNN_` prefixes were renamed to unique numbers (002–005
> dupes → 003–010, then 006–040 → 011–045). Databases that recorded the old
> names are rewritten automatically by `apply` (or explicitly via `remap`);
> nothing is re-run. Historical examples below use the pre-rename numbering.

**First run on THIS database** (it already has the 001–007 schema; 008–011 are new):
```bash
python deploy/run_migrations.py mark '00[1-7]_*.sql'   # baseline what's already there
python deploy/run_migrations.py status                 # confirm 008–011 are 'pending'
python deploy/run_migrations.py apply                  # applies 008, 009, 010, 011
python scripts/migrate_sanja_to_postgres.py            # load Sanja into PG
python scripts/migrate_digitized_profiles_to_postgres.py
```
> Before 009, de-duplicate any duplicate monthly reports (see the comment in
> `migration/014_timesheet_report_integrity.sql`, formerly `009_...`).

**On the NEW server after restoring a `pg_dump`** (schema is already in the dump):
```bash
python deploy/run_migrations.py baseline   # mark everything applied
```

---

## 2. Nightly backup — `backup-nhmb` (production: nhmb-srv01)

Production runs **`backup-nhmb.timer` → `backup-nhmb.service`** every night at
02:30, executing `/usr/local/bin/backup-nhmb.sh` (source in the repo:
`deploy/backup-nhmb.sh`). It does three things:

1. `pg_dump` of `mis_db` into `/backup/current/db/` (gzipped, daily);
2. **rsync refresh of the file trees** — `/data/arhiva`, `/data/mis/dokumenti`,
   `/data/mis/media`, `/data/fototeka_ulaz` → `/backup/current/data/`, with a
   file count + SHA-256 manifest; a source error FAILS the job (no `|| true`);
3. a read-only btrfs snapshot of `/backup/current` under
   `/backup/.snapshots/<date>`.

`/backup` is a separate 19 TB disk (`/dev/sdb1`); `/data` lives on `/dev/sda1`
— the rsync step is what keeps new fototeka material on **two** disks.
Failures alert by mail via `OnFailure=mis-alarm@%n.service`.
Install/update: `deploy/RUNBOOK-backup-nhmb.md`.

**Restore drill is AUTOMATED** — `restore-proba.timer` → `restore-proba.service`
runs on the 1st of each month at 03:30 (`/usr/local/bin/restore-proba.sh`,
repo copy: `deploy/restore-proba.sh`, prod copy is authoritative): restores the
latest dump into a temporary `restore_test` database, compares per-table row
counts against the live `mis_db`, then `dropdb restore_test`. To run one by
hand: `sudo systemctl start restore-proba.service` and check
`journalctl -u restore-proba -n 40`.

---

## 3. Health check — `GET /healthz`

Unauthenticated readiness probe. Returns `200 {"status":"ok","db":"ok","redis":"ok"}`
when healthy, `503 {"status":"degraded",...}` otherwise.

```bash
curl -k https://localhost/healthz        # through nginx (recommended)
```
Wire it into the service so a boot that can't reach the DB is reported as failed:
```ini
# in museum-system.service, [Service] section:
ExecStartPost=/usr/bin/curl -fsS --retry 10 --retry-delay 2 -k https://localhost/healthz
```

---

## 4. Log rotation

The app log now rotates automatically (10 MB × 5 via `RotatingFileHandler`).
For gunicorn/nginx logs, install the backstop:
```bash
sudo cp deploy/logrotate-museum /etc/logrotate.d/museum-info-system
sudo logrotate --debug /etc/logrotate.d/museum-info-system   # dry-run check
```

---

## 5. Security hardening & reproducible builds

**Reproducible install** — `requirements.txt` uses `>=` ranges; `requirements.lock`
pins the exact versions that work today. On the new server install from the lock:
```bash
pip install -r requirements.lock
pip install pip-audit && pip-audit -r requirements.lock   # optional: known-CVE scan
```

**Dedicated, passworded database role** (the app/control-center currently connect as
the personal `aleksandarlukovic` role via peer auth, which won't exist on the new box):
```sql
-- as the postgres superuser:
CREATE ROLE museum_app LOGIN PASSWORD 'CHANGE_ME';
GRANT CONNECT ON DATABASE museum_system TO museum_app;
GRANT USAGE ON SCHEMA public TO museum_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO museum_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO museum_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO museum_app;
```
Then point the app at it (`.env`): `DATABASE_URL=postgresql+psycopg://museum_app:CHANGE_ME@localhost/museum_system`,
require strong auth in `pg_hba.conf` (`host museum_system museum_app 127.0.0.1/32 scram-sha-256`,
remove `trust`/`peer`), and `sudo systemctl reload postgresql`.

**Control center** now reads its DB identity from the environment — set it where you
launch the desktop tool: `MUSEUM_DB_USER=museum_app MUSEUM_DB_NAME=museum_system`
(plus a `~/.pgpass` line so it isn't prompted for the password).

**Mail key permissions** (currently world-readable `0644`):
```bash
chmod 600 data/.mail_key && chown <service-user>:<service-user> data/.mail_key
```

---

## 6. Updating the server from git — `deploy/update.sh`

Once installed, every code change ships via git. On the server:
```bash
deploy/update.sh         # git pull -> pip install -> migrate -> restart -> healthcheck
```
It refuses to run on a dirty tree, is a no-op when there are no new commits, prints
a rollback command if the health check fails, and applies any new DB migrations
automatically. Tunable via env: `MUSEUM_GIT_BRANCH` (default `main`),
`MUSEUM_SERVICE`, `MUSEUM_HEALTH_URL`.

> Safety: prefer running this **manually** (or only from a branch your tests have
> passed). Auto-deploying every push to the live museum system — e.g. a blind cron
> `git pull` — risks shipping an untested commit. Gate it behind the test suite.

---

## Cutover checklist (current box → new server)

**Before (on this box):** dedupe reports → `run_migrations.py mark '00[1-7]_*.sql'`
→ `apply` → load Sanja + profiles → enable the backup timer → take a final
`pg_dump -Fc` and confirm it lands on Google Drive.

**During (new box):** install PostgreSQL/Redis/nginx → restore globals + the dump
→ `run_migrations.py baseline` → reset sequences → create `.env`
(fresh `SECRET_KEY`, real `DATABASE_URL`, `MAIL_SETTINGS_ENCRYPTION_KEY`) →
deploy code → enable `museum-system` + the backup timer → install logrotate.

**Verify before going live:** `curl -k https://localhost/healthz` is `200 ok`,
log in, and regenerate one known monthly Radna Lista and compare it to the old
server's output. Keep the old box for one reporting cycle as the safety net.
