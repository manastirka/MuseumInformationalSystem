# CLAUDE.md — Museum Information System (MIS)

## Projekat

Flask + PostgreSQL aplikacija Prirodnjačkog muzeja u Beogradu (zbirke,
geoprostorni podaci/Leaflet, QR etikete, evidencija rada, finansije,
izložbe). U produkciji radi iza gunicorn + nginx na Fedora Serveru.

## Okruženja — gde se šta sme

| Uloga | Mašina | Napomena |
|---|---|---|
| **DEV** | stari server (`192.168.144.48`) | ovde se piše kod |
| **PROD** | `nhmb-srv01` (`192.168.144.194`) | aplikacija: `/opt/mis/app`, venv: `/opt/mis/venv`, servis: `mis.service`, podaci: `/data/mis`, noćni backup 02:30 |
| **GitHub** | `manastirka/MuseumInformationalSystem` | izvor istine |

**Kod putuje isključivo kroz git** (dev → GitHub → prod). Podaci putuju
rsync-om. Tajne (`.env`) ne putuju nikako — svako okruženje ima svoj.

## Pravila za Claude Code sesije

**Na DEV mašini** — puna sloboda: pisanje koda, refaktorisanje,
eksperimenti. Obavezno pri tom:
- `pytest` mora biti zelen pre svakog commita (suite ima ~365 testova);
- izmene šeme baze isključivo kroz migracije, nikad ručni `ALTER`;
- nove zavisnosti odmah u `requirements.txt`, sa verzijom;
- konfiguracija (putanje, kredencijali, SECRET_KEY) samo kroz `.env` /
  config — nikad hardkodovano u kodu;
- `.env`, `__pycache__`, lokalni podaci se ne commituju.

**Na PROD serveru** — isključivo uloga operatera:
- DOZVOLJENO: `deploy.sh`, čitanje logova (`journalctl -u mis`),
  `systemctl status/restart mis`, dijagnostika (uključujući čitanje koda).
- ZABRANJENO: menjanje koda direktno, pisanje u bazu mimo aplikacije,
  instaliranje paketa mimo `requirements.txt`, menjanje configa bez
  znanja korisnika.
- Ako `git pull --ff-only` odbije — STANI i prijavi korisniku: znači da
  je neko menjao kod na produkciji mimo procedure.

## Deploy procedura

1. Na DEV: `pytest` zelen → commit → push.
2. Označi verziju: `git tag prod-YYYY-MM-DD && git push --tags`
3. Na PROD: `sudo /usr/local/bin/deploy.sh`
   (skripta: backup → pull --ff-only → pip install → restart → smoke test)

**Rollback:** na PROD
`sudo -u mis git -C /opt/mis/app checkout <prethodni-tag>` +
`sudo systemctl restart mis`.

## Poznati tehnički dug (popisano 2026-07-03)

Prvi zadaci za DEV sesije — na produkciji trenutno pokriveno
improvizacijama koje treba da postanu nepotrebne:

1. **Hardkodovane putanje** (`/home/aleksandarlukovic/...`) u kodu —
   prebaciti na config/env vrednosti. (Na prod pokriveno symlinkom.)
2. **requirements.txt nepotpun** — fale `psutil`, `xlrd`, `openpyxl`
   (na prod instalirani ručno; uskladiti fajl sa stvarnim uvozima).
3. **gunicorn.conf.py** hardkoduje korisnika — parametrizovati ili
   ukloniti (produkcija gunicorn parametre drži u systemd unitu).

Posle svake od ovih popravki: pytest, pa normalan deploy ciklus.
