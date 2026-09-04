"""Глобална претрага (Ctrl+K): једно поље, резултати из свих база на које
пријављени корисник има приступ, груписани по бази.

Правила:
- упит 2–80 знакова; % и _ се третирају као обичан текст (ILIKE, подразумевани
  ESCAPE је \\); упит се тражи и у другом писму (ћирилица <-> латиница), јер су
  подаци у базама мешовито уписани;
- свака база даје највише NAJVISE резултата; пад упита једне базе не руши
  остале (група се прескаче и бележи у лог);
- приступ: исти модули као у навигацији (user_has_module_access), за
  збирке преко museum_qr.korisnik_ima_pristup; приватне фотографије само
  аутору (као у галерији Фототеке).
"""
import logging

from flask import session, url_for

import museum_qr
from postgres_service import get_postgres_connection

logger = logging.getLogger(__name__)

NAJVISE = 6
NAJMANJE_ZNAKOVA = 2
NAJVISE_ZNAKOVA = 80


def _app():
    import app as museum_app
    return museum_app


def _v(red, i, kljuc):
    return red[kljuc] if isinstance(red, dict) else red[i]


def _ima_modul(modul):
    if 'user_id' not in session:
        return False
    return bool(_app().user_has_module_access(
        session.get('user_email', ''), session.get('user_role', 'user'), modul))


def normalizuj_upit(q):
    """Обрезан упит или None ако је прекратак; предугачак се сече."""
    q = ' '.join(str(q or '').split())[:NAJVISE_ZNAKOVA]
    return q if len(q) >= NAJMANJE_ZNAKOVA else None


def sablon(q):
    """ILIKE шаблон са ескејпованим % и _ (подразумевани ESCAPE '\\')."""
    return '%' + q.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_') + '%'


_CIR_LAT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'ђ': 'đ', 'е': 'e', 'ж': 'ž',
    'з': 'z', 'и': 'i', 'ј': 'j', 'к': 'k', 'л': 'l', 'љ': 'lj', 'м': 'm', 'н': 'n',
    'њ': 'nj', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'ћ': 'ć', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'č', 'џ': 'dž', 'ш': 'š',
}
_LAT_CIR = {v: k for k, v in _CIR_LAT.items()}
_LAT_DVOJNI = ('lj', 'nj', 'dž')


def u_latinicu(q):
    return ''.join(_CIR_LAT.get(z, _CIR_LAT.get(z.lower(), z).upper() if z.isupper() else z) for z in q)


def u_cirilicu(q):
    out, i, s = [], 0, q.lower()
    while i < len(s):
        dv = s[i:i + 2]
        if dv in _LAT_DVOJNI:
            out.append(_LAT_CIR[dv]); i += 2
        else:
            out.append(_LAT_CIR.get(s[i], s[i])); i += 1
    return ''.join(out)


def varijante(q):
    """Упит и његови преписи у друго писмо (без дупликата, ILIKE је неосетљив на величину слова)."""
    v = [q]
    for k in (u_latinicu(q), u_cirilicu(q)):
        if k.lower() not in [x.lower() for x in v]:
            v.append(k)
    return v


def sabloni(q):
    return [sablon(v) for v in varijante(q)]


def _minerali(cur, s):
    cur.execute(
        """SELECT id, inventory_number, item_name, card_locality, storage_location
           FROM minerals
           WHERE inventory_number ILIKE ANY(%s) OR item_name ILIKE ANY(%s)
              OR card_locality ILIKE ANY(%s)
           ORDER BY (inventory_number ILIKE ANY(%s)) DESC, id
           LIMIT %s""", (s, s, s, s, NAJVISE))
    st = []
    for r in cur.fetchall():
        inv = _v(r, 1, 'inventory_number') or ''
        st.append({'naslov': ' · '.join(x for x in ('M' + str(inv) if inv else '', _v(r, 2, 'item_name') or '') if x),
                   'opis': ' · '.join(x for x in (_v(r, 3, 'card_locality') or '',
                                                    ('смештај ' + str(_v(r, 4, 'storage_location'))) if _v(r, 4, 'storage_location') else '') if x),
                   'url': museum_qr.url_detalja('minerals', _v(r, 0, 'id'))})
    return st


def _meteoriti(cur, s):
    cur.execute(
        """SELECT id, catalog_number, specimen_name, meteorite_class, fall_location
           FROM meteorite_specimens
           WHERE catalog_number ILIKE ANY(%s) OR specimen_name ILIKE ANY(%s)
              OR fall_location ILIKE ANY(%s)
           ORDER BY id LIMIT %s""", (s, s, s, NAJVISE))
    return [{'naslov': ' · '.join(x for x in (_v(r, 1, 'catalog_number') or '', _v(r, 2, 'specimen_name') or '') if x),
             'opis': ' · '.join(x for x in (_v(r, 3, 'meteorite_class') or '', _v(r, 4, 'fall_location') or '') if x),
             'url': museum_qr.url_detalja('meteorite', _v(r, 0, 'id'))} for r in cur.fetchall()]


