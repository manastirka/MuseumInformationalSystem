// Browser test: админ откључавање уноса радне листе по кориснику.
// Админ отвара страницу, бира запосленог и стари месец, откључава — види успех.
// (Замена за уклоњени механизам „захтева за унос".)
const { test, expect } = require('@playwright/test');
const { execFileSync } = require('child_process');
const path = require('path');

const ADMIN_EMAIL = process.env.CYPRESS_ADMIN_EMAIL;
const ADMIN_PASS = process.env.CYPRESS_ADMIN_PASSWORD;
const EMP_EMAIL = process.env.CYPRESS_EMPLOYEE_EMAIL;

const SEED = path.join(__dirname, 'helpers', 'seed_vracena_lista.py');
const REPO_ROOT = path.join(__dirname, '..', '..');
const MONTHS_BACK = 6;

const now = new Date();
const idx = now.getFullYear() * 12 + now.getMonth() - MONTHS_BACK;
const OLD_YEAR = Math.floor(idx / 12);
const OLD_MONTH = (idx % 12) + 1;

async function login(page, email, pass) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(email);
  await page.getByTestId('login-password').fill(pass);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

test.describe('Админ откључавање уноса', () => {
  test.skip(!ADMIN_EMAIL || !ADMIN_PASS || !EMP_EMAIL, 'QA админ/запослени креденцијали су потребни.');

  test.afterEach(() => {
    // Обриши откључани извештај (који је unlock креирао као DRAFT).
    execFileSync('python', [SEED, 'clean', '', String(MONTHS_BACK)],
      { cwd: REPO_ROOT, encoding: 'utf8', env: process.env });
  });

  test('админ откључава стари месец изабраном запосленом', async ({ page }) => {
    await login(page, ADMIN_EMAIL, ADMIN_PASS);
    await page.goto('/admin/timesheet/otkljucaj-unos');
    await page.waitForLoadState('networkidle');

    await page.getByTestId('unlock-employee').selectOption(EMP_EMAIL);
    await page.getByTestId('unlock-from-month').selectOption(String(OLD_MONTH));
    await page.getByTestId('unlock-from-year').selectOption(String(OLD_YEAR));

    await page.getByTestId('unlock-submit').click();

    const result = page.getByTestId('unlock-result');
    await expect(result.locator('.alert-success')).toBeVisible({ timeout: 15000 });
    await expect(result).toContainText('Откључан унос');
  });
});
