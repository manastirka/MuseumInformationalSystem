#!/usr/bin/env python3
"""
RRUFF Scientific Mineral Database Loader - PostgreSQL Version
Loads general mineralogical scientific data from PostgreSQL
"""

import os
import logging
from typing import List, Dict, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

logger = logging.getLogger(__name__)

# Get DATABASE_URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system')


class RRUFFDatabase:
    """RRUFF scientific mineral database accessor - PostgreSQL version."""

    def __init__(self, db_url: str = DATABASE_URL):
        """Initialize RRUFF database."""
        self.db_url = db_url
        try:
            self.engine = create_engine(db_url, poolclass=NullPool)
            # Test connection
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM rruff_minerals"))
                count = result.scalar()
                self.available = True
                logger.info(f"RRUFF database loaded: {count} minerals from PostgreSQL")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL RRUFF database: {e}")
            self.available = False

    def get_all_minerals(self, limit: int = None) -> List[Dict]:
        """Get all RRUFF mineral records."""
        if not self.available:
            return []

        try:
            with self.engine.connect() as conn:
                params = {}
                limit_clause = ""
                if limit:
                    limit_clause = "LIMIT :limit"
                    params['limit'] = int(limit)

                query = text("""
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
                """ + limit_clause)

                result = conn.execute(query, params)
                minerals = [dict(row._mapping) for row in result]
                
            return minerals

        except Exception as e:
            logger.error(f"Error loading RRUFF minerals: {e}")
            return []

    def get_mineral_by_id(self, mineral_id: int) -> Optional[Dict]:
        """Get single RRUFF mineral by ID."""
        if not self.available:
            return None

        try:
            with self.engine.connect() as conn:
                query = text("""
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
                    WHERE id = :id
                """)
                
                result = conn.execute(query, {"id": mineral_id})
                row = result.first()
                
                if row:
                    mineral = dict(row._mapping)
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
            with self.engine.connect() as conn:
                query = text("""
                    SELECT * FROM rruff_minerals WHERE rruff_id = :rruff_id
                """)
                
                result = conn.execute(query, {"rruff_id": rruff_id})
                row = result.first()
                
                if row:
                    mineral = dict(row._mapping)
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
            with self.engine.connect() as conn:
                query = text("""
                    SELECT oxide, weight_percent
                    FROM rruff_chemistry
                    WHERE rruff_id = :rruff_id
                    ORDER BY weight_percent DESC
                """)
                
                result = conn.execute(query, {"rruff_id": rruff_id})
                chemistry = [dict(row._mapping) for row in result]
                
            return chemistry

        except Exception as e:
            logger.error(f"Error loading chemistry for {rruff_id}: {e}")
            return []

    def search_minerals(self, query: str, limit: int = 100) -> List[Dict]:
        """Search RRUFF minerals by name or formula."""
        if not self.available or not query:
            return []

        try:
            with self.engine.connect() as conn:
                search_query = text("""
                    SELECT
                        id,
                        rruff_id,
                        name,
                        name_plain,
                        formula_rruff,
                        formula_concise,
                        crystal_system,
                        ima_status
                    FROM rruff_minerals
                    WHERE 
                        name ILIKE :search OR
                        name_plain ILIKE :search OR
                        formula_rruff ILIKE :search OR
                        formula_concise ILIKE :search
                    ORDER BY name
                    LIMIT :limit
                """)
                
                result = conn.execute(search_query, {
                    "search": f"%{query}%",
                    "limit": limit
                })
                minerals = [dict(row._mapping) for row in result]
                
            return minerals

        except Exception as e:
            logger.error(f"Error searching RRUFF minerals: {e}")
            return []

    def get_statistics(self) -> Dict:
        """Get RRUFF database statistics."""
        if not self.available:
            return {}

        try:
            with self.engine.connect() as conn:
                stats = {}
                
                # Total minerals
                result = conn.execute(text("SELECT COUNT(*) FROM rruff_minerals"))
                stats['total_minerals'] = result.scalar()
                
                # By crystal system
                result = conn.execute(text("""
                    SELECT crystal_system, COUNT(*) as count
                    FROM rruff_minerals
                    WHERE crystal_system IS NOT NULL
                    GROUP BY crystal_system
                    ORDER BY count DESC
                """))
                stats['by_crystal_system'] = [
                    {'crystal_system': row[0], 'count': row[1]} 
                    for row in result
                ]
                
                # By IMA status
                result = conn.execute(text("""
                    SELECT ima_status, COUNT(*) as count
                    FROM rruff_minerals
                    WHERE ima_status IS NOT NULL
                    GROUP BY ima_status
                    ORDER BY count DESC
                """))
                stats['by_ima_status'] = [
                    {'ima_status': row[0], 'count': row[1]} 
                    for row in result
                ]
                
            return stats

        except Exception as e:
            logger.error(f"Error getting RRUFF statistics: {e}")
            return {}

    def get_minerals_paginated(self, page: int = 1, per_page: int = 50,
                               search: str = '', crystal_system: str = '',
                               ima_status: str = '', elements: str = '') -> Dict:
        """Get RRUFF minerals with pagination and filtering."""
        if not self.available:
            return {'minerals': [], 'total': 0, 'page': 1, 'per_page': per_page, 'total_pages': 0}

        try:
            with self.engine.connect() as conn:
                # Build WHERE clause
                where_clauses = []
                params = {}
                
                if search:
                    where_clauses.append("""(
                        name ILIKE :search OR 
                        name_plain ILIKE :search OR 
                        formula_rruff ILIKE :search OR 
                        formula_concise ILIKE :search
                    )""")
                    params['search'] = f'%{search}%'
                
                if crystal_system:
                    where_clauses.append("crystal_system = :crystal_system")
                    params['crystal_system'] = crystal_system
                
                if ima_status:
                    where_clauses.append("ima_status = :ima_status")
                    params['ima_status'] = ima_status
                
                if elements:
                    where_clauses.append("chemistry_elements ILIKE :elements")
                    params['elements'] = f'%{elements}%'
                
                where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
                
                # Get total count
                count_query = text(
                    "SELECT COUNT(*) FROM rruff_minerals" + where_sql
                )
                result = conn.execute(count_query, params)
                total = result.scalar()

                total_pages = (total + per_page - 1) // per_page
                offset = (page - 1) * per_page

                # Get paginated results
                params['limit'] = per_page
                params['offset'] = offset

                data_query = text(
                    "SELECT id, rruff_id, name, name_plain, "
                    "formula_rruff, formula_ima, formula_concise, "
                    "crystal_system, ima_status "
                    "FROM rruff_minerals "
                    + where_sql
                    + " ORDER BY name LIMIT :limit OFFSET :offset"
                )
                
                result = conn.execute(data_query, params)
                minerals = [dict(row._mapping) for row in result]
                
            return {
                'minerals': minerals,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': total_pages
            }

        except Exception as e:
            logger.error(f"Error getting paginated RRUFF minerals: {e}")
            return {'minerals': [], 'total': 0, 'page': 1, 'per_page': per_page, 'total_pages': 0}
