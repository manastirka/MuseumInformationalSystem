"""Интерактивни уџбеник — руте (udzbenik.py ради посао).

HTML: листа уџбеника и ЈЕДНА љуска (``udzbenik.html``) за уџбеник и дубоки
линк на лекцију — мотор из static/udzbenik/ црта садржај. API по брифу §4:
структура, лекција са разрешеним блоковима, напредак (POST, CSRF), CIF
структуре минерала. Грешке API-ја су увек JSON ``{"greska": ...}`` са
правим статусом (401/403/404/503), никад 200.
"""
from flask import (Blueprint, Response, abort, flash, jsonify, redirect, render_template,
                   request, session, url_for)

import udzbenik
from rate_limit_ext import limiter

udzbenik_bp = Blueprint('udzbenik', __name__)
API_KOREN = '/api/udzbenik'


def _pismo():
    jezik = session.get('museum_lang', request.cookies.get('museum_lang', 'sr-Cyrl')) or ''
    return 'lat' if str(jezik).lower().startswith('sr-latn') else 'cyrl'


def _na_prijavu():
    flash('Морате бити пријављени да бисте приступили овој страници.', 'warning')
    return redirect(url_for('login'))


def _greska(status, poruka):
    return jsonify({'greska': poruka}), status


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
        abort(404)
    return _ljuska(red, poglavlje, lekcija)


def _ljuska(red, poglavlje, lekcija):
    return render_template(
        'udzbenik.html', udzbenik=red, poglavlje=poglavlje, lekcija=lekcija, pismo=_pismo(),
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
        return _greska(404, 'Лекција не постоји')
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
