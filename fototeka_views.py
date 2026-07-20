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
import logging
import mimetypes
import os
import re
import shutil
import tempfile
import uuid
import zipfile
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote

from flask import (
    Response,
    abort,
    after_this_request,
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


logger = logging.getLogger(__name__)


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

# Short, uppercase format labels for the gallery thumbnail badge. RAW and any
# other extension fall through to a bare uppercase of the extension.
_FORMAT_LABELS = {
    '.jpg': 'JPG', '.jpeg': 'JPG', '.jpe': 'JPG', '.jfif': 'JPG',
    '.tif': 'TIFF', '.tiff': 'TIFF',
    '.png': 'PNG', '.webp': 'WEBP', '.bmp': 'BMP', '.gif': 'GIF',
}


def _format_label(ekstenzija) -> str:
    ext = (ekstenzija or '').strip().lower()
    if ext in _FORMAT_LABELS:
        return _FORMAT_LABELS[ext]
    return ext.lstrip('.').upper() or '—'

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
    """Metadata/links: the author, admins, the director and department heads.
    A department head may edit only photos they are allowed to *see* — a
    private photo of another author stays off-limits (its GET page is 403, and
    a direct POST must not be able to mutate it either)."""
    if _session_is_admin(session_data) or _session_is_director(session_data):
        return True
    autor = (photo.get('autor_email') or '').strip().lower()
    user_email = _session_email(session_data)
    if bool(user_email) and user_email == autor:
        return True
    if bool(session_data.get('is_department_head', False)):
        return can_view_photo(session_data, photo)
    return False


def can_view_photo(session_data, photo) -> bool:
    """Access control: 'javno' photos are visible to every logged-in employee;
    'privatno' only to the author, plus admins and the director (supervision).
    A missing value is treated as 'javno' (legacy-safe)."""
    if (photo.get('vidljivost') or 'javno') == 'javno':
        return True
    if _session_is_admin(session_data) or _session_is_director(session_data):
        return True
    autor = (photo.get('autor_email') or '').strip().lower()
    user_email = _session_email(session_data)
    return bool(user_email) and user_email == autor


def can_change_visibility(session_data, photo) -> bool:
    """Only the author and admins/the director may change a photo's visibility
    (department heads may edit metadata but not flip visibility)."""
    if _session_is_admin(session_data) or _session_is_director(session_data):
        return True
    autor = (photo.get('autor_email') or '').strip().lower()
    user_email = _session_email(session_data)
    return bool(user_email) and user_email == autor


def _visibility_filter(session_data, alias='f'):
    """Return (sql_clause, params) restricting a list query to photos the
    caller may see. Admins/the director see everything (no restriction)."""
    if _session_is_admin(session_data) or _session_is_director(session_data):
        return None, []
    return (
        f"({alias}.vidljivost = %s OR LOWER({alias}.autor_email) = %s)",
        ['javno', _session_email(session_data)],
    )


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


def _parse_vidljivost(form):
    """Read the visibility choice; anything but an explicit 'privatno' is
    treated as the default 'javno'."""
    return 'privatno' if (form.get('vidljivost') or 'javno').strip() == 'privatno' else 'javno'


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


def _get_or_create_teren(cur, godina, naziv, created_by_email=None):
    """created_by_email=None -> iz sesije (UI tok); headless uvoz ga prosleđuje
    eksplicitno jer van HTTP zahteva nema sesije."""
    if created_by_email is None:
        created_by_email = _session_email(session)
    cur.execute(
        """
        INSERT INTO fototeka_tereni (godina, naziv, created_by_email)
        VALUES (%s, %s, %s)
        ON CONFLICT (godina, naziv) DO UPDATE SET naziv = EXCLUDED.naziv
        RETURNING id
        """,
        (godina, naziv, created_by_email),
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
            if not teren_id_raw.isdigit():
                raise ValueError('Изабрани терен није исправан.')
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
            if not projekat_id_raw.isdigit():
                raise ValueError('Изабрани пројекат није исправан.')
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
            if not izlozba_id_raw.isdigit():
                raise ValueError('Изабрана изложба није исправна.')
            cur.execute('SELECT id FROM exhibitions WHERE id = %s', (int(izlozba_id_raw),))
            row = cur.fetchone()
            if not row:
                raise ValueError('Изабрана изложба не постоји.')
            return {'tip': 'izlozba', 'izlozba_id': _scalar(row, 'id')}
        naziv = ' '.join((form.get('veza_izlozba_naziv') or '').split())
        if not naziv:
            raise ValueError('Изаберите изложбу или унесите назив нове.')
        # Get-or-create by title. The sequential upload sends N per-file
        # requests carrying the same new-exhibition name; without this, each
        # request would INSERT its own row (exhibitions.title has no UNIQUE),
        # leaving N duplicate exhibitions. Reusing an existing same-titled row
        # keeps one exhibition per name. (teren/projekat already get-or-create.)
        cur.execute(
            'SELECT id FROM exhibitions WHERE title = %s ORDER BY id LIMIT 1',
            (naziv,),
        )
        existing = cur.fetchone()
        if existing:
            return {'tip': 'izlozba', 'izlozba_id': _scalar(existing, 'id')}
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
               vidljivost, fixity_proveren_at, fixity_ok, created_at, updated_at
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

GALLERY_SORT_COLUMNS = {
    'upload': 'f.created_at',
    'snimak': 'COALESCE(f.datum_snimanja, f.created_at::date)',
    'naziv': 'lower(f.original_ime)',
    'autor': 'lower(f.autor_email)',
}


def render_galerija():
    q = (request.args.get('q') or '').strip()
    tag = (request.args.get('tag') or '').strip()
    autor = (request.args.get('autor') or '').strip().lower()
    godina_raw = (request.args.get('godina') or '').strip()
    veza = (request.args.get('veza') or '').strip()
    sort = (request.args.get('sort') or 'snimak').strip()
    if sort not in GALLERY_SORT_COLUMNS:
        sort = 'snimak'
    smer = 'asc' if (request.args.get('smer') or 'desc').strip().lower() == 'asc' else 'desc'
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
        filters.append(
            'f.sklonjena_sa_reda = FALSE AND (' + bez_ijedne_veze_sql('f') + ')')

    # server-side access control: hide others' private photos
    vis_clause, vis_params = _visibility_filter(session, 'f')
    if vis_clause:
        filters.append(vis_clause)
        params.extend(vis_params)

    where_sql = ' AND '.join(filters)
    offset = (page - 1) * GALLERY_PAGE_SIZE

    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f'SELECT COUNT(*) AS total FROM fotografije f WHERE {where_sql}',
                params,
            )
            total = _scalar(cur.fetchone(), 'total') or 0
            # sort/smer come from a fixed whitelist, never interpolated raw.
            order_sql = f'{GALLERY_SORT_COLUMNS[sort]} {smer.upper()} NULLS LAST, f.id DESC'
            cur.execute(
                f"""
                SELECT f.id, f.original_ime, f.opis, f.status, f.autor_email,
                       f.datum_snimanja, f.u_prijemnom_redu, f.created_at,
                       f.ekstenzija, f.velicina_bajtova
                FROM fotografije f
                WHERE {where_sql}
                ORDER BY {order_sql}
                LIMIT %s OFFSET %s
                """,
                params + [GALLERY_PAGE_SIZE, offset],
            )
            photos = _rows_to_dicts(cur, cur.fetchall())
            for photo in photos:
                photo['format_label'] = _format_label(photo.get('ekstenzija'))

            # Facets must be drawn from the SAME visible set as the list, or a
            # private photo's author/tag leaks to users who can't see the photo.
            vis_autor_clause, vis_autor_params = _visibility_filter(session, 'fotografije')
            cur.execute(
                f"""
                SELECT DISTINCT autor_email FROM fotografije
                WHERE obrisana = FALSE
                  {('AND ' + vis_autor_clause) if vis_autor_clause else ''}
                ORDER BY autor_email
                """,
                vis_autor_params,
            )
            autori = [_scalar(row, 'autor_email') for row in
                      _rows_to_dicts(cur, cur.fetchall())]
            vis_tag_clause, vis_tag_params = _visibility_filter(session, 'f')
            cur.execute(
                f"""
                SELECT DISTINCT t.tag FROM fotografija_tagovi t
                JOIN fotografije f ON f.id = t.fotografija_id
                WHERE f.obrisana = FALSE
                  {('AND ' + vis_tag_clause) if vis_tag_clause else ''}
                ORDER BY t.tag LIMIT 200
                """,
                vis_tag_params,
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
        sort=sort, smer=smer,
        autori=autori,
        tagovi=tagovi,
        tereni=tereni,
        projekti=projekti,
        izlozbe=izlozbe,
        zbirke=get_zbirka_labels(),
        status_labels=PHOTO_STATUS_LABELS,
        zip_max_bytes=ZIP_MAX_TOTAL_BYTES,
        zip_max_count=DOWNLOAD_ZIP_MAX,
    )


# ---------------------------------------------------------------------------
# Reception queue (пријемни ред)
# ---------------------------------------------------------------------------

# Prijemni red se IZVODI iz stanja, ne iz zastavice. Zastavica
# `u_prijemnom_redu` je umela da laze: stari uvoz ju je postavljao na FALSE za
# svako ime koje je LICILO na inventarni broj, pa i kad predmet ne postoji —
# takve fotografije su ostajale nevidljive kustosu. Veze ne lazu.
#
# JEDAN IZVOR ISTINE za "je li fotografija ikako povezana": OVDE se nabrajaju
# SVE veze-tabele. Nova veza-tabela (npr. foto_veza_kr_dosije za K-R dosije)
# MORA biti dodata i ovde, inace slike unete izvan UI-ja (CLI: uvezi-kr-dosije)
# pogresno ispadaju kao sirocad iako su u bazi uredno vezane. (test_prijemni_red)
_BEZ_IJEDNE_VEZE_SQL = """
    NOT EXISTS (SELECT 1 FROM foto_veza_predmet v WHERE v.fotografija_id = {alias}.id)
    AND NOT EXISTS (SELECT 1 FROM foto_veza_teren t WHERE t.fotografija_id = {alias}.id)
    AND NOT EXISTS (SELECT 1 FROM foto_veza_projekat p WHERE p.fotografija_id = {alias}.id)
    AND NOT EXISTS (SELECT 1 FROM foto_veza_izlozba i WHERE i.fotografija_id = {alias}.id)
    AND NOT EXISTS (SELECT 1 FROM foto_veza_kr_dosije k WHERE k.fotografija_id = {alias}.id)
"""


def bez_ijedne_veze_sql(alias='fotografije'):
    return _BEZ_IJEDNE_VEZE_SQL.format(alias=alias)


def render_prijemni_red():
    """Every photo with NO link at all — regardless of how it got there (batch
    import, retroactive relink, plain upload) — oldest first. Derived from the
    links themselves, not from a flag that could lie; a photo leaves the queue
    the moment a link is added, or when a curator deliberately clears it."""
    vis_clause, vis_params = _visibility_filter(session, 'fotografije')
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT id, original_ime, opis, status, autor_email,
                       datum_snimanja, created_at
                FROM fotografije
                WHERE obrisana = FALSE
                  AND sklonjena_sa_reda = FALSE
                  AND {bez_ijedne_veze_sql('fotografije')}
                  {('AND ' + vis_clause) if vis_clause else ''}
                ORDER BY created_at ASC, id ASC
                """,
                vis_params,
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
                UPDATE fotografije
                SET sklonjena_sa_reda = TRUE, u_prijemnom_redu = FALSE,
                    updated_at = now()
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


def _has_raw_container_signature(head: bytes) -> bool:
    """True if the leading bytes look like an accepted archival RAW / TIFF /
    ISO-BMFF container. Camera RAW is mostly TIFF-based (II*\\0 / MM\\0*); a few
    vendors use their own magic. A file matching none of these is not a valid
    archival original and must not be archived as-is (arbitrary content renamed
    to .cr2). This is a signature gate, not a full RAW parse."""
    tiff_or_raw = (
        b'II\x2a\x00',   # little-endian TIFF: CR2/NEF/NRW/ARW/SR2/SRF/DNG/PEF/SRW/3FR/IIQ/RWL
        b'MM\x00\x2a',   # big-endian TIFF
        b'II\x55\x00',   # Panasonic RW2 / .RAW
        b'IIRO', b'IIRS', b'MMOR',  # Olympus ORF variants
        b'FUJIFILM',     # Fujifilm RAF
        b'FOVb',         # Sigma X3F (Foveon)
    )
    if any(head.startswith(sig) for sig in tiff_or_raw):
        return True
    # ISO base media file format (Canon CR3): size(4 bytes) + 'ftyp' + brand
    if len(head) >= 12 and head[4:8] == b'ftyp':
        return True
    return False


def _read_file_head(path, n: int = 16) -> bytes:
    with open(path, 'rb') as handle:
        return handle.read(n)


def _place_raw_exclusive(temp_path, raw_full):
    """Install temp_path at raw_full WITHOUT ever overwriting an existing file.

    O_EXCL claims the archive path atomically; if anything is already there (a
    hash collision, or a leftover from an earlier crashed attempt) it raises
    FileExistsError instead of silently replacing a write-once original. The
    bytes are streamed in (works even when temp and archive live on different
    filesystems, unlike os.rename), fsynced, and only then is the temp file
    removed. On any write error the partial file we just created is removed."""
    raw_full.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(raw_full), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, 'wb') as dst, open(temp_path, 'rb') as src:
            shutil.copyfileobj(src, dst, length=1024 * 1024)
            dst.flush()
            os.fsync(dst.fileno())
    except BaseException:
        Path(raw_full).unlink(missing_ok=True)
        raise
    os.unlink(temp_path)


def _intake_photo_from_path(cur, temp_path, original_ime, file_size, ext, *,
                            autor_email, opis, tags, datum_override, veza,
                            u_prijemnom_redu, poreklo, vidljivost='javno'):
    """Core intake shared by upload and Samba import. Validates the image,
    dedups by sha256, places the RAW original by origin (write-once, exclusive
    create — a collision is refused, never an overwrite), inserts the row with
    tags + link and enqueues the derivative job. On success temp_path is
    consumed; on dedup/invalid it is left for the caller to clean up. If any DB
    step fails after the file is placed, exactly that file is removed so a
    rolled-back transaction leaves no orphan. Returns (fotografija_id, None) or
    (None, skip_reason)."""
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
        # Camera RAW / archival original: PIL can't open it. Validate the
        # container signature so arbitrary content merely renamed to a RAW
        # extension is refused rather than silently archived forever (deletes
        # are soft — the RAW file always stays). The worker still marks it
        # 'bez_derivata' if libvips can't build a preview.
        if not _has_raw_container_signature(_read_file_head(temp_path)):
            return None, (f'{original_ime}: садржај није препознат као исправан '
                          f'RAW/архивски формат')
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
    # Place the RAW first, exclusively: a collision (leftover orphan or a
    # concurrent upload of the same content) is refused here, never overwritten.
    try:
        _place_raw_exclusive(temp_path, raw_full)
    except FileExistsError:
        return None, (f'{original_ime}: идентична датотека већ постоји у '
                      f'архиви (није преписана)')

    # The RAW is now ours. If any DB step fails, remove exactly this file so the
    # rolled-back transaction leaves no orphan in the write-once archive.
    try:
        cur.execute(
            """
            INSERT INTO fotografije
                (sha256, raw_putanja, original_ime, ekstenzija,
                 velicina_bajtova, width, height, autor_email,
                 datum_snimanja, exif, opis, poreklo, u_prijemnom_redu, vidljivost)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (sha256, raw_rel, original_ime, ext, file_size,
             exif_info['width'], exif_info['height'], autor_email,
             datum_snimanja, json.dumps(exif_info['exif']), opis, poreklo,
             u_prijemnom_redu, vidljivost),
        )
        fotografija_id = _scalar(cur.fetchone(), 'id')
        _replace_tags(cur, fotografija_id, tags)
        _insert_veza(cur, fotografija_id, veza)
        fototeka_jobs.enqueue_job(cur, fotografija_id, 'derivati')
    except BaseException:
        Path(raw_full).unlink(missing_ok=True)
        raise
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
                        vidljivost=_parse_vidljivost(request.form),
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
                    vidljivost=_parse_vidljivost(request.form),
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
        # per-process temp name + guaranteed cleanup (same rationale as the
        # worker's make_derivatives — no shared .tmp_<sha> collision/leftover)
        temp_out = final_path.with_name(f'.tmp_{os.getpid()}_{final_path.name}')
        try:
            with Image.open(source_path) as img:
                img = img.convert('RGB')
                dims = {'width': img.width, 'height': img.height}
                img.thumbnail((size, size), Image.Resampling.LANCZOS)
                img.save(temp_out, format='JPEG', quality=85, optimize=True)
            os.replace(temp_out, final_path)
        finally:
            if temp_out.exists():
                temp_out.unlink()
    return dims


