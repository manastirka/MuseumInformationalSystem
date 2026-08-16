# QA Automation

## Browser E2E

Install dependencies:

```bash
npm install
```

Start the local QA server:

```bash
npm run qa:server
```

Start the local QA server through Gunicorn instead:

```bash
npm run qa:server:gunicorn
```

Or run the full local wrapper, which starts the server, waits for `/login`, runs Python QA, then runs both Cypress suites:

```bash
export CYPRESS_BASE_URL=http://127.0.0.1:5050
export CYPRESS_ADMIN_EMAIL=admin@nhmbeo.rs
export CYPRESS_ADMIN_PASSWORD='...'
export CYPRESS_EMPLOYEE_EMAIL='...'
export CYPRESS_EMPLOYEE_PASSWORD='...'
export CYPRESS_FIRST_LOGIN_EMAIL='...'
export CYPRESS_FIRST_LOGIN_PASSWORD='...'
export CYPRESS_RESET_TARGET_EMAIL='...'
export CYPRESS_ARCHIVE_EMAIL='...'
export CYPRESS_ARCHIVE_PASSWORD='...'
./run_qa.sh
```

For a production-like wrapper run through Gunicorn:

```bash
export CYPRESS_ADMIN_EMAIL=admin@nhmbeo.rs
export CYPRESS_ADMIN_PASSWORD='...'
export CYPRESS_EMPLOYEE_EMAIL='...'
export CYPRESS_EMPLOYEE_PASSWORD='...'
export CYPRESS_FIRST_LOGIN_EMAIL='...'
export CYPRESS_FIRST_LOGIN_PASSWORD='...'
export CYPRESS_RESET_TARGET_EMAIL='...'
export CYPRESS_ARCHIVE_EMAIL='...'
export CYPRESS_ARCHIVE_PASSWORD='...'
QA_SERVER_MODE=gunicorn QA_INCLUDE_K6=1 ./run_qa.sh
```

If you want the QA server to exercise shared Redis-backed sessions across Gunicorn workers, also provide:

```bash
export QA_REDIS_URL=redis://127.0.0.1:6379/0
```

Or let the wrapper start a local Redis container through `podman`:

```bash
QA_SERVER_MODE=gunicorn QA_USE_REDIS=1 QA_INCLUDE_K6=1 ./run_qa.sh
```

By default the wrapper also runs:

- `npm run qa:lint`
- `npm run e2e:playwright`

Optional local k6 run:

```bash
QA_INCLUDE_K6=1 ./run_qa.sh
```

Server mode options:

- `QA_SERVER_MODE=flask` uses `python app.py` on `127.0.0.1:5050`
- `QA_SERVER_MODE=gunicorn` uses Gunicorn on `127.0.0.1:5051`
- `QA_USE_REDIS=1` starts a local Redis QA dependency through `podman` when `QA_REDIS_URL` is not already set

Gunicorn mode is the recommended path for browser smoke and load checks.

Run the production-readiness smoke suite against the local app:

```bash
CYPRESS_BASE_URL=http://127.0.0.1:5050 \
CYPRESS_ADMIN_EMAIL=admin@nhmbeo.rs \
CYPRESS_ADMIN_PASSWORD='...' \
CYPRESS_EMPLOYEE_EMAIL='...' \
CYPRESS_EMPLOYEE_PASSWORD='...' \
CYPRESS_FIRST_LOGIN_EMAIL='...' \
CYPRESS_FIRST_LOGIN_PASSWORD='...' \
CYPRESS_RESET_TARGET_EMAIL='...' \
npm run e2e:smoke
```

Covered journeys in `cypress/e2e/production_readiness.cy.js`:

- login -> dashboard -> logout
- first-login password change
- employee timesheet save/submit
- admin password reset
- archive request creation

Run the comprehensive admin suite:

