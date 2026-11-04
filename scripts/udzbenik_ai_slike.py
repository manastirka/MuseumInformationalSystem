#!/usr/bin/env python3
"""AI илустрације геолошких процеса → Фототека → блокови ``slika`` у лекцијама.

    python scripts/udzbenik_ai_slike.py --mapa ai-slike-mapa.json --slike DIR --dry-run
    python scripts/udzbenik_ai_slike.py --mapa ai-slike-mapa.json --slike DIR \\
        --execute museum_system --autor ko@nhmbeo.rs

Мапа је JSON листа ``{slika, lekcija, posle_bloka, potpis, alt}``; ``slika`` је
име фајла без наставка у директоријуму ``--slike``. Правила:

- **Фототека**: свака слика улази кроз исти пут као упload/batch увоз
  (``fototeka_views._intake_photo_from_path``: провера слике, RAW write-once,
  ред за деривате) — никад директним уписом фајла. Слика није везана ни за
  један примерак и одмах је скинута са пријемног реда (намерно самостална).
  Порекло („AI ilustracija, šematski“) и алат („Gemini (Antigravity)“) иду у
  ``opis`` уз ``alt`` (колона ``poreklo`` је технички CHECK upload/import) и у
  тагове;
- **идемпотентно по sha256**: слика чији sha256 већ постоји у Фототеци се не
  увози поново — користи се постојећи ``fotografije.id`` (обрисана = грешка);
- **лекције**: свака лекција из мапе добија ЈЕДНУ нову верзију кроз исти
  механизам као scripts/udzbenik_uvoz.py (``verzija + 1`` + ред у
  udzbenik_lekcija_verzija, ``napomena = 'ai-slike: <мапа>'``); блок
  ``{"id": "ai-<slika ascii>", "tip": "slika", ...}`` иде одмах после блока
  ``posle_bloka`` (више слика на истом месту — редослед из мапе); блок чији
  ``id`` већ постоји се прескаче; лекција без иједног новог блока се не дира;
- ``posle_bloka`` који не постоји је ГРЕШКА за ту лекцију; све грешке се
  испишу одједном и ништа се не упише (ни у базу ни на диск);
- ``lekcija`` у мапи сме да носи префикс редоследа (``03-sedimentni-...`` за
  лекцију ``sedimentni-...`` са ``redosled = 3``) — разрешава се по slug-у
  унутар уџбеника ``--zbirka``, никад по id-у, па иста мапа важи и на
  продукцији;
- подразумевано је dry-run; ``--execute <ime baze>`` мора да буде дословно име
  базе на коју је скрипта повезана (``current_database()``) и ради све у
  ЈЕДНОЈ трансакцији; пад после постављања RAW фајлова уклања баш те фајлове.
"""
import argparse
import importlib.util
import json
import os
import re
import shutil
import sys
import unicodedata
import uuid
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from udzbenik import ucitaj_semu  # noqa: E402

POREKLO_TEKST = 'AI ilustracija, šematski'
ALAT_TEKST = 'Gemini (Antigravity)'
TAGOVI = ('ai-ilustracija', 'udzbenik')
POREKLO_BLOKA = 'ai-ilustracija'
SIRINA_BLOKA = 'puna'
PREFIKS_ID = 'ai-'
NASTAVCI = ('.png', '.jpg', '.jpeg', '.webp')
OBAVEZNA_POLJA = ('slika', 'lekcija', 'posle_bloka', 'potpis', 'alt')
PREFIKS_REDOSLEDA = re.compile(r'^(\d{1,2})-(.+)$')
ZBIRKA = 'minerali'