# A preview may be attached only to a photo that has no valid auto-derivative;
# never to a 'spremna' one (that would silently overwrite the derivative built
# from the RAW original with unrelated content, which fixity of the RAW cannot
# detect).
PREVIEW_ATTACHABLE_STATUSES = {'bez_derivata', 'greska'}


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
                if photo['status'] not in PREVIEW_ATTACHABLE_STATUSES:
                    flash('Преглед се може приложити само фотографији без '
                          'умањеног приказа.', 'warning')
                    return redirect(url_for('fototeka.fototeka_fotografija',
                                            fotografija_id=fotografija_id))
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
            if not can_view_photo(session, photo):
                abort(403)
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
    # Only offer the original download when the archival file genuinely exists;
    # label it "RAW" only for actual camera RAW originals.
    ima_original = _archival_original_path(photo) is not None
    original_je_raw = (photo.get('ekstenzija') or '').lower() in ARCHIVAL_RAW_EXTENSIONS
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
        moze_menjati_vidljivost=can_change_visibility(session, photo),
        ima_original=ima_original,
        original_je_raw=original_je_raw,
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


def handle_promeni_vidljivost(fotografija_id):
    """Flip a photo between 'javno' and 'privatno'. The author and admins/the
    director may do this (department heads may not)."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            photo = _fetch_photo(cur, fotografija_id)
            if not photo:
                abort(404)
            if not can_change_visibility(session, photo):
                abort(403)
            vidljivost = _parse_vidljivost(request.form)
            cur.execute(
                """
                UPDATE fotografije SET vidljivost = %s, updated_at = now()
                WHERE id = %s
                """,
                (vidljivost, fotografija_id),
            )
    flash('Видљивост фотографије је ажурирана.', 'success')
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
    # Audit trail: removing a link is non-destructive to the file but is lost
    # curation work, so record who did it.
    logger.info('Fototeka veza uklonjena: foto=%s tip=%s veza_id=%s by=%s',
                fotografija_id, tip, veza_id, _session_email(session))
    flash('Веза је уклоњена.', 'success')
    return redirect(url_for('fototeka.fototeka_fotografija', fotografija_id=fotografija_id))


def handle_ponovi_obradu(fotografija_id):
    """Re-enqueue the derivative job after a failed processing run. Only a photo
    that actually needs (re)processing qualifies — reprocessing a 'spremna' one
    is not an offered action and would needlessly rebuild a good derivative."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            photo = _fetch_photo(cur, fotografija_id)
            if not photo:
                abort(404)
            if not can_edit_photo(session, photo):
                abort(403)
            if photo['status'] not in ('greska', 'bez_derivata'):
                flash('Обрада се може поновити само за фотографију у грешци '
                      'или без умањеног приказа.', 'warning')
                return redirect(url_for('fototeka.fototeka_fotografija',
                                        fotografija_id=fotografija_id))
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


