"""Конзерваторско-рестаураторски досије — view/handler логика.

Routing и декоратори су у `blueprints/kr_dosije.py`; овде је сва логика
(као и остали *_views.py модули). Чисто рашчлањавање и формати су у
`kr_dosije_core.py`. Слике иду кроз постојећу Фототеку (`fototeka_views`).
"""

import os
import uuid
from datetime import date, datetime
from pathlib import Path

from flask import (
    abort, flash, jsonify, redirect, render_template, request, send_file,
    session, url_for,
)

from postgres_service import get_postgres_connection
import audit_support
import kr_dosije_core as core
import fototeka_views
import fototeka_jobs


# ---------------------------------------------------------------------------
# Контекст корисника / права
# ---------------------------------------------------------------------------
def _ctx():
    """Право-релевантан контекст тренутног корисника из сесије."""
    role = session.get('user_role', '')
    return {
        'email': (session.get('user_email') or '').strip().lower(),
        'name': session.get('user_name', ''),
        'role': role,
        'is_admin': role == 'admin',
        'is_director': role == 'direktor',
        'is_head': bool(session.get('is_department_head')),
        'odeljenje': core.department_to_odeljenje(session.get('user_department', '')),
    }


def _sees_all(ctx):
    """Директор и админ виде све; остали само своје одељење."""
    return ctx['is_admin'] or ctx['is_director']


def _visible_odeljenja(ctx):
    """Скуп одељења која корисник сме да види, или None = сва."""
    if _sees_all(ctx):
        return None
    return {ctx['odeljenje']} if ctx['odeljenje'] else set()


def _can_edit(ctx, dosije):
    """Уређивање: админ/директор свуда; иначе само у свом одељењу."""
    if _sees_all(ctx):
        return True
    return ctx['odeljenje'] is not None and dosije['odeljenje'] == ctx['odeljenje']


def _can_delete(ctx, dosije):
    """Брисање: админ/директор или сам аутор записа."""
    return _sees_all(ctx) or dosije.get('created_by_email') == ctx['email']


# ---------------------------------------------------------------------------
# Читање из базе
# ---------------------------------------------------------------------------
def _row_dict(cur, row):
    if row is None:
        return None
    return {desc[0]: val for desc, val in zip(cur.description, row)}


def _fetch_dosije(cur, dosije_id):
    cur.execute('SELECT * FROM kr_dosije WHERE id = %s', (dosije_id,))
    return _row_dict(cur, cur.fetchone())


def _fetch_izvrsioci(cur, dosije_id):
    cur.execute(
        """
        SELECT user_email, ime_tekst
        FROM kr_dosije_izvrsilac
        WHERE dosije_id = %s
        ORDER BY redosled, id
        """,
        (dosije_id,),
    )
    return [{'user_email': e, 'ime_tekst': i} for e, i in cur.fetchall()]


def _fetch_fotografije(cur, dosije_id):
    """Повезане фотографије по фази (id + мета за приказ сличица)."""
    cur.execute(
        """
        SELECT v.id AS veza_id, v.faza, f.id AS foto_id, f.sha256,
               f.original_ime, f.opis, f.obrisana
        FROM foto_veza_kr_dosije v
        JOIN fotografije f ON f.id = v.fotografija_id
        WHERE v.dosije_id = %s AND f.obrisana = FALSE
        ORDER BY v.faza, v.redosled, v.id
        """,
        (dosije_id,),
    )
    out = {'pre': [], 'tokom': [], 'posle': []}
    for veza_id, faza, foto_id, sha256, ime, opis, _obr in cur.fetchall():
        out.setdefault(faza, []).append({
            'veza_id': veza_id, 'foto_id': foto_id, 'sha256': sha256,
            'original_ime': ime, 'opis': opis,
        })
    return out


# ---------------------------------------------------------------------------
# Листа
# ---------------------------------------------------------------------------
PER_PAGE = 25


