// Контраст НОВИХ статусних површина возила (слободно/заузето/недоступно) кроз токене.
// Мери СТВАРНЕ пикселе (helpers/kontrast.js) на обе површине + текст, у свим
// режимима (светла/тамна/високи контраст) и стиловима. Тако „ново" не пролази
// испод AA, а постојећи sweep остаје независан.
const { test, expect } = require('@playwright/test');
const { postaviTemu, izmeriKontrast, SVI_REZIMI, STILOVI } = require('./helpers/kontrast');

const EMAIL = process.env.CYPRESS_ADMIN_EMAIL || process.env.QA_EMAIL;
const PASS = process.env.CYPRESS_ADMIN_PASSWORD || process.env.QA_PASSWORD;

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(EMAIL);
  await page.getByTestId('login-password').fill(PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

// Убаци мерни панел са обе статусне површине и видљивим текстом (детерминистички,
// не зависи од података/резервација). Badge пролази кроз heritage-shell, па ово
// уједно проверава да градијент не гази пастелну подлогу.
async function ubaciPanel(page) {
  await page.evaluate(() => {
    const old = document.getElementById('kontrast-status-panel');
    if (old) {old.remove();}
    const panel = document.createElement('div');
    panel.id = 'kontrast-status-panel';
    panel.style.cssText = 'padding:24px; display:flex; gap:16px; position:relative; z-index:1;';
    panel.innerHTML =
      '<span class="badge vehicle-status-free" style="font-size:16px; padding:10px 16px;">Слободно возило</span>' +
      '<span class="badge vehicle-status-busy" style="font-size:16px; padding:10px 16px;">Заузето возило</span>' +
      '<span class="badge vehicle-status-unavailable" style="font-size:16px; padding:10px 16px;">Недоступно возило</span>';
    const c = document.querySelector('.container, .container-fluid, main, body');
    c.insertBefore(panel, c.firstChild);
  });
}

for (const rezim of SVI_REZIMI) {
  for (const stil of STILOVI) {
    test(`статус возила AA (${rezim} × ${stil})`, async ({ page }) => {
      test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');
      await login(page);
      await page.goto('/vehicle_reservations');
      await page.waitForLoadState('networkidle');
      // Табела мора да се изгради (JS) и да постоји бар једна „слободно" ћелија.
      await page.waitForSelector('#calendarBody .vehicle-status-free', { timeout: 10000 });

      await ubaciPanel(page);
      await postaviTemu(page, rezim, stil);

      const padovi = await izmeriKontrast(page, '#kontrast-status-panel');
      expect(padovi, 'Испод AA на статусним површинама:\n' + JSON.stringify(padovi, null, 2)).toEqual([]);
    });
  }
}

test('табела резервација: слободно=зелена, заузето=црвена површина присутне', async ({ page }) => {
  test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');
  await login(page);
  await page.goto('/vehicle_reservations');
  await page.waitForLoadState('networkidle');
  await page.waitForSelector('#calendarBody .vehicle-status-free', { timeout: 10000 });

  // Слободне ћелије постоје и имају статусни токен као подлогу (не Bootstrap bg).
  const free = page.locator('#calendarBody .vehicle-status-free').first();
  await expect(free).toBeVisible();
  const freeBg = await free.evaluate(el => getComputedStyle(el).backgroundColor);
  // Провидна подлога значи да ћелија нема статусни токен и да се види
  // Bootstrap подлога испод — управо регресија коју овај тест хвата.
  expect(freeBg).not.toEqual('rgba(0, 0, 0, 0)');
  expect(freeBg).toMatch(/^rgb/);
  const rootFree = await page.evaluate(() =>
    getComputedStyle(document.documentElement).getPropertyValue('--status-free-bg').trim());
  expect(rootFree).not.toEqual('');           // токен дефинисан
  const rootUnavail = await page.evaluate(() =>
    getComputedStyle(document.documentElement).getPropertyValue('--status-unavail-bg').trim());
  expect(rootUnavail).not.toEqual('');        // недоступно токен дефинисан
  // Легенда носи обе површине.
  await expect(page.locator('.legend-box.vehicle-status-free')).toBeVisible();
  await expect(page.locator('.legend-box.vehicle-status-busy')).toBeVisible();
});
