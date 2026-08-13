/* Креатор сопствене теме (фаза 3).
 *
 * Огледало серверске логике из custom_theme.py: исте формуле за
 * осветљавање/затамњивање, WCAG контраст и мапирање дванаест боја + сенка +
 * заобљеност у --pal-* токене. Уживо примењује токене на документ (без уписа у
 * базу) за преглед; чување/примену/извоз/увоз/брисање ради кроз JSON руте.
 *
 * База је једини извор истине: чување шаље СЕМАНТИЧКЕ изборе (боје/сенка/радијус),
 * а сервер их поново мапира; клијентско мапирање служи само за преглед.
 */
(function () {
  'use strict';

  var COLOR_KEYS = ['primary', 'header', 'sidebar', 'body', 'card', 'accent',
    'selection', 'button', 'text', 'border', 'link', 'warning'];
  var SHADOW_OPTIONS = ['none', 'soft', 'medium', 'strong'];
  var SHADOW_CSS = {
    none: 'none',
    soft: '0 1px 3px rgba(15, 23, 42, 0.08), 0 1px 2px rgba(15, 23, 42, 0.06)',
    medium: '0 4px 12px rgba(15, 23, 42, 0.12), 0 2px 4px rgba(15, 23, 42, 0.08)',
    strong: '0 10px 28px rgba(15, 23, 42, 0.22), 0 4px 10px rgba(15, 23, 42, 0.16)'
  };
  var RADIUS_MIN = 0, RADIUS_MAX = 20;

  var DEFAULT_DEF = {
    colors: {
      primary: '#1d5fab', header: '#16375d', sidebar: '#143257', body: '#f1f5fb',
      card: '#ffffff', accent: '#1d5fab', selection: '#d9e7fa', button: '#1d5fab',
      text: '#1f2a37', border: '#d5dde9', link: '#1d5fab', warning: '#8a5606'
    },
    shadow: 'soft', radius: 8
  };

  // ---- боја: помоћне (истоветно custom_theme.py) --------------------------
  function normHex(v) {
    if (typeof v !== 'string') return null;
    var t = v.trim();
    var m6 = /^#?([0-9a-fA-F]{6})$/.exec(t);
    if (m6) return '#' + m6[1].toLowerCase();
    var m3 = /^#?([0-9a-fA-F]{3})$/.exec(t);
    if (m3) { var s = m3[1].toLowerCase(); return '#' + s[0] + s[0] + s[1] + s[1] + s[2] + s[2]; }
    return null;
  }
  function toRgb(h) { h = h.replace('#', ''); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; }
  function toHex(rgb) { return '#' + rgb.map(function (c) { c = Math.max(0, Math.min(255, Math.round(c))); return (c < 16 ? '0' : '') + c.toString(16); }).join(''); }
  function darken(h, f) { var c = toRgb(h); return toHex([c[0] * (1 - f), c[1] * (1 - f), c[2] * (1 - f)]); }
  function lighten(h, f) { var c = toRgb(h); return toHex([c[0] + (255 - c[0]) * f, c[1] + (255 - c[1]) * f, c[2] + (255 - c[2]) * f]); }
  function chLin(c) { var cs = c / 255; return cs <= 0.03928 ? cs / 12.92 : Math.pow((cs + 0.055) / 1.055, 2.4); }
  function lum(h) { var c = toRgb(h); return 0.2126 * chLin(c[0]) + 0.7152 * chLin(c[1]) + 0.0722 * chLin(c[2]); }
  function contrast(a, b) { var la = lum(a), lb = lum(b); var hi = Math.max(la, lb), lo = Math.min(la, lb); return (hi + 0.05) / (lo + 0.05); }
  function bestInk(bg) { return contrast('#ffffff', bg) >= contrast('#111111', bg) ? '#ffffff' : '#111111'; }

  // ---- дефиниција -> --pal-* токени (истоветно custom_theme.pal_tokens) ----
  function palTokens(def) {
    var c = def.colors;
    return {
      '--pal-primary': c.primary,
      '--pal-primary-dark': darken(c.primary, 0.15),
      '--pal-primary-light': lighten(c.primary, 0.15),
      '--pal-bg-body': c.body,
      '--pal-bg-card': c.card,
      '--pal-bg-nav': c.header,
      '--pal-elevated': darken(c.card, 0.03),
      '--pal-hover': darken(c.card, 0.06),
      '--pal-stripe': darken(c.card, 0.035),
      '--pal-text': c.text,
      '--pal-text2': lighten(c.text, 0.18),
      '--pal-muted': lighten(c.text, 0.32),
      '--pal-border': c.border,
      '--pal-thead-bg': c.header,
      '--pal-thead-text': bestInk(c.header),
      '--pal-sel-bg': c.selection,
      '--pal-sel-text': bestInk(c.selection),
      '--pal-side-bg': c.sidebar,
      '--pal-side-text': bestInk(c.sidebar),
      '--pal-accent': c.accent,
      '--pal-accent-dark': darken(c.accent, 0.15),
      '--pal-btn': c.button,
      '--pal-btn-dark': darken(c.button, 0.15),
      '--pal-on-accent': bestInk(c.button),
      '--pal-link': c.link,
      '--pal-warning': c.warning,
      '--pal-shadow': SHADOW_CSS[def.shadow] || SHADOW_CSS.soft,
      '--pal-radius-card': (def.radius + 2) + 'px',
      '--pal-radius-btn': def.radius + 'px'
    };
  }
  function bsTheme(def) { return lum(def.colors.card) < 0.4 ? 'dark' : 'light'; }

  // ---- локална копија радне дефиниције ------------------------------------
  function cloneDef(d) { return { colors: Object.assign({}, d.colors), shadow: d.shadow, radius: d.radius }; }
  var working = cloneDef(DEFAULT_DEF);
  var editingId = null;      // id теме која се уређује (или null за нову)
  var editingName = '';
  var previewActive = false; // да ли је преглед на целој апликацији активан

  var request = window.secureFetch || fetch;
  var BASE = '/podesavanja/izgled/moje-teme';

  // ---- DOM закачке --------------------------------------------------------
  var $ = function (id) { return document.getElementById(id); };
  function qs(sel, root) { return (root || document).querySelector(sel); }

  // Примени радну дефиницију на дати корен (документ или минијатура).
  function applyTokensTo(rootEl, def) {
    var t = palTokens(def);
    Object.keys(t).forEach(function (k) { rootEl.style.setProperty(k, t[k]); });
  }
  function clearTokensFrom(rootEl) {
    var t = palTokens(DEFAULT_DEF);
    Object.keys(t).forEach(function (k) { rootEl.style.removeProperty(k); });
  }

  // ---- контраст очитавања (уживо AA) --------------------------------------
  // Парови које меримо: текст-на-позадини, текст-на-картици, мастило дугмета,
  // мастило заглавља, мастило бочног менија, мастило селектованог реда, линк-на-картици.
  var CONTRAST_PAIRS = [
    { id: 'ck-text-body', label: 'Текст на позадини', fg: function (c) { return c.text; }, bg: function (c) { return c.body; } },
    { id: 'ck-text-card', label: 'Текст на картици', fg: function (c) { return c.text; }, bg: function (c) { return c.card; } },
    { id: 'ck-btn', label: 'Натпис на дугмету', fg: function (c) { return bestInk(c.button); }, bg: function (c) { return c.button; } },
    { id: 'ck-header', label: 'Наслов заглавља', fg: function (c) { return bestInk(c.header); }, bg: function (c) { return c.header; } },
    { id: 'ck-sidebar', label: 'Бочни мени', fg: function (c) { return bestInk(c.sidebar); }, bg: function (c) { return c.sidebar; } },
    { id: 'ck-selection', label: 'Селектовани ред', fg: function (c) { return bestInk(c.selection); }, bg: function (c) { return c.selection; } },
    { id: 'ck-link', label: 'Линк на картици', fg: function (c) { return c.link; }, bg: function (c) { return c.card; } }
  ];

  var contrastFailing = false;

  function renderContrast() {
    var box = $('contrastReadout');
    if (!box) return;
    var anyFail = false;
    CONTRAST_PAIRS.forEach(function (p) {
      var el = $(p.id);
      if (!el) return;
      var ratio = contrast(p.fg(working.colors), p.bg(working.colors));
      var pass = ratio >= 4.5;
      if (!pass) anyFail = true;
      el.querySelector('.ck-ratio').textContent = ratio.toFixed(2) + ':1';
      var badge = el.querySelector('.ck-badge');
      badge.textContent = pass ? 'AA' : 'пада';
      badge.className = 'ck-badge ' + (pass ? 'ck-pass' : 'ck-fail');
      el.classList.toggle('is-fail', !pass);
    });
    var warn = $('contrastWarn');
    if (warn) warn.hidden = !anyFail;
    contrastFailing = anyFail;
    // Сервер одбија чување теме која пада AA — угаси дугмад док има пада.
    ['ccSave', 'ccApply'].forEach(function (id) {
      var btn = $(id);
      if (btn) btn.disabled = anyFail;
    });
  }

  // ---- пуни осврт: примени преглед на цео документ -------------------------
  function pushLivePreview() {
    var root = document.documentElement;
    window.MuseumTheme = window.MuseumTheme || {};
    window.MuseumTheme.palette = 'custom';
    window.MuseumTheme.customBs = bsTheme(working);
    root.setAttribute('data-palette', 'custom');
    root.removeAttribute('data-style');
    root.removeAttribute('data-accent');
    root.removeAttribute('data-theme');
    root.setAttribute('data-bs-theme', bsTheme(working));
    applyTokensTo(root, working);
  }

  // Врати документ на изглед пре прегледа (сачувана корисникова тема).
  function restoreSavedLook() {
    clearTokensFrom(document.documentElement);
    // Поново примени изворно стање теме странице кроз base.html механизам.
    if (window.MuseumTheme && typeof window.MuseumTheme.applyResolved === 'function') {
      window.MuseumTheme.palette = SAVED.palette;
      window.MuseumTheme.customBs = SAVED.customBs;
      // Врати inline токене сачуване custom теме (ако је корисник на custom).
      if (SAVED.palette === 'custom' && SAVED.css) {
        var decls = SAVED.css.split(';');
        decls.forEach(function (d) {
          var i = d.indexOf(':'); if (i < 0) return;
          document.documentElement.style.setProperty(d.slice(0, i).trim(), d.slice(i + 1).trim());
        });
      }
      window.MuseumTheme.applyResolved(SAVED.mode);
    }
  }

  // ---- мини-преглед (увек ужива, независно од пуног осврта) ---------------
  function renderMiniPreview() {
    var mini = $('creatorMini');
    if (!mini) return;
    applyTokensTo(mini, working);
    mini.style.setProperty('--x-body', working.colors.body);
    mini.style.setProperty('--x-card', working.colors.card);
    mini.style.setProperty('--x-header', working.colors.header);
    mini.style.setProperty('--x-sidebar', working.colors.sidebar);
    mini.style.setProperty('--x-primary', working.colors.primary);
    mini.style.setProperty('--x-button', working.colors.button);
    mini.style.setProperty('--x-btnink', bestInk(working.colors.button));
    mini.style.setProperty('--x-text', working.colors.text);
    mini.style.setProperty('--x-border', working.colors.border);
    mini.style.setProperty('--x-selection', working.colors.selection);
    mini.style.setProperty('--x-selink', bestInk(working.colors.selection));
    mini.style.setProperty('--x-headink', bestInk(working.colors.header));
    mini.style.setProperty('--x-sideink', bestInk(working.colors.sidebar));
    mini.style.setProperty('--x-link', working.colors.link);
    mini.style.setProperty('--x-warning', working.colors.warning);
    mini.style.setProperty('--x-radius', working.radius + 'px');
    mini.style.setProperty('--x-shadow', SHADOW_CSS[working.shadow]);
  }

  // Пун прерис после сваке измене.
  function refresh() {
    renderMiniPreview();
    renderContrast();
    if (previewActive) pushLivePreview();
  }

  // ---- синхронизуј контроле са радном дефиницијом --------------------------
  function syncControlsFromWorking() {
    COLOR_KEYS.forEach(function (k) {
      var picker = $('cc-' + k);
      var hexIn = $('cc-hex-' + k);
      if (picker) picker.value = working.colors[k];
      if (hexIn) hexIn.value = working.colors[k];
    });
    var rad = $('cc-radius'); if (rad) rad.value = working.radius;
    var radv = $('cc-radius-val'); if (radv) radv.textContent = working.radius + ' px';
    document.querySelectorAll('[data-shadow]').forEach(function (b) {
      b.classList.toggle('active', b.getAttribute('data-shadow') === working.shadow);
    });
    var nameIn = $('cc-name'); if (nameIn) nameIn.value = editingName || '';
  }

  function bindControls() {
    COLOR_KEYS.forEach(function (k) {
      var picker = $('cc-' + k);
      var hexIn = $('cc-hex-' + k);
      if (picker) picker.addEventListener('input', function () {
        working.colors[k] = picker.value.toLowerCase();
        if (hexIn) hexIn.value = working.colors[k];
        refresh();
      });
      if (hexIn) hexIn.addEventListener('change', function () {
        var n = normHex(hexIn.value);
        if (n) { working.colors[k] = n; if (picker) picker.value = n; hexIn.value = n; refresh(); }
        else { hexIn.value = working.colors[k]; }
      });
    });
    var rad = $('cc-radius');
    if (rad) rad.addEventListener('input', function () {
      working.radius = Math.max(RADIUS_MIN, Math.min(RADIUS_MAX, parseInt(rad.value, 10) || 0));
      var radv = $('cc-radius-val'); if (radv) radv.textContent = working.radius + ' px';
      refresh();
    });
    document.querySelectorAll('[data-shadow]').forEach(function (b) {
      b.addEventListener('click', function () {
        working.shadow = b.getAttribute('data-shadow');
        document.querySelectorAll('[data-shadow]').forEach(function (x) { x.classList.remove('active'); });
        b.classList.add('active');
        refresh();
      });
    });
  }

  // ---- операције ----------------------------------------------------------
  function flash(msg, ok) {
    var el = $('creatorMsg');
    if (!el) { if (!ok) alert(msg); return; }
    el.textContent = msg;
    el.className = 'creator-msg ' + (ok ? 'ok' : 'err');
    el.hidden = false;
    window.clearTimeout(flash._t);
    flash._t = window.setTimeout(function () { el.hidden = true; }, 4000);
  }

  function jsonPost(url, body, method) {
    return request(url, {
      method: method || 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined
    }).then(function (r) {
      return r.json().then(function (data) {
        if (!r.ok || data.status === 'error') throw new Error(data.message || 'Грешка');
        return data;
      });
    });
  }

  function loadList() {
    return request(BASE, { headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (data) { renderList(data.themes || [], data.active_id); return data; })
      .catch(function () { /* тихо */ });
  }

  function renderList(themes, activeId) {
    var box = $('customThemeList');
    if (!box) return;
    var empty = $('customThemeEmpty');
    box.innerHTML = '';
    if (empty) empty.hidden = themes.length > 0;
    themes.forEach(function (t) {
      var row = document.createElement('div');
      row.className = 'saved-theme' + (t.id === activeId ? ' is-active' : '');
      row.setAttribute('data-id', t.id);
      var sw = '';
      ['header', 'primary', 'card', 'body'].forEach(function (key) {
        var col = (t.definition && t.definition.colors && t.definition.colors[key]) || '#ccc';
        sw += '<span class="st-sw" style="background:' + col + '"></span>';
      });
      var nm = document.createElement('div');
      nm.className = 'st-main';
      nm.innerHTML = '<div class="st-swatches">' + sw + '</div><span class="st-name"></span>' +
        (t.id === activeId ? '<span class="st-active">Примењено</span>' : '');
      nm.querySelector('.st-name').textContent = t.name;
      var act = document.createElement('div');
      act.className = 'st-actions';
      act.innerHTML =
        '<button type="button" class="btn btn-sm btn-primary" data-op="apply">Примени</button>' +
        '<button type="button" class="btn btn-sm btn-outline-secondary" data-op="edit">Уреди</button>' +
        '<button type="button" class="btn btn-sm btn-outline-secondary" data-op="duplicate">Дуплирај</button>' +
        '<a class="btn btn-sm btn-outline-secondary" data-op="export" href="' + BASE + '/' + t.id + '/izvoz">Извези</a>' +
        '<button type="button" class="btn btn-sm btn-outline-danger" data-op="delete">Обриши</button>';
      row.appendChild(nm);
      row.appendChild(act);
      box.appendChild(row);

      act.querySelector('[data-op="apply"]').addEventListener('click', function () { applyTheme(t); });
      act.querySelector('[data-op="edit"]').addEventListener('click', function () { editTheme(t); });
      act.querySelector('[data-op="duplicate"]').addEventListener('click', function () { duplicateTheme(t); });
      act.querySelector('[data-op="delete"]').addEventListener('click', function () { deleteTheme(t); });
    });
  }

  function collectName() {
    var nameIn = $('cc-name');
    return nameIn ? nameIn.value.trim() : '';
  }

  function saveTheme() {
    if (contrastFailing) { flash('Тема не задовољава AA контраст — исправите означене парове пре чувања.', false); return; }
    var name = collectName();
    if (!name) { flash('Унесите назив теме.', false); var n = $('cc-name'); if (n) n.focus(); return; }
    var body = { name: name, definition: working };
    var url = editingId ? (BASE + '/' + editingId) : BASE;
    jsonPost(url, body).then(function (data) {
      editingId = data.id;
      editingName = data.name;
      flash('Тема „' + data.name + '" је сачувана.', true);
      loadList();
    }).catch(function (e) { flash(e.message, false); });
  }

  function applyEditorTheme() {
    // Сачувај (нову или измену) па примени.
    if (contrastFailing) { flash('Тема не задовољава AA контраст — исправите означене парове пре примене.', false); return; }
    var name = collectName();
    if (!name) { flash('Унесите назив теме пре примене.', false); return; }
    var body = { name: name, definition: working };
    var url = editingId ? (BASE + '/' + editingId) : BASE;
    jsonPost(url, body).then(function (data) {
      editingId = data.id; editingName = data.name;
      return jsonPost(BASE + '/' + data.id + '/primeni');
    }).then(function (data) {
      // тема је сада сачувана; освежи SAVED и остани у прегледу
      SAVED.palette = 'custom';
      SAVED.customBs = data.bs_theme;
      SAVED.css = data.pal_css;
      SAVED.mode = window.MuseumTheme ? window.MuseumTheme.mode : 'system';
      previewActive = true;
      pushLivePreview();
      flash('Тема је сачувана и примењена.', true);
      loadList();
      updatePreviewBar();
    }).catch(function (e) { flash(e.message, false); });
  }

  function applyTheme(t) {
    jsonPost(BASE + '/' + t.id + '/primeni').then(function (data) {
      SAVED.palette = 'custom'; SAVED.customBs = data.bs_theme; SAVED.css = data.pal_css;
      SAVED.mode = window.MuseumTheme ? window.MuseumTheme.mode : 'system';
      // одмах примени на документ
      window.MuseumTheme.palette = 'custom';
      window.MuseumTheme.customBs = data.bs_theme;
      var decls = data.pal_css.split(';');
      decls.forEach(function (d) { var i = d.indexOf(':'); if (i > -1) document.documentElement.style.setProperty(d.slice(0, i).trim(), d.slice(i + 1).trim()); });
      document.documentElement.setAttribute('data-palette', 'custom');
      document.documentElement.removeAttribute('data-theme');
      document.documentElement.removeAttribute('data-accent');
      document.documentElement.setAttribute('data-bs-theme', data.bs_theme);
      flash('Тема „' + t.name + '" је примењена.', true);
      loadList();
    }).catch(function (e) { flash(e.message, false); });
  }

  function editTheme(t) {
    var cleaned = sanitizeDef(t.definition);
    if (!cleaned) { flash('Дефиниција теме је неисправна.', false); return; }
    working = cleaned;
    editingId = t.id;
    editingName = t.name;
    syncControlsFromWorking();
    refresh();
    flash('Уређујете „' + t.name + '". Измене чувајте дугметом Сачувај.', true);
    scrollToCreator();
  }

  function duplicateTheme(t) {
    jsonPost(BASE + '/' + t.id + '/dupliciraj').then(function (data) {
      flash('Направљена копија „' + data.name + '".', true);
      loadList();
    }).catch(function (e) { flash(e.message, false); });
  }

  function deleteTheme(t) {
    if (!window.confirm('Обрисати тему „' + t.name + '"? Ова радња се не може опозвати.')) return;
    request(BASE + '/' + t.id, { method: 'DELETE' })
      .then(function (r) { return r.json().then(function (d) { if (!r.ok || d.status === 'error') throw new Error(d.message || 'Грешка'); return d; }); })
      .then(function () {
        flash('Тема је обрисана.', true);
        if (editingId === t.id) { newTheme(); }
        loadList();
      }).catch(function (e) { flash(e.message, false); });
  }

  function newTheme() {
    working = cloneDef(DEFAULT_DEF);
    editingId = null; editingName = '';
    syncControlsFromWorking();
    refresh();
  }

  function resetDefaults() {
    working = cloneDef(DEFAULT_DEF);
    syncControlsFromWorking();
    refresh();
    flash('Враћене подразумеване вредности.', true);
  }

  // ---- увоз/извоз ---------------------------------------------------------
  function sanitizeDef(raw) {
    if (!raw || typeof raw !== 'object') return null;
    var src = raw.colors && typeof raw.colors === 'object' ? raw.colors : raw;
    var colors = {};
    for (var i = 0; i < COLOR_KEYS.length; i++) {
      var n = normHex(src[COLOR_KEYS[i]]);
      if (!n) return null;
      colors[COLOR_KEYS[i]] = n;
    }
    var shadow = SHADOW_OPTIONS.indexOf(raw.shadow) > -1 ? raw.shadow : 'soft';
    var radius = parseInt(raw.radius, 10);
    if (isNaN(radius)) radius = 8;
    radius = Math.max(RADIUS_MIN, Math.min(RADIUS_MAX, radius));
    return { colors: colors, shadow: shadow, radius: radius };
  }

  function handleImportFile(file) {
    var reader = new FileReader();
    reader.onload = function () {
      var parsed;
      try { parsed = JSON.parse(reader.result); }
      catch (e) { flash('Датотека није исправан JSON.', false); return; }
      // клијентска провера пре слања (сервер поново валидира)
      var defRaw = parsed && parsed.definition ? parsed.definition : parsed;
      var cleaned = sanitizeDef(defRaw);
      if (!cleaned) { flash('Тема у датотеци је неисправна.', false); return; }
      jsonPost(BASE + '/uvoz', { name: parsed.name, definition: cleaned }).then(function (data) {
        flash('Увезена тема „' + data.name + '". Учитана је за уређивање.', true);
        working = sanitizeDef(data.definition) || cleaned;
        editingId = data.id; editingName = data.name;
        syncControlsFromWorking();
        refresh();
        loadList();
        scrollToCreator();
      }).catch(function (e) { flash(e.message, false); });
    };
    reader.readAsText(file);
  }

  // ---- трака прегледа целе апликације --------------------------------------
  function updatePreviewBar() {
    var bar = $('creatorPreviewBar');
    if (!bar) return;
    bar.hidden = !previewActive;
  }

  function startPreview() {
    previewActive = true;
    pushLivePreview();
    updatePreviewBar();
    flash('Преглед је укључен. Крећите се кроз апликацију — измене нису сачуване.', true);
  }
  function stopPreview() {
    previewActive = false;
    restoreSavedLook();
    updatePreviewBar();
  }

  function scrollToCreator() {
    var el = $('themeCreator');
    if (el && el.scrollIntoView) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // ---- сачувано стање (за враћање из прегледа) -----------------------------
  // css = inline --pal-* које је сервер уписао на <html> ако је корисник већ на
  // custom теми; служи да враћање из прегледа врати изворни изглед.
  var SAVED = {
    palette: (window.MuseumTheme && window.MuseumTheme.palette) || 'plava-klasicna',
    customBs: (window.MuseumTheme && window.MuseumTheme.customBs) || 'light',
    mode: (window.MuseumTheme && window.MuseumTheme.mode) || 'system',
    css: document.documentElement.getAttribute('style') || ''
  };

  // ---- init ---------------------------------------------------------------
  function init() {
    if (!$('themeCreator')) return;
    bindControls();
    syncControlsFromWorking();
    refresh();
    // Учитај листу; ако корисник већ има примењену custom тему, отвори је у
    // едитору (без ремећења ако је почео нову).
    loadList().then(function (data) {
      if (!data || !data.active_id || editingId !== null) return;
      var t = (data.themes || []).filter(function (x) { return x.id === data.active_id; })[0];
      if (!t) return;
      var d = sanitizeDef(t.definition);
      if (!d) return;
      working = d; editingId = t.id; editingName = t.name;
      syncControlsFromWorking();
      refresh();
    });

    var bind = function (id, fn) { var el = $(id); if (el) el.addEventListener('click', fn); };
    bind('ccSave', saveTheme);
    bind('ccApply', applyEditorTheme);
    bind('ccPreview', startPreview);
    bind('ccPreviewStop', stopPreview);
    bind('ccNew', newTheme);
    bind('ccReset', resetDefaults);
    bind('ccExportCurrent', function () {
      // извоз тренутне (несачуване) радне дефиниције као датотеке — без сервера
      var bundle = { mis_custom_theme: 1, name: collectName() || 'Моја тема', definition: working };
      var blob = new Blob([JSON.stringify(bundle, null, 2)], { type: 'application/json' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'mis-tema.json';
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
      URL.revokeObjectURL(a.href);
    });
    var fileIn = $('ccImportFile');
    bind('ccImport', function () { if (fileIn) fileIn.click(); });
    if (fileIn) fileIn.addEventListener('change', function () {
      if (fileIn.files && fileIn.files[0]) handleImportFile(fileIn.files[0]);
      fileIn.value = '';
    });
    updatePreviewBar();

    // Ако корисник напусти страну док је преглед активан, ништа се не чува
    // (преглед је чисто клијентски); нема потребе за upozorenjem.
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  // изложи за тестове
  window.ThemeCreator = { palTokens: palTokens, contrast: contrast, bestInk: bestInk, sanitizeDef: sanitizeDef, bsTheme: bsTheme };
})();
