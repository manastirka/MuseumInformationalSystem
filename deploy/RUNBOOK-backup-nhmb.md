# Runbook: instalacija noćnog backupa i restore-probe na nhmb-srv01

Sve korake pokreće **Aleksandar ručno kao root** na produkciji — sandbox/dev
nema pristup. Repo je izvor istine za skripte i jedinice; posle svake izmene
u `deploy/` ponovi korake 1–3.

Preduslov za mejl-alarm: lokalni MTA + `mail` (s-nail) podešen tako da pošta
za `root` stiže do prave adrese (`/etc/aliases`).

## 1. Skripte u /usr/local/bin

```bash
cd /opt/mis/app
sudo install -m 755 deploy/backup-nhmb.sh   /usr/local/bin/backup-nhmb.sh
sudo install -m 755 deploy/restore-proba.sh /usr/local/bin/restore-proba.sh
```

> `restore-proba.sh` u repou je rekonstrukcija postojeće prod skripte po
> ponašanju — pre prvog prepisivanja uporedi sa zatečenim
> `/usr/local/bin/restore-proba.sh` i zadrži prod specifičnosti ako ih ima.

## 2. systemd jedinice

```bash
sudo cp deploy/backup-nhmb.service deploy/backup-nhmb.timer \
        deploy/restore-proba.service deploy/restore-proba.timer \
        "deploy/mis-alarm@.service" /etc/systemd/system/
sudo systemctl daemon-reload
```

## 3. Uključivanje tajmera

```bash
sudo systemctl enable --now backup-nhmb.timer restore-proba.timer
systemctl list-timers 'backup-nhmb*' 'restore-proba*'
```

## 4. Probni run i provere

```bash
sudo systemctl start backup-nhmb.service
journalctl -u backup-nhmb -n 60 --no-pager
ls -l /backup/current/data            # arhiva/, mis/, fototeka_ulaz/ — današnji datum
head -1 /backup/current/data/MANIFEST.sha256   # "# backup-nhmb <datum> — N fajlova"
ls /backup/.snapshots | tail -3
```

Očekivanje: prvi run posle 15.07.2026. dugo rsync-uje (fototeka od tada
postoji samo na /data disku); kasniji runovi su inkrementalni.

Proba restore drila i mejl-alarma:

```bash
sudo systemctl start restore-proba.service
journalctl -u restore-proba -n 40 --no-pager
sudo systemctl start mis-alarm@test.service    # mora da stigne mejl root-u
```

## 5. Offsite kopija DB dump-ova (rclone)

**Zašto (međukorak do selidbe servera):** prod i svi bekapi — `/backup/current`
i btrfs snimci — trenutno su u ISTOM kućištu. Požar, krađa ili prenapon nose
original i sve kopije zajedno. Dok server ne bude preseljen, bar dump baze
(~183 MB noću) ide van kućišta svake noći; fajl-stabla (~20 GB) ostaju za
posle selidbe.

Jednokratno podešavanje na prod serveru:

```bash
sudo dnf install rclone
sudo rclone config          # napravi remote, npr. "offsite" (SFTP/S3/drive…)
sudo rclone mkdir offsite:mis-db
sudo rclone copy --checksum /backup/current/db offsite:mis-db   # prvi prenos
```

Zatim remote saopšti servisu kroz drop-in (skripta bez `OFFSITE_REMOTE` samo
upozorava u journalu, ne pada):

```bash
sudo systemctl edit backup-nhmb.service
# [Service]
# Environment=OFFSITE_REMOTE=offsite:mis-db
sudo systemctl daemon-reload
sudo systemctl start backup-nhmb.service
journalctl -u backup-nhmb -n 20 --no-pager   # traži "offsite kopija potvrđena"
rclone ls offsite:mis-db | tail -3
```

Kad je `OFFSITE_REMOTE` podešen, pad rclone koraka OBARA job (mejl-alarm) —
tiho zastarela offsite kopija je gora od bučnog pada.
