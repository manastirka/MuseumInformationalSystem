#!/usr/bin/env python3
"""
RRUFF Scientific Mineral Database Loader
Loads general mineralogical scientific data from RRUFF Project database
"""

import sqlite3
import os
import logging
from contextlib import closing
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    'PrirodnjackiMuzej',
    'prirodnjacki_muzej.sqlite'
)


class RRUFFDatabase:
    """RRUFF scientific mineral database accessor."""

    def __init__(self, db_path: str = DB_PATH):
        """Initialize RRUFF database."""
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            logger.error(f"RRUFF database not found: {self.db_path}")
            self.available = False
        else:
            self.available = True
            logger.info(f"RRUFF database loaded from: {self.db_path}")

    def _get_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)

    def get_all_minerals(self, limit: int = None) -> List[Dict]:
        """Get all RRUFF mineral records."""
        if not self.available:
            return []

        try:
            with closing(self._get_connection()) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                params = []
                limit_clause = ""
                if limit is not None:
                    limit_clause = "LIMIT ?"
                    params.append(int(limit))

                cursor.execute("""
                    SELECT
                        id,
                        rruff_id,
                        name,
                        name_plain,
                        formula_rruff,
                        formula_ima,
                        formula_concise,
                        formula_html,
                        ideal_chemistry,
                        chemistry_elements,
                        ima_number,
                        ima_status,
                        ima_mineral,
                        year_first_published,
                        structural_groupname,
                        fleischers_groupname,
                        crystal_system,
                        space_group,
                        country_type_locality,
                        crystal_morphology,
                        oldest_known_age_ma,
                        paragenetic_modes,
                        status_notes
                    FROM rruff_minerals
                    ORDER BY name
                """ + limit_clause, params)

                minerals = []
                for row in cursor.fetchall():
                    minerals.append(dict(row))

                return minerals

        except Exception as e:
            logger.error(f"Error loading RRUFF minerals: {e}")
            return []

    def get_mineral_by_id(self, mineral_id: int) -> Optional[Dict]:
        """Get single RRUFF mineral by ID."""
        if not self.available:
            return None

        try:
            with closing(self._get_connection()) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT
                        id,
                        rruff_id,
                        name,
                        name_plain,
                        formula_rruff,
                        formula_ima,
                        formula_concise,
                        formula_html,
                        ideal_chemistry,
                        chemistry_elements,
                        valence_elements,
                        ima_number,
                        ima_status,
                        ima_mineral,
                        ima_mineral_symbol,
                        year_first_published,
                        structural_groupname,
                        fleischers_groupname,
                        fleischers_glossary,
                        crystal_system,
                        crystal_systems,
                        space_group,
                        space_groups,
                        country_type_locality,
                        crystal_morphology,
                        oldest_known_age_ma,
                        paragenetic_modes,
                        status_notes,
                        rruff_ids,
                        database_id
                    FROM rruff_minerals
                    WHERE id = ?
                """, (mineral_id,))

                row = cursor.fetchone()

            if row:
                mineral = dict(row)
                # Get chemistry data
                mineral['chemistry'] = self.get_mineral_chemistry(mineral['rruff_id'])
                return mineral

            return None

        except Exception as e:
            logger.error(f"Error loading RRUFF mineral {mineral_id}: {e}")
            return None

    def get_mineral_by_rruff_id(self, rruff_id: str) -> Optional[Dict]:
        """Get mineral by RRUFF ID."""
        if not self.available:
            return None

        try:
            with closing(self._get_connection()) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT * FROM rruff_minerals WHERE rruff_id = ?
                """, (rruff_id,))

                row = cursor.fetchone()

            if row:
                mineral = dict(row)
                mineral['chemistry'] = self.get_mineral_chemistry(rruff_id)
                return mineral

            return None

        except Exception as e:
            logger.error(f"Error loading RRUFF mineral {rruff_id}: {e}")
            return None

    def get_mineral_chemistry(self, rruff_id: str) -> List[Dict]:
        """Get chemical composition for a mineral."""
        if not self.available:
            return []

        try:
            with closing(self._get_connection()) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT oxide, weight_percent
                    FROM rruff_chemistry
                    WHERE rruff_id = ?
                    ORDER BY weight_percent DESC
                """, (rruff_id,))

                chemistry = [dict(row) for row in cursor.fetchall()]
                return chemistry

        except Exception as e:
            logger.error(f"Error loading chemistry for {rruff_id}: {e}")
            return []

    def search_minerals(self, query: str, limit: int = 100) -> List[Dict]:
        """Search RRUFF minerals by name or formula."""
        if not self.available:
            return []

        try:
            with closing(self._get_connection()) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT
                        id,
                        rruff_id,
                        name,
                        formula_rruff,
                        formula_ima,
                        crystal_system,
                        ima_status,
                        country_type_locality
                    FROM rruff_minerals
                    WHERE
                        name LIKE ? OR
                        name_plain LIKE ? OR
                        formula_rruff LIKE ? OR
                        formula_ima LIKE ? OR
                        rruff_id LIKE ? OR
                        chemistry_elements LIKE ?
                    ORDER BY name
                    LIMIT ?
                """, (f'%{query}%', f'%{query}%', f'%{query}%',
                      f'%{query}%', f'%{query}%', f'%{query}%', limit))

                minerals = [dict(row) for row in cursor.fetchall()]
                return minerals

        except Exception as e:
            logger.error(f"Error searching RRUFF minerals: {e}")
            return []

    def get_statistics(self) -> Dict:
        """Get RRUFF database statistics."""
        if not self.available:
            return {}

        try:
            with closing(self._get_connection()) as conn:
                cursor = conn.cursor()

                stats = {}

                # Total count
                cursor.execute("SELECT COUNT(*) FROM rruff_minerals")
                stats['total_minerals'] = cursor.fetchone()[0]

                # IMA approved
                cursor.execute("SELECT COUNT(*) FROM rruff_minerals WHERE ima_status = 'Approved'")
                stats['ima_approved'] = cursor.fetchone()[0]

                # By crystal system
                cursor.execute("""
                    SELECT crystal_system, COUNT(*) as count
                    FROM rruff_minerals
                    WHERE crystal_system IS NOT NULL AND crystal_system != ''
                    GROUP BY crystal_system
                    ORDER BY count DESC
                """)
                stats['by_crystal_system'] = [
                    {'system': row[0], 'count': row[1]}
                    for row in cursor.fetchall()
                ]

                # Top countries
                cursor.execute("""
                    SELECT country_type_locality, COUNT(*) as count
                    FROM rruff_minerals
                    WHERE country_type_locality IS NOT NULL AND country_type_locality != ''
                    GROUP BY country_type_locality
                    ORDER BY count DESC
                    LIMIT 10
                """)
                stats['top_countries'] = [
                    {'country': row[0], 'count': row[1]}
                    for row in cursor.fetchall()
                ]

                # Top structural groups
                cursor.execute("""
                    SELECT structural_groupname, COUNT(*) as count
                    FROM rruff_minerals
                    WHERE structural_groupname IS NOT NULL
                      AND structural_groupname != ''
                      AND structural_groupname != 'Not in a structural group'
                    GROUP BY structural_groupname
                    ORDER BY count DESC
                    LIMIT 10
                """)
                stats['top_groups'] = [
                    {'group': row[0], 'count': row[1]}
                    for row in cursor.fetchall()
                ]

                return stats

        except Exception as e:
            logger.error(f"Error getting RRUFF statistics: {e}")
            return {}

    def get_by_crystal_system(self, crystal_system: str) -> List[Dict]:
        """Get minerals by crystal system."""
        if not self.available:
            return []

        try:
            with closing(self._get_connection()) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT
                        id, rruff_id, name, formula_rruff,
                        crystal_system, space_group
                    FROM rruff_minerals
                    WHERE crystal_system = ?
                    ORDER BY name
                    LIMIT 100
                """, (crystal_system,))

                minerals = [dict(row) for row in cursor.fetchall()]
                return minerals

        except Exception as e:
            logger.error(f"Error getting minerals by crystal system: {e}")
            return []


# Singleton instance
_rruff_db = None

def get_rruff_database() -> RRUFFDatabase:
    """Get or create singleton RRUFFDatabase instance."""
    global _rruff_db
    if _rruff_db is None:
        _rruff_db = RRUFFDatabase()
    return _rruff_db
