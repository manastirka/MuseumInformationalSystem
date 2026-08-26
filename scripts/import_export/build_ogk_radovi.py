#!/usr/bin/env python3
"""Build data/ogk_radovi.json from the online harvest of papers per OGK point.

Source (read-only CIFS mount, never written to):
    /mnt/licno/OGK_Srbija_podaci/04_harvest_online/radovi/lokaliteti/<OGK_ID>/dosije.json

The harvest was run by locality NAME, so it is full of misses: a paper about
the Senj town choir hangs on „Сењ јурски кречњак“. Nothing is dropped, but each
paper carries the judgement passed on it in ``data/ogk_radovi_ocene.json``
(``potvrdjen`` / ``verovatan`` / ``nesigurno`` / ``nije``, with the reason), so
the map popup can show the ones that really belong to the locality first and
fold the rest away.

That judgement is the ONLY measure of relevance here. The keyword regex this
script used to carry was a second, parallel source of truth for the same
question — it disagreed with the model on 527 of 2203 papers — and it is gone;
the paper without a judgement gets ``neoceneno``, never ``nije``.

The abstract itself is NOT written to the output (it would multiply the file
size several times over).

The script is idempotent: the same inputs always produce the same JSON, and
--dry-run only prints the counts without touching the disk.
"""
import argparse
import datetime
import json
import os
import sys
import unicodedata

OGK_ROOT = '/mnt/licno/OGK_Srbija_podaci'
RADOVI_DIR = os.path.join(OGK_ROOT, '04_harvest_online', 'radovi')
LOKALITETI_DIR = os.path.join(RADOVI_DIR, 'lokaliteti')

OUTPUT_PATH = os.path.join('data', 'ogk_radovi.json')
TACKE_PATH = os.path.join('data', 'ogk_points.json')
OCENE_PATH = os.path.join('data', 'ogk_radovi_ocene.json')
IZVOR = 'OGK harvest online 04_harvest_online/radovi'

NEOCENJEN = 'neoceneno'
# Редослед у поповеру и у самом фајлу: потврђено горе, неповезано на дно.
# `neoceneno` стоји ИЗНАД `nije` — рад који нико није судио није исто што и
# рад који је осуђен, и не сме да склизне у исту корпу.
REDOSLED_OCENA = ('potvrdjen', 'verovatan', 'nesigurno', NEOCENJEN, 'nije')
_RANG_OCENE = {ocena: i for i, ocena in enumerate(REDOSLED_OCENA)}

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


class NeslaganjeNaslova(Exception):
    """Оцена и жетва се разилазе — спајање по редном броју више не важи."""


def _godina(vrednost):
    """Return int ili None — рад без године иде на крај своје групе."""
    try:
        return int(vrednost)
    except (TypeError, ValueError):
        return None


def _kljuc_sortiranja(rad):
    # Прво по оцени, па новије горе, па по наслову. Рад без године иде на крај
    # своје групе — зато засебна застава испред саме године.
    godina = rad['godina']
    return (
        _RANG_OCENE.get(rad['ocena'], len(REDOSLED_OCENA)),
        1 if godina is None else 0,
        -(godina or 0),
        _normalizuj(rad['naslov']),
    )


def _procitaj_dosije(putanja):
    with open(putanja, encoding='utf-8') as handle:
        return json.load(handle)


def ucitaj_ocene(putanja):
    """Return (ocene_po_lokalitetu, meta) iz data/ogk_radovi_ocene.json.

    Фајл који недостаје није тиха нула: без њега би сваки рад испао
    ``neoceneno``, па се посао прекида.
    """
    if not os.path.exists(putanja):
        raise NeslaganjeNaslova(
            'нема {} — покрени scripts/tekst/oceni_radove_ogk.py --saberi'
            .format(putanja))
    with open(putanja, encoding='utf-8') as handle:
        podaci = json.load(handle)
    ocene = podaci.get('ocene')
    if not isinstance(ocene, dict) or not ocene:
        raise NeslaganjeNaslova('{} нема мапу „ocene“'.format(putanja))
    return ocene, podaci


