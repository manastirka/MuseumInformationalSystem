"""QR руте: резолвер, налепнице, кутије минералошке збирке и API за телефон.

Наслеђени облик `/qr_box/minerals/<kutija>` остаје заувек — налепнице са њим
су залепљене на кутијама (носе адресу старог сервера 192.168.144.48, коју
nginx на тој адреси преусмерава овамо; види deploy/nginx_qr_stara_adresa.conf).
Остали стари облици (`/qr_view/…`, `?highlight=`) никад нису одштампани и
уклоњени су.
"""

import logging

from flask import (
    Blueprint, abort, flash, jsonify, redirect, render_template,
    request, session, url_for,
)

import museum_qr
from rate_limit_ext import limiter
from security_utils import login_required, module_access_required

logger = logging.getLogger(__name__)

qr_bp = Blueprint('qr', __name__)


def _ko():
    return session.get('user_email') or session.get('username') or 'непознат'


def _nepoznata(oznaka):
    return (
        render_template(
            'error.html',
            error_title='Непозната QR ознака',
            error_message=f'Ознака „{oznaka}” није у систему. Проверите да ли је налепница из МИС-а.',
        ),
        404,
    )


# --------------------------------------------------------------------------
# Резолвер — оно што телефон отвара
# --------------------------------------------------------------------------

@qr_bp.route('/q/<oznaka>')
@limiter.limit("60 per minute")
def resolver(oznaka):
    """Јавно: ознака → детаљи (пријављен са приступом) или јавна картица."""
    try:
        red, opis = museum_qr.razresi(oznaka)
    except museum_qr.NepoznataOznaka:
        return _nepoznata(oznaka)
    except museum_qr.NepoznatObjekat:
        return (
            render_template(
                'error.html',
                error_title='Запис више не постоји',
                error_message=f'Ознака „{oznaka}” је важећа, али запис на који показује је обрисан.',
            ),
            410,
        )

    if red['vrsta'] == museum_qr.VRSTA_KUTIJA:
        return _prikaz_kutije(red['objekat_id'])

    if museum_qr.korisnik_ima_pristup(red['zbirka']):
        return redirect(museum_qr.url_detalja(red['zbirka'], red['objekat_id']))

    return render_template(
        'qr_kartica.html',
        vrsta=red['vrsta'],
        oznaka=red['oznaka'],
        naslov=opis['naslov'],
        katalog=opis.get('katalog', ''),
        zbirka=museum_qr.naziv_zbirke(red['zbirka']),
        polja=museum_qr.javna_polja(red['zbirka'], opis['zapis']),
        prijavljen='user_id' in session,
        url_prijave=url_for('login', next=url_for('qr.resolver', oznaka=red['oznaka'])),
    )


@qr_bp.route('/qr_box/minerals/<kutija>')
@limiter.limit("60 per minute")
def kutija_minerala(kutija):
    """Јавно: садржај кутије минералошке збирке. Облик је ЗАЛЕПЉЕН на кутијама."""
    return _prikaz_kutije(kutija)


def _prikaz_kutije(kutija):
    kutija = str(kutija or '').strip()
    try:
        minerali = museum_qr.kutija_minerali(kutija)
    except Exception as exc:
        logger.error("Кутија %s: база минерала није доступна: %s", kutija, exc)
        return (
            render_template('error.html', error_title='Грешка',
                            error_message='База минерала тренутно није доступна.'),
            503,
        )
    if not minerali:
        return (
            render_template('error.html', error_title='Кутија није пронађена',
                            error_message=f'Кутија „{kutija}” није пронађена или је празна.'),
            404,
        )
    return render_template(
        'qr_kartica.html',
        vrsta=museum_qr.VRSTA_KUTIJA,
        oznaka=None,
        naslov=f'Кутија {kutija}',
        katalog=kutija,
        zbirka='Минералошка збирка',
        minerali=minerali,
        prijavljen='user_id' in session,
        moze_detalji=museum_qr.korisnik_ima_pristup(museum_qr.ZBIRKA_MINERALI),
        url_prijave=url_for('login', next=request.path),
    )


# --------------------------------------------------------------------------
# API за телефон
# --------------------------------------------------------------------------

@qr_bp.route('/api/q/<oznaka>')
@limiter.limit("60 per minute")
def api_oznaka(oznaka):
    """JSON: шта је скенирано. Јавно — исто што и картица, без поља записа."""
    try:
        red, opis = museum_qr.razresi(oznaka)
    except museum_qr.NepoznataOznaka:
        return jsonify({'ok': False, 'error': 'Непозната ознака'}), 404
    except museum_qr.NepoznatObjekat:
        return jsonify({'ok': False, 'error': 'Запис више не постоји'}), 410
    return jsonify(museum_qr.opis_za_api(red, opis))


