// Browser test: dvostubačni raspored forme za unos radne liste.
// Na širokim ekranima (≥1200px) matrica prisustva stoji LEVO, a obavljeni
// poslovi DESNO (side-by-side, bez horizontalnog skrola). Ispod ~1200px se
// stupci slažu vertikalno (kao ranije). Testira SAMO raspored — polja i logika
// se ne diraju.
const { test, expect } = require('@playwright/test');

const EMAIL = process.env.CYPRESS_EMPLOYEE_EMAIL || process.env.CYPRESS_ADMIN_EMAIL || process.env.QA_EMAIL;
const PASS = process.env.CYPRESS_EMPLOYEE_PASSWORD || process.env.CYPRESS_ADMIN_PASSWORD || process.env.QA_PASSWORD;

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(EMAIL);
  await page.getByTestId('login-password').fill(PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

test('desktop: matrica levo + poslovi desno; usko: slaganje', async ({ page }) => {
  test.skip(!EMAIL || !PASS, 'QA kredencijali su potrebni.');
  await login(page);

  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/timesheet/entry');
  // Matrica se gradi JS-om — sačekaj redove.
  await page.waitForSelector('.ts-entry-table tbody tr.working-day, .ts-entry-table tbody tr', { timeout: 10000 });
  await page.waitForTimeout(400);

  const matrix = page.locator('.ts-matrix-row');
  const work = page.locator('.ts-work-row');
  await expect(matrix).toBeVisible();
  await expect(work).toBeVisible();

  const m = await matrix.boundingBox();
  const w = await work.boundingBox();
  const vw = page.viewportSize().width;

  // Dva stupca: poslovi su desno od matrice, na približno istoj visini.
  expect(w.x).toBeGreaterThan(m.x + m.width * 0.5);
  expect(Math.abs(w.y - m.y)).toBeLessThan(200);

  // Oba stupca unutar viewporta — nema horizontalnog skrola OD stubova.
  expect(m.x + m.width).toBeLessThanOrEqual(vw + 1);
  expect(w.x + w.width).toBeLessThanOrEqual(vw + 1);

  // Sva polja ostaju prisutna (raspored ne uklanja ni jedno polje): matrica ima
  // 8 kategorija po danu, a desni stub sve tekstualne kategorije. (can_edit
  // zavisi od roka za unos — ovde ne diramo edit, samo prisustvo/vidljivost.)
  await expect(page.locator('.ts-entry-table .timesheet-input').first()).toBeVisible();
  expect(await page.locator('.work-category').count()).toBeGreaterThan(10);
  await expect(work.locator('.work-category').first()).toBeVisible();

  // Usko (<1200px): stupci se slažu — poslovi ispod matrice, ista leva ivica.
  await page.setViewportSize({ width: 900, height: 1000 });
  await page.waitForTimeout(400);
  const m2 = await matrix.boundingBox();
  const w2 = await work.boundingBox();
  expect(w2.y).toBeGreaterThan(m2.y + m2.height - 60);
  expect(Math.abs(w2.x - m2.x)).toBeLessThan(60);
});
