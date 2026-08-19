/* cybersec-iq — interactive console
   Static, client-side only. No network calls, no eval, no innerHTML.
   Every node is built with createElement + textContent, so console output
   can never be interpreted as markup. */
(function () {
  'use strict';

  var log  = document.getElementById('log');
  var form = document.getElementById('form');
  var cmd  = document.getElementById('cmd');
  if (!log || !form || !cmd) { return; }

  var history = [];
  var cursor  = 0;

  var REDUCED = window.matchMedia &&
                window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- output primitives (XSS-safe by construction) ---------- */

  function line(text, variant) {
    var p = document.createElement('p');
    p.className = 'term__line' + (variant ? ' term__line--' + variant : '');
    p.textContent = text === undefined ? '' : String(text);
    log.appendChild(p);
    return p;
  }

  function pair(key, value) {
    var p = document.createElement('p');
    p.className = 'term__line';
    var k = document.createElement('span');
    k.className = 'term__line--key';
    k.textContent = (key + '            ').slice(0, 12);
    var v = document.createElement('span');
    v.textContent = ' ' + value;
    p.appendChild(k);
    p.appendChild(v);
    log.appendChild(p);
  }

  /* Anchors are only ever built from this hard-coded allowlist. */
  var LINKS = {
    github:  { url: 'https://github.com/cybersec-iq', label: 'github.com/cybersec-iq' },
    website: { url: 'https://aryaniq.com',            label: 'aryaniq.com' },
    source:  { url: 'https://github.com/cybersec-iq/cybersec-iq', label: 'github.com/cybersec-iq/cybersec-iq' }
  };

  function linkLine(prefix, key) {
    var target = LINKS[key];
    if (!target) { return; }
    var p = document.createElement('p');
    p.className = 'term__line';
    p.appendChild(document.createTextNode(prefix + ' '));
    var a = document.createElement('a');
    a.href = target.url;
    a.textContent = target.label;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    p.appendChild(a);
    log.appendChild(p);
  }

  function scroll() { log.scrollTop = log.scrollHeight; }

  /* ---------- commands ---------- */

  var COMMANDS = {
    help: function () {
      line('AVAILABLE COMMANDS', 'key');
      line('');
      pair('help',     'this list');
      pair('whoami',   'operator identity');
      pair('projects', 'selected systems');
      pair('stack',    'technology stack');
      pair('github',   'github profile link');
      pair('website',  'primary site link');
      pair('snake',    'launch SNAKE PROTOCOL');
      pair('clear',    'reset console');
    },

    whoami: function () {
      line('ARYAN IQ', 'ok');
      line('Full-Stack Developer / Cybersecurity / AI Systems Builder', 'dim');
      line('');
      pair('LOCATION', 'MUSCAT, OMAN');
      pair('STATUS',   'BUILDING');
      pair('MISSION',  'NOTHING IS IMPOSSIBLE');
    },

    projects: function () {
      line('SELECTED SYSTEMS', 'key');
      line('');
      pair('ARYANIQ',  'personal platform + engineering hub  [LIVE]');
      pair('KAMINO',   'music label platform, headless CMS   [PRIVATE]');
      pair('SHINEL',   'multilingual commerce platform       [PRIVATE]');
      pair('XPRIME',   'TypeScript product platform          [PRIVATE]');
      pair('XOS',      'internal system                      [UNDISCLOSED]');
      pair('XADMIN',   'internal control plane               [UNDISCLOSED]');
      line('');
      line('Source for private systems is not published.', 'dim');
    },

    stack: function () {
      line('TECHNOLOGY STACK', 'key');
      line('');
      pair('FRONTEND', 'React, Next.js, TypeScript');
      pair('BACKEND',  'Node.js, Python, REST APIs');
      pair('DATA',     'PostgreSQL');
      pair('INFRA',    'Docker, Linux, GitHub Actions, Git');
      pair('PRACTICE', 'secure SDLC, automation, threat modelling');
    },

    github:  function () { linkLine('->', 'github'); },
    website: function () { linkLine('->', 'website'); },

    snake: function () {
      line('LAUNCHING SNAKE PROTOCOL ...', 'hi');
      window.setTimeout(function () {
        window.location.assign('./snake/');
      }, 420);
    },

    clear: function () {
      while (log.firstChild) { log.removeChild(log.firstChild); }
    }
  };

  var ALIASES = {
    '?': 'help', 'ls': 'projects', 'who': 'whoami',
    'tech': 'stack', 'home': 'website', 'cls': 'clear', 'play': 'snake'
  };

  function run(raw) {
    var input = String(raw).trim();
    if (input === '') { return; }

    var echo = document.createElement('p');
    echo.className = 'term__line';
    var ps = document.createElement('span');
    ps.className = 'term__line--hi';
    ps.textContent = '> ';
    echo.appendChild(ps);
    var body = document.createElement('span');
    body.className = 'term__line--cmd';
    body.textContent = input;
    echo.appendChild(body);
    log.appendChild(echo);

    var name = input.toLowerCase().split(/\s+/)[0];
    name = ALIASES[name] || name;

    if (Object.prototype.hasOwnProperty.call(COMMANDS, name)) {
      COMMANDS[name]();
    } else {
      line('command not found: ' + input, 'err');
      line('type help for the command list', 'dim');
    }

    if (name !== 'clear') { line(''); }
    scroll();
  }

  /* ---------- boot ---------- */

  var BOOT = [
    ['cybersec-iq // command center', 'key'],
    ['initialising session ......... OK', 'dim'],
    ['loading operator profile ..... OK', 'dim'],
    ['integrity check .............. PASS', 'ok'],
    ['', null],
    ['Console ready. Type help to begin.', 'hi'],
    ['', null]
  ];

  function boot(i) {
    if (i >= BOOT.length) { return; }
    line(BOOT[i][0], BOOT[i][1]);
    scroll();
    if (REDUCED) { boot(i + 1); }
    else { window.setTimeout(function () { boot(i + 1); }, 160); }
  }
  boot(0);

  /* ---------- input ---------- */

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    var value = cmd.value;
    if (value.trim() !== '') {
      history.push(value);
      if (history.length > 50) { history.shift(); }
    }
    cursor = history.length;
    run(value);
    cmd.value = '';
  });

  cmd.addEventListener('keydown', function (event) {
    if (event.key === 'ArrowUp') {
      if (cursor > 0) { cursor -= 1; cmd.value = history[cursor]; }
      event.preventDefault();
    } else if (event.key === 'ArrowDown') {
      if (cursor < history.length - 1) { cursor += 1; cmd.value = history[cursor]; }
      else { cursor = history.length; cmd.value = ''; }
      event.preventDefault();
    }
  });

  /* Clicking the console body focuses the prompt — unless the user is
     selecting text or activating a link. */
  log.addEventListener('click', function (event) {
    if (event.target && event.target.closest && event.target.closest('a')) { return; }
    if (window.getSelection && String(window.getSelection()) !== '') { return; }
    cmd.focus();
  });
})();
