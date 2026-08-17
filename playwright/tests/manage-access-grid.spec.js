// Browser test: mreža modula na /admin/manage_access.
// Produkcijski bug (2026-07): dodeljen per-user modul (Baza minerala) — pristup
// je radio, a kartica je i dalje pokazivala "+" (kao da NIJE dodeljena), bez
// jasne vizuelne razlike. Proverava se u pravom browseru: dodela odmah oboji
// karticu (ДОДЕЉЕНО badge + zelena + dugme "-"), i to stanje PREŽIVI reload
// (server rendera stvarnu dozvolu iz svežeg izvora).
const { test, expect } = require('@playwright/test');

const EMAIL = process.env.CYPRESS_ADMIN_EMAIL || process.env.QA_EMAIL;
const PASS = process.env.CYPRESS_ADMIN_PASSWORD || process.env.QA_PASSWORD;

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(EMAIL);
  await page.getByTestId('login-password').fill(PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

/* global showUserModules */ // funkcija iz app JS-a, postoji u stranici
// Izaberi prvog stvarnog korisnika i vrati mu email.
async function selectFirstUser(page) {
  const email = await page.evaluate(() => {
    const sel = document.getElementById('userSelect');
    const opt = Array.from(sel.options).find((o) => o.value);
    sel.value = opt.value;
    showUserModules();
    return opt.value;
  });
  await expect(page.locator('#modulesList')).toBeVisible();
  return email;
}

// Ključ prve NE-dodeljene, ne-podrazumevane (bez SVI) kartice modula.
async function firstUnassignedModuleKey(page) {
  return page.evaluate(() =>
    Array.from(document.querySelectorAll('.module-card'))
      .filter((c) => !c.classList.contains('has-access'))
      .filter((c) => !c.querySelector('.badge.bg-success:not(.assigned-badge)'))
      .map((c) => c.id.replace('module-', ''))[0] || null);
}

test('dodela modula odmah oboji karticu i preživi reload', async ({ page }) => {
  test.skip(!EMAIL || !PASS, 'QA kredencijali su potrebni.');
  await login(page);
  await page.goto('/admin/manage_access');

  const email = await selectFirstUser(page);
  const key = await firstUnassignedModuleKey(page);
  test.skip(!key, 'Nema slobodnog per-user modula za test.');

  const card = page.locator(`#module-${key}`);
  await expect(card).not.toHaveClass(/has-access/);
  await expect(card.locator('.assigned-badge')).toBeHidden();

  // Dodeli (klik na "+").
  await card.locator('.grant-btn').click();

  // ODMAH, bez reload-a: kartica istaknuta, badge ДОДЕЉЕНО, dugme "-".
  await expect(card).toHaveClass(/has-access/);
  await expect(card.locator('.assigned-badge')).toBeVisible();
  await expect(card.locator('.revoke-btn')).toBeVisible();
  await expect(card.locator('.grant-btn')).toBeHidden();

  // Vizuelna razlika je stvarna i tema-nezavisna: dodeljena kartica se po
  // okviru/akcentu razlikuje od nedodeljene (ne oslanja se na CDN Bootstrap).
  const styleOf = (loc) => loc.evaluate((el) => {
    const s = getComputedStyle(el);
    return s.borderColor + '|' + s.boxShadow;
  });
  const assignedStyle = await styleOf(card);
  const plainCard = page.locator('.module-card:not(.has-access)').first();
  const plainStyle = await styleOf(plainCard);
  expect(assignedStyle).not.toBe(plainStyle);

  // Reload → server rendera stvarnu dozvolu; kartica OSTAJE dodeljena.
  await page.goto('/admin/manage_access');
  await page.evaluate((wanted) => {
    const sel = document.getElementById('userSelect');
    sel.value = wanted;
    showUserModules();
  }, email);
  const cardAfter = page.locator(`#module-${key}`);
  await expect(cardAfter).toHaveClass(/has-access/);
  await expect(cardAfter.locator('.assigned-badge')).toBeVisible();

  // Čišćenje: vrati na prethodno stanje (ukini pristup).
  await cardAfter.locator('.revoke-btn').click();
  await expect(cardAfter).not.toHaveClass(/has-access/);
});
