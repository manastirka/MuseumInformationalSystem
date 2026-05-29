"""Shared route implementations for scientific paper views."""

import logging

from flask import current_app, flash, jsonify, redirect, render_template, request, url_for

logger = logging.getLogger(__name__)


def _resolve_endpoint(endpoint):
    """Map legacy scientific paper endpoints to blueprint endpoints when needed."""
    if endpoint in current_app.view_functions:
        return endpoint
    endpoint_aliases = {
        'scientific_papers_view': 'science.scientific_papers_view',
        'scientific_paper_detail': 'science.scientific_paper_detail',
        'scientific_papers_by_locality': 'science.scientific_papers_by_locality',
    }
    return endpoint_aliases.get(endpoint, endpoint)


def render_scientific_papers(*, scientific_papers_database, museum_databases_endpoint):
    """Browse scientific papers with pagination and filters."""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        search = request.args.get('search', '').strip() or None
        locality_filter = request.args.get('locality', '').strip() or None
        year_filter = request.args.get('year', '').strip() or None
        journal_filter = request.args.get('journal', '').strip() or None
        sort_by = request.args.get('sort_by', 'cited_by_count')
        sort_order = request.args.get('sort_order', 'DESC')
        min_citations = request.args.get('min_citations', '').strip() or None

        papers, total_count, total_pages = scientific_papers_database.get_all_papers(
            page=page,
            per_page=per_page,
            search=search,
            locality_filter=locality_filter,
            year_filter=year_filter,
            journal_filter=journal_filter,
            sort_by=sort_by,
            sort_order=sort_order,
            min_citations=min_citations,
        )

        return render_template(
            'admin_scientific_papers.html',
            papers=papers,
            total_count=total_count,
            total_pages=total_pages,
            current_page=page,
            per_page=per_page,
            all_localities=scientific_papers_database.get_all_localities(),
            all_journals=scientific_papers_database.get_all_journals(),
            all_years=scientific_papers_database.get_all_years(),
            stats=scientific_papers_database.get_statistics(),
            search=search or '',
            locality_filter=locality_filter or '',
            year_filter=year_filter or '',
            journal_filter=journal_filter or '',
            sort_by=sort_by,
            sort_order=sort_order,
            min_citations=min_citations or '',
        )
    except Exception as exc:
        logger.error("Error loading scientific papers: %s", exc)
        flash('Грешка при учитавању базе научних радова.', 'error')
        return redirect(url_for(museum_databases_endpoint))


def render_scientific_paper_detail(*, paper_id, scientific_papers_database, list_endpoint):
    """Render a single scientific paper detail page."""
    try:
        paper = scientific_papers_database.get_paper_by_id(paper_id)
        if not paper:
            flash('Рад није пронађен.', 'error')
            return redirect(url_for(_resolve_endpoint(list_endpoint)))
        return render_template('admin_scientific_paper_detail.html', paper=paper)
    except Exception as exc:
        logger.error("Error loading scientific paper %s: %s", paper_id, exc)
        flash('Грешка при учитавању рада.', 'error')
        return redirect(url_for(_resolve_endpoint(list_endpoint)))


def render_scientific_papers_by_locality(
    *,
    locality_name,
    scientific_papers_database,
):
    """Render papers for a specific geological locality."""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        sort_by = request.args.get('sort_by', 'cited_by_count')
        sort_order = request.args.get('sort_order', 'DESC')

        papers, total_count, total_pages = scientific_papers_database.get_papers_by_locality(
            locality_name,
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        return render_template(
            'admin_scientific_papers.html',
            papers=papers,
            total_count=total_count,
            total_pages=total_pages,
            current_page=page,
            per_page=per_page,
            all_localities=scientific_papers_database.get_all_localities(),
            all_journals=scientific_papers_database.get_all_journals(),
            all_years=scientific_papers_database.get_all_years(),
            stats=scientific_papers_database.get_statistics(),
            search='',
            locality_filter=locality_name,
            year_filter='',
            journal_filter='',
            sort_by=sort_by,
            sort_order=sort_order,
            min_citations='',
        )
    except Exception as exc:
        logger.error("Error loading papers for locality %s: %s", locality_name, exc)
        flash('Грешка при учитавању радова за локалитет.', 'error')
        return redirect(url_for(_resolve_endpoint('scientific_papers_view')))


def api_locality_papers(*, locality_name, scientific_papers_database):
    """Return a paper summary for a map locality."""
    try:
        summary = scientific_papers_database.get_locality_paper_summary(locality_name)
        return jsonify({'success': True, 'data': summary})
    except Exception as exc:
        logger.error("Error getting papers for locality %s: %s", locality_name, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_feature_papers(*, feature_type, feature_name, map_feature_paper_enricher):
    """Return a paper summary for an enriched map feature."""
    try:
        summary = map_feature_paper_enricher.get_feature_paper_summary(feature_type, feature_name)
        return jsonify({'success': True, 'data': summary})
    except Exception as exc:
        logger.error("Error getting papers for %s/%s: %s", feature_type, feature_name, exc)
        return jsonify({'success': False, 'message': str(exc)}), 500


def api_start_paper_enrichment(*, map_feature_paper_enricher):
    """Trigger background paper enrichment."""
    started = map_feature_paper_enricher.start_enrichment_background()
    if started:
        return jsonify({'success': True, 'message': 'Enrichment started'})
    return jsonify({'success': False, 'message': 'Enrichment already running'})


def api_paper_enrichment_status(*, map_feature_paper_enricher):
    """Return current background paper enrichment state."""
    status = map_feature_paper_enricher.get_enrichment_status()
    return jsonify({'success': True, 'data': status})
