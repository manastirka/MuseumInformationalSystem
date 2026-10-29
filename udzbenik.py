"""Интерактивни уџбеник — логика (руте су у blueprints/udzbenik.py).

Уџбеник по збирци → поглавља → лекције; садржај лекције је JSONB по
udzbenik/schema/lekcija.schema.json, а мотор (Three.js читач у
static/udzbenik/) чита искључиво API описан у брифу (§4). Овај модул:

- одлучује о приступу на ЈЕДНОМ месту (``sme_da_cita``): пријављен + модул
  ``udzbenik`` → да; непријављен → само ако је уџбеник јаван и објављен;
  администратор и директор исто што и свако пријављен;
- склапа одговоре API-ја (структура, лекција са РАЗРЕШЕНИМ блоковима слике и
  примерка, претходна/следећа преко границе поглавља);
- упис напретка са валидацијом до базе;
- CIF структуре минерала из локалног RRUFF скупа, под правом ``udzbenik``.

База је једини извор истине; при читању се садржај НЕ валидира по шеми
(валидација је на упису — scripts/udzbenik_uvoz.py), али блок непознатог
``tip``-а пролази са ``nepoznat: true``.
"""
import json
import logging

from flask import session, url_for

import museum_qr
from postgres_service import get_postgres_connection

logger = logging.getLogger(__name__)

MODUL = 'udzbenik'
STATUS_NACRT = 'nacrt'
STATUS_OBJAVLJEN = 'objavljen'
STATUSI = (STATUS_NACRT, STATUS_OBJAVLJEN)
NAJVISE_FOTOGRAFIJA_PRIMERKA = 4
POZNATI_TIPOVI = ('tekst', 'slika', 'scena', 'primerak', 'pitanje', 'napomena')
DERIVAT_VELIKI = 'jpg'
DERIVAT_MALI = 'thumb'


class GreskaZahteva(Exception):
    """Грешка коју рута преводи у JSON ``{"greska": ...}`` + HTTP статус."""

    def __init__(self, status, poruka):
        super().__init__(poruka)
        self.status = status
        self.poruka = poruka


def _app():
    import app as museum_app
    return museum_app


def _redovi(cur):
    kolone = [k.name for k in cur.description]
    return [dict(zip(kolone, red)) for red in cur.fetchall()]


def _red(cur):
    redovi = _redovi(cur)
    return redovi[0] if redovi else None


def _iso(vreme):
    return vreme.isoformat() if vreme is not None else None


def _json(vrednost):
    """JSONB стиже као већ парсиран објекат или као текст — изједначи."""
    if isinstance(vrednost, (str, bytes)):
        return json.loads(vrednost)
    return vrednost


# --------------------------------------------------------------------------
# Права
# --------------------------------------------------------------------------

def prijavljen():
    return 'user_id' in session


def korisnik_email():
    return (session.get('user_email') or '').strip().lower()


def ima_modul():
    """Пријављен корисник са модулом ``udzbenik`` (админ/директор пролазе кроз
    исту проверу — user_has_module_access их пушта по улози)."""
    if not prijavljen():
        return False
    return bool(_app().user_has_module_access(
        session.get('user_email', ''), session.get('user_role', 'user'), MODUL))


def sme_fototeku():
    """Медиј слика служи fototeka.fototeka_media (пријава + модул fototeka);
    анонимни читалац јавног уџбеника и пријављени без модула не могу да га
    учитају, па блок мора поштено да каже „недоступан“."""
    if not prijavljen():
        return False
    return bool(_app().user_has_module_access(
        session.get('user_email', ''), session.get('user_role', 'user'), 'fototeka'))


RAZLOG_BEZ_FOTOTEKE = 'nema prava na Фототеку'


def javan(udzbenik_red):
    return bool(udzbenik_red and udzbenik_red.get('javno')
                and udzbenik_red.get('status') == STATUS_OBJAVLJEN)


def sme_da_cita(udzbenik_red):
    """Једино место где се одлучује приступ уџбенику (None = не постоји)."""
    if udzbenik_red is None:
        return False
    if prijavljen():
        return ima_modul()
    return javan(udzbenik_red)


