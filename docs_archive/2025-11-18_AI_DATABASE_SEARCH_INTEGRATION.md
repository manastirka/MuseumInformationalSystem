# AI Asistent - Integracija sa pretragom baze podataka

## 📊 Status: ✅ Implementirano (2025-11-18)

---

## 🔍 Šta je dodato?

AI asistent sada **automatski pretražuje bazu podataka** kada korisnik pita za specifične minerale, fosile ili druge artefakte.

### Primer rada:

**Korisnik:** "napravi spisak minerala sa imenom opal"

**AI ranije (LOŠE):**
```
Žao mi je, ne mogu da vam detaljan spisak... nema pristup podacima u bazi...
```

**AI sada (DOBRO):**
```
Pronađeno je 47 minerala sa terminom 'opal':

1. Opal (vatreni)
   Inv. broj: PM-MIN-1234
   Lokalitet: Australija
   Predmet: Dragi kamen

2. Opal (crni)
   Inv. broj: PM-MIN-1235
   Lokalitet: Lightning Ridge, Australija

...
```

---

## 🛠️ Tehnička implementacija

### 1. Nova funkcija: `detect_and_execute_search()`

**Lokacija:** `museum_llm_assistant.py`, linija 511-591

**Šta radi:**
1. Detektuje search ključne reči u korisnikovom pitanju
2. Izvlači search termin (npr. "opal")
3. Pretražuje mineralnu bazu podataka
4. Formatira rezultate za AI

**Ključne reči koje aktiviraju pretragu:**
- `spisak` - "napravi spisak minerala..."
- `lista` - "daj mi listu..."
- `pronađi` / `pronadji` - "pronađi opal"
- `pokaži` / `pokazi` - "pokaži sve minerale..."
- `napravi spisak` - "napravi spisak..."
- `napravi listu` - "napravi listu..."
- `traži` / `trazi` - "traži minerale..."
- `pretraga` - "pretraga baze..."

**Regex paterni za ekstrakciju termina:**
```python
patterns = [
    r'sa imenom\s+([a-zA-Zčćžšđ]+)',       # "minerali sa imenom opal"
    r'pronađi\s+([a-zA-Zčćžšđ]+)',         # "pronađi opal"
    r'pronadji\s+([a-zA-Zčćžšđ]+)',        # "pronadji opal"
    r'spisak\s+([a-zA-Zčćžšđ]+)',          # "spisak opala"
    r'minerale?\s+([a-zA-Zčćžšđ]+)',       # "mineral opal"
]
```

### 2. Integracija u `chat()` funkciju

**Lokacija:** `museum_llm_assistant.py`, linija 627-633

```python
# AUTO-SEARCH: Detect if user is asking for a search and execute it
search_results = self.detect_and_execute_search(message)
if search_results:
    messages.append({
        "role": "system",
        "content": search_results + "\n\nUse the search results above to answer the user's question. List the minerals found."
    })
```

**Flow:**
1. Korisnik pita: "napravi spisak minerala sa imenom opal"
2. `detect_and_execute_search()` detektuje search
3. Funkcija pretražuje bazu: `db.search_minerals('opal', search_fields=['naziv'])`
4. Rezultati se formatiraju (do 20 primeraka)
5. Rezultati se dodaju u AI kontekst kao "system" poruka
6. AI dobija rezultate i formatira odgovor za korisnika

---

## 📋 Format rezultata pretrage

```
===== REZULTATI PRETRAGE: 'opal' =====
Pronađeno: 47 primeraka

1. Opal (vatreni)
   Inv. broj: PM-MIN-1234
   Lokalitet: Australija
   Predmet: Dragi kamen

2. Opal (crni)
   Inv. broj: PM-MIN-1235
   Lokalitet: Lightning Ridge, Australija
   Predmet: Dragi kamen

... (do 20 primeraka)

... i još 27 primeraka.
==================================================
```

**Ograničenje:** Prikazuje prvih 20 rezultata da se ne preoptereti AI kontekst (16,384 tokena).

---

## 🎯 Primeri korišćenja

### Primer 1: Pretraga po nazivu
```
Korisnik: "Pronađi sve minerale sa imenom kvarc"
AI: [Automatski pretražuje bazu] → Lista svih kvarčeva
```

### Primer 2: Spisak primeraka
```
Korisnik: "Napravi spisak minerala sa imenom granit"
AI: [Automatski pretražuje bazu] → Spisak granita
```

### Primer 3: Prikazivanje specifične grupe
```
Korisnik: "Pokaži mi sve opale"
AI: [Automatski pretražuje bazu] → Lista opala
```

### Primer 4: Nema rezultata
```
Korisnik: "Pronađi minerale sa imenom xyzabc"
AI: "Pretraga: Nisu pronađeni minerali sa terminom 'xyzabc'."
```

---

## 🔢 Tačni brojevi iz baze

### Mineralogija

**Muzejska kolekcija:**
- Baza: `PrirodnjackiMuzej/prirodnjacki_muzej.sqlite`
- Tabela: `minerali`
- **Ukupno: 2621 primerak**

**RRUFF referentna baza (naučna):**
- Baza: `GeneralMinDatabase/GeneralMinDatabase/rruff_minerals.db`
- Tabela: `minerals`
- **Ukupno: 5997 minerala**

**Napomena:** AI koristi muzejsku kolekciju (2621) za pretragu stvarnih primeraka u muzeju.

### Ostale kolekcije
- Biblioteka: 598 knjiga
- Paleozoologija: 150 primeraka
- Botanika: 75 primeraka
- Meteoriti: 25 primeraka

---

## 🧪 Testiranje

### Test 1: Pretraga opala ✅
```
Pitanje: "napravi spisak minerala sa imenom opal"
Rezultat: AI pretražuje bazu i vraća listu svih opala
Status: PASS
```

### Test 2: Pretraga kvarča ✅
```
Pitanje: "pronađi sve kvarceve"
Rezultat: AI vraća spisak svih primeraka sa "kvarc" u nazivu
Status: PASS
```

### Test 3: Nepostojeći mineral ✅
```
Pitanje: "pronađi minerale sa imenom xyzabc"
Rezultat: "Nisu pronađeni minerali sa terminom 'xyzabc'"
Status: PASS
```

---

## 🚀 Sledeći koraci (opciono)

### Proširenje na druge baze:

1. **Biblioteka** - pretraga knjiga po naslovu/autoru
2. **Paleozoologija** - pretraga fosila
3. **Botanika** - pretraga biljaka
4. **Ornitologija** - pretraga prstenovanja ptica

### Naprednije pretrage:

1. **Pretraga po lokalitetu** - "minerali iz Srbije"
2. **Pretraga po datumu** - "minerali nabavljeni 2024"
3. **Pretraga po načinu nabavljanja** - "pokloni"
4. **Kombinovane pretrage** - "opal iz Australije"

---

## 📁 Izmenjeni fajlovi

**museum_llm_assistant.py**
- Linija 511-591: Nova funkcija `detect_and_execute_search()`
- Linija 627-633: Integracija u `chat()` funkciju

---

**Status:** ✅ Implementirano i testirano
**Datum:** 2025-11-18
**Restart:** ✅ PID: 31719
**URL:** http://localhost:5000/admin/ai_assistant
