// Контраст на странама захтева (преглед молбе) и музејске збирке, тамна тема.
//
// Корен 1 — `.document-preview`: преглед молбе је ФИКСНО бели папир (документ
// који се штампа), а текст у њему је наслеђивао токен теме → у тамној крем на
// белом, измерено 1.18–1.31:1. Иста замка као навигација, само обрнута: тамно
// мастило на трајно светлој подлози → токен `--paper-text`. Исти шаблон
// прегледа користе 4 стране захтева, зато се овде проверавају све четири.
//
// Корен 2 — `.bg-light .text-muted`: `.bg-light` је у тамној `--gray-100`
// (#374151), светлије од картице, па `--text-muted` пада на 3.35:1.
const { test, expect } = require('@playwright/test');
const { STILOVI, postaviTemu, izmeriKontrast } = require('./helpers/kontrast');

const EMAIL = process.env.CYPRESS_ADMIN_EMAIL || process.env.QA_EMAIL;
const PASS = process.env.CYPRESS_ADMIN_PASSWORD || process.env.QA_PASSWORD;

const STRANE = [
  '/zahtevi/godisnji-odmor',
  '/zahtevi/slobodan-dan',
  '/zahtevi/razno',
  '/zahtev-sluzbeni-put',
  '/admin/mineral_collection',
];

// Познати ОТВОРЕНИ падови — НИСУ баг тамне теме. Сви падају и у СВЕТЛОЈ
// (мерено): заглавље молбе — розе градијент у самом шаблону, бело на #f093fb
// 2.21:1 светла / 1.69:1 тамна; `badge bg-success` 2.56:1 светла;
// `badge bg-white.text-dark` 2.89:1 светла; `.nav-tabs-custom .nav-link.active`
// — бело на зеленом градијенту 4.15:1 светла. Светла је ПОДРАЗУМЕВАНА тема, па
// њихова поправка мења изглед свима → тражи одлуку, не тиху закрпу само у
// тамној. `span.page-link` је „…" у онеспособљеној пагинацији (3.83:1).
// Детаљно: `docs/kontrast-sweep-2026-07-16.md`.
const OTVORENO = [
  'h1.h3.mb-1',
  'p.mb-0.opacity-75',
  'span.badge.bg-success.ms-1',
  'span.badge.bg-white.text-dark',
  'a.nav-link.active',
  'span.page-link',
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
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(400);
      await postaviTemu(page, 'dark', stil);

      const padovi = (await izmeriKontrast(page)).filter((p) => !OTVORENO.includes(p.selektor));
      const opis = padovi.map((p) => `${p.selektor} "${p.tekst}" ${p.odnos}:1 (fg=${p.fg} bg=${p.bg})`).join('\n');
      expect(padovi, `Текст испод AA (тамна × ${stil}) на ${url}:\n${opis}`).toEqual([]);
    });
  }
}
