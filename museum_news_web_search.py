"""Automatska pretraga veba za vesti o Prirodnjackom muzeju u Beogradu.

Zasto ovo nije prosto "povuci RSS": upit „Природњачки музеј" vraca i vesti o
muzeju u Svilajncu, o muzeju u srcu Kablara, o prirodnjackim muzejima u
Londonu i Becu. Ime je genericko. Zato svaki nalaz dobija OCENU po pojmovima
koji ga vezuju za nas muzej i po pojmovima koji ga vezuju za neki drugi, i
prolazi samo iznad praga.

I posle toga niko ne tvrdi da je bodovanje savrseno: sve sto prodje ide u red
za pregled (tabela news_web_kandidati, migracija 056), a ne pravo medju vesti.
Kustos odobrava. Odbacene ostaju zapisane da ih sledeca pretraga ne nudi opet.

Izvori (oba rade bez API kljuca, provereno 31.08.2026):
  - Google News RSS  — sira pokrivenost (~100 nalaza), bez izvoda, link je
    preusmerenje pa se prava adresa ne vidi iz odgovora
  - Bing News RSS    — manje nalaza (~10), ali ima izvod i pravu adresu
    sakrivenu u parametru ``url`` apiclick veze
"""

import hashlib
import logging
import re
import unicodedata
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup
from psycopg.rows import dict_row

logger = logging.getLogger(__name__)

IZVOR = 'veb'

CONNECT_TIMEOUT_SECONDS = 6
READ_TIMEOUT_SECONDS = 25

HEADERS = {
    'User-Agent': ('Mozilla/5.0 (compatible; MIS-NHMB/1.0; '
                   '+https://nhmbeo.rs/) museum-news-web-search'),
    'Accept': 'application/rss+xml, application/xml, text/xml',
}

GOOGLE_URL = 'https://news.google.com/rss/search'
BING_URL = 'https://www.bing.com/news/search'

# Upiti su namerno uski — trazimo vesti o OVOM muzeju, ne o struci uopste.
# RSS фидови самих медија. Зашто поред Google-а и Bing-а: Google News у
# `link` даје свој омот (`news.google.com/rss/articles/…`) који се не да
# разрешити без недокументованих Google интерних позива — са њега се вуче
# само Google-ов лого, не слика чланка. Фид медија даје ПРАВУ адресу,
# слику и прави извод. Мана: носи само најновије ставке, па историју и
# даље покривају Google и Bing.
#
# Провера 31.08.2026: сви враћају 200 и <item>.
IZVORI_MEDIJA = (
    ('Политика',  'https://www.politika.rs/scc/rss'),
    ('Данас',     'https://www.danas.rs/feed/'),
    ('N1',        'https://n1info.rs/feed/'),
    ('Нова.рс',   'https://nova.rs/feed/'),
    ('Новости',   'https://www.novosti.rs/rss/vesti'),
    ('Blic',      'https://www.blic.rs/rss/danasnje-vesti'),
    ('B92',       'https://www.b92.net/info/rss/vesti.xml'),
    ('RTS',       'https://www.rts.rs/page/stories/sr/rss/1/'),
    ('Курир',     'https://www.kurir.rs/rss/'),
)

UPITI = (
    '"Prirodnjački muzej" Beograd',
    '"Природњачки музеј" Београд',
    '"Prirodnjački muzej u Beogradu"',
    'nhmbeo.rs',
)

