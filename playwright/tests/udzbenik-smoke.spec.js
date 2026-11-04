const { test, expect } = require('@playwright/test');

// Smoke мотора уџбеника (static/udzbenik/ bundle) на живом серверу, са
// сесијом кустоса (CYPRESS_EMPLOYEE_*). Прескаче се без креденцијала.
// Пре покретања: python playwright/tests/helpers/seed_udzbenik_smoke.py seed
// (тест-уџбеник udztest-smoke са блоком literatura — на dev-у SciSearch није
// повезан, па блок мора бити сиви „недоступан“); после: ... clean.
// Dev сервер је иза nginx-а са self-signed сертификатом → ignoreHTTPSErrors.

test.use({ ignoreHTTPSErrors: true });

// Headless Chromium у sandbox-у без GPU-а нема WebGL ни са SwiftShader-ом:
// Three.js (weather_particles.js из base.html и мотор за сцене) јави „Error
// creating WebGL context“ и падне на резервне PNG-ове. То је окружење, не
// мотор, па се једино та порука толерише — и то само кад прегледач стварно
// нема WebGL (на машини са GPU-ом тест је строг).
const BEZ_WEBGL = /Error creating WebGL context/;

const employeeEmail = process.env.CYPRESS_EMPLOYEE_EMAIL;
const employeePassword = process.env.CYPRESS_EMPLOYEE_PASSWORD;

const LEKCIJE = [
  { zbirka: 'minerali', poglavlje: 'postanak-minerala', lekcija: 'sedimentni-i-povrsinski-procesi',
    slike: true, dijagram: true },
  { zbirka: 'minerali', poglavlje: 'kristalohemija', lekcija: 'polimorfizam-i-politipizam',
    slike: false, dijagram: 'fazni-dijagram' },
  { zbirka: 'minerali', poglavlje: 'opticka-mineralogija', lekcija: 'opticki-znak-i-konoskopija',
    slike: false, dijagram: 'konoskopska-figura' },
];
const SMOKE = { zbirka: 'udztest-smoke', poglavlje: 'smoke', lekcija: 'literatura-i-dijagram' };

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(employeeEmail);
  await page.getByTestId('login-password').fill(employeePassword);
  await page.getByTestId('login-submit').click();
  await expect(page).not.toHaveURL(/\/login$/);
}

function hvatajGreske(page) {
  const greske = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') { greske.push(`console ${msg.location().url}: ${msg.text()}`); }
  });
  page.on('pageerror', (err) => greske.push(`pageerror: ${err.message}`));
  return greske;
}

async function proveriGreske(page, greske) {
  const imaWebgl = await page.evaluate(() => {
    const c = document.createElement('canvas');
    return !!(c.getContext('webgl') || c.getContext('experimental-webgl'));
  });
  const relevantne = imaWebgl ? greske : greske.filter((g) => !BEZ_WEBGL.test(g));
  expect(relevantne).toEqual([]);
  return imaWebgl;
}

async function otvoriLekciju(page, l) {
  await page.goto(`/udzbenik/${l.zbirka}/${l.poglavlje}/${l.lekcija}`);
  await expect(page.locator('#udzbenik-app .udzbenik-blok').first()).toBeVisible({ timeout: 20_000 });
  // Лењи chunk дијаграма и слике стижу после првог блока.
  await page.waitForLoadState('networkidle');
}

