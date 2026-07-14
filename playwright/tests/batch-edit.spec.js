// Browser test: modal za grupno uređivanje izabranih fotografija.
// Proverava ono što unit test ne vidi: da dugme broji izbor, da modal
// prikazuje ŠTA ĆE SE TAČNO DESITI pre izvršenja, da je "Примени" onemogućen
// dok nema nijedne akcije, i da rezultat prijavi izmenjeno/preskočeno.
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

test('modal za grupno uređivanje: brojač, sažetak akcija, potvrda', async ({ page }) => {
  test.skip(!EMAIL || !PASS, 'QA kredencijali su potrebni.');
  await login(page);
  await page.goto('/fototeka');

  const ima = await page.locator('.foto-item').count();
  test.skip(ima === 0, 'Nema fotografija u galeriji.');

  // izbor -> brojač na dugmetu
  await page.click('#fototekaSelectAll');
  const brojac = await page.locator('#fototekaBatchCount').textContent();
  expect(Number(brojac)).toBeGreaterThan(0);

  // modal
  await page.click('#fototekaBatchOpen');
  await expect(page.locator('#fototekaBatchBackdrop')).toBeVisible();

  // "Примени" mora biti onemogućen dok nijedna akcija nije izabrana
  await expect(page.locator('#fototekaBatchSubmit')).toBeDisabled();

  // izbor akcije -> sažetak mora reći šta se tačno dešava
  await page.check('input[name=tag_akcija][value=zameni]');
  await page.fill('#fototekaBatchTagovi', 'плејрајт-проба');
  const sazetak = page.locator('#fototekaBatchSazetak');
  await expect(sazetak).toContainText('ЗАМЕЊУЈУ');          // jasno označena akcija
  await expect(sazetak).toContainText('прескочене');        // upozorenje o preskakanju
  await expect(page.locator('#fototekaBatchSubmit')).toBeEnabled();

  await page.click('#fototekaBatchSubmit');
  await page.waitForLoadState('networkidle');
  await expect(page.locator('.alert').first()).toContainText(/Измењено|Прескочено|промене/);
});

test('modal se zatvara na Одустани i ne menja ništa', async ({ page }) => {
  test.skip(!EMAIL || !PASS, 'QA kredencijali su potrebni.');
  await login(page);
  await page.goto('/fototeka');
  test.skip((await page.locator('.foto-item').count()) === 0, 'Nema fotografija.');

  await page.click('#fototekaSelectAll');
  await page.click('#fototekaBatchOpen');
  await expect(page.locator('#fototekaBatchBackdrop')).toBeVisible();
  await page.click('#fototekaBatchCancel');
  await expect(page.locator('#fototekaBatchBackdrop')).toBeHidden();
  await expect(page.locator('.alert')).toHaveCount(0);
});
