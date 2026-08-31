"""Shared route implementations for museum reporting and content views."""

import logging
import os

from flask import (abort, flash, jsonify, redirect, render_template, request,
                   send_file, url_for)
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


def load_visitor_records():
    """Load visitor records from PostgreSQL (raises on failure)."""
    with get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, visit_date AS date, visitor_type, group_size,
                       age_category, nationality, ticket_type, guided_tour,
                       exhibition, feedback_rating, notes
                FROM visitor_records
                ORDER BY visit_date DESC NULLS LAST, id DESC
                """
            )
            return cur.fetchall()


def load_research_projects():
    """Load research projects from PostgreSQL (raises on failure)."""
    with get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, project_code, principal_investigator,
                       department, research_area, start_date, end_date,
                       funding_source, budget, status, description,
                       publications, collaborators, keywords
                FROM research_projects
                ORDER BY start_date DESC NULLS LAST, id DESC
                """
            )
            return cur.fetchall()


def handle_add_visitor():
    """Handle visitor record creation form (persists to PostgreSQL)."""
    if request.method == 'POST':
        try:
            with get_postgres_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO visitor_records (
                            visit_date, visitor_type, group_size, age_category,
                            nationality, ticket_type, guided_tour, exhibition,
                            feedback_rating, notes
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            request.form.get('date', '').strip() or None,
                            request.form.get('visitor_type', '').strip(),
                            int(request.form.get('group_size', '').strip())
                            if request.form.get('group_size', '').strip().isdigit()
                            else 1,
                            request.form.get('age_category', '').strip(),
                            request.form.get('nationality', 'Србија').strip(),
                            request.form.get('ticket_type', '').strip(),
                            request.form.get('guided_tour') == 'on',
                            request.form.get('exhibition', '').strip(),
                            request.form.get('feedback_rating', '').strip(),
                            request.form.get('notes', '').strip(),
                        ),
                    )
                conn.commit()
        except Exception:
            logger.exception("Error saving visitor record")
            flash('Грешка при чувању посете — податак НИЈЕ забележен.', 'error')
            return render_template('admin_add_visitor.html')

        flash('Посета је успешно забележена!', 'success')
        return redirect(url_for('visitors_database'))

    return render_template('admin_add_visitor.html')


def handle_add_research():
    """Handle research project creation form (persists to PostgreSQL)."""
    if request.method == 'POST':
        try:
            with get_postgres_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO research_projects (
                            title, project_code, principal_investigator,
                            department, research_area, start_date, end_date,
                            funding_source, budget, status, description,
                            publications, collaborators, keywords
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            request.form.get('title', '').strip(),
                            request.form.get('project_code', '').strip(),
                            request.form.get('principal_investigator', '').strip(),
                            request.form.get('department', '').strip(),
                            request.form.get('research_area', '').strip(),
                            request.form.get('start_date', '').strip() or None,
                            request.form.get('end_date', '').strip() or None,
                            request.form.get('funding_source', '').strip(),
                            request.form.get('budget', '').strip(),
                            request.form.get('status', 'У току').strip(),
                            request.form.get('description', '').strip(),
                            request.form.get('publications', '').strip(),
                            request.form.get('collaborators', '').strip(),
                            request.form.get('keywords', '').strip(),
                        ),
                    )
                conn.commit()
        except Exception:
            logger.exception("Error saving research project")
            flash('Грешка при чувању пројекта — податак НИЈЕ забележен.', 'error')
            return render_template('admin_add_research.html')

        flash('Истраживачки пројекат је успешно додат!', 'success')
        return redirect(url_for('research_database'))

    return render_template('admin_add_research.html')


def render_visitors_database():
    """Render visitor records database page."""
    visitor_records = load_visitor_records()
    return render_template(
        'admin_visitors_database.html',
        visitors=visitor_records,
        total_visitors=len(visitor_records),
    )


