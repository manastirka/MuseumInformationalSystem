#!/usr/bin/env python3
"""
Analyze Yugoslav localities in mineral database
Identify famous mining districts and prepare data for exhibition
"""

import sqlite3
import json
from collections import defaultdict

DB_PATH = 'PrirodnjackiMuzej/prirodnjacki_muzej.sqlite'

def get_connection():
    return sqlite3.connect(DB_PATH)

# Yugoslav region keywords
yugoslav_keywords = {
    'serbia': ['srbij', 'serbia', 'beograd', 'belgrade'],
    'kosovo': ['kosovo', 'kim', 'kosmet'],
    'bosnia': ['bosn', 'bih'],
    'croatia': ['hrvat', 'croat'],
    'montenegro': ['crna gora', 'montenegro'],
    'slovenia': ['sloveni', 'slovenia'],
    'macedonia': ['makedon', 'macedonia']
}

# Famous localities to focus on
famous_localities = [
    'trepča', 'trepca',
    'bor',
    'majdanpek',
    'rudnik',
    'kopaonik',
    'rtanj',
    'alšar', 'alsar',
    'mežice', 'mezice',
    'zajača', 'zajaca',
    'stolice',
    'busovača', 'busovaca',
    'srebrenica',
    'čajniče', 'cajnice',
    'koželj', 'kozelj'
]

conn = get_connection()
cursor = conn.cursor()

# Get all minerals with localities from former Yugoslavia
cursor.execute("""
    SELECT
        id,
        "Inv. broj" as inv_broj,
        "Naziv" as naziv,
        "Lokalitet sa kartice" as lokalitet,
        "Predmet" as predmet,
        "Napomena/opis" as opis,
        "Komentar/napomena" as komentar,
        "Način nabavljanja" as nacin_nabavljanja,
        "Datum nabavljanja" as datum_nabavljanja
    FROM minerali
    WHERE "Lokalitet sa kartice" IS NOT NULL
    AND "Lokalitet sa kartice" != ''
    AND "Naziv" IS NOT NULL
    AND "Naziv" != ''
    ORDER BY "Lokalitet sa kartice", "Inv. broj"
""")

all_minerals = cursor.fetchall()

# Group by locality
localities_dict = defaultdict(list)

for mineral in all_minerals:
    mid, inv, naziv, lokalitet, predmet, opis, komentar, nacin, datum = mineral
    lokalitet_lower = lokalitet.lower() if lokalitet else ''

    # Check if from Yugoslav region
    is_yugoslav = False
    for region, keywords in yugoslav_keywords.items():
        if any(kw in lokalitet_lower for kw in keywords):
            is_yugoslav = True
            break

    if is_yugoslav:
        localities_dict[lokalitet].append({
            'id': mid,
            'inv_broj': int(inv) if inv else None,
            'naziv': naziv,
            'lokalitet': lokalitet,
            'predmet': predmet,
            'opis': opis,
            'komentar': komentar,
            'nacin_nabavljanja': nacin,
            'datum_nabavljanja': datum
        })

# Sort by specimen count
sorted_localities = sorted(localities_dict.items(), key=lambda x: len(x[1]), reverse=True)

print("="*100)
print("LOCALITIES FROM FORMER YUGOSLAVIA")
print("="*100)
print(f"\nTotal localities found: {len(sorted_localities)}")
print(f"Total specimens: {sum(len(v) for v in localities_dict.values())}")

print("\n" + "="*100)
print("TOP 30 LOCALITIES BY SPECIMEN COUNT:")
print("="*100)

for i, (locality, specimens) in enumerate(sorted_localities[:30], 1):
    print(f"{i:2}. {locality:50} - {len(specimens):4} specimens")
    # Show sample minerals
    sample_names = list(set([s['naziv'] for s in specimens[:10]]))[:5]
    print(f"    Sample minerals: {', '.join(sample_names)}")

# Identify major mining districts by grouping similar locality names
print("\n" + "="*100)
print("MAJOR MINING DISTRICTS:")
print("="*100)

major_districts = {}

# Trepča complex
trepca_specimens = []
for locality, specimens in localities_dict.items():
    if 'trepč' in locality.lower() or 'trepca' in locality.lower():
        trepca_specimens.extend(specimens)
major_districts['Trepča'] = trepca_specimens

# Bor
bor_specimens = []
for locality, specimens in localities_dict.items():
    if 'bor' in locality.lower() and 'dolni bor' not in locality.lower():
        bor_specimens.extend(specimens)
major_districts['Bor'] = bor_specimens

# Majdanpek
majdanpek_specimens = []
for locality, specimens in localities_dict.items():
    if 'majdanpek' in locality.lower():
        majdanpek_specimens.extend(specimens)
major_districts['Majdanpek'] = majdanpek_specimens