def samo_objavljeno():
    """Непријављени виде само објављене лекције; пријављени и нацрте."""
    return not prijavljen()


# --------------------------------------------------------------------------
# Читање
# --------------------------------------------------------------------------

def dohvati_udzbenik(zbirka, cur=None):
    sql = """SELECT id, zbirka, naslov, opis, status, javno, autor_email, created_at, updated_at
             FROM udzbenik WHERE zbirka = %s"""
    if cur is not None:
        cur.execute(sql, (zbirka,))
        return _red(cur)
    with get_postgres_connection() as conn:
        with conn.cursor() as cur2:
            cur2.execute(sql, (zbirka,))
            return _red(cur2)


def _poglavlja(cur, udzbenik_id):
    cur.execute("""SELECT id, slug, naslov, opis, redosled FROM udzbenik_poglavlje
                   WHERE udzbenik_id = %s ORDER BY redosled""", (udzbenik_id,))
    return _redovi(cur)


def _lekcije(cur, udzbenik_id, email):
    """Све лекције уџбеника по (поглавље.redosled, лекција.redosled) са
    ознаком завршености за дати e-mail."""
    cur.execute(
        """SELECT l.id, l.poglavlje_id, l.slug, l.naslov, l.sazetak, l.redosled, l.status,
                  l.verzija, l.updated_at, p.slug AS poglavlje_slug, p.naslov AS poglavlje_naslov,
                  p.redosled AS poglavlje_redosled,
                  COALESCE(n.zavrseno, FALSE) AS zavrseno
           FROM udzbenik_lekcija l
           JOIN udzbenik_poglavlje p ON p.id = l.poglavlje_id
           LEFT JOIN udzbenik_napredak n ON n.lekcija_id = l.id AND n.user_email = %s
           WHERE p.udzbenik_id = %s
           ORDER BY p.redosled, l.redosled""", (email or '', udzbenik_id))
    lekcije = _redovi(cur)
    if samo_objavljeno():
        lekcije = [x for x in lekcije if x['status'] == STATUS_OBJAVLJEN]
    return lekcije


def struktura(udzbenik_red):
    """Одговор за GET /api/udzbenik/<zbirka> (бриф §4.1)."""
    email = korisnik_email()
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            poglavlja = _poglavlja(cur, udzbenik_red['id'])
            lekcije = _lekcije(cur, udzbenik_red['id'], email)
    po_poglavlju = {}
    for lek in lekcije:
        po_poglavlju.setdefault(lek['poglavlje_id'], []).append({
            'slug': lek['slug'], 'naslov': lek['naslov'], 'redosled': lek['redosled'],
            'sazetak': lek['sazetak'], 'zavrseno': bool(lek['zavrseno']),
        })
    izlaz_poglavlja = []
    for p in poglavlja:
        stavke = po_poglavlju.get(p['id'], [])
        if not stavke and samo_objavljeno():
            continue
        izlaz_poglavlja.append({'slug': p['slug'], 'naslov': p['naslov'], 'redosled': p['redosled'],
                                'opis': p['opis'], 'lekcije': stavke})
    return {
        'udzbenik': {
            'zbirka': udzbenik_red['zbirka'], 'naslov': udzbenik_red['naslov'],
            'opis': udzbenik_red['opis'], 'status': udzbenik_red['status'],
            'javno': bool(udzbenik_red['javno']), 'azurirano': _iso(udzbenik_red['updated_at']),
        },
        'poglavlja': izlaz_poglavlja,
        'korisnik': {'prijavljen': prijavljen(), 'moze_da_uredjuje': False},
    }


def nadji_lekciju(udzbenik_red, poglavlje_slug, lekcija_slug):
    """(лекција, претходна, следећа) или None ако пут не постоји / није видљив."""
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            lekcije = _lekcije(cur, udzbenik_red['id'], korisnik_email())
    for i, lek in enumerate(lekcije):
        if lek['poglavlje_slug'] == poglavlje_slug and lek['slug'] == lekcija_slug:
            return lek, (lekcije[i - 1] if i > 0 else None), (lekcije[i + 1] if i + 1 < len(lekcije) else None)
    return None


