#!/usr/bin/env python3
"""Ordered, idempotent PostgreSQL migration runner for MuseumInfoSystem.

Applies migration/NNN_*.sql files in filename order, exactly once each, tracked
in a schema_migrations table. Safe to re-run. Requires DATABASE_URL.

Commands:
    python deploy/run_migrations.py status        # show applied vs pending
    python deploy/run_migrations.py apply          # DRY RUN: print the plan
                                                    #   (host, database, files)
    python deploy/run_migrations.py apply --execute --database mis_db
                                                    # actually run pending files
                                                    #   (--applied-log <fajl>:
                                                    #   upiši svaki primenjen fajl,
                                                    #   za rollback poruku deploja)
    python deploy/run_migrations.py baseline        # DRY RUN: verify schema vs
                                                    #   files, show what would be
                                                    #   marked applied
    python deploy/run_migrations.py baseline --execute --database mis_db
    python deploy/run_migrations.py mark <glob>... --execute --database mis_db
                                                    # mark matching file(s) applied
                                                    #   without running them
    python deploy/run_migrations.py remap           # dry-run: show old->new filename
                                                    #   rows in schema_migrations
    python deploy/run_migrations.py remap --execute --database mis_db

Svaka komanda koja MENJA bazu je podrazumevano dry-run (ispis plana, nula
izmena). Izmena traži --execute I --database <ime> — ime mora da se poklopi
sa current_database(), da apply/baseline nikad ne pogodi pogrešnu bazu.

New server after restoring a pg_dump (schema already in the dump):
    python deploy/run_migrations.py baseline --execute --database <ime>
    # future schema changes then run with 'apply --execute --database <ime>'
"""

import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MIGRATION_DIR = REPO / 'migration'

# 2026-08: duplicate NNN_ prefixes (002/003/004/005 each existed twice or three
# times) were renamed to unique, strictly increasing numbers; 006..040 shifted
# by +5. Databases that applied migrations under the old names keep those names
# in schema_migrations — this map rewrites them so nothing is re-applied.
# 'apply' runs the remap automatically; 'remap' does it explicitly (dry-run by
# default).
RENAMES = {
    '002_timesheet_schema_fixes.sql': '003_timesheet_schema_fixes.sql',
    '003_exhibition_access_control.sql': '004_exhibition_access_control.sql',
    '003_fix_sync_trigger.sql': '005_fix_sync_trigger.sql',
    '004_archive_verification_system.sql': '006_archive_verification_system.sql',
    '004_timesheet_audit_log.sql': '007_timesheet_audit_log.sql',
    '005_digital_signatures.sql': '008_digital_signatures.sql',
    '005_optimize_sync_trigger.sql': '009_optimize_sync_trigger.sql',
    '005_user_notifications.sql': '010_user_notifications.sql',
    '006_timesheet_status_workflow.sql': '011_timesheet_status_workflow.sql',
    '007_remaining_sqlite_runtime_to_postgres.sql': '012_remaining_sqlite_runtime_to_postgres.sql',
    '008_add_color_ring_to_bird_ringing_records.sql': '013_add_color_ring_to_bird_ringing_records.sql',
    '009_timesheet_report_integrity.sql': '014_timesheet_report_integrity.sql',
    '010_create_sanja_table.sql': '015_create_sanja_table.sql',
    '011_create_digitized_profiles_table.sql': '016_create_digitized_profiles_table.sql',
    '012_update_collection_type_icons.sql': '017_update_collection_type_icons.sql',
    '013_add_is_department_head_to_employee_profiles.sql': '018_add_is_department_head_to_employee_profiles.sql',
    '014_add_vehicle_specs.sql': '019_add_vehicle_specs.sql',
    '015_user_dashboard_config.sql': '020_user_dashboard_config.sql',
    '016_fix_vehicle_reservations_legacy_status.sql': '021_fix_vehicle_reservations_legacy_status.sql',
    '017_document_library.sql': '022_document_library.sql',
    '018_operativni_zahtevi_odobravanje.sql': '023_operativni_zahtevi_odobravanje.sql',
    '019_fototeka.sql': '024_fototeka.sql',
    '020_fototeka_bez_derivata.sql': '025_fototeka_bez_derivata.sql',
    '021_fototeka_vidljivost.sql': '026_fototeka_vidljivost.sql',
    '022_user_theme_preference.sql': '027_user_theme_preference.sql',
    '023_theme_contrast_mode.sql': '028_theme_contrast_mode.sql',
    '024_default_theme_light.sql': '029_default_theme_light.sql',
    '025_user_style_density.sql': '030_user_style_density.sql',
    '026_fototeka_uvoz_log.sql': '031_fototeka_uvoz_log.sql',
    '027_localities_registry.sql': '032_localities_registry.sql',
    '028_uvoz_run_veze.sql': '033_uvoz_run_veze.sql',
    '029_prijemni_red_iz_stanja.sql': '034_prijemni_red_iz_stanja.sql',
    '030_kr_dosije.sql': '035_kr_dosije.sql',
    '031_timesheet_import_source.sql': '036_timesheet_import_source.sql',
    '032_global_audit_log.sql': '037_global_audit_log.sql',
    '033_theme_palette.sql': '038_theme_palette.sql',
    '034_dvostepeno_odobrenje.sql': '039_dvostepeno_odobrenje.sql',
    '035_administrativno_odobrenje_i_arhiva.sql': '040_administrativno_odobrenje_i_arhiva.sql',
    '036_employee_email_not_null.sql': '041_employee_email_not_null.sql',
    '037_teme_faza2.sql': '042_teme_faza2.sql',
    '038_teme_faza3_custom.sql': '043_teme_faza3_custom.sql',
    '039_knjiga_vs_depo.sql': '044_knjiga_vs_depo.sql',
    '040_posete_i_istrazivacki_projekti.sql': '045_posete_i_istrazivacki_projekti.sql',
}