def _archival_original_path(photo):
    """Resolved path to the archival original IF it really exists under the
    archive root, else None. Never assume the file is there — check disk."""
    if not photo or not photo.get('raw_putanja'):
        return None
    arhiva_root = fototeka_jobs.get_arhiva_path().resolve()
    full_path = (arhiva_root / photo['raw_putanja']).resolve()
    if not str(full_path).startswith(str(arhiva_root) + os.sep):
        return None
    return full_path if full_path.is_file() else None


def _derivative_path(photo, kind):
    """Resolved path to a derivative IF the photo is ready and the file exists,
    else None."""
    if not photo or photo.get('status') != 'spremna':
        return None
    media_root = fototeka_jobs.get_media_path().resolve()
    full_path = (media_root / fototeka_jobs.derivative_relative_path(
        (photo['sha256'] or '').strip(), kind)).resolve()
    if not str(full_path).startswith(str(media_root) + os.sep):
        return None
    return full_path if full_path.is_file() else None


# Interne nginx putanje za X-Accel-Redirect. Flask ovde SAMO proveri prava pa
# vrati ovaj header s praznim telom; nginx (interna `location`) sam isporuci
# fajl sa /data/mis/media odnosno /data/arhiva, oslobadjajuci gunicorn worker.
XACCEL_DERIVAT_PREFIX = '/_zasticeno/derivati/'
XACCEL_RAW_PREFIX = '/_zasticeno/raw/'


def _xaccel_enabled():
    """X-Accel isporuka je iza prekidača da bi deploy bio bezbedan PRE nego što
    se nginx ručno podesi na produkciji. Isključeno (default) = send_file."""
    return os.environ.get('FOTOTEKA_XACCEL', '').strip().lower() in ('1', 'true', 'yes', 'on')


def _xaccel_uri(prefix, full_path, root):
    """Interni URI iz VEĆ razrešene i proverene putanje, ne iz sirove vrednosti iz
    baze. nginx normalizuje `..` PRE poklapanja `location`, pa bi sirov segment
    ispao iz interne lokacije i razišao se sa onim što send_file posluži."""
    return prefix + full_path.relative_to(root).as_posix()


def _xaccel_response(internal_uri, *, mimetype, download_name=None):
    """Prazan odgovor koji transfer fajla prepušta nginx-u preko X-Accel-Redirect.
    Prava su već proverena uzvodno — nginx samo strimuje fajl iz `internal`
    lokacije. URI se URL-enkoduje jer ga nginx interno dekodira."""
    response = Response(b'', mimetype=mimetype)
    response.headers['X-Accel-Redirect'] = quote(internal_uri, safe='/')
    if download_name:
        ascii_fallback = download_name.encode('ascii', 'ignore').decode() or 'download'
        response.headers['Content-Disposition'] = (
            "attachment; filename=\"%s\"; filename*=UTF-8''%s"
            % (ascii_fallback, quote(download_name))
        )
    return response


def serve_derivat(fotografija_id, kind):
    if kind not in ('jpg', 'thumb'):
        abort(404)
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            photo = _fetch_photo(cur, fotografija_id)
    if not photo:
        abort(404)
    # server-side access control on the file route itself — a direct URL to
    # someone else's private photo is 403, not merely hidden in the UI
    if not can_view_photo(session, photo):
        abort(403)
    if photo['status'] != 'spremna':
        return _send_placeholder(kind)
    sha = photo['sha256'].strip()
    rel_path = fototeka_jobs.derivative_relative_path(sha, kind)
    media_root = fototeka_jobs.get_media_path().resolve()
    full_path = (media_root / rel_path).resolve()
    if not str(full_path).startswith(str(media_root) + os.sep):
        abort(404)
    if not full_path.is_file():
        return _send_placeholder(kind)
    if _xaccel_enabled():
        response = _xaccel_response(
            _xaccel_uri(XACCEL_DERIVAT_PREFIX, full_path, media_root),
            mimetype='image/jpeg',
        )
    else:
        response = send_file(full_path, mimetype='image/jpeg')
    _apply_private_cache_headers(response, photo)
    return response


def _apply_private_cache_headers(response, photo):
    """These files sit behind login + per-photo access control, so a shared
    cache must NEVER store them. A private photo additionally gets `no-store`
    so a later javno→privatno flip takes effect immediately (the URL is a pure
    function of sha256 and never changes)."""
    is_private = (photo.get('vidljivost') or 'javno') == 'privatno'
    response.headers['Cache-Control'] = (
        'private, no-store' if is_private else 'private, max-age=3600'
    )
    response.headers['Vary'] = 'Cookie'
    return response


