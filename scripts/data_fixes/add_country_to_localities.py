#!/usr/bin/env python3
"""
Add missing country names to localities in PostgreSQL minerals database.
"""

import psycopg
import re

DATABASE_URL = 'postgresql://aleksandarlukovic@localhost:5432/museum_system'

# Serbian places - will add ", Srbija"
SERBIAN_PLACES = [
    'Avala', 'Beograd', 'Kosmaj', 'Bukulja', 'Rudnik', 'Kopaonik', 'Fruška gora', 'Fruška Gora',
    'Majdanpek', 'Bor', 'Zaječar', 'Niš', 'Vranje', 'Leskovac', 'Prokuplje', 'Pirot',
    'Kragujevac', 'Čačak', 'Užice', 'Valjevo', 'Šabac', 'Loznica', 'Krupanj', 'Ljubovija',
    'Aranđelovac', 'Arandjelovac', 'Topola', 'Smederevo', 'Požarevac', 'Negotin',
    'Trstenik', 'Kruševac', 'Aleksandrovac', 'Raška', 'Novi Pazar', 'Tutin',
    'Zlatibor', 'Tara', 'Mokra Gora', 'Ivanjica', 'Arilje', 'Požega', 'Bajina Bašta',
    'Sjenica', 'Prijepolje', 'Nova Varoš', 'Priboj',
    'Kikinda', 'Zrenjanin', 'Vršac', 'Pančevo', 'Novi Sad', 'Subotica', 'Sombor',
    'Sremska Mitrovica', 'Šid', 'Ruma', 'Inđija', 'Stara Pazova',
    # Specific Serbian localities
    'Stolice', 'Stolica', 'Zajača', 'Zajaca', 'Mačkatica', 'Mackatica',
    'Trepča', 'Stari Trg', 'Lece', 'Kukavica', 'Besna Kobila', 'Besna kobila',
    'Pasjača', 'Pasjaca', 'Blagojev Kamen', 'Blagojev kamen',
    'Goleš', 'Goles', 'Novo Brdo', 'Ajvalija', 'Badovac', 'Bare',
    'Bujanovac', 'Preševo', 'Presevo', 'Vrnjci', 'Sijarinska Banja',
    'Rudna glava', 'Kučajna', 'Kucajna', 'Neresnica', 'Petrovac na Mlavi',
    'Homoljski srez', 'Homoljske planine', 'Crnjaka', 'Crnajka',
    'Degurić', 'Deguric', 'Ljubić', 'Ljubic', 'Grošnica', 'Grosnica',
    'Lipnica', 'Gruža', 'Gruza', 'Stragari', 'Batočina', 'Batocina',
    'Ripanj', 'Rakovica', 'Leštane', 'Lestane', 'Šuplja stena', 'Suplja stena',
    'Koporić', 'Koporic', 'Jošanička banja', 'Josanicka banja',
    'Suvo Rudište', 'Suvo rudiste', 'Suvo Rudiste', 'Zimovnik',
    'Banjica', 'Savsko jezero', 'Resavska pećina', 'Risovača',
    'Kanjon Uvca', 'Zavlaka', 'Plana', 'Venčac', 'Vencac',
    'Cer', 'Suvobor', 'Maljen', 'Povlen', 'Medvednik',
    'Boljevac', 'Knjaževac', 'Sokobanja', 'Svrljig',
    'Vlasotince', 'Lebane', 'Medveđa', 'Bojnik',
    'Blace', 'Kuršumlija', 'Brus', 'Žitorađa',
    'Gadžin han', 'Doljevac', 'Merošina', 'Surdulica', 'Bosilegrad', 'Bosiljgrad',
    'Trgovište', 'Vladičin Han', 'Crna Trava',
    # Rivers and mountains
    'Jovačka reka', 'Jovacka reka', 'Dobrotinjska reka', 'Dobrotinska reka',
    'Klinovački potok', 'Klinovacki potok', 'Kiževak potok', 'Kizevak potok',
    'Leštarski potok', 'Lestarski potok', 'Razanska reka',
    # Specific mines/locations
    'Bor, dnevni kop', 'Borski rudnik', 'Bor - rudnik',
    'horizont', 'potkop', 'etaža',
]