def _zbirke(cur, s):
    """collection_specimens — све збирке заједно, свака ставка носи назив збирке;
    приступ се проверава по збирци."""
    cur.execute(
        """SELECT id, collection_type, catalog_number, scientific_name, common_name_sr, location_found
           FROM collection_specimens
           WHERE catalog_number ILIKE ANY(%s) OR scientific_name ILIKE ANY(%s)
              OR common_name_sr ILIKE ANY(%s) OR location_found ILIKE ANY(%s)
           ORDER BY collection_type, id LIMIT %s""", (s, s, s, s, NAJVISE * 4))
    st = []
    dozvola = {}
    for r in cur.fetchall():
        tip = _v(r, 1, 'collection_type')
        if tip not in dozvola:
            try:
                dozvola[tip] = museum_qr.korisnik_ima_pristup(tip)
            except Exception:  # noqa: BLE001 - непозната збирка = нема приступа
                dozvola[tip] = False
        if not dozvola[tip]:
            continue
        try:
            url = museum_qr.url_detalja(tip, _v(r, 0, 'id'))
            naziv = museum_qr.naziv_zbirke(tip)
        except Exception:  # noqa: BLE001
            continue
        st.append({'naslov': ' · '.join(x for x in (_v(r, 2, 'catalog_number') or '', _v(r, 3, 'scientific_name') or _v(r, 4, 'common_name_sr') or '') if x),
                   'opis': ' · '.join(x for x in (naziv, _v(r, 5, 'location_found') or '') if x),
                   'url': url})
        if len(st) >= NAJVISE:
            break
    return st


def _zaposleni(cur, s):
    cur.execute(
        """SELECT u.full_name, u.email, u.position, d.name
           FROM users u LEFT JOIN departments d ON d.id = u.department_id
           WHERE u.is_active = TRUE AND (u.full_name ILIKE ANY(%s) OR u.email ILIKE ANY(%s)
                 OR u.position ILIKE ANY(%s))
           ORDER BY u.full_name LIMIT %s""", (s, s, s, NAJVISE))
    return [{'naslov': _v(r, 0, 'full_name') or _v(r, 1, 'email'),
             'opis': ' · '.join(x for x in (_v(r, 2, 'position') or '', _v(r, 3, 'name') or '', _v(r, 1, 'email') or '') if x),
             'url': url_for('employees_database') + '?q=' + _q(_v(r, 0, 'full_name') or _v(r, 1, 'email'))}
            for r in cur.fetchall()]


def _knjige(cur, s):
    cur.execute(
        """SELECT id, title, author, publication_year, location
           FROM library_books
           WHERE title ILIKE ANY(%s) OR author ILIKE ANY(%s) OR isbn ILIKE ANY(%s)
           ORDER BY title LIMIT %s""", (s, s, s, NAJVISE))
    return [{'naslov': _v(r, 1, 'title') or '',
             'opis': ' · '.join(str(x) for x in (_v(r, 2, 'author') or '', _v(r, 3, 'publication_year') or '', _v(r, 4, 'location') or '') if x),
             'url': url_for('library_database') + '?q=' + _q(_v(r, 1, 'title') or '')}
            for r in cur.fetchall()]


def _kr_dosijei(cur, s):
    cur.execute(
        """SELECT id, evidencioni_broj, naziv_predmeta, odeljenje, inventarni_broj
           FROM kr_dosije
           WHERE evidencioni_broj ILIKE ANY(%s) OR naziv_predmeta ILIKE ANY(%s)
              OR inventarni_broj ILIKE ANY(%s)
           ORDER BY id DESC LIMIT %s""", (s, s, s, NAJVISE))
    return [{'naslov': ' · '.join(x for x in (_v(r, 1, 'evidencioni_broj') or '', _v(r, 2, 'naziv_predmeta') or '') if x),
             'opis': ' · '.join(x for x in (_v(r, 3, 'odeljenje') or '', ('инв. ' + _v(r, 4, 'inventarni_broj')) if _v(r, 4, 'inventarni_broj') else '') if x),
             'url': url_for('kr_dosije.detalj', dosije_id=_v(r, 0, 'id'))} for r in cur.fetchall()]


