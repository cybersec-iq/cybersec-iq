/* Deterministic test suite for docs/snake/game.js
   Stubs the DOM surface the game touches and drives requestAnimationFrame by
   hand, so every tick is reproducible.

   Run:  node tests/snake.test.js */
'use strict';
const fs = require('fs');
const vm = require('vm');

const GAME = process.argv[2] ||
  require('path').join(__dirname, '..', 'docs', 'snake', 'game.js');

function makeCtx() {
  const noop = () => {};
  return {
    fillStyle: '', strokeStyle: '', lineWidth: 0,
    shadowColor: '', shadowBlur: 0, globalAlpha: 1,
    fillRect: noop, beginPath: noop, moveTo: noop, lineTo: noop,
    stroke: noop, save: noop, restore: noop, translate: noop,
    rotate: noop, roundRect: noop, fill: noop
  };
}

function el(id) {
  return {
    id, textContent: '', hidden: false, tagName: 'DIV',
    attrs: {}, listeners: {}, clientWidth: 660,
    setAttribute(k, v) { this.attrs[k] = v; },
    getAttribute(k) { return this.attrs[k]; },
    addEventListener(t, fn) { (this.listeners[t] = this.listeners[t] || []).push(fn); },
    getBoundingClientRect() { return { width: 660, height: 660 }; }
  };
}

function build(opts) {
  opts = opts || {};
  const nodes = {};
  ['canvas', 'board', 'overlay', 'ov-k', 'ov-t', 'ov-d', 'ov-btn',
   'score', 'high', 'length', 'status', 'live', 'btn-toggle', 'btn-restart']
    .forEach(id => { nodes[id] = el(id); });

  const ctx = makeCtx();
  nodes.canvas.width = 0;
  nodes.canvas.height = 0;
  nodes.canvas.getContext = () => ctx;

  const pads = ['up', 'left', 'down', 'right'].map(d => {
    const b = el('pad-' + d);
    b.tagName = 'BUTTON';
    b.getAttribute = k => (k === 'data-dir' ? d : undefined);
    return b;
  });

  const store = Object.assign({}, opts.store || {});
  const winListeners = {};
  const docListeners = {};
  const rafQueue = [];
  let randomQueue = [];

  const win = {
    devicePixelRatio: 1,
    localStorage: {
      getItem: k => (k in store ? store[k] : null),
      setItem: (k, v) => { store[k] = String(v); }
    },
    matchMedia: () => ({ matches: false }),
    requestAnimationFrame: fn => { rafQueue.push(fn); return rafQueue.length; },
    addEventListener: (t, fn) => { (winListeners[t] = winListeners[t] || []).push(fn); },
    ResizeObserver: null,
    location: { assign() {} }
  };
  win.setTimeout = fn => { fn(); return 0; };

  const doc = {
    hidden: false,
    getElementById: id => nodes[id] || null,
    querySelectorAll: () => pads,
    addEventListener: (t, fn) => { (docListeners[t] = docListeners[t] || []).push(fn); },
    createElement: () => el('tmp')
  };

  const sandbox = {
    window: win, document: doc, console,
    Math: Object.create(Math),
    Date, parseInt, parseFloat, isFinite, String, Object, Array, Number
  };
  sandbox.Math.random = () => (randomQueue.length ? randomQueue.shift() : 0);
  sandbox.globalThis = sandbox;
  sandbox.setTimeout = win.setTimeout;

  vm.createContext(sandbox);
  vm.runInContext(fs.readFileSync(GAME, 'utf8'), sandbox, { filename: 'game.js' });

  let clock = 0;
  function tickFrames(count, msPerFrame) {
    for (let i = 0; i < count; i++) {
      const fns = rafQueue.splice(0, rafQueue.length);
      clock += msPerFrame;
      fns.forEach(fn => fn(clock));
    }
  }

  function key(k) {
    (winListeners.keydown || []).forEach(fn =>
      fn({ key: k, target: { tagName: 'BODY' }, preventDefault() {} }));
  }

  function snap() {
    return {
      score: nodes.score.textContent,
      high: nodes.high.textContent,
      len: nodes.length.textContent,
      status: nodes.status.textContent,
      overlayHidden: nodes.overlay.hidden,
      ovK: nodes['ov-k'].textContent,
      ovT: nodes['ov-t'].textContent,
      toggle: nodes['btn-toggle'].textContent,
      canvas: nodes.canvas.width,
      live: nodes.live.textContent
    };
  }

  return {
    snap, key, tickFrames, nodes, store,
    setHidden: v => { doc.hidden = v; },
    setRandom: q => { randomQueue = q.slice(); },
    // The first animation frame only establishes the time base and never
    // advances the game. begin() consumes it: afterwards, 1 frame == 1 step.
    begin() { key(' '); tickFrames(1, 138); },
    click: id => (nodes[id].listeners.click || []).forEach(fn => fn({ preventDefault() {} })),
    pad: (dir, type) => {
      const b = pads.find(p => p.getAttribute('data-dir') === dir);
      (b.listeners[type] || []).forEach(fn => fn({ preventDefault() {} }));
    },
    boardEvent: (type, ev) => (nodes.board.listeners[type] || []).forEach(fn => fn(ev)),
    docEvent: type => (docListeners[type] || []).forEach(fn => fn())
  };
}

