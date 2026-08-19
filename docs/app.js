/* cybersec-iq — command center runtime.
 *
 * Static and client-side only: no network calls, no eval, no innerHTML, no
 * cookies, no analytics. Console output is built with createElement +
 * textContent, so it can never be interpreted as markup.
 *
 * The session panel deliberately reports only things the browser actually
 * knows — clock, timezone, viewport. A static page cannot measure CPU, RAM,
 * bandwidth or uptime, so those are not displayed at all rather than faked.
 */
(function () {
  'use strict';

  var REDUCED = window.matchMedia &&
                window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------- session panel (real browser facts) ---------------- */

  function pad2(n) { return (n < 10 ? '0' : '') + n; }

  function clock() {
    var el = document.getElementById('s-time');
    if (!el) { return; }
    var d = new Date();
    el.textContent = pad2(d.getHours()) + ':' + pad2(d.getMinutes()) + ':' + pad2(d.getSeconds());
  }

  function session() {
    var tz = document.getElementById('s-tz');
    if (tz) {
      var zone = '—';
      try {
        zone = Intl.DateTimeFormat().resolvedOptions().timeZone || '—';
      } catch (e) { /* older engines */ }
      var offset = -new Date().getTimezoneOffset() / 60;
      var sign = offset >= 0 ? '+' : '';
      tz.textContent = zone + ' (UTC' + sign + offset + ')';
    }
    var vw = document.getElementById('s-vw');
    if (vw) {
      vw.textContent = window.innerWidth + ' × ' + window.innerHeight;
    }
  }

  clock();
  session();
  window.setInterval(clock, 1000);
  window.addEventListener('resize', session);

  /* ---------------- scrollspy navigation ---------------- */

  var links = Array.prototype.slice.call(document.querySelectorAll('.nav__link'));
  var sections = links
    .map(function (a) { return document.querySelector(a.getAttribute('href')); })
    .filter(Boolean);

  function mark(id) {
    links.forEach(function (a) {
      var on = a.getAttribute('href') === '#' + id;
      if (on) { a.setAttribute('aria-current', 'true'); }
      else { a.removeAttribute('aria-current'); }
    });
  }

  if ('IntersectionObserver' in window && sections.length) {
    var visible = Object.create(null);
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        visible[e.target.id] = e.isIntersecting ? e.intersectionRatio : 0;
      });
      var bestId = null, best = 0;
      Object.keys(visible).forEach(function (id) {
        if (visible[id] > best) { best = visible[id]; bestId = id; }
      });
      if (bestId) { mark(bestId); }
    }, { rootMargin: '-15% 0px -55% 0px', threshold: [0, 0.25, 0.5, 0.75, 1] });
    sections.forEach(function (s) { io.observe(s); });
  } else {
    mark('whoami');
  }

  /* ---------------- identity terminal typewriter ---------------- */

  var whoTyped = document.getElementById('who-typed');
  var whoResult = document.getElementById('who-result');
  var WHO_SEQUENCE = [
    { command: 'whoami', result: '→ ARYAN IQ' },
    { command: 'mission --status', result: '→ NOTHING IS IMPOSSIBLE.' }
  ];

  function typeWho(text, done) {
    if (!whoTyped) { return; }
    if (REDUCED) {
      whoTyped.textContent = text;
      if (done) { done(); }
      return;
    }
    whoTyped.textContent = '';
    var i = 0;
    function step() {
      i += 1;
      whoTyped.textContent = text.slice(0, i);
      if (i < text.length) { window.setTimeout(step, 82); }
      else if (done) { done(); }
    }
    window.setTimeout(step, 180);
  }

  function playWho(index) {
    if (!whoTyped || !whoResult) { return; }
    var item = WHO_SEQUENCE[index];
    whoResult.textContent = '';
    typeWho(item.command, function () {
      window.setTimeout(function () {
        whoResult.textContent = item.result;
        window.setTimeout(function () {
          playWho((index + 1) % WHO_SEQUENCE.length);
        }, index === WHO_SEQUENCE.length - 1 ? 2800 : 1500);
      }, 520);
    });
  }

  if (whoTyped && whoResult) {
    if (REDUCED) {
      whoTyped.textContent = WHO_SEQUENCE[0].command;
      whoResult.textContent = WHO_SEQUENCE[0].result;
    } else {
      playWho(0);
    }
  }

  /* ---------------- console ---------------- */

  var log = document.getElementById('log');
  var form = document.getElementById('form');
  var cmd = document.getElementById('cmd');
  if (!log || !form || !cmd) { return; }

  var history = [];
  var cursor = 0;

  function line(txt, variant) {
    var p = document.createElement('p');
    p.className = 'term__line' + (variant ? ' term__line--' + variant : '');
    p.textContent = txt === undefined ? '' : String(txt);
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
    website: { url: 'https://aryaniq.com', label: 'aryaniq.com' },
    source:  { url: 'https://github.com/cybersec-iq/cybersec-iq', label: 'cybersec-iq/cybersec-iq' }
  };

  function linkLine(prefix, key) {
    var t = LINKS[key];
    if (!t) { return; }
    var p = document.createElement('p');
    p.className = 'term__line';
    p.appendChild(document.createTextNode(prefix + ' '));
    var a = document.createElement('a');
    a.href = t.url;
    a.textContent = t.label;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    p.appendChild(a);
    log.appendChild(p);
  }

  function scroll() { log.scrollTop = log.scrollHeight; }

  function goto(id) {
    var el = document.getElementById(id);
    if (!el) { return; }
    el.scrollIntoView({ behavior: REDUCED ? 'auto' : 'smooth', block: 'start' });
    mark(id);
  }

  var COMMANDS = {
    help: function () {
      line('AVAILABLE COMMANDS', 'key');
      line('');
      pair('help', 'this list');
      pair('whoami', 'operator identity');
      pair('about', 'operating principles');
      pair('stack', 'technology stack');
      pair('projects', 'selected systems');
      pair('activity', 'public github activity');
      pair('snake', 'launch SNAKE PROTOCOL');
      pair('contact', 'contact details');
      pair('github', 'github profile link');
      pair('website', 'primary site link');
      pair('clear', 'reset console');
    },
    whoami: function () {
      line('ARYAN IQ', 'ok');
      line('Full-Stack Developer / Cybersecurity / AI Systems Builder', 'dim');
      line('');
      pair('LOCATION', 'MUSCAT, OMAN');
      pair('STATUS', 'BUILDING');
      pair('MISSION', 'NOTHING IS IMPOSSIBLE');
      goto('whoami');
    },
    about: function () {
      line('OPERATING PRINCIPLES', 'key');
      line('');
      pair('1', 'Security first');
      pair('2', 'Automate the repeatable');
      pair('3', 'Boring infrastructure, interesting products');
      pair('4', 'Own the whole path');
      pair('5', 'Ship, measure, harden');
      goto('about');
    },
    stack: function () {
      line('TECHNOLOGY STACK', 'key');
      line('');
      pair('FRONTEND', 'React, Next.js, TypeScript, JavaScript');
      pair('BACKEND', 'Node.js, Python, REST APIs');
      pair('DATA', 'PostgreSQL');
      pair('INFRA', 'Docker, Linux, Git, GitHub Actions');
      pair('SECURITY', 'Secure SDLC, threat modelling, hardening');
      goto('stack');
    },
    projects: function () {
      line('SELECTED SYSTEMS', 'key');
      line('');
      pair('ARYANIQ', 'personal platform + engineering hub  [LIVE]');
      pair('KAMINO', 'music label platform                 [PRIVATE]');
      pair('SHINEL', 'multilingual commerce platform       [PRIVATE]');
      pair('XPRIME', 'product platform                     [PRIVATE]');
      pair('XOS', 'internal system                      [UNDISCLOSED]');
      pair('XADMIN', 'internal system                      [UNDISCLOSED]');
      line('');
      line('Source for private systems is not published.', 'dim');
      goto('projects');
    },
    activity: function () {
      line('PUBLIC GITHUB ACTIVITY', 'key');
      line('Figures are regenerated daily by GitHub Actions', 'dim');
      line('from the live API. Public activity only.', 'dim');
      goto('activity');
    },
    contact: function () {
      line('CONTACT', 'key');
      line('');
      pair('WEBSITE', 'aryaniq.com');
      pair('GITHUB', '@cybersec-iq');
      pair('LOCATION', 'Muscat, Oman');
      goto('contact');
    },
    snake: function () {
      line('LAUNCHING SNAKE PROTOCOL ...', 'hi');
      window.setTimeout(function () { window.location.assign('./snake/'); }, 420);
    },
    github: function () { linkLine('->', 'github'); },
    website: function () { linkLine('->', 'website'); },
    clear: function () { while (log.firstChild) { log.removeChild(log.firstChild); } }
  };

  var ALIASES = {
    '?': 'help', 'ls': 'projects', 'who': 'whoami', 'tech': 'stack',
    'skills': 'stack', 'work': 'projects', 'stats': 'activity',
    'home': 'website', 'cls': 'clear', 'play': 'snake'
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
    else { window.setTimeout(function () { boot(i + 1); }, 150); }
  }
  boot(0);

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = cmd.value;
    if (v.trim() !== '') {
      history.push(v);
      if (history.length > 50) { history.shift(); }
    }
    cursor = history.length;
    run(v);
    cmd.value = '';
  });

  cmd.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowUp') {
      if (cursor > 0) { cursor -= 1; cmd.value = history[cursor]; }
      e.preventDefault();
    } else if (e.key === 'ArrowDown') {
      if (cursor < history.length - 1) { cursor += 1; cmd.value = history[cursor]; }
      else { cursor = history.length; cmd.value = ''; }
      e.preventDefault();
    }
  });

  /* "/" focuses the console from anywhere, the way a search box would. */
  window.addEventListener('keydown', function (e) {
    if (e.key !== '/' || e.ctrlKey || e.metaKey || e.altKey) { return; }
    var t = e.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA')) { return; }
    e.preventDefault();
    cmd.focus();
  });

  log.addEventListener('click', function (e) {
    if (e.target && e.target.closest && e.target.closest('a')) { return; }
    if (window.getSelection && String(window.getSelection()) !== '') { return; }
    cmd.focus();
  });
})();
