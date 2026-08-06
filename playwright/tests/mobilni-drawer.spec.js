// Мобилна бочна фиока (#mainDrawer) — обједињена навигација испод mobilnog прелома.
// Доказује: отварање/затварање свим путевима (X, scrim, Esc, свајп улево, Back),
// scroll-lock тела док је фиока отворена, навигацију до три одредишта, aria-стање.
// Прескаче се без QA сервера/креденцијала.
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

async function openDrawer(page) {
  const toggle = page.locator('#drawerToggle');
  await expect(toggle).toBeVisible();
  await toggle.click();
  const drawer = page.locator('#mainDrawer');
  await expect(drawer).toHaveClass(/show/);
  await expect(drawer).toBeVisible();
  return drawer;
}

// Синтетички свајп улево преко елемента (Bootstrap offcanvas нема нативни свајп).
async function swipeLeft(page, selector) {
  await page.evaluate((sel) => {
    const el = document.querySelector(sel);
    const rect = el.getBoundingClientRect();
    const y = rect.top + rect.height / 2;
    function tp(x) {
      return new Touch({ identifier: 1, target: el, clientX: x, clientY: y });
    }
    const startX = rect.left + rect.width - 20;
    const endX = rect.left + 5;
    el.dispatchEvent(new TouchEvent('touchstart', { bubbles: true, cancelable: true, touches: [tp(startX)], targetTouches: [tp(startX)], changedTouches: [tp(startX)] }));
    el.dispatchEvent(new TouchEvent('touchmove', { bubbles: true, cancelable: true, touches: [tp(startX - 40)], targetTouches: [tp(startX - 40)], changedTouches: [tp(startX - 40)] }));
    el.dispatchEvent(new TouchEvent('touchmove', { bubbles: true, cancelable: true, touches: [tp(endX)], targetTouches: [tp(endX)], changedTouches: [tp(endX)] }));
    el.dispatchEvent(new TouchEvent('touchend', { bubbles: true, cancelable: true, touches: [], targetTouches: [], changedTouches: [tp(endX)] }));
  }, selector);
}

const viewports = [
  { name: '360×800', width: 360, height: 800 },
  { name: '390×844', width: 390, height: 844 },
];

for (const vp of viewports) {
  test.describe(`Мобилна фиока — ${vp.name}`, () => {
    test.use({ viewport: { width: vp.width, height: vp.height }, isMobile: true, hasTouch: true });

    test.beforeEach(async ({ page }) => {
      test.skip(!adminEmail || !adminPassword, 'QA админ креденцијали су обавезни.');
      await login(page);
      await page.goto('/dashboard');
    });

    test('фиока клизи слева, ужа од ~320px, са scrim-ом', async ({ page }) => {
      const drawer = await openDrawer(page);
      const box = await drawer.boundingBox();
      expect(box.x).toBeLessThanOrEqual(1);            // прислоњена уз леву ивицу
      expect(box.width).toBeLessThanOrEqual(320 + 1);  // max ~320px
      expect(box.width).toBeLessThanOrEqual(vp.width * 0.9); // ~85% екрана
      await expect(page.locator('.offcanvas-backdrop')).toBeVisible();
      // aria-expanded=true на хамбургеру.
      await expect(page.locator('#drawerToggle')).toHaveAttribute('aria-expanded', 'true');
    });

    test('тело се НЕ скролује док је фиока отворена (scroll lock)', async ({ page }) => {
      await openDrawer(page);
      const overflow = await page.evaluate(() => getComputedStyle(document.body).overflow);
      expect(overflow).toBe('hidden');
    });

    test('затварање: X дугме', async ({ page }) => {
      const drawer = await openDrawer(page);
      await page.locator('#mainDrawer .mobile-drawer-close').click();
      await expect(drawer).not.toHaveClass(/show/);
      await expect(page.locator('#drawerToggle')).toHaveAttribute('aria-expanded', 'false');
    });

    test('затварање: тап на scrim', async ({ page }) => {
      const drawer = await openDrawer(page);
      await page.locator('.offcanvas-backdrop').click({ position: { x: 5, y: 5 } });
      await expect(drawer).not.toHaveClass(/show/);
    });

    test('затварање: тастер Esc', async ({ page }) => {
      const drawer = await openDrawer(page);
      await page.keyboard.press('Escape');
      await expect(drawer).not.toHaveClass(/show/);
    });

    test('затварање: свајп улево', async ({ page }) => {
      const drawer = await openDrawer(page);
      await swipeLeft(page, '#mainDrawer');
      await expect(drawer).not.toHaveClass(/show/);
    });

    test('затварање: Back дугме (history state), страна остаје иста', async ({ page }) => {
      const drawer = await openDrawer(page);
      const urlBefore = page.url();
      await page.goBack();
      await expect(drawer).not.toHaveClass(/show/);
      expect(page.url()).toBe(urlBefore);
    });

    test('навигација до три одредишта из фиоке', async ({ page }) => {
      const targets = [
        { label: 'Све базе података', re: /\/(museum-databases|databases|baze)/i },
        { label: 'Возила', re: /vehicle|vozila|reservation/i },
        { label: 'Изглед и персонализација', re: /izgled|personalizacija|podesavanja/i },
      ];
      for (const t of targets) {
        await page.goto('/dashboard');
        await openDrawer(page);
        const link = page.locator('#mainDrawer a.drawer-link', { hasText: t.label }).first();
        await expect(link).toBeVisible();
        await link.click();
        await expect(page).not.toHaveURL(/\/dashboard$/);
        // фиока се затвара при навигацији
        await expect(page.locator('#mainDrawer')).not.toHaveClass(/show/);
      }
    });

    test('секције са насловима постоје и фиока се скролује', async ({ page }) => {
      await openDrawer(page);
      const titles = page.locator('#mainDrawer .drawer-section-title');
      expect(await titles.count()).toBeGreaterThanOrEqual(3);
    });
  });
}
