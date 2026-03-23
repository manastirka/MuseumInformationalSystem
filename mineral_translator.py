"""
Mineral Name Translation System
Translates Serbian mineral names to English and parses combined mineral names.
"""

import re
from typing import List, Dict, Optional, Tuple

# Comprehensive Serbian to English mineral translation dictionary
MINERAL_TRANSLATIONS = {
    # A
    'adamin': 'Adamite',
    'adular': 'Adularia',
    'ahat': 'Agate',
    'aksinit': 'Axinite',
    'aktinolit': 'Actinolite',
    'akvamarin': 'Aquamarine',
    'alabaster': 'Alabaster',
    'alanit': 'Allanite',
    'albit': 'Albite',
    'almandin': 'Almandine',
    'aluminijum': 'Aluminum',
    'aluminit': 'Aluminite',
    'alunit': 'Alunite',
    'amazonit': 'Amazonite',
    'ametist': 'Amethyst',
    'amfibol': 'Amphibole',
    'analcim': 'Analcime',
    'anatas': 'Anatase',
    'andaluzit': 'Andalusite',
    'andradit': 'Andradite',
    'anglezit': 'Anglesite',
    'anhidrit': 'Anhydrite',
    'ankerit': 'Ankerite',
    'antigorit': 'Antigorite',
    'antimon': 'Antimony',
    'antimonit': 'Stibnite',  # Antimonite = Stibnite
    'antofilit': 'Anthophyllite',
    'antracit': 'Anthracite',
    'apatit': 'Apatite',
    'apofilit': 'Apophyllite',
    'aragonit': 'Aragonite',
    'aragostroncijanit': 'Aragonite-Strontianite',
    'arduinit': 'Arduinite',
    'arfedsonit': 'Arfvedsonite',
    'argentit': 'Argentite',
    'arsen': 'Arsenic',
    'arsenopirit': 'Arsenopyrite',
    'atakamit': 'Atacamite',
    'augit': 'Augite',
    'aurihalcit': 'Aurichalcite',
    'aurikalcit': 'Aurichalcite',
    'auripigment': 'Orpiment',
    'autunit': 'Autunite',
    'avalit': 'Avalite',
    'avanturin': 'Aventurine',
    'azbest': 'Asite',
    'azurit': 'Azurite',

    # B
    'bakar': 'Copper',
    'barit': 'Barite',
    'baritokalcit': 'Barytocalcite',
    'bastnezit': 'Bastnäsite',
    'bavenit': 'Bavenite',
    'beril': 'Beryl',
    'bertijerit': 'Berthierite',
    'berzelianit': 'Berzelianite',
    'bigar': 'Travertine',
    'biotit': 'Biotite',
    'bizmut': 'Bismuth',
    'bizmutinit': 'Bismuthinite',
    'boracit': 'Boracite',
    'bornit': 'Bornite',
    'braunit': 'Braunite',
    'brucit': 'Brucite',
    'brukit': 'Brookite',

    # C/Č
    'celestin': 'Celestine',
    'cerusit': 'Cerussite',
    'ceruzit': 'Cerussite',
    'cirkon': 'Zircon',
    'citrin': 'Citrine',
    'cinkenit': 'Zinckenite',
    'cinkit': 'Zincite',
    'coisit': 'Zoisite',
    'kolemanit': 'Colemanite',

    # D
    'dijaspor': 'Diaspore',
    'diopsid': 'Diopside',
    'disten': 'Kyanite',  # Disthene = Kyanite (Al2SiO5)
    'disthen': 'Kyanite',
    'dolomit': 'Dolomite',
    'draguljasti kamen': 'Gemstone',

    # E
    'enargit': 'Enargite',
    'enstatit': 'Enstatite',
    'epidot': 'Epidote',
    'eritrin': 'Erythrite',

    # F
    'feldspat': 'Feldspar',
    'filipsit': 'Phillipsite',
    'fluorit': 'Fluorite',
    'forsterit': 'Forsterite',
    'fosfat': 'Phosphate',
    'franklinit': 'Franklinite',

    # G
    'galenit': 'Galena',
    'ganet': 'Garnet',
    'ganit': 'Gahnite',
    'garnet': 'Garnet',  # English name (group)
    'geoda': 'Geode',
    'getit': 'Goethite',
    'gips': 'Gypsum',
    'glaukonit': 'Glauconite',
    'gnajst': 'Gneiss',
    'grafit': 'Graphite',
    'granat': 'Garnet',
    'grosular': 'Grossular',

    # H
    'halit': 'Halite',
    'halkantit': 'Chalcanthite',
    'halkopirit': 'Chalcopyrite',
    'halkozin': 'Chalcocite',
    'heliodor': 'Heliodor',
    'heliotropi': 'Heliotrope',
    'hematit': 'Hematite',
    'hemimorf': 'Hemimorphite',
    'hemimorfin': 'Hemimorphite',
    'hidromagnezit': 'Hydromagnesite',
    'hidrocirkon': 'Hydrozircon',
    'hipersten': 'Hypersthene',
    'hlorit': 'Chlorite',
    'hornblenda': 'Hornblende',
    'hubnerit': 'Hübnerite',

    # I
    'ilmenit': 'Ilmenite',
    'ilvarit': 'Ilvaite',

    # J
    'jaspis': 'Jasper',
    'jarosit': 'Jarosite',
    'jadarit': 'Jadarite',

    # K
    'kalcedon': 'Chalcedony',
    'kalcit': 'Calcite',
    'kalij': 'Potassium',
    'kalijev feldspat': 'K-feldspar',
    'kaolinit': 'Kaolinite',
    'karbonat': 'Carbite',
    'karneol': 'Carnelian',
    'kasiterit': 'Cassiterite',
    'kianit': 'Kyanite',
    'klorit': 'Chlorite',
    'kobaltit': 'Cobaltite',
    'korund': 'Corundum',
    'kriolit': 'Cryolite',
    'kristobalit': 'Cristobalite',
    'krokoit': 'Crocoite',
    'kunzit': 'Kunzite',
    'kuprit': 'Cuprite',
    'kvarc': 'Quartz',
    'kvarcit': 'Quartzite',

    # L
    'labrador': 'Labradorite',
    'labradorit': 'Labradorite',
    'lapislazuli': 'Lapis Lazuli',
    'lapis lazuli': 'Lapis Lazuli',
    'lazulit': 'Lazulite',
    'lazurit': 'Lazurite',
    'lepidokrokit': 'Lepidocrocite',
    'lepidolit': 'Lepidolite',
    'leucit': 'Leucite',
    'limonit': 'Limonite',
    'linarit': 'Linarite',
    'liskun': 'Mica',

    # M
    'magnetit': 'Magnetite',
    'magnezit': 'Magnesite',
    'malahit': 'Malachite',
    'mangan': 'Manganese',
    'manganokalcit': 'Manganocalcite',
    'markazit': 'Marcasite',
    'melanit': 'Melanite',
    'mermer': 'Marble',
    'mikroklin': 'Microcline',
    'milonit': 'Mylonite',
    'mimetezit': 'Mimetite',
    'molibdenit': 'Molybdenite',
    'monacit': 'Monazite',
    'morganit': 'Morganite',
    'muskovit': 'Muscovite',

    # N
    'natrolit': 'Natrolite',
    'nefelin': 'Nepheline',
    'nefrit': 'Nephrite',
    'neotocit': 'Neotocite',
    'nikal': 'Nickel',
    'nikolit': 'Nickeline',

    # O
    'obsidijan': 'Obsidian',
    'oksid': 'Oxide',
    'oligoklas': 'Oligoclase',
    'olivin': 'Olivine',
    'oniks': 'Onyx',
    'opal': 'Opal',
    'ortoklas': 'Orthoclase',

    # P
    'pargasit': 'Pargasite',
    'pegmatit': 'Pegmatite',
    'pentlandit': 'Pentlandite',
    'periklin': 'Pericline',
    'periklas': 'Periclase',
    'peridot': 'Peridot',
    'peristeri': 'Peristerite',
    'perlit': 'Perlite',
    'piemontit': 'Piemontite',
    'pirit': 'Pyrite',
    'pirofan': 'Pyromorphite',
    'pirofilit': 'Pyrophyllite',
    'piroksenit': 'Pyroxenite',
    'piroluzit': 'Pyrolusite',
    'piromorfin': 'Pyromorphite',
    'piromorfita': 'Pyromorphite',
    'pirop': 'Pyrope',
    'pirotin': 'Pyrrhotite',
    'pirotit': 'Pyrrhotite',
    'plaginoklas': 'Plagioclase',
    'plagiokalze': 'Plagioclase',
    'plumozit': 'Plumosite',
    'prehnit': 'Prehnite',
    'psilomelan': 'Psilomelane',
    'pumpa': 'Pumice',

    # R
    'realgar': 'Realgar',
    'riolit': 'Rhyolite',
    'rodohrozit': 'Rhodochrosite',
    'rodonit': 'Rhodonite',
    'rogorit': 'Hornfels',
    'rozenkvarc': 'Rose Quartz',
    'rozenkvarc': 'Rose Quartz',
    'rubin': 'Ruby',
    'rutil': 'Rutile',

    # S
    'safir': 'Sapphire',
    'sanidind': 'Sanidine',
    'sanidin': 'Sanidine',
    'sardoniks': 'Sardonyx',
    'selenid': 'Selenide',
    'selenite': 'Selenite',
    'senarmonit': 'Senarmontite',
    'senarmontit': 'Senarmontite',
    'serpentin': 'Serpentine',
    'serpentinit': 'Serpentinite',
    'siderit': 'Siderite',
    'sijena': 'Sienna',
    'sijenit': 'Syenite',
    'sileks': 'Chert',
    'silikat': 'Silicate',
    'silimanit': 'Sillimanite',
    'silvanit': 'Sylvanite',
    'silvit': 'Sylvite',
    'skoril': 'Schorl',
    'skorodit': 'Scorodite',
    'skuterudit': 'Skutterudite',
    'smaragd': 'Emerald',
    'smithsonit': 'Smithsonite',
    'smitsonit': 'Smithsonite',
    'sodalit': 'Sodalite',
    'spekularit': 'Specularite',
    'spesartin': 'Spessartine',
    'sfalerit': 'Sphalerite',
    'sfen': 'Titanite',  # Sphene = Titanite
    'sfenosiderit': 'Sphenosiderite',
    'spinel': 'Spinel',
    'starolit': 'Staurolite',
    'steatiit': 'Steatite',
    'stilbit': 'Stilbite',
    'stroncijanit': 'Strontianite',
    'sulfat': 'Sulfate',
    'sulfid': 'Sulfide',
    'sumpor': 'Sulphur',
    'supmor': 'Sulphur',  # Common typo

    # Š
    'šelit': 'Scheelite',
    'škriljevac': 'Slate',

    # T
    'talk': 'Talc',
    'tantalit': 'Tantalite',
    'telurid': 'Telluride',
    'tenantit': 'Tennantite',
    'tenorit': 'Tenorite',
    'tetraedrit': 'Tetrahedrite',
    'titanit': 'Titanite',
    'topaz': 'Topaz',
    'torij': 'Thorium',
    'torit': 'Thorite',
    'tremolit': 'Tremolite',
    'tridimit': 'Tridymite',
    'turgit': 'Turgite',
    'turmalin': 'Tourmaline',
    'turkuiz': 'Turquoise',

    # U
    'unakit': 'Unakite',
    'uraniit': 'Uraninite',
    'uranit': 'Uraninite',
    'uvarovit': 'Uvarovite',

    # V
    'valentinit': 'Valentinite',
    'vanadinit': 'Vanadinite',
    'variscit': 'Variscite',
    'vermiculit': 'Vermiculite',
    'vernerit': 'Wernerite',
    'vesuvijan': 'Vesuvianite',
    'vesuvianit': 'Vesuvianite',
    'vivianit': 'Vivianite',
    'volastonit': 'Wollastonite',
    'volframit': 'Wolframite',
    'vulkanit': 'Volcanic rock',

    # W
    'wad': 'Wad',
    'wilemit': 'Willemite',
    'wulfenit': 'Wulfenite',

    # Z
    'zeolite': 'Zeolite',
    'zeolit': 'Zeolite',
    'cinkit': 'Zincite',
    'cink': 'Zinc',
    'cirkonij': 'Zirconium',
    'coisit': 'Zoisite',
    'zoisit': 'Zoisite',

    # Ž
    'živin sulfid': 'Cinnabar',

    # Common rock types (for filtering)
    'granit': 'Granite',
    'bazalt': 'Basalt',
    'gabro': 'Gabbro',
    'dijabaz': 'Diabase',
    'andezit': 'Andesite',
    'dacit': 'Dacite',
    'peščar': 'Sandstone',
    'krečnjak': 'Limestone',
    'škriljac': 'Schist',
    'mramor': 'Marble',
    'konglomerat': 'Conglomerate',
    'breca': 'Breccia',
    'breča': 'Breccia',
    'tuf': 'Tuff',
    'lapora': 'Marl',
    'lapor': 'Marl',
}

