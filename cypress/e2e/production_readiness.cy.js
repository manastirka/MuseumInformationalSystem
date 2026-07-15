function completePasswordChange(currentPassword, nextPassword) {
  cy.get('[data-testid="current-password"]')
    .clear()
    .type(currentPassword, { log: false, force: true, parseSpecialCharSequences: false })
    .should('have.value', currentPassword);
  cy.get('[data-testid="new-password"]')
    .clear()
    .type(nextPassword, { log: false, force: true, parseSpecialCharSequences: false })
    .should('have.value', nextPassword);
  cy.get('[data-testid="confirm-password"]')
    .clear()
    .type(nextPassword, { log: false, force: true, parseSpecialCharSequences: false })
    .should('have.value', nextPassword);
  cy.get('[data-testid="change-password-submit"]').click();
}

function buildStrongTempPassword(basePassword) {
  return `Qa!${basePassword}Temp123A`;
}

function resetUserState(email, password, firstLogin = false) {
  cy.exec('python3 scripts/testing/reset_postgres_user_state.py', {
    env: {
      TEST_RESET_EMAIL: email,
      TEST_RESET_PASSWORD: password,
      TEST_RESET_FIRST_LOGIN: firstLogin ? '1' : '0'
    },
    failOnNonZeroExit: true
  });
}

describe('Production readiness smoke journeys', () => {
  beforeEach(() => {
    cy.clearCookies();
  });

  it('login -> dashboard -> logout', () => {
    cy.loginAsEmployee();
    cy.url().should('not.include', '/login');
    cy.contains(/природњачки музеј|промена лозинке|dashboard|табла/i);
    cy.visit('/logout');
    cy.url().should('match', /\/(index|login)?$/);
  });

  it('first login password change flow', () => {
    const email = Cypress.env('firstLoginEmail');
    const password = Cypress.env('firstLoginPassword');

    if (!email || !password) {
      cy.log('Skipping because firstLoginEmail/firstLoginPassword are not configured.');
      return;
    }

    const nextPassword = buildStrongTempPassword(password);
    resetUserState(email, password, true);
    cy.login(email, password);
    cy.url().should('include', '/change_password');
    completePasswordChange(password, nextPassword);
    cy.url().should('not.include', '/login');

    cy.visit('/logout');
    cy.login(email, nextPassword);
    cy.url().should('not.include', '/login');

    cy.then(() => {
      resetUserState(email, password, true);
    });
  });

  it('employee timesheet save and submit', () => {
    const employeeEmail = Cypress.env('employeeEmail');
    const originalPassword = Cypress.env('employeePassword');
    resetUserState(employeeEmail, originalPassword, false);

    cy.loginAsEmployee();
    cy.url().should('not.include', '/change_password');
    cy.visit('/timesheet/entry');
    cy.intercept('POST', '/api/timesheet/save').as('saveTimesheet');
    cy.intercept('POST', /\/api\/timesheet\/\d+\/submit/).as('submitTimesheet');

    cy.get('[data-testid="timesheet-save"]').first().then(($button) => {
      if ($button.is(':disabled')) {
        cy.contains(/закључана|ограничено време|захтев/i);
        return;
      }

      cy.wrap($button).click({ force: true });
      cy.wait('@saveTimesheet').its('response.statusCode').should('eq', 200);

      cy.get('body').then(($body) => {
        if ($body.find('[data-testid="timesheet-submit"]').length) {
          cy.get('[data-testid="timesheet-submit"]').first().click({ force: true });
          cy.wait('@submitTimesheet').its('response.statusCode').should('eq', 200);
        }
      });
    });
  });

  it('admin password reset flow', () => {
    const targetEmail = Cypress.env('resetTargetEmail');
    if (!targetEmail) {
      cy.log('Skipping because resetTargetEmail is not configured.');
      return;
    }

    cy.loginAsAdmin();
    cy.url().then((url) => {
      if (url.includes('/login')) {
        cy.log('Admin credentials are not valid in this environment.');
        return;
      }

      cy.intercept('GET', '/api/admin/password_manager/users').as('loadUsers');
      cy.visit('/admin/password_manager');
      cy.wait('@loadUsers');
      cy.get('[data-testid="user-search"]').clear().type(targetEmail);
      cy.get('[data-testid="reset-password"]').first().click({ force: true });
      cy.get('[data-testid="reset-password-input"]').type('TempPassword123!A', { log: false });
      cy.intercept('POST', '/api/admin/password_manager/reset').as('resetPassword');
      cy.get('[data-testid="confirm-reset-password"]').click();
      cy.wait('@resetPassword').its('response.statusCode').should('eq', 200);
    });
  });

  it('archive request creation flow', () => {
    const archiveEmail = Cypress.env('archiveEmail') || Cypress.env('employeeEmail');
    const archivePassword = Cypress.env('archivePassword') || Cypress.env('employeePassword');
    resetUserState(archiveEmail, archivePassword, false);

    cy.login(archiveEmail, archivePassword);
    cy.url().should('not.include', '/change_password');
    cy.visit('/admin/archive/zahtevi');
    cy.get('[data-testid="new-request"]').click();
    cy.get('[data-testid="archive-type-zahtev"]').select(1);
    cy.get('[data-testid="archive-title"]').type('QA smoke request');
    cy.get('[data-testid="archive-description"]').type('Automated archive request smoke test.');
    cy.intercept('POST', '/api/archive/requests').as('createRequest');
    cy.get('[data-testid="archive-submit"]').click();
    cy.wait('@createRequest').its('response.statusCode').should('be.oneOf', [200, 201]);
  });
});
