// CSRF обнова (static/js/csrf_obnova.js + глобални secureFetch из base.html).
//
// Прод лог 23.11.2026: „The CSRF token has expired“ — страница отворена дуже
// од рока токена пада при упису. Сервер на AJAX сада враћа 400
// {error:'csrf_expired', csrf_token}; омотач window.fetch освежи meta,
// скривена поља и CSRF_TOKEN и понови захтев ЈЕДНОМ са новим токеном.
// Харнес у правом Chromium-у, сервер глуми page.route.

const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const KOREN = path.resolve(__dirname, '../..');
const OBNOVA = fs.readFileSync(path.join(KOREN, 'static/js/csrf_obnova.js'), 'utf8');
const BASE = fs.readFileSync(path.join(KOREN, 'templates/base.html'), 'utf8');
const i = BASE.indexOf('let CSRF_TOKEN');
const j = BASE.indexOf('// HTML escaping', i);
const GLOBALNO = BASE.slice(i, j).replace(/\{\{[^}]*\}\}/g, "''");
const ORIGIN = 'https://mis.test';
const STARI = 'stari-token';
const NOVI = 'novi-token';

function strana() {
  return `<!doctype html><html><head><meta charset="utf-8">
<meta name="csrf-token" content="${STARI}">
<script>${OBNOVA}</script></head><body>
<form><input type="hidden" name="csrf_token" value="${STARI}"></form>
<script>${GLOBALNO}</script></body></html>`;
}

async function pripremi(page, { uvekIstekao = false } = {}) {
  const pozivi = [];
  await page.route(`${ORIGIN}/**`, async (route) => {
    const req = route.request();
    if (req.method() === 'GET') {
      return route.fulfill({ contentType: 'text/html', body: strana() });
    }
    const token = req.headers()['x-csrftoken'];
    const telo = req.postData() || '';
    pozivi.push({ url: req.url(), token, telo });
    if (uvekIstekao || token !== NOVI) {
      return route.fulfill({ status: 400, contentType: 'application/json',
        body: JSON.stringify({ ok: false, error: 'csrf_expired', csrf_token: NOVI }) });
    }
    return route.fulfill({ contentType: 'application/json', body: JSON.stringify({ ok: true }) });
  });
  await page.goto(`${ORIGIN}/udzbenik`);
  return pozivi;
}

test('secureFetch: istekao token → osveži i ponovi jednom, upis prolazi', async ({ page }) => {
  const pozivi = await pripremi(page);
  const rez = await page.evaluate(async () => {
    const r = await secureFetch('/api/udzbenik/napredak', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ a: 1 }),
    });
    return {
      status: r.status, telo: await r.json(), globalno: CSRF_TOKEN,
      meta: document.querySelector('meta[name="csrf-token"]').content,
      polje: document.querySelector('input[name="csrf_token"]').value,
    };
  });
  expect(rez).toEqual({ status: 200, telo: { ok: true }, globalno: NOVI, meta: NOVI, polje: NOVI });
  expect(pozivi.map((p) => p.token)).toEqual([STARI, NOVI]);
  expect(pozivi[1].telo).toBe('{"a":1}');
});

test('sirovi fetch sa FormData: token i u telu zamenjen', async ({ page }) => {
  const pozivi = await pripremi(page);
  const status = await page.evaluate(async () => {
    const fd = new FormData();
    fd.append('csrf_token', 'stari-token');
    fd.append('x', '1');
    const r = await fetch('/forma', { method: 'POST', headers: { 'X-CSRFToken': 'stari-token' }, body: fd });
    return r.status;
  });
  expect(status).toBe(200);
  expect(pozivi).toHaveLength(2);
  expect(pozivi[1].telo).toContain('novi-token');
  expect(pozivi[1].telo).not.toContain('stari-token');
});

test('posle obnove sledeći zahtev odmah ide sa novim tokenom', async ({ page }) => {
  const pozivi = await pripremi(page);
  await page.evaluate(async () => {
    await secureFetch('/a', { method: 'POST', body: '1' });
    await secureFetch('/b', { method: 'POST', body: '2' });
  });
  expect(pozivi.map((p) => [new URL(p.url).pathname, p.token])).toEqual([
    ['/a', STARI], ['/a', NOVI], ['/b', NOVI],
  ]);
});

test('ponavlja samo jednom — nema petlje', async ({ page }) => {
  const pozivi = await pripremi(page, { uvekIstekao: true });
  const status = await page.evaluate(async () => (await secureFetch('/x', { method: 'POST', body: '1' })).status);
  expect(status).toBe(400);
  expect(pozivi).toHaveLength(2);
});
