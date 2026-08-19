"""~/whoami — compact terminal identity module.

The composition follows 02_WHOAMI_ABOUT_REFERENCE.png: visible terminal
chrome, a two-line Linux prompt, left-aligned identity output, restrained
facts and a thin bottom divider. There is deliberately no competing dashboard
illustration.
"""

import design as D

USER = 'cybersec-iq@github'
ROWS = [
    (D.i_pin,    'LOCATION', 'MUSCAT, OMAN',          D.TEXT_HI),
    (D.i_pulse,  'STATUS',   'BUILDING',              D.YELLOW),
    (D.i_target, 'MISSION',  'NOTHING IS IMPOSSIBLE', D.GREEN),
]
DISCIPLINES = 'FULL-STACK DEVELOPER  /  CYBERSECURITY  /  AI SYSTEMS BUILDER'

DESC = ('Terminal identity panel. Prompt cybersec-iq at github, tilde profile, '
        'command whoami. Output ARYAN IQ. Full-stack developer, cybersecurity, '
        'AI systems builder. Location Muscat, Oman. Status building. '
        'Mission nothing is impossible.')
TITLE = 'whoami - Aryan IQ'


def _chrome(x, y, w, h=44, compact=False):
    """macOS/Linux-style terminal chrome required by the reference."""
    o = D.panel(x, y, w, h, fill=D.SURFACE_3, stroke=D.LINE_2, rx=3, sw=1.1)
    r, gap = ((4.2, 14) if compact else (5.2, 17))
    sx = x + (18 if compact else 22)
    cy = y + h / 2
    for i, col in enumerate(('#FF5F57', '#FEBC2E', '#28C840')):
        o += f'    <circle cx="{sx + i * gap}" cy="{cy}" r="{r}" fill="{col}"/>\n'
    size = 10.5 if compact else 13
    title_x = sx + gap * 3 + (2 if compact else 8)
    o += D.text(title_x, cy + size * .34, 'bash — cybersec-iq — 96×24',
                size=size, fill=D.TEXT, tracking=.35)
    label = 'ONLINE'
    label_w = D.tw(label, size, 1.5)
    lx = x + w - label_w - (16 if compact else 22)
    o += D.status_dot(lx - (10 if compact else 13), cy, D.GREEN, 3.4 if compact else 4)
    o += D.text(lx, cy + size * .34, label, size=size, fill=D.GREEN,
                weight='600', tracking=1.5, filt='glowSm')
    return o


def _bottom_divider(x, y, w):
    mid = x + w / 2
    o = D.hline(x, y, w, D.LINE_2, 1)
    o += D.hline(x, y, w * .48, D.GREEN_DIM, 1)
    o += D.hline(mid + w * .02, y, w * .48, D.CYAN_DIM, 1)
    o += (f'    <rect x="{mid - 5}" y="{y - 5}" width="10" height="10" '
          f'transform="rotate(45 {mid} {y})" fill="{D.SURFACE}" '
          f'stroke="{D.YELLOW}" stroke-width="1.2"/>\n')
    return o


def _typewriter(x, y, command, size, clip_id, tracking=.1, duration=12):
    """SMIL typing reveal with a readable frozen-frame fallback.

    The first frame contains the complete command. If an image proxy freezes
    animation, the prompt therefore stays understandable. Live renderers then
    reset and reveal one character every ~96 ms before a long pause.
    """
    advance = size * D.ADV + tracking
    full = advance * len(command)
    key_times = [0, .01, .011, .08]
    key_times += [.08 + .008 * (i + 1) for i in range(len(command))]
    key_times += [.78, .96, 1]
    widths = [full, full, 0, 0]
    widths += [advance * (i + 1) for i in range(len(command))]
    widths += [full, full, full]
    xs = [x + value for value in widths]
    kt = ';'.join(f'{value:.3f}' for value in key_times)
    wv = ';'.join(f'{value:.1f}' for value in widths)
    xv = ';'.join(f'{value:.1f}' for value in xs)
    extra = f'''    <clipPath id="{clip_id}">
      <rect x="{x}" y="{y - size}" width="{full:.1f}" height="{size * 1.35:.1f}">
        <animate attributeName="width" values="{wv}" keyTimes="{kt}" dur="{duration}s" calcMode="discrete" repeatCount="indefinite"/>
      </rect>
    </clipPath>
'''
    body = D.text(x, y, command, size=size, fill=D.TEXT_HI, weight='600',
                  tracking=tracking, style=f'clip-path:url(#{clip_id})')
    body += (f'    <rect x="{x + full + 4:.1f}" y="{y - size + 2:.1f}" width="{max(5, size * .48):.1f}" '
             f'height="{size * 1.05:.1f}" fill="{D.GREEN}" class="blink" filter="url(#glowSm)">'
             f'<animate attributeName="x" values="{xv}" keyTimes="{kt}" dur="{duration}s" '
             f'calcMode="discrete" repeatCount="indefinite"/></rect>\n')
    return extra, body