/* ------------------------------------------------------------------ */

let pass = 0, fail = 0;
function check(name, actual, expected) {
  if (JSON.stringify(actual) === JSON.stringify(expected)) {
    pass++; console.log('  PASS  ' + name);
  } else {
    fail++;
    console.log('  FAIL  ' + name);
    console.log('        expected ' + JSON.stringify(expected));
    console.log('        actual   ' + JSON.stringify(actual));
  }
}

const TICK = 138;                      // BASE_MS
const KEY = 'cybersec-iq.snake.high';

console.log('');
console.log('== 1. boot state ==');
{
  const g = build();
  const s = g.snap();
  check('status READY', s.status, 'READY');
  check('score 0000', s.score, '0000');
  check('length 003', s.len, '003');
  check('overlay visible', s.overlayHidden, false);
  check('overlay copy', s.ovT, 'READY TO EXECUTE');
  check('toggle label', s.toggle, 'START');
  check('canvas sized to board x dpr', s.canvas, 660);
}

console.log('');
console.log('== 2. start, movement, boundary collision ==');
{
  const g = build();
  g.setRandom([0]);                    // food parks at (0,0), clear of the path
  g.begin();
  check('status ACTIVE', g.snap().status, 'ACTIVE');
  check('overlay hidden', g.snap().overlayHidden, true);

  g.tickFrames(10, TICK);              // head (10,10) -> (20,10)
  check('alive on the last legal column', g.snap().status, 'ACTIVE');
  g.tickFrames(1, TICK);               // -> (21,10), off the board
  check('dies leaving the right edge', g.snap().status, 'FAILED');
  check('reason', g.snap().ovK, 'BOUNDARY BREACH');
  check('overlay shown', g.snap().overlayHidden, false);
  check('game over copy', g.snap().ovT, 'GAME OVER');
  check('announced to screen readers', /Game over/.test(g.snap().live), true);
}

console.log('');
console.log('== 3. eating: score, growth, high score ==');
{
  const g = build();
  // Aim the first food at (11,10), directly ahead: row-major 221, minus the
  // 3 occupied cells = free index 218 of 438.
  g.setRandom([218 / 438, 0, 0, 0, 0]);
  g.begin();
  g.tickFrames(1, TICK);
  check('score +10', g.snap().score, '0010');
  check('length 004', g.snap().len, '004');
  check('high score tracks', g.snap().high, '0010');
  check('persisted to localStorage', g.store[KEY], '10');
}

console.log('');
console.log('== 4. reversal is rejected ==');
{
  const g = build();
  g.setRandom([0]);
  g.begin();
  g.key('ArrowLeft');                  // 180 degree flip while heading right
  g.tickFrames(10, TICK);
  check('still alive (turn ignored)', g.snap().status, 'ACTIVE');
  g.tickFrames(1, TICK);
  check('kept heading right into the wall', g.snap().ovK, 'BOUNDARY BREACH');
}

console.log('');
console.log('== 5. steering: arrows and WASD ==');
{
  const g = build();
  g.setRandom([0]);
  g.begin();
  g.key('ArrowDown');
  g.tickFrames(10, TICK);              // row 10 -> row 20
  check('arrow: alive on the last legal row', g.snap().status, 'ACTIVE');
  g.tickFrames(1, TICK);
  check('arrow: dies leaving the bottom edge', g.snap().ovK, 'BOUNDARY BREACH');

  const h = build();
  h.setRandom([0]);
  h.begin();
  h.key('w');
  h.tickFrames(10, TICK);              // row 10 -> row 0
  check('WASD: alive on the top row', h.snap().status, 'ACTIVE');
  h.tickFrames(1, TICK);
  check('WASD: dies leaving the top edge', h.snap().ovK, 'BOUNDARY BREACH');
}

console.log('');
console.log('== 6. pause and resume ==');
{
  const g = build();
  g.setRandom([0]);
  g.begin();
  g.tickFrames(3, TICK);
  g.key('p');
  check('paused', g.snap().status, 'PAUSED');
  check('overlay shown', g.snap().overlayHidden, false);
  check('resume label', g.snap().toggle, 'RESUME');
  g.tickFrames(40, TICK);              // a long freeze must not advance the run
  check('still paused after 40 frames', g.snap().status, 'PAUSED');
  g.key('p');
  g.tickFrames(1, TICK);               // resume re-primes the clock
  check('resumed', g.snap().status, 'ACTIVE');
  g.tickFrames(6, TICK);
  check('alive after resume', g.snap().status, 'ACTIVE');
}

