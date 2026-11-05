"""SciSearch — читајући клијент сервисног API-ја (уговор LITERATURA.md §2).

SciSearch је самосталан сервис са својом базом; МИС га САМО чита преко
``GET /svc/search`` на истом хосту. Подешавање искључиво кроз окружење:

- ``SCISEARCH_URL`` — корен сервиса (прод ``http://127.0.0.1:8010/nauka``,
  dev ``https://192.168.144.194/nauka``);
- ``SCISEARCH_SVC_TOKEN`` — тајна за заглавље ``X-Svc-Token`` (никад у репоу).

Без обе вредности клијент је „неподешен“ и ``pretrazi`` диже
``SciSearchNijePodesen`` — позивалац то поштено преводи у „библиотека није
повезана“. Свака друга грешка (мрежа, timeout 4 s, не-200, лош JSON) диже
``SciSearchGreska`` са разлогом — никад тихо.

Кеш у меморији процеса, 10 минута по (upit, n); кешира се само успех.
``isecak`` сме да садржи само ``<mark>`` — све друге тагове клијент уклања
без обзира на то шта сервис обећава.

Фаза 2 (MIS-UGOVOR-SLIKE.md): ``figura(id)`` чита ``GET /svc/figure/<id>``
(исти кеш 10 минута, кључ ``('figura', id)``), а ``preuzmi_sliku(id, mala)``
стримује ``/svc/figure/<id>.jpg`` или ``/svc/figure/<id>/thumb.jpg``:
timeout 8 s, највише 15 MB, само ``image/jpeg``/``image/png``. Бајтови
слике иду у LRU кеш до 200 MB да се SciSearch не зове за сваки приказ.
Токен никад не напушта клијент (ни у лог, ни у изузетак).
"""
import logging
import os
import re
import threading
import time
from collections import OrderedDict

import requests

logger = logging.getLogger(__name__)

TIMEOUT_S = 4
KES_TRAJANJE_S = 10 * 60
NAJVISE_REZULTATA = 8
NAJVISE_ZNAKOVA_ISECKA = 400
NAJVISE_ZNAKOVA_POTPISA = 500
RAZLOG_NIJE_PODESEN = 'biblioteka nije povezana'
SLIKA_TIMEOUT_S = 8
SLIKA_NAJVISE_BAJTOVA = 15 * 1024 * 1024
SLIKA_KES_NAJVISE_BAJTOVA = 200 * 1024 * 1024
SLIKA_DOZVOLJENI_TIPOVI = ('image/jpeg', 'image/png')
_SLIKA_KOMAD = 64 * 1024

_TAG_RE = re.compile(r'<[^>]*>')
_MARK_RE = re.compile(r'^</?mark>$', re.IGNORECASE)
_kes = {}
_kes_brava = threading.Lock()
_slika_kes = OrderedDict()
_slika_kes_bajtova = 0
_slika_kes_brava = threading.Lock()


class SciSearchGreska(Exception):
    """SciSearch није дао резултате; ``razlog`` је кратак текст за лог."""

    def __init__(self, razlog):
        super().__init__(razlog)
        self.razlog = razlog


class SciSearchNijePodesen(SciSearchGreska):
    def __init__(self):
        super().__init__(RAZLOG_NIJE_PODESEN)


class SciSearchNemaFigure(SciSearchGreska):
    """Сервис је одговорио 404: фигура не постоји, скривена је или је ван
    дозвољених извора — то није пад сервиса."""

    def __init__(self, figura_id):
        super().__init__(f'figura {figura_id} ne postoji')


def _podesavanja():
    url = (os.environ.get('SCISEARCH_URL') or '').strip().rstrip('/')
    token = (os.environ.get('SCISEARCH_SVC_TOKEN') or '').strip()
    return url, token


def podesen():
    url, token = _podesavanja()
    return bool(url and token)


def ocisti_kes():
    global _slika_kes_bajtova
    with _kes_brava:
        _kes.clear()
    with _slika_kes_brava:
        _slika_kes.clear()
        _slika_kes_bajtova = 0


def ocisti_isecak(isecak):
    """Остави само ``<mark>``/``</mark>``; остале тагове уклони, текст
    остави какав је (сервис га већ escape-ује)."""
    tekst = str(isecak or '')

    def _tag(m):
        return m.group(0).lower() if _MARK_RE.match(m.group(0)) else ''
    tekst = _TAG_RE.sub(_tag, tekst)
    if len(tekst) > NAJVISE_ZNAKOVA_ISECKA:
        tekst = tekst[:NAJVISE_ZNAKOVA_ISECKA]
    return tekst


def _ceo(vrednost):
    return vrednost if isinstance(vrednost, int) and not isinstance(vrednost, bool) else None


def _poglavlje(vrednost):
    if not isinstance(vrednost, dict):
        return None
    return {
        'naslov': str(vrednost.get('naslov') or ''),
        'autori': str(vrednost.get('autori') or ''),
        'strana_od': _ceo(vrednost.get('strana_od')),
        'strana_do': _ceo(vrednost.get('strana_do')),
    }


