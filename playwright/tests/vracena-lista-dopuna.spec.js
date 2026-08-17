// Browser testovi za bug + dorade "vraćena radna lista se ne može dopuniti".
// Scenario: admin/šef vrati listu NA DOPUNU (status REJECTED, aktivan 24h
// prozor, posle isteka kalendarskog roka). Zaposleni MORA moći da:
//   1) vidi jasno označen status "Враћено на допуну" + razlog vraćanja,
//   2) izmeni matricu prisustva i opis poslova (polja i dugme NISU disabled),
//   3) ponovo pošalje listu → vraća se u tok odobravanja (SUBMITTED).
// Dorade:
//   A) STARIJI MESEC: vraćena lista iz starijeg meseca (ovde pre 3 meseca)
//      mora se moći otvoriti/dopuniti, ne samo prethodni mesec.
//   B) AUTO-RELOAD: čuvanje vraćene liste je auto-resubmit → strana se sama
//      osveži i REJECTED baner odmah nestane (bez ručnog reload-a).
//
// Serijski describe: oba testa dele istog QA zaposlenog i bazu, pa NE smeju
// da idu paralelno (nav baner jedne liste bi se video u drugoj).
const { test, expect } = require('@playwright/test');
const { execFileSync } = require('child_process');
const path = require('path');

const EMAIL = process.env.CYPRESS_EMPLOYEE_EMAIL || process.env.QA_EMAIL;
const PASS = process.env.CYPRESS_EMPLOYEE_PASSWORD || process.env.QA_PASSWORD;

const SEED = path.join(__dirname, 'helpers', 'seed_vracena_lista.py');
const REPO_ROOT = path.join(__dirname, '..', '..');
const MONTHS_BACK = 3;

// Isti obračun perioda kao u seed helperu (getMonth() je 0-based = month-1).
const now = new Date();
const oldIdx = now.getFullYear() * 12 + now.getMonth() - MONTHS_BACK;
const OLD_YEAR = Math.floor(oldIdx / 12);
const OLD_MONTH = (oldIdx % 12) + 1;

function runSeed(mode, monthsBack) {
  const args = [SEED, mode, ''];
  if (monthsBack !== null && monthsBack !== undefined) {
    args.push(String(monthsBack));
  }
  return execFileSync('python', args, {
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

// Razlog vraćanja unutar KONKRETNOG banera (ne bilo gde na strani) — status
// baner i navigacioni baner oba mogu da sadrže isti tekst.
function statusBanner(page) {
  return page.locator('.alert-danger').filter({ hasText: 'Враћено на допуну' });
}

test.describe.serial('Vraćena radna lista — dopuna', () => {
  test.skip(!EMAIL || !PASS, 'QA kredencijali su potrebni.');

  test.afterEach(() => {
    runSeed('clean');            // prethodni mesec
    runSeed('clean', MONTHS_BACK); // stariji mesec
  });

  test('prethodni mesec: vidi razlog, izmeni i ponovo pošalje', async ({ page }) => {
    runSeed('seed');
    page.on('dialog', (d) => d.accept());

    await login(page);
    await page.goto('/timesheet/entry');
    await page.waitForLoadState('networkidle');

    // (3) Jasno označen status + razlog vraćanja (u status baneru).
    await expect(statusBanner(page)).toBeVisible();
    await expect(statusBanner(page)).toContainText('Допуните дане 15. и 16.');

    await page.waitForSelector('.ts-entry-table .timesheet-input', { timeout: 10000 });

    // (1+2) Dugme "Сачувај" i polja NISU disabled.
    const saveBtn = page.getByTestId('timesheet-save');
    await expect(saveBtn).toBeEnabled();
    const firstInput = page.locator('.ts-entry-table .timesheet-input').first();
    await expect(firstInput).toBeEnabled();

    // (izmeni + auto-resubmit) Čuvanje vraćene liste je i ponovno podnošenje.
    await firstInput.fill('8');
    const saveResp = page.waitForResponse(
      (r) => r.url().includes('/api/timesheet/save') && r.request().method() === 'POST'
    );
    await saveBtn.click();
    const body = await (await saveResp).json();
    expect(body.success).toBeTruthy();
    expect(body.auto_resubmitted).toBeTruthy();

    // (B) Auto-reload: SUBMITTED baner se pojavi SAM, bez ručnog reloada.
    await expect(
      page.locator('.alert-warning').filter({ hasText: 'Поднето на преглед' })
    ).toBeVisible({ timeout: 15000 });
    await expect(page.getByText('Враћено на допуну')).toHaveCount(0);
  });

  test('stariji mesec: navigacija, otvaranje i dopuna vraćene liste', async ({ page }) => {
    runSeed('seed', MONTHS_BACK);
    page.on('dialog', (d) => d.accept());

    await login(page);

    // (A-1) Na podrazumevanoj strani stoji navigacija ka vraćenim listama iz
    // DRUGIH meseci, sa linkom na stari mesec.
    await page.goto('/timesheet/entry');
    await page.waitForLoadState('networkidle');
    const nav = page.getByTestId('returned-lists-nav');
    await expect(nav).toBeVisible();
    await expect(
      nav.locator(`a[href*="month=${OLD_MONTH}"][href*="year=${OLD_YEAR}"]`)
    ).toBeVisible();

    // (A-2) Otvori stari vraćeni mesec direktno → mora biti izmenjiv.
    await page.goto(`/timesheet/entry?month=${OLD_MONTH}&year=${OLD_YEAR}`);
    await page.waitForLoadState('networkidle');
    await expect(statusBanner(page)).toBeVisible();
    await expect(statusBanner(page)).toContainText('Допуните дане 15. и 16.');

    await page.waitForSelector('.ts-entry-table .timesheet-input', { timeout: 10000 });
    const saveBtn = page.getByTestId('timesheet-save');
    await expect(saveBtn).toBeEnabled();
    const firstInput = page.locator('.ts-entry-table .timesheet-input').first();
    await expect(firstInput).toBeEnabled();

    await firstInput.fill('8');
    const saveResp = page.waitForResponse(
      (r) => r.url().includes('/api/timesheet/save') && r.request().method() === 'POST'
    );
    await saveBtn.click();
    const body = await (await saveResp).json();
    expect(body.success).toBeTruthy();
    expect(body.auto_resubmitted).toBeTruthy();

    await expect(
      page.locator('.alert-warning').filter({ hasText: 'Поднето на преглед' })
    ).toBeVisible({ timeout: 15000 });
    await expect(page.getByText('Враћено на допуну')).toHaveCount(0);
  });
});