def serve_raw(fotografija_id):
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            photo = _fetch_photo(cur, fotografija_id)
    if not photo:
        abort(404)
    if not can_view_photo(session, photo):
        abort(403)
    full_path = _archival_original_path(photo)
    if full_path is None:
        abort(404)
    download_name = photo['original_ime'] or full_path.name
    if _xaccel_enabled():
        mimetype = mimetypes.guess_type(download_name)[0] or 'application/octet-stream'
        response = _xaccel_response(
            _xaccel_uri(XACCEL_RAW_PREFIX, full_path, fototeka_jobs.get_arhiva_path().resolve()),
            mimetype=mimetype,
            download_name=download_name,
        )
    else:
        response = send_file(
            full_path,
            as_attachment=True,
            download_name=download_name,
            max_age=0,
        )
    _apply_private_cache_headers(response, photo)
    return response


DOWNLOAD_ZIP_MAX = 300
# Cap the whole archive by bytes, not just by file count: 300 archival
# originals of up to 200 MB each would be ~58 GB, enough to fill the temp disk
# and hang the (single, sync) gunicorn worker. The build stops once this budget
# would be exceeded and notes the truncation.
ZIP_MAX_TOTAL_BYTES = 2 * 1024 * 1024 * 1024  # 2 GB


def _unique_zip_name(base, photo_id, used):
    base = Path(base or '').name or f'foto_{photo_id}'
    if base not in used:
        used.add(base)
        return base
    name = f'{Path(base).stem}_{photo_id}{Path(base).suffix}'
    used.add(name)
    return name


def handle_preuzmi_zip():
    """Stream a ZIP of the selected photos, either the derivative JPG (default)
    or the archival original. The archive is built to a temp file on disk (not
    memory), so large originals never blow up RAM."""
    raw_ids = request.form.getlist('ids') or (request.form.get('ids') or '').split(',')
    ids, seen = [], set()
    for value in raw_ids:
        value = str(value).strip()
        if value.isdigit() and int(value) not in seen:
            seen.add(int(value))
            ids.append(int(value))
    if not ids:
        flash('Изаберите бар једну фотографију.', 'warning')
        return redirect(url_for('fototeka.fototeka_galerija'))
    capped = len(ids) > DOWNLOAD_ZIP_MAX
    ids = ids[:DOWNLOAD_ZIP_MAX]
    sloj = 'original' if (request.form.get('sloj') or 'jpg').strip() == 'original' else 'jpg'

    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, sha256, raw_putanja, original_ime, ekstenzija, status,
                       vidljivost, autor_email
                FROM fotografije
                WHERE obrisana = FALSE AND id = ANY(%s)
                """,
                (ids,),
            )
            photos = _rows_to_dicts(cur, cur.fetchall())

    # server-side access control: refuse the whole request if any selected
    # photo is another user's private one (a forged/direct request, since the
    # UI never shows those to this user)
    for photo in photos:
        if not can_view_photo(session, photo):
            abort(403)

    # Build to a temp file on the data partition (media/temp), never the
    # default /tmp — on this host /tmp is tmpfs (RAM), so a big archive there
    # would eat memory rather than disk.
    temp_root = fototeka_jobs.get_media_path() / 'temp'
    temp_root.mkdir(parents=True, exist_ok=True)
    tmp = tempfile.NamedTemporaryFile(prefix='fototeka_', suffix='.zip',
                                      delete=False, dir=str(temp_root))
    tmp_path = Path(tmp.name)
    tmp.close()
    used_names, added, total_bytes, byte_capped = set(), 0, 0, False
    try:
        with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_STORED, allowZip64=True) as zf:
            for photo in photos:
                if sloj == 'original':
                    src = _archival_original_path(photo)
                    base = photo['original_ime'] or f"foto_{photo['id']}{photo.get('ekstenzija') or ''}"
                else:
                    src = _derivative_path(photo, 'jpg')
                    if src is not None:
                        base = f"{Path(photo['original_ime'] or ('foto_' + str(photo['id']))).stem}.jpg"
                    else:
                        # no derivative (RAW/bez_derivata) — fall back to the original
                        src = _archival_original_path(photo)
                        base = photo['original_ime'] or f"foto_{photo['id']}{photo.get('ekstenzija') or ''}"
                if src is None:
                    continue
                try:
                    size = os.path.getsize(src)
                except OSError:
                    continue
                # keep at least one file, then stop before the running total
                # would exceed the archive byte budget
                if added > 0 and total_bytes + size > ZIP_MAX_TOTAL_BYTES:
                    byte_capped = True
                    break
                zf.write(src, arcname=_unique_zip_name(base, photo['id'], used_names))
                total_bytes += size
                added += 1
            notes = []
            if capped:
                notes.append(
                    f'Изабрано је више од {DOWNLOAD_ZIP_MAX} фотографија; '
                    f'преузето је првих {DOWNLOAD_ZIP_MAX}.')
            if byte_capped:
                notes.append(
                    f'Укупна величина је премашила лимит преузимања '
                    f'({ZIP_MAX_TOTAL_BYTES // (1024 * 1024)} MB); '
                    f'архива садржи првих {added} датотека.')
            if notes:
                zf.writestr('NAPOMENA.txt', ('\n'.join(notes) + '\n').encode('utf-8'))
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise

    if added == 0:
        tmp_path.unlink(missing_ok=True)
        flash('Изабране фотографије немају датотеке за преузимање.', 'warning')
        return redirect(url_for('fototeka.fototeka_galerija'))

    @after_this_request
    def _cleanup(response):
        tmp_path.unlink(missing_ok=True)
        return response

    return send_file(
        tmp_path,
        mimetype='application/zip',
        as_attachment=True,
        download_name='fototeka.zip',
        max_age=0,
    )


# ---------------------------------------------------------------------------
# Autocomplete APIs
# ---------------------------------------------------------------------------

def api_tagovi():
    q = (request.args.get('q') or '').strip()
    # Only suggest tags that live on photos the caller may see and that are not
    # deleted — otherwise a private photo's tag leaks through autocomplete.
    vis_clause, vis_params = _visibility_filter(session, 'f')
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT DISTINCT t.tag FROM fotografija_tagovi t
                JOIN fotografije f ON f.id = t.fotografija_id
                WHERE f.obrisana = FALSE AND t.tag ILIKE %s
                  {('AND ' + vis_clause) if vis_clause else ''}
                ORDER BY t.tag LIMIT 15
                """,
                [f'%{q}%', *vis_params],
            )
            tags = [_scalar(row, 'tag') for row in _rows_to_dicts(cur, cur.fetchall())]
    return jsonify(tags)


def api_predmeti():
    """Inventory-number autocomplete. Phase 1 covers the mineral collection
    (the only one whose items live in PostgreSQL); for other collections the
    inventory number is typed in freely."""
    from flask import current_app

    zbirka = (request.args.get('zbirka') or '').strip()
    q = (request.args.get('q') or '').strip()
    if zbirka != 'mineral' or len(q) < 1:
        return jsonify([])
    # The mineral database has its own, narrower access control than the
    # Фototeka module (which every employee has). Don't let this autocomplete
    # enumerate mineral inventory numbers/names for users who may not open it.
    access_checker = getattr(current_app, 'user_has_module_access', None)
    if access_checker is not None and not access_checker(
            session.get('user_email', ''), session.get('user_role', ''),
            'mineral_database'):
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
    vis_clause, vis_params = _visibility_filter(session, 'f')
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT f.id, f.opis, f.original_ime, f.status
                FROM fotografije f
                JOIN {table} ON {table}.fotografija_id = f.id
                WHERE f.obrisana = FALSE AND {cond}
                  {('AND ' + vis_clause) if vis_clause else ''}
                ORDER BY f.id DESC
                """,
                list(params) + vis_params,
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
    vis_clause, vis_params = _visibility_filter(session, 'f')
    if vis_clause:
        filters.append(vis_clause)
        params.extend(vis_params)
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
    already a valid `veza` dict, so it goes straight into `_insert_veza`.
    Requires that the caller may actually *see* the photo — otherwise a forged
    POST with a guessed id could link (and thereby confirm the existence of)
    another user's private photo. A 404 (not 403) avoids leaking existence."""
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
            if not photo or not can_view_photo(session, photo):
                return jsonify({'ok': False, 'error': 'Фотографија не постоји.'}), 404
            _insert_veza(cur, fotografija_id, entity)
            # linking is a curation step: a queued photo leaves the reception
            # queue here too, mirroring handle_dodaj_vezu.
            if photo['u_prijemnom_redu']:
                cur.execute(
                    """
                    UPDATE fotografije SET u_prijemnom_redu = FALSE, updated_at = now()
                    WHERE id = %s
                    """,
                    (fotografija_id,),
                )
    return jsonify({'ok': True})


