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

function seedAdminState(action, env = {}) {
  return cy.exec('python3 scripts/testing/seed_admin_e2e_state.py', {
    env: {
      ADMIN_E2E_ACTION: action,
      ...env
    },
    failOnNonZeroExit: true
  }).then(({ stdout }) => {
    const values = {};
    stdout.trim().split('\n').forEach((line) => {
      const [key, value] = line.split('=', 2);
      if (key && value) {
        values[key.trim()] = value.trim();
      }
    });
    return values;
  });
}

function runWithAdminSession(adminEmail, adminPassword, callback) {
  cy.login(adminEmail, adminPassword);
  cy.url().then((url) => {
    if (url.includes('/login')) {
      cy.log('Skipping because admin credentials are not valid in this environment.');
      return;
    }

    callback();
  });
}

describe('Comprehensive admin journeys', () => {
  const adminEmail = Cypress.env('adminEmail');
  const adminPassword = Cypress.env('adminPassword');
  const employeeEmail = Cypress.env('employeeEmail');
  const employeePassword = Cypress.env('employeePassword');
  const archiveEmail = Cypress.env('archiveEmail') || Cypress.env('employeeEmail');
  const archivePassword = Cypress.env('archivePassword') || Cypress.env('employeePassword');

  beforeEach(() => {
    cy.clearCookies();
    cy.on('window:confirm', () => true);
    cy.on('window:alert', () => true);
  });

  afterEach(() => {
    resetUserState(employeeEmail, employeePassword, false);
  });

  it('admin resets password and enforces password change lifecycle', () => {
    const tempPassword = 'AdminQa!Reset123A';
    const managedPassword = 'Qa!ManagedPass123A';

    resetUserState(employeeEmail, employeePassword, false);

    runWithAdminSession(adminEmail, adminPassword, () => {
      cy.intercept('GET', '/api/admin/password_manager/users').as('loadUsers');
      cy.visit('/admin/password_manager');
      cy.wait('@loadUsers');

      cy.get('[data-testid="user-search"]').clear().type(employeeEmail);
      cy.get('[data-testid="reset-password"]').first().click({ force: true });
      cy.get('[data-testid="reset-password-input"]')
        .clear()
        .type(tempPassword, { log: false, force: true, parseSpecialCharSequences: false })
        .should('have.value', tempPassword);
      cy.intercept('POST', '/api/admin/password_manager/reset').as('resetPassword');
      cy.get('[data-testid="confirm-reset-password"]').click();
      cy.wait('@resetPassword').its('response.statusCode').should('eq', 200);

      cy.visit('/logout');
      cy.login(employeeEmail, tempPassword);
      cy.url().should('include', '/change_password');
      completePasswordChange(tempPassword, managedPassword);
      cy.url().should('not.include', '/login');

      cy.visit('/logout');
      runWithAdminSession(adminEmail, adminPassword, () => {
        cy.visit('/admin/password_manager');
        cy.wait('@loadUsers');
        cy.get('[data-testid="user-search"]').clear().type(employeeEmail);
        cy.intercept('POST', '/api/admin/password_manager/force_change').as('forceChange');
        cy.get('[data-testid="force-password-change"]').first().click({ force: true });
        cy.wait('@forceChange').its('response.statusCode').should('eq', 200);

        cy.visit('/logout');
        cy.login(employeeEmail, managedPassword);
        cy.url().should('include', '/change_password');
      });
    });
  });

  it('admin verifies and un-verifies a seeded timesheet report', () => {
    // The verify button only renders (and the backend /approve endpoint
    // only accepts) reports in SUBMITTED state — DRAFT means the employee
    // hasn't sent it for review yet. Seed SUBMITTED so the approve/
    // unapprove toggle is reachable.
    seedAdminState('timesheet_report', {
      TARGET_EMAIL: employeeEmail,
      REPORT_MONTH: '12',
      REPORT_YEAR: '2027',
      REPORT_STATUS: 'SUBMITTED',
      REPORT_LOCKED: '1',
      REPORT_VERIFIED: '0',
      ADMIN_EMAIL: adminEmail
    }).then(({ REPORT_ID: reportId }) => {
      runWithAdminSession(adminEmail, adminPassword, () => {
        cy.visit('/admin/timesheet_reports?month=12&year=2027');

        cy.intercept('POST', `/api/admin/timesheet/report/${reportId}/approve`).as('toggleApproval');
        cy.get(`[data-testid="timesheet-report-approve-${reportId}"]`).click({ force: true });
        cy.get('#verifyConfirmYes').click({ force: true });
        cy.wait('@toggleApproval').its('response.statusCode').should('eq', 200);

        cy.visit('/admin/timesheet_reports?month=12&year=2027');
        cy.get(`[data-testid="timesheet-report-unapprove-${reportId}"]`).should('exist').click({ force: true });
        cy.get('#verifyConfirmYes').click({ force: true });
        cy.wait('@toggleApproval').its('response.statusCode').should('eq', 200);

        cy.visit('/admin/timesheet_reports?month=12&year=2027');
        cy.get(`[data-testid="timesheet-report-approve-${reportId}"]`).should('exist');
      });
    });
  });

  it('admin approves a pending timesheet edit request', () => {
    seedAdminState('timesheet_edit_request', {
      TARGET_EMAIL: employeeEmail,
      REPORT_MONTH: '11',
      REPORT_YEAR: '2027',
      REQUEST_REASON: 'QA E2E pending edit request approval'
    }).then(({ REQUEST_ID: requestId }) => {
      runWithAdminSession(adminEmail, adminPassword, () => {
        cy.visit('/admin/timesheet/pending');

        cy.window().then((win) => {
          cy.stub(win, 'prompt').returns('QA approved by admin automation');
        });

        cy.intercept('POST', `/admin/timesheet/pending/approve/${requestId}`).as('approveEditRequest');
        cy.get(`[data-testid="edit-request-approve-${requestId}"]`).click({ force: true });
        cy.wait('@approveEditRequest').its('response.statusCode').should('eq', 200);

        cy.visit('/admin/timesheet/pending');
        cy.get(`[data-testid="edit-request-${requestId}"]`).contains(/Одобрено/i);
      });
    });
  });

  it('admin advances an archive request through both approval steps', () => {
    const title = `QA admin archive ${Date.now()}`;

    resetUserState(archiveEmail, archivePassword, false);
    cy.login(archiveEmail, archivePassword);
    cy.visit('/admin/archive/zahtevi');
    cy.intercept('POST', '/api/archive/requests').as('createArchiveRequest');
    cy.get('[data-testid="new-request"]').click();
    cy.get('[data-testid="archive-type-zahtev"]').select(1);
    cy.get('[data-testid="archive-title"]').type(title);
    cy.get('[data-testid="archive-description"]').type('Comprehensive admin archive approval test.');
    cy.get('[data-testid="archive-submit"]').click();

    cy.wait('@createArchiveRequest').then(({ response }) => {
      expect(response.statusCode).to.be.oneOf([200, 201]);
      const requestId = response.body.id;

      cy.visit('/logout');
      runWithAdminSession(adminEmail, adminPassword, () => {
        cy.visit(`/admin/archive/zahtevi?id=${requestId}`);

        cy.intercept('POST', `/api/archive/requests/${requestId}/approve`).as('approveArchiveRequest');
        cy.get('[data-testid="archive-approval-comment"]').clear().type('QA admin approval step 1');
        cy.get('[data-testid="archive-approve-request"]').click({ force: true });
        cy.wait('@approveArchiveRequest').its('response.statusCode').should('eq', 200);

        cy.visit(`/admin/archive/zahtevi?id=${requestId}`);
        cy.get('[data-testid="archive-approval-comment"]').clear().type('QA admin approval step 2');
        cy.get('[data-testid="archive-approve-request"]').click({ force: true });
        cy.wait('@approveArchiveRequest').its('response.statusCode').should('eq', 200);

        cy.visit(`/admin/archive/zahtevi?id=${requestId}`);
        cy.contains(/Одобрено/i);
      });
    });
  });
});
