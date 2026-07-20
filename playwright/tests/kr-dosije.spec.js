const { test, expect } = require('@playwright/test');

// E2E за модул „Конзерваторско-рестаураторски досије" (K-R досије).
// Тестови се прескачу ако нема креденцијала/сервера — исти образац као
// production-readiness.spec.js. Захтева покренут QA сервер на baseURL.

async function login(page, email, password) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(email);
  await page.getByTestId('login-password').fill(password);
  await page.getByTestId('login-submit').click();
  await expect(page).not.toHaveURL(/\/login$/);
}

const adminEmail = process.env.CYPRESS_ADMIN_EMAIL;
const adminPassword = process.env.CYPRESS_ADMIN_PASSWORD;
const employeeEmail = process.env.CYPRESS_EMPLOYEE_EMAIL;
const employeePassword = process.env.CYPRESS_EMPLOYEE_PASSWORD;

test.describe('К-Р досије', () => {
  test('админ отвара листу, креира досије и преузима PDF', async ({ page }) => {
    test.skip(!adminEmail || !adminPassword,
      'Админ креденцијали су обавезни за K-R досије QA.');

    await login(page, adminEmail, adminPassword);

    // Листа се отвара.
    await page.goto('/kr-dosije');
    await expect(page).toHaveURL(/\/kr-dosije$/);
    await expect(page.locator('body')).toContainText(/досије/i);

    // Форма за нови досије.
    await page.goto('/kr-dosije/novi');
    const naziv = `QA досије ${Date.now()}`;
    await page.fill('[name="naziv_predmeta"]', naziv);
    // Одељење се приказује само админу/директору.
    const odeljenje = page.locator('select[name="odeljenje"]');
    if (await odeljenje.count()) {
      await odeljenje.selectOption('geo');
    }
    await page.fill('[name="opis_pre"]', 'Стање пре (QA).');
    await page.fill('[name="opis_postupak"]', 'Поступак (QA).');
    await page.fill('[name="opis_posle"]', 'Стање после (QA).');
    // Пошаљи баш форму досијеа (не неку навигациону форму на страници).
    await page.locator('form:has([name="naziv_predmeta"])')
      .evaluate((f) => f.requestSubmit());

    // После снимања видимо детаљ са називом.
    await expect(page.locator('body')).toContainText(naziv);
    await expect(page).toHaveURL(/\/kr-dosije\/\d+/);

    // Евиденциони број у формату КР-ГЕО-YYYY-NNN.
    await expect(page.locator('body')).toContainText(/КР-ГЕО-\d{4}-\d{3}/);

    // PDF је доступан и има application/pdf тип.
    const dosijeUrl = page.url();
    const idMatch = dosijeUrl.match(/\/kr-dosije\/(\d+)/);
    expect(idMatch).not.toBeNull();
    const pdfResp = await page.request.get(`/kr-dosije/${idMatch[1]}/pdf`);
    expect(pdfResp.status()).toBe(200);
    expect(pdfResp.headers()['content-type']).toContain('application/pdf');

    // Чишћење: обриши креирани досије.
    await page.goto(dosijeUrl);
    const del = page.locator('form[action*="/brisanje"] button, form[action*="/brisanje"] [type="submit"]');
    if (await del.count()) {
      page.once('dialog', (d) => d.accept());
      await del.first().click();
    }
  });

  test('предлошци: админ додаје предложак поступка', async ({ page }) => {
    test.skip(!adminEmail || !adminPassword,
      'Админ креденцијали су обавезни за K-R досије QA.');

    await login(page, adminEmail, adminPassword);
    await page.goto('/kr-dosije/predlosci');
    await expect(page.locator('body')).toContainText(/предлож/i);

    const naziv = `QA предложак ${Date.now()}`;
    await page.selectOption('form[action*="/predlosci/novi"] select[name="vrsta"]', 'postupak');
    await page.fill('form[action*="/predlosci/novi"] [name="naziv"]', naziv);
    await page.fill('form[action*="/predlosci/novi"] [name="sadrzaj"]', 'Садржај предлошка (QA).');
    await page.locator('form[action*="/predlosci/novi"]').evaluate((f) => f.requestSubmit());
    // Постојећи предлошци се приказују као уредиве форме — назив је вредност инпута.
    await expect(page.locator(`input[name="naziv"][value="${naziv}"]`).first()).toBeVisible();
    // (Чишћење QA предлошка иде преко базе после теста — да не бришемо туђе редове.)
  });

  test('запослени без права не приступа K-R досијеу', async ({ page }) => {
    test.skip(!employeeEmail || !employeePassword,
      'Креденцијали запосленог су обавезни за проверу права.');

    await login(page, employeeEmail, employeePassword);
    const resp = await page.request.get('/kr-dosije', { maxRedirects: 0 });
    // module_access_required одбија: 403 или редирект (не 200 са листом).
    expect([302, 303, 403]).toContain(resp.status());
  });
});
