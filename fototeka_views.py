"""Фототека: самосталне фотографије са таговима и опционим везама.

A photograph is a first-class object; links to a collection item, field trip,
project or exhibition are optional and added from either side at any time.
RAW originals go under FOTOTEKA_ARHIVA_PATH (write-once — this module only
ever creates files there, never modifies or deletes), derivatives are built
by the dedicated worker (fototeka_worker.py) from the foto_poslovi queue and
served from FOTOTEKA_MEDIA_PATH. Deleting a photo is a soft delete in the
database; the RAW file always stays.
"""

import json
import os
import re
import shutil
import uuid
from datetime import date, datetime
from pathlib import Path

from flask import (
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)

import fototeka_jobs
import image_matcher
from collection_registry import iter_collection_list_entries
from postgres_service import get_postgres_connection


# Formats PIL can open — validated and EXIF-read at intake.
PIL_DECODABLE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.webp', '.bmp', '.gif'}

# Camera RAW / archival originals accepted as-is (PIL/libvips can't open them,
# so no intake validation and no auto-derivative — see fototeka_jobs).
ARCHIVAL_RAW_EXTENSIONS = {
    '.cr2', '.cr3', '.nef', '.nrw', '.arw', '.srf', '.sr2', '.dng', '.raf',
    '.orf', '.rw2', '.pef', '.srw', '.raw', '.3fr', '.iiq', '.rwl', '.x3f',
}

ALLOWED_PHOTO_EXTENSIONS = PIL_DECODABLE_EXTENSIONS | ARCHIVAL_RAW_EXTENSIONS

# Preview formats accepted when attaching a derivative to a 'bez_derivata' photo.
PREVIEW_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

MAX_PHOTO_SIZE = 200 * 1024 * 1024  # 200MB — RAW files are large; matches nginx client_max_body_size

PHOTO_STATUS_LABELS = {
    'primljena': 'Примљена',
    'obrada': 'Обрада у току',
    'spremna': 'Спремна',
    'greska': 'Грешка у обради',
    'bez_derivata': 'Без умањеног приказа',
}

VEZA_TIP_LABELS = {
    'predmet': 'Предмет',
    'teren': 'Терен',
    'projekat': 'Пројекат',
    'izlozba': 'Изложба',
}

GALLERY_PAGE_SIZE = 60

_EXIF_DATETIME_ORIGINAL = 36867
_EXIF_MAKE = 271
_EXIF_MODEL = 272
_EXIF_IFD = 0x8769


def get_zbirka_labels():
    labels = {
        entry.collection_type: entry.collection_name
        for entry in iter_collection_list_entries()
    }
    labels['mineral'] = 'База минерала'
    return labels


def _session_email(session_data) -> str:
    return (session_data.get('user_email') or '').strip().lower()


def _session_is_admin(session_data) -> bool:
    return session_data.get('user_role') == 'admin'


def _session_is_director(session_data) -> bool:
    return session_data.get('user_role') == 'direktor'


def can_edit_photo(session_data, photo) -> bool:
    """Metadata/links: the author, admins, the director and department heads."""
    if _session_is_admin(session_data) or _session_is_director(session_data):
        return True
    if bool(session_data.get('is_department_head', False)):
        return True
    autor = (photo.get('autor_email') or '').strip().lower()
    user_email = _session_email(session_data)
    return bool(user_email) and user_email == autor


def _row_to_dict(cursor, row):
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    columns = [column.name for column in cursor.description]
    return dict(zip(columns, row))


def _rows_to_dicts(cursor, rows):
    return [_row_to_dict(cursor, row) for row in rows]


def _scalar(row, key):
    if row is None:
        return None
    return row.get(key) if isinstance(row, dict) else row[0]


def _parse_tags(raw: str):
    tags = []
    for piece in (raw or '').replace(';', ',').split(','):
        tag = ' '.join(piece.split())
        if tag and tag.casefold() not in {t.casefold() for t in tags}:
            tags.append(tag)
    return tags[:30]


def _parse_datum(raw: str):
    raw = (raw or '').strip()
    if not raw:
        return None
    try:
        return date.fromisoformat(raw)
    except ValueError:
        return None


def _extract_exif(pil_image):
    """Minimal EXIF excerpt: capture date, camera make/model, dimensions."""
    width, height = pil_image.size
    info = {'width': width, 'height': height, 'datum_snimanja': None, 'exif': {}}
    try:
        exif = pil_image.getexif()
        raw_datetime = exif.get_ifd(_EXIF_IFD).get(_EXIF_DATETIME_ORIGINAL)
        make = exif.get(_EXIF_MAKE)
        model = exif.get(_EXIF_MODEL)
        if raw_datetime:
            info['exif']['DateTimeOriginal'] = str(raw_datetime)
            try:
                info['datum_snimanja'] = datetime.strptime(
                    str(raw_datetime), '%Y:%m:%d %H:%M:%S',
                ).date()
            except ValueError:
                pass
        if make:
            info['exif']['Make'] = str(make).strip('\x00 ')
        if model:
            info['exif']['Model'] = str(model).strip('\x00 ')
    except Exception:
        pass
    return info


def _get_or_create_teren(cur, godina, naziv):
    cur.execute(
        """
        INSERT INTO fototeka_tereni (godina, naziv, created_by_email)
        VALUES (%s, %s, %s)
        ON CONFLICT (godina, naziv) DO UPDATE SET naziv = EXCLUDED.naziv
        RETURNING id
        """,
        (godina, naziv, _session_email(session)),
    )
    return _scalar(cur.fetchone(), 'id')


