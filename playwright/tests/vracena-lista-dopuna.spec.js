// Browser test za bug: "vraćena radna lista se ne može dopuniti".
// Scenario: admin/šef vrati radnu listu NA DOPUNU (status REJECTED sa aktivnim
// 24h prozorom, i posle isteka kalendarskog roka). Zaposleni MORA moći da:
//   1) vidi jasno označen status "Враћено на допуну" + razlog vraćanja,
//   2) izmeni matricu prisustva i opis poslova (polja i dugme NISU disabled),
//   3) ponovo pošalje listu → vraća se u tok odobravanja (status SUBMITTED).
//
// Stanje se seeduje Python helperom direktno u bazu (pre popravke ovaj isti
// seed bi renderovao stranicu sa svim poljima disabled).
const { test, expect } = require('@playwright/test');
const { execFileSync } = require('child_process');
const path = require('path');

const EMAIL = process.env.CYPRESS_EMPLOYEE_EMAIL || process.env.QA_EMAIL;
const PASS = process.env.CYPRESS_EMPLOYEE_PASSWORD || process.env.QA_PASSWORD;

const SEED = path.join(__dirname, 'helpers', 'seed_vracena_lista.py');
const REPO_ROOT = path.join(__dirname, '..', '..');

function runSeed(mode) {
  return execFileSync('python', [SEED, mode], {
    cwd: REPO_ROOT,
    encoding: 'utf8',
    env: process.env,
  }).trim();
}

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(EMAIL);
  await page.getByTestId('login-password').fill(PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

test.describe('Vraćena radna lista — dopuna', () => {
  test.skip(!EMAIL || !PASS, 'QA kredencijali su potrebni.');

  test.beforeAll(() => {
    runSeed('seed');
  });

  test.afterAll(() => {
    runSeed('clean');
  });

  test('zaposleni vidi razlog, izmeni i ponovo pošalje vraćenu listu', async ({ page }) => {
    // confirm() u submitForReview() — automatski prihvati.
    page.on('dialog', (d) => d.accept());

    await login(page);
    await page.goto('/timesheet/entry');
    await page.waitForLoadState('networkidle');

    // (3) Jasno označen status + razlog vraćanja.
    await expect(page.getByText('Враћено на допуну')).toBeVisible();
    await expect(
      page.getByText('Допуните дане 15. и 16.', { exact: false })
    ).toBeVisible();

    // Matrica prisustva se gradi JS-om — sačekaj redove.
    await page.waitForSelector('.ts-entry-table .timesheet-input', { timeout: 10000 });

    // (1+2) JEZGRO REGRESIJE: dugme "Сачувај" i polja NISU disabled.
    const saveBtn = page.getByTestId('timesheet-save');
    await expect(saveBtn).toBeVisible();
    await expect(saveBtn).toBeEnabled();

    const firstInput = page.locator('.ts-entry-table .timesheet-input').first();
    await expect(firstInput).toBeEnabled();

    // (izmeni + pošalji ponovo) Unesi sat u prvo polje i sačuvaj. Čuvanje
    // VRAĆENE liste ujedno je i ponovno podnošenje (server auto-resubmit):
    // status se u jednom kliku vraća na SUBMITTED.
    await firstInput.fill('8');
    const saveResp = page.waitForResponse(
      (r) => r.url().includes('/api/timesheet/save') && r.request().method() === 'POST'
    );
    await saveBtn.click();
    const resp = await saveResp;
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body.success).toBeTruthy();
    expect(body.auto_resubmitted).toBeTruthy();

    // Posle osvežavanja lista je nazad u toku odobravanja → SUBMITTED baner.
    await page.reload();
    await page.waitForLoadState('networkidle');
    await expect(
      page.locator('.alert-warning').filter({ hasText: 'Поднето на преглед' })
    ).toBeVisible({ timeout: 15000 });
    // Vraćena lista više NIJE u REJECTED stanju.
    await expect(page.getByText('Враћено на допуну')).toHaveCount(0);
  });
});
