// Стража љуске уџбеника (static/js/udzbenik_straza.js + templates/udzbenik.html).
//
// Регресија 2026-11-09: мотор (ES модул) пукао на import-у старог keširanog
// chunk-а (SyntaxError) пре првог fetch-а, а читалац је гледао вечно
// „Учитавање уџбеника…“ без иједне поруке. Харнес узима ИСПОРУЧЕНИ шаблон
// (#udzbenik-app + <template id="udzbenik-straza">) и исти static/js, у правом
// Chromium-у преко file:// — да дугме „Поново учитај“ стварно поново учита.
// Unit тест не види тајмер, window 'error' од модула ни замену садржаја.

const { test, expect } = require('@playwright/test');
const fs = require('fs');
const os = require('os');
const path = require('path');

const KOREN = path.resolve(__dirname, '../..');
const SABLON = fs.readFileSync(path.join(KOREN, 'templates/udzbenik.html'), 'utf8');
const STRAZA = path.join(KOREN, 'static/js/udzbenik_straza.js');
const STRAZA_MS = 400;

function izmedju(tekst, pocetak, kraj) {
  const i = tekst.indexOf(pocetak);
  const j = tekst.indexOf(kraj, i);
  if (i < 0 || j < 0) throw new Error(`nije nadjeno: ${pocetak} … ${kraj}`);
  return tekst.slice(i, j + kraj.length);
}

// Испоручени markup љуске са разрешеним Jinja изразима и краћим тајмером.
const LJUSKA = (izmedju(SABLON, '<div id="udzbenik-app"', '</template>'))
  .replace(/\{\{[^}]*\}\}/g, '')
  .replace('data-straza-ms="8000"', `data-straza-ms="${STRAZA_MS}"`);

function fixture(motor) {
  return `<!doctype html><html lang="sr"><head><meta charset="utf-8"></head><body>
${LJUSKA}
<script src="file://${STRAZA}"></script>
<script type="module">${motor}</script>
</body></html>`;
}

let dir;
test.beforeAll(() => { dir = fs.mkdtempSync(path.join(os.tmpdir(), 'udzbenik-straza-')); });
test.afterAll(() => { fs.rmSync(dir, { recursive: true, force: true }); });

async function otvori(page, ime, motor) {
  const putanja = path.join(dir, `${ime}.html`);
  fs.writeFileSync(putanja, fixture(motor));
  const greske = [];
  page.on('console', (m) => { if (m.type() === 'error') greske.push(m.text()); });
  await page.goto(`file://${putanja}`);
  return greske;
}

test('модул пукао на import-у → порука, разлог и дугме уместо вечног „Учитавање…“', async ({ page }) => {
  const greske = await otvori(page, 'pukao',
    `throw new SyntaxError("The requested module './udzbenik-three.js' does not provide an export named 'm'");`);
  await expect(page.locator('#udzbenik-app .udzbenik-ucitavanje')).toHaveCount(0, { timeout: STRAZA_MS * 5 });
  const poruka = page.locator('#udzbenik-app .udzbenik-greska');
  await expect(poruka).toBeVisible();
  await expect(poruka).toHaveAttribute('role', 'alert');
  await expect(poruka.locator('.udzbenik-greska__naslov')).toHaveText('Уџбеник се није учитао.');
  await expect(poruka.locator('[data-razlog]')).toContainText("does not provide an export named 'm'");
  await expect(poruka.getByRole('button', { name: /Поново учитај/ })).toBeVisible();
  const straza = greske.filter((g) => g.includes('Уџбеник: мотор се није покренуо'));
  expect(straza).toHaveLength(1);
  expect(straza[0]).toContain(`${STRAZA_MS} ms`);
  expect(straza[0]).toContain("does not provide an export named 'm'");
});

test('мотор који се покрене на време — стража ћути', async ({ page }) => {
  const greske = await otvori(page, 'radi',
    `document.getElementById('udzbenik-app').replaceChildren(Object.assign(document.createElement('p'), { textContent: 'Лекција' }));`);
  await page.waitForTimeout(STRAZA_MS * 3);
  await expect(page.locator('#udzbenik-app')).toHaveText('Лекција');
  await expect(page.locator('.udzbenik-greska')).toHaveCount(0);
  expect(greske.filter((g) => g.includes('Уџбеник'))).toEqual([]);
});

test('без иједне грешке (скрипт блокиран) — порука каже да мотор није јавио грешку', async ({ page }) => {
  const greske = await otvori(page, 'tiho', '/* модул који никад не црта */');
  await expect(page.locator('#udzbenik-app .udzbenik-greska')).toBeVisible({ timeout: STRAZA_MS * 5 });
  await expect(page.locator('[data-razlog]')).toContainText('motor nije javio grešku');
  expect(greske.some((g) => g.includes('motor nije javio grešku'))).toBe(true);
});

test('„Поново учитај“ стварно поново учитава страну', async ({ page }) => {
  await otvori(page, 'dugme', 'throw new Error("пукло");');
  const dugme = page.locator('#udzbenik-app .udzbenik-greska button');
  await expect(dugme).toBeVisible({ timeout: STRAZA_MS * 5 });
  await Promise.all([page.waitForEvent('load'), dugme.click()]);
  await expect(page.locator('#udzbenik-app .udzbenik-ucitavanje')).toHaveText('Учитавање уџбеника…');
});