@qr_bp.route('/api/q/kutija/minerali/<kutija>')
@limiter.limit("60 per minute")
def api_kutija(kutija):
    """JSON за стари облик налепнице на кутији (Android парсира путању)."""
    kutija = str(kutija or '').strip()
    try:
        minerali = museum_qr.kutija_minerali(kutija)
    except Exception as exc:
        logger.error("API кутија %s: %s", kutija, exc)
        return jsonify({'ok': False, 'error': 'База минерала није доступна'}), 503
    if not minerali:
        return jsonify({'ok': False, 'error': 'Кутија није пронађена'}), 404
    return jsonify({
        'ok': True,
        'vrsta': museum_qr.VRSTA_KUTIJA,
        'zbirka': museum_qr.ZBIRKA_MINERALI,
        'objekat_id': kutija,
        'naslov': f'Кутија {kutija}',
        'broj_minerala': len(minerali),
        'minerali': [
            {'id': m.get('id'), 'inventarni_broj': m.get('inventarni_broj', ''),
             'naziv': m.get('naziv', ''), 'lokalitet': m.get('lokalitet', '')}
            for m in minerali
        ],
        'url_detalja': url_for('qr.kutija_minerala', kutija=kutija),
    })


@qr_bp.route('/api/qr/dodeli', methods=['POST'])
@login_required
def api_dodeli():
    """Додели ознаку објекту (идемпотентно) — зове дугме у детаљима."""
    podaci = request.get_json(silent=True) or {}
    vrsta = str(podaci.get('vrsta') or museum_qr.VRSTA_PRIMERAK).strip()
    zbirka = museum_qr.normalizuj_zbirku(podaci.get('zbirka'))
    objekat_id = str(podaci.get('objekat_id') or '').strip()
    if vrsta not in museum_qr.VRSTE or not zbirka or not objekat_id:
        return jsonify({'ok': False, 'error': 'Недостају vrsta, zbirka или objekat_id'}), 400
    if not museum_qr.zbirka_config(zbirka):
        return jsonify({'ok': False, 'error': 'Непозната збирка'}), 400
    if not museum_qr.korisnik_ima_pristup(zbirka):
        return jsonify({'ok': False, 'error': 'Немате приступ овој збирци'}), 403
    if vrsta == museum_qr.VRSTA_PRIMERAK and museum_qr.dohvati_zapis(zbirka, objekat_id) is None:
        return jsonify({'ok': False, 'error': 'Запис не постоји'}), 404
    try:
        red = museum_qr.dodeli_oznaku(vrsta, zbirka, objekat_id, _ko())
    except Exception as exc:
        logger.error("Додела QR ознаке %s/%s/%s није успела: %s", vrsta, zbirka, objekat_id, exc)
        return jsonify({'ok': False, 'error': 'Ознака није уписана — база није доступна'}), 503
    return jsonify({
        'ok': True,
        'oznaka': red['oznaka'],
        'stampano_puta': red['stampano_puta'],
        'url_nalepnice': url_for('qr.nalepnica', oznaka=red['oznaka']),
        'sadrzaj': museum_qr.sadrzaj_koda(red),
    })


# --------------------------------------------------------------------------
# Налепнице
# --------------------------------------------------------------------------

@qr_bp.route('/q/<oznaka>/nalepnica')
@login_required
def nalepnica(oznaka):
    """Једна налепница спремна за штампу; бележи припрему за штампу."""
    try:
        red, opis = museum_qr.razresi(oznaka)
    except (museum_qr.NepoznataOznaka, museum_qr.NepoznatObjekat):
        return _nepoznata(oznaka)
    if not museum_qr.korisnik_ima_pristup(red['zbirka']):
        abort(403)

    format_kljuc = request.args.get('format') or museum_qr.PODRAZUMEVANI_FORMAT[red['vrsta']]
    if format_kljuc not in museum_qr.FORMATI:
        abort(400)
    try:
        kopija = max(1, min(int(request.args.get('kopija', 1)), museum_qr.NAJVISE_NA_LISTU))
    except ValueError:
        kopija = 1
    red = museum_qr.zabelezi_stampu(red['oznaka'], _ko()) or red
    sadrzaj = museum_qr.sadrzaj_koda(red)
    nalepnice = [{
        'oznaka': red['oznaka'],
        'svg': museum_qr.svg_kod(sadrzaj),
        'naslov': opis['naslov'],
        'katalog': opis.get('katalog', ''),
        'sazetak': opis.get('sazetak', ''),
        'sadrzaj': sadrzaj,
    }] * (kopija if format_kljuc == 'list' else 1)
    return render_template(
        'qr_nalepnica.html',
        nalepnice=nalepnice,
        format_kljuc=format_kljuc,
        format=museum_qr.FORMATI[format_kljuc],
        formati=museum_qr.FORMATI,
        red=red,
        kopija=kopija,
        url_nazad=museum_qr.url_detalja(red['zbirka'], red['objekat_id'])
        if red['vrsta'] == museum_qr.VRSTA_PRIMERAK
        else url_for('qr.kutije_minerala'),
    )


