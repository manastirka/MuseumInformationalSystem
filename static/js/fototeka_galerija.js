/* Фototeka gallery: remember the view mode (grid/list/compact) in
   localStorage, and drive the multi-select download (select-all + count). */
(function () {
    'use strict';

    var VIEWS = ['grid', 'list', 'compact'];
    var STORAGE_KEY = 'fototekaView';

    function applyView(container, buttons, view) {
        if (VIEWS.indexOf(view) === -1) { view = 'grid'; }
        VIEWS.forEach(function (v) { container.classList.remove('view-' + v); });
        container.classList.add('view-' + view);
        buttons.forEach(function (btn) {
            btn.classList.toggle('active', btn.dataset.view === view);
        });
        try { window.localStorage.setItem(STORAGE_KEY, view); } catch (e) { /* ignore */ }
    }

    function initViewToggle() {
        var container = document.getElementById('fototekaItems');
        var buttons = Array.prototype.slice.call(document.querySelectorAll('.fototeka-view-btn'));
        if (!buttons.length) { return; }
        var saved = 'grid';
        try { saved = window.localStorage.getItem(STORAGE_KEY) || 'grid'; } catch (e) { /* ignore */ }
        if (container) { applyView(container, buttons, saved); }
        buttons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                if (container) { applyView(container, buttons, btn.dataset.view); }
            });
        });
    }

    function initSelection() {
        var form = document.getElementById('fototekaZipForm');
        var selectAll = document.getElementById('fototekaSelectAll');
        var count = document.getElementById('fototekaSelCount');
        if (!form) { return; }
        var boxes = Array.prototype.slice.call(form.querySelectorAll('input[name=ids]'));

        function refresh() {
            var n = 0;
            boxes.forEach(function (b) {
                // keep the visual state (blue check + highlight) in lock-step
                // with the checkbox and the counter
                var item = b.closest('.foto-item');
                if (item) { item.classList.toggle('selected', b.checked); }
                if (b.checked) { n += 1; }
            });
            if (count) { count.textContent = String(n); }
            if (selectAll) {
                selectAll.checked = n > 0 && n === boxes.length;
                selectAll.indeterminate = n > 0 && n < boxes.length;
            }
        }
        boxes.forEach(function (b) { b.addEventListener('change', refresh); });
        if (selectAll) {
            selectAll.addEventListener('change', function () {
                boxes.forEach(function (b) { b.checked = selectAll.checked; });
                refresh();
            });
        }
        form.addEventListener('submit', function (event) {
            if (!boxes.some(function (b) { return b.checked; })) {
                event.preventDefault();
                window.alert('Изаберите бар једну фотографију.');
            }
        });
        refresh();
    }

    document.addEventListener('DOMContentLoaded', function () {
        initViewToggle();
        initSelection();
    });
}());
