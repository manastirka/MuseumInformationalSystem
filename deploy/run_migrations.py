#!/usr/bin/env python3
"""Ordered, idempotent PostgreSQL migration runner for MuseumInfoSystem.

Applies migration/NNN_*.sql files in filename order, exactly once each, tracked
in a schema_migrations table. Safe to re-run. Requires DATABASE_URL.

Commands:
    python deploy/run_migrations.py status        # show applied vs pending
    python deploy/run_migrations.py apply          # run all pending, in order
    python deploy/run_migrations.py baseline        # mark ALL current files as
                                                    #   applied WITHOUT running them
    python deploy/run_migrations.py mark <glob>...  # mark matching file(s) applied
                                                    #   without running them
    python deploy/run_migrations.py remap           # dry-run: show old->new filename
                                                    #   rows in schema_migrations
    python deploy/run_migrations.py remap --execute # rewrite those rows

New server after restoring a pg_dump (schema already in the dump):
    python deploy/run_migrations.py baseline               # mark everything applied
    # future schema changes then run with 'apply'
"""

import os
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


def _applied(cur):
    cur.execute("SELECT filename FROM schema_migrations")
    return {row[0] for row in cur.fetchall()}


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
        _ensure_table(cur)
        conn.commit()
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


def cmd_apply():
    conn = _connect()
    try:
        cur = conn.cursor()
        _ensure_table(cur)
        conn.commit()
        renamed = _apply_renames(cur)
        if renamed:
            conn.commit()
            print(f"Remapped {renamed} renamed migration filename(s) in schema_migrations.")
        applied = _applied(cur)
        pending = [f for f in discover_migrations() if f not in applied]
        if not pending:
            print("Nothing to apply; database is up to date.")
            return 0
        for f in pending:
            sql = (MIGRATION_DIR / f).read_text(encoding='utf-8')
            print(f"Applying {f} ...")
            try:
                cur.execute(sql)
                cur.execute("INSERT INTO schema_migrations(filename) VALUES (%s)", (f,))
                conn.commit()
            except Exception as exc:
                conn.rollback()
                print(f"  FAILED on {f}: {exc}")
                print("  Stopped. Fix the migration, or 'mark' it if it was already applied.")
                return 1
        print(f"Applied {len(pending)} migration(s).")
        return 0
    finally:
        conn.close()


def cmd_baseline():
    conn = _connect()
    try:
        cur = conn.cursor()
        _ensure_table(cur)
        files = discover_migrations()
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


def cmd_mark(patterns):
    if not patterns:
        print("Usage: mark <glob> [<glob> ...]")
        return 1
    conn = _connect()
    try:
        cur = conn.cursor()
        _ensure_table(cur)
        files = discover_migrations()
        marked = 0
        for pattern in patterns:
            for f in files:
                if f == pattern or Path(f).match(pattern):
                    cur.execute(
                        "INSERT INTO schema_migrations(filename) VALUES (%s) ON CONFLICT DO NOTHING",
                        (f,),
                    )
                    print(f"  marked {f}")
                    marked += 1
        conn.commit()
        print(f"Marked {marked} file(s) as applied (not run).")
        return 0
    finally:
        conn.close()


def cmd_remap(args):
    execute = '--execute' in args
    conn = _connect()
    try:
        cur = conn.cursor()
        _ensure_table(cur)
        conn.commit()
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
                  "Re-run with --execute to apply.")
            return 0
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
    cmd = args[0] if args else 'status'
    if cmd == 'status':
        return cmd_status()
    if cmd == 'apply':
        return cmd_apply()
    if cmd == 'baseline':
        return cmd_baseline()
    if cmd == 'mark':
        return cmd_mark(args[1:])
    if cmd == 'remap':
        return cmd_remap(args[1:])
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
