"""Shared route implementations for museum reporting and content views."""

import logging
import os

from flask import flash, jsonify, redirect, render_template, request, send_file, url_for
from psycopg.rows import dict_row

from postgres_service import get_postgres_connection
from pdf_export import export_research_project_pdf

logger = logging.getLogger(__name__)


def handle_add_book(*, library_database, save_library_database, phase3a_databases=None):
    """Handle library book creation form."""
    if request.method == 'POST':
        book_data = {
            'title': request.form.get('title', '').strip(),
            'author': request.form.get('author', '').strip(),
            'isbn': request.form.get('isbn', '').strip(),
            'category': request.form.get('category', '').strip(),
            'publication_year': int(request.form.get('year', 0))
            if request.form.get('year', '').strip().isdigit()
            else None,
            'location': request.form.get('location', '').strip(),
            'status': request.form.get('status', 'доступна').strip(),
            'description': request.form.get('description', '').strip(),
            'pages': int(request.form.get('pages', 0))
            if request.form.get('pages', '').strip().isdigit()
            else None,
            'publisher': request.form.get('publisher', '').strip(),
            'language': request.form.get('language', 'српски').strip(),
        }

        if os.environ.get('DATABASE_URL') and phase3a_databases is not None:
            book_id = phase3a_databases.save_library_book(book_data)
            if book_id:
                flash('Књига је успешно додата у библиотеку!', 'success')
            else:
                flash('Грешка при чувању књиге у базу.', 'error')
        else:
            book_data['id'] = len(library_database['books']) + 1
            book_data['year'] = book_data.pop('publication_year')
            library_database['books'].append(book_data)
            save_library_database()
            flash('Књига је успешно додата у библиотеку!', 'success')

        return redirect(url_for('library_database'))

    return render_template('admin_add_book.html')


def handle_add_visitor(*, visitor_records):
    """Handle visitor record creation form."""
    if request.method == 'POST':
        visitor_data = {
            'id': max((record.get('id', 0) for record in visitor_records), default=0) + 1,
            'date': request.form.get('date', '').strip(),
            'visitor_type': request.form.get('visitor_type', '').strip(),
            'group_size': int(request.form.get('group_size', '').strip())
            if request.form.get('group_size', '').strip().isdigit()
            else 1,
            'age_category': request.form.get('age_category', '').strip(),
            'nationality': request.form.get('nationality', 'Србија').strip(),
            'ticket_type': request.form.get('ticket_type', '').strip(),
            'guided_tour': request.form.get('guided_tour') == 'on',
            'exhibition': request.form.get('exhibition', '').strip(),
            'feedback_rating': request.form.get('feedback_rating', '').strip(),
            'notes': request.form.get('notes', '').strip(),
        }
        visitor_records.append(visitor_data)
        flash('Посета је успешно забележена!', 'success')
        return redirect(url_for('visitors_database'))

    return render_template('admin_add_visitor.html')


def handle_add_research(*, research_projects):
    """Handle research project creation form."""
    if request.method == 'POST':
        research_data = {
            'id': max((project.get('id', 0) for project in research_projects), default=0) + 1,
            'title': request.form.get('title', '').strip(),
            'project_code': request.form.get('project_code', '').strip(),
            'principal_investigator': request.form.get('principal_investigator', '').strip(),
            'department': request.form.get('department', '').strip(),
            'research_area': request.form.get('research_area', '').strip(),
            'start_date': request.form.get('start_date', '').strip(),
            'end_date': request.form.get('end_date', '').strip(),
            'funding_source': request.form.get('funding_source', '').strip(),
            'budget': request.form.get('budget', '').strip(),
            'status': request.form.get('status', 'У току').strip(),
            'description': request.form.get('description', '').strip(),
            'publications': request.form.get('publications', '').strip(),
            'collaborators': request.form.get('collaborators', '').strip(),
            'keywords': request.form.get('keywords', '').strip(),
        }
        research_projects.append(research_data)
        flash('Истраживачки пројекат је успешно додат!', 'success')
        return redirect(url_for('research_database'))

    return render_template('admin_add_research.html')