def discover_migrations():
    """Return migration filenames in deterministic (filename) order."""
    return sorted(p.name for p in MIGRATION_DIR.glob('*.sql'))


def _connect():
    sys.path.insert(0, str(REPO))
    from postgres_service import get_postgres_connection
    return get_postgres_connection()


def _ensure_table(cur):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            filename   TEXT PRIMARY KEY,
            applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )


def _tracking_table_exists(cur):
    cur.execute("SELECT to_regclass('public.schema_migrations') IS NOT NULL")
    return bool(cur.fetchone()[0])


def _applied(cur):
    # Dry-run putanje ne smeju ni da naprave tabelu evidencije — bez tabele
    # jednostavno ništa nije primenjeno.
    if not _tracking_table_exists(cur):
        return set()
    cur.execute("SELECT filename FROM schema_migrations")
    return {row[0] for row in cur.fetchall()}


def _current_database(cur):
    cur.execute("SELECT current_database()")
    return cur.fetchone()[0]


def _target_host():
    url = os.environ.get('DATABASE_URL', '')
    rest = url.split('://', 1)[-1]
    hostpart = rest.split('/', 1)[0]
    return (hostpart.rsplit('@', 1)[-1] or 'localhost') or 'localhost'


def _print_target(cur):
    print(f"Cilj: host={_target_host()}  baza={_current_database(cur)}")


def _require_database_match(cur, database):
    """Potvrda imena baze uz --execute: --database mora = current_database()."""
    current = _current_database(cur)
    if not database:
        print("ODBIJENO: izmena baze traži --execute I --database <ime> "
              f"(current_database() je „{current}“).")
        return False
    if database != current:
        print(f"ODBIJENO: --database {database} ≠ current_database() "
              f"„{current}“ — pogrešna baza ili pogrešan DATABASE_URL.")
        return False
    return True


def _pending_renames(cur):
    """Return (old, new) pairs for old filenames still present in schema_migrations."""
    applied = _applied(cur)
    return [(old, new) for old, new in RENAMES.items() if old in applied]


def _apply_renames(cur):
    """Rewrite old filenames in schema_migrations to their new names.

    Idempotent: if the new name is already recorded, the old row is deleted
    instead of creating a duplicate. Returns the number of rows changed.
    """
    changed = 0
    for old, new in _pending_renames(cur):
        cur.execute("SELECT 1 FROM schema_migrations WHERE filename = %s", (new,))
        if cur.fetchone():
            cur.execute("DELETE FROM schema_migrations WHERE filename = %s", (old,))
        else:
            cur.execute(
                "UPDATE schema_migrations SET filename = %s WHERE filename = %s",
                (new, old),
            )
        changed += 1
    return changed


def cmd_status():
    conn = _connect()
    try:
        cur = conn.cursor()
        _print_target(cur)
        renames = _pending_renames(cur)
        if renames:
            print(f"NOTE: {len(renames)} old filename(s) in schema_migrations need remap")
            print("      (run 'apply' or 'remap --execute'):")
            for old, new in renames:
                print(f"        {old} -> {new}")
            print()
        applied = _applied(cur)
        files = discover_migrations()
        for f in files:
            print(f"  [{'x' if f in applied else ' '}] {f}")
        pending = [f for f in files if f not in applied]
        print(f"\n{len(applied)} applied, {len(pending)} pending.")
        return 0
    finally:
        conn.close()


