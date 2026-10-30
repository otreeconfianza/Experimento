// Prueba del controlador real de la barra con un DOM mínimo, sin navegador.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname, '../BarraCreencia.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
function create() {
    const events = {};
    const button = {disabled: false};
    const form = {
        querySelectorAll: () => [button],
        addEventListener: (name, callback) => { events[name] = callback; }
    };
    const range = {value: '50', closest: () => form, focus() {},
        addEventListener: (name, callback) => { events[name] = callback; }};
    const hidden = {value: ''};
    const output = {textContent: ''};
    const elements = {barraCreencia: range, respuestaCreencia: hidden, valorBarra: output};
    vm.runInNewContext(script, {document: {readyState: 'complete', getElementById: id => elements[id]}});
    return {range, hidden, output, button, events};
}
const untouched = create();
assert.equal(untouched.button.disabled, true);
let prevented = false;
untouched.events.submit({preventDefault() { prevented = true; }});
assert.equal(prevented, true);
untouched.events.input(); // Un evento sin cambiar la posición no cuenta como movimiento.
assert.equal(untouched.hidden.value, '');
assert.equal(untouched.button.disabled, true);
for (const value of ['0', '100', '51']) {
    const state = create();
    state.range.value = value;
    state.events.input();
    assert.equal(state.hidden.value, value);
    assert.equal(state.button.disabled, false);
    state.events.submit({preventDefault() { throw new Error('Respuesta válida bloqueada'); }});
    state.range.value = '50';
    state.events.input();
    assert.equal(state.hidden.value, '50');
    assert.equal(state.button.disabled, false);
}
console.log('Barra: movimiento obligatorio, envío bloqueado, extremos y retorno a 50% OK');
