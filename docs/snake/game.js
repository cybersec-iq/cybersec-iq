/* cybersec-iq — SNAKE PROTOCOL
   Zero dependencies. Zero network calls. Zero tracking.
   High score is kept in localStorage on the visitor's own device only. */
(function () {
  'use strict';

  /* ---------------- configuration ---------------- */

  var GRID     = 21;    // cells per side
  var BASE_MS  = 138;   // starting tick interval
  var MIN_MS   = 68;    // fastest tick interval
  var RAMP_MS  = 4;     // interval shaved per food eaten
  var START_LEN = 3;
  var POINTS   = 10;
  var STORE_KEY = 'cybersec-iq.snake.high';

  var COLOR = {
    bg:     '#05070A',
    grid:   'rgba(27,39,51,0.55)',
    head:   '#C6FF00',
    body:   '#39FF14',
    tail:   '#00E5FF',
    food:   '#C6FF00',
    foodHi: '#FFD400'
  };

  /* ---------------- dom ---------------- */

  var canvas   = document.getElementById('canvas');
  var board    = document.getElementById('board');
  var overlay  = document.getElementById('overlay');
  var ovK      = document.getElementById('ov-k');
  var ovT      = document.getElementById('ov-t');
  var ovD      = document.getElementById('ov-d');
  var ovBtn    = document.getElementById('ov-btn');
  var elScore  = document.getElementById('score');
  var elHigh   = document.getElementById('high');
  var elLength = document.getElementById('length');
  var elStatus = document.getElementById('status');
  var elLive   = document.getElementById('live');
  var btnToggle  = document.getElementById('btn-toggle');
  var btnRestart = document.getElementById('btn-restart');

  if (!canvas || !canvas.getContext) { return; }
  var ctx = canvas.getContext('2d');

  var REDUCED = window.matchMedia &&
                window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------- state ---------------- */

  var snake, dir, queue, food, score, high, eaten, state, acc, last, raf;

  function loadHigh() {
    try {
      var raw = window.localStorage.getItem(STORE_KEY);
      var n = parseInt(raw, 10);
      return (isFinite(n) && n >= 0) ? n : 0;
    } catch (e) { return 0; }
  }

  function saveHigh(value) {
    try { window.localStorage.setItem(STORE_KEY, String(value)); } catch (e) { /* private mode */ }
  }

  function pad(n, width) {
    var s = String(Math.max(0, n | 0));
    while (s.length < width) { s = '0' + s; }
    return s;
  }

  /* ---------------- board sizing (crisp on any DPR) ---------------- */

  var cell = 0;

  function resize() {
    var rect = board.getBoundingClientRect();
    // The board is square by CSS (aspect-ratio: 1/1). If the height has not
    // resolved yet — aspect-ratio still pending, or an engine that does not
    // support it — fall back to the width rather than measuring zero and
    // leaving the board blank until the next animation frame.
    var css = rect.height > 0 ? Math.min(rect.width, rect.height) : rect.width;
    // Layout genuinely unavailable (hidden tab): skip. The polling check in
    // frame() picks it up as soon as the board has real geometry.
    if (!(css > 0)) { return; }

    var dpr = Math.min(window.devicePixelRatio || 1, 3);
    var px = Math.round(css * dpr);

    if (canvas.width !== px || canvas.height !== px) {
      canvas.width = px;
      canvas.height = px;
    }
    cell = px / GRID;
    draw();
  }

  /* ---------------- game setup ---------------- */

  function reset() {
    snake = [];
    var mid = Math.floor(GRID / 2);
    for (var i = 0; i < START_LEN; i++) {
      snake.push({ x: mid - i, y: mid });
    }
    dir = { x: 1, y: 0 };
    queue = [];
    score = 0;
    eaten = 0;
    acc = 0;
    last = 0;
    placeFood();
    syncHud();
  }

  function occupied(x, y) {
    for (var i = 0; i < snake.length; i++) {
      if (snake[i].x === x && snake[i].y === y) { return true; }
    }
    return false;
  }

  /* Choose uniformly from the free cells — always terminates, even when the
     board is nearly full. */
  function placeFood() {
    var free = [];
    for (var y = 0; y < GRID; y++) {
      for (var x = 0; x < GRID; x++) {
        if (!occupied(x, y)) { free.push(y * GRID + x); }
      }
    }
    if (free.length === 0) { food = null; return; }
    var pick = free[Math.floor(Math.random() * free.length)];
    food = { x: pick % GRID, y: Math.floor(pick / GRID) };
  }

  function interval() {
    return Math.max(MIN_MS, BASE_MS - eaten * RAMP_MS);
  }

  /* ---------------- direction input ---------------- */

  var VECTORS = {
    up:    { x: 0,  y: -1 },
    down:  { x: 0,  y: 1  },
    left:  { x: -1, y: 0  },
    right: { x: 1,  y: 0  }
  };

  function steer(name) {
    var v = VECTORS[name];
    if (!v) { return; }
    if (state === 'idle') { start(); }
    if (state !== 'running') { return; }

    // Compare against the last committed/queued heading so a fast double-tap
    // can never fold the snake back into itself.
    var ref = queue.length ? queue[queue.length - 1] : dir;
    if (v.x === -ref.x && v.y === -ref.y) { return; }
    if (v.x === ref.x && v.y === ref.y) { return; }
    if (queue.length < 2) { queue.push(v); }
  }

  /* ---------------- loop ---------------- */

  function step() {
    if (queue.length) { dir = queue.shift(); }

    var head = { x: snake[0].x + dir.x, y: snake[0].y + dir.y };

    if (head.x < 0 || head.y < 0 || head.x >= GRID || head.y >= GRID) {
      return gameOver('BOUNDARY BREACH');
    }

    // The tail cell frees up this tick unless we grow into it.
    var growing = !!(food && head.x === food.x && head.y === food.y);
    var limit = growing ? snake.length : snake.length - 1;
    for (var i = 0; i < limit; i++) {
      if (snake[i].x === head.x && snake[i].y === head.y) {
        return gameOver('SELF COLLISION');
      }
    }

    snake.unshift(head);

    if (growing) {
      score += POINTS;
      eaten += 1;
      if (score > high) { high = score; saveHigh(high); }
      placeFood();
      if (!food) { return win(); }
    } else {
      snake.pop();
    }

    syncHud();
  }

  var sizeCheck = 0;

  function frame(now) {
    raf = window.requestAnimationFrame(frame);

    // Cheap safety net: ResizeObserver can miss the first real layout when
    // the tab starts hidden, which would leave the board rendering blank.
    sizeCheck += 1;
    if (sizeCheck % 20 === 0) {
      var dpr = Math.min(window.devicePixelRatio || 1, 3);
      var want = Math.round(board.clientWidth * dpr);
      if (want > 0 && want !== canvas.width) { resize(); }
    }

    if (state !== 'running') { last = now; return; }
    if (!last) { last = now; }

    var delta = now - last;
    last = now;
    // A backgrounded tab can hand us a huge delta; clamp it so the snake
    // never teleports across the board on return.
    acc += Math.min(delta, 250);

    var tick = interval();
    while (acc >= tick && state === 'running') {
      acc -= tick;
      step();
      tick = interval();
    }
    draw();
  }

  /* ---------------- rendering ---------------- */

  function rect(x, y, w, h, r) {
    if (typeof ctx.roundRect === 'function') {
      ctx.beginPath();
      ctx.roundRect(x, y, w, h, r);
      ctx.fill();
    } else {
      ctx.fillRect(x, y, w, h);
    }
  }

  function draw() {
    var size = canvas.width;
    if (!size || !cell) { return; }

    ctx.fillStyle = COLOR.bg;
    ctx.fillRect(0, 0, size, size);

    // grid
    ctx.strokeStyle = COLOR.grid;
    ctx.lineWidth = Math.max(1, size / 900);
    ctx.beginPath();
    for (var g = 1; g < GRID; g++) {
      var p = Math.round(g * cell) + 0.5;
      ctx.moveTo(p, 0); ctx.lineTo(p, size);
      ctx.moveTo(0, p); ctx.lineTo(size, p);
    }
    ctx.stroke();

    if (!snake) { return; }

    // food
    if (food) {
      var fx = food.x * cell + cell / 2;
      var fy = food.y * cell + cell / 2;
      var beat = REDUCED ? 1 : (1 + 0.14 * Math.sin(Date.now() / 190));
      var fr = (cell * 0.30) * beat;

      ctx.save();
      ctx.translate(fx, fy);
      ctx.rotate(Math.PI / 4);
      ctx.shadowColor = COLOR.food;
      ctx.shadowBlur = cell * 0.9;
      ctx.fillStyle = COLOR.food;
      ctx.fillRect(-fr, -fr, fr * 2, fr * 2);
      ctx.shadowBlur = 0;
      ctx.fillStyle = COLOR.foodHi;
      ctx.fillRect(-fr * 0.34, -fr * 0.34, fr * 0.68, fr * 0.68);
      ctx.restore();
    }

    // snake — head lime, body neon, fading toward cyan at the tail
    var inset = Math.max(1, cell * 0.10);
    var side = cell - inset * 2;
    var radius = Math.max(1, cell * 0.16);

    for (var i = snake.length - 1; i >= 0; i--) {
      var seg = snake[i];
      var t = snake.length > 1 ? i / (snake.length - 1) : 0;

      if (i === 0) {
        ctx.fillStyle = COLOR.head;
        ctx.shadowColor = COLOR.head;
        ctx.shadowBlur = cell * 0.85;
      } else {
        ctx.fillStyle = mix(COLOR.body, COLOR.tail, Math.min(1, t * 1.15));
        ctx.shadowColor = COLOR.body;
        ctx.shadowBlur = cell * 0.28;
        ctx.globalAlpha = 0.92 - t * 0.28;
      }

      rect(seg.x * cell + inset, seg.y * cell + inset, side, side, radius);
      ctx.globalAlpha = 1;
      ctx.shadowBlur = 0;
    }
  }

  var mixCache = {};
  function mix(a, b, t) {
    var key = a + b + Math.round(t * 20);
    if (mixCache[key]) { return mixCache[key]; }
    var ca = [parseInt(a.substr(1, 2), 16), parseInt(a.substr(3, 2), 16), parseInt(a.substr(5, 2), 16)];
    var cb = [parseInt(b.substr(1, 2), 16), parseInt(b.substr(3, 2), 16), parseInt(b.substr(5, 2), 16)];
    var out = 'rgb(' +
      Math.round(ca[0] + (cb[0] - ca[0]) * t) + ',' +
      Math.round(ca[1] + (cb[1] - ca[1]) * t) + ',' +
      Math.round(ca[2] + (cb[2] - ca[2]) * t) + ')';
    mixCache[key] = out;
    return out;
  }

  /* ---------------- hud + state ---------------- */

  function syncHud() {
    elScore.textContent = pad(score, 4);
    elHigh.textContent = pad(high, 4);
    elLength.textContent = pad(snake ? snake.length : START_LEN, 3);
  }

  function announce(message) {
    if (elLive) { elLive.textContent = message; }
  }

  var OVERLAY = {
    idle: {
      k: 'SNAKE PROTOCOL',
      t: 'READY TO EXECUTE',
      d: 'Steer with arrow keys, W A S D, swipe, or the pad below.',
      btn: 'START',
      toggle: 'START'
    },
    paused: {
      k: 'SESSION HELD',
      t: 'PAUSED',
      d: 'Press Space or P to resume.',
      btn: 'RESUME',
      toggle: 'RESUME'
    }
  };

  function setState(next, reason) {
    state = next;

    elStatus.textContent =
      next === 'running' ? 'ACTIVE' :
      next === 'paused'  ? 'PAUSED' :
      next === 'over'    ? 'FAILED' : 'READY';
    elStatus.setAttribute('data-s', elStatus.textContent);

    if (next === 'running') {
      overlay.hidden = true;
      overlay.setAttribute('data-state', 'running');
      btnToggle.textContent = 'PAUSE';
      announce('Game running.');
      return;
    }

    overlay.hidden = false;
    overlay.setAttribute('data-state', next);

    if (next === 'over') {
      ovK.textContent = reason || 'RUN TERMINATED';
      ovT.textContent = 'GAME OVER';
      ovD.textContent = 'Score ' + pad(score, 4) + '  ·  Best ' + pad(high, 4) +
                        (score > 0 && score === high ? '  ·  New record.' : '');
      ovBtn.textContent = 'RUN AGAIN';
      btnToggle.textContent = 'START';
      announce('Game over. ' + reason + '. Final score ' + score + '. Best ' + high + '.');
      return;
    }

    var copy = OVERLAY[next] || OVERLAY.idle;
    ovK.textContent = copy.k;
    ovT.textContent = copy.t;
    ovD.textContent = copy.d;
    ovBtn.textContent = copy.btn;
    btnToggle.textContent = copy.toggle;
    announce(next === 'paused' ? 'Game paused.' : 'Ready. Press start.');
  }

  function start() {
    if (state === 'over' || state === 'idle') { reset(); }
    last = 0;
    acc = 0;
    setState('running');
  }

  function pause() {
    if (state !== 'running') { return; }
    setState('paused');
    draw();
  }

  function toggle() {
    if (state === 'running') { pause(); }
    else { start(); }
  }

  function restart() {
    reset();
    last = 0;
    acc = 0;
    setState('running');
    draw();
  }

  function gameOver(reason) {
    setState('over', reason);
    draw();
  }

  function win() {
    setState('over', 'BOARD SATURATED');
    draw();
  }

  /* ---------------- events ---------------- */

  var KEYS = {
    ArrowUp: 'up', ArrowDown: 'down', ArrowLeft: 'left', ArrowRight: 'right',
    w: 'up', a: 'left', s: 'down', d: 'right',
    W: 'up', A: 'left', S: 'down', D: 'right'
  };

  window.addEventListener('keydown', function (event) {
    if (event.ctrlKey || event.metaKey || event.altKey) { return; }

    var isButton = event.target && event.target.tagName === 'BUTTON';
    var move = KEYS[event.key];

    if (move) {
      event.preventDefault();   // arrows must not scroll the page mid-run
      steer(move);
      return;
    }

    if (event.key === ' ' || event.key === 'Spacebar') {
      if (isButton) { return; } // let Space activate a focused button
      event.preventDefault();
      toggle();
      return;
    }

    if (event.key === 'p' || event.key === 'P') { toggle(); return; }
    if (event.key === 'r' || event.key === 'R') { restart(); return; }
    if (event.key === 'Escape') { pause(); }
  });

  btnToggle.addEventListener('click', toggle);
  btnRestart.addEventListener('click', restart);
  ovBtn.addEventListener('click', function () { start(); });

  // Directional pad — pointerdown so held presses feel immediate on touch.
  var padButtons = document.querySelectorAll('.pad__b');
  for (var b = 0; b < padButtons.length; b++) {
    (function (button) {
      var name = button.getAttribute('data-dir');
      button.addEventListener('pointerdown', function (event) {
        event.preventDefault();
        steer(name);
      });
      // Keyboard activation of the pad button still works via click.
      button.addEventListener('click', function () { steer(name); });
    })(padButtons[b]);
  }

  // Swipe
  var swipe = null;
  var THRESHOLD = 22;

  board.addEventListener('pointerdown', function (event) {
    swipe = { x: event.clientX, y: event.clientY };
  });

  board.addEventListener('pointerup', function (event) {
    if (!swipe) { return; }
    var dx = event.clientX - swipe.x;
    var dy = event.clientY - swipe.y;
    swipe = null;

    if (Math.abs(dx) < THRESHOLD && Math.abs(dy) < THRESHOLD) {
      // A tap on the board starts or resumes, but never pauses a live run
      // (that would be too easy to trigger by accident).
      if (state !== 'running') { start(); }
      return;
    }
    if (Math.abs(dx) > Math.abs(dy)) { steer(dx > 0 ? 'right' : 'left'); }
    else { steer(dy > 0 ? 'down' : 'up'); }
  });

  board.addEventListener('pointercancel', function () { swipe = null; });

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) { pause(); }
  });
  window.addEventListener('blur', pause);

  if (window.ResizeObserver) {
    new window.ResizeObserver(resize).observe(board);
  } else {
    window.addEventListener('resize', resize);
  }
  window.addEventListener('orientationchange', function () {
    window.setTimeout(resize, 180);
  });

  /* ---------------- boot ---------------- */

  high = loadHigh();
  reset();
  setState('idle');
  resize();
  raf = window.requestAnimationFrame(frame);
})();
