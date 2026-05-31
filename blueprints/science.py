"""Science and depot routes extracted from app.py."""

from flask import Blueprint, current_app, render_template

import depot_science_views
import map_feature_paper_enricher
import scientific_paper_views
import scientific_papers_database
from security_utils import admin_required, login_required, module_access_required


science_bp = Blueprint('science', __name__)


@science_bp.route('/admin/science_news')
@module_access_required('mineral_database')
def admin_science_news():
    """Curated scientific news page for the mineralogical database."""
    return render_template('admin_science_news.html')


@science_bp.route('/admin/scientific_papers')
@module_access_required('scientific_papers')
def scientific_papers_view():
    """Browse scientific papers with pagination and filters."""
    return scientific_paper_views.render_scientific_papers(
        scientific_papers_database=scientific_papers_database,
        museum_databases_endpoint='museum_databases',
    )


@science_bp.route('/admin/scientific_paper/<int:paper_id>')
@module_access_required('scientific_papers')
def scientific_paper_detail(paper_id):
    """View detailed information for a single scientific paper."""
    return scientific_paper_views.render_scientific_paper_detail(
        paper_id=paper_id,
        scientific_papers_database=scientific_papers_database,
        list_endpoint='scientific_papers_view',
    )


@science_bp.route('/admin/scientific_papers/locality/<locality_name>')
@module_access_required('scientific_papers')
def scientific_papers_by_locality(locality_name):
    """View papers for a specific geological map sheet locality."""
    return scientific_paper_views.render_scientific_papers_by_locality(
        locality_name=locality_name,
        scientific_papers_database=scientific_papers_database,
    )


@science_bp.route('/api/map/locality-papers/<locality_name>')
@login_required
def api_locality_papers(locality_name):
    """JSON API for locality paper summary (map popup integration)."""
    return scientific_paper_views.api_locality_papers(
        locality_name=locality_name,
        scientific_papers_database=scientific_papers_database,
    )


@science_bp.route('/api/map/feature-papers/<feature_type>/<path:feature_name>')
@login_required
def api_feature_papers(feature_type, feature_name):
    """JSON API for feature paper summary (map popup integration)."""
    return scientific_paper_views.api_feature_papers(
        feature_type=feature_type,
        feature_name=feature_name,
        map_feature_paper_enricher=map_feature_paper_enricher,
    )


@science_bp.route('/api/admin/start-paper-enrichment', methods=['POST'])
@admin_required
def api_start_paper_enrichment():
    """Admin trigger for background paper enrichment."""
    return scientific_paper_views.api_start_paper_enrichment(
        map_feature_paper_enricher=map_feature_paper_enricher,
    )


@science_bp.route('/api/admin/paper-enrichment-status')
@admin_required
def api_paper_enrichment_status():
    """Progress polling for paper enrichment."""
    return scientific_paper_views.api_paper_enrichment_status(
        map_feature_paper_enricher=map_feature_paper_enricher,
    )


@science_bp.route('/api/depot/localities', methods=['GET'])
@login_required
def api_get_localities():
    """Get all unique localities from the mineral collection with counts and info."""
    return depot_science_views.api_get_localities(
        get_mineral_database=current_app.get_mineral_database,
    )


@science_bp.route('/api/science-news', methods=['GET'])
@login_required
def api_get_science_news():
    """Get curated science news from database with optional filters."""
    return depot_science_views.api_get_science_news()


@science_bp.route('/api/science-news', methods=['POST'])
@admin_required
def api_add_science_news():
    """Add a new science news item."""
    return depot_science_views.api_add_science_news()


@science_bp.route('/api/science-news/<news_id>', methods=['DELETE'])
@admin_required
def api_delete_science_news(news_id):
    """Delete a science news item."""
    return depot_science_views.api_delete_science_news(news_id=news_id)


@science_bp.route('/api/depot/locality/<path:locality_name>', methods=['GET'])
@login_required
def api_get_locality_detail(locality_name):
    """Get detailed information about a specific locality."""
    return depot_science_views.api_get_locality_detail(
        locality_name,
        get_mineral_database=current_app.get_mineral_database,
    )
