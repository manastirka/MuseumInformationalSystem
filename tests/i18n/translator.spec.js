// Tests for static/js/translator.js — the real client-side i18n engine.
// Loads the actual shipped file into a blank page (no Flask server needed)
// and exercises MuseumTranslator directly.
//
// English was soft-removed 2026-07-08: the app is Serbian-only (Cyrillic +
// Latin). These tests verify that:
//   - Serbian Latin transliteration still works, incl. all-caps digraphs;
//   - selecting / restoring English falls back to Cyrillic with no raw keys;
//   - the English dictionary + translation code stay dormant (re-enablable).

const { test, expect } = require('@playwright/test');
const path = require('path');

const TRANSLATOR = path.resolve(__dirname, '../../static/js/translator.js');
const CYR = /[Ѐ-ӿ]/;
// A token mixing Latin and Cyrillic letters = garbled/translated output.
const MIXED = /[A-Za-zČĆŽŠĐčćžšđ][Ѐ-ӿ]|[Ѐ-ӿ][A-Za-zČĆŽŠĐčćžšđ]/;
const LATIN_WORD = /[A-Za-z]{2,}/;

async function loadTranslator(page) {
  await page.setContent(
    '<!doctype html><html><head><meta name="csrf-token" content="x"></head><body></body></html>'
  );
  await page.addScriptTag({ path: TRANSLATOR });
}

// Drive the real engine in the page. A blank setContent page has an opaque
// origin where document.cookie throws, so we stub cookie (with a chosen value)
// and fetch, build one <span> per input string, run `action`, and report back.
async function run(page, { strings = [], cookie = '', action = null }) {
  return page.evaluate(({ strings, cookie, action }) => {
    Object.defineProperty(Document.prototype, 'cookie', {
      get() { return cookie; }, set() {}, configurable: true,
    });
    window.fetch = function () { return Promise.reject(new Error('stubbed')); };

    const body = document.body;
    body.innerHTML = '';
    const spans = strings.map((t) => {
      const s = document.createElement('span');
      s.textContent = t;
      body.appendChild(s);
      return s;
    });

    const pref = MuseumTranslator.getLangPreference();
    if (action === 'switch-en') MuseumTranslator.switchLanguage('en');
    else if (action === 'switch-latn') MuseumTranslator.switchLanguage('sr-Latn');
    else if (action === 'init') MuseumTranslator.init();

    return {
      pref,
      texts: spans.map((s) => s.textContent),
      htmlLang: document.documentElement.lang,
    };
  }, { strings, cookie, action });
}

test.describe('Serbian Latin transliteration (active)', () => {
  test('all-caps digraphs Љ/Њ/Џ become NJ/LJ/DŽ', async ({ page }) => {
    await loadTranslator(page);
    const c = await page.evaluate(() => {
      const T = (t) => MuseumTranslator.transliterate(t, false);
      return {
        prirodnjacki: T('ПРИРОДЊАЧКИ'),
        njegos_upper: T('ЊЕГОШ'),
        njegos_title: T('Његош'),
        sortiranje_upper: T('СОРТИРАЊЕ'),
        ljudska: T('ЉУДСКА'),
      };
    });
    expect(c.prirodnjacki).toBe('PRIRODNJAČKI');
    expect(c.njegos_upper).toBe('NJEGOŠ');
    expect(c.njegos_title).toBe('Njegoš');
    expect(c.sortiranje_upper).toBe('SORTIRANJE');
    expect(c.ljudska).toBe('LJUDSKA');
  });

  test('switching to sr-Latn transliterates the page', async ({ page }) => {
    await loadTranslator(page);
    const { texts } = await run(page, { strings: ['Његош', 'Одобри'], action: 'switch-latn' });
    expect(texts).toEqual(['Njegoš', 'Odobri']);
  });
});

test.describe('English is soft-removed', () => {
  test('selecting English falls back to Cyrillic (no translation, no raw keys)', async ({ page }) => {
    await loadTranslator(page);
    // 'Датотека' HAS an English dictionary key ('File'); 'период' has none.
    // With English disabled, both must stay exactly Cyrillic.
    const { texts, htmlLang } = await run(page, {
      strings: ['Датотека', 'период', 'Центар за одобравање'],
      action: 'switch-en',
    });
    expect(texts).toEqual(['Датотека', 'период', 'Центар за одобравање']);
    for (const t of texts) {
      expect(t).not.toMatch(MIXED);
      expect(t).not.toMatch(LATIN_WORD);
    }
    expect(htmlLang).not.toBe('en');
  });

  test('a saved museum_lang=en preference resolves to Cyrillic', async ({ page }) => {
    await loadTranslator(page);
    const { pref, texts } = await run(page, {
      strings: ['Датотека', 'Одобравате:'],
      cookie: 'museum_lang=en; theme=dark',
      action: 'init',
    });
    expect(pref).toBe('sr-Cyrl');
    // init() with a legacy 'en' cookie must leave the page Cyrillic, untouched.
    expect(texts).toEqual(['Датотека', 'Одобравате:']);
    for (const t of texts) expect(t).not.toMatch(LATIN_WORD);
  });
});

test.describe('English engine stays dormant (re-enablable)', () => {
  test('dictionary is preserved so English can be restored', async ({ page }) => {
    await loadTranslator(page);
    const dict = await page.evaluate(() => MuseumTranslator.translations);
    expect(Object.keys(dict).length).toBeGreaterThan(1000);
    // sample keys, including ones added for the new modules, remain intact
    expect(dict['Датотека']).toBe('File');
    expect(dict['Центар за одобравање']).toBe('Approval Center');
  });
});
