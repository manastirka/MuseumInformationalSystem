"""Интерактивни уџбеник — руте (udzbenik.py ради посао).

HTML: листа уџбеника и ЈЕДНА љуска (``udzbenik.html``) за уџбеник, дубоки
линк на лекцију и референтне табеле (списак, једна табела, UGOVOR-TABLICE.md
§4, и детаљ реда табеле, UGOVOR-TABLICE-2.md део 2) — мотор из
static/udzbenik/ црта садржај. API по брифу §4: структура, лекција са
разрешеним блоковима, табела, детаљ реда табеле, напредак (POST, CSRF), CIF
структуре минерала, proxy слике из литературе (SciSearch, само интерно).
Грешке API-ја су увек JSON ``{"greska": ...}`` са правим статусом
(401/403/404/503), никад 200.
"""
import gzip

from flask import (Blueprint, Response, abort, flash, jsonify, redirect, render_template,
                   request, session, url_for)

import scisearch_klijent
import udzbenik
from rate_limit_ext import limiter

udzbenik_bp = Blueprint('udzbenik', __name__)
API_KOREN = '/api/udzbenik'
PRIKAZ_TABLICE = 'tablice'


def _pismo():
    jezik = session.get('museum_lang', request.cookies.get('museum_lang', 'sr-Cyrl')) or ''
    return 'lat' if str(jezik).lower().startswith('sr-latn') else 'cyrl'


def _na_prijavu():
    flash('Морате бити пријављени да бисте приступили овој страници.', 'warning')
    return redirect(url_for('login'))


def _greska(status, poruka):
    return jsonify({'greska': poruka}), status


GZIP_PRAG = 1024


def _prihvata_gzip():
    for deo in request.headers.get('Accept-Encoding', '').lower().split(','):
        ime, _, param = deo.strip().partition(';')
        if ime.strip() == 'gzip':
            return param.replace(' ', '') not in ('q=0', 'q=0.0', 'q=0.00', 'q=0.000')
    return False


def _json_kompresovan(podaci):
    """JSON табеле компресован gzip-ом кад клијент то прихвата: геохемијске табеле
    имају до 2000 редова (~1 MB), а ни nginx ни Flask иначе не компресују JSON."""
    odgovor = jsonify(podaci)
    odgovor.vary.add('Accept-Encoding')
    telo = odgovor.get_data()
    if len(telo) >= GZIP_PRAG and _prihvata_gzip():
        odgovor.set_data(gzip.compress(telo, compresslevel=6))
        odgovor.headers['Content-Encoding'] = 'gzip'
    return odgovor


def _udzbenik_za_html(zbirka):
    """Уџбеник или одговор (redirect/abort) по правилу sme_da_cita."""
    red = udzbenik.dohvati_udzbenik(zbirka)
    if udzbenik.sme_da_cita(red):
        return red, None
    if not udzbenik.prijavljen():
        return None, _na_prijavu()
    if red is None:
        abort(404)
    abort(403)


def _udzbenik_za_api(zbirka):
    red = udzbenik.dohvati_udzbenik(zbirka)
    if udzbenik.sme_da_cita(red):
        return red, None
    if not udzbenik.prijavljen():
        return None, _greska(401, 'Морате бити пријављени')
    if red is None:
        return None, _greska(404, 'Уџбеник не постоји')
    return None, _greska(403, 'Немате дозволу за овај уџбеник')


# --------------------------------------------------------------------------
# HTML
# --------------------------------------------------------------------------

@udzbenik_bp.route('/udzbenik')
def lista():
    if udzbenik.prijavljen() and not udzbenik.ima_modul():
        abort(403)
    udzbenici = udzbenik.lista_udzbenika()
    if not udzbenik.prijavljen() and not udzbenici:
        return _na_prijavu()
    return render_template('udzbenik_lista.html', udzbenici=udzbenici)


@udzbenik_bp.route('/udzbenik/<zbirka>')
def ljuska(zbirka):
    red, odgovor = _udzbenik_za_html(zbirka)
    if odgovor is not None:
        return odgovor
    return _ljuska(red, '', '')


