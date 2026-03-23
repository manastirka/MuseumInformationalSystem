#!/usr/bin/env python3
"""Generate test timesheet reports for all employees with realistic varied data.

Populates timesheet_reports and timesheet_report_days for:
- January 2026 (full month)
- February 2026 (days 1-4 only)

Skips any employee+month combination that already has a report.
The database trigger on timesheet_report_days automatically syncs
aggregated totals to timesheet_entries.
"""

import os
import json
import random
from datetime import date

import psycopg
from psycopg.rows import dict_row

from serbian_holidays import SerbianHolidays

# Database connection
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system')


def _get_pg_url() -> str:
    return DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')


# ---------------------------------------------------------------------------
# Work description samples (Serbian Cyrillic)
# ---------------------------------------------------------------------------

WORK_SAMPLES = {
    'cat_2_1': [
        'Инвентаризација збирке минерала',
        'Ревизија фонда палеонтологије',
        'Конзерваторска процена експоната',
        'Унос нових примерака у базу података',
        'Обрада и каталогизација узорака',
    ],
    'cat_2_2': [
        'Детерминација минерала из Србије',
        'Идентификација фосила за extern захтев',
        'Експертиза геолошких узорака',
        'Таксономска верификација примерака',
    ],
    'cat_2_3': [
        'Рад на научном раду о минералима Копаоника',
        'Припрема рецензије за часопис',
        'Учешће на научном скупу у Београду',
        'Истраживање литературе за пројекат',
        'Писање поглавља за монографију',
    ],
    'cat_3_1': [
        'Теренски рад на Фрушкој гори - прикупљање узорака',
        'Истраживање локалитета Западна Србија',
        'Геолошко картирање терена код Ваљева',
        'Рекогносцирање терена за будућа истраживања',
    ],
    'cat_3_2': [
        'Нови примерци минерала са Голије',
        'Фосили из околине Пирота',
        'Донација приватног колекционара - 15 примерака',
        'Узорци са теренског истраживања',
    ],
    'cat_4_1': [
        'Рад на сталној поставци - одржавање',
        'Припрема експоната за текућу изложбу',
        'Постављање витрина у галерији',
    ],
    'cat_4_2': [
        'Планирање изложбе "Минерали Србије"',
        'Израда концепта за нову изложбу',
        'Селекција експоната за планирану изложбу',
    ],
    'cat_5_1': [
        'Консултације са педагошком службом о програму',
        'Припрема материјала за едукативне радионице',
    ],
    'cat_5_2': [
        'Стручно вођење групе ученика',
        'Предавање за студенте геологије',
        'Радионица о минералима за децу',
        'Вођење 3 групе посетилаца',
    ],
    'cat_5_3': [
        'Интервју за РТС о новој изложби',
        'Припрема садржаја за друштвене мреже',
        'Комуникација са медијима',
    ],
    'cat_6_1': [
        'Састанак радне групе за дигитализацију',
        'Учешће у пројекту "Геонаслеђе Србије"',
        'Координација са партнерским институцијама',
    ],
    'cat_6_2': [
        'Сарадња са Природњачким музејом у Бечу',
        'Размена информација са колегама из региона',
        'Међународни пројекат каталогизације',
    ],
    'cat_7': [
        'Дигитализација збирке - фотографисање примерака',
        'Унос метаподатака у базу',
        'GIS мапирање локалитета',
        '3D скенирање одабраних експоната',
        'Ажурирање базе података',
    ],
    'cat_8': [
        'Административни послови',
        'Састанак колектива',
        'Координација са управом',
        'Планирање активности за наредни месец',
        'Извештавање о раду одељења',
    ],
}

# Positions that are likely to do field work
FIELD_WORK_POSITIONS = [
    'кустос', 'истраживач', 'палеонтолог', 'минералог', 'геолог',
    'ботаничар', 'зоолог', 'ентомолог', 'палеозоолог', 'палеоботаничар',
]


