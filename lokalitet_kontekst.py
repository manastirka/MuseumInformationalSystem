"""Контекст локалитета из Google Earth Engine (миграција 066).

Свеске 12-kontekst-lokaliteta и 13-bio-stanista рачунају, ван MIS-а, по тачки
(примерак или локалитет из шифарника) надморску висину, нагиб, покривач
земљишта (Dynamic World), лист OGK 1:100 000, шуму 2000. и њен губитак
(Hansen GFC) и уделе класа покривача у кругу 1 km. Овде су:

- ``ucitaj_csv`` / ``validiraj_redove`` — чисте функције над CSV текстом
  (тестирају се без базе); упис ради scripts/kontekst_lokaliteta_uvoz.py;
- ``kontekst_za_mineral`` — читање за детаљ примерка (пад базе или
  непримењена миграција не обара страну — враћа None).
"""

from __future__ import annotations

import csv
import io
import json
import logging
import os
import re
from datetime import date

logger = logging.getLogger(__name__)

VRSTE = ('mineral', 'lokalitet')

# Dynamic World V1, трака label (Brown и др. 2022, doi:10.1038/s41597-022-01307-4).
DW_KLASE = ('water', 'trees', 'grass', 'flooded_vegetation', 'crops', 'shrub_and_scrub',
            'built', 'bare', 'snow_and_ice')
DW_NAZIVI = {
    'water': 'Вода', 'trees': 'Дрвеће', 'grass': 'Трава', 'flooded_vegetation': 'Плавна вегетација',
    'crops': 'Усеви', 'shrub_and_scrub': 'Жбуње и шикара', 'built': 'Изграђено', 'bare': 'Голо тле',
    'snow_and_ice': 'Снег и лед',
}

# Колоне по свесци, тачно по уговору (/tmp/petro/colab/rad/BRIF-GEE.md).
KOLONE_12 = ('lat', 'lon', 'nadmorska_visina_m', 'nagib_stepeni', 'pokrivac_klasa', 'pokrivac_godina',
             'ogk_list', 'izvor', 'datum_izracuna')
KOLONE_13 = ('suma_2000_pct', 'gubitak_sume_ha', 'gubitak_sume_pct', 'gubitak_od', 'gubitak_do',
             'dw_udeli', 'dw_godina', 'bio_izvor', 'bio_datum_izracuna')
KOLONE = KOLONE_12 + KOLONE_13

OGK_LIST = re.compile(r'^[KL]34-[0-9]{2,3}$')
_GODINA = (1984, 2100)


def _broj(v, polje, od=None, do=None):
    x = float(v)
    if x != x or x in (float('inf'), float('-inf')):
        raise ValueError(f'{polje}: није број')
    if (od is not None and x < od) or (do is not None and x > do):
        raise ValueError(f'{polje}: {v} ван опсега {od}–{do}')
    return x


def _ceo(v, polje, od, do):
    if not re.fullmatch(r'-?\d+', v):
        raise ValueError(f'{polje}: „{v}“ није цео број')
    x = int(v)
    if not od <= x <= do:
        raise ValueError(f'{polje}: {x} ван опсега {od}–{do}')
    return x


def _datum(v, polje):
    try:
        return date.fromisoformat(v)
    except ValueError:
        raise ValueError(f'{polje}: „{v}“ није ISO датум (YYYY-MM-DD)') from None


def _list(v):
    if not OGK_LIST.match(v):
        raise ValueError(f'ogk_list: „{v}“ није облик K34-03 / L34-141')
    return v


def _udeli(v):
    try:
        d = json.loads(v)
    except ValueError:
        raise ValueError('dw_udeli: није JSON') from None
    if not isinstance(d, dict) or not d:
        raise ValueError('dw_udeli: очекиван непразан JSON објекат')
    for k, x in d.items():
        if k not in DW_KLASE:
            raise ValueError(f'dw_udeli: непозната класа „{k}“')
        if isinstance(x, bool) or not isinstance(x, (int, float)) or not 0 <= x <= 100:
            raise ValueError(f'dw_udeli: {k} = {x!r} није удео 0–100')
    zbir = sum(d.values())
    if not 98 <= zbir <= 102:
        raise ValueError(f'dw_udeli: збир удела {zbir:.1f} није ≈100')
    return d


_PRETVARANJE = {
    'lat': lambda v: _broj(v, 'lat', -90, 90),
    'lon': lambda v: _broj(v, 'lon', -180, 180),
    'nadmorska_visina_m': lambda v: _broj(v, 'nadmorska_visina_m', -500, 9000),
    'nagib_stepeni': lambda v: _broj(v, 'nagib_stepeni', 0, 90),
    'pokrivac_klasa': lambda v: _ceo(v, 'pokrivac_klasa', 0, 8),
    'pokrivac_godina': lambda v: _ceo(v, 'pokrivac_godina', *_GODINA),
    'ogk_list': _list,
    'izvor': lambda v: v,
    'datum_izracuna': lambda v: _datum(v, 'datum_izracuna'),
    'suma_2000_pct': lambda v: _broj(v, 'suma_2000_pct', 0, 100),
    'gubitak_sume_ha': lambda v: _broj(v, 'gubitak_sume_ha', 0),
    'gubitak_sume_pct': lambda v: _broj(v, 'gubitak_sume_pct', 0, 100),
    'gubitak_od': lambda v: _ceo(v, 'gubitak_od', 2000, _GODINA[1]),
    'gubitak_do': lambda v: _ceo(v, 'gubitak_do', 2000, _GODINA[1]),
    'dw_udeli': _udeli,
    'dw_godina': lambda v: _ceo(v, 'dw_godina', 2015, _GODINA[1]),
    'bio_izvor': lambda v: v,
    'bio_datum_izracuna': lambda v: _datum(v, 'bio_datum_izracuna'),
}


