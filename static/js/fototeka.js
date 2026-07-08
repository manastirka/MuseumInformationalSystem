/* Фототека: toggle of the optional-link sections + inventory-number
   autocomplete (mineral collection only in phase 1). */
(function () {
    'use strict';

    function toggleSections(select) {
        var prefix = select.dataset.prefix || '';
        var mapping = {
            predmet: 'VezaPredmet',
            teren: 'VezaTeren',
            projekat: 'VezaProjekat',
            izlozba: 'VezaIzlozba'
        };
        Object.keys(mapping).forEach(function (tip) {
            var section = document.getElementById(prefix + mapping[tip]);
            if (section) {
                section.hidden = select.value !== tip;
            }
        });
    }

    function bindVezaForm(select) {
        toggleSections(select);
        select.addEventListener('change', function () {
            toggleSections(select);
        });

        var prefix = select.dataset.prefix || '';
        var invInput = document.getElementById(prefix + 'VezaInvBroj');
        var zbirkaSelect = document.getElementById(prefix + 'VezaZbirka');
        var datalist = document.getElementById(prefix + 'PredmetiLista');
        if (!invInput || !zbirkaSelect || !datalist) {
            return;
        }
        var debounceTimer = null;
        invInput.addEventListener('input', function () {
            window.clearTimeout(debounceTimer);
            var query = invInput.value.trim();
            if (zbirkaSelect.value !== 'mineral' || query.length < 2) {
                datalist.innerHTML = '';
                return;
            }
            debounceTimer = window.setTimeout(function () {
                fetch('/fototeka/api/predmeti?zbirka=' + encodeURIComponent(zbirkaSelect.value)
                        + '&q=' + encodeURIComponent(query))
                    .then(function (response) { return response.ok ? response.json() : []; })
                    .then(function (items) {
                        datalist.innerHTML = '';
                        items.forEach(function (item) {
                            var option = document.createElement('option');
                            option.value = item.inventarni_broj;
                            option.label = item.naziv || '';
                            datalist.appendChild(option);
                        });
                    })
                    .catch(function () { /* autocomplete is best-effort */ });
            }, 250);
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.fototeka-veza-tip').forEach(bindVezaForm);
    });
}());
