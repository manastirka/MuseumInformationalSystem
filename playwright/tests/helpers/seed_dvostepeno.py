#!/usr/bin/env python3
"""Seed/clean a PARTIALLY-signed SUBMITTED report for the two-signature UI test.

Puts the QA employee's previous-month report into SUBMITTED with the department
head's signature present but the director's still missing — so the employee page
shows the phase ("Шеф одељења потврдио" + "Чека потпис директора").

Usage: python seed_dvostepeno.py seed|clean [email]
"""

import os
import sys

os.environ.setdefault('FLASK_ENV', 'testing')
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
)

import timesheet_postgres as tp


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'seed'
    email = (sys.argv[2] if len(sys.argv) > 2 and sys.argv[2].strip()
             else os.environ.get('CYPRESS_EMPLOYEE_EMAIL', ''))
    if not email:
        print('ERROR: no employee email', file=sys.stderr)
        sys.exit(2)
    month, year = tp.default_entry_period()
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT full_name FROM users WHERE LOWER(email)=LOWER(%s)", (email,))
            row = cur.fetchone()
            if not row:
                print(f'ERROR: no user for {email}', file=sys.stderr)
                sys.exit(3)
            name = row['full_name']
            cur.execute("DELETE FROM timesheet_reports WHERE (employee_email=%s OR employee_name=%s) "
                        "AND month=%s AND year=%s", (email, name, month, year))
            if mode == 'clean':
                conn.commit()
                print('CLEANED')
                return
            cur.execute(
                "INSERT INTO timesheet_reports "
                "(employee_name, employee_email, month, year, status, is_locked, "
                " submitted_at, head_verified_by, head_verified_at) "
                "VALUES (%s, %s, %s, %s, 'SUBMITTED', TRUE, NOW(), %s, NOW()) RETURNING id",
                (name, email, month, year, 'sef.odeljenja@nhmbeo.rs'))
            print(cur.fetchone()['id'])
            conn.commit()


if __name__ == '__main__':
    main()
