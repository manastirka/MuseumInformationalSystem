// АЛАТ за систематски обилазак контраста (није gate — не трчи у обичном пролазу).
//
// Отвара стране и њихове overlay елементе (модали, dropdown-и) у задатој теми и
// стилу, мери СТВАРНИ пиксел испод сваког текста (`helpers/kontrast.js`, види
// зашто axe није довољан) и уписује налазе у JSON.
//
// Покретање (обавезан SWEEP_REZIM, иначе се прескаче):
//   SWEEP_REZIM=dark SWEEP_STIL=institucionalna SWEEP_OUT=/tmp/nalazi.json \
//     npx playwright test playwright/tests/kontrast-sweep.spec.js --workers=1
//
// Овим алатом је 2026-07-16 пописано 89 корена испод AA — списак и приоритети
// су у `docs/kontrast-sweep-2026-07-16.md`.
const { test } = require('@playwright/test');
const { postaviTemu, izmeriKontrast } = require('./helpers/kontrast');

const EMAIL = process.env.CYPRESS_ADMIN_EMAIL || process.env.QA_EMAIL;
const PASS = process.env.CYPRESS_ADMIN_PASSWORD || process.env.QA_PASSWORD;

const PODRAZUMEVANE = [
  '/fototeka', '/fototeka/prijemni-red', '/fototeka/upload', '/fototeka/uvoz',
  '/admin/mineral_collection', '/admin/manage_access', '/admin/virtual_depot',
  '/vehicle_management', '/vehicle_reservations',
  '/dokumenti', '/dokumenti/odobravanje',
  '/zahtevi/godisnji-odmor', '/zahtevi/slobodan-dan', '/zahtevi/razno',
  '/zahtev-sluzbeni-put', '/zahtevi/odobravanje',
  '/admin/timesheet_reports', '/dashboard', '/admin_panel', '/terenska-aktivnost',
].join(',');
const STRANE = (process.env.SWEEP_STRANE || PODRAZUMEVANE).split(',');

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(EMAIL);
  await page.getByTestId('login-password').fill(PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

const rezim = process.env.SWEEP_REZIM || 'dark';
const stil = process.env.SWEEP_STIL || 'institucionalna';

test(`sweep ${rezim} x ${stil}`, async ({ page }) => {
  test.skip(!process.env.SWEEP_REZIM, 'Алат — покреће се ручно уз SWEEP_REZIM.');
  test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');
  test.setTimeout(600000);
  await login(page);
  const nalazi = [];

  for (const url of STRANE) {
    let resp;
    try { resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 }); }
    catch { continue; }
    if (!resp || resp.status() !== 200) continue;
    await postaviTemu(page, rezim, stil);
    await page.waitForTimeout(200);

    // 1) osnovna strana
    for (const p of await izmeriKontrast(page)) nalazi.push({ url, gde: 'strana', ...p });

    // 2) modali preko svojih trigera
    const trigeri = await page.locator('[data-bs-toggle="modal"]').all();
    for (let i = 0; i < Math.min(trigeri.length, 6); i++) {
      try {
        const target = await trigeri[i].getAttribute('data-bs-target');
        await trigeri[i].click({ timeout: 3000 });
        await page.waitForTimeout(500);
        const sel = target && target.startsWith('#') ? target : '.modal.show';
        if (await page.locator(sel).count()) {
          for (const p of await izmeriKontrast(page, sel)) nalazi.push({ url, gde: `modal ${sel}`, ...p });
        }
        await page.keyboard.press('Escape');
        await page.waitForTimeout(250);
      } catch { /* trigger nije klikabilan */ }
    }

    // 3) dropdown-i
    const dd = await page.locator('[data-bs-toggle="dropdown"]').all();
    for (let i = 0; i < Math.min(dd.length, 8); i++) {
      try {
        await dd[i].click({ timeout: 2000 });
        await page.waitForTimeout(250);
        const meni = page.locator('.dropdown-menu.show').first();
        if (await meni.count()) {
          for (const p of await izmeriKontrast(page, '.dropdown-menu.show')) nalazi.push({ url, gde: 'dropdown', ...p });
        }
        await page.keyboard.press('Escape');
      } catch { /* preskoči */ }
    }
  }

  const fs = require('fs');
  const izlaz = process.env.SWEEP_OUT || `/tmp/sweep-${rezim}-${stil}.json`;
  fs.writeFileSync(izlaz, JSON.stringify(nalazi, null, 1));
  console.log(`NALAZI_${rezim}_${stil}: ${nalazi.length} -> ${izlaz}`);
});
