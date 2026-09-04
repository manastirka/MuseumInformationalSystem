// Тестови чистих функција из static/js/sortiranje_tabela.js (без DOM-а).
// Покретање: node --test tests/js

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const SOURCE = fs.readFileSync(
    path.resolve(__dirname, '../../static/js/sortiranje_tabela.js'), 'utf8');

function ucitaj() {
    const sandbox = { window: undefined, Intl, Date, Number, isFinite, String, Array, setTimeout };
    sandbox.globalThis = sandbox;
    vm.createContext(sandbox);
    vm.runInContext(SOURCE, sandbox);
    assert.ok(sandbox.MISSortiranje, 'MISSortiranje мора бити изложен и без document-а');
    return sandbox.MISSortiranje;
}

test('uBroj: српски и енглески запис, јединице, минус', () => {
    const { uBroj } = ucitaj();
    assert.equal(uBroj('1.234,56'), 1234.56);
    assert.equal(uBroj('1234.56'), 1234.56);
    assert.equal(uBroj('12'), 12);
    assert.equal(uBroj(' 3,5 kg '), 3.5);
    assert.equal(uBroj('45%'), 45);
    assert.equal(uBroj('-7'), -7);
    assert.equal(uBroj('−7'), -7);
    assert.equal(uBroj('2.017'), 2017);
    assert.equal(uBroj('MET-001'), null);
    assert.equal(uBroj('12.03.2024.'), null);
    assert.equal(uBroj(''), null);
});

test('uDatum: српски и ISO формат, неисправан датум је null', () => {
    const { uDatum } = ucitaj();
    assert.equal(uDatum('12.03.2024.'), Date.UTC(2024, 2, 12));
    assert.equal(uDatum('12.3.2024'), Date.UTC(2024, 2, 12));
    assert.equal(uDatum('2024-03-12'), Date.UTC(2024, 2, 12));
    assert.equal(uDatum('2024-03-12 14:05'), Date.UTC(2024, 2, 12, 14, 5));
    assert.equal(uDatum('31.02.2024.'), Date.UTC(2024, 1, 31)); // синтаксно исправан, не проверава календар
    assert.equal(uDatum('13.13.2024.'), null);
    assert.equal(uDatum('Београд'), null);
});

test('tipKolone: сви непразни бројеви → broj, датуми → datum, мешано → tekst', () => {
    const { tipKolone } = ucitaj();
    assert.equal(tipKolone(['12', '', '3,5', ' ']), 'broj');
    assert.equal(tipKolone(['12.03.2024.', '2024-01-01', '']), 'datum');
    assert.equal(tipKolone(['12', 'а']), 'tekst');
    assert.equal(tipKolone(['', '']), 'tekst');
});

test('redosled: бројеви нумерички, празно на крају у оба смера', () => {
    const { redosled } = ucitaj();
    const vred = ['10', '', '9', '100', '1.000'];
    assert.deepEqual(redosled(vred, 'asc').indeksi, [2, 0, 3, 4, 1]);
    assert.deepEqual(redosled(vred, 'desc').indeksi, [4, 3, 0, 2, 1]);
});

test('redosled: текст ћирилицом и латиницом, природни бројеви у тексту, стабилно', () => {
    const { redosled } = ucitaj();
    const vred = ['Кутија 10', 'Кутија 2', 'Ćup', 'ампула', 'Ампула'];
    const r = redosled(vred, 'asc');
    assert.equal(r.tip, 'tekst');
    // природни редослед: „Кутија 2“ пре „Кутија 10“; ампула/Ампула стабилно (3 пре 4)
    const sorted = r.indeksi.map((i) => vred[i]);
    assert.ok(sorted.indexOf('Кутија 2') < sorted.indexOf('Кутија 10'));
    assert.ok(sorted.indexOf('ампула') < sorted.indexOf('Ампула'));
});

test('redosled: датуми хронолошки', () => {
    const { redosled } = ucitaj();
    const vred = ['05.01.2025.', '2024-12-31', '01.02.2025.', ''];
    assert.deepEqual(redosled(vred, 'asc').indeksi, [1, 0, 2, 3]);
    assert.deepEqual(redosled(vred, 'desc').indeksi, [2, 0, 1, 3]);
});
