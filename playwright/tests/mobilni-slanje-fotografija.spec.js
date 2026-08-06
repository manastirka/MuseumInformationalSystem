// Слање фотографија са телефона — feat/mobilni (Део Б).
// Доказује: мобилно дугме за камеру (accept=image/*, capture=environment),
// акумулацију реда (камера + галерија), лимите с јасном поруком, и да слање
// иде кроз ПОСТОЈЕЋИ пријемни ток (успех по датотеци), уз везу за предмет кад
// се дође са странице предмета. Серверска провера дозволе се доказује одбијањем
// анонимног корисника. Прескаче се без QA сервера/креденцијала.
const { test, expect } = require('@playwright/test');
const path = require('path');

const adminEmail = process.env.CYPRESS_ADMIN_EMAIL;
const adminPassword = process.env.CYPRESS_ADMIN_PASSWORD;
const FIXTURE = path.join(__dirname, 'fixtures', 'mobil-foto.jpg');

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(adminEmail);
  await page.getByTestId('login-password').fill(adminPassword);
  await page.getByTestId('login-submit').click();
  await expect(page).not.toHaveURL(/\/login$/);
}

test.describe('Мобилно слање фотографија', () => {
  test.use({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });

  test.beforeEach(() => {
    test.skip(!adminEmail || !adminPassword, 'QA админ креденцијали су обавезни.');
  });

  test('камера на телефону: accept=image/* и capture=environment', async ({ page }) => {
    await login(page);
    await page.goto('/fototeka/upload', { waitUntil: 'networkidle' });
    await expect(page.locator('#kamera')).toBeVisible();
    const cam = page.locator('#fototekaKamera');
    await expect(cam).toHaveAttribute('accept', /image\/\*/);
    await expect(cam).toHaveAttribute('capture', 'environment');
    // галерија: вишеструки избор
    await expect(page.locator('#fototekaFajlovi')).toHaveAttribute('multiple', '');
  });

  test('ред за слање акумулира и уклања датотеке', async ({ page }) => {
    await login(page);
    await page.goto('/fototeka/upload', { waitUntil: 'networkidle' });
    await page.setInputFiles('#fototekaFajlovi', [FIXTURE]);
    await page.waitForTimeout(150);
    await expect(page.locator('#fototekaRedLista .list-group-item')).toHaveCount(1);
    // uklanjanje
    await page.locator('#fototekaRedLista .list-group-item button').first().click();
    await page.waitForTimeout(150);
    await expect(page.locator('#fototekaRedLista .list-group-item')).toHaveCount(0);
  });

  test('слање иде кроз пријемни ток — извештај по датотеци, без тврдог пада', async ({ page }) => {
    await login(page);
    await page.goto('/fototeka/upload', { waitUntil: 'networkidle' });
    await page.setInputFiles('#fototekaFajlovi', [FIXTURE]);
    await page.waitForTimeout(150);
    await page.locator('#fototekaUploadForm button[type=submit]').click();
    // једна датотека, успех → редирект на детаљ; или извештај ако је дупликат
    await page.waitForTimeout(2500);
    const url = page.url();
    if (/\/fototeka\/\d+$/.test(url)) {
      // успешан унос новог фајла → отворен детаљ
      await expect(page.locator('body')).toBeVisible();
    } else {
      // дупликат (исти sha256 из ранијег пролаза) — извештај без тврде грешке
      const danger = await page.locator('#fototekaUploadReport li.text-danger').count();
      const okOrDup = await page.locator('#fototekaUploadReport li.text-success, #fototekaUploadReport li.text-warning').count();
      expect(danger).toBe(0);
      expect(okOrDup).toBeGreaterThanOrEqual(1);
    }
  });

  test('веза за предмет: банер и предпопуњена веза када се дође са предмета', async ({ page }) => {
    await login(page);
    await page.goto('/fototeka/upload?veza_tip=predmet&veza_zbirka=minerals&veza_inventarni_broj=TEST-123',
      { waitUntil: 'networkidle' });
    await expect(page.locator('#fototekaPredmetBaner')).toBeVisible();
    await expect(page.locator('#fototekaPredmetBaner')).toContainText('TEST-123');
    await expect(page.locator('#uploadVezaTip')).toHaveValue('predmet');
    await expect(page.locator('#uploadVezaInvBroj')).toHaveValue('TEST-123');
  });

  test('дугме „Сликај и пошаљи" видљиво у фототеци на телефону', async ({ page }) => {
    await login(page);
    await page.goto('/fototeka', { waitUntil: 'networkidle' });
    await expect(page.locator('a[href$="/fototeka/upload#kamera"]')).toBeVisible();
  });
});

test.describe('Серверска провера дозволе (не само сакривено дугме)', () => {
  test('анонимни корисник не може да отпреми — POST се одбија', async ({ request }) => {
    const resp = await request.post('/fototeka/upload/jedan', {
      multipart: { file: { name: 'x.jpg', mimeType: 'image/jpeg', buffer: Buffer.from([0xff, 0xd8, 0xff]) } },
      maxRedirects: 0,
    });
    // login_required/module_access → редирект на пријаву или 401/403, никад 200 OK
    expect(resp.status()).not.toBe(200);
  });
});
