// Client-side tests for the gallery download modal in
// static/js/fototeka_galerija.js. Uses only Node's standard library and a
// minimal DOM fixture.

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const GALLERY_JS = path.resolve(__dirname, '../../static/js/fototeka_galerija.js');
const SOURCE = fs.readFileSync(GALLERY_JS, 'utf8');

function makeEl(props) {
    const listeners = {};
    const set = new Set();
    const el = {
        hidden: false, checked: false, indeterminate: false,
        value: '', textContent: '', innerHTML: '',
        dataset: {},
        classList: {
            toggle(c, on) { if (on === undefined) { on = !set.has(c); } if (on) { set.add(c); } else { set.delete(c); } return on; },
            add(c) { set.add(c); }, remove(c) { set.delete(c); }, contains(c) { return set.has(c); },
        },
        addEventListener(type, fn) { (listeners[type] = listeners[type] || []).push(fn); },
        dispatch(type, ev) { (listeners[type] || []).forEach((fn) => fn(ev || { target: el })); },
        closest() { return el._closest || null; },
        querySelector(sel) { return el._qs ? el._qs(sel) : null; },
        querySelectorAll(sel) { return el._qsa ? el._qsa(sel) : []; },
        submit() { el._submitted = true; },
    };
    return Object.assign(el, props);
}

function buildScene(bytesList) {
    const boxes = bytesList.map((b) => {
        const item = makeEl({});
        const cb = makeEl({ checked: false });
        cb.dataset.bytes = String(b);
        cb._closest = item;
        return cb;
    });
    const rjpg = makeEl({ checked: true, value: 'jpg' });
    const rorig = makeEl({ checked: false, value: 'original' });
    const radios = [rjpg, rorig];

    const modal = makeEl({
        hidden: true,  // starts hidden, like the template
        _qs(sel) { return sel.indexOf(':checked') !== -1 ? radios.find((r) => r.checked) || null : null; },
        _qsa() { return radios; },
    });
    const form = makeEl({
        _qsa(sel) { return sel === 'input[name=ids]' ? boxes : []; },
    });
    form.dataset.zipMaxBytes = String(2 * 1024 * 1024 * 1024); // 2 GB
    form.dataset.zipMaxCount = '300';

    const els = {
        fototekaZipForm: form,
        fototekaSelectAll: makeEl({}),
        fototekaSelCount: makeEl({}),
        fototekaSloj: makeEl({ value: 'jpg' }),
        fototekaDownloadOpen: makeEl({}),
        fototekaDownloadModal: modal,
        fototekaModalCount: makeEl({}),
        fototekaModalSize: makeEl({}),
        fototekaModalWarn: makeEl({ hidden: true }),
        fototekaModalCancel: makeEl({}),
        fototekaModalConfirm: makeEl({}),
    };

    let domReady;
    const document = {
        addEventListener(type, fn) { if (type === 'DOMContentLoaded') { domReady = fn; } },
        getElementById(id) { return els[id] || null; },
        querySelectorAll() { return []; },  // no view buttons
    };
    const sandbox = {
        Array, Math, parseInt,
        document,
        window: { alert() {}, localStorage: { getItem() { return null; }, setItem() {} } },
    };
    vm.runInNewContext(SOURCE, sandbox, { filename: GALLERY_JS });
    domReady();
    return { els, form, boxes, radios, modal };
}

test('modal shows count and total size of the selected originals', () => {
    const s = buildScene([1000, 3 * 1024 * 1024 * 1024]);  // ~3 GB total
    s.boxes.forEach((b) => { b.checked = true; });
    s.els.fototekaDownloadOpen.dispatch('click');

    assert.equal(s.els.fototekaDownloadModal.hidden, false);
    assert.equal(s.els.fototekaModalCount.textContent, '2');
    assert.match(s.els.fototekaModalSize.textContent, /GB/);
});

test('originals over the byte limit raise a warning; jpg does not', () => {
    const s = buildScene([3 * 1024 * 1024 * 1024]);  // 3 GB > 2 GB cap
    s.boxes[0].checked = true;
    s.els.fototekaDownloadOpen.dispatch('click');
    // default choice is jpg -> no size warning
    assert.equal(s.els.fototekaModalWarn.hidden, true);

    // switch to originals -> warning appears
    s.radios[0].checked = false;
    s.radios[1].checked = true;
    s.radios[1].dispatch('change');
    assert.equal(s.els.fototekaModalWarn.hidden, false);
    assert.match(s.els.fototekaModalWarn.innerHTML, /скраћена/);
});

test('confirm copies the chosen layer into the hidden input and submits', () => {
    const s = buildScene([1000]);
    s.boxes[0].checked = true;
    s.els.fototekaDownloadOpen.dispatch('click');
    s.radios[0].checked = false;
    s.radios[1].checked = true;  // original
    s.els.fototekaModalConfirm.dispatch('click');

    assert.equal(s.els.fototekaSloj.value, 'original');
    assert.equal(s.form._submitted, true);
});

test('opening with nothing selected does not open the modal', () => {
    const s = buildScene([1000]);
    // no box checked
    s.els.fototekaDownloadOpen.dispatch('click');
    assert.equal(s.els.fototekaDownloadModal.hidden, true);
});