# Words to ignore (not minerals, just descriptors)
IGNORE_WORDS = {
    'sa', 'i', 'na', 'u', 'iz', 'od', 'do', 'za', 'po', 'pri', 'kroz',
    'mali', 'mala', 'malo', 'veliki', 'velika', 'veliko',
    'beli', 'bela', 'belo', 'crni', 'crna', 'crno', 'crveni', 'crvena', 'crveno',
    'zeleni', 'zelena', 'zeleno', 'plavi', 'plava', 'plavo',
    'žuti', 'žuta', 'žuto', 'sivi', 'siva', 'sivo',
    'ružičasti', 'ružičasta', 'ružičasto', 'ljubičasti', 'ljubičasta',
    'tamni', 'tamna', 'tamno', 'svetli', 'svetla', 'svetlo',
    'prizmatični', 'prizmatična', 'prizmatično',
    'okrugli', 'okrugla', 'okruglo',
    'duguljasti', 'duguljasta', 'duguljasto',
    'manji', 'manja', 'manje', 'veći', 'veća', 'veće',
    'primerak', 'kristal', 'kristali', 'druza', 'druze', 'druzom',
    'geoda', 'kora', 'biseri', 'nakit', 'pećinski',
    'ruža', 'ruže', 'ruda', 'rudna', 'rudama',
    'povijeni', 'povijena', 'povijeno',
    'oksidi', 'oksida', 'oksidom',
    'h2o', 'al2', 'oh', 'so4', 'sio2',
    # Rock types (not minerals)
    'skarn', 'pegmatit', 'granit', 'bazalt', 'gnajst', 'mramor',
    'škriljac', 'škriljevac', 'vulkanit', 'milonit',
    # Elements (not minerals)
    'mangan', 'manganov', 'manganovim', 'gvožđe', 'gvožđem', 'bakar', 'bakrom',
}

