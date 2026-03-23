# ČIŠĆENJE I UNOS REALNIH PODATAKA - SISTEM RADNIH LISTA
## Timesheet System - Clear Test Data and Enter Real Employee Data

**Datum:** 2026-01-09
**Svrha:** Brisanje test podataka i priprema za unos realnih podataka zaposlenih

---

## 📊 TRENUTNO STANJE

### Test podaci u sistemu:

| Stavka | Broj |
|--------|------|
| Timesheet Reports | 9 |
| Timesheet Entries | 72 |
| Test zaposleni | 3 (Немања Ђорђевић, Марко Марковић, Јелена Петровић) |
| Meseci sa podacima | Oktobar, Novembar, Decembar 2025 |

### Backup kreiran:
- **Lokacija:** `/home/aleksandarlukovic/MuseumInfoSystem/backups/timesheet_data/`
- **Fajl:** `timesheet_backup_20260109_115900.sql`
- **Veličina:** 7.5K

---

## 🔧 OPCIJE ZA ČIŠĆENJE PODATAKA

### Opcija 1: Interaktivni Script (PREPORUČENO)

**Koristi ovu opciju ako želiš sigurnost i konfirmaciju pre brisanja.**

```bash
cd /home/aleksandarlukovic/MuseumInfoSystem
./clear_timesheet_data.sh
```

Script će:
1. ✅ Prikazati trenutne podatke
2. ✅ Kreirati novi backup
3. ⚠️ Tražiti konfirmaciju (mora se ukucati "YES")
4. ✅ Obrisati sve timesheet podatke
5. ✅ Resetovati ID sekvence (novi unosi kreću od ID 1)
6. ✅ Verifikovati uspešno brisanje
7. ✅ Prikazati summary i instrukcije za restore

**Prednosti:**
- Sigurnost (traži konfirmaciju)
- Automatski backup
- Detaljan output
- Restore instrukcije

---

### Opcija 2: Brzi SQL Script

**Koristi ovu opciju samo ako si 100% siguran!**

```bash
psql -U aleksandarlukovic -d museum_system -f /home/aleksandarlukovic/MuseumInfoSystem/clear_timesheet_quick.sql
```

**PAŽNJA:** Ovaj script NE traži konfirmaciju i obriše sve odmah!

---

### Opcija 3: Manuelne SQL Komande

Ako želiš potpunu kontrolu:

```sql
-- 1. Proveri trenutne podatke
SELECT COUNT(*) FROM timesheet_reports;
SELECT COUNT(*) FROM timesheet_entries;

-- 2. Napravi backup (pre nego što obrišeš!)
\! pg_dump -U aleksandarlukovic -d museum_system -t timesheet_reports -t timesheet_entries --data-only > /home/aleksandarlukovic/MuseumInfoSystem/backups/timesheet_data/manual_backup_$(date +%Y%m%d_%H%M%S).sql

-- 3. Obriši entries prvo (foreign key)
DELETE FROM timesheet_entries;

-- 4. Obriši reports
DELETE FROM timesheet_reports;

-- 5. Resetuj sekvence
ALTER SEQUENCE timesheet_reports_id_seq RESTART WITH 1;
ALTER SEQUENCE timesheet_entries_id_seq RESTART WITH 1;

-- 6. Verifikuj
SELECT COUNT(*) FROM timesheet_reports;  -- Treba biti 0
SELECT COUNT(*) FROM timesheet_entries;  -- Treba biti 0
```

---

## 📝 NAKON ČIŠĆENJA PODATAKA

### 1. Verifikacija da su podaci obrisani:

```bash
psql -U aleksandarlukovic -d museum_system -c "SELECT COUNT(*) as reports FROM timesheet_reports; SELECT COUNT(*) as entries FROM timesheet_entries;"
```

Trebalo bi da vidiš:
```
 reports
---------
       0

 entries
---------
       0
```

### 2. Provera da li sistem radi:

```bash
systemctl status museum-system.service
```

### 3. Pristup timesheet sistemu:

**URL:** http://localhost:5555/timesheet

---

## 👥 UNOS REALNIH PODATAKA

### Metod 1: Web Interface (PREPORUČENO za zaposlene)

**Korak po korak:**

1. **Otvori browser:** http://localhost:5555/login

2. **Login sa employee kredencijalima:**
   - Email: `ime.prezime@nhmbeo.rs`
   - Password: (lozinka zaposlenog)

3. **Idi na Timesheet:**
   - Klikni na "Систем за радне листе" u dashboard-u
   - Ili direktno: http://localhost:5555/timesheet

4. **Izaberi mesec i godinu:**
   - Trenutni mesec je automatski selektovan
   - Možeš izabrati bilo koji mesec/godinu

