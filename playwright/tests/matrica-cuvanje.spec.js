// End-to-end: матрица присуства се ЧУВА и ПРИКАЗУЈЕ при поновном отварању.
// Попуни → сачувај → ПРОВЕРИ У БАЗИ да timesheet_report_days има редове са
// тачним вредностима → освежи страницу → потврди да су вредности приказане.
// (Регресија за прод буг „матрица се не чува / све нуле".)
const { test, expect } = require('@playwright/test');
const { execFileSync } = require('child_process');
const path = require('path');

const EMAIL = process.env.CYPRESS_EMPLOYEE_EMAIL;
const PASS = process.env.CYPRESS_EMPLOYEE_PASSWORD;
const DB = path.join(__dirname, 'helpers', 'matrica_db.py');
const REPO_ROOT = path.join(__dirname, '..', '..');

function db(mode) {
  return execFileSync('python', [DB, mode], { cwd: REPO_ROOT, encoding: 'utf8', env: process.env }).trim();
}

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(EMAIL);
  await page.getByTestId('login-password').fill(PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

const now = new Date();
const M = now.getMonth() + 1, Y = now.getFullYear();

test.describe('Матрица присуства — чување и приказ', () => {
  test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');

  test.beforeAll(() => db('clean'));
  test.afterAll(() => db('clean'));

  test('попуни → сачувај → у бази има редове → поново отвори → вредности приказане', async ({ page }) => {
    await login(page);
    await page.goto(`/timesheet/entry?month=${M}&year=${Y}`);
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('.ts-entry-table .timesheet-input', { timeout: 10000 });

    // Попуни дан 1 (рад 8, ван 2) и дан 2 (год. одмор 8).
    await page.locator('.ts-entry-table input[name="rad_na_mestu_1"]').fill('8');
    await page.locator('.ts-entry-table input[name="van_muzeja_1"]').fill('2');
    await page.locator('.ts-entry-table input[name="godisnji_odmor_2"]').fill('8');

    const saveResp = page.waitForResponse((r) => r.url().includes('/api/timesheet/save') && r.request().method() === 'POST');
    await page.getByTestId('timesheet-save').click();
    const body = await (await saveResp).json();
    expect(body.success).toBeTruthy();

    // ПРОВЕРА У БАЗИ: timesheet_report_days има тачне редове.
    const rows = JSON.parse(db('rows'));
    const byDay = Object.fromEntries(rows.map((r) => [r.day, r]));
    expect(byDay[1]).toBeTruthy();
    expect(byDay[1].rad).toBe(8);
    expect(byDay[1].van).toBe(2);
    expect(byDay[2].god).toBe(8);

    // ПОНОВО ОТВОРИ: вредности морају бити приказане у пољима (не нуле/празно).
    await page.goto(`/timesheet/entry?month=${M}&year=${Y}`);
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('.ts-entry-table .timesheet-input', { timeout: 10000 });
    await page.waitForTimeout(1200); // допусти да се учита из базе

    await expect(page.locator('.ts-entry-table input[name="rad_na_mestu_1"]')).toHaveValue('8');
    await expect(page.locator('.ts-entry-table input[name="van_muzeja_1"]')).toHaveValue('2');
    await expect(page.locator('.ts-entry-table input[name="godisnji_odmor_2"]')).toHaveValue('8');
  });
});
