#!/usr/bin/env python3
"""Build data/ogk_radovi.json from the online harvest of papers per OGK point.

Source (read-only CIFS mount, never written to):
    /mnt/licno/OGK_Srbija_podaci/04_harvest_online/radovi/lokaliteti/<OGK_ID>/dosije.json

The harvest was run by locality NAME, so it is full of misses: a paper about
the Senj town choir hangs on „Сењ јурски кречњак“. Nothing is dropped, but each
paper is marked ``geo`` — whether its title, journal or abstract carries at
least one geological term. The map popup shows the geological ones first and
folds the rest away, so the popup does not turn into a dump.

The abstract itself is NOT written to the output (it would multiply the file
size several times over); it is only read while judging ``geo``.

The script is idempotent: the same inputs always produce the same JSON, and
--dry-run only prints the counts without touching the disk.
"""
import argparse
import datetime
import json
import os
import re
import sys
import unicodedata

OGK_ROOT = '/mnt/licno/OGK_Srbija_podaci'
RADOVI_DIR = os.path.join(OGK_ROOT, '04_harvest_online', 'radovi')
LOKALITETI_DIR = os.path.join(RADOVI_DIR, 'lokaliteti')

OUTPUT_PATH = os.path.join('data', 'ogk_radovi.json')
TACKE_PATH = os.path.join('data', 'ogk_points.json')
IZVOR = 'OGK harvest online 04_harvest_online/radovi'

# Колико знакова апстракта улази у оцену — почетак носи тему рада, а реп
# уме да склизне у захвалнице и референце (тамо „geological“ значи ништа).
APSTRAKT_ZNAKOVA = 500

# Геолошки појмови, српски и енглески, у ASCII облику без дијакритике (текст
# се нормализује пре поређења). Свака реч се мери на стварним подацима: тражи
# се ПОЧЕТАК речи (\b + појам), не било где у речи — иначе „ore“ покупи
# „before“ и „more“ и оцена престане да значи ишта (мерено: 398 → 144 погодака).
# Појмови без иједног поготка се задржавају као документован речник — не
# сметају, а описују шта се тражи.
GEO_POJMOVI = (
    # опште геолошко
    'geolo', 'geomorf', 'litolog', 'litho', 'facies', 'tekton', 'stratigraf',
    'sediment', 'massif', 'nappe', 'navlak', 'fault', 'rased', 'rasjed',
    # магматско / метаморфно
    'magmat', 'volcan', 'vulkan', 'petrol', 'granit', 'andesite', 'andezit',
    'basalt', 'bazalt', 'tuff', 'serpentin', 'ofiolit', 'ophiolit', 'metamorf',
    'skrilj', 'schist', 'gneiss', 'gnajs',
    # седиментно / карбонатно
    'krecnjak', 'limestone', 'dolomit', 'travertin', 'loess',
    # минерали и сировине
    'mineral', 'kvarc', 'quartz', 'opal', 'zeolit', 'barit', 'boksit',
    'coal', 'ugalj', 'lignit',
    # рударство и лежишта
    'ruda', 'rudn', 'rudarsk', 'ore', 'deposit', 'mining', 'quarry',
    'kamenolom', 'skarn', 'porphyr', 'porfir', 'epitherm', 'hydrothermal',
    'hidroterm', 'flotation', 'flotac',
    # палеонтологија
    'fosil', 'fossil', 'paleo', 'conodont', 'ammonit', 'amonit', 'trilobit',
    'foraminifer', 'radiolarij', 'mamut', 'mammoth', 'dinosaur',
    # хидрогеологија и карст
    'karst', 'hidrogeo', 'aquifer', 'speleo', 'geothermal', 'geoterm',
    'borehole', 'busotin',
    # геохемија и датовање
    'geochem', 'geohem', 'isotope', 'geochronolog', 'geohronolog',
    # хроностратиграфија
    'triass', 'jura', 'kred', 'cretaceous', 'terti', 'eocen', 'oligocen',
    'neogen', 'miocen', 'pliocen', 'quaternary', 'kvartar', 'pleistoc',
    'holocen',
)

_GEO_IZRAZI = tuple(re.compile(r'\b' + re.escape(pojam)) for pojam in GEO_POJMOVI)


# Ћирилица се пресликава у латиницу пре поређења (исти образац као
# uskladi_knjiga_depo_cli._name_key), да „Рудник“ и „Rudnik“ буду иста реч.
_CIR_U_LAT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'ђ': 'dj', 'е': 'e',
    'ж': 'z', 'з': 'z', 'и': 'i', 'ј': 'j', 'к': 'k', 'л': 'l', 'љ': 'lj',
    'м': 'm', 'н': 'n', 'њ': 'nj', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
    'т': 't', 'ћ': 'c', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'c',
    'џ': 'dz', 'ш': 's',
}


def _normalizuj(tekst):
    """Return lowercase ASCII text — ćirilica u latinicu, dijakritika pada."""
    tekst = (tekst or '').lower()
    tekst = ''.join(_CIR_U_LAT.get(znak, znak) for znak in tekst)
    tekst = unicodedata.normalize('NFKD', tekst)
    return ''.join(znak for znak in tekst if not unicodedata.combining(znak))


def je_geoloski(rad):
    """Return True ako naslov + časopis + početak apstrakta nose geološki pojam."""
    blob = _normalizuj(' '.join([
        rad.get('title') or '',
        rad.get('journal') or '',
        (rad.get('abstract') or '')[:APSTRAKT_ZNAKOVA],
    ]))
    return any(izraz.search(blob) for izraz in _GEO_IZRAZI)


