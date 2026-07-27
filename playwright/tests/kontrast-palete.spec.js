// Контраст 5 нових плаво-белих тема (data-palette, миграција 033, фаза 1).
//
// Свака нова тема мора проћи WCAG AA пре него што уђе у систем. Мери се исти
// скуп страна као heritage контраст гејт, али преко нове осе: 5 палета × 2
// густине (комфорно/компакт). Палета носи своју светлу основу (без data-theme),
// па се мери само density као друга димензија.
//
// Механизам мерења је пиксел-мерач (`helpers/kontrast.js`) — чита стварну боју
// испод текста, што хвата и градијенте/слике где axe ћути.
const { test, expect } = require('@playwright/test');
const { PALETE, GUSTINE, postaviPaletu, izmeriKontrast } = require('./helpers/kontrast');

const EMAIL = process.env.CYPRESS_ADMIN_EMAIL || process.env.QA_EMAIL;
const PASS = process.env.CYPRESS_ADMIN_PASSWORD || process.env.QA_PASSWORD;

// `densities` по страни: подразумевано обе. `/vehicle_reservations` носи
// хоризонтално-скроловану табелу (`.table-responsive` календар); при снимку
// целе стране у КОМПАКТ густини распоред се хоризонтално помери (исти
// `min-height:100vh` расед који мерач већ документује за lepljive елементе), па
// пиксел падне поред обојене ћелије — лажна пријава. Боје су независне од
// густине и потпуно су покривене у КОМФОРНО, где мерач ради исправно (заглавље
// календара измерено тамноплаво/бело ≈12:1). Зато ту страну мери само комфорно.
const STRANE = [
  { url: '/vehicle_reservations', densities: ['komforno'] }, // календар: види коментар
  { url: '/admin/timesheet_reports' }, // беџеви, `.text-white` заглавље
  { url: '/vehicle_management' },      // `card bg-dark text-white`
  { url: '/dashboard' },               // пригушени описи, прогноза
  { url: '/terenska-aktivnost' },      // заглавље-градијент, пригушено у табели
  { url: '/zahtevi/godisnji-odmor' },  // заглавље, `.form-text`
  { url: '/zahtevi/odobravanje' },     // табови, ланац одобравања
  { url: '/fototeka/uvoz' },           // `<code>` на заглављу
  { url: '/admin/manage_access' },     // беџеви
  { url: '/podesavanja/izgled' },      // сам бирач тема (картице, минијатуре, трака)
];

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(EMAIL);
  await page.getByTestId('login-password').fill(PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

for (const strana of STRANE) {
  const url = strana.url;
  const gustine = strana.densities || GUSTINE;
  for (const paleta of PALETE) {
    for (const gustina of gustine) {
      test(`контраст (${paleta} × ${gustina}): ${url}`, async ({ page }) => {
        test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');
        await login(page);
        const resp = await page.goto(url, { waitUntil: 'domcontentloaded' });
        test.skip(!resp || resp.status() !== 200, `Стране ${url} нема на овом окружењу.`);
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(600);
        await postaviPaletu(page, paleta, gustina);

        const padovi = await izmeriKontrast(page);
        const opis = padovi
          .map((p) => `${p.selektor} "${p.tekst}" ${p.odnos}:1 (fg=${p.fg} bg=${p.bg})`)
          .join('\n');
        expect(padovi, `Текст испод AA (${paleta} × ${gustina}) на ${url}:\n${opis}`).toEqual([]);
      });
    }
  }
}