# Makedonija places
MACEDONIAN_PLACES = [
    'Prilep', 'Bitolj', 'Skopje', 'Tetovo', 'Kumanovo', 'Štip', 'Stip',
    'Ohrid', 'Struga', 'Veles', 'Kočani', 'Kocani', 'Strumica', 'Gevgelija',
    'Kavadarci', 'Negotino', 'Debar', 'Kičevo', 'Kicevo', 'Gostivar',
    'Kratovo', 'Probištip', 'Probistip', 'Delčevo', 'Delcevo', 'Berovo',
    'Alšar', 'Alsar', 'Zletovo', 'Lojane', 'Nežilovo', 'Nezilovo',
    'Čanište', 'Caniste', 'Selečke planine', 'Selecke planine',
    'Orehovo', 'Dobrevo', 'Dbrevo', 'Alinci', 'Prilepac',
    'Modra Glava', 'Golesnica', 'Rabrovo', 'Spančevo', 'Spancevo',
    'Pelagonija', 'Tikveš', 'Tikves', 'Polog',
    'Drenovci', 'Babuna', 'Tajmiste', 'Matejča', 'Matejca',
]

# BiH places  
BIH_PLACES = [
    'Sarajevo', 'Banja Luka', 'Tuzla', 'Zenica', 'Mostar', 'Bijeljina',
    'Brčko', 'Brcko', 'Prijedor', 'Doboj', 'Cazin', 'Bihać', 'Bihac',
    'Srebrenica', 'Zvornik', 'Višegrad', 'Visegrad', 'Foča', 'Foca',
    'Goražde', 'Gorazde', 'Trebinje', 'Konjic', 'Jablanica', 'Prozor',
    'Livno', 'Glamoč', 'Glamoc', 'Drvar', 'Bosanski Petrovac',
    'Vareš', 'Vares', 'Kreševo', 'Kresevo', 'Kiseljak', 'Fojnica',
    'Visoko', 'Kakanj', 'Zavidovići', 'Zavidovici', 'Maglaj', 'Tešanj', 'Tesanj',
    'Busovača', 'Busovaca', 'Vitez', 'Travnik', 'Jajce', 'Bugojno',
    'Ilidža', 'Ilidza', 'Vogošća', 'Vogosca', 'Hadžići', 'Hadzici',
    'Bakovići', 'Bakovici', 'Dubrave', 'Tisovac', 'Scitovo',
    'Veovača', 'Veovaca', 'Kostajnica', 'Parsovići', 'Parsovici',
    'Čevljanović', 'Cevljanovic', 'Čumavić', 'Cumavic', 'Vitlovac',
    'Medjuvršje', 'Medjuvrsje', 'Zagradje', 'Zagrađe',
    'Hrge', 'Komari', 'Deževice', 'Dezevice', 'Repovci', 'Draževićo', 'Drazevico',
    'Tušanj', 'Tusanj',
]

# Slovenija places
SLOVENIAN_PLACES = [
    'Ljubljana', 'Maribor', 'Celje', 'Kranj', 'Koper', 'Velenje',
    'Novo mesto', 'Ptuj', 'Trbovlje', 'Kamnik', 'Jesenice', 'Domžale',
    'Nova Gorica', 'Murska Sobota', 'Slovenj Gradec', 'Izola',
    'Idrija', 'Mežice', 'Mezice', 'Oplatnica', 'Pohorje', 'Bohnija', 'Blejsko',
]

# Crna Gora places
MONTENEGRO_PLACES = [
    'Podgorica', 'Nikšić', 'Niksic', 'Pljevlja', 'Bijelo Polje', 'Herceg Novi',
    'Berane', 'Budva', 'Cetinje', 'Bar', 'Ulcinj', 'Kotor', 'Tivat',
    'Rožaje', 'Rozaje', 'Plav', 'Andrijevica', 'Kolašin', 'Kolasin',
    'Mojkovac', 'Žabljak', 'Zabljak', 'Šavnik', 'Savnik', 'Danilovgrad',
    'Lučino vrelo', 'Lucino vrelo',
]

