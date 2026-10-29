#!/usr/bin/env python3
"""Увоз садржаја интерактивног уџбеника из JSON фајла у базу.

    python scripts/udzbenik_uvoz.py --fajl primer-minerali.json --dry-run
    python scripts/udzbenik_uvoz.py --fajl primer-minerali.json --execute mis_db --autor ko@nhmbeo.rs

Правила:
- цео фајл се ПРВО валидира (структура, ``sadrzaj`` свake лекције по
  udzbenik/schema/lekcija.schema.json, јединствени ``id`` блокова, постојање
  фотографија у Фототеци и примерака у збирци); све грешке се испишу одједном,
  са путањом (``poglavlja[1].lekcije[0].blokovi[3]``), и ништа се не упише;
- upsert по ``zbirka`` → ``slug`` поглавља → ``slug`` лекције; лекција чији се
  ``sadrzaj`` променио добија ``verzija + 1`` и нов ред у
  udzbenik_lekcija_verzija (``napomena = 'uvoz: <ime fajla>'``); непромењена
  лекција се не дира; поглавља/лекције којих има у бази а нема у фајлу се НЕ
  бришу — испише се упозорење;
- подразумевано је dry-run (испис плана, нула измена); ``--execute mis_db``
  (дословно) ради све у ЈЕДНОЈ трансакцији.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

SEMA_PUTANJA = REPO / 'udzbenik' / 'schema' / 'lekcija.schema.json'
POTVRDA = 'mis_db'
SLUG_RE = re.compile(r'^[a-z0-9][a-z0-9-]{1,59}$')
STATUSI = ('nacrt', 'objavljen')
TIPOVI = ('tekst', 'slika', 'scena', 'primerak', 'pitanje', 'napomena')


# --------------------------------------------------------------------------
# Валидација
# --------------------------------------------------------------------------

def ucitaj_semu():
    with open(SEMA_PUTANJA, encoding='utf-8') as f:
        return json.load(f)


def _tekst(vrednost, putanja, greske, obavezno=True, najvise=None):
    if vrednost is None or vrednost == '':
        if obavezno:
            greske.append(f'{putanja}: обавезно поље')
        return
    if not isinstance(vrednost, str):
        greske.append(f'{putanja}: мора бити текст')
    elif najvise and len(vrednost) > najvise:
        greske.append(f'{putanja}: дуже од {najvise} знакова')


def _slug(vrednost, putanja, greske):
    if not isinstance(vrednost, str) or not SLUG_RE.match(vrednost):
        greske.append(f'{putanja}: slug мора бити по образцу ^[a-z0-9][a-z0-9-]{{1,59}}$ (добијено {vrednost!r})')


def _redosled(vrednost, putanja, greske):
    if isinstance(vrednost, bool) or not isinstance(vrednost, int) or vrednost < 1:
        greske.append(f'{putanja}: redosled мора бити цео број ≥ 1')


def _status(vrednost, putanja, greske):
    if vrednost is not None and vrednost not in STATUSI:
        greske.append(f'{putanja}: status мора бити један од {list(STATUSI)}')


def _jedinstveno(stavke, kljuc, putanja, greske, naziv):
    videno = {}
    for i, stavka in enumerate(stavke):
        v = stavka.get(kljuc) if isinstance(stavka, dict) else None
        if v is None:
            continue
        if v in videno:
            greske.append(f'{putanja}[{i}].{kljuc}: {naziv} {v!r} понавља се (први пут у {putanja}[{videno[v]}])')
        else:
            videno[v] = i


def _json_putanja(greska):
    """``$.parametri.sistem`` → ``.parametri.sistem``; корен → ''."""
    p = greska.json_path
    return p[1:] if p.startswith('$') else p


def validiraj_sadrzaj(sadrzaj, putanja, sema, validatori, greske):
    """Садржај лекције по шеми: корен + сваки блок посебно (јасније поруке од
    oneOf), јединствени ``id`` блокова."""
    import jsonschema

    koren = {
        'type': 'object', 'required': ['verzija', 'blokovi'], 'additionalProperties': False,
        'properties': {'verzija': sema['properties']['verzija'],
                       'blokovi': {'type': 'array', 'minItems': 1}},
    }
    pre = len(greske)
    for g in sorted(jsonschema.Draft202012Validator(koren).iter_errors(sadrzaj), key=str):
        greske.append(f'{putanja}{_json_putanja(g)}: {g.message}')
    if len(greske) > pre:
        return
    ids = {}
    for i, blok in enumerate(sadrzaj['blokovi']):
        p = f'{putanja}.blokovi[{i}]'
        if not isinstance(blok, dict):
            greske.append(f'{p}: блок мора бити објекат')
            continue
        tip = blok.get('tip')
        if tip not in TIPOVI:
            greske.append(f'{p}.tip: непознат тип блока {tip!r}; дозвољено {list(TIPOVI)}')
            continue
        for g in sorted(validatori[tip].iter_errors(blok), key=lambda e: (str(e.json_path), e.message)):
            greske.append(f'{p}{_json_putanja(g)}: {g.message}')
        bid = blok.get('id')
        if isinstance(bid, str):
            if bid in ids:
                greske.append(f'{p}.id: id блока {bid!r} понавља се (први пут у {putanja}.blokovi[{ids[bid]}])')
            else:
                ids[bid] = i


def _validatori(sema):
    import jsonschema

    return {tip: jsonschema.Draft202012Validator({'$ref': f'#/$defs/{tip}', '$defs': sema['$defs']})
            for tip in TIPOVI}


def validiraj(podaci, cur):
    """Листа грешака (празна = фајл исправан). Провере постојања у бази иду
    кроз ``cur`` (фотографије) и museum_qr (примерци)."""
    greske = []
    if not isinstance(podaci, dict):
        return ['(корен): фајл мора бити JSON објекат']
    u = podaci.get('udzbenik')
    if not isinstance(u, dict):
        greske.append('udzbenik: обавезан објекат')
    else:
        _tekst(u.get('zbirka'), 'udzbenik.zbirka', greske)
        _tekst(u.get('naslov'), 'udzbenik.naslov', greske)
        _tekst(u.get('opis'), 'udzbenik.opis', greske, obavezno=False)
        _status(u.get('status'), 'udzbenik.status', greske)
        if 'javno' in u and not isinstance(u['javno'], bool):
            greske.append('udzbenik.javno: мора бити true/false')
    poglavlja = podaci.get('poglavlja')
    if not isinstance(poglavlja, list) or not poglavlja:
        greske.append('poglavlja: обавезна непразна листа')
        return greske

    sema = ucitaj_semu()
    validatori = _validatori(sema)
    _jedinstveno(poglavlja, 'slug', 'poglavlja', greske, 'slug поглавља')
    _jedinstveno(poglavlja, 'redosled', 'poglavlja', greske, 'redosled поглавља')
    for i, p in enumerate(poglavlja):
        pp = f'poglavlja[{i}]'
        if not isinstance(p, dict):
            greske.append(f'{pp}: поглавље мора бити објекат')
            continue
        _slug(p.get('slug'), f'{pp}.slug', greske)
        _tekst(p.get('naslov'), f'{pp}.naslov', greske)
        _tekst(p.get('opis'), f'{pp}.opis', greske, obavezno=False)
        _redosled(p.get('redosled'), f'{pp}.redosled', greske)
        lekcije = p.get('lekcije')
        if not isinstance(lekcije, list) or not lekcije:
            greske.append(f'{pp}.lekcije: обавезна непразна листа')
            continue
        _jedinstveno(lekcije, 'slug', f'{pp}.lekcije', greske, 'slug лекције')
        _jedinstveno(lekcije, 'redosled', f'{pp}.lekcije', greske, 'redosled лекције')
        for j, lek in enumerate(lekcije):
            lp = f'{pp}.lekcije[{j}]'
            if not isinstance(lek, dict):
                greske.append(f'{lp}: лекција мора бити објекат')
                continue
            _slug(lek.get('slug'), f'{lp}.slug', greske)
            _tekst(lek.get('naslov'), f'{lp}.naslov', greske)
            _tekst(lek.get('sazetak'), f'{lp}.sazetak', greske, obavezno=False)
            _redosled(lek.get('redosled'), f'{lp}.redosled', greske)
            _status(lek.get('status'), f'{lp}.status', greske)
            sadrzaj = lek.get('sadrzaj')
            if not isinstance(sadrzaj, dict):
                greske.append(f'{lp}.sadrzaj: обавезан објекат по lekcija.schema.json')
                continue
            validiraj_sadrzaj(sadrzaj, f'{lp}.sadrzaj', sema, validatori, greske)
            if isinstance(sadrzaj.get('blokovi'), list):
                _proveri_reference(sadrzaj['blokovi'], f'{lp}.sadrzaj', cur, greske)
    return greske


def _proveri_reference(blokovi, putanja, cur, greske):
    """Постојање у бази — све грешке одједном, па се проверава и кад шема
    пријави нешто друго; блок без исправног id референце је већ пријављен."""
    for i, blok in enumerate(blokovi):
        if not isinstance(blok, dict):
            continue
        p = f'{putanja}.blokovi[{i}]'
        if blok.get('tip') == 'slika' and _ceo(blok.get('fotografija_id')):
            cur.execute('SELECT 1 FROM fotografije WHERE id = %s AND obrisana = FALSE', (blok['fotografija_id'],))
            if cur.fetchone() is None:
                greske.append(f'{p}.fotografija_id: фотографија {blok["fotografija_id"]} не постоји у Фототеци')
        elif blok.get('tip') == 'primerak' and _ceo(blok.get('objekat_id')) and isinstance(blok.get('zbirka'), str):
            if not primerak_postoji(blok['zbirka'], blok['objekat_id']):
                greske.append(f'{p}.objekat_id: примерак {blok["zbirka"]}/{blok["objekat_id"]} не постоји')


def _ceo(vrednost):
    return isinstance(vrednost, int) and not isinstance(vrednost, bool) and vrednost >= 1


def primerak_postoji(zbirka, objekat_id):
    import museum_qr

    try:
        return museum_qr.dohvati_zapis(zbirka, objekat_id) is not None
    except Exception as exc:  # noqa: BLE001 - пријави као грешку уноса, не руши увоз
        print(f'  ! провера примерка {zbirka}/{objekat_id} није успела: {exc}', file=sys.stderr)
        return False


# --------------------------------------------------------------------------
# План (чита базу, не пише)
# --------------------------------------------------------------------------

def _json(vrednost):
    return json.loads(vrednost) if isinstance(vrednost, (str, bytes)) else vrednost


def napravi_plan(cur, podaci):
    u = podaci['udzbenik']
    cur.execute('SELECT id, naslov, opis, status, javno FROM udzbenik WHERE zbirka = %s', (u['zbirka'],))
    red = cur.fetchone()
    plan = {'zbirka': u['zbirka'], 'upozorenja': [], 'poglavlja': []}
    if red is None:
        plan['udzbenik'] = {'akcija': 'dodaje', 'id': None}
    else:
        isto = (red[1] == u['naslov'] and red[2] == u.get('opis')
                and ('status' not in u or red[3] == u['status'])
                and ('javno' not in u or red[4] == u['javno']))
        plan['udzbenik'] = {'akcija': 'isto' if isto else 'menja', 'id': red[0]}

    postojeca_poglavlja = {}
    if red is not None:
        cur.execute('SELECT id, slug, naslov, opis, redosled FROM udzbenik_poglavlje WHERE udzbenik_id = %s', (red[0],))
        postojeca_poglavlja = {r[1]: {'id': r[0], 'naslov': r[2], 'opis': r[3], 'redosled': r[4]} for r in cur.fetchall()}

    for p in podaci['poglavlja']:
        staro = postojeca_poglavlja.get(p['slug'])
        stavka = {'slug': p['slug'], 'id': staro['id'] if staro else None, 'lekcije': []}
        if staro is None:
            stavka['akcija'] = 'dodaje'
        elif (staro['naslov'], staro['opis'], staro['redosled']) == (p['naslov'], p.get('opis'), p['redosled']):
            stavka['akcija'] = 'isto'
        else:
            stavka['akcija'] = 'menja'
        postojece_lekcije = {}
        if staro is not None:
            cur.execute("""SELECT id, slug, naslov, sazetak, redosled, status, verzija, sadrzaj
                           FROM udzbenik_lekcija WHERE poglavlje_id = %s""", (staro['id'],))
            postojece_lekcije = {r[1]: {'id': r[0], 'naslov': r[2], 'sazetak': r[3], 'redosled': r[4],
                                        'status': r[5], 'verzija': r[6], 'sadrzaj': _json(r[7])}
                                 for r in cur.fetchall()}
        for lek in p['lekcije']:
            stara = postojece_lekcije.get(lek['slug'])
            l_stavka = {'slug': lek['slug'], 'id': stara['id'] if stara else None, 'nova_verzija': None}
            if stara is None:
                l_stavka['akcija'] = 'dodaje'
                l_stavka['nova_verzija'] = 1
            else:
                sadrzaj_isti = stara['sadrzaj'] == lek['sadrzaj']
                podaci_isti = ((stara['naslov'], stara['sazetak'], stara['redosled']) ==
                               (lek['naslov'], lek.get('sazetak'), lek['redosled'])
                               and ('status' not in lek or stara['status'] == lek['status']))
                if not sadrzaj_isti:
                    l_stavka['akcija'] = 'menja sadrzaj'
                    l_stavka['nova_verzija'] = stara['verzija'] + 1
                elif not podaci_isti:
                    l_stavka['akcija'] = 'menja podatke'
                else:
                    l_stavka['akcija'] = 'isto'
            stavka['lekcije'].append(l_stavka)
        for slug in sorted(set(postojece_lekcije) - {lek['slug'] for lek in p['lekcije']}):
            plan['upozorenja'].append(f'лекција {p["slug"]}/{slug} је у бази, а нема је у фајлу — остаје нетакнута')
        plan['poglavlja'].append(stavka)
    for slug in sorted(set(postojeca_poglavlja) - {p['slug'] for p in podaci['poglavlja']}):
        plan['upozorenja'].append(f'поглавље {slug} је у бази, а нема га у фајлу — остаје нетакнуто')
    return plan


# --------------------------------------------------------------------------
# Примена (само уз --execute, у трансакцији позиваоца)
# --------------------------------------------------------------------------

def primeni_plan(cur, podaci, plan, autor, napomena):
    u = podaci['udzbenik']
    if plan['udzbenik']['akcija'] == 'dodaje':
        cur.execute("""INSERT INTO udzbenik (zbirka, naslov, opis, status, javno, autor_email)
                       VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
                    (u['zbirka'], u['naslov'], u.get('opis'), u.get('status', 'nacrt'),
                     u.get('javno', False), autor))
        udzbenik_id = cur.fetchone()[0]
    else:
        udzbenik_id = plan['udzbenik']['id']
        if plan['udzbenik']['akcija'] == 'menja':
            cur.execute("""UPDATE udzbenik SET naslov = %s, opis = %s,
                               status = COALESCE(%s, status), javno = COALESCE(%s, javno), updated_at = now()
                           WHERE id = %s""",
                        (u['naslov'], u.get('opis'), u.get('status'), u.get('javno'), udzbenik_id))

    # Редослед је UNIQUE: постојећа поглавља/лекције из фајла прво добијају
    # привремен негативан redosled да размена места не удари у ограничење.
    postojeca = [s['id'] for s in plan['poglavlja'] if s['id'] is not None]
    if postojeca:
        cur.execute('UPDATE udzbenik_poglavlje SET redosled = -id WHERE id = ANY(%s)', (postojeca,))

    for p, stavka in zip(podaci['poglavlja'], plan['poglavlja']):
        if stavka['akcija'] == 'dodaje':
            cur.execute("""INSERT INTO udzbenik_poglavlje (udzbenik_id, redosled, slug, naslov, opis)
                           VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                        (udzbenik_id, p['redosled'], p['slug'], p['naslov'], p.get('opis')))
            poglavlje_id = cur.fetchone()[0]
        else:
            poglavlje_id = stavka['id']
            cur.execute('UPDATE udzbenik_poglavlje SET redosled = %s, naslov = %s, opis = %s WHERE id = %s',
                        (p['redosled'], p['naslov'], p.get('opis'), poglavlje_id))
        postojece = [lek['id'] for lek in stavka['lekcije'] if lek['id'] is not None]
        if postojece:
            cur.execute('UPDATE udzbenik_lekcija SET redosled = -id WHERE id = ANY(%s)', (postojece,))
        for lek, l_stavka in zip(p['lekcije'], stavka['lekcije']):
            sadrzaj = json.dumps(lek['sadrzaj'], ensure_ascii=False)
            if l_stavka['akcija'] == 'dodaje':
                cur.execute("""INSERT INTO udzbenik_lekcija (poglavlje_id, redosled, slug, naslov, sazetak,
                                   sadrzaj, verzija, status, azurirao_email)
                               VALUES (%s, %s, %s, %s, %s, %s, 1, %s, %s) RETURNING id""",
                            (poglavlje_id, lek['redosled'], lek['slug'], lek['naslov'], lek.get('sazetak'),
                             sadrzaj, lek.get('status', 'nacrt'), autor))
                lekcija_id = cur.fetchone()[0]
                _upisi_verziju(cur, lekcija_id, 1, sadrzaj, autor, napomena)
                continue
            lekcija_id = l_stavka['id']
            if l_stavka['akcija'] == 'menja sadrzaj':
                cur.execute("""UPDATE udzbenik_lekcija SET redosled = %s, naslov = %s, sazetak = %s,
                                   status = COALESCE(%s, status), sadrzaj = %s, verzija = %s,
                                   azurirao_email = %s, updated_at = now()
                               WHERE id = %s""",
                            (lek['redosled'], lek['naslov'], lek.get('sazetak'), lek.get('status'),
                             sadrzaj, l_stavka['nova_verzija'], autor, lekcija_id))
                _upisi_verziju(cur, lekcija_id, l_stavka['nova_verzija'], sadrzaj, autor, napomena)
            else:
                # 'isto' такође пролази овде само да врати привремени redosled
                cur.execute("""UPDATE udzbenik_lekcija SET redosled = %s, naslov = %s, sazetak = %s,
                                   status = COALESCE(%s, status),
                                   updated_at = CASE WHEN %s THEN now() ELSE updated_at END
                               WHERE id = %s""",
                            (lek['redosled'], lek['naslov'], lek.get('sazetak'), lek.get('status'),
                             l_stavka['akcija'] == 'menja podatke', lekcija_id))


def _upisi_verziju(cur, lekcija_id, verzija, sadrzaj, autor, napomena):
    cur.execute("""INSERT INTO udzbenik_lekcija_verzija (lekcija_id, verzija, sadrzaj, autor_email, napomena)
                   VALUES (%s, %s, %s, %s, %s)""", (lekcija_id, verzija, sadrzaj, autor, napomena))


# --------------------------------------------------------------------------
# Испис
# --------------------------------------------------------------------------

ZNAK = {'dodaje': '+', 'menja': '~', 'menja sadrzaj': '~', 'menja podatke': '~', 'isto': '='}


def ispisi_plan(plan, izvrsavanje):
    glagol = 'Урађено' if izvrsavanje else 'План (dry-run, ништа није уписано)'
    print(f'{glagol} за уџбеник „{plan["zbirka"]}“:')
    print(f'  {ZNAK[plan["udzbenik"]["akcija"]]} udzbenik {plan["zbirka"]} ({plan["udzbenik"]["akcija"]})')
    brojac = {'poglavlja': 0, 'lekcije': 0, 'nove_verzije': 0}
    for p in plan['poglavlja']:
        brojac['poglavlja'] += 1
        print(f'  {ZNAK[p["akcija"]]} poglavlje {p["slug"]} ({p["akcija"]})')
        for lek in p['lekcije']:
            brojac['lekcije'] += 1
            dodatak = f' → verzija {lek["nova_verzija"]}' if lek['nova_verzija'] else ''
            if lek['nova_verzija']:
                brojac['nove_verzije'] += 1
            print(f'      {ZNAK[lek["akcija"]]} lekcija {p["slug"]}/{lek["slug"]} ({lek["akcija"]}{dodatak})')
    for u in plan['upozorenja']:
        print(f'  ! упозорење: {u}')
    print(f'Укупно: {brojac["poglavlja"]} поглавља, {brojac["lekcije"]} лекција, '
          f'{brojac["nove_verzije"]} нових верзија, {len(plan["upozorenja"])} упозорења.')
    return brojac


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _argumenti(argv):
    p = argparse.ArgumentParser(description='Увоз садржаја уџбеника из JSON фајла (подразумевано dry-run).')
    p.add_argument('--fajl', required=True, help='JSON фајл са уџбеником, поглављима и лекцијама')
    p.add_argument('--dry-run', action='store_true', help='само испиши шта би било урађено (подразумевано)')
    p.add_argument('--execute', metavar='POTVRDA', help=f'стварно упиши; потврда мора бити дословно „{POTVRDA}“')
    p.add_argument('--autor', default=None, help='e-mail аутора за udzbenik.autor_email / verzija.autor_email')
    return p.parse_args(argv)


def main(argv=None):
    arg = _argumenti(argv)
    if arg.execute is not None and arg.execute != POTVRDA:
        print(f'ГРЕШКА: --execute тражи дословно „{POTVRDA}“ (добијено {arg.execute!r}).', file=sys.stderr)
        return 2
    izvrsavanje = arg.execute == POTVRDA
    try:
        with open(arg.fajl, encoding='utf-8') as f:
            podaci = json.load(f)
    except (OSError, ValueError) as exc:
        print(f'ГРЕШКА: фајл се не може прочитати као JSON: {exc}', file=sys.stderr)
        return 2
    napomena = f'uvoz: {os.path.basename(arg.fajl)}'

    from postgres_service import get_postgres_connection

    with get_postgres_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute('SELECT current_database()')
                print(f'База: {cur.fetchone()[0]}  фајл: {arg.fajl}  режим: {"EXECUTE" if izvrsavanje else "dry-run"}')
                greske = validiraj(podaci, cur)
                if greske:
                    print(f'ГРЕШКЕ У ФАЈЛУ ({len(greske)}) — ништа није уписано:', file=sys.stderr)
                    for g in greske:
                        print(f'  - {g}', file=sys.stderr)
                    conn.rollback()
                    return 1
                plan = napravi_plan(cur, podaci)
                if izvrsavanje:
                    primeni_plan(cur, podaci, plan, arg.autor, napomena)
            if izvrsavanje:
                conn.commit()
            else:
                conn.rollback()
        except Exception:
            conn.rollback()
            raise
    ispisi_plan(plan, izvrsavanje)
    return 0


if __name__ == '__main__':
    sys.exit(main())
