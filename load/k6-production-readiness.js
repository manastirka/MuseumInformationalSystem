import http from 'k6/http';
import { check, sleep } from 'k6';

const EMPLOYEE_EMAIL = __ENV.CYPRESS_EMPLOYEE_EMAIL || __ENV.QA_K6_EMPLOYEE_EMAIL || '';
const EMPLOYEE_PASSWORD = __ENV.CYPRESS_EMPLOYEE_PASSWORD || __ENV.QA_K6_EMPLOYEE_PASSWORD || '';
const AUTH_FLOW_ENABLED = ['1', 'true', 'yes'].includes((__ENV.QA_K6_ENABLE_AUTH || '').toLowerCase());
let employeeSessionEstablished = false;

function standardThresholds() {
  return {
    checks: ['rate==1.0'],
    http_req_failed: ['rate==0'],
    http_req_duration: ['p(95)<800', 'p(99)<1500']
  };
}

function smokeOptions() {
  return {
    vus: Number(__ENV.QA_K6_SMOKE_VUS || __ENV.K6_VUS || 20),
    duration: __ENV.QA_K6_SMOKE_DURATION || __ENV.K6_DURATION || '15s',
    noCookiesReset: true,
    thresholds: standardThresholds()
  };
}

function spikeOptions() {
  return {
    scenarios: {
      spike_reads: {
        executor: 'ramping-vus',
        startVUs: 0,
        stages: [
          {
            duration: __ENV.QA_K6_SPIKE_RAMP_UP || __ENV.K6_SPIKE_RAMP_UP || '10s',
            target: Number(__ENV.QA_K6_SPIKE_VUS || __ENV.K6_SPIKE_VUS || 80)
          },
          {
            duration: __ENV.QA_K6_SPIKE_HOLD || __ENV.K6_SPIKE_HOLD || '20s',
            target: Number(__ENV.QA_K6_SPIKE_VUS || __ENV.K6_SPIKE_VUS || 80)
          },
          {
            duration: __ENV.QA_K6_SPIKE_RAMP_DOWN || __ENV.K6_SPIKE_RAMP_DOWN || '10s',
            target: 0
          }
        ],
        gracefulRampDown: '5s'
      }
    },
    noCookiesReset: true,
    thresholds: standardThresholds()
  };
}

function soakOptions() {
  return {
    scenarios: {
      soak_reads: {
        executor: 'constant-vus',
        vus: Number(__ENV.QA_K6_SOAK_VUS || __ENV.K6_SOAK_VUS || 25),
        duration: __ENV.QA_K6_SOAK_DURATION || __ENV.K6_SOAK_DURATION || '10m'
      }
    },
    noCookiesReset: true,
    thresholds: standardThresholds()
  };
}

function loadOptions() {
  return {
    scenarios: {
      dashboard_reads: {
        executor: 'ramping-arrival-rate',
        startRate: 20,
        timeUnit: '1s',
        preAllocatedVUs: 100,
        maxVUs: 1200,
        stages: [
          { target: 100, duration: '2m' },
          { target: 300, duration: '5m' },
          { target: 600, duration: '5m' },
          { target: 1000, duration: '3m' },
          { target: 0, duration: '2m' }
        ]
      }
    },
    noCookiesReset: true,
    thresholds: standardThresholds()
  };
}

const legacySmokeMode = __ENV.K6_SMOKE === '1';
const profile = (__ENV.QA_K6_PROFILE || __ENV.K6_PROFILE || (legacySmokeMode ? 'smoke' : 'load')).toLowerCase();

function selectOptions() {
  if (profile === 'smoke') {
    return smokeOptions();
  }
  if (profile === 'spike') {
    return spikeOptions();
  }
  if (profile === 'soak') {
    return soakOptions();
  }
  return loadOptions();
}

export const options = selectOptions();

const BASE_URL = __ENV.BASE_URL || 'https://127.0.0.1:5050';
http.setResponseCallback(http.expectedStatuses({ min: 200, max: 399 }, 401));

function extractCsrfToken(html) {
  const match = html.match(/name="csrf_token"\s+value="([^"]+)"/i);
  return match ? match[1] : '';
}

function hasEmployeeSession() {
  return employeeSessionEstablished;
}

function runAuthenticatedEmployeeFlow() {
  if (!AUTH_FLOW_ENABLED || !EMPLOYEE_EMAIL || !EMPLOYEE_PASSWORD) {
    return;
  }

  if (!hasEmployeeSession()) {
    const loginPage = http.get(`${BASE_URL}/login`, {
      tags: { name: `employee_login_page_${profile}` },
      timeout: '15s',
      responseCallback: http.expectedStatuses(200)
    });
    const csrfToken = extractCsrfToken(loginPage.body || '');
    const loginPayload = {
      email: EMPLOYEE_EMAIL,
      password: EMPLOYEE_PASSWORD
    };
    if (csrfToken) {
      loginPayload.csrf_token = csrfToken;
    }

    const loginResponse = http.post(
      `${BASE_URL}/login`,
      loginPayload,
      {
        tags: { name: `employee_login_submit_${profile}` },
        timeout: '15s',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        redirects: 0,
        responseCallback: http.expectedStatuses(302, 303)
      }
    );
    const loginOk = check(loginResponse, {
      'employee login submit ok': (r) =>
        [302, 303].includes(r.status) &&
        !String(r.headers.Location || '').includes('/login')
    });
    if (!loginOk) {
      employeeSessionEstablished = false;
      return;
    }
    employeeSessionEstablished = true;
  }

  const timesheetEntry = http.get(`${BASE_URL}/timesheet/entry`, {
    tags: { name: `employee_timesheet_entry_${profile}` },
    timeout: '15s',
    responseCallback: http.expectedStatuses(200)
  });
  const timesheetEntryOk = check(timesheetEntry, {
    'employee timesheet entry reachable': (r) =>
      r.status === 200 && /Радна листа|timesheet-save|Унос радне листе/i.test(r.body || '')
  });
  if (!timesheetEntryOk) {
    employeeSessionEstablished = false;
  }
}

export default function () {
  const loginPage = http.get(`${BASE_URL}/login`, {
    tags: { name: `login_page_${profile}` },
    timeout: '15s',
    responseCallback: http.expectedStatuses(200)
  });
  check(loginPage, { 'login page ok': (r) => r.status === 200 });

  const websiteNews = http.get(`${BASE_URL}/api/website-news`, {
    tags: { name: `website_news_${profile}` },
    timeout: '15s',
    responseCallback: http.expectedStatuses(200, 401)
  });
  check(websiteNews, { 'website news reachable': (r) => [200, 401].includes(r.status) });

  runAuthenticatedEmployeeFlow();

  sleep(1);
}