def _uvoz():
    """scripts/udzbenik_uvoz.py — иста валидација садржаја и исти упис верзије."""
    spec = importlib.util.spec_from_file_location('udzbenik_uvoz', Path(__file__).resolve().parent / 'udzbenik_uvoz.py')
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def ascii_id(ime):
    """``rečni-placer`` → ``recni-placer``: NFKD без дијакритика, đ → dj."""
    tekst = str(ime).replace('đ', 'dj').replace('Đ', 'dj')
    tekst = unicodedata.normalize('NFKD', tekst)
    tekst = ''.join(ch for ch in tekst if not unicodedata.combining(ch))
    return tekst.encode('ascii', 'ignore').decode().lower()


def id_bloka(slika):
    return PREFIKS_ID + ascii_id(slika)


def opis_fotografije(alt):
    return f'{alt}\nPoreklo: {POREKLO_TEKST}. Alat: {ALAT_TEKST}.'


def _json(vrednost):
    return json.loads(vrednost) if isinstance(vrednost, (str, bytes)) else vrednost


# --------------------------------------------------------------------------
# Мапа и фајлови
# --------------------------------------------------------------------------

def ucitaj_mapu(putanja):
    with open(putanja, encoding='utf-8') as f:
        return json.load(f)


def validiraj_mapu(mapa, slike_dir):
    """Облик мапе + постојање фајлова; враћа листу грешака (све одједном)."""
    greske = []
    if not isinstance(mapa, list) or not mapa:
        return ['мапа мора бити непразна JSON листа']
    videni_id = {}
    for i, stavka in enumerate(mapa):
        p = f'mapa[{i}]'
        if not isinstance(stavka, dict):
            greske.append(f'{p}: ставка мора бити објекат')
            continue
        for polje in OBAVEZNA_POLJA:
            v = stavka.get(polje)
            if not isinstance(v, str) or not v.strip():
                greske.append(f'{p}.{polje}: обавезан непразан текст')
        if not isinstance(stavka.get('slika'), str) or not stavka['slika'].strip():
            continue
        if nadji_fajl(slike_dir, stavka['slika']) is None:
            greske.append(f'{p}.slika: нема фајла {stavka["slika"]}{NASTAVCI[0]} у {slike_dir}')
        bid = id_bloka(stavka['slika'])
        if not re.match(r'^[a-z0-9][a-z0-9-]{1,39}$', bid):
            greske.append(f'{p}.slika: id блока {bid!r} није по шеми (^[a-z0-9][a-z0-9-]{{1,39}}$)')
        kljuc = (stavka.get('lekcija'), bid)
        if kljuc in videni_id:
            greske.append(f'{p}: слика {stavka["slika"]!r} у лекцији {stavka.get("lekcija")!r} понавља се '
                          f'(први пут у mapa[{videni_id[kljuc]}])')
        else:
            videni_id[kljuc] = i
    return greske


def nadji_fajl(slike_dir, slika):
    for nastavak in NASTAVCI:
        kandidat = Path(slike_dir) / f'{slika}{nastavak}'
        if kandidat.is_file():
            return kandidat
    return None


# --------------------------------------------------------------------------
# План (чита базу и диск, не пише)
# --------------------------------------------------------------------------

def _lekcije_udzbenika(cur, zbirka):
    cur.execute("""SELECT l.id, l.slug, l.redosled, l.verzija, l.sadrzaj, p.slug AS poglavlje
                   FROM udzbenik_lekcija l
                   JOIN udzbenik_poglavlje p ON p.id = l.poglavlje_id
                   JOIN udzbenik u ON u.id = p.udzbenik_id
                   WHERE u.zbirka = %s ORDER BY p.redosled, l.redosled""", (zbirka,))
    return [{'id': r[0], 'slug': r[1], 'redosled': r[2], 'verzija': r[3], 'sadrzaj': _json(r[4]),
             'poglavlje': r[5]} for r in cur.fetchall()]


