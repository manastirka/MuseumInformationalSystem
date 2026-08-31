"""Uvoz muzejskih vesti sa sajta nhmbeo.rs (WordPress REST API).

Zasto REST a ne HTML: dashboard_data_support.fetch_website_news() grebe
https://nhmbeo.rs/vesti/ i pogadja <article> tagove — puca pri svakoj izmeni
teme. WordPress REST (/wp-json/wp/v2/posts) daje ugovoren oblik: naslov,
datum, modified, izvod, sadrzaj, link i naslovnu sliku.

Pravila koja ovaj modul postuje:

1. Jedan izvor istine = baza. Upsert ide u news_articles po
   (izvor='nhmbeo', spoljni_id); nema JSON fallback-a.
2. Nikad tiho gutanje greske. Svako pokretanje upisuje red u news_import_log;
   pad mreze zavrsava kao status='greska' sa porukom, a izuzetak se dize dalje
   pozivaocu. "Nema novih vesti" i "uvoz je pukao" nikad ne izgledaju isto.
3. Nema stranog HTML-a u nasim stranama. Sadrzaj se cuva kao cist tekst
   (tagovi skinuti), pa ga Jinja escape-uje kao i svaki drugi tekst iz baze.
   Time je XSS iz tudjeg CMS-a nemoguc; za original postoji link na sajt.
4. Uvezeni redovi se ne menjaju rucno — sledeci uvoz bi izmenu pregazio.
   Granicu cuva museum_content_views.api_save_news.
"""

import html
import logging
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from psycopg.rows import dict_row

logger = logging.getLogger(__name__)

IZVOR = 'nhmbeo'
API_URL = 'https://nhmbeo.rs/wp-json/wp/v2/posts'
SAJT = 'https://nhmbeo.rs/'

CONNECT_TIMEOUT_SECONDS = 6
READ_TIMEOUT_SECONDS = 25
# Sajt muzeja obara REST odgovor na 500 za neke opsege objava (jedna
# neispravna objava u WordPress-u ruši ceo odgovor). Manja strana znači
# manji gubitak, a _spasi_stranu ispod vadi ostatak takve strane redom.
PER_PAGE = 10
DEFAULT_PAGES = 6

HEADERS = {
    'User-Agent': 'MIS-NHMB/1.0 (+https://nhmbeo.rs/) museum-news-importer',
    'Accept': 'application/json',
}

# WordPress kategorije sajta -> tip vesti u MIS-u. Vecina objava je
# 'Uncategorized', pa je podrazumevano 'Вест'.
TIP_PO_KATEGORIJI = {
    'izlozbe': 'Изложба',
    'virtuelni-muzej': 'Виртуелни музеј',
}
PODRAZUMEVANI_TIP = 'Вест'

# Elementi posle kojih ide novi red pri pretvaranju HTML-a u tekst.
BLOK_TAGOVI = ('p', 'div', 'section', 'article', 'header', 'footer',
               'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'tr',
               'blockquote', 'figcaption', 'pre')


def _get_postgres_connection(**kwargs):
    from postgres_service import get_postgres_connection
    return get_postgres_connection(**kwargs)


def ocisti_tekst(vrednost):
    """HTML iz WordPress-a -> cist tekst, bez tagova i bez entiteta."""
    if not vrednost:
        return ''
    supa = BeautifulSoup(str(vrednost), 'lxml')
    # get_text(separator='\n') seče i na <strong>/<em>/<span>, pa se jedna
    # recenica raspadne na pet "pasusa". Novi red pravimo samo tamo gde ga i
    # WordPress ima — na blokovskim elementima.
    for prelom in supa.find_all('br'):
        prelom.replace_with('\n')
    for blok in supa.find_all(BLOK_TAGOVI):
        blok.append('\n\n')
    tekst = supa.get_text()
    tekst = html.unescape(tekst)
    tekst = tekst.replace('\xa0', ' ')
    tekst = re.sub(r'[ \t]+', ' ', tekst)
    # WP ugradjene medije (video, galerija) get_text() pretvara u goli URL —
    # ponekad u zasebnom redu, ponekad usred recenice. To nije tekst vesti.
    redovi = [red for red in tekst.split('\n')
              if not re.fullmatch(r'\s*https?://\S+\s*', red)]
    tekst = '\n'.join(redovi)
    tekst = re.sub(
        r'\s*https?://\S+\.(?:mp4|mov|webm|m4v|jpe?g|png|gif|webp|pdf)\b',
        '', tekst, flags=re.IGNORECASE)
    tekst = re.sub(r'\n\s*\n\s*\n+', '\n\n', tekst)
    return tekst.strip()


