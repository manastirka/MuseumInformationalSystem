"""QR ознаке за примерке и кутије — један идентитет, један резолвер.

QR код не носи адресу стране него ознаку објекта (8 знакова). Резолвер
(`/q/<oznaka>`) ознаку преводи у оно што треба приказати: пријављеном кориснику
детаље, непријављеном јавну картицу. Адреса сервера је подешавање
(`qr_bazna_adresa` у системским подешавањима), не константа — при селидби се
мења једно поље, а све раније одштампано важи преко резолвера.

Кутије минералошке збирке: идентитет је текст поља `storage_location`, а QR
садржај остаје стари облик `/qr_box/minerals/<kutija>` — налепнице са тим
обликом су већ залепљене, па нове морају да буду истоветне старима.
"""

import logging
import re
import secrets
from urllib.parse import quote

import qrcode
from qrcode.image.svg import SvgPathImage

from postgres_service import get_postgres_connection

logger = logging.getLogger(__name__)

# Crockford base32: без I, L, O, U — ништа што се брка при читању са налепнице.
ALFABET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
DUZINA_OZNAKE = 8
OZNAKA_RE = re.compile(r'^[0-9A-HJKMNP-TV-Z]{8}$')
_ZAMENE_PRI_CITANJU = str.maketrans({'O': '0', 'I': '1', 'L': '1'})

VRSTA_PRIMERAK = 'primerak'
VRSTA_KUTIJA = 'kutija'
VRSTE = (VRSTA_PRIMERAK, VRSTA_KUTIJA)
ZBIRKA_MINERALI = 'minerals'

PODRAZUMEVANA_BAZNA_ADRESA = 'https://192.168.144.194'
KLJUC_PODESAVANJA = 'qr_bazna_adresa'

# Формати налепница (mm). `list` је А4 са више истих налепница.
FORMATI = {
    'primerak': {'naziv': 'Примерак 25 × 15 mm', 'sirina': 25, 'visina': 15, 'qr': 12},
    'kutija': {'naziv': 'Кутија 50 × 30 mm', 'sirina': 50, 'visina': 30, 'qr': 24},
    'list': {'naziv': 'А4 лист (више истих)', 'sirina': 50, 'visina': 30, 'qr': 24},
}
PODRAZUMEVANI_FORMAT = {VRSTA_PRIMERAK: 'primerak', VRSTA_KUTIJA: 'kutija'}
NAJVISE_NA_LISTU = 40

# Поља која јавна картица сме да покаже непријављеном — ништа о депоу, легатору,
# вредности набавке или напоменама.
JAVNA_POLJA = (
    ('scientific_name', 'Научно име'),
    ('common_name_sr', 'Народно име'),
    ('meteorite_name', 'Назив метеорита'),
    ('specimen_name', 'Назив примерка'),
    ('rock_name', 'Назив стене'),
    ('name', 'Назив'),
    ('family', 'Фамилија'),
    ('order_name', 'Ред'),
    ('class_name', 'Класа'),
    ('classification', 'Класификација'),
    ('meteorite_class', 'Класа метеорита'),
    ('rock_type', 'Тип стене'),
    ('category', 'Категорија'),
    ('subcategory', 'Поткатегорија'),
    ('geological_period', 'Геолошки период'),
    ('geological_age', 'Геолошка старост'),
    ('age_million_years', 'Старост (милиони година)'),
    ('location_found', 'Локација налаза'),
    ('fall_location', 'Место пада'),
    ('habitat', 'Станиште'),
    ('date_collected', 'Датум прикупљања'),
    ('fall_date', 'Датум пада'),
    ('collector', 'Сакупљач'),
    ('conservation_status', 'Статус заштите'),
    ('description', 'Опис'),
)


class NepoznataOznaka(LookupError):
    """Ознака није у бази или није исправног облика."""


class NepoznatObjekat(LookupError):
    """Ознака постоји, али записа на који показује више нема."""


# --------------------------------------------------------------------------
# Ознаке
# --------------------------------------------------------------------------

def normalizuj_oznaku(tekst):
    """Врати ознаку у канонском облику или None ако није ознака.

    Толерише мала слова и уобичајене грешке читања (O→0, I/L→1), па се ознака
    сме укуцати руком са налепнице.
    """
    if tekst is None:
        return None
    kandidat = str(tekst).strip().upper().translate(_ZAMENE_PRI_CITANJU)
    return kandidat if OZNAKA_RE.match(kandidat) else None


