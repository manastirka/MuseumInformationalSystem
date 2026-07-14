// Browser test: hover uvećanje i fotografija u kartici predmeta.
// Ova dva buga su PROŠLA unit testove a pala u praksi (overlay sečen
// overflow-om, kartica čitala samo staru putanju) — zato se proveravaju u
// pravom browseru, na stvarnoj strani.
const { test, expect } = require('@playwright/test');

const EMAIL = process.env.CYPRESS_ADMIN_EMAIL || process.env.QA_EMAIL;
const PASS = process.env.CYPRESS_ADMIN_PASSWORD || process.env.QA_PASSWORD;

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(EMAIL);
  await page.getByTestId('login-password').fill(PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

test('hover na sličicu prikazuje uvećanje iznad tabele, unutar ekrana', async ({ page }) => {
  test.skip(!EMAIL || !PASS, 'QA kredencijali su potrebni.');
  await login(page);
  await page.goto('/admin/mineral_collection');

  const thumb = page.locator('img.img-thumbnail[data-preview]').first();
  const ima = await thumb.count();
  test.skip(ima === 0, 'Nijedan predmet nema fotografiju u ovoj bazi.');

  await thumb.hover();
  const overlay = page.locator('#mineralThumbPreview');
  await expect(overlay).toBeVisible();

  const stanje = await overlay.evaluate((el) => {
    const r = el.getBoundingClientRect();
    return {
      uBody: el.parentElement === document.body,           // ne sme biti u tabeli (overflow:hidden)
      unutarViewporta: r.left >= 0 && r.top >= 0 &&
        r.right <= window.innerWidth && r.bottom <= window.innerHeight,
      slikaUcitana: el.querySelector('img').naturalWidth,
    };
  });
  expect(stanje.uBody).toBe(true);
  expect(stanje.unutarViewporta).toBe(true);
  expect(stanje.slikaUcitana).toBeGreaterThan(100);
});

test('hover preživljava presl​ovljavanje (MutationObserver ne skida slušaoce)', async ({ page }) => {
  test.skip(!EMAIL || !PASS, 'QA kredencijali su potrebni.');
  await login(page);
  await page.goto('/admin/mineral_collection');
  const thumb = page.locator('img.img-thumbnail[data-preview]').first();
  test.skip((await thumb.count()) === 0, 'Nema fotografija.');

  await page.click('#langSwitcherBtn');
  await page.click('.lang-option[data-lang="sr-Latn"]');
  await page.waitForTimeout(1200);

  await thumb.hover();
  await expect(page.locator('#mineralThumbPreview')).toBeVisible();
});

test('kartica predmeta prikazuje fotografiju iz Фототеke, ne placeholder', async ({ page }) => {
  test.skip(!EMAIL || !PASS, 'QA kredencijali su potrebni.');
  await login(page);
  await page.goto('/admin/mineral_collection');

  const red = page.locator('tbody tr').filter({ has: page.locator('img[src*="/fototeka/media/"]') }).first();
  test.skip((await red.count()) === 0, 'Nijedan predmet nema fototeka fotografiju.');

  const href = await red.locator('a[href*="/admin/mineral_detail/"]').first().getAttribute('href');
  await page.goto(href);

  const slika = page.locator('img.img-fluid.rounded.shadow').first();
  const src = await slika.getAttribute('src');
  expect(src).toContain('/fototeka/media/');           // ne stara putanja
  expect(await slika.evaluate((el) => el.naturalWidth)).toBeGreaterThan(100);  // ne placeholder
});
