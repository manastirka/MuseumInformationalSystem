#!/usr/bin/env python3
"""
Phase 3A Database Accessors for PostgreSQL
Provides functions to access Library, Exhibitions, Heritage, Meteorites, Employees
"""

import os
import logging
import psycopg
from dotenv import load_dotenv
from typing import List, Dict, Optional, Any

# Load environment variables
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Convert SQLAlchemy-style URL to psycopg format
DB_URL = DATABASE_URL.replace('postgresql+psycopg://', 'postgresql://')

logger = logging.getLogger(__name__)

# ============================================================================
# DATABASE CONNECTION
# ============================================================================

def get_db_connection():
    """Get a database connection."""
    try:
        return psycopg.connect(DB_URL)
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        raise

# ============================================================================
# 1. LIBRARY DATABASE
# ============================================================================

def get_library_database():
    """
    Load library database from PostgreSQL.
    Returns structure compatible with existing code.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Get all books
        cur.execute("""
            SELECT
                id, title, author, isbn, publisher, publication_year,
                category, subcategory, language, pages, format,
                location, shelf_number, status, acquisition_date,
                acquisition_method, price, condition, description, notes,
                keywords, created_at, updated_at
            FROM library_books
            ORDER BY title
        """)

        columns = [desc[0] for desc in cur.description]
        books = []

        for row in cur.fetchall():
            book = dict(zip(columns, row))
            # Convert date to string if needed
            if book.get('acquisition_date'):
                book['acquisition_date'] = str(book['acquisition_date'])
            if book.get('created_at'):
                book['created_at'] = str(book['created_at'])
            if book.get('updated_at'):
                book['updated_at'] = str(book['updated_at'])
            # Convert keywords array to list
            if book.get('keywords') is None:
                book['keywords'] = []
            books.append(book)

        # Get categories
        cur.execute("SELECT DISTINCT category FROM library_books WHERE category IS NOT NULL ORDER BY category")
        categories = [row[0] for row in cur.fetchall()]

        # Calculate statistics
        cur.execute("""
            SELECT
                COUNT(*) as total_books,
                COUNT(*) FILTER (WHERE status = 'доступна') as available_books,
                COUNT(*) FILTER (WHERE status = 'позајмљена') as borrowed_books
            FROM library_books
        """)
        stats = cur.fetchone()

        statistics = {
            'total_books': stats[0] if stats else 0,
            'available_books': stats[1] if stats else 0,
            'borrowed_books': stats[2] if stats else 0,
            'total_categories': len(categories)
        }

        cur.close()
        conn.close()

        logger.info(f"Loaded library database from PostgreSQL: {statistics['total_books']} books")

        return {
            'books': books,
            'categories': categories,
            'statistics': statistics
        }

    except Exception as e:
        logger.error(f"Error loading library database from PostgreSQL: {e}")
        # Return empty structure
        return {
            'books': [],
            'categories': [],
            'statistics': {
                'total_books': 0,
                'available_books': 0,
                'borrowed_books': 0,
                'total_categories': 0
            }
        }

def save_library_book(book_data: Dict[str, Any]) -> Optional[int]:
    """
    Save a library book to PostgreSQL.
    Returns the book ID if successful, None otherwise.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO library_books (
                title, author, isbn, publisher, publication_year,
                category, subcategory, language, pages, format,
                location, shelf_number, status, acquisition_date,
                acquisition_method, price, condition, description, notes, keywords
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            RETURNING id
        """, (
            book_data.get('title'),
            book_data.get('author'),
            book_data.get('isbn'),
            book_data.get('publisher'),
            book_data.get('publication_year') or book_data.get('year'),
            book_data.get('category'),
            book_data.get('subcategory'),
            book_data.get('language', 'српски'),
            book_data.get('pages'),
            book_data.get('format'),
            book_data.get('location'),
            book_data.get('shelf_number'),
            book_data.get('status', 'доступна'),
            book_data.get('acquisition_date'),
            book_data.get('acquisition_method'),
            book_data.get('price'),
            book_data.get('condition'),
            book_data.get('description'),
            book_data.get('notes'),
            book_data.get('keywords')
        ))

        book_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        logger.info(f"Saved library book: {book_data.get('title')} (ID: {book_id})")
        return book_id

    except Exception as e:
        logger.error(f"Error saving library book: {e}")
        return None

# ============================================================================
# 2. EXHIBITIONS DATABASE
# ============================================================================

def load_exhibitions_data():
    """
    Load exhibitions from PostgreSQL.
    Returns list of exhibitions compatible with existing code.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id, title, subtitle, description, exhibition_type,
                location, venue, start_date, end_date, opening_date,
                curator, co_curators, organizer, sponsors, status,
                visitor_count, catalog_published, catalog_path, poster_path,
                budget, notes, created_at, updated_at
            FROM exhibitions
            ORDER BY start_date DESC NULLS LAST, title
        """)

        columns = [desc[0] for desc in cur.description]
        exhibitions = []

        for row in cur.fetchall():
            exhibition = dict(zip(columns, row))
            # Convert dates to strings
            if exhibition.get('start_date'):
                exhibition['start_date'] = str(exhibition['start_date'])
            if exhibition.get('end_date'):
                exhibition['end_date'] = str(exhibition['end_date'])
            if exhibition.get('opening_date'):
                exhibition['opening_date'] = str(exhibition['opening_date'])
            if exhibition.get('created_at'):
                exhibition['created_at'] = str(exhibition['created_at'])
            if exhibition.get('updated_at'):
                exhibition['updated_at'] = str(exhibition['updated_at'])
            # Convert arrays to lists
            if exhibition.get('co_curators') is None:
                exhibition['co_curators'] = []
            if exhibition.get('sponsors') is None:
                exhibition['sponsors'] = []
            exhibitions.append(exhibition)

        cur.close()
        conn.close()

        logger.info(f"Loaded {len(exhibitions)} exhibitions from PostgreSQL")
        return exhibitions

    except Exception as e:
        logger.error(f"Error loading exhibitions from PostgreSQL: {e}")
        return []

# ============================================================================
# 3. CULTURAL HERITAGE DATABASE
# ============================================================================

def get_cultural_heritage_database():
    """
    Load cultural heritage database from PostgreSQL.
    Returns structure compatible with existing code.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Get all heritage items
        cur.execute("""
            SELECT
                id, registry_number, item_name, alternative_names, heritage_type,
                category, subcategory, significance_level, description, detailed_description,
                dimensions_height, dimensions_width, dimensions_depth, dimensions_diameter,
                dimensions_unit, weight, weight_unit, material, technique, color,
                date_of_origin, century, cultural_period, creator, creator_nationality,
                provenance, historical_context, current_location, storage_location,
                display_status, protection_status, protection_level, legal_basis,
                inscription_date, condition, condition_notes, conservation_history,
                conservation_needs, bibliography, related_items, keywords, notes,
                images, created_at, updated_at
            FROM heritage_items
            ORDER BY item_name
        """)

        columns = [desc[0] for desc in cur.description]
        heritage_items = []

        for row in cur.fetchall():
            item = dict(zip(columns, row))
            # Rename fields to match old structure
            item['name'] = item['item_name']
            item['type'] = item['heritage_type']
            item['significance'] = item['significance_level']
            item['location'] = item['current_location']

            # Convert dates to strings
            if item.get('inscription_date'):
                item['inscription_date'] = str(item['inscription_date'])
            if item.get('created_at'):
                item['created_at'] = str(item['created_at'])
            if item.get('updated_at'):
                item['updated_at'] = str(item['updated_at'])

            # Convert arrays to lists
            if item.get('alternative_names') is None:
                item['alternative_names'] = []
            if item.get('related_items') is None:
                item['related_items'] = []
            if item.get('keywords') is None:
                item['keywords'] = []

            heritage_items.append(item)

        # Get distinct values for dropdowns
        cur.execute("SELECT DISTINCT heritage_type FROM heritage_items WHERE heritage_type IS NOT NULL ORDER BY heritage_type")
        heritage_types = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT DISTINCT category FROM heritage_items WHERE category IS NOT NULL ORDER BY category")
        categories = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT DISTINCT subcategory FROM heritage_items WHERE subcategory IS NOT NULL ORDER BY subcategory")
        subcategories = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT DISTINCT significance_level FROM heritage_items WHERE significance_level IS NOT NULL ORDER BY significance_level")
        significance_levels = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT DISTINCT current_location FROM heritage_items WHERE current_location IS NOT NULL ORDER BY current_location")
        locations = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT DISTINCT condition FROM heritage_items WHERE condition IS NOT NULL ORDER BY condition")
        conditions = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT DISTINCT protection_status FROM heritage_items WHERE protection_status IS NOT NULL ORDER BY protection_status")
        protection_statuses = [row[0] for row in cur.fetchall()]

        # Calculate statistics
        cur.execute("""
            SELECT
                COUNT(*) as total,
                COUNT(*) FILTER (WHERE significance_level = 'Културно добро од изузетног значаја') as exceptional,
                COUNT(*) FILTER (WHERE significance_level = 'Културно добро од великог значаја') as great
            FROM heritage_items
        """)
        stats = cur.fetchone()

        statistics = {
            'total_heritage_items': stats[0] if stats else 0,
            'exceptional_significance': stats[1] if stats else 0,
            'great_significance': stats[2] if stats else 0
        }

        cur.close()
        conn.close()

        logger.info(f"Loaded {len(heritage_items)} heritage items from PostgreSQL")

        return {
            'heritage_items': heritage_items,
            'heritage_types': heritage_types,
            'categories': categories,
            'subcategories': subcategories,
            'significance_levels': significance_levels,
            'locations': locations,
            'conditions': conditions,
            'protection_statuses': protection_statuses,
            'statistics': statistics
        }

    except Exception as e:
        logger.error(f"Error loading cultural heritage from PostgreSQL: {e}")
        return {
            'heritage_items': [],
            'heritage_types': [],
            'categories': [],
            'subcategories': [],
            'significance_levels': [],
            'locations': [],
            'conditions': [],
            'protection_statuses': [],
            'statistics': {
                'total_heritage_items': 0,
                'exceptional_significance': 0,
                'great_significance': 0
            }
        }

# ============================================================================
# 4. METEORITE COLLECTION DATABASE
# ============================================================================

def get_meteorite_collection_database():
    """
    Load meteorite collection from PostgreSQL.
    Returns structure compatible with existing code.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Get all meteorite specimens (including all new Phase 3A fields)
        cur.execute("""
            SELECT
                id, catalog_number, specimen_name, alternative_names,
                meteorite_class, meteorite_group, meteorite_type, classification_scheme,
                mass, mass_unit, total_mass, total_mass_unit, quantity,
                dimensions, shape, color, surface_features,
                main_minerals, minor_minerals, chemical_composition,
                metal_content, silicate_content, mineralogy,
                fall_date, fall_date_text, fall_type, fall_location,
                fall_country, fall_coordinates, fall_witnessed, fall_description,
                discovery_date, discovery_location, discoverer, collection_date,
                collector, collection_method, acquisition_date, acquisition_date_text, acquisition_method,
                acquisition_source, acquisition_value,
                shock_stage, weathering_grade, texture, petrographic_notes,
                geochemical_data, isotopic_data,
                age_estimation, parent_body, cosmic_ray_exposure,
                widmanstatten_pattern, fusion_crust,
                meteorite_bulletin_number, serbian_meteorite,
                storage_location, storage_conditions,
                condition, condition_notes, description, scientific_significance,
                publications, bibliography_references, keywords, notes, images,
                status, display_status, created_at, updated_at
            FROM meteorite_specimens
            ORDER BY specimen_name
        """)

        columns = [desc[0] for desc in cur.description]
        specimens = []

        for row in cur.fetchall():
            specimen = dict(zip(columns, row))
            # Rename fields to match old structure
            specimen['meteorite_name'] = specimen['specimen_name']
            specimen['classification'] = specimen['meteorite_class']
            specimen['type'] = specimen['meteorite_type']
            specimen['location_found'] = specimen['fall_location']
            specimen['country'] = specimen['fall_country']
            specimen['curator'] = specimen['collector']
            specimen['source'] = specimen['acquisition_method']
            specimen['storage'] = specimen['storage_location']

            # Convert dates to strings
            if specimen.get('fall_date'):
                specimen['fall_date'] = str(specimen['fall_date'])
            if specimen.get('discovery_date'):
                specimen['discovery_date'] = str(specimen['discovery_date'])
            if specimen.get('collection_date'):
                specimen['collection_date'] = str(specimen['collection_date'])
            if specimen.get('acquisition_date'):
                specimen['acquisition_date'] = str(specimen['acquisition_date'])
            if specimen.get('created_at'):
                specimen['created_at'] = str(specimen['created_at'])
            if specimen.get('updated_at'):
                specimen['updated_at'] = str(specimen['updated_at'])

            # Convert arrays to lists
            if specimen.get('alternative_names') is None:
                specimen['alternative_names'] = []
            if specimen.get('main_minerals') is None:
                specimen['main_minerals'] = []
            if specimen.get('minor_minerals') is None:
                specimen['minor_minerals'] = []
            if specimen.get('publications') is None:
                specimen['publications'] = []
            if specimen.get('keywords') is None:
                specimen['keywords'] = []

            specimens.append(specimen)

        # Calculate statistics
        cur.execute("""
            SELECT
                COUNT(*) as total,
                COUNT(DISTINCT meteorite_class) as classes,
                SUM(CASE WHEN mass_unit = 'kg' THEN mass * 1000 ELSE mass END) as total_mass_grams,
                COUNT(*) FILTER (WHERE fall_witnessed = TRUE) as witnessed_falls,
                COUNT(*) FILTER (WHERE fall_witnessed = FALSE) as finds,
                COUNT(*) FILTER (WHERE serbian_meteorite = TRUE) as serbian,
                COUNT(*) FILTER (WHERE serbian_meteorite = FALSE OR serbian_meteorite IS NULL) as foreign
            FROM meteorite_specimens
        """)
        stats = cur.fetchone()

        statistics = {
            'total_specimens': stats[0] if stats else 0,
            'serbian_meteorites': stats[5] if stats else 0,
            'foreign_meteorites': stats[6] if stats else 0,
            'total_classes': stats[1] if stats else 0,
            'total_mass_grams': float(stats[2]) if stats and stats[2] else 0.0,
            'witnessed_falls': stats[3] if stats else 0,
            'finds': stats[4] if stats else 0
        }

        cur.close()
        conn.close()

        logger.info(f"Loaded {len(specimens)} meteorite specimens from PostgreSQL")

        return {
            'specimens': specimens,
            'statistics': statistics
        }

    except Exception as e:
        logger.error(f"Error loading meteorite collection from PostgreSQL: {e}")
        return {
            'specimens': [],
            'statistics': {
                'total_specimens': 0,
                'serbian_meteorites': 0,
                'foreign_meteorites': 0,
                'total_classes': 0,
                'total_mass_grams': 0.0,
                'witnessed_falls': 0,
                'finds': 0
            }
        }

# ============================================================================
# 5. EMPLOYEE DIRECTORY
# ============================================================================

def load_employee_directory():
    """
    Load employee directory from PostgreSQL.
    Returns list of employee profiles.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                ep.id, ep.user_id, ep.employee_id, ep.full_name, ep.name_cyrillic,
                ep.date_of_birth, ep.place_of_birth, ep.nationality, ep.email, ep.phone,
                ep.mobile, ep.emergency_contact, ep.emergency_phone, ep.position,
                ep.department, ep.division, ep.employment_type, ep.employment_status,
                ep.hire_date, ep.termination_date, ep.contract_type, ep.academic_title,
                ep.academic_degree, ep.education_level, ep.specialization, ep.university,
                ep.graduation_year, ep.expertise_areas, ep.research_interests,
                ep.languages_spoken, ep.certifications, ep.memberships,
                ep.publications_count, ep.research_projects, ep.awards, ep.biography,
                ep.biography_short, ep.professional_experience, ep.office_location,
                ep.office_phone, ep.office_hours, ep.photo_url, ep.cv_url, ep.notes,
                ep.metadata, ep.created_at, ep.updated_at,
                COALESCE(r.name, 'employee') as role
            FROM employee_profiles ep
            LEFT JOIN users u ON ep.user_id = u.id
            LEFT JOIN roles r ON u.role_id = r.id
            WHERE ep.employment_status = 'активан'
            ORDER BY ep.full_name
        """)

        columns = [desc[0] for desc in cur.description]
        employees = []

        for row in cur.fetchall():
            employee = dict(zip(columns, row))
            # Rename fields to match old structure
            employee['name'] = employee['full_name']
            employee['description'] = employee.get('biography', '')  # Map biography to description for compatibility

            # Convert dates to strings
            if employee.get('date_of_birth'):
                employee['date_of_birth'] = str(employee['date_of_birth'])
            if employee.get('hire_date'):
                employee['hire_date'] = str(employee['hire_date'])
            if employee.get('termination_date'):
                employee['termination_date'] = str(employee['termination_date'])
            if employee.get('created_at'):
                employee['created_at'] = str(employee['created_at'])
            if employee.get('updated_at'):
                employee['updated_at'] = str(employee['updated_at'])

            # Convert arrays to lists
            if employee.get('expertise_areas') is None:
                employee['expertise_areas'] = []
            if employee.get('research_interests') is None:
                employee['research_interests'] = []
            if employee.get('languages_spoken') is None:
                employee['languages_spoken'] = []
            if employee.get('certifications') is None:
                employee['certifications'] = []
            if employee.get('memberships') is None:
                employee['memberships'] = []
            if employee.get('research_projects') is None:
                employee['research_projects'] = []
            if employee.get('awards') is None:
                employee['awards'] = []

            employees.append(employee)

        cur.close()
        conn.close()

        logger.info(f"Loaded {len(employees)} employee profiles from PostgreSQL")
        return employees

    except Exception as e:
        logger.error(f"Error loading employee directory from PostgreSQL: {e}")
        return []

# ============================================================================
# 6. NEWS/EXHIBITIONS ARTICLES
# ============================================================================

def get_news_database():
    """
    Load news/exhibitions articles from PostgreSQL.
    Returns structure compatible with existing code.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Get all articles
        cur.execute("""
            SELECT
                id, original_id, title, title_en, type, status, category,
                start_date, end_date, location, curator, co_curator,
                specimens_count, species_count, boxes_count,
                illustrations_count, visitor_count,
                description, description_en, target_audience,
                educational_programs, guided_tours, catalog_available,
                keywords, source_link, created_at, updated_at
            FROM news_articles
            ORDER BY start_date DESC NULLS LAST
        """)

        columns = [desc[0] for desc in cur.description]
        articles = []

        for row in cur.fetchall():
            article = dict(zip(columns, row))
            # Use original_id as id for compatibility
            if article.get('original_id'):
                article['id'] = article['original_id']
            # Convert dates to strings
            if article.get('start_date'):
                article['start_date'] = str(article['start_date'])
            if article.get('end_date'):
                article['end_date'] = str(article['end_date'])
            if article.get('created_at'):
                article['created_at'] = str(article['created_at'])
            if article.get('updated_at'):
                article['updated_at'] = str(article['updated_at'])
            articles.append(article)

        cur.close()
        conn.close()

        logger.info(f"Loaded {len(articles)} news articles from PostgreSQL")
        return articles

    except Exception as e:
        logger.error(f"Failed to load news articles from PostgreSQL: {e}")
        return []


def load_news_data():
    """
    Load news/exhibitions articles from PostgreSQL.
    Wrapper function for compatibility with existing code.
    """
    return get_news_database()

# ============================================================================
# 7. BIOLOGICAL COLLECTIONS
# ============================================================================

def get_collection_by_type(collection_type: str):
    """
    Load specimens for a specific collection type from PostgreSQL.
    Returns structure compatible with existing code.

    Args:
        collection_type: One of 'botany', 'ichthyology', 'entomology', 'mycology',
                        'herpetology', 'ornithology', 'paleozoology', 'paleobotany', 'petrology'
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Get all specimens for this collection
        cur.execute("""
            SELECT
                id, catalog_number, collection_type, scientific_name, common_name_sr,
                family, order_name, class_name, location_found, locality_details,
                habitat, altitude, date_collected, collector, age, sex, condition,
                measurements, endemic_status, conservation_status, storage_location,
                herbarium_number, curator, description, notes, status,
                created_at, updated_at
            FROM collection_specimens
            WHERE collection_type = %s
            ORDER BY catalog_number
        """, (collection_type,))

        columns = [desc[0] for desc in cur.description]
        specimens = []

        for row in cur.fetchall():
            specimen = dict(zip(columns, row))

            # Convert dates to strings
            if specimen.get('date_collected'):
                specimen['date_collected'] = str(specimen['date_collected'])
            if specimen.get('created_at'):
                specimen['created_at'] = str(specimen['created_at'])
            if specimen.get('updated_at'):
                specimen['updated_at'] = str(specimen['updated_at'])

            specimens.append(specimen)

        # Get statistics from the view
        cur.execute("""
            SELECT
                total_specimens, endemic_species, threatened_species,
                on_display, families_count
            FROM collection_statistics
            WHERE code = %s
        """, (collection_type,))

        stats_row = cur.fetchone()
        if stats_row:
            statistics = {
                'total_specimens': stats_row[0],
                'endemic_species': stats_row[1],
                'threatened_species': stats_row[2],
                'on_display': stats_row[3],
                'families_count': stats_row[4]
            }
        else:
            statistics = {
                'total_specimens': len(specimens),
                'endemic_species': 0,
                'threatened_species': 0
            }

        cur.close()
        conn.close()

        logger.info(f"Loaded {len(specimens)} specimens from {collection_type} collection")

        return {
            'specimens': specimens,
            'statistics': statistics
        }

    except Exception as e:
        logger.error(f"Failed to load {collection_type} collection from PostgreSQL: {e}")
        return {
            'specimens': [],
            'statistics': {'total_specimens': 0, 'endemic_species': 0, 'threatened_species': 0}
        }


# Collection type accessors
def get_botany_collection():
    """Load botany collection from PostgreSQL."""
    return get_collection_by_type('botany')


def get_ichthyology_collection():
    """Load ichthyology collection from PostgreSQL."""
    return get_collection_by_type('ichthyology')


def get_entomology_collection():
    """Load entomology collection from PostgreSQL."""
    return get_collection_by_type('entomology')


def get_mycology_collection():
    """Load mycology collection from PostgreSQL."""
    return get_collection_by_type('mycology')


def get_herpetology_collection():
    """Load herpetology collection from PostgreSQL."""
    return get_collection_by_type('herpetology')


def get_ornithology_collection():
    """Load ornithology collection from PostgreSQL."""
    return get_collection_by_type('ornithology')


def get_paleozoology_collection():
    """Load paleozoology collection from PostgreSQL."""
    return get_collection_by_type('paleozoology')


def get_paleobotany_collection():
    """Load paleobotany collection from PostgreSQL."""
    return get_collection_by_type('paleobotany')


def get_petrology_collection():
    """Load petrology/geological collection from PostgreSQL."""
    return get_collection_by_type('petrology')


# ============================================================================
# 10. VEHICLE MANAGEMENT SYSTEM
# ============================================================================

def get_vehicles_list():
    """
    Load all vehicles from PostgreSQL.
    Returns list of vehicles compatible with existing code.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Get all vehicles
        cur.execute("""
            SELECT
                id, name, registration, type, capacity, status,
                year, make_model, notes, image_ids,
                created_at, updated_at
            FROM vehicles
            ORDER BY name
        """)

        vehicles = []
        for row in cur.fetchall():
            vehicle = {
                'id': row[0],
                'name': row[1],
                'registration': row[2],
                'type': row[3],
                'capacity': row[4],
                'status': row[5],
                'year': row[6],
                'make_model': row[7],
                'notes': row[8],
                'image_ids': row[9] if row[9] else []
            }
            vehicles.append(vehicle)

        cur.close()
        conn.close()

        logger.info(f"Loaded {len(vehicles)} vehicles from PostgreSQL")
        return vehicles

    except Exception as e:
        logger.error(f"Error loading vehicles from PostgreSQL: {e}")
        raise


def get_vehicle_by_id(vehicle_id: int) -> Optional[Dict[str, Any]]:
    """
    Load a specific vehicle by ID from PostgreSQL.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id, name, registration, type, capacity, status,
                year, make_model, notes, image_ids,
                created_at, updated_at
            FROM vehicles
            WHERE id = %s
        """, (vehicle_id,))

        row = cur.fetchone()
        if not row:
            cur.close()
            conn.close()
            return None

        vehicle = {
            'id': row[0],
            'name': row[1],
            'registration': row[2],
            'type': row[3],
            'capacity': row[4],
            'status': row[5],
            'year': row[6],
            'make_model': row[7],
            'notes': row[8],
            'image_ids': row[9] if row[9] else []
        }

        cur.close()
        conn.close()

        return vehicle

    except Exception as e:
        logger.error(f"Error loading vehicle {vehicle_id} from PostgreSQL: {e}")
        raise


