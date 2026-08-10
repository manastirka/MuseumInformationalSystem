# New-Server Setup — Fedora (MuseumInfoSystem)

Full, ordered bring-up for the dedicated internal server. Copy-paste section by
section; adjust the **subnet, paths, and passwords** marked `<...>` / `CHANGE_ME`.

**Hardware assumed**
- OS on the 2 TB NVMe
- 2 × 20 TB HDD → **btrfs RAID1 mirror** for the database + backups + uploads
- APC UPS on USB
- Wired LAN; a **static IP** is recommended

---

## 0. On the OLD box first — take what you'll carry over
```bash
# full database dump (custom format), the secrets, and the rclone Google-Drive config
pg_dump -Fc "$DATABASE_URL" -f /tmp/museum_system.dump        # or use a recent backup .dump
cp ~/MuseumInfoSystem/.env /tmp/museum.env
cp ~/MuseumInfoSystem/data/.mail_key /tmp/museum.mail_key 2>/dev/null || true
cp ~/.config/rclone/rclone.conf /tmp/rclone.conf
# move /tmp/museum_system.dump /tmp/museum.env /tmp/museum.mail_key /tmp/rclone.conf to the new server
```

## 1. Base OS
```bash
sudo dnf -y update
sudo hostnamectl set-hostname museum-server
sudo timedatectl set-timezone Europe/Belgrade
sudo dnf -y install git curl vim policycoreutils-python-utils
# (recommended) give the box a static LAN IP via your router or nmcli
```

## 2. Storage — RAID1 mirror of the two 20 TB disks (btrfs)
btrfs RAID1 gives a mirror **plus checksums + scrubbing**, which detect silent
bit-rot — partly compensating for skipping ECC.
```bash
lsblk                                   # find the two 20 TB disks (e.g. /dev/sda /dev/sdb) — NOT the NVMe
sudo wipefs -a /dev/sda /dev/sdb        # ⚠️ DOUBLE-CHECK these are the empty 20 TB HDDs
sudo mkfs.btrfs -m raid1 -d raid1 -L museumdata /dev/sda /dev/sdb
sudo mkdir -p /srv/museum
sudo mount /dev/sda /srv/museum
sudo btrfs subvolume create /srv/museum/pg
sudo btrfs subvolume create /srv/museum/backups
sudo btrfs subvolume create /srv/museum/uploads
UUID=$(sudo blkid -s UUID -o value /dev/sda)
echo "UUID=$UUID /srv/museum btrfs defaults,compress=zstd 0 0" | sudo tee -a /etc/fstab
sudo systemctl daemon-reload && sudo mount -a
# monthly integrity scrub
sudo systemctl enable --now "btrfs-scrub@$(systemd-escape -p /srv/museum).timer"
```

## 3. UPS — graceful shutdown (apcupsd)
```bash
sudo dnf -y install apcupsd
sudo sed -i 's/^UPSCABLE.*/UPSCABLE usb/; s/^UPSTYPE.*/UPSTYPE usb/; s/^DEVICE .*/DEVICE/' /etc/apcupsd/apcupsd.conf
sudo systemctl enable --now apcupsd
apcaccess status            # should list your APC SMV1500CAi; it shuts down cleanly on low battery
```

## 4. Packages
```bash
sudo dnf -y install postgresql-server postgresql-contrib redis nginx \
  python3 python3-pip python3-devel gcc gcc-c++ make rclone \
  libjpeg-turbo-devel zlib-devel libffi-devel libxml2-devel libxslt-devel openssl-devel \
  gdal gdal-devel
sudo systemctl enable --now redis
```

## 5. PostgreSQL — initialised ON THE MIRROR
```bash
sudo mkdir -p /srv/museum/pg
sudo chown postgres:postgres /srv/museum/pg && sudo chmod 700 /srv/museum/pg
# init the cluster on the mirror, with page checksums on
sudo -u postgres /usr/bin/initdb -D /srv/museum/pg --data-checksums
# SELinux: label the custom data dir as postgres data (Fedora is enforcing)
sudo semanage fcontext -a -t postgresql_db_t "/srv/museum/pg(/.*)?"
sudo restorecon -Rv /srv/museum/pg
# point the postgresql service at the mirror dir
sudo mkdir -p /etc/systemd/system/postgresql.service.d
printf '[Service]\nEnvironment=PGDATA=/srv/museum/pg\n' | sudo tee /etc/systemd/system/postgresql.service.d/pgdata.conf
sudo systemctl daemon-reload && sudo systemctl enable --now postgresql
# app role + database, scram auth
sudo -u postgres psql -c "ALTER SYSTEM SET password_encryption='scram-sha-256';"
sudo systemctl restart postgresql
sudo -u postgres psql <<'SQL'
CREATE ROLE museum_app LOGIN PASSWORD 'CHANGE_ME_STRONG';
CREATE DATABASE museum_system OWNER museum_app;
SQL
echo "host museum_system museum_app 127.0.0.1/32 scram-sha-256" | sudo tee -a /srv/museum/pg/pg_hba.conf
sudo systemctl reload postgresql
```

## 6. App user + code (on the NVMe; data is on the mirror)
```bash
sudo useradd -r -m -d /opt/museum -s /usr/sbin/nologin museum 2>/dev/null || true
sudo -u museum git clone https://github.com/manastirka/MuseumInformationalSystem.git /opt/museum/app
cd /opt/museum/app
sudo -u museum git checkout main                 # or your branch
sudo -u museum python3 -m venv venv
sudo -u museum ./venv/bin/pip install -r requirements.lock
```

