// Tests for the geological map layer menu (templates/admin_maps.html).
//
// The menu markup and its JavaScript live inline in the Jinja template, so the
// fixture is built from the SHIPPED template: the .map-controls block, the
// page <style> block and the OGK + menu script section are extracted verbatim,
// the handful of Jinja tags are resolved, and the result runs in a real
// Chromium. Leaflet, Bootstrap collapse and fetch are stubbed — everything
// under test (lazy loading, theme tokens, badges, localStorage, the "turn all
// layers off" button) is the real shipped code.
//
// A unit test cannot see any of this: badge counting, the collapse state that
// survives a reload, or a marker colour that follows the theme tokens.

const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const KOREN = path.resolve(__dirname, '../..');
const SABLON = fs.readFileSync(path.join(KOREN, 'templates/admin_maps.html'), 'utf8');
const OGK_JSON = JSON.parse(
  fs.readFileSync(path.join(KOREN, 'data/ogk_points.json'), 'utf8'),
);
const OGK_RADOVI = JSON.parse(
  fs.readFileSync(path.join(KOREN, 'data/ogk_radovi.json'), 'utf8'),
).radovi;

// Сервер лепи n_radova/n_radova_potvrdjenih/n_radova_verovatnih на сваку тачку
// — харнес ради исто, из истих података, да мени добије тачно оно што добија и
// у апликацији.
function prebroj(spisak, ocena) {
  return spisak.filter((rad) => rad.ocena === ocena).length;
}

const TACKE = OGK_JSON.tacke.map((tacka) => {
  const spisak = OGK_RADOVI[tacka.id] || [];
  return Object.assign({}, tacka, {
    n_radova: spisak.length,
    n_radova_potvrdjenih: prebroj(spisak, 'potvrdjen'),
    n_radova_verovatnih: prebroj(spisak, 'verovatan'),
  });
});
// Бројач филтера: тачке са бар једним потврђеним ИЛИ вероватним радом, не
// све тачке које носе било какав помен назива.
const SA_POTVRDOM = TACKE.filter(
  (tacka) => tacka.n_radova_potvrdjenih > 0 || tacka.n_radova_verovatnih > 0,
).length;

function izmedju(tekst, pocetak, kraj, ukljuciKraj) {
  const i = tekst.indexOf(pocetak);
  const j = tekst.indexOf(kraj, i);
  if (i < 0 || j < 0) throw new Error(`nije nadjeno: ${pocetak} … ${kraj}`);
  return tekst.slice(i, ukljuciKraj ? j + kraj.length : j);
}

function razresiJinju(html) {
  return html
    .replace(/\{\{\s*\(ogk_grupe or \{\}\)\.get\('(\w+)',\s*0\)\s*\}\}/g,
      (_, kljuc) => String(OGK_JSON.grupe[kljuc] ?? 0))
    .replace(/\{\{\s*ogk_sa_radovima or 0\s*\}\}/g, String(SA_POTVRDOM))
    .replace(/\{%[^%]*%\}/g, '')
    .replace(/\{\{[^}]*\}\}/g, '#');
}

const STIL = izmedju(SABLON, '<style>', '</style>').replace('<style>', '');
const MENI = razresiJinju(
  izmedju(SABLON, '<div class="map-controls">', '</div><!-- end map-controls -->', true),
);
const SKRIPTA = izmedju(
  SABLON,
  '    // ==================== OGK ТАЧКЕ 1:100 000 (Део 3) ====================',
  '    // ---- Initial load:',
);

// Токени: светла и тамна варијанта, да се промена теме стварно види на маркеру.
// `box-sizing: border-box` је оно што Bootstrap reboot ради на правој страни —
// без њега харнес лаже о ширинама.
const TOKENI = `
  *, *::before, *::after { box-sizing: border-box; }
  :root {
    --danger: rgb(220, 38, 38);
    --warning: rgb(217, 119, 6);
    --success: rgb(5, 150, 105);
    --info: rgb(37, 99, 235);
    --accent: rgb(45, 106, 79);
    --text-primary: rgb(31, 41, 55);
    --text-secondary: rgb(107, 114, 128);
    --text-muted: rgb(102, 112, 133);
    --bg-card: rgb(255, 255, 255);
    --bg-elevated: rgb(249, 250, 251);
    --border-color: rgb(229, 231, 235);
    --status-busy-bg: rgb(253, 231, 231);
    --status-busy-border: rgb(243, 194, 194);
    --status-busy-text: rgb(138, 24, 24);
    --radius-sm: 4px;
    --space-2: 0.5rem;
  }
  :root[data-theme="dark"] {
    --info: rgb(125, 176, 255);
    --bg-card: rgb(31, 41, 55);
    --text-primary: rgb(249, 250, 251);
  }
  body { margin: 0; color: var(--text-primary); background: var(--bg-card); }
`;

