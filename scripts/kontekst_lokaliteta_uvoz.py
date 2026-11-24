#!/usr/bin/env python3
"""Увоз контекста локалитета (GEE) из CSV-а у lokalitet_kontekst (миграција 066).

Употреба::

    python scripts/kontekst_lokaliteta_uvoz.py --fajl 12-kontekst-lokaliteta-izlaz.csv
    python scripts/kontekst_lokaliteta_uvoz.py --fajl 12-kontekst-lokaliteta-izlaz.csv \\
        --execute museum_system --autor ko@nhmbeo.rs
    python scripts/kontekst_lokaliteta_uvoz.py --fajl 13-bio-stanista-izlaz.csv --execute museum_system

Правила:

- CSV је излаз свеске 12-kontekst-lokaliteta (id, lat, lon, висина, нагиб,
  покривач, лист OGK, извор, датум) или 13-bio-stanista (шума 2000, губитак,
  удели Dynamic World, bio_izvor, bio_datum_izracuna); колоне по уговору у
  /tmp/petro/colab/rad/BRIF-GEE.md. Ажурирају се САМО колоне које фајл носи —
  увоз 13 не дира поља из 12 и обрнуто; празна ћелија = NULL (непознато);
- ``id`` је ``minerals.id`` (подразумевано) или ``localities.id``
  (``--vrsta lokalitet``); непостојећи објекат, понављен id, лоша вредност
  — ГРЕШКА, ништа се не упише;
- нов ред тражи lat/lon (дакле прво CSV свеске 12);
- подразумевано је dry-run (испис плана, нула измена); ``--execute <ime baze>``
  (дословно ``current_database()``) ради све у ЈЕДНОЈ трансакцији.
"""
import argparse
import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from lokalitet_kontekst import VRSTE, ucitaj_csv, validiraj_redove  # noqa: E402

TABELA_VRSTE = {'mineral': 'minerals', 'lokalitet': 'localities'}


def _argumenti(argv):
    p = argparse.ArgumentParser(description='Увоз контекста локалитета (GEE) из CSV-а.')
    p.add_argument('--fajl', required=True, help='CSV из свеске 12 или 13')
    p.add_argument('--vrsta', choices=VRSTE, default='mineral',
                   help='на шта показује id (подразумевано: mineral = minerals.id)')
    p.add_argument('--execute', metavar='IME_BAZE',
                   help='изврши упис; тражи дословно име базе (иначе dry-run)')
    p.add_argument('--autor', help='е-адреса кустоса који увози (uvezao_email)')
    return p.parse_args(argv)


def _isto(stara, nova):
    """Иста вредност у бази и у CSV-у (REAL у бази је float4 — 1e-4 релативно је исто)."""
    if stara is None or nova is None:
        return stara is nova
    if isinstance(nova, dict):
        return isinstance(stara, dict) and stara.keys() == nova.keys() and all(
            _isto(stara[k], nova[k]) for k in nova)
    if isinstance(nova, float) and not isinstance(stara, str):
        return abs(float(stara) - nova) <= 1e-4 * max(1.0, abs(nova))
    return stara == nova


def napravi_plan(cur, vrsta, kolone, po_id):
    """Упореди са базом: нов / измењен / исти. Враћа (plan, грешке)."""
    greske = []
    ids = sorted(po_id)
    cur.execute(f'SELECT id FROM {TABELA_VRSTE[vrsta]} WHERE id = ANY(%s)', (ids,))
    postoje = {r[0] for r in cur.fetchall()}
    for oid in ids:
        if oid not in postoje:
            greske.append(f'id {oid}: нема га у {TABELA_VRSTE[vrsta]}')
    cur.execute(f"SELECT objekat_id, {', '.join(kolone)} FROM lokalitet_kontekst "
                'WHERE vrsta = %s AND objekat_id = ANY(%s)', (vrsta, ids))
    u_bazi = {r[0]: dict(zip(kolone, r[1:])) for r in cur.fetchall()}
    plan = {'novi': [], 'izmenjeni': [], 'isti': []}
    for oid in ids:
        if oid not in postoje:
            continue
        nove = po_id[oid]
        if oid not in u_bazi:
            if 'lat' not in kolone:
                greske.append(f'id {oid}: нема реда контекста, а CSV нема lat/lon — прво увези CSV свеске 12')
                continue
            plan['novi'].append(oid)
            continue
        stare = u_bazi[oid]
        isti = all(_isto(stare[k], nove[k]) for k in kolone)
        plan['isti' if isti else 'izmenjeni'].append(oid)
    return plan, greske