def poglavlje_postoji(udzbenik_red, poglavlje_slug):
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM udzbenik_poglavlje WHERE udzbenik_id = %s AND slug = %s",
                        (udzbenik_red['id'], poglavlje_slug))
            return cur.fetchone() is not None


def _sused(lek):
    if lek is None:
        return None
    return {'poglavlje': lek['poglavlje_slug'], 'lekcija': lek['slug'], 'naslov': lek['naslov']}


def lekcija(udzbenik_red, poglavlje_slug, lekcija_slug):
    """Одговор за GET /api/udzbenik/<zbirka>/lekcija/<p>/<l> (бриф §4.2) или None."""
    nadjeno = nadji_lekciju(udzbenik_red, poglavlje_slug, lekcija_slug)
    if nadjeno is None:
        return None
    lek, prethodna, sledeca = nadjeno
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT sadrzaj FROM udzbenik_lekcija WHERE id = %s", (lek['id'],))
            sadrzaj = _json(cur.fetchone()[0]) or {}
            blokovi = razresi_blokove(cur, sadrzaj.get('blokovi') or [])
    return {'lekcija': {
        'slug': lek['slug'], 'naslov': lek['naslov'],
        'poglavlje': {'slug': lek['poglavlje_slug'], 'naslov': lek['poglavlje_naslov']},
        'verzija': lek['verzija'], 'azurirano': _iso(lek['updated_at']),
        'prethodna': _sused(prethodna), 'sledeca': _sused(sledeca),
        'zavrseno': bool(lek['zavrseno']), 'blokovi': blokovi,
    }}


# --------------------------------------------------------------------------
# Разрешавање блокова — сервер ДОПУЊУЈЕ, не мења ауторова поља
# --------------------------------------------------------------------------

def razresi_blokove(cur, blokovi):
    izlaz = []
    for blok in blokovi:
        if not isinstance(blok, dict):
            izlaz.append({'vrednost': blok, 'nepoznat': True})
            continue
        tip = blok.get('tip')
        if tip == 'slika':
            izlaz.append(_razresi_sliku(cur, blok))
        elif tip == 'primerak':
            izlaz.append(_razresi_primerak(cur, blok))
        elif tip in POZNATI_TIPOVI:
            izlaz.append(dict(blok))
        else:
            izlaz.append(dict(blok, nepoznat=True))
    return izlaz


def _nedostupan(blok, razlog):
    return dict(blok, nedostupan=True, razlog=razlog)


def _ime_autora(cur, email):
    if not email:
        return ''
    cur.execute("SELECT full_name FROM users WHERE LOWER(email) = LOWER(%s)", (email,))
    red = cur.fetchone()
    return (red[0] if red and red[0] else email)


def _razresi_sliku(cur, blok):
    import fototeka_views

    if not sme_fototeku():
        return _nedostupan(blok, RAZLOG_BEZ_FOTOTEKE)
    cur.execute("""SELECT id, width, height, autor_email, vidljivost, obrisana, status
                   FROM fotografije WHERE id = %s""", (blok.get('fotografija_id'),))
    foto = _red(cur)
    if foto is None or foto['obrisana']:
        return _nedostupan(blok, 'фотографија не постоји')
    if not fototeka_views.can_view_photo(session, foto):
        return _nedostupan(blok, 'приватна фотографија')
    return dict(
        blok,
        url=url_for('fototeka.fototeka_media', fotografija_id=foto['id'], kind=DERIVAT_VELIKI),
        url_mala=url_for('fototeka.fototeka_media', fotografija_id=foto['id'], kind=DERIVAT_MALI),
        sirina_px=foto['width'], visina_px=foto['height'],
        autor=_ime_autora(cur, foto['autor_email']),
    )


