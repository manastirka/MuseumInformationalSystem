#!/usr/bin/env python3
"""Build data/ogk_points.json from the OGK Srbija point database.

Source (read-only CIFS mount, never written to):
    /mnt/licno/OGK_Srbija_podaci/03_master/sve_tacke.csv   (UTF-8, ',')
    /mnt/licno/OGK_Srbija_podaci/03_master/minerali.csv    (UTF-8 BOM, ';')
    /mnt/licno/OGK_Srbija_podaci/00_inventar/listovi.csv   (UTF-8, ',')

Only geological point categories are kept; settlements, hydrography and relief
are dropped because the OSM basemap already carries them. The script is
idempotent: the same inputs always produce the same JSON, and --dry-run only
prints the group counts without touching the disk.
"""
import argparse
import csv
import datetime
import json
import os
import sys

OGK_ROOT = '/mnt/licno/OGK_Srbija_podaci'
TACKE_CSV = os.path.join(OGK_ROOT, '03_master', 'sve_tacke.csv')
MINERALI_CSV = os.path.join(OGK_ROOT, '03_master', 'minerali.csv')
LISTOVI_CSV = os.path.join(OGK_ROOT, '00_inventar', 'listovi.csv')

OUTPUT_PATH = os.path.join('data', 'ogk_points.json')
IZVOR = 'OGK SFRJ 1:100 000'

# kategorija -> grupa (grupe su slojevi u bočnom meniju karte).
KATEGORIJA_U_GRUPU = {
    'rudnik': 'rudnici',
    'pojava_minerala': 'rudnici',
    'kamenolom': 'kamenolomi',
    'peskara': 'kamenolomi',
    'gliniste': 'kamenolomi',
    'busotina': 'busotine',
    'izvor': 'izvori',
    'fosilni_lokalitet': 'fosili',
    'rased': 'rasedi',
    'geoloska_jedinica': 'jedinice',
    'ostalo': 'ostalo',
}

# Redosled grupa u izlazu (stabilan, da JSON ne igra između pokretanja).
GRUPE = ['rudnici', 'kamenolomi', 'busotine', 'izvori',
         'fosili', 'rasedi', 'jedinice', 'ostalo']

# Granice Srbije — tačka van ovog pravougaonika je greška u izvoru.
LAT_MIN, LAT_MAX = 41.5, 46.5
LON_MIN, LON_MAX = 18.5, 23.5


def _ucitaj_nazive_listova():
    """Return list_id -> naziv lista iz inventara listova."""
    nazivi = {}
    with open(LISTOVI_CSV, encoding='utf-8-sig', newline='') as handle:
        for red in csv.DictReader(handle):
            list_id = (red.get('list_id') or '').strip()
            if list_id:
                nazivi[list_id] = (red.get('naziv') or '').strip()
    return nazivi


def _ucitaj_sirovine():
    """Return id -> sirovina iz minerali.csv (BOM + ';' separator)."""
    sirovine = {}
    with open(MINERALI_CSV, encoding='utf-8-sig', newline='') as handle:
        for red in csv.DictReader(handle, delimiter=';'):
            tacka_id = (red.get('id') or '').strip()
            sirovina = (red.get('sirovina') or '').strip()
            if tacka_id and sirovina:
                sirovine[tacka_id] = sirovina
    return sirovine


def _koordinata(vrednost):
    """Return float or None — prazno i neispravno se tretiraju isto."""
    try:
        return float((vrednost or '').strip())
    except (TypeError, ValueError):
        return None