def _nova_oznaka(cur):
    for _ in range(20):
        oznaka = ''.join(secrets.choice(ALFABET) for _ in range(DUZINA_OZNAKE))
        cur.execute("SELECT 1 FROM qr_oznake WHERE oznaka = %s", (oznaka,))
        if cur.fetchone() is None:
            return oznaka
    raise RuntimeError('Не могу да нађем слободну QR ознаку после 20 покушаја')


_KOLONE = ('oznaka', 'vrsta', 'zbirka', 'objekat_id', 'napravio', 'napravljeno_at',
           'stampano_puta', 'poslednje_stampano', 'poslednje_stampao')
_SELECT = 'SELECT ' + ', '.join(_KOLONE) + ' FROM qr_oznake'


def _red(row):
    return dict(zip(_KOLONE, row)) if row else None


def dohvati_oznaku(oznaka):
    """Врати ред ознаке (dict) или None."""
    oznaka = normalizuj_oznaku(oznaka)
    if not oznaka:
        return None
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(_SELECT + " WHERE oznaka = %s", (oznaka,))
            return _red(cur.fetchone())


def oznaka_za_objekat(vrsta, zbirka, objekat_id):
    """Врати ред ознаке додељене објекту, или None ако објекат још нема ознаку."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                _SELECT + " WHERE vrsta = %s AND zbirka = %s AND objekat_id = %s",
                (vrsta, zbirka, str(objekat_id)),
            )
            return _red(cur.fetchone())


def dodeli_oznaku(vrsta, zbirka, objekat_id, ko):
    """Додели ознаку објекту; ако је већ има, врати постојећу (идемпотентно).

    Упис је у једној трансакцији; при паду базе изузетак иде позиваоцу — никад
    „успех" без реда у бази.
    """
    if vrsta not in VRSTE:
        raise ValueError(f'Непозната врста QR ознаке: {vrsta!r}')
    objekat_id = str(objekat_id).strip()
    if not objekat_id:
        raise ValueError('objekat_id је празан')
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                _SELECT + " WHERE vrsta = %s AND zbirka = %s AND objekat_id = %s FOR UPDATE",
                (vrsta, zbirka, objekat_id),
            )
            postojeca = _red(cur.fetchone())
            if postojeca:
                conn.commit()
                return postojeca
            oznaka = _nova_oznaka(cur)
            cur.execute(
                """
                INSERT INTO qr_oznake (oznaka, vrsta, zbirka, objekat_id, napravio)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING """ + ', '.join(_KOLONE),
                (oznaka, vrsta, zbirka, objekat_id, ko or 'непознат'),
            )
            red = _red(cur.fetchone())
            conn.commit()
            logger.info("QR ознака %s додељена: %s/%s/%s (%s)", oznaka, vrsta, zbirka, objekat_id, ko)
            return red


def zabelezi_stampu(oznaka, ko):
    """Повећај бројач штампања; враћа нови ред или None ако ознаке нема."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE qr_oznake
                   SET stampano_puta = stampano_puta + 1,
                       poslednje_stampano = now(),
                       poslednje_stampao = %s
                 WHERE oznaka = %s
                RETURNING """ + ', '.join(_KOLONE),
                (ko or 'непознат', oznaka),
            )
            red = _red(cur.fetchone())
            conn.commit()
            return red


# --------------------------------------------------------------------------
# Садржај кода и слика
# --------------------------------------------------------------------------

def bazna_adresa():
    """Адреса коју носе нови QR кодови — подешавање, па env, па подразумевано."""
    import os

    vrednost = ''
    try:
        import admin_system_views

        vrednost = (admin_system_views.load_saved_settings() or {}).get(KLJUC_PODESAVANJA) or ''
    except Exception as exc:  # подешавања недоступна — не обарамо штампу због тога
        logger.warning("QR базна адреса из подешавања није прочитана: %s", exc)
    vrednost = str(vrednost or os.environ.get('QR_BAZNA_ADRESA') or PODRAZUMEVANA_BAZNA_ADRESA)
    return vrednost.strip().rstrip('/')


def sadrzaj_koda(red):
    """Шта се уписује у QR: за кутију стари облик (истоветан залепљеним), иначе /q/."""
    if red['vrsta'] == VRSTA_KUTIJA and red['zbirka'] == ZBIRKA_MINERALI:
        return f"{bazna_adresa()}/qr_box/minerals/{quote(red['objekat_id'], safe='')}"
    return f"{bazna_adresa()}/q/{red['oznaka']}"


def svg_kod(sadrzaj):
    """QR као SVG (path) — оштар у сваком размеру и мањи од PNG-а."""
    kod = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=1,
        image_factory=SvgPathImage,
    )
    kod.add_data(sadrzaj)
    kod.make(fit=True)
    slika = kod.make_image()
    svg = slika.to_string(encoding='unicode')
    # Уклони XML пролог да SVG може inline у HTML.
    if svg.startswith('<?xml'):
        svg = svg.split('?>', 1)[1].lstrip()
    return svg


# --------------------------------------------------------------------------
# Објекти на које ознаке показују
# --------------------------------------------------------------------------

def _app():
    import app as museum_app

    return museum_app


def normalizuj_zbirku(zbirka):
    """Алијаси (minerals/mineral, meteorites/meteorite, geology/petrology) → канонски кључ."""
    zbirka = str(zbirka or '').strip().lower()
    if zbirka == 'mineral':
        return ZBIRKA_MINERALI
    return _app().normalize_qr_collection_type(zbirka)


def zbirka_config(zbirka):
    return _app().get_qr_collection_config(normalizuj_zbirku(zbirka))


def naziv_zbirke(zbirka):
    cfg = zbirka_config(zbirka)
    return cfg['name'] if cfg else zbirka


def modul_zbirke(zbirka):
    cfg = zbirka_config(zbirka)
    return cfg.get('module') if cfg else None


def korisnik_ima_pristup(zbirka):
    """Да ли пријављени корисник сме у ову збирку (по модулу)."""
    from flask import session

    if 'user_id' not in session:
        return False
    modul = modul_zbirke(zbirka)
    if not modul:
        return False
    return bool(_app().user_has_module_access(
        session.get('user_email', ''), session.get('user_role', 'user'), modul))


def _mineral(objekat_id):
    try:
        mineral_id = int(str(objekat_id).strip())
    except (TypeError, ValueError):
        return None
    baza = _app().get_mineral_database()
    if not baza or not getattr(baza, 'available', True):
        return None
    return baza.get_mineral_by_id(mineral_id)


def dohvati_zapis(zbirka, objekat_id):
    """Запис примерка по id-у, у облику dict, или None."""
    zbirka = normalizuj_zbirku(zbirka)
    if zbirka == ZBIRKA_MINERALI:
        return _mineral(objekat_id)
    trazeni = str(objekat_id).strip()
    for zapis in _app().get_qr_collection_records(zbirka) or []:
        if str(zapis.get('id', '')).strip() == trazeni:
            return zapis
    return None


def opis_zapisa(zbirka, zapis):
    """Наслов и подаци за налепницу/картицу, независно од збирке."""
    zbirka = normalizuj_zbirku(zbirka)
    if zbirka == ZBIRKA_MINERALI:
        return {
            'naslov': zapis.get('naziv') or 'Минерал',
            'katalog': zapis.get('inventarni_broj') or zapis.get('inventory_number') or '',
            'sazetak': zapis.get('lokalitet') or zapis.get('card_locality') or '',
            'kutija': zapis.get('gde_se_nalazi') or zapis.get('storage_location') or '',
        }
    app = _app()
    return {
        'naslov': app.get_qr_record_name(zapis, zbirka),
        'katalog': app.get_qr_record_catalog_label(zapis, zbirka),
        'sazetak': app.get_qr_record_summary(zapis, zbirka),
        'kutija': zapis.get('storage_location') or '',
    }


def javna_polja(zbirka, zapis):
    """Парови (лабела, вредност) које јавна картица сме да покаже."""
    zbirka = normalizuj_zbirku(zbirka)
    if zbirka == ZBIRKA_MINERALI:
        kandidati = (
            ('naziv', 'Назив'), ('formula', 'Формула'), ('lokalitet', 'Локалитет'),
            ('card_locality', 'Локалитет'), ('kristalni_sistem', 'Кристални систем'),
            ('crystal_system', 'Кристални систем'), ('boja', 'Боја'), ('color', 'Боја'),
        )
    else:
        kandidati = JAVNA_POLJA
    parovi, videne = [], set()
    for kljuc, labela in kandidati:
        vrednost = zapis.get(kljuc)
        if vrednost in (None, '', [], {}) or labela in videne:
            continue
        videne.add(labela)
        parovi.append((labela, str(vrednost)))
    return parovi


def labele_polja():
    """Лабеле поља записа (из collection_access_support), за страну детаља."""
    return dict(getattr(_app(), 'QR_FIELD_LABELS', None) or {})


def url_detalja(zbirka, objekat_id):
    """Страна детаља за пријављеног корисника."""
    from flask import url_for

    zbirka = normalizuj_zbirku(zbirka)
    if zbirka == ZBIRKA_MINERALI:
        return url_for('collections.admin_mineral_detail', mineral_id=int(objekat_id))
    return url_for('qr.detalji_primerka', zbirka=zbirka, objekat_id=int(objekat_id))


def url_kartice(oznaka):
    from flask import url_for

    return url_for('qr.resolver', oznaka=oznaka)


def kutija_minerali(kutija):
    """Минерали у кутији (по `storage_location`), као листа dict-ова."""
    kutija = str(kutija or '').strip()
    if not kutija:
        return []
    baza = _app().get_mineral_database()
    if not baza or not getattr(baza, 'available', True):
        raise RuntimeError('База минерала није доступна')
    from sqlalchemy import text as sa_text

    with baza.engine.connect() as conn:
        redovi = conn.execute(
            sa_text(
                "SELECT * FROM minerals WHERE TRIM(storage_location) = :kutija "
                "ORDER BY inventory_number"
            ),
            {'kutija': kutija},
        ).mappings().all()
    minerali = []
    for red in redovi:
        mineral = dict(red)
        mineral.setdefault('naziv', mineral.get('item_name', ''))
        mineral.setdefault('inventarni_broj', mineral.get('inventory_number', ''))
        mineral.setdefault('lokalitet', mineral.get('card_locality', ''))
        mineral.setdefault('gde_se_nalazi', mineral.get('storage_location', ''))
        mineral.setdefault('kolicina', mineral.get('quantity', ''))
        minerali.append(mineral)
    return minerali


def sve_kutije():
    """Све кутије минералошке збирке са бројем минерала, сортиране као на полици."""
    baza = _app().get_mineral_database()
    if not baza or not getattr(baza, 'available', True):
        raise RuntimeError('База минерала није доступна')
    from sqlalchemy import text as sa_text

    with baza.engine.connect() as conn:
        redovi = conn.execute(
            sa_text(
                "SELECT TRIM(storage_location) AS kutija, COUNT(*) AS broj, "
                "MIN(item_name) AS primer "
                "FROM minerals WHERE COALESCE(TRIM(storage_location), '') <> '' "
                "GROUP BY TRIM(storage_location)"
            )
        ).mappings().all()
        bez = conn.execute(
            sa_text("SELECT COUNT(*) FROM minerals WHERE COALESCE(TRIM(storage_location), '') = ''")
        ).scalar() or 0

    def kljuc(red):
        k = red['kutija']
        if ',' not in k and k.isdigit():
            return (0, int(k), k)
        return (1, 0, k.lower())

    kutije = sorted((dict(r) for r in redovi), key=kljuc)
    return kutije, int(bez)


# --------------------------------------------------------------------------
# Резолуција ознаке у објекат
# --------------------------------------------------------------------------

def razresi(oznaka):
    """Врати (red, opis) за ознаку; диже NepoznataOznaka / NepoznatObjekat."""
    red = dohvati_oznaku(oznaka)
    if not red:
        raise NepoznataOznaka(oznaka)
    if red['vrsta'] == VRSTA_KUTIJA:
        return red, {'naslov': f"Кутија {red['objekat_id']}", 'katalog': red['objekat_id'],
                     'sazetak': naziv_zbirke(red['zbirka']), 'kutija': red['objekat_id']}
    zapis = dohvati_zapis(red['zbirka'], red['objekat_id'])
    if zapis is None:
        raise NepoznatObjekat(oznaka)
    opis = opis_zapisa(red['zbirka'], zapis)
    opis['zapis'] = zapis
    return red, opis


def opis_za_api(red, opis):
    """JSON уговор за Android клијент (`GET /api/q/<oznaka>`)."""
    from flask import url_for

    zbirka = normalizuj_zbirku(red['zbirka'])
    if red['vrsta'] == VRSTA_KUTIJA:
        detalji = url_for('qr.kutija_minerala', kutija=red['objekat_id'])
    else:
        detalji = url_detalja(zbirka, red['objekat_id'])
    return {
        'ok': True,
        'oznaka': red['oznaka'],
        'vrsta': red['vrsta'],
        'zbirka': zbirka,
        'objekat_id': red['objekat_id'],
        'naslov': opis['naslov'],
        'katalog': opis.get('katalog', ''),
        'url_detalja': detalji,
        'url_kartice': url_kartice(red['oznaka']),
    }