def render_lista():
    ctx = _ctx()
    q = (request.args.get('q') or '').strip()
    odeljenje_filter = (request.args.get('odeljenje') or '').strip()
    page = _parse_page(request.args.get('page'))

    where, params = [], []
    vis = _visible_odeljenja(ctx)
    if vis is not None:
        if not vis:
            # Корисник без препознатог одељења (нпр. администрација) без
            # директорских права не види ниједан досије.
            return render_template('kr_dosije_lista.html', dosijei=[], q=q,
                                   odeljenje_filter=odeljenje_filter, ctx=ctx,
                                   odeljenje_labels=core.ODELJENJE_LABELS,
                                   page=1, total_pages=1, total=0)
        where.append('odeljenje = ANY(%s)')
        params.append(list(vis))
    if odeljenje_filter in core.ODELJENJE_LABELS:
        where.append('odeljenje = %s')
        params.append(odeljenje_filter)
    if q:
        where.append('(evidencioni_broj ILIKE %s OR naziv_predmeta ILIKE %s '
                     'OR inventarni_broj ILIKE %s OR kolektorski_broj ILIKE %s)')
        like = f'%{q}%'
        params += [like, like, like, like]

    where_sql = (' WHERE ' + ' AND '.join(where)) if where else ''
    with get_postgres_connection() as conn, conn.cursor() as cur:
        cur.execute('SELECT COUNT(*) FROM kr_dosije' + where_sql, params)
        total = cur.fetchone()[0]
        total_pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)
        page = min(page, total_pages)
        cur.execute(
            'SELECT * FROM kr_dosije' + where_sql +
            ' ORDER BY created_at DESC, id DESC LIMIT %s OFFSET %s',
            params + [PER_PAGE, (page - 1) * PER_PAGE],
        )
        dosijei = [_row_dict(cur, r) for r in cur.fetchall()]
        for d in dosijei:
            d['izvrsioci'] = _fetch_izvrsioci(cur, d['id'])

    return render_template('kr_dosije_lista.html', dosijei=dosijei, q=q,
                           odeljenje_filter=odeljenje_filter, ctx=ctx,
                           odeljenje_labels=core.ODELJENJE_LABELS,
                           page=page, total_pages=total_pages, total=total)


def _parse_page(raw):
    try:
        return max(1, int(raw))
    except (TypeError, ValueError):
        return 1


# ---------------------------------------------------------------------------
# Форма (нови / измена)
# ---------------------------------------------------------------------------
def render_forma(dosije_id=None):
    ctx = _ctx()
    dosije, izvrsioci, fotografije = None, [], {'pre': [], 'tokom': [], 'posle': []}
    if dosije_id is not None:
        with get_postgres_connection() as conn, conn.cursor() as cur:
            dosije = _fetch_dosije(cur, dosije_id)
            if dosije is None:
                abort(404)
            if not _can_edit(ctx, dosije):
                abort(403)
            izvrsioci = _fetch_izvrsioci(cur, dosije_id)
            fotografije = _fetch_fotografije(cur, dosije_id)

    korisnici = _active_users()
    return render_template(
        'kr_dosije_forma.html', dosije=dosije, izvrsioci=izvrsioci,
        fotografije=fotografije, ctx=ctx, korisnici=korisnici,
        odeljenje_labels=core.ODELJENJE_LABELS, faza_labels=core.FAZA_LABELS,
    )


def _form_common(form):
    """Заједничко читање поља форме у dict за upsert."""
    predmet_tip = 'zbirka' if form.get('predmet_tip') == 'zbirka' else 'slobodan'
    naziv = (form.get('naziv_predmeta') or '').strip()
    period_od = _parse_date_field(form.get('period_od'))
    period_do = _parse_date_field(form.get('period_do'))
    return {
        'predmet_tip': predmet_tip,
        'database_name': (form.get('database_name') or '').strip() or None,
        'inventarni_broj': (form.get('inventarni_broj') or '').strip() or None,
        'kolektorski_broj': (form.get('kolektorski_broj') or '').strip() or None,
        'naziv_predmeta': naziv,
        'narucilac': (form.get('narucilac') or '').strip() or None,
        'opis_pre': (form.get('opis_pre') or '').strip() or None,
        'opis_postupak': (form.get('opis_postupak') or '').strip() or None,
        'opis_posle': (form.get('opis_posle') or '').strip() or None,
        'period_od': period_od,
        'period_do': period_do,
        'period_tekst': (form.get('period_tekst') or '').strip() or None,
        'napomena': (form.get('napomena') or '').strip() or None,
    }


