#!/usr/bin/env python3
"""Seed/clean an imported-2015 + current-year report pair for a uniquely-named
test employee, to prove the current/archive admin split in the browser.

Usage: python seed_arhiva.py seed|clean
"""

import os
import sys
from datetime import datetime

os.environ.setdefault('FLASK_ENV', 'testing')
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
)

import timesheet_postgres as tp

NAME = 'ЗЗ Архива Проба'
EMAIL = 'zz.arhiva.proba@example.com'


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'seed'
    cy = datetime.now().year
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM timesheet_reports WHERE employee_email=%s", (EMAIL,))
            if mode == 'clean':
                conn.commit()
                print('CLEANED')
                return
            cur.execute(
                "INSERT INTO timesheet_reports "
                "(employee_name, employee_email, month, year, status, imported_from) "
                "VALUES (%s, %s, 6, 2015, 'APPROVED', 'word-arhiva')",
                (NAME, EMAIL))
            cur.execute(
                "INSERT INTO timesheet_reports "
                "(employee_name, employee_email, month, year, status, imported_from) "
                "VALUES (%s, %s, 6, %s, 'SUBMITTED', NULL)",
                (NAME, EMAIL, cy))
            conn.commit()
            print(f'SEEDED name={NAME} cy={cy}')


if __name__ == '__main__':
    main()
