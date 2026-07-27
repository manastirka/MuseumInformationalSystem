// Browser test: раздвајање текућих и архивских радних листа у админ прегледу.
// Увезена листа из 2015 се НЕ види у текућем прегледу, али ЈЕСТЕ у архиви;
// нова листа текуће године се види у текућем прегледу. Навигација ради у оба смера.
const { test, expect } = require('@playwright/test');
const { execFileSync } = require('child_process');
const path = require('path');

const ADMIN_EMAIL = process.env.CYPRESS_ADMIN_EMAIL;
const ADMIN_PASS = process.env.CYPRESS_ADMIN_PASSWORD;
const SEED = path.join(__dirname, 'helpers', 'seed_arhiva.py');
const REPO_ROOT = path.join(__dirname, '..', '..');
const NAME = 'ЗЗ Архива Проба';
const SEARCH = 'Архива Проба';

function seed(mode) {
  return execFileSync('python', [SEED, mode], { cwd: REPO_ROOT, encoding: 'utf8', env: process.env }).trim();
}

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(ADMIN_EMAIL);
  await page.getByTestId('login-password').fill(ADMIN_PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

test.describe('Раздвајање текућих и архивских радних листа', () => {
  test.skip(!ADMIN_EMAIL || !ADMIN_PASS, 'QA админ креденцијали су потребни.');

  test.beforeAll(() => seed('seed'));
  test.afterAll(() => seed('clean'));

  test('увезена 2015 само у архиви; текућа у прегледу; навигација ради', async ({ page }) => {
    await login(page);

    // Текући преглед: тражи по имену → види се тачно 1 ред (текућа година),
    // НЕ архивска 2015.
    await page.goto(`/admin/timesheet_reports?search=${encodeURIComponent(SEARCH)}`);
    await page.waitForLoadState('networkidle');
    const currentRows = page.locator('tbody tr', { hasText: NAME });
    await expect(currentRows).toHaveCount(1);
    await expect(page.getByTestId('nav-archive')).toBeVisible();

    // Пређи у архиву преко навигације.
    await page.getByTestId('nav-archive').click();
    await page.waitForLoadState('networkidle');
    await expect(page.getByText('Архива радних листа')).toBeVisible();

    // Архива, филтер по имену → види се 2015 ред (увезена).
    await page.goto(`/admin/timesheet/arhiva?search=${encodeURIComponent(SEARCH)}&year=2015`);
    await page.waitForLoadState('networkidle');
    const archiveRows = page.locator('tbody tr', { hasText: NAME });
    await expect(archiveRows).toHaveCount(1);
    await expect(archiveRows.first()).toContainText('2015');

    // Назад у текући преглед.
    await expect(page.getByTestId('nav-current')).toBeVisible();
    await page.getByTestId('nav-current').click();
    await page.waitForLoadState('networkidle');
    await expect(page.getByText('Радне листе — текући преглед')).toBeVisible();
  });
});