def handle_create():
    ctx = _ctx()
    data = _form_common(request.form)
    if not data['naziv_predmeta']:
        flash('Назив предмета је обавезан.', 'danger')
        return redirect(url_for('kr_dosije.novi'))

    odeljenje = (request.form.get('odeljenje') or '').strip()
    if not _sees_all(ctx):
        # Конзерватор увек уписује у своје одељење, без обзира на форму.
        odeljenje = ctx['odeljenje']
    if odeljenje not in core.ODELJENJE_LABELS:
        flash('Изаберите важеће одељење.', 'danger')
        return redirect(url_for('kr_dosije.novi'))

    with get_postgres_connection() as conn, conn.cursor() as cur:
        evb = core.next_evidencioni_broj(cur, odeljenje, date.today().year)
        cur.execute(
            """
            INSERT INTO kr_dosije
                (evidencioni_broj, odeljenje, predmet_tip, database_name,
                 inventarni_broj, kolektorski_broj, naziv_predmeta, narucilac,
                 opis_pre, opis_postupak, opis_posle, period_od, period_do,
                 period_tekst, napomena, izvor, created_by_email)
            VALUES (%(evb)s, %(odeljenje)s, %(predmet_tip)s, %(database_name)s,
                    %(inventarni_broj)s, %(kolektorski_broj)s, %(naziv_predmeta)s,
                    %(narucilac)s, %(opis_pre)s, %(opis_postupak)s, %(opis_posle)s,
                    %(period_od)s, %(period_do)s, %(period_tekst)s, %(napomena)s,
                    'rucno', %(email)s)
            RETURNING id
            """,
            {**data, 'evb': evb, 'odeljenje': odeljenje, 'email': ctx['email']},
        )
        dosije_id = cur.fetchone()[0]
        _save_izvrsioci(cur, dosije_id, request.form)
        conn.commit()

    flash(f'Досије {evb} је креиран.', 'success')
    return redirect(url_for('kr_dosije.detalj', dosije_id=dosije_id))


def handle_update(dosije_id):
    ctx = _ctx()
    data = _form_common(request.form)
    if not data['naziv_predmeta']:
        flash('Назив предмета је обавезан.', 'danger')
        return redirect(url_for('kr_dosije.izmena', dosije_id=dosije_id))

    with get_postgres_connection() as conn, conn.cursor() as cur:
        dosije = _fetch_dosije(cur, dosije_id)
        if dosije is None:
            abort(404)
        if not _can_edit(ctx, dosije):
            abort(403)
        cur.execute(
            """
            UPDATE kr_dosije SET
                predmet_tip=%(predmet_tip)s, database_name=%(database_name)s,
                inventarni_broj=%(inventarni_broj)s, kolektorski_broj=%(kolektorski_broj)s,
                naziv_predmeta=%(naziv_predmeta)s, narucilac=%(narucilac)s,
                opis_pre=%(opis_pre)s, opis_postupak=%(opis_postupak)s,
                opis_posle=%(opis_posle)s, period_od=%(period_od)s,
                period_do=%(period_do)s, period_tekst=%(period_tekst)s,
                napomena=%(napomena)s, updated_at=NOW()
            WHERE id=%(id)s
            """,
            {**data, 'id': dosije_id},
        )
        cur.execute('DELETE FROM kr_dosije_izvrsilac WHERE dosije_id = %s', (dosije_id,))
        _save_izvrsioci(cur, dosije_id, request.form)
        conn.commit()

    flash('Досије је сачуван.', 'success')
    return redirect(url_for('kr_dosije.detalj', dosije_id=dosije_id))


def _save_izvrsioci(cur, dosije_id, form):
    """Извршиоци из форме: изабрани корисници (email-ови) + слободни уноси имена."""
    emails = form.getlist('izvrsilac_email')
    slobodni = form.getlist('izvrsilac_ime')
    korisnici = {u['email']: u['full_name'] for u in _active_users(cur)}
    redosled = 0
    seen = set()
    for email in emails:
        email = (email or '').strip().lower()
        if not email or email in seen or email not in korisnici:
            continue
        seen.add(email)
        _insert_izvrsilac(cur, dosije_id, email, korisnici[email], redosled)
        redosled += 1
    for ime in slobodni:
        ime = ' '.join((ime or '').split())
        if not ime or ime in seen:
            continue
        seen.add(ime)
        _insert_izvrsilac(cur, dosije_id, None, ime, redosled)
        redosled += 1


def _insert_izvrsilac(cur, dosije_id, email, ime, redosled):
    cur.execute(
        """
        INSERT INTO kr_dosije_izvrsilac (dosije_id, user_email, ime_tekst, redosled)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (dosije_id, ime_tekst) DO NOTHING
        """,
        (dosije_id, email, ime, redosled),
    )


