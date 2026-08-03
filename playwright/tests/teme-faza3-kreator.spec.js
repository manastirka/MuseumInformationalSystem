// Фаза 3 — креатор сопствене теме, пун UI ток:
// направи → сачувај → примени → извези → увези назад → обриши.
const { test, expect } = require('@playwright/test');
const fs = require('fs');
const os = require('os');
const path = require('path');

const ADMIN_EMAIL = process.env.CYPRESS_ADMIN_EMAIL;
const ADMIN_PASSWORD = process.env.CYPRESS_ADMIN_PASSWORD;

async function login(page, email, password) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(email);
  await page.getByTestId('login-password').fill(password);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

// Обриши све постојеће сачуване теме да тест крене од чистог стања.
async function clearExisting(page) {
  page.on('dialog', (d) => d.accept());
  await page.goto('/podesavanja/izgled');
  await page.waitForLoadState('networkidle');
  // Сачекај да JS попуни листу.
  await page.waitForTimeout(500);
  let guard = 0;
  while (guard < 30) {
    const del = page.locator('#customThemeList .saved-theme [data-op="delete"]').first();
    if (await del.count() === 0) { break; }
    await del.click();
    await page.waitForTimeout(400);
    guard++;
  }
}

test.describe('Фаза 3: креатор сопствене теме', () => {
  test.skip(!ADMIN_EMAIL || !ADMIN_PASSWORD, 'Admin creds required.');

  test('направи, сачувај, примени, извези, увези, обриши', async ({ page }) => {
    const errors = [];
    page.on('pageerror', (e) => errors.push(String(e)));
    page.on('console', (m) => {
      if (m.type() === 'error' && /is not defined|ReferenceError|is not a function/i.test(m.text())) { errors.push(m.text()); }
    });

    await login(page, ADMIN_EMAIL, ADMIN_PASSWORD);
    await clearExisting(page);

    // --- креатор постоји ---
    const creator = page.locator('#themeCreator');
    await expect(creator).toBeVisible();
    await creator.scrollIntoViewIfNeeded();

    // --- измени боје и параметре ---
    const uniqueName = 'E2E тема ' + Date.now();
    // Постави основну боју кроз hex поље (change догађај).
    await page.fill('#cc-hex-primary', '#8a2f38');
    await page.dispatchEvent('#cc-hex-primary', 'change');
    await page.fill('#cc-hex-header', '#4d1719');
    await page.dispatchEvent('#cc-hex-header', 'change');
    await page.fill('#cc-hex-button', '#8a2f38');
    await page.dispatchEvent('#cc-hex-button', 'change');
    await page.locator('[data-shadow="strong"]').click();
    await page.fill('#cc-name', uniqueName);

    // --- живи мини-преглед прати избор ---
    const miniBtn = await page.evaluate(() => {
      const mini = document.getElementById('creatorMini');
      return getComputedStyle(mini).getPropertyValue('--x-button').trim();
    });
    expect(miniBtn.toLowerCase()).toBe('#8a2f38');

    // --- контраст очитавање ради (има бројеве) ---
    const ratioText = await page.locator('#ck-text-card .ck-ratio').textContent();
    expect(ratioText).toMatch(/\d+\.\d+:1/);

    // --- Сачувај ---
    await page.locator('#ccSave').click();
    await expect(page.locator('#customThemeList .saved-theme .st-name', { hasText: uniqueName })).toBeVisible({ timeout: 8000 });

    // --- Сачувај и примени ---
    await page.locator('#ccApply').click();
    await page.waitForTimeout(600);
    // Документ носи custom палету са inline --pal-* токенима.
    const applied = await page.evaluate(() => {
      const el = document.documentElement;
      return {
        pal: el.getAttribute('data-palette'),
        primary: el.style.getPropertyValue('--pal-primary').trim(),
        nav: el.style.getPropertyValue('--pal-bg-nav').trim(),
      };
    });
    expect(applied.pal).toBe('custom');
    expect(applied.primary.toLowerCase()).toBe('#8a2f38');
    expect(applied.nav.toLowerCase()).toBe('#4d1719');

    // Примена преживљава навигацију (сервер рендерује inline стил).
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');
    const navAfter = await page.evaluate(() => document.documentElement.getAttribute('data-palette'));
    expect(navAfter).toBe('custom');

    // --- Извоз (преузимање датотеке) ---
    await page.goto('/podesavanja/izgled');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(500);
    const row = page.locator('#customThemeList .saved-theme', { has: page.locator('.st-name', { hasText: uniqueName }) }).first();
    await expect(row).toBeVisible();
    const [download] = await Promise.all([
      page.waitForEvent('download'),
      row.locator('a[data-op="export"]').click(),
    ]);
    const tmpFile = path.join(os.tmpdir(), 'mis-e2e-tema.json');
    await download.saveAs(tmpFile);
    const bundle = JSON.parse(fs.readFileSync(tmpFile, 'utf8'));
    expect(bundle.name).toBe(uniqueName);
    expect(bundle.definition.colors.primary).toBe('#8a2f38');
    expect(bundle.definition.shadow).toBe('strong');

    // --- Увоз назад (нова тема) ---
    const beforeCount = await page.locator('#customThemeList .saved-theme').count();
    await page.setInputFiles('#ccImportFile', tmpFile);
    await page.waitForTimeout(800);
    const afterCount = await page.locator('#customThemeList .saved-theme').count();
    expect(afterCount).toBe(beforeCount + 1);

    // --- Обриши једну тему (потврда прихваћена) ---
    const delFirst = page.locator('#customThemeList .saved-theme [data-op="delete"]').first();
    await delFirst.click();
    await page.waitForTimeout(600);
    const afterDelete = await page.locator('#customThemeList .saved-theme').count();
    expect(afterDelete).toBe(afterCount - 1);

    expect(errors, 'no JS reference errors').toEqual([]);
  });
});
