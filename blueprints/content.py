"""Content and overview routes extracted from app.py."""

from flask import Blueprint, redirect, request, url_for

import bird_ringing_views
import collection_management_views
import dashboard_integration_views
import exhibition_planner_views
import museum_content_views
import nhm_portal_views
from security_utils import admin_required, login_required, module_access_required


content_bp = Blueprint('content', __name__)


@content_bp.route('/admin/reports')
@admin_required
def system_reports():
    """Generate system reports and analytics. Standalone URL redirects to the unified
    hub tab; ?embedded=1 renders bare content for the iframe (bookmarks keep working)."""
    if not request.args.get('embedded'):
        return redirect(url_for('admin.admin_system_hub') + '#izvestaji')

    import app as museum_app

    return museum_content_views.render_system_reports(
        get_library_database=museum_app.get_library_database,
        get_employee_directory=museum_app.get_employee_directory,
        get_exhibit_statistics=museum_app.get_exhibit_statistics,
        user_has_module_access=museum_app.user_has_module_access,
    )


@content_bp.route('/admin/exhibits_database')
@admin_required
def exhibits_database():
    """Detailed inventory of museum artifacts and exhibits."""
    import app as museum_app

    return museum_content_views.render_exhibits_database(
        exhibits_database=museum_app.EXHIBITS_DATABASE,
        get_exhibit_statistics=museum_app.get_exhibit_statistics,
    )


@content_bp.route('/admin/exhibitions_database')
@module_access_required('exhibitions_database')
def exhibitions_database():
    """Timeline of gallery exhibitions with analytics."""
    import app as museum_app

    return museum_content_views.render_exhibitions_database(
        exhibitions_database=museum_app.EXHIBITIONS_DATABASE,
        get_exhibition_statistics=museum_app.get_exhibition_statistics,
    )


@content_bp.route('/admin/news')
@module_access_required('news')
def museum_news():
    """Museum news and announcements."""
    import app as museum_app

    return museum_content_views.render_museum_news(
        news_database=museum_app.NEWS_DATABASE,
    )


@content_bp.route('/api/news/save', methods=['POST'])
@admin_required
def api_save_news():
    """Save a news article to the database."""
    import app as museum_app

    return museum_content_views.api_save_news(
        news_database=museum_app.NEWS_DATABASE,
    )


@content_bp.route('/api/website-news')
@login_required
def api_website_news():
    """API endpoint to fetch news from museum website."""
    import app as museum_app

    return dashboard_integration_views.api_website_news(
        fetch_website_news=museum_app.fetch_website_news,
    )


@content_bp.route('/api/weather/details')
@login_required
def api_weather_details():
    """Return current weather, 7-day forecast, and RHMZ warning status."""
    import app as museum_app

    return dashboard_integration_views.api_weather_details(
        get_current_weather=museum_app.get_current_weather,
        get_weather_forecast=museum_app.get_weather_forecast,
        get_rhmz_weather_warnings=museum_app.get_rhmz_weather_warnings,
        rhmz_warning_url=museum_app._RHMZ_WARNING_URL,
    )


@content_bp.route('/admin/library_database')
@module_access_required('library_database')
def library_database():
    """Library database management system."""
    import app as museum_app

    return dashboard_integration_views.render_library_database(
        get_library_database=museum_app.get_library_database,
    )


@content_bp.route('/admin/nhm_data_portal')
@module_access_required('nhm_data_portal')
def nhm_data_portal():
    """Natural History Museum London Data Portal."""
    return nhm_portal_views.render_nhm_data_portal()


@content_bp.route('/api/nhm/search')
@login_required
def api_nhm_search():
    """API endpoint for NHM dataset search."""
    return nhm_portal_views.api_nhm_search()


@content_bp.route('/api/nhm/dataset/<dataset_id>')
@login_required
def api_nhm_dataset(dataset_id):
    """Get detailed metadata for a NHM dataset."""
    return nhm_portal_views.api_nhm_dataset(dataset_id)


@content_bp.route('/api/nhm/resource/<resource_id>')
@login_required
def api_nhm_resource(resource_id):
    """Get metadata for a NHM resource."""
    return nhm_portal_views.api_nhm_resource(resource_id)


