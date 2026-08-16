const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: process.env.CYPRESS_BASE_URL || 'https://127.0.0.1:5050',
    specPattern: 'cypress/e2e/**/*.cy.js',
    supportFile: 'cypress/support/e2e.js',
    video: false,
    screenshotOnRunFailure: true,
    chromeWebSecurity: false,
    defaultCommandTimeout: 10000,
    requestTimeout: 15000,
    responseTimeout: 15000,
    setupNodeEvents(on) {
      on('before:browser:launch', (browser = {}, launchOptions) => {
        if (browser.family === 'chromium' || browser.name === 'electron') {
          launchOptions.args.push('--enable-unsafe-swiftshader');
        }

        return launchOptions;
      });
    },
    env: {
      adminEmail: process.env.CYPRESS_ADMIN_EMAIL || 'admin@nhmbeo.rs',
      adminPassword: process.env.CYPRESS_ADMIN_PASSWORD || '',
      employeeEmail: process.env.CYPRESS_EMPLOYEE_EMAIL || '',
      employeePassword: process.env.CYPRESS_EMPLOYEE_PASSWORD || '',
      resetTargetEmail: process.env.CYPRESS_RESET_TARGET_EMAIL || '',
      firstLoginEmail: process.env.CYPRESS_FIRST_LOGIN_EMAIL || '',
      firstLoginPassword: process.env.CYPRESS_FIRST_LOGIN_PASSWORD || '',
      archiveEmail: process.env.CYPRESS_ARCHIVE_EMAIL || '',
      archivePassword: process.env.CYPRESS_ARCHIVE_PASSWORD || ''
    }
  }
});
