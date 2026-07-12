# Runbook — Фототека: batch uvoz sa mrežnog diska (produkcija)

Sve komande se izvršavaju na **nhmb-srv01** (192.168.144.194) kao sudo.
Samba i systemd timer NISU pod `deploy.sh` — ovaj dokument je izvor istine.
Kod (engine, UI, skripta, migracija 026) stiže standardnim deploy ciklusom.

## 1. Samba share (jednokratno)

Model: jedan share `fototeka-ulaz`, svaki korisnik kroz `%U` vidi SAMO svoj
podfolder. Ime foldera = **lokalni deo email adrese u MIS-u** (npr.
`sjovanovic` za `sjovanovic@nhmbeo.rs`) — iz njega uvoz izvodi autorstvo.

```bash
sudo dnf install -y samba
sudo groupadd -f fototeka-ulaz
sudo mkdir -p /data/fototeka_ulaz
sudo chgrp fototeka-ulaz /data/fototeka_ulaz && sudo chmod 2770 /data/fototeka_ulaz

# servisni nalog aplikacije čita i premešta fajlove
sudo usermod -aG fototeka-ulaz mis

# SELinux kontekst (Fedora — obavezno, inače smbd ne može da piše)
sudo semanage fcontext -a -t samba_share_t "/data/fototeka_ulaz(/.*)?"
sudo restorecon -Rv /data/fototeka_ulaz

# firewall — samba je samo za LAN
sudo firewall-cmd --permanent --add-service=samba
sudo firewall-cmd --reload
```

U `/etc/samba/smb.conf` dodati na kraj:

```ini
[fototeka-ulaz]
   path = /data/fototeka_ulaz/%U
   valid users = @fototeka-ulaz
   writable = yes
   create mask = 0660
   directory mask = 2770
   force group = fototeka-ulaz
```

Provera i start:

```bash
sudo testparm
sudo systemctl enable --now smb
```

## 2. Nalog po kustosu (za svakog novog korisnika)

```bash
# primer: sjovanovic (mora odgovarati lokalnom delu email-a u MIS users tabeli)
sudo useradd -M -s /sbin/nologin -G fototeka-ulaz sjovanovic
sudo smbpasswd -a sjovanovic        # lozinku zadaje admin/kustos
sudo install -d -o sjovanovic -g fototeka-ulaz -m 2770 /data/fototeka_ulaz/sjovanovic
```

Pristup sa radnih stanica:
- Windows: `\\192.168.144.194\fototeka-ulaz` (Map network drive)
- Mac Finder: `Cmd+K` → `smb://192.168.144.194/fototeka-ulaz`

Napomena: folder čije ime ne odgovara nijednom (ili odgovara dvama)
MIS nalogu se uvozi pod servisnim autorom + tag `uvoz-nepoznat-autor`.

## 3. Aplikacija (.env + migracija)

U `/opt/mis/app/.env` dodati/proveriti:

```bash
FOTOTEKA_IMPORT_PATH=/data/fototeka_ulaz
```

Migracija `026_fototeka_uvoz_log.sql` ide automatski kroz `deploy.sh`
(korak 3b). Posle deploy-a restart je već u proceduri.

## 4. Systemd timer (na 30 minuta)

```bash
sudo cp /opt/mis/app/deploy/fototeka-import.service \
        /opt/mis/app/deploy/fototeka-import.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now fototeka-import.timer
systemctl list-timers fototeka-import.timer
```

Preduslov: `mis-fototeka-worker` servis radi (derivati); `mis` je u grupi
`fototeka-ulaz` (korak 1).

## 5. Smoke test

```bash
# 1) probni fajl u svoj folder (kroz mrežni disk ili direktno):
sudo -u mis cp /neka/proba.jpg /data/fototeka_ulaz/<tvoj-folder>/M-99999_proba.jpg

# 2) dry-run (ništa ne piše):
sudo -u mis /opt/mis/venv/bin/python /opt/mis/app/fototeka_import.py

# 3) stvarni uvoz:
sudo -u mis /opt/mis/venv/bin/python /opt/mis/app/fototeka_import.py --izvrsi

# 4) provere:
#    - fajl premešten u /data/fototeka_ulaz/<folder>/obradjeno/<YYYY-MM>/
#    - RAW u /data/arhiva/zbirke/mineral/99999/
#    - fotografija vidljiva u MIS Фототеци (derivat pravi worker)
#    - istorija na /fototeka/uvoz pokazuje run (izvor: cli)
#    - journalctl -u fototeka-import.service  (za timer runove)
```

Posle smoke testa probnu fotografiju obrisati kroz MIS (soft delete) ili
ostaviti kao prvu pravu.

## 6. Ponašanje i održavanje

- **Konvencija imena:** `PMB-M-01234_2026-07-02_01.tif` ili `M-01234_...`
  → predmet (datum iz imena postaje datum snimanja ako nema EXIF-a);
  `TEREN_2026_Lokalitet_01.tif` → teren; sve ostalo → prijemni red
  (`/fototeka/prijemni-red`, kustos dopisuje veze/tagove).
- **Posle uvoza:** uspešno → `obradjeno/<YYYY-MM>/`; duplikat (sha256) →
  `obradjeno/duplikati/`; neispravan format/prazan/preko 200 MB →
  `neuspesno/`. Fajl sa prolaznom greškom (npr. baza nedostupna) ostaje
  u ulazu za sledeći run.
- **Vidljivost uvezenih:** `javno` (svi ulogovani zaposleni) — kao upload.
- **UI:** `/fototeka/uvoz` (admin/direktor/kustos) — „Скенирај улаз" je
  uvek dry-run; uvoz kreće tek na „Потврди".
- **Čišćenje `obradjeno/`:** odluka je ručna; predlog kad zatreba prostor:
  ```bash
  find /data/fototeka_ulaz/*/obradjeno -type f -mtime +90 -delete
  ```
  (RAW kopija je već u /data/arhiva — u backup rutini.)

## 7. Ako nešto ne radi

| Simptom | Provera |
|---|---|
| Korisnik ne vidi share | `smbclient -L //localhost -U <user>`; `testparm`; firewall zona |
| Vidi share ali ne može da piše | SELinux: `ls -Z /data/fototeka_ulaz`; `restorecon -Rv` |
| Uvoz ne uzima fajlove | `sudo -u mis ls /data/fototeka_ulaz/<folder>` (grupa/mode 2770?) |
| Timer ne radi | `systemctl list-timers`; `journalctl -u fototeka-import.service -n 50` |
| Nema derivata | `systemctl status mis-fototeka-worker`; red u `foto_poslovi` |
| Sve u prijemnom redu | ime fajla ne prati konvenciju — vidi tačku 6 |
