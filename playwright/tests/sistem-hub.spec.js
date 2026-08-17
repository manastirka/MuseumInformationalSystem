const { test, expect } = require('@playwright/test');
const { postaviTemu, izmeriKontrast } = require('./helpers/kontrast');

const ADMIN_EMAIL = process.env.CYPRESS_ADMIN_EMAIL;
const ADMIN_PASSWORD = process.env.CYPRESS_ADMIN_PASSWORD;
const EMP_EMAIL = process.env.CYPRESS_EMPLOYEE_EMAIL;
const EMP_PASSWORD = process.env.CYPRESS_EMPLOYEE_PASSWORD;
const SHOT = process.env.SISTEM_SHOT_PATH;

async function login(page, email, password) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(email);
  await page.getByTestId('login-password').fill(password);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

// Collect JS reference errors from page + subframes.
function attachErrorSink(page) {
  const errors = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      const t = msg.text();
      if (/is not defined|ReferenceError|is not a function/i.test(t)) {errors.push(t);}
    }
  });
  page.on('pageerror', (err) => errors.push(String(err)));
  return errors;
}

test('hub: сви табови се отварају, чиста конзола, снимак', async ({ page }) => {
  test.skip(!ADMIN_EMAIL || !ADMIN_PASSWORD, 'Admin creds required.');
  const errors = attachErrorSink(page);

  await login(page, ADMIN_EMAIL, ADMIN_PASSWORD);
  await page.goto('/admin/sistem');
  await page.waitForLoadState('networkidle');

  // Tab buttons present
  for (const id of ['tab-podesavanja', 'tab-posta', 'tab-izvestaji', 'tab-revizija']) {
    await expect(page.locator('#' + id)).toBeVisible();
  }

  // First tab (settings) iframe content loads
  const settings = page.frameLocator('iframe[title="Подешавања"]');
  await expect(settings.locator('#generalSettingsForm')).toBeVisible({ timeout: 15000 });

  // Click each remaining tab → its iframe content loads
  await page.locator('#tab-posta').click();
  await expect(page.frameLocator('iframe[title="Пошта"]').locator('body')).toContainText(/пошт|mail|SMTP|сервер/i, { timeout: 15000 });

  await page.locator('#tab-izvestaji').click();
  await expect(page.frameLocator('iframe[title="Извештаји"]').locator('body')).toContainText(/извештај|статист|запослен/i, { timeout: 15000 });

  await page.locator('#tab-revizija').click();
  await expect(page.frameLocator('iframe[title="Ревизиони траг"]').locator('body')).toContainText(/ревизион|акција|ентитет/i, { timeout: 15000 });

  if (SHOT) {
    await page.locator('#tab-podesavanja').click();
    await page.waitForTimeout(800);
    await page.screenshot({ path: SHOT, fullPage: true });
  }

  expect(errors, 'Console/page reference errors:\n' + errors.join('\n')).toEqual([]);
});

test('hub: подешавања таб чува измене (round-trip)', async ({ page }) => {
  test.skip(!ADMIN_EMAIL || !ADMIN_PASSWORD, 'Admin creds required.');
  await login(page, ADMIN_EMAIL, ADMIN_PASSWORD);
  await page.goto('/admin/sistem');
  await page.waitForLoadState('networkidle');

  const settings = page.frameLocator('iframe[title="Подешавања"]');
  await expect(settings.locator('#generalSettingsForm')).toBeVisible({ timeout: 15000 });

  // Submit the general settings form with its current values → expect a 200 save.
  const [resp] = await Promise.all([
    page.waitForResponse((r) => r.url().includes('/api/admin/settings/general') && r.request().method() === 'POST', { timeout: 15000 }),
    settings.locator('#generalSettingsForm button[type="submit"]').click(),
  ]);
  expect(resp.status()).toBe(200);
});

test('hub: старе руте редиректују на таб', async ({ page }) => {
  test.skip(!ADMIN_EMAIL || !ADMIN_PASSWORD, 'Admin creds required.');
  await login(page, ADMIN_EMAIL, ADMIN_PASSWORD);

  const map = {
    '/admin/system-settings': 'podesavanja',
    '/admin/mail-settings': 'posta',
    '/admin/reports': 'izvestaji',
    '/admin/audit-log': 'revizija',
  };
  for (const [oldPath, tab] of Object.entries(map)) {
    await page.goto(oldPath);
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL(new RegExp('/admin/sistem#' + tab + '$'));
  }
});

test('hub: контраст траке табова (AA) у свим режимима', async ({ page }) => {
  test.skip(!ADMIN_EMAIL || !ADMIN_PASSWORD, 'Admin creds required.');
  await login(page, ADMIN_EMAIL, ADMIN_PASSWORD);
  await page.goto('/admin/sistem');
  await page.waitForLoadState('networkidle');
  for (const rezim of ['light', 'dark', 'contrast']) {
    await postaviTemu(page, rezim, 'institucionalna');
    const padovi = await izmeriKontrast(page, '.sistem-header, .sistem-tabs');
    expect(padovi, `Испод AA (${rezim}):\n` + JSON.stringify(padovi, null, 2)).toEqual([]);
  }
});

test('hub: запослени нема приступ (права непромењена)', async ({ page }) => {
  test.skip(!EMP_EMAIL || !EMP_PASSWORD, 'Employee creds required.');
  await login(page, EMP_EMAIL, EMP_PASSWORD);
  await page.goto('/admin/sistem');
  await page.waitForLoadState('networkidle');
  // Page route → redirected away from the hub (existing convention: dashboard).
  await expect(page).not.toHaveURL(/\/admin\/sistem/);
  await expect(page.locator('body')).not.toContainText('tab-podesavanja');
});