# Bodovanje. Tekst se pre poredjenja prebacuje u latinicu bez dijakritike, pa
# su svi pojmovi ispod pisani tako.
# Google News не даје извод, само наслов — а наслови често пишу само
# „Природњачки музеј" без „Београд". Зато сам помен музеја носи довољно
# бодова да пређе праг, а одсецање раде НЕГАТИВНИ појмови (други музеји
# истог имена). Остали позитивни појмови подижу оцену, па ред за преглед
# може да се сортира по поузданости.
# Појмови су РЕГУЛАРНИ ИЗРАЗИ, не обични низови — српски деклинира, па
# „Природњачки музеј", „Природњачког музеја" и „Природњачком музеју" морају
# да се хватају истим правилом. Без тога наслов „Отворена изложба
# Природњачког музеја у Београду" промаши и не стигне до кустоса.
#
# Google News не даје извод, само наслов, а наслови често пишу само
# „Природњачки музеј" без „Београд". Зато сам помен музеја носи довољно
# бодова да пређе праг, а одсецање раде НЕГАТИВНИ појмови (други музеји
# истог имена). Остали позитивни појмови подижу оцену, па ред за преглед
# може да се сортира по поузданости.
POJMOVI_ZA = (
    (r'prirodnjack\w*\s+muzej\w*', 6, 'помиње Природњачки музеј'),
    (r'muzej\w*\s+prirodnjack\w*', 6, 'помиње Природњачки музеј'),
    (r'natural history museum\w*\s+(?:in\s+)?belgrade', 6,
     'помиње музеј на енглеском'),
    (r'\bbeogradu?\b|\bbeogradsk\w*', 3, 'помиње Београд'),
    (r'\bkalemegdan\w*', 3, 'помиње Калемегдан'),
    (r'\bnjegosev\w*', 2, 'помиње адресу музеја'),
    (r'nhmbeo', 5, 'упућује на сајт музеја'),
)

# Други музеји истог генеричког имена. Бодови су довољно негативни да
# надјачају помен музеја и Београда заједно — такав чланак не сме да прође
# ни кад успут спомене Београд.
POJMOVI_PROTIV = (
    (r'\bsvilajn\w*', -9, 'реч је о музеју у Свилајнцу'),
    (r'\bkablar\w*', -9, 'реч је о музеју на Каблару'),
    (r'\blondon\w*', -7, 'реч је о музеју у Лондону'),
    (r'\bbec\b|\bbecu\b|\bbeck\w*', -7, 'реч је о музеју у Бечу'),
    (r'\bva[sz]ingtonu?\b|\bwashington\w*', -7, 'реч је о музеју у Вашингтону'),
    (r'\bzagreb\w*', -7, 'реч је о музеју у Загребу'),
    (r'\bnjujork\w*|\bnew york\b', -7, 'реч је о музеју у Њујорку'),
    (r'\bpariz\w*|\bparis\b', -7, 'реч је о музеју у Паризу'),
    (r'\bberlin\w*', -7, 'реч је о музеју у Берлину'),
)

PRAG = 6

# Sopstvene objave stizu drugim putem (museum_news_importer), ne kroz red.
SOPSTVENI_DOMENI = ('nhmbeo.rs',)

_CIRILICA = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'ђ': 'dj', 'е': 'e',
    'ж': 'z', 'з': 'z', 'и': 'i', 'ј': 'j', 'к': 'k', 'л': 'l', 'љ': 'lj',
    'м': 'm', 'н': 'n', 'њ': 'nj', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
    'т': 't', 'ћ': 'c', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'c',
    'џ': 'dz', 'ш': 's',
}


def _get_postgres_connection(**kwargs):
    from postgres_service import get_postgres_connection
    return get_postgres_connection(**kwargs)


def u_latinicu(tekst):
    """Ćirilica i dijakritika -> gola latinica, za poredjenje pojmova.

    Srpski mediji pisu i jednim i drugim pismom; bez ovoga bi isti pojam
    promasio pola nalaza.
    """
    if not tekst:
        return ''
    niz = []
    for znak in str(tekst).lower():
        niz.append(_CIRILICA.get(znak, znak))
    spojeno = ''.join(niz)
    razlozeno = unicodedata.normalize('NFKD', spojeno)
    return ''.join(z for z in razlozeno if not unicodedata.combining(z))


def normalizuj_naslov(naslov):
    """Naslov -> kljuc za dedup: bez imena medija na kraju i bez interpunkcije."""
    ociscen = re.sub(r'\s+[-–—]\s+[^-–—]{2,40}$', '', naslov or '')
    ociscen = u_latinicu(ociscen)
    ociscen = re.sub(r'[^a-z0-9 ]+', ' ', ociscen)
    return re.sub(r'\s+', ' ', ociscen).strip()


