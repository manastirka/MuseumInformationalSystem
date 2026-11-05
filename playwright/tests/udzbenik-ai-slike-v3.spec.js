const { test, expect } = require('@playwright/test');

// AI илустрације v3 (udzbenik/ai-slike-mapa.json) на живом dev серверу, са
// сесијом кустоса (CYPRESS_EMPLOYEE_*): свака AI слика у лекцији је из мапе
// (нов потпис), стиже као image/* и исцрта се; блокови slika-literatura постоје
// за пријављеног (SciSearch без /svc/figures → „недоступан“, лекција се учита),
// а анонимни не види ни лекцију (401 / преусмерење на пријаву).
// nginx: 10 r/s + burst 20 (503 преко тога) → једна пријава, лекције редом са
// паузом, не паралелно.

test.use({ ignoreHTTPSErrors: true });
test.describe.configure({ mode: 'serial' });

const BEZ_WEBGL = /Error creating WebGL context/;
const MAPA = require('../../udzbenik/ai-slike-mapa.json');
const POTPISI = new Set(MAPA.map((m) => m.potpis));

const employeeEmail = process.env.CYPRESS_EMPLOYEE_EMAIL;
const employeePassword = process.env.CYPRESS_EMPLOYEE_PASSWORD;

const LEKCIJE = [
  ['postanak-minerala', 'magmatski-i-pegmatitski-procesi'],
  ['postanak-minerala', 'hidrotermalni-procesi'],
  ['postanak-minerala', 'sedimentni-i-povrsinski-procesi'],
  ['postanak-minerala', 'metamorfni-procesi'],
  ['kristalografija', 'rast-kristala-i-agregati'],
  ['sistematika-silikati', 'tektosilikati'],
  ['muzejska-praksa', 'cuvanje-osetljivih-minerala'],
];

const pauza = (ms) => new Promise((r) => setTimeout(r, ms));

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(employeeEmail);
  await page.getByTestId('login-password').fill(employeePassword);
  await page.getByTestId('login-submit').click();
  await expect(page).not.toHaveURL(/\/login$/);
  await pauza(3000);
}

function hvatajGreske(page) {
  const greske = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') { greske.push(`console ${msg.location().url}: ${msg.text()}`); }
  });
  page.on('pageerror', (err) => greske.push(`pageerror: ${err.message}`));
  return greske;
}

async function bezWebgl(page) {
  return page.evaluate(() => {
    const c = document.createElement('canvas');
    return !(c.getContext('webgl') || c.getContext('experimental-webgl'));
  });
}

test.describe('Уџбеник — AI илустрације v3 + slika-literatura', () => {
  test.skip(!employeeEmail || !employeePassword, 'Кустос креденцијали (CYPRESS_EMPLOYEE_*) су обавезни.');
  test.setTimeout(240_000);

  test('кустос: нове AI слике стижу и исцртавају се, slika-literatura присутна', async ({ page }) => {
    await login(page);
    const greske = hvatajGreske(page);
    let ukupnoAi = 0;
    let ukupnoSl = 0;
    const prikazSl = new Set();

    for (const [poglavlje, lekcija] of LEKCIJE) {
      const api = await page.request.get(`/api/udzbenik/minerali/lekcija/${poglavlje}/${lekcija}`);
      test.skip(api.status() === 404, 'Садржај уџбеника „minerali“ није увезен у ову базу.');
      expect(api.status(), `${poglavlje}/${lekcija}`).toBe(200);
      const blokovi = (await api.json()).lekcija.blokovi;
      const ai = blokovi.filter((b) => b.tip === 'slika' && String(b.id).startsWith('ai-'));
      const sl = blokovi.filter((b) => b.tip === 'slika-literatura');
      expect(ai.length, `${lekcija}: лекција из листе мора имати AI слике`).toBeGreaterThan(0);
      for (const b of ai) {
        expect(b.nedostupan, `${b.id}: ${b.razlog}`).toBeFalsy();
        expect(POTPISI.has(b.potpis), `${b.id}: потпис није из мапе v3: ${b.potpis}`).toBeTruthy();
      }
      for (const b of sl) {
        expect(b.nedostupan, `${b.id} треба „недоступан“ док SciSearch нема /svc/figures`).toBe(true);
        expect(typeof b.razlog).toBe('string');
        expect(b.slika).toBeUndefined();
      }
      ukupnoAi += ai.length;
      ukupnoSl += sl.length;

      await pauza(2500);
      await page.goto(`/udzbenik/minerali/${poglavlje}/${lekcija}`);
      await expect(page.locator('#udzbenik-app .udzbenik-blok').first()).toBeVisible({ timeout: 20_000 });
      await page.waitForLoadState('networkidle');
      expect(await page.locator('#udzbenik-app .udzbenik-blok').count(), `${lekcija}: сви блокови исцртани`)
        .toBe(blokovi.length);

      const figure = page.locator('.udzbenik-blok--slika');
      let aiUDomu = 0;
      for (let i = 0; i < await figure.count(); i += 1) {
        const f = figure.nth(i);
        const potpis = (await f.locator('.udzbenik-slika-potpis-tekst').first().textContent() || '').trim();
        if (!POTPISI.has(potpis)) { continue; }
        aiUDomu += 1;
        const img = f.locator('img.udzbenik-slika-element');
        await img.scrollIntoViewIfNeeded(); // loading="lazy"
        const src = await img.getAttribute('src');
        const r = await page.request.get(src);
        expect(r.status(), src).toBe(200);
        expect(r.headers()['content-type'], src).toMatch(/^image\//);
        await expect.poll(() => img.evaluate((el) => el.complete && el.naturalWidth), src).toBeGreaterThan(0);
      }
      expect(aiUDomu, `${lekcija}: AI слике у DOM-у = у API-ју`).toBe(ai.length);

      // Како мотор приказује slika-literatura: bundle 700587c не зна тај тип, па
      // блок стоји као сиви „непознат“ — лекција се ипак учита цела.
      if (sl.length) {
        prikazSl.add(`nepoznat=${await page.locator('.udzbenik-blok--nepoznat').count()} за ${sl.length} slika-literatura`);
      }
    }
    expect(ukupnoAi, `AI слика у ${LEKCIJE.length} лекција`).toBe(19);
    expect(ukupnoSl).toBeGreaterThan(0);
    test.info().annotations.push({ type: 'провера', description:
      `AI слика: ${ukupnoAi}; slika-literatura блокова: ${ukupnoSl}; приказ: ${[...prikazSl].join(' | ')}` });

    const relevantne = (await bezWebgl(page)) ? greske.filter((g) => !BEZ_WEBGL.test(g)) : greske;
    expect(relevantne).toEqual([]);
  });

  test('анонимни: нема лекције ни slika-literatura (401 / пријава)', async ({ page }) => {
    const [poglavlje, lekcija] = LEKCIJE[1];
    const api = await page.request.get(`/api/udzbenik/minerali/lekcija/${poglavlje}/${lekcija}`);
    expect(api.status()).toBe(401);
    expect(JSON.stringify(await api.json())).not.toContain('slika-literatura');
    const r = await page.request.get(`/udzbenik/minerali/${poglavlje}/${lekcija}`, { maxRedirects: 0 });
    expect(r.status()).toBe(302);
    expect(r.headers().location).toMatch(/\/login/);
  });
});
