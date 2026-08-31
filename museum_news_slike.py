"""Lokalna kopija slika za vesti nadjene na vebu.

Zasto uopste: aplikacija salje CSP zaglavlje sa `img-src 'self' data: blob:
*.openstreetmap.org www.facebook.com nhmbeo.rs`. Slika sa politika.rs ili
b92.net ima ispravnu adresu u bazi, ali je pregledac ODBIJA da ucita. Sirenje
te liste na svaki medij bi znacilo menjanje bezbednosne politike pri svakom
novom izvoru, citaocev pregledac bi odlazio na tudje servere, a slika bi
nestala cim je izvor obrise.

Zato se slika preuzme jednom i cuva kod nas, u static/vesti_slike/ — isti
obrazac kao kes plocica karte (maps_terrain_support.resolve_tile_cache_dir).
Servira se sa 'self', pa CSP ostaje netaknut.

Ogranicenja su namerna: samo image/*, najvise NAJVECI_ULAZ bajtova sa mreze,
i sve se prevodi u JPEG sirine do SIRINA_PX. Tudji sadrzaj nikad ne ulazi u
nas prostor u izvornom obliku.
"""

import hashlib
import logging
import os
import tempfile

import requests

logger = logging.getLogger(__name__)

# pyvips на INFO нивоу испише „threadpool completed…" за сваку слику — то
# затрпава траг увоза, а нама не говори ништа.
logging.getLogger('pyvips').setLevel(logging.WARNING)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

CONNECT_TIMEOUT_SECONDS = 6
READ_TIMEOUT_SECONDS = 25
NAJVECI_ULAZ = 8 * 1024 * 1024      # 8 MB sa mreze — dovoljno za svaku novinsku sliku
SIRINA_PX = 900
KVALITET = 82

HEADERS = {
    'User-Agent': ('Mozilla/5.0 (compatible; MIS-NHMB/1.0; '
                   '+https://nhmbeo.rs/) museum-news-images'),
    'Accept': 'image/*,*/*;q=0.8',
}


def resolve_cache_dir():
    """Direktorijum za lokalne kopije; isti obrazac kao kes plocica karte."""
    preferred = os.path.join(APP_ROOT, 'static', 'vesti_slike')
    parent = os.path.dirname(preferred)
    if os.access(parent, os.W_OK):
        return preferred
    return os.environ.get(
        'MUSEUM_NEWS_IMAGE_DIR',
        os.path.join(tempfile.gettempdir(), 'museum_info_system_vesti_slike'),
    )


CACHE_DIR = resolve_cache_dir()


def ime_fajla(url):
    """Stabilno ime po adresi — ista slika se ne preuzima dvaput."""
    return hashlib.sha256((url or '').encode('utf-8')).hexdigest()[:32] + '.jpg'


def putanja(ime):
    return os.path.join(CACHE_DIR, ime)


def postoji(ime):
    return bool(ime) and os.path.exists(putanja(ime))


def _u_jpeg(podaci, cilj):
    """Prevedi u JPEG sirine do SIRINA_PX. Vraca True kad je fajl nastao."""
    import pyvips

    slika = pyvips.Image.new_from_buffer(podaci, '')
    if slika.width > SIRINA_PX:
        slika = slika.thumbnail_image(SIRINA_PX)
    # Neke novinske slike su CMYK ili imaju alfa kanal; JPEG trazi sRGB bez alfe.
    if slika.bands == 4 and slika.interpretation != 'cmyk':
        slika = slika.flatten(background=[255, 255, 255])
    slika = slika.colourspace('srgb')

    privremeni = cilj + '.novi'
    slika.jpegsave(privremeni, Q=KVALITET, strip=True, optimize_coding=True)
    # Preimenovanje je atomicno: strana koja cita nikad ne vidi pola fajla.
    os.replace(privremeni, cilj)
    return True


def preuzmi(url, *, session=None):
    """Preuzmi sliku i sacuvaj lokalnu kopiju. Vraca ime fajla ili None.

    Ne dize izuzetak: vest bez slike je i dalje upotrebljiva vest, pa pad
    jedne slike ne sme da obori uvoz. Razlog se upisuje u log.
    """
    if not url:
        return None

    ime = ime_fajla(url)
    cilj = putanja(ime)
    if os.path.exists(cilj):
        return ime

    os.makedirs(CACHE_DIR, exist_ok=True)
    klijent = session or requests

    try:
        odgovor = klijent.get(
            url, headers=HEADERS, stream=True,
            timeout=(CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS))
        odgovor.raise_for_status()

        tip = (odgovor.headers.get('Content-Type') or '').lower()
        if tip and not tip.startswith('image/'):
            logger.info('Preskacem %s — nije slika nego %s', url[:70], tip)
            return None

        podaci = b''
        for deo in odgovor.iter_content(64 * 1024):
            podaci += deo
            if len(podaci) > NAJVECI_ULAZ:
                logger.info('Preskacem %s — veca od %d B', url[:70], NAJVECI_ULAZ)
                return None
        if not podaci:
            return None

        _u_jpeg(podaci, cilj)
    except Exception as exc:
        logger.info('Slika %s nije sacuvana: %s', url[:70], exc)
        # Полу-написан фајл не сме да остане иза грешке.
        for ostatak in (cilj + '.novi', cilj):
            try:
                if os.path.exists(ostatak) and not os.path.getsize(ostatak):
                    os.remove(ostatak)
            except OSError:
                pass
        return None

    return ime
