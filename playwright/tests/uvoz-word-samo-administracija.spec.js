// Browser test: улаз за увоз радних листа из Word-а постоји ИСКЉУЧИВО у
// Администрацији радних листи.
//   1. Обичан запослени нигде у радним листама не види улаз ка увозу, а
//      директан URL увоза му је одбијен (серверска заштита).
//   2. Админ у прегледу/архиви радних листа НЕМА улаз ка увозу, али у
//      Администрацији улаз постоји и води на функционалну страну увоза.
const { test, expect } = require('@playwright/test');

const ADMIN_EMAIL = process.env.CYPRESS_ADMIN_EMAIL;
const ADMIN_PASS = process.env.CYPRESS_ADMIN_PASSWORD;
const EMP_EMAIL = process.env.CYPRESS_EMPLOYEE_EMAIL;
const EMP_PASS = process.env.CYPRESS_EMPLOYEE_PASSWORD;

const IMPORT_HREF = '/admin/timesheet/uvoz';

async function login(page, email, pass) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(email);
  await page.getByTestId('login-password').fill(pass);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

test.describe('Увоз из Word-а — само у Администрацији', () => {
  test('запослени: нигде у радним листама нема улаза ка увозу', async ({ page }) => {
    test.skip(!EMP_EMAIL || !EMP_PASS, 'QA креденцијали запосленог су потребни.');
    await login(page, EMP_EMAIL, EMP_PASS);

    // Преглед/унос радне листе запосленог — ниједан линк ка увозу.
    await page.goto('/timesheet');
    await page.waitForLoadState('networkidle');
    await expect(page.locator(`a[href*="${IMPORT_HREF}"]`)).toHaveCount(0);
    await expect(page.getByText('Увоз из Word', { exact: false })).toHaveCount(0);

    // Серверска заштита: директан URL увоза уз сесију запосленог →
    // одбијање (admin_required: редирект 302/303 или 403), никада 200.
    const resp = await page.request.get(IMPORT_HREF, { maxRedirects: 0 });
    expect([302, 303, 403]).toContain(resp.status());
  });

  test('админ: улаз ка увозу само у Администрацији, не у прегледу/архиви', async ({ page }) => {
    test.skip(!ADMIN_EMAIL || !ADMIN_PASS, 'QA админ креденцијали су потребни.');
    await login(page, ADMIN_EMAIL, ADMIN_PASS);

    // Текући преглед радних листа — без улаза ка увозу.
    await page.goto('/admin/timesheet_reports');
    await page.waitForLoadState('networkidle');
    await expect(page.locator(`a[href*="${IMPORT_HREF}"]`)).toHaveCount(0);

    // Архива радних листа — без улаза ка увозу.
    await page.goto('/admin/timesheet/arhiva');
    await page.waitForLoadState('networkidle');
    await expect(page.locator(`a[href*="${IMPORT_HREF}"]`)).toHaveCount(0);

    // Администрација — улаз ка увозу постоји и води на функционалну страну.
    await page.goto('/admin/timesheet');
    await page.waitForLoadState('networkidle');
    const importLink = page.locator(`a[href*="${IMPORT_HREF}"]`).first();
    await expect(importLink).toBeVisible();
    await importLink.click();
    await page.waitForLoadState('networkidle');
    // Обједињена страна увоза: оба тока (појединачни + архивски) су присутна.
    await expect(page).toHaveURL(new RegExp(IMPORT_HREF.replace(/\//g, '\\/')));
    await expect(page.locator('form[action*="/timesheet/uvoz/pregled"]')).toBeVisible();
    await expect(page.locator('form[action*="/admin/timesheet/uvoz-arhiva/pregled"]')).toBeVisible();
  });
});
