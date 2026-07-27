#!/usr/bin/env python3
"""Seed/clean helper for the vraćena-radna-lista Playwright test.

Puts the QA employee's PREVIOUS-month report into the exact production state
that triggered the bug: status REJECTED, unlocked, with a live 24 h edit
window (``editable_until`` in the future) and a šef's rejection note — i.e. a
list returned NA DOPUNU after the calendar deadline has passed.

Usage:
    python seed_vracena_lista.py seed  [email] [months_back]   # prints report_id
    python seed_vracena_lista.py clean [email] [months_back]

``months_back`` (default: previous month) shifts the target period further into
the past, to exercise returning an OLDER list (e.g. 3 for three months ago).
"""

import os
import sys

os.environ.setdefault('FLASK_ENV', 'testing')

# Repo root (four levels up: helpers -> tests -> playwright -> repo).
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
)

import timesheet_postgres as tp


def _resolve_name(cur, email):
    cur.execute("SELECT full_name FROM users WHERE email = %s", (email,))
    row = cur.fetchone()
    return row['full_name'] if row else None


def _clean(cur, email, name, month, year):
    cur.execute(
        "DELETE FROM timesheet_reports "
        "WHERE (employee_email = %s OR employee_name = %s) "
        "  AND month = %s AND year = %s",
        (email, name, month, year),
    )


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'seed'
    email = (sys.argv[2] if len(sys.argv) > 2 and sys.argv[2].strip()
             else os.environ.get('CYPRESS_EMPLOYEE_EMAIL', ''))
    if not email:
        print('ERROR: no employee email', file=sys.stderr)
        sys.exit(2)

    if len(sys.argv) > 3 and sys.argv[3].strip():
        from datetime import datetime
        now = datetime.now()
        offset = int(sys.argv[3])
        idx = (now.year * 12 + (now.month - 1)) - offset
        year, month = idx // 12, idx % 12 + 1
    else:
        month, year = tp.default_entry_period()

    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            name = _resolve_name(cur, email)
            if not name:
                print(f'ERROR: no user for {email}', file=sys.stderr)
                sys.exit(3)

            _clean(cur, email, name, month, year)

            if mode == 'clean':
                conn.commit()
                print('CLEANED')
                return

            cur.execute(
                "INSERT INTO timesheet_reports "
                "(employee_name, employee_email, month, year, organization_unit, "
                " position, special_tasks, status, is_locked, is_verified, "
                " submitted_at, reviewed_at, reviewed_by_email, rejection_note, "
                " editable_until, version) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, 'REJECTED', FALSE, FALSE, "
                "        NOW(), NOW(), %s, %s, NOW() + INTERVAL '24 hours', 2) "
                "RETURNING id",
                (name, email, month, year, 'Природњачки музеј', 'Запослени',
                 'почетни послови', 'sef.test@example.com',
                 'Допуните дане 15. и 16. и опис послова.'),
            )
            report_id = cur.fetchone()['id']
            conn.commit()
            print(report_id)


if __name__ == '__main__':
    main()
