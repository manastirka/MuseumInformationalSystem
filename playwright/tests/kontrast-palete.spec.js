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
  { url: '/admin' },
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

// --- 3) ЗАГЛАВЉА ВЕЛИКИХ ТАБЕЛА × палета × режим --------------------------
// Заглавље табеле у палети иде на структурну (тамноплаву/сиву/…) површину, па
// сав ТЕКСТ у ћелији заглавља — укључујући сортабилне линкове (`.text-dark`) и
// иконе стрелица — мора бити читљив (бела на тамноплавом). Продукцијски баг:
// зглавље минералне збирке остало таман текст на тамноплавом (1.26:1).
// Мери се само `thead`; `tbody` се сакрије јер веома високе табеле руше
// fullPage декодовање снимка (није баг производа, него ограничење мерача).
const TABELE_STRANE = [
  '/admin/mineral_collection', // пријављени баг: сортабилни .text-dark линкови
  '/admin/inventory_book',
  '/admin/library_database',
  '/admin/employees_database',
  '/admin/visitors_database',
  '/kr-dosije',
  '/fototeka',
];
for (const url of TABELE_STRANE) {
  for (const paleta of PALETE) {
    for (const rezim of PALETE_REZIMI) {
      test(`контраст заглавља табеле (${paleta} × ${rezim}): ${url}`, async ({ page }) => {
        test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');
        await login(page);
        const resp = await page.goto(url, { waitUntil: 'domcontentloaded' });
        test.skip(!resp || resp.status() !== 200, `Стране ${url} нема на овом окружењу.`);
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(600);
        await postaviPaletu(page, paleta, 'komforno', rezim);
        await page.addStyleTag({ content: '.table tbody, table tbody { display: none !important; }' });
        await page.waitForTimeout(150);

        const padovi = await izmeriKontrast(page, 'thead');
        expect(padovi,
          `Заглавље табеле испод AA (${paleta} × ${rezim}) на ${url}:\n${opisPadova(padovi)}`)
          .toEqual([]);
      });
    }
  }
}

// --- 4) ЗАГЛАВЉА БАЗА/ЗБИРКИ (.db-hero) × палета × режим -------------------
// Свака база носи хардкодован банер (Bootstrap bg-info/success/warning/dark,
// инлајн градијент код изложби, локални зелени градијент код минерала). Кроз
// заједничку класу `.db-hero` у палети иду на тамноплаво→плави градијент, а сав
// текст (укључујући `text-dark` заглавља) на бело. Мери се СВАКИ механизам
// позадине бар једном; пошто је CSS правило заједничко, репрезентативан узорак
// доказује цео скуп.
const HERO_STRANE = [
  '/admin/mineral_collection',          // локални .page-header зелени градијент
  '/admin/exhibitions_database',        // инлајн linear-gradient
  '/admin/cultural_heritage_database',  // bg-warning + text-dark (најризичнији)
  '/admin/inventory_book',              // bg-warning + text-white
  '/admin/research_database',           // bg-dark
  '/admin/library_database',            // bg-info
];
for (const url of HERO_STRANE) {
  for (const paleta of PALETE) {
    for (const rezim of PALETE_REZIMI) {
      test(`контраст заглавља базе (${paleta} × ${rezim}): ${url}`, async ({ page }) => {
        test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');
        await login(page);
        const resp = await page.goto(url, { waitUntil: 'domcontentloaded' });
        test.skip(!resp || resp.status() !== 200, `Стране ${url} нема на овом окружењу.`);
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(600);
        await postaviPaletu(page, paleta, 'komforno', rezim);
        // Дугачке базе (нпр. библиотека/минерали) дају врло висок fullPage снимак
        // који руши декодовање мерача (EncodingError). Заглавље је при врху, па се
        // садржај испод сакрива да снимак остане декодабилан (исто као thead група).
        await page.addStyleTag({ content: '.table tbody, table tbody { display: none !important; }' });
        await page.waitForTimeout(150);

        const padovi = await izmeriKontrast(page, '.db-hero');
        expect(padovi,
          `Заглавље базе испод AA (${paleta} × ${rezim}) на ${url}:\n${opisPadova(padovi)}`)
          .toEqual([]);
      });
    }
  }
}

// --- 5) ЈЕДИНСТВЕНО ЗАГЛАВЉЕ СТРАНЕ (.page-hero) × палета × режим -----------
// Заглавља осталих модула (радне листе, захтеви, админ форме, K-R досије,
// документи, пројекти…) су раније носила сопствену боју (Bootstrap bg-*,
// инлајн градијент, модул-специфичне класе) па нису пратила палету. Сада сва
// деле класу `.page-hero` (исти механизам као `.db-hero`): равна палета их води
// на --pal-thead-bg са белим текстом. Мери се бар по један представник сваког
// механизма/модула; пошто је CSS правило заједничко, узорак доказује цео скуп.
const PAGE_HERO_STRANE = [
  '/admin/timesheet',            // bg-primary картица (радне листе)
  '/vehicle_management',         // bg-dark (најтамнији bg-*)
  '/admin/manage_access',        // bg-info
  '/zahtevi/godisnji-odmor',     // инлајн linear-gradient
  '/terenska-aktivnost',         // инлајн linear-gradient
  '/dokumenti',                  // модул класа .dokumenti-header
  '/kr-dosije',                  // модул класа .kr-header
  '/admin/projekti',             // модул класа .project-hero
];
for (const url of PAGE_HERO_STRANE) {
  for (const paleta of PALETE) {
    for (const rezim of PALETE_REZIMI) {
      test(`контраст заглавља стране (${paleta} × ${rezim}): ${url}`, async ({ page }) => {
        test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');
        await login(page);
        const resp = await page.goto(url, { waitUntil: 'domcontentloaded' });
        test.skip(!resp || resp.status() !== 200, `Стране ${url} нема на овом окружењу.`);
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(600);
        await postaviPaletu(page, paleta, 'komforno', rezim);
        await page.addStyleTag({ content: '.table tbody, table tbody { display: none !important; }' });
        await page.waitForTimeout(150);

        const padovi = await izmeriKontrast(page, '.page-hero');
        expect(padovi,
          `Заглавље стране испод AA (${paleta} × ${rezim}) на ${url}:\n${opisPadova(padovi)}`)
          .toEqual([]);
      });
    }
  }
}