# Patterns for splitting mineral names
SPLIT_PATTERNS = [
    r'\s*,\s*',           # comma
    r'\s+i\s+',           # " i " (and)
    r'\s*-\s*',           # dash
    r'\s*/\s*',           # slash
    r'\s+sa\s+',          # " sa " (with) - sometimes indicates association
    r'\s+na\s+',          # " na " (on)
    r'\s+u\s+',           # " u " (in)
]


def normalize_name(name: str) -> str:
    """Normalize mineral name for lookup."""
    if not name:
        return ''
    # Convert to lowercase and strip
    normalized = name.lower().strip()
    # Remove special characters but keep letters
    normalized = re.sub(r'[*?!]', '', normalized)
    # Remove parenthetical content for initial lookup
    normalized = re.sub(r'\([^)]*\)', '', normalized).strip()
    return normalized


def extract_minerals_from_name(full_name: str) -> List[str]:
    """
    Extract individual mineral names from a combined name.
    Returns list of individual mineral names.
    """
    if not full_name:
        return []

    minerals = []

    # First, try to split by common separators
    # Start with the most specific patterns
    parts = [full_name]

    for pattern in SPLIT_PATTERNS:
        new_parts = []
        for part in parts:
            split_parts = re.split(pattern, part, flags=re.IGNORECASE)
            new_parts.extend(split_parts)
        parts = new_parts

    # Process each part
    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Check for parenthetical content (e.g., "Almandin (granat)")
        paren_match = re.search(r'\(([^)]+)\)', part)
        if paren_match:
            paren_content = paren_match.group(1).strip()
            # Add parenthetical content if it's a mineral
            if paren_content.lower() not in IGNORE_WORDS:
                minerals.append(paren_content)
            # Also add the main part without parentheses
            main_part = re.sub(r'\([^)]*\)', '', part).strip()
            if main_part and main_part.lower() not in IGNORE_WORDS:
                minerals.append(main_part)
        else:
            # Check if this is a mineral or just a descriptor
            normalized = normalize_name(part)
            words = normalized.split()

            for word in words:
                word = word.strip()
                if word and word not in IGNORE_WORDS and len(word) > 2:
                    # Check if it looks like a mineral name
                    if word in MINERAL_TRANSLATIONS or word[0].isupper() or len(word) > 4:
                        minerals.append(word)

    # Remove duplicates while preserving order
    seen = set()
    unique_minerals = []
    for m in minerals:
        normalized = normalize_name(m)
        if normalized not in seen and normalized not in IGNORE_WORDS:
            seen.add(normalized)
            unique_minerals.append(m)

    return unique_minerals if unique_minerals else [full_name]