def _fotografije(cur, s):
    email = (session.get('user_email') or '').strip().lower()
    cur.execute(
        """SELECT id, original_ime, opis, autor_email, datum_snimanja
           FROM fotografije
           WHERE obrisana = FALSE AND (vidljivost = 'javno' OR LOWER(autor_email) = %s)
             AND (original_ime ILIKE ANY(%s) OR opis ILIKE ANY(%s))
           ORDER BY id DESC LIMIT %s""", (email, s, s, NAJVISE))
    return [{'naslov': _v(r, 1, 'original_ime') or ('Фотографија %s' % _v(r, 0, 'id')),
             'opis': ' · '.join(str(x) for x in ((_v(r, 2, 'opis') or '')[:80], _v(r, 3, 'autor_email') or '', _v(r, 4, 'datum_snimanja') or '') if x),
             'url': url_for('fototeka.fototeka_fotografija', fotografija_id=_v(r, 0, 'id'))} for r in cur.fetchall()]


def _dokumenti(cur, s):
    cur.execute(
        """SELECT id, title, category, department
           FROM documents
           WHERE is_active = TRUE AND (title ILIKE ANY(%s) OR description ILIKE ANY(%s))
           ORDER BY id DESC LIMIT %s""", (s, s, NAJVISE))
    return [{'naslov': _v(r, 1, 'title') or '',
             'opis': ' · '.join(x for x in (_v(r, 2, 'category') or '', _v(r, 3, 'department') or '') if x),
             'url': url_for('documents.dokumenti_detalj', document_id=_v(r, 0, 'id'))} for r in cur.fetchall()]


def _prstenovanje(cur, s):
    cur.execute(
        """SELECT r.id, r.ring_number, bs.species_name, r.location, r.event_date
           FROM bird_ringing_records r LEFT JOIN bird_species bs ON bs.id = r.species_id
           WHERE r.ring_number ILIKE ANY(%s)
           ORDER BY r.id DESC LIMIT %s""", (s, NAJVISE))
    return [{'naslov': ' · '.join(x for x in (_v(r, 1, 'ring_number') or '', _v(r, 2, 'species_name') or '') if x),
             'opis': ' · '.join(str(x) for x in (_v(r, 3, 'location') or '', _v(r, 4, 'event_date') or '') if x),
             'url': url_for('content.bird_ringing_record_detail', record_id=_v(r, 0, 'id'))} for r in cur.fetchall()]


def _q(t):
    from urllib.parse import quote
    return quote(str(t)[:80])


# (кључ, назив, иконица, провера приступа, функција, страна „сви резултати“)
IZVORI = (
    ('minerali', 'Минерали', 'bi-gem', lambda: _ima_modul('mineral_database'), _minerali,
     lambda q: url_for('collections.admin_mineral_collection', search_mode='collection', search=q)),
    ('meteoriti', 'Метеорити', 'bi-stars', lambda: _ima_modul('meteorite_collection'), _meteoriti, None),
    ('zbirke', 'Збирке', 'bi-collection', lambda: 'user_id' in session, _zbirke, None),
    ('prstenovanje', 'Прстеновање птица', 'bi-egg', lambda: _ima_modul('bird_ringing_database'), _prstenovanje, None),
    ('knjige', 'Библиотека', 'bi-book', lambda: _ima_modul('library_database'), _knjige,
     lambda q: url_for('library_database') + '?q=' + _q(q)),
    ('zaposleni', 'Запослени', 'bi-people', lambda: _ima_modul('employees_database') or _ima_modul('employee_profiles'), _zaposleni,
     lambda q: url_for('employees_database') + '?q=' + _q(q)),
    ('kr', 'К-Р досијеи', 'bi-clipboard2-pulse', lambda: _ima_modul('kr_dosije'), _kr_dosijei, None),
    ('fotografije', 'Фототека', 'bi-camera', lambda: _ima_modul('fototeka'), _fotografije, None),
    ('dokumenti', 'Документа', 'bi-folder2-open', lambda: _ima_modul('dokumenti'), _dokumenti, None),
)


def pretrazi(q):
    """Речник {upit, grupe:[{kljuc,naziv,ikona,stavke,jos}]} за пријављеног корисника."""
    upit = normalizuj_upit(q)
    if not upit:
        return {'upit': q or '', 'grupe': [], 'prekratko': True}
    s = sabloni(upit)
    grupe = []
    with get_postgres_connection() as conn:
        for kljuc, naziv, ikona, dozvola, fn, jos in IZVORI:
            try:
                if not dozvola():
                    continue
            except Exception:  # noqa: BLE001
                continue
            try:
                with conn.cursor() as cur:
                    stavke = fn(cur, s)
                conn.commit()
            except Exception as exc:  # noqa: BLE001 - једна база не руши претрагу
                conn.rollback()
                logger.warning('Претрага: група %s није претражена: %s', kljuc, exc)
                continue
            if stavke:
                grupe.append({'kljuc': kljuc, 'naziv': naziv, 'ikona': ikona, 'stavke': stavke,
                              'jos': jos(upit) if jos else None})
    return {'upit': upit, 'grupe': grupe, 'prekratko': False}
