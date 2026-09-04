/* Глобална претрага (Ctrl+K / ⌘K): модал са једним пољем, резултати из
 * /api/pretraga груписани по бази; стрелице ↑↓ + Enter, Esc затвара. */
(function () {
    'use strict';
    var modalEl = document.getElementById('pretragaModal');
    if (!modalEl || typeof bootstrap === 'undefined') { return; }
    var polje = modalEl.querySelector('#pretragaPolje');
    var rezultati = modalEl.querySelector('#pretragaRezultati');
    var modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    var tajmer = null, poslednji = '', aktivan = -1, kontroler = null;

    function esc(t) {
        return String(t == null ? '' : t).replace(/[&<>"']/g, function (c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
        });
    }

    function poruka(html) { rezultati.innerHTML = '<div class="pretraga-poruka">' + html + '</div>'; aktivan = -1; }

    function nacrtaj(podaci) {
        if (podaci.prekratko) { poruka('Унесите бар два знака.'); return; }
        if (!podaci.grupe.length) { poruka('Нема резултата за „' + esc(podaci.upit) + '“.'); return; }
        var h = '';
        podaci.grupe.forEach(function (g) {
            h += '<div class="pretraga-grupa"><div class="pretraga-grupa-naslov"><i class="bi ' + esc(g.ikona) + '" aria-hidden="true"></i>' + esc(g.naziv);
            if (g.jos) { h += '<a class="pretraga-jos" href="' + esc(g.jos) + '">сви резултати →</a>'; }
            h += '</div>';
            g.stavke.forEach(function (s) {
                h += '<a class="pretraga-stavka" href="' + esc(s.url) + '" role="option"><span class="pretraga-naslov">' + esc(s.naslov) + '</span>'
                   + (s.opis ? '<span class="pretraga-opis">' + esc(s.opis) + '</span>' : '') + '</a>';
            });
            h += '</div>';
        });
        rezultati.innerHTML = h;
        aktivan = -1;
        oznaci(0);
    }

    function stavke() { return Array.prototype.slice.call(rezultati.querySelectorAll('.pretraga-stavka')); }

    function oznaci(i) {
        var s = stavke();
        if (!s.length) { aktivan = -1; return; }
        if (i < 0) { i = s.length - 1; }
        if (i >= s.length) { i = 0; }
        s.forEach(function (el, k) { el.classList.toggle('aktivna', k === i); });
        aktivan = i;
        s[i].scrollIntoView({ block: 'nearest' });
    }

    function trazi() {
        var q = polje.value.trim();
        if (q === poslednji) { return; }
        poslednji = q;
        if (q.length < 2) { poruka(q ? 'Унесите бар два знака.' : 'Инвентарни број, назив, локалитет, књига, запослени, досије, фотографија…'); return; }
        if (kontroler) { kontroler.abort(); }
        kontroler = new AbortController();
        poruka('<span class="spinner-border spinner-border-sm me-2" role="status"></span>Тражим…');
        fetch('/api/pretraga?q=' + encodeURIComponent(q), { credentials: 'same-origin', signal: kontroler.signal, headers: { 'Accept': 'application/json' } })
            .then(function (r) { if (!r.ok) { throw new Error(r.status); } return r.json(); })
            .then(function (p) { if (polje.value.trim() === q) { nacrtaj(p); } })
            .catch(function (e) { if (e.name !== 'AbortError') { poruka('Претрага тренутно није доступна.'); } });
    }

    polje.addEventListener('input', function () {
        clearTimeout(tajmer);
        tajmer = setTimeout(trazi, 220);
    });
    polje.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowDown') { e.preventDefault(); oznaci(aktivan + 1); }
        else if (e.key === 'ArrowUp') { e.preventDefault(); oznaci(aktivan - 1); }
        else if (e.key === 'Enter') {
            var s = stavke();
            if (aktivan >= 0 && s[aktivan]) { e.preventDefault(); window.location.href = s[aktivan].getAttribute('href'); }
        }
    });
    modalEl.addEventListener('shown.bs.modal', function () { polje.focus(); polje.select(); });
    modalEl.addEventListener('hidden.bs.modal', function () { if (kontroler) { kontroler.abort(); } });

    function otvori() { modal.show(); }
    document.addEventListener('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && !e.altKey && (e.key === 'k' || e.key === 'K' || e.key === 'л' || e.key === 'Л')) {
            e.preventDefault(); otvori();
        }
    });
    document.querySelectorAll('[data-pretraga-otvori]').forEach(function (b) {
        b.addEventListener('click', function (e) { e.preventDefault(); otvori(); });
    });
    poruka('Инвентарни број, назив, локалитет, књига, запослени, досије, фотографија…');
})();
