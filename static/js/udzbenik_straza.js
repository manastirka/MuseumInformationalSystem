/* Стража љуске уџбеника (templates/udzbenik.html).
   Мотор (static/udzbenik/udzbenik.js, ES модул) замењује „Учитавање уџбеника…“
   чим се покрене. Ако после data-straza-ms (подразумевано 8000 ms) то није
   урадио — модул пукао на import-у, скрипт блокиран, без одговора — читалац
   не сме да гледа вечни „Учитавање…“: прикаже се <template id="udzbenik-straza">
   (ћирилица у шаблону, translator.js је пресловљава) са дугметом за поновно
   учитавање, а разлог иде у console.error.
   Класичан скрипт, учитан ПРЕ модула: тако хвата и грешку повезивања модула
   (SyntaxError из import-а, 2026-11-09) преко window 'error'. Без текста УИ-ја
   у JS-у — он је у шаблону. */
(function () {
    'use strict';
    var app = document.getElementById('udzbenik-app');
    if (!app) return;
    var greske = [];

    function zabelezi(poruka) {
        if (poruka) greske.push(String(poruka).slice(0, 300));
    }

    window.addEventListener('error', function (e) {
        if (e.message) {
            var gde = e.filename ? ' (' + e.filename.replace(/^.*\//, '') + ':' + e.lineno + ')' : '';
            zabelezi(e.message + gde);
            return;
        }
        var cilj = e.target;
        if (cilj && cilj.tagName === 'SCRIPT' && cilj.src) {
            zabelezi('skript nije učitan: ' + cilj.src.replace(/^.*\//, ''));
        }
    }, true);
    window.addEventListener('unhandledrejection', function (e) {
        var r = e.reason;
        zabelezi(r && (r.stack || r.message) || r);
    });

    var ms = parseInt(app.getAttribute('data-straza-ms'), 10) || 8000;
    window.setTimeout(function () {
        if (!app.querySelector('.udzbenik-ucitavanje')) return;
        var razlog = greske.length ? greske.join(' | ')
            : 'motor nije javio grešku (skript blokiran ili bez odgovora)';
        console.error('Уџбеник: мотор се није покренуо за ' + ms + ' ms. Разлог: ' + razlog);
        var sablon = document.getElementById('udzbenik-straza');
        if (!sablon) return;
        var poruka = sablon.content.cloneNode(true);
        var detalj = poruka.querySelector('[data-razlog]');
        if (detalj) detalj.textContent = razlog;
        var dugme = poruka.querySelector('button');
        if (dugme) {
            dugme.addEventListener('click', function () { window.location.reload(); });
        }
        app.replaceChildren(poruka);
    }, ms);
})();
