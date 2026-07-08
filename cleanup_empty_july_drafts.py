"""`flask cleanup-empty-july-drafts` — ukloni prazne julske DRAFT radne liste.

Posledica buga u podrazumevanom mesecu za unos (pre e4f642a): posle reseta,
`render_timesheet_entry()` je na svako otvaranje preko `ensure_draft_exists`
INSERT-ovao prazan DRAFT za JUL 2026 (tekuci mesec) umesto za jun. Ova komanda
brise iskljucivo te prazne ljuske i NE dira nijednu listu sa unetim danima.

Kriterijum brisanja (tacno po dogovoru):
  month=7, year=2026, status='DRAFT', is_verified=FALSE, is_locked=FALSE,
  I bez ijednog reda u timesheet_report_days I bez ijednog u timesheet_entries.

Podrazumevano je dry-run (broj + spisak ID-jeva, bez izmena). `--execute`
trazi kucanje imena baze pa radi JEDAN transakcioni DELETE; FK deca su
ON DELETE CASCADE, a audit trigger upise 'DELETE' trag u timesheet_audit_log.
Filter je u samom DELETE ... WHERE (NOT EXISTS), pa konkurentan unos ne moze
da dovede do brisanja u medjuvremenu popunjene liste.
"""

from urllib.parse import urlsplit

import click

from postgres_service import get_database_url, get_postgres_connection

TARGET_MONTH = 7
TARGET_YEAR = 2026

# Zajednicki uslov za dry-run SELECT i za DELETE — jedan izvor istine, da se
# pregled i stvarno brisanje ne mogu razici.
_EMPTY_DRAFT_PREDICATE = """
    r.month = %s AND r.year = %s
    AND r.status = 'DRAFT'
    AND r.is_verified = FALSE
    AND r.is_locked = FALSE
    AND NOT EXISTS (
        SELECT 1 FROM timesheet_report_days d WHERE d.report_id = r.id
    )
    AND NOT EXISTS (
        SELECT 1 FROM timesheet_entries e WHERE e.report_id = r.id
    )
"""


def _database_name():
    return urlsplit(get_database_url()).path.lstrip('/')


def _find_empty_drafts(cur):
    cur.execute(
        f"""
        SELECT r.id, r.employee_name, r.employee_email, r.created_at
        FROM timesheet_reports r
        WHERE {_EMPTY_DRAFT_PREDICATE}
        ORDER BY r.id
        """,
        (TARGET_MONTH, TARGET_YEAR),
    )
    return cur.fetchall()


def register_cli(app):
    @app.cli.command('cleanup-empty-july-drafts')
    @click.option(
        '--execute',
        is_flag=True,
        help='Stvarno obrisi prazne julske DRAFT liste (podrazumevano dry-run).',
    )
    def cleanup_empty_july_drafts(execute):
        """Ukloni prazne DRAFT radne liste za JUL 2026 (posledica buga)."""
        mode = 'EXECUTE' if execute else 'DRY-RUN (bez izmena)'
        click.echo(
            f'=== cleanup-empty-july-drafts — {mode} — baza: {_database_name()} ==='
        )
        click.echo(
            f'Kriterijum: month={TARGET_MONTH} year={TARGET_YEAR}, status=DRAFT, '
            'is_verified=FALSE, is_locked=FALSE, bez unetih dana i entries.'
        )

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                candidates = _find_empty_drafts(cur)

        if not candidates:
            click.echo('Nema praznih julskih DRAFT listi — nista za brisanje.')
            return

        click.echo(f'Kandidati za brisanje ({len(candidates)}):')
        for row in candidates:
            report_id, name, email, created_at = row[0], row[1], row[2], row[3]
            click.echo(
                f'  - id={report_id:<6} {name or email or "?"} '
                f'(kreirano {created_at})'
            )

        if not execute:
            click.echo(
                f'Dry-run: nista nije izmenjeno. Za brisanje {len(candidates)} '
                'listi: --execute'
            )
            return

        db_name = _database_name()
        answer = click.prompt(
            f'POTVRDA: za brisanje otkucaj tacno ime baze ({db_name!r})',
            default='',
            show_default=False,
        )
        if answer != db_name:
            raise click.ClickException('Ime baze se ne poklapa — prekid, bez izmena.')

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"DELETE FROM timesheet_reports r WHERE {_EMPTY_DRAFT_PREDICATE}",
                    (TARGET_MONTH, TARGET_YEAR),
                )
                deleted = cur.rowcount

        click.echo(
            f'GOTOVO: obrisano {deleted} praznih julskih DRAFT listi '
            '(FK deca kaskadno, audit trag upisan). Liste sa unetim danima '
            'nisu dirane.'
        )