# Italija places
ITALIAN_PLACES = [
    'Roma', 'Milano', 'Napoli', 'Torino', 'Palermo', 'Genova', 'Bologna',
    'Firenze', 'Venezia', 'Verona', 'Trieste', 'Padova', 'Brescia',
    'Sicilija', 'Sardegna', 'Sardinija', 'Sardinia', 'Elba', 'Toscana', 'Toskana',
    'Piemonte', 'Piemont', 'Pijemont', 'Lombardia', 'Veneto', 'Liguria',
    'Emilia', 'Lazio', 'Campania', 'Puglia', 'Calabria', 'Abruzzo',
    'Val di Fassa', 'Val d\'Aosta', 'Valle D\'aosta', 'Aosta',
    'Baveno', 'Traversella', 'Gambatesa', 'Gavorrano', 'Campiglia',
    'Monteponi', 'Montevecchio', 'Rio Marina', 'Livorno', 'Lucca',
    'Grosseto', 'Iglesias', 'Antrona', 'Domodossola', 'Novara',
    'Bergamo', 'Brescia', 'Como', 'Sondrio', 'Bolzano', 'Trento',
    'Vicenza', 'Parma', 'Modena', 'Reggio', 'Ravenna', 'Rimini',
    'Faiallo', 'Ramazzo', 'Piona', 'Roccamarfina', 'Cerezzola',
    'Calafuria', 'Cava Menegolli', 'Bedulita', 'Braono',
    'Monti Monzoni', 'M.Monzoni', 'Monzoni', 'Monconi', 'Adamello',
    'Đerđenti', 'Đirđenti', 'Djurdjenti', 'Djerdjenti', 'Agrigento',
    'Etna', 'Vezuv', 'Vesuvio',
]

# Austrija places
AUSTRIAN_PLACES = [
    'Wien', 'Beč', 'Graz', 'Linz', 'Salzburg', 'Salcburg', 'Innsbruck',
    'Klagenfurt', 'Villach', 'Wels', 'St. Pölten', 'Dornbirn', 'Steyr',
    'Tirol', 'Štajerska', 'Stajerska', 'Steiermark', 'Koruška', 'Kärnten',
    'Oberösterreich', 'Niederösterreich', 'Vorarlberg', 'Burgenland',
    'Bleiberg', 'Blajberg', 'Bleiburg', 'Raibl', 'Verfen', 'Werfen',
    'Habahtal', 'Habahštal', 'Zell am See', 'Dienten', 'Golnig',
    'Rannariss', 'Ranriss', 'Rauriss', 'Alm b/Saalfelden', 'Saalfelden',
    'Osttirol', 'Pregraten', 'Vargen', 'Fisac', 'Fišac', 'Malajten',
    'Hitenberg', 'Sil', 'Gross Glochener', 'Grossglockner',
]

# Nemačka places
GERMAN_PLACES = [
    'Berlin', 'München', 'Hamburg', 'Frankfurt', 'Köln', 'Stuttgart',
    'Düsseldorf', 'Dortmund', 'Essen', 'Leipzig', 'Bremen', 'Dresden',
    'Hannover', 'Nürnberg', 'Duisburg', 'Bochum', 'Wuppertal', 'Bielefeld',
    'Bajern', 'Bayern', 'Bavarska', 'Saksonija', 'Sachsen', 'Hessen',
    'Švarcvald', 'Schwarzwald', 'Erzgebirge', 'Harz', 'Fichtelgebirge',
    'Siegerland', 'Rheinland', 'Reinland', 'Pfalz', 'Baden', 'Württemberg',
    'Frajberg', 'Freiberg', 'Wolsendorf', 'Wölsendorf', 'Ramelsberg', 'Goslar',
    'Essen Borbeck', 'Christian Levih', 'Elbogen', 'Limburg', 'Limberg',
    'Schnekenstein', 'St.Egidien', 'Brembach', 'Braubah', 'Fernsbah',
    'Bingen', 'Braumbah', 'Waldalgesheim', 'Zeilberg', 'Wiesloch',
    'Sasbach', 'Kaiserstuhl', 'Schauinsland', 'Schelingen',
    'Pohla', 'Steinheim', 'Štajnhajm', 'Friedland', 'Oberpfalz',
    'Wolf herdorf', 'Wolf Herdorf', 'Herdorf', 'Eupel', 'Enpel',
    'Fusseberg', 'Füsseberg', 'Daaden', 'Doaden',
    'Kirn', 'Nahe', 'Išl', 'Isl',
]

