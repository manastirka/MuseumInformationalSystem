"""
Online Mineral Data Fetcher
Fetches mineral information from online sources when local RRUFF database is missing data.
Sources: Wikipedia API, Mindat.org, webmineral.com
"""

import re
import json
import urllib.request
import urllib.parse
from typing import Dict, Optional
import ssl

# Create SSL context that doesn't verify certificates (for internal use)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Known mineral formulas (fallback when Wikipedia parsing fails)
KNOWN_FORMULAS = {
    'kyanite': 'Al2SiO5',
    'garnet': 'X3Y2(SiO4)3',  # General formula
    'almandine': 'Fe3Al2(SiO4)3',
    'pyrope': 'Mg3Al2(SiO4)3',
    'spessartine': 'Mn3Al2(SiO4)3',
    'grossular': 'Ca3Al2(SiO4)3',
    'andradite': 'Ca3Fe2(SiO4)3',
    'uvarovite': 'Ca3Cr2(SiO4)3',
    'disthene': 'Al2SiO5',  # Same as kyanite
    'quartz': 'SiO2',
    'calcite': 'CaCO3',
    'dolomite': 'CaMg(CO3)2',
    'feldspar': '(K,Na,Ca)(Al,Si)4O8',
    'mica': 'KAl2(AlSi3O10)(OH)2',
    'muscovite': 'KAl2(AlSi3O10)(OH)2',
    'biotite': 'K(Mg,Fe)3(AlSi3O10)(OH)2',
    'olivine': '(Mg,Fe)2SiO4',
    'pyroxene': '(Ca,Mg,Fe)2Si2O6',
    'amphibole': 'Ca2(Mg,Fe)5Si8O22(OH)2',
    'tourmaline': '(Na,Ca)(Mg,Fe,Li,Al)3Al6(BO3)3Si6O18(OH)4',
    'beryl': 'Be3Al2Si6O18',
    'topaz': 'Al2SiO4(F,OH)2',
    'zircon': 'ZrSiO4',
    'apatite': 'Ca5(PO4)3(F,Cl,OH)',
    'fluorite': 'CaF2',
    'barite': 'BaSO4',
    'gypsum': 'CaSO4·2H2O',
    'halite': 'NaCl',
    'pyrite': 'FeS2',
    'galena': 'PbS',
    'sphalerite': 'ZnS',
    'chalcopyrite': 'CuFeS2',
    'magnetite': 'Fe3O4',
    'hematite': 'Fe2O3',
    'corundum': 'Al2O3',
    'rutile': 'TiO2',
    'spinel': 'MgAl2O4',
}


def fetch_url(url: str, timeout: int = 10) -> Optional[str]:
    """Fetch URL content with error handling."""
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'MuseumInfoSystem/1.0 (Natural History Museum Belgrade)'}
        )
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def get_wikipedia_mineral_data(mineral_name: str) -> Optional[Dict]:
    """
    Fetch mineral data from Wikipedia API.
    Returns basic mineral information if available.
    """
    # Clean the mineral name
    clean_name = mineral_name.strip().title()

    # Try with "(mineral)" suffix first for disambiguation
    search_terms = [
        f"{clean_name} (mineral)",
        clean_name,
        f"{clean_name} mineral"
    ]

    for search_term in search_terms:
        # Wikipedia API - get page extract
        encoded_term = urllib.parse.quote(search_term)
        api_url = (
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_term}"
        )

        content = fetch_url(api_url)
        if not content:
            continue

        try:
            data = json.loads(content)

            # Check if this is about a mineral
            extract = data.get('extract', '').lower()
            if not any(word in extract for word in ['mineral', 'crystal', 'silicate', 'oxide', 'carbonate', 'sulfide', 'gemstone', 'ore']):
                continue

            title = data.get('title', clean_name)
            description = data.get('description', '')
            extract_text = data.get('extract', '')

            # Try to extract chemical formula from the text
            formula = extract_formula_from_text(extract_text)

            # Try to extract crystal system
            crystal_system = extract_crystal_system(extract_text)

            # Build result
            result = {
                'name': title,
                'source': 'Wikipedia',
                'description': extract_text[:500] if extract_text else '',
                'formula': formula,
                'crystal_system': crystal_system,
                'wikipedia_url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                'ima_status': 'See Wikipedia for details',
            }

            # Try to get more detailed info from the full page
            detailed = get_wikipedia_infobox(title)
            if detailed:
                result.update(detailed)

            return result

        except json.JSONDecodeError:
            continue

    return None