const STUBOVI = `
  window.__fetchPozivi = [];
  window.__fetchPada = false;
  window.fetch = function (url) {
    window.__fetchPozivi.push(url);
    if (window.__fetchPada) return Promise.reject(new Error('мрежа пала'));
    var radoviId = (url.match(/ogk-points\\/([^/]+)\\/radovi/) || [])[1];
    if (radoviId) {
      var spisak = window.__RADOVI[decodeURIComponent(radoviId)] || [];
      return Promise.resolve({
        ok: true,
        json: function () {
          var po = function (o) {
            return spisak.filter(function (r) { return r.ocena === o; }).length;
          };
          return Promise.resolve({
            success: true,
            data: {
              id: radoviId,
              naziv: '',
              radovi: spisak,
              n_radova: spisak.length,
              n_radova_potvrdjenih: po('potvrdjen'),
              n_radova_verovatnih: po('verovatan'),
              po_oceni: {
                potvrdjen: po('potvrdjen'),
                verovatan: po('verovatan'),
                nesigurno: po('nesigurno'),
                neoceneno: po('neoceneno'),
                nije: po('nije'),
              },
            },
          });
        },
      });
    }
    var grupa = (url.split('grupe=')[1] || '').split('&')[0];
    var tacke = window.__TACKE.filter(function (t) { return t.grupa === grupa; });
    return Promise.resolve({
      ok: true,
      json: function () {
        return Promise.resolve({
          success: true,
          data: {
            ukupno: tacke.length,
            grupe: {},
            radovi_izvor: window.__RADOVI_IZVOR,
            tacke: tacke,
          },
        });
      },
    });
  };

  window.L = {
    canvas: function (opcije) { return { __canvas: true, opcije: opcije }; },
    layerGroup: function () {
      var slojevi = [];
      return {
        __slojevi: slojevi,
        addLayer: function (m) { slojevi.push(m); return this; },
        clearLayers: function () { slojevi.length = 0; return this; },
        eachLayer: function (fn) { slojevi.slice().forEach(fn); return this; },
        addTo: function (m) { if (m.__dodati.indexOf(this) < 0) m.__dodati.push(this); return this; },
      };
    },
    circleMarker: function (latlng, stil) {
      return {
        __latlng: latlng,
        __osluskivaci: {},
        options: Object.assign({}, stil),
        bindPopup: function (html) { this.__popup = html; return this; },
        on: function (dogadjaj, fn) {
          (this.__osluskivaci[dogadjaj] = this.__osluskivaci[dogadjaj] || []).push(fn);
          return this;
        },
        // Прави popupopen: Leaflet прво убаци садржај у DOM, па опали
        // догађај на маркеру са {popup} који зна свој елемент.
        __otvoriPopup: function () {
          var el = document.createElement('div');
          el.className = 'leaflet-popup';
          el.innerHTML = this.__popup;
          document.body.appendChild(el);
          var popover = { getElement: function () { return el; } };
          (this.__osluskivaci.popupopen || []).forEach(function (fn) {
            fn({ popup: popover });
          });
          return el;
        },
        setStyle: function (s) { Object.assign(this.options, s); return this; },
        setRadius: function (r) { this.options.radius = r; return this; },
      };
    },
  };
  window.map = {
    __dodati: [],
    __zum: 8,
    __osluskivaci: {},
    removeLayer: function (sloj) {
      var i = this.__dodati.indexOf(sloj);
      if (i >= 0) this.__dodati.splice(i, 1);
    },
    hasLayer: function (sloj) { return this.__dodati.indexOf(sloj) >= 0; },
    getZoom: function () { return this.__zum; },
    on: function (dogadjaj, fn) {
      (this.__osluskivaci[dogadjaj] = this.__osluskivaci[dogadjaj] || []).push(fn);
    },
    // Прави зум: помери ниво па опали zoomend, исто како Leaflet ради.
    __zumiraj: function (z) {
      this.__zum = z;
      (this.__osluskivaci.zoomend || []).forEach(function (fn) { fn(); });
    },
  };
  window.bringThematicLayersToFront = function () {};
  window.toFiniteNumber = function (v) {
    var n = typeof v === 'number' ? v : parseFloat(v);
    return Number.isFinite(n) ? n : null;
  };
  window.formatCoord = function (v, d) {
    var n = window.toFiniteNumber(v);
    return n === null ? '—' : n.toFixed(d);
  };
  window.escHtml = function (s) {
    if (!s) return '';
    var d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  };
  window.safeRenderItems = function (items, ime, render) {
    items.forEach(function (item, i) {
      try { render(item, i); } catch (e) { console.error(ime, i, e); }
    });
  };

  // Минимални Bootstrap collapse: класа .show + прави shown/hidden догађаји.
  document.addEventListener('click', function (e) {
    var okidac = e.target.closest('[data-bs-toggle="collapse"]');
    if (!okidac) return;
    e.preventDefault();
    var cilj = document.querySelector(okidac.getAttribute('href'));
    if (!cilj) return;
    var otvara = !cilj.classList.contains('show');
    cilj.classList.toggle('show', otvara);
    okidac.setAttribute('aria-expanded', otvara ? 'true' : 'false');
    cilj.dispatchEvent(new Event(otvara ? 'shown.bs.collapse' : 'hidden.bs.collapse'));
  });
`;

