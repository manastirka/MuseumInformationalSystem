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

First run on the EXISTING database (it already has the 001..007 schema):
    python deploy/run_migrations.py mark '00[1-7]_*.sql'   # baseline what's there
    python deploy/run_migrations.py apply                  # runs 008..011

New server after restoring a pg_dump (schema already in the dump):
    python deploy/run_migrations.py baseline               # mark everything applied
    # future schema changes then run with 'apply'
"""

import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MIGRATION_DIR = REPO / 'migration'


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


def cmd_status():
    conn = _connect()
    try:
        cur = conn.cursor()
        _ensure_table(cur)
        conn.commit()
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
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
