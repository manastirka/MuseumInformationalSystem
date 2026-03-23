#!/usr/bin/env python3
"""Extract ore deposit data from SerbiaOreDeposits.pdf into JSON."""
import json
import re
import pdfplumber

PDF_PATH = 'Karte/SerbiaOreDeposits.pdf'
OUTPUT_PATH = 'data/ore_deposits.json'


def extract_deposits():
    pdf = pdfplumber.open(PDF_PATH)
    all_text = []
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            all_text.append(text)
    pdf.close()

    full_text = '\n'.join(all_text)

    # Split into deposit entries by the YUG identifier pattern at the start of each entry
    # Each deposit page starts with the header line then YUG-XXXXX
    entries = re.split(r'Mineral deposits of Serbia\s*-\s*Ore deposits database\n', full_text)

    deposits = []
    current_deposit = None

    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue

        # Check if this chunk starts a new deposit (has YUG-XXXXX followed by General data)
        yug_match = re.match(r'(YUG-\d+)\s*\n(.+?)(?:\n|$)', entry)
        if not yug_match:
            # Continuation page of previous deposit - skip (we already got coordinates from first page)
            # But check if it's a continuation that still has the same YUG ID
            yug_cont = re.match(r'(YUG-\d+)\s*\n', entry)
            if yug_cont and current_deposit and yug_cont.group(1) == current_deposit.get('identifier'):
                # Continuation page - could extract more data but we have the essentials
                pass
            continue

        identifier = yug_match.group(1)
        name = yug_match.group(2).strip()

        # Check if this has General data section (first page of a deposit)
        if 'General data' not in entry:
            # continuation page
            continue

        deposit = {
            'identifier': identifier,
            'name': name,
            'latitude': None,
            'longitude': None,
            'commodities': [],
            'status': '',
            'district': '',
            'company': '',
            'deposit_type': '',
            'exploitation_type': '',
        }

        # Extract longitude
        lon_match = re.search(r'Longitude:\s+([\d.]+)', entry)
        if lon_match:
            try:
                deposit['longitude'] = float(lon_match.group(1))
            except ValueError:
                pass

        # Extract latitude
        lat_match = re.search(r'Latitude:\s+([\d.]+)', entry)
        if lat_match:
            try:
                deposit['latitude'] = float(lat_match.group(1))
            except ValueError:
                pass

        # Extract district
        dist_match = re.search(r'District:\s+(.+?)(?:\n|$)', entry)
        if dist_match:
            deposit['district'] = dist_match.group(1).strip()

        # Extract status
        status_match = re.search(r'Status:\s+(.+?)(?:\n|$)', entry)
        if status_match:
            deposit['status'] = status_match.group(1).strip()

        # Extract company
        comp_match = re.search(r'Company:\s+(.+?)(?:\n|$)', entry)
        if comp_match:
            val = comp_match.group(1).strip()
            # Don't capture if it's actually the next field
            if val and 'Longitude' not in val:
                deposit['company'] = val

        # Extract commodities from the Commodities: lines
        # Pattern: symbol followed by amount, t, Class, letter
        comm_section = re.search(r'Commodities:\s+(.+?)(?=Company:|Longitude:)', entry, re.DOTALL)
        if comm_section:
            comm_text = comm_section.group(1)
            # Match commodity lines: Au 0 t Class N/A or Pb 215 000 t Class B
            for m in re.finditer(r'([A-Za-z]+)\s+([\d\s]+)\s*t\s+Class\s+([A-Z/]+)', comm_text):
                symbol = m.group(1).strip()
                tonnage_str = m.group(2).strip().replace(' ', '')
                class_val = m.group(3).strip()
                try:
                    tonnage = int(tonnage_str)
                except ValueError:
                    tonnage = 0
                deposit['commodities'].append({
                    'symbol': symbol,
                    'tonnage': tonnage,
                    'class': class_val
                })

        # Extract deposit type (gitology)
        git_match = re.search(r'Ore deposit type \(gitology\)\s*\n\s*(.+?)(?:\n|$)', entry)
        if git_match:
            deposit['deposit_type'] = git_match.group(1).strip()

        # Extract exploitation type
        expl_match = re.search(r'Exploitation type\s*\n\s*(.+?)(?:\n|$)', entry)
        if expl_match:
            deposit['exploitation_type'] = expl_match.group(1).strip()

        # Only include deposits with valid coordinates
        if deposit['latitude'] and deposit['longitude']:
            current_deposit = deposit
            deposits.append(deposit)
        else:
            current_deposit = deposit  # track for continuation pages

    return deposits


if __name__ == '__main__':
    deposits = extract_deposits()
    print(f"Extracted {len(deposits)} deposits with coordinates")

    # Stats
    no_coords = 0
    with_coords = len(deposits)
    statuses = {}
    for d in deposits:
        s = d['status']
        statuses[s] = statuses.get(s, 0) + 1

    print(f"\nStatus distribution:")
    for s, c in sorted(statuses.items(), key=lambda x: -x[1]):
        print(f"  {s}: {c}")

    # Commodity summary
    all_comms = {}
    for d in deposits:
        for c in d['commodities']:
            sym = c['symbol']
            all_comms[sym] = all_comms.get(sym, 0) + 1
    print(f"\nCommodity frequency:")
    for sym, c in sorted(all_comms.items(), key=lambda x: -x[1]):
        print(f"  {sym}: {c}")

    # Sample
    print(f"\nSample entries:")
    for d in deposits[:3]:
        print(f"  {d['name']} ({d['identifier']}): {d['latitude']}, {d['longitude']} - {d['district']} - {[c['symbol'] for c in d['commodities']]}")

    # Save
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(deposits, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {OUTPUT_PATH}")
