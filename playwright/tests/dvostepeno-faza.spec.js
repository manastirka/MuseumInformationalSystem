// Browser test: запослени види ФАЗУ двостепеног одобрења на поднетој листи —
// шеф потврдио, чека директора. (Двостепено: оба потписа обавезна.)
const { test, expect } = require('@playwright/test');
const { execFileSync } = require('child_process');
const path = require('path');

const EMAIL = process.env.CYPRESS_EMPLOYEE_EMAIL;
const PASS = process.env.CYPRESS_EMPLOYEE_PASSWORD;
const SEED = path.join(__dirname, 'helpers', 'seed_dvostepeno.py');
const REPO_ROOT = path.join(__dirname, '..', '..');

function seed(mode) {
  return execFileSync('python', [SEED, mode], { cwd: REPO_ROOT, encoding: 'utf8', env: process.env }).trim();
}

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(EMAIL);
  await page.getByTestId('login-password').fill(PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

test.describe('Двостепено одобрење — фаза (запослени)', () => {
  test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');

  test.beforeAll(() => seed('seed'));
  test.afterAll(() => seed('clean'));

  test('поднета листа приказује: шеф потврдио, чека директора', async ({ page }) => {
    await login(page);
    await page.goto('/timesheet/entry');
    await page.waitForLoadState('networkidle');

    const phase = page.getByTestId('signature-phase');
    await expect(phase).toBeVisible();
    await expect(phase).toContainText('Шеф одељења потврдио');
    await expect(phase).toContainText('Чека потпис директора');
  });
});