@udzbenik_bp.route('/udzbenik/<zbirka>/<poglavlje>/<lekcija>')
def ljuska_lekcije(zbirka, poglavlje, lekcija):
    red, odgovor = _udzbenik_za_html(zbirka)
    if odgovor is not None:
        return odgovor
    if udzbenik.nadji_lekciju(red, poglavlje, lekcija) is None:
        alias = udzbenik.nadji_alias(red, poglavlje, lekcija)
        if alias is None:
            abort(404)
        return redirect(url_for('udzbenik.ljuska_lekcije', zbirka=zbirka, poglavlje=alias[0], lekcija=alias[1]), 301)
    return _ljuska(red, poglavlje, lekcija)


@udzbenik_bp.route('/udzbenik/<zbirka>/tablice')
def ljuska_tablica(zbirka):
    red, odgovor = _udzbenik_za_html(zbirka)
    if odgovor is not None:
        return odgovor
    return _ljuska(red, '', '', tablica='', prikaz=PRIKAZ_TABLICE)


@udzbenik_bp.route('/udzbenik/<zbirka>/tablice/<slug>')
def ljuska_tablice(zbirka, slug):
    red, odgovor = _udzbenik_za_html(zbirka)
    if odgovor is not None:
        return odgovor
    if not udzbenik.tablica_vidljiva(red, slug):
        abort(404)
    return _ljuska(red, '', '', tablica=slug, prikaz=PRIKAZ_TABLICE)


@udzbenik_bp.route('/udzbenik/<zbirka>/tablice/<slug>/<kljuc>')
def ljuska_detalja(zbirka, slug, kljuc):
    red, odgovor = _udzbenik_za_html(zbirka)
    if odgovor is not None:
        return odgovor
    if not udzbenik.detalj_vidljiv(red, slug, kljuc):
        abort(404)
    return _ljuska(red, '', '', tablica=slug, prikaz=PRIKAZ_TABLICE, detalj=kljuc)


def _ljuska(red, poglavlje, lekcija, tablica='', prikaz='', detalj=''):
    return render_template(
        'udzbenik.html', udzbenik=red, poglavlje=poglavlje, lekcija=lekcija, pismo=_pismo(),
        tablica=tablica, prikaz=prikaz, detalj=detalj,
        api=url_for('udzbenik.api_struktura', zbirka=red['zbirka']), api_koren=API_KOREN,
    )


# --------------------------------------------------------------------------
# API
# --------------------------------------------------------------------------

@udzbenik_bp.route(API_KOREN + '/<zbirka>')
@limiter.limit("120 per minute")
def api_struktura(zbirka):
    red, odgovor = _udzbenik_za_api(zbirka)
    if odgovor is not None:
        return odgovor
    return jsonify(udzbenik.struktura(red))


@udzbenik_bp.route(API_KOREN + '/<zbirka>/lekcija/<poglavlje>/<lekcija>')
@limiter.limit("120 per minute")
def api_lekcija(zbirka, poglavlje, lekcija):
    red, odgovor = _udzbenik_za_api(zbirka)
    if odgovor is not None:
        return odgovor
    podaci = udzbenik.lekcija(red, poglavlje, lekcija)
    if podaci is None:
        alias = udzbenik.nadji_alias(red, poglavlje, lekcija)
        if alias is not None:
            return redirect(url_for('udzbenik.api_lekcija', zbirka=zbirka, poglavlje=alias[0], lekcija=alias[1]), 301)
        return _greska(404, 'Лекција не постоји')
    return jsonify(podaci)


@udzbenik_bp.route(API_KOREN + '/<zbirka>/tablica/<slug>')
@limiter.limit("120 per minute")
def api_tablica(zbirka, slug):
    red, odgovor = _udzbenik_za_api(zbirka)
    if odgovor is not None:
        return odgovor
    podaci = udzbenik.tablica(red, slug)
    if podaci is None:
        return _greska(404, 'Табела не постоји')
    return _json_kompresovan(podaci)


