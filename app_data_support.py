"""Shared data-loading helpers used by the main Flask app bootstrap."""


def load_library_database_data(*, library_path, database_url, phase3a_databases, museum_staff_support):
    """Load library database from PostgreSQL or JSON fallback."""
    return museum_staff_support.load_library_database(
        library_path=library_path,
        database_url=database_url,
        phase3a_databases=phase3a_databases,
    )


def save_library_database_data(*, library_path, library_database, museum_staff_support):
    """Persist the library database to the JSON fallback file."""
    return museum_staff_support.save_library_database(
        library_path=library_path,
        library_database=library_database,
    )


def load_employee_directory_data(*, directory_path, database_url, phase3a_databases, museum_staff_support):
    """Load employee directory from PostgreSQL or JSON fallback."""
    return museum_staff_support.load_employee_directory(
        directory_path=directory_path,
        database_url=database_url,
        phase3a_databases=phase3a_databases,
    )


def load_exhibitions_data(*, database_url, phase3a_databases, museum_content_support):
    """Load exhibitions from PostgreSQL or JSON fallback."""
    return museum_content_support.load_exhibitions_data(
        database_url=database_url,
        phase3a_databases=phase3a_databases,
    )


def load_news_data(*, database_url, phase3a_databases, museum_content_support):
    """Load news articles from PostgreSQL or JSON fallback."""
    return museum_content_support.load_news_data(
        database_url=database_url,
        phase3a_databases=phase3a_databases,
    )


def build_exhibitions_database(*, load_exhibitions_data, museum_content_support):
    """Build the exhibition cache payload on demand."""
    return museum_content_support.build_exhibitions_database(
        load_exhibitions_data=load_exhibitions_data,
    )


def build_news_database(*, load_news_data, museum_content_support):
    """Build the news cache payload on demand."""
    return museum_content_support.build_news_database(
        load_news_data=load_news_data,
    )


def get_exhibit_statistics(*, exhibits_database, museum_content_support):
    """Aggregate exhibit metrics from the artifacts dataset."""
    return museum_content_support.get_exhibit_statistics(
        exhibits_database=exhibits_database,
    )


def get_exhibition_statistics(*, exhibitions_database, current_year, museum_content_support):
    """Aggregate exhibition metrics for dashboard and detail views."""
    return museum_content_support.get_exhibition_statistics(
        exhibitions_database=exhibitions_database,
        current_year=current_year,
    )


def load_vehicles_data(*, phase3a_databases, vehicle_data_support):
    """Load vehicles from PostgreSQL (single source of truth; raises on failure)."""
    return vehicle_data_support.load_vehicles(
        phase3a_databases=phase3a_databases,
    )


def load_reservations_data(*, phase3a_databases, vehicle_data_support):
    """Load reservations from PostgreSQL (single source of truth; raises on failure)."""
    return vehicle_data_support.load_reservations(
        phase3a_databases=phase3a_databases,
    )