# Rudnik
rudnik_specimens = []
for locality, specimens in localities_dict.items():
    if 'rudnik' in locality.lower() and 'suvo rud' not in locality.lower():
        rudnik_specimens.extend(specimens)
major_districts['Rudnik'] = rudnik_specimens

# Kopaonik
kopaonik_specimens = []
for locality, specimens in localities_dict.items():
    if 'kopaonik' in locality.lower():
        kopaonik_specimens.extend(specimens)
major_districts['Kopaonik'] = kopaonik_specimens

# Rtanj
rtanj_specimens = []
for locality, specimens in localities_dict.items():
    if 'rtanj' in locality.lower():
        rtanj_specimens.extend(specimens)
major_districts['Rtanj'] = rtanj_specimens

# Mežica (Slovenia)
mezice_specimens = []
for locality, specimens in localities_dict.items():
    if 'mežic' in locality.lower() or 'mezic' in locality.lower():
        mezice_specimens.extend(specimens)
major_districts['Mežica'] = mezice_specimens

# Alšar (Macedonia)
alsar_specimens = []
for locality, specimens in localities_dict.items():
    if 'alšar' in locality.lower() or 'alsar' in locality.lower():
        alsar_specimens.extend(specimens)
major_districts['Alšar'] = alsar_specimens

# Busovača (Bosnia)
busovaca_specimens = []
for locality, specimens in localities_dict.items():
    if 'busovač' in locality.lower() or 'busovac' in locality.lower() or 'tisovac' in locality.lower():
        busovaca_specimens.extend(specimens)
major_districts['Busovača'] = busovaca_specimens

# Zajača
zajaca_specimens = []
for locality, specimens in localities_dict.items():
    if 'zajač' in locality.lower() or 'zajac' in locality.lower():
        zajaca_specimens.extend(specimens)
major_districts['Zajača'] = zajaca_specimens

# Stolice
stolice_specimens = []
for locality, specimens in localities_dict.items():
    if 'stolice' in locality.lower():
        stolice_specimens.extend(specimens)
major_districts['Stolice'] = stolice_specimens

# Jastrebac/Crna Trava region
jastrebac_specimens = []
for locality, specimens in localities_dict.items():
    if 'jastrebac' in locality.lower() or 'crna trava' in locality.lower() or 'bučje' in locality.lower():
        jastrebac_specimens.extend(specimens)
if jastrebac_specimens:
    major_districts['Jastrebac'] = jastrebac_specimens

# Lece
lece_specimens = []
for locality, specimens in localities_dict.items():
    if 'lece' in locality.lower() or 'leće' in locality.lower():
        lece_specimens.extend(specimens)
if lece_specimens:
    major_districts['Lece'] = lece_specimens

# Avala
avala_specimens = []
for locality, specimens in localities_dict.items():
    if 'avala' in locality.lower():
        avala_specimens.extend(specimens)
if avala_specimens:
    major_districts['Avala'] = avala_specimens

# Display major districts
for district, specimens in sorted(major_districts.items(), key=lambda x: len(x[1]), reverse=True):
    if len(specimens) > 0:
        print(f"\n{district}: {len(specimens)} specimens")
        # Get unique mineral names
        unique_minerals = {}
        for s in specimens:
            name = s['naziv']
            if name not in unique_minerals:
                unique_minerals[name] = 1
            else:
                unique_minerals[name] += 1

        # Top minerals
        top_minerals = sorted(unique_minerals.items(), key=lambda x: x[1], reverse=True)[:8]
        print(f"  Top minerals: {', '.join([f'{m[0]} ({m[1]})' for m in top_minerals])}")

# Save data for document generation
output_data = {
    'major_districts': {}
}

for district, specimens in major_districts.items():
    if len(specimens) > 0:
        # Select up to 15 most diverse specimens
        selected = []
        seen_names = {}

        # First pass: one of each unique mineral
        for specimen in specimens:
            name = specimen['naziv']
            if name not in seen_names:
                selected.append(specimen)
                seen_names[name] = 1
                if len(selected) >= 15:
                    break

        # Second pass: add more if we have room and prefer specimens with inventory numbers
        if len(selected) < 15:
            for specimen in specimens:
                name = specimen['naziv']
                if specimen['inv_broj'] and (name not in seen_names or seen_names[name] < 2):
                    if specimen not in selected:
                        selected.append(specimen)
                        seen_names[name] = seen_names.get(name, 0) + 1
                        if len(selected) >= 15:
                            break

        output_data['major_districts'][district] = {
            'total_specimens': len(specimens),
            'selected_specimens': selected[:15]
        }

with open('yugoslav_localities_data.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("\n" + "="*100)
print(f"Data saved to yugoslav_localities_data.json")
print(f"Major districts identified: {len([d for d, s in major_districts.items() if len(s) > 0])}")
print("="*100)

conn.close()