// setContent даје about:blank, а на opaque origin-у localStorage не ради —
// зато се харнес служи са правог (пресретнутог) origin-а.
const HARNES_URL = 'http://mis.harness.test/maps-menu';

async function ucitajMeni(page, {
  tacke = null, localStorageStanje = null, radoviIzvor = 'ok', radovi = null,
} = {}) {
  await page.route(HARNES_URL, (route) => route.fulfill({
    status: 200,
    contentType: 'text/html; charset=utf-8',
    body:
      `<!doctype html><html><head><meta charset="utf-8"><style>${TOKENI}${STIL}</style></head>` +
      `<body><div id="map-right-col">${MENI}</div></body></html>`,
  }));
  await page.goto(HARNES_URL);
  await page.evaluate(([izabrane, stanje, izvor, spisak]) => {
    window.__TACKE = izabrane;
    window.__RADOVI_IZVOR = izvor;
    window.__RADOVI = spisak;
    if (stanje) localStorage.setItem('mis.maps.grupe', stanje);
  }, [
    tacke || TACKE.slice(0, 400),
    localStorageStanje,
    radoviIzvor,
    radovi || {},
  ]);
  await page.addScriptTag({ content: STUBOVI });
  await page.addScriptTag({ content: SKRIPTA });
}

test('бројач у заглављу групе прати упаљене слојеве', async ({ page }) => {
  await ucitajMeni(page);

  // Подлога креће са OSM + геолошки прекривач упаљеним.
  await expect(page.locator('[data-map-group-badge="podloga"]')).toHaveText('2');
  await expect(page.locator('[data-map-group-badge="geologija"]')).toHaveText('0');

  await page.locator('#toggle-ogk-busotine').check();
  await expect(page.locator('[data-map-group-badge="geologija"]')).toHaveText('1');

  await page.locator('#toggle-ogk-rasedi').check();
  await expect(page.locator('[data-map-group-badge="geologija"]')).toHaveText('2');
  // Друге групе се не мешају.
  await expect(page.locator('[data-map-group-badge="podloga"]')).toHaveText('2');

  await page.locator('#toggle-ogk-busotine').uncheck();
  await expect(page.locator('[data-map-group-badge="geologija"]')).toHaveText('1');
});

test('бејџ прекидача носи број тачака групе још пре учитавања слоја', async ({ page }) => {
  await ucitajMeni(page);
  await expect(page.locator('[data-ogk-broj="busotine"]'))
    .toHaveText(String(OGK_JSON.grupe.busotine));
  await expect(page.locator('[data-ogk-broj="rudnici"]'))
    .toHaveText(String(OGK_JSON.grupe.rudnici));
});