def handle_delete(dosije_id):
    ctx = _ctx()
    with get_postgres_connection() as conn, conn.cursor() as cur:
        dosije = _fetch_dosije(cur, dosije_id)
        if dosije is None:
            abort(404)
        if not _can_delete(ctx, dosije):
            abort(403)
        # foto_veza_kr_dosije и izvrsioci падају уз ON DELETE CASCADE.
        # Саме фотографије у Фototeci остају (веза се само раскида).
        cur.execute('DELETE FROM kr_dosije WHERE id = %s', (dosije_id,))
        conn.commit()
    audit_support.record_audit(
        action=audit_support.ACTION_DELETE,
        entity_type='kr_dosije',
        entity_id=dosije_id,
        summary=f'Обрисан К-Р досије #{dosije_id}'
                + (f' — {dosije.get("naziv_predmeta")}' if dosije.get('naziv_predmeta') else ''),
        old_values=dict(dosije) if isinstance(dosije, dict) else None,
        changed_by=ctx.get('email') if isinstance(ctx, dict) else None,
    )
    flash('Досије је обрисан.', 'success')
    return redirect(url_for('kr_dosije.lista'))


# ---------------------------------------------------------------------------
# Детаљ
# ---------------------------------------------------------------------------
def render_detalj(dosije_id):
    ctx = _ctx()
    with get_postgres_connection() as conn, conn.cursor() as cur:
        dosije = _fetch_dosije(cur, dosije_id)
        if dosije is None:
            abort(404)
        vis = _visible_odeljenja(ctx)
        if vis is not None and dosije['odeljenje'] not in vis:
            abort(403)
        izvrsioci = _fetch_izvrsioci(cur, dosije_id)
        fotografije = _fetch_fotografije(cur, dosije_id)

    return render_template(
        'kr_dosije_detalj.html', dosije=dosije, izvrsioci=izvrsioci,
        fotografije=fotografije, ctx=ctx, can_edit=_can_edit(ctx, dosije),
        can_delete=_can_delete(ctx, dosije),
        odeljenje_labels=core.ODELJENJE_LABELS, faza_labels=core.FAZA_LABELS,
    )


def handle_pdf(dosije_id):
    ctx = _ctx()
    with get_postgres_connection() as conn, conn.cursor() as cur:
        dosije = _fetch_dosije(cur, dosije_id)
        if dosije is None:
            abort(404)
        vis = _visible_odeljenja(ctx)
        if vis is not None and dosije['odeljenje'] not in vis:
            abort(403)
        dosije['izvrsioci'] = _fetch_izvrsioci(cur, dosije_id)
        dosije['fotografije'] = _fetch_fotografije(cur, dosije_id)

    from pdf_export import export_kr_dosije_pdf
    buffer = export_kr_dosije_pdf(dosije)
    return send_file(
        buffer, mimetype='application/pdf', as_attachment=True,
        download_name=f"KR_dosije_{dosije['evidencioni_broj']}.pdf",
    )


# ---------------------------------------------------------------------------
# Фотографије по фази (кроз постојећу Фototeku)
# ---------------------------------------------------------------------------
def handle_foto_upload(dosije_id):
    """Отпреми једну или више слика у Фototeku и вежи их за досије са фазом."""
    ctx = _ctx()
    faza = (request.form.get('faza') or '').strip()
    if faza not in core.FAZA_LABELS:
        flash('Изаберите фазу (пре/током/после).', 'danger')
        return redirect(url_for('kr_dosije.detalj', dosije_id=dosije_id))

    files = [f for f in request.files.getlist('slike')
             if f and (f.filename or '').strip()]
    if not files:
        flash('Нисте изабрали ниједну слику.', 'warning')
        return redirect(url_for('kr_dosije.detalj', dosije_id=dosije_id))

    dodato, preskoceno = 0, 0
    with get_postgres_connection() as conn, conn.cursor() as cur:
        dosije = _fetch_dosije(cur, dosije_id)
        if dosije is None:
            abort(404)
        if not _can_edit(ctx, dosije):
            abort(403)
        for uploaded in files:
            foto_id, _reason = _intake_web_file(cur, uploaded, ctx['email'])
            if foto_id is None:
                preskoceno += 1
                continue
            _link_foto(cur, foto_id, dosije_id, faza, ctx['email'])
            dodato += 1
        conn.commit()

    msg = f'Додато {dodato} слика у фазу „{core.FAZA_LABELS[faza]}".'
    if preskoceno:
        msg += f' Прескочено {preskoceno} (дупликат/неисправна).'
    flash(msg, 'success' if dodato else 'warning')
    return redirect(url_for('kr_dosije.detalj', dosije_id=dosije_id))


