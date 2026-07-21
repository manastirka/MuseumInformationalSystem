"""`flask uvezi-arhivske-liste <folder> [--korisnik EMAIL_LOKALNI]` — масовни
архивски увоз радних листа из Word-а (.doc/.docx), рекурзивно кроз подфолдере.

Исти парсер и АРХИВСКА логика као веб (`timesheet_uvoz_views` / `timesheet_import`):
уписује као ОДОБРЕНЕ архивске листе (`imported_from='word-arhiva'`).

  flask uvezi-arhivske-liste "/put/до/архива"                 # DRY-RUN (извештај)
  flask uvezi-arhivske-liste "/put/до/архива" --execute       # тражи име базе
  flask uvezi-arhivske-liste "/put" --korisnik aca.lukovic    # власник кад име не мапира

Понашање:
  * DRY-RUN подразумеван — табела по фајлу (месец/година, статус OK/прескочен+разлог),
    зборно по години. --execute уписује уз куцање имена базе.
  * --korisnik (локални део мејла) поставља власника КАД име из фајла не може да се
    мапира (placeholder/латиница). Ако парсер нађе име које се поклапа са ДРУГИМ
    корисником — УПОЗОРИ, не прегази тихо.
  * ДУПЛИКАТИ: ако листа за (корисник, месец, година) већ постоји (у бази или у
    истом покретању — постоје и .doc и .docx исте листе) — прескочи с ознаком.
  * Фајлови који нису месечне листе (годишњи извештаји…) се прескачу с разлогом.
"""

import os
from urllib.parse import urlsplit

import click

from postgres_service import get_database_url, get_postgres_connection
import radna_lista_word_parser as parser
import timesheet_import as tsimport

_EXTS = ('.doc', '.docx')
_DEFAULT_DOMAIN = 'nhmbeo.rs'


def _database_name():
    return urlsplit(get_database_url()).path.lstrip('/') or '?'


def _resolve_korisnik(korisnik):
    if not korisnik:
        return None
    k = korisnik.strip()
    return k if '@' in k else f'{k}@{_DEFAULT_DOMAIN}'


def _discover(folder):
    out = []
    for root, _dirs, files in os.walk(folder):
        for name in files:
            if name.lower().endswith(_EXTS) and not name.startswith('~$'):
                out.append(os.path.join(root, name))
    return sorted(out)


def _resolve_owner(match, korisnik_email):
    """Врати (owner_email, warn). owner из имена ако се поуздано мапира; иначе
    --korisnik. Ако име мапира на ДРУГОГ корисника него --korisnik → warn."""
    if match['confident'] and match['email']:
        warn = None
        if korisnik_email and korisnik_email.lower() != match['email'].lower():
            warn = (f'име у фајлу → {match["email"]}, --korisnik → {korisnik_email}; '
                    f'користим име из фајла')
        return match['email'], warn
    if korisnik_email:
        return korisnik_email, None
    return None, None


def plan_import(folder, korisnik_email, cur):
    """Прегледај фолдер и врати листу резултата по фајлу (без уписа)."""
    seen = set()  # (email, month, year) виђено у овом покретању
    results = []
    for path in _discover(folder):
        rel = os.path.relpath(path, folder)
        try:
            parsed = parser.parse_radna_lista(path)
        except parser.RadnaListaParseError as exc:
            results.append({'file': rel, 'ok': False,
                            'razlog': f'није месечна листа ({exc})'})
            continue
        month, year = parsed['month'], parsed['year']
        match = tsimport.match_employee(cur, parsed.get('employee_name'))
        owner, warn = _resolve_owner(match, korisnik_email)
        base = {'file': rel, 'mesec': month, 'godina': year,
                'ime': parsed.get('employee_name'), 'owner': owner, 'warn': warn}
        if not owner:
            results.append({**base, 'ok': False,
                            'razlog': 'име се не мапира — задај --korisnik'})
            continue
        key = (owner.lower(), month, year)
        if key in seen or tsimport._find_report(cur, owner, parsed.get('employee_name'),
                                                month, year):
            results.append({**base, 'ok': False,
                            'razlog': 'дупликат (месец за корисника већ постоји)'})
            continue
        seen.add(key)
        results.append({**base, 'ok': True, 'parsed': parsed})
    return results


def register_cli(app):
    @app.cli.command('uvezi-arhivske-liste')
    @click.argument('folder')
    @click.option('--korisnik', default=None,
                  help='Локални део мејла власника кад име из фајла не мапира.')
    @click.option('--execute', is_flag=True,
                  help='Стварно упиши (подразумевано dry-run).')
    def uvezi_arhivske_liste(folder, korisnik, execute):
        """Масовни архивски увоз радних листа из фолдера (рекурзивно)."""
        if not os.path.isdir(folder):
            raise click.ClickException(f'Фолдер не постоји: {folder}')
        mode = 'EXECUTE' if execute else 'DRY-RUN (без измена)'
        korisnik_email = _resolve_korisnik(korisnik)
        click.echo(f'=== uvezi-arhivske-liste — {mode} — база: {_database_name()} ===')
        if korisnik_email:
            click.echo(f'--korisnik: {korisnik_email}')

        with get_postgres_connection() as conn, conn.cursor() as cur:
            results = plan_import(folder, korisnik_email, cur)

        _print_report(results)
        ok_items = [r for r in results if r['ok']]
        if not execute:
            click.echo(f'\nDry-run: ништа није уписано. За упис {len(ok_items)}: --execute')
            return
        if not ok_items:
            click.echo('\nНема ставки за упис.')
            return

        db_name = _database_name()
        odgovor = click.prompt(
            f'\nПОТВРДА: за упис откуцај тачно име базе ({db_name!r})',
            default='', show_default=False)
        if odgovor != db_name:
            raise click.ClickException('Име базе се не поклапа — прекид, без измена.')

        upisano = 0
        for r in ok_items:
            ok, _msg, _rid = tsimport.import_archive(
                r['parsed'], r['owner'], r['ime'], f'cli-arhiva@{_DEFAULT_DOMAIN}')
            if ok:
                upisano += 1
        click.echo(f'\nУписано архивских листа: {upisano}')


def _print_report(results):
    click.echo(f'\nФајлова: {len(results)}')
    click.echo(f'{"фајл":50} {"мес/год":9} {"статус"}')
    click.echo('-' * 80)
    for r in results:
        mg = f'{r.get("mesec","?")}/{r.get("godina","?")}' if r.get('mesec') else '—'
        if r['ok']:
            status = f'OK → {r["owner"]}'
            if r.get('warn'):
                status += f'  ⚠ {r["warn"]}'
        else:
            status = f'ПРЕСКОЧЕН: {r["razlog"]}'
        click.echo(f'{r["file"][:50]:50} {mg:9} {status}')

    # Зборно по години.
    by_year = {}
    for r in results:
        y = r.get('godina') or 'непознато'
        d = by_year.setdefault(y, {'ok': 0, 'skip': 0})
        d['ok' if r['ok'] else 'skip'] += 1
    click.echo('\nЗборно по години:')
    for y in sorted(by_year, key=lambda x: str(x)):
        click.echo(f'  {y}: OK {by_year[y]["ok"]}, прескочено {by_year[y]["skip"]}')