def get_wikipedia_infobox(title: str) -> Optional[Dict]:
    """
    Try to extract mineral infobox data from Wikipedia page.
    """
    encoded_title = urllib.parse.quote(title)
    api_url = (
        f"https://en.wikipedia.org/w/api.php?"
        f"action=query&titles={encoded_title}&prop=revisions&rvprop=content&format=json&rvslots=main"
    )

    content = fetch_url(api_url)
    if not content:
        return None

    try:
        data = json.loads(content)
        pages = data.get('query', {}).get('pages', {})

        for page_id, page_data in pages.items():
            if page_id == '-1':
                continue

            revisions = page_data.get('revisions', [])
            if not revisions:
                continue

            wikitext = revisions[0].get('slots', {}).get('main', {}).get('*', '')

            result = {}

            # Extract formula from infobox
            formula_match = re.search(r'\|\s*formula\s*=\s*([^\|\n]+)', wikitext, re.IGNORECASE)
            if formula_match:
                formula = clean_wiki_markup(formula_match.group(1))
                if formula:
                    result['formula'] = formula

            # Extract crystal system
            crystal_match = re.search(r'\|\s*crystal\s*system\s*=\s*([^\|\n]+)', wikitext, re.IGNORECASE)
            if crystal_match:
                result['crystal_system'] = clean_wiki_markup(crystal_match.group(1))

            # Extract space group
            space_match = re.search(r'\|\s*space\s*group\s*=\s*([^\|\n]+)', wikitext, re.IGNORECASE)
            if space_match:
                result['space_group'] = clean_wiki_markup(space_match.group(1))

            # Extract Mohs hardness
            mohs_match = re.search(r'\|\s*mohs\s*=\s*([^\|\n]+)', wikitext, re.IGNORECASE)
            if mohs_match:
                result['mohs_hardness'] = clean_wiki_markup(mohs_match.group(1))

            # Extract specific gravity/density
            gravity_match = re.search(r'\|\s*specific\s*gravity\s*=\s*([^\|\n]+)', wikitext, re.IGNORECASE)
            if gravity_match:
                result['specific_gravity'] = clean_wiki_markup(gravity_match.group(1))

            # Extract color
            color_match = re.search(r'\|\s*color\s*=\s*([^\|\n]+)', wikitext, re.IGNORECASE)
            if color_match:
                result['color'] = clean_wiki_markup(color_match.group(1))

            # Extract luster
            luster_match = re.search(r'\|\s*luster\s*=\s*([^\|\n]+)', wikitext, re.IGNORECASE)
            if luster_match:
                result['luster'] = clean_wiki_markup(luster_match.group(1))

            # Extract IMA symbol
            ima_match = re.search(r'\|\s*ima\s*symbol\s*=\s*([^\|\n]+)', wikitext, re.IGNORECASE)
            if ima_match:
                result['ima_symbol'] = clean_wiki_markup(ima_match.group(1))

            # Extract Strunz classification
            strunz_match = re.search(r'\|\s*strunz\s*=\s*([^\|\n]+)', wikitext, re.IGNORECASE)
            if strunz_match:
                result['strunz_classification'] = clean_wiki_markup(strunz_match.group(1))

            # Extract Dana classification
            dana_match = re.search(r'\|\s*dana\s*=\s*([^\|\n]+)', wikitext, re.IGNORECASE)
            if dana_match:
                result['dana_classification'] = clean_wiki_markup(dana_match.group(1))

            if result:
                return result

    except (json.JSONDecodeError, KeyError):
        pass

    return None


def clean_wiki_markup(text: str) -> str:
    """Remove Wikipedia markup from text."""
    if not text:
        return ''

    # Handle {{chem2|...}} chemical formula templates - extract the formula
    text = re.sub(r'\{\{chem2?\|([^}|]+)(?:\|[^}]*)?\}\}', r'\1', text)
    text = re.sub(r'\{\{chem\|([^}]+)\}\}', lambda m: m.group(1).replace('|', ''), text)

    # Handle {{Cite...}} templates - remove them
    text = re.sub(r'\{\{[Cc]ite[^}]*\}\}', '', text)

    # Handle nested templates {{...{{...}}...}}
    while '{{' in text:
        old_text = text
        text = re.sub(r'\{\{[^{}]*\}\}', '', text)
        if text == old_text:
            break

    # Remove wiki links [[text|display]] -> display or [[text]] -> text
    text = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', text)
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)

    # Remove templates {{template|arg}}
    text = re.sub(r'\{\{[^}]+\}\}', '', text)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove references
    text = re.sub(r'<ref[^>]*>.*?</ref>', '', text, flags=re.DOTALL)
    text = re.sub(r'<ref[^/]*/>', '', text)

    # Clean up subscript/superscript markup
    text = re.sub(r'\{\{sub\|([^}]+)\}\}', r'_\1', text)
    text = re.sub(r'\{\{sup\|([^}]+)\}\}', r'^\1', text)

    # Remove extra whitespace
    text = ' '.join(text.split())

    return text.strip()