def kljuc_naslova(naslov):
    osnova = normalizuj_naslov(naslov)
    return hashlib.sha256(osnova.encode('utf-8')).hexdigest()[:32]


def oceni(naslov, izvod, url):
    """Vrati (ocena, razlog) — razlog je citljiv spisak sta je dalo bodove."""
    tekst = u_latinicu(' '.join(filter(None, [naslov, izvod, url])))
    ocena = 0
    razlozi = []

    vec_dato = set()
    for obrazac, bodovi, objasnjenje in POJMOVI_ZA + POJMOVI_PROTIV:
        if objasnjenje in vec_dato:
            continue        # два облика истог појма не бодују се двапут
        if re.search(obrazac, tekst):
            ocena += bodovi
            vec_dato.add(objasnjenje)
            razlozi.append('%+d %s' % (bodovi, objasnjenje))

    return ocena, ' · '.join(razlozi) if razlozi else 'нема поклапања'


def _prava_adresa(link):
    """Bing sakriva pravu adresu u parametru ``url`` apiclick veze."""
    if not link:
        return link
    delovi = urlparse(link)
    if 'bing.com' in delovi.netloc:
        skriveno = parse_qs(delovi.query).get('url')
        if skriveno:
            return skriveno[0]
    return link


def _vreme(vrednost):
    if not vrednost:
        return None
    try:
        trenutak = parsedate_to_datetime(vrednost)
    except (TypeError, ValueError):
        return None
    if trenutak is not None and trenutak.tzinfo is None:
        trenutak = trenutak.replace(tzinfo=timezone.utc)
    return trenutak


def _bez_tagova(vrednost):
    if not vrednost:
        return ''
    tekst = re.sub(r'<[^>]+>', ' ', str(vrednost))
    tekst = re.sub(r'&nbsp;?', ' ', tekst)
    return re.sub(r'\s+', ' ', tekst).strip()


def _domen_medija(stavka):
    """Google крије праву адресу иза преусмерења, али <source url> има домен."""
    izvor = stavka.find('source')
    if izvor is not None:
        return (izvor.attrib.get('url') or '').strip()
    return ''


def _slika_iz_stavke(stavka):
    """Слика из RSS ставке: media:content, media:thumbnail или enclosure."""
    for dete in stavka:
        oznaka = dete.tag.rsplit('}', 1)[-1].lower()
        if oznaka in ('content', 'thumbnail', 'enclosure'):
            url = (dete.attrib.get('url') or '').strip()
            tip = (dete.attrib.get('type') or '').lower()
            if not url:
                continue
            if tip and not tip.startswith('image'):
                continue        # видео или аудио прилог, не слика
            if re.search(r'\.(?:mp4|mov|webm|mp3|m4a)(?:\?|$)', url, re.I):
                continue
            if 'youtube.com' in url or 'youtu.be' in url:
                continue        # уграђен видео, не слика чланка
            return url
    # Понеки фид слику држи само у HTML-у описа.
    opis = stavka.findtext('description') or ''
    nadjena = re.search(r'<img[^>]+src=["\']([^"\']+)', opis, re.I)
    return nadjena.group(1) if nadjena else None


def _ime_medija(naslov, stavka):
    """Google nosi ime medija u <source>, Bing u imenovanom prostoru."""
    izvor = stavka.find('source')
    if izvor is not None and (izvor.text or '').strip():
        return izvor.text.strip()
    for dete in stavka:
        if dete.tag.endswith('}Source') and (dete.text or '').strip():
            return dete.text.strip()
    # Poslednji pokusaj: Google lepi „ - Medij" na kraj naslova.
    rep = re.search(r'\s+[-–—]\s+([^-–—]{2,40})$', naslov or '')
    return rep.group(1).strip() if rep else ''


def _skini_medij_iz_naslova(naslov, medij):
    if medij and naslov.endswith(medij):
        return re.sub(r'\s+[-–—]\s+' + re.escape(medij) + r'$', '', naslov).strip()
    return naslov