@udzbenik_bp.route(API_KOREN + '/<zbirka>/tablica/<slug>/detalj/<kljuc>')
@limiter.limit("120 per minute")
def api_detalj_tablice(zbirka, slug, kljuc):
    red, odgovor = _udzbenik_za_api(zbirka)
    if odgovor is not None:
        return odgovor
    podaci = udzbenik.detalj_tablice(red, slug, kljuc)
    if podaci is None:
        return _greska(404, 'Детаљ реда табеле не постоји')
    return jsonify(podaci)


@udzbenik_bp.route(API_KOREN + '/napredak', methods=['POST'])
@limiter.limit("120 per minute")
def api_napredak():
    try:
        return jsonify(udzbenik.upisi_napredak(request.get_json(silent=True)))
    except udzbenik.GreskaZahteva as exc:
        return jsonify({'ok': False, 'greska': exc.poruka}), exc.status


@udzbenik_bp.route(API_KOREN + '/struktura/<mineral>')
@limiter.limit("120 per minute")
def api_struktura_minerala(mineral):
    """CIF јединичне ћелије (text/plain, P1) под правом модула ``udzbenik``.
    Параметар ``prikaz`` је укинут — суперћелију гради мотор на клијенту."""
    if not udzbenik.prijavljen():
        return _greska(401, 'Морате бити пријављени')
    if not udzbenik.ima_modul():
        return _greska(403, 'Немате дозволу за модул уџбеника')
    if 'prikaz' in request.args:
        return _greska(400, 'Параметар prikaz је укинут: API враћа само P1 јединичну ћелију, '
                            'суперћелија се гради у мотору на клијенту')
    try:
        cif = udzbenik.cif_strukture(mineral)
    except udzbenik.GreskaZahteva as exc:
        return _greska(exc.status, exc.poruka)
    odgovor = Response(cif, mimetype='text/plain')
    odgovor.headers['Content-Type'] = 'text/plain; charset=utf-8'
    odgovor.headers['Cache-Control'] = 'private, max-age=3600'
    return odgovor


@udzbenik_bp.route(API_KOREN + '/literatura-slika/<int:figura_id>')
@limiter.limit("120 per minute")
def api_literatura_slika(figura_id):
    return _literatura_slika(figura_id, mala=False)


@udzbenik_bp.route(API_KOREN + '/literatura-slika/<int:figura_id>/thumb')
@limiter.limit("120 per minute")
def api_literatura_slika_mala(figura_id):
    return _literatura_slika(figura_id, mala=True)


def _literatura_slika(figura_id, mala):
    """Proxy слике из SciSearch-а (MIS-UGOVOR-SLIKE.md §2): пријављени са
    модулом уџбеника; остали само слику под слободном лиценцом из јавног
    уџбеника, иначе анонимном 404 (рута му „не постоји“). Токен иде само
    ка SciSearch-у, клијенту никад; одговор је ``private`` за кеш прегледача."""
    if not udzbenik.sme_sliku_literature() and not udzbenik.figura_javno_slobodna(figura_id):
        if not udzbenik.prijavljen():
            return _greska(404, 'Не постоји')
        return _greska(403, 'Немате дозволу за модул уџбеника')
    try:
        bajtovi, tip = scisearch_klijent.preuzmi_sliku(figura_id, mala=mala)
    except scisearch_klijent.SciSearchNemaFigure:
        return _greska(404, 'Слика не постоји у библиотеци')
    except scisearch_klijent.SciSearchNijePodesen:
        return _greska(503, 'Библиотека није повезана')
    except scisearch_klijent.SciSearchGreska as exc:
        udzbenik.logger.warning('Уџбеник: слика из литературе %s није преузета: %s', figura_id, exc.razlog)
        return _greska(503, 'Библиотека тренутно није доступна')
    odgovor = Response(bajtovi, mimetype=tip)
    odgovor.headers['Cache-Control'] = 'private, max-age=604800'
    odgovor.headers['Content-Length'] = str(len(bajtovi))
    return odgovor