5. **Unesi radne sate po danima:**
   - Svaki dan ima dropdown za kategoriju
   - Unesi sate (decimalni broj, npr. 8, 7.5, 4)

   **8 Kategorija:**
   - **Рад у музеју** - Normalan rad u muzeju
   - **Рад ван музеја** - Terenske aktivnosti, konferencije
   - **Годишњи одмор** - Godišnji odmor
   - **Државни празник** - Državni praznici (automatski)
   - **Плаћено одсуство** - Plaćeno odsustvo
   - **Остало одсуство** - Drugo odsustvo
   - **Боловање < 30 дана** - Bolovanje kraće od 30 dana
   - **Боловање ≥ 30 дана** - Bolovanje duže od 30 dana

6. **Sačuvaj:**
   - Klikni "Сачувај" dugme
   - Sistem će sačuvati podatke u PostgreSQL bazu

7. **Pregled izvještaja:**
   - Admin može videti sve izvještaje: http://localhost:5555/admin/timesheet_reports
   - Može eksportovati u Word dokument

---

### Metod 2: Python Script (za bulk import)

Ako imaš već pripremljene podatke (npr. u Excel-u), možeš kreirati Python script:

```python
#!/usr/bin/env python3
import os
from datetime import datetime
from timesheet_repository import TimesheetRepository

# Inicijalizuj repository
db_url = os.environ.get('DATABASE_URL')
repo = TimesheetRepository(db_url)

# Primer podataka za jednog zaposlenog
employee_data = {
    'employee_name': 'Александар Луковић',
    'employee_email': 'aca.lukovic@nhmbeo.rs',
    'month': 1,  # Januar
    'year': 2026,
    'organization_unit': 'Геолошко одељење',
    'position': 'кустос минералог',
    'entries': [
        {'day': 1, 'category': 'drzavni_praznik', 'hours': 8, 'description': 'Нова Година'},
        {'day': 2, 'category': 'drzavni_praznik', 'hours': 8, 'description': 'Нова Година'},
        {'day': 3, 'category': 'rad_na_mestu', 'hours': 8, 'description': 'Редован рад'},
        {'day': 4, 'category': 'rad_na_mestu', 'hours': 8, 'description': 'Редован рад'},
        # ... dodaj sve dane meseca
    ]
}

# Sačuvaj u bazu
# (Potrebno je implementirati save_timesheet_report funkciju)
print("Import completed!")
```

---

### Metod 3: Direct SQL Insert (za admin-e)

```sql
-- Kreiraj report
INSERT INTO timesheet_reports (employee_name, employee_email, month, year, organization_unit, position)
VALUES ('Александар Луковић', 'aca.lukovic@nhmbeo.rs', 1, 2026, 'Геолошко одељење', 'кустос минералог')
RETURNING id;

-- Pretpostavimo da je dobijen ID = 1

-- Dodaj entries
INSERT INTO timesheet_entries (report_id, day, category, hours, description) VALUES
(1, 1, 'drzavni_praznik', 8, 'Нова Година'),
(1, 2, 'drzavni_praznik', 8, 'Нова Година'),
(1, 3, 'rad_na_mestu', 8, 'Редован рад'),
(1, 4, 'rad_na_mestu', 8, 'Редован рад'),
-- ... itd za sve dane
```

---

## 📅 VAŽNE NAPOMENE

### Kategorije rada (category vrijednosti):

| SQL Vrijednost | Opis na srpskom | Sati |
|----------------|-----------------|------|
| `rad_na_mestu` | Рад у музеју | 8 |
| `van_muzeja` | Рад ван музеја | 8 |
| `godisnji_odmor` | Годишњи одмор | 8 |
| `drzavni_praznik` | Државни празник | 8 |
| `placeno_odsustvo` | Плаћено одсуство | 8 |
| `ostalo_odsustvo` | Остало одсуство | 0 |
| `bolovanje_manje_30` | Боловање < 30 дана | 8 |
| `bolovanje_vece_30` | Боловање ≥ 30 дана | 8 |

### Državni praznici (automatski detektovani):

Sistem automatski prepoznaje srpske državne praznike:
- 1-2 Januar - Нова Година
- 7 Januar - Божић (Orthodox)
- 15-16 Februar - Дан државности
- Veliki Petak (promenljiv)
- Velika Subota (promenljiv)
- Uskrsnji Ponedeljak (promenljiv)
- 1-2 Maj - Praznik rada

### Radni sati:

- Standardan radni dan: **8 sati**
- Pola radnog dana: **4 sata**
- Decimalni unos dozvoljen: **7.5, 6.5, itd.**
- Maksimum po danu: **24 sata**

---

## 🔄 RESTORE PODATAKA (ako je potrebno)

### Ako si slučajno obrisao podatke koji ti trebaju:

