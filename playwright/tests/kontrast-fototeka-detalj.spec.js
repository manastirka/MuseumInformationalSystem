// Контраст на ДЕТАЉНОМ ПРИКАЗУ ФОТОГРАФИЈЕ у тамној теми и високом контрасту.
//
// Баг са продукције (пети из истог обрасца): текст око слике био је слабо
// видљив у тамној теми. Узрок није текст него ПОВРШИНА — `.fototeka-card` је
// имао хардкодован бели градијент у сваком режиму, а текст у њему наслеђује
// токен теме (у тамној: крем `--text-primary`). Измерено пре поправке:
// наслов „Подаци" 1.05:1, метаподаци 1.13:1, лабеле 1.54:1.
//
// Зашто НЕ axe: позадина је градијент, па axe не уме да израчуна контраст и
// чвор заврши у `incomplete` корпи (`bgGradient`), а НЕ у `violations` — тест
// на axe-у би прошао зелен док корисник гледа нечитљиву страну. Зато се овде
// мери стварни пиксел испод текста (`helpers/kontrast.js`).
const { test, expect } = require('@playwright/test');
const { REZIMI, STILOVI, postaviTemu, izmeriKontrast } = require('./helpers/kontrast');

const EMAIL = process.env.CYPRESS_ADMIN_EMAIL || process.env.QA_EMAIL;
const PASS = process.env.CYPRESS_ADMIN_PASSWORD || process.env.QA_PASSWORD;

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(EMAIL);
  await page.getByTestId('login-password').fill(PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

async function nadjiFotografiju(page) {
  await page.goto('/fototeka');
  const href = await page.locator('a[href*="/fototeka/"]').evaluateAll(
    (els) => els.map((e) => e.getAttribute('href')).find((h) => /\/fototeka\/\d+$/.test(h)) || null
  );
  return href;
}

for (const rezim of REZIMI) {
  for (const stil of STILOVI) {
    test(`контраст детаљног приказа фотографије: ${rezim} × ${stil}`, async ({ page }) => {
      test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');
      await login(page);

      const href = await nadjiFotografiju(page);
      test.skip(!href, 'Нема ниједне фотографије у овој бази.');

      await page.goto(href);
      await postaviTemu(page, rezim, stil);

      // мери се САМО плоча око слике — навигација/подножје имају своје тестове
      const padovi = await izmeriKontrast(page, '.fototeka-card');
      const opis = padovi.map((p) => `${p.selektor} "${p.tekst}" ${p.odnos}:1 (fg=${p.fg} bg=${p.bg})`).join('\n');
      expect(padovi, `Текст испод AA на .fototeka-card (${rezim} × ${stil}):\n${opis}`).toEqual([]);
    });
  }
}