test('стање групе преживљава поновно учитавање (mis.maps.grupe)', async ({ page }) => {
  await ucitajMeni(page);

  const geologija = page.locator('#mapGroupGeologija');
  await expect(geologija).not.toHaveClass(/show/);
  await page.locator('[href="#mapGroupGeologija"]').click();
  await expect(geologija).toHaveClass(/show/);

  const upisano = await page.evaluate(() => localStorage.getItem('mis.maps.grupe'));
  expect(JSON.parse(upisano).geologija).toBe(true);

  // Ново учитавање стране са затеченим стањем: група је и даље отворена,
  // а Подлога (подразумевано отворена) затворена.
  await ucitajMeni(page, {
    localStorageStanje: JSON.stringify({ geologija: true, podloga: false }),
  });
  await expect(page.locator('#mapGroupGeologija')).toHaveClass(/show/);
  await expect(page.locator('[href="#mapGroupGeologija"]'))
    .toHaveAttribute('aria-expanded', 'true');
  await expect(page.locator('#mapGroupPodloga')).not.toHaveClass(/show/);
});

test('„Угаси све слојеве“ шаље прави change догађај и штеди OSM подлогу', async ({ page }) => {
  await ucitajMeni(page);

  // Затечени слушалац какав постојећи JS већ качи по id-у.
  await page.evaluate(() => {
    window.__pogodjeni = [];
    ['toggle-ore-deposits', 'toggle-overlay', 'toggle-basemap', 'toggle-ogk-rudnici']
      .forEach(function (id) {
        document.getElementById(id).addEventListener('change', function () {
          window.__pogodjeni.push(id + ':' + this.checked);
        });
      });
  });

  await page.locator('#toggle-ore-deposits').check();
  await page.locator('#toggle-ogk-rudnici').check();
  await expect(page.locator('[data-map-group-badge="rudarstvo"]')).toHaveText('1');

  await page.locator('#btn-ugasi-sve-slojeve').click();

  await expect(page.locator('#toggle-ore-deposits')).not.toBeChecked();
  await expect(page.locator('#toggle-ogk-rudnici')).not.toBeChecked();
  await expect(page.locator('#toggle-overlay')).not.toBeChecked();
  // OSM подлога остаје — она није тематски слој.
  await expect(page.locator('#toggle-basemap')).toBeChecked();

  const pogodjeni = await page.evaluate(() => window.__pogodjeni);
  expect(pogodjeni).toContain('toggle-ore-deposits:false');
  expect(pogodjeni).toContain('toggle-overlay:false');
  expect(pogodjeni).toContain('toggle-ogk-rudnici:false');
  expect(pogodjeni).not.toContain('toggle-basemap:false');

  await expect(page.locator('[data-map-group-badge="rudarstvo"]')).toHaveText('0');
  await expect(page.locator('[data-map-group-badge="podloga"]')).toHaveText('1');
});

test('OGK слој се учитава лењо и кешира — други пут нема захтева', async ({ page }) => {
  const busotine = TACKE.filter((t) => t.grupa === 'busotine');
  await ucitajMeni(page, { tacke: busotine });

  expect(await page.evaluate(() => window.__fetchPozivi.length)).toBe(0);

  await page.locator('#toggle-ogk-busotine').check();
  await expect.poll(() => page.evaluate(() => window.__fetchPozivi.length)).toBe(1);
  expect(await page.evaluate(() => window.__fetchPozivi[0]))
    .toBe('/api/map/ogk-points?grupe=busotine');

  // Слој је додат на карту са свим тачкама групе.
  expect(await page.evaluate(() => window.map.__dodati.length)).toBe(1);
  expect(await page.evaluate(() => window.map.__dodati[0].__slojevi.length))
    .toBe(busotine.length);

  await page.locator('#toggle-ogk-busotine').uncheck();
  await page.locator('#toggle-ogk-busotine').check();
  await page.waitForTimeout(100);
  expect(await page.evaluate(() => window.__fetchPozivi.length)).toBe(1);
});