@content_bp.route('/api/nhm/datastore/<resource_id>')
@login_required
def api_nhm_datastore(resource_id):
    """Search within a NHM datastore resource."""
    return nhm_portal_views.api_nhm_datastore(resource_id)


@content_bp.route('/api/nhm/statistics')
@login_required
def api_nhm_statistics():
    """Get NHM Data Portal statistics."""
    return nhm_portal_views.api_nhm_statistics()


@content_bp.route('/api/nhm/local/search')
@login_required
def api_nhm_local_search():
    """Search through locally downloaded NHM datasets."""
    return nhm_portal_views.api_nhm_local_search()


@content_bp.route('/api/nhm/local/dataset/<dataset_name>')
@login_required
def api_nhm_local_dataset(dataset_name):
    """Get locally stored dataset details."""
    return nhm_portal_views.api_nhm_local_dataset(dataset_name)


@content_bp.route('/api/nhm/local/statistics')
@login_required
def api_nhm_local_statistics():
    """Get statistics about locally downloaded NHM data."""
    return nhm_portal_views.api_nhm_local_statistics()


@content_bp.route('/api/nhm/local/tags')
@login_required
def api_nhm_local_tags():
    """Get all tags from locally downloaded datasets."""
    return nhm_portal_views.api_nhm_local_tags()


@content_bp.route('/api/nhm/local/formats')
@login_required
def api_nhm_local_formats():
    """Get all resource formats from locally downloaded datasets."""
    return nhm_portal_views.api_nhm_local_formats()


@content_bp.route('/api/nhm/local/authors')
@login_required
def api_nhm_local_authors():
    """Get all authors from locally downloaded datasets."""
    return nhm_portal_views.api_nhm_local_authors()


@content_bp.route('/api/nhm/download', methods=['POST'])
@admin_required
def api_nhm_download_datasets():
    """Download/update NHM datasets."""
    return nhm_portal_views.api_nhm_download_datasets()


@content_bp.route('/api/nhm/data/search/local')
@login_required
def api_nhm_data_search_local():
    """Search local museum databases."""
    return nhm_portal_views.api_nhm_data_search_local()


@content_bp.route('/api/nhm/data/search/nhm')
@login_required
def api_nhm_data_search_nhm():
    """Search NHM specimen data via API."""
    return nhm_portal_views.api_nhm_data_search_nhm()


@content_bp.route('/admin/cultural_heritage_database')
@module_access_required('cultural_heritage')
def cultural_heritage_database():
    """Cultural heritage database management system."""
    import app as museum_app

    return collection_management_views.render_cultural_heritage_database(
        get_cultural_heritage_database=museum_app.get_cultural_heritage_database,
        prepare_collection_records_for_display=museum_app.prepare_collection_records_for_display,
        get_qr_collection_action_url=museum_app.get_qr_collection_action_url,
    )


@content_bp.route('/admin/add_book', methods=['GET', 'POST'])
@admin_required
def add_book():
    """Add new book to library database."""
    import app as museum_app

    if museum_app.LIBRARY_DATABASE is None:
        museum_app.LIBRARY_DATABASE = museum_app.load_library_database()
    return museum_content_views.handle_add_book(
        library_database=museum_app.LIBRARY_DATABASE,
        save_library_database=museum_app.save_library_database,
        phase3a_databases=getattr(museum_app, 'phase3a_databases', None),
    )


@content_bp.route('/admin/add_heritage_item', methods=['GET', 'POST'])
@admin_required
def add_heritage_item():
    """Add new heritage item to cultural heritage database."""
    import app as museum_app

    return collection_management_views.handle_add_heritage_item(
        get_cultural_heritage_database=museum_app.get_cultural_heritage_database,
    )


@content_bp.route('/admin/add_visitor', methods=['GET', 'POST'])
@admin_required
def add_visitor():
    """Add new visitor record."""
    import app as museum_app

    return museum_content_views.handle_add_visitor(
        visitor_records=museum_app.VISITOR_RECORDS,
    )