def _rezultat(stavka):
    """Облик из уговора §1 — само позната поља, ``url`` остаје релативан
    (``/nauka/...``) јер је SciSearch на истом хосту као МИС."""
    url = str(stavka.get('url') or '')
    if not url.startswith('/'):
        url = ''
    return {
        'doc_id': _ceo(stavka.get('doc_id')),
        'naslov': str(stavka.get('naslov') or ''),
        'autor': str(stavka.get('autor') or ''),
        'godina': _ceo(stavka.get('godina')),
        'vrsta': str(stavka.get('vrsta') or ''),
        'izvor': str(stavka.get('izvor') or ''),
        'poglavlje': _poglavlje(stavka.get('poglavlje')),
        'strana': _ceo(stavka.get('strana')),
        'isecak': ocisti_isecak(stavka.get('isecak')),
        'url': url,
    }


def pretrazi(upit, broj=3, as_user=None):
    """Листа резултата (највише ``broj``) за ``upit``; празна листа = нема
    резултата. Диже SciSearchNijePodesen / SciSearchGreska."""
    url, token = _podesavanja()
    if not (url and token):
        raise SciSearchNijePodesen()
    upit = ' '.join(str(upit or '').split())
    if not upit:
        return []
    broj = max(1, min(int(broj or 3), NAJVISE_REZULTATA))
    kljuc = (upit, broj)
    sada = time.monotonic()
    with _kes_brava:
        pogodak = _kes.get(kljuc)
        if pogodak and pogodak[0] > sada:
            return [dict(r) for r in pogodak[1]]

    parametri = {'q': upit, 'n': broj, 'mode': 'hybrid'}
    if as_user:
        parametri['as_user'] = as_user
    try:
        odgovor = requests.get(url + '/svc/search', params=parametri,
                               headers={'X-Svc-Token': token}, timeout=TIMEOUT_S)
    except requests.Timeout as exc:
        raise SciSearchGreska(f'timeout после {TIMEOUT_S} s') from exc
    except requests.RequestException as exc:
        raise SciSearchGreska(f'мрежна грешка: {exc}') from exc
    if odgovor.status_code != 200:
        raise SciSearchGreska(f'HTTP {odgovor.status_code}')
    try:
        telo = odgovor.json()
    except ValueError as exc:
        raise SciSearchGreska('одговор није JSON') from exc
    if not isinstance(telo, dict) or not isinstance(telo.get('rezultati'), list):
        raise SciSearchGreska('одговор без поља rezultati')
    rezultati = [_rezultat(s) for s in telo['rezultati'] if isinstance(s, dict)][:broj]
    with _kes_brava:
        _kes[kljuc] = (sada + KES_TRAJANJE_S, rezultati)
    return [dict(r) for r in rezultati]


def zdravlje():
    """``GET /svc/health`` → речник (``{"ok": true, "docs": N}``)."""
    url, token = _podesavanja()
    if not (url and token):
        raise SciSearchNijePodesen()
    try:
        odgovor = requests.get(url + '/svc/health', headers={'X-Svc-Token': token}, timeout=TIMEOUT_S)
    except requests.RequestException as exc:
        raise SciSearchGreska(f'мрежна грешка: {exc}') from exc
    if odgovor.status_code != 200:
        raise SciSearchGreska(f'HTTP {odgovor.status_code}')
    try:
        return odgovor.json()
    except ValueError as exc:
        raise SciSearchGreska('одговор није JSON') from exc


# --------------------------------------------------------------------------
# Фаза 2: фигуре (слике из литературе) — само метаподаци и проксирани бајтови
# --------------------------------------------------------------------------

def _figura_id(figura_id):
    if isinstance(figura_id, bool) or not isinstance(figura_id, int) or figura_id < 1:
        raise SciSearchGreska('figura_id mora biti ceo broj >= 1')
    return figura_id


def _figura(stavka):
    """Облик из уговора §1 (/svc/figure/<id>) — само позната поља; ``potpis``
    је чист текст (тагове уклањамо као и код исечка)."""
    potpis = _TAG_RE.sub('', str(stavka.get('potpis') or ''))
    return {
        'id': _ceo(stavka.get('id')),
        'doc_id': _ceo(stavka.get('doc_id')),
        'strana': _ceo(stavka.get('strana')),
        'sirina': _ceo(stavka.get('sirina')),
        'visina': _ceo(stavka.get('visina')),
        'vrsta': str(stavka.get('vrsta') or ''),
        'potpis': potpis[:NAJVISE_ZNAKOVA_POTPISA],
        'naslov': str(stavka.get('naslov') or ''),
        'autor': str(stavka.get('autor') or ''),
        'godina': _ceo(stavka.get('godina')),
    }