@qr_bp.route('/admin/qr/kutije/minerali')
@module_access_required('mineral_database')
def kutije_minerala():
    """Избор кутија минералошке збирке за штампу налепница."""
    try:
        kutije, bez_kutije = museum_qr.sve_kutije()
    except Exception as exc:
        logger.error("Списак кутија није учитан: %s", exc)
        flash('База минерала није доступна.', 'danger')
        return redirect(url_for('admin_mineral_collection'))
    return render_template(
        'admin_qr_kutije.html',
        kutije=kutije,
        ukupno_kutija=len(kutije),
        bez_kutije=bez_kutije,
        najvise=museum_qr.NAJVISE_NA_LISTU,
    )


@qr_bp.route('/admin/qr/kutije/minerali/nalepnice', methods=['POST'])
@module_access_required('mineral_database')
def nalepnice_kutija():
    """Налепнице за изабране кутије (А4 лист); свакој кутији додели ознаку."""
    izabrane = [k.strip() for k in request.form.getlist('kutije') if k.strip()]
    if not izabrane:
        flash('Изаберите бар једну кутију.', 'warning')
        return redirect(url_for('qr.kutije_minerala'))
    if len(izabrane) > museum_qr.NAJVISE_NA_LISTU:
        flash(f'Највише {museum_qr.NAJVISE_NA_LISTU} кутија одједном.', 'warning')
        return redirect(url_for('qr.kutije_minerala'))
    nalepnice = []
    try:
        for kutija in izabrane:
            red = museum_qr.dodeli_oznaku(museum_qr.VRSTA_KUTIJA, museum_qr.ZBIRKA_MINERALI, kutija, _ko())
            red = museum_qr.zabelezi_stampu(red['oznaka'], _ko()) or red
            sadrzaj = museum_qr.sadrzaj_koda(red)
            nalepnice.append({
                'oznaka': red['oznaka'],
                'svg': museum_qr.svg_kod(sadrzaj),
                'naslov': f'Кутија {kutija}',
                'katalog': kutija,
                'sazetak': 'Минералошка збирка',
                'sadrzaj': sadrzaj,
            })
    except Exception as exc:
        logger.error("Налепнице кутија нису направљене: %s", exc)
        flash('Налепнице нису направљене — база није доступна.', 'danger')
        return redirect(url_for('qr.kutije_minerala'))
    return render_template(
        'qr_nalepnica.html',
        nalepnice=nalepnice,
        format_kljuc='list',
        format=museum_qr.FORMATI['list'],
        formati=museum_qr.FORMATI,
        red=None,
        kopija=1,
        url_nazad=url_for('qr.kutije_minerala'),
    )


# --------------------------------------------------------------------------
# Генеричка страна детаља за збирке које је немају
# --------------------------------------------------------------------------

@qr_bp.route('/zbirka/<zbirka>/<int:objekat_id>')
@login_required
def detalji_primerka(zbirka, objekat_id):
    """Детаљи једног примерка (све збирке осим минерала, који имају своју страну)."""
    zbirka = museum_qr.normalizuj_zbirku(zbirka)
    cfg = museum_qr.zbirka_config(zbirka)
    if not cfg:
        abort(404)
    if zbirka == museum_qr.ZBIRKA_MINERALI:
        return redirect(url_for('collections.admin_mineral_detail', mineral_id=objekat_id))
    if not museum_qr.korisnik_ima_pristup(zbirka):
        flash('Немате дозволу за приступ овој збирци.', 'danger')
        return redirect(url_for('dashboard'))
    zapis = museum_qr.dohvati_zapis(zbirka, objekat_id)
    if zapis is None:
        abort(404)
    opis = museum_qr.opis_zapisa(zbirka, zapis)
    oznaka = museum_qr.oznaka_za_objekat(museum_qr.VRSTA_PRIMERAK, zbirka, objekat_id)
    labele = museum_qr.labele_polja()
    skrivena = {'id', 'images', 'created_at', 'updated_at', 'measurements', 'coordinates'}
    polja = [
        (labele.get(k, k), v)
        for k, v in zapis.items()
        if k not in skrivena and v not in (None, '', [], {})
    ]
    return render_template(
        'zbirka_detalji.html',
        zbirka=zbirka,
        naziv_zbirke=cfg['name'],
        url_zbirke=url_for(cfg['route']) if cfg.get('route') else url_for('museum_databases'),
        zapis=zapis,
        opis=opis,
        polja=polja,
        oznaka=oznaka,
        objekat_id=objekat_id,
    )