def handle_entitet_ukloni():
    """Remove one entity<->photo link (non-destructive). Loads the photo first
    and requires view access, so a guessed id cannot touch another user's
    private photo (a 404, not 403, avoids leaking existence)."""
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
            photo = _fetch_photo(cur, fotografija_id)
            if not photo or not can_view_photo(session, photo):
                return jsonify({'ok': False, 'error': 'Фотографија не постоји.'}), 404
            cur.execute(
                f'DELETE FROM {table} WHERE fotografija_id = %s AND {cond} RETURNING id',
                (fotografija_id, *params),
            )
            deleted = cur.fetchone()
    if deleted:
        logger.info('Fototeka entitet-veza uklonjena: foto=%s entitet=%s by=%s',
                    fotografija_id, entity.get('tip'), _session_email(session))
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


def _scan_import_files(directory, offset=0):
    """Sorted top-level image files in `directory`, returned as
    (total_count, page) where page is the slice [offset : offset+BATCH]. The
    import copies files (it never moves them off the share), so without an
    advancing offset a directory holding more than one batch could never be
    fully imported — every run would re-scan the same first N and dedup them.
    The caller advances `offset` batch by batch."""
    files = sorted(
        p for p in directory.iterdir()
        if p.is_file() and p.suffix.lower() in ALLOWED_PHOTO_EXTENSIONS
    )
    offset = max(0, offset)
    return len(files), files[offset:offset + IMPORT_BATCH_LIMIT]


def _parse_offset(form):
    raw = (form.get('offset') or '0').strip()
    return int(raw) if raw.isdigit() else 0


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
        # Fleksibilno: 'M 028' == 'M-28' == '028' == '28'. Postojanje predmeta se
        # proverava kasnije (nadji_predmet) — broj koji ne postoji u zbirci ide
        # BEZ VEZE, ne u tihu vezu u prazno.
        broj = normalizuj_inv_broj(broj) or broj
        label = get_zbirka_labels().get(default_zbirka, default_zbirka)
        return {'klasa': 'predmet',
                'veza_meta': {'tip': 'predmet', 'database_name': default_zbirka,
                              'inventarni_broj': broj},
                'u_prijemnom_redu': False,
                'note': f'Предмет — {label} {broj}'}
    return {'klasa': 'prijemni_red', 'veza_meta': None,
            'u_prijemnom_redu': True, 'note': 'Пријемни ред'}


def _resolve_import_veza(cur, veza_meta, created_by_email=None):
    """Turn a classification's veza_meta into a full `veza` for _insert_veza,
    creating the field-trip row if needed."""
    if not veza_meta:
        return None
    if veza_meta['tip'] == 'teren':
        teren_id = _get_or_create_teren(
            cur, veza_meta['godina'], veza_meta['naziv'],
            created_by_email=created_by_email)
        return {'tip': 'teren', 'teren_id': teren_id,
                'godina': veza_meta['godina'], 'naziv': veza_meta['naziv']}
    return veza_meta


