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
"""
import logging
import os
import re
import threading
import time

import requests

logger = logging.getLogger(__name__)

TIMEOUT_S = 4
KES_TRAJANJE_S = 10 * 60
NAJVISE_REZULTATA = 8
NAJVISE_ZNAKOVA_ISECKA = 400
RAZLOG_NIJE_PODESEN = 'biblioteka nije povezana'

_TAG_RE = re.compile(r'<[^>]*>')
_MARK_RE = re.compile(r'^</?mark>$', re.IGNORECASE)
_kes = {}
_kes_brava = threading.Lock()


class SciSearchGreska(Exception):
    """SciSearch није дао резултате; ``razlog`` је кратак текст за лог."""

    def __init__(self, razlog):
        super().__init__(razlog)
        self.razlog = razlog


class SciSearchNijePodesen(SciSearchGreska):
    def __init__(self):
        super().__init__(RAZLOG_NIJE_PODESEN)


def _podesavanja():
    url = (os.environ.get('SCISEARCH_URL') or '').strip().rstrip('/')
    token = (os.environ.get('SCISEARCH_SVC_TOKEN') or '').strip()
    return url, token


def podesen():
    url, token = _podesavanja()
    return bool(url and token)


def ocisti_kes():
    with _kes_brava:
        _kes.clear()


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
