#!/usr/bin/env python3
"""Seed deterministic PostgreSQL state for admin E2E scenarios."""

import calendar
import os
import sys
from pathlib import Path

import psycopg

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _load_dotenv(dotenv_path: Path) -> None:
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip().rstrip("\r")
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv(REPO_ROOT / ".env")

from psycopg.rows import dict_row  # noqa: E402
from timesheet_postgres import get_user_department_and_position, save_timesheet_to_postgres  # noqa: E402


def _database_url() -> str:
    db_url = os.environ.get("DATABASE_URL", "").strip()
    if not db_url:
        raise SystemExit("DATABASE_URL is not configured")
    return db_url.replace("postgresql+psycopg://", "postgresql://")


def _bool_env(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_user(email: str) -> dict:
    with psycopg.connect(_database_url(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT u.email, u.full_name, COALESCE(d.name, 'Природњачки музеј') AS department,
                       COALESCE(u.position, 'Запослени') AS position
                FROM users u
                LEFT JOIN departments d ON u.department_id = d.id
                WHERE LOWER(u.email) = LOWER(%s)
                """,
                (email,),
            )
            user = cur.fetchone()
            if not user:
                raise SystemExit(f"user not found: {email}")
            return dict(user)


def _delete_existing_report(email: str, full_name: str, month: int, year: int) -> None:
    with psycopg.connect(_database_url(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id
                FROM timesheet_reports
                WHERE (LOWER(employee_email) = LOWER(%s) OR (employee_email IS NULL AND employee_name = %s))
                  AND month = %s
                  AND year = %s
                """,
                (email, full_name, month, year),
            )
            report_ids = [row["id"] for row in cur.fetchall()]

            for report_id in report_ids:
                cur.execute("DELETE FROM timesheet_status_history WHERE report_id = %s", (report_id,))
                cur.execute("DELETE FROM timesheet_edit_requests WHERE report_id = %s", (report_id,))
                cur.execute("DELETE FROM timesheet_entries WHERE report_id = %s", (report_id,))
                cur.execute("DELETE FROM timesheet_report_days WHERE report_id = %s", (report_id,))
                cur.execute("DELETE FROM timesheet_reports WHERE id = %s", (report_id,))

        conn.commit()


def _build_daily_data(month: int, year: int) -> dict:
    days_in_month = calendar.monthrange(year, month)[1]
    daily_data = {}
    first_workday = None
    for day in range(1, days_in_month + 1):
        weekday = calendar.weekday(year, month, day)
        if first_workday is None and weekday < 5:
            first_workday = day
        daily_data[day] = {
            "rad_na_mestu": 0,
            "van_muzeja": 0,
            "godisnji_odmor": 0,
            "drzavni_praznik": 0,
            "placeno_odsustvo": 0,
            "ostalo_odsustvo": 0,
            "bolovanje_manje30": 0,
            "bolovanje_30_ili_vise": 0,
        }

    workday = first_workday or 1
    daily_data[workday]["rad_na_mestu"] = 8
    return daily_data


def seed_timesheet_report() -> int:
    email = os.environ.get("TARGET_EMAIL", "").strip()
    month = int(os.environ.get("REPORT_MONTH", "12"))
    year = int(os.environ.get("REPORT_YEAR", "2027"))
    status = os.environ.get("REPORT_STATUS", "DRAFT").strip().upper() or "DRAFT"
    locked = _bool_env("REPORT_LOCKED", default=False)
    verified = _bool_env("REPORT_VERIFIED", default=False)

    user = _get_user(email)
    _delete_existing_report(user["email"], user["full_name"], month, year)

    organization_unit, position = get_user_department_and_position(user["email"])
    result = save_timesheet_to_postgres(
        user_email=user["email"],
        user_name=user["full_name"],
        month=month,
        year=year,
        daily_data=_build_daily_data(month, year),
        work_description="QA seeded admin E2E report",
        organization_unit=organization_unit or user["department"],
        position=position or user["position"],
    )
    if not result.success:
        raise SystemExit(f"failed to seed report: {result.error.message if result.error else 'unknown'}")

    report_id = int(result.data["report_id"])
    verified_by = os.environ.get("ADMIN_EMAIL", "admin@nhmbeo.rs").strip() if verified else None
    rejection_note = "QA seeded rejection" if status == "REJECTED" else None

    with psycopg.connect(_database_url()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE timesheet_reports
                SET status = %s,
                    is_locked = %s,
                    is_verified = %s,
                    verified_by = %s,
                    verified_at = CASE WHEN %s THEN NOW() ELSE NULL END,
                    rejection_note = %s
                WHERE id = %s
                """,
                (status, locked, verified, verified_by, verified, rejection_note, report_id),
            )
        conn.commit()

    print(f"REPORT_ID={report_id}")
    return 0


def seed_edit_request() -> int:
    email = os.environ.get("TARGET_EMAIL", "").strip()
    month = int(os.environ.get("REPORT_MONTH", "11"))
    year = int(os.environ.get("REPORT_YEAR", "2027"))
    reason = os.environ.get("REQUEST_REASON", "QA seeded edit approval request").strip()

    user = _get_user(email)
    _delete_existing_report(user["email"], user["full_name"], month, year)

    organization_unit, position = get_user_department_and_position(user["email"])
    result = save_timesheet_to_postgres(
        user_email=user["email"],
        user_name=user["full_name"],
        month=month,
        year=year,
        daily_data=_build_daily_data(month, year),
        work_description="QA seeded locked report for edit request",
        organization_unit=organization_unit or user["department"],
        position=position or user["position"],
    )
    if not result.success:
        raise SystemExit(f"failed to seed edit-request report: {result.error.message if result.error else 'unknown'}")

    report_id = int(result.data["report_id"])

    with psycopg.connect(_database_url(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE timesheet_reports
                SET status = 'DRAFT',
                    is_locked = TRUE,
                    is_verified = FALSE,
                    verified_by = NULL,
                    verified_at = NULL,
                    rejection_note = NULL
                WHERE id = %s
                """,
                (report_id,),
            )
            cur.execute("DELETE FROM timesheet_edit_requests WHERE report_id = %s", (report_id,))
            cur.execute(
                """
                INSERT INTO timesheet_edit_requests
                    (report_id, requester_email, reason, status, requested_at)
                VALUES (%s, %s, %s, 'pending', NOW())
                RETURNING id
                """,
                (report_id, user["email"], reason),
            )
            request_id = int(cur.fetchone()["id"])
        conn.commit()

    print(f"REPORT_ID={report_id}")
    print(f"REQUEST_ID={request_id}")
    return 0


def main() -> int:
    action = os.environ.get("ADMIN_E2E_ACTION", "").strip().lower()
    if action == "timesheet_report":
        return seed_timesheet_report()
    if action == "timesheet_edit_request":
        return seed_edit_request()
    raise SystemExit("ADMIN_E2E_ACTION must be one of: timesheet_report, timesheet_edit_request")


if __name__ == "__main__":
    raise SystemExit(main())
