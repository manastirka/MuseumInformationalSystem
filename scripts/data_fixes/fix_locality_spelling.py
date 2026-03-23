#!/usr/bin/env python3
"""
Fix locality spelling in PostgreSQL minerals database.
Corrects missing Serbian diacritical marks (č, ć, š, ž, đ).
"""

import psycopg

# Database connection
DATABASE_URL = 'postgresql://aleksandarlukovic@localhost:5432/museum_system'

# Comprehensive spelling corrections dictionary
# Format: 'incorrect' -> 'correct'
CORRECTIONS = {
    # Country names
    'Cehoslovacka': 'Čehoslovačka',
    'Čehoslovačka': 'Čehoslovačka',  # Already correct, keep consistent
    'Ceska': 'Češka',
    'Nemacka': 'Nemačka',
    'Svajcarska': 'Švajcarska',
    'Spanija': 'Španija',
    'Grcka': 'Grčka',
    'Norveska': 'Norveška',
    'Madjarska': 'Mađarska',
    'Brazilia': 'Brazilija',
    
    # Region names  
    'Stajerska': 'Štajerska',
    'Saksonska': 'Saksonija',
    'Slezija': 'Šlezija',
    'Sicilija': 'Sicilija',  # This is correct
    'Koruska': 'Koruška',
    'Moravska': 'Moravska',  # This is correct
    
    # Serbian/Yugoslav place names
    'Trepca': 'Trepča',
    'Trepča': 'Trepča',  # Keep consistent
    'trepča': 'Trepča',  # Capitalize
    'Cacak': 'Čačak',
    'Zajaca': 'Zajača',
    'Pasjaca': 'Pasjača',
    'Mackatica': 'Mačkatica',
    'Crnajka': 'Crnjaka',  # or keep as is if correct
    'Semnic': 'Šemnic',
    'Smira': 'Šmira',
    'Caniste': 'Čanište',
    'Suplja': 'Šuplja',
    'Sipacina': 'Šipačina',
    'Sipačina': 'Šipačina',
    'Siparčika': 'Šipačika',
    'Cumavić': 'Čumavić',
    'Cechy': 'Čechy',
    'Makedonijia': 'Makedonija',
    
    # Specific location corrections (word by word replacement)
    'Stajerska, Nemacka': 'Štajerska, Nemačka',
    'Stajerska, Austrija': 'Štajerska, Austrija',
    'Gornja Stajerska': 'Gornja Štajerska',
    'Obervald, Stajerska': 'Obervald, Štajerska',
    'Steiermark, Nemacka': 'Štajerska, Nemačka',
    
    # Czech locations
    'Cehoslovacka': 'Čehoslovačka',
    'Ceholsovacka': 'Čehoslovačka',
    'Cehoslvacka': 'Čehoslovačka',
    'ČSSR': 'Čehoslovačka',
    
    # German places with correct spelling
    'Frajberg': 'Frajberg',  # Keep German transcription
    'Frajberg, Nemacka': 'Frajberg, Nemačka',
    'Freiberg,Nemacka': 'Frajberg, Nemačka',
    'Schwarzwald,Nemacka': 'Švarcvald, Nemačka',
    'Schwarzwald, Nemacka': 'Švarcvald, Nemačka',
    'Schwarzwald, Nemačka': 'Švarcvald, Nemačka',
    
    # Various typos and inconsistencies
    'Alšar, Makedonijia': 'Alšar, Makedonija',
    'Busovaca, Bosna': 'Busovača, Bosna',
    'Busovača, BIH': 'Busovača, BiH',
    'Busovaca, BiH': 'Busovača, BiH',
    'Kresevo': 'Kreševo',
    'Vares': 'Vareš',
    'Mezice,Slovenija': 'Mežice, Slovenija',
    'Mezice': 'Mežice',
    
    # Specific mine/location fixes
    'Stari trg, Trepca': 'Stari Trg, Trepča',
    'Stari Trg, Trepca': 'Stari Trg, Trepča', 
    'Stari trg, Trepča': 'Stari Trg, Trepča',
    'Stari Trg, Trepča. Srbija': 'Stari Trg, Trepča, Srbija',
    'Stari Trg, trepča, Srbija': 'Stari Trg, Trepča, Srbija',
}

