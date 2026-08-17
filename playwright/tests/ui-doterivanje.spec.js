// Регресија за три доградње (fix/ui-doterivanje-2), доказане на ЖИВОЈ страници:
//  1) База изложби враћа 200 (не 500) — раније је NULL опис/број посетилаца рушио
//     шаблон (None[:150] / format(None)); овде проверавамо саму руту.
//  2) Поздравна порука на контролној табли је ВИДЉИВО мања (претходно је CSS
//     `.dashboard-header h1` (специфичност 0,2,1) газио Bootstrap `.h5`).
//  3) „Администрација" НИЈЕ у падајућем менију Базе података (изравната група),
//     али админ панел ОСТАЈЕ у главној навигацији, а базе остају као ставке.
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

test.describe('UI доградње (fix/ui-doterivanje-2)', () => {
  test.beforeEach(async ({ page }) => {
    test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');
    await login(page);
  });

  test('1) База изложби враћа 200', async ({ page }) => {
    const resp = await page.goto('/admin/exhibitions_database', { waitUntil: 'domcontentloaded' });
    expect(resp.status()).toBe(200);
  });

  test('2) поздрав на табли је видљиво мањи (< 26px)', async ({ page }) => {
    await page.goto('/dashboard', { waitUntil: 'networkidle' });
    const px = await page.evaluate(() => {
      const el = [...document.querySelectorAll('.dashboard-header h1, h1')]
        .find((e) => /Добродошли|Welcome/.test(e.textContent));
      return el ? parseFloat(getComputedStyle(el).fontSize) : null;
    });
    expect(px, 'поздрав пронађен').not.toBeNull();
    expect(px).toBeLessThan(26);
  });

  test('3) „Администрација" није у Базе података, али базе и главни нав остају', async ({ page }) => {
    await page.goto('/dashboard', { waitUntil: 'networkidle' });
    const info = await page.evaluate(() => {
      const dd = document.querySelector('ul[aria-labelledby="databasesDropdown"]');
      const adminInMenu = dd
        ? [...dd.querySelectorAll('a, span')].some((e) => /Администрација/.test(e.textContent))
        : true;
      const links = dd
        ? [...dd.querySelectorAll('a.dropdown-item')].map((a) => a.textContent.trim().replace(/\s+/g, ' '))
        : [];
      const mainNavAdmin = [...document.querySelectorAll('a.nav-link')]
        .some((a) => /Администрација/.test(a.textContent) && a.getAttribute('href') === '/admin');
      return { adminInMenu, links, mainNavAdmin };
    });
    // „Администрација" више није у падајућем менију Базе података
    expect(info.adminInMenu).toBe(false);
    // али базе које су биле под њом остају као ставке
    expect(info.links.some((t) => t.includes('База изложби'))).toBe(true);
    expect(info.links.some((t) => t.includes('Културно наслеђе'))).toBe(true);
    // а админ панел је и даље доступан из главне навигације
    expect(info.mainNavAdmin).toBe(true);
  });
});