def _godina(vrednost):
    """Return int ili None — рад без године иде на крај своје групе."""
    try:
        return int(vrednost)
    except (TypeError, ValueError):
        return None


def _kljuc_sortiranja(rad):
    # Прво geo, па новије горе, па по наслову. Рад без године иде на крај
    # своје групе — зато засебна застава испред саме године.
    godina = rad['godina']
    return (
        0 if rad['geo'] else 1,
        1 if godina is None else 0,
        -(godina or 0),
        _normalizuj(rad['naslov']),
    )


def _procitaj_dosije(putanja):
    with open(putanja, encoding='utf-8') as handle:
        return json.load(handle)


def izgradi_radove():
    """Return (radovi_po_lokalitetu, ukupno_radova, geo, ne_geo)."""
    radovi = {}
    ukupno = 0
    geo = 0

    for ime in sorted(os.listdir(LOKALITETI_DIR)):
        putanja = os.path.join(LOKALITETI_DIR, ime, 'dosije.json')
        if not os.path.exists(putanja):
            continue
        dosije = _procitaj_dosije(putanja)
        ogk_id = (dosije.get('ogk_id') or ime).strip()
        sirovi = dosije.get('radovi') or []
        if not sirovi:
            # Локалитет без иједног рада се не уписује — нема празних низова.
            continue

        spisak = []
        for rad in sirovi:
            je_geo = je_geoloski(rad)
            geo += 1 if je_geo else 0
            ukupno += 1
            spisak.append({
                'naslov': (rad.get('title') or '').strip(),
                'godina': _godina(rad.get('year')),
                'autori': (rad.get('authors') or '').strip(),
                'casopis': (rad.get('journal') or '').strip(),
                'doi': (rad.get('doi') or '').strip(),
                'url': (rad.get('url') or '').strip(),
                'pdf_url': (rad.get('pdf_url') or '').strip(),
                'geo': je_geo,
            })

        spisak.sort(key=_kljuc_sortiranja)
        radovi[ogk_id] = spisak

    return radovi, ukupno, geo, ukupno - geo


def sirocici(radovi, tacke_putanja):
    """Return ogk_id-evi kojih nema u data/ogk_points.json (ne gutamo ih tiho)."""
    if not os.path.exists(tacke_putanja):
        return None
    with open(tacke_putanja, encoding='utf-8') as handle:
        podaci = json.load(handle)
    poznati = {(tacka.get('id') or '').strip()
               for tacka in podaci.get('tacke', [])}
    return sorted(ogk_id for ogk_id in radovi if ogk_id not in poznati)


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
                        help='само испиши бројеве, ништа не уписуј')
    parser.add_argument('--output', default=OUTPUT_PATH,
                        help='путања излазног JSON-а (подразумевано %(default)s)')
    parser.add_argument('--tacke', default=TACKE_PATH,
                        help='путања до ogk_points.json ради провере сирочића')
    args = parser.parse_args(argv)

    # Извор је CIFS са прода: ако није монтиран, боље ненулти излаз него
    # тихо уписан празан фајл преко исправних података.
    if not os.path.isdir(LOKALITETI_DIR):
        print('ГРЕШКА: извор није доступан: {}\n'
              'Монтирај дељење пре покретања — ништа није уписано.'
              .format(LOKALITETI_DIR), file=sys.stderr)
        return 2

    radovi, ukupno, geo, ne_geo = izgradi_radove()
    if not radovi:
        print('ГРЕШКА: извор је доступан али нема ниједног рада — '
              'ништа није уписано.', file=sys.stderr)
        return 3

    print('  {:<22} {:>5}'.format('локалитета са радом', len(radovi)))
    print('  {:<22} {:>5}'.format('радова укупно', ukupno))
    print('  {:<22} {:>5}'.format('геолошких (geo)', geo))
    print('  {:<22} {:>5}'.format('осталих помена', ne_geo))

    nepoznati = sirocici(radovi, args.tacke)
    if nepoznati is None:
        print('Упозорење: {} не постоји — провера сирочића прескочена.'
              .format(args.tacke))
    elif nepoznati:
        print('УПОЗОРЕЊЕ: {} ogk_id-ева из жетве нема у {} (првих 10): {}'
              .format(len(nepoznati), args.tacke, ', '.join(nepoznati[:10])))
    else:
        print('  {:<22} {:>5}'.format('сирочића', 0))

    if args.dry_run:
        print('--dry-run: ниједан фајл није измењен.')
        return 0

    podaci = {
        'generisano': datetime.date.today().isoformat(),
        'izvor': IZVOR,
        'ukupno_lokaliteta': len(radovi),
        'ukupno_radova': ukupno,
        'radovi': radovi,
    }
    # Идемпотентно: ако се подаци нису променили, задржи затечени датум
    # генерисања да поновљено покретање остави фајл бајт-идентичним.
    zatecen = _procitaj_zatecen(args.output)
    if zatecen is not None:
        uporedi = dict(podaci)
        uporedi['generisano'] = zatecen.get('generisano')
        if uporedi == zatecen:
            podaci['generisano'] = zatecen.get('generisano')
    with open(args.output, 'w', encoding='utf-8') as handle:
        json.dump(podaci, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    print('Уписано: {} ({} локалитета, {} радова)'
          .format(args.output, len(radovi), ukupno))
    return 0


if __name__ == '__main__':
    sys.exit(main())