def _datum(vrednost):
    """WordPress ISO datum -> datetime; None kad je neupotrebljiv."""
    if not vrednost:
        return None
    try:
        return datetime.fromisoformat(str(vrednost).replace('Z', '+00:00'))
    except ValueError:
        logger.warning("Neupotrebljiv datum iz WP-a: %r", vrednost)
        return None


def _slika(post):
    ugradjeno = (post.get('_embedded') or {}).get('wp:featuredmedia') or []
    for medija in ugradjeno:
        url = medija.get('source_url')
        if url:
            return url
    bolja = post.get('better_featured_image') or {}
    return bolja.get('source_url') or None


def _tip(post):
    for kategorija in post.get('categories_detail') or []:
        tip = TIP_PO_KATEGORIJI.get((kategorija.get('slug') or '').lower())
        if tip:
            return tip
    for grupa in (post.get('_embedded') or {}).get('wp:term') or []:
        for pojam in grupa or []:
            tip = TIP_PO_KATEGORIJI.get((pojam.get('slug') or '').lower())
            if tip:
                return tip
    return PODRAZUMEVANI_TIP


def _skini_ponovljen_naslov(tekst, naslov):
    """Ukloni naslov kad se ponavlja na pocetku tela objave."""
    if not tekst or not naslov:
        return tekst
    ociscen = tekst.lstrip()
    if ociscen.startswith(naslov):
        ociscen = ociscen[len(naslov):]
        return ociscen.lstrip(' \n\t.,;:-–—').strip()
    return tekst


def normalizuj(post):
    """Jedna WP objava -> red spreman za news_articles. None kad je bez naslova."""
    naslov = ocisti_tekst((post.get('title') or {}).get('rendered'))
    if not naslov:
        return None

    objavljeno = _datum(post.get('date'))
    izvod = ocisti_tekst((post.get('excerpt') or {}).get('rendered'))
    sadrzaj = ocisti_tekst((post.get('content') or {}).get('rendered'))

    # WP izvod ume da bude prvih par recenica sadrzaja plus "Detaljnije";
    # kad ga nema, uzmi pocetak sadrzaja da kartica ne ostane prazna.
    izvod = re.sub(r'\s*\[?…\]?\s*$', '…', izvod).strip()

    # Objave na sajtu pocinju ponovljenim naslovom u telu teksta; bez ovoga
    # kartica dva puta pise isto.
    sadrzaj = _skini_ponovljen_naslov(sadrzaj, naslov)
    izvod = _skini_ponovljen_naslov(izvod, naslov)

    if not izvod and sadrzaj:
        izvod = sadrzaj[:400].rstrip() + ('…' if len(sadrzaj) > 400 else '')

    return {
        'spoljni_id': str(post.get('id')),
        'title': naslov[:500],
        'description': izvod,
        'sadrzaj_tekst': sadrzaj,
        'type': _tip(post),
        'start_date': objavljeno.date() if objavljeno else None,
        'source_link': post.get('link') or SAJT,
        'slika_url': _slika(post),
        'autor': ocisti_tekst(post.get('author_name')) or '',
        'spoljni_izmenjen': _datum(post.get('modified')) or objavljeno,
    }


def preuzmi_objave(*, strana=1, po_strani=PER_PAGE, pomak=None, session=None):
    """Jedna strana WP odgovora. Mrezni/HTTP problem dize izuzetak.

    ``pomak`` (WP ``offset``) ide umesto ``page`` kad se spasava strana koja
    je pala — WP ne dozvoljava oba parametra zajedno.
    """
    klijent = session or requests
    parametri = {
        'per_page': po_strani,
        '_embed': '1',
        'orderby': 'date',
        'order': 'desc',
    }
    if pomak is None:
        parametri['page'] = strana
    else:
        parametri['offset'] = pomak

    odgovor = klijent.get(
        API_URL,
        params=parametri,
        headers=HEADERS,
        timeout=(CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS),
    )
    odgovor.raise_for_status()
    podaci = odgovor.json()
    if not isinstance(podaci, list):
        raise ValueError(
            'WP REST nije vratio listu objava nego %s' % type(podaci).__name__)
    return podaci