def _fotografije_primerka(cur, zbirka, zapis, katalog):
    import fototeka_views

    if not sme_fototeku():
        return []
    if zbirka == museum_qr.ZBIRKA_MINERALI:
        uslov = "(v.mineral_id = %s OR (v.database_name = 'mineral' AND v.inventarni_broj = %s))"
        parametri = [zapis.get('id'), str(katalog or '')]
    else:
        uslov = "(v.database_name = %s AND v.inventarni_broj = %s)"
        parametri = [zbirka, str(katalog or '')]
    sql = f"""SELECT DISTINCT f.id FROM foto_veza_predmet v
              JOIN fotografije f ON f.id = v.fotografija_id
              WHERE {uslov} AND f.obrisana = FALSE"""
    vidljivost, vid_parametri = fototeka_views._visibility_filter(session, 'f')
    if vidljivost:
        sql += ' AND ' + vidljivost
        parametri.extend(vid_parametri)
    sql += ' ORDER BY f.id LIMIT %s'
    parametri.append(NAJVISE_FOTOGRAFIJA_PRIMERKA)
    cur.execute(sql, parametri)
    return [{
        'id': red[0],
        'url': url_for('fototeka.fototeka_media', fotografija_id=red[0], kind=DERIVAT_VELIKI),
        'url_mala': url_for('fototeka.fototeka_media', fotografija_id=red[0], kind=DERIVAT_MALI),
    } for red in cur.fetchall()]


def _razresi_primerak(cur, blok):
    zbirka = museum_qr.normalizuj_zbirku(blok.get('zbirka'))
    if not museum_qr.korisnik_ima_pristup(zbirka):
        return _nedostupan(blok, 'nema prava na zbirku')
    try:
        zapis = museum_qr.dohvati_zapis(zbirka, blok.get('objekat_id'))
    except Exception as exc:  # noqa: BLE001 - примерак не сме да сруши лекцију
        logger.warning('Уџбеник: примерак %s/%s није дохваћен: %s', zbirka, blok.get('objekat_id'), exc)
        zapis = None
    if zapis is None:
        return _nedostupan(blok, 'примерак не постоји')
    opis = museum_qr.opis_zapisa(zbirka, zapis)
    katalog = opis.get('katalog') or ''
    razresen = dict(
        blok,
        naziv=opis.get('naslov') or '',
        inventarni_broj=zapis.get('inventarni_broj_display') or katalog,
        lokalitet=opis.get('sazetak') or '',
        url_kartica=museum_qr.url_detalja(zbirka, zapis.get('id', blok.get('objekat_id'))),
        fotografije=_fotografije_primerka(cur, zbirka, zapis, katalog),
    )
    if not sme_fototeku():
        razresen['fotografije_razlog'] = RAZLOG_BEZ_FOTOTEKE
    return razresen


# --------------------------------------------------------------------------
# Листа уџбеника
# --------------------------------------------------------------------------

