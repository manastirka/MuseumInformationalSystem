#!/usr/bin/env python3
"""
Bird Ringing Database Module.

This module is PostgreSQL-only. The legacy SQLite fallback has been removed.
"""

import datetime as dt
import json
import logging
from typing import Dict, List, Optional, Tuple

from psycopg.rows import dict_row

from postgres_service import get_database_url, get_postgres_connection


logger = logging.getLogger(__name__)

PG_UPDATEABLE_FIELDS = {
    'ring_number',
    'color_ring',
    'age',
    'sex',
    'location',
    'coordinate_accuracy',
    'metal_ring_position',
    'plastic_ring',
    'catching_method',
    'bait',
    'manipulation',
    'status',
    'clutch_size',
    'pullus_age',
    'wing_length',
    'third_primary_feather',
    'mass',
    'molting',
    'back_claw',
    'bill_length',
    'bill_measurement_method',
    'head_length',
    'tarsus',
    'tarsus_measurement_method',
    'tail_length',
    'fat_deposits',
    'pectoral_muscle',
    'incubation_patch',
    'alula',
    'carpal_feathers',
    'sex_determination',
    'protected_areas',
    'ringer',
    'notes',
    'raw_json',
}

_PG_BASE_QUERY = """
    SELECT
        br.id,
        br.ring_number,
        NULL AS color_ring,
        br.age,
        br.sex,
        br.location,
        br.coordinate_accuracy,
        br.event_date,
        br.event_time,
        br.metal_ring_position,
        br.plastic_ring,
        br.catching_method,
        br.bait,
        br.manipulation,
        br.status,
        br.clutch_size,
        br.pullus_age,
        br.wing_length,
        br.third_primary_feather,
        br.mass,
        br.molting,
        br.back_claw,
        br.bill_length,
        br.bill_measurement_method,
        br.head_length,
        br.tarsus,
        br.tarsus_measurement_method,
        br.tail_length,
        br.fat_deposits,
        br.pectoral_muscle,
        br.incubation_patch,
        br.alula,
        br.carpal_feathers,
        br.sex_determination,
        br.protected_areas,
        br.ringer,
        br.notes,
        br.raw_json,
        br.created_at,
        ST_Y(br.coordinates::geometry) AS latitude,
        ST_X(br.coordinates::geometry) AS longitude,
        bs.species_name AS species
    FROM bird_ringing_records br
    LEFT JOIN bird_species bs ON bs.id = br.species_id
"""


def _postgres_available() -> bool:
    try:
        get_database_url()
        return True
    except Exception:
        return False


def _require_postgres():
    if not _postgres_available():
        raise RuntimeError('Bird ringing module requires PostgreSQL and DATABASE_URL is not configured.')


def _pg_connect():
    _require_postgres()
    return get_postgres_connection(row_factory=dict_row)


def get_connection():
    """Backward-compatible DB-API connection accessor."""
    return _pg_connect()


def get_all_records(page=1, per_page=50, search=None, species_filter=None,
                    location_filter=None, ringer_filter=None, year_filter=None):
    """
    Get bird ringing records with pagination and filters.

    Returns:
        Tuple[list, int, int]: (records, total_count, total_pages)
    """
    return _pg_get_all_records(
        page, per_page, search, species_filter, location_filter, ringer_filter, year_filter
    )


def _pg_get_all_records(page=1, per_page=50, search=None, species_filter=None,
                        location_filter=None, ringer_filter=None, year_filter=None):
    where_sql, filter_params = _build_pg_filters(
        search, species_filter, location_filter, ringer_filter, year_filter
    )
    offset = (page - 1) * per_page
    query = f"""{_PG_BASE_QUERY}
        WHERE {where_sql}
        ORDER BY br.event_date DESC NULLS LAST, br.id DESC
        LIMIT %s OFFSET %s
    """
    count_query = f"""
        SELECT COUNT(*) AS total
        FROM bird_ringing_records br
        LEFT JOIN bird_species bs ON bs.id = br.species_id
        WHERE {where_sql}
    """
    with _pg_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, filter_params + [per_page, offset])
            records = [_normalize_pg_row(row) for row in cur.fetchall()]
            cur.execute(count_query, filter_params)
            total_count = cur.fetchone()['total']

    total_pages = (total_count + per_page - 1) // per_page if per_page else 0
    return records, total_count, total_pages