```bash
CYPRESS_BASE_URL=http://127.0.0.1:5050 \
CYPRESS_ADMIN_EMAIL=admin@nhmbeo.rs \
CYPRESS_ADMIN_PASSWORD='...' \
CYPRESS_EMPLOYEE_EMAIL='...' \
CYPRESS_EMPLOYEE_PASSWORD='...' \
CYPRESS_ARCHIVE_EMAIL='...' \
CYPRESS_ARCHIVE_PASSWORD='...' \
npm run e2e:admin
```

Covered journeys in `cypress/e2e/admin_comprehensive.cy.js`:

- admin password reset + enforced password change
- admin force-password-change lifecycle
- admin verify / un-verify timesheet
- admin approve pending edit request
- admin approve archive request through both approval steps

Run both browser suites together:

```bash
CYPRESS_BASE_URL=http://127.0.0.1:5050 \
CYPRESS_ADMIN_EMAIL=admin@nhmbeo.rs \
CYPRESS_ADMIN_PASSWORD='...' \
CYPRESS_EMPLOYEE_EMAIL='...' \
CYPRESS_EMPLOYEE_PASSWORD='...' \
CYPRESS_FIRST_LOGIN_EMAIL='...' \
CYPRESS_FIRST_LOGIN_PASSWORD='...' \
CYPRESS_RESET_TARGET_EMAIL='...' \
CYPRESS_ARCHIVE_EMAIL='...' \
CYPRESS_ARCHIVE_PASSWORD='...' \
npm run e2e:all
```

Run the Playwright browser layer:

```bash
CYPRESS_BASE_URL=http://127.0.0.1:5051 \
PLAYWRIGHT_BASE_URL=http://127.0.0.1:5051 \
CYPRESS_ADMIN_EMAIL=admin@nhmbeo.rs \
CYPRESS_ADMIN_PASSWORD='...' \
CYPRESS_EMPLOYEE_EMAIL='...' \
CYPRESS_EMPLOYEE_PASSWORD='...' \
CYPRESS_ARCHIVE_EMAIL='...' \
CYPRESS_ARCHIVE_PASSWORD='...' \
npm run e2e:playwright
```

Covered Playwright journeys in `playwright/tests/production-readiness.spec.js`:

- login flow using the real Flask app
- employee timesheet entry rendering
- admin password manager reachability
- archive request creation
- axe-core accessibility scans for the login page and admin password manager, failing on serious/critical issues

## Python QA

Run the targeted Python regression layer:

```bash
npm run qa:python
```

Print the current observability bootstrap status for the active env:

```bash
npm run qa:observability
```

Run the QA linter:

```bash
npm run qa:lint
```

Run the current combined QA target:

```bash
export CYPRESS_BASE_URL=http://127.0.0.1:5050
export CYPRESS_ADMIN_EMAIL=admin@nhmbeo.rs
export CYPRESS_ADMIN_PASSWORD='...'
export CYPRESS_EMPLOYEE_EMAIL='...'
export CYPRESS_EMPLOYEE_PASSWORD='...'
export CYPRESS_FIRST_LOGIN_EMAIL='...'
export CYPRESS_FIRST_LOGIN_PASSWORD='...'
export CYPRESS_RESET_TARGET_EMAIL='...'
export CYPRESS_ARCHIVE_EMAIL='...'
export CYPRESS_ARCHIVE_PASSWORD='...'
npm run qa:all
```

## Load testing

Run the default k6 smoke profile:

```bash
PATH="/tmp/k6-v0.49.0-linux-amd64:$PATH" \
BASE_URL=http://127.0.0.1:5051 \
K6_PROFILE=smoke \
./scripts/testing/run_k6.sh
```

To include the authenticated employee load path, enable it explicitly and provide employee credentials:

```bash
PATH="/tmp/k6-v0.49.0-linux-amd64:$PATH" \
BASE_URL=http://127.0.0.1:5051 \
QA_K6_ENABLE_AUTH=1 \
CYPRESS_EMPLOYEE_EMAIL='...' \
CYPRESS_EMPLOYEE_PASSWORD='...' \
K6_PROFILE=smoke \
./scripts/testing/run_k6.sh
```

Run the spike profile:

```bash
PATH="/tmp/k6-v0.49.0-linux-amd64:$PATH" \
BASE_URL=http://127.0.0.1:5051 \
K6_PROFILE=spike \
K6_SPIKE_VUS=80 \
K6_SPIKE_RAMP_UP=5s \
K6_SPIKE_HOLD=10s \
K6_SPIKE_RAMP_DOWN=5s \
./scripts/testing/run_k6.sh
```

Run the soak profile:

```bash
PATH="/tmp/k6-v0.49.0-linux-amd64:$PATH" \
BASE_URL=http://127.0.0.1:5051 \
K6_PROFILE=soak \
K6_SOAK_VUS=25 \
K6_SOAK_DURATION=30s \
./scripts/testing/run_k6.sh
```

Profile defaults:

- `smoke`: `K6_VUS=20`, `K6_DURATION=15s`
- `spike`: `K6_SPIKE_VUS=80`, `K6_SPIKE_RAMP_UP=10s`, `K6_SPIKE_HOLD=20s`, `K6_SPIKE_RAMP_DOWN=10s`
- `soak`: `K6_SOAK_VUS=25`, `K6_SOAK_DURATION=10m`
- `load`: original duži ramping-arrival-rate scenario

The default thresholds target:

- `p95 < 800ms`
- `p99 < 1500ms`
- `< 1%` HTTP failures

## Observability

Optional runtime observability bootstrap now lives in [observability.py](/home/aleksandarlukovic/MuseumInfoSystem/observability.py).

Supported env vars:

- `SENTRY_DSN`
- `SENTRY_ENVIRONMENT`
- `SENTRY_TRACES_SAMPLE_RATE`
- `SENTRY_SEND_DEFAULT_PII`
- `OTEL_ENABLED`
- `OTEL_SERVICE_NAME`
- `OTEL_EXPORTER_OTLP_ENDPOINT`

Behavior:

- Sentry is enabled only when `SENTRY_DSN` is set.
- OpenTelemetry is enabled only when `OTEL_ENABLED=true` or an OTLP endpoint is present.
- Both integrations fail open: if packages are missing or startup fails, the app logs a warning and continues booting.

## Notes

- The local QA server is run over HTTP with `SESSION_COOKIE_SECURE=False`; that is intentional for Cypress.
- `qa:wrapper` defaults to Flask mode for quick local development.
- `qa:wrapper:gunicorn` runs the full wrapper in Gunicorn mode and enables the k6 smoke check.
- The new `data-testid` hooks are intentionally limited to critical production-readiness flows so UI automation is less brittle.
- `qa:all` assumes the local app is already running via `npm run qa:server`.
- `qa:wrapper` / `./run_qa.sh` starts the local server itself unless one is already reachable at `CYPRESS_BASE_URL`.
- The admin suite seeds deterministic timesheet state in PostgreSQL and creates real archive requests during the run.

## GitHub Actions

The workflow is in [qa.yml](/home/aleksandarlukovic/MuseumInfoSystem/.github/workflows/qa.yml).

- `python-qa` always runs on GitHub-hosted runners.
- `qa-lint` validates Cypress, Playwright, config, and k6 JS assets.
- `full-local-qa` runs only if the repository has the required QA secrets for the PostgreSQL-backed local test environment.
- `zap-baseline` runs only if `QA_STAGING_URL` is configured as a repository secret.

Required secrets for the full browser/admin job:

- `QA_DATABASE_URL`
- `QA_ADMIN_EMAIL`
- `QA_ADMIN_PASSWORD`
- `QA_EMPLOYEE_EMAIL`
- `QA_EMPLOYEE_PASSWORD`
- `QA_FIRST_LOGIN_EMAIL`
- `QA_FIRST_LOGIN_PASSWORD`
- `QA_RESET_TARGET_EMAIL`
- `QA_ARCHIVE_EMAIL`
- `QA_ARCHIVE_PASSWORD`

Optional but recommended:

- `QA_SECRET_KEY`
- `QA_STAGING_URL`