def _spasi_stranu(strana, po_strani, session, neuspele_objave):
    """Strana je pala — izvuci objavu po objavu, preskoci samo neispravne.

    Bez ovoga jedna pokvarena objava na sajtu odnese celu stranu vesti.
    """
    pocetak = (strana - 1) * po_strani
    spaseno = []
    for korak in range(po_strani):
        pomak = pocetak + korak
        try:
            spaseno.extend(
                preuzmi_objave(po_strani=1, pomak=pomak, session=session))
        except Exception as exc:
            neuspele_objave.append(pomak)
            logger.warning(
                'Objava na pomaku %d se ne moze preuzeti sa sajta: %s',
                pomak, exc)
    return spaseno


def _upsert(cur, red):
    """Upsert jedne uvezene vesti. Vraca 'nova' ili 'azurirana' ili 'ista'."""
    cur.execute(
        """
        INSERT INTO news_articles (
            izvor, spoljni_id, title, description, sadrzaj_tekst, type,
            start_date, source_link, slika_url, autor, spoljni_izmenjen,
            uvezeno_at, created_at, updated_at
        )
        VALUES (%(izvor)s, %(spoljni_id)s, %(title)s, %(description)s,
                %(sadrzaj_tekst)s, %(type)s, %(start_date)s, %(source_link)s,
                %(slika_url)s, %(autor)s, %(spoljni_izmenjen)s,
                now(), now(), now())
        ON CONFLICT (izvor, spoljni_id) WHERE spoljni_id IS NOT NULL
        DO UPDATE SET
            title            = EXCLUDED.title,
            description      = EXCLUDED.description,
            sadrzaj_tekst    = EXCLUDED.sadrzaj_tekst,
            type             = EXCLUDED.type,
            start_date       = EXCLUDED.start_date,
            source_link      = EXCLUDED.source_link,
            slika_url        = EXCLUDED.slika_url,
            autor            = EXCLUDED.autor,
            spoljni_izmenjen = EXCLUDED.spoljni_izmenjen,
            uvezeno_at       = now(),
            updated_at       = now()
        WHERE news_articles.spoljni_izmenjen IS DISTINCT FROM
                  EXCLUDED.spoljni_izmenjen
           OR news_articles.title         IS DISTINCT FROM EXCLUDED.title
           OR news_articles.description   IS DISTINCT FROM EXCLUDED.description
           OR news_articles.sadrzaj_tekst IS DISTINCT FROM EXCLUDED.sadrzaj_tekst
           OR news_articles.slika_url     IS DISTINCT FROM EXCLUDED.slika_url
           OR news_articles.type          IS DISTINCT FROM EXCLUDED.type
        RETURNING (xmax = 0) AS nova
        """,
        dict(red, izvor=IZVOR),
    )
    ishod = cur.fetchone()
    if ishod is None:
        # ON CONFLICT ... WHERE nije prosao: red postoji i nista se nije menjalo.
        return 'ista'
    return 'nova' if ishod['nova'] else 'azurirana'