def _po_rednom_broju(spisak_ocena):
    """Return {br: stavka} — дупли редни број је грешка, не последњи побеђује."""
    mapa = {}
    for stavka in spisak_ocena or []:
        br = stavka.get('br')
        if br in mapa:
            raise NeslaganjeNaslova('двапут оцењен редни број {}'.format(br))
        mapa[br] = stavka
    return mapa


def _uskladi_ocenu(ogk_id, redni_broj, rad, stavka):
    """Return (ocena, razlog) za jedan rad; neslaganje naslova je glasna greška.

    Спајање иде по редном броју у низу ``radovi`` из dosije.json. Ако се
    жетва у међувремену померила, редни број показује на туђи рад — то се
    хвата поређењем наслова и прекида посао, никад тихо не прескаче.
    """
    if stavka is None:
        return NEOCENJEN, ''
    ocenjen = _normalizuj(stavka.get('naslov'))
    stvarni = _normalizuj(rad.get('title'))
    if ocenjen != stvarni:
        raise NeslaganjeNaslova(
            '{} рад {}: оцена носи наслов „{}“, а жетва „{}“ — '
            'редни бројеви се више не поклапају'
            .format(ogk_id, redni_broj, (stavka.get('naslov') or '').strip(),
                    (rad.get('title') or '').strip()))
    return stavka.get('ocena') or NEOCENJEN, (stavka.get('razlog') or '').strip()


def izgradi_radove(ocene_po_lokalitetu):
    """Return (radovi_po_lokalitetu, ukupno_radova, brojac_ocena)."""
    radovi = {}
    ukupno = 0
    brojac = dict.fromkeys(REDOSLED_OCENA, 0)

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

        po_broju = _po_rednom_broju(ocene_po_lokalitetu.get(ogk_id))
        spisak = []
        for redni_broj, rad in enumerate(sirovi, 1):
            ocena, razlog = _uskladi_ocenu(ogk_id, redni_broj, rad,
                                           po_broju.get(redni_broj))
            brojac[ocena] = brojac.get(ocena, 0) + 1
            ukupno += 1
            spisak.append({
                'naslov': (rad.get('title') or '').strip(),
                'godina': _godina(rad.get('year')),
                'autori': (rad.get('authors') or '').strip(),
                'casopis': (rad.get('journal') or '').strip(),
                'doi': (rad.get('doi') or '').strip(),
                'url': (rad.get('url') or '').strip(),
                'pdf_url': (rad.get('pdf_url') or '').strip(),
                'ocena': ocena,
                'razlog': razlog,
            })

        spisak.sort(key=_kljuc_sortiranja)
        radovi[ogk_id] = spisak

    return radovi, ukupno, brojac


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