def razresi_lekciju(lekcije, trazeni):
    """(лекција, грешка): тачан slug, или ``NN-slug`` где је NN = redosled."""
    po_slugu = [lek for lek in lekcije if lek['slug'] == trazeni]
    poklapanje = PREFIKS_REDOSLEDA.match(trazeni)
    if not po_slugu and poklapanje:
        redosled, slug = int(poklapanje.group(1)), poklapanje.group(2)
        po_slugu = [lek for lek in lekcije if lek['slug'] == slug]
        if po_slugu and not any(lek['redosled'] == redosled for lek in po_slugu):
            return None, (f'лекција {trazeni!r}: slug {slug!r} постоји, али му redosled није {redosled} '
                          f'(нађено {[lek["redosled"] for lek in po_slugu]})')
        po_slugu = [lek for lek in po_slugu if lek['redosled'] == redosled]
    if not po_slugu:
        return None, f'лекција {trazeni!r} не постоји у уџбенику'
    if len(po_slugu) > 1:
        return None, (f'лекција {trazeni!r} је двосмислена: '
                      f'{[lek["poglavlje"] + "/" + lek["slug"] for lek in po_slugu]}')
    return po_slugu[0], None


def _fotografija_po_sha(cur, sha256):
    cur.execute('SELECT id, obrisana FROM fotografije WHERE sha256 = %s', (sha256,))
    red = cur.fetchone()
    return (red[0], red[1]) if red else (None, None)


def napravi_plan(cur, mapa, slike_dir, zbirka):
    import fototeka_jobs

    uvoz = _uvoz()
    sema = ucitaj_semu()
    validatori = uvoz._validatori(sema)
    plan = {'zbirka': zbirka, 'slike': [], 'lekcije': [], 'greske': []}

    # 1. слике: sha256 → постојећи id или нова (иста датотека на два места = једна слика)
    po_sha = {}
    for i, stavka in enumerate(mapa):
        fajl = nadji_fajl(slike_dir, stavka['slika'])
        sha256 = fototeka_jobs.sha256_of_file(fajl)
        slika = po_sha.get(sha256)
        if slika is None:
            postojeci_id, obrisana = _fotografija_po_sha(cur, sha256)
            slika = {'slika': stavka['slika'], 'fajl': fajl, 'sha256': sha256, 'fotografija_id': postojeci_id,
                     'akcija': 'postoji' if postojeci_id else 'dodaje', 'alt': stavka['alt'],
                     'indeks': len(plan['slike'])}
            if obrisana:
                plan['greske'].append(f'mapa[{i}].slika: фотографија {postojeci_id} са истим sha256 постоји, '
                                      f'али је обрисана — врати је у Фототеци или промени слику')
            po_sha[sha256] = slika
            plan['slike'].append(slika)
        elif slika['slika'] != stavka['slika']:
            plan['greske'].append(f'mapa[{i}].slika: {stavka["slika"]!r} је иста датотека као '
                                  f'{slika["slika"]!r} (sha256) — једна слика, два имена')
        stavka['_slika'] = slika

    # 2. лекције: груписано по редоследу првог појављивања у мапи
    lekcije = _lekcije_udzbenika(cur, zbirka)
    if not lekcije:
        plan['greske'].append(f'уџбеник {zbirka!r} нема лекција у бази')
        return plan
    # Групише се по РАЗРЕШЕНОЈ лекцији (``01-slug`` и ``slug`` су иста лекција →
    # једна нова верзија), по редоследу првог појављивања у мапи.
    razreseno, grupe = {}, {}
    for stavka in mapa:
        trazeni = stavka['lekcija']
        if trazeni not in razreseno:
            razreseno[trazeni] = razresi_lekciju(lekcije, trazeni)
            if razreseno[trazeni][1]:
                plan['greske'].append(razreseno[trazeni][1])
        lek = razreseno[trazeni][0]
        if lek is not None:
            grupe.setdefault(lek['id'], (lek, trazeni, []))[2].append(stavka)
    for lek, trazeni, stavke in grupe.values():
        plan['lekcije'].append(_plan_lekcije(lek, trazeni, stavke, plan['greske'], uvoz, sema, validatori))
    return plan


