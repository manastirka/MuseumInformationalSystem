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

        refreshSelection();
    }

    document.addEventListener('DOMContentLoaded', function () {
        initViewToggle();
        init();
    });
}());
