// Образац „црно/тамно на тамном" — `/admin/timesheet_reports` и
// `/vehicle_reservations` у тамној теми, сва 4 стила.
//
// Три корена која овај тест чува (сваки измерен пре поправке):
//  1) Контекстуалне врсте табеле (`.table-success` и род) — Bootstrap на врсти
//     хардкодује `--bs-table-color: #000`, подлога у тамној теми постаје тамна,
//     текст остаје црн: 1.23:1.
//  2) `.text-success` — `--success` (#059669) је боја ПОЗАДИНЕ; као текст на
//     тамној ћелији даје 2.28:1. Отуда засебан токен `--success-text`.
//  3) `.dropdown-toggle-submenu` (мега-мени, overlay) — ранија поправка се
//     ослонила на светлији `--primary-dark`, али `body.heritage-shell` га враћа
//     на тамнозелену на СВАКОЈ страни: 2.61:1.
const { test, expect } = require('@playwright/test');
const { STILOVI, postaviTemu, izmeriKontrast } = require('./helpers/kontrast');

const EMAIL = process.env.CYPRESS_ADMIN_EMAIL || process.env.QA_EMAIL;
const PASS = process.env.CYPRESS_ADMIN_PASSWORD || process.env.QA_PASSWORD;

const STRANE = ['/admin/timesheet_reports', '/vehicle_reservations'];

// Познати ОТВОРЕНИ падови — намерно НИСУ покривени овим тестом.
// Сви су хардкодоване heritage површине (браон беџ/дугме/заглавље + крем текст)
// које падају и у СВЕТЛОЈ теми (мерено: badge bg-light 2.59:1, bg-warning
// 2.98:1, btn-secondary 4.48:1) — дакле нису баг тамне теме него глобални, а
// поправка мења изглед подразумеване светле теме. Види
// `docs/kontrast-sweep-2026-07-16.md`.
const OTVORENO = [
  'span.badge.bg-warning.text-dark',
  'span.badge.bg-light.text-dark',
  'span.badge.bg-secondary',
  'button.btn.btn-secondary',
  'h5.mb-0',
  'small.text-muted',
];

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(EMAIL);
  await page.getByTestId('login-password').fill(PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

for (const url of STRANE) {
  for (const stil of STILOVI) {
    test(`контраст (тамна × ${stil}): ${url}`, async ({ page }) => {
      test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');
      await login(page);
      const resp = await page.goto(url, { waitUntil: 'domcontentloaded' });
      test.skip(!resp || resp.status() !== 200, `Стране ${url} нема на овом окружењу.`);
      // Календар резервација се гради из JS-а ПОСЛЕ учитавања — без чекања
      // мерење хвата полупразну страну и тест је нестабилан.
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(600);
      await postaviTemu(page, 'dark', stil);

      const padovi = (await izmeriKontrast(page))
        .filter((p) => !OTVORENO.includes(p.selektor));
      const opis = padovi.map((p) => `${p.selektor} "${p.tekst}" ${p.odnos}:1 (fg=${p.fg} bg=${p.bg})`).join('\n');
      expect(padovi, `Текст испод AA (тамна × ${stil}) на ${url}:\n${opis}`).toEqual([]);
    });
  }
}
