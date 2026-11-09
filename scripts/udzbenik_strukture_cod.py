#!/usr/bin/env python3
"""Кристалне структуре за уџбеник из Crystallography Open Database (COD) → база.

    python scripts/udzbenik_strukture_cod.py                       # dry-run, сви минерали
    python scripts/udzbenik_strukture_cod.py --mineral halit --mineral kvarc
    python scripts/udzbenik_strukture_cod.py --execute --baza museum_system --uvezao ko@nhmbeo.rs

Један извор истине је табела ``udzbenik_struktura`` (миграција 061), не
фајлови. За сваки минерал из MINERALI:
1. упит COD-у (``/cod/result?text=<en>&el1=..&strictmin/strictmax=<број
   елемената>&format=json``), па филтер: тачан назив минерала, резултат са
   координатама, идеална формула (чист крајњи члан, без хидратације и
   делимичних заузетости), дозвољена просторна група/политип, собна
   температура и нормалан притисак (без податка или ~293 K / ≤ 0,2 MPa) и
   параметри ћелије у оквиру ±0,5 % од референтних — то хвата загрејане и
   компримоване ћелије које у CIF-у немају T/P;
2. редослед: прво AMCSD записи (9xxxxxx), па новији;
3. CIF се преузима (``/cod/<id>.cif``), шири у P1 (kristalografija.py — исти
   облик као некадашњи generate_cif_from_dif(expand_unitcell=True)) и
   проверава број атома по ћелији (Z × формула); ако било шта не прође,
   следећи кандидат.

Подразумевано dry-run: табела изабраних записа. Упис тек уз ``--execute
--baza <ime>`` (потврда = дословно име базе, као у udzbenik_uvoz.py).
Поновни упис је идемпотентан (исти COD id + исти P1 → „исто“, без измене).
``--kes DIR`` чува/чита преузете JSON и CIF фајлове (тестови га користе са
tests/fixtures/cod, без мреже).
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import kristalografija  # noqa: E402

COD_URL = 'https://www.crystallography.net/cod'
POKUSAJA = 3
TIMEOUT = 90
SOBNA_T = (285.0, 305.0)       # K
NORMALAN_P_KPA = 200.0         # ≤ 0,2 MPa (COD држи kPa; 0 = амбијент)
TOLERANCIJA_CELIJE = 0.005

# Референтне ћелије (Å) су собне вредности из литературе; упоређују се сортиране
# дужине, па Pbnm/Pnma пермутација форстерита пролази.
MINERALI = {
    'bakar': dict(en='Copper', elementi=('Cu',), formula={'Cu': 1}, grupe=('Fm-3m',), celija=(3.615, 3.615, 3.615)),
    'beril': dict(en='Beryl', elementi=('Be', 'Al', 'Si', 'O'), formula={'Be': 3, 'Al': 2, 'Si': 6, 'O': 18},
                  grupe=('P6/mcc',), celija=(9.21, 9.21, 9.19)),
    'dijamant': dict(en='Diamond', elementi=('C',), formula={'C': 1}, grupe=('Fd-3m', 'Fd-3m:1', 'Fd-3m:2'),
                     celija=(3.567, 3.567, 3.567)),
    'fluorit': dict(en='Fluorite', elementi=('Ca', 'F'), formula={'Ca': 1, 'F': 2}, grupe=('Fm-3m',),
                    celija=(5.463, 5.463, 5.463)),
    'forsterit': dict(en='Forsterite', elementi=('Mg', 'Si', 'O'), formula={'Mg': 2, 'Si': 1, 'O': 4},
                      grupe=('Pbnm', 'Pnma'), celija=(4.755, 10.20, 5.98)),
    'galenit': dict(en='Galena', elementi=('Pb', 'S'), formula={'Pb': 1, 'S': 1}, grupe=('Fm-3m',),
                    celija=(5.936, 5.936, 5.936)),
    'grafit': dict(en='Graphite', elementi=('C',), formula={'C': 1}, grupe=('P63/mmc',),
                   celija=(2.464, 2.464, 6.711), napomena='2H'),
    'halit': dict(en='Halite', elementi=('Na', 'Cl'), formula={'Na': 1, 'Cl': 1}, grupe=('Fm-3m',),
                  celija=(5.640, 5.640, 5.640)),
    'halkopirit': dict(en='Chalcopyrite', elementi=('Cu', 'Fe', 'S'), formula={'Cu': 1, 'Fe': 1, 'S': 2},
                       grupe=('I-42d',), celija=(5.289, 5.289, 10.423)),
    'kalcit': dict(en='Calcite', elementi=('Ca', 'C', 'O'), formula={'Ca': 1, 'C': 1, 'O': 3},
                   grupe=('R-3c', 'R-3c:H'), celija=(4.99, 4.99, 17.06)),
    'kvarc': dict(en='Quartz', elementi=('Si', 'O'), formula={'Si': 1, 'O': 2}, grupe=('P3221', 'P3121'),
                  celija=(4.913, 4.913, 5.405), napomena='α-кварц'),
    'magnetit': dict(en='Magnetite', elementi=('Fe', 'O'), formula={'Fe': 3, 'O': 4},
                     grupe=('Fd-3m', 'Fd-3m:1', 'Fd-3m:2'), celija=(8.396, 8.396, 8.396)),
    'olivin': dict(en='Olivine', elementi=('Mg', 'Si', 'O'), formula={'Mg': 2, 'Si': 1, 'O': 4},
                   grupe=('Pbnm', 'Pnma'), celija=(4.755, 10.20, 5.98), upit='Forsterite',
                   napomena='крајњи члан форстерит'),
    'pirit': dict(en='Pyrite', elementi=('Fe', 'S'), formula={'Fe': 1, 'S': 2}, grupe=('Pa-3',),
                  celija=(5.417, 5.417, 5.417)),
    'rutil': dict(en='Rutile', elementi=('Ti', 'O'), formula={'Ti': 1, 'O': 2}, grupe=('P42/mnm',),
                  celija=(4.594, 4.594, 2.959)),
    'sfalerit': dict(en='Sphalerite', elementi=('Zn', 'S'), formula={'Zn': 1, 'S': 1}, grupe=('F-43m',),
                     celija=(5.409, 5.409, 5.409), napomena='кубни ZnS'),
    'talk': dict(en='Talc', elementi=('Mg', 'Si', 'O', 'H'), formula={'Mg': 3, 'Si': 4, 'O': 12, 'H': 2},
                 grupe=('C-1', 'P-1'), celija=(5.29, 9.17, 9.46)),
    'muskovit': dict(en='Muscovite', elementi=('K', 'Al', 'Si', 'O', 'H'),
                     formula={'K': 1, 'Al': 3, 'Si': 3, 'O': 12, 'H': 2}, grupe=('C12/c1', 'C2/c'),
                     celija=(5.19, 9.03, 20.05), napomena='2M1'),
}


# --------------------------------------------------------------------------
# COD — мрежа (са кешом)
# --------------------------------------------------------------------------

def _sesija():
    import requests

    s = requests.Session()
    s.headers['Accept-Encoding'] = 'identity'   # chunked+gzip са COD-а уме да пукне усред одговора
    s.headers['User-Agent'] = 'MIS-udzbenik strukture (Prirodnjacki muzej u Beogradu)'
    return s


def _preuzmi(url, params, kes_putanja):
    if kes_putanja is not None and kes_putanja.exists():
        return kes_putanja.read_text(encoding='utf-8')
    sesija = _sesija()
    greska = None
    for pokusaj in range(POKUSAJA):
        try:
            r = sesija.get(url, params=params, timeout=TIMEOUT)
            r.raise_for_status()
            tekst = r.text
            break
        except Exception as exc:  # noqa: BLE001 - пробај поново, па пријави
            greska = exc
            time.sleep(2 * (pokusaj + 1))
    else:
        raise RuntimeError(f'COD не одговара ({url}): {greska}')
    if kes_putanja is not None:
        kes_putanja.parent.mkdir(parents=True, exist_ok=True)
        kes_putanja.write_text(tekst, encoding='utf-8')
    return tekst


def preuzmi_rezultate(upit, elementi, kes=None):
    """JSON листа COD записа за упит (назив минерала) ограничен на тачно те елементе."""
    params = {'text': upit, 'format': 'json', 'strictmin': len(elementi), 'strictmax': len(elementi)}
    for i, el in enumerate(elementi, 1):
        params[f'el{i}'] = el
    putanja = (Path(kes) / f'{upit.lower()}.json') if kes else None
    return json.loads(_preuzmi(f'{COD_URL}/result', params, putanja))


def preuzmi_cif(cod_id, kes=None):
    putanja = (Path(kes) / f'{cod_id}.cif') if kes else None
    return _preuzmi(f'{COD_URL}/{cod_id}.cif', None, putanja)


# --------------------------------------------------------------------------
# Избор записа
# --------------------------------------------------------------------------

def normalizuj_grupu(hm):
    return re.sub(r'\s+', '', str(hm or '')).replace(':h', ':H').replace(':r', ':R')


def formula_iz_teksta(tekst):
    """COD 'formula' ('- Cl Na -') или CIF formula_sum → {el: količina}."""
    return {el: float(n) if n else 1.0 for el, n in kristalografija._FORMULA_CLAN.findall(str(tekst or ''))
            if el in kristalografija.ELEMENTI}


def ista_formula(formula, idealna):
    return set(formula) == set(idealna) and all(abs(formula[el] - idealna[el]) < 1e-6 for el in idealna)


def _broj(v):
    try:
        return None if v in (None, '') else float(v)
    except (TypeError, ValueError):
        return None


def ambijentalni(zapis):
    t = _broj(zapis.get('celltemp')) or _broj(zapis.get('diffrtemp'))
    p = _broj(zapis.get('cellpressure'))
    if p is None:
        p = _broj(zapis.get('diffrpressure'))
    if t is not None and not SOBNA_T[0] <= t <= SOBNA_T[1]:
        return False
    return p is None or p <= NORMALAN_P_KPA


def celija_odgovara(zapis, referentna):
    duzine = [_broj(zapis.get(k)) for k in 'abc']
    if any(d is None for d in duzine):
        return False
    return all(abs(d - r) <= TOLERANCIJA_CELIJE * r for d, r in zip(sorted(duzine), sorted(referentna)))


def razlog_odbijanja(zapis, spec):
    """None ако запис пролази све филтере, иначе кратак разлог."""
    ime = (zapis.get('mineral') or '').strip().lower()
    trazeno = (spec.get('upit') or spec['en']).lower()
    if ime != trazeno:
        return f'назив минерала {zapis.get("mineral")!r}'
    if 'has coordinates' not in str(zapis.get('flags') or ''):
        return 'без координата'
    if not ista_formula(formula_iz_teksta(zapis.get('formula')), spec['formula']):
        return f'формула {zapis.get("formula")!r}'
    if normalizuj_grupu(zapis.get('sg')) not in spec['grupe']:
        return f'просторна група {zapis.get("sg")!r}'
    if not ambijentalni(zapis):
        t = zapis.get('celltemp') or zapis.get('diffrtemp')
        return f'T={t} P={zapis.get("cellpressure") or zapis.get("diffrpressure")}'
    if not celija_odgovara(zapis, spec['celija']):
        return f'ћелија a={zapis.get("a")} b={zapis.get("b")} c={zapis.get("c")} ван ±0,5 % од референтне'
    return None


def izaberi_kandidate(spec, zapisi):
    """Записи који пролазе филтере, најбољи први: AMCSD (9xxxxxx) па новији."""
    prolaze = [z for z in zapisi if razlog_odbijanja(z, spec) is None]
    return sorted(prolaze, key=lambda z: (0 if str(z.get('file', '')).startswith('9') else 1,
                                          -int(_broj(z.get('year')) or 0), int(z.get('file') or 0)))


def pripremi_strukturu(slug, spec, kes=None, ispis=print):
    """(запис, cif_izvorni, cif_p1, podaci) првог кандидата чији CIF прође
    ширење и проверу броја атома, или None (са исписаним разлозима)."""
    upit = spec.get('upit') or spec['en']
    zapisi = preuzmi_rezultate(upit, spec['elementi'], kes)
    kandidati = izaberi_kandidate(spec, zapisi)
    if not kandidati:
        ispis(f'  ! {slug}: ниједан од {len(zapisi)} COD записа не пролази филтере')
        for z in zapisi[:8]:
            ispis(f'      - {z.get("file")}: {razlog_odbijanja(z, spec)}')
        return None
    for zapis in kandidati:
        cod_id = int(zapis['file'])
        try:
            cif_izvorni = preuzmi_cif(cod_id, kes)
            cif_p1, podaci = kristalografija.struktura_p1(cif_izvorni, slug)
            grupa_cif = normalizuj_grupu(podaci['prostorna_grupa'])
            if grupa_cif not in spec['grupe']:
                raise kristalografija.CifGreska(f'просторна група у CIF-у {podaci["prostorna_grupa"]!r}')
            if not ista_formula(podaci['formula'], spec['formula']):
                raise kristalografija.CifGreska(f'формула у CIF-у {podaci["formula"]!r}')
        except (kristalografija.CifGreska, RuntimeError, ValueError) as exc:
            ispis(f'  ! {slug}: COD {cod_id} одбачен — {exc}')
            continue
        return zapis, cif_izvorni, cif_p1, podaci
    return None


# --------------------------------------------------------------------------
# База
# --------------------------------------------------------------------------

def navod(citat):
    delovi = [', '.join(citat.get('autori') or []) or '—']
    if citat.get('godina'):
        delovi[0] += f' ({citat["godina"]})'
    if citat.get('casopis'):
        delovi.append(citat['casopis'] + (f' {citat["tom"]}' if citat.get('tom') else '')
                      + (f', {citat["strane"]}' if citat.get('strane') else ''))
    if citat.get('doi'):
        delovi.append(f'doi:{citat["doi"]}')
    return '; '.join(delovi)


def postojeci(cur, slug):
    cur.execute('SELECT cod_id, cif_p1 FROM udzbenik_struktura WHERE mineral = %s', (slug,))
    red = cur.fetchone()
    return (red[0], red[1]) if red else None


def upisi(cur, slug, spec, zapis, cif_izvorni, cif_p1, podaci, uvezao):
    """Upsert по slug-у; враћа 'dodaje' / 'menja' / 'isto'."""
    staro = postojeci(cur, slug)
    cod_id = int(zapis['file'])
    if staro == (cod_id, cif_p1):
        return 'isto'
    cur.execute(
        """INSERT INTO udzbenik_struktura (mineral, naziv_en, izvor, cod_id, cif_izvorni, cif_p1, citat, uslovi, uvezao)
           VALUES (%s, %s, 'COD', %s, %s, %s, %s::jsonb, %s::jsonb, %s)
           ON CONFLICT (mineral) DO UPDATE SET
               naziv_en = EXCLUDED.naziv_en, cod_id = EXCLUDED.cod_id, cif_izvorni = EXCLUDED.cif_izvorni,
               cif_p1 = EXCLUDED.cif_p1, citat = EXCLUDED.citat, uslovi = EXCLUDED.uslovi,
               uvezeno_at = now(), uvezao = EXCLUDED.uvezao""",
        (slug, spec['en'], cod_id, cif_izvorni, cif_p1, json.dumps(podaci['citat'], ensure_ascii=False),
         json.dumps(podaci['uslovi'], ensure_ascii=False), uvezao))
    return 'dodaje' if staro is None else 'menja'


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _argumenti(argv):
    p = argparse.ArgumentParser(description='Кристалне структуре (COD → P1) за уџбеник; подразумевано dry-run.')
    p.add_argument('--mineral', action='append', metavar='SLUG', help='само ови минерали (понављати)')
    p.add_argument('--kes', metavar='DIR', help='директоријум за преузете JSON/CIF фајлове (читање и упис)')
    p.add_argument('--execute', action='store_true', help='стварно упиши у базу')
    p.add_argument('--baza', metavar='IME_BAZE', help='потврда: дословно име базе на коју је скрипта повезана')
    p.add_argument('--uvezao', default=None, help='e-mail за колону uvezao')
    return p.parse_args(argv)


def main(argv=None):
    arg = _argumenti(argv)
    if arg.execute and not arg.baza:
        print('ГРЕШКА: --execute тражи и --baza <ime>.', file=sys.stderr)
        return 2
    slugovi = arg.mineral or list(MINERALI)
    nepoznati = [s for s in slugovi if s not in MINERALI]
    if nepoznati:
        print(f'ГРЕШКА: непознат минерал {nepoznati}; дозвољено {list(MINERALI)}', file=sys.stderr)
        return 2

    from postgres_service import get_postgres_connection

    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT current_database()')
            baza = cur.fetchone()[0]
            print(f'База: {baza}  режим: {"EXECUTE" if arg.execute else "dry-run"}  минерала: {len(slugovi)}')
            cur.execute("SELECT to_regclass('public.udzbenik_struktura')")
            if cur.fetchone()[0] is None:
                print('ГРЕШКА: нема табеле udzbenik_struktura — прво миграција 061 (deploy/run_migrations.py).',
                      file=sys.stderr)
                conn.rollback()
                return 2
            if arg.execute and arg.baza != baza:
                print(f'ГРЕШКА: --baza тражи дословно име базе „{baza}“ (добијено {arg.baza!r}).', file=sys.stderr)
                conn.rollback()
                return 2
            redovi, neuspeli = [], []
            for slug in slugovi:
                spec = MINERALI[slug]
                rezultat = pripremi_strukturu(slug, spec, arg.kes)
                if rezultat is None:
                    neuspeli.append(slug)
                    continue
                zapis, cif_izvorni, cif_p1, podaci = rezultat
                akcija = upisi(cur, slug, spec, zapis, cif_izvorni, cif_p1, podaci, arg.uvezao) if arg.execute \
                    else ('isto' if postojeci(cur, slug) == (int(zapis['file']), cif_p1) else 'dodaje/menja')
                c = podaci['celija']
                redovi.append((slug, int(zapis['file']), podaci['prostorna_grupa'],
                               f"{c['a']:.3f} {c['b']:.3f} {c['c']:.3f}", podaci['broj_atoma'], akcija,
                               navod(podaci['citat']), spec.get('napomena', '')))
            if arg.execute and not neuspeli:
                conn.commit()
            else:
                conn.rollback()

    print(f'{"mineral":<11} {"COD":>8} {"grupa":<12} {"a b c (Å)":<22} {"atoma":>5} {"akcija":<13} navod')
    for r in redovi:
        print(f'{r[0]:<11} {r[1]:>8} {str(r[2]):<12} {r[3]:<22} {r[4]:>5} {r[5]:<13} {r[6]}'
              + (f'  [{r[7]}]' if r[7] else ''))
    if neuspeli:
        print(f'НЕУСПЕЛО ({len(neuspeli)}): {", ".join(neuspeli)} — ништа није уписано.', file=sys.stderr)
        return 1
    print('Уписано у базу.' if arg.execute else 'Dry-run: ништа није уписано (за упис: --execute --baza <ime>).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
