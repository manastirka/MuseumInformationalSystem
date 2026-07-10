/* Фототека upload: send a multi-select set ONE FILE AT A TIME so many/large
   files never fail as a single oversized multipart POST (nginx cap 200M).
   Shows progress and a per-file pass/fail report. Falls back to the plain
   form POST if this script does not run. */
(function () {
    'use strict';

    function sharedFields(form) {
        // All form fields except the file input, so each per-file request
        // carries the same metadata + optional link + CSRF token.
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

    function init() {
        var form = document.getElementById('fototekaUploadForm');
        if (!form) { return; }
        var fileInput = form.querySelector('input[type=file]');
        var progress = document.getElementById('fototekaUploadProgress');
        var bar = document.getElementById('fototekaUploadBar');
        var report = document.getElementById('fototekaUploadReport');
        var submitBtn = form.querySelector('button[type=submit]');

        form.addEventListener('submit', function (event) {
            var files = fileInput && fileInput.files ? Array.prototype.slice.call(fileInput.files) : [];
            if (!files.length) { return; }  // let the browser show "required"
            event.preventDefault();
            submitBtn.disabled = true;
            report.innerHTML = '';
            progress.hidden = false;

            var okCount = 0, done = 0, lastId = null;
            function step(i) {
                if (i >= files.length) {
                    bar.style.width = '100%';
                    bar.textContent = okCount + '/' + files.length;
                    var summary = document.createElement('div');
                    summary.className = 'mt-2';
                    if (okCount === 1 && files.length === 1 && lastId) {
                        window.location.href = '/fototeka/' + lastId;
                        return;
                    }
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
