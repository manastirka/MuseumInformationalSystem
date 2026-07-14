/* Фototeka gallery: remember the view mode (grid/list/compact) in
   localStorage; drive the multi-select (select-all + count + selected size);
   and the download modal (JPG vs original choice + size warning), which
   replaces the old inline layer select. */
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

    function humanBytes(n) {
        if (!n || n < 1) { return '0 B'; }
        var units = ['B', 'KB', 'MB', 'GB', 'TB'];
        var i = 0, v = n;
        while (v >= 1024 && i < units.length - 1) { v /= 1024; i += 1; }
        return (i === 0 ? v : v.toFixed(v < 10 ? 1 : 0)) + ' ' + units[i];
    }

    function init() {
        var form = document.getElementById('fototekaZipForm');
        if (!form) { return; }
        var boxes = Array.prototype.slice.call(form.querySelectorAll('input[name=ids]'));
        var selectAll = document.getElementById('fototekaSelectAll');
        var count = document.getElementById('fototekaSelCount');
        var slojInput = document.getElementById('fototekaSloj');

        var maxBytes = parseInt(form.dataset.zipMaxBytes, 10) || 0;
        var maxCount = parseInt(form.dataset.zipMaxCount, 10) || 0;

        // modal elements
        var openBtn = document.getElementById('fototekaDownloadOpen');
        var modal = document.getElementById('fototekaDownloadModal');
        var modalCount = document.getElementById('fototekaModalCount');
        var modalSize = document.getElementById('fototekaModalSize');
        var modalWarn = document.getElementById('fototekaModalWarn');
        var cancelBtn = document.getElementById('fototekaModalCancel');
        var confirmBtn = document.getElementById('fototekaModalConfirm');

        function selected() { return boxes.filter(function (b) { return b.checked; }); }

        function totalBytes(sel) {
            return sel.reduce(function (sum, b) {
                return sum + (parseInt(b.dataset.bytes, 10) || 0);
            }, 0);
        }

        function chosenSloj() {
            var r = modal && modal.querySelector('input[name=fototekaSlojChoice]:checked');
            return r ? r.value : 'jpg';
        }

        function refreshSelection() {
            var sel = selected();
            boxes.forEach(function (b) {
                var item = b.closest('.foto-item');
                if (item) { item.classList.toggle('selected', b.checked); }
            });
            if (count) { count.textContent = String(sel.length); }
            var batchCount = document.getElementById('fototekaBatchCount');
            if (batchCount) { batchCount.textContent = String(sel.length); }
            if (selectAll) {
                selectAll.checked = sel.length > 0 && sel.length === boxes.length;
                selectAll.indeterminate = sel.length > 0 && sel.length < boxes.length;
            }
        }

        function refreshModal() {
            var sel = selected();
            var bytes = totalBytes(sel);
            if (modalCount) { modalCount.textContent = String(sel.length); }
            if (modalSize) { modalSize.textContent = humanBytes(bytes); }
            if (!modalWarn) { return; }
            var msgs = [];
            if (maxCount && sel.length > maxCount) {
                msgs.push('Изабрано је више од ' + maxCount + ' фотографија; преузеће се првих ' + maxCount + '.');
            }
            if (chosenSloj() === 'original' && maxBytes && bytes > maxBytes) {
                msgs.push('Оригинали прелазе ' + humanBytes(maxBytes)
                    + '; архива ће бити скраћена на тај лимит. Размотрите JPG преглед или мањи избор.');
            }
            if (msgs.length) {
                modalWarn.innerHTML = msgs.join('<br>');
                modalWarn.hidden = false;
            } else {
                modalWarn.hidden = true;
            }
        }

        function openModal() {
            if (!selected().length) {
                window.alert('Изаберите бар једну фотографију.');
                return;
            }
            refreshModal();
            if (modal) { modal.hidden = false; }
        }

        function closeModal() { if (modal) { modal.hidden = true; } }

        boxes.forEach(function (b) { b.addEventListener('change', refreshSelection); });
        if (selectAll) {
            selectAll.addEventListener('change', function () {
                boxes.forEach(function (b) { b.checked = selectAll.checked; });
                refreshSelection();
            });
        }
        if (openBtn) { openBtn.addEventListener('click', openModal); }
        if (cancelBtn) { cancelBtn.addEventListener('click', closeModal); }
        if (modal) {
            modal.addEventListener('click', function (e) {
                if (e.target === modal) { closeModal(); }  // backdrop click
            });
            Array.prototype.forEach.call(
                modal.querySelectorAll('input[name=fototekaSlojChoice]'),
                function (r) { r.addEventListener('change', refreshModal); }
            );
        }
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && modal && !modal.hidden) { closeModal(); }
        });
        if (confirmBtn) {
            confirmBtn.addEventListener('click', function () {
                if (!selected().length) { closeModal(); return; }
                if (slojInput) { slojInput.value = chosenSloj(); }
                form.submit();
            });
        }

        initBatchEdit(selected, refreshSelection);
        refreshSelection();
    }

    /* Групно уређивање изабраних: модал приказује ТАЧНО шта ће се десити
       (колико фотографија, које акције), па тек онда шаље. Права се и даље
       проверавају на серверу, по свакој ставци. */
    function initBatchEdit(selected, refreshSelection) {
        var openBtn = document.getElementById('fototekaBatchOpen');
        var backdrop = document.getElementById('fototekaBatchBackdrop');
        if (!openBtn || !backdrop) { return; }

        var form = document.getElementById('fototekaBatchForm');
        var idsBox = document.getElementById('fototekaBatchIds');
        var stats = document.getElementById('fototekaBatchStats');
        var sazetak = document.getElementById('fototekaBatchSazetak');
        var submitBtn = document.getElementById('fototekaBatchSubmit');
        var cancelBtn = document.getElementById('fototekaBatchCancel');

        function zatvori() { backdrop.hidden = true; }

        function opisAkcije() {
            var poruke = [];
            var tagA = form.querySelector('input[name=tag_akcija]:checked');
            var tagovi = (form.querySelector('[name=tagovi]').value || '').trim();
            if (tagA && tagA.value && tagovi) {
                var kako = { dodaj: 'додају (постојећи остају)', zameni: 'ЗАМЕЊУЈУ све постојеће',
                             ukloni: 'уклањају' }[tagA.value];
                poruke.push('Тагови се ' + kako + ': ' + tagovi);
            }
            var opisA = form.querySelector('input[name=opis_akcija]:checked');
            var opis = (form.querySelector('[name=opis]').value || '').trim();
            if (opisA && opisA.value && opis) {
                poruke.push(opisA.value === 'postavi'
                    ? 'Опис се ПОСТАВЉА свима (преписује постојећи)'
                    : 'Опис се дописује на крај постојећег');
            }
            var vid = form.querySelector('[name=vidljivost]').value;
            if (vid) { poruke.push('Видљивост: ' + (vid === 'javno' ? 'јавно' : 'приватно')); }
            var vezaTip = form.querySelector('[name=veza_tip]');
            if (vezaTip && vezaTip.value && vezaTip.value !== 'bez') {
                poruke.push('Веза се додаје свима: ' + vezaTip.options[vezaTip.selectedIndex].text);
            }
            var autor = form.querySelector('[name=autor_email]');
            if (autor && autor.value.trim()) { poruke.push('Аутор се мења у: ' + autor.value.trim()); }
            return poruke;
        }

        function osveziSazetak() {
            var broj = selected().length;
            var poruke = opisAkcije();
            stats.innerHTML = 'Изабрано: <strong>' + broj + '</strong> фотографија.';
            if (!poruke.length) {
                sazetak.textContent = 'Изаберите бар једну акцију.';
                submitBtn.disabled = true;
                return;
            }
            sazetak.innerHTML = 'Над <strong>' + broj + '</strong> фотографија: <br>• ' +
                poruke.join('<br>• ') +
                '<br><small>Фотографије које не смете да мењате биће прескочене.</small>';
            submitBtn.disabled = broj === 0;
        }

        openBtn.addEventListener('click', function () {
            var sel = selected();
            if (!sel.length) { return; }
            idsBox.innerHTML = '';
            sel.forEach(function (b) {
                var input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'ids';
                input.value = b.value;
                idsBox.appendChild(input);
            });
            backdrop.hidden = false;
            osveziSazetak();
        });

        form.addEventListener('input', osveziSazetak);
        form.addEventListener('change', osveziSazetak);
        if (cancelBtn) { cancelBtn.addEventListener('click', zatvori); }
        backdrop.addEventListener('click', function (e) { if (e.target === backdrop) { zatvori(); } });
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && !backdrop.hidden) { zatvori(); }
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        initViewToggle();
        init();
    });
}());
