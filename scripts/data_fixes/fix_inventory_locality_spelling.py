#!/usr/bin/env python3
"""
Fix locality spelling in PostgreSQL inventory_entries table.
Corrects missing Serbian diacritical marks (č, ć, š, ž, đ).
"""

import psycopg
import re

DATABASE_URL = 'postgresql://aleksandarlukovic@localhost:5432/museum_system'

def apply_word_corrections(text):
    """Apply word-by-word corrections to a locality string."""
    if not text:
        return text
    
    result = text
    
    # Word replacements (comprehensive list)
    word_corrections = {
        # Country names
        'Cehoslovacka': 'Čehoslovačka',
        'Ceholsovacka': 'Čehoslovačka',
        'Nemacka': 'Nemačka',
        'Svajcarska': 'Švajcarska',
        'Spanija': 'Španija',
        'Grcka': 'Grčka',
        'Norveska': 'Norveška',
        'Madjarska': 'Mađarska',
        'Brazilia': 'Brazilija',
        
        # Regions
        'Stajerska': 'Štajerska',
        'Koruska': 'Koruška',
        'Slezija': 'Šlezija',
        'Saksonska': 'Saksonija',
        
        # Serbian places
        'Trepca': 'Trepča',
        'Cacak': 'Čačak',
        'Zajaca': 'Zajača',
        'Pasjaca': 'Pasjača',
        'Mackatica': 'Mačkatica',
        'Busovaca': 'Busovača',
        'Kresevo': 'Kreševo',
        'Vares': 'Vareš',
        'Caniste': 'Čanište',
        'Suplja': 'Šuplja',
        'Sipacina': 'Šipačina',
        'Semnic': 'Šemnic',
        'Smira': 'Šmira',
        'Mezice': 'Mežice',
        'Cechy': 'Čechy',
        'Ceska': 'Češka',
        'Makedonijia': 'Makedonija',
        
        # Transcriptions
        'Schwarzwald': 'Švarcvald',
        'Djebel': 'Džebel',
        'Djerdjenti': 'Đerđenti',
        'Djurdjenti': 'Đurđenti',
        'Djakovica': 'Đakovica',
        'Dzep': 'Džep',
        'Dzumeb': 'Džumeb',
    }
    
    for wrong, correct in word_corrections.items():
        # Word boundary replacement
        pattern = r'\b' + re.escape(wrong) + r'\b'
        result = re.sub(pattern, correct, result)
        # Also handle comma/period-attached cases
        result = result.replace(wrong + ',', correct + ',')
        result = result.replace(wrong + '.', correct + '.')
        result = result.replace(',' + wrong, ',' + correct)
        result = result.replace(' ' + wrong + ' ', ' ' + correct + ' ')
    
    return result

def fix_localities():
    """Apply all corrections to inventory_entries."""
    corrections_made = []
    
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            # Get all localities
            cur.execute("""
                SELECT DISTINCT locality 
                FROM inventory_entries 
                WHERE locality IS NOT NULL AND locality != ''
            """)
            localities = [row[0] for row in cur.fetchall()]
            
            for original in localities:
                corrected = apply_word_corrections(original)
                
                if corrected != original:
                    corrections_made.append((original, corrected))
                    cur.execute("""
                        UPDATE inventory_entries 
                        SET locality = %s 
                        WHERE locality = %s
                    """, (corrected, original))
                    
            conn.commit()
    
    return corrections_made

if __name__ == '__main__':
    print("Fixing inventory_entries localities...")
    corrections = fix_localities()
    
    print(f"\nMade {len(corrections)} corrections:")
    for original, corrected in sorted(corrections):
        print(f"  '{original}' -> '{corrected}'")
    
    print("\nDone!")
