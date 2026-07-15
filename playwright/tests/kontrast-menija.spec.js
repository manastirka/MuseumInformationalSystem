// Kontrast menija u TAMNOJ temi i VISOKOM KONTRASTU, za sva 4 stila.
// Bug sa produkcije: tekst u menijima je bio nečitljiv. Dva korena:
//   1) .dropdown-item.active je uzimao Bootstrap plavu (#0d6efd) — ne prati
//      nijedan token, u tamnoj/kontrastu daje 2.0–3.4:1;
//   2) .navbar .nav-link je koristio --on-accent, a taj token je u tamnoj temi
//      TAMAN (tekst NA akcentu) — a traka navigacije je uvek tamna → tamno na
//      tamnom. Navbar sada ima svoj token --navbar-text.
// Test meri stvarni kontrast (axe-core) nad OTVORENIM menijima i pada ispod AA.
const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

const EMAIL = process.env.CYPRESS_ADMIN_EMAIL || process.env.QA_EMAIL;
const PASS = process.env.CYPRESS_ADMIN_PASSWORD || process.env.QA_PASSWORD;

const REZIMI = ['dark', 'contrast'];
const STILOVI = ['institucionalna', 'moderna', 'arhivska', 'terenska'];
const MENIJI = [
  { ime: 'базе података', sel: '.navbar .nav-link.dropdown-toggle:has-text("Базе")' },
  { ime: 'бирач теме', sel: '#themeSwitcherBtn' },
  { ime: 'бирач језика', sel: '#langSwitcherBtn' },
];

async function login(page) {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(EMAIL);
  await page.getByTestId('login-password').fill(PASS);
  await page.getByTestId('login-submit').click();
  await page.waitForLoadState('networkidle');
}

for (const rezim of REZIMI) {
  for (const stil of STILOVI) {
    test(`kontrast menija: ${rezim} × ${stil}`, async ({ page }) => {
      test.skip(!EMAIL || !PASS, 'QA kredencijali su potrebni.');
      await login(page);
      await page.setViewportSize({ width: 1600, height: 950 });

      await page.evaluate(([r, s]) => {
        document.documentElement.setAttribute('data-theme', r);
        document.documentElement.setAttribute('data-bs-theme', r === 'dark' ? 'dark' : 'light');
        if (s === 'institucionalna') document.documentElement.removeAttribute('data-style');
        else document.documentElement.setAttribute('data-style', s);
      }, [rezim, stil]);
      await page.waitForTimeout(300);

      const problemi = [];
      for (const m of MENIJI) {
        const dug = page.locator(m.sel).first();
        if (!(await dug.count())) continue;
        await dug.click({ timeout: 3000 }).catch(() => {});
        await page.waitForTimeout(300);
        if (!(await page.locator('.dropdown-menu.show').count())) continue;

        const rez = await new AxeBuilder({ page })
          .include('.dropdown-menu.show')      // samo otvoreni meni
          .withRules(['color-contrast'])
          .analyze();

        for (const v of rez.violations) {
          for (const n of v.nodes) {
            problemi.push(`${m.ime}: ${String(n.target[0]).slice(0, 50)} — ${(n.any[0]?.message || '').slice(0, 70)}`);
          }
        }
        await page.keyboard.press('Escape');
        await page.waitForTimeout(120);
      }

      expect(problemi, `Kontrast ispod AA (${rezim} × ${stil}):\n${problemi.join('\n')}`).toEqual([]);
    });
  }
}


// Hover kartica (tooltip) vozila — bug sa produkcije: u tamnoj temi tekst na
// tamnoj podlozi (bg i color su bili tamni ~1:1). Tooltip se lazy-renderuje na
// hover, pa ga sweep menija nije video. Meri se stvarni kontrast teksta.
function _lum(c) {
  const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]);
}
function _rgb(s) { const m = s.match(/rgba?\(([^)]+)\)/); return m[1].split(',').map(parseFloat); }
function _odnos(a, b) { const l1 = _lum(a), l2 = _lum(b); return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05); }

for (const rezim of REZIMI) {
  for (const stil of STILOVI) {
    test(`kontrast hover kartice vozila: ${rezim} × ${stil}`, async ({ page }) => {
      test.skip(!EMAIL || !PASS, 'QA kredencijali su potrebni.');
      await login(page);
      const resp = await page.goto('/vehicle_reservations');
      test.skip(!resp || resp.status() >= 400, 'Странице возила нема.');

      await page.evaluate(([r, s]) => {
        document.documentElement.setAttribute('data-theme', r);
        document.documentElement.setAttribute('data-bs-theme', r === 'dark' ? 'dark' : 'light');
        if (s === 'institucionalna') document.documentElement.removeAttribute('data-style');
        else document.documentElement.setAttribute('data-style', s);
      }, [rezim, stil]);
      await page.waitForTimeout(250);

      const karta = page.locator('.vehicle-card[data-bs-toggle="tooltip"]').first();
      test.skip((await karta.count()) === 0, 'Нема возила у бази.');

      // Tooltip se lazy-renderuje; hover ume da promaši pri brzom radu, pa
      // pokušavamo do 3 puta (miš van -> nazad) dok se ne pojavi.
      let info = null;
      for (let poku = 0; poku < 3 && !info; poku++) {
        await page.mouse.move(2, 2);
        await page.waitForTimeout(150);
        await karta.hover();
        await page.waitForTimeout(500);
        info = await page.evaluate(() => {
          const t = document.querySelector('.tooltip-inner');
          if (!t || t.offsetParent === null) return null;
          const cs = getComputedStyle(t);
          return { bg: cs.backgroundColor, color: cs.color };
        });
      }
      expect(info, 'tooltip se nije prikazao').not.toBeNull();
      const o = _odnos(_rgb(info.color), _rgb(info.bg));
      expect(o, `kontrast teksta tooltipa vozila ${o.toFixed(2)} < 4.5 (${info.color} na ${info.bg})`)
        .toBeGreaterThanOrEqual(4.5);
    });
  }
}