def lista_udzbenika():
    """Уџбеници на које корисник сме, са бројем лекција и % завршено."""
    email = korisnik_email()
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT u.id, u.zbirka, u.naslov, u.opis, u.status, u.javno, u.updated_at,
                                  COUNT(l.id) AS broj_lekcija,
                                  COUNT(n.lekcija_id) FILTER (WHERE n.zavrseno) AS zavrsenih
                           FROM udzbenik u
                           LEFT JOIN udzbenik_poglavlje p ON p.udzbenik_id = u.id
                           LEFT JOIN udzbenik_lekcija l ON l.poglavlje_id = p.id
                                AND (%s OR l.status = %s)
                           LEFT JOIN udzbenik_napredak n ON n.lekcija_id = l.id AND n.user_email = %s
                           GROUP BY u.id ORDER BY u.naslov""",
                        (not samo_objavljeno(), STATUS_OBJAVLJEN, email))
            redovi = _redovi(cur)
    izlaz = []
    for red in redovi:
        if not sme_da_cita(red):
            continue
        broj = int(red['broj_lekcija'] or 0)
        zavrsenih = int(red['zavrsenih'] or 0)
        red['procenat'] = (round(100 * zavrsenih / broj) if (broj and prijavljen()) else None)
        izlaz.append(red)
    return izlaz


# --------------------------------------------------------------------------
# Напредак
# --------------------------------------------------------------------------

def _ceo_broj(vrednost, ime):
    if isinstance(vrednost, bool) or not isinstance(vrednost, int) or vrednost < 0:
        raise GreskaZahteva(400, f'„{ime}“ мора бити цео број ≥ 0')
    return vrednost


def upisi_napredak(telo):
    """POST /api/udzbenik/napredak (бриф §4.3): валидација → upsert у
    udzbenik_napredak. Враћа тек када је ред у бази; грешка → GreskaZahteva."""
    if not prijavljen():
        raise GreskaZahteva(401, 'Морате бити пријављени')
    if not isinstance(telo, dict):
        raise GreskaZahteva(400, 'Тело захтева мора бити JSON објекат')
    zbirka = str(telo.get('zbirka') or '').strip()
    poglavlje = str(telo.get('poglavlje') or '').strip()
    lekcija_slug = str(telo.get('lekcija') or '').strip()
    if not (zbirka and poglavlje and lekcija_slug):
        raise GreskaZahteva(400, 'Обавезна поља: zbirka, poglavlje, lekcija')
    zavrseno = telo.get('zavrseno', True)
    if not isinstance(zavrseno, bool):
        raise GreskaZahteva(400, '„zavrseno“ мора бити true/false')
    rezultat = telo.get('rezultat')
    if rezultat is not None:
        if not isinstance(rezultat, dict):
            raise GreskaZahteva(400, '„rezultat“ мора бити објекат')
        tacno = _ceo_broj(rezultat.get('tacno', 0), 'tacno')
        ukupno = _ceo_broj(rezultat.get('ukupno', 0), 'ukupno')
        if tacno > ukupno:
            raise GreskaZahteva(400, '„tacno“ не може бити већe од „ukupno“')
        odgovori = rezultat.get('odgovori', {})
        if not isinstance(odgovori, dict):
            raise GreskaZahteva(400, '„odgovori“ мора бити објекат')
        rezultat = {'tacno': tacno, 'ukupno': ukupno, 'odgovori': odgovori}

    udzbenik_red = dohvati_udzbenik(zbirka)
    if udzbenik_red is None:
        raise GreskaZahteva(404, 'Уџбеник не постоји')
    if not sme_da_cita(udzbenik_red):
        raise GreskaZahteva(403, 'Немате дозволу за овај уџбеник')
    nadjeno = nadji_lekciju(udzbenik_red, poglavlje, lekcija_slug)
    if nadjeno is None:
        raise GreskaZahteva(404, 'Лекција не постоји')
    lek = nadjeno[0]
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO udzbenik_napredak (user_email, lekcija_id, zavrseno, rezultat, updated_at)
                   VALUES (%s, %s, %s, %s, now())
                   ON CONFLICT (user_email, lekcija_id) DO UPDATE
                   SET zavrseno = EXCLUDED.zavrseno, rezultat = EXCLUDED.rezultat, updated_at = now()""",
                (korisnik_email(), lek['id'], zavrseno,
                 json.dumps(rezultat, ensure_ascii=False) if rezultat is not None else None))
        conn.commit()
    return {'ok': True}


# --------------------------------------------------------------------------
# Структура минерала (CIF) из локалног RRUFF скупа
# --------------------------------------------------------------------------

def cif_strukture(mineral):
    """CIF јединичне ћелије проширен у P1 за ``mineral`` (српски или
    енглески назив). Само ћелија — суперћелију гради мотор на клијенту."""
    import local_rruff_data
    from mineral_translator import get_all_translations

    ime = ' '.join(str(mineral or '').split())
    if len(ime) < 2:
        raise GreskaZahteva(400, 'Назив минерала је прекратак')
    rruff = local_rruff_data.LocalRRUFFData()
    if not getattr(rruff, 'available', False):
        raise GreskaZahteva(503, 'Локални RRUFF подаци нису доступни на овом серверу')
    for kandidat in _kandidati_imena(ime):
        for prevod in get_all_translations(kandidat):
            cif = rruff.generate_cif_from_dif(prevod['english'], expand_unitcell=True)
            if cif:
                return cif
    raise GreskaZahteva(404, 'Структура није доступна за овај минерал')


def _kandidati_imena(ime):
    """mineral_translator зна латиницу и енглески; ћирилично име (како га
    аутор лекције природно пише) прво се преписује у латиницу."""
    import pretraga

    latinica = pretraga.u_latinicu(ime)
    return [ime] if latinica == ime else [latinica, ime]