def render_visitors_database(*, visitor_records):
    """Render visitor records database page."""
    return render_template(
        'admin_visitors_database.html',
        visitors=visitor_records,
        total_visitors=len(visitor_records),
    )


def export_visitors_to_pdf(*, visitors_endpoint='visitors_database'):
    """Show placeholder export behavior for visitor statistics."""
    flash('Функционалност извоза посетилаца у PDF је у развоју.', 'info')
    return redirect(url_for(visitors_endpoint))


def render_research_database(*, research_projects):
    """Render research projects database page."""
    return render_template(
        'admin_research_database.html',
        projects=research_projects,
        total_projects=len(research_projects),
    )


def export_research_to_pdf(*, research_projects, project_id, list_endpoint='research_database'):
    """Export a single research project to PDF."""
    project = next(
        (entry for entry in research_projects if str(entry.get('id')) == str(project_id)),
        None,
    )
    if project is None:
        flash('Истраживачки пројекат није пронађен.', 'error')
        return redirect(url_for(list_endpoint))

    pdf_buffer = export_research_project_pdf(project)
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"research_project_{project_id}.pdf",
    )


def render_system_reports(
    *,
    get_library_database,
    get_employee_directory,
    get_exhibit_statistics,
    user_has_module_access,
):
    """Render system-wide reporting and analytics."""
    library_database = get_library_database()
    employees = get_employee_directory()

    total_employees = len(employees)
    total_books = len(library_database['books'])
    exhibit_stats = get_exhibit_statistics()
    total_artifacts = exhibit_stats['total_artifacts']

    admin_count = len([emp for emp in employees if emp.get('role') == 'admin'])
    employee_count = total_employees - admin_count

    dept_stats = {}
    for emp in employees:
        department = emp.get('department') or 'Непознато'
        dept_stats[department] = dept_stats.get(department, 0) + 1

    library_stats = library_database['statistics'].copy()
    available_books = len([book for book in library_database['books'] if book['status'] == 'доступна'])
    borrowed_books = len([book for book in library_database['books'] if book['status'] == 'позајмљена'])

    displayed_artifacts = exhibit_stats['displayed_artifacts']
    storage_artifacts = exhibit_stats['storage_artifacts']

    timesheet_users = len(
        [
            emp
            for emp in employees
            if user_has_module_access(emp.get('email', ''), emp.get('role', 'employee'), 'timesheet')
        ]
    )
    database_users = len(
        [
            emp
            for emp in employees
            if user_has_module_access(
                emp.get('email', ''),
                emp.get('role', 'employee'),
                'museum_databases',
            )
        ]
    )

    report_data = {
        'system_overview': {
            'total_employees': total_employees,
            'total_books': total_books,
            'total_artifacts': total_artifacts,
            'active_databases': 5,
            'planned_databases': 2,
        },
        'employee_stats': {
            'total': total_employees,
            'admins': admin_count,
            'employees': employee_count,
            'departments': dept_stats,
        },
        'library_stats': {
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books,
            'utilization_rate': round((borrowed_books / total_books * 100), 1)
            if total_books > 0
            else 0,
        },
        'exhibit_stats': {
            'total_artifacts': total_artifacts,
            'displayed_artifacts': displayed_artifacts,
            'storage_artifacts': storage_artifacts,
            'display_rate': round((displayed_artifacts / total_artifacts * 100), 1)
            if total_artifacts > 0
            else 0,
        },
        'access_stats': {
            'timesheet_users': timesheet_users,
            'database_users': database_users,
            'total_with_access': timesheet_users,
        },
    }
    library_stats.update(
        {
            'available_books': available_books,
            'borrowed_books': borrowed_books,
        }
    )
    report_data['library_stats'].update(library_stats)

    return render_template('admin_reports.html', report_data=report_data)