```bash
# Pronađi backup fajl
ls -lh /home/aleksandarlukovic/MuseumInfoSystem/backups/timesheet_data/

# Restore iz backup-a
psql -U aleksandarlukovic -d museum_system < /home/aleksandarlukovic/MuseumInfoSystem/backups/timesheet_data/timesheet_backup_20260109_115900.sql
```

### Verifikuj restore:

```bash
psql -U aleksandarlukovic -d museum_system -c "SELECT COUNT(*) FROM timesheet_reports; SELECT COUNT(*) FROM timesheet_entries;"
```

---

## 📊 MONITORING I IZVJEŠTAJI

### Provera unesenih podataka:

```bash
# Broj izvještaja po zaposlenom
psql -U aleksandarlukovic -d museum_system -c "
SELECT employee_name, COUNT(*) as reports
FROM timesheet_reports
GROUP BY employee_name
ORDER BY reports DESC;
"

# Poslednjih 10 izvještaja
psql -U aleksandarlukovic -d museum_system -c "
SELECT id, employee_name, month, year,
       TO_CHAR(generated_at, 'YYYY-MM-DD HH24:MI') as created
FROM timesheet_reports
ORDER BY generated_at DESC
LIMIT 10;
"

# Ukupno sati po kategoriji za sve zaposlene
psql -U aleksandarlukovic -d museum_system -c "
SELECT category, SUM(hours) as total_hours, COUNT(*) as entries
FROM timesheet_entries
GROUP BY category
ORDER BY total_hours DESC;
"
```

### Admin pregled izvještaja:

**URL:** http://localhost:5555/admin/timesheet_reports

Features:
- Pregled svih izvještaja
- Filter po mesecima/godini
- Pretraga po imenu zaposlenog
- Export u Word dokument
- Detaljni pregled svakog izvještaja

---

## ⚠️ TROUBLESHOOTING

### Problem: "Permission denied" pri pokretanju script-a

```bash
chmod +x /home/aleksandarlukovic/MuseumInfoSystem/clear_timesheet_data.sh
```

### Problem: "Connection refused" - PostgreSQL nije pokrenut

```bash
sudo systemctl start postgresql
sudo systemctl status postgresql
```

### Problem: Ne mogu da pristupim /timesheet

```bash
# Proveri da li je museum-system servis pokrenut
systemctl status museum-system.service

# Restartuj ako treba
sudo systemctl restart museum-system.service

# Proveri logove
tail -f /home/aleksandarlukovic/MuseumInfoSystem/logs/museum_info_system.log
```

### Problem: Nepoštuju se podatke nakon unosa

```bash
# Proveri da li se čuva u PostgreSQL
psql -U aleksandarlukovic -d museum_system -c "SELECT * FROM timesheet_reports ORDER BY generated_at DESC LIMIT 1;"

# Očisti browser cache i sesije
rm -rf /home/aleksandarlukovic/MuseumInfoSystem/flask_session/*
```

---

## 📚 DODATNI RESURSI

### Dokumentacija:
- **TIMESHEET_QUICKSTART.md** - Brzi start guide
- **TIMESHEET_INTEGRATION_COMPLETE.md** - Tehnička dokumentacija
- **MUSEUM_SYSTEM_SCHEMA.md** - Kompletna šema sistema

### Logovi:
```bash
# Aplikacijski logovi
tail -f /home/aleksandarlukovic/MuseumInfoSystem/logs/museum_info_system.log

# Gunicorn logovi
tail -f /home/aleksandarlukovic/MuseumInfoSystem/logs/gunicorn_error.log

# PostgreSQL logovi
sudo journalctl -u postgresql -f
```

---

## ✅ CHECKLIST ZA UNOS REALNIH PODATAKA

- [ ] 1. Napravi backup postojećih podataka
- [ ] 2. Pokreni cleanup script
- [ ] 3. Verifikuj da su podaci obrisani (COUNT = 0)
- [ ] 4. Testiraj pristup timesheet sistemu
- [ ] 5. Obuči zaposlene kako da unesu podatke
- [ ] 6. Pokreni probni unos za jedan mesec
- [ ] 7. Verifikuj da se podaci čuvaju
- [ ] 8. Generiši test izvještaj
- [ ] 9. Eksportuj u Word dokument
- [ ] 10. Počni sa redovnim unosom podataka

---

## 📞 PODRŠKA

**Za tehničku podršku:**
- Aleksandar Luković: aca.lukovic@nhmbeo.rs

**Lokacija script-ova:**
- Cleanup script: `/home/aleksandarlukovic/MuseumInfoSystem/clear_timesheet_data.sh`
- Quick SQL: `/home/aleksandarlukovic/MuseumInfoSystem/clear_timesheet_quick.sql`
- Backups: `/home/aleksandarlukovic/MuseumInfoSystem/backups/timesheet_data/`

---

**Kreiran:** 2026-01-09
**Status:** Ready to clear and enter real data ✅
