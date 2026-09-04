/* Сортирање табела кликом на заглавље колоне — за све табеле у апликацији
 * које немају сопствено сортирање.
 *
 * Правила:
 *  - обухвата сваку <table> са <thead> и једним <tbody>; прескаче табелу која
 *    већ има своје сортирање (th.sortable, th.sortable-header, th[data-sort],
 *    линк са sort_by у заглављу) или је означена data-sortiranje="ne"
 *    (на табели или на било ком претку);
 *  - колона се сортира по data-vrednost ћелије ако постоји, иначе по тексту;
 *    тип се утврђује по садржају колоне: број („1.234,56“, „12“, „3,5 kg“),
 *    датум („12.03.2024.“, „2024-03-12“) или текст (српски колатор, ћирилица
 *    и латиница равноправно, бројеви у тексту природно);
 *  - празне ћелије и редови са colspan („Нема података“) увек иду на крај;
 *  - ако страна поново нацрта редове (филтер, претрага), изабрани редослед се
 *    поново примени.
 *
 * Чисте функције су на window.MISSortiranje (за тестове у Node-у).
 */
(function (global) {
    'use strict';

    var SVOJE_SORTIRANJE = 'th.sortable, th.sortable-header, th[data-sort], th a[href*="sort_by"], th[onclick]';
    // Колоне са дугмадима — нема смисла сортирати их.
    var NASLOVI_BEZ_SORTIRANJA = /^(акције|радње|опције|акција|actions?|akcije|radnje|opcije|слика|приказ|#)$/i;
    var BROJ_RE = /^[-+−]?\d{1,3}(?:[.\s\u00a0]\d{3})*(?:,\d+)?$|^[-+−]?\d+(?:[.,]\d+)?$/;
    var BROJ_SA_JEDINICOM_RE = /^([-+−]?[\d.,\s\u00a0]+)\s*(?:%|kg|g|mg|cm|mm|m|km|дин\.?|RSD|€|EUR|\$)?\.?$/i;
    var DATUM_SR_RE = /^(\d{1,2})\.\s?(\d{1,2})\.\s?(\d{4})\.?(?:\s+(\d{1,2}):(\d{2}))?$/;
    var DATUM_ISO_RE = /^(\d{4})-(\d{2})-(\d{2})(?:[T\s](\d{1,2}):(\d{2}))?/;

    var kolator;
    try {
        kolator = new Intl.Collator(['sr', 'sr-Latn', 'en'], { numeric: true, sensitivity: 'base' });
    } catch (e) {
        kolator = { compare: function (a, b) { return a < b ? -1 : a > b ? 1 : 0; } };
    }

    function ocistiTekst(t) {
        return String(t == null ? '' : t).replace(/\s+/g, ' ').trim();
    }

    /* „1.234,56“ → 1234.56; „12“ → 12; „3,5 kg“ → 3.5; иначе null. */
    function uBroj(tekst) {
        var t = ocistiTekst(tekst).replace(/\u00a0/g, ' ');
        if (!t) { return null; }
        var m = BROJ_SA_JEDINICOM_RE.exec(t);
        if (m) { t = m[1].trim(); }
        if (!BROJ_RE.test(t)) { return null; }
        t = t.replace(/^−/, '-');
        if (/,\d+$/.test(t)) {
            t = t.replace(/[.\s]/g, '').replace(',', '.');
        } else if (/^[-+]?\d{1,3}(?:[.\s]\d{3})+$/.test(t)) {
            t = t.replace(/[.\s]/g, '');
        }
        var n = Number(t);
        return isFinite(n) ? n : null;
    }

    /* „12.03.2024.“ / „2024-03-12“ (уз опционо време) → миллисекунде; иначе null. */
    function uDatum(tekst) {
        var t = ocistiTekst(tekst);
        if (!t) { return null; }
        var m = DATUM_SR_RE.exec(t);
        var g, mes, d, h = 0, min = 0;
        if (m) {
            d = +m[1]; mes = +m[2]; g = +m[3]; h = +(m[4] || 0); min = +(m[5] || 0);
        } else {
            m = DATUM_ISO_RE.exec(t);
            if (!m) { return null; }
            g = +m[1]; mes = +m[2]; d = +m[3]; h = +(m[4] || 0); min = +(m[5] || 0);
        }
        if (mes < 1 || mes > 12 || d < 1 || d > 31) { return null; }
        return Date.UTC(g, mes - 1, d, h, min);
    }

    /* Тип колоне по свим непразним вредностима: 'broj' | 'datum' | 'tekst'. */
    function tipKolone(vrednosti) {
        var nepr = vrednosti.filter(function (v) { return ocistiTekst(v) !== ''; });
        if (!nepr.length) { return 'tekst'; }
        if (nepr.every(function (v) { return uBroj(v) !== null; })) { return 'broj'; }
        if (nepr.every(function (v) { return uDatum(v) !== null; })) { return 'datum'; }
        return 'tekst';
    }

    /* Компаратор за две вредности датог типа; празно увек на крај. */
    function uporedi(a, b, tip, smer) {
        var ta = ocistiTekst(a), tb = ocistiTekst(b);
        var praznoA = ta === '', praznoB = tb === '';
        if (praznoA && praznoB) { return 0; }
        if (praznoA) { return 1; }
        if (praznoB) { return -1; }
        var r;
        if (tip === 'broj') {
            r = uBroj(ta) - uBroj(tb);
        } else if (tip === 'datum') {
            r = uDatum(ta) - uDatum(tb);
        } else {
            r = kolator.compare(ta, tb);
        }
        return smer === 'desc' ? -r : r;
    }

    /* Сортира низ {vrednost, indeks} стабилно; враћа редослед индекса. */
    function redosled(vrednosti, smer) {
        var tip = tipKolone(vrednosti);
        var stavke = vrednosti.map(function (v, i) { return { v: v, i: i }; });
        stavke.sort(function (x, y) {
            return uporedi(x.v, y.v, tip, smer) || (x.i - y.i);
        });
        return { tip: tip, indeksi: stavke.map(function (s) { return s.i; }) };
    }

    global.MISSortiranje = { uBroj: uBroj, uDatum: uDatum, tipKolone: tipKolone, uporedi: uporedi, redosled: redosled };

    /* ---------- DOM део (само у прегледачу) ---------- */
    var doc = global.document;
    if (!doc || typeof doc.querySelectorAll !== 'function') { return; }

    var CSS = '\
.srt-zaglavlje{cursor:pointer;user-select:none}\
.srt-zaglavlje:hover,.srt-zaglavlje:focus-visible{text-decoration:underline;text-underline-offset:.2em}\
.srt-zaglavlje::after{content:"\\2195";display:inline-block;margin-left:.35em;opacity:.35;font-size:.85em}\
.srt-zaglavlje[aria-sort="ascending"]::after{content:"\\2191";opacity:1}\
.srt-zaglavlje[aria-sort="descending"]::after{content:"\\2193";opacity:1}';

    function ubaciStil() {
        if (doc.getElementById('srt-stil')) { return; }
        var s = doc.createElement('style');
        s.id = 'srt-stil';
        s.textContent = CSS;
        (doc.head || doc.documentElement).appendChild(s);
    }

    function kandidat(table) {
        if (table.__srt) { return false; }
        if (table.closest('[data-sortiranje="ne"]') || table.querySelector(SVOJE_SORTIRANJE)) {
            table.__srt = 'svoje';  // трајно прескочи — не проверавај при сваком новом реду
            return false;
        }
        var thead = table.tHead;
        if (!thead || !thead.rows.length) { return false; }
        if (table.tBodies.length !== 1) { return false; }
        var red = thead.rows[thead.rows.length - 1];
        for (var i = 0; i < red.cells.length; i++) {
            if (red.cells[i].colSpan > 1) { return false; }
        }
        return red.cells.length >= 2;
    }

    function vrednostCelije(tr, kolona) {
        var td = tr.cells[kolona];
        if (!td) { return ''; }
        if (td.dataset && td.dataset.vrednost != null) { return td.dataset.vrednost; }
        var ulaz = td.querySelector && td.querySelector('input:not([type=checkbox]):not([type=button]), select');
        if (ulaz) { return ulaz.value; }
        return td.textContent;
    }

    function primeniSort(table) {
        var st = table.__srt;
        if (!st || st.kolona == null) { return; }
        var tbody = table.tBodies[0];
        if (!tbody) { return; }
        var redovi = Array.prototype.slice.call(tbody.rows);
        var obicni = [], posebni = [];
        redovi.forEach(function (tr) {
            var poseban = false;
            for (var i = 0; i < tr.cells.length; i++) {
                if (tr.cells[i].colSpan > 1) { poseban = true; break; }
            }
            (poseban ? posebni : obicni).push(tr);
        });
        var vrednosti = obicni.map(function (tr) { return vrednostCelije(tr, st.kolona); });
        var r = redosled(vrednosti, st.smer);
        var novi = r.indeksi.map(function (i) { return obicni[i]; }).concat(posebni);
        var isti = novi.length === redovi.length && novi.every(function (tr, i) { return tr === redovi[i]; });
        if (!isti) {
            // Наше премештање редова изазива мутацију коју посматрач мора да
            // прескочи — иначе би се сортирање вртело у круг.
            st.ocekujMutaciju = true;
            var frag = doc.createDocumentFragment();
            novi.forEach(function (tr) { frag.appendChild(tr); });
            tbody.appendChild(frag);
        }
        var red = table.tHead.rows[table.tHead.rows.length - 1];
        for (var k = 0; k < red.cells.length; k++) {
            var th = red.cells[k];
            if (!th.classList.contains('srt-zaglavlje')) { continue; }
            if (k === st.kolona) {
                th.setAttribute('aria-sort', st.smer === 'asc' ? 'ascending' : 'descending');
            } else {
                th.setAttribute('aria-sort', 'none');
            }
        }
    }

    function klik(table, kolona) {
        var st = table.__srt;
        if (st.kolona === kolona) {
            st.smer = st.smer === 'asc' ? 'desc' : 'asc';
        } else {
            st.kolona = kolona;
            st.smer = 'asc';
        }
        primeniSort(table);
    }

    function pripremi(table) {
        if (!kandidat(table)) { return; }
        ubaciStil();
        var st = { kolona: null, smer: 'asc', ocekujMutaciju: false };
        table.__srt = st;
        var red = table.tHead.rows[table.tHead.rows.length - 1];
        var prviRed = null;
        Array.prototype.some.call(table.tBodies[0] ? table.tBodies[0].rows : [], function (tr) {
            var poseban = Array.prototype.some.call(tr.cells, function (c) { return c.colSpan > 1; });
            if (!poseban && tr.cells.length === red.cells.length) { prviRed = tr; return true; }
            return false;
        });
        Array.prototype.forEach.call(red.cells, function (th, k) {
            var naslov = ocistiTekst(th.textContent);
            if (!naslov || NASLOVI_BEZ_SORTIRANJA.test(naslov)) { return; }
            if (th.querySelector('input, button, select, a')) { return; }
            if (th.dataset && th.dataset.sortiranje === 'ne') { return; }
            // Колона без текста, само дугмад/слике/поља („Акције“, „Слика“) — нема шта да се сортира.
            if (prviRed) {
                var uzorak = prviRed.cells[k];
                if (uzorak && !ocistiTekst(uzorak.textContent) && !(uzorak.dataset && uzorak.dataset.vrednost != null)
                        && uzorak.querySelector('a, button, img, input, select, svg, i')) { return; }
            }
            th.classList.add('srt-zaglavlje');
            th.setAttribute('aria-sort', 'none');
            th.setAttribute('tabindex', '0');
            th.setAttribute('role', 'button');
            if (!th.title) { th.title = 'Сортирај по овој колони'; }
            th.addEventListener('click', function () { klik(table, k); });
            th.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); klik(table, k); }
            });
        });
        if (typeof MutationObserver === 'function' && table.tBodies[0]) {
            var zakazano = false;
            new MutationObserver(function () {
                if (st.ocekujMutaciju) { st.ocekujMutaciju = false; return; }
                if (st.kolona == null || zakazano) { return; }
                zakazano = true;
                (global.requestAnimationFrame || setTimeout)(function () {
                    zakazano = false;
                    primeniSort(table);
                });
            }).observe(table.tBodies[0], { childList: true });
        }
    }

    function pripremiSve(koren) {
        var tabele = (koren && koren.querySelectorAll) ? koren.querySelectorAll('table') : [];
        Array.prototype.forEach.call(tabele, pripremi);
        if (koren && koren.tagName === 'TABLE') { pripremi(koren); }
        // Заглавље попуњено накнадно (JS црта <thead>): провери и табелу-претка.
        var predak = koren && koren.closest && koren.closest('table');
        if (predak) { pripremi(predak); }
    }

    function start() {
        pripremiSve(doc);
        if (typeof MutationObserver === 'function' && doc.body) {
            new MutationObserver(function (mutacije) {
                // Један пролаз по табели, ма колико редова стигло у истом налету.
                var koreni = [];
                mutacije.forEach(function (m) {
                    Array.prototype.forEach.call(m.addedNodes, function (n) {
                        if (n.nodeType !== 1) { return; }
                        var t = (n.tagName === 'TABLE') ? n : (n.closest && n.closest('table'));
                        var koren = t || n;
                        if (koreni.indexOf(koren) === -1) { koreni.push(koren); }
                    });
                });
                koreni.forEach(pripremiSve);
            }).observe(doc.body, { childList: true, subtree: true });
        }
    }

    global.MISSortiranje.pripremi = pripremi;
    global.MISSortiranje.pripremiSve = pripremiSve;

    if (doc.readyState === 'loading') {
        doc.addEventListener('DOMContentLoaded', start);
    } else {
        start();
    }
})(typeof window !== 'undefined' ? window : globalThis);
