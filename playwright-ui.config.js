// Dedicated Playwright config for client-side UI unit tests.
// Like playwright-i18n.config.js, these run against a blank page (no Flask
// server) and exercise the real shipped static/js against fixtures.
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests/ui',
  timeout: 30_000,
  use: { headless: true },
  reporter: [['list']],
});