def _vrednost(v):
    return json.dumps(v, ensure_ascii=False) if isinstance(v, dict) else v


def primeni_plan(cur, vrsta, kolone, po_id, plan, autor):
    for oid in plan['novi']:
        polja = ('vrsta', 'objekat_id') + kolone + ('uvezao_email',)
        vrednosti = [vrsta, oid] + [_vrednost(po_id[oid][k]) for k in kolone] + [autor]
        cur.execute(f"INSERT INTO lokalitet_kontekst ({', '.join(polja)}) "
                    f"VALUES ({', '.join(['%s'] * len(polja))})", vrednosti)
    for oid in plan['izmenjeni']:
        dodela = ', '.join(f'{k} = %s' for k in kolone)
        cur.execute(f'UPDATE lokalitet_kontekst SET {dodela}, uvezao_email = COALESCE(%s, uvezao_email), '
                    'updated_at = NOW() WHERE vrsta = %s AND objekat_id = %s',
                    [_vrednost(po_id[oid][k]) for k in kolone] + [autor, vrsta, oid])


def ispisi_plan(plan, kolone, izvrseno):
    print(f"Колоне: {', '.join(kolone)}")
    print(f"Редова: {sum(len(v) for v in plan.values())} "
          f"(+{len(plan['novi'])} ~{len(plan['izmenjeni'])} ={len(plan['isti'])})")
    if izvrseno:
        print('ИЗВРШЕНО: упис је потврђен (commit).')
    else:
        print('DRY-RUN: ништа није промењено. За упис: --execute <име базе>')


def main(argv=None):
    arg = _argumenti(argv)
    izvrsavanje = arg.execute is not None
    try:
        tekst = Path(arg.fajl).read_text(encoding='utf-8')
        kolone, redovi = ucitaj_csv(tekst)
    except (OSError, UnicodeDecodeError, ValueError, csv.Error) as exc:
        print(f'ГРЕШКА: CSV се не може прочитати: {exc}', file=sys.stderr)
        return 2
    po_id, greske = validiraj_redove(kolone, redovi)

    from postgres_service import get_postgres_connection

    with get_postgres_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute('SELECT current_database()')
                baza = cur.fetchone()[0]
                print(f'База: {baza}  фајл: {arg.fajl}  врста: {arg.vrsta}  '
                      f'режим: {"EXECUTE" if izvrsavanje else "dry-run"}')
                if izvrsavanje and arg.execute != baza:
                    print(f'ГРЕШКА: --execute тражи дословно име базе „{baza}“ (добијено {arg.execute!r}).',
                          file=sys.stderr)
                    conn.rollback()
                    return 2
                cur.execute("SELECT to_regclass('public.lokalitet_kontekst')")
                if cur.fetchone()[0] is None:
                    print('ГРЕШКА: нема табеле lokalitet_kontekst — прво миграција 066.', file=sys.stderr)
                    conn.rollback()
                    return 2
                plan, greske_baze = napravi_plan(cur, arg.vrsta, kolone, po_id) if po_id else (
                    {'novi': [], 'izmenjeni': [], 'isti': []}, [])
                greske += greske_baze
                if not redovi:
                    greske.append('CSV нема ниједан ред')
                if greske:
                    print(f'ГРЕШКЕ ({len(greske)}) — ништа није уписано:', file=sys.stderr)
                    for g in greske:
                        print(f'  - {g}', file=sys.stderr)
                    conn.rollback()
                    return 1
                if izvrsavanje:
                    primeni_plan(cur, arg.vrsta, kolone, po_id, plan, arg.autor)
            if izvrsavanje:
                conn.commit()
            else:
                conn.rollback()
        except Exception:
            conn.rollback()
            raise
    ispisi_plan(plan, kolone, izvrsavanje)
    return 0


if __name__ == '__main__':
    sys.exit(main())