def is_field_worker(position: str) -> bool:
    """Check if the position typically involves field work."""
    if not position:
        return False
    pos_lower = position.lower()
    return any(kw in pos_lower for kw in FIELD_WORK_POSITIONS)


def generate_work_categories() -> str:
    """Generate random special_tasks JSON for the report header."""
    categories = {}
    for cat_key, samples in WORK_SAMPLES.items():
        if random.random() < 0.55:
            categories[cat_key] = random.choice(samples)
        else:
            categories[cat_key] = ''
    return json.dumps(categories, ensure_ascii=False)


def get_employees(conn):
    """Fetch all active employees from the database."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT u.id, u.full_name, u.email,
                   COALESCE(d.name, 'Природњачки музеј') AS department,
                   u.position
            FROM users u
            LEFT JOIN departments d ON u.department_id = d.id
            WHERE u.is_active = TRUE
            ORDER BY u.full_name
        """)
        return cur.fetchall()


def get_existing_reports(conn):
    """Return a set of (employee_email, month, year) for existing 2026 reports."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT employee_email, month, year
            FROM timesheet_reports
            WHERE year = 2026 AND month IN (1, 2)
        """)
        return {(r['employee_email'], r['month'], r['year']) for r in cur.fetchall()}


def generate_month_days(year: int, month: int, last_day: int, field_worker: bool):
    """Generate daily hour rows for a single report.

    Args:
        year, month: the period
        last_day: last calendar day to generate (e.g. 31 for full Jan, 4 for partial Feb)
        field_worker: whether this employee does field work

    Returns:
        list of dicts ready for DB insertion (only days that have hours > 0)
    """
    holidays = SerbianHolidays.get_all_holidays(year)

    # Pre-decide how many vacation days this employee takes this month (0-3)
    max_vacation = random.randint(0, 3)
    vacation_used = 0

    # Pre-decide if employee has a sick leave stretch
    sick_stretch_start = None
    sick_stretch_len = 0
    if random.random() < 0.08:  # ~8% chance of sick leave
        sick_stretch_len = random.randint(1, 4)
        sick_stretch_start = random.randint(1, max(1, last_day - sick_stretch_len))

    days = []

    for day_num in range(1, last_day + 1):
        d = date(year, month, day_num)

        # Weekend — skip (no entry)
        if d.weekday() >= 5:
            continue

        hours = {
            'work_in_museum': 0,
            'work_outside': 0,
            'vacation': 0,
            'public_holiday': 0,
            'paid_leave': 0,
            'other_leave': 0,
            'sick_leave_lt30': 0,
            'sick_leave_gte30': 0,
        }

        # Public holiday
        if d in holidays:
            hours['public_holiday'] = 8
            days.append({'day': day_num, **hours})
            continue

        # Sick leave stretch
        if (sick_stretch_start is not None
                and sick_stretch_start <= day_num < sick_stretch_start + sick_stretch_len):
            hours['sick_leave_lt30'] = 8
            days.append({'day': day_num, **hours})
            continue

        # Vacation days
        if vacation_used < max_vacation and random.random() < 0.12:
            hours['vacation'] = 8
            vacation_used += 1
            days.append({'day': day_num, **hours})
            continue

        # Paid leave (rare)
        if random.random() < 0.02:
            hours['paid_leave'] = 8
            days.append({'day': day_num, **hours})
            continue

        # Normal work day — decide type
        roll = random.random()
        if field_worker and roll < 0.15:
            # Full field day
            hours['work_outside'] = 8
        elif field_worker and roll < 0.22:
            # Mixed day
            hours['work_in_museum'] = 4
            hours['work_outside'] = 4
        else:
            # Regular museum work
            hours['work_in_museum'] = 8

        days.append({'day': day_num, **hours})

    return days