def figura(figura_id):
    """Метаподаци једне фигуре (``GET /svc/figure/<id>``); кеш 10 минута.
    Диже SciSearchNijePodesen / SciSearchNemaFigure (404) / SciSearchGreska."""
    url, token = _podesavanja()
    if not (url and token):
        raise SciSearchNijePodesen()
    figura_id = _figura_id(figura_id)
    kljuc = ('figura', figura_id)
    sada = time.monotonic()
    with _kes_brava:
        pogodak = _kes.get(kljuc)
        if pogodak and pogodak[0] > sada:
            return dict(pogodak[1])
    try:
        odgovor = requests.get(f'{url}/svc/figure/{figura_id}', headers={'X-Svc-Token': token},
                               timeout=TIMEOUT_S)
    except requests.Timeout as exc:
        raise SciSearchGreska(f'timeout после {TIMEOUT_S} s') from exc
    except requests.RequestException as exc:
        raise SciSearchGreska(f'мрежна грешка: {exc}') from exc
    if odgovor.status_code == 404:
        raise SciSearchNemaFigure(figura_id)
    if odgovor.status_code != 200:
        raise SciSearchGreska(f'HTTP {odgovor.status_code}')
    try:
        telo = odgovor.json()
    except ValueError as exc:
        raise SciSearchGreska('одговор није JSON') from exc
    if not isinstance(telo, dict) or _ceo(telo.get('id')) is None:
        raise SciSearchGreska('одговор без поља id')
    podaci = _figura(telo)
    with _kes_brava:
        _kes[kljuc] = (sada + KES_TRAJANJE_S, podaci)
    return dict(podaci)


def _slika_iz_kesa(kljuc):
    with _slika_kes_brava:
        pogodak = _slika_kes.get(kljuc)
        if pogodak is not None:
            _slika_kes.move_to_end(kljuc)
        return pogodak


def _slika_u_kes(kljuc, bajtovi, tip):
    global _slika_kes_bajtova
    if len(bajtovi) > SLIKA_KES_NAJVISE_BAJTOVA:
        return
    with _slika_kes_brava:
        staro = _slika_kes.pop(kljuc, None)
        if staro is not None:
            _slika_kes_bajtova -= len(staro[0])
        _slika_kes[kljuc] = (bajtovi, tip)
        _slika_kes_bajtova += len(bajtovi)
        while _slika_kes_bajtova > SLIKA_KES_NAJVISE_BAJTOVA and _slika_kes:
            _, (izbaceno, _tip) = _slika_kes.popitem(last=False)
            _slika_kes_bajtova -= len(izbaceno)


def velicina_kesa_slika():
    with _slika_kes_brava:
        return _slika_kes_bajtova


def preuzmi_sliku(figura_id, mala=False):
    """(бајтови, content-type) слике фигуре — ``/svc/figure/<id>.jpg`` или
    ``/svc/figure/<id>/thumb.jpg``. Стрим са timeout-ом 8 s, прекид изнад
    15 MB, одбијање свега што није image/jpeg|png. LRU кеш до 200 MB.
    Диже SciSearchNijePodesen / SciSearchNemaFigure (404) / SciSearchGreska."""
    url, token = _podesavanja()
    if not (url and token):
        raise SciSearchNijePodesen()
    figura_id = _figura_id(figura_id)
    kljuc = (figura_id, bool(mala))
    pogodak = _slika_iz_kesa(kljuc)
    if pogodak is not None:
        return pogodak
    putanja = f'/svc/figure/{figura_id}/thumb.jpg' if mala else f'/svc/figure/{figura_id}.jpg'
    try:
        odgovor = requests.get(url + putanja, headers={'X-Svc-Token': token},
                               timeout=SLIKA_TIMEOUT_S, stream=True)
    except requests.Timeout as exc:
        raise SciSearchGreska(f'timeout после {SLIKA_TIMEOUT_S} s') from exc
    except requests.RequestException as exc:
        raise SciSearchGreska(f'мрежна грешка: {exc}') from exc
    try:
        if odgovor.status_code == 404:
            raise SciSearchNemaFigure(figura_id)
        if odgovor.status_code != 200:
            raise SciSearchGreska(f'HTTP {odgovor.status_code}')
        tip = (odgovor.headers.get('Content-Type') or '').split(';')[0].strip().lower()
        if tip not in SLIKA_DOZVOLJENI_TIPOVI:
            raise SciSearchGreska(f'nedozvoljen tip sadržaja: {tip or "?"}')
        duzina = odgovor.headers.get('Content-Length')
        if duzina and duzina.isdigit() and int(duzina) > SLIKA_NAJVISE_BAJTOVA:
            raise SciSearchGreska(f'slika veća od {SLIKA_NAJVISE_BAJTOVA // (1024 * 1024)} MB')
        delovi, ukupno = [], 0
        try:
            for deo in odgovor.iter_content(_SLIKA_KOMAD):
                if not deo:
                    continue
                ukupno += len(deo)
                if ukupno > SLIKA_NAJVISE_BAJTOVA:
                    raise SciSearchGreska(f'slika veća od {SLIKA_NAJVISE_BAJTOVA // (1024 * 1024)} MB')
                delovi.append(deo)
        except requests.RequestException as exc:
            raise SciSearchGreska(f'prekinut prenos: {exc}') from exc
    finally:
        odgovor.close()
    bajtovi = b''.join(delovi)
    if not bajtovi:
        raise SciSearchGreska('prazna slika')
    _slika_u_kes(kljuc, bajtovi, tip)
    return bajtovi, tip
