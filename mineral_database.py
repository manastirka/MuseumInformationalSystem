#!/usr/bin/env python3
"""
Mineral Database Loader
Loads mineral collection data from PrirodnjackiMuzej SQLite database
Enriched with RRUFF scientific data
"""

import sqlite3
import os
import logging
from typing import List, Dict, Optional

from mineral_search_utils import build_search_specs

logger = logging.getLogger(__name__)

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    'PrirodnjackiMuzej',
    'prirodnjacki_muzej.sqlite'
)


class MineralDatabase:
    """Mineralogical collection database accessor."""

    def __init__(self, db_path: str = DB_PATH):
        """Initialize mineral database."""
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            logger.error(f"Mineral database not found: {self.db_path}")
            self.available = False
        else:
            self.available = True
            logger.info(f"Mineral database loaded from: {self.db_path}")

    def _get_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)

    def get_all_minerals(self, page: int = 1, per_page: int = 50,
                         sort_by: str = 'id', sort_order: str = 'asc') -> Dict:
        """Get mineral records with pagination and sorting.

        Returns:
            Dict with 'minerals', 'total', 'page', 'per_page', 'total_pages'
        """
        if not self.available:
            return {'minerals': [], 'total': 0, 'page': 1, 'per_page': per_page, 'total_pages': 0}

        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Validate sort column
            valid_sort_columns = {
                'id': 'id',
                'image': 'id',
                'inventarni_broj': '"Inv. broj"',
                'naziv': '"Naziv"',
                'predmet': '"Predmet"',
                'lokalitet': '"Lokalitet sa kartice"',
                'datum_nabavljanja': '"Datum nabavljanja"',
                'gde_se_nalazi': '"Gde se nalazi"'
            }

            sort_column = valid_sort_columns.get(sort_by, 'id')
            if sort_column not in valid_sort_columns.values():
                sort_column = 'id'
            sort_direction = 'DESC' if sort_order.lower() == 'desc' else 'ASC'

            # Get total count
            cursor.execute("SELECT COUNT(*) FROM minerali")
            total = cursor.fetchone()[0]

            total_pages = (total + per_page - 1) // per_page
            offset = (page - 1) * per_page

            # Build ORDER BY from validated whitelist values only
            if sort_by == 'gde_se_nalazi':
                order_clause = (
                    'CASE WHEN "Gde se nalazi" GLOB \'[0-9]*\' THEN 0 ELSE 1 END ' + sort_direction + ', '
                    'CAST("Gde se nalazi" AS INTEGER) ' + sort_direction + ', '
                    '"Gde se nalazi" ' + sort_direction
                )
            else:
                order_clause = sort_column + ' ' + sort_direction

            # Get paginated results
            cursor.execute(
                """
                SELECT
                    id,
                    "Inv. broj" as inventarni_broj,
                    "Predmet" as predmet,
                    "Naziv" as naziv,
                    "Način nabavljanja" as nacin_nabavljanja,
                    "Datum nabavljanja" as datum_nabavljanja,
                    "Datum unosa u bazu" as datum_unosa,
                    "Uneo u bazu" as uneo_u_bazu,
                    "Legator / Našao / Doneo" as legator,
                    "Identifikovao" as identifikovao,
                    "Komentar/napomena" as komentar,
                    "Napomena/opis" as napomena,
                    "Gde se nalazi" as gde_se_nalazi,
                    "Lokalitet sa kartice" as lokalitet,
                    "U bibliografiji" as u_bibliografiji,
                    "Količina" as kolicina,
                    created_at,
                    updated_at
                FROM minerali
                ORDER BY """ + order_clause + """
                LIMIT ? OFFSET ?
                """, (per_page, offset))

            minerals = []
            for row in cursor.fetchall():
                mineral = dict(row)
                mineral['has_image'] = False

                # Format inventory number for display
                if mineral['inventarni_broj']:
                    inv_num = int(mineral['inventarni_broj']) if isinstance(mineral['inventarni_broj'], float) else mineral['inventarni_broj']
                    mineral['inventarni_broj_display'] = f"M{inv_num}"
                else:
                    mineral['inventarni_broj_display'] = 'N/A'

                minerals.append(mineral)

            conn.close()

            return {
                'minerals': minerals,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': total_pages
            }

        except Exception as e:
            logger.error(f"Error loading minerals: {e}")
            return {'minerals': [], 'total': 0, 'page': 1, 'per_page': per_page, 'total_pages': 0}

    def get_mineral_by_id(self, mineral_id: int) -> Optional[Dict]:
        """Get single mineral by ID."""
        if not self.available:
            return None

        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id,
                    "Inv. broj" as inventarni_broj,
                    "Predmet" as predmet,
                    "Naziv" as naziv,
                    "Način nabavljanja" as nacin_nabavljanja,
                    "Datum nabavljanja" as datum_nabavljanja,
                    "Datum unosa u bazu" as datum_unosa,
                    "Uneo u bazu" as uneo_u_bazu,
                    "Legator / Našao / Doneo" as legator,
                    "Identifikovao" as identifikovao,
                    "Komentar/napomena" as komentar,
                    "Napomena/opis" as napomena,
                    "Gde se nalazi" as gde_se_nalazi,
                    "Lokalitet sa kartice" as lokalitet,
                    "U bibliografiji" as u_bibliografiji,
                    "Količina" as kolicina,
                    created_at,
                    updated_at
                FROM minerali
                WHERE id = ?
            """, (mineral_id,))

            row = cursor.fetchone()
            conn.close()

            if row:
                mineral = dict(row)
                mineral['has_image'] = False
                if mineral['inventarni_broj']:
                    inv_num = int(mineral['inventarni_broj']) if isinstance(mineral['inventarni_broj'], float) else mineral['inventarni_broj']
                    mineral['inventarni_broj_display'] = f"M{inv_num}"
                else:
                    mineral['inventarni_broj_display'] = 'N/A'
                return mineral

            return None

        except Exception as e:
            logger.error(f"Error loading mineral {mineral_id}: {e}")
            return None

    def get_mineral_by_inventory_number(self, inv_number: str) -> Optional[Dict]:
        """Get mineral by inventory number (supports M12345 or 12345 format)."""
        if not self.available:
            return None

        # Remove 'M' prefix if present
        inv_num_clean = inv_number.replace('M', '').replace('m', '').strip()

        try:
            inv_num_float = float(inv_num_clean)
        except:
            return None

        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id,
                    "Inv. broj" as inventarni_broj,
                    "Predmet" as predmet,
                    "Naziv" as naziv,
                    "Način nabavljanja" as nacin_nabavljanja,
                    "Datum nabavljanja" as datum_nabavljanja,
                    "Datum unosa u bazu" as datum_unosa,
                    "Uneo u bazu" as uneo_u_bazu,
                    "Legator / Našao / Doneo" as legator,
                    "Identifikovao" as identifikovao,
                    "Komentar/napomena" as komentar,
                    "Napomena/opis" as napomena,
                    "Gde se nalazi" as gde_se_nalazi,
                    "Lokalitet sa kartice" as lokalitet,
                    "U bibliografiji" as u_bibliografiji,
                    "Količina" as kolicina,
                    created_at,
                    updated_at
                FROM minerali
                WHERE "Inv. broj" = ?
            """, (inv_num_float,))

            row = cursor.fetchone()
            conn.close()

            if row:
                mineral = dict(row)
                mineral['has_image'] = False
                if mineral['inventarni_broj']:
                    inv_num = int(mineral['inventarni_broj']) if isinstance(mineral['inventarni_broj'], float) else mineral['inventarni_broj']
                    mineral['inventarni_broj_display'] = f"M{inv_num}"
                else:
                    mineral['inventarni_broj_display'] = 'N/A'
                return mineral

            return None

        except Exception as e:
            logger.error(f"Error loading mineral by inventory {inv_number}: {e}")
            return None

    def search_minerals(self, query: str) -> List[Dict]:
        """Search minerals by name, inventory number, or locality."""
        if not self.available:
            return []

        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            search_specs = build_search_specs(query)
            if not search_specs:
                conn.close()
                return []

            where_clauses = []
            params: List[str] = []

            for spec in search_specs:
                term_clauses = []

                if spec['inventory_only']:
                    if spec['inv_num']:
                        term_clauses.append('"Inv. broj" = ?')
                        params.append(spec['inv_num'])
                    elif spec['inv_prefix']:
                        term_clauses.append('UPPER("Inv. broj") LIKE ?')
                        params.append(spec['inv_prefix'])
                else:
                    term_clauses.extend([
                        '"Naziv" LIKE ?',
                        '"Inv. broj" LIKE ?',
                        '"Lokalitet sa kartice" LIKE ?',
                        '"Predmet" LIKE ?'
                    ])
                    params.extend([spec['pattern']] * 4)

                    if spec['inv_num']:
                        term_clauses.append('"Inv. broj" = ?')
                        params.append(spec['inv_num'])
                    elif spec['inv_prefix']:
                        term_clauses.append('UPPER("Inv. broj") LIKE ?')
                        params.append(spec['inv_prefix'])

                if term_clauses:
                    where_clauses.append(f"({' OR '.join(term_clauses)})")

            where_sql = ' OR '.join(where_clauses) if where_clauses else '0 = 1'
            cursor.execute(
                """
                SELECT
                    id,
                    "Inv. broj" as inventarni_broj,
                    "Predmet" as predmet,
                    "Naziv" as naziv,
                    "Način nabavljanja" as nacin_nabavljanja,
                    "Datum nabavljanja" as datum_nabavljanja,
                    "Datum unosa u bazu" as datum_unosa,
                    "Uneo u bazu" as uneo_u_bazu,
                    "Legator / Našao / Doneo" as legator,
                    "Identifikovao" as identifikovao,
                    "Komentar/napomena" as komentar,
                    "Napomena/opis" as napomena,
                    "Gde se nalazi" as gde_se_nalazi,
                    "Lokalitet sa kartice" as lokalitet,
                    "U bibliografiji" as u_bibliografiji,
                    "Količina" as kolicina,
                    created_at,
                    updated_at
                FROM minerali
                WHERE """ + where_sql + """
                ORDER BY id
                LIMIT 100
                """, params)

            minerals = []
            for row in cursor.fetchall():
                mineral = dict(row)
                if mineral['inventarni_broj']:
                    inv_num = int(mineral['inventarni_broj']) if isinstance(mineral['inventarni_broj'], float) else mineral['inventarni_broj']
                    mineral['inventarni_broj_display'] = f"M{inv_num}"
                else:
                    mineral['inventarni_broj_display'] = 'N/A'
                minerals.append(mineral)

            conn.close()
            return minerals

        except Exception as e:
            logger.error(f"Error searching minerals: {e}")
            return []

    def get_statistics(self) -> Dict:
        """Get mineral collection statistics."""
        if not self.available:
            return {}

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            stats = {}

            # Total count
            cursor.execute("SELECT COUNT(*) FROM minerali")
            stats['total_minerals'] = cursor.fetchone()[0]

            # Count with inventory numbers
            cursor.execute('SELECT COUNT(*) FROM minerali WHERE "Inv. broj" IS NOT NULL')
            stats['with_inventory'] = cursor.fetchone()[0]

            # Count with locality info
            cursor.execute('SELECT COUNT(*) FROM minerali WHERE "Lokalitet sa kartice" IS NOT NULL AND "Lokalitet sa kartice" != ""')
            stats['with_locality'] = cursor.fetchone()[0]

            # Top localities
            cursor.execute('''
                SELECT "Lokalitet sa kartice", COUNT(*) as count
                FROM minerali
                WHERE "Lokalitet sa kartice" IS NOT NULL AND "Lokalitet sa kartice" != ""
                GROUP BY "Lokalitet sa kartice"
                ORDER BY count DESC
                LIMIT 10
            ''')
            stats['top_localities'] = [{'locality': row[0], 'count': row[1]} for row in cursor.fetchall()]

            conn.close()
            return stats

        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}

    def get_rruff_data_for_mineral(self, mineral_name: str) -> Optional[Dict]:
        """Get RRUFF scientific data for a mineral by name matching.

        Args:
            mineral_name: The mineral name to search for

        Returns:
            RRUFF mineral data or None if not found
        """
        if not mineral_name:
            return None

        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Try exact match first (case insensitive)
            cursor.execute("""
                SELECT
                    id, rruff_id, name, name_plain,
                    formula_rruff, formula_ima, formula_concise,
                    ideal_chemistry, chemistry_elements,
                    ima_number, ima_status, ima_mineral, ima_mineral_symbol,
                    year_first_published,
                    structural_groupname, fleischers_groupname,
                    crystal_system, crystal_systems,
                    space_group, space_groups,
                    country_type_locality, crystal_morphology,
                    oldest_known_age_ma, paragenetic_modes
                FROM rruff_minerals
                WHERE LOWER(name) = LOWER(?) OR LOWER(name_plain) = LOWER(?)
                LIMIT 1
            """, (mineral_name, mineral_name))

            row = cursor.fetchone()

            if row:
                rruff_data = dict(row)

                # Get chemistry composition
                cursor.execute("""
                    SELECT oxide, weight_percent
                    FROM rruff_chemistry
                    WHERE rruff_id = ?
                    ORDER BY weight_percent DESC
                """, (rruff_data['rruff_id'],))

                rruff_data['chemistry'] = [dict(r) for r in cursor.fetchall()]

                conn.close()
                return rruff_data

            conn.close()
            return None

        except Exception as e:
            logger.error(f"Error getting RRUFF data for {mineral_name}: {e}")
            return None

    def get_rruff_minerals(self, page: int = 1, per_page: int = 50,
                           search: str = '', crystal_system: str = '',
                           ima_status: str = '', elements: str = '') -> Dict:
        """Get RRUFF minerals with filtering."""
        if not self.available:
            return {'minerals': [], 'total': 0, 'page': 1, 'per_page': per_page, 'total_pages': 0}

        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Build WHERE clause
            where_clauses = []
            params = []

            if search:
                where_clauses.append("(name LIKE ? OR name_plain LIKE ? OR formula_rruff LIKE ? OR formula_concise LIKE ?)")
                params.extend([f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%'])

            if crystal_system:
                where_clauses.append("crystal_system = ?")
                params.append(crystal_system)

            if ima_status:
                where_clauses.append("ima_status = ?")
                params.append(ima_status)

            if elements:
                where_clauses.append("chemistry_elements LIKE ?")
                params.append(f'%{elements}%')

            where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""

            # Get total count
            cursor.execute(
                "SELECT COUNT(*) FROM rruff_minerals" + where_sql, params)
            total = cursor.fetchone()[0]

            total_pages = (total + per_page - 1) // per_page
            offset = (page - 1) * per_page

            # Get paginated results
            cursor.execute(
                """
                SELECT
                    id, rruff_id, name, name_plain,
                    formula_rruff, formula_ima, formula_concise,
                    crystal_system, ima_status
                FROM rruff_minerals
                """ + where_sql + """
                ORDER BY name
                LIMIT ? OFFSET ?
                """, params + [per_page, offset])

            minerals = [dict(row) for row in cursor.fetchall()]
            conn.close()

            return {
                'minerals': minerals,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': total_pages
            }

        except Exception as e:
            logger.error(f"Error loading RRUFF minerals: {e}")
            return {'minerals': [], 'total': 0, 'page': 1, 'per_page': per_page, 'total_pages': 0}

    def get_rruff_mineral_by_id(self, mineral_id: int) -> Optional[Dict]:
        """Get single RRUFF mineral by ID with all data including chemistry.

        Args:
            mineral_id: The database ID of the RRUFF mineral

        Returns:
            Dictionary with all mineral data and chemistry, or None if not found
        """
        if not self.available:
            return None

        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Get main mineral data
            cursor.execute("""
                SELECT *
                FROM rruff_minerals
                WHERE id = ?
            """, (mineral_id,))

            row = cursor.fetchone()
            if not row:
                conn.close()
                return None

            mineral = dict(row)

            # Get chemistry data
            cursor.execute("""
                SELECT oxide, weight_percent
                FROM rruff_chemistry
                WHERE rruff_id = ?
                ORDER BY weight_percent DESC
            """, (mineral['rruff_id'],))

            chemistry = [{'oxide': row[0], 'weight_percent': row[1]} for row in cursor.fetchall()]
            mineral['chemistry'] = chemistry

            conn.close()
            return mineral

        except Exception as e:
            logger.error(f"Error loading RRUFF mineral by ID {mineral_id}: {e}")
            return None

    def get_rruff_statistics(self) -> Dict:
        """Get RRUFF database statistics."""
        if not self.available:
            return {}

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            stats = {}

            # Total count
            cursor.execute("SELECT COUNT(*) FROM rruff_minerals")
            stats['total_minerals'] = cursor.fetchone()[0]

            # By crystal system
            cursor.execute("""
                SELECT crystal_system, COUNT(*) as count
                FROM rruff_minerals
                WHERE crystal_system IS NOT NULL AND crystal_system != ''
                GROUP BY crystal_system
                ORDER BY count DESC
            """)
            stats['by_crystal_system'] = [{'system': row[0], 'count': row[1]} for row in cursor.fetchall()]

            conn.close()
            return stats

        except Exception as e:
            logger.error(f"Error getting RRUFF statistics: {e}")
            return {}


# Singleton instance
_mineral_db = None

def get_mineral_database() -> MineralDatabase:
    """Get or create singleton MineralDatabase instance."""
    global _mineral_db
    if _mineral_db is None:
        _mineral_db = MineralDatabase()
    return _mineral_db
