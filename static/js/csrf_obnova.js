/* CSRF обнова: када сервер одговори 400 {error:'csrf_expired', csrf_token}
 * (страница предуго отворена), освежи <meta name="csrf-token">, скривена
 * поља csrf_token и глобални CSRF_TOKEN, па захтев понови ЈЕДНОМ са новим
 * токеном. Омотава window.fetch, па важи и за secureFetch и за сирове fetch
 * позиве; XHR место (чет) користи window.misCsrf.osvezi. */
(function () {
    'use strict';
    if (window.misCsrf) return;
    var izvorniFetch = window.fetch ? window.fetch.bind(window) : null;
    var ZAGLAVLJA = ['X-CSRFToken', 'X-CSRF-Token'];

    function meta() {
        return document.querySelector('meta[name="csrf-token"]');
    }

    function token() {
        var m = meta();
        return m ? m.getAttribute('content') || '' : '';
    }

    function osvezi(novi) {
        if (!novi) return;
        var m = meta();
        if (m) m.setAttribute('content', novi);
        document.querySelectorAll('input[name="csrf_token"]').forEach(function (polje) {
            polje.value = novi;
        });
        try {
            // глобални `let CSRF_TOKEN` из base.html — читају га secureFetch и htmx
            if (typeof CSRF_TOKEN !== 'undefined') CSRF_TOKEN = novi;
        } catch (e) { /* const у старом шаблону — meta је довољна */ }
    }

    function zameniTelo(telo, novi) {
        if (typeof FormData !== 'undefined' && telo instanceof FormData) {
            if (telo.has('csrf_token')) telo.set('csrf_token', novi);
        } else if (typeof URLSearchParams !== 'undefined' && telo instanceof URLSearchParams) {
            if (telo.has('csrf_token')) telo.set('csrf_token', novi);
        } else if (typeof telo === 'string' && /(^|&)csrf_token=/.test(telo)) {
            telo = telo.replace(/(^|&)csrf_token=[^&]*/, '$1csrf_token=' + encodeURIComponent(novi));
        }
        return telo;
    }

    function saNovimTokenom(init, novi) {
        var nov = Object.assign({}, init || {});
        var zaglavlja = new Headers((init && init.headers) || {});
        var imaZaglavlje = false;
        ZAGLAVLJA.forEach(function (ime) {
            if (zaglavlja.has(ime)) { zaglavlja.set(ime, novi); imaZaglavlje = true; }
        });
        if (!imaZaglavlje) zaglavlja.set('X-CSRFToken', novi);
        nov.headers = zaglavlja;
        if (nov.body !== undefined && nov.body !== null) nov.body = zameniTelo(nov.body, novi);
        return nov;
    }

    async function procitajIstek(odgovor) {
        if (odgovor.status !== 400) return null;
        var tip = odgovor.headers.get('Content-Type') || '';
        if (tip.indexOf('application/json') === -1) return null;
        try {
            var podaci = await odgovor.clone().json();
            if (podaci && (podaci.error === 'csrf_expired' || podaci.error === 'csrf_invalid') && podaci.csrf_token) {
                return podaci;
            }
        } catch (e) { /* није JSON */ }
        return null;
    }

    if (izvorniFetch) {
        window.fetch = async function (ulaz, init) {
            var rezerva = (typeof Request !== 'undefined' && ulaz instanceof Request) ? ulaz.clone() : ulaz;
            var odgovor = await izvorniFetch(ulaz, init);
            var istek = await procitajIstek(odgovor);
            if (!istek) return odgovor;
            osvezi(istek.csrf_token);
            if (istek.error !== 'csrf_expired') return odgovor;
            if (rezerva instanceof Request) {
                var zaglavlja = new Headers(rezerva.headers);
                zaglavlja.set('X-CSRFToken', istek.csrf_token);
                return izvorniFetch(new Request(rezerva, { headers: zaglavlja }), init);
            }
            return izvorniFetch(rezerva, saNovimTokenom(init, istek.csrf_token));
        };
    }

    // htmx не понавља сам; бар освежи токен да следећи покушај прође.
    document.addEventListener('htmx:responseError', function (dogadjaj) {
        var xhr = dogadjaj.detail && dogadjaj.detail.xhr;
        if (!xhr || xhr.status !== 400) return;
        try {
            var podaci = JSON.parse(xhr.responseText);
            if (podaci && podaci.csrf_token) osvezi(podaci.csrf_token);
        } catch (e) { /* није JSON */ }
    });

    window.misCsrf = { token: token, osvezi: osvezi };
})();