def _uvoz_istorija(limit=10):
    """Poslednji batch uvozi (za istoriju na ekranu)."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, pokrenut_at, izvor, pokrenuo_email, ukupno,
                       uvezeno, duplikata, neuspesno, u_prijemni_red,
                       vezano_predmet, vezano_teren, bez_veze
                FROM fototeka_uvoz_run
                ORDER BY id DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()
    polja = ('id', 'pokrenut_at', 'izvor', 'pokrenuo_email', 'ukupno',
             'uvezeno', 'duplikata', 'neuspesno', 'u_prijemni_red',
             'vezano_predmet', 'vezano_teren', 'bez_veze')
    rezultat = []
    for row in rows:
        if isinstance(row, dict):
            rezultat.append({polje: row.get(polje) for polje in polja})
        else:
            rezultat.append(dict(zip(polja, row)))
    return rezultat


def render_import_form(rezime=None, zbirka='mineral'):
    return render_template(
        'fototeka_import.html',
        zbirke=get_zbirka_labels(),
        root=str(get_import_path()),
        zbirka=zbirka,
        rezime=rezime,
        istorija=_uvoz_istorija(),
    )


def handle_import_scan():
    """Podrazumevani korak: dry-run preko CELOG ulaza — klasifikacija i
    predikcija ishoda po fajlu, bez ijednog upisa. Kustos vidi brojeve pa
    tek onda potvrđuje."""
    zbirka = (request.form.get('zbirka') or 'mineral').strip()
    if zbirka not in get_zbirka_labels():
        zbirka = 'mineral'
    rezime = run_batch_import(dry_run=True, default_zbirka=zbirka)
    return render_import_form(rezime=rezime, zbirka=zbirka)


def handle_import_confirm():
    """Stvarni uvoz celog ulaza (posle dry-run pregleda): intake kroz isti
    tok kao upload (poreklo='import'), premeštanje originala po ishodu i
    trajni zapis u fototeka_uvoz_run/stavka."""
    zbirka = (request.form.get('zbirka') or 'mineral').strip()
    if zbirka not in get_zbirka_labels():
        zbirka = 'mineral'
    rezime = run_batch_import(
        dry_run=False, default_zbirka=zbirka,
        izvor='ui', pokrenuo_email=_session_email(session),
    )
    if rezime['uvezeno']:
        flash(
            f"Увезено фотографија: {rezime['uvezeno']} — "
            f"везано за предмет: {rezime['po_klasi'].get('predmet', 0)}, "
            f"терен: {rezime['po_klasi'].get('teren', 0)}, "
            f"БЕЗ ВЕЗЕ: {rezime['po_klasi'].get('prijemni_red', 0)} "
            f"(чекају у пријемном реду). "
            f"Умањени прикази се обрађују у позадини.", 'success')
    if rezime['po_klasi'].get('prijemni_red'):
        flash(
            f"{rezime['po_klasi']['prijemni_red']} фотографија НИЈЕ везано ни за "
            f"један предмет — отворите Пријемни ред да их повежете.", 'warning')
    if rezime['duplikata']:
        flash(f"Прескочено дупликата: {rezime['duplikata']} "
              f"(премештени у obradjeno/duplikati).", 'info')
    if rezime['neuspesno']:
        flash(f"Неуспешно: {rezime['neuspesno']} (premešteno u neuspesno/).", 'warning')
    if not rezime['ukupno']:
        flash('Улазни фолдер је празан — нема датотека за увоз.', 'info')
    return redirect(url_for('fototeka.fototeka_import'))



# ---------------------------------------------------------------------------
# Batch uvoz sa mrežnog (Samba) foldera — headless engine.
#
# Raspored na share-u: /<ulaz>/<korisnicki-folder>/*.tif — ime foldera je
# lokalni deo email adrese kustosa (autorstvo). Fajl se posle uspešnog uvoza
# PREMEŠTA u obradjeno/<YYYY-MM>/ unutar korisnikovog foldera; duplikat u
# obradjeno/duplikati/; neispravan u neuspesno/. Dry-run ne piše ništa
# (ni u bazu ni po disku) — vraća samo klasifikaciju i predikciju ishoda.
# ---------------------------------------------------------------------------

IMPORT_SKIP_DIRS = frozenset({'obradjeno', 'neuspesno'})

_INSTITUTION_PREFIX_RE = re.compile(r'^(?:PMB|ПМБ)[-_\s]+', re.IGNORECASE)
_FILENAME_DATE_RE = re.compile(r'(?:^|[_\-])((?:19|20)\d{2})-(\d{2})-(\d{2})(?:[_\-.]|$)')


def _strip_institution_prefix(stem):
    """Konvencija toleriše institucijski prefiks (PMB-M-01234 == M-01234)."""
    return _INSTITUTION_PREFIX_RE.sub('', stem)


def datum_iz_imena(filename):
    """`<INV>_<YYYY-MM-DD>_<NN>` — datum iz imena kao fallback kad nema EXIF-a."""
    match = _FILENAME_DATE_RE.search(Path(filename).stem)
    if not match:
        return None
    try:
        return datetime(int(match.group(1)), int(match.group(2)),
                        int(match.group(3))).date()
    except ValueError:
        return None


def autor_iz_foldera(cur, folder_name):
    """Ime korisničkog foldera na share-u = lokalni deo email adrese u MIS-u.
    Vraća email ili None (nepoznat/dvosmislen folder)."""
    if not folder_name:
        return None
    cur.execute(
        """
        SELECT email FROM users
        WHERE is_active = TRUE
          AND LOWER(SPLIT_PART(email, '@', 1)) = LOWER(%s)
        """,
        (folder_name,),
    )
    rows = cur.fetchall()
    if len(rows) != 1:
        return None
    return _scalar(rows[0], 'email')


def _premesti_original(path, odrediste_dir):
    """Premesti fajl sa share-a u odredišni folder, bez prepisivanja: pri
    koliziji imena dodaje brojčani sufiks. Vraća novu putanju."""
    odrediste_dir.mkdir(parents=True, exist_ok=True)
    target = odrediste_dir / path.name
    counter = 1
    while target.exists():
        target = odrediste_dir / f'{path.stem}__{counter}{path.suffix}'
        counter += 1
    shutil.move(str(path), str(target))
    return target


def _uvoz_folderi(root):
    """Korisnički podfolderi ulaza (sortirano) + koren za fajlove van foldera."""
    if not root.is_dir():
        return []
    folders = sorted(
        p for p in root.iterdir()
        if p.is_dir() and p.name.lower() not in IMPORT_SKIP_DIRS
    )
    return [root] + folders


def _uvoz_fajlovi(directory):
    return sorted(
        p for p in directory.iterdir()
        if p.is_file() and p.suffix.lower() in ALLOWED_PHOTO_EXTENSIONS
    )


def _sha256_postoji(cur, path):
    """Pre-check duplikata direktno sa share-a (bez kopiranja): vraća
    (sha256, postojeći_id ili None)."""
    sha256 = fototeka_jobs.sha256_of_file(path)
    cur.execute('SELECT id FROM fotografije WHERE sha256 = %s', (sha256,))
    row = cur.fetchone()
    return sha256, (_scalar(row, 'id') if row else None)


def run_batch_import(*, dry_run=True, default_zbirka='mineral',
                     fallback_autor_email='fototeka@nhmbeo.rs',
                     izvor='cli', pokrenuo_email=None):
    """Prođe kroz SVE korisničke foldere ulaza i uveze fajlove po konvenciji.

    dry_run=True: nula upisa (baza i disk netaknuti) — vraća predikciju po
    fajlu. dry_run=False: intake kroz _intake_photo_from_path (dedup,
    write-once RAW, red za derivate), premeštanje originala po ishodu i upis
    u fototeka_uvoz_run/stavka.

    Vraća rezime: {'ukupno', 'uvezeno', 'duplikata', 'neuspesno',
    'u_prijemni_red', 'po_klasi': {...}, 'stavke': [...], 'run_id'}.
    """
    root = get_import_path()
    stavke = []
    brojaci = {'ukupno': 0, 'uvezeno': 0, 'duplikata': 0, 'neuspesno': 0,
               'u_prijemni_red': 0}
    po_klasi = {'predmet': 0, 'teren': 0, 'prijemni_red': 0}

    temp_dir = fototeka_jobs.get_media_path() / 'temp'
    if not dry_run:
        temp_dir.mkdir(parents=True, exist_ok=True)

    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            autori = {}
            for folder in _uvoz_folderi(root):
                folder_name = folder.name if folder != root else ''
                if folder_name and folder_name not in autori:
                    autori[folder_name] = autor_iz_foldera(cur, folder_name)

    for folder in _uvoz_folderi(root):
        folder_name = folder.name if folder != root else ''
        for path in _uvoz_fajlovi(folder):
            brojaci['ukupno'] += 1
            stavka = {'datoteka': path.name, 'folder': folder_name,
                      'ishod': None, 'klasa': None, 'fotografija_id': None,
                      'poruka': None}
            stavke.append(stavka)

            file_size = path.stat().st_size
            if file_size <= 0 or file_size > MAX_PHOTO_SIZE:
                stavka['ishod'] = 'neuspesno'
                stavka['poruka'] = ('датотека је празна' if file_size <= 0
                                    else 'већа од дозвољених 200 MB')
                brojaci['neuspesno'] += 1
                if not dry_run:
                    _premesti_original(path, folder / 'neuspesno')
                continue

            klasifikovano = classify_import_filename(
                _strip_institution_prefix(path.name), default_zbirka)

            with get_postgres_connection() as conn:
                with conn.cursor() as cur:
                    # Predmet se veze SAMO ako stvarno postoji u zbirci. Broj koji
                    # ne postoji (ili je dvosmislen) NIJE vezan predmet — ide u
                    # prijemni red i vidi se u izvestaju kao BEZ VEZE.
                    if klasifikovano['klasa'] == 'predmet':
                        trazeni = klasifikovano['veza_meta']['inventarni_broj']
                        nadjen, status = nadji_predmet(cur, default_zbirka, trazeni)
                        if status == 'ok':
                            klasifikovano['veza_meta']['inventarni_broj'] = nadjen
                        elif status == 'neprovereno':
                            klasifikovano['note'] += ' (постојање предмета није проверено)'
                        else:
                            razlog = ('инв. бр. %s не постоји у збирци' % trazeni
                                      if status == 'nema'
                                      else 'инв. бр. %s је двосмислен (више предмета)' % trazeni)
                            klasifikovano = {
                                'klasa': 'prijemni_red',
                                'veza_meta': None,
                                'u_prijemnom_redu': True,
                                'note': f'БЕЗ ВЕЗЕ — {razlog}',
                            }

                    stavka['klasa'] = klasifikovano['klasa']
                    stavka['poruka'] = klasifikovano['note']
                    po_klasi[klasifikovano['klasa']] = po_klasi.get(klasifikovano['klasa'], 0) + 1

                    sha256, postojeci_id = _sha256_postoji(cur, path)
                    if postojeci_id:
                        stavka['ishod'] = 'duplikat'
                        stavka['fotografija_id'] = postojeci_id
                        stavka['poruka'] = f'идентична фотографија већ постоји (бр. {postojeci_id})'
                        brojaci['duplikata'] += 1
                        po_klasi[klasifikovano['klasa']] -= 1
                        if not dry_run:
                            _premesti_original(path, folder / 'obradjeno' / 'duplikati')
                        continue

                    if dry_run:
                        stavka['ishod'] = 'uvezeno'
                        if klasifikovano['u_prijemnom_redu']:
                            brojaci['u_prijemni_red'] += 1
                        brojaci['uvezeno'] += 1
                        continue

                    autor = autori.get(folder_name) or fallback_autor_email
                    tags = [] if autori.get(folder_name) else ['uvoz-nepoznat-autor']
                    temp_path = temp_dir / f'{uuid.uuid4().hex}_{path.suffix.lstrip(".")}'
                    try:
                        shutil.copy2(path, temp_path)
                        veza = _resolve_import_veza(
                            cur, klasifikovano['veza_meta'],
                            created_by_email=autor)
                        fotografija_id, reason = _intake_photo_from_path(
                            cur, temp_path, path.name, file_size,
                            path.suffix.lower(), autor_email=autor, opis=None,
                            tags=tags,
                            datum_override=datum_iz_imena(path.name),
                            veza=veza,
                            u_prijemnom_redu=klasifikovano['u_prijemnom_redu'],
                            poreklo='import',
                        )
                    except Exception as greska:  # jedan fajl ne obara ceo uvoz
                        fotografija_id, reason = None, f'neočekivana greška: {greska}'
                    finally:
                        if temp_path.exists():
                            temp_path.unlink()

            if dry_run:
                continue
            if fotografija_id:
                stavka['ishod'] = 'uvezeno'
                stavka['fotografija_id'] = fotografija_id
                brojaci['uvezeno'] += 1
                if klasifikovano['u_prijemnom_redu']:
                    brojaci['u_prijemni_red'] += 1
                mesec = datetime.now().strftime('%Y-%m')
                _premesti_original(path, folder / 'obradjeno' / mesec)
            elif reason and 'идентичн' in reason:
                stavka['ishod'] = 'duplikat'
                stavka['poruka'] = reason
                brojaci['duplikata'] += 1
                _premesti_original(path, folder / 'obradjeno' / 'duplikati')
            else:
                stavka['ishod'] = 'neuspesno'
                stavka['poruka'] = reason or 'непозната грешка'
                brojaci['neuspesno'] += 1
                if reason and reason.startswith('neočekivana greška'):
                    pass  # prolazna greška (baza/disk): fajl ostaje za sledeći run
                else:
                    _premesti_original(path, folder / 'neuspesno')

    run_id = None
    if not dry_run:
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO fototeka_uvoz_run
                        (zavrsen_at, izvor, pokrenuo_email, ukupno, uvezeno,
                         duplikata, neuspesno, u_prijemni_red,
                         vezano_predmet, vezano_teren, bez_veze)
                    VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (izvor, pokrenuo_email, brojaci['ukupno'],
                     brojaci['uvezeno'], brojaci['duplikata'],
                     brojaci['neuspesno'], brojaci['u_prijemni_red'],
                     po_klasi.get('predmet', 0), po_klasi.get('teren', 0),
                     po_klasi.get('prijemni_red', 0)),
                )
                run_id = _scalar(cur.fetchone(), 'id')
                for stavka in stavke:
                    cur.execute(
                        """
                        INSERT INTO fototeka_uvoz_stavka
                            (run_id, datoteka, korisnicki_folder, ishod,
                             klasa, fotografija_id, poruka)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (run_id, stavka['datoteka'], stavka['folder'] or None,
                         stavka['ishod'], stavka['klasa'],
                         stavka['fotografija_id'], stavka['poruka']),
                    )

    return {**brojaci, 'po_klasi': po_klasi, 'stavke': stavke, 'run_id': run_id}


