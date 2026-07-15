beforeEach(() => {
  cy.intercept('GET', '**/api/notifications', {
    statusCode: 200,
    body: { success: true, notifications: [], unread_count: 0 }
  });
  cy.intercept('GET', '**/api/website-news*', {
    statusCode: 200,
    body: { success: true, news: [] }
  });
  cy.intercept('GET', '**/api/mail/check', {
    statusCode: 200,
    body: { success: true, unread: 0 }
  });
  cy.intercept('GET', '**/api/weather/details', {
    statusCode: 200,
    body: { success: true, weather: null, forecast: [], warnings: [] }
  });
});

Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login');
  cy.get('[data-testid="login-email"]').clear().type(email);
  cy.get('[data-testid="login-password"]').clear().type(password, {
    log: false,
    parseSpecialCharSequences: false
  });
  cy.get('[data-testid="login-submit"]').click();
});

Cypress.Commands.add('loginAsAdmin', () => {
  cy.login(Cypress.env('adminEmail'), Cypress.env('adminPassword'));
});

Cypress.Commands.add('loginAsEmployee', () => {
  cy.login(Cypress.env('employeeEmail'), Cypress.env('employeePassword'));
});

Cypress.Commands.add('logoutIfPossible', () => {
  cy.get('body').then(($body) => {
    const logoutLink = $body.find('a[href*="/logout"], form[action*="/logout"]');
    if (logoutLink.length) {
      cy.visit('/logout');
    }
  });
});
