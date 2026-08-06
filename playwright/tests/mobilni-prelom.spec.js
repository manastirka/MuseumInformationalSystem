// Мобилни прелом (телефон) — feat/mobilni.
// Доказује да се ниједна кључна страна не скролује БОЧНО на телефону (360px)
// и да велике табеле постају картице по запису. Десктоп прелом се не мења —
// то чувају постојећи десктоп тестови. Прескаче се без QA сервера/креденцијала.
const { test, expect } = require('@playwright/test');

const adminEmail = process.env.CYPRESS_ADMIN_EMAIL;
const adminPassword = process.env.CYPRESS_ADMIN_PASSWORD;

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(adminEmail);
  await page.getByTestId('login-password').fill(adminPassword);
  await page.getByTestId('login-submit').click();
  await expect(page).not.toHaveURL(/\/login$/);
}

// Права ширина документа не сме да пређе ширину прозора (нема бочног скрола).
async function nemaBocnogSkrola(page) {
  return page.evaluate(() => {
    const vw = document.documentElement.clientWidth;
    const sw = document.documentElement.scrollWidth;
    return { vw, sw, ok: sw <= vw + 1 };
  });
}

test.describe('Мобилни прелом — телефон 360×800', () => {
  test.use({ viewport: { width: 360, height: 800 }, isMobile: true, hasTouch: true });

  test.beforeEach(() => {
    test.skip(!adminEmail || !adminPassword, 'QA админ креденцијали су обавезни.');
  });

  const strane = [
    ['табла', '/dashboard'],
    ['мineraloška збирка', '/admin/mineral_collection'],
    ['инвентарска књига', '/admin/inventory_book'],
    ['фототека', '/fototeka'],
    ['радне листе', '/admin/timesheet_reports'],
    ['K-R досије', '/kr-dosije'],
    ['возила (резервације)', '/vehicle_reservations'],
  ];

  for (const [naziv, url] of strane) {
    test(`нема бочног скрола: ${naziv}`, async ({ page }) => {
      await login(page);
      await page.goto(url, { waitUntil: 'networkidle' }).catch(async () => {
        await page.goto(url, { waitUntil: 'domcontentloaded' });
      });
      await page.waitForTimeout(400);
      const r = await nemaBocnogSkrola(page);
      expect(r.ok, `${naziv}: scrollWidth=${r.sw} > clientWidth=${r.vw}`).toBeTruthy();
    });
  }

  test('пријава нема бочног скрола', async ({ page }) => {
    await page.goto('/login', { waitUntil: 'networkidle' });
    const r = await nemaBocnogSkrola(page);
    expect(r.ok, `пријава: scrollWidth=${r.sw} > clientWidth=${r.vw}`).toBeTruthy();
  });

  // Велике табеле → картице по запису на телефону; сама табела је скривена.
  const tabeleUKartice = [
    ['инвентарска књига', '/admin/inventory_book', '.desktop-tabela', '.mobil-kartice .mobil-kartica'],
    ['K-R досије', '/kr-dosije', '.desktop-tabela', '.mobil-kartice .mobil-kartica'],
    ['радне листе', '/admin/timesheet_reports', '.desktop-tabela', '.mobil-kartice .mobil-kartica'],
    ['збирка (mikologija)', '/admin/mycology_collection', '.collection-table-bottom-scroll', '#specimensMobile .mobil-kartica'],
  ];

  for (const [naziv, url, deskSel, cardSel] of tabeleUKartice) {
    test(`табела → картице: ${naziv}`, async ({ page }) => {
      await login(page);
      await page.goto(url, { waitUntil: 'networkidle' }).catch(async () => {
        await page.goto(url, { waitUntil: 'domcontentloaded' });
      });
      await page.waitForTimeout(500);
      const cards = page.locator(cardSel);
      const brojKartica = await cards.count();
      test.skip(brojKartica === 0, `нема записа у бази за ${naziv}`);
      await expect(cards.first()).toBeVisible();
      // десктоп табела је сакривена на телефону
      const deskHidden = await page.locator(deskSel).first().evaluate(
        (el) => getComputedStyle(el).display === 'none' || el.getBoundingClientRect().width === 0
      );
      expect(deskHidden, `${naziv}: десктоп табела мора бити сакривена на телефону`).toBeTruthy();
    });
  }

  test('садржај користи пуну ширину (нема левог појаса)', async ({ page }) => {
    await login(page);
    await page.goto('/kr-dosije', { waitUntil: 'networkidle' });
    const box = await page.locator('.content-wrapper').boundingBox();
    expect(box.x).toBeLessThanOrEqual(1);
    expect(box.width).toBeGreaterThan(340);
  });
});

test.describe('Десктоп остаје табела (не мења се)', () => {
  test.use({ viewport: { width: 1280, height: 900 } });

  test.beforeEach(() => {
    test.skip(!adminEmail || !adminPassword, 'QA админ креденцијали су обавезни.');
  });

  test('на десктопу се види табела, а мобилне картице су сакривене', async ({ page }) => {
    await login(page);
    await page.goto('/kr-dosije', { waitUntil: 'networkidle' });
    const table = page.locator('.desktop-tabela').first();
    await expect(table).toBeVisible();
    const cardsHidden = await page.locator('.mobil-kartice').first().evaluate(
      (el) => getComputedStyle(el).display === 'none'
    );
    expect(cardsHidden, 'мобилне картице морају бити сакривене на десктопу').toBeTruthy();
  });
});