## 7. Secrets + config (.env)
```bash
sudo install -o museum -g museum -m 600 /tmp/museum.env /opt/museum/app/.env
sudo install -o museum -g museum -m 600 /tmp/museum.mail_key /opt/museum/app/data/.mail_key 2>/dev/null || true
sudoedit /opt/museum/app/.env      # set, at minimum:
#   DATABASE_URL=postgresql+psycopg://museum_app:CHANGE_ME_STRONG@localhost/museum_system
#   SECRET_KEY=<fresh long random>            FLASK_ENV=production
#   SESSION_TYPE=redis   REDIS_URL=redis://localhost:6379/0
#   RATELIMIT_STORAGE_URL=redis://localhost:6379/1   WORKERS=2
#   MAIL_SETTINGS_ENCRYPTION_KEY=<same value as the old box>
#   BACKUP_DIRECTORY=/srv/museum/backups
```

## 8. Restore the database + baseline migrations
```bash
sudo -u museum pg_restore --no-owner \
  -d "postgresql://museum_app:CHANGE_ME_STRONG@localhost/museum_system" /tmp/museum_system.dump
cd /opt/museum/app
sudo -u museum ./venv/bin/python deploy/run_migrations.py baseline   # schema is already in the dump
sudo -u museum ./venv/bin/python deploy/run_migrations.py status     # confirm 0 pending
```

## 9. gunicorn service (systemd)
```bash
sudo tee /etc/systemd/system/museum-system.service >/dev/null <<'UNIT'
[Unit]
Description=Museum Information System (gunicorn)
After=network.target postgresql.service redis.service
Wants=postgresql.service redis.service

[Service]
Type=exec
User=museum
Group=museum
WorkingDirectory=/opt/museum/app
Environment=FLASK_ENV=production
Environment=PYTHONPATH=/opt/museum/app
ExecStart=/opt/museum/app/venv/bin/python -m gunicorn --config gunicorn.conf.py wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=10
RuntimeDirectory=museum
[Install]
WantedBy=multi-user.target
UNIT
sudo systemctl daemon-reload && sudo systemctl enable --now museum-system
```

## 10. nginx — TLS + LAN allowlist + proxy
```bash
sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
  -keyout /etc/pki/tls/private/museum.key -out /etc/pki/tls/certs/museum.crt -subj "/CN=museum-server"
sudo tee /etc/nginx/conf.d/museum.conf >/dev/null <<'NGINX'
upstream museum_app { server 127.0.0.1:8000; }
server { listen 80; listen [::]:80; server_name _; return 301 https://$host$request_uri; }
server {
    listen 443 ssl http2; listen [::]:443 ssl http2; server_name _;
    ssl_certificate /etc/pki/tls/certs/museum.crt; ssl_certificate_key /etc/pki/tls/private/museum.key;
    client_max_body_size 50M;
    allow 127.0.0.1; allow ::1;
    allow 192.168.1.0/24;        # <-- SET YOUR LAN SUBNET
    allow 100.64.0.0/10;          # Tailscale (remove if unused)
    deny all;
    location / {
        proxy_pass http://museum_app;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    location ~ /\. { deny all; }
}
NGINX
sudo setsebool -P httpd_can_network_connect 1     # SELinux: let nginx reach gunicorn
sudo nginx -t && sudo systemctl enable --now nginx
```

## 11. Firewall
```bash
sudo firewall-cmd --permanent --add-service={ssh,http,https}
sudo firewall-cmd --reload
```

## 12. Backups
The production server (nhmb-srv01) runs the nightly backup as
`backup-nhmb.timer` / `backup-nhmb.service` (02:30, script
`/usr/local/bin/backup-nhmb.sh`) plus the monthly automated restore drill
`restore-proba.timer` / `restore-proba.service` (1st of month, 03:30).
Install both per `deploy/RUNBOOK-backup-nhmb.md`:
```bash
sudo install -m 755 /opt/mis/app/deploy/backup-nhmb.sh /usr/local/bin/backup-nhmb.sh
sudo install -m 755 /opt/mis/app/deploy/restore-proba.sh /usr/local/bin/restore-proba.sh
sudo cp /opt/mis/app/deploy/{backup-nhmb,restore-proba}.{service,timer} /etc/systemd/system/
sudo cp /opt/mis/app/deploy/mis-alarm@.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now backup-nhmb.timer restore-proba.timer
sudo systemctl start backup-nhmb.service             # run one now
```

## 13. Verify (go/no-go)
```bash
curl -k https://localhost/healthz                    # {"status":"ok","db":"ok","redis":"ok"}
systemctl is-active postgresql redis nginx museum-system
# Browse to https://<server-LAN-IP>/ , log in, generate one monthly Radna Lista,
# and compare its totals to the same report on the old box.
```

## 14. Updates, forever after
```bash
cd /opt/museum/app && sudo -u museum deploy/update.sh   # git pull -> deps -> migrate -> restart -> healthcheck
```

---

### Notes
- **Logrotate backstop:** `sudo cp deploy/logrotate-museum /etc/logrotate.d/museum-info-system`.
- **Background worker** (recurring jobs): create a sibling `museum-worker.service` with
  `Environment=MUSEUM_BACKGROUND_WORKER=1` running `background_worker.py`, if you use it.
- **Faster alternative:** `migration/deploy.sh` automates steps 4 + 9–11 in one shot, but it
  installs under `/home`, uses the default Postgres data dir (NOT the mirror), and a self-signed
  cert. This manual runbook is preferred because it puts the **database on the redundant mirror**.
- **Self-signed TLS** will warn in browsers; import `museum.crt` into the few client PCs to silence it.
