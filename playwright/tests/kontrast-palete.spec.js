// Контраст равних тема (data-palette) — фаза 1 (plava-*) + фаза 2 (неутралне/
// институционалне палете, акцентна оса, ауто/тамна).
//
// Свака нова тема и СВАКА комбинација тема×режим и тема×акценат мора проћи WCAG
// AA пре него што уђе у понуду. Мери се пиксел-мерачем (`helpers/kontrast.js`)
// који чита стварну боју испод текста (хвата и градијенте/слике где axe ћути).
//
// Две групе:
//  1) Палета × режим(светло/тамно) × густина × стране — покрива структуру
//     (заглавља, табеле, беџеви, форме) у обе основе.
//  2) Акцентна оса × режим на репрезентативној равној палети — акцентовани
//     елементи (дугмад/линкови/селекције/ознаке) седе на белој/тамној РАДНОЈ
//     површини заједничкој свим равним палетама, па је њихов контраст независан
//     од палете: мери се једном, доказује све комбинације тема×акценат.
const { test, expect } = require('@playwright/test');
const {
  PALETE, GUSTINE, PALETE_REZIMI, ACCENTI,
  postaviPaletu, postaviAkcenat, izmeriKontrast,
} = require('./helpers/kontrast');

const EMAIL = process.env.CYPRESS_ADMIN_EMAIL || process.env.QA_EMAIL;
const PASS = process.env.CYPRESS_ADMIN_PASSWORD || process.env.QA_PASSWORD;

// `densities` по страни: подразумевано обе. `/vehicle_reservations` носи
// хоризонтално-скроловану табелу (`.table-responsive` календар); при снимку целе
// стране у КОМПАКТ густини распоред се хоризонтално помери па пиксел падне поред
// обојене ћелије — лажна пријава (види коментар у helpers/kontrast.js). Боје су
// независне од густине, па се та страна мери само комфорно.
const STRANE = [
  { url: '/vehicle_reservations', densities: ['komforno'] },
  { url: '/admin/timesheet_reports' },
  { url: '/vehicle_management' },
  { url: '/dashboard' },
  { url: '/terenska-aktivnost' },
  { url: '/zahtevi/godisnji-odmor' },
  { url: '/zahtevi/odobravanje' },
  { url: '/fototeka/uvoz' },
  { url: '/admin/manage_access' },
  { url: '/podesavanja/izgled' },
];

// Акцентни гејт: репрезентативна НЕУТРАЛНА палета (бела радна површина, структурни
// сиви рам) на странама богатим дугмадима/беџевима/линковима.
const ACC_PALETA = 'siva-poslovna';
const ACC_STRANE = ['/podesavanja/izgled', '/admin/timesheet_reports'];

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(EMAIL);
  await page.getByTestId('login-password').fill(PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

function opisPadova(padovi) {
  return padovi
    .map((p) => `${p.selektor} "${p.tekst}" ${p.odnos}:1 (fg=${p.fg} bg=${p.bg})`)
    .join('\n');
}

// --- 1) Палета × режим × густина × стране ---------------------------------
for (const strana of STRANE) {
  const url = strana.url;
  const gustine = strana.densities || GUSTINE;
  for (const paleta of PALETE) {
    for (const rezim of PALETE_REZIMI) {
      for (const gustina of gustine) {
        test(`контраст (${paleta} × ${rezim} × ${gustina}): ${url}`, async ({ page }) => {
          test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');
          await login(page);
          const resp = await page.goto(url, { waitUntil: 'domcontentloaded' });
          test.skip(!resp || resp.status() !== 200, `Стране ${url} нема на овом окружењу.`);
          await page.waitForLoadState('networkidle');
          await page.waitForTimeout(600);
          await postaviPaletu(page, paleta, gustina, rezim);

          const padovi = await izmeriKontrast(page);
          expect(padovi,
            `Текст испод AA (${paleta} × ${rezim} × ${gustina}) на ${url}:\n${opisPadova(padovi)}`)
            .toEqual([]);
        });
      }
    }
  }
}

// --- 2) Акцентна оса × режим (репрезентативна палета) ----------------------
for (const url of ACC_STRANE) {
  for (const rezim of PALETE_REZIMI) {
    for (const akcenat of ACCENTI) {
      test(`контраст акцента (${akcenat} × ${rezim} на ${ACC_PALETA}): ${url}`, async ({ page }) => {
        test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');
        await login(page);
        const resp = await page.goto(url, { waitUntil: 'domcontentloaded' });
        test.skip(!resp || resp.status() !== 200, `Стране ${url} нема на овом окружењу.`);
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(600);
        await postaviPaletu(page, ACC_PALETA, 'komforno', rezim);
        await postaviAkcenat(page, akcenat);

        const padovi = await izmeriKontrast(page);
        expect(padovi,
          `Текст испод AA (акценат ${akcenat} × ${rezim}) на ${url}:\n${opisPadova(padovi)}`)
          .toEqual([]);
      });
    }
  }
}
