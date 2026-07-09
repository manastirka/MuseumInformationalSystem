// Tests for static/js/fototeka_galerija.js — gallery multi-select feedback.
// Loads the actual shipped file into a blank page (no Flask server) and drives
// the checkboxes against a minimal fixture.
//
// Regression: selecting a thumbnail updated the counter but never toggled the
// .selected class on the .foto-item, so the thumbnail showed no blue check /
// highlight. These tests assert BOTH the class (on the right element) and the
// counter, kept in lock-step, plus that the checkmark is actually rendered.

const { test, expect } = require('@playwright/test');
const path = require('path');

const GALLERY_JS = path.resolve(__dirname, '../../static/js/fototeka_galerija.js');

// The selection CSS shipped in templates/fototeka_galerija.html, kept in sync.
const FIXTURE = `<!doctype html><html><head><meta charset="utf-8"><style>
  .foto-item { position: relative; }
  .foto-item.selected { outline: 3px solid rgb(13, 110, 253); outline-offset: -3px; }
  .foto-item.selected::after {
    content: "\\2713"; position: absolute; top: 6px; right: 6px;
    width: 26px; height: 26px; line-height: 26px; text-align: center;
    background: rgb(13, 110, 253); color: #fff; border-radius: 50%; z-index: 3;
  }
</style></head><body>
  <div class="btn-group">
    <button type="button" class="fototeka-view-btn" data-view="grid"></button>
    <button type="button" class="fototeka-view-btn" data-view="list"></button>
    <button type="button" class="fototeka-view-btn" data-view="compact"></button>
  </div>
  <input type="checkbox" id="fototekaSelectAll">
  <span id="fototekaSelCount">0</span>
  <form id="fototekaZipForm">
    <div id="fototekaItems" class="view-grid">
      <div class="foto-item" data-id="1">
        <input class="foto-check" type="checkbox" name="ids" value="1">
      </div>
      <div class="foto-item" data-id="2">
        <input class="foto-check" type="checkbox" name="ids" value="2">
      </div>
    </div>
  </form>
</body></html>`;

async function loadGallery(page) {
  await page.setContent(FIXTURE);
  await page.addScriptTag({ path: GALLERY_JS });
  // setContent already fired DOMContentLoaded before the script attached its
  // listener, so fire it again to run the gallery init().
  await page.evaluate(() => document.dispatchEvent(new Event('DOMContentLoaded')));
}

test('selecting a thumbnail marks it and updates the counter', async ({ page }) => {
  await loadGallery(page);

  const firstItem = page.locator('.foto-item[data-id="1"]');
  const secondItem = page.locator('.foto-item[data-id="2"]');
  const counter = page.locator('#fototekaSelCount');

  await expect(counter).toHaveText('0');
  await expect(firstItem).not.toHaveClass(/selected/);

  await firstItem.locator('input[name="ids"]').check();

  // the class lands on the correct element AND the counter agrees
  await expect(firstItem).toHaveClass(/selected/);
  await expect(counter).toHaveText('1');
  await expect(secondItem).not.toHaveClass(/selected/);

  // the checkmark is actually rendered (selection CSS present + visible)
  const checkmark = await firstItem.evaluate(
    (el) => getComputedStyle(el, '::after').content
  );
  expect(checkmark.replace(/["']/g, '')).toBe('✓');

  // deselecting clears both the class and the counter
  await firstItem.locator('input[name="ids"]').uncheck();
  await expect(firstItem).not.toHaveClass(/selected/);
  await expect(counter).toHaveText('0');
});

test('select-all marks every thumbnail and matches the counter', async ({ page }) => {
  await loadGallery(page);

  await page.locator('#fototekaSelectAll').check();

  await expect(page.locator('.foto-item[data-id="1"]')).toHaveClass(/selected/);
  await expect(page.locator('.foto-item[data-id="2"]')).toHaveClass(/selected/);
  await expect(page.locator('#fototekaSelCount')).toHaveText('2');
});