def _razbori_odgovor(tekst, pretrazivac, upit):
    # ET.fromstring на bytes поштује XML декларацију о кодирању; на str
    # пуца ако фид каже windows-1250 или слично.
    koren = ET.fromstring(tekst)
    nalazi = []
    for stavka in koren.findall('.//item'):
        sirov_naslov = _bez_tagova(stavka.findtext('title'))
        if not sirov_naslov:
            continue
        medij = _ime_medija(sirov_naslov, stavka)
        naslov = _skini_medij_iz_naslova(sirov_naslov, medij)
        url = _prava_adresa((stavka.findtext('link') or '').strip())
        domen_medija = _domen_medija(stavka)
        izvod = _bez_tagova(stavka.findtext('description'))
        # Google u <description> stavlja samo <a> sa naslovom kao tekstom —
        # to nije izvod nego naslov po drugi put, i na ekranu izgleda kao greska.
        if (izvod.startswith('http') or len(izvod) < 25
                or normalizuj_naslov(izvod).startswith(
                    normalizuj_naslov(naslov)[:60])):
            izvod = ''
        nalazi.append({
            'naslov': naslov,
            'url': url,
            'izvod': izvod,
            'izvor_naziv': medij,
            'domen_medija': domen_medija,
            'slika_url': _slika_iz_stavke(stavka),
            'objavljeno': _vreme(stavka.findtext('pubDate')),
            'pretrazivac': pretrazivac,
            'upit': upit,
        })
    return nalazi


def pretrazi_google(upit, *, session=None):
    klijent = session or requests
    odgovor = klijent.get(
        GOOGLE_URL,
        params={'q': upit, 'hl': 'sr', 'gl': 'RS', 'ceid': 'RS:sr'},
        headers=HEADERS,
        timeout=(CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS),
    )
    odgovor.raise_for_status()
    return _razbori_odgovor(odgovor.content, 'google', upit)


def pretrazi_bing(upit, *, session=None):
    klijent = session or requests
    odgovor = klijent.get(
        BING_URL,
        params={'q': upit, 'format': 'RSS'},
        headers=HEADERS,
        timeout=(CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS),
    )
    odgovor.raise_for_status()
    return _razbori_odgovor(odgovor.content, 'bing', upit)


def pretrazi_medij(ime, url_fida, *, session=None):
    """Најновије ставке из фида једног медија, са правом адресом и сликом."""
    klijent = session or requests
    odgovor = klijent.get(
        url_fida, headers=HEADERS,
        timeout=(CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS))
    odgovor.raise_for_status()
    nalazi = _razbori_odgovor(odgovor.content, 'medij', ime)
    for nalaz in nalazi:
        # Фид не носи име медија у ставци — знамо га из самог фида.
        nalaz['izvor_naziv'] = ime
        nalaz['domen_medija'] = url_fida
    return nalazi


def _je_sopstveni_sajt(url):
    domen = (urlparse(url or '').netloc or '').lower()
    return any(domen == d or domen.endswith('.' + d) for d in SOPSTVENI_DOMENI)


def _upisi_kandidata(cur, nalaz, ocena, razlog):
    """Upsert po kljucu naslova. Vraca True samo za stvarno NOV red.

    Postojeci red se NE dira: ako ga je kustos vec odbacio, ponovni nalaz ne
    sme da ga vrati na cekanje.
    """
    cur.execute(
        """
        INSERT INTO news_web_kandidati (
            kljuc, url, naslov, izvod, izvor_naziv, objavljeno, slika_url,
            upit, pretrazivac, ocena, razlog
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (kljuc) DO NOTHING
        RETURNING id
        """,
        (nalaz['kljuc'], nalaz['url'], nalaz['naslov'], nalaz['izvod'] or None,
         nalaz['izvor_naziv'] or None, nalaz['objavljeno'],
         nalaz.get('slika_url') or None, nalaz['upit'],
         nalaz['pretrazivac'], ocena, razlog),
    )
    return cur.fetchone() is not None


OG_NAJVISE_PO_POKRETANJU = 40


def _je_google_omot(url):
    return 'news.google.com' in (urlparse(url or '').netloc or '')


