"""`flask reset-test-data` — praznjenje probnih (test) podataka pred user testiranje.

Podrazumevano ponasanje je dry-run: izvestaj sta bi bilo obrisano (imenovane
tabele + broj redova + fajlovi na disku), bez ikakvih izmena. Stvarno brisanje
radi tek `--execute`, uz interaktivnu potvrdu kucanjem imena baze. Brisanje je
transakciono (jedan TRUNCATE ... RESTART IDENTITY), pa se sekvence resetuju.

Spisak tabela potvrdio korisnik 2026-07-08 (Korak 0 iz ~/zadatak-reset.md).
"""

import os
from pathlib import Path
from urllib.parse import urlsplit

import click

from postgres_service import get_database_url, get_postgres_connection

# Tabele koje se prazne — deca pre roditelja (FK redosled); TRUNCATE ih uzima
# sve u jednoj naredbi, a redosled ovde odredjuje i redosled u izvestaju.
RESET_TABLES = [
    # Dokumenta — modul iz migracije 017 + digitalni potpisi dokumenata
    'signature_audit_log',
    'document_signatures',
    'document_audit_log',
    'document_versions',
    'documents',
    # Zahtevi + tok odobravanja + arhiva (migracije 004 + 018)
    'request_comments',
    'request_history',
    'approval_signatures',
    'procurement_requests',
    'archive_requests',
    # Radne liste / mesecni izvestaji
    'timesheet_edit_requests',
    'timesheet_status_history',
    'timesheet_report_days',
    'timesheet_entries',
    'timesheet_audit_log',
    'timesheet_reports',
    # Rezervacije vozila (tabela vehicles kao entitet OSTAJE)
    'vehicle_reservations',
    # Korisnicki tragovi testiranja
    'user_dashboard_config',
    'user_notifications',
    'user_sessions',
    'user_activity_log',
    'audit_log',
    # Chat
    'chat_messages',
    'chat_presence',
    'chat_unread_cursors',
    # Probni unosi (odluka korisnika 2026-07-08)
    'financial_plans',
    'geo_field_data',
    # Mail kes (mail_user_settings OSTAJE)
    'mail_cache_pending_reads',
    'mail_cache_messages',
    'mail_cache_folders',
    'mail_cache_meta',
]

# Institucionalne tabele — komanda ih NIKAD ne dira. Zastitni test u
# test_reset_test_data.py proverava da nijedna nije u RESET_TABLES niti u
# izvrsenom SQL-u. Biblioteka (ustanova) je zasticena isto kao zbirke.
PROTECTED_TABLES = [
    # Zbirke i naucni podaci
    'bilja_hydrobioidea_radoman',
    'bilja_kenozojske_invertebrate',
    'bilja_opsta_zbirka_mollusca',
    'bilja_recentni_morski_mekusci',
    'bilja_skoljke_tadic',
    'bilja_suvozemni_puzevi_pavlovic',
    'sanja_paleogene_neogene_mammals',
    'minerals',
    'mineral_references',
    'mineral_rruff_matches',
    'rruff_chemistry',
    'rruff_localities',
    'rruff_minerals',
    'rruff_references',
    'meteorite_specimens',
    'collection_specimens',
    'collection_types',
    'inventory_entries',
    'bird_ringing_records',
    'bird_species',
    'digitized_profiles',
    'images',
    'heritage_categories',
    'heritage_items',
    'heritage_types',
    # Biblioteka i bibliografija
    'library_books',
    'library_categories',
    'library_loans',
    'employee_publications',
    'scientific_papers',
    'paper_locality_links',
    'paper_feature_links',
    # Ljudi, nalozi, role, odeljenja, dozvole
    'users',
    'roles',
    'departments',
    'employee_profiles',
    'user_module_permissions',
    # Entiteti i podesavanja
    'vehicles',
    'signature_templates',
    'app_shared_settings',
    'mail_user_settings',
    'schema_migrations',
    'spatial_ref_sys',
    'staging_bird_ringing',
    'staging_inventory',
    'staging_minerals',
    'staging_timesheet_days',
    'staging_timesheet_reports',
    # Sadrzaj sajta (stvarne vesti i izlozbe, ne test)
    'news_articles',
    'exhibitions',
    'exhibition_items',
    'exhibition_events',
]


def _database_name():
    """Ime baze iz DATABASE_URL — sluzi za interaktivnu potvrdu."""
    return urlsplit(get_database_url()).path.lstrip('/')


