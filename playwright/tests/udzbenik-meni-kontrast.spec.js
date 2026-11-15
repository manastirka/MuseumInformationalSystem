const { test, expect } = require('@playwright/test');
const { PALETE, PALETE_REZIMI, postaviPaletu, izmeriKontrast } = require('./helpers/kontrast');

// Бочни списак поглавља уџбеника као падајући мени (мотор, 15.11.2026): дугмад
// поглавља, стрелице и лекције отвореног поглавља морају проћи WCAG AA у СВИМ
// равним палетама × светло/тамно. Мери се пиксел-мерачем на 390 px (отворен
// мобилни мени — навигација није лепљива, па се снимак и координате поклапају).
// Прескаче се без креденцијала кустоса (CYPRESS_EMPLOYEE_*).

test.use({ ignoreHTTPSErrors: true });

const EMAIL = process.env.CYPRESS_EMPLOYEE_EMAIL;
const PASS = process.env.CYPRESS_EMPLOYEE_PASSWORD;
const LEKCIJA = '/udzbenik/minerali/kristalohemija/polimorfizam-i-politipizam';

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(EMAIL);
  await page.getByTestId('login-password').fill(PASS);
  await page.getByTestId('login-submit').click();
  await expect(page).not.toHaveURL(/\/login$/);
}

function opisPadova(padovi) {
  return padovi
    .map((p) => `${p.selektor} "${p.tekst}" ${p.odnos}:1 (fg=${p.fg} bg=${p.bg})`)
    .join('\n');
}

for (const paleta of PALETE) {
  for (const rezim of PALETE_REZIMI) {
    test(`мени поглавља уџбеника — контраст (${paleta} × ${rezim})`, async ({ page }) => {
      test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');
      await page.setViewportSize({ width: 390, height: 844 });
      await login(page);
      const resp = await page.goto(LEKCIJA, { waitUntil: 'domcontentloaded' });
      test.skip(!resp || resp.status() !== 200, 'Уџбеника нема на овом окружењу.');
      await expect(page.locator('h2#udzbenik-lekcija-naslov')).toBeVisible({ timeout: 20_000 });
      await postaviPaletu(page, paleta, 'komforno', rezim);

      await page.locator('.udzbenik-mobilni-meni-dugme').click();
      const dugmad = page.locator('.udzbenik-nav-poglavlje-dugme');
      await expect(dugmad.first()).toBeVisible();
      // Отворено текуће поглавље + још једно (лекције, истакнута текућа, затворена дугмад)
      const zatvoreno = page.locator('.udzbenik-nav-poglavlje-dugme[aria-expanded="false"]').first();
      await zatvoreno.click();
      await page.mouse.move(0, 0);
      await page.waitForTimeout(300);

      const padovi = await izmeriKontrast(page, '.udzbenik-nav');
      expect(padovi,
        `Текст менија поглавља испод AA (${paleta} × ${rezim}):\n${opisPadova(padovi)}`).toEqual([]);
    });
  }
}
