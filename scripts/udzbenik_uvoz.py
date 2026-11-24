#!/usr/bin/env python3
"""Увоз садржаја интерактивног уџбеника из JSON фајла у базу.

    python scripts/udzbenik_uvoz.py --fajl primer-minerali.json --dry-run
    python scripts/udzbenik_uvoz.py --fajl primer-minerali.json --execute museum_system --autor ko@nhmbeo.rs

Правила:
- цео фајл се ПРВО валидира (структура, ``sadrzaj`` свake лекције по
  udzbenik/schema/lekcija.schema.json, јединствени ``id`` блокова, постојање
  фотографија у Фототеци и примерака у збирци, правила која шема не изражава:
  ``karta-lokaliteta`` са oblast=srbija има све тачке у оквиру Србије,
  ``paragenetska-sekvenca`` има ``od <= do < broj faza``, ``habitus`` са четири
  индекса има ``i = -(h+k)``, ``infografika`` највише једна по лекцији и
  обавезно први блок, а свака њена ``<Slika>`` референца постоји);
  референтне табеле (кључ ``tablice``, UGOVOR-TABLICE.md §1): ``sadrzaj`` по
  udzbenik/schema/tablica.schema.json, јединствени slug/redosled, ``poglavlje``
  постоји међу поглављима фајла, кључеви колона јединствени, кључеви реда ⊆
  колоне ∪ {izvor}, вредност по типу колоне, ``izvor`` реда почиње неком
  ``oznaka`` из ``izvori``; поглавље са slug-ом ``tablice`` је забрањено
  (резервисан сегмент URL-а); блок ``tablica-link`` упућује на табелу из фајла
  или већ у бази за тај уџбеник, а кључеви ``filter`` су колоне табеле (кад је
  у фајлу); са ``zbirka`` другог уџбеника табела мора бити у бази за тај
  уџбеник, а ``uputi_na`` (и ``iz_lekcije`` као објекат) питања са ``zbirka``
  другог уџбеника — тај
  уџбеник, лекција (и ``blok`` ако је дат) морају постојати у бази;
  табела може имати ``detalji`` {vrsta, kolona, stavke}
  (UGOVOR-TABLICE-2.md, део 2): ``vrsta`` има шему детаља, ``kolona`` је
  колона табеле, кључ сваке ставке је вредност те колоне (као текст) у неком
  реду, свака ставка по шеми врсте; све грешке се испишу одједном,
  са путањом (``poglavlja[1].lekcije[0].blokovi[3]``), и ништа се не упише;
- upsert по ``zbirka`` → ``slug`` поглавља → ``slug`` лекције; лекција чији се
  ``sadrzaj`` променио добија ``verzija + 1`` и нов ред у
  udzbenik_lekcija_verzija (``napomena = 'uvoz: <ime fajla>'``); непромењена
  лекција се не дира; поглавља/лекције којих има у бази а нема у фајлу се НЕ
  бришу — испише се упозорење; табеле исто: upsert по ``slug`` табеле,
  промењен ``sadrzaj`` → ``verzija + 1`` и ред у udzbenik_tablica_verzija,
  табела из базе које нема у фајлу остаје уз упозорење; детаљи редова:
  ``sadrzaj`` табеле добија само {"detalji": {vrsta, kolona}}, ставке иду у
  udzbenik_tablica_detalj (upsert промењених/нових, брисање оних којих нема
  у фајлу); табела без ``detalji`` у фајлу а са ставкама у бази — детаљи
  остају нетакнути уз упозорење;
- видео клипови (кључ ``videi``, UGOVOR-VIDEO.md): ставка по
  udzbenik/schema/video.schema.json, јединствен ``kljuc``, ``fajl`` и
  ``poster`` постоје у ``--video-dir`` са наведеним sha256; блок ``video``
  упућује на клип из фајла или већ у бази за тај уџбеник; upsert по
  ``kljuc`` у udzbenik_video, а фајлови се при ``--execute`` копирају у
  FOTOTEKA_MEDIA_PATH/udzbenik-video/ (адресирано садржајем); клип из базе
  којег нема у фајлу остаје уз упозорење;
- подразумевано је dry-run (испис плана, нула измена); ``--execute <ime baze>``
  (дословно име базе на коју је скрипта стварно повезана, ``current_database()``,
  као у udzbenik_ai_slike.py) ради све у ЈЕДНОЈ трансакцији;
- ``--proveri-literaturu`` (опционо) за сваки блок ``literatura`` пита
  SciSearch: 0 резултата је УПОЗОРЕЊЕ (увоз иде даље); за сваки блок
  ``slika-literatura`` (и сваку ``figura_id`` слику у ``infografika``)
  проверава да ``figura_id`` постоји — непостојећа
  (скривена, ван извора) фигура је ГРЕШКА; неподешен клијент или пад
  сервиса је грешка — тражена провера се није могла обавити, ништа се
  не упише.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from udzbenik import (kljuc_reda, mesta_procesa, mesta_slika, tipovi_blokova, ucitaj_semu,  # noqa: E402
                      video_putanja)

SLUG_RE = re.compile(r'^[a-z0-9][a-z0-9-]{1,59}$')
STATUSI = ('nacrt', 'objavljen')
SEMA_TABLICE_PUTANJA = REPO / 'udzbenik' / 'schema' / 'tablica.schema.json'
SEMA_VIDEA_PUTANJA = REPO / 'udzbenik' / 'schema' / 'video.schema.json'
POLJA_VIDEA = ('sha256', 'velicina_b', 'mime', 'trajanje_s', 'sirina_px', 'visina_px', 'zvuk',
               'poster_sha256', 'opis', 'ai', 'oznaka', 'autor', 'licenca')
REZERVISAN_SLUG_POGLAVLJA = 'tablice'      # сегмент URL-а /udzbenik/<zbirka>/tablice
KLJUC_IZVORA = 'izvor'
NASLOV_TABLICE_NAJVISE = 200
OPIS_TABLICE_NAJVISE = 2000
POLJA_TABLICE = ('slug', 'redosled', 'naslov', 'opis', 'poglavlje', 'status', 'sadrzaj', 'detalji')
# Детаљи редова (UGOVOR-TABLICE-2.md, део 2): врста → шема садржаја ставке.
SEME_DETALJA = {'prostorna-grupa': REPO / 'udzbenik' / 'schema' / 'detalj-prostorna-grupa.schema.json'}
POLJA_DETALJA = ('vrsta', 'kolona', 'stavke')
KLJUC_DETALJA = 'detalji'                  # кључ мета-података у udzbenik_tablica.sadrzaj
KLJUC_STAVKE_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,39}$')   # = CHECK у миграцији 064
# тип колоне → (провера вредности, опис); null је увек дозвољен (празно)
TIPOVI_VREDNOSTI = {
    'broj': (lambda v: isinstance(v, (int, float)) and not isinstance(v, bool), 'број'),
    'da-ne': (lambda v: isinstance(v, bool), 'true/false'),
    'tekst': (lambda v: isinstance(v, str), 'текст'),
    'simbol': (lambda v: isinstance(v, str), 'текст'),
}
# allOf[i] колоне у tablica.schema.json → јаснија порука од „'broj' is not one of …“
PORUKE_USLOVA_KOLONE = ('format је дозвољен само уз tip simbol или tekst',
                        'decimale је дозвољено само уз tip broj')
# Оквир Србије (са Косовом и Метохијом) за karta-lokaliteta, oblast=srbija.
SRBIJA_LAT = (41.8, 46.2)
SRBIJA_LON = (18.8, 23.1)


# --------------------------------------------------------------------------
# Валидација
# --------------------------------------------------------------------------


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
        if tip not in validatori:
            greske.append(f'{p}.tip: непознат тип блока {tip!r}; дозвољено {list(validatori)}')
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
            for tip in tipovi_blokova(sema)}


def validiraj(podaci, cur, video_dir=None):
    """Листа грешака (празна = фајл исправан). Провере постојања у бази иду
    кроз ``cur`` (фотографије) и museum_qr (примерци); фајлови клипова кроз
    ``video_dir``."""
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
    kolone_tablica = validiraj_tablice(podaci.get('tablice'), poglavlja, greske)
    zbirka = u.get('zbirka') if isinstance(u, dict) and isinstance(u.get('zbirka'), str) else None
    kljucevi_videa = validiraj_videe(podaci.get('videi'), video_dir, greske)
    _jedinstveno(poglavlja, 'slug', 'poglavlja', greske, 'slug поглавља')
    _jedinstveno(poglavlja, 'redosled', 'poglavlja', greske, 'redosled поглавља')
    for i, p in enumerate(poglavlja):
        pp = f'poglavlja[{i}]'
        if not isinstance(p, dict):
            greske.append(f'{pp}: поглавље мора бити објекат')
            continue
        _slug(p.get('slug'), f'{pp}.slug', greske)
        if p.get('slug') == REZERVISAN_SLUG_POGLAVLJA:
            greske.append(f'{pp}.slug: slug поглавља {REZERVISAN_SLUG_POGLAVLJA!r} је забрањен '
                          f'(резервисан сегмент URL-а /udzbenik/<zbirka>/{REZERVISAN_SLUG_POGLAVLJA})')
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
            if 'prethodni_slug' in lek:
                _slug(lek.get('prethodni_slug'), f'{lp}.prethodni_slug', greske)
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
                _proveri_infografiku(sadrzaj['blokovi'], f'{lp}.sadrzaj', greske)
                _proveri_pravila(sadrzaj['blokovi'], f'{lp}.sadrzaj', greske)
                _proveri_reference(sadrzaj['blokovi'], f'{lp}.sadrzaj', cur, greske)
                _proveri_tablica_linkove(sadrzaj['blokovi'], f'{lp}.sadrzaj', kolone_tablica, zbirka, cur, greske)
                _proveri_uputnice(sadrzaj['blokovi'], f'{lp}.sadrzaj', zbirka, cur, greske)
                _proveri_video_blokove(sadrzaj['blokovi'], f'{lp}.sadrzaj', kljucevi_videa, zbirka, cur, greske)
    return greske


def sha256_fajla(putanja):
    h = hashlib.sha256()
    with open(putanja, 'rb') as f:
        for komad in iter(lambda: f.read(1 << 20), b''):
            h.update(komad)
    return h.hexdigest()


def validiraj_videe(videi, video_dir, greske):
    """Кључ ``videi`` (UGOVOR-VIDEO.md): ставке по video.schema.json, јединствен
    ``kljuc``, фајл и постер у ``video_dir`` са наведеним sha256; враћа скуп кључева."""
    import jsonschema

    if videi is None:
        return set()
    if not isinstance(videi, list):
        greske.append('videi: мора бити листа')
        return set()
    with open(SEMA_VIDEA_PUTANJA, encoding='utf-8') as f:
        validator = jsonschema.Draft202012Validator(json.load(f))
    _jedinstveno(videi, 'kljuc', 'videi', greske, 'kljuc видеа')
    if videi and video_dir is None:
        greske.append('videi: фајл има клипове — потребан је --video-dir са фајловима клипова и постера')
    kljucevi = set()
    for i, v in enumerate(videi):
        vp = f'videi[{i}]'
        pre = len(greske)
        for g in sorted(validator.iter_errors(v), key=lambda e: list(e.absolute_path)):
            greske.append(f'{vp}{_json_putanja(g)}: {g.message}')
        if len(greske) > pre or not isinstance(v, dict):
            continue
        kljucevi.add(v['kljuc'])
        if video_dir is None:
            continue
        for polje, sha_polje in (('fajl', 'sha256'), ('poster', 'poster_sha256')):
            putanja = Path(video_dir) / v[polje]
            if not putanja.is_file():
                greske.append(f'{vp}.{polje}: фајл {putanja} не постоји')
            elif sha256_fajla(putanja) != v[sha_polje]:
                greske.append(f'{vp}.{sha_polje}: sha256 фајла {putanja} се не поклапа')
    return kljucevi


def _proveri_video_blokove(blokovi, putanja, kljucevi_videa, zbirka, cur, greske):
    """Блок ``video`` упућује на клип из ``videi`` или већ у бази за тај уџбеник."""
    for i, b in enumerate(blokovi):
        if not isinstance(b, dict) or b.get('tip') != 'video' or not isinstance(b.get('video'), str):
            continue
        if b['video'] in kljucevi_videa:
            continue
        cur.execute("""SELECT 1 FROM udzbenik_video v JOIN udzbenik u ON u.id = v.udzbenik_id
                       WHERE v.kljuc = %s AND u.zbirka = %s""", (b['video'], zbirka))
        if cur.fetchone() is None:
            greske.append(f'{putanja}.blokovi[{i}].video: клип {b["video"]!r} не постоји ни у videi фајла '
                          f'ни у бази за уџбеник {zbirka!r}')


def ucitaj_semu_tablice():
    with open(SEMA_TABLICE_PUTANJA, encoding='utf-8') as f:
        return json.load(f)


def validiraj_tablice(tablice, poglavlja, greske):
    """Кључ ``tablice`` (UGOVOR-TABLICE.md §1); враћа {slug: {кључ: тип}
    колона, или None кад колоне нису исправне} за проверу блокова
    ``tablica-link``. Све грешке одједном, отпорно на погрешан облик."""
    import jsonschema

    if tablice is None:
        return {}
    if not isinstance(tablice, list):
        greske.append('tablice: мора бити листа')
        return {}
    slugovi_poglavlja = {p.get('slug') for p in poglavlja if isinstance(p, dict)}
    validator = jsonschema.Draft202012Validator(ucitaj_semu_tablice())
    _jedinstveno(tablice, 'slug', 'tablice', greske, 'slug табеле')
    _jedinstveno(tablice, 'redosled', 'tablice', greske, 'redosled табеле')
    kolone_tablica = {}
    for i, t in enumerate(tablice):
        tp = f'tablice[{i}]'
        if not isinstance(t, dict):
            greske.append(f'{tp}: табела мора бити објекат')
            continue
        _slug(t.get('slug'), f'{tp}.slug', greske)
        _redosled(t.get('redosled'), f'{tp}.redosled', greske)
        _tekst(t.get('naslov'), f'{tp}.naslov', greske, najvise=NASLOV_TABLICE_NAJVISE)
        _tekst(t.get('opis'), f'{tp}.opis', greske, obavezno=False, najvise=OPIS_TABLICE_NAJVISE)
        _status(t.get('status'), f'{tp}.status', greske)
        if t.get('poglavlje') is not None and t['poglavlje'] not in slugovi_poglavlja:
            greske.append(f'{tp}.poglavlje: поглавље {t["poglavlje"]!r} не постоји међу поглављима фајла')
        for kljuc in sorted(set(t) - set(POLJA_TABLICE)):
            greske.append(f'{tp}.{kljuc}: непознато поље табеле (дозвољено {list(POLJA_TABLICE)})')
        sadrzaj = t.get('sadrzaj')
        if not isinstance(sadrzaj, dict):
            greske.append(f'{tp}.sadrzaj: обавезан објекат по tablica.schema.json')
            continue
        sp = f'{tp}.sadrzaj'
        for g in sorted(validator.iter_errors(sadrzaj), key=lambda e: (str(e.json_path), e.message)):
            putanja_seme = list(g.absolute_schema_path)
            poruka = g.message
            if 'allOf' in putanja_seme:
                poruka = PORUKE_USLOVA_KOLONE[putanja_seme[putanja_seme.index('allOf') + 1]]
            greske.append(f'{sp}{_json_putanja(g)}: {poruka}')
        kolone = _proveri_sadrzaj_tablice(sadrzaj, sp, greske)
        if KLJUC_DETALJA in t:
            _proveri_detalje(t[KLJUC_DETALJA], sadrzaj, kolone, f'{tp}.{KLJUC_DETALJA}', greske)
        if isinstance(t.get('slug'), str):
            kolone_tablica[t['slug']] = kolone
    return kolone_tablica


def _proveri_sadrzaj_tablice(sadrzaj, sp, greske):
    """Правила која шема не изражава; враћа {кључ: тип} колона или None."""
    kolone = sadrzaj.get('kolone')
    if not isinstance(kolone, list) or not all(isinstance(k, dict) for k in kolone):
        return None
    _jedinstveno(kolone, 'kljuc', f'{sp}.kolone', greske, 'kljuc колоне')
    tipovi = {k['kljuc']: k.get('tip') for k in kolone if isinstance(k.get('kljuc'), str)}
    izvori = sadrzaj.get('izvori')
    oznake = []
    if isinstance(izvori, list):
        _jedinstveno(izvori, 'oznaka', f'{sp}.izvori', greske, 'oznaka извора')
        oznake = [z['oznaka'] for z in izvori
                  if isinstance(z, dict) and isinstance(z.get('oznaka'), str) and z['oznaka']]
    redovi = sadrzaj.get('redovi')
    if not isinstance(redovi, list):
        return tipovi
    for r, red in enumerate(redovi):
        if not isinstance(red, dict):
            continue
        rp = f'{sp}.redovi[{r}]'
        for kljuc, vrednost in red.items():
            if kljuc == KLJUC_IZVORA:
                if isinstance(vrednost, str) and not any(vrednost.startswith(o) for o in oznake):
                    greske.append(f'{rp}.{KLJUC_IZVORA}: {vrednost!r} не почиње ниједном oznaka из izvori {oznake}')
                continue
            if kljuc not in tipovi:
                greske.append(f'{rp}.{kljuc}: кључ није колона табеле (дозвољено {sorted(tipovi)} и {KLJUC_IZVORA!r})')
                continue
            provera = TIPOVI_VREDNOSTI.get(tipovi[kljuc])
            if vrednost is None or provera is None or isinstance(vrednost, (dict, list)):
                continue        # празно; непознат тип или сложену вредност је шема већ пријавила
            ispravno, opis = provera
            if not ispravno(vrednost):
                greske.append(f'{rp}.{kljuc}: колона типа {tipovi[kljuc]!r} тражи {opis} или null '
                              f'(добијено {vrednost!r})')
    return tipovi


def ucitaj_semu_detalja(vrsta):
    with open(SEME_DETALJA[vrsta], encoding='utf-8') as f:
        return json.load(f)


def _proveri_detalje(detalji, sadrzaj, kolone, dp, greske):
    """``detalji`` табеле: врста са шемом, колона табеле, кључ ставке =
    вредност колоне у неком реду, свака ставка по шеми врсте."""
    import jsonschema

    if not isinstance(detalji, dict):
        greske.append(f'{dp}: мора бити објекат {{vrsta, kolona, stavke}}')
        return
    for kljuc in sorted(set(detalji) - set(POLJA_DETALJA)):
        greske.append(f'{dp}.{kljuc}: непознато поље детаља (дозвољено {list(POLJA_DETALJA)})')
    vrsta = detalji.get('vrsta')
    if not isinstance(vrsta, str) or vrsta not in SEME_DETALJA:
        greske.append(f'{dp}.vrsta: врста детаља мора бити једна од {sorted(SEME_DETALJA)} (добијено {vrsta!r})')
        vrsta = None
    kolona = detalji.get('kolona')
    vrednosti = None
    if kolone is not None:
        if not isinstance(kolona, str) or kolona not in kolone:
            greske.append(f'{dp}.kolona: {kolona!r} није колона табеле (колоне {sorted(kolone)})')
        elif isinstance(sadrzaj.get('redovi'), list):
            vrednosti = {kljuc_reda(r.get(kolona)) for r in sadrzaj['redovi'] if isinstance(r, dict)}
    stavke = detalji.get('stavke')
    if not isinstance(stavke, dict):
        greske.append(f'{dp}.stavke: обавезан објекат кључ → садржај ставке')
        return
    validator = jsonschema.Draft202012Validator(ucitaj_semu_detalja(vrsta)) if vrsta else None
    for kljuc, stavka in stavke.items():
        sp = f'{dp}.stavke[{json.dumps(kljuc, ensure_ascii=False)}]'
        if not KLJUC_STAVKE_RE.match(kljuc):
            greske.append(f'{sp}: кључ ставке мора бити по обрасцу {KLJUC_STAVKE_RE.pattern}')
        elif vrednosti is not None and kljuc not in vrednosti:
            greske.append(f'{sp}: ниједан ред табеле нема {kolona} = {kljuc!r}')
        if validator is not None:
            for g in sorted(validator.iter_errors(stavka), key=lambda e: (str(e.json_path), e.message)):
                greske.append(f'{sp}{_json_putanja(g)}: {g.message}')


def _proveri_tablica_linkove(blokovi, putanja, kolone_tablica, zbirka, cur, greske):
    """Блок ``tablica-link``: табела из фајла или већ у бази за тај уџбеник;
    кључеви ``filter`` су колоне табеле кад је табела у фајлу. Са ``zbirka``
    другог уџбеника — само табела у бази за тај уџбеник."""
    for i, blok in enumerate(blokovi):
        if not isinstance(blok, dict) or blok.get('tip') != 'tablica-link' or not isinstance(blok.get('tablica'), str):
            continue
        p = f'{putanja}.blokovi[{i}]'
        slug = blok['tablica']
        cilj = blok.get('zbirka') if isinstance(blok.get('zbirka'), str) else zbirka
        if cilj != zbirka:
            cur.execute("""SELECT 1 FROM udzbenik_tablica t JOIN udzbenik u ON u.id = t.udzbenik_id
                           WHERE u.zbirka = %s AND t.slug = %s""", (cilj, slug))
            if cur.fetchone() is None:
                greske.append(f'{p}.tablica: табела {slug!r} не постоји у бази за уџбеник {cilj!r}')
            continue
        if slug in kolone_tablica:
            kolone = kolone_tablica[slug]
            filter_ = blok.get('filter')
            if kolone is not None and isinstance(filter_, dict):
                for kljuc in filter_:
                    if kljuc not in kolone:
                        greske.append(f'{p}.filter.{kljuc}: табела {slug!r} нема колону {kljuc!r} '
                                      f'(колоне {sorted(kolone)})')
            continue
        postoji = False
        if zbirka is not None:
            cur.execute("""SELECT 1 FROM udzbenik_tablica t JOIN udzbenik u ON u.id = t.udzbenik_id
                           WHERE u.zbirka = %s AND t.slug = %s""", (zbirka, slug))
            postoji = cur.fetchone() is not None
        if not postoji:
            greske.append(f'{p}.tablica: табела {slug!r} не постоји ни у tablice фајла ни у бази '
                          f'за уџбеник {zbirka!r}')


def _proveri_uputnice(blokovi, putanja, zbirka, cur, greske):
    """``uputi_na`` и ``iz_lekcije`` (облик објекта) питања са ``zbirka``
    другог уџбеника: уџбеник, лекција и (ако је дат) ``blok`` у њој постоје у
    бази. Без ``zbirka`` (или са сопственом) — као и до сада, без провере."""
    for i, blok in enumerate(blokovi):
        if not isinstance(blok, dict) or blok.get('tip') != 'pitanje':
            continue
        for kljuc in ('uputi_na', 'iz_lekcije'):
            if isinstance(blok.get(kljuc), dict):
                _proveri_uputnicu(blok[kljuc], f'{putanja}.blokovi[{i}].{kljuc}', zbirka, cur, greske)


def _proveri_uputnicu(uputi, p, zbirka, cur, greske):
    cilj, lekcija = uputi.get('zbirka'), uputi.get('lekcija')
    if not isinstance(cilj, str) or cilj == zbirka or not isinstance(lekcija, str):
        return
    cur.execute('SELECT id FROM udzbenik WHERE zbirka = %s', (cilj,))
    red = cur.fetchone()
    if red is None:
        greske.append(f'{p}.zbirka: уџбеник {cilj!r} не постоји у бази')
        return
    cur.execute("""SELECT l.sadrzaj FROM udzbenik_lekcija l JOIN udzbenik_poglavlje p ON p.id = l.poglavlje_id
                   WHERE p.udzbenik_id = %s AND l.slug = %s""", (red[0], lekcija))
    lekcije = cur.fetchall()
    if not lekcije:
        greske.append(f'{p}.lekcija: лекција {lekcija!r} не постоји у уџбенику {cilj!r}')
        return
    id_bloka = uputi.get('blok')
    if isinstance(id_bloka, str) and not any(
            isinstance(b, dict) and b.get('id') == id_bloka
            for (sadrzaj,) in lekcije for b in ((_json(sadrzaj) or {}).get('blokovi') or [])):
        greske.append(f'{p}.blok: блок {id_bloka!r} не постоји у лекцији {cilj}/{lekcija}')


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
        elif blok.get('tip') == 'infografika':
            for mesto in mesta_slika(blok):
                slika = mesto.kontejner.get(mesto.kljuc)
                if not isinstance(slika, dict):
                    continue
                if _ceo(slika.get('fotografija_id')):
                    cur.execute('SELECT 1 FROM fotografije WHERE id = %s AND obrisana = FALSE',
                                (slika['fotografija_id'],))
                    if cur.fetchone() is None:
                        greske.append(f'{p}.{mesto.putanja}.fotografija_id: фотографија {slika["fotografija_id"]} '
                                      f'не постоји у Фототеци')
                primerak = slika.get('primerak')
                if isinstance(primerak, dict) and _ceo(primerak.get('objekat_id')) \
                        and isinstance(primerak.get('zbirka'), str) \
                        and not primerak_postoji(primerak['zbirka'], primerak['objekat_id']):
                    greske.append(f'{p}.{mesto.putanja}.primerak: примерак {primerak["zbirka"]}/'
                                  f'{primerak["objekat_id"]} не постоји')


def _proveri_infografiku(blokovi, putanja, greske):
    """Правило уговора које шема не изражава: највише један блок
    ``infografika`` по лекцији и мора бити први блок."""
    for i, blok in enumerate(blokovi):
        if not isinstance(blok, dict) or blok.get('tip') != 'infografika':
            continue
        p = f'{putanja}.blokovi[{i}]'
        if i == 0:
            continue
        if isinstance(blokovi[0], dict) and blokovi[0].get('tip') == 'infografika':
            greske.append(f'{p}: највише један блок infografika по лекцији (први је у {putanja}.blokovi[0])')
        else:
            greske.append(f'{p}: блок infografika мора бити први блок лекције ({putanja}.blokovi[0])')


def _ceo(vrednost):
    return isinstance(vrednost, int) and not isinstance(vrednost, bool) and vrednost >= 1


def _broj(vrednost):
    return isinstance(vrednost, (int, float)) and not isinstance(vrednost, bool)


def _proveri_pravila(blokovi, putanja, greske):
    """Правила која JSON шема не изражава (односи међу пољима); све одједном,
    отпорно на погрешан облик јер је шема такве блокове већ пријавила."""
    for i, blok in enumerate(blokovi):
        if not isinstance(blok, dict) or not isinstance(blok.get('parametri'), dict):
            continue
        par = blok['parametri']
        p = f'{putanja}.blokovi[{i}].parametri'
        if blok.get('tip') == 'dijagram' and blok.get('dijagram') == 'karta-lokaliteta':
            _karta_u_okviru_srbije(par, p, greske)
        elif blok.get('tip') == 'dijagram' and blok.get('dijagram') == 'paragenetska-sekvenca':
            _sekvenca_u_fazama(par, p, greske)
        elif blok.get('tip') == 'scena' and blok.get('scena') == 'habitus':
            _bravais_miller(par, p, greske)


TIPOVI_LITERATURE = ('literatura', 'slika-literatura', 'infografika')


def _blokovi_literature(podaci):
    """(путања, блок) за сваки блок ``literatura``/``slika-literatura``/
    ``infografika`` у исправно обликованом фајлу."""
    for i, p in enumerate(podaci.get('poglavlja') or []):
        for j, lek in enumerate(p.get('lekcije') or []):
            blokovi = (lek.get('sadrzaj') or {}).get('blokovi') or []
            for k, blok in enumerate(blokovi):
                if isinstance(blok, dict) and (blok.get('tip') in TIPOVI_LITERATURE or (
                        blok.get('tip') == 'dijagram' and blok.get('dijagram') == 'proces')):
                    yield f'poglavlja[{i}].lekcije[{j}].sadrzaj.blokovi[{k}]', blok


def _figure(putanja, blok):
    """(путања, figura_id) — блок ``slika-literatura`` има једну, ``infografika``
    по једну на сваком ``<Slika>`` месту са ``figura_id``."""
    if blok.get('tip') == 'slika-literatura':
        yield f'{putanja}.figura_id', blok['figura_id']
        return
    if blok.get('tip') == 'dijagram':
        for i, mesto in mesta_procesa(blok):
            yield f'{putanja}.parametri.mesta[{i}].figura_id', mesto['figura_id']
        return
    for mesto in mesta_slika(blok):
        slika = mesto.kontejner.get(mesto.kljuc)
        if isinstance(slika, dict) and 'figura_id' in slika:
            yield f'{putanja}.{mesto.putanja}.figura_id', slika['figura_id']


def proveri_literaturu(podaci):
    """(упозорења, грешке) — упозорење за блок без резултата, грешка за
    непостојећу фигуру и када SciSearch није подешен или не одговара."""
    import scisearch_klijent

    upozorenja, greske = [], []
    if not scisearch_klijent.podesen():
        return upozorenja, ['SciSearch није подешен (SCISEARCH_URL / SCISEARCH_SVC_TOKEN) — '
                            '--proveri-literaturu се не може обавити']
    for putanja, blok in _blokovi_literature(podaci):
        if blok.get('tip') != 'literatura':
            for putanja_figure, figura_id in _figure(putanja, blok):
                try:
                    scisearch_klijent.figura(figura_id)
                except scisearch_klijent.SciSearchNemaFigure:
                    greske.append(f'{putanja_figure}: фигура {figura_id} не постоји у SciSearch-у')
                except scisearch_klijent.SciSearchGreska as exc:
                    greske.append(f'{putanja_figure}: SciSearch није одговорио ({exc.razlog})')
            continue
        try:
            rezultati = scisearch_klijent.pretrazi(blok['upit'], blok.get('broj', 3))
        except scisearch_klijent.SciSearchGreska as exc:
            greske.append(f'{putanja}: SciSearch није одговорио ({exc.razlog})')
            continue
        if not rezultati:
            upozorenja.append(f'{putanja}.upit: {blok["upit"]!r} даје 0 резултата у SciSearch-у')
    return upozorenja, greske


def _karta_u_okviru_srbije(par, p, greske):
    """Шема подразумева oblast=srbija кад поље недостаје."""
    if par.get('oblast', 'srbija') != 'srbija' or not isinstance(par.get('lokaliteti'), list):
        return
    for j, lok in enumerate(par['lokaliteti']):
        if not isinstance(lok, dict):
            continue
        for polje, (najmanje, najvise) in (('lat', SRBIJA_LAT), ('lon', SRBIJA_LON)):
            v = lok.get(polje)
            if _broj(v) and not najmanje <= v <= najvise:
                greske.append(f'{p}.lokaliteti[{j}].{polje}: {v} је ван оквира Србије '
                              f'({najmanje}–{najvise}) за oblast=srbija')


def _sekvenca_u_fazama(par, p, greske):
    if not isinstance(par.get('faze'), list) or not isinstance(par.get('minerali'), list):
        return
    broj_faza = len(par['faze'])
    for j, m in enumerate(par['minerali']):
        if not isinstance(m, dict):
            continue
        od, do = m.get('od'), m.get('do')
        if not (_broj(od) and _broj(do)):
            continue
        if od > do:
            greske.append(f'{p}.minerali[{j}]: od={od} је веће од do={do}')
        if do >= broj_faza:
            greske.append(f'{p}.minerali[{j}].do: {do} је ван низа faze (0–{broj_faza - 1})')


def _bravais_miller(par, p, greske):
    """Четири индекса (hkil): i = −(h+k)."""
    if not isinstance(par.get('forme'), list):
        return
    for j, forma in enumerate(par['forme']):
        hkl = forma.get('hkl') if isinstance(forma, dict) else None
        if not (isinstance(hkl, list) and len(hkl) == 4 and all(_broj(x) for x in hkl)):
            continue
        h, k, i = hkl[0], hkl[1], hkl[2]
        if i != -(h + k):
            greske.append(f'{p}.forme[{j}].hkl: i={i} а мора бити −(h+k)={-(h + k)} за (hkil)={hkl}')


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
    plan = {'zbirka': u['zbirka'], 'upozorenja': [], 'greske': [], 'poglavlja': []}
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

    # Лекција коју фајл наводи у другом поглављу него база премешта се (исти id,
    # историја верзија и напредак читалаца остају), уместо да настане дупликат.
    premestene = {}
    if red is not None:
        u_fajlu = {(p['slug'], lek['slug']) for p in podaci['poglavlja'] for lek in p['lekcije']}
        cur.execute("""SELECT l.id, l.slug, l.naslov, l.sazetak, l.redosled, l.status, l.verzija, l.sadrzaj, p.slug
                       FROM udzbenik_lekcija l JOIN udzbenik_poglavlje p ON p.id = l.poglavlje_id
                       WHERE p.udzbenik_id = %s""", (red[0],))
        u_bazi = cur.fetchall()
        stari_par = {(r[8], r[1]) for r in u_bazi}
        prethodni = {lek['prethodni_slug']: (p['slug'], lek['slug']) for p in podaci['poglavlja']
                     for lek in p['lekcije'] if lek.get('prethodni_slug')}
        for r in u_bazi:
            if (r[8], r[1]) in u_fajlu:
                continue
            if r[1] in prethodni and prethodni[r[1]] not in stari_par:     # преименована (и можда премештена)
                novo_p, novo_s = prethodni[r[1]]
            else:
                novo = [ps for ps, ls in u_fajlu if ls == r[1] and (ps, ls) not in stari_par]
                if len(novo) != 1:
                    continue
                novo_p, novo_s = novo[0], r[1]
            premestene[novo_s] = {'id': r[0], 'naslov': r[2], 'sazetak': r[3], 'redosled': r[4], 'status': r[5],
                                  'verzija': r[6], 'sadrzaj': _json(r[7]), 'iz': r[8], 'u': novo_p,
                                  'stari_slug': r[1]}
    plan['premestene'] = {slug: (v['iz'], v['u']) for slug, v in premestene.items()}
    stari_slugovi = {v['stari_slug'] for v in premestene.values()}

    slugovi_u_fajlu = {p['slug'] for p in podaci['poglavlja']}
    zauzeti = {v['redosled']: slug for slug, v in postojeca_poglavlja.items() if slug not in slugovi_u_fajlu}
    for i, p in enumerate(podaci['poglavlja']):
        staro = postojeca_poglavlja.get(p['slug'])
        if p['redosled'] in zauzeti:
            plan['greske'].append(
                f'poglavlja[{i}].redosled: redosled {p["redosled"]} већ држи поглавље '
                f'{zauzeti[p["redosled"]]!r} које је у бази, а нема га у фајлу — додај га у фајл '
                f'са другим redosled-ом или промени redosled новог поглавља')
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
        slugovi_lekcija = {lek['slug'] for lek in p['lekcije']}
        zauzete = {v['redosled']: slug for slug, v in postojece_lekcije.items()
                   if slug not in slugovi_lekcija and slug not in stari_slugovi}
        for j, lek in enumerate(p['lekcije']):
            stara = postojece_lekcije.get(lek['slug'])
            premestena = premestene.get(lek['slug']) if stara is None and premestene.get(lek['slug'], {}).get('u') == p['slug'] else None
            if premestena is not None:
                stara = premestena
            if lek['redosled'] in zauzete:
                plan['greske'].append(
                    f'poglavlja[{i}].lekcije[{j}].redosled: redosled {lek["redosled"]} већ држи лекција '
                    f'{p["slug"]}/{zauzete[lek["redosled"]]} која је у бази, а нема је у фајлу — додај је у фајл '
                    f'са другим redosled-ом или промени redosled нове лекције')
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
                elif not podaci_isti or premestena is not None:
                    l_stavka['akcija'] = 'menja podatke'
                else:
                    l_stavka['akcija'] = 'isto'
                if premestena is not None:
                    l_stavka['iz_poglavlja'] = premestena['iz']
                    l_stavka['stari_slug'] = premestena['stari_slug']
            stavka['lekcije'].append(l_stavka)
        for slug in sorted(set(postojece_lekcije) - {lek['slug'] for lek in p['lekcije']} - stari_slugovi):
            plan['upozorenja'].append(f'лекција {p["slug"]}/{slug} је у бази, а нема је у фајлу — остаје нетакнута')
        plan['poglavlja'].append(stavka)
    for slug in sorted(set(postojeca_poglavlja) - {p['slug'] for p in podaci['poglavlja']}):
        plan['upozorenja'].append(f'поглавље {slug} је у бази, а нема га у фајлу — остаје нетакнуто')
    _planiraj_tablice(cur, podaci, plan, red[0] if red is not None else None)
    _planiraj_videe(cur, podaci, plan, red[0] if red is not None else None)
    return plan


def _planiraj_videe(cur, podaci, plan, udzbenik_id):
    """Upsert по ``kljuc``; кључ који већ држи други уџбеник је грешка."""
    plan['videi'] = []
    for i, v in enumerate(podaci.get('videi') or []):
        cur.execute(f"SELECT id, udzbenik_id, {', '.join(POLJA_VIDEA)} FROM udzbenik_video WHERE kljuc = %s",
                    (v['kljuc'],))
        red = cur.fetchone()
        stavka = {'kljuc': v['kljuc'], 'id': red[0] if red else None}
        if red is None:
            stavka['akcija'] = 'dodaje'
        elif red[1] != udzbenik_id:
            plan['greske'].append(f'videi[{i}].kljuc: клип {v["kljuc"]!r} већ припада другом уџбенику')
            stavka['akcija'] = 'isto'
        else:
            stara = dict(zip(POLJA_VIDEA, red[2:]))
            stara['trajanje_s'] = float(stara['trajanje_s'])
            stavka['akcija'] = 'isto' if stara == _polja_videa(v, stara['velicina_b']) else 'menja'
        plan['videi'].append(stavka)
    if udzbenik_id is not None:
        cur.execute('SELECT kljuc FROM udzbenik_video WHERE udzbenik_id = %s', (udzbenik_id,))
        u_fajlu = {v['kljuc'] for v in podaci.get('videi') or []}
        for (kljuc,) in sorted(cur.fetchall()):
            if kljuc not in u_fajlu:
                plan['upozorenja'].append(f'видео {kljuc} је у бази, а нема га у фајлу — остаје нетакнут')


def _polja_videa(v, velicina_b):
    return {'sha256': v['sha256'], 'velicina_b': velicina_b, 'mime': v['mime'],
            'trajanje_s': float(v['trajanje_s']), 'sirina_px': v['sirina_px'], 'visina_px': v['visina_px'],
            'zvuk': v.get('zvuk', False), 'poster_sha256': v['poster_sha256'], 'opis': v['opis'],
            'ai': v['ai'], 'oznaka': v.get('oznaka'), 'autor': v.get('autor'), 'licenca': v.get('licenca')}


def _planiraj_tablice(cur, podaci, plan, udzbenik_id):
    """Upsert по slug-у табеле; промењен ``sadrzaj`` → нова верзија; ставке
    детаља се пореде посебно (+ нове, ~ промењене, - којих нема у фајлу)."""
    tablice = podaci.get('tablice') or []
    postojece = {}
    if udzbenik_id is not None:
        cur.execute("""SELECT id, slug, redosled, naslov, opis, poglavlje_slug, status, verzija, sadrzaj
                       FROM udzbenik_tablica WHERE udzbenik_id = %s""", (udzbenik_id,))
        postojece = {r[1]: {'id': r[0], 'redosled': r[2], 'naslov': r[3], 'opis': r[4], 'poglavlje': r[5],
                            'status': r[6], 'verzija': r[7], 'sadrzaj': _json(r[8])} for r in cur.fetchall()}
    slugovi = {t['slug'] for t in tablice}
    zauzeti = {v['redosled']: slug for slug, v in postojece.items() if slug not in slugovi}
    plan['tablice'] = []
    for i, t in enumerate(tablice):
        if t['redosled'] in zauzeti:
            plan['greske'].append(
                f'tablice[{i}].redosled: redosled {t["redosled"]} већ држи табела {zauzeti[t["redosled"]]!r} '
                f'која је у бази, а нема је у фајлу — додај је у фајл са другим redosled-ом или промени '
                f'redosled нове табеле')
        stara = postojece.get(t['slug'])
        sadrzaj = _sadrzaj_za_upis(t, stara, i, plan)
        stavka = {'slug': t['slug'], 'id': stara['id'] if stara else None, 'nova_verzija': None,
                  'sadrzaj': sadrzaj, 'detalji': _planiraj_detalje(cur, t, stara),
                  'broj_detalja': len(t[KLJUC_DETALJA]['stavke']) if KLJUC_DETALJA in t else 0}
        if stara is None:
            stavka.update(akcija='dodaje', nova_verzija=1)
        elif stara['sadrzaj'] != sadrzaj:
            stavka.update(akcija='menja sadrzaj', nova_verzija=stara['verzija'] + 1)
        elif ((stara['redosled'], stara['naslov'], stara['opis'], stara['poglavlje'])
              != (t['redosled'], t['naslov'], t.get('opis'), t.get('poglavlje'))
              or ('status' in t and stara['status'] != t['status'])):
            stavka['akcija'] = 'menja podatke'
        elif stavka['detalji'] is not None and any(stavka['detalji'].values()):
            stavka['akcija'] = 'menja detalje'
        else:
            stavka['akcija'] = 'isto'
        plan['tablice'].append(stavka)
    for slug in sorted(set(postojece) - slugovi):
        plan['upozorenja'].append(f'табела {slug} је у бази, а нема је у фајлу — остаје нетакнута')


def _sadrzaj_za_upis(t, stara, i, plan):
    """``sadrzaj`` табеле какав иде у базу: из фајла + {"detalji": {vrsta,
    kolona}} (без ставки). Табела без ``detalji`` у фајлу задржава мета-податке
    детаља из базе (ставке остају нетакнуте, као лекције којих нема у фајлу)."""
    sadrzaj = dict(t['sadrzaj'])
    if KLJUC_DETALJA in t:
        sadrzaj[KLJUC_DETALJA] = {'vrsta': t[KLJUC_DETALJA]['vrsta'], 'kolona': t[KLJUC_DETALJA]['kolona']}
    elif stara is not None and isinstance(stara['sadrzaj'], dict) and KLJUC_DETALJA in stara['sadrzaj']:
        meta = stara['sadrzaj'][KLJUC_DETALJA]
        sadrzaj[KLJUC_DETALJA] = meta
        plan['upozorenja'].append(f'табела {t["slug"]}: детаљи редова ({meta.get("vrsta")}) су у бази, а нема их '
                                  f'у фајлу — остају нетакнути')
        kolone = {k.get('kljuc') for k in t['sadrzaj'].get('kolone', [])}
        if meta.get('kolona') not in kolone:
            plan['greske'].append(f'tablice[{i}].sadrzaj.kolone: колона детаља {meta.get("kolona")!r} из базе '
                                  f'више није колона табеле — додај ``detalji`` у фајл')
    return sadrzaj


def _planiraj_detalje(cur, t, stara):
    """{'dodaje': [...], 'menja': [...], 'brise': [...]} кључева ставки, или
    None кад фајл не наводи ``detalji`` за табелу."""
    if KLJUC_DETALJA not in t:
        return None
    u_bazi = {}
    if stara is not None:
        cur.execute('SELECT kljuc, sadrzaj FROM udzbenik_tablica_detalj WHERE tablica_id = %s', (stara['id'],))
        u_bazi = {r[0]: _json(r[1]) for r in cur.fetchall()}
    stavke = t[KLJUC_DETALJA]['stavke']
    return {'dodaje': [k for k in stavke if k not in u_bazi],
            'menja': [k for k in stavke if k in u_bazi and u_bazi[k] != stavke[k]],
            'brise': sorted(set(u_bazi) - set(stavke))}


# --------------------------------------------------------------------------
# Примена (само уз --execute, у трансакцији позиваоца)
# --------------------------------------------------------------------------

def primeni_plan(cur, podaci, plan, autor, napomena, video_dir=None):
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
    premestene = [lek['id'] for s in plan['poglavlja'] for lek in s['lekcije'] if lek.get('iz_poglavlja')]
    if premestene:
        cur.execute('UPDATE udzbenik_lekcija SET redosled = -id WHERE id = ANY(%s)', (premestene,))

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
            if l_stavka.get('iz_poglavlja'):
                cur.execute('UPDATE udzbenik_lekcija SET poglavlje_id = %s, slug = %s WHERE id = %s',
                            (poglavlje_id, lek['slug'], lekcija_id))
                cur.execute("""INSERT INTO udzbenik_lekcija_alias (lekcija_id, poglavlje_slug, slug)
                               VALUES (%s, %s, %s) ON CONFLICT DO NOTHING""",
                            (lekcija_id, l_stavka['iz_poglavlja'], l_stavka['stari_slug']))
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
    primeni_tablice(cur, podaci, plan, udzbenik_id, autor, napomena)
    primeni_videe(cur, podaci, plan, udzbenik_id, autor, video_dir)


def media_koren():
    """FOTOTEKA_MEDIA_PATH као у апликацији; релативна путања је од корена репоа."""
    koren = Path(os.environ.get('FOTOTEKA_MEDIA_PATH', './data/fototeka_media'))
    return koren if koren.is_absolute() else REPO / koren


def _smesti(izvor, relativna):
    """Копија у media корен (атомски: привремени фајл па rename); исти садржај
    је већ ту ако постоји фајл исте величине (путања је sha256)."""
    cilj = media_koren() / relativna
    if cilj.is_file() and cilj.stat().st_size == izvor.stat().st_size:
        return
    cilj.parent.mkdir(parents=True, exist_ok=True)
    privremeni = cilj.with_name(cilj.name + '.uvoz')
    shutil.copyfile(izvor, privremeni)
    os.replace(privremeni, cilj)


def primeni_videe(cur, podaci, plan, udzbenik_id, autor, video_dir):
    for v, stavka in zip(podaci.get('videi') or [], plan.get('videi', [])):
        if stavka['akcija'] == 'isto':
            continue
        fajl, poster = Path(video_dir) / v['fajl'], Path(video_dir) / v['poster']
        nastavak = 'webm' if v['mime'] == 'video/webm' else 'mp4'
        putanja, poster_putanja = video_putanja(v['sha256'], nastavak), video_putanja(v['poster_sha256'], 'jpg')
        _smesti(fajl, putanja)
        _smesti(poster, poster_putanja)
        polja = _polja_videa(v, fajl.stat().st_size)
        kolone = ['udzbenik_id', 'kljuc', 'putanja', 'poster_putanja', 'uvezao_email', *POLJA_VIDEA]
        vrednosti = [udzbenik_id, v['kljuc'], putanja, poster_putanja, autor, *(polja[k] for k in POLJA_VIDEA)]
        izmene = ', '.join(f'{k} = EXCLUDED.{k}' for k in kolone if k not in ('udzbenik_id', 'kljuc'))
        cur.execute(f"""INSERT INTO udzbenik_video ({', '.join(kolone)}) VALUES ({', '.join(['%s'] * len(kolone))})
                        ON CONFLICT (kljuc) DO UPDATE SET {izmene}, updated_at = now()""", vrednosti)


def primeni_tablice(cur, podaci, plan, udzbenik_id, autor, napomena):
    """Redosled је UNIQUE: постојеће табеле из фајла прво добијају привремен
    негативан redosled (као поглавља), па размена места не удари у ограничење."""
    postojece = [s['id'] for s in plan['tablice'] if s['id'] is not None]
    if postojece:
        cur.execute('UPDATE udzbenik_tablica SET redosled = -id WHERE id = ANY(%s)', (postojece,))
    for t, stavka in zip(podaci.get('tablice') or [], plan['tablice']):
        sadrzaj = json.dumps(stavka['sadrzaj'], ensure_ascii=False)
        tablica_id = stavka['id']
        if stavka['akcija'] == 'dodaje':
            cur.execute("""INSERT INTO udzbenik_tablica (udzbenik_id, slug, redosled, naslov, opis, poglavlje_slug,
                               status, sadrzaj, verzija, azurirao_email)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1, %s) RETURNING id""",
                        (udzbenik_id, t['slug'], t['redosled'], t['naslov'], t.get('opis'), t.get('poglavlje'),
                         t.get('status', 'nacrt'), sadrzaj, autor))
            tablica_id = cur.fetchone()[0]
            _upisi_verziju_tablice(cur, tablica_id, 1, sadrzaj, autor, napomena)
        elif stavka['akcija'] == 'menja sadrzaj':
            cur.execute("""UPDATE udzbenik_tablica SET redosled = %s, naslov = %s, opis = %s, poglavlje_slug = %s,
                               status = COALESCE(%s, status), sadrzaj = %s, verzija = %s,
                               azurirao_email = %s, updated_at = now()
                           WHERE id = %s""",
                        (t['redosled'], t['naslov'], t.get('opis'), t.get('poglavlje'), t.get('status'),
                         sadrzaj, stavka['nova_verzija'], autor, stavka['id']))
            _upisi_verziju_tablice(cur, stavka['id'], stavka['nova_verzija'], sadrzaj, autor, napomena)
        else:
            # 'isto' такође пролази овде само да врати привремени redosled
            cur.execute("""UPDATE udzbenik_tablica SET redosled = %s, naslov = %s, opis = %s, poglavlje_slug = %s,
                               status = COALESCE(%s, status),
                               updated_at = CASE WHEN %s THEN now() ELSE updated_at END
                           WHERE id = %s""",
                        (t['redosled'], t['naslov'], t.get('opis'), t.get('poglavlje'), t.get('status'),
                         stavka['akcija'] in ('menja podatke', 'menja detalje'), stavka['id']))
        if stavka['detalji'] is not None:
            _primeni_detalje(cur, tablica_id, t[KLJUC_DETALJA]['stavke'], stavka['detalji'])


def _primeni_detalje(cur, tablica_id, stavke, plan_detalja):
    """Upsert нових/промењених ставки, брисање ставки којих нема у фајлу."""
    for kljuc in plan_detalja['dodaje'] + plan_detalja['menja']:
        cur.execute("""INSERT INTO udzbenik_tablica_detalj (tablica_id, kljuc, sadrzaj) VALUES (%s, %s, %s)
                       ON CONFLICT (tablica_id, kljuc) DO UPDATE SET sadrzaj = EXCLUDED.sadrzaj, azurirano = now()""",
                    (tablica_id, kljuc, json.dumps(stavke[kljuc], ensure_ascii=False)))
    if plan_detalja['brise']:
        cur.execute('DELETE FROM udzbenik_tablica_detalj WHERE tablica_id = %s AND kljuc = ANY(%s)',
                    (tablica_id, plan_detalja['brise']))


def _upisi_verziju_tablice(cur, tablica_id, verzija, sadrzaj, autor, napomena):
    cur.execute("""INSERT INTO udzbenik_tablica_verzija (tablica_id, verzija, sadrzaj, autor_email, napomena)
                   VALUES (%s, %s, %s, %s, %s)""", (tablica_id, verzija, sadrzaj, autor, napomena))


def _upisi_verziju(cur, lekcija_id, verzija, sadrzaj, autor, napomena):
    cur.execute("""INSERT INTO udzbenik_lekcija_verzija (lekcija_id, verzija, sadrzaj, autor_email, napomena)
                   VALUES (%s, %s, %s, %s, %s)""", (lekcija_id, verzija, sadrzaj, autor, napomena))


# --------------------------------------------------------------------------
# Испис
# --------------------------------------------------------------------------

ZNAK = {'dodaje': '+', 'menja': '~', 'menja sadrzaj': '~', 'menja podatke': '~', 'menja detalje': '~', 'isto': '='}


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
            if lek.get('iz_poglavlja') and lek['stari_slug'] != lek['slug']:
                dodatak += f'; преименује се из {lek["iz_poglavlja"]}/{lek["stari_slug"]}'
            elif lek.get('iz_poglavlja'):
                dodatak += f'; премешта се из поглавља {lek["iz_poglavlja"]}'
            if lek['nova_verzija']:
                brojac['nove_verzije'] += 1
            print(f'      {ZNAK[lek["akcija"]]} lekcija {p["slug"]}/{lek["slug"]} ({lek["akcija"]}{dodatak})')
    brojac.update(tablice=0, nove_verzije_tablica=0, detalji=0, detalji_dodaje=0, detalji_menja=0, detalji_brise=0)
    for t in plan.get('tablice', []):
        brojac['tablice'] += 1
        dodatak = f' → verzija {t["nova_verzija"]}' if t['akcija'] == 'menja sadrzaj' else ''
        if t['nova_verzija']:
            brojac['nove_verzije_tablica'] += 1
        d = t.get('detalji')
        if d is not None:
            promene = f'+{len(d["dodaje"])} ~{len(d["menja"])} -{len(d["brise"])}'
            brojac['detalji'] += t['broj_detalja']
            for vrsta in ('dodaje', 'menja', 'brise'):
                brojac[f'detalji_{vrsta}'] += len(d[vrsta])
            if t['akcija'] == 'menja detalje':
                dodatak = f': {promene}'
            elif any(d.values()):
                dodatak += f'; detalji: {promene}'
        print(f'  {ZNAK[t["akcija"]]} tablica {t["slug"]} ({t["akcija"]}{dodatak})')
    for v in plan.get('videi', []):
        print(f'  {ZNAK[v["akcija"]]} video {v["kljuc"]} ({v["akcija"]})')
    for u in plan['upozorenja']:
        print(f'  ! упозорење: {u}')
    if plan.get('videi'):
        akcije = [v['akcija'] for v in plan['videi']]
        print(f'Видео: {len(akcije)} клипова (+{akcije.count("dodaje")} ~{akcije.count("menja")} '
              f'={akcije.count("isto")}).')
    print(f'Укупно: {brojac["poglavlja"]} поглавља, {brojac["lekcije"]} лекција, '
          f'{brojac["nove_verzije"]} нових верзија, {brojac["tablice"]} табела '
          f'({brojac["nove_verzije_tablica"]} нових верзија табела), {brojac["detalji"]} детаља редова '
          f'(+{brojac["detalji_dodaje"]} ~{brojac["detalji_menja"]} -{brojac["detalji_brise"]}), '
          f'{len(plan["upozorenja"])} упозорења.')
    return brojac


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _argumenti(argv):
    p = argparse.ArgumentParser(description='Увоз садржаја уџбеника из JSON фајла (подразумевано dry-run).')
    p.add_argument('--fajl', required=True, help='JSON фајл са уџбеником, поглављима и лекцијама')
    p.add_argument('--dry-run', action='store_true', help='само испиши шта би било урађено (подразумевано)')
    p.add_argument('--execute', metavar='IME_BAZE', help='стварно упиши; потврда = име базе на коју је повезано')
    p.add_argument('--autor', default=None, help='e-mail аутора за udzbenik.autor_email / verzija.autor_email')
    p.add_argument('--video-dir', default=None,
                   help='директоријум са фајловима клипова и постера из кључа videi (путање су релативне)')
    p.add_argument('--proveri-literaturu', action='store_true',
                   help='за сваки блок literatura питај SciSearch (0 резултата = упозорење); '
                        'за slika-literatura провери да figura_id постоји')
    return p.parse_args(argv)


def main(argv=None):
    arg = _argumenti(argv)
    izvrsavanje = arg.execute is not None
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
                baza = cur.fetchone()[0]
                print(f'База: {baza}  фајл: {arg.fajl}  режим: {"EXECUTE" if izvrsavanje else "dry-run"}')
                if izvrsavanje and arg.execute != baza:
                    print(f'ГРЕШКА: --execute тражи дословно име базе „{baza}“ (добијено {arg.execute!r}).',
                          file=sys.stderr)
                    conn.rollback()
                    return 2
                greske = validiraj(podaci, cur, arg.video_dir)
                if greske:
                    print(f'ГРЕШКЕ У ФАЈЛУ ({len(greske)}) — ништа није уписано:', file=sys.stderr)
                    for g in greske:
                        print(f'  - {g}', file=sys.stderr)
                    conn.rollback()
                    return 1
                plan = napravi_plan(cur, podaci)
                if arg.proveri_literaturu:
                    upozorenja, greske = proveri_literaturu(podaci)
                    if greske:
                        print(f'ГРЕШКЕ ПРОВЕРЕ ЛИТЕРАТУРЕ ({len(greske)}) — ништа није уписано:', file=sys.stderr)
                        for g in greske:
                            print(f'  - {g}', file=sys.stderr)
                        conn.rollback()
                        return 1
                    plan['upozorenja'].extend(upozorenja)
                if plan['greske']:
                    print(f'ГРЕШКЕ У ПЛАНУ ({len(plan["greske"])}) — колизија redosled-а са базом, '
                          'ништа није уписано:', file=sys.stderr)
                    for g in plan['greske']:
                        print(f'  - {g}', file=sys.stderr)
                    conn.rollback()
                    return 1
                if izvrsavanje:
                    primeni_plan(cur, podaci, plan, arg.autor, napomena, arg.video_dir)
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