# Švajcarska places
SWISS_PLACES = [
    'Zürich', 'Genf', 'Basel', 'Bern', 'Lausanne', 'Winterthur',
    'St. Gallen', 'Lugano', 'Biel', 'Thun', 'Köniz', 'La Chaux-de-Fonds',
    'Binental', 'Binnertall', 'Binnertal', 'St. Gotthard', 'St Gothard', 'Gottardo',
    'Zermatt', 'Gorner Grat', 'Val Nalps', 'Val Canarien', 'Grison',
    'Chamonix', 'Jermalt', 'Ticino', 'Luccomagno',
]

# Čehoslovačka/Češka places
CZECH_PLACES = [
    'Praha', 'Brno', 'Ostrava', 'Plzeň', 'Liberec', 'Olomouc',
    'České Budějovice', 'Hradec Králové', 'Ústí nad Labem', 'Pardubice',
    'Psibram', 'Příbram', 'Jahimov', 'Jáchymov', 'Joachimsthal',
    'Karlsbad', 'Karlovy Vary', 'Cinovec', 'Krupka', 'Horni Slavkov',
    'Chvaletice', 'Dolni Bory', 'Rozna', 'Rožná', 'Stribro',
    'Kozakov', 'Kozako', 'Nucice', 'Trenice', 'Hazlov', 'Cechy', 'Čechy',
    'Morava', 'Moravská', 'Bohemia', 'Bohutin', 'Bukov', 'Maglovec',
    'Eva-Jahimov', 'Klement-Jahimov', 'Svornost-Jahimov',
    'Repcice', 'Rona-Kladno', 'Stere Ransko', 'Straznik-Perimov',
    'Namdraz', 'Zelechov', 'Zlate Hory', 'Voltac', 'Vrancice',
    'Vysocani', 'Zbraslav', 'Teplice', 'Lubietova', 'Vapena',
    'Podsedice', 'Ruskov', 'Marsikov', 'Markovice', 'Krasna Iforka',
    'Cinvald',
]

# Rusija/SSSR places
RUSSIAN_PLACES = [
    'Moskva', 'Sankt-Peterburg', 'Novosibirsk', 'Jekaterinburg', 'Kazan',
    'Ural', 'Sibir', 'Kavkaz', 'Kola', 'Kamčatka',
    'Baženovskoe', 'Bazenovskoe', 'Seljankino', 'Blajva', 'Bljava',
    'Karabas', 'Karabaš', 'Borisovske sopki', 'Borisovekie sopki',
    'Pusma', 'Pišma', 'Nahicesvarn', 'Nahičevari', 'Kedabek',
    'Nižni Toginsk', 'Nizni Toginsk', 'Chibinska', 'Gruzija',
]