def _documents_root():
    return Path(os.environ.get('DOCUMENTS_STORAGE_PATH', './data/dokumenti'))


def _chat_files_root():
    from chat_room import CHAT_FILES_DIR
    return Path(CHAT_FILES_DIR)


def _dir_inventory(root):
    """(broj fajlova, ukupno bajtova) rekurzivno pod root; (0, 0) ako ne postoji."""
    if not root.is_dir():
        return 0, 0
    files = [p for p in root.rglob('*') if p.is_file()]
    return len(files), sum(p.stat().st_size for p in files)


def _clear_directory(root):
    """Obrisi sav sadrzaj direktorijuma, a sam direktorijum ostavi."""
    import shutil

    if not root.is_dir():
        return
    for entry in root.iterdir():
        if entry.is_dir() and not entry.is_symlink():
            shutil.rmtree(entry)
        else:
            entry.unlink()


def _existing_tables(cur):
    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
    return {row[0] for row in cur.fetchall()}


def _table_counts(cur):
    counts = {}
    for table in RESET_TABLES:
        cur.execute(f'SELECT count(*) FROM "{table}"')
        counts[table] = cur.fetchone()[0]
    return counts


def _print_report(counts, file_targets, execute):
    mode = 'EXECUTE' if execute else 'DRY-RUN (bez izmena)'
    click.echo(f'=== reset-test-data — {mode} — baza: {_database_name()} ===')
    click.echo('Tabele koje komanda prazni (TRUNCATE ... RESTART IDENTITY):')
    for table in RESET_TABLES:
        click.echo(f'  - {table:<28} {counts[table]:>8} redova')
    total = sum(counts.values())
    click.echo(f'UKUPNO: {total} redova u {len(RESET_TABLES)} tabela')
    click.echo('Fajlovi na disku (brise se sadrzaj, direktorijum ostaje):')
    for label, root, n_files, n_bytes in file_targets:
        click.echo(f'  - {label}: {root} — {n_files} fajlova ({n_bytes} B)')
    click.echo(
        'NE diraju se: institucionalne tabele (zbirke, biblioteka, zaposleni, '
        'nalozi, role, odeljenja, vozila, podesavanja), mail_user_settings.'
    )
    return total


def register_cli(app):
    @app.cli.command('reset-test-data')
    @click.option(
        '--execute',
        is_flag=True,
        help='Stvarno obrisi podatke (podrazumevano je dry-run izvestaj).',
    )
    def reset_test_data(execute):
        """Isprazni probne (test) podatke pred user testiranje."""
        overlap = set(RESET_TABLES) & set(PROTECTED_TABLES)
        if overlap:
            raise RuntimeError(
                f'RESET_TABLES sadrzi zasticene tabele: {sorted(overlap)}'
            )

        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                missing = set(RESET_TABLES) - _existing_tables(cur)
                if missing:
                    raise click.ClickException(
                        'U bazi ne postoje tabele iz spiska (migracije nisu '
                        f'primenjene?): {sorted(missing)} — prekid, bez izmena.'
                    )
                counts = _table_counts(cur)

        documents_root = _documents_root()
        chat_root = _chat_files_root()
        file_targets = [
            ('dokumenta (017)', documents_root, *_dir_inventory(documents_root)),
            ('chat prilozi', chat_root, *_dir_inventory(chat_root)),
        ]

        _print_report(counts, file_targets, execute)

        if not execute:
            click.echo('Dry-run: nista nije izmenjeno. Za brisanje: --execute')
            return

        db_name = _database_name()
        answer = click.prompt(
            f'POTVRDA: za brisanje otkucaj tacno ime baze ({db_name!r})',
            default='',
            show_default=False,
        )
        if answer != db_name:
            raise click.ClickException('Ime baze se ne poklapa — prekid, bez izmena.')

        quoted = ', '.join(f'"{table}"' for table in RESET_TABLES)
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'TRUNCATE TABLE {quoted} RESTART IDENTITY')

        removed_files = 0
        for _label, root, n_files, _n_bytes in file_targets:
            _clear_directory(root)
            removed_files += n_files

        click.echo(
            f'GOTOVO: obrisano {sum(counts.values())} redova iz '
            f'{len(RESET_TABLES)} tabela, {removed_files} fajlova sa diska; '
            'sekvence resetovane (RESTART IDENTITY).'
        )
        click.echo('Institucionalne i bibliotecke tabele nisu dirane.')