console.log('');
console.log('== 7. restart ==');
{
  const g = build();
  g.setRandom([218 / 438, 0, 0, 0]);
  g.begin();
  g.tickFrames(1, TICK);
  check('scored before restart', g.snap().score, '0010');
  g.key('r');
  check('score reset', g.snap().score, '0000');
  check('length reset', g.snap().len, '003');
  check('high score retained', g.snap().high, '0010');
  check('running after restart', g.snap().status, 'ACTIVE');
}

console.log('');
console.log('== 8. self collision ==');
{
  const g = build();
  const idx = (x, y, occupied) => (y * 21 + x - occupied) / (441 - occupied);
  g.setRandom([idx(11, 10, 3), idx(12, 10, 4), idx(13, 10, 5), 0, 0, 0]);
  g.begin();
  g.tickFrames(3, TICK);
  check('length 006 after 3 feeds', g.snap().len, '006');
  check('score 0030', g.snap().score, '0030');

  // head (13,10), body trailing west. Curl back onto it.
  g.key('ArrowDown'); g.tickFrames(1, TICK);   // (13,11)
  g.key('ArrowLeft'); g.tickFrames(1, TICK);   // (12,11)
  check('alive mid-turn', g.snap().status, 'ACTIVE');
  g.key('ArrowUp');   g.tickFrames(1, TICK);   // (12,10) is body
  check('self collision detected', g.snap().status, 'FAILED');
  check('reason', g.snap().ovK, 'SELF COLLISION');
}

console.log('');
console.log('== 9. touch: d-pad, swipe, tap ==');
{
  const g = build();
  g.setRandom([0]);
  g.begin();
  g.pad('down', 'pointerdown');
  g.tickFrames(10, TICK);
  check('d-pad steered south', g.snap().status, 'ACTIVE');
  g.tickFrames(1, TICK);
  check('d-pad path ends at the bottom edge', g.snap().ovK, 'BOUNDARY BREACH');

  const h = build();
  h.setRandom([0]);
  h.begin();
  h.boardEvent('pointerdown', { clientX: 100, clientY: 100 });
  h.boardEvent('pointerup',   { clientX: 100, clientY: 180 });   // swipe down
  h.tickFrames(10, TICK);
  check('swipe steered south', h.snap().status, 'ACTIVE');
  h.tickFrames(1, TICK);
  check('swipe path ends at the bottom edge', h.snap().ovK, 'BOUNDARY BREACH');

  const t = build();
  t.setRandom([0]);
  check('idle before tap', t.snap().status, 'READY');
  t.boardEvent('pointerdown', { clientX: 50, clientY: 50 });
  t.boardEvent('pointerup',   { clientX: 52, clientY: 51 });     // tap, not swipe
  check('tap starts the run', t.snap().status, 'ACTIVE');
  t.boardEvent('pointerdown', { clientX: 50, clientY: 50 });
  t.boardEvent('pointerup',   { clientX: 51, clientY: 50 });
  check('tap does not pause a live run', t.snap().status, 'ACTIVE');
}

console.log('');
console.log('== 10. buttons and auto-pause when the tab hides ==');
{
  const g = build();
  g.setRandom([0]);
  g.click('btn-toggle');
  check('START button starts', g.snap().status, 'ACTIVE');
  g.click('btn-toggle');
  check('PAUSE button pauses', g.snap().status, 'PAUSED');
  g.click('ov-btn');
  check('overlay button resumes', g.snap().status, 'ACTIVE');
  g.click('btn-restart');
  check('RESTART button restarts', g.snap().status, 'ACTIVE');

  g.setHidden(true);
  g.docEvent('visibilitychange');
  check('auto-pause when hidden', g.snap().status, 'PAUSED');
  g.setHidden(false);
  g.docEvent('visibilitychange');
  check('does not auto-resume when shown', g.snap().status, 'PAUSED');
}

console.log('');
console.log('== 11. a backgrounded tab does not teleport the snake ==');
{
  const g = build();
  g.setRandom([0]);
  g.begin();
  // One frame carrying 30 seconds. Without the catch-up clamp this would run
  // ~217 steps at once and cross the board many times over.
  g.tickFrames(1, 30000);
  check('survives a 30s frame delta', g.snap().status, 'ACTIVE');
}

console.log('');
console.log('== 12. localStorage handling ==');
{
  check('corrupt value falls back to 0',
        build({ store: { [KEY]: 'not-a-number' } }).snap().high, '0000');
  check('negative value falls back to 0',
        build({ store: { [KEY]: '-5' } }).snap().high, '0000');
  check('valid value is restored',
        build({ store: { [KEY]: '420' } }).snap().high, '0420');
}

console.log('');
console.log('----------------------------------------');
console.log('  ' + pass + ' passed, ' + fail + ' failed');
console.log('----------------------------------------');
console.log('');
process.exit(fail === 0 ? 0 : 1);