def uvezi_vesti(*, strana_od=1, strana_do=DEFAULT_PAGES, pokrenuo='timer',
                session=None):
    """Preuzmi i upisi vesti sa sajta muzeja.

    Vraca {'status', 'novih', 'azuriranih', 'pregledano', 'preskoceno',
    'poruka'} gde je status 'uspeh' | 'delimicno' | 'greska'.

    'delimicno' znaci da su neke objave uvezene a neke se nisu mogle preuzeti —
    to NIJE uspeh i strana ga prikazuje kao upozorenje. Ako se ne moze preuzeti
    nista, upisuje se 'greska' i izuzetak ide dalje pozivaocu.
    """
    novih = azuriranih = pregledano = 0
    neuspele_objave = []
    log_id = None

    with _get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO news_import_log (izvor, pokrenuo) '
                'VALUES (%s, %s) RETURNING id',
                (IZVOR, str(pokrenuo)[:200]),
            )
            log_id = cur.fetchone()['id']
        conn.commit()

        try:
            for strana in range(strana_od, strana_do + 1):
                try:
                    objave = preuzmi_objave(strana=strana, session=session)
                except requests.HTTPError as exc:
                    # Sajt je odgovorio, samo lose (500 na jednoj objavi u
                    # opsegu) — vredi izvuci ostatak strane.
                    logger.warning('Strana %d nije preuzeta (%s) — spasavam '
                                   'objavu po objavu', strana, exc)
                    objave = _spasi_stranu(
                        strana, PER_PAGE, session, neuspele_objave)
                except Exception:
                    # Prekid veze, DNS, timeout: sajt je nedostupan, nema sta
                    # da se spasava i uzrok mora da ostane u tragu takav
                    # kakav jeste, ne prekriven porukom o spasavanju.
                    raise

                if not objave:
                    if not neuspele_objave:
                        break
                    continue

                with conn.cursor() as cur:
                    for post in objave:
                        red = normalizuj(post)
                        if red is None:
                            continue
                        pregledano += 1
                        ishod = _upsert(cur, red)
                        if ishod == 'nova':
                            novih += 1
                        elif ishod == 'azurirana':
                            azuriranih += 1
                conn.commit()

                if len(objave) < PER_PAGE and not neuspele_objave:
                    break
        except Exception as exc:
            conn.rollback()
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE news_import_log SET status = 'greska', "
                    'zavrseno_at = now(), poruka = %s, pregledano = %s '
                    'WHERE id = %s',
                    (str(exc)[:1000], pregledano, log_id),
                )
            conn.commit()
            logger.exception('Uvoz muzejskih vesti sa %s nije uspeo', API_URL)
            raise

        if pregledano == 0 and neuspele_objave:
            greska = RuntimeError(
                'Nijedna objava nije preuzeta; %d pokusaja je palo'
                % len(neuspele_objave))
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE news_import_log SET status = 'greska', "
                    'zavrseno_at = now(), poruka = %s WHERE id = %s',
                    (str(greska), log_id),
                )
            conn.commit()
            raise greska

        status = 'delimicno' if neuspele_objave else 'uspeh'
        poruka = 'Нових: %d · ажурираних: %d · прегледано: %d' % (
            novih, azuriranih, pregledano)
        if neuspele_objave:
            poruka += ' · сајт није вратио %d објав%s' % (
                len(neuspele_objave),
                'у' if len(neuspele_objave) == 1 else 'а',
            )

        with conn.cursor() as cur:
            cur.execute(
                'UPDATE news_import_log SET status = %s, '
                'zavrseno_at = now(), novih = %s, azuriranih = %s, '
                'pregledano = %s, poruka = %s WHERE id = %s',
                (status, novih, azuriranih, pregledano, poruka, log_id),
            )
        conn.commit()

    logger.info('Uvoz muzejskih vesti (%s): %s', status, poruka)
    return {
        'status': status,
        'novih': novih,
        'azuriranih': azuriranih,
        'pregledano': pregledano,
        'preskoceno': len(neuspele_objave),
        'poruka': poruka,
    }


def poslednji_uvoz():
    """Poslednji zapis iz news_import_log ili None."""
    with _get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT id, status, pokrenuto_at, zavrseno_at, novih, '
                'azuriranih, pregledano, poruka, pokrenuo '
                'FROM news_import_log WHERE izvor = %s '
                'ORDER BY pokrenuto_at DESC LIMIT 1',
                (IZVOR,),
            )
            return cur.fetchone()


if __name__ == '__main__':
    import argparse

    from dotenv import load_dotenv

    # Samostalno pokretanje (systemd timer / CLI) nema Flask-ov ucitan .env.
    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    )
    parser = argparse.ArgumentParser(
        description='Uvoz muzejskih vesti sa nhmbeo.rs u news_articles')
    parser.add_argument('--strane', type=int, default=DEFAULT_PAGES,
                        help='Koliko strana po %d objava (podrazumevano %d)'
                             % (PER_PAGE, DEFAULT_PAGES))
    parser.add_argument('--pokrenuo', default='cli')
    argumenti = parser.parse_args()

    ishod = uvezi_vesti(strana_do=max(1, argumenti.strane),
                        pokrenuo=argumenti.pokrenuo)
    print(ishod['poruka'])
