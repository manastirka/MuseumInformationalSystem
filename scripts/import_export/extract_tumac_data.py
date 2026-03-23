#!/usr/bin/env python3
"""Extract structured data from OGK tumac PDFs/DOCs and update geological_map_sheets.json."""
import json
import os
import re
import subprocess
import unicodedata

import PyPDF2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TUMACI_DIR = os.path.join(BASE_DIR, 'Karte', 'Tumaci Srbija')
SHEETS_FILE = os.path.join(BASE_DIR, 'data', 'geological_map_sheets.json')

# Explicit overrides: sheet folder -> tumac filename
EXPLICIT_MATCHES = {
    'bor':                  'Tumac_Bor.pdf',
    'nis':                  'K34-32_Tumac_Nis.doc',
    'kumanovo':             'Tumac_Kumanova.pdf',
    'pec i kukes':          'K34-53_Pec i K34-65_Kukes-Tumac.doc',
    'L34-64 Subotica':      'L34-64_Tumac Bacalmas_Subotica_Segedin.doc',
    'L34-130 Turnu Severin': 'L34-130_Tumac_Donji Milanovac Baja de Arama Orsova TURNU SEVERIN.doc',
    'vlasotince':           'K34-45_Tumac_Vlasotince.doc',
    'vranje':               'K34-56_Tumac_Vranje.doc',
    'vrnjci':               'K34-18_Tumac_Vrnjci.doc',
    'Vrsac':                'L34-103_Tumac_Vrsac.doc',
    'zagubica':             'L34-140_Tumac_Zagubica.doc',
    'zajecar':              'K34-9_Tumac_Zajecar.doc',
}

# City name aliases for matching tumac filenames to map sheets
NAME_ALIASES = {
    'bijelo polje': ['bijelo polje', 'bpolje', 'b.polje', 'b polje'],
    'K34-22 Belogradcik': ['belogradcik', 'belogradchik', 'knjazevac belogradcik'],
    'K34-30 Novi Pazar': ['novi pazar', 'n.pazar', 'n pazar'],
    'titova mitrovica': ['titova mitrovica', 'kosovska mitrovica', 'mitrovica'],
    'pec i kukes': ['pec i kukes', 'pec i k34-65 kukes'],
    'L34-130 Turnu Severin': ['turnu severin', 'donji milanovac baja de arama orsova turnu severin'],
    'L34-64 Subotica': ['subotica', 'bacalmas subotica segedin'],
    'ali bunar': ['alibunar', 'ali bunar'],
    'backa palanka': ['backa palanka'],
    'bela crkva': ['bela crkva'],
    'bela palanka': ['bela palanka'],
    'donji milanovac': ['donji milanovac'],
    'gornji milanovac': ['gornji milanovac'],
    'Jasa Tomic': ['jasa tomic'],
    'vrnjci': ['vrnjci', 'vrnjacka banja'],
    'kumanovo': ['kumanovo', 'kumanova'],
}

# Geological periods to detect in TOC (both Latin and Cyrillic)
GEOLOGICAL_PERIODS = [
    ('Prekambrijum', ['PREKAMBRIJUM', 'PROTEROZOIK', 'ПРЕКАМБРИЈУМ', 'ПРОТЕРОЗОИК']),
    ('Rifeo-kambrijum', ['RIFEO-KAMBRIJUM', 'RIFEJ', 'РИФЕЈ']),
    ('Kambrijum', ['KAMBRIJUM', 'КАМБРИЈУМ']),
    ('Ordovicijum', ['ORDOVICIJUM', 'ОРДОВИЦИЈУМ']),
    ('Silur', ['SILUR', 'СИЛУР']),
    ('Devon', ['DEVON', 'ДЕВОН']),
    ('Karbon', ['KARBON', 'КАРБОН']),
    ('Perm', [' PERM', 'PERM ', 'ПЕРМ']),
    ('Trijas', ['TRIJAS', 'ТРИЈАС']),
    ('Jura', [' JURA', 'JURA ', 'ЈУРА']),
    ('Kreda', ['KREDA', 'DONJA KREDA', 'GORNJA KREDA', 'КРЕДА']),
    ('Paleogen', ['PALEOGEN', 'ПАЛЕОГЕН']),
    ('Neogen', ['NEOGEN', 'НЕОГЕН']),
    ('Kvartar', ['KVARTAR', 'КВАРТАР']),
    ('Pleistocen', ['PLEISTOCEN', 'ПЛЕИСТОЦЕН']),
    ('Holocen', ['HOLOCEN', 'ХОЛОЦЕН']),
]