def wide():
    # A narrower canvas keeps the text from occupying only the left third
    # after removing the competing illustration. GitHub still scales it to the
    # README width.
    W, H = 900, 412
    px, py, pw, ph = 22, 42, W - 44, 322
    chrome_h = 46
    left_x = px + 42
    typing_defs, typing = _typewriter(left_x + 48, 148, 'whoami', 15,
                                      'type-whoami-wide')

    o = D.text(px + 2, 28, '~/whoami', size=17, fill=D.CYAN, weight='600', tracking=.4)
    o += D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4, sw=1.2)
    o += _chrome(px, py, pw, chrome_h)
    o += D.hline(px, py + chrome_h, pw, D.LINE_3, 1)
    o += D.brackets(px, py, pw, ph, color=D.GREEN, arm=17, sw=1.6,
                    corners='bl,br', opacity=.62)

    # Reference-faithful two-line shell prompt.
    ps = 15
    o += D.text(left_x, 122, '╭─(cybersec-iq ◉ github)-[ ~/profile ]',
                size=ps, fill=D.GREEN, weight='600', tracking=.15)
    o += D.text(left_x, 148, '╰─$', size=ps, fill=D.GREEN, weight='600')
    o += typing

    # Identity output: compact, crisp and left aligned.
    nx, ny, ns = left_x, 202, 56
    o += D.text(nx, ny, 'ARYAN', size=ns, fill=D.GREEN, weight='700',
                tracking=3.2, filt='glowMd')
    ix = nx + D.tw('ARYAN', ns, 3.2) + 24
    o += D.text(ix, ny, 'IQ', size=ns, fill=D.GREEN_HI, weight='700',
                tracking=3.2, filt='glowMd')
    o += D.text(left_x, 236, DISCIPLINES, size=13.2, fill=D.TEXT,
                tracking=1.45, preserve=True)
    o += D.rule(left_x, 254, pw - 84, h=1.5)

    for i, (_, key, val, col) in enumerate(ROWS):
        ry = 287 + i * 31
        o += D.text(left_x, ry, key, size=15.5, fill=D.CYAN, tracking=2.1)
        o += D.text(left_x + 124, ry, ':', size=15.5, fill=D.FAINT)
        o += D.text(left_x + 151, ry, val, size=15.5, fill=col,
                    weight='600', tracking=1.15)
        if key == 'STATUS':
            o += D.status_dot(left_x + 151 + D.tw(val, 15.5, 1.15) + 17,
                              ry - 5, D.YELLOW, 4)

    o += _bottom_divider(px + 42, 390, pw - 84)
    return D.doc(W, H, TITLE, DESC, o, extra_defs=typing_defs)


def narrow():
    W, H = 440, 432
    px, py, pw, ph = 10, 34, W - 20, 364
    cx = px + 18
    typing_defs, typing = _typewriter(cx + 38, 140, 'whoami', 12,
                                      'type-whoami-narrow', duration=12)

    o = D.text(px + 1, 23, '~/whoami', size=13.5, fill=D.CYAN,
               weight='600', tracking=.3)
    o += D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
    o += _chrome(px, py, pw, h=40, compact=True)
    o += D.hline(px, py + 40, pw, D.LINE_3, 1)
    o += D.text(cx, 116, '╭─(cybersec-iq ◉ github)-[ ~/profile ]',
                size=11.4, fill=D.GREEN, weight='600')
    o += D.text(cx, 140, '╰─$', size=12, fill=D.GREEN, weight='600')
    o += typing

    nx, ny, ns = cx, 202, 40
    o += D.text(nx, ny, 'ARYAN', size=ns, fill=D.GREEN, weight='700',
                tracking=1.8, filt='glowMd')
    ix = nx + D.tw('ARYAN', ns, 1.8) + 14
    o += D.text(ix, ny, 'IQ', size=ns, fill=D.GREEN_HI, weight='700',
                tracking=1.8, filt='glowMd')
    o += D.text(cx, 230, 'FULL-STACK DEVELOPER / CYBERSECURITY',
                size=10.7, fill=D.TEXT, tracking=.45)
    o += D.text(cx, 248, '/ AI SYSTEMS BUILDER', size=10.7,
                fill=D.TEXT, tracking=.45)
    o += D.rule(cx, 266, 272, h=1.3)

    for i, (_, key, val, col) in enumerate(ROWS):
        ry = 300 + i * 32
        o += D.text(cx, ry, key, size=11.8, fill=D.CYAN, tracking=1.3)
        o += D.text(cx + 90, ry, ':', size=11.8, fill=D.FAINT)
        o += D.text(cx + 108, ry, val, size=11.8, fill=col,
                    weight='600', tracking=.45)
        if key == 'STATUS':
            o += D.status_dot(cx + 108 + D.tw(val, 11.8, .45) + 13,
                              ry - 4, D.YELLOW, 3.5)

    o += _bottom_divider(cx, 419, pw - 36)
    return D.doc(W, H, TITLE, DESC, o, extra_defs=typing_defs)
