// Browser test: редизајн администраторског панела у духу OS подешавања.
//   - Брзе администраторске акције су уклоњене.
//   - Дводелни распоред: лева трака секција + десни садржај; избор мења панел.
//   - Претрага филтрира ставке; све постојеће ставке су ту; навигација ради.
//   - Респонзивно: на уском екрану нема хоризонталног скрола.
//   - Скриншотови у плавој и бордо палети (пре/после поређење).
const { test, expect } = require('@playwright/test');
const path = require('path');

const ADMIN_EMAIL = process.env.CYPRESS_ADMIN_EMAIL;
const ADMIN_PASS = process.env.CYPRESS_ADMIN_PASSWORD;
const SHOT_DIR = process.env.ADMIN_SHOT_DIR;

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(ADMIN_EMAIL);
  await page.getByTestId('login-password').fill(ADMIN_PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

async function setPalette(page, palette, mode) {
  const status = await page.evaluate(async ({ palette, mode }) => {
    const r = await fetch('/set_theme', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ palette, mode }),
    });
    return r.status;
  }, { palette, mode });
  expect(status).toBe(200);
  await page.reload();
  await page.waitForLoadState('networkidle');
}

test.describe('Админ панел — OS изглед', () => {
  test.skip(!ADMIN_EMAIL || !ADMIN_PASS, 'QA админ креденцијали су потребни.');

  test('дводелни распоред, претрага, ставке и навигација', async ({ page }) => {
    await login(page);
    await page.goto('/admin');
    await page.waitForLoadState('networkidle');

    const body = page.locator('body');

    // 1) Брзе администраторске акције уклоњене.
    await expect(body).not.toContainText('Брзе администраторске акције');

    // 2) Дводелни распоред: лева трака + 3 секције.
    await expect(page.locator('.admin-os-nav')).toBeVisible();
    await expect(page.locator('.admin-nav-item')).toHaveCount(3);

    // Подразумевано отворена секција „Корисници и приступ".
    const usersPane = page.locator('.admin-pane[data-pane="users-access"]');
    const collectionsPane = page.locator('.admin-pane[data-pane="collections-content"]');
    await expect(usersPane).toBeVisible();
    await expect(collectionsPane).toBeHidden();

    // Избор секције мења десни панел.
    await page.locator('.admin-nav-item[data-section="collections-content"]').click();
    await expect(collectionsPane).toBeVisible();
    await expect(usersPane).toBeHidden();

    // 3) Претрага филтрира ставке по називу/опису.
    const search = page.locator('.admin-os-search input');
    await search.fill('лозинки');
    await expect(page.getByText('Менаџер лозинки')).toBeVisible();
    await expect(page.getByText('Статистика збирки')).toBeHidden();
    await search.fill('');
    // По брисању, активна секција се враћа.
    await expect(page.locator('.admin-nav-item.active')).toHaveCount(1);

    // 4) Све постојеће ставке су присутне у DOM-у (ништа изгубљено).
    const labels = [
      'Управљај приступом модулима', 'Листа корисника', 'Додај корисника',
      'Менаџер лозинки', 'Статистика збирки', 'Преглед свих база',
      'QR у збиркама', 'База запослених', 'Профили запослених', 'Систем',
    ];
    for (const label of labels) {
      await expect(page.getByText(label, { exact: false }).first()).toHaveCount(1);
    }

    // 5) Навигација ради: клик на ставку води на праву страну.
    await page.locator('.admin-nav-item[data-section="collections-content"]').click();
    await page.getByRole('link', { name: /Статистика збирки/ }).click();
    await page.waitForLoadState('networkidle');
    await expect(page).not.toHaveURL(/\/admin$/);
    await expect(page.locator('body')).not.toContainText(/Internal Server Error|Not Found|Traceback/i);
  });

  test('респонзивно: уска трака без хоризонталног скрола', async ({ page }) => {
    await login(page);
    await page.setViewportSize({ width: 390, height: 800 });
    await page.goto('/admin');
    await page.waitForLoadState('networkidle');
    // Лева трака и даље видљива (постаје листа изнад садржаја).
    await expect(page.locator('.admin-os-nav')).toBeVisible();
    // Нема хоризонталног скрола документа.
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(overflow).toBeLessThanOrEqual(1);
  });

  test('скриншотови у плавој и бордо палети', async ({ page }) => {
    test.skip(!SHOT_DIR, 'Постави ADMIN_SHOT_DIR за снимке.');
    await login(page);
    for (const palette of ['plava-klasicna', 'bordo-muzejska']) {
      await page.goto('/admin');
      await setPalette(page, palette, 'light');
      await page.screenshot({ path: path.join(SHOT_DIR, `admin-${palette}.png`), fullPage: true });
    }
  });
});