test('маркер расте са зумом, и то само на слојевима који су на карти', async ({ page }) => {
  const busotine = TACKE.filter((t) => t.grupa === 'busotine').slice(0, 20);
  const izvori = TACKE.filter((t) => t.grupa === 'izvori').slice(0, 20);
  await ucitajMeni(page, { tacke: busotine.concat(izvori) });

  await page.locator('#toggle-ogk-busotine').check();
  await expect.poll(() => page.evaluate(() => window.map.__dodati.length)).toBe(1);

  // Харнес креће са зумом 8 → полупречник 6 (не затечених 4).
  const poluprecnik = () => page.evaluate(
    () => window.map.__dodati[0].__slojevi[0].options.radius,
  );
  expect(await poluprecnik()).toBe(6);
  expect(await page.evaluate(
    () => window.map.__dodati[0].__slojevi[0].options.weight,
  )).toBe(1.25);

  // Приказ целе Србије — најмањи, али и даље већи од затечена 4.
  await page.evaluate(() => window.map.__zumiraj(7));
  expect(await poluprecnik()).toBe(5);

  // Ниво листа 1:100 000 и ближе — таван на 11.
  await page.evaluate(() => window.map.__zumiraj(11));
  expect(await poluprecnik()).toBe(9);
  await page.evaluate(() => window.map.__zumiraj(14));
  expect(await poluprecnik()).toBe(10);

  // Угашен слој се не дира: упали га на зуму 14 и он одмах носи 11,
  // а не вредност затечену пре зумирања.
  await page.locator('#toggle-ogk-izvori').check();
  await expect.poll(() => page.evaluate(() => window.map.__dodati.length)).toBe(2);
  expect(await page.evaluate(
    () => window.map.__dodati[1].__slojevi[0].options.radius,
  )).toBe(10);
});

test('пад fetch-а даје видљив црвен текст поред прекидача', async ({ page }) => {
  await ucitajMeni(page);
  await page.evaluate(() => { window.__fetchPada = true; });

  const greska = page.locator('[data-ogk-greska="izvori"]');
  await expect(greska).toBeHidden();

  await page.locator('#toggle-ogk-izvori').check();

  await expect(greska).toBeVisible();
  await expect(greska).toContainText('Слој није учитан');
  const boja = await greska.evaluate((el) => getComputedStyle(el).color);
  expect(boja).toBe('rgb(138, 24, 24)');  // --status-busy-text (AA и у тамној теми)

  // Гашење прекидача склања поруку.
  await page.locator('#toggle-ogk-izvori').uncheck();
  await expect(greska).toBeHidden();
});

test('боја маркера долази из токена теме и прати промену теме', async ({ page }) => {
  const busotine = TACKE.filter((t) => t.grupa === 'busotine').slice(0, 20);
  await ucitajMeni(page, { tacke: busotine });

  // Узорак боје у менију већ носи токен.
  const uzorak = page.locator('[data-ogk-swatch="busotine"]');
  await expect(uzorak).toHaveCSS('background-color', 'rgb(37, 99, 235)');

  await page.locator('#toggle-ogk-busotine').check();
  await expect.poll(() => page.evaluate(() => window.map.__dodati.length)).toBe(1);

  const svetla = await page.evaluate(
    () => window.map.__dodati[0].__slojevi[0].options.fillColor,
  );
  expect(svetla).toBe('rgb(37, 99, 235)');   // --info, светла тема

  await page.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark'));

  await expect.poll(() => page.evaluate(
    () => window.map.__dodati[0].__slojevi[0].options.fillColor,
  )).toBe('rgb(125, 176, 255)');             // --info, тамна тема
  await expect.poll(() => page.evaluate(
    () => window.map.__dodati[0].__slojevi[0].options.color,
  )).toBe('rgb(31, 41, 55)');                // --bg-card обод, тамна тема
  await expect(uzorak).toHaveCSS('background-color', 'rgb(125, 176, 255)');
});

test('мени ради и на уском екрану, без хоризонталног прелива', async ({ page }) => {
  await page.setViewportSize({ width: 380, height: 720 });
  await ucitajMeni(page);

  const kontrole = page.locator('.map-controls');
  const prelivi = await kontrole.evaluate(
    (el) => el.scrollWidth - el.clientWidth,
  );
  expect(prelivi).toBeLessThanOrEqual(1);

  // Заглавље групе се и даље отвара и прекидач унутра ради.
  await page.locator('[href="#mapGroupGeologija"]').click();
  await expect(page.locator('#mapGroupGeologija')).toHaveClass(/show/);
  await page.locator('#toggle-ogk-fosili').check();
  await expect(page.locator('[data-map-group-badge="geologija"]')).toHaveText('1');
});

// --- Радови по OGK тачки -----------------------------------------------------

// Банска (каменолом): 1 потврђен, 2 вероватна, 1 несигуран, 4 „није“ —
// једина тачка у испоруци која носи све четири оцене одједном.
const MESOVITA = 'K34-42-0043';
// Сењ (каменолом): 8 радова о ГРАДУ Сењу, ниједан о кречњаку. Тачка која
// мора да каже да ниједан прикупљени рад није њен.
const BEZ_POTVRDE = 'K34-07-0055';