# Mineral resource types (both Latin and Cyrillic)
MINERAL_TYPES = [
    ('Metali', ['METAL', 'BAKAR', 'ZLATO', 'SREBRO', 'OLOVO', 'CINK',
                'GVOŽĐ', 'HROM', 'NIKAL', 'ANTIMON', 'MANGAN', 'MOLIBDEN',
                'МЕТАЛ', 'БАКАР', 'ЗЛАТО', 'СРЕБРО', 'ОЛОВО', 'ЦИНК',
                'ГВОЖЂ', 'ХРОМ', 'НИКАЛ', 'АНТИМОН']),
    ('Nemetali', ['NEMETAL', 'MAGNEZIT', 'AZBEST', 'FELDSPAT', 'KVARC',
                  'KAOLIN', 'GLINA', 'GIPS',
                  'НЕМЕТАЛ', 'МАГНЕЗИТ', 'АЗБЕСТ', 'КАОЛИН']),
    ('Ugljevi', ['UGALJ', 'UGLJEVI', 'LIGNIT', 'MRKI UGALJ',
                 'УГАЉ', 'УГЉЕВИ', 'ЛИГНИТ']),
    ('Gradjevinski materijal', ['GRAĐEVINSK', 'TEHNIČKO-GRAĐEVINSK',
                                'KAMEN', 'ŠLJUNAK', 'PESAK',
                                'ГРАЂЕВИНСК', 'КАМЕН', 'ШЉУНАК', 'ПЕСАК']),
    ('Rude', ['RUDNE POJAVE', 'RUDNA', 'RUDE', 'RUDNO',
              'РУДНЕ ПОЈАВЕ', 'РУДНА', 'РУДЕ', 'РУДНО']),
]

# Tectonic features
TECTONIC_FEATURES = [
    'ANTIKLINORIJ', 'SINKLINORIJ', 'SINFORMA', 'ANTIFORMA',
    'DEPRESIJ', 'NAVLAK', 'RASED',
    'DINARI', 'KARPATID', 'SRBOMAKED', 'VARDAR',
    'ŠUMADIJ', 'MORAV', 'TIMOČK',
    'АНТИКЛИНОРИЈ', 'СИНКЛИНОРИЈ', 'СИНФОРМА', 'АНТИФОРМА',
    'ДЕПРЕСИЈ', 'НАВЛАК', 'РАСЕД',
    'ДИНАРИ', 'КАРПАТИД', 'СРБОМАКЕД', 'ВАРДАР',
    'ШУМАДИЈ', 'МОРАВ', 'ТИМОЧК',
]


def normalize_text(text):
    """Normalize text for matching: lowercase, strip accents."""
    text = text.lower()
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in nfkd if not unicodedata.combining(c))


def find_tumac_file(sheet, all_files):
    """Find the best matching tumac file for a map sheet."""
    folder = sheet['folder']

    # Check explicit override first
    if folder in EXPLICIT_MATCHES:
        override = os.path.join(TUMACI_DIR, EXPLICIT_MATCHES[folder])
        if os.path.isfile(override):
            return override

    ogk_code = sheet['ogk_code']
    name = sheet['name']
    name_lower = name.lower()
    folder_lower = folder.lower()
    code_normalized = ogk_code.replace(' ', '')

    # Build alias list
    aliases = list(NAME_ALIASES.get(folder, []))
    if name_lower not in aliases:
        aliases.append(name_lower)
    if folder_lower not in aliases:
        aliases.append(folder_lower)

    candidates = []

    for fpath in all_files:
        fname = os.path.basename(fpath)
        fname_lower = fname.lower()
        fname_normalized = normalize_text(fname)
        is_pdf = fname_lower.endswith('.pdf')

        score = 0

        # OGK code match (strongest signal)
        code_match = re.search(r'[KL]34-\d+', fname, re.IGNORECASE)
        if code_match and code_match.group().replace(' ', '') == code_normalized:
            score += 100

        # Exact word boundary match for city name
        for alias in aliases:
            alias_escaped = re.escape(alias)
            # Word boundary match in filename
            if re.search(r'(?:^|[\s_\-])' + alias_escaped + r'(?:[\s_\-.,]|$)', fname_lower):
                score += 60
                break
            elif re.search(r'(?:^|[\s_\-])' + re.escape(normalize_text(alias)) + r'(?:[\s_\-.,]|$)', fname_normalized):
                score += 55
                break

        # Substring match (weaker, only for longer names)
        if score == 0 and len(name_lower) > 4:
            if name_lower in fname_lower:
                score += 30

        # Prefer PDFs over DOCs
        if is_pdf:
            score += 10

        if score > 10:  # Must have at least name or code match
            candidates.append((score, fpath))

    if not candidates:
        return None

    candidates.sort(key=lambda x: -x[0])
    return candidates[0][1]