def remove_serbian_case_suffix(word: str) -> str:
    """
    Remove Serbian grammatical case suffixes to get the base form (nominative).
    Serbian has 7 cases with different endings.
    """
    # Common case endings to try removing (longest first)
    case_suffixes = [
        'om', 'em', 'im',  # Instrumental (-om, -em, -im)
        'a', 'e', 'i', 'u',  # Genitive/Dative/Locative
        'ом', 'ем', 'им',  # Cyrillic instrumental
        'а', 'е', 'и', 'у',  # Cyrillic other cases
    ]

    for suffix in case_suffixes:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            base = word[:-len(suffix)]
            # Check if removing suffix gives us a known mineral
            if base in MINERAL_TRANSLATIONS:
                return base
            # Try adding common mineral endings
            for ending in ['it', 'in', 'at', 'c', 't']:
                test = base + ending
                if test in MINERAL_TRANSLATIONS:
                    return test

    return word


def translate_mineral_name(serbian_name: str) -> Tuple[str, bool]:
    """
    Translate a Serbian mineral name to English.
    Returns (english_name, was_translated).
    """
    if not serbian_name:
        return '', False

    normalized = normalize_name(serbian_name)

    # Try exact match first
    if normalized in MINERAL_TRANSLATIONS:
        return MINERAL_TRANSLATIONS[normalized], True

    # Try removing Serbian case suffixes
    base_form = remove_serbian_case_suffix(normalized)
    if base_form != normalized and base_form in MINERAL_TRANSLATIONS:
        return MINERAL_TRANSLATIONS[base_form], True

    # Try common variations
    variations = [
        normalized,
        normalized.replace('č', 'c').replace('ć', 'c').replace('š', 's').replace('ž', 'z').replace('đ', 'dj'),
    ]

    for var in variations:
        if var in MINERAL_TRANSLATIONS:
            return MINERAL_TRANSLATIONS[var], True

    # Try fuzzy matching - find minerals that start with same prefix
    if len(normalized) >= 4:
        prefix = normalized[:4]
        for key, value in MINERAL_TRANSLATIONS.items():
            if key.startswith(prefix):
                return value, True

    # Try without common suffixes/prefixes
    for suffix in ['it', 'ит', 'in', 'ин', 'at', 'ат', 'om', 'em', 'a', 'e', 'i', 'u']:
        if normalized.endswith(suffix) and len(normalized) > len(suffix) + 3:
            base = normalized[:-len(suffix)]
            for key in MINERAL_TRANSLATIONS:
                if key.startswith(base) and len(key) - len(base) <= 3:
                    return MINERAL_TRANSLATIONS[key], True

    # If name is already in Latin characters and looks English, return as-is
    if serbian_name and serbian_name[0].isupper() and all(c.isascii() or c.isspace() for c in serbian_name):
        # Capitalize properly
        return serbian_name.title(), False

    # Return original capitalized if no translation found
    return serbian_name.title(), False


def get_all_translations(full_mineral_name: str) -> List[Dict]:
    """
    Parse a combined mineral name, extract individual minerals,
    and translate each one.
    Returns list of dicts with original, translated, and was_translated.
    """
    minerals = extract_minerals_from_name(full_mineral_name)
    results = []

    seen_translations = set()
    for mineral in minerals:
        english, was_translated = translate_mineral_name(mineral)
        if english.lower() not in seen_translations:
            seen_translations.add(english.lower())
            results.append({
                'original': mineral,
                'english': english,
                'was_translated': was_translated
            })

    return results


# Test function
if __name__ == '__main__':
    test_names = [
        'Kalcit',
        'azurit i malahit',
        'Antimonit sa valentinitom',
        'Ahat, opal, kalcedon',
        'Arsenopirit, pirit, galenit, kvarc, rodohrozit',
        'Almandin (granat)',
        'Ahat sa druzom kvarca',
        'Auripigment -Realgar',
        'Adular, sfen, epidot',
    ]

    for name in test_names:
        print(f"\n'{name}':")
        translations = get_all_translations(name)
        for t in translations:
            status = '✓' if t['was_translated'] else '?'
            print(f"  {status} {t['original']} -> {t['english']}")