# Other countries mapping
COUNTRY_PATTERNS = {
    # USA
    'Arizona': 'USA', 'Colorado': 'USA', 'California': 'USA', 'Kalifornija': 'USA',
    'Utah': 'USA', 'Nevada': 'USA', 'New Mexico': 'USA', 'New Jersey': 'USA',
    'Wyoming': 'USA', 'Montana': 'USA', 'Idaho': 'USA', 'Oregon': 'USA',
    'Washington': 'USA', 'Oklahoma': 'USA', 'Arkansas': 'USA', 'Arkanzas': 'USA',
    'Texas': 'USA', 'Nebraska': 'USA', 'South Dakota': 'USA', 'Illinois': 'USA',
    'Vermont': 'USA', 'Massachusetts': 'USA', 'Massacusets': 'USA',
    'Teller County': 'USA', 'Douglas County': 'USA', 'Boulder county': 'USA',
    'Clear creek county': 'USA', 'Eagle County': 'USA', 'Grand county': 'USA',
    'Gunnison county': 'USA', 'Jackson county': 'USA', 'Lake county': 'USA',
    'Larimer County': 'USA', 'Montrose county': 'USA', 'Park county': 'USA',
    'San Miguel county': 'USA', 'Valencia County': 'USA', 'Weld County': 'USA',
    'Dawes County': 'USA', 'Pinal County': 'USA',
    'Crystal Peak': 'USA', 'Devils Head': 'USA', 'Mt Spokane': 'USA',
    'Apache Mine': 'USA', 'Biedell Mine': 'USA', 'van Pool Mine': 'USA',
    'Tintic': 'USA', 'Tintik': 'USA', 'Pitcher': 'USA', 'Black Hills': 'USA',
    
    # Meksiko
    'Durango': 'Meksiko', 'Sonora': 'Meksiko', 'Zacatecas': 'Meksiko',
    'Guerrero': 'Meksiko', 'Chihuahua': 'Meksiko', 'Mapimi': 'Meksiko',
    'Ojuela': 'Meksiko', 'Mexquitic': 'Meksiko', 'Imuris': 'Meksiko',
    
    # Brazil
    'Minas Gerais': 'Brazil', 'Rio Grande': 'Brazil', 'Goyaz': 'Brazil',
    'Ceare': 'Brazil', 'Oro Puerto': 'Brazil', 'Pirauikabo': 'Brazil',
    
    # Afrika
    'Madagaskar': 'Madagaskar', 'Tsumeb': 'Namibija', 'Tzumeb': 'Namibija',
    'Cumeb': 'Namibija', 'Džumeb': 'Namibija', 'Okoruso': 'Namibija',
    'Katanga': 'Kongo', 'Kinshasa': 'Kongo', 'Zair': 'Kongo',
    'Angola': 'Angola', 'Zambija': 'Zambija', 'Malawi': 'Malavi',
    'Kenya': 'Kenija', 'Tanzanija': 'Tanzanija', 'Bocvana': 'Bocvana',
    
    # Azija
    'Indija': 'Indija', 'Poona': 'Indija', 'Pakistan': 'Pakistan',
    'Kina': 'Kina', 'Mongolija': 'Mongolija', 'Kambodza': 'Kambodža',
    'Cejlon': 'Šri Lanka', 'Iran': 'Iran', 'Persija': 'Iran',
    'Izrael': 'Izrael',
    
    # Ostalo
    'Australija': 'Australija', 'Queensland': 'Australija',
    'Novi Zeland': 'Novi Zeland', 'Gvatemala': 'Gvatemala',
    'Argentina': 'Argentina', 'Bolivija': 'Bolivija', 'Čile': 'Čile',
    'Cile': 'Čile', 'Atakama': 'Čile', 'Urugvaj': 'Urugvaj',
    'Kanada': 'Kanada', 'Blind River': 'Kanada',
    'Island': 'Island', 'Norveška': 'Norveška', 'Hittero': 'Norveška',
    'Langozunafjord': 'Norveška', 'Arendal': 'Norveška',
    'Turska': 'Turska', 'Bigadi': 'Turska', 'Espery': 'Turska', 'Murgul': 'Turska',
    'Alžir': 'Alžir', 'Alzir': 'Alžir', 'Maroko': 'Maroko', 'Mibladen': 'Maroko',
    'Tunis': 'Tunis', 'Libija': 'Libija', 'Tripoli': 'Libija',
    'Rumunija': 'Rumunija', 'Felsobanya': 'Rumunija', 'Felsebana': 'Rumunija',
    'Mađarska': 'Mađarska', 'Madjarska': 'Mađarska',
    'Poljska': 'Poljska', 'Olkasz': 'Poljska', 'Wieliczska': 'Poljska',
    'Tarnobrzeg': 'Poljska', 'Stolpo': 'Poljska',
    'Grčka': 'Grčka', 'Laurion': 'Grčka', 'Lavron': 'Grčka', 'Atika': 'Grčka',
    'Ukrajina': 'Ukrajina', 'Ukraina': 'Ukrajina',
    'Belgija': 'Belgija', 'Holandija': 'Holandija',
    'Francuska': 'Francuska', 'Bretagne': 'Francuska', 'Limoges': 'Francuska',
    'Haute Vienne': 'Francuska', 'Chamonix': 'Francuska',
    'Španija': 'Španija', 'Mingllanila': 'Španija', 'Tenereife': 'Španija',
    'Engleska': 'Engleska', 'Kornvol': 'Engleska', 'Cornwall': 'Engleska',
    'Peak District': 'Engleska',
}

