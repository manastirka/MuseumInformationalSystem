// Tests for static/js/translator.js — the real client-side i18n engine.
// Loads the actual shipped file into a blank page (no Flask server needed)
// and exercises MuseumTranslator directly.
//
// Covers two known defects and new-module EN coverage:
//   Bug A — greedy substring collision: short EN keys (од/Да/Пол/Пон/Ред…)
//           corrupt ordinary words mid-string ("период"→"периof").
//   Bug B — sr-Latn all-caps digraph: "ПРИРОДЊАЧКИ"→"PRIRODNjAČKI"
//           instead of "PRIRODNJAČKI".
//   Coverage — new approval/archive/documents modules must fully translate.

const { test, expect } = require('@playwright/test');
const path = require('path');

const TRANSLATOR = path.resolve(__dirname, '../../static/js/translator.js');
const CYR = /[Ѐ-ӿ]/;
// A token that mixes Latin and Cyrillic letters = garbled output.
const MIXED = /[A-Za-zČĆŽŠĐčćžšđ][Ѐ-ӿ]|[Ѐ-ӿ][A-Za-zČĆŽŠĐčćžšđ]/;

async function loadTranslator(page) {
  await page.setContent(
    '<!doctype html><html><head><meta name="csrf-token" content="x"></head><body></body></html>'
  );
  await page.addScriptTag({ path: TRANSLATOR });
}

// A blank setContent page has an opaque origin where document.cookie throws.
// The translator persists the chosen language via cookie + fetch; stub both in
// the page realm so the pure translation logic under test can run.
const STUB_PERSIST = `
  Object.defineProperty(Document.prototype, 'cookie', {
    get() { return ''; }, set() {}, configurable: true,
  });
  window.fetch = function () { return Promise.reject(new Error('stubbed')); };
`;

// Translate a batch of Cyrillic strings to English through the REAL engine.
// Each string goes in its own <span> so nodes never interfere.
async function toEnglish(page, strings) {
  return page.evaluate((items) => {
    // eslint-disable-next-line no-eval
    eval(items.stub);
    items = items.list;
    const body = document.body;
    body.innerHTML = '';
    const spans = items.map((t, i) => {
      const s = document.createElement('span');
      s.id = 'seg' + i;
      s.textContent = t;
      body.appendChild(s);
      return s;
    });
    // engine starts at sr-Cyrl baseline; force a clean switch each call
    MuseumTranslator.switchLanguage('sr-Cyrl');
    MuseumTranslator.switchLanguage('en');
    return spans.map((s) => s.textContent);
  }, { list: strings, stub: STUB_PERSIST });
}

test.describe('Bug B — sr-Latn transliteration (all-caps digraphs)', () => {
  test('uppercase Љ/Њ/Џ become NJ/LJ/DŽ in all-caps words', async ({ page }) => {
    await loadTranslator(page);
    const cases = await page.evaluate(() => {
      const T = (t) => MuseumTranslator.transliterate(t, false); // Cyr -> Lat
      return {
        prirodnjacki: T('ПРИРОДЊАЧКИ'),
        njegos_upper: T('ЊЕГОШ'),
        njegos_title: T('Његош'),
        sortiranje_upper: T('СОРТИРАЊЕ'),
        sortiranje_lower: T('сортирање'),
        ljudska: T('ЉУДСКА'),
      };
    });
    expect(cases.prirodnjacki).toBe('PRIRODNJAČKI');
    expect(cases.njegos_upper).toBe('NJEGOŠ');
    expect(cases.njegos_title).toBe('Njegoš');
    expect(cases.sortiranje_upper).toBe('SORTIRANJE');
    expect(cases.sortiranje_lower).toBe('sortiranje');
    expect(cases.ljudska).toBe('LJUDSKA');
  });
});

test.describe('Bug A — EN translation must not garble words mid-string', () => {
  test('ordinary words keep their letters (no Latin+Cyrillic mash)', async ({ page }) => {
    await loadTranslator(page);
    const inputs = ['период', 'Полица А1-15', 'Хермафродит', 'Историја', 'Средина'];
    const out = await toEnglish(page, inputs);
    for (const s of out) {
      expect(s, `"${s}" must not mix scripts`).not.toMatch(MIXED);
    }
    // These have no dictionary key, so they must stay intact (not partially eaten).
    expect(out[0]).toBe('период');
    expect(out[1]).toContain('Полица');
    expect(out[2]).toBe('Хермафродит');
  });

  test('short keys still translate when standalone', async ({ page }) => {
    await loadTranslator(page);
    const out = await toEnglish(page, ['Пол', 'Да', 'Не', 'Пон', '5 од 10']);
    expect(out[0]).toBe('Sex');
    expect(out[1]).toBe('Yes');
    expect(out[2]).toBe('No');
    expect(out[3]).toBe('Mon');
    expect(out[4]).toBe('5 of 10');
  });
});

test.describe('Coverage — new modules translate fully to English', () => {
  test('approval center / archive / documents key strings', async ({ page }) => {
    await loadTranslator(page);
    const inputs = [
      'Центар за одобравање',
      'Ток одобравања',
      'Поништи',
      'Датотека',
      'Отпремио',
      'Отпреми као нацрт',
      'Наслов документа',
      'Одобрена документа',
      'Пошаљи на одобрење',
      'Сва одељења',
    ];
    const out = await toEnglish(page, inputs);
    for (const s of out) {
      expect(s, `"${s}" should be fully English`).not.toMatch(CYR);
    }
  });
});
