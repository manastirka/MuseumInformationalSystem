/* Фототека reverse-linking widget: shows photos linked to an entity and lets
   the user link/unlink existing photos. Non-destructive — the photo and its
   RAW original are never touched. Initializes every .fototeka-entitet-widget
   on the page. */
(function () {
    'use strict';

    function entityParams(widget) {
        var d = widget.dataset;
        var params = new URLSearchParams({ tip: d.tip });
        if (d.tip === 'predmet') {
            params.set('database', d.database);
            params.set('broj', d.broj);
        } else if (d.tip === 'teren') {
            params.set('teren_id', d.terenId);
        } else if (d.tip === 'projekat') {
            params.set('projekat_id', d.projekatId);
        } else if (d.tip === 'izlozba') {
            params.set('izlozba_id', d.izlozbaId);
        }
        return params;
    }

    function photoCard(photo, actionLabel, actionClass) {
        var col = document.createElement('div');
        col.className = 'col-auto text-center';
        col.style.width = '110px';
        var link = document.createElement('a');
        link.href = photo.url;
        var img = document.createElement('img');
        img.src = photo.thumb_url;
        img.alt = photo.opis || '';
        img.loading = 'lazy';
        img.style.cssText = 'width:100px;height:75px;object-fit:cover;border-radius:8px;background:#eee;';
        link.appendChild(img);
        var caption = document.createElement('div');
        caption.className = 'small text-truncate';
        caption.style.maxWidth = '100px';
        caption.textContent = photo.opis || '';
        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'btn btn-sm ' + actionClass + ' mt-1 w-100';
        button.textContent = actionLabel;
        col.appendChild(link);
        col.appendChild(caption);
        col.appendChild(button);
        return { col: col, button: button };
    }

    function post(widget, url, photoId, onDone) {
        var params = entityParams(widget);
        params.set('fotografija_id', String(photoId));
        params.set('csrf_token', widget.dataset.csrf);
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': widget.dataset.csrf
            },
            body: params.toString()
        })
            .then(function (r) { return r.ok ? r.json() : { ok: false }; })
            .then(function (data) { onDone(!!data.ok); })
            .catch(function () { onDone(false); });
    }

    function loadLinked(widget) {
        var container = widget.querySelector('.fototeka-entitet-linked');
        fetch('/fototeka/api/entitet/fotografije?' + entityParams(widget).toString())
            .then(function (r) { return r.ok ? r.json() : { ok: false, fotografije: [] }; })
            .then(function (data) {
                container.innerHTML = '';
                var photos = (data && data.fotografije) || [];
                if (!photos.length) {
                    var empty = document.createElement('div');
                    empty.className = 'col-12 text-muted small';
                    empty.textContent = 'Нема повезаних фотографија.';
                    container.appendChild(empty);
                    return;
                }
                photos.forEach(function (photo) {
                    var card = photoCard(photo, 'Уклони везу', 'btn-outline-danger');
                    card.button.addEventListener('click', function () {
                        card.button.disabled = true;
                        post(widget, '/fototeka/api/entitet/veza/ukloni', photo.id, function (ok) {
                            if (ok) { loadLinked(widget); }
                            else { card.button.disabled = false; }
                        });
                    });
                    container.appendChild(card.col);
                });
            });
    }

    function bindSearch(widget) {
        var input = widget.querySelector('.fototeka-entitet-pretraga');
        var results = widget.querySelector('.fototeka-entitet-rezultati');
        var timer = null;
        input.addEventListener('input', function () {
            window.clearTimeout(timer);
            var q = input.value.trim();
            timer = window.setTimeout(function () {
                var params = entityParams(widget);
                params.set('q', q);
                fetch('/fototeka/api/entitet/pretraga?' + params.toString())
                    .then(function (r) { return r.ok ? r.json() : { fotografije: [] }; })
                    .then(function (data) {
                        results.innerHTML = '';
                        ((data && data.fotografije) || []).forEach(function (photo) {
                            var card = photoCard(photo, 'Повежи', 'btn-outline-success');
                            card.button.addEventListener('click', function () {
                                card.button.disabled = true;
                                post(widget, '/fototeka/api/entitet/veza', photo.id, function (ok) {
                                    if (ok) {
                                        card.col.remove();
                                        loadLinked(widget);
                                    } else {
                                        card.button.disabled = false;
                                    }
                                });
                            });
                            results.appendChild(card.col);
                        });
                    });
            }, 250);
        });
    }

    function init(widget) {
        if (widget.dataset.fototekaInit) { return; }
        widget.dataset.fototekaInit = '1';
        loadLinked(widget);
        bindSearch(widget);
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.fototeka-entitet-widget').forEach(init);
    });
}());