def izgradi_tacke():
    """Return (tacke, odbaceno) — odbaceno su redovi sa lošim koordinatama."""
    nazivi_listova = _ucitaj_nazive_listova()
    sirovine = _ucitaj_sirovine()

    tacke = []
    odbaceno = []
    with open(TACKE_CSV, encoding='utf-8-sig', newline='') as handle:
        for red in csv.DictReader(handle):
            kategorija = (red.get('kategorija') or '').strip()
            grupa = KATEGORIJA_U_GRUPU.get(kategorija)
            if grupa is None:
                continue

            tacka_id = (red.get('id') or '').strip()
            lat = _koordinata(red.get('lat'))
            lon = _koordinata(red.get('lon'))
            if lat is None or lon is None:
                odbaceno.append((tacka_id, 'координате нису број',
                                 red.get('lat'), red.get('lon')))
                continue
            if not (LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX):
                odbaceno.append((tacka_id, 'ван граница Србије', lat, lon))
                continue

            list_id = (red.get('list_id') or '').strip()
            tacke.append({
                'id': tacka_id,
                'list_id': list_id,
                'list_naziv': nazivi_listova.get(list_id, ''),
                'grupa': grupa,
                'kategorija': kategorija,
                'naziv': (red.get('naziv') or '').strip(),
                'opis': (red.get('opis') or '').strip(),
                'simbol_karte': (red.get('simbol_karte') or '').strip(),
                'jedinica': (red.get('jedinica') or '').strip(),
                'sirovina': sirovine.get(tacka_id, ''),
                'lat': lat,
                'lon': lon,
                'pouzdanost_gps': (red.get('pouzdanost_gps') or '').strip(),
            })

    tacke.sort(key=lambda t: t['id'])
    return tacke, odbaceno


def prebroj_grupe(tacke):
    """Return {grupa: N} u stabilnom redosledu, i za prazne grupe."""
    brojaci = {grupa: 0 for grupa in GRUPE}
    for tacka in tacke:
        brojaci[tacka['grupa']] += 1
    return brojaci


def _procitaj_zatecen(putanja):
    """Return već upisani JSON ili None ako ga nema / nije čitljiv."""
    if not os.path.exists(putanja):
        return None
    try:
        with open(putanja, encoding='utf-8') as handle:
            return json.load(handle)
    except (OSError, ValueError) as greska:
        print('Упозорење: затечени {} се не да прочитати ({}) — пише се нов.'
              .format(putanja, greska))
        return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true',
                        help='само испиши бројеве по групи, ништа не уписуј')
    parser.add_argument('--output', default=OUTPUT_PATH,
                        help='путања излазног JSON-а (подразумевано %(default)s)')
    args = parser.parse_args(argv)

    tacke, odbaceno = izgradi_tacke()
    brojaci = prebroj_grupe(tacke)

    for grupa in GRUPE:
        print('  {:<12} {:>5}'.format(grupa, brojaci[grupa]))
    print('  {:<12} {:>5}'.format('УКУПНО', len(tacke)))

    if odbaceno:
        # Ne gutamo tiho: svaki odbačen red mora da se vidi u izlazu.
        print('ОДБАЧЕНО (лоше координате): {}'.format(len(odbaceno)))
        for tacka_id, razlog, lat, lon in odbaceno:
            print('  {} — {} (lat={!r}, lon={!r})'.format(tacka_id, razlog, lat, lon))
    else:
        print('ОДБАЧЕНО (лоше координате): 0')

    if args.dry_run:
        print('--dry-run: ниједан фајл није измењен.')
        return 0

    podaci = {
        'generisano': datetime.date.today().isoformat(),
        'izvor': IZVOR,
        'ukupno': len(tacke),
        'grupe': brojaci,
        'tacke': tacke,
    }
    # Idempotentno: ako se podaci nisu promenili, zadrži zatečeni datum
    # generisanja da ponovljeno pokretanje ostavi fajl bajt-identičnim.
    zatecen = _procitaj_zatecen(args.output)
    if zatecen is not None:
        uporedi = dict(podaci)
        uporedi['generisano'] = zatecen.get('generisano')
        if uporedi == zatecen:
            podaci['generisano'] = zatecen.get('generisano')
    with open(args.output, 'w', encoding='utf-8') as handle:
        json.dump(podaci, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    print('Уписано: {} ({} тачака)'.format(args.output, len(tacke)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