def export_visitors_to_pdf(*, visitors_endpoint='visitors_database'):
    """Show placeholder export behavior for visitor statistics."""
    flash('Функционалност извоза посетилаца у PDF је у развоју.', 'info')
    return redirect(url_for(visitors_endpoint))


def render_research_database():
    """Render research projects database page."""
    research_projects = load_research_projects()
    return render_template(
        'admin_research_database.html',
        projects=research_projects,
        total_projects=len(research_projects),
    )


def export_research_to_pdf(*, project_id, list_endpoint='research_database'):
    """Export a single research project to PDF."""
    project = next(
        (entry for entry in load_research_projects() if str(entry.get('id')) == str(project_id)),
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


def _stranica_iz_zahteva(podrazumevano=12, najvise=48):
    """Broj strane i velicina strane iz query stringa, uvek u razumnom opsegu."""
    try:
        strana = max(1, int(request.args.get('strana', 1)))
    except (TypeError, ValueError):
        strana = 1
    try:
        po_strani = int(request.args.get('po_strani', podrazumevano))
    except (TypeError, ValueError):
        po_strani = podrazumevano
    po_strani = min(max(po_strani, 6), najvise)
    return strana, po_strani


def render_museum_news(*, news_store):
    """Prikaz muzejskih vesti — cita bazu pri svakom zahtevu, ne kes u procesu."""
    upit = (request.args.get('q') or '').strip()
    tip = (request.args.get('tip') or '').strip() or None
    izvor = (request.args.get('izvor') or '').strip() or None
    godina = (request.args.get('godina') or '').strip() or None

    if izvor not in (None, 'rucni', 'nhmbeo'):
        izvor = None

    strana, po_strani = _stranica_iz_zahteva()

    vesti, ukupno = news_store.dohvati_vesti(
        upit=upit or None,
        tip=tip,
        izvor=izvor,
        godina=godina,
        limit=po_strani,
        pomak=(strana - 1) * po_strani,
    )
    pregled = news_store.pregled()

    ima_filtera = bool(upit or tip or izvor or godina)
    # Naslovna vest se izdvaja samo na prvoj strani bez filtera — inace bi
    # korisnik pomislio da je rezultat pretrage nekako povlascen.
    naslovna = vesti[0] if (vesti and strana == 1 and not ima_filtera) else None
    ostale = vesti[1:] if naslovna else vesti

    ukupno_strana = max(1, -(-ukupno // po_strani))

    return render_template(
        'admin_news.html',
        naslovna=naslovna,
        vesti=ostale,
        ukupno=ukupno,
        pregled=pregled,
        upit=upit,
        tip=tip,
        izvor=izvor,
        godina=godina,
        ima_filtera=ima_filtera,
        strana=strana,
        po_strani=po_strani,
        ukupno_strana=ukupno_strana,
    )


def render_news_article(*, news_store, vest_id):
    """Strana za citanje jedne vesti."""
    vest = news_store.dohvati_vest(vest_id)
    if vest is None:
        abort(404)
    novija, starija = news_store.susedne_vesti(vest)
    pasusi = [red.strip() for red in (vest.get('sadrzaj_tekst') or '').split('\n')
              if red.strip()]
    return render_template(
        'news_article.html',
        vest=vest,
        pasusi=pasusi,
        novija=novija,
        starija=starija,
    )


def api_refresh_news(*, news_importer, news_store, pokrenuo='ручно',
                     razmak_sekundi=60):
    """Rucno pokretanje uvoza sa sajta muzeja.

    Delimican uvoz se NE prijavljuje kao uspeh — korisnik mora da vidi da
    sajt nije vratio deo objava, inace izgleda kao da vesti prosto nema.
    Uzastopni klikovi u roku od ``razmak_sekundi`` vracaju posledji ishod
    umesto da ponovo gadjaju tudji sajt.
    """
    from datetime import datetime, timezone

    try:
        poslednji = news_store.pregled()['poslednji_uvoz']
    except Exception:
        logger.exception("Ne mogu da procitam trag poslednjeg uvoza")
        poslednji = None

    if poslednji and poslednji.get('zavrseno_at'):
        proteklo = (datetime.now(timezone.utc)
                    - poslednji['zavrseno_at']).total_seconds()
        if 0 <= proteklo < razmak_sekundi:
            return jsonify({
                'success': poslednji['status'] == 'uspeh',
                'status': poslednji['status'],
                'novih': poslednji['novih'],
                'azuriranih': poslednji['azuriranih'],
                'pregledano': poslednji['pregledano'],
                'preskoceno': 0,
                'ponovljeno': True,
                'message': 'Освежено пре %d s · %s' % (
                    int(proteklo), poslednji['poruka'] or ''),
            })

    try:
        ishod = news_importer.uvezi_vesti(pokrenuo=pokrenuo)
    except Exception as exc:
        logger.exception("Rucni uvoz muzejskih vesti nije uspeo")
        return jsonify({
            'success': False,
            'status': 'greska',
            'message': 'Увоз са сајта музеја није успео: %s' % exc,
        }), 502

    return jsonify({
        'success': ishod['status'] == 'uspeh',
        'status': ishod['status'],
        'novih': ishod['novih'],
        'azuriranih': ishod['azuriranih'],
        'pregledano': ishod['pregledano'],
        'preskoceno': ishod.get('preskoceno', 0),
        'message': ishod['poruka'],
    })


def api_get_news(*, news_store, vest_id):
    """Jedna rucna vest kao JSON — modal za izmenu je puni odavde.

    Podaci ne idu kroz HTML atribute (data-naslov i slicno) jer bi svaki
    propust u escape-ovanju odmah bio XSS; ovako naslov nikad ne dodiruje
    HTML parser.
    """
    vest = news_store.dohvati_vest(vest_id)
    if vest is None:
        return jsonify({'success': False, 'message': 'Вест не постоји'}), 404
    if vest['izvor'] != 'rucni':
        return jsonify({
            'success': False,
            'message': 'Вест је преузета са сајта музеја и уређује се тамо.',
        }), 409
    return jsonify({
        'id': vest['id'],
        'title': vest['title'] or '',
        'description': vest['description'] or '',
        'type': vest['type'] or '',
        'start_date': vest['start_date'].isoformat() if vest['start_date'] else '',
        'curator': vest['curator'] or '',
        'location': vest['location'] or '',
        'source_link': vest['source_link'] or '',
        'keywords': vest['keywords'] or '',
    })


def api_delete_news(*, news_store, vest_id):
    """Brisanje rucne vesti; uvezene se ne brisu odavde."""
    try:
        obrisano, poruka = news_store.obrisi_vest(vest_id)
    except Exception as exc:
        logger.exception("Brisanje vesti nije uspelo")
        return jsonify({'success': False, 'message': 'Грешка: %s' % exc}), 500
    return jsonify({'success': obrisano, 'message': poruka}), (
        200 if obrisano else 400)


def api_save_news():
    """Sacuvaj rucnu vest. Baza je izvor istine — nema kesa da se osvezava."""
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
                        'SELECT izvor FROM news_articles WHERE id = %s',
                        (article_id,),
                    )
                    postojeca = cur.fetchone()
                    if postojeca is None:
                        return jsonify({
                            'success': False,
                            'message': 'Вест не постоји',
                        }), 404
                    if postojeca['izvor'] != 'rucni':
                        # Sledeci uvoz bi izmenu pregazio, pa je odbijamo
                        # odmah umesto da korisnik izgubi rad.
                        return jsonify({
                            'success': False,
                            'message': ('Вест је преузета са сајта музеја и '
                                        'уређује се тамо — измена овде би '
                                        'нестала при следећем увозу.'),
                        }), 409

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

        return jsonify({'success': True, 'message': message})
    except Exception as exc:
        logger.exception("Error saving news")
        return jsonify({'success': False, 'message': f'Грешка: {exc}'})
