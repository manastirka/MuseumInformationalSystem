#!/usr/bin/env python3
"""
Mineral Database Loader - PostgreSQL Version
Loads mineral collection data from PostgreSQL database
"""

import os
import logging
from typing import List, Dict, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

from mineral_search_utils import build_search_specs

logger = logging.getLogger(__name__)

# Get DATABASE_URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql+psycopg://aleksandarlukovic@localhost:5432/museum_system')


class MineralDatabase:
    """Mineralogical collection database accessor - PostgreSQL version."""

    # Фототека је једини извор слика. Веза иде на инвентарни број (не на id),
    # исто као `glavne_fotografije_predmeta` у fototeka_views — рачунају се само
    # спремне и необрисане фотографије. Видљивост се овде не филтрира: ово служи
    # сортирању по слици, а не приказу.
    _HAS_IMAGE_SQL = """
        EXISTS (
            SELECT 1
            FROM foto_veza_predmet v
            JOIN fotografije f ON f.id = v.fotografija_id
            WHERE v.database_name = 'mineral'
              AND v.inventarni_broj = minerals.inventory_number
              AND f.obrisana = FALSE
              AND f.status = 'spremna'
        )
    """

    def __init__(self, db_url: str = DATABASE_URL):
        """Initialize mineral database."""
        self.db_url = db_url
        try:
            self.engine = create_engine(db_url, poolclass=NullPool)
            # Test connection
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM minerals"))
                count = result.scalar()
                self.available = True
                logger.info(f"Mineral database loaded: {count} minerals from PostgreSQL")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL mineral database: {e}")
            self.available = False

    def get_all_minerals(self, page: int = 1, per_page: int = 50,
                         sort_by: str = 'id', sort_order: str = 'asc',
                         physical: str = 'all') -> Dict:
        """Get mineral records with pagination and sorting.

        Returns:
            Dict with 'minerals', 'total', 'page', 'per_page', 'total_pages'
        """
        if not self.available:
            return {'minerals': [], 'total': 0, 'page': 1, 'per_page': per_page, 'total_pages': 0}

        try:
            with self.engine.connect() as conn:
                # Validate sort column (map old names to new PostgreSQL schema)
                valid_sort_columns = {
                    'id': 'id',
                    'image': 'has_image',
                    'inventarni_broj': 'inventory_number',
                    'naziv': 'item_name',
                    'predmet': 'item_name',
                    'lokalitet': 'card_locality',
                    'datum_nabavljanja': 'acquisition_date',
                    'gde_se_nalazi': 'storage_location',
                    'nacin_nabavljanja': 'acquisition_method',
                    'legator': 'donor',
                    'identifikovao': 'identifier',
                    'kolicina': 'quantity',
                    'datum_unosa': 'input_date'
                }

                sort_column = valid_sort_columns.get(sort_by, 'id')
                if sort_column not in valid_sort_columns.values():
                    sort_column = 'id'
                sort_direction = 'DESC' if sort_order.lower() == 'desc' else 'ASC'

                # Build ORDER BY from validated whitelist values only
                if sort_column == 'inventory_number':
                    nulls_fallback = '999999999' if sort_direction == 'ASC' else '-1'
                    order_clause = (
                        "CASE WHEN inventory_number ~ '^[0-9]+$' THEN 0 "
                        "WHEN inventory_number LIKE 'BEZ-%' THEN 2 ELSE 1 END ASC, "
                        "CASE WHEN inventory_number ~ '^[0-9]+$' "
                        "THEN CAST(inventory_number AS INTEGER) ELSE 0 END " + sort_direction + ", "
                        "inventory_number " + sort_direction + " NULLS LAST"
                    )
                elif sort_column == 'storage_location':
                    nulls_fallback = '999999999' if sort_direction == 'ASC' else '-1'
                    order_clause = (
                        "CASE WHEN storage_location ~ '[0-9]' THEN "
                        "CAST(SUBSTRING(storage_location FROM '([0-9]+)') AS INTEGER) "
                        "ELSE " + nulls_fallback + " END " + sort_direction + ", "
                        "storage_location " + sort_direction + " NULLS LAST"
                    )
                elif sort_column == 'has_image':
                    order_clause = "has_image " + sort_direction + ", id ASC"
                else:
                    order_clause = sort_column + " " + sort_direction + " NULLS LAST"

                # Optional physical-presence filter (книга vs депо)
                if physical == 'unconfirmed':
                    physical_where = "WHERE physical_presence_confirmed = FALSE "
                elif physical == 'confirmed':
                    physical_where = "WHERE physical_presence_confirmed = TRUE "
                else:
                    physical_where = ""

                # Get total count
                result = conn.execute(text("SELECT COUNT(*) FROM minerals " + physical_where))
                total = result.scalar()

                total_pages = (total + per_page - 1) // per_page
                offset = (page - 1) * per_page

                # Get paginated results
                query = text(
                    "SELECT id, "
                    + self._HAS_IMAGE_SQL + " as has_image, "
                    "inventory_number as inventarni_broj, "
                    "item_name as predmet, "
                    "item_name as naziv, "
                    "acquisition_method as nacin_nabavljanja, "
                    "acquisition_date as datum_nabavljanja, "
                    "input_date as datum_unosa, "
                    "input_by as uneo_u_bazu, "
                    "donor as legator, "
                    "identifier as identifikovao, "
                    "comments as komentar, "
                    "description as napomena, "
                    "storage_location as gde_se_nalazi, "
                    "card_locality as lokalitet, "
                    "bibliography_flag as u_bibliografiji, "
                    "quantity as kolicina, "
                    "physical_presence_confirmed, source, "
                    "created_at, updated_at "
                    "FROM minerals "
                    + physical_where +
                    "ORDER BY " + order_clause + " "
                    "LIMIT :limit OFFSET :offset"
                )

                result = conn.execute(query, {"limit": per_page, "offset": offset})
                
                minerals = []
                for row in result.mappings():
                    mineral = dict(row)

                    # Format inventory number for display
                    if mineral['inventarni_broj']:
                        try:
                            inv_num = int(float(mineral['inventarni_broj']))
                            mineral['inventarni_broj_display'] = f"M{inv_num}"
                        except (ValueError, TypeError):
                            mineral['inventarni_broj_display'] = str(mineral['inventarni_broj'])
                    else:
                        mineral['inventarni_broj_display'] = 'N/A'

                    minerals.append(mineral)

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
            with self.engine.connect() as conn:
                query = text("""
                    SELECT
                        id,
                        inventory_number as inventarni_broj,
                        item_name as predmet,
                        item_name as naziv,
                        acquisition_method as nacin_nabavljanja,
                        acquisition_date as datum_nabavljanja,
                        input_date as datum_unosa,
                        input_by as uneo_u_bazu,
                        donor as legator,
                        identifier as identifikovao,
                        comments as komentar,
                        description as napomena,
                        storage_location as gde_se_nalazi,
                        card_locality as lokalitet,
                        bibliography_flag as u_bibliografiji,
                        quantity as kolicina,
                        created_at,
                        updated_at
                    FROM minerals
                    WHERE id = :id
                """)

                result = conn.execute(query, {"id": mineral_id})
                row = result.mappings().first()

                if row:
                    mineral = dict(row)
                    if mineral['inventarni_broj']:
                        try:
                            inv_num = int(float(mineral['inventarni_broj']))
                            mineral['inventarni_broj_display'] = f"M{inv_num}"
                        except (ValueError, TypeError):
                            mineral['inventarni_broj_display'] = str(mineral['inventarni_broj'])
                    else:
                        mineral['inventarni_broj_display'] = 'N/A'
                    return mineral

                return None

        except Exception as e:
            logger.error(f"Error loading mineral {mineral_id}: {e}")
            return None

    def add_mineral(self, mineral_data: Dict) -> Optional[int]:
        """Add a new mineral to the database.

        Args:
            mineral_data: Dictionary with mineral fields

        Returns:
            The ID of the newly created mineral, or None on failure
        """
        if not self.available:
            return None

        try:
            with self.engine.connect() as conn:
                query = text("""
                    INSERT INTO minerals (
                        inventory_number,
                        item_name,
                        acquisition_method,
                        acquisition_date,
                        input_date,
                        input_by,
                        donor,
                        identifier,
                        comments,
                        description,
                        storage_location,
                        card_locality,
                        bibliography_flag,
                        quantity,
                        created_at,
                        updated_at
                    ) VALUES (
                        :inventory_number,
                        :item_name,
                        :acquisition_method,
                        :acquisition_date,
                        :input_date,
                        :input_by,
                        :donor,
                        :identifier,
                        :comments,
                        :description,
                        :storage_location,
                        :card_locality,
                        :bibliography_flag,
                        :quantity,
                        NOW(),
                        NOW()
                    ) RETURNING id
                """)

                result = conn.execute(query, {
                    'inventory_number': mineral_data.get('inventory_number', ''),
                    'item_name': mineral_data.get('item_name', ''),
                    'acquisition_method': mineral_data.get('acquisition_method', ''),
                    'acquisition_date': mineral_data.get('acquisition_date') or None,
                    'input_date': mineral_data.get('input_date') or None,
                    'input_by': mineral_data.get('input_by', ''),
                    'donor': mineral_data.get('donor', ''),
                    'identifier': mineral_data.get('identifier', ''),
                    'comments': mineral_data.get('comments', ''),
                    'description': mineral_data.get('description', ''),
                    'storage_location': mineral_data.get('storage_location', ''),
                    'card_locality': mineral_data.get('card_locality', ''),
                    'bibliography_flag': mineral_data.get('bibliography_flag', False),
                    'quantity': mineral_data.get('quantity', 1)
                })

                conn.commit()
                new_id = result.scalar()
                logger.info(f"Added new mineral with ID: {new_id}")
                return new_id

        except Exception as e:
            logger.error(f"Error adding mineral: {e}")
            return None

    def update_mineral(self, mineral_id: int, mineral_data: Dict) -> bool:
        """Update an existing mineral in the database.

        Args:
            mineral_id: The ID of the mineral to update
            mineral_data: Dictionary with updated mineral fields

        Returns:
            True if successful, False otherwise
        """
        if not self.available:
            return False

        try:
            with self.engine.connect() as conn:
                query = text("""
                    UPDATE minerals SET
                        inventory_number = :inventory_number,
                        item_name = :item_name,
                        acquisition_method = :acquisition_method,
                        acquisition_date = :acquisition_date,
                        input_date = :input_date,
                        input_by = :input_by,
                        donor = :donor,
                        identifier = :identifier,
                        comments = :comments,
                        description = :description,
                        storage_location = :storage_location,
                        card_locality = :card_locality,
                        bibliography_flag = :bibliography_flag,
                        quantity = :quantity,
                        updated_at = NOW()
                    WHERE id = :id
                """)

                result = conn.execute(query, {
                    'id': mineral_id,
                    'inventory_number': mineral_data.get('inventory_number', ''),
                    'item_name': mineral_data.get('item_name', ''),
                    'acquisition_method': mineral_data.get('acquisition_method', ''),
                    'acquisition_date': mineral_data.get('acquisition_date') or None,
                    'input_date': mineral_data.get('input_date') or None,
                    'input_by': mineral_data.get('input_by', ''),
                    'donor': mineral_data.get('donor', ''),
                    'identifier': mineral_data.get('identifier', ''),
                    'comments': mineral_data.get('comments', ''),
                    'description': mineral_data.get('description', ''),
                    'storage_location': mineral_data.get('storage_location', ''),
                    'card_locality': mineral_data.get('card_locality', ''),
                    'bibliography_flag': mineral_data.get('bibliography_flag', False),
                    'quantity': mineral_data.get('quantity', 1)
                })

                if result.rowcount == 0:
                    conn.rollback()
                    logger.warning(f"Update matched no mineral with ID: {mineral_id}")
                    return False

                conn.commit()
                logger.info(f"Updated mineral with ID: {mineral_id}")
                return True

        except Exception as e:
            logger.error(f"Error updating mineral {mineral_id}: {e}")
            return False

    def delete_mineral(self, mineral_id: int) -> bool:
        """Delete a mineral from the database.

        Args:
            mineral_id: The ID of the mineral to delete

        Returns:
            True if successful, False otherwise
        """
        if not self.available:
            return False

        try:
            with self.engine.connect() as conn:
                query = text("DELETE FROM minerals WHERE id = :id")
                result = conn.execute(query, {'id': mineral_id})
                if result.rowcount == 0:
                    conn.rollback()
                    logger.warning(f"Delete matched no mineral with ID: {mineral_id}")
                    return False
                conn.commit()
                logger.info(f"Deleted mineral with ID: {mineral_id}")
                return True

        except Exception as e:
            logger.error(f"Error deleting mineral {mineral_id}: {e}")
            return False

    def get_next_inventory_number(self) -> str:
        """Get the next available inventory number."""
        if not self.available:
            return "1"

        try:
            with self.engine.connect() as conn:
                query = text("""
                    SELECT MAX(CAST(inventory_number AS INTEGER))
                    FROM minerals
                    WHERE inventory_number ~ '^[0-9]+$'
                """)
                result = conn.execute(query)
                max_num = result.scalar()

                if max_num:
                    return str(max_num + 1)
                return "1"

        except Exception as e:
            # Транзијентна DB грешка не сме да „измисли" инвентарски број 1 —
            # куратор би преписао постојећи запис (ревизија #6).
            logger.error(f"Error getting next inventory number: {e}")
            raise

    def get_mineral_by_inventory_number(self, inv_number: str) -> Optional[Dict]:
        """Get mineral by inventory number (supports M12345 or 12345 format)."""
        if not self.available:
            return None

        # Remove 'M' prefix if present
        inv_num_clean = inv_number.replace('M', '').replace('m', '').strip()

        try:
            with self.engine.connect() as conn:
                query = text("""
                    SELECT
                        id,
                        inventory_number as inventarni_broj,
                        item_name as predmet,
                        item_name as naziv,
                        acquisition_method as nacin_nabavljanja,
                        acquisition_date as datum_nabavljanja,
                        input_date as datum_unosa,
                        input_by as uneo_u_bazu,
                        donor as legator,
                        identifier as identifikovao,
                        comments as komentar,
                        description as napomena,
                        storage_location as gde_se_nalazi,
                        card_locality as lokalitet,
                        bibliography_flag as u_bibliografiji,
                        quantity as kolicina,
                        created_at,
                        updated_at
                    FROM minerals
                    WHERE inventory_number = :inv_num
                """)

                result = conn.execute(query, {"inv_num": inv_num_clean})
                row = result.mappings().first()

                if row:
                    mineral = dict(row)
                    if mineral['inventarni_broj']:
                        try:
                            inv_num = int(float(mineral['inventarni_broj']))
                            mineral['inventarni_broj_display'] = f"M{inv_num}"
                        except (ValueError, TypeError):
                            mineral['inventarni_broj_display'] = str(mineral['inventarni_broj'])
                    else:
                        mineral['inventarni_broj_display'] = 'N/A'
                    return mineral

                return None

        except Exception as e:
            logger.error(f"Error loading mineral by inventory number {inv_number}: {e}")
            return None

    def search_minerals(self, query: str, page: int = 1, per_page: int = 50,
                        sort_by: str = 'relevance', sort_order: str = 'desc',
                        physical: str = 'all') -> Dict:
        """Smart search minerals by text query with optional sorting."""
        if not self.available:
            return {'minerals': [], 'total': 0, 'page': 1, 'per_page': per_page, 'total_pages': 0}

        try:
            with self.engine.connect() as conn:
                query = query.strip()
                search_specs = build_search_specs(query)
                if not search_specs:
                    return {'minerals': [], 'total': 0, 'page': 1, 'per_page': per_page, 'total_pages': 0}

                search_filters = []
                relevance_cases = []
                params: Dict[str, str] = {}

                for index, spec in enumerate(search_specs):
                    pattern_key = f"pattern_{index}"
                    exact_key = f"exact_query_{index}"
                    starts_with_key = f"starts_with_{index}"
                    inv_num_key = f"inv_num_{index}"
                    inv_prefix_key = f"inv_prefix_{index}"

                    filter_parts = []

                    if spec['inventory_only']:
                        if spec['inv_num']:
                            params[inv_num_key] = spec['inv_num']
                            filter_parts.append(f"inventory_number = :{inv_num_key}")
                            relevance_cases.append(f"WHEN inventory_number = :{inv_num_key} THEN 100")
                        elif spec['inv_prefix']:
                            params[inv_prefix_key] = spec['inv_prefix']
                            filter_parts.append(f"inventory_number ILIKE :{inv_prefix_key}")
                            relevance_cases.append(f"WHEN inventory_number ILIKE :{inv_prefix_key} THEN 100")
                    else:
                        params[pattern_key] = spec['pattern']
                        params[exact_key] = spec['term']
                        params[starts_with_key] = spec['starts_with']

                        filter_parts.extend([
                            f"item_name ILIKE :{pattern_key}",
                            f"inventory_number::TEXT ILIKE :{pattern_key}",
                            f"card_locality ILIKE :{pattern_key}",
                            f"storage_location ILIKE :{pattern_key}",
                            f"donor ILIKE :{pattern_key}",
                            f"identifier ILIKE :{pattern_key}",
                            f"comments ILIKE :{pattern_key}",
                            f"description ILIKE :{pattern_key}",
                            f"acquisition_method ILIKE :{pattern_key}",
                        ])

                        if spec['inv_num']:
                            params[inv_num_key] = spec['inv_num']
                            filter_parts.append(f"inventory_number = :{inv_num_key}")
                            relevance_cases.append(f"WHEN inventory_number = :{inv_num_key} THEN 100")
                        elif spec['inv_prefix']:
                            params[inv_prefix_key] = spec['inv_prefix']
                            filter_parts.append(f"inventory_number ILIKE :{inv_prefix_key}")
                            relevance_cases.append(f"WHEN inventory_number ILIKE :{inv_prefix_key} THEN 100")

                        relevance_cases.extend([
                            f"WHEN LOWER(item_name) = LOWER(:{exact_key}) THEN 50",
                            f"WHEN LOWER(item_name) LIKE LOWER(:{starts_with_key}) THEN 30",
                            f"WHEN item_name ILIKE :{pattern_key} THEN 20",
                            f"WHEN card_locality ILIKE :{pattern_key} THEN 15",
                            f"WHEN inventory_number::TEXT ILIKE :{pattern_key} THEN 10",
                        ])

                    if filter_parts:
                        search_filters.append(f"({' OR '.join(filter_parts)})")

                where_clause = " OR ".join(search_filters) if search_filters else "FALSE"

                # Optional physical-presence filter (книга vs депо) composed with
                # the text-search predicate. Wrap the OR-joined search filters so
                # the AND binds against the whole search expression, not its last term.
                if physical == 'unconfirmed':
                    where_clause = "(" + where_clause + ") AND physical_presence_confirmed = FALSE"
                elif physical == 'confirmed':
                    where_clause = "(" + where_clause + ") AND physical_presence_confirmed = TRUE"

                relevance_clause = (
                    "CASE\n                            "
                    + "\n                            ".join(relevance_cases)
                    + "\n                            ELSE 1\n                        END"
                )

                # Build smart search with relevance scoring
                # Score: exact name match (10), starts with (5), contains (2), other fields (1)
                count_query = text(
                    "SELECT COUNT(*) FROM minerals WHERE " + where_clause
                )

                result = conn.execute(count_query, params)
                total = result.scalar()

                total_pages = (total + per_page - 1) // per_page
                offset = (page - 1) * per_page

                # Determine ORDER BY clause based on sort parameters
                valid_sort_columns = {
                    'id': 'id',
                    'image': 'has_image',
                    'inventarni_broj': 'inventory_number',
                    'naziv': 'item_name',
                    'predmet': 'item_name',
                    'lokalitet': 'card_locality',
                    'datum_nabavljanja': 'acquisition_date',
                    'gde_se_nalazi': 'storage_location',
                    'nacin_nabavljanja': 'acquisition_method',
                    'legator': 'donor',
                    'identifikovao': 'identifier',
                    'kolicina': 'quantity',
                    'datum_unosa': 'input_date',
                    'relevance': 'relevance'
                }

                sort_column = valid_sort_columns.get(sort_by, 'relevance')
                if sort_column not in valid_sort_columns.values():
                    sort_column = 'relevance'
                sort_direction = 'DESC' if sort_order.lower() == 'desc' else 'ASC'

                # Build ORDER BY from validated whitelist values only
                if sort_column == 'inventory_number':
                    order_clause = (
                        "CASE WHEN inventory_number ~ '^[0-9]+$' THEN 0 "
                        "WHEN inventory_number LIKE 'BEZ-%' THEN 2 ELSE 1 END ASC, "
                        "CASE WHEN inventory_number ~ '^[0-9]+$' "
                        "THEN CAST(inventory_number AS INTEGER) ELSE 0 END " + sort_direction + ", "
                        "inventory_number " + sort_direction + " NULLS LAST"
                    )
                elif sort_column == 'storage_location':
                    nulls_fallback = '999999999' if sort_direction == 'ASC' else '-1'
                    order_clause = (
                        "CASE WHEN storage_location ~ '[0-9]' THEN "
                        "CAST(SUBSTRING(storage_location FROM '([0-9]+)') AS INTEGER) "
                        "ELSE " + nulls_fallback + " END " + sort_direction + ", "
                        "storage_location " + sort_direction + " NULLS LAST"
                    )
                elif sort_column == 'has_image':
                    order_clause = "has_image " + sort_direction + ", id ASC"
                elif sort_column == 'relevance':
                    order_clause = "relevance DESC, item_name ASC"
                else:
                    order_clause = sort_column + " " + sort_direction + " NULLS LAST"

                # Get paginated search results with relevance ranking
                search_query = text(
                    "SELECT id, "
                    + self._HAS_IMAGE_SQL + " as has_image, "
                    "inventory_number as inventarni_broj, "
                    "item_name as predmet, item_name as naziv, "
                    "acquisition_method as nacin_nabavljanja, "
                    "acquisition_date as datum_nabavljanja, "
                    "input_date as datum_unosa, input_by as uneo_u_bazu, "
                    "donor as legator, identifier as identifikovao, "
                    "comments as komentar, description as napomena, "
                    "storage_location as gde_se_nalazi, "
                    "card_locality as lokalitet, "
                    "bibliography_flag as u_bibliografiji, "
                    "quantity as kolicina, "
                    "physical_presence_confirmed, source, "
                    "created_at, updated_at, "
                    + relevance_clause + " as relevance "
                    "FROM minerals "
                    "WHERE " + where_clause + " "
                    "ORDER BY " + order_clause + " "
                    "LIMIT :limit OFFSET :offset"
                )

                query_params = dict(params)
                query_params.update({
                    "limit": per_page,
                    "offset": offset
                })

                result = conn.execute(search_query, query_params)

                minerals = []
                for row in result.mappings():
                    mineral = dict(row)

                    # Remove relevance score from output
                    mineral.pop('relevance', None)

                    # Format inventory number for display
                    if mineral['inventarni_broj']:
                        try:
                            inv_num = int(float(mineral['inventarni_broj']))
                            mineral['inventarni_broj_display'] = f"M{inv_num}"
                        except (ValueError, TypeError):
                            mineral['inventarni_broj_display'] = str(mineral['inventarni_broj'])
                    else:
                        mineral['inventarni_broj_display'] = 'N/A'

                    minerals.append(mineral)

                return {
                    'minerals': minerals,
                    'total': total,
                    'page': page,
                    'per_page': per_page,
                    'total_pages': total_pages
                }

        except Exception as e:
            logger.error(f"Error searching minerals: {e}")
            return {'minerals': [], 'total': 0, 'page': 1, 'per_page': per_page, 'total_pages': 0}

    def get_statistics(self) -> Dict:
        """Get mineral collection statistics."""
        if not self.available:
            return {}

        try:
            with self.engine.connect() as conn:
                stats = {}
                
                # Total count
                result = conn.execute(text("SELECT COUNT(*) FROM minerals"))
                stats['total_minerals'] = result.scalar()
                
                # Count with locations
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM minerals 
                    WHERE storage_location IS NOT NULL AND storage_location != ''
                """))
                stats['with_location'] = result.scalar()
                
                # Count with locality
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM minerals 
                    WHERE card_locality IS NOT NULL AND card_locality != ''
                """))
                stats['with_locality'] = result.scalar()
                
                return stats

        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}

    def get_rruff_statistics(self) -> Dict:
        """Get RRUFF database statistics."""
        if not self.available:
            return {}
        
        try:
            with self.engine.connect() as conn:
                stats = {}
                
                # Total RRUFF minerals
                result = conn.execute(text("SELECT COUNT(*) FROM rruff_minerals"))
                stats['total_minerals'] = result.scalar()
                
                # By crystal system
                result = conn.execute(text("""
                    SELECT crystal_system, COUNT(*) as count
                    FROM rruff_minerals
                    WHERE crystal_system IS NOT NULL AND crystal_system != ''
                    GROUP BY crystal_system
                    ORDER BY count DESC
                    LIMIT 10
                """))
                stats['by_crystal_system'] = [
                    {'crystal_system': row[0], 'count': row[1]} 
                    for row in result
                ]
                
                # By IMA status
                result = conn.execute(text("""
                    SELECT ima_status, COUNT(*) as count
                    FROM rruff_minerals
                    WHERE ima_status IS NOT NULL AND ima_status != ''
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
    
    def get_rruff_minerals(self, page: int = 1, per_page: int = 50,
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
    
    def get_rruff_mineral_by_id(self, mineral_id: int) -> Optional[Dict]:
        """Get single RRUFF mineral by ID with full details."""
        if not self.available:
            return None

        try:
            with self.engine.connect() as conn:
                query = text("""
                    SELECT
                        id, rruff_id, name, name_plain,
                        formula_rruff, formula_ima, formula_concise, formula_html,
                        ideal_chemistry, chemistry_elements, valence_elements,
                        ima_number, ima_status, ima_mineral, ima_mineral_symbol,
                        year_first_published, structural_groupname, fleischers_groupname,
                        fleischers_glossary, crystal_system, crystal_systems,
                        space_group, space_groups, country_type_locality,
                        crystal_morphology, oldest_known_age_ma, paragenetic_modes,
                        status_notes, rruff_ids, database_id
                    FROM rruff_minerals
                    WHERE id = :id
                """)
                
                result = conn.execute(query, {"id": mineral_id})
                row = result.mappings().first()
                
                if row:
                    mineral = dict(row)
                    # Get chemistry data
                    mineral['chemistry'] = self._get_rruff_chemistry(mineral['rruff_id'])
                    return mineral

            return None

        except Exception as e:
            logger.error(f"Error loading RRUFF mineral {mineral_id}: {e}")
            return None
    
    def _get_rruff_chemistry(self, rruff_id: str) -> List[Dict]:
        """Get chemical composition for a RRUFF mineral."""
        try:
            with self.engine.connect() as conn:
                query = text("""
                    SELECT oxide, weight_percent
                    FROM rruff_chemistry
                    WHERE rruff_id = :rruff_id
                    ORDER BY weight_percent DESC
                """)
                
                result = conn.execute(query, {"rruff_id": rruff_id})
                return [dict(row._mapping) for row in result]

        except Exception as e:
            logger.error(f"Error loading chemistry for {rruff_id}: {e}")
            return []
    
    def get_rruff_data_for_mineral(self, mineral_name: str) -> Optional[Dict]:
        """Get RRUFF scientific data for a mineral by name matching."""
        if not mineral_name:
            return None
        
        try:
            with self.engine.connect() as conn:
                # Try exact match first (case insensitive)
                query = text("""
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
                    WHERE LOWER(name) = LOWER(:name) OR LOWER(name_plain) = LOWER(:name)
                    LIMIT 1
                """)
                
                result = conn.execute(query, {"name": mineral_name})
                row = result.mappings().first()
                
                if row:
                    rruff_data = dict(row)
                    # Get chemistry composition
                    rruff_data['chemistry'] = self._get_rruff_chemistry(rruff_data['rruff_id'])
                    return rruff_data
                
                return None
        
        except Exception as e:
            logger.error(f"Error getting RRUFF data for {mineral_name}: {e}")
            return None


# Singleton instance
_mineral_db = None


def get_mineral_database() -> MineralDatabase:
    """Get singleton mineral database instance."""
    global _mineral_db
    if _mineral_db is None:
        _mineral_db = MineralDatabase()
    return _mineral_db
