// Client-side regression tests for static/js/fototeka_upload.js.
// Uses only Node's standard library and a minimal DOM fixture.

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const UPLOAD_JS = path.resolve(__dirname, '../../static/js/fototeka_upload.js');
const SOURCE = fs.readFileSync(UPLOAD_JS, 'utf8');

function makeElement() {
    return {
        children: [],
        className: '',
        innerHTML: '',
        textContent: '',
        style: {},
        appendChild(child) { this.children.push(child); },
    };
}

async function renderUploadResult(serverResult) {
    let domReadyHandler;
    let submitHandler;

    const fileInput = { files: [{ name: serverResult.ime || 'photo.jpg' }] };
    const csrfInput = { name: 'csrf_token', type: 'hidden', value: 'test-token' };
    const submitButton = { disabled: false };
    const form = {
        elements: [csrfInput],
        addEventListener(type, handler) {
            if (type === 'submit') { submitHandler = handler; }
        },
        querySelector(selector) {
            if (selector === 'input[type=file]') { return fileInput; }
            if (selector === '[name=csrf_token]') { return csrfInput; }
            if (selector === 'button[type=submit]') { return submitButton; }
            return null;
        },
    };
    const progress = { hidden: true };
    const bar = makeElement();
    const report = makeElement();
    const elements = {
        fototekaUploadForm: form,
        fototekaUploadProgress: progress,
        fototekaUploadBar: bar,
        fototekaUploadReport: report,
    };
    const document = {
        addEventListener(type, handler) {
            if (type === 'DOMContentLoaded') { domReadyHandler = handler; }
        },
        createElement: makeElement,
        getElementById(id) { return elements[id] || null; },
    };
    class FakeFormData {
        append() {}
    }
    const sandbox = {
        Array,
        FormData: FakeFormData,
        Promise,
        document,
        fetch: async () => ({ json: async () => serverResult }),
        window: { location: { href: '' } },
    };

    vm.runInNewContext(SOURCE, sandbox, { filename: UPLOAD_JS });
    domReadyHandler();
    submitHandler({ preventDefault() {} });
    await new Promise((resolve) => setImmediate(resolve));
    return report.children[0];
}

test('SHA duplicate gets a clear warning without leaking the existing ID', async () => {
    const row = await renderUploadResult({
        ok: false,
        ime: 'kopija.jpg',
        error: 'kopija.jpg: већ постоји (ID 742)',
    });

    assert.equal(row.className, 'small text-warning');
    assert.equal(
        row.textContent,
        '↺ kopija.jpg — фотографија са истим садржајем већ постоји у Фототеци; '
            + 'ова датотека није поново сачувана',
    );
    assert.doesNotMatch(row.textContent, /742|\bID\b/);
});

test('ordinary upload failure remains an error with the server message', async () => {
    const row = await renderUploadResult({
        ok: false,
        ime: 'virus.exe',
        error: 'тип датотеке није дозвољен',
    });

    assert.equal(row.className, 'small text-danger');
    assert.equal(row.textContent, '✗ virus.exe — тип датотеке није дозвољен');
});
