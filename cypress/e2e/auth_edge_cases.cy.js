describe('Authentication and permission edge cases', () => {
  beforeEach(() => {
    cy.clearCookies();
  });

  it('rejects invalid login credentials without creating a session', () => {
    cy.visit('/login');
    cy.get('[data-testid="login-email"]').clear().type('employee@example.com');
    cy.get('[data-testid="login-password"]').clear().type('WrongPass123!', {
      log: false,
      parseSpecialCharSequences: false
    });
    cy.get('[data-testid="login-submit"]').click();

    cy.url().should('include', '/login');
    cy.contains(/Неисправни подаци за пријаву/i);
  });

  it('redirects anonymous users away from admin pages', () => {
    cy.visit('/admin/timesheet/pending');

    cy.url().should('include', '/login');
    cy.contains(/Морате бити пријављени/i);
  });

  it('returns 401 for anonymous admin API requests', () => {
    cy.request({
      method: 'POST',
      url: '/api/admin/timesheet/report/999/approve',
      body: { approve: true },
      failOnStatusCode: false
    }).then((response) => {
      expect(response.status).to.eq(401);
      expect(response.body).to.deep.equal({
        success: false,
        message: 'Морате бити пријављени'
      });
    });
  });

  it('returns 403 when an employee calls an admin-only API', () => {
    cy.loginAsEmployee();
    cy.url().should('not.include', '/login');

    cy.request({
      method: 'POST',
      url: '/api/admin/timesheet/reports/batch-approve',
      body: { report_ids: [1], approve: true },
      failOnStatusCode: false
    }).then((response) => {
      expect(response.status).to.eq(403);
      expect(response.body).to.deep.equal({
        success: false,
        message: 'Немате дозволу за приступ'
      });
    });
  });
});
