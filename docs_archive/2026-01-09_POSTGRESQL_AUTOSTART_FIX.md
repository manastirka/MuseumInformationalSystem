# PostgreSQL Auto-Start Fix

## Problem

Nakon restartovanja računara, samo **sys admin** može da se uloguje, dok **aca.lukovic** i **slavko.spasic** ne mogu.

### Uzrok problema:

PostgreSQL servis nije pokrenut automatski nakon restartovanja računara, što znači:
1. PostgreSQL je bio **disabled** (nije podešen za auto-start)
2. Museum sistem pada na **fallback authentication**
3. Fallback autentifikacija ima samo **admin** korisnika (po dizajnu za sigurnost)
4. Regularni korisnici (aca.lukovic, slavko.spasic) su u PostgreSQL bazi, ne u fallback sistemu

### Dokaz iz logova:

```
connection to server at "127.0.0.1", port 5432 failed: Connection refused
Is the server running on that host and accepting TCP/IP connections?

Using fallback auth for: aca.lukovic@nhmbeo.rs - login_failed
Using fallback auth for: slavko.spasic@nhmbeo.rs - login_failed
Using fallback auth for: admin - login_success
```

---

## Rešenje

### Automatsko rešenje (preporučeno):

Pokreni automatski script koji popravlja sve:

```bash
cd /home/aleksandarlukovic/MuseumInfoSystem
./fix_postgresql_startup.sh
```

Script će automatski:
1. ✅ Pokrenuti PostgreSQL
2. ✅ Omogućiti auto-start PostgreSQL-a na boot
3. ✅ Testirati konekciju na bazu
4. ✅ Restartovati museum-system servis
5. ✅ Očistiti stare sesije
6. ✅ Prikazati status

### Manuelno rešenje:

Ako automatski script ne radi, koristi ove komande:

```bash
# 1. Pokreni PostgreSQL
sudo systemctl start postgresql

# 2. Omogući auto-start
sudo systemctl enable postgresql

# 3. Proveri status
sudo systemctl status postgresql

# 4. Testiraj konekciju
psql -U aleksandarlukovic -d museum_system -c "SELECT email FROM users;"

# 5. Restartuj museum sistem
sudo systemctl restart museum-system.service

# 6. Očisti sesije
rm -rf /home/aleksandarlukovic/MuseumInfoSystem/flask_session/*

# 7. Proveri logove
tail -f /home/aleksandarlukovic/MuseumInfoSystem/logs/museum_info_system.log
```

---

## Provera da li je problem rešen

### 1. Proveri PostgreSQL status:

```bash
sudo systemctl status postgresql
```

Trebalo bi da vidiš: `Active: active (running)`

### 2. Proveri da li je enabled za boot:

```bash
systemctl is-enabled postgresql
```

Trebalo bi da vidiš: `enabled`

### 3. Testiraj login:

Idi na http://localhost:5555/login i pokušaj da se uloguješ sa:
- **Email:** aca.lukovic@nhmbeo.rs
- **Password:** (tvoja lozinka)

Ili:
- **Email:** slavko.spasic@nhmbeo.rs
- **Password:** (tvoja lozinka)

### 4. Proveri logove:

```bash
tail -20 /home/aleksandarlukovic/MuseumInfoSystem/logs/museum_info_system.log
```

Trebalo bi da vidiš:
- ✅ `PostgresAuth: Connected successfully (X users)`
- ✅ `login_success` umesto `login_failed`
- ❌ **NE** bi trebalo da vidiš: `Using fallback auth`

---

## Prevencija problema u budućnosti

### Proveri auto-start postavke:

```bash
# Proveri koje servise su enabled za boot
systemctl list-unit-files | grep enabled | grep -E '(postgres|museum)'
```

Trebalo bi da vidiš:
```
postgresql.service                enabled
museum-system.service             enabled
```

### Kreiraj systemd dependency:

Ažuriraj museum-system.service da zavisi od PostgreSQL-a:

```bash
sudo nano /etc/systemd/system/museum-system.service
```

Dodaj u `[Unit]` sekciju:
```ini
[Unit]
Description=Museum Information System
After=network.target postgresql.service
Requires=postgresql.service
```

Zatim reload i restart:
```bash
sudo systemctl daemon-reload
sudo systemctl restart museum-system.service
```

---

## Troubleshooting

### Problem: PostgreSQL se ne pokreće

**Proveri logove:**
```bash
sudo journalctl -u postgresql -n 50
```

**Mogući uzroci:**
- Port 5432 je zauzet
- Disk space je pun
- Permission problemi

### Problem: Museum sistem se ne pokreće nakon PostgreSQL-a

**Proveri da li PostgreSQL prihvata konekcije:**
```bash
psql -U aleksandarlukovic -d museum_system -c "SELECT 1;"
```

**Proveri DATABASE_URL:**
```bash
grep DATABASE_URL /home/aleksandarlukovic/MuseumInfoSystem/.env
```

Trebalo bi da bude:
```
DATABASE_URL=postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system
```

### Problem: Korisnici i dalje ne mogu da se uloguju

**1. Proveri da li korisnici postoje u bazi:**
```bash
psql -U aleksandarlukovic -d museum_system -c "SELECT id, email, is_active FROM users;"
```

**2. Proveri da li su aktivni:**
```bash
psql -U aleksandarlukovic -d museum_system -c "SELECT email, is_active FROM users WHERE email IN ('aca.lukovic@nhmbeo.rs', 'slavko.spasic@nhmbeo.rs');"
```

Trebalo bi da vidiš `is_active = t` (true).

**3. Reset lozinke ako je potrebno:**
```bash
cd /home/aleksandarlukovic/MuseumInfoSystem
python3 << 'EOF'
from postgres_auth import get_postgres_auth
from security_utils import PasswordHasher

# Inicijalizuj
pg_auth = get_postgres_auth()
hasher = PasswordHasher()

# Generiši novi hash
new_password = "nova_lozinka_123"
password_hash, salt = hasher.hash_password(new_password)

# Update u bazi (manual SQL)
print(f"Password hash: {password_hash}")
print(f"Salt: {salt}")
print(f"\nSQL komanda:")
print(f"UPDATE users SET password_hash = '{password_hash}', salt = '{salt}' WHERE email = 'aca.lukovic@nhmbeo.rs';")
EOF
```

---

## Brzi pregled komandi

### Startuj sve:
```bash
sudo systemctl start postgresql
sudo systemctl start museum-system.service
```

### Proveri status:
```bash
sudo systemctl status postgresql
systemctl status museum-system.service
```

### Restart nakon problema:
```bash
sudo systemctl restart postgresql
sudo systemctl restart museum-system.service
rm -rf /home/aleksandarlukovic/MuseumInfoSystem/flask_session/*
```

### Proveri logove uživo:
```bash
# Museum sistem logovi
tail -f /home/aleksandarlukovic/MuseumInfoSystem/logs/museum_info_system.log

# PostgreSQL logovi
sudo journalctl -u postgresql -f

# Museum service logovi
journalctl -u museum-system.service -f
```

---

## Kontakt

Ako problem i dalje postoji nakon primene ovih koraka:
1. Sačuvaj logove: `tail -100 /home/aleksandarlukovic/MuseumInfoSystem/logs/museum_info_system.log > problem_logs.txt`
2. Proveri status servisa: `systemctl status postgresql museum-system.service > status.txt`
3. Kontaktiraj sistem administratora

---

**Datum:** 2026-01-09
**Problem:** PostgreSQL not auto-starting after reboot
**Status:** Resolved ✅