def get_record_by_id(record_id: int) -> Optional[Dict]:
    """Get a single bird ringing record by ID."""
    return _pg_get_record_by_id(record_id)


def _pg_get_record_by_id(record_id: int) -> Optional[Dict]:
    query = f"""{_PG_BASE_QUERY}
        WHERE br.id = %s
        LIMIT 1
    """
    with _pg_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (record_id,))
            row = cur.fetchone()
            return _normalize_pg_row(row) if row else None


def get_statistics() -> Dict:
    """Get database statistics."""
    return _pg_get_statistics()


def _pg_get_statistics() -> Dict:
    stats: Dict[str, object] = {}
    with _pg_connect() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) AS total FROM bird_ringing_records')
            stats['total_records'] = cur.fetchone()['total']

            cur.execute("""
                SELECT COUNT(DISTINCT bs.species_name) AS total
                FROM bird_ringing_records br
                LEFT JOIN bird_species bs ON bs.id = br.species_id
                WHERE bs.species_name IS NOT NULL
            """)
            stats['unique_species'] = cur.fetchone()['total']

            cur.execute("""
                SELECT COUNT(DISTINCT location) AS total
                FROM bird_ringing_records
                WHERE location IS NOT NULL AND location <> ''
            """)
            stats['unique_locations'] = cur.fetchone()['total']

            cur.execute("""
                SELECT COUNT(DISTINCT ringer) AS total
                FROM bird_ringing_records
                WHERE ringer IS NOT NULL AND ringer <> ''
            """)
            stats['unique_ringers'] = cur.fetchone()['total']

            cur.execute("""
                SELECT COALESCE(bs.species_name, 'Непозната врста') AS species, COUNT(*) AS cnt
                FROM bird_ringing_records br
                LEFT JOIN bird_species bs ON bs.id = br.species_id
                WHERE bs.species_name IS NOT NULL
                GROUP BY species
                ORDER BY cnt DESC
                LIMIT 10
            """)
            stats['top_species'] = [{'species': row['species'], 'count': row['cnt']} for row in cur.fetchall()]

            cur.execute("""
                SELECT location, COUNT(*) AS cnt
                FROM bird_ringing_records
                WHERE location IS NOT NULL AND location <> ''
                GROUP BY location
                ORDER BY cnt DESC
                LIMIT 10
            """)
            stats['top_locations'] = [{'location': row['location'], 'count': row['cnt']} for row in cur.fetchall()]

            cur.execute("""
                SELECT ringer, COUNT(*) AS cnt
                FROM bird_ringing_records
                WHERE ringer IS NOT NULL AND ringer <> ''
                GROUP BY ringer
                ORDER BY cnt DESC
                LIMIT 10
            """)
            stats['top_ringers'] = [{'ringer': row['ringer'], 'count': row['cnt']} for row in cur.fetchall()]

            cur.execute("""
                SELECT EXTRACT(YEAR FROM event_date)::INTEGER AS year, COUNT(*) AS cnt
                FROM bird_ringing_records
                WHERE event_date IS NOT NULL
                GROUP BY year
                ORDER BY year DESC
                LIMIT 20
            """)
            stats['records_by_year'] = [{'year': row['year'], 'count': row['cnt']} for row in cur.fetchall()]

    return stats


def get_all_species() -> List[str]:
    """Get list of all unique species."""
    return _pg_get_all_species()


def _pg_get_all_species() -> List[str]:
    query = """
        SELECT DISTINCT bs.species_name AS species
        FROM bird_ringing_records br
        LEFT JOIN bird_species bs ON bs.id = br.species_id
        WHERE bs.species_name IS NOT NULL
        ORDER BY species
    """
    with _pg_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return [row['species'] for row in cur.fetchall()]