def get_vehicle_reservations(vehicle_id: Optional[int] = None, status: Optional[str] = None):
    """
    Load vehicle reservations from PostgreSQL.
    If vehicle_id is provided, returns reservations for that vehicle only.
    If status is provided, filters by status.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Build query
        query = """
            SELECT
                id, vehicle_id, reserved_by, purpose,
                start_date, end_date, start_time, end_time,
                destination, estimated_km, driver_name, driver_license,
                passengers, notes, status, approved_by, approved_at,
                created_at, updated_at
            FROM vehicle_reservations
            WHERE 1=1
        """
        params = []

        if vehicle_id is not None:
            query += " AND vehicle_id = %s"
            params.append(vehicle_id)

        if status is not None:
            query += " AND status = %s"
            params.append(status)

        query += " ORDER BY start_date DESC, start_time DESC"

        cur.execute(query, params)

        reservations = []
        for row in cur.fetchall():
            reservation = {
                'id': row[0],
                'vehicle_id': row[1],
                'reserved_by': row[2],
                'purpose': row[3],
                'start_date': row[4].isoformat() if row[4] else None,
                'end_date': row[5].isoformat() if row[5] else None,
                'start_time': row[6].isoformat() if row[6] else None,
                'end_time': row[7].isoformat() if row[7] else None,
                'destination': row[8],
                'estimated_km': row[9],
                'driver_name': row[10],
                'driver_license': row[11],
                'passengers': row[12],
                'notes': row[13],
                'status': row[14],
                'approved_by': row[15],
                'approved_at': row[16].isoformat() if row[16] else None
            }
            reservations.append(reservation)

        cur.close()
        conn.close()

        logger.info(f"Loaded {len(reservations)} reservations from PostgreSQL")
        return reservations

    except Exception as e:
        logger.error(f"Error loading reservations from PostgreSQL: {e}")
        raise


def get_active_vehicle_reservations():
    """
    Load active vehicle reservations using the database view.
    Returns reservations with vehicle information.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id, vehicle_id, reserved_by, purpose,
                start_date, end_date, start_time, end_time,
                destination, estimated_km, driver_name, driver_license,
                passengers, notes, status, approved_by, approved_at,
                vehicle_name, vehicle_registration, vehicle_type
            FROM active_vehicle_reservations
            ORDER BY start_date, start_time
        """)

        reservations = []
        for row in cur.fetchall():
            reservation = {
                'id': row[0],
                'vehicle_id': row[1],
                'reserved_by': row[2],
                'purpose': row[3],
                'start_date': row[4].isoformat() if row[4] else None,
                'end_date': row[5].isoformat() if row[5] else None,
                'start_time': row[6].isoformat() if row[6] else None,
                'end_time': row[7].isoformat() if row[7] else None,
                'destination': row[8],
                'estimated_km': row[9],
                'driver_name': row[10],
                'driver_license': row[11],
                'passengers': row[12],
                'notes': row[13],
                'status': row[14],
                'approved_by': row[15],
                'approved_at': row[16].isoformat() if row[16] else None,
                'vehicle_name': row[17],
                'vehicle_registration': row[18],
                'vehicle_type': row[19]
            }
            reservations.append(reservation)

        cur.close()
        conn.close()

        return reservations

    except Exception as e:
        logger.error(f"Error loading active reservations from PostgreSQL: {e}")
        raise


def get_vehicle_availability():
    """
    Get vehicle availability status using the database view.
    Returns vehicles with their availability information.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id, name, registration, type, status,
                active_reservations, next_available_date
            FROM vehicle_availability
            ORDER BY name
        """)

        vehicles = []
        for row in cur.fetchall():
            vehicle = {
                'id': row[0],
                'name': row[1],
                'registration': row[2],
                'type': row[3],
                'status': row[4],
                'active_reservations': row[5],
                'next_available_date': row[6].isoformat() if row[6] else None
            }
            vehicles.append(vehicle)

        cur.close()
        conn.close()

        return vehicles

    except Exception as e:
        logger.error(f"Error loading vehicle availability from PostgreSQL: {e}")
        raise


def get_vehicle_usage_stats(vehicle_id: Optional[int] = None):
    """
    Get vehicle usage statistics using the database view.
    If vehicle_id is provided, returns stats for that vehicle only.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if vehicle_id:
            cur.execute("""
                SELECT
                    id, name, registration,
                    total_reservations, completed_reservations,
                    active_reservations, cancelled_reservations,
                    total_km, first_reservation, last_reservation
                FROM vehicle_usage_stats
                WHERE id = %s
            """, (vehicle_id,))
        else:
            cur.execute("""
                SELECT
                    id, name, registration,
                    total_reservations, completed_reservations,
                    active_reservations, cancelled_reservations,
                    total_km, first_reservation, last_reservation
                FROM vehicle_usage_stats
                ORDER BY total_reservations DESC
            """)

        stats = []
        for row in cur.fetchall():
            stat = {
                'id': row[0],
                'name': row[1],
                'registration': row[2],
                'total_reservations': row[3],
                'completed_reservations': row[4],
                'active_reservations': row[5],
                'cancelled_reservations': row[6],
                'total_km': row[7],
                'first_reservation': row[8].isoformat() if row[8] else None,
                'last_reservation': row[9].isoformat() if row[9] else None
            }
            stats.append(stat)

        cur.close()
        conn.close()

        if vehicle_id:
            return stats[0] if stats else None
        return stats

    except Exception as e:
        logger.error(f"Error loading vehicle usage stats from PostgreSQL: {e}")
        raise


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def test_connection():
    """Test database connection."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT version()")
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        logger.info(f"PostgreSQL connection successful: {version}")
        return True
    except Exception as e:
        logger.error(f"PostgreSQL connection failed: {e}")
        return False

# Test connection on import
if __name__ == '__main__':
    print("Testing PostgreSQL connection...")
    if test_connection():
        print("✓ Connection successful")
        print("\nTesting library database...")
        lib = get_library_database()
        print(f"✓ Loaded {lib['statistics']['total_books']} books")

        print("\nTesting exhibitions database...")
        exh = load_exhibitions_data()
        print(f"✓ Loaded {len(exh)} exhibitions")

        print("\nTesting cultural heritage database...")
        her = get_cultural_heritage_database()
        print(f"✓ Loaded {her['statistics']['total_heritage_items']} heritage items")

        print("\nTesting meteorite collection...")
        met = get_meteorite_collection_database()
        print(f"✓ Loaded {met['statistics']['total_specimens']} meteorite specimens")

        print("\nTesting employee directory...")
        emp = load_employee_directory()
        print(f"✓ Loaded {len(emp)} employees")
    else:
        print("✗ Connection failed")