def promena_strane(zatecen, radovi):
    """Return (laznih, promasenih) u odnosu na stari regeks `geo`, ili None.

    Стари фајл је једини преостали запис регекса — сам регекс је избачен из
    скрипте да не буде други извор истине. Кад се једном препише, поређење
    више нема са чим да се ради и извештај се тихо гаси; зато мора да буде
    испричан гласно на пролазу који мења страну.
    """
    if not isinstance(zatecen, dict):
        return None
    stari = zatecen.get('radovi')
    if not isinstance(stari, dict):
        return None
    lazni = promaseni = 0
    imao_geo = False
    for ogk_id, spisak in radovi.items():
        po_naslovu = {}
        for rad in stari.get(ogk_id) or []:
            if 'geo' in rad:
                imao_geo = True
                po_naslovu[_normalizuj(rad.get('naslov'))] = bool(rad['geo'])
        for rad in spisak:
            bio_geo = po_naslovu.get(_normalizuj(rad['naslov']))
            if bio_geo is None:
                continue
            if bio_geo and rad['ocena'] == 'nije':
                lazni += 1
            elif not bio_geo and rad['ocena'] in ('potvrdjen', 'verovatan'):
                promaseni += 1
    return (lazni, promaseni) if imao_geo else None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true',
                        help='само испиши бројеве, ништа не уписуј')
    parser.add_argument('--output', default=OUTPUT_PATH,
                        help='путања излазног JSON-а (подразумевано %(default)s)')
    parser.add_argument('--tacke', default=TACKE_PATH,
                        help='путања до ogk_points.json ради провере сирочића')
    parser.add_argument('--ocene', default=OCENE_PATH,
                        help='путања до оцена радова (подразумевано %(default)s)')
    args = parser.parse_args(argv)

    # Извор је CIFS са прода: ако није монтиран, боље ненулти излаз него
    # тихо уписан празан фајл преко исправних података.
    if not os.path.isdir(LOKALITETI_DIR):
        print('ГРЕШКА: извор није доступан: {}\n'
              'Монтирај дељење пре покретања — ништа није уписано.'
              .format(LOKALITETI_DIR), file=sys.stderr)
        return 2

    try:
        ocene_po_lokalitetu, meta_ocena = ucitaj_ocene(args.ocene)
        radovi, ukupno, brojac = izgradi_radove(ocene_po_lokalitetu)
    except NeslaganjeNaslova as greska:
        print('ГРЕШКА: {}'.format(greska), file=sys.stderr)
        return 4
    if not radovi:
        print('ГРЕШКА: извор је доступан али нема ниједног рада — '
              'ништа није уписано.', file=sys.stderr)
        return 3

    potvrdjenih = brojac.get('potvrdjen', 0)
    sa_potvrdom = sum(
        1 for spisak in radovi.values()
        if any(rad['ocena'] in ('potvrdjen', 'verovatan') for rad in spisak))

    print('  {:<24} {:>5}'.format('локалитета са радом', len(radovi)))
    print('  {:<24} {:>5}'.format('радова укупно', ukupno))
    for ocena in REDOSLED_OCENA:
        print('  {:<24} {:>5}'.format(ocena, brojac.get(ocena, 0)))
    print('  {:<24} {:>5}'.format('локалитета са потврдом', sa_potvrdom))

    nepoznati = sirocici(radovi, args.tacke)
    if nepoznati is None:
        print('Упозорење: {} не постоји — провера сирочића прескочена.'
              .format(args.tacke))
    elif nepoznati:
        print('УПОЗОРЕЊЕ: {} ogk_id-ева из жетве нема у {} (првих 10): {}'
              .format(len(nepoznati), args.tacke, ', '.join(nepoznati[:10])))
    else:
        print('  {:<24} {:>5}'.format('сирочића', 0))

    zatecen = _procitaj_zatecen(args.output)
    razlika = promena_strane(zatecen, radovi)
    if razlika is not None:
        lazni, promaseni = razlika
        print('Промена стране у односу на стари регекс „geo“: '
              '{} лажних поготака (geo → nije), {} промашених '
              '(не-geo → potvrdjen/verovatan).'.format(lazni, promaseni))

    if args.dry_run:
        print('--dry-run: ниједан фајл није измењен.')
        return 0

    podaci = {
        'generisano': datetime.date.today().isoformat(),
        'izvor': IZVOR,
        'ocene_iz': os.path.basename(args.ocene),
        'ukupno_lokaliteta': len(radovi),
        'ukupno_radova': ukupno,
        'raspodela': {ocena: brojac.get(ocena, 0) for ocena in REDOSLED_OCENA},
        'ukupno_potvrdjenih': potvrdjenih,
        'radovi': radovi,
    }
    # Идемпотентно: ако се подаци нису променили, задржи затечени датум
    # генерисања да поновљено покретање остави фајл бајт-идентичним.
    if zatecen is not None:
        uporedi = dict(podaci)
        uporedi['generisano'] = zatecen.get('generisano')
        if uporedi == zatecen:
            podaci['generisano'] = zatecen.get('generisano')
    with open(args.output, 'w', encoding='utf-8') as handle:
        json.dump(podaci, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    print('Уписано: {} ({} локалитета, {} радова, {} потврђених)'
          .format(args.output, len(radovi), ukupno, potvrdjenih))
    return 0


if __name__ == '__main__':
    sys.exit(main())
