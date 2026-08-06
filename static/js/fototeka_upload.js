/* Фототека upload: пошаљи изабрани сет ЈЕДНУ ПО ЈЕДНУ ДАТОТЕКУ, да много/велике
   датотеке никад не падну као један предимензиониран multipart POST (nginx cap).
   Извори су галерија и (на телефону) камера — обоје пуне исти ред. Приказује
   напредак и извештај по датотеци. Ако се скрипта не изврши, форма ради као
   обичан POST (galerijski input задржава name="files" multiple). */
(function () {
    'use strict';

    function sharedFields(form) {
        // Сва поља осим датотека, да сваки захтев по датотеци носи исте
        // метаподатке + евентуалну везу + CSRF токен.
        var pairs = [];
        Array.prototype.forEach.call(form.elements, function (el) {
            if (!el.name || el.type === 'file') { return; }
            if ((el.type === 'checkbox' || el.type === 'radio') && !el.checked) { return; }
            pairs.push([el.name, el.value]);
        });
        return pairs;
    }

    function sendOne(file, form) {
        var data = new FormData();
        sharedFields(form).forEach(function (p) { data.append(p[0], p[1]); });
        data.append('file', file);
        return fetch('/fototeka/upload/jedan', {
            method: 'POST',
            body: data,
            headers: { 'X-CSRFToken': form.querySelector('[name=csrf_token]').value }
        })
            .then(function (r) { return r.json().catch(function () { return { ok: false, ime: file.name, error: 'грешка сервера' }; }); })
            .catch(function () { return { ok: false, ime: file.name, error: 'мрежна грешка' }; });
    }

    function isDuplicate(result) {
        return !result.ok && typeof result.error === 'string'
            && result.error.indexOf('већ постоји') !== -1;
    }

    function row(result) {
        var duplicate = isDuplicate(result);
        var li = document.createElement('li');
        li.className = 'small ' + (result.ok ? 'text-success'
            : (duplicate ? 'text-warning' : 'text-danger'));
        li.textContent = (result.ok ? '✓ ' : (duplicate ? '↺ ' : '✗ '))
            + (result.ime || '')
            + (result.ok ? '' : ' — ' + (duplicate
                ? 'фотографија са истим садржајем већ постоји у Фототеци; ова датотека није поново сачувана'
                : (result.error || 'неуспешно')));
        return li;
    }

    function humanSize(bytes) {
        if (bytes >= 1024 * 1024) { return (bytes / (1024 * 1024)).toFixed(1) + ' MB'; }
        return Math.max(1, Math.round(bytes / 1024)) + ' KB';
    }

    function init() {
        var form = document.getElementById('fototekaUploadForm');
        if (!form) { return; }
        var galInput = document.getElementById('fototekaFajlovi');
        var camInput = document.getElementById('fototekaKamera');
        var redBox = document.getElementById('fototekaRed');
        var redLista = document.getElementById('fototekaRedLista');
        var redBroj = document.getElementById('fototekaRedBroj');
        var progress = document.getElementById('fototekaUploadProgress');
        var bar = document.getElementById('fototekaUploadBar');
        var report = document.getElementById('fototekaUploadReport');
        var submitBtn = form.querySelector('button[type=submit]');

        var maxFiles = parseInt(form.getAttribute('data-max-files'), 10) || 40;
        var maxBytes = (parseInt(form.getAttribute('data-max-mb'), 10) || 50) * 1024 * 1024;
        var maxMb = Math.round(maxBytes / (1024 * 1024));

        // Ред за отпремање — јединствени извор истине; галеријски input се одржава
        // усклађен преко DataTransfer-а (да `required` и fallback раде).
        var queue = [];

        function key(f) { return f.name + '|' + f.size + '|' + f.lastModified; }

        function syncGalInput() {
            // Ако браузер подржава DataTransfer, пресликај ред у input.files
            // (тако required важи и када су слике стигле само из камере).
            try {
                var dt = new DataTransfer();
                queue.forEach(function (f) { dt.items.add(f); });
                galInput.files = dt.files;
            } catch (e) { /* старији браузер: ред и даље ради кроз JS */ }
        }

        function flash(msg) {
            report.innerHTML = '';
            progress.hidden = false;
            bar.style.width = '0%';
            bar.textContent = '';
            var li = document.createElement('li');
            li.className = 'small text-danger';
            li.textContent = '✗ ' + msg;
            report.appendChild(li);
        }

        function renderQueue() {
            redLista.innerHTML = '';
            if (!queue.length) { redBox.classList.add('d-none'); return; }
            redBox.classList.remove('d-none');
            redBroj.textContent = 'У реду за слање: ' + queue.length + ' / ' + maxFiles;
            queue.forEach(function (f, idx) {
                var li = document.createElement('li');
                li.className = 'list-group-item d-flex justify-content-between align-items-center gap-2 py-2';
                var name = document.createElement('span');
                name.className = 'text-truncate';
                name.textContent = f.name + ' (' + humanSize(f.size) + ')';
                var rm = document.createElement('button');
                rm.type = 'button';
                rm.className = 'btn btn-sm btn-outline-danger flex-shrink-0';
                rm.setAttribute('aria-label', 'Уклони из реда');
                rm.innerHTML = '<i class="bi bi-x-lg"></i>';
                rm.addEventListener('click', function () {
                    queue.splice(idx, 1);
                    syncGalInput();
                    renderQueue();
                });
                li.appendChild(name);
                li.appendChild(rm);
                redLista.appendChild(li);
            });
        }

        function addFiles(fileList) {
            var incoming = Array.prototype.slice.call(fileList || []);
            var rejectedBig = [];
            var seen = {};
            queue.forEach(function (f) { seen[key(f)] = true; });
            incoming.forEach(function (f) {
                if (f.size > maxBytes) { rejectedBig.push(f.name); return; }
                var k = key(f);
                if (seen[k]) { return; }   // дупликат у истом реду
                if (queue.length >= maxFiles) { return; }
                seen[k] = true;
                queue.push(f);
            });
            syncGalInput();
            renderQueue();
            var msgs = [];
            if (rejectedBig.length) {
                msgs.push('Прескочено (веће од ' + maxMb + ' MB): ' + rejectedBig.join(', '));
            }
            if (queue.length >= maxFiles && incoming.length) {
                msgs.push('Достигнут лимит од ' + maxFiles + ' датотека по слању — уклоните неке пре додавања.');
            }
            if (msgs.length) { flash(msgs.join(' ')); }
        }

        if (galInput) {
            galInput.addEventListener('change', function () {
                // Прикупи изабране, па поново пресликај ред у input (акумулира
                // камеру + галерију, уместо да замени).
                addFiles(galInput.files);
            });
        }
        if (camInput) {
            camInput.addEventListener('change', function () {
                addFiles(camInput.files);
                camInput.value = '';  // дозволи поновно сликање исте „датотеке"
            });
        }

        form.addEventListener('submit', function (event) {
            var files = queue.slice();
            if (!files.length) {
                // Ако JS акумулација није коришћена (нпр. input.files директно),
                // падни на input.
                files = galInput && galInput.files ? Array.prototype.slice.call(galInput.files) : [];
            }
            if (!files.length) { return; }  // пусти браузеру да прикаже "required"
            event.preventDefault();
            submitBtn.disabled = true;
            report.innerHTML = '';
            progress.hidden = false;
            bar.style.width = '0%';

            var okCount = 0, done = 0, lastId = null;
            function step(i) {
                if (i >= files.length) {
                    bar.style.width = '100%';
                    bar.textContent = okCount + '/' + files.length;
                    if (okCount === 1 && files.length === 1 && lastId) {
                        window.location.href = '/fototeka/' + lastId;
                        return;
                    }
                    var summary = document.createElement('div');
                    summary.className = 'mt-2';
                    summary.innerHTML = 'Примљено: <strong>' + okCount + '/' + files.length
                        + '</strong>. <a href="/fototeka">Отвори Фототеку</a>';
                    report.appendChild(summary);
                    submitBtn.disabled = false;
                    return;
                }
                sendOne(files[i], form).then(function (result) {
                    done += 1;
                    if (result.ok) { okCount += 1; lastId = result.id; }
                    report.appendChild(row(result));
                    var pct = Math.round((done / files.length) * 100);
                    bar.style.width = pct + '%';
                    bar.textContent = done + '/' + files.length;
                    step(i + 1);
                });
            }
            step(0);
        });
    }

    document.addEventListener('DOMContentLoaded', init);
}());