def _plan_lekcije(lek, trazeni, stavke, greske, uvoz, sema, validatori):
    blokovi = lek['sadrzaj'].get('blokovi') or []
    ids = [b.get('id') for b in blokovi if isinstance(b, dict)]
    stavka_plana = {'trazeni': trazeni, 'id': lek['id'], 'slug': lek['slug'], 'poglavlje': lek['poglavlje'],
                    'verzija': lek['verzija'], 'nova_verzija': None, 'blokovi': [], 'preskoceni': [],
                    'greske': []}
    # Нови блок иде одмах после ``posle_bloka``; више слика на истом месту
    # прати редослед из мапе и при поновном покретању (слика која већ постоји
    # у лекцији постаје сидро за следећу из мапе, па исход не зависи од тога
    # да ли је мапа примењена одједном или у два наврата).
    novi_po_mestu, poslednji_postojeci = {}, {}
    for stavka in stavke:
        bid = id_bloka(stavka['slika'])
        mesto = stavka['posle_bloka']
        if bid in ids:
            stavka_plana['preskoceni'].append(bid)
            poslednji_postojeci[mesto] = bid
            continue
        if mesto not in ids:
            stavka_plana['greske'].append(f'блок {mesto!r} (posle_bloka за {stavka["slika"]!r}) '
                                          f'не постоји у лекцији {lek["poglavlje"]}/{lek["slug"]}')
            continue
        blok = {'id': bid, 'tip': 'slika', 'fotografija_id': stavka['_slika']['fotografija_id'],
                'potpis': stavka['potpis'], 'alt': stavka['alt'],
                'poreklo': POREKLO_BLOKA, 'sirina': SIRINA_BLOKA}
        novi_po_mestu.setdefault(poslednji_postojeci.get(mesto, mesto), []).append(blok)
        stavka_plana['blokovi'].append({'id': bid, 'posle_bloka': stavka['posle_bloka'], 'slika': stavka['_slika'],
                                        'blok': blok})
    if stavka_plana['greske']:
        greske.extend(stavka_plana['greske'])
        return stavka_plana
    if not stavka_plana['blokovi']:
        stavka_plana['akcija'] = 'isto'
        return stavka_plana
    novi_blokovi = []
    for blok in blokovi:
        novi_blokovi.append(blok)
        novi_blokovi.extend(novi_po_mestu.get(blok.get('id') if isinstance(blok, dict) else None, []))
    stavka_plana['sadrzaj'] = dict(lek['sadrzaj'], blokovi=novi_blokovi)
    stavka_plana['akcija'] = 'menja sadrzaj'
    stavka_plana['nova_verzija'] = lek['verzija'] + 1
    # Шема над целим новим садржајем — id нове фотографије још није познат у
    # dry-run-у, па се за проверу облика привремено стави 1.
    za_proveru = json.loads(json.dumps(stavka_plana['sadrzaj']))
    for blok in za_proveru['blokovi']:
        if blok.get('fotografija_id') is None and blok.get('poreklo') == POREKLO_BLOKA:
            blok['fotografija_id'] = 1
    pre = len(greske)
    uvoz.validiraj_sadrzaj(za_proveru, f'lekcija {lek["poglavlje"]}/{lek["slug"]}', sema, validatori, greske)
    stavka_plana['greske'] = greske[pre:]
    return stavka_plana


# --------------------------------------------------------------------------
# Примена (само уз --execute, у трансакцији позиваоца)
# --------------------------------------------------------------------------