def extract_formula_from_text(text: str) -> str:
    """Try to extract chemical formula from text."""
    if not text:
        return ''

    # Common mineral formula patterns
    patterns = [
        # Match formulas like Al2SiO5, CaCO3, Fe2O3
        r'\b([A-Z][a-z]?\d*(?:[A-Z][a-z]?\d*)*(?:\([A-Z][a-z]?\d*(?:[A-Z][a-z]?\d*)*\)\d*)*)\b',
        # Match formulas with parentheses like Ca(CO3)
        r'\b([A-Z][a-z]?\d*(?:\([^)]+\)\d*)?(?:[A-Z][a-z]?\d*)*)\b',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # Validate it looks like a formula (has letters and usually numbers)
            if len(match) >= 4 and re.search(r'[A-Z]', match) and re.search(r'[a-z0-9]', match):
                # Filter out common words
                if match.lower() not in ['the', 'and', 'for', 'are', 'this', 'with']:
                    return match

    return ''


def extract_crystal_system(text: str) -> str:
    """Extract crystal system from text."""
    crystal_systems = [
        'triclinic', 'monoclinic', 'orthorhombic', 'tetragonal',
        'trigonal', 'hexagonal', 'cubic', 'isometric'
    ]

    text_lower = text.lower()
    for system in crystal_systems:
        if system in text_lower:
            return system.capitalize()

    return ''


def get_mindat_search(mineral_name: str) -> Optional[Dict]:
    """
    Search Mindat.org for mineral info (basic scraping, no API key needed).
    Note: Mindat has rate limits, use sparingly.
    """
    clean_name = mineral_name.strip().lower().replace(' ', '-')
    url = f"https://www.mindat.org/min-{clean_name}.html"

    content = fetch_url(url)
    if not content:
        # Try search
        search_url = f"https://www.mindat.org/search.php?search={urllib.parse.quote(mineral_name)}"
        content = fetch_url(search_url)
        if not content:
            return None

    # Basic extraction from HTML (simplified)
    result = {'name': mineral_name.title(), 'source': 'Mindat.org'}

    # Try to find formula
    formula_match = re.search(r'<span[^>]*class="formula"[^>]*>([^<]+)</span>', content)
    if formula_match:
        result['formula'] = formula_match.group(1).strip()

    # Try to find crystal system
    crystal_match = re.search(r'Crystal System[:\s]*</[^>]+>\s*<[^>]+>([^<]+)', content, re.IGNORECASE)
    if crystal_match:
        result['crystal_system'] = crystal_match.group(1).strip()

    return result if len(result) > 2 else None


def get_online_mineral_data(mineral_name: str) -> Optional[Dict]:
    """
    Main function to get mineral data from online sources.
    Tries Wikipedia first, then Mindat as fallback.
    """
    if not mineral_name or len(mineral_name) < 2:
        return None

    # Try Wikipedia first (most reliable and comprehensive)
    wiki_data = get_wikipedia_mineral_data(mineral_name)
    if wiki_data:
        return wiki_data

    # Mindat as fallback (may have rate limits)
    # Uncomment if needed:
    # mindat_data = get_mindat_search(mineral_name)
    # if mindat_data:
    #     return mindat_data

    return None


def format_online_data_for_display(data: Dict) -> Dict:
    """
    Format online mineral data to match RRUFF display format.
    """
    if not data:
        return None

    name = data.get('name', '')
    formula = data.get('formula', '')

    # If formula looks invalid (contains wiki markup, plain text, or is too short), use known formula
    formula_looks_invalid = (
        not formula or
        len(formula) < 3 or
        '{{' in formula or
        '[[' in formula or
        formula.lower().startswith('the ') or
        formula.lower().startswith('a ') or
        '<!--' in formula
    )

    if formula_looks_invalid:
        formula = KNOWN_FORMULAS.get(name.lower(), '')

    # Clean up formula if it still has issues
    if formula:
        # Remove any remaining wiki markup
        formula = re.sub(r'\{\{[^}]*\}\}', '', formula)
        formula = re.sub(r'\[\[[^\]]*\]\]', '', formula)
        formula = re.sub(r'<!--.*?-->', '', formula)
        formula = formula.strip()

    return {
        'name': name,
        'rruff_id': f"WIKI-{name.upper()[:10]}",
        'formula': formula,
        'crystal_system': data.get('crystal_system', ''),
        'space_group': data.get('space_group', ''),
        'chemistry_elements': '',  # Would need parsing from formula
        'ima_status': data.get('ima_status', 'Wikipedia source'),
        'ima_number': data.get('ima_symbol', ''),
        'year_first_published': '',
        'country_type_locality': '',
        'structural_groupname': data.get('strunz_classification', ''),
        'fleischers_groupname': data.get('dana_classification', ''),
        'crystal_morphology': '',
        'oldest_known_age_ma': '',
        'paragenetic_modes': '',
        # Additional Wikipedia data
        'mohs_hardness': data.get('mohs_hardness', ''),
        'specific_gravity': data.get('specific_gravity', ''),
        'color': data.get('color', ''),
        'luster': data.get('luster', ''),
        'description': data.get('description', ''),
        'source': data.get('source', 'Online'),
        'source_url': data.get('wikipedia_url', ''),
    }


# Test function
if __name__ == '__main__':
    test_minerals = ['Kyanite', 'Garnet', 'Disthene', 'Almandine', 'Quartz']

    for mineral in test_minerals:
        print(f"\n=== {mineral} ===")
        data = get_online_mineral_data(mineral)
        if data:
            formatted = format_online_data_for_display(data)
            for key, value in formatted.items():
                if value:
                    print(f"  {key}: {value}")
        else:
            print("  No data found")
