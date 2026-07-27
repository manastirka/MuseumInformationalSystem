#!/usr/bin/env python3
"""DB helper for the matrix-persistence Playwright test.

  clean [email]  — delete the employee's CURRENT-month report (fresh start)
  rows  [email]  — print JSON of that report's timesheet_report_days
"""

import json
import os
import sys
from datetime import datetime

os.environ.setdefault('FLASK_ENV', 'testing')
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
)

import timesheet_postgres as tp


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'rows'
    email = (sys.argv[2] if len(sys.argv) > 2 and sys.argv[2].strip()
             else os.environ.get('CYPRESS_EMPLOYEE_EMAIL', ''))
    now = datetime.now()
    with tp.get_pg_connection() as conn:
        with conn.cursor() as cur:
            if mode == 'clean':
                cur.execute("DELETE FROM timesheet_reports WHERE employee_email=%s "
                            "AND month=%s AND year=%s", (email, now.month, now.year))
                conn.commit()
                print('CLEANED')
                return
            cur.execute("SELECT id FROM timesheet_reports WHERE employee_email=%s "
                        "AND month=%s AND year=%s", (email, now.month, now.year))
            r = cur.fetchone()
            if not r:
                print('[]')
                return
            cur.execute("SELECT day, work_in_museum::float AS rad, work_outside::float AS van, "
                        "vacation::float AS god FROM timesheet_report_days WHERE report_id=%s "
                        "ORDER BY day", (r['id'],))
            print(json.dumps([dict(x) for x in cur.fetchall()]))


if __name__ == '__main__':
    main()
