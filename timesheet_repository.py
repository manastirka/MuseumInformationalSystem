#!/usr/bin/env python3
"""
Timesheet repository that prefers PostgreSQL (DATABASE_URL) for radna lista data.
Provides aggregate queries for the Flask admin dashboard.
"""

import logging
import os
from decimal import Decimal
from typing import Dict, List, Optional, Tuple

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import NullPool

logger = logging.getLogger(__name__)


class TimesheetRepository:
    """Read-only access layer for migrated radna_lista data."""

    CATEGORY_LABELS = {
        'rad_na_mestu': 'Рад у музеју',
        'van_muzeja': 'Рад ван музеја',
        'godisnji_odmor': 'Годишњи одмор',
        'drzavni_praznik': 'Државни празник',
        'placeno_odsustvo': 'Плаћено одсуство',
        'ostalo_odsustvo': 'Остало одсуство',
        'bolovanje_manje_30': 'Боловање < 30 дана',
        'bolovanje_vece_30': 'Боловање ≥ 30 дана'
    }

    def __init__(self, db_url: Optional[str] = None):
        self.db_url = db_url or os.environ.get('DATABASE_URL')
        self.available = False
        self.engine = None

        if not self.db_url:
            logger.info("Timesheet repository disabled (DATABASE_URL not set).")
            return

        try:
            self.engine = create_engine(self.db_url, poolclass=NullPool)
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            self.available = True
            logger.info("Timesheet repository connected to PostgreSQL.")
        except SQLAlchemyError as exc:
            logger.error("Failed to initialize timesheet repository: %s", exc)
            self.available = False

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------
    def latest_period(self) -> Optional[Tuple[int, int]]:
        """Return the latest (year, month) tuple with data."""
        if not self.available:
            return None
        query = text("""
            SELECT year, month
            FROM timesheet_reports
            ORDER BY year DESC, month DESC
            LIMIT 1
        """)
        try:
            with self.engine.connect() as conn:
                row = conn.execute(query).first()
                if row:
                    return int(row.year), int(row.month)
        except SQLAlchemyError as exc:
            logger.error("Error fetching latest timesheet period: %s", exc)
        return None

    def list_reports(
        self,
        page: int = 1,
        per_page: int = 25,
        month: Optional[int] = None,
        year: Optional[int] = None,
        search: Optional[str] = None,
        department: Optional[str] = None,
    ) -> Dict:
        """Return paginated list of reports with category totals.

        When `department` is supplied, only reports whose employee (matched by
        full_name in `employee_profiles`) belongs to that department are
        returned. This supports department-head-scoped verification.
        """
        if not self.available:
            return {'reports': [], 'total': 0, 'page': page, 'total_pages': 0}

        where_sql, params = self._build_filters(month, year, search, department)
        offset = (page - 1) * per_page

        query = text(
            "SELECT "
            "tr.id, tr.employee_name, tr.month, tr.year, "
            "tr.organization_unit, tr.position, "
            "tr.is_verified, tr.verified_by, tr.verified_at, tr.is_locked, "
            "COALESCE(tr.status, 'DRAFT') AS status, tr.reviewed_at, "
            "tr.rejection_note, "
            "SUM(CASE WHEN te.category = 'rad_na_mestu' THEN te.hours ELSE 0 END) AS work_in_museum, "
            "SUM(CASE WHEN te.category = 'van_muzeja' THEN te.hours ELSE 0 END) AS work_outside, "
            "SUM(CASE WHEN te.category = 'godisnji_odmor' THEN te.hours ELSE 0 END) AS vacation, "
            "SUM(CASE WHEN te.category = 'drzavni_praznik' THEN te.hours ELSE 0 END) AS public_holiday, "
            "SUM(CASE WHEN te.category = 'placeno_odsustvo' THEN te.hours ELSE 0 END) AS paid_leave, "
            "SUM(CASE WHEN te.category = 'ostalo_odsustvo' THEN te.hours ELSE 0 END) AS other_leave, "
            "SUM(CASE WHEN te.category = 'bolovanje_manje_30' THEN te.hours ELSE 0 END) AS sick_lt30, "
            "SUM(CASE WHEN te.category = 'bolovanje_vece_30' THEN te.hours ELSE 0 END) AS sick_gte30, "
            "COALESCE(SUM(te.hours), 0) AS total_hours "
            "FROM timesheet_reports tr "
            "LEFT JOIN timesheet_entries te ON te.report_id = tr.id "
            "WHERE " + where_sql + " "
            "GROUP BY tr.id, tr.employee_name, tr.month, tr.year, tr.organization_unit, "
            "tr.position, tr.is_verified, tr.verified_by, tr.verified_at, tr.is_locked, tr.status, tr.reviewed_at, tr.rejection_note "
            "ORDER BY tr.year DESC, tr.month DESC, tr.employee_name "
            "LIMIT :limit OFFSET :offset"
        )

        count_query = text(
            "SELECT COUNT(*) AS total FROM timesheet_reports tr WHERE " + where_sql
        )

        try:
            with self.engine.connect() as conn:
                rows = conn.execute(
                    query,
                    {**params, 'limit': per_page, 'offset': offset}
                ).mappings().all()
                total = conn.execute(count_query, params).scalar_one()

            reports = [self._normalize_report_row(row) for row in rows]
            total_pages = (total + per_page - 1) // per_page if per_page else 0
            return {
                'reports': reports,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': total_pages
            }
        except SQLAlchemyError as exc:
            logger.error("Error listing timesheet reports: %s", exc)
            return {'reports': [], 'total': 0, 'page': page, 'total_pages': 0}

    def get_month_summary(self, month: Optional[int] = None, year: Optional[int] = None) -> Optional[Dict]:
        """Return aggregated totals for a specific month/year (defaults to latest)."""
        if not self.available:
            return None
        if month is None or year is None:
            latest = self.latest_period()
            if not latest:
                return None
            year, month = latest

        query = text("""
            SELECT
                SUM(CASE WHEN te.category = 'rad_na_mestu' THEN te.hours ELSE 0 END) AS work_in_museum,
                SUM(CASE WHEN te.category = 'van_muzeja' THEN te.hours ELSE 0 END) AS work_outside,
                SUM(CASE WHEN te.category = 'godisnji_odmor' THEN te.hours ELSE 0 END) AS vacation,
                SUM(CASE WHEN te.category = 'drzavni_praznik' THEN te.hours ELSE 0 END) AS public_holiday,
                SUM(CASE WHEN te.category = 'placeno_odsustvo' THEN te.hours ELSE 0 END) AS paid_leave,
                SUM(CASE WHEN te.category = 'ostalo_odsustvo' THEN te.hours ELSE 0 END) AS other_leave,
                SUM(CASE WHEN te.category = 'bolovanje_manje_30' THEN te.hours ELSE 0 END) AS sick_lt30,
                SUM(CASE WHEN te.category = 'bolovanje_vece_30' THEN te.hours ELSE 0 END) AS sick_gte30,
                COUNT(DISTINCT tr.id) AS reports_count
            FROM timesheet_reports tr
            LEFT JOIN timesheet_entries te ON te.report_id = tr.id
            WHERE tr.month = :month AND tr.year = :year
        """)

        try:
            with self.engine.connect() as conn:
                row = conn.execute(query, {'month': month, 'year': year}).mappings().first()
                if not row:
                    return None
                totals = self._coerce_hours_row(row)
                totals['reports_count'] = int(row.reports_count or 0)
                totals['total_hours'] = sum(totals[k] for k in self.CATEGORY_LABELS.keys())
                # Worked-hours subtotal (museum + outside) exposed alongside the
                # all-recorded total so screens can show both, clearly labeled,
                # and agree with the official Word report's two figures.
                totals['worked_hours'] = totals['rad_na_mestu'] + totals['van_muzeja']
                return {
                    'month': month,
                    'year': year,
                    'totals': totals
                }
        except SQLAlchemyError as exc:
            logger.error("Error fetching monthly timesheet summary: %s", exc)
        return None

    def get_overall_summary(self) -> Optional[Dict]:
        """Return global totals for dashboard widgets."""
        if not self.available:
            return None
        query = text("""
            SELECT
                COUNT(*) AS report_count,
                COUNT(DISTINCT employee_name) AS unique_employees
            FROM timesheet_reports
        """)
        try:
            with self.engine.connect() as conn:
                counts = conn.execute(query).mappings().first()
            totals_query = text("""
                SELECT category, SUM(hours) AS total
                FROM timesheet_entries
                GROUP BY category
            """)
            with self.engine.connect() as conn:
                totals_rows = conn.execute(totals_query).mappings().all()
            category_totals = {cat: 0.0 for cat in self.CATEGORY_LABELS.keys()}
            for row in totals_rows:
                category_totals[row.category] = self._to_float(row.total)
            return {
                'reports': int(counts.report_count or 0),
                'employees': int(counts.unique_employees or 0),
                'category_totals': category_totals
            }
        except SQLAlchemyError as exc:
            logger.error("Error computing overall timesheet summary: %s", exc)
        return None

    def get_report(self, report_id: int) -> Optional[Dict]:
        """Return header, per-day data, and category totals for a specific report."""
        if not self.available:
            return None
        header_query = text("""
            SELECT * FROM timesheet_reports WHERE id = :report_id
        """)
        days_query = text("""
            SELECT *
            FROM timesheet_report_days
            WHERE report_id = :report_id
            ORDER BY day
        """)
        totals_query = text("""
            SELECT category, SUM(hours) AS total
            FROM timesheet_entries
            WHERE report_id = :report_id
            GROUP BY category
        """)
        try:
            with self.engine.connect() as conn:
                header = conn.execute(header_query, {'report_id': report_id}).mappings().first()
                if not header:
                    return None
                days = conn.execute(days_query, {'report_id': report_id}).mappings().all()
                totals_rows = conn.execute(totals_query, {'report_id': report_id}).mappings().all()

            category_totals = {cat: 0.0 for cat in self.CATEGORY_LABELS.keys()}
            for row in totals_rows:
                category_totals[row.category] = self._to_float(row.total)

            normalized_days = []
            for row in days:
                normalized_days.append({
                    'day': int(row.day),
                    'work_in_museum': self._to_float(row.work_in_museum),
                    'work_outside': self._to_float(row.work_outside),
                    'vacation': self._to_float(row.vacation),
                    'public_holiday': self._to_float(row.public_holiday),
                    'paid_leave': self._to_float(row.paid_leave),
                    'other_leave': self._to_float(row.other_leave),
                    'sick_lt30': self._to_float(row.sick_leave_lt30),
                    'sick_gte30': self._to_float(row.sick_leave_gte30)
                })

            return {
                'header': dict(header),
                'days': normalized_days,
                'category_totals': category_totals,
                'total_hours': sum(category_totals.values())
            }
        except SQLAlchemyError as exc:
            logger.error("Error fetching timesheet report %s: %s", report_id, exc)
        return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _build_filters(
        self,
        month: Optional[int],
        year: Optional[int],
        search: Optional[str],
        department: Optional[str] = None,
    ) -> Tuple[str, Dict]:
        clauses = []
        params: Dict[str, object] = {}
        if month:
            clauses.append("tr.month = :f_month")
            params['f_month'] = month
        if year:
            clauses.append("tr.year = :f_year")
            params['f_year'] = year
        if search:
            clauses.append("tr.employee_name ILIKE :f_search")
            params['f_search'] = f"%{search}%"
        if department:
            # Match by canonical employee_email, not full_name — names drift
            # (legacy rows, renames, case differences) and would silently
            # exclude reports from the dept head's view.
            clauses.append(
                "LOWER(tr.employee_email) IN "
                "(SELECT LOWER(ep.email) FROM employee_profiles ep "
                " WHERE ep.department = :f_department)"
            )
            params['f_department'] = department
        where_sql = " AND ".join(clauses) if clauses else "TRUE"
        return where_sql, params

    def _normalize_report_row(self, row) -> Dict:
        return {
            'id': row.id,
            'employee_name': row.employee_name,
            'month': int(row.month),
            'year': int(row.year),
            'organization_unit': row.organization_unit,
            'position': row.position,
            'is_verified': bool(row.is_verified) if hasattr(row, 'is_verified') else False,
            'is_locked': bool(row.is_locked) if hasattr(row, 'is_locked') else False,
            'verified_by': row.verified_by if hasattr(row, 'verified_by') else None,
            'verified_at': row.verified_at if hasattr(row, 'verified_at') else None,
            'status': row.status if hasattr(row, 'status') else 'DRAFT',
            'rejection_note': row.rejection_note if hasattr(row, 'rejection_note') else None,
            'work_in_museum': self._to_float(row.work_in_museum),
            'work_outside': self._to_float(row.work_outside),
            'vacation': self._to_float(row.vacation),
            'public_holiday': self._to_float(row.public_holiday),
            'paid_leave': self._to_float(row.paid_leave),
            'other_leave': self._to_float(row.other_leave),
            'sick_lt30': self._to_float(row.sick_lt30),
            'sick_gte30': self._to_float(row.sick_gte30),
            'total_hours': self._to_float(row.total_hours)
        }

    def _coerce_hours_row(self, row) -> Dict[str, float]:
        return {
            'rad_na_mestu': self._to_float(row.work_in_museum),
            'van_muzeja': self._to_float(row.work_outside),
            'godisnji_odmor': self._to_float(row.vacation),
            'drzavni_praznik': self._to_float(row.public_holiday),
            'placeno_odsustvo': self._to_float(row.paid_leave),
            'ostalo_odsustvo': self._to_float(row.other_leave),
            'bolovanje_manje_30': self._to_float(row.sick_lt30),
            'bolovanje_vece_30': self._to_float(row.sick_gte30)
        }

    @staticmethod
    def _to_float(value: Optional[Decimal]) -> float:
        if value is None:
            return 0.0
        if isinstance(value, Decimal):
            return float(value)
        return float(value)