def render_exhibits_database(*, exhibits_database, get_exhibit_statistics):
    """Render the exhibits database view."""
    artifacts = exhibits_database['artifacts']
    statistics = get_exhibit_statistics()
    categories = sorted({artifact['category'] for artifact in artifacts})
    statuses = exhibits_database.get('statuses', sorted({artifact['status'] for artifact in artifacts}))
    conditions = exhibits_database.get(
        'conditions',
        sorted({artifact['condition'] for artifact in artifacts}),
    )

    return render_template(
        'admin_exhibits_database.html',
        artifacts=artifacts,
        statistics=statistics,
        categories=categories,
        statuses=statuses,
        conditions=conditions,
    )


def render_exhibitions_database(*, exhibitions_database, get_exhibition_statistics):
    """Render the exhibitions database view."""
    exhibitions_all = sorted(
        exhibitions_database['exhibitions'],
        key=lambda exhibition: exhibition.get('start_date') or '',
        reverse=True,
    )
    gallery_exhibitions = [
        exhibition
        for exhibition in exhibitions_all
        if exhibition.get('category', 'gallery') != 'touring'
    ]
    touring_exhibitions = [
        exhibition
        for exhibition in exhibitions_all
        if exhibition.get('category', 'gallery') == 'touring'
    ]
    statistics = get_exhibition_statistics()
    exhibition_types = exhibitions_database.get(
        'types',
        sorted({exhibition.get('type', 'Изложба') for exhibition in gallery_exhibitions}),
    )

    return render_template(
        'admin_exhibitions_database.html',
        exhibitions=gallery_exhibitions,
        touring_exhibitions=touring_exhibitions,
        statistics=statistics,
        exhibition_types=exhibition_types,
    )


def render_museum_news(*, news_database):
    """Render the museum news view."""
    articles_all = sorted(
        news_database['articles'],
        key=lambda article: article.get('start_date', ''),
        reverse=True,
    )
    recent_articles = articles_all[:20]

    return render_template(
        'admin_news.html',
        articles=recent_articles,
        total_articles=len(articles_all),
    )


def api_save_news(*, news_database):
    """Save a news article and refresh the cached news dataset."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Нема података'})

        title = data.get('title', '').strip()
        description = data.get('description', '').strip()

        if not title or not description:
            return jsonify({'success': False, 'message': 'Наслов и опис су обавезни'})

        with get_postgres_connection(row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                article_id = data.get('id')

                if article_id:
                    cur.execute(
                        """
                        UPDATE news_articles SET
                            title = %s,
                            description = %s,
                            type = %s,
                            start_date = %s,
                            curator = %s,
                            location = %s,
                            source_link = %s,
                            keywords = %s,
                            updated_at = NOW()
                        WHERE id = %s
                        """,
                        (
                            title,
                            description,
                            data.get('type', 'Објава'),
                            data.get('start_date') or None,
                            data.get('curator', ''),
                            data.get('location', ''),
                            data.get('source_link', ''),
                            data.get('keywords', ''),
                            article_id,
                        ),
                    )
                    message = 'Вест је успешно ажурирана'
                else:
                    cur.execute(
                        """
                        INSERT INTO news_articles (
                            title,
                            description,
                            type,
                            start_date,
                            curator,
                            location,
                            source_link,
                            keywords,
                            created_at
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
                        RETURNING id
                        """,
                        (
                            title,
                            description,
                            data.get('type', 'Објава'),
                            data.get('start_date') or None,
                            data.get('curator', ''),
                            data.get('location', ''),
                            data.get('source_link', ''),
                            data.get('keywords', ''),
                        ),
                    )
                    new_id = cur.fetchone()['id']
                    message = f'Вест је успешно сачувана (ID: {new_id})'

                conn.commit()

        news_database.refresh()
        return jsonify({'success': True, 'message': message})
    except Exception as exc:
        logger.exception("Error saving news")
        return jsonify({'success': False, 'message': f'Грешка: {exc}'})