def _log_applied(applied_log, filename):
    """Upiši primenjen fajl u evidenciju pokušaja (za rollback poruku deploja)."""
    if not applied_log:
        return
    try:
        with open(applied_log, 'a', encoding='utf-8') as fh:
            fh.write(filename + '\n')
    except OSError as exc:
        print(f"  UPOZORENJE: ne mogu da upišem {applied_log}: {exc}")


def cmd_apply(execute, database, applied_log=None):
    conn = _connect()
    try:
        cur = conn.cursor()
        _print_target(cur)
        renames = _pending_renames(cur)
        applied = _applied(cur)
        pending = [f for f in discover_migrations() if f not in applied]

        # Plan se štampa UVEK, pre ijedne izmene.
        if renames:
            print(f"Remap {len(renames)} starih imena u schema_migrations:")
            for old, new in renames:
                print(f"  {old} -> {new}")
        if pending:
            print(f"Za primenu ({len(pending)}):")
            for f in pending:
                print(f"  {f}")
        elif not renames:
            print("Nothing to apply; database is up to date.")

        if not pending and not renames:
            return 0

        if not execute:
            print("\nDRY RUN: ništa NIJE primenjeno. Deploy NIJE završen — "
                  "pokreni ponovo sa --execute --database <ime baze> da bi se "
                  "migracije stvarno primenile.")
            return 2
        if not _require_database_match(cur, database):
            return 1

        _ensure_table(cur)
        conn.commit()
        renamed = _apply_renames(cur)
        if renamed:
            conn.commit()
            print(f"Remapped {renamed} renamed migration filename(s) in schema_migrations.")
            applied = _applied(cur)
            pending = [f for f in discover_migrations() if f not in applied]
        for f in pending:
            sql = (MIGRATION_DIR / f).read_text(encoding='utf-8')
            print(f"Applying {f} ...")
            try:
                cur.execute(sql)
                cur.execute("INSERT INTO schema_migrations(filename) VALUES (%s)", (f,))
                conn.commit()
                _log_applied(applied_log, f)
            except Exception as exc:
                conn.rollback()
                print(f"  FAILED on {f}: {exc}")
                print("  Stopped. Fix the migration, or 'mark' it if it was already applied.")
                return 1
        print(f"Applied {len(pending)} migration(s).")
        return 0
    finally:
        conn.close()