def extract_pdf_text(pdf_path, max_pages=12):
    """Extract text from first N pages of a PDF."""
    try:
        reader = PyPDF2.PdfReader(pdf_path)
        total_pages = len(reader.pages)
        texts = []
        for i in range(min(max_pages, total_pages)):
            try:
                text = reader.pages[i].extract_text() or ''
                texts.append(text)
            except Exception:
                texts.append('')
        return texts, total_pages
    except Exception as e:
        print(f"  ERROR reading PDF {pdf_path}: {e}")
        return [], 0


def extract_doc_text(doc_path):
    """Extract text from a DOC file using antiword."""
    try:
        result = subprocess.run(
            ['antiword', doc_path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            print(f"  WARNING: antiword error: {result.stderr[:200]}")
            return [], 0

        full_text = result.stdout
        # Split into pseudo-pages by form feed or estimate
        lines = full_text.split('\n')
        total_lines = len(lines)
        # Approximate pages (roughly 50 lines per page)
        total_pages = max(1, total_lines // 50)

        # Split into chunks for processing
        chunk_size = min(50, max(20, total_lines // max(1, total_pages)))
        texts = []
        for i in range(0, min(total_lines, chunk_size * 12), chunk_size):
            chunk = '\n'.join(lines[i:i+chunk_size])
            texts.append(chunk)

        return texts, total_pages
    except Exception as e:
        print(f"  ERROR reading DOC {doc_path}: {e}")
        return [], 0


def extract_file_text(fpath, max_pages=12):
    """Extract text from either PDF or DOC file."""
    if fpath.lower().endswith('.pdf'):
        return extract_pdf_text(fpath, max_pages)
    elif fpath.lower().endswith('.doc'):
        return extract_doc_text(fpath)
    return [], 0


def extract_title_info(page1_text):
    """Extract sheet name, OGK code, and year from title page."""
    info = {}

    # Extract OGK code (Latin)
    code_match = re.search(r'[KL]\s*34[-–]\s*(\d+)', page1_text)
    if code_match:
        info['ogk_code_from_tumac'] = code_match.group().replace(' ', '').replace('–', '-')

    # Extract year
    year_match = re.search(r'(?:Beograd|Zagreb|Sarajevo|Titograd|Ljubljana|Београд|Загреб)[\s,.]*(\d{4})', page1_text)
    if year_match:
        info['year'] = int(year_match.group(1))
    else:
        year_match = re.search(r'\b(19[5-9]\d|20[0-2]\d)\b', page1_text)
        if year_match:
            info['year'] = int(year_match.group(1))

    return info


def extract_authors_info(pages_text):
    """Extract authors and institution from early pages."""
    info = {}
    combined = ' '.join(pages_text[:6])

    # Institution (Latin and Cyrillic patterns)
    inst_patterns = [
        r'(GEOLOŠKI INSTITUT[^,\n]*)',
        r'(ZAVOD ZA GEOLOŠK[^,\n]*)',
        r'(RO GEOLOŠKI[^,\n]*)',
        r'(INSTITUT ZA GEOLOG[^,\n]*)',
        r'(GEOINŽENJERING[^,\n]*)',
        r'(RUDARSKO-GEOLOŠK[^,\n]*)',
        r'(ГЕОЛОШКИ ИНСТИТУТ[^,\n]*)',
        r'(ЗАВОД ЗА ГЕОЛОШК[^,\n]*)',
        r'(РУДАРСКО.ГЕОЛОШК[^,\n]*)',
    ]
    for pat in inst_patterns:
        m = re.search(pat, combined, re.IGNORECASE)
        if m:
            inst = m.group(1).strip().rstrip(',.')
            inst = re.sub(r'\s+', ' ', inst)
            info['institution'] = inst
            break

    # Year from author page
    for text in pages_text[:6]:
        m = re.search(r'(?:IZRADIO|izradio|Izradio|ИЗРАДИО|израдио)[:\s]*.*?(\d{4})', text, re.DOTALL)
        if m:
            info['map_year'] = int(m.group(1))
            break

    # Authors of map (Latin)
    for text in pages_text[:6]:
        m = re.search(r'Autori\s+karte[:\s]*([A-ZŠĐČĆŽ][A-ZŠĐČĆŽ\s,IILJ.]+)', text)
        if m:
            authors_raw = m.group(1).strip()
            authors_raw = re.sub(r'\s+', ' ', authors_raw)
            authors_raw = authors_raw.rstrip('.')
            info['map_authors'] = authors_raw
            break

    # Authors of map (Cyrillic)
    if 'map_authors' not in info:
        for text in pages_text[:6]:
            m = re.search(r'(?:Карту израдили|Аутори карте)[:\s]*([А-ЯЁа-яёЂЉЊЋЏђљњћџĐŠČĆŽšđčćž\s,И.]+)', text)
            if m:
                authors_raw = m.group(1).strip()
                authors_raw = re.sub(r'\s+', ' ', authors_raw)
                authors_raw = authors_raw.rstrip('.')
                info['map_authors'] = authors_raw
                break

    # Authors of tumac (Latin)
    for text in pages_text[:6]:
        m = re.search(r'Autori\s+tuma[čc]a[:\s]*([A-ZŠĐČĆŽ][A-ZŠĐČĆŽ\s,IILJ.]+)', text)
        if m:
            authors_raw = m.group(1).strip()
            authors_raw = re.sub(r'\s+', ' ', authors_raw)
            authors_raw = authors_raw.rstrip('.')
            info['tumac_authors'] = authors_raw
            break

    # Authors of tumac (Cyrillic)
    if 'tumac_authors' not in info:
        for text in pages_text[:6]:
            m = re.search(r'(?:Тумач написали|Аутори тумача)[:\s]*([А-ЯЁа-яёЂЉЊЋЏђљњћџ\s,И.]+)', text)
            if m:
                authors_raw = m.group(1).strip()
                authors_raw = re.sub(r'\s+', ' ', authors_raw)
                authors_raw = authors_raw.rstrip('.')
                info['tumac_authors'] = authors_raw
                break

    return info


def extract_geological_periods(toc_text):
    """Extract geological periods present from TOC text."""
    periods = []
    toc_upper = toc_text.upper()

    for period_name, keywords in GEOLOGICAL_PERIODS:
        for kw in keywords:
            if kw in toc_upper:
                if period_name not in periods:
                    periods.append(period_name)
                break

    return periods


def extract_tectonic_info(toc_text):
    """Extract tectonic units/features from TOC."""
    features = []
    toc_upper = toc_text.upper()

    # Look for TEKTONIKA section content (Latin and Cyrillic)
    tek_match = re.search(
        r'(?:TEKTONIKA|ТЕКТОНИКА)(.*?)(?:PREGLED MINERALNIH|ПРЕГЛЕД МИНЕРАЛНИХ|ISTORIJA|ИСТОРИЈА|LITERATURA|ЛИТЕРАТУРА|$)',
        toc_upper, re.DOTALL
    )
    if tek_match:
        tek_section = tek_match.group(1)
        lines = tek_section.split('\n')
        for line in lines:
            line = line.strip()
            line = re.sub(r'[.\d]+$', '', line).strip()
            line = re.sub(r'\.{2,}', '', line).strip()
            if len(line) > 3 and not re.match(r'^(?:PREGLED|ПРЕГЛЕД|ISTORIJA|ИСТОРИЈА)', line):
                features.append(line.title())

    if not features:
        for feat in TECTONIC_FEATURES:
            if feat in toc_upper:
                for line in toc_upper.split('\n'):
                    if feat in line:
                        clean = re.sub(r'[.\d]+$', '', line).strip()
                        clean = re.sub(r'\.{2,}', '', clean).strip()
                        if clean and len(clean) > 3:
                            features.append(clean.title())
                            break

    # Deduplicate
    seen = set()
    unique = []
    for f in features:
        fl = f.lower()
        if fl not in seen:
            seen.add(fl)
            unique.append(f)
    return unique[:8]


def extract_mineral_resources(toc_text, full_text=''):
    """Extract mineral resource types from TOC."""
    resources = []
    search_text = (toc_text + ' ' + full_text).upper()

    min_match = re.search(
        r'(?:PREGLED MINERALNIH SIROVINA|ПРЕГЛЕД МИНЕРАЛНИХ СИРОВИНА)(.*?)(?:ISTORIJA|ИСТОРИЈА|LITERATURA|ЛИТЕРАТУРА|$)',
        search_text, re.DOTALL
    )
    search_area = min_match.group(1) if min_match else search_text

    for res_name, keywords in MINERAL_TYPES:
        for kw in keywords:
            if kw in search_area:
                if res_name not in resources:
                    resources.append(res_name)
                break

    return resources


def process_sheet(sheet, all_files):
    """Process a single map sheet: find tumac and extract data."""
    fpath = find_tumac_file(sheet, all_files)
    if not fpath:
        return None

    fname = os.path.basename(fpath)
    print(f"  Matched: {sheet['name']} ({sheet['ogk_code']}) -> {fname}")

    pages_text, total_pages = extract_file_text(fpath)
    if not pages_text:
        return None

    # Combine all extracted text for TOC search
    all_text = ' '.join(pages_text)

    # Find TOC section
    toc_text = ''
    for i, text in enumerate(pages_text):
        text_upper = text.upper()
        if 'SADRŽAJ' in text_upper or 'САДРЖАЈ' in text_upper or 'OPIS KARTIRANIH' in text_upper or 'ОПИС КАРТИРАНИХ' in text_upper:
            toc_text = ' '.join(pages_text[i:i+4])
            break
    if not toc_text:
        toc_text = all_text  # Use all text as fallback

    # Extract all data
    title_info = extract_title_info(pages_text[0] if pages_text else '')
    authors_info = extract_authors_info(pages_text)
    periods = extract_geological_periods(toc_text)
    tectonics = extract_tectonic_info(toc_text)
    minerals = extract_mineral_resources(toc_text, all_text)

    tumac_data = {
        'tumac_file': fname,
        'total_pages': total_pages,
    }

    if title_info.get('year'):
        tumac_data['year'] = title_info['year']
    if authors_info.get('map_year'):
        tumac_data['map_year'] = authors_info['map_year']
    if authors_info.get('institution'):
        tumac_data['institution'] = authors_info['institution']
    if authors_info.get('map_authors'):
        # Clean trailing junk from author strings
        auth = authors_info['map_authors']
        auth = re.sub(r'\s*(?:SADRŽAJ|SADR|Autori|$).*', '', auth, flags=re.IGNORECASE).rstrip('. ')
        if auth:
            tumac_data['map_authors'] = auth
    if authors_info.get('tumac_authors'):
        auth = authors_info['tumac_authors']
        auth = re.sub(r'\s*(?:SADRŽAJ|SADR|Autori|$).*', '', auth, flags=re.IGNORECASE).rstrip('. ')
        if auth:
            tumac_data['tumac_authors'] = auth
    if periods:
        tumac_data['geological_periods'] = periods
    if tectonics:
        tumac_data['tectonic_features'] = tectonics
    if minerals:
        tumac_data['mineral_resources'] = minerals

    return tumac_data


def main():
    with open(SHEETS_FILE, 'r', encoding='utf-8') as f:
        sheets = json.load(f)

    # Collect ALL files (PDFs and DOCs)
    all_files = []
    for fname in os.listdir(TUMACI_DIR):
        if fname.lower().endswith(('.pdf', '.doc')):
            all_files.append(os.path.join(TUMACI_DIR, fname))

    print(f"Found {len(all_files)} tumac files ({sum(1 for f in all_files if f.endswith('.pdf'))} PDF, "
          f"{sum(1 for f in all_files if f.endswith('.doc'))} DOC) for {len(sheets)} map sheets\n")

    matched = 0
    unmatched = []

    for sheet in sheets:
        print(f"Processing: {sheet['name']} ({sheet['ogk_code']})")
        tumac_data = process_sheet(sheet, all_files)
        if tumac_data:
            sheet['tumac'] = tumac_data
            matched += 1
        else:
            print(f"  NO MATCH FOUND")
            unmatched.append(sheet['name'])

    with open(SHEETS_FILE, 'w', encoding='utf-8') as f:
        json.dump(sheets, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"Matched: {matched}/{len(sheets)}")
    if unmatched:
        print(f"Unmatched: {', '.join(unmatched)}")

    # Print a sample
    for sheet in sheets:
        if sheet.get('tumac') and sheet['name'] == 'Beograd':
            print(f"\nSample (Beograd):")
            print(json.dumps(sheet['tumac'], ensure_ascii=False, indent=2))
            break

    # Print a Cyrillic sample
    for sheet in sheets:
        if sheet.get('tumac') and sheet['tumac']['tumac_file'].endswith('.doc'):
            print(f"\nSample DOC ({sheet['name']}):")
            print(json.dumps(sheet['tumac'], ensure_ascii=False, indent=2))
            break


if __name__ == '__main__':
    main()