def preuzmi_og_sliku(url, *, session=None):
    """Скини og:image са странице чланка. None кад је нема или страна пукне.

    Ради само над ПРАВОМ адресом: Google-ов омот врати Google-ов лого, што
    је горе од ниједне слике.
    """
    if not url or _je_google_omot(url):
        return None
    klijent = session or requests
    odgovor = klijent.get(
        url, headers=HEADERS,
        timeout=(CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS),
        allow_redirects=True)
    odgovor.raise_for_status()
    if _je_google_omot(odgovor.url):
        return None
    supa = BeautifulSoup(odgovor.content, 'lxml')
    for trazi in ({'property': 'og:image'}, {'name': 'og:image'},
                  {'property': 'twitter:image'}, {'name': 'twitter:image'}):
        oznaka = supa.find('meta', attrs=trazi)
        if oznaka and (oznaka.get('content') or '').strip():
            return oznaka['content'].strip()
    return None


def dopuni_slike(*, najvise=OG_NAJVISE_PO_POKRETANJU, session=None):
    """За кандидате на чекању без слике скини og:image са чланка.

    Враћа (допуњено, покушано). Пад једне странице не руши посао — таква
    вест једноставно остане без слике.
    """
    dopunjeno = pokusano = 0
    with _get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, url FROM news_web_kandidati "
                "WHERE status = 'na_cekanju' AND slika_url IS NULL "
                "  AND url NOT LIKE %s "
                "ORDER BY objavljeno DESC NULLS LAST, id DESC LIMIT %s",
                ('%news.google.com%', int(najvise)))
            redovi = cur.fetchall()

        for red in redovi:
            pokusano += 1
            try:
                slika = preuzmi_og_sliku(red['url'], session=session)
            except Exception as exc:
                logger.info('og:image за %s није скинут: %s',
                            red['url'][:70], exc)
                continue
            if not slika:
                continue
            with conn.cursor() as cur:
                cur.execute(
                    'UPDATE news_web_kandidati SET slika_url = %s '
                    'WHERE id = %s AND slika_url IS NULL',
                    (slika, red['id']))
                dopunjeno += cur.rowcount
            conn.commit()

    if pokusano:
        logger.info('og:image: допуњено %d од %d', dopunjeno, pokusano)
    return dopunjeno, pokusano