def _uvezi_sliku(cur, slika, autor, temp_dir):
    """Кроз постојећи intake Фототеке; враћа (id, raw_putanja)."""
    import fototeka_views

    fajl = slika['fajl']
    temp_path = temp_dir / f'{uuid.uuid4().hex}_{fajl.suffix.lstrip(".")}'
    try:
        shutil.copy2(fajl, temp_path)
        fotografija_id, razlog = fototeka_views._intake_photo_from_path(
            cur, temp_path, fajl.name, fajl.stat().st_size, fajl.suffix.lower(),
            autor_email=autor, opis=opis_fotografije(slika['alt']), tags=list(TAGOVI),
            datum_override=None, veza=None, u_prijemnom_redu=False, poreklo='import')
    finally:
        if temp_path.exists():
            temp_path.unlink()
    if fotografija_id is None:
        raise RuntimeError(f'Фототека је одбила {fajl.name}: {razlog}')
    # Намерно самостална илустрација — не чека везу на пријемном реду (исто
    # што ради кустос преко „скини са реда“).
    cur.execute("""UPDATE fotografije SET sklonjena_sa_reda = TRUE, u_prijemnom_redu = FALSE, updated_at = now()
                   WHERE id = %s""", (fotografija_id,))
    cur.execute('SELECT raw_putanja FROM fotografije WHERE id = %s', (fotografija_id,))
    return fotografija_id, cur.fetchone()[0]


def primeni_plan(cur, plan, autor, napomena, postavljeni_raw):
    """Слике па лекције; ``postavljeni_raw`` пуни се RAW путањама да позивалац
    при паду уклони баш те фајлове."""
    import fototeka_jobs

    uvoz = _uvoz()
    temp_dir = fototeka_jobs.get_media_path() / 'temp'
    temp_dir.mkdir(parents=True, exist_ok=True)
    for slika in plan['slike']:
        if slika['akcija'] != 'dodaje':
            continue
        slika['fotografija_id'], raw_rel = _uvezi_sliku(cur, slika, autor, temp_dir)
        postavljeni_raw.append(fototeka_jobs.get_arhiva_path() / raw_rel)
    for lek in plan['lekcije']:
        if lek['akcija'] != 'menja sadrzaj':
            continue
        for stavka in lek['blokovi']:
            stavka['blok']['fotografija_id'] = stavka['slika']['fotografija_id']
        sadrzaj = json.dumps(lek['sadrzaj'], ensure_ascii=False)
        cur.execute("""UPDATE udzbenik_lekcija
                       SET sadrzaj = %s, verzija = %s, azurirao_email = %s, updated_at = now()
                       WHERE id = %s""", (sadrzaj, lek['nova_verzija'], autor, lek['id']))
        uvoz._upisi_verziju(cur, lek['id'], lek['nova_verzija'], sadrzaj, autor, napomena)


# --------------------------------------------------------------------------
# Испис
# --------------------------------------------------------------------------