# ---------------------------------------------------------------------------
# Thumbnail glavne fotografije za liste predmeta (tabela zbirke).
#
# JEDAN batch upit za celu stranu (bez N+1): za skup inventarnih brojeva vrati
# {inv_broj -> fotografija_id} glavne fotografije. "Glavna" = najstarija
# (najmanji id) — ista konvencija koju vec koristi collection_media_views za
# sliku predmeta, pa tabela i detalj pokazuju istu fotografiju.
#
# Vidljivost se filtrira SERVERSKI (_visibility_filter): tudja privatna
# fotografija se ne vraca, pa predmet u tabeli izgleda kao da je bez slike.
# ---------------------------------------------------------------------------

def glavne_fotografije_predmeta(session_data, database_name, inventarni_brojevi):
    """Mapa {inventarni_broj: fotografija_id} glavnih fotografija predmeta.

    Prazan ulaz -> prazna mapa (bez upita). Racuna se samo na fotografije koje
    su 'spremna' (derivat postoji) i nisu obrisane.
    """
    brojevi = [str(broj).strip() for broj in (inventarni_brojevi or []) if str(broj or '').strip()]
    if not brojevi:
        return {}

    vis_clause, vis_params = _visibility_filter(session_data, 'f')
    sql = """
        SELECT DISTINCT ON (v.inventarni_broj) v.inventarni_broj, f.id
        FROM foto_veza_predmet v
        JOIN fotografije f ON f.id = v.fotografija_id
        WHERE v.database_name = %s
          AND v.inventarni_broj = ANY(%s)
          AND f.obrisana = FALSE
          AND f.status = 'spremna'
    """
    params = [database_name, brojevi]
    if vis_clause:
        sql += f' AND {vis_clause}'
        params.extend(vis_params)
    sql += ' ORDER BY v.inventarni_broj, f.id'

    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            redovi = cur.fetchall()

    mapa = {}
    for red in redovi:
        broj = red['inventarni_broj'] if isinstance(red, dict) else red[0]
        foto_id = red['id'] if isinstance(red, dict) else red[1]
        mapa[str(broj)] = foto_id
    return mapa


# ---------------------------------------------------------------------------
# Fleksibilno prepoznavanje inventarskih brojeva iz imena datoteke.
#
# Kustosi imenuju fajlove kako im je pri ruci: 'M 028.JPG', 'M-28.jpg',
# 'M028.jpg', 'PMB-M-01234.tif'. U bazi je inventarni broj nekonzistentan i sa
# druge strane: pretezno cist broj bez nula ('28', '3359'), ali ima i zapisa sa
# slovnom oznakom ('M4301') i sa vodecom nulom. Zato se NE poredi sirov tekst
# nego NORMALIZOVAN oblik sa obe strane:
#   veliko slovo -> skini slovnu oznaku zbirke -> skini razdvajac -> skini
#   vodece nule.  'M 028' == 'M-28' == 'M028' == '028' == '28'
#
# Kljucno (uzrok buga u run-u 71): fotografija se veze SAMO ako predmet sa tim
# brojem stvarno postoji. Broj koji ne postoji u zbirci vise nije "vezan
# predmet" (tiha veza u prazno) nego BEZ VEZE -> pijemni red, vidljivo u
# izvestaju.
# ---------------------------------------------------------------------------

# Zbirke cije predmete umemo da proverimo u PostgreSQL-u: zbirka -> (tabela, kolona).
# Za zbirke van ove mape postojanje se NE proverava (status 'neprovereno').
PREDMET_TABELE = {
    'mineral': ('minerals', 'inventory_number'),
}

_INV_PREFIX_RE = re.compile(r'^[A-ZА-ЯЂЈЉЊЋЖЧШЏ]+[-_\s]*', re.IGNORECASE)


def normalizuj_inv_broj(raw):
    """'M 028' / 'M-28' / 'M028' / '028' / 28  ->  '28'.

    Skida slovnu oznaku zbirke, razdvajac i vodece nule. Broj koji je sav od
    nula ostaje '0'. Vraca '' ako od ulaza ne ostane nista upotrebljivo.
    """
    tekst = str(raw or '').strip().upper()
    if not tekst:
        return ''
    # Skidaj slovne oznake dok ih ima: 'PMB-M-01234' -> 'M-01234' -> '01234'
    # (institucijski prefiks + oznaka zbirke mogu da stoje jedan za drugim).
    while True:
        skraceno = _INV_PREFIX_RE.sub('', tekst, count=1)
        if skraceno == tekst or not skraceno:
            break
        tekst = skraceno
    tekst = tekst.replace(' ', '').replace('-', '').replace('_', '')
    if not tekst:
        return ''
    if tekst.isdigit():
        return tekst.lstrip('0') or '0'
    return tekst