def main():
    print("Generisanje test izvestaja za radne liste")
    print("=" * 55)

    pg_url = _get_pg_url()
    if not pg_url or pg_url == 'postgresql://':
        print("DATABASE_URL nije podesen!")
        return

    with psycopg.connect(conninfo=pg_url, row_factory=dict_row) as conn:
        employees = get_employees(conn)
        print(f"Pronadjeno {len(employees)} aktivnih zaposlenih")

        existing = get_existing_reports(conn)
        print(f"Postojecih izvestaja za 2026: {len(existing)}")

        # Periods to generate
        periods = [
            (2026, 1, 31),   # January full month
            (2026, 2, 4),    # February 1-4 only
        ]

        created = 0
        skipped = 0

        for emp in employees:
            email = emp['email']
            name = emp['full_name']
            dept = emp['department'] or 'Природњачки музеј'
            position = emp['position'] or 'Запослени'
            fw = is_field_worker(position)

            for year, month, last_day in periods:
                if (email, month, year) in existing:
                    skipped += 1
                    print(f"  SKIP {name} {month}/{year} (vec postoji)")
                    continue

                special_tasks = generate_work_categories()
                day_rows = generate_month_days(year, month, last_day, fw)

                with conn.cursor() as cur:
                    # Insert report header
                    cur.execute("""
                        INSERT INTO timesheet_reports (
                            employee_email, employee_name,
                            month, year,
                            organization_unit, position,
                            special_tasks,
                            is_verified, is_locked,
                            version,
                            created_at
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s,
                            FALSE, FALSE, 1, NOW()
                        ) RETURNING id
                    """, (email, name, month, year, dept, position, special_tasks))

                    report_id = cur.fetchone()['id']

                    # Batch insert daily rows
                    if day_rows:
                        values = []
                        params = []
                        for dr in day_rows:
                            values.append("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                            params.extend([
                                report_id, dr['day'],
                                dr['work_in_museum'], dr['work_outside'],
                                dr['vacation'], dr['public_holiday'],
                                dr['paid_leave'], dr['other_leave'],
                                dr['sick_leave_lt30'], dr['sick_leave_gte30'],
                            ])

                        cur.execute(f"""
                            INSERT INTO timesheet_report_days (
                                report_id, day,
                                work_in_museum, work_outside,
                                vacation, public_holiday,
                                paid_leave, other_leave,
                                sick_leave_lt30, sick_leave_gte30
                            ) VALUES {','.join(values)}
                        """, params)

                conn.commit()
                created += 1
                print(f"  + {name} {month}/{year}  (ID {report_id}, {len(day_rows)} dana)")

        # ---------------------------------------------------------------
        # Verification
        # ---------------------------------------------------------------
        print()
        print("=" * 55)
        print(f"Kreirano: {created}  |  Preskoceno: {skipped}")
        print()

        with conn.cursor() as cur:
            cur.execute("""
                SELECT year, month, COUNT(*) AS cnt
                FROM timesheet_reports
                WHERE year = 2026
                GROUP BY year, month
                ORDER BY year, month
            """)
            for row in cur.fetchall():
                print(f"  Izvestaji {row['month']:02d}/{row['year']}: {row['cnt']}")

            cur.execute("""
                SELECT COUNT(*) AS cnt
                FROM timesheet_report_days rd
                JOIN timesheet_reports r ON rd.report_id = r.id
                WHERE r.year = 2026
            """)
            total_days = cur.fetchone()['cnt']
            print(f"  Ukupno dnevnih unosa: {total_days}")

            cur.execute("""
                SELECT COUNT(*) AS cnt
                FROM timesheet_entries e
                JOIN timesheet_reports r ON e.report_id = r.id
                WHERE r.year = 2026
            """)
            total_entries = cur.fetchone()['cnt']
            print(f"  Ukupno timesheet_entries (via trigger): {total_entries}")

        print()
        print("Gotovo.")


if __name__ == '__main__':
    main()