# baseline sme da označi fajl primenjenim samo ako šema stvarno izgleda kao
# posle te migracije. Potpuna provera je nemoguća generički — proveravamo ono
# što se iz SQL-a pouzdano čita: CREATE TABLE mora da postoji, ALTER TABLE
# ... ADD COLUMN mora da postoji. Fajl bez proverivih objekata (čisti
# UPDATE/INSERT) se prijavi kao neproveriv, ali ne obara baseline.
_CREATE_TABLE_RE = re.compile(
    r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?("?[\w.]+"?)', re.I)
_ADD_COLUMN_RE = re.compile(
    r'ALTER\s+TABLE\s+(?:IF\s+EXISTS\s+)?(?:ONLY\s+)?("?[\w.]+"?)\s+'
    r'ADD\s+(?:COLUMN\s+)?(?:IF\s+NOT\s+EXISTS\s+)?'
    r'(?!CONSTRAINT\b|PRIMARY\b|FOREIGN\b|UNIQUE\b|CHECK\b|EXCLUDE\b)'
    r'("?\w+"?)', re.I)


def _bare(name):
    return name.strip('"').split('.')[-1].lower()


def _verify_schema_for(cur, filename):
    """Return (problems, checked) for one migration file."""
    sql = (MIGRATION_DIR / filename).read_text(encoding='utf-8')
    problems, checked = [], 0
    for match in _CREATE_TABLE_RE.finditer(sql):
        table = _bare(match.group(1))
        checked += 1
        cur.execute("SELECT to_regclass(%s) IS NOT NULL", (f'public.{table}',))
        if not cur.fetchone()[0]:
            problems.append(f"tabela {table} ne postoji")
    for match in _ADD_COLUMN_RE.finditer(sql):
        table, column = _bare(match.group(1)), _bare(match.group(2))
        checked += 1
        cur.execute(
            """
            SELECT 1 FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s AND column_name = %s
            """,
            (table, column),
        )
        if not cur.fetchone():
            problems.append(f"kolona {table}.{column} ne postoji")
    return problems, checked


def cmd_baseline(execute, database):
    conn = _connect()
    try:
        cur = conn.cursor()
        _print_target(cur)
        files = discover_migrations()
        applied = _applied(cur)
        to_mark = [f for f in files if f not in applied]
        bad, unverifiable = [], []
        for f in to_mark:
            problems, checked = _verify_schema_for(cur, f)
            if problems:
                bad.append((f, problems))
            elif not checked:
                unverifiable.append(f)
        print(f"Baseline bi označio {len(to_mark)} fajl(ova) kao primenjene "
              f"({len(applied)} već evidentirano).")
        for f in unverifiable:
            print(f"  ? {f} — nema proverivih objekata (čisti data-SQL)")
        if bad:
            print("ODBIJENO: šema NE odgovara sledećim migracijama — baseline "
                  "bi lagao da su primenjene:")
            for f, problems in bad:
                for p in problems:
                    print(f"  ! {f}: {p}")
            return 1
        if not execute:
            print("\nDRY RUN: ništa nije menjano. Za upis dodaj "
                  "--execute --database <ime baze>.")
            return 0
        if not _require_database_match(cur, database):
            return 1
        _ensure_table(cur)
        for f in files:
            cur.execute(
                "INSERT INTO schema_migrations(filename) VALUES (%s) ON CONFLICT DO NOTHING",
                (f,),
            )
        conn.commit()
        print(f"Baselined {len(files)} migration file(s) as applied (not run).")
        return 0
    finally:
        conn.close()


def cmd_mark(patterns, execute, database):
    if not patterns:
        print("Usage: mark <glob> [<glob> ...] --execute --database <ime>")
        return 1
    conn = _connect()
    try:
        cur = conn.cursor()
        _print_target(cur)
        files = discover_migrations()
        matched = []
        for pattern in patterns:
            for f in files:
                if (f == pattern or Path(f).match(pattern)) and f not in matched:
                    matched.append(f)
        for f in matched:
            print(f"  would mark {f}")
        if not execute:
            print(f"\nDRY RUN: {len(matched)} fajl(ova) bi bilo označeno. "
                  "Za upis dodaj --execute --database <ime baze>.")
            return 0
        if not _require_database_match(cur, database):
            return 1
        _ensure_table(cur)
        for f in matched:
            cur.execute(
                "INSERT INTO schema_migrations(filename) VALUES (%s) ON CONFLICT DO NOTHING",
                (f,),
            )
        conn.commit()
        print(f"Marked {len(matched)} file(s) as applied (not run).")
        return 0
    finally:
        conn.close()


def cmd_remap(execute, database):
    conn = _connect()
    try:
        cur = conn.cursor()
        _print_target(cur)
        renames = _pending_renames(cur)
        if not renames:
            print("No old migration filenames in schema_migrations; nothing to remap.")
            return 0
        applied = _applied(cur)
        for old, new in renames:
            action = 'delete old row (new name already recorded)' if new in applied else 'rename'
            print(f"  {old} -> {new}  [{action}]")
        if not execute:
            print(f"\nDRY RUN: {len(renames)} row(s) would be changed. "
                  "Re-run with --execute --database <ime baze> to apply.")
            return 0
        if not _require_database_match(cur, database):
            return 1
        changed = _apply_renames(cur)
        conn.commit()
        print(f"\nRemapped {changed} row(s) in schema_migrations.")
        return 0
    finally:
        conn.close()


def main():
    # Load DATABASE_URL (and friends) from the repo .env if not already exported.
    try:
        from dotenv import load_dotenv
        load_dotenv(REPO / '.env')
    except Exception:
        pass
    if not os.environ.get('DATABASE_URL'):
        print("DATABASE_URL is not set; refusing to run.")
        return 1
    args = sys.argv[1:]
    execute = '--execute' in args
    database = None
    if '--database' in args:
        idx = args.index('--database')
        if idx + 1 >= len(args):
            print("--database traži ime baze odmah iza sebe.")
            return 1
        database = args[idx + 1]
        del args[idx:idx + 2]
    applied_log = None
    if '--applied-log' in args:
        idx = args.index('--applied-log')
        if idx + 1 >= len(args):
            print("--applied-log traži putanju fajla odmah iza sebe.")
            return 1
        applied_log = args[idx + 1]
        del args[idx:idx + 2]
    args = [a for a in args if a != '--execute']
    cmd = args[0] if args else 'status'
    if cmd == 'status':
        return cmd_status()
    if cmd == 'apply':
        return cmd_apply(execute, database, applied_log)
    if cmd == 'baseline':
        return cmd_baseline(execute, database)
    if cmd == 'mark':
        return cmd_mark(args[1:], execute, database)
    if cmd == 'remap':
        return cmd_remap(execute, database)
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
