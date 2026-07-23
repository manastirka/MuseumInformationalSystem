// Browser test: dashboard виџет „Друштвене мреже музеја".
// Циљ поправке: виџет се сме укључити БЕЗ иједне console грешке пореклом са
// НАШЕ стране. Facebook feed је sandbox iframe (facebook.com origin) — FB грешке
// остају унутар њега и не рачунају се. Ако је FB блокиран → уредан fallback.
const { test, expect } = require('@playwright/test');

const EMAIL = process.env.CYPRESS_ADMIN_EMAIL || process.env.QA_EMAIL;
const PASS = process.env.CYPRESS_ADMIN_PASSWORD || process.env.QA_PASSWORD;

// Грешке из facebook iframe-а НЕ рачунамо (њихов origin, не наш).
function isFacebook(url) {
  return /facebook\.com|fbcdn|fbsbx/i.test(url || '');
}
// Позната headless-GPU бука: weather виџет тражи WebGL контекст који headless
// Chromium не може да направи (у правом прегледачу са GPU-ом је нема). Није у
// вези са друштвеним мрежама — филтрирамо да тест мери оно што треба.
function isHeadlessGpuNoise(text, url) {
  return /WebGL|three\.min\.js/i.test(text || '') ||
         /weather_particles|three\.min\.js/i.test(url || '');
}

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(EMAIL);
  await page.getByTestId('login-password').fill(PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

function collectOurErrors(page) {
  const errors = [];
  page.on('console', m => {
    if (m.type() !== 'error') return;
    const url = (m.location() && m.location().url) || '';
    if (isFacebook(url)) return;
    if (isHeadlessGpuNoise(m.text(), url)) return;
    errors.push(m.text().slice(0, 200) + '  @ ' + url);
  });
  page.on('pageerror', e => {
    const s = String(e);
    if (isHeadlessGpuNoise(s, '')) return;
    errors.push('pageerror: ' + s.slice(0, 200));
  });
  return errors;
}

test('dashboard са укљученим виџетом: нула console грешака са нашег origin-а', async ({ page }) => {
  test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');
  await login(page);
  const ourErrors = collectOurErrors(page);

  await page.goto('/dashboard');
  await page.waitForLoadState('networkidle');

  const section = page.locator('[data-social-embed="facebook"]');
  await expect(section).toHaveCount(1);                 // виџет је враћен/укључен
  await section.scrollIntoViewIfNeeded();
  await page.waitForTimeout(6500);                      // FB се учита ИЛИ падне на fallback (~5s)

  expect(ourErrors, 'Console грешке са нашег origin-а:\n' + ourErrors.join('\n')).toEqual([]);
});

test('виџет: fallback картица кад је Facebook блокиран (route abort)', async ({ page }) => {
  test.skip(!EMAIL || !PASS, 'QA креденцијали су потребни.');
  await login(page);
  const ourErrors = collectOurErrors(page);

  await page.route('**facebook.com/**', r => r.abort());  // adblock/мрежа: FB недоступан

  await page.goto('/dashboard');
  await page.waitForLoadState('networkidle');

  const section = page.locator('[data-social-embed="facebook"]');
  await expect(section).toHaveCount(1);
  await section.scrollIntoViewIfNeeded();

  // Уместо празне рупе → уредан fallback са линковима; iframe сакривен.
  await expect(section.locator('[data-role="fallback"]')).toBeVisible({ timeout: 9000 });
  await expect(section.locator('[data-role="frame"]')).toBeHidden();

  // Аборт FB-а не сме да прља нашу конзолу.
  expect(ourErrors, 'Console грешке са нашег origin-а:\n' + ourErrors.join('\n')).toEqual([]);
});