def _intake_web_file(cur, uploaded, autor_email):
    """Сними отпремљени фајл у temp и провуци кроз Фototeka intake.
    Ако слика већ постоји (исти sha256), врати постојећи id да се само вежe."""
    original_ime = Path(uploaded.filename).name
    ext = Path(original_ime).suffix.lower()
    if ext not in fototeka_views.ALLOWED_PHOTO_EXTENSIONS:
        return None, 'тип датотеке није дозвољен'
    uploaded.stream.seek(0, os.SEEK_END)
    file_size = uploaded.stream.tell()
    uploaded.stream.seek(0)
    if file_size <= 0 or file_size > fototeka_views.MAX_PHOTO_SIZE:
        return None, 'величина датотеке није у дозвољеном опсегу'

    temp_dir = fototeka_jobs.get_media_path() / 'temp'
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / f'{uuid.uuid4().hex}_{ext.lstrip(".")}'
    try:
        uploaded.save(temp_path)
        sha256 = fototeka_jobs.sha256_of_file(temp_path)
        cur.execute('SELECT id FROM fotografije WHERE sha256 = %s', (sha256,))
        existing = cur.fetchone()
        if existing:
            return existing[0], None
        foto_id, reason = fototeka_views._intake_photo_from_path(
            cur, temp_path, original_ime, file_size, ext,
            autor_email=autor_email, opis=None, tags=['к-р-досије'],
            datum_override=None, veza=None, u_prijemnom_redu=False,
            poreklo='upload', vidljivost='javno',
        )
        return foto_id, reason
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _link_foto(cur, foto_id, dosije_id, faza, email):
    cur.execute(
        """
        INSERT INTO foto_veza_kr_dosije
            (fotografija_id, dosije_id, faza, redosled, created_by_email)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (fotografija_id, dosije_id, faza) DO NOTHING
        """,
        (foto_id, dosije_id, faza, core.FAZA_REDOSLED.get(faza, 0), email),
    )


def handle_foto_detach(dosije_id, veza_id):
    """Раскини везу досије↔фотографија (сама слика остаје у Фototeci)."""
    ctx = _ctx()
    with get_postgres_connection() as conn, conn.cursor() as cur:
        dosije = _fetch_dosije(cur, dosije_id)
        if dosije is None:
            abort(404)
        if not _can_edit(ctx, dosije):
            abort(403)
        cur.execute(
            'DELETE FROM foto_veza_kr_dosije WHERE id = %s AND dosije_id = %s',
            (veza_id, dosije_id),
        )
        conn.commit()
    flash('Веза са фотографијом је уклоњена.', 'success')
    return redirect(url_for('kr_dosije.detalj', dosije_id=dosije_id))


