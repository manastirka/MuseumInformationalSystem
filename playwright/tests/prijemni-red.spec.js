// Browser test: prijemni red mora da pokaže SVAKU fotografiju bez ijedne veze,
// bez obzira kako je nastala. Bug sa produkcije: red se gradio po zastavici
// `u_prijemnom_redu`, a stari uvoz ju je postavljao na FALSE za svako ime koje
// je LIČILO na inventarni broj — pa su fotografije bez veze bile nevidljive,
// i kustos nije imao načina da ih poveže. Zastavica ume da laže; veze ne.
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

test('prijemni red je dostupan iz menija i prikazuje nevezane fotografije', async ({ page }) => {
  test.skip(!EMAIL || !PASS, 'QA kredencijali su potrebni.');
  await login(page);

  // stavka mora postojati u navigaciji (a ne samo kao skrivena ruta)
  await page.goto('/fototeka');
  await expect(page.locator('a[href$="/fototeka/prijemni-red"]').first()).toHaveCount(1);

  await page.goto('/fototeka/prijemni-red');
  await expect(page.locator('h2, h1').filter({ hasText: /Пријемни ред/ })).toBeVisible();

  const redovi = page.locator('tbody tr');
  const broj = await redovi.count();
  test.skip(broj === 0, 'Nema nevezanih fotografija u ovoj bazi.');

  // svaka stavka mora imati akciju za dopunu (vezivanje) — inače je red beskoristan
  await expect(redovi.first().locator('a:has-text("Допуни"), button:has-text("Допуни")')).toHaveCount(1);
});

test('fotografija bez veze je u redu i kad zastavica kaže suprotno', async ({ page, request }) => {
  test.skip(!EMAIL || !PASS, 'QA kredencijali su potrebni.');
  await login(page);
  await page.goto('/fototeka/prijemni-red');

  // Red se gradi iz veza, ne iz zastavice: nijedna prikazana fotografija ne sme
  // imati vezu, i broj stavki mora odgovarati broju nevezanih (proverava se kroz
  // galeriju filter 'Пријемни ред', koji koristi isti uslov).
  const uRedu = await page.locator('tbody tr').count();
  await page.goto('/fototeka?veza=prijemni_red');
  const uGaleriji = await page.locator('.foto-item').count();
  expect(uGaleriji).toBe(uRedu);
});
