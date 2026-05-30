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
python deploy/run_migrations.py mark '00[1-7]_*.sql'   # mark some applied, don't run
```

**First run on THIS database** (it already has the 001–007 schema; 008–011 are new):
```bash
python deploy/run_migrations.py mark '00[1-7]_*.sql'   # baseline what's already there
python deploy/run_migrations.py status                 # confirm 008–011 are 'pending'
python deploy/run_migrations.py apply                  # applies 008, 009, 010, 011
python scripts/migrate_sanja_to_postgres.py            # load Sanja into PG
python scripts/migrate_digitized_profiles_to_postgres.py
```
> Before 009, de-duplicate any duplicate monthly reports (see the comment in
> `migration/009_timesheet_report_integrity.sql`).

**On the NEW server after restoring a `pg_dump`** (schema is already in the dump):
```bash
python deploy/run_migrations.py baseline   # mark everything applied
```

---

## 2. Nightly backup → your personal Google Drive

`deploy/museum-backup.sh` dumps PostgreSQL (custom format) + flat-file data,
copies it off-box to **`gdrive:MuseumBackups`** (your rclone remote), and prunes
old copies. Runs as `aleksandarlukovic` so the rclone Google Drive config works.

Install the timer:
```bash
sudo cp deploy/museum-backup.service /etc/systemd/system/
sudo cp deploy/museum-backup.timer   /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now museum-backup.timer
sudo systemctl start museum-backup.service     # run one now to test
journalctl -u museum-backup.service -n 40       # check it
rclone ls gdrive:MuseumBackups                  # confirm files landed on Drive
```
Tunable via env (in the `.service` or `.env`): `MUSEUM_BACKUP_GDRIVE_REMOTE`,
`MUSEUM_BACKUP_DIR`, `MUSEUM_BACKUP_LOCAL_KEEP_DAYS` (7), `MUSEUM_BACKUP_DRIVE_KEEP_DAYS`
(30), `MUSEUM_BACKUP_INCLUDE_SECRETS` (0 — set 1 to also back up `.env`/`.mail_key`).

**Restore drill (do once to prove it works):**
```bash
createdb museum_restore_test
pg_restore --no-owner -d museum_restore_test backups/museum_db_<stamp>.dump
# verify a few row counts, then: dropdb museum_restore_test
```

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