def _parse_veza_form(form, cur):
    """Read the optional link fields from an upload/link form. Returns a dict
    {'tip': ..., ...} or None; raises ValueError with a user-facing message.
    New field trips / projects are get-or-created inside the caller's
    transaction."""
    tip = (form.get('veza_tip') or '').strip()
    if not tip or tip == 'bez':
        return None
    if tip == 'predmet':
        zbirka = (form.get('veza_zbirka') or '').strip()
        inventarni_broj = ' '.join((form.get('veza_inventarni_broj') or '').split())
        if zbirka not in get_zbirka_labels():
            raise ValueError('Изаберите важећу збирку.')
        if not inventarni_broj:
            raise ValueError('Инвентарни број је обавезан за везу са предметом.')
        return {'tip': 'predmet', 'database_name': zbirka,
                'inventarni_broj': inventarni_broj}
    if tip == 'teren':
        teren_id_raw = (form.get('veza_teren_id') or '').strip()
        if teren_id_raw:
            cur.execute(
                'SELECT id, godina, naziv FROM fototeka_tereni WHERE id = %s',
                (int(teren_id_raw),),
            )
            teren = _row_to_dict(cur, cur.fetchone())
            if not teren:
                raise ValueError('Изабрани терен не постоји.')
            return {'tip': 'teren', 'teren_id': teren['id'],
                    'godina': teren['godina'], 'naziv': teren['naziv']}
        naziv = ' '.join((form.get('veza_teren_naziv') or '').split())
        godina_raw = (form.get('veza_teren_godina') or '').strip()
        if not naziv or not godina_raw.isdigit():
            raise ValueError('За нови терен унесите годину и назив акције.')
        godina = int(godina_raw)
        if not 1850 <= godina <= 2100:
            raise ValueError('Година терена није исправна.')
        teren_id = _get_or_create_teren(cur, godina, naziv)
        return {'tip': 'teren', 'teren_id': teren_id, 'godina': godina, 'naziv': naziv}
    if tip == 'projekat':
        projekat_id_raw = (form.get('veza_projekat_id') or '').strip()
        if projekat_id_raw:
            cur.execute(
                'SELECT id FROM fototeka_projekti WHERE id = %s',
                (int(projekat_id_raw),),
            )
            row = cur.fetchone()
            if not row:
                raise ValueError('Изабрани пројекат не постоји.')
            return {'tip': 'projekat', 'projekat_id': _scalar(row, 'id')}
        naziv = ' '.join((form.get('veza_projekat_naziv') or '').split())
        if not naziv:
            raise ValueError('Унесите назив новог пројекта.')
        cur.execute(
            """
            INSERT INTO fototeka_projekti (naziv, created_by_email)
            VALUES (%s, %s)
            ON CONFLICT (naziv) DO UPDATE SET naziv = EXCLUDED.naziv
            RETURNING id
            """,
            (naziv, _session_email(session)),
        )
        return {'tip': 'projekat', 'projekat_id': _scalar(cur.fetchone(), 'id')}
    if tip == 'izlozba':
        izlozba_id_raw = (form.get('veza_izlozba_id') or '').strip()
        if izlozba_id_raw:
            cur.execute('SELECT id FROM exhibitions WHERE id = %s', (int(izlozba_id_raw),))
            row = cur.fetchone()
            if not row:
                raise ValueError('Изабрана изложба не постоји.')
            return {'tip': 'izlozba', 'izlozba_id': _scalar(row, 'id')}
        naziv = ' '.join((form.get('veza_izlozba_naziv') or '').split())
        if not naziv:
            raise ValueError('Изаберите изложбу или унесите назив нове.')
        # Create a new exhibition — same bar as the exhibition planner
        # (login only); provenance from the session.
        cur.execute(
            """
            INSERT INTO exhibitions (title, created_by_email, created_by_name)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (naziv, _session_email(session), session.get('user_name', '')),
        )
        return {'tip': 'izlozba', 'izlozba_id': _scalar(cur.fetchone(), 'id')}
    raise ValueError('Непозната врста везе.')


def _insert_veza(cur, fotografija_id, veza):
    if veza is None:
        return
    if veza['tip'] == 'predmet':
        cur.execute(
            """
            INSERT INTO foto_veza_predmet (fotografija_id, database_name, inventarni_broj)
            VALUES (%s, %s, %s)
            ON CONFLICT (fotografija_id, database_name, inventarni_broj) DO NOTHING
            """,
            (fotografija_id, veza['database_name'], veza['inventarni_broj']),
        )
    elif veza['tip'] == 'teren':
        cur.execute(
            """
            INSERT INTO foto_veza_teren (fotografija_id, teren_id)
            VALUES (%s, %s)
            ON CONFLICT (fotografija_id, teren_id) DO NOTHING
            """,
            (fotografija_id, veza['teren_id']),
        )
    elif veza['tip'] == 'projekat':
        cur.execute(
            """
            INSERT INTO foto_veza_projekat (fotografija_id, projekat_id)
            VALUES (%s, %s)
            ON CONFLICT (fotografija_id, projekat_id) DO NOTHING
            """,
            (fotografija_id, veza['projekat_id']),
        )
    elif veza['tip'] == 'izlozba':
        cur.execute(
            """
            INSERT INTO foto_veza_izlozba (fotografija_id, exhibition_id)
            VALUES (%s, %s)
            ON CONFLICT (fotografija_id, exhibition_id) DO NOTHING
            """,
            (fotografija_id, veza['izlozba_id']),
        )


def _replace_tags(cur, fotografija_id, tags):
    cur.execute(
        'DELETE FROM fotografija_tagovi WHERE fotografija_id = %s',
        (fotografija_id,),
    )
    for tag in tags:
        cur.execute(
            """
            INSERT INTO fotografija_tagovi (fotografija_id, tag)
            VALUES (%s, %s)
            ON CONFLICT (fotografija_id, tag) DO NOTHING
            """,
            (fotografija_id, tag),
        )


def _fetch_photo(cur, fotografija_id, include_deleted=False):
    cur.execute(
        """
        SELECT id, sha256, raw_putanja, original_ime, ekstenzija,
               velicina_bajtova, width, height, autor_email, datum_snimanja,
               exif, opis, poreklo, status, u_prijemnom_redu, obrisana,
               fixity_proveren_at, fixity_ok, created_at, updated_at
        FROM fotografije WHERE id = %s
        """,
        (fotografija_id,),
    )
    photo = _row_to_dict(cur, cur.fetchone())
    if not photo:
        return None
    if photo['obrisana'] and not include_deleted:
        return None
    return photo


def _reference_lists(cur):
    """Dropdown data shared by the upload form and the link form."""
    cur.execute(
        'SELECT id, godina, naziv FROM fototeka_tereni ORDER BY godina DESC, naziv',
    )
    tereni = _rows_to_dicts(cur, cur.fetchall())
    cur.execute('SELECT id, naziv FROM fototeka_projekti ORDER BY naziv')
    projekti = _rows_to_dicts(cur, cur.fetchall())
    cur.execute('SELECT id, title FROM exhibitions ORDER BY id DESC LIMIT 300')
    izlozbe = _rows_to_dicts(cur, cur.fetchall())
    return tereni, projekti, izlozbe


# ---------------------------------------------------------------------------
# Gallery
# ---------------------------------------------------------------------------

def render_galerija():
    q = (request.args.get('q') or '').strip()
    tag = (request.args.get('tag') or '').strip()
    autor = (request.args.get('autor') or '').strip().lower()
    godina_raw = (request.args.get('godina') or '').strip()
    veza = (request.args.get('veza') or '').strip()
    try:
        page = max(1, int(request.args.get('strana', '1')))
    except ValueError:
        page = 1

    filters = ['f.obrisana = FALSE']
    params = []
    if q:
        filters.append('(f.opis ILIKE %s OR f.original_ime ILIKE %s)')
        params.extend([f'%{q}%', f'%{q}%'])
    if tag:
        filters.append(
            'EXISTS (SELECT 1 FROM fotografija_tagovi t '
            'WHERE t.fotografija_id = f.id AND lower(t.tag) = lower(%s))'
        )
        params.append(tag)
    if autor:
        filters.append('LOWER(f.autor_email) = %s')
        params.append(autor)
    if godina_raw.isdigit():
        filters.append(
            'EXTRACT(YEAR FROM COALESCE(f.datum_snimanja, f.created_at::date)) = %s'
        )
        params.append(int(godina_raw))

    veza_exists = {
        'predmet': 'EXISTS (SELECT 1 FROM foto_veza_predmet x WHERE x.fotografija_id = f.id)',
        'teren': 'EXISTS (SELECT 1 FROM foto_veza_teren x WHERE x.fotografija_id = f.id)',
        'projekat': 'EXISTS (SELECT 1 FROM foto_veza_projekat x WHERE x.fotografija_id = f.id)',
        'izlozba': 'EXISTS (SELECT 1 FROM foto_veza_izlozba x WHERE x.fotografija_id = f.id)',
    }
    if veza in veza_exists:
        filters.append(veza_exists[veza])
    elif veza == 'bez':
        filters.append(
            'NOT (' + ' OR '.join(veza_exists.values()) + ')'
        )
    elif veza == 'prijemni_red':
        filters.append('f.u_prijemnom_redu = TRUE')

    where_sql = ' AND '.join(filters)
    offset = (page - 1) * GALLERY_PAGE_SIZE

    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f'SELECT COUNT(*) AS total FROM fotografije f WHERE {where_sql}',
                params,
            )
            total = _scalar(cur.fetchone(), 'total') or 0
            cur.execute(
                f"""
                SELECT f.id, f.original_ime, f.opis, f.status, f.autor_email,
                       f.datum_snimanja, f.u_prijemnom_redu, f.created_at
                FROM fotografije f
                WHERE {where_sql}
                ORDER BY COALESCE(f.datum_snimanja, f.created_at::date) DESC, f.id DESC
                LIMIT %s OFFSET %s
                """,
                params + [GALLERY_PAGE_SIZE, offset],
            )
            photos = _rows_to_dicts(cur, cur.fetchall())

            cur.execute(
                """
                SELECT DISTINCT autor_email FROM fotografije
                WHERE obrisana = FALSE ORDER BY autor_email
                """,
            )
            autori = [_scalar(row, 'autor_email') for row in
                      _rows_to_dicts(cur, cur.fetchall())]
            cur.execute(
                """
                SELECT DISTINCT t.tag FROM fotografija_tagovi t
                JOIN fotografije f ON f.id = t.fotografija_id
                WHERE f.obrisana = FALSE ORDER BY t.tag LIMIT 200
                """,
            )
            tagovi = [_scalar(row, 'tag') for row in
                      _rows_to_dicts(cur, cur.fetchall())]
            tereni, projekti, izlozbe = _reference_lists(cur)

    total_pages = max(1, -(-total // GALLERY_PAGE_SIZE))
    return render_template(
        'fototeka_galerija.html',
        photos=photos,
        total=total,
        page=page,
        total_pages=total_pages,
        q=q, tag=tag, autor=autor, godina=godina_raw, veza=veza,
        autori=autori,
        tagovi=tagovi,
        tereni=tereni,
        projekti=projekti,
        izlozbe=izlozbe,
        zbirke=get_zbirka_labels(),
        status_labels=PHOTO_STATUS_LABELS,
    )


# ---------------------------------------------------------------------------
# Reception queue (пријемни ред)
# ---------------------------------------------------------------------------

def render_prijemni_red():
    """Photos flagged for curation (u_prijemnom_redu) — oldest first, so the
    backlog is worked front to back. A photo leaves the queue as soon as a
    link is added (handle_dodaj_vezu) or it is cleared here."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, original_ime, opis, status, autor_email,
                       datum_snimanja, created_at
                FROM fotografije
                WHERE obrisana = FALSE AND u_prijemnom_redu = TRUE
                ORDER BY created_at ASC, id ASC
                """,
            )
            photos = _rows_to_dicts(cur, cur.fetchall())
    return render_template(
        'fototeka_prijemni_red.html',
        photos=photos,
        status_labels=PHOTO_STATUS_LABELS,
    )


def handle_skini_sa_reda(fotografija_id):
    """Mark a queued photo as processed without adding a link (it may simply
    belong in the free gallery)."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            photo = _fetch_photo(cur, fotografija_id)
            if not photo:
                abort(404)
            if not can_edit_photo(session, photo):
                abort(403)
            cur.execute(
                """
                UPDATE fotografije SET u_prijemnom_redu = FALSE, updated_at = now()
                WHERE id = %s
                """,
                (fotografija_id,),
            )
    flash('Фотографија је скинута са пријемног реда.', 'success')
    return redirect(url_for('fototeka.fototeka_prijemni_red'))


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------

def render_upload_form():
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            tereni, projekti, izlozbe = _reference_lists(cur)
    # Optional link prefill from an entity page ("add a photo for this item").
    prefill = {
        'veza_tip': (request.args.get('veza_tip') or '').strip(),
        'veza_zbirka': (request.args.get('veza_zbirka') or '').strip(),
        'veza_inventarni_broj': (request.args.get('veza_inventarni_broj') or '').strip(),
        'veza_teren_id': (request.args.get('veza_teren_id') or '').strip(),
        'veza_projekat_id': (request.args.get('veza_projekat_id') or '').strip(),
        'veza_izlozba_id': (request.args.get('veza_izlozba_id') or '').strip(),
    }
    return render_template(
        'fototeka_upload.html',
        tereni=tereni,
        projekti=projekti,
        izlozbe=izlozbe,
        zbirke=get_zbirka_labels(),
        prefill=prefill,
    )


def _intake_photo_from_path(cur, temp_path, original_ime, file_size, ext, *,
                            autor_email, opis, tags, datum_override, veza,
                            u_prijemnom_redu, poreklo):
    """Core intake shared by upload and Samba import. Validates the image,
    dedups by sha256, places the RAW original by origin, inserts the row with
    tags + link and enqueues the derivative job. Moves temp_path into the
    archive on success; on dedup/invalid it leaves temp_path for the caller to
    clean up. Returns (fotografija_id, None) or (None, skip_reason)."""
    sha256 = fototeka_jobs.sha256_of_file(temp_path)
    if ext in PIL_DECODABLE_EXTENSIONS:
        try:
            from PIL import Image
            with Image.open(temp_path) as pil_image:
                pil_image.verify()
            with Image.open(temp_path) as pil_image:
                exif_info = _extract_exif(pil_image)
        except Exception:
            return None, f'{original_ime}: датотека није исправна слика'
    else:
        # Camera RAW / archival original: PIL can't open it, so accept as-is
        # without validation or EXIF. The worker will mark it 'bez_derivata'
        # if libvips also can't decode it.
        exif_info = {'width': None, 'height': None, 'datum_snimanja': None, 'exif': {}}

    cur.execute('SELECT id FROM fotografije WHERE sha256 = %s', (sha256,))
    existing = cur.fetchone()
    if existing:
        return None, (f'{original_ime}: идентична фотографија већ постоји '
                      f'(бр. {_scalar(existing, "id")})')

    datum_snimanja = datum_override or exif_info['datum_snimanja']
    raw_rel = fototeka_jobs.raw_intake_relative_path(
        veza_predmet=(
            (veza['database_name'], veza['inventarni_broj'])
            if veza and veza['tip'] == 'predmet' else None
        ),
        veza_teren=(
            (veza['godina'], veza['naziv'])
            if veza and veza['tip'] == 'teren' else None
        ),
        original_ime=original_ime,
        sha256=sha256,
        datum=datum_snimanja,
    )
    raw_full = fototeka_jobs.get_arhiva_path() / raw_rel
    raw_full.parent.mkdir(parents=True, exist_ok=True)
    # shutil.move survives temp and archive being on different filesystems
    # (os.replace would raise EXDEV).
    shutil.move(str(temp_path), str(raw_full))

    cur.execute(
        """
        INSERT INTO fotografije
            (sha256, raw_putanja, original_ime, ekstenzija,
             velicina_bajtova, width, height, autor_email,
             datum_snimanja, exif, opis, poreklo, u_prijemnom_redu)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (sha256, raw_rel, original_ime, ext, file_size,
         exif_info['width'], exif_info['height'], autor_email,
         datum_snimanja, json.dumps(exif_info['exif']), opis, poreklo,
         u_prijemnom_redu),
    )
    fotografija_id = _scalar(cur.fetchone(), 'id')
    _replace_tags(cur, fotografija_id, tags)
    _insert_veza(cur, fotografija_id, veza)
    fototeka_jobs.enqueue_job(cur, fotografija_id, 'derivati')
    return fotografija_id, None


def handle_upload():
    """Receive one or more photos with shared metadata and an optional link.
    Each file goes through _intake_photo_from_path (validate -> dedup -> RAW
    placement -> row + tags + link -> enqueue)."""
    files = [f for f in request.files.getlist('files')
             if f and (f.filename or '').strip()]
    if not files:
        flash('Изаберите бар једну фотографију.', 'warning')
        return redirect(url_for('fototeka.fototeka_upload'))

    opis = (request.form.get('opis') or '').strip() or None
    tags = _parse_tags(request.form.get('tagovi') or '')
    datum_override = _parse_datum(request.form.get('datum_snimanja'))
    u_prijemnom_redu = bool(request.form.get('u_prijemnom_redu'))
    user_email = _session_email(session)

    # The optional link is shared by every file; parse (and create any new
    # teren/projekat) once before the loop.
    try:
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                veza = _parse_veza_form(request.form, cur)
    except ValueError as exc:
        flash(str(exc), 'danger')
        return redirect(url_for('fototeka.fototeka_upload'))

    temp_dir = fototeka_jobs.get_media_path() / 'temp'
    temp_dir.mkdir(parents=True, exist_ok=True)

    saved, skipped = [], []
    for uploaded in files:
        original_ime = Path(uploaded.filename).name
        ext = Path(original_ime).suffix.lower()
        if ext not in ALLOWED_PHOTO_EXTENSIONS:
            skipped.append(f'{original_ime}: тип датотеке није дозвољен')
            continue
        uploaded.stream.seek(0, os.SEEK_END)
        file_size = uploaded.stream.tell()
        uploaded.stream.seek(0)
        if file_size <= 0:
            skipped.append(f'{original_ime}: датотека је празна')
            continue
        if file_size > MAX_PHOTO_SIZE:
            skipped.append(f'{original_ime}: већа од дозвољених 200 MB')
            continue

        temp_path = temp_dir / f'{uuid.uuid4().hex}_{ext.lstrip(".")}'
        try:
            uploaded.save(temp_path)
            with get_postgres_connection() as conn:
                with conn.cursor() as cur:
                    fotografija_id, reason = _intake_photo_from_path(
                        cur, temp_path, original_ime, file_size, ext,
                        autor_email=user_email, opis=opis, tags=tags,
                        datum_override=datum_override, veza=veza,
                        u_prijemnom_redu=u_prijemnom_redu, poreklo='upload',
                    )
            if fotografija_id:
                saved.append(fotografija_id)
            elif reason:
                skipped.append(reason)
        finally:
            if temp_path.exists():
                temp_path.unlink()

    if saved:
        flash(
            f'Примљено фотографија: {len(saved)}. Умањени прикази се обрађују у позадини.',
            'success',
        )
    for reason in skipped:
        flash(reason, 'warning')
    if len(saved) == 1 and not skipped:
        return redirect(url_for('fototeka.fototeka_fotografija', fotografija_id=saved[0]))
    return redirect(url_for('fototeka.fototeka_galerija'))


def handle_upload_jedan():
    """Intake exactly ONE file and return JSON. The browser sends the selected
    files one at a time (each request stays small, well under nginx's limit),
    so many/large files no longer fail as a single oversized multipart POST."""
    uploaded = request.files.get('file')
    if uploaded is None or not (uploaded.filename or '').strip():
        return jsonify({'ok': False, 'error': 'Недостаје датотека.'}), 400
    original_ime = Path(uploaded.filename).name
    ext = Path(original_ime).suffix.lower()
    if ext not in ALLOWED_PHOTO_EXTENSIONS:
        return jsonify({'ok': False, 'ime': original_ime,
                        'error': 'тип датотеке није дозвољен'}), 200
    uploaded.stream.seek(0, os.SEEK_END)
    file_size = uploaded.stream.tell()
    uploaded.stream.seek(0)
    if file_size <= 0:
        return jsonify({'ok': False, 'ime': original_ime, 'error': 'датотека је празна'}), 200
    if file_size > MAX_PHOTO_SIZE:
        return jsonify({'ok': False, 'ime': original_ime,
                        'error': 'већа од дозвољених 200 MB'}), 200

    opis = (request.form.get('opis') or '').strip() or None
    tags = _parse_tags(request.form.get('tagovi') or '')
    datum_override = _parse_datum(request.form.get('datum_snimanja'))
    u_prijemnom_redu = bool(request.form.get('u_prijemnom_redu'))
    user_email = _session_email(session)

    temp_dir = fototeka_jobs.get_media_path() / 'temp'
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / f'{uuid.uuid4().hex}_{ext.lstrip(".")}'
    try:
        uploaded.save(temp_path)
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                try:
                    veza = _parse_veza_form(request.form, cur)
                except ValueError as exc:
                    return jsonify({'ok': False, 'ime': original_ime,
                                    'error': str(exc)}), 200
                fotografija_id, reason = _intake_photo_from_path(
                    cur, temp_path, original_ime, file_size, ext,
                    autor_email=user_email, opis=opis, tags=tags,
                    datum_override=datum_override, veza=veza,
                    u_prijemnom_redu=u_prijemnom_redu, poreklo='upload',
                )
    finally:
        if temp_path.exists():
            temp_path.unlink()

    if fotografija_id:
        return jsonify({'ok': True, 'ime': original_ime, 'id': fotografija_id})
    return jsonify({'ok': False, 'ime': original_ime, 'error': reason or 'неуспешно'}), 200


def _make_preview_derivatives(source_path, sha256):
    """Build both derivatives from an attached preview using PIL — never pyvips,
    so the web process stays libvips-free. Mirrors the worker's sizes/quality."""
    from PIL import Image

    media_root = fototeka_jobs.get_media_path()
    dims = {}
    for kind, size in (('jpg', 2500), ('thumb', 300)):
        final_path = media_root / fototeka_jobs.derivative_relative_path(sha256, kind)
        final_path.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(source_path) as img:
            img = img.convert('RGB')
            dims = {'width': img.width, 'height': img.height}
            img.thumbnail((size, size), Image.Resampling.LANCZOS)
            temp_out = final_path.with_name(f'.tmp_{final_path.name}')
            img.save(temp_out, format='JPEG', quality=85, optimize=True)
        os.replace(temp_out, final_path)
    return dims


def handle_prilozi_derivat(fotografija_id):
    """Attach a JPG/PNG preview to a photo that has no auto-derivative (camera
    RAW / undecodable). Generates the derivatives with PIL and flips the photo
    to 'spremna'."""
    uploaded = request.files.get('preview')
    if uploaded is None or not (uploaded.filename or '').strip():
        flash('Изаберите JPG/PNG за преглед.', 'warning')
        return redirect(url_for('fototeka.fototeka_fotografija', fotografija_id=fotografija_id))
    ext = Path(uploaded.filename).suffix.lower()
    if ext not in PREVIEW_EXTENSIONS:
        flash('Преглед мора бити JPG или PNG.', 'danger')
        return redirect(url_for('fototeka.fototeka_fotografija', fotografija_id=fotografija_id))

    temp_dir = fototeka_jobs.get_media_path() / 'temp'
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / f'{uuid.uuid4().hex}_{ext.lstrip(".")}'
    try:
        uploaded.save(temp_path)
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                photo = _fetch_photo(cur, fotografija_id)
                if not photo:
                    abort(404)
                if not can_edit_photo(session, photo):
                    abort(403)
                try:
                    dims = _make_preview_derivatives(temp_path, photo['sha256'].strip())
                except Exception:
                    flash('Приложени преглед није исправна слика.', 'danger')
                    return redirect(url_for('fototeka.fototeka_fotografija',
                                            fotografija_id=fotografija_id))
                cur.execute(
                    """
                    UPDATE fotografije
                    SET status = 'spremna',
                        width = COALESCE(width, %s), height = COALESCE(height, %s),
                        updated_at = now()
                    WHERE id = %s
                    """,
                    (dims.get('width'), dims.get('height'), fotografija_id),
                )
    finally:
        if temp_path.exists():
            temp_path.unlink()
    flash('Преглед је приложен.', 'success')
    return redirect(url_for('fototeka.fototeka_fotografija', fotografija_id=fotografija_id))


# ---------------------------------------------------------------------------
# Photo page
# ---------------------------------------------------------------------------

def render_fotografija(fotografija_id):
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            photo = _fetch_photo(cur, fotografija_id)
            if not photo:
                abort(404)
            cur.execute(
                """
                SELECT tag FROM fotografija_tagovi
                WHERE fotografija_id = %s ORDER BY tag
                """,
                (fotografija_id,),
            )
            tags = [_scalar(row, 'tag') for row in _rows_to_dicts(cur, cur.fetchall())]
            cur.execute(
                """
                SELECT id, database_name, inventarni_broj FROM foto_veza_predmet
                WHERE fotografija_id = %s ORDER BY id
                """,
                (fotografija_id,),
            )
            veze_predmeti = _rows_to_dicts(cur, cur.fetchall())
            cur.execute(
                """
                SELECT v.id, t.godina, t.naziv FROM foto_veza_teren v
                JOIN fototeka_tereni t ON t.id = v.teren_id
                WHERE v.fotografija_id = %s ORDER BY v.id
                """,
                (fotografija_id,),
            )
            veze_tereni = _rows_to_dicts(cur, cur.fetchall())
            cur.execute(
                """
                SELECT v.id, p.naziv FROM foto_veza_projekat v
                JOIN fototeka_projekti p ON p.id = v.projekat_id
                WHERE v.fotografija_id = %s ORDER BY v.id
                """,
                (fotografija_id,),
            )
            veze_projekti = _rows_to_dicts(cur, cur.fetchall())
            cur.execute(
                """
                SELECT v.id, e.id AS exhibition_id, e.title FROM foto_veza_izlozba v
                JOIN exhibitions e ON e.id = v.exhibition_id
                WHERE v.fotografija_id = %s ORDER BY v.id
                """,
                (fotografija_id,),
            )
            veze_izlozbe = _rows_to_dicts(cur, cur.fetchall())
            cur.execute(
                """
                SELECT tip, status, pokusaji, poslednja_greska, updated_at
                FROM foto_poslovi WHERE fotografija_id = %s
                ORDER BY id DESC LIMIT 10
                """,
                (fotografija_id,),
            )
            poslovi = _rows_to_dicts(cur, cur.fetchall())
            tereni, projekti, izlozbe = _reference_lists(cur)

    zbirke = get_zbirka_labels()
    for veza in veze_predmeti:
        veza['zbirka_label'] = zbirke.get(veza['database_name'], veza['database_name'])
    return render_template(
        'fototeka_fotografija.html',
        photo=photo,
        tags=tags,
        tags_text=', '.join(tags),
        veze_predmeti=veze_predmeti,
        veze_tereni=veze_tereni,
        veze_projekti=veze_projekti,
        veze_izlozbe=veze_izlozbe,
        poslovi=poslovi,
        tereni=tereni,
        projekti=projekti,
        izlozbe=izlozbe,
        zbirke=zbirke,
        status_labels=PHOTO_STATUS_LABELS,
        can_edit=can_edit_photo(session, photo),
    )


def handle_azuriraj(fotografija_id):
    """Update description, capture date and the tag set."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            photo = _fetch_photo(cur, fotografija_id)
            if not photo:
                abort(404)
            if not can_edit_photo(session, photo):
                abort(403)
            opis = (request.form.get('opis') or '').strip() or None
            datum = _parse_datum(request.form.get('datum_snimanja'))
            cur.execute(
                """
                UPDATE fotografije
                SET opis = %s, datum_snimanja = %s, updated_at = now()
                WHERE id = %s
                """,
                (opis, datum, fotografija_id),
            )
            _replace_tags(cur, fotografija_id, _parse_tags(request.form.get('tagovi') or ''))
    flash('Подаци о фотографији су сачувани.', 'success')
    return redirect(url_for('fototeka.fototeka_fotografija', fotografija_id=fotografija_id))


def handle_dodaj_vezu(fotografija_id):
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            photo = _fetch_photo(cur, fotografija_id)
            if not photo:
                abort(404)
            if not can_edit_photo(session, photo):
                abort(403)
            try:
                veza = _parse_veza_form(request.form, cur)
            except ValueError as exc:
                flash(str(exc), 'danger')
                return redirect(url_for('fototeka.fototeka_fotografija',
                                        fotografija_id=fotografija_id))
            if veza is None:
                flash('Изаберите врсту везе.', 'warning')
                return redirect(url_for('fototeka.fototeka_fotografija',
                                        fotografija_id=fotografija_id))
            _insert_veza(cur, fotografija_id, veza)
            if photo['u_prijemnom_redu']:
                cur.execute(
                    """
                    UPDATE fotografije SET u_prijemnom_redu = FALSE, updated_at = now()
                    WHERE id = %s
                    """,
                    (fotografija_id,),
                )
    flash('Веза је додата.', 'success')
    return redirect(url_for('fototeka.fototeka_fotografija', fotografija_id=fotografija_id))


_VEZA_TABLES = {
    'predmet': 'foto_veza_predmet',
    'teren': 'foto_veza_teren',
    'projekat': 'foto_veza_projekat',
    'izlozba': 'foto_veza_izlozba',
}


def handle_ukloni_vezu(fotografija_id, tip, veza_id):
    table = _VEZA_TABLES.get(tip)
    if not table:
        abort(404)
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            photo = _fetch_photo(cur, fotografija_id)
            if not photo:
                abort(404)
            if not can_edit_photo(session, photo):
                abort(403)
            cur.execute(
                f'DELETE FROM {table} WHERE id = %s AND fotografija_id = %s RETURNING id',
                (veza_id, fotografija_id),
            )
            if not cur.fetchone():
                abort(404)
    flash('Веза је уклоњена.', 'success')
    return redirect(url_for('fototeka.fototeka_fotografija', fotografija_id=fotografija_id))


def handle_ponovi_obradu(fotografija_id):
    """Re-enqueue the derivative job after a failed processing run."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            photo = _fetch_photo(cur, fotografija_id)
            if not photo:
                abort(404)
            if not can_edit_photo(session, photo):
                abort(403)
            cur.execute(
                """
                SELECT 1 FROM foto_poslovi
                WHERE fotografija_id = %s AND tip = 'derivati'
                  AND status IN ('ceka', 'radi')
                """,
                (fotografija_id,),
            )
            if cur.fetchone():
                flash('Обрада је већ у реду.', 'info')
                return redirect(url_for('fototeka.fototeka_fotografija',
                                        fotografija_id=fotografija_id))
            cur.execute(
                """
                UPDATE fotografije SET status = 'primljena', updated_at = now()
                WHERE id = %s
                """,
                (fotografija_id,),
            )
            fototeka_jobs.enqueue_job(cur, fotografija_id, 'derivati')
    flash('Обрада је поново заказана.', 'success')
    return redirect(url_for('fototeka.fototeka_fotografija', fotografija_id=fotografija_id))


def handle_obrisi(fotografija_id):
    """Soft delete only — the RAW file in the archive is never touched."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            photo = _fetch_photo(cur, fotografija_id)
            if not photo:
                abort(404)
            cur.execute(
                """
                UPDATE fotografije SET obrisana = TRUE, updated_at = now()
                WHERE id = %s
                """,
                (fotografija_id,),
            )
    flash('Фотографија је уклоњена из Фототеке (оригинал остаје у архиви).', 'success')
    return redirect(url_for('fototeka.fototeka_galerija'))


# ---------------------------------------------------------------------------
# Serving files
# ---------------------------------------------------------------------------

def _send_placeholder(kind):
    from flask import current_app
    name = ('specimen-placeholder-thumb.png' if kind == 'thumb'
            else 'specimen-placeholder.png')
    placeholder = Path(current_app.static_folder) / 'images' / name
    if placeholder.is_file():
        return send_file(placeholder, mimetype='image/png', max_age=0)
    abort(404)


def serve_derivat(fotografija_id, kind):
    if kind not in ('jpg', 'thumb'):
        abort(404)
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            photo = _fetch_photo(cur, fotografija_id)
    if not photo:
        abort(404)
    if photo['status'] != 'spremna':
        return _send_placeholder(kind)
    media_root = fototeka_jobs.get_media_path().resolve()
    full_path = (media_root / fototeka_jobs.derivative_relative_path(
        photo['sha256'].strip(), kind)).resolve()
    if not str(full_path).startswith(str(media_root) + os.sep):
        abort(404)
    if not full_path.is_file():
        return _send_placeholder(kind)
    return send_file(full_path, mimetype='image/jpeg', max_age=3600)


def serve_raw(fotografija_id):
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            photo = _fetch_photo(cur, fotografija_id)
    if not photo:
        abort(404)
    arhiva_root = fototeka_jobs.get_arhiva_path().resolve()
    full_path = (arhiva_root / photo['raw_putanja']).resolve()
    if not str(full_path).startswith(str(arhiva_root) + os.sep):
        abort(404)
    if not full_path.is_file():
        abort(404)
    return send_file(
        full_path,
        as_attachment=True,
        download_name=photo['original_ime'] or full_path.name,
        max_age=0,
    )


# ---------------------------------------------------------------------------
# Autocomplete APIs
# ---------------------------------------------------------------------------

def api_tagovi():
    q = (request.args.get('q') or '').strip()
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT DISTINCT tag FROM fotografija_tagovi
                WHERE tag ILIKE %s ORDER BY tag LIMIT 15
                """,
                (f'%{q}%',),
            )
            tags = [_scalar(row, 'tag') for row in _rows_to_dicts(cur, cur.fetchall())]
    return jsonify(tags)


def api_predmeti():
    """Inventory-number autocomplete. Phase 1 covers the mineral collection
    (the only one whose items live in PostgreSQL); for other collections the
    inventory number is typed in freely."""
    zbirka = (request.args.get('zbirka') or '').strip()
    q = (request.args.get('q') or '').strip()
    if zbirka != 'mineral' or len(q) < 1:
        return jsonify([])
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT inventory_number, item_name FROM minerals
                WHERE inventory_number ILIKE %s OR item_name ILIKE %s
                ORDER BY inventory_number LIMIT 15
                """,
                (f'%{q}%', f'%{q}%'),
            )
            rows = _rows_to_dicts(cur, cur.fetchall())
    return jsonify([
        {'inventarni_broj': row['inventory_number'], 'naziv': row['item_name']}
        for row in rows
    ])


# ---------------------------------------------------------------------------
# Reverse linking (entitet -> foto): the "other direction" widget on a
# collection item / field trip / project / exhibition page. Linking is a
# non-destructive cross-reference, so any user with fototeka module access may
# add or remove links (the photo and its RAW original are never affected).
# ---------------------------------------------------------------------------

def _parse_entity_ref(source):
    """Read an entity reference (the linking target) from request args/form.
    Returns a dict that doubles as a valid `veza` for `_insert_veza`, or
    raises ValueError with a user-facing message."""
    tip = (source.get('tip') or '').strip()
    if tip == 'predmet':
        database_name = (source.get('database') or '').strip()
        inventarni_broj = ' '.join((source.get('broj') or '').split())
        if database_name not in get_zbirka_labels():
            raise ValueError('Непозната збирка.')
        if not inventarni_broj:
            raise ValueError('Недостаје инвентарни број.')
        return {'tip': 'predmet', 'database_name': database_name,
                'inventarni_broj': inventarni_broj}
    if tip == 'teren':
        raw = (source.get('teren_id') or '').strip()
        if not raw.isdigit():
            raise ValueError('Недостаје терен.')
        return {'tip': 'teren', 'teren_id': int(raw)}
    if tip == 'projekat':
        raw = (source.get('projekat_id') or '').strip()
        if not raw.isdigit():
            raise ValueError('Недостаје пројекат.')
        return {'tip': 'projekat', 'projekat_id': int(raw)}
    if tip == 'izlozba':
        raw = (source.get('izlozba_id') or '').strip()
        if not raw.isdigit():
            raise ValueError('Недостаје изложба.')
        return {'tip': 'izlozba', 'izlozba_id': int(raw)}
    raise ValueError('Непозната врста ентитета.')


def _entity_photo_filter(entity):
    """Return (table, condition, params) selecting the link rows for `entity`.
    The condition is table-qualified so it works in a JOIN, a NOT EXISTS and a
    DELETE alike. The table comes from the fixed _VEZA_TABLES whitelist."""
    tip = entity['tip']
    table = _VEZA_TABLES[tip]
    if tip == 'predmet':
        return (table,
                f'{table}.database_name = %s AND {table}.inventarni_broj = %s',
                (entity['database_name'], entity['inventarni_broj']))
    if tip == 'teren':
        return (table, f'{table}.teren_id = %s', (entity['teren_id'],))
    if tip == 'projekat':
        return (table, f'{table}.projekat_id = %s', (entity['projekat_id'],))
    return (table, f'{table}.exhibition_id = %s', (entity['izlozba_id'],))


def _photo_card(row):
    return {
        'id': row['id'],
        'opis': row['opis'] or row['original_ime'],
        'status': row['status'],
        'thumb_url': url_for('fototeka.fototeka_media',
                             fotografija_id=row['id'], kind='thumb'),
        'url': url_for('fototeka.fototeka_fotografija', fotografija_id=row['id']),
    }


def api_entitet_fotografije():
    """Photos already linked to the given entity (widget initial load)."""
    try:
        entity = _parse_entity_ref(request.args)
    except ValueError as exc:
        return jsonify({'ok': False, 'error': str(exc)}), 400
    table, cond, params = _entity_photo_filter(entity)
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT f.id, f.opis, f.original_ime, f.status
                FROM fotografije f
                JOIN {table} ON {table}.fotografija_id = f.id
                WHERE f.obrisana = FALSE AND {cond}
                ORDER BY f.id DESC
                """,
                params,
            )
            rows = _rows_to_dicts(cur, cur.fetchall())
    return jsonify({'ok': True, 'fotografije': [_photo_card(r) for r in rows]})


def api_entitet_pretraga():
    """Candidate photos to link to the entity: search by id, description,
    filename or tag, excluding photos already linked."""
    try:
        entity = _parse_entity_ref(request.args)
    except ValueError as exc:
        return jsonify({'ok': False, 'error': str(exc)}), 400
    q = (request.args.get('q') or '').strip()
    table, cond, cond_params = _entity_photo_filter(entity)
    filters = [
        'f.obrisana = FALSE',
        f'NOT EXISTS (SELECT 1 FROM {table} '
        f'WHERE {table}.fotografija_id = f.id AND {cond})',
    ]
    params = list(cond_params)
    if q.isdigit():
        filters.append('f.id = %s')
        params.append(int(q))
    elif q:
        filters.append(
            '(f.opis ILIKE %s OR f.original_ime ILIKE %s OR EXISTS ('
            'SELECT 1 FROM fotografija_tagovi t '
            'WHERE t.fotografija_id = f.id AND t.tag ILIKE %s))'
        )
        params.extend([f'%{q}%', f'%{q}%', f'%{q}%'])
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT f.id, f.opis, f.original_ime, f.status
                FROM fotografije f
                WHERE {' AND '.join(filters)}
                ORDER BY f.id DESC LIMIT 24
                """,
                params,
            )
            rows = _rows_to_dicts(cur, cur.fetchall())
    return jsonify({'ok': True, 'fotografije': [_photo_card(r) for r in rows]})


def handle_entitet_veza():
    """Link an existing photo to the entity (reverse direction). `entity` is
    already a valid `veza` dict, so it goes straight into `_insert_veza`."""
    try:
        entity = _parse_entity_ref(request.form)
    except ValueError as exc:
        return jsonify({'ok': False, 'error': str(exc)}), 400
    raw_id = (request.form.get('fotografija_id') or '').strip()
    if not raw_id.isdigit():
        return jsonify({'ok': False, 'error': 'Недостаје фотографија.'}), 400
    fotografija_id = int(raw_id)
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            photo = _fetch_photo(cur, fotografija_id)
            if not photo:
                return jsonify({'ok': False, 'error': 'Фотографија не постоји.'}), 404
            _insert_veza(cur, fotografija_id, entity)
    return jsonify({'ok': True})


def handle_entitet_ukloni():
    """Remove one entity<->photo link (non-destructive)."""
    try:
        entity = _parse_entity_ref(request.form)
    except ValueError as exc:
        return jsonify({'ok': False, 'error': str(exc)}), 400
    raw_id = (request.form.get('fotografija_id') or '').strip()
    if not raw_id.isdigit():
        return jsonify({'ok': False, 'error': 'Недостаје фотографија.'}), 400
    fotografija_id = int(raw_id)
    table, cond, params = _entity_photo_filter(entity)
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f'DELETE FROM {table} WHERE fotografija_id = %s AND {cond} RETURNING id',
                (fotografija_id, *params),
            )
            deleted = cur.fetchone()
    return jsonify({'ok': bool(deleted)})


# ---------------------------------------------------------------------------
# Samba import (admin): scan a mounted share, classify by filename convention,
# preview, then intake the same way as upload. Reuses image_matcher's per-
# collection inventory patterns. Admin-only (enforced by the route decorator).
# ---------------------------------------------------------------------------

IMPORT_BATCH_LIMIT = 500

_YEAR_RE = re.compile(r'(?:18|19|20)\d{2}')


def get_import_path() -> Path:
    return Path(os.environ.get('FOTOTEKA_IMPORT_PATH', './data/fototeka_import'))


def _safe_import_dir(subdir):
    """Resolve `subdir` under FOTOTEKA_IMPORT_PATH, refusing anything that
    escapes the root (path traversal). Returns a Path or None."""
    root = get_import_path().resolve()
    target = (root / (subdir or '')).resolve()
    if target != root and not str(target).startswith(str(root) + os.sep):
        return None
    return target


def _scan_import_files(directory):
    """Top-level image files in `directory`, sorted, capped at the batch limit."""
    files = sorted(
        p for p in directory.iterdir()
        if p.is_file() and p.suffix.lower() in ALLOWED_PHOTO_EXTENSIONS
    )
    return files[:IMPORT_BATCH_LIMIT]


def _extract_predmet_broj(filename, zbirka):
    """Reuse image_matcher's per-collection inventory pattern (not the loose
    generic fallback, so unmatched names fall to the reception queue). Strip
    the collection-letter prefix to leave the stored identifier (e.g. the
    mineral filename 'M-123' -> '123', matching the numeric DB value)."""
    cfg = image_matcher.ImageMatcher.INVENTORY_PATTERNS.get(zbirka)
    if not cfg:
        return None
    match = re.search(cfg['pattern'], Path(filename).stem, re.IGNORECASE)
    if not match:
        return None
    raw = match.group(1).strip().upper()
    core = re.sub(r'^[A-ZА-Я]+[-_\s]?', '', raw)
    return core or raw


def classify_import_filename(filename, default_zbirka):
    """Map a filename to an import outcome by convention:
    `TEREN_<godina>_<akcija>` -> field trip; a collection inventory number ->
    collection item; anything else -> reception queue for a curator."""
    stem = Path(filename).stem
    if stem.upper().startswith('TEREN_'):
        rest = stem[len('TEREN_'):]
        year = _YEAR_RE.search(rest)
        if year:
            godina = int(year.group(0))
            naziv = _YEAR_RE.sub(' ', rest)
            naziv = re.sub(r'[_\-]+', ' ', naziv).strip() or 'Терен'
            return {'klasa': 'teren',
                    'veza_meta': {'tip': 'teren', 'godina': godina, 'naziv': naziv},
                    'u_prijemnom_redu': False,
                    'note': f'Терен {godina} — {naziv}'}
        return {'klasa': 'prijemni_red', 'veza_meta': None,
                'u_prijemnom_redu': True,
                'note': 'Терен без године — пријемни ред'}
    broj = _extract_predmet_broj(filename, default_zbirka)
    if broj:
        label = get_zbirka_labels().get(default_zbirka, default_zbirka)
        return {'klasa': 'predmet',
                'veza_meta': {'tip': 'predmet', 'database_name': default_zbirka,
                              'inventarni_broj': broj},
                'u_prijemnom_redu': False,
                'note': f'Предмет — {label} {broj}'}
    return {'klasa': 'prijemni_red', 'veza_meta': None,
            'u_prijemnom_redu': True, 'note': 'Пријемни ред'}


def _resolve_import_veza(cur, veza_meta):
    """Turn a classification's veza_meta into a full `veza` for _insert_veza,
    creating the field-trip row if needed."""
    if not veza_meta:
        return None
    if veza_meta['tip'] == 'teren':
        teren_id = _get_or_create_teren(cur, veza_meta['godina'], veza_meta['naziv'])
        return {'tip': 'teren', 'teren_id': teren_id,
                'godina': veza_meta['godina'], 'naziv': veza_meta['naziv']}
    return veza_meta


def render_import_form():
    return render_template(
        'fototeka_import.html',
        zbirke=get_zbirka_labels(),
        root=str(get_import_path()),
        subdir='',
        zbirka='mineral',
        scanned=None,
    )


def handle_import_scan():
    """Dry run: classify every file under the chosen subdir and show a preview.
    No files are copied and nothing is written to the database."""
    subdir = (request.form.get('subdir') or '').strip()
    zbirka = (request.form.get('zbirka') or 'mineral').strip()
    if zbirka not in get_zbirka_labels():
        zbirka = 'mineral'
    directory = _safe_import_dir(subdir)
    if directory is None:
        flash('Неисправна путања за увоз.', 'danger')
        return redirect(url_for('fototeka.fototeka_import'))
    if not directory.is_dir():
        flash('Изабрани директоријум не постоји на дељеном диску.', 'warning')
        return redirect(url_for('fototeka.fototeka_import'))

    scanned = []
    for path in _scan_import_files(directory):
        result = classify_import_filename(path.name, zbirka)
        scanned.append({'ime': path.name, 'klasa': result['klasa'], 'note': result['note']})
    return render_template(
        'fototeka_import.html',
        zbirke=get_zbirka_labels(),
        root=str(get_import_path()),
        subdir=subdir,
        zbirka=zbirka,
        scanned=scanned,
    )


def handle_import_confirm():
    """Intake every file under the chosen subdir using the same pipeline as
    upload (poreklo='import'), applying the filename-convention link."""
    subdir = (request.form.get('subdir') or '').strip()
    zbirka = (request.form.get('zbirka') or 'mineral').strip()
    if zbirka not in get_zbirka_labels():
        zbirka = 'mineral'
    directory = _safe_import_dir(subdir)
    if directory is None or not directory.is_dir():
        flash('Неисправна путања за увоз.', 'danger')
        return redirect(url_for('fototeka.fototeka_import'))

    user_email = _session_email(session)
    temp_dir = fototeka_jobs.get_media_path() / 'temp'
    temp_dir.mkdir(parents=True, exist_ok=True)

    saved, skipped = 0, []
    for path in _scan_import_files(directory):
        file_size = path.stat().st_size
        if file_size <= 0:
            skipped.append(f'{path.name}: датотека је празна')
            continue
        if file_size > MAX_PHOTO_SIZE:
            skipped.append(f'{path.name}: већа од дозвољених 200 MB')
            continue
        result = classify_import_filename(path.name, zbirka)
        temp_path = temp_dir / f'{uuid.uuid4().hex}_{path.suffix.lstrip(".")}'
        try:
            shutil.copy2(path, temp_path)  # copy: the share original stays put
            with get_postgres_connection() as conn:
                with conn.cursor() as cur:
                    veza = _resolve_import_veza(cur, result['veza_meta'])
                    fotografija_id, reason = _intake_photo_from_path(
                        cur, temp_path, path.name, file_size, path.suffix.lower(),
                        autor_email=user_email, opis=None, tags=[],
                        datum_override=None, veza=veza,
                        u_prijemnom_redu=result['u_prijemnom_redu'], poreklo='import',
                    )
            if fotografija_id:
                saved += 1
            elif reason:
                skipped.append(reason)
        finally:
            if temp_path.exists():
                temp_path.unlink()

    if saved:
        flash(f'Увезено фотографија: {saved}. Умањени прикази се обрађују у позадини.', 'success')
    if not saved and not skipped:
        flash('Нема датотека за увоз у изабраном директоријуму.', 'info')
    for reason in skipped[:20]:
        flash(reason, 'warning')
    return redirect(url_for('fototeka.fototeka_galerija'))