def ispisi_plan(plan, izvrsavanje):
    glagol = 'Урађено' if izvrsavanje else 'План (dry-run, ништа није уписано)'
    print(f'{glagol} за уџбеник „{plan["zbirka"]}“:')
    print('Слике:')
    for s in plan['slike']:
        if s['akcija'] == 'dodaje':
            broj = f' → fotografija #{s["fotografija_id"]}' if izvrsavanje else ''
            print(f'  + {s["slika"]} ({s["fajl"].name}, sha256 {s["sha256"][:12]}…) увоз у Фототеку{broj}')
        else:
            print(f'  = {s["slika"]} већ у Фототеци као fotografija #{s["fotografija_id"]} (исти sha256)')
    print('Лекције:')
    for lek in plan['lekcije']:
        ime = f'{lek["poglavlje"]}/{lek["slug"]}'
        if lek['trazeni'] != lek['slug']:
            ime += f' (мапа: {lek["trazeni"]})'
        if lek['greske']:
            print(f'  ! {ime}: ГРЕШКА — остаје нетакнута')
            for g in lek['greske']:
                print(f'      - {g}')
            continue
        if lek['akcija'] == 'isto':
            print(f'  = {ime}: сви блокови већ постоје ({", ".join(lek["preskoceni"])}) — без нове верзије')
            continue
        print(f'  ~ {ime}: verzija {lek["verzija"]} → {lek["nova_verzija"]}, +{len(lek["blokovi"])} блок(ова)')
        for b in lek['blokovi']:
            foto_id = b['slika']['fotografija_id']
            foto = f'fotografija #{foto_id}' if foto_id else 'нова фотографија'
            print(f'      + {b["id"]} после {b["posle_bloka"]} ({foto})')
        for bid in lek['preskoceni']:
            print(f'      = {bid} већ постоји — прескочен')
    for g in plan['greske']:
        if not any(g in lek['greske'] for lek in plan['lekcije']):
            print(f'  ! {g}')
    nove_slike = sum(1 for s in plan['slike'] if s['akcija'] == 'dodaje')
    nove_verzije = sum(1 for lek in plan['lekcije'] if lek.get('akcija') == 'menja sadrzaj')
    print(f'Укупно: {len(plan["slike"])} слика ({nove_slike} нових), {len(plan["lekcije"])} лекција '
          f'({nove_verzije} нових верзија), {len(plan["greske"])} грешака.')


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _argumenti(argv):
    p = argparse.ArgumentParser(description='AI илустрације → Фототека → лекције уџбеника (подразумевано dry-run).')
    p.add_argument('--mapa', required=True, help='JSON листа {slika, lekcija, posle_bloka, potpis, alt}')
    p.add_argument('--slike', required=True, help='директоријум са <slika>.png')
    rezim = p.add_mutually_exclusive_group()
    rezim.add_argument('--dry-run', action='store_true', help='само испиши шта би било урађено (подразумевано)')
    rezim.add_argument('--execute', metavar='IME_BAZE', help='стварно упиши; потврда = име базе на коју је повезано')
    p.add_argument('--autor', required=True, help='e-mail аутора за fotografije.autor_email и verzija.autor_email')
    p.add_argument('--zbirka', default=ZBIRKA, help=f'уџбеник (zbirka) чије лекције мапа описује (default {ZBIRKA})')
    return p.parse_args(argv)


def main(argv=None):
    arg = _argumenti(argv)
    izvrsavanje = arg.execute is not None
    try:
        mapa = ucitaj_mapu(arg.mapa)
    except (OSError, ValueError) as exc:
        print(f'ГРЕШКА: мапа се не може прочитати као JSON: {exc}', file=sys.stderr)
        return 2
    greske = validiraj_mapu(mapa, arg.slike)
    if greske:
        print(f'ГРЕШКЕ У МАПИ ({len(greske)}) — ништа није уписано:', file=sys.stderr)
        for g in greske:
            print(f'  - {g}', file=sys.stderr)
        return 1
    napomena = f'ai-slike: {os.path.basename(arg.mapa)}'

    from postgres_service import get_postgres_connection

    postavljeni_raw = []
    with get_postgres_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute('SELECT current_database()')
                baza = cur.fetchone()[0]
                print(f'База: {baza}  мапа: {arg.mapa}  слике: {arg.slike}  '
                      f'режим: {"EXECUTE" if izvrsavanje else "dry-run"}')
                if izvrsavanje and arg.execute != baza:
                    print(f'ГРЕШКА: --execute тражи дословно име базе „{baza}“ (добијено {arg.execute!r}).',
                          file=sys.stderr)
                    conn.rollback()
                    return 2
                plan = napravi_plan(cur, mapa, arg.slike, arg.zbirka)
                if plan['greske']:
                    ispisi_plan(plan, False)
                    print(f'ГРЕШКЕ ({len(plan["greske"])}) — ништа није уписано.', file=sys.stderr)
                    conn.rollback()
                    return 1
                if not izvrsavanje:
                    ispisi_plan(plan, False)
                    conn.rollback()
                    return 0
                primeni_plan(cur, plan, arg.autor, napomena, postavljeni_raw)
            conn.commit()
        except BaseException:
            conn.rollback()
            for raw in postavljeni_raw:
                Path(raw).unlink(missing_ok=True)
            raise
    ispisi_plan(plan, True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
