const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;
const { execFileSync } = require('node:child_process');
const path = require('node:path');

const repoRoot = path.resolve(__dirname, '..', '..');
const resetUserScript = path.join(repoRoot, 'scripts', 'testing', 'reset_postgres_user_state.py');

function resetUserState(email, password, firstLogin = false) {
  if (!email || !password) {
    return;
  }

  execFileSync('python3', [resetUserScript], {
    cwd: repoRoot,
    env: {
      ...process.env,
      TEST_RESET_EMAIL: email,
      TEST_RESET_PASSWORD: password,
      TEST_RESET_FIRST_LOGIN: firstLogin ? '1' : '0'
    },
    stdio: 'pipe'
  });
}

async function login(page, email, password) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(email);
  await page.getByTestId('login-password').fill(password);
  await page.getByTestId('login-submit').click();
}

async function expectNoSeriousAccessibilityIssues(page, message) {
  const analysis = await new AxeBuilder({ page }).analyze();
  const seriousIssues = analysis.violations.filter(
    (violation) => violation.impact === 'serious' || violation.impact === 'critical'
  );
  expect(seriousIssues, message).toEqual([]);
}

test('employee login flow stays functional and avoids serious accessibility issues', async ({ page }) => {
  const employeeEmail = process.env.CYPRESS_EMPLOYEE_EMAIL;
  const employeePassword = process.env.CYPRESS_EMPLOYEE_PASSWORD;

  test.skip(!employeeEmail || !employeePassword, 'Employee credentials are required for Playwright login QA.');

  await page.goto('/login');
  await expectNoSeriousAccessibilityIssues(
    page,
    'Login page has serious or critical accessibility violations'
  );

  await login(page, employeeEmail, employeePassword);
  await expect(page).not.toHaveURL(/\/login$/);
  await expect(page.locator('body')).toContainText(/природњачки музеј|dashboard|табла/i);
});

test('employee timesheet entry flow renders save or locked state correctly', async ({ page }) => {
  const employeeEmail = process.env.CYPRESS_EMPLOYEE_EMAIL;
  const employeePassword = process.env.CYPRESS_EMPLOYEE_PASSWORD;

  test.skip(
    !employeeEmail || !employeePassword,
    'Employee credentials are required for Playwright timesheet QA.'
  );

  resetUserState(employeeEmail, employeePassword, false);

  await login(page, employeeEmail, employeePassword);
  await expect(page).not.toHaveURL(/\/change_password$/);

  await page.goto('/timesheet/entry');

  const saveButton = page.getByTestId('timesheet-save').first();
  await expect(saveButton).toBeVisible();

  const isDisabled = await saveButton.isDisabled();
  if (isDisabled) {
    await expect(page.locator('body')).toContainText(/закључана|ограничено време|захтев/i);
    return;
  }

  await saveButton.click();
  await expect(page.locator('body')).toContainText(/успешно|сачуван|save/i);
});

test('admin password manager page is reachable and avoids serious accessibility issues', async ({ page }) => {
  const adminEmail = process.env.CYPRESS_ADMIN_EMAIL;
  const adminPassword = process.env.CYPRESS_ADMIN_PASSWORD;

  test.skip(!adminEmail || !adminPassword, 'Admin credentials are required for Playwright admin QA.');

  await login(page, adminEmail, adminPassword);
  await expect(page).not.toHaveURL(/\/login$/);

  await page.goto('/admin/password_manager');
  await expect(page.getByTestId('user-search')).toBeVisible();
  await expect(page.getByTestId('reset-password').first()).toBeVisible();
  await expectNoSeriousAccessibilityIssues(
    page,
    'Admin password manager has serious or critical accessibility violations'
  );
});

test('archive request creation flow remains functional', async ({ page }) => {
  const archiveEmail = process.env.CYPRESS_ARCHIVE_EMAIL || process.env.CYPRESS_EMPLOYEE_EMAIL;
  const archivePassword = process.env.CYPRESS_ARCHIVE_PASSWORD || process.env.CYPRESS_EMPLOYEE_PASSWORD;

  test.skip(!archiveEmail || !archivePassword, 'Archive or employee credentials are required for archive QA.');

  resetUserState(archiveEmail, archivePassword, false);

  await login(page, archiveEmail, archivePassword);
  await page.goto('/admin/archive/zahtevi');

  await page.getByTestId('new-request').click();
  await page.getByTestId('archive-type-zahtev').selectOption({ index: 1 });
  await page.getByTestId('archive-title').fill(`Playwright QA request ${Date.now()}`);
  await page
    .getByTestId('archive-description')
    .fill('Automated Playwright archive request validation.');
  await page.getByTestId('archive-submit').click();

  await expect(page).toHaveURL(/\/admin\/archive\/zahtevi\?id=\d+/);
});
