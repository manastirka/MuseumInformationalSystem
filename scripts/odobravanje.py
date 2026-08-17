#!/usr/bin/env python3
"""Прекидачи одобравања из командне линије.

Постоји и дугме у админ панелу; ово је исти механизам, за случај кад
страница не ради и за упис у скрипту. Оба пишу у иста `system_settings`.

    python3 scripts/odobravanje.py stanje
    python3 scripts/odobravanje.py iskljuci izvestaji
    python3 scripts/odobravanje.py iskljuci izvestaji --execute
    python3 scripts/odobravanje.py ukljuci dokumenti --execute

Подразумевано је DRY RUN: испише шта би се променило и не дира ништа.
Гашење затвара и оно што ВЕЋ чека одобрење — зато dry-run прво каже колико
је то редова.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

KOREN = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOREN))

try:
    from dotenv import load_dotenv
    load_dotenv(KOREN / '.env')
except Exception:
    pass

import odobravanje_prekidac as prekidac  # noqa: E402
import odobravanje_razresavanje as razresavanje  # noqa: E402

# Трећа ставка нема шта да разрешава — рок није ред који чека, него правило.
TOKOVI = {
    'izvestaji': (prekidac.KLJUC_IZVESTAJI, 'месечни извештаји (радне листе)',
                  prekidac.odobravanje_izvestaja_ukljuceno),
    'dokumenti': (prekidac.KLJUC_DOKUMENTI, 'библиотека докумената',
                  prekidac.odobravanje_dokumenata_ukljuceno),
    'rok': (prekidac.KLJUC_ROK, 'рок предаје (до 10. у наредном месецу)',
            prekidac.rok_predaje_ukljucen),
    'verifikacija': (prekidac.KLJUC_VERIFIKACIJA,
                     'правна верификација у Архиви',
                     prekidac.verifikacija_arhive_ukljucena),
}


def _stanje() -> int:
    s = prekidac.stanje()
    print('Одобравање:')
    for ime, (kljuc, opis, _) in TOKOVI.items():
        print(f"  {ime:<11} {'УКЉУЧЕНО' if s[kljuc] else 'ИСКЉУЧЕНО'}   {opis}")
    preklop = {k: v for k, v in s['env_preklop'].items() if v is not None}
    if preklop:
        print('\nПРЕКЛОП ИЗ ОКРУЖЕЊА (јачи од подешавања у бази):')
        for k, v in preklop.items():
            print(f"  {k} = {'укључено' if v else 'искључено'}")
    try:
        z = razresavanje.prebroj_zatecene()
        print(f"\nЧека одобрење: {z['izvestaji']} радних листа, "
              f"{z['dokumenti']} верзија докумената")
    except Exception as exc:
        print(f"\nБрој затечених се не може прочитати: {exc}", file=sys.stderr)
        return 1
    return 0


def _postavi(tok: str, ukljuceno: bool, izvrsi: bool) -> int:
    kljuc, opis, procitaj = TOKOVI[tok]
    trenutno = procitaj()

    print(f"Ток: {opis}")
    print(f"Сада: {'УКЉУЧЕНО' if trenutno else 'ИСКЉУЧЕНО'}"
          f"  →  тражено: {'УКЉУЧЕНО' if ukljuceno else 'ИСКЉУЧЕНО'}")
    if trenutno == ukljuceno:
        print('Ништа се не мења.')
        return 0

    posao = None
    # Само та два тока имају ред који чека; рок и верификација су правила.
    if not ukljuceno and tok in ('izvestaji', 'dokumenti'):
        posao = (razresavanje.razresi_izvestaje if tok == 'izvestaji'
                 else razresavanje.razresi_dokumente)
        pregled = posao('dry-run', izvrsi=False)
        if tok == 'izvestaji':
            print(f"Затворило би се радних листа: {pregled['pronadjeno']}")
        else:
            print(f"Верзија на чекању: {pregled['verzija_na_cekanju']}, "
                  f"постаје важећих: {pregled['dokumenata']}")

    if not izvrsi:
        print('\nDRY RUN: ништа није промењено. Додај --execute.')
        return 0

    import admin_system_views
    podesavanja = admin_system_views.load_saved_settings(force=True) or {}
    podesavanja[kljuc] = ukljuceno
    if not admin_system_views.save_settings(podesavanja):
        print('НЕУСПЕХ: подешавање није уписано — прекидач НИЈЕ промењен.',
              file=sys.stderr)
        return 1
    print(f"Прекидач уписан: {kljuc} = {ukljuceno}")

    if posao is not None:
        try:
            rezultat = posao('cli', izvrsi=True)
        except Exception as exc:
            # Прекидач је већ уписан — не сме да испадне да ништа није урађено.
            print(f"\nПРЕКИДАЧ ЈЕ УПИСАН, али разрешавање затечених није "
                  f"прошло: {exc}", file=sys.stderr)
            print(f"Затечене ставке и даље чекају. Понови исту команду када "
                  f"разрешиш узрок.", file=sys.stderr)
            return 1
        print(f"Разрешено затечених: {rezultat['promenjeno']}")
    elif tok not in ('rok', 'verifikacija'):
        print('Затечени редови се НЕ враћају у ред за одобрење — оно што је '
              'већ затворено остаје затворено.')
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    pod = p.add_subparsers(dest='naredba')
    pod.add_parser('stanje', help='шта је сада укључено')
    for ime in ('ukljuci', 'iskljuci'):
        s = pod.add_parser(ime, help=f'{ime} одобравање за један ток')
        s.add_argument('tok', choices=sorted(TOKOVI))
        s.add_argument('--execute', action='store_true',
                       help='заиста промени (без овога: dry-run)')
    a = p.parse_args()

    if a.naredba == 'stanje' or a.naredba is None:
        return _stanje()
    return _postavi(a.tok, a.naredba == 'ukljuci', a.execute)


if __name__ == '__main__':
    raise SystemExit(main())