test.describe('Уџбеник — smoke мотора', () => {
  test.skip(!employeeEmail || !employeePassword, 'Кустос креденцијали (CYPRESS_EMPLOYEE_*) су обавезни.');

  test('bundle је нов и статика стиже', async ({ page }) => {
    const v = await page.request.get('/static/udzbenik/VERZIJA.txt');
    expect(v.status()).toBe(200);
    expect(await v.text()).toMatch(/^mis-udzbenik 700587c/);
    for (const f of ['udzbenik.js', 'udzbenik-three.js', 'udzbenik-dijagrami.js', 'udzbenik.css']) {
      const r = await page.request.get(`/static/udzbenik/${f}`);
      expect(r.status(), f).toBe(200);
    }
  });

  for (const l of LEKCIJE) {
    test(`лекција ${l.poglavlje}/${l.lekcija}: API + мотор`, async ({ page }) => {
      await login(page);

      const api = await page.request.get(`/api/udzbenik/${l.zbirka}/lekcija/${l.poglavlje}/${l.lekcija}`);
      test.skip(api.status() === 404, 'Садржај уџбеника „minerali“ није увезен у ову базу.');
      expect(api.status()).toBe(200);
      const telo = await api.json();
      const blokovi = telo.lekcija.blokovi;
      expect(Array.isArray(blokovi) && blokovi.length > 0).toBeTruthy();
      if (l.slike) {
        const slike = blokovi.filter((b) => b.tip === 'slika');
        expect(slike.length).toBeGreaterThan(0);
        for (const s of slike) {
          expect(s.nedostupan, `slika ${s.id} nedostupna: ${s.razlog}`).toBeFalsy();
          expect(s.url).toMatch(/^\//);
        }
      }
      if (typeof l.dijagram === 'string') {
        expect(blokovi.some((b) => b.tip === 'dijagram' && b.dijagram === l.dijagram)).toBeTruthy();
      }

      const greske = hvatajGreske(page);
      await otvoriLekciju(page, l);

      await expect(page.locator('.udzbenik-blok--nepoznat')).toHaveCount(0);
      const brojBlokova = await page.locator('#udzbenik-app .udzbenik-blok').count();
      expect(brojBlokova).toBe(blokovi.length);

      if (l.slike) {
        const imgs = page.locator('.udzbenik-blok--slika img.udzbenik-slika-element');
        const n = await imgs.count();
        expect(n).toBeGreaterThan(0);
        for (let i = 0; i < n; i += 1) {
          const img = imgs.nth(i);
          await img.scrollIntoViewIfNeeded(); // loading="lazy"
          const src = await img.getAttribute('src');
          const r = await page.request.get(src);
          expect(r.status(), src).toBe(200);
          expect(r.headers()['content-type'], src).toMatch(/^image\//);
          await expect.poll(() => img.evaluate((el) => el.complete && el.naturalWidth), src).toBeGreaterThan(0);
        }
      }

      if (l.dijagram) {
        const dijagrami = page.locator('.udzbenik-blok--dijagram');
        const n = await dijagrami.count();
        expect(n).toBeGreaterThan(0);
        for (let i = 0; i < n; i += 1) {
          const d = dijagrami.nth(i);
          await d.scrollIntoViewIfNeeded();
          const svg = d.locator('svg').first();
          await expect(svg).toBeVisible({ timeout: 15_000 });
          expect(await svg.evaluate((el) => el.childElementCount)).toBeGreaterThan(0);
          // Резервни PNG је увек у DOM-у; мотор га сакрије (hidden) кад SVG успе.
          await expect(d.locator('.udzbenik-dijagram-rezerva')).toBeHidden();
        }
      }

      const imaWebgl = await proveriGreske(page, greske);
      if (!imaWebgl) {
        // Без WebGL-а сцене морају пасти на резервни PNG из bundle-а (200).
        const rezerve = page.locator('.udzbenik-blok--scena img[src*="/static/udzbenik/rezerve/"]');
        for (let i = 0; i < await rezerve.count(); i += 1) {
          const src = await rezerve.nth(i).getAttribute('src');
          const r = await page.request.get(src);
          expect(r.status(), src).toBe(200);
          expect(r.headers()['content-type'], src).toMatch(/^image\/png/);
        }
      }
    });
  }

  test('блок literatura без SciSearch-а = сиви „недоступан“', async ({ page }) => {
    await login(page);
    const api = await page.request.get(`/api/udzbenik/${SMOKE.zbirka}/lekcija/${SMOKE.poglavlje}/${SMOKE.lekcija}`);
    test.skip(api.status() === 404, 'Тест-уџбеник није seed-ован (seed_udzbenik_smoke.py seed).');
    expect(api.status()).toBe(200);
    const telo = await api.json();
    const lit = telo.lekcija.blokovi.find((b) => b.tip === 'literatura');
    expect(lit).toBeTruthy();
    expect(lit.nedostupan).toBe(true);
    expect(lit.razlog).toBe('biblioteka nije povezana');
    expect(lit.rezultati).toBeUndefined();

    const greske = hvatajGreske(page);
    await otvoriLekciju(page, SMOKE);
    await expect(page.locator('.udzbenik-blok--nepoznat')).toHaveCount(0);

    const blok = page.locator('.udzbenik-blok--literatura .udzbenik-literatura--nedostupan');
    await expect(blok).toHaveCount(1);
    await expect(blok).toBeVisible();
    await expect(blok.locator('.udzbenik-literatura-nedostupan-razlog')).toHaveText('biblioteka nije povezana');
    await expect(blok.locator('.udzbenik-literatura-nedostupan-naslov')).toContainText('Пирит у литератури');
    // „Сиви блок“: непрозирна позадина са R≈G≈B (нема боје), а не провидна.
    const boja = await blok.evaluate((el) => getComputedStyle(el).backgroundColor);
    const m = boja.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
    expect(m, boja).not.toBeNull();
    const [r, g, b] = [m[1], m[2], m[3]].map(Number);
    expect(m[4] === undefined || Number(m[4]) > 0, boja).toBeTruthy();
    expect(Math.max(r, g, b) - Math.min(r, g, b), boja).toBeLessThanOrEqual(24);

    // Дијаграм у истој лекцији се исцртава (лењи chunk).
    const svg = page.locator('.udzbenik-blok--dijagram svg').first();
    await svg.scrollIntoViewIfNeeded();
    await expect(svg).toBeVisible({ timeout: 15_000 });
    expect(await svg.evaluate((el) => el.childElementCount)).toBeGreaterThan(0);
    await expect(page.locator('.udzbenik-blok--dijagram .udzbenik-dijagram-rezerva')).toBeHidden();

    await proveriGreske(page, greske);
  });
});