function samoJednaTacka(id) {
  return {
    tacke: [TACKE.find((tacka) => tacka.id === id)],
    radovi: { [id]: OGK_RADOVI[id] },
  };
}

test('поповер OGK тачке приказује рад са https линком, лењо', async ({ page }) => {
  await ucitajMeni(page, samoJednaTacka(MESOVITA));

  await page.locator('#toggle-ogk-kamenolomi').check();
  await expect.poll(() => page.evaluate(() => window.map.__dodati.length)).toBe(1);

  // Поповер креће празан: списак се тражи тек кад се поповер отвори.
  const pocetni = await page.evaluate(
    () => window.map.__dodati[0].__slojevi[0].__popup,
  );
  expect(pocetni).toContain('data-ogk-radovi="' + MESOVITA + '"');
  expect(pocetni).toContain('учитавам');
  expect(await page.evaluate(() => window.__fetchPozivi.length)).toBe(1);

  await page.evaluate(() => window.map.__dodati[0].__slojevi[0].__otvoriPopup());
  const popover = page.locator('.leaflet-popup');
  await expect(popover.locator('.ogk-rad').first()).toBeVisible();
  expect(await page.evaluate(() => window.__fetchPozivi[1]))
    .toBe('/api/map/ogk-points/' + MESOVITA + '/radovi');

  const href = await popover.locator('.ogk-rad a').first().getAttribute('href');
  expect(href).toMatch(/^https:\/\//);
  await expect(popover.locator('.ogk-rad a').first())
    .toHaveAttribute('rel', 'noopener noreferrer');
});

test('поповер има три одељка: потврђени, вероватни, склопљено остало', async ({ page }) => {
  const spisak = OGK_RADOVI[MESOVITA];
  const potvrdjenih = prebroj(spisak, 'potvrdjen');
  const verovatnih = prebroj(spisak, 'verovatan');
  const ostalih = spisak.length - potvrdjenih - verovatnih;
  expect(potvrdjenih).toBeGreaterThan(0);
  expect(verovatnih).toBeGreaterThan(0);
  expect(ostalih).toBeGreaterThan(0);
  await ucitajMeni(page, samoJednaTacka(MESOVITA));

  await page.locator('#toggle-ogk-kamenolomi').check();
  await expect.poll(() => page.evaluate(() => window.map.__dodati.length)).toBe(1);
  await page.evaluate(() => window.map.__dodati[0].__slojevi[0].__otvoriPopup());

  const popover = page.locator('.leaflet-popup');
  const naslovi = popover.locator('.ogk-radovi-naslov');
  await expect(naslovi).toHaveCount(2);
  await expect(naslovi.nth(0))
    .toHaveText('Радови о овом локалитету (' + potvrdjenih + ')');
  await expect(naslovi.nth(1))
    .toHaveText('Вероватно исти простор (' + verovatnih + ')');
  // Оба одељка су одмах видљива, али је други визуелно подређен.
  await expect(naslovi.nth(0)).toBeVisible();
  await expect(naslovi.nth(1)).toBeVisible();
  await expect(naslovi.nth(1)).toHaveClass(/ogk-radovi-naslov--slabiji/);
  const [jaci, slabiji] = await naslovi.evaluateAll(
    (els) => els.map((el) => getComputedStyle(el).textTransform),
  );
  expect(jaci).toBe('uppercase');
  expect(slabiji).toBe('none');

  // Трећи одељак: несигурно + неповезано, склопљено и затворено.
  const detalji = popover.locator('details');
  await expect(detalji).toHaveCount(1);
  await expect(detalji.locator('summary'))
    .toHaveText('Несигурно и неповезано (' + ostalih + ')');
  expect(await detalji.evaluate((el) => el.open)).toBe(false);
  // Ништа се не брише — само је склопљено.
  await expect(detalji.locator('.ogk-rad')).toHaveCount(ostalih);
  await expect(detalji.locator('.ogk-rad').first()).toBeHidden();
  await detalji.locator('summary').click();
  await expect(detalji.locator('.ogk-rad').first()).toBeVisible();

  // Ниједан рад није испао: 3 видљива + остатак у склопивом одељку.
  await expect(popover.locator('.ogk-rad')).toHaveCount(spisak.length);
});

test('испод сваког рада стоји разлог његове оцене', async ({ page }) => {
  const spisak = OGK_RADOVI[MESOVITA];
  await ucitajMeni(page, samoJednaTacka(MESOVITA));

  await page.locator('#toggle-ogk-kamenolomi').check();
  await expect.poll(() => page.evaluate(() => window.map.__dodati.length)).toBe(1);
  await page.evaluate(() => window.map.__dodati[0].__slojevi[0].__otvoriPopup());

  const popover = page.locator('.leaflet-popup');
  await expect(popover.locator('.ogk-rad-razlog')).toHaveCount(spisak.length);
  // Разлог првог (потврђеног) рада стоји уз њега, реч по реч из података.
  await expect(popover.locator('.ogk-rad').first().locator('.ogk-rad-razlog'))
    .toHaveText(spisak[0].razlog);
  // Пригушен, али кроз токен теме — не хардкодована боја.
  expect(await popover.locator('.ogk-rad-razlog').first()
    .evaluate((el) => getComputedStyle(el).color)).toBe('rgb(102, 112, 133)');
});

test('тачка без иједног потврђеног рада то каже отворено', async ({ page }) => {
  const spisak = OGK_RADOVI[BEZ_POTVRDE];
  expect(spisak.length).toBeGreaterThan(0);
  expect(prebroj(spisak, 'potvrdjen') + prebroj(spisak, 'verovatan')).toBe(0);
  await ucitajMeni(page, samoJednaTacka(BEZ_POTVRDE));

  await page.locator('#toggle-ogk-kamenolomi').check();
  await expect.poll(() => page.evaluate(() => window.map.__dodati.length)).toBe(1);
  await page.evaluate(() => window.map.__dodati[0].__slojevi[0].__otvoriPopup());

  const popover = page.locator('.leaflet-popup');
  const poruka = popover.locator('.ogk-radovi-prazno');
  await expect(poruka).toBeVisible();
  await expect(poruka).toHaveText('Ниједан прикупљени рад није потврђен за овај локалитет.');
  // Порука долази ПРЕ склопљеног одељка, и нема лажног одељка потврђених.
  await expect(popover.locator('.ogk-radovi-naslov')).toHaveCount(0);
  const detalji = popover.locator('details');
  await expect(detalji).toHaveCount(1);
  expect(await detalji.evaluate((el) => el.open)).toBe(false);
  await expect(detalji.locator('.ogk-rad')).toHaveCount(spisak.length);
});

test('url који није http(s) се исписује као текст, не као href', async ({ page }) => {
  const tacka = Object.assign({}, TACKE.find((t) => t.id === MESOVITA), {
    n_radova: 1, n_radova_potvrdjenih: 1, n_radova_verovatnih: 0,
  });
  await ucitajMeni(page, {
    tacke: [tacka],
    radovi: {
      [MESOVITA]: [{
        naslov: 'Сумњив рад', godina: 2020, autori: 'Аутор', casopis: 'Часопис',
        doi: '', url: 'javascript:alert(1)', pdf_url: 'javascript:alert(2)',
        ocena: 'potvrdjen', razlog: 'разлог',
      }],
    },
  });

  await page.locator('#toggle-ogk-kamenolomi').check();
  await expect.poll(() => page.evaluate(() => window.map.__dodati.length)).toBe(1);
  await page.evaluate(() => window.map.__dodati[0].__slojevi[0].__otvoriPopup());

  const popover = page.locator('.leaflet-popup');
  await expect(popover.locator('.ogk-rad')).toContainText('Сумњив рад');
  await expect(popover.locator('.ogk-rad a')).toHaveCount(0);
});

test('пад захтева за радовима даје црвену поруку у самом поповеру', async ({ page }) => {
  await ucitajMeni(page, samoJednaTacka(MESOVITA));

  await page.locator('#toggle-ogk-kamenolomi').check();
  await expect.poll(() => page.evaluate(() => window.map.__dodati.length)).toBe(1);
  await page.evaluate(() => { window.__fetchPada = true; });
  await page.evaluate(() => window.map.__dodati[0].__slojevi[0].__otvoriPopup());

  const greska = page.locator('.leaflet-popup .ogk-radovi-greska');
  await expect(greska).toBeVisible();
  await expect(greska).toContainText('Радови нису учитани');
  expect(await greska.evaluate((el) => getComputedStyle(el).color))
    .toBe('rgb(138, 24, 24)');   // --status-busy-text (AA и у тамној теми)
});

test('„Само са потврђеним радовима“ смањује број маркера и враћа их', async ({ page }) => {
  const busotine = TACKE.filter((t) => t.grupa === 'busotine');
  const saPotvrdom = busotine.filter(
    (t) => t.n_radova_potvrdjenih > 0 || t.n_radova_verovatnih > 0,
  ).length;
  const saBiloKakvimRadom = busotine.filter((t) => t.n_radova > 0).length;
  expect(saPotvrdom).toBeGreaterThan(0);
  expect(saPotvrdom).toBeLessThan(busotine.length);
  // Филтер више не значи „има било какав рад“ — иначе тест ништа не доказује.
  expect(saPotvrdom).toBeLessThan(saBiloKakvimRadom);
  await ucitajMeni(page, { tacke: busotine });

  await expect(page.locator('#toggle-ogk-samo-radovi + label'))
    .toContainText('Само са потврђеним радовима');
  await expect(page.locator('[data-ogk-broj="samo-radovi"]'))
    .toHaveText(String(SA_POTVRDOM));

  await page.locator('#toggle-ogk-busotine').check();
  const iscrtano = () => page.evaluate(() => window.map.__dodati[0].__slojevi.length);
  await expect.poll(iscrtano).toBe(busotine.length);

  await page.locator('#toggle-ogk-samo-radovi').check();
  await expect.poll(iscrtano).toBe(saPotvrdom);
  // Бејџ прати оно што је исцртано, а сервер се не пита поново.
  await expect(page.locator('[data-ogk-broj="busotine"]')).toHaveText(String(saPotvrdom));
  expect(await page.evaluate(() => window.__fetchPozivi.length)).toBe(1);

  // Тачка са радовима од којих ниједан није њен НЕ пролази филтер.
  const preziveli = await page.evaluate(
    () => window.map.__dodati[0].__slojevi.map((m) => m.__popup),
  );
  const tudji = busotine.find((t) => t.n_radova > 0 && !t.n_radova_potvrdjenih
    && !t.n_radova_verovatnih);
  expect(tudji).toBeTruthy();
  expect(preziveli.some((html) => html.includes('data-ogk-radovi="' + tudji.id + '"')))
    .toBe(false);

  await page.locator('#toggle-ogk-samo-radovi').uncheck();
  await expect.poll(iscrtano).toBe(busotine.length);
  await expect(page.locator('[data-ogk-broj="busotine"]')).toHaveText(String(busotine.length));
});

test('филтер радова памти стање, а не дира mis.maps.grupe', async ({ page }) => {
  await ucitajMeni(page, { localStorageStanje: JSON.stringify({ geologija: true }) });

  await page.locator('#toggle-ogk-samo-radovi').check();
  expect(await page.evaluate(() => localStorage.getItem('mis.maps.ogk-samo-radovi')))
    .toBe('1');
  expect(await page.evaluate(() => localStorage.getItem('mis.maps.grupe')))
    .toBe(JSON.stringify({ geologija: true }));

  // Ново учитавање стране: прекидач је и даље упаљен.
  await ucitajMeni(page);
  await expect(page.locator('#toggle-ogk-samo-radovi')).toBeChecked();
  await expect(page.locator('#mapGroupGeologija')).toHaveClass(/show/);
});

test('сервер без ogk_radovi.json се види поред прекидача филтера', async ({ page }) => {
  await ucitajMeni(page, { radoviIzvor: 'nedostaje' });

  const greska = page.locator('[data-ogk-greska="samo-radovi"]');
  await expect(greska).toBeHidden();

  await page.locator('#toggle-ogk-izvori').check();
  await expect(greska).toBeVisible();
  await expect(greska).toContainText('Радови нису доступни');
});

test('ниједан затечени прекидач слоја није нестао из менија', async ({ page }) => {
  await ucitajMeni(page);
  const postojeci = [
    'toggle-overlay', 'toggle-basemap', 'toggle-field-markers',
    'toggle-ore-deposits', 'toggle-stratigraphy', 'toggle-paleontology',
    'toggle-sanja-mammals', 'toggle-mining-operations',
    'toggle-exploration-licenses', 'toggle-map-sheets', 'toggle-geo-hover',
    'toggle-calibration',
  ];
  for (const id of postojeci) {
    await expect(page.locator(`#${id}`)).toHaveCount(1);
  }
});
