// Heritage тонови ћелија и беџева + очигледни падови — СВЕ ТРИ теме × 4 стила.
//
// Ово је први тест који мери и СВЕТЛУ тему. Досадашња конвенција („светла остаје
// пиксел-идентична") правила је слепу мрљу: 26 корена / 464 појаве у светлој
// нико није мерио, јер је светла била подразумевана па се сматрала исправном.
//
// Шта овај тест чува (свако измерено ПРЕ поправке):
//
//  1) МРТВА ПРОЗИРНОСТ (корен, 310 од 464 појаве). Bootstrap боју позадине даје
//     као `rgba(<боја>, var(--bs-bg-opacity))`, а heritage је преписивао
//     ГРАДИЈЕНТОМ кроз скраћеницу `background:` — градијент ту променљиву не
//     чита, па је `.bg-opacity-25` под heritage-ом била без дејства. Ћелије
//     календара замишљене као блага тинта испадале су ПУНЕ и средњетамне, а на
//     њима пада и тамни и бели текст: `small.text-muted` 2.06:1, `.text-success`
//     2.28:1 на `/vehicle_reservations`.
//     Није било питање тона него мртве прозирности — зато `color-mix`.
//
//  2) СЛИКА ПРЕКО БОЈЕ. Иста скраћеница гази и Bootstrap-ове помоћне класе:
//     `<div class="card bg-dark text-white">` добијао је heritage кремасти
//     градијент ИЗНАД тамне боје (слика се црта преко боје), па је остајао бели
//     текст на крему — 1.21:1 на `/vehicle_management`. Исто и
//     `#calendarTable th` (3.47:1) кроз пергаментни вео преко браон заглавља.
//
//  3) БЕЏЕВИ. `bg-light`/`bg-warning` траже СВЕТЛУ плочу и тамно мастило, а
//     heritage је преко сваког беџа развлачио браон: 2.59:1 („Рад у музеју"),
//     3.74:1 („Поднето"). Уз то су све врсте беџа испадале исто браон, па је боја
//     престајала да носи значење. Сада су то трајно светле плоче са
//     `--paper-text` мастилом — исти образац као `.document-preview`.
//
//  4) ТОКЕНИ ПОДЕШЕНИ ЗА ЈЕДНУ ПОВРШИНУ. `--success-text` је у светлој био
//     једнак `--success` (боја ПОЗАДИНЕ) → 3.35:1 као текст; `--text-muted` у
//     heritage-у 3.79:1 на кремастој картици, у тамној 4.39:1 на ћелији табеле.
//
// Мери се стварни пиксел испод текста (`helpers/kontrast.js`), не боја из CSS-а:
// све горе су градијенти, где axe ћути (чвор оде у `incomplete`, не у
// `violations`) — тест на axe-у био би зелен над нечитљивом страном.
const { test, expect } = require('@playwright/test');
const { SVI_REZIMI, STILOVI, postaviTemu, izmeriKontrast } = require('./helpers/kontrast');

const EMAIL = process.env.CYPRESS_ADMIN_EMAIL || process.env.QA_EMAIL;
const PASS = process.env.CYPRESS_ADMIN_PASSWORD || process.env.QA_PASSWORD;

const STRANE = [
  '/vehicle_reservations',   // ћелије календара (мртва прозирност), заглавље табеле
  '/admin/timesheet_reports', // беџеви bg-light/bg-warning, `.text-white` заглавље
  '/vehicle_management',     // `card bg-dark text-white`
  '/dashboard',              // пригушени описи вести, прогноза
  '/terenska-aktivnost',     // заглавље-градијент, пригушено у табели
  '/zahtevi/godisnji-odmor', // заглавље-градијент, `.form-text`
  '/zahtevi/odobravanje',    // табови и стрелица ланца одобравања
  '/fototeka/uvoz',          // `<code>` на тамнозеленом заглављу
  '/admin/manage_access',    // беџеви
];

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(EMAIL);
  await page.getByTestId('login-password').fill(PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

for (const url of STRANE) {
  for (const rezim of SVI_REZIMI) {
    for (const stil of STILOVI) {
      test(`контраст (${rezim} × ${stil}): ${url}`, async ({ page }) => {
        test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');
        await login(page);
        const resp = await page.goto(url, { waitUntil: 'domcontentloaded' });
        test.skip(!resp || resp.status() !== 200, `Стране ${url} нема на овом окружењу.`);
        // Календар резервација се гради из JS-а ПОСЛЕ учитавања — без чекања
        // мерење хвата полупразну страну и тест је нестабилан.
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(600);
        await postaviTemu(page, rezim, stil);

        const padovi = await izmeriKontrast(page);
        const opis = padovi
          .map((p) => `${p.selektor} "${p.tekst}" ${p.odnos}:1 (fg=${p.fg} bg=${p.bg})`)
          .join('\n');
        expect(padovi, `Текст испод AA (${rezim} × ${stil}) на ${url}:\n${opis}`).toEqual([]);
      });
    }
  }
}