def nadji_predmet(cur, zbirka, broj):
    """Pronadji predmet po fleksibilno uparenom inventarnom broju.

    Vraca (inventarni_broj_iz_baze, status) gde je status:
      'ok'           — tacno jedan predmet (koristi se njegov zapis iz baze),
      'nema'         — nijedan predmet sa tim brojem (fotografija ide BEZ VEZE),
      'dvosmisleno'  — vise predmeta se normalizuje na isti broj (covek odlucuje),
      'neprovereno'  — zbirka nije u PREDMET_TABELE, ne umemo da proverimo.
    """
    kljuc = normalizuj_inv_broj(broj)
    if not kljuc:
        return None, 'nema'

    tabela_kolona = PREDMET_TABELE.get(zbirka)
    if not tabela_kolona:
        return broj, 'neprovereno'

    tabela, kolona = tabela_kolona
    # Normalizacija u SQL-u mora da preslika Python normalizuj_inv_broj():
    # veliko slovo -> skini slovni prefiks i razdvajac -> skini vodece nule.
    cur.execute(
        f"""
        SELECT {kolona}
        FROM {tabela}
        WHERE {kolona} IS NOT NULL
          AND ltrim(
                regexp_replace(upper(btrim({kolona})), '^[A-ZА-Я]+[-_ ]*', ''),
                '0'
              ) = %s
        LIMIT 2
        """,
        (kljuc,),
    )
    redovi = cur.fetchall()
    if not redovi:
        return None, 'nema'
    if len(redovi) > 1:
        return None, 'dvosmisleno'
    red = redovi[0]
    return (red[kolona] if isinstance(red, dict) else red[0]), 'ok'


# ---------------------------------------------------------------------------
# Grupno uredjivanje izabranih fotografija (batch edit).
#
# Posle uvoza od 100+ fotografija kustos ih je morao uredjivati jednu po jednu.
# Ovde se ista logika (tagovi, opis, vidljivost, veza) primenjuje na skup, uz
# provere PO SVAKOJ STAVCI na serveru — UI nikad nije jedina brana. Fotografija
# koju korisnik ne sme da menja se PRESKACE (broji se i prijavljuje), nikad ne
# obara ceo posao.
# ---------------------------------------------------------------------------

BATCH_MAX = 500

TAG_AKCIJE = ('dodaj', 'zameni', 'ukloni')
OPIS_AKCIJE = ('postavi', 'dopisi')


def _audit_upisi(cur, fotografija_id, akcija, izmene, korisnik_id):
    """Trag u opšti `audit_log` (tabela postoji od db/schema.sql)."""
    cur.execute(
        """
        INSERT INTO audit_log (table_name, record_id, action, new_values, performed_by)
        VALUES ('fotografije', %s, %s, %s, %s)
        """,
        (fotografija_id, akcija, json.dumps(izmene, ensure_ascii=False), korisnik_id),
    )


def _tagovi_fotografije(cur, fotografija_id):
    cur.execute(
        'SELECT tag FROM fotografija_tagovi WHERE fotografija_id = %s',
        (fotografija_id,),
    )
    return [(red['tag'] if isinstance(red, dict) else red[0]) for red in cur.fetchall()]


def primeni_batch_izmenu(cur, session_data, photo, akcije):
    """Primeni tražene akcije na JEDNU fotografiju. Vraća dict izmena (za audit).

    Poziva se tek pošto je can_edit_photo prošao — ovde se ne proverava pravo.
    """
    izmene = {}

    tag_akcija = akcije.get('tag_akcija')
    tagovi = akcije.get('tagovi') or []
    if tag_akcija and tagovi:
        postojeci = _tagovi_fotografije(cur, photo['id'])
        if tag_akcija == 'zameni':
            novi = list(tagovi)
        elif tag_akcija == 'dodaj':
            novi = list(postojeci)
            for tag in tagovi:
                if tag.casefold() not in {t.casefold() for t in novi}:
                    novi.append(tag)
        elif tag_akcija == 'ukloni':
            za_uklanjanje = {t.casefold() for t in tagovi}
            novi = [t for t in postojeci if t.casefold() not in za_uklanjanje]
        else:
            novi = postojeci
        if sorted(novi) != sorted(postojeci):
            _replace_tags(cur, photo['id'], novi)
            izmene['tagovi'] = {'akcija': tag_akcija, 'pre': postojeci, 'posle': novi}

    opis_akcija = akcije.get('opis_akcija')
    opis = (akcije.get('opis') or '').strip()
    if opis_akcija and opis:
        stari = (photo.get('opis') or '').strip()
        if opis_akcija == 'dopisi':
            novi_opis = (stari + '\n' + opis).strip() if stari else opis
        else:
            novi_opis = opis
        if novi_opis != stari:
            cur.execute(
                'UPDATE fotografije SET opis = %s, updated_at = now() WHERE id = %s',
                (novi_opis, photo['id']),
            )
            izmene['opis'] = {'akcija': opis_akcija, 'posle': novi_opis}

    vidljivost = akcije.get('vidljivost')
    if vidljivost in ('javno', 'privatno') and vidljivost != photo.get('vidljivost'):
        if can_change_visibility(session_data, photo):
            cur.execute(
                'UPDATE fotografije SET vidljivost = %s, updated_at = now() WHERE id = %s',
                (vidljivost, photo['id']),
            )
            izmene['vidljivost'] = {'pre': photo.get('vidljivost'), 'posle': vidljivost}

    veza = akcije.get('veza')
    if veza:
        _insert_veza(cur, photo['id'], veza)
        izmene['veza'] = {k: v for k, v in veza.items() if k != 'tip'} | {'tip': veza['tip']}

    autor = (akcije.get('autor_email') or '').strip().lower()
    if autor and _session_is_admin(session_data):   # samo admin sme autora
        if autor != (photo.get('autor_email') or '').lower():
            cur.execute(
                'UPDATE fotografije SET autor_email = %s, updated_at = now() WHERE id = %s',
                (autor, photo['id']),
            )
            izmene['autor_email'] = {'pre': photo.get('autor_email'), 'posle': autor}

    return izmene


def handle_batch_edit():
    """Grupna izmena izabranih fotografija iz galerije.

    Prava se proveravaju PO STAVCI (can_edit_photo); fotografije koje korisnik
    ne sme da menja se preskaču i prijavljuju. Autora sme da menja samo admin.
    """
    ids_raw = request.form.getlist('ids')
    ids = [int(x) for x in ids_raw if str(x).strip().isdigit()][:BATCH_MAX]
    if not ids:
        flash('Није изабрана ниједна фотографија.', 'warning')
        return redirect(request.referrer or url_for('fototeka.fototeka_galerija'))

    tag_akcija = (request.form.get('tag_akcija') or '').strip()
    opis_akcija = (request.form.get('opis_akcija') or '').strip()
    akcije = {
        'tag_akcija': tag_akcija if tag_akcija in TAG_AKCIJE else None,
        'tagovi': _parse_tags(request.form.get('tagovi') or ''),
        'opis_akcija': opis_akcija if opis_akcija in OPIS_AKCIJE else None,
        'opis': request.form.get('opis') or '',
        'vidljivost': (request.form.get('vidljivost') or '').strip() or None,
        'autor_email': request.form.get('autor_email') or '',
    }

    izmenjeno, preskoceno, bez_promene = 0, 0, 0
    korisnik_id = session.get('user_id')

    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            try:
                akcije['veza'] = _parse_veza_form(request.form, cur)
            except ValueError as greska:
                flash(str(greska), 'danger')
                return redirect(request.referrer or url_for('fototeka.fototeka_galerija'))

            for fotografija_id in ids:
                photo = _fetch_photo(cur, fotografija_id)
                if not photo:
                    preskoceno += 1
                    continue
                # SERVERSKA provera po svakoj stavci — UI nije brana.
                if not can_edit_photo(session, photo):
                    preskoceno += 1
                    continue
                izmene = primeni_batch_izmenu(cur, session, photo, akcije)
                if izmene:
                    _audit_upisi(cur, fotografija_id, 'BATCH_EDIT', izmene, korisnik_id)
                    izmenjeno += 1
                else:
                    bez_promene += 1

    if izmenjeno:
        flash(f'Измењено фотографија: {izmenjeno}.', 'success')
    if bez_promene:
        flash(f'Без промене (већ су такве): {bez_promene}.', 'info')
    if preskoceno:
        flash(
            f'Прескочено: {preskoceno} — немате право измене над њима '
            f'(туђе приватне фотографије).', 'warning')
    if not izmenjeno and not preskoceno and not bez_promene:
        flash('Ништа није промењено — ниједна акција није изабрана.', 'info')

    return redirect(request.referrer or url_for('fototeka.fototeka_galerija'))