def get_all_locations() -> List[str]:
    return _pg_get_all_locations()


def _pg_get_all_locations() -> List[str]:
    with _pg_connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT location
                FROM bird_ringing_records
                WHERE location IS NOT NULL AND location <> ''
                ORDER BY location
            """)
            return [row['location'] for row in cur.fetchall()]


def get_all_ringers() -> List[str]:
    return _pg_get_all_ringers()


def _pg_get_all_ringers() -> List[str]:
    with _pg_connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT ringer
                FROM bird_ringing_records
                WHERE ringer IS NOT NULL AND ringer <> ''
                ORDER BY ringer
            """)
            return [row['ringer'] for row in cur.fetchall()]


def get_all_years() -> List[int]:
    return _pg_get_all_years()


def _pg_get_all_years() -> List[int]:
    with _pg_connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT EXTRACT(YEAR FROM event_date)::INTEGER AS year
                FROM bird_ringing_records
                WHERE event_date IS NOT NULL
                ORDER BY year DESC
            """)
            return [row['year'] for row in cur.fetchall()]


def get_map_localities(species_filter: Optional[str] = None,
                       year_filter: Optional[int] = None,
                       location_filter: Optional[str] = None) -> List[Dict]:
    """
    Get aggregated bird ringing localities for the biodiversity map.

    Returns list of dicts with:
        location, latitude, longitude, record_count, species_count,
        top_species, first_year, last_year
    """
    return _pg_get_map_localities(species_filter, year_filter, location_filter)


def _pg_get_map_localities(species_filter, year_filter, location_filter):
    where_clauses = ['br.coordinates IS NOT NULL']
    params = []

    if species_filter:
        where_clauses.append('bs.species_name = %s')
        params.append(species_filter)
    if year_filter:
        where_clauses.append('EXTRACT(YEAR FROM br.event_date) = %s')
        params.append(year_filter)
    if location_filter:
        where_clauses.append('br.location = %s')
        params.append(location_filter)

    where_sql = ' AND '.join(where_clauses)

    query = f"""
        SELECT
            br.location,
            ROUND(ST_Y(br.coordinates::geometry)::numeric, 4) AS latitude,
            ROUND(ST_X(br.coordinates::geometry)::numeric, 4) AS longitude,
            COUNT(*) AS record_count,
            COUNT(DISTINCT bs.species_name) AS species_count,
            MIN(EXTRACT(YEAR FROM br.event_date))::INTEGER AS first_year,
            MAX(EXTRACT(YEAR FROM br.event_date))::INTEGER AS last_year
        FROM bird_ringing_records br
        LEFT JOIN bird_species bs ON bs.id = br.species_id
        WHERE {where_sql}
        GROUP BY br.location,
                 ROUND(ST_Y(br.coordinates::geometry)::numeric, 4),
                 ROUND(ST_X(br.coordinates::geometry)::numeric, 4)
        ORDER BY record_count DESC
    """

    top_species_query = f"""
        SELECT
            br.location,
            ROUND(ST_Y(br.coordinates::geometry)::numeric, 4) AS latitude,
            ROUND(ST_X(br.coordinates::geometry)::numeric, 4) AS longitude,
            bs.species_name AS species,
            COUNT(*) AS cnt
        FROM bird_ringing_records br
        LEFT JOIN bird_species bs ON bs.id = br.species_id
        WHERE {where_sql} AND bs.species_name IS NOT NULL
        GROUP BY br.location,
                 ROUND(ST_Y(br.coordinates::geometry)::numeric, 4),
                 ROUND(ST_X(br.coordinates::geometry)::numeric, 4),
                 bs.species_name
        ORDER BY br.location, cnt DESC
    """

    with _pg_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

            cur.execute(top_species_query, params)
            species_rows = cur.fetchall()

    species_by_loc = {}
    for species_row in species_rows:
        key = (
            species_row['location'],
            float(species_row['latitude']),
            float(species_row['longitude']),
        )
        species_by_loc.setdefault(key, [])
        if len(species_by_loc[key]) < 5:
            species_by_loc[key].append({
                'species': species_row['species'],
                'count': species_row['cnt'],
            })

    results = []
    for row in rows:
        lat = float(row['latitude'])
        lon = float(row['longitude'])
        key = (row['location'], lat, lon)
        results.append({
            'location': row['location'] or 'Непознато',
            'latitude': lat,
            'longitude': lon,
            'record_count': row['record_count'],
            'species_count': row['species_count'],
            'top_species': species_by_loc.get(key, []),
            'first_year': row['first_year'],
            'last_year': row['last_year'],
        })

    return results


def get_map_localities_no_coords(species_filter: Optional[str] = None,
                                 year_filter: Optional[int] = None,
                                 location_filter: Optional[str] = None) -> List[Dict]:
    """
    Get aggregated bird ringing localities for records that have a location name
    but no GPS coordinates.
    """
    return _pg_get_map_localities_no_coords(species_filter, year_filter, location_filter)


def _pg_get_map_localities_no_coords(species_filter, year_filter, location_filter):
    where_clauses = ['br.coordinates IS NULL', "br.location IS NOT NULL AND br.location <> ''"]
    params = []

    if species_filter:
        where_clauses.append('bs.species_name = %s')
        params.append(species_filter)
    if year_filter:
        where_clauses.append('EXTRACT(YEAR FROM br.event_date) = %s')
        params.append(year_filter)
    if location_filter:
        where_clauses.append('br.location = %s')
        params.append(location_filter)

    where_sql = ' AND '.join(where_clauses)

    query = f"""
        SELECT
            br.location,
            COUNT(*) AS record_count,
            COUNT(DISTINCT bs.species_name) AS species_count,
            MIN(EXTRACT(YEAR FROM br.event_date))::INTEGER AS first_year,
            MAX(EXTRACT(YEAR FROM br.event_date))::INTEGER AS last_year
        FROM bird_ringing_records br
        LEFT JOIN bird_species bs ON bs.id = br.species_id
        WHERE {where_sql}
        GROUP BY br.location
        ORDER BY record_count DESC
    """

    top_species_query = f"""
        SELECT
            br.location,
            bs.species_name AS species,
            COUNT(*) AS cnt
        FROM bird_ringing_records br
        LEFT JOIN bird_species bs ON bs.id = br.species_id
        WHERE {where_sql} AND bs.species_name IS NOT NULL
        GROUP BY br.location, bs.species_name
        ORDER BY br.location, cnt DESC
    """

    with _pg_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

            cur.execute(top_species_query, params)
            species_rows = cur.fetchall()

    species_by_loc = {}
    for species_row in species_rows:
        species_by_loc.setdefault(species_row['location'], [])
        if len(species_by_loc[species_row['location']]) < 5:
            species_by_loc[species_row['location']].append({
                'species': species_row['species'],
                'count': species_row['cnt'],
            })

    return [{
        'location': row['location'] or 'Непознато',
        'record_count': row['record_count'],
        'species_count': row['species_count'],
        'top_species': species_by_loc.get(row['location'], []),
        'first_year': row['first_year'],
        'last_year': row['last_year'],
    } for row in rows]


def search_records(query: str, limit: int = 100) -> List[Dict]:
    """Search bird ringing records."""
    if not query:
        return []
    return _pg_search_records(query, limit)


def _pg_search_records(query: str, limit: int) -> List[Dict]:
    where_sql, params = _build_pg_filters(query, None, None, None, None)
    search_query = f"""{_PG_BASE_QUERY}
        WHERE {where_sql}
        ORDER BY br.event_date DESC NULLS LAST, br.id DESC
        LIMIT %s
    """
    with _pg_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(search_query, params + [limit])
            return [_normalize_pg_row(row) for row in cur.fetchall()]


def insert_record(record_data: Dict) -> int:
    """Insert a new bird ringing record."""
    return _pg_insert_record(record_data)


def _pg_insert_record(record_data: Dict) -> int:
    payload = {key: _clean_value(value) for key, value in record_data.items()}
    payload['metal_ring_position'] = _safe_int(record_data.get('metal_ring_position'))
    payload['coordinates'] = _coordinates_to_wkt(record_data.get('coordinates'))
    payload['date'] = record_data.get('date') or None
    payload['time'] = record_data.get('time') or None
    payload['raw_json'] = json.dumps(record_data)

    with _pg_connect() as conn:
        with conn.cursor() as cur:
            species_name = _clean_value(record_data.get('species'))
            if species_name:
                cur.execute("""
                    INSERT INTO bird_species (species_name)
                    VALUES (%s)
                    ON CONFLICT (species_name)
                    DO UPDATE SET species_name = EXCLUDED.species_name
                    RETURNING id
                """, (species_name,))
                payload['species_id'] = cur.fetchone()['id']
            else:
                payload['species_id'] = None

            cur.execute("""
                INSERT INTO bird_ringing_records (
                    ring_number, color_ring, species_id, age, sex, location,
                    coordinates, coordinate_accuracy, event_date, event_time,
                    metal_ring_position, plastic_ring, catching_method, bait,
                    manipulation, status, clutch_size, pullus_age, wing_length,
                    third_primary_feather, mass, molting, back_claw, bill_length,
                    bill_measurement_method, head_length, tarsus, tarsus_measurement_method,
                    tail_length, fat_deposits, pectoral_muscle, incubation_patch,
                    alula, carpal_feathers, sex_determination, protected_areas,
                    ringer, notes, raw_json
                )
                VALUES (
                    %(ring_number)s, %(color_ring)s, %(species_id)s, %(age)s, %(sex)s, %(location)s,
                    ST_GeogFromText(%(coordinates)s), %(coordinate_accuracy)s, %(date)s, %(time)s,
                    %(metal_ring_position)s, %(plastic_ring)s, %(catching_method)s, %(bait)s,
                    %(manipulation)s, %(status)s, %(clutch_size)s, %(pullus_age)s, %(wing_length)s,
                    %(third_primary_feather)s, %(mass)s, %(molting)s, %(back_claw)s, %(bill_length)s,
                    %(bill_measurement_method)s, %(head_length)s, %(tarsus)s, %(tarsus_measurement_method)s,
                    %(tail_length)s, %(fat_deposits)s, %(pectoral_muscle)s, %(incubation_patch)s,
                    %(alula)s, %(carpal_feathers)s, %(sex_determination)s, %(protected_areas)s,
                    %(ringer)s, %(notes)s, %(raw_json)s
                )
                RETURNING id
            """, payload)
            new_id = cur.fetchone()['id']
        conn.commit()

    return new_id


def update_record(record_id: int, record_data: Dict) -> bool:
    """Update an existing bird ringing record."""
    return _pg_update_record(record_id, record_data)


def _pg_update_record(record_id: int, record_data: Dict) -> bool:
    if not record_data:
        return False

    set_clauses = []
    params: Dict[str, object] = {}

    coordinates_value = record_data.get('coordinates')
    if coordinates_value is not None:
        set_clauses.append('coordinates = ST_GeogFromText(%(coordinates)s)')
        params['coordinates'] = _coordinates_to_wkt(coordinates_value)

    if 'date' in record_data:
        set_clauses.append('event_date = %(event_date)s')
        params['event_date'] = record_data.get('date') or None

    if 'time' in record_data:
        set_clauses.append('event_time = %(event_time)s')
        params['event_time'] = record_data.get('time') or None

    species_value = record_data.get('species')

    with _pg_connect() as conn:
        with conn.cursor() as cur:
            if species_value is not None:
                cleaned_species = _clean_value(species_value)
                if cleaned_species:
                    cur.execute("""
                        INSERT INTO bird_species (species_name)
                        VALUES (%s)
                        ON CONFLICT (species_name)
                        DO UPDATE SET species_name = EXCLUDED.species_name
                        RETURNING id
                    """, (cleaned_species,))
                    params['species_id'] = cur.fetchone()['id']
                else:
                    params['species_id'] = None
                set_clauses.append('species_id = %(species_id)s')

            for field, value in record_data.items():
                if field in {'coordinates', 'date', 'time', 'species', 'id', 'created_at'}:
                    continue
                if field not in PG_UPDATEABLE_FIELDS:
                    continue
                params[field] = _safe_int(value) if field == 'metal_ring_position' else _clean_value(value)
                set_clauses.append(f'{field} = %({field})s')

            if not set_clauses:
                return False

            if 'raw_json' not in params:
                params['raw_json'] = json.dumps(record_data)
                set_clauses.append('raw_json = %(raw_json)s')

            params['record_id'] = record_id
            cur.execute(
                "UPDATE bird_ringing_records SET "
                + ', '.join(set_clauses)
                + " WHERE id = %(record_id)s",
                params,
            )
            updated = cur.rowcount > 0
        conn.commit()

    return updated


def delete_record(record_id: int) -> bool:
    """Delete a bird ringing record."""
    return _pg_delete_record(record_id)


def _pg_delete_record(record_id: int) -> bool:
    with _pg_connect() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM bird_ringing_records WHERE id = %s', (record_id,))
            deleted = cur.rowcount > 0
        conn.commit()

    return deleted


def _build_pg_filters(search=None, species_filter=None, location_filter=None,
                      ringer_filter=None, year_filter=None) -> Tuple[str, List]:
    clauses = []
    params: List = []

    if search:
        like = f'%{search}%'
        clauses.append("""
            (COALESCE(bs.species_name, '') ILIKE %s
             OR COALESCE(br.location, '') ILIKE %s
             OR COALESCE(br.ringer, '') ILIKE %s)
        """)
        params.extend([like, like, like])

    if species_filter:
        clauses.append('bs.species_name = %s')
        params.append(species_filter)

    if location_filter:
        clauses.append('br.location = %s')
        params.append(location_filter)

    if ringer_filter:
        clauses.append('br.ringer = %s')
        params.append(ringer_filter)

    if year_filter:
        try:
            params.append(int(year_filter))
            clauses.append('EXTRACT(YEAR FROM br.event_date) = %s')
        except (TypeError, ValueError):
            pass

    return ' AND '.join(clauses) if clauses else 'TRUE', params


def _normalize_pg_row(row: Optional[Dict]) -> Optional[Dict]:
    if row is None:
        return None

    normalized = dict(row)
    latitude = normalized.pop('latitude', None)
    longitude = normalized.pop('longitude', None)
    normalized['coordinates'] = _format_coordinate_value(latitude, longitude)
    normalized['date'] = _format_date_value(normalized.pop('event_date', None))
    normalized['time'] = _format_time_value(normalized.pop('event_time', None))

    created_at = normalized.get('created_at')
    if isinstance(created_at, dt.datetime):
        normalized['created_at'] = created_at.isoformat()

    return normalized


def _format_coordinate_value(lat: Optional[float], lon: Optional[float]) -> Optional[str]:
    if lat is None or lon is None:
        return None
    return f'{lat:.6f}, {lon:.6f}'


def _format_date_value(value):
    if value is None:
        return None
    if isinstance(value, dt.date):
        return value.isoformat()
    return str(value)


def _format_time_value(value):
    if value is None:
        return None
    if isinstance(value, dt.time):
        return value.strftime('%H:%M')
    return str(value)


def _clean_value(value):
    if value is None:
        return None
    if isinstance(value, str):
        cleaned = value.strip()
        return cleaned or None
    return value


def _coordinates_to_wkt(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    try:
        lat_str, lon_str = [part.strip() for part in value.split(',', 1)]
        lat = float(lat_str)
        lon = float(lon_str)
        return f'SRID=4326;POINT({lon} {lat})'
    except Exception:
        return None


def _safe_int(value) -> Optional[int]:
    if value in (None, ''):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