def ucitaj_csv(tekst):
    """CSV текст → (колоне које фајл носи, редови као речници). Грешке → ValueError."""
    citac = csv.DictReader(io.StringIO(tekst.lstrip('﻿')))
    zaglavlje = [k.strip() for k in (citac.fieldnames or [])]
    if 'id' not in zaglavlje:
        raise ValueError('CSV нема колону „id“')
    kolone = tuple(k for k in KOLONE if k in zaglavlje)
    if not kolone:
        raise ValueError('CSV нема ниједну колону контекста (ни свеске 12 ни 13)')
    if ('lat' in kolone) != ('lon' in kolone):
        raise ValueError('CSV мора имати и lat и lon, или ниједну')
    redovi = [{(k or '').strip(): (v or '').strip() for k, v in red.items()} for red in citac]
    return kolone, redovi


def validiraj_redove(kolone, redovi):
    """Претвори вредности по колонама; празно = NULL. Враћа (по_id, грешке)."""
    po_id, greske = {}, []
    for br, red in enumerate(redovi, start=2):
        sirov_id = red.get('id', '')
        if not re.fullmatch(r'\d+', sirov_id) or int(sirov_id) <= 0:
            greske.append(f'ред {br}: id „{sirov_id}“ није позитиван цео број')
            continue
        oid = int(sirov_id)
        if oid in po_id:
            greske.append(f'ред {br}: id {oid} се понавља')
            continue
        vrednosti = {}
        for k in kolone:
            v = red.get(k, '')
            if v == '':
                vrednosti[k] = None
                continue
            try:
                vrednosti[k] = _PRETVARANJE[k](v)
            except ValueError as exc:
                greske.append(f'ред {br} (id {oid}): {exc}')
        if 'lat' in kolone and (vrednosti.get('lat') is None or vrednosti.get('lon') is None):
            greske.append(f'ред {br} (id {oid}): lat/lon су обавезни')
        od, do = vrednosti.get('gubitak_od'), vrednosti.get('gubitak_do')
        if od is not None and do is not None and od > do:
            greske.append(f'ред {br} (id {oid}): gubitak_od {od} > gubitak_do {do}')
        po_id[oid] = vrednosti
    return po_id, greske


# ---------------------------------------------------------------------------
# Приказ у детаљу примерка
# ---------------------------------------------------------------------------

_LISTOVI = None


def _normalizuj_list(sifra):
    m = re.fullmatch(r'([KL])-?34-0*(\d{1,3})', (sifra or '').strip())
    return f'{m.group(1)}34-{int(m.group(2)):02d}' if m else None


def naziv_lista(sifra):
    """Назив листа OGK из data/geological_map_sheets.json (K34-3 и K34-03 су исти лист)."""
    global _LISTOVI
    if _LISTOVI is None:
        putanja = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'geological_map_sheets.json')
        try:
            with open(putanja, encoding='utf-8') as f:
                _LISTOVI = {_normalizuj_list(s.get('ogk_code')): s.get('name') for s in json.load(f)}
        except (OSError, ValueError) as exc:
            logger.warning('Листови OGK нису учитани: %s', exc)
            _LISTOVI = {}
    return _LISTOVI.get(_normalizuj_list(sifra))


_POLJA_CITANJA = ('vrsta', 'objekat_id', 'lat', 'lon') + KOLONE[2:]


def _za_prikaz(red):
    k = dict(zip(_POLJA_CITANJA, red))
    klasa = k.get('pokrivac_klasa')
    k['pokrivac_naziv'] = DW_NAZIVI[DW_KLASE[klasa]] if klasa is not None else None
    k['ogk_naziv'] = naziv_lista(k.get('ogk_list')) if k.get('ogk_list') else None
    udeli = k.get('dw_udeli') or {}
    k['dw_udeli_prikaz'] = [(DW_NAZIVI[c], udeli[c]) for c in sorted(udeli, key=lambda c: -udeli[c])
                            if c in DW_NAZIVI and udeli[c] > 0]
    return k


def kontekst_za_mineral(mineral_id, card_locality=None):
    """Ред за примерак; ако га нема — ред локалитета чији је назив = card_locality."""
    try:
        from postgres_service import get_postgres_connection
        kolone = ', '.join(f'k.{p}' for p in _POLJA_CITANJA)
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT to_regclass('public.lokalitet_kontekst')")
                if cur.fetchone()[0] is None:
                    return None
                cur.execute(f"SELECT {kolone} FROM lokalitet_kontekst k "
                            "WHERE k.vrsta = 'mineral' AND k.objekat_id = %s", (mineral_id,))
                red = cur.fetchone()
                if red is None and card_locality and card_locality.strip():
                    cur.execute(f"SELECT {kolone} FROM lokalitet_kontekst k JOIN localities l "
                                "ON k.vrsta = 'lokalitet' AND k.objekat_id = l.id WHERE l.name = %s",
                                (card_locality.strip(),))
                    red = cur.fetchone()
        return _za_prikaz(red) if red else None
    except Exception as exc:
        logger.warning('Контекст локалитета за минерал %s није прочитан: %s', mineral_id, exc)
        return None
