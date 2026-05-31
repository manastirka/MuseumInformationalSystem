#!/usr/bin/env python3
"""One-off migration: add employee_profiles.is_department_head and flag
known department heads.

Safe to run multiple times — uses IF NOT EXISTS and idempotent UPDATE.
"""

import os
import sys
import logging

import psycopg

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


DEPARTMENT_HEAD_EMAILS = [
    'biljana.mitrovic@nhmbeo.rs',   # Geology
    'verica.stojanovic@nhmbeo.rs',  # Biology
    'ana.zivanovic@nhmbeo.rs',      # General and Legal Affairs (sef_pravne_sluzbe)
    'dusica.ivic@nhmbeo.rs',        # Accounting / Finance (sef_racunovodstva)
]


def main():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        logger.error('DATABASE_URL not set.')
        sys.exit(1)

    pg_url = db_url.replace('postgresql+psycopg://', 'postgresql://')

    with psycopg.connect(pg_url) as conn:
        with conn.cursor() as cur:
            logger.info('Adding is_department_head column if missing...')
            cur.execute(
                """
                ALTER TABLE employee_profiles
                ADD COLUMN IF NOT EXISTS is_department_head BOOLEAN NOT NULL DEFAULT FALSE
                """
            )

            for email in DEPARTMENT_HEAD_EMAILS:
                cur.execute(
                    "UPDATE employee_profiles SET is_department_head = TRUE WHERE LOWER(email) = LOWER(%s)",
                    (email,),
                )
                if cur.rowcount:
                    logger.info('Flagged %s as department head.', email)
                else:
                    logger.warning('No employee_profiles row for %s — skipped.', email)

            conn.commit()

    logger.info('Migration complete.')


if __name__ == '__main__':
    main()