def get_all_localities():
    """Get all distinct localities from database."""
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT card_locality 
                FROM minerals 
                WHERE card_locality IS NOT NULL AND card_locality != ''
                ORDER BY card_locality
            """)
            return [row[0] for row in cur.fetchall()]

def apply_word_corrections(text):
    """Apply word-by-word corrections to a locality string."""
    if not text:
        return text
    
    result = text
    
    # Word replacements (case-sensitive for accuracy)
    word_corrections = {
        'Cehoslovacka': 'Čehoslovačka',
        'Ceholsovacka': 'Čehoslovačka',
        'Nemacka': 'Nemačka',
        'Svajcarska': 'Švajcarska',
        'Spanija': 'Španija',
        'Grcka': 'Grčka',
        'Norveska': 'Norveška',
        'Madjarska': 'Mađarska',
        'Stajerska': 'Štajerska',
        'Trepca': 'Trepča',
        'Cacak': 'Čačak',
        'Zajaca': 'Zajača',
        'Pasjaca': 'Pasjača',
        'Mackatica': 'Mačkatica',
        'Busovaca': 'Busovača',
        'Kresevo': 'Kreševo',
        'Vares': 'Vareš',
        'Caniste': 'Čanište',
        'Cechy': 'Čechy',
        'Ceska': 'Češka',
        'Makedonijia': 'Makedonija',
        'Suplja': 'Šuplja',
        'Sipacina': 'Šipačina',
        'Koruska': 'Koruška',
        'Slezija': 'Šlezija',
        'Semnic': 'Šemnic',
        'Smira': 'Šmira',
        'Mezice': 'Mežice',
        'Brazilia': 'Brazilija',
        # Additional corrections
        'Schwarzwald': 'Švarcvald',
        'Isl': 'Išl',
        'Civis': 'Civiš',
        'Dzep': 'Džep',
        'Dzumeb': 'Džumeb',
        'Djakovica': 'Đakovica',
        'Djebel': 'Džebel',
        'Djerdjenti': 'Đerđenti',
        'Djurdjenti': 'Đurđenti',
    }
    
    for wrong, correct in word_corrections.items():
        # Replace as whole word or at word boundaries
        import re
        pattern = r'\b' + re.escape(wrong) + r'\b'
        result = re.sub(pattern, correct, result, flags=re.IGNORECASE if wrong[0].isupper() else 0)
        # Also handle comma-attached cases
        result = result.replace(wrong + ',', correct + ',')
        result = result.replace(wrong + '.', correct + '.')
        result = result.replace(',' + wrong, ',' + correct)
    
    return result

def fix_localities():
    """Apply all corrections to the database."""
    corrections_made = []
    
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            # Get all localities
            cur.execute("""
                SELECT DISTINCT card_locality 
                FROM minerals 
                WHERE card_locality IS NOT NULL AND card_locality != ''
            """)
            localities = [row[0] for row in cur.fetchall()]
            
            for original in localities:
                corrected = apply_word_corrections(original)
                
                # Check direct corrections dictionary
                if original in CORRECTIONS:
                    corrected = CORRECTIONS[original]
                
                if corrected != original:
                    corrections_made.append((original, corrected))
                    # Update database
                    cur.execute("""
                        UPDATE minerals 
                        SET card_locality = %s 
                        WHERE card_locality = %s
                    """, (corrected, original))
                    
            conn.commit()
    
    return corrections_made

if __name__ == '__main__':
    print("Analyzing localities for corrections...")
    localities = get_all_localities()
    print(f"Found {len(localities)} distinct localities")
    
    print("\nApplying corrections...")
    corrections = fix_localities()
    
    print(f"\nMade {len(corrections)} corrections:")
    for original, corrected in sorted(corrections):
        print(f"  '{original}' -> '{corrected}'")
    
    print("\nDone!")