@content_bp.route('/admin/add_research', methods=['GET', 'POST'])
@admin_required
def add_research():
    """Add new research project record."""
    import app as museum_app

    return museum_content_views.handle_add_research(
        research_projects=museum_app.RESEARCH_PROJECTS,
    )


@content_bp.route('/admin/visitors_database')
@admin_required
def visitors_database():
    """View visitors database."""
    import app as museum_app

    return museum_content_views.render_visitors_database(
        visitor_records=museum_app.VISITOR_RECORDS,
    )


@content_bp.route('/admin/export_visitors_to_pdf')
@admin_required
def export_visitors_to_pdf():
    """Export visitors statistics to PDF."""
    return museum_content_views.export_visitors_to_pdf(
        visitors_endpoint='visitors_database',
    )


@content_bp.route('/admin/research_database')
@admin_required
def research_database():
    """View research projects database."""
    import app as museum_app

    return museum_content_views.render_research_database(
        research_projects=museum_app.RESEARCH_PROJECTS,
    )


@content_bp.route('/admin/export_research_to_pdf/<int:project_id>')
@admin_required
def export_research_to_pdf(project_id):
    """Export one research project to PDF."""
    import app as museum_app

    return museum_content_views.export_research_to_pdf(
        research_projects=museum_app.RESEARCH_PROJECTS,
        project_id=project_id,
        list_endpoint='research_database',
    )


@content_bp.route('/admin/bird_ringing_database')
@module_access_required('bird_ringing_database')
def bird_ringing_database_view():
    """View bird ringing database with pagination and filters."""
    import app as museum_app

    return bird_ringing_views.render_bird_ringing_database(
        bird_ringing_database=museum_app.bird_ringing_database,
        museum_databases_endpoint='museum_databases',
    )


@content_bp.route('/admin/bird_ringing_record/<int:record_id>')
@module_access_required('bird_ringing_database')
def bird_ringing_record_detail(record_id):
    """View detailed information for a single bird ringing record."""
    import app as museum_app

    return bird_ringing_views.render_bird_ringing_record_detail(
        record_id=record_id,
        bird_ringing_database=museum_app.bird_ringing_database,
        list_endpoint='bird_ringing_database_view',
    )


@content_bp.route('/admin/add_bird_ringing', methods=['GET', 'POST'])
@admin_required
def add_bird_ringing():
    """Add a new bird ringing record."""
    import app as museum_app

    return bird_ringing_views.handle_add_bird_ringing(
        bird_ringing_database=museum_app.bird_ringing_database,
        detail_endpoint='bird_ringing_record_detail',
        list_endpoint='bird_ringing_database_view',
    )


@content_bp.route('/museum_terminology')
@login_required
def museum_terminology():
    """Display museum terminology page."""
    return exhibition_planner_views.render_museum_terminology()


@content_bp.route('/exhibition_planner')
@login_required
def exhibition_planner():
    """Display exhibition planning tool."""
    return exhibition_planner_views.render_exhibition_planner()


@content_bp.route('/api/exhibitions', methods=['GET'])
@login_required
def api_get_exhibitions():
    """Get exhibitions for the planner based on user role."""
    return exhibition_planner_views.api_get_exhibitions()


@content_bp.route('/api/exhibitions', methods=['POST'])
@login_required
def api_create_exhibition():
    """Create a new exhibition."""
    return exhibition_planner_views.api_create_exhibition()


@content_bp.route('/api/exhibitions/<int:exhibition_id>', methods=['PUT'])
@login_required
def api_update_exhibition(exhibition_id):
    """Update an existing exhibition."""
    return exhibition_planner_views.api_update_exhibition(exhibition_id)


@content_bp.route('/api/exhibitions/<int:exhibition_id>', methods=['DELETE'])
@login_required
def api_delete_exhibition(exhibition_id):
    """Delete an exhibition."""
    return exhibition_planner_views.api_delete_exhibition(exhibition_id)


@content_bp.route('/api/exhibitions/<int:exhibition_id>/checklist', methods=['PUT'])
@login_required
def api_update_exhibition_checklist(exhibition_id):
    """Update exhibition checklist data."""
    return exhibition_planner_views.api_update_exhibition_checklist(exhibition_id)