# ---------------------------------------------------------------------------
# Autocomplete предмета (minerals + inventory_entries.collector)
# ---------------------------------------------------------------------------
def api_predmet_search():
    q = (request.args.get('q') or '').strip()
    if len(q) < 2:
        return jsonify({'rezultati': []})
    like = f'%{q}%'
    with get_postgres_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT m.inventory_number AS inv, m.item_name AS naziv, ie.collector AS col
            FROM minerals m
            LEFT JOIN inventory_entries ie ON ie.inventory_number = m.inventory_number
            WHERE m.inventory_number ILIKE %s OR m.item_name ILIKE %s
                  OR ie.collector ILIKE %s
            ORDER BY m.inventory_number
            LIMIT 20
            """,
            (like, like, like),
        )
        rezultati = []
        for inv, naziv, col in cur.fetchall():
            rezultati.append({
                'database_name': 'mineral',
                'inventarni_broj': inv,
                'kolektorski_broj': col,
                'naziv': naziv,
                'prikaz': f"M{inv} — {naziv or ''}".strip(' —'),
            })
    return jsonify({'rezultati': rezultati})


# ---------------------------------------------------------------------------
# Предлошци поступака (CRUD)
# ---------------------------------------------------------------------------
def render_predlosci():
    ctx = _ctx()
    with get_postgres_connection() as conn, conn.cursor() as cur:
        cur.execute(
            'SELECT * FROM kr_predlozak ORDER BY vrsta, naziv'
        )
        predlosci = [_row_dict(cur, r) for r in cur.fetchall()]
    return render_template('kr_predlosci.html', predlosci=predlosci, ctx=ctx,
                           vrsta_labels=core.VRSTA_LABELS,
                           odeljenje_labels=core.ODELJENJE_LABELS)


def api_predlosci():
    """JSON предлошци за бирач у форми (филтрирани по врсти/одељењу)."""
    vrsta = (request.args.get('vrsta') or '').strip()
    odeljenje = (request.args.get('odeljenje') or '').strip()
    where, params = [], []
    if vrsta in core.VRSTA_LABELS:
        where.append('vrsta = %s')
        params.append(vrsta)
    if odeljenje in core.ODELJENJE_LABELS:
        where.append('(odeljenje = %s OR odeljenje IS NULL)')
        params.append(odeljenje)
    sql = 'SELECT id, vrsta, naziv, sadrzaj FROM kr_predlozak'
    if where:
        sql += ' WHERE ' + ' AND '.join(where)
    sql += ' ORDER BY naziv LIMIT 100'
    with get_postgres_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        out = [{'id': i, 'vrsta': v, 'naziv': n, 'sadrzaj': s}
               for i, v, n, s in cur.fetchall()]
    return jsonify({'predlosci': out})


def handle_predlozak_create():
    ctx = _ctx()
    vrsta = (request.form.get('vrsta') or '').strip()
    naziv = (request.form.get('naziv') or '').strip()
    sadrzaj = (request.form.get('sadrzaj') or '').strip()
    odeljenje = (request.form.get('odeljenje') or '').strip() or None
    if vrsta not in core.VRSTA_LABELS or not naziv or not sadrzaj:
        flash('Врста, назив и садржај предлошка су обавезни.', 'danger')
        return redirect(url_for('kr_dosije.predlosci'))
    if odeljenje is not None and odeljenje not in core.ODELJENJE_LABELS:
        odeljenje = None
    with get_postgres_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO kr_predlozak (odeljenje, vrsta, naziv, sadrzaj, created_by_email)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (odeljenje, vrsta, naziv, sadrzaj, ctx['email']),
        )
        conn.commit()
    flash('Предложак је додат.', 'success')
    return redirect(url_for('kr_dosije.predlosci'))


def handle_predlozak_update(predlozak_id):
    ctx = _ctx()
    naziv = (request.form.get('naziv') or '').strip()
    sadrzaj = (request.form.get('sadrzaj') or '').strip()
    if not naziv or not sadrzaj:
        flash('Назив и садржај су обавезни.', 'danger')
        return redirect(url_for('kr_dosije.predlosci'))
    with get_postgres_connection() as conn, conn.cursor() as cur:
        cur.execute(
            'UPDATE kr_predlozak SET naziv=%s, sadrzaj=%s, updated_at=NOW() WHERE id=%s',
            (naziv, sadrzaj, predlozak_id),
        )
        conn.commit()
    flash('Предложак је сачуван.', 'success')
    return redirect(url_for('kr_dosije.predlosci'))


def handle_predlozak_delete(predlozak_id):
    with get_postgres_connection() as conn, conn.cursor() as cur:
        cur.execute('DELETE FROM kr_predlozak WHERE id = %s', (predlozak_id,))
        conn.commit()
    flash('Предложак је обрисан.', 'success')
    return redirect(url_for('kr_dosije.predlosci'))


# ---------------------------------------------------------------------------
# Помоћно
# ---------------------------------------------------------------------------
def _active_users(cur=None):
    """Активни корисници (за бирач извршилаца). Ради са датим курсором или
    отвара свој."""
    def _run(c):
        c.execute(
            'SELECT email, full_name FROM users WHERE is_active = TRUE ORDER BY full_name'
        )
        return [{'email': e, 'full_name': n} for e, n in c.fetchall()]
    if cur is not None:
        return _run(cur)
    with get_postgres_connection() as conn, conn.cursor() as cur2:
        return _run(cur2)


def _parse_date_field(value):
    value = (value or '').strip()
    if not value:
        return None
    for fmt in ('%Y-%m-%d', '%d.%m.%Y'):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None
