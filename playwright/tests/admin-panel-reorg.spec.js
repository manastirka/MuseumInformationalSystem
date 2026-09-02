const { test, expect } = require('@playwright/test');

// Verifies the reorganized admin panel (fix/admin-panel-raspored):
// vertical domain sections, every live module present, the legacy
// "Управљање сликама" card gone, and module navigation working.
// Skips unless admin QA credentials are provided.

const ADMIN_EMAIL = process.env.CYPRESS_ADMIN_EMAIL;
const ADMIN_PASSWORD = process.env.CYPRESS_ADMIN_PASSWORD;
const SHOT = process.env.ADMIN_SHOT_PATH; // optional: capture a full-page screenshot

async function login(page, email, password) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(email);
  await page.getByTestId('login-password').fill(password);
  await page.getByTestId('login-submit').click();
}

test('admin panel: vertical sections, all modules, working navigation', async ({ page }) => {
  test.skip(!ADMIN_EMAIL || !ADMIN_PASSWORD, 'Admin credentials required.');

  await login(page, ADMIN_EMAIL, ADMIN_PASSWORD);
  await expect(page).not.toHaveURL(/\/login$/);

  await page.goto('/admin');
  await page.waitForLoadState('networkidle');
  if (SHOT) {
    await page.screenshot({ path: SHOT, fullPage: true });
  }

  const body = page.locator('body');

  // Vertical domain sections
  await expect(body).toContainText('Корисници и приступ');
  await expect(body).toContainText('Збирке и садржај');
  await expect(body).toContainText('Систем и логови');

  // Legacy image-management card removed
  await expect(body).not.toContainText('Управљање сликама');

  // Every live module present (admin sees all)
  const labels = [
    'Управљај приступом модулима',
    'Листа корисника',
    'Додај корисника',
    'Менаџер лозинки',
    'Ревизиони траг',
    'Статистика збирки',
    'Преглед свих база',
    'База запослених',
    'Профили запослених',
    'Системска подешавања',
    'Управљање базом података',
    'Системски логови',
    'Безбедносна подешавања',
    'Извештаји система',
    'Администрација поште',
  ];
  for (const label of labels) {
    await expect(body).toContainText(label);
  }

  // Navigation works: click a module and confirm we leave /admin onto a real page
  await page.getByRole('link', { name: /Статистика збирки/ }).click();
  await page.waitForLoadState('networkidle');
  await expect(page).not.toHaveURL(/\/admin$/);
  await expect(page.locator('body')).not.toContainText(/Internal Server Error|Not Found|Traceback/i);
});
