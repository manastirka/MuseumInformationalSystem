// Dedicated Playwright config for translator.js unit tests.
// These run against a blank page (no Flask server), unlike the QA e2e suite.
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests/i18n',
  timeout: 30_000,
  use: { headless: true },
  reporter: [['list']],
});