def get_country_for_locality(locality):
    """Determine country for a locality."""
    if not locality:
        return None
    
    loc_lower = locality.lower()
    
    # Check if already has country suffix
    country_suffixes = [
        'Srbija', 'Makedonija', 'Italija', 'Nemačka', 'Austrija', 'Švajcarska',
        'Francuska', 'Španija', 'Rusija', 'USA', 'Meksiko', 'Čehoslovačka',
        'BiH', 'Bosna', 'Slovenija', 'Hrvatska', 'Grčka', 'Turska', 'Rumunija',
        'Mađarska', 'Poljska', 'Norveška', 'SSSR', 'Maroko', 'Tunis', 'Afrika',
        'Brazil', 'Madagaskar', 'Engleska', 'Kanada', 'Alžir', 'Libija',
        'Kongo', 'Namibija', 'Indija', 'Kina', 'Japan', 'Australija',
        'Argentina', 'Bolivija', 'Čile', 'Crna Gora', 'Kosovo',
    ]
    
    for suffix in country_suffixes:
        if locality.endswith(', ' + suffix) or locality.endswith(',' + suffix):
            return None  # Already has country
        if locality == suffix:
            return None  # Is just the country name
    
    # Check Serbian places
    for place in SERBIAN_PLACES:
        if place.lower() in loc_lower or loc_lower.startswith(place.lower()):
            return 'Srbija'
    
    # Check Macedonian places
    for place in MACEDONIAN_PLACES:
        if place.lower() in loc_lower:
            return 'Makedonija'
    
    # Check BiH places
    for place in BIH_PLACES:
        if place.lower() in loc_lower:
            return 'BiH'
    
    # Check Slovenian places
    for place in SLOVENIAN_PLACES:
        if place.lower() in loc_lower:
            return 'Slovenija'
    
    # Check Montenegro places
    for place in MONTENEGRO_PLACES:
        if place.lower() in loc_lower:
            return 'Crna Gora'
    
    # Check Italian places
    for place in ITALIAN_PLACES:
        if place.lower() in loc_lower:
            return 'Italija'
    
    # Check Austrian places
    for place in AUSTRIAN_PLACES:
        if place.lower() in loc_lower:
            return 'Austrija'
    
    # Check German places
    for place in GERMAN_PLACES:
        if place.lower() in loc_lower:
            return 'Nemačka'
    
    # Check Swiss places
    for place in SWISS_PLACES:
        if place.lower() in loc_lower:
            return 'Švajcarska'
    
    # Check Czech places
    for place in CZECH_PLACES:
        if place.lower() in loc_lower:
            return 'Čehoslovačka'
    
    # Check Russian places
    for place in RUSSIAN_PLACES:
        if place.lower() in loc_lower:
            return 'Rusija'
    
    # Check other country patterns
    for pattern, country in COUNTRY_PATTERNS.items():
        if pattern.lower() in loc_lower:
            return country
    
    return None

def add_countries_to_localities():
    """Add missing country names to localities."""
    updates = []
    
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT card_locality 
                FROM minerals 
                WHERE card_locality IS NOT NULL AND card_locality != ''
            """)
            localities = [row[0] for row in cur.fetchall()]
            
            for locality in localities:
                country = get_country_for_locality(locality)
                if country:
                    new_locality = locality.rstrip(',. ') + ', ' + country
                    updates.append((locality, new_locality, country))
                    cur.execute("""
                        UPDATE minerals 
                        SET card_locality = %s 
                        WHERE card_locality = %s
                    """, (new_locality, locality))
            
            conn.commit()
    
    return updates

if __name__ == '__main__':
    print("Adding country names to localities...")
    updates = add_countries_to_localities()
    
    # Group by country
    by_country = {}
    for old, new, country in updates:
        if country not in by_country:
            by_country[country] = []
        by_country[country].append((old, new))
    
    print(f"\nAdded country to {len(updates)} localities:\n")
    for country in sorted(by_country.keys()):
        print(f"\n=== {country} ({len(by_country[country])}) ===")
        for old, new in sorted(by_country[country])[:10]:
            print(f"  '{old}' -> '{new}'")
        if len(by_country[country]) > 10:
            print(f"  ... and {len(by_country[country]) - 10} more")
    
    print("\nDone!")