def pretrazi_veb(*, upiti=UPITI, izvori_medija=IZVORI_MEDIJA, prag=PRAG,
                 pokrenuo='timer', session=None, dopuni_og=True):
    """Pretrazi veb, oceni nalaze i stavi one iznad praga u red za pregled.

    Vraca {'status', 'novih', 'pregledano', 'odbijeno_ocenom', 'poruka'}.
    Status je 'uspeh' | 'delimicno' | 'greska' — kao i kod uvoza sa sajta,
    pad dela izvora nikad ne prolazi kao pun uspeh.
    """
    pregledano = novih = odbijeno = 0
    neuspeli = []
    vidjeni = set()
    log_id = None

    with _get_postgres_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO news_import_log (izvor, pokrenuo) '
                'VALUES (%s, %s) RETURNING id', (IZVOR, str(pokrenuo)[:200]))
            log_id = cur.fetchone()['id']
        conn.commit()

        # Редослед НИЈЕ произвољан. Дедупликација иде по наслову и прва
        # верзија побеђује, па прво иду извори са најбољим подацима:
        #   1. фидови медија — права адреса, слика, прави извод
        #   2. Bing — права адреса (сакривена у apiclick вези), извод
        #   3. Google — највећи домет, али само наслов и свој омот уместо
        #      адресе, па са њега нема ни слике
        poslovi = [('medij:%s' % ime, ime_fida)
                   for ime, ime_fida in izvori_medija]
        poslovi += [('bing/%s' % u, u) for u in upiti]
        poslovi += [('google/%s' % u, u) for u in upiti]

        def _pokreni(oznaka, argument):
            if oznaka.startswith('medij:'):
                return pretrazi_medij(oznaka[6:], argument, session=session)
            if oznaka.startswith('bing/'):
                return pretrazi_bing(argument, session=session)
            return pretrazi_google(argument, session=session)

        try:
            for oznaka, argument in poslovi:
                try:
                    nalazi = _pokreni(oznaka, argument)
                except Exception as exc:
                    neuspeli.append(oznaka)
                    logger.warning('Извор „%s" није одговорио: %s',
                                   oznaka, exc)
                    continue

                with conn.cursor() as cur:
                    for nalaz in nalazi:
                        nalaz['kljuc'] = kljuc_naslova(nalaz['naslov'])
                        if nalaz['kljuc'] in vidjeni:
                            continue
                        vidjeni.add(nalaz['kljuc'])
                        pregledano += 1

                        if (_je_sopstveni_sajt(nalaz['url'])
                                or _je_sopstveni_sajt(
                                    nalaz.get('domen_medija'))):
                            continue    # stize kroz uvoz sa sajta

                        ocena, razlog = oceni(
                            nalaz['naslov'], nalaz['izvod'], nalaz['url'])
                        if ocena < prag:
                            odbijeno += 1
                            continue
                        if _upisi_kandidata(cur, nalaz, ocena, razlog):
                            novih += 1
                conn.commit()
        except Exception as exc:
            conn.rollback()
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE news_import_log SET status = 'greska', "
                    'zavrseno_at = now(), poruka = %s, pregledano = %s '
                    'WHERE id = %s', (str(exc)[:1000], pregledano, log_id))
            conn.commit()
            logger.exception('Pretraga veba nije uspela')
            raise

        if pregledano == 0 and neuspeli:
            greska = RuntimeError(
                'Nijedan izvor nije odgovorio (%s)' % ', '.join(neuspeli))
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE news_import_log SET status = 'greska', "
                    'zavrseno_at = now(), poruka = %s WHERE id = %s',
                    (str(greska), log_id))
            conn.commit()
            raise greska

        sa_slikom = 0
        # НЕ услављавати ово бројем нових. Кандидати нађени пре него што је
        # допуна слика уведена (или они којима је страна тад била недоступна)
        # иначе никад не би добили слику — допуна ради над свима на чекању
        # који су без ње, ограничено на OG_NAJVISE_PO_POKRETANJU по позиву.
        if dopuni_og:
            try:
                sa_slikom, _ = dopuni_slike(session=session)
            except Exception:
                logger.exception('Допуна слика није успела — вести остају без њих')

        status = 'delimicno' if neuspeli else 'uspeh'
        poruka = 'Нових за преглед: %d · прегледано: %d · испод прага: %d' % (
            novih, pregledano, odbijeno)
        if sa_slikom:
            poruka += ' · слика догледано: %d' % sa_slikom
        if neuspeli:
            poruka += ' · није одговорило: %s' % ', '.join(neuspeli)

        with conn.cursor() as cur:
            cur.execute(
                'UPDATE news_import_log SET status = %s, zavrseno_at = now(), '
                'novih = %s, pregledano = %s, poruka = %s WHERE id = %s',
                (status, novih, pregledano, poruka, log_id))
        conn.commit()

    logger.info('Pretraga veba (%s): %s', status, poruka)
    return {
        'status': status,
        'novih': novih,
        'pregledano': pregledano,
        'odbijeno_ocenom': odbijeno,
        'poruka': poruka,
    }


if __name__ == '__main__':
    import argparse

    from dotenv import load_dotenv
    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    parser = argparse.ArgumentParser(
        description='Pretraga veba za vesti o Prirodnjackom muzeju u Beogradu')
    parser.add_argument('--prag', type=int, default=PRAG)
    parser.add_argument('--pokrenuo', default='cli')
    parser.add_argument('--samo-slike', action='store_true',
                        dest='samo_slike',
                        help='само допуни слике постојећим кандидатима, '
                             'без нове претраге')
    a = parser.parse_args()

    if a.samo_slike:
        dopunjeno, pokusano = dopuni_slike()
        print('Слика допуњено: %d од %d покушаних' % (dopunjeno, pokusano))
    else:
        print(pretrazi_veb(prag=a.prag, pokrenuo=a.pokrenuo)['poruka'])
