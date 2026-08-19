"""~/whoami — compact terminal identity module.

The composition follows 02_WHOAMI_ABOUT_REFERENCE.png: visible terminal
chrome, a two-line shell prompt, left-aligned identity output, restrained
facts and a thin bottom divider. The supplementary HUD reference contributes
only the secondary rotating globe.
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


def wide():
    W, H = 1200, 510
    px, py, pw, ph = 22, 42, W - 44, 420
    chrome_h = 46
    left_x, split_x = px + 42, 830

    o = D.text(px + 2, 28, '~/whoami', size=17, fill=D.CYAN, weight='600', tracking=.4)
    o += D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4, sw=1.2)
    o += _chrome(px, py, pw, chrome_h)
    o += D.hline(px, py + chrome_h, pw, D.LINE_3, 1)
    o += D.brackets(px, py, pw, ph, color=D.GREEN, arm=17, sw=1.6,
                    corners='bl,br', opacity=.62)

    # Reference-faithful two-line shell prompt.
    ps = 15
    o += D.text(left_x, 126, '╭─(cybersec-iq ◉ github)-[ ~/profile ]',
                size=ps, fill=D.GREEN, weight='600', tracking=.15)
    o += D.text(left_x, 151, '╰─$', size=ps, fill=D.GREEN, weight='600')
    o += D.text(left_x + 48, 151, 'whoami', size=ps, fill=D.TEXT_HI, weight='600')

    # Identity output: compact, crisp and left aligned.
    nx, ny, ns = left_x, 230, 66
    o += D.text(nx, ny, 'ARYAN', size=ns, fill=D.GREEN, weight='700',
                tracking=3.2, filt='glowMd')
    ix = nx + D.tw('ARYAN', ns, 3.2) + 24
    o += D.text(ix, ny, 'IQ', size=ns, fill=D.GREEN_HI, weight='700',
                tracking=3.2, filt='glowMd')
    o += D.text(left_x, 266, DISCIPLINES, size=14.5, fill=D.TEXT,
                tracking=1.45, preserve=True)
    o += D.rule(left_x, 286, 500, h=1.5)

    for i, (_, key, val, col) in enumerate(ROWS):
        ry = 326 + i * 39
        o += D.text(left_x, ry, key, size=15.5, fill=D.CYAN, tracking=2.1)
        o += D.text(left_x + 124, ry, ':', size=15.5, fill=D.FAINT)
        o += D.text(left_x + 151, ry, val, size=15.5, fill=col,
                    weight='600', tracking=1.15)
        if key == 'STATUS':
            o += D.status_dot(left_x + 151 + D.tw(val, 15.5, 1.15) + 17,
                              ry - 5, D.YELLOW, 4)

    # Secondary network globe occupies 30% and never competes with identity.
    o += D.vline(split_x, 112, 306, D.LINE, 1)
    o += D.globe(1001, 257, 126, D.GREEN_DIM, .78)
    o += D.text(1001, 397, 'MUSCAT, OMAN', size=11.5, fill=D.CYAN,
                tracking=1.8, anchor='middle')
    o += D.label(1001, 421, 'NETWORK ORIGIN', size=9.5, fill=D.MUTED,
                 tracking=2.2, anchor='middle')
    o += _bottom_divider(px + 42, 482, pw - 84)
    return D.doc(W, H, TITLE, DESC, o)


def narrow():
    W, H = 440, 610
    px, py, pw, ph = 10, 34, W - 20, 534
    cx = px + 18

    o = D.text(px + 1, 23, '~/whoami', size=13.5, fill=D.CYAN,
               weight='600', tracking=.3)
    o += D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
    o += _chrome(px, py, pw, h=40, compact=True)
    o += D.hline(px, py + 40, pw, D.LINE_3, 1)
    o += D.text(cx, 103, '╭─(cybersec-iq ◉ github)-[ ~/profile ]',
                size=11.4, fill=D.GREEN, weight='600')
    o += D.text(cx, 126, '╰─$', size=12, fill=D.GREEN, weight='600')
    o += D.text(cx + 38, 126, 'whoami', size=12, fill=D.TEXT_HI, weight='600')

    nx, ny, ns = cx, 188, 42
    o += D.text(nx, ny, 'ARYAN', size=ns, fill=D.GREEN, weight='700',
                tracking=1.8, filt='glowMd')
    ix = nx + D.tw('ARYAN', ns, 1.8) + 14
    o += D.text(ix, ny, 'IQ', size=ns, fill=D.GREEN_HI, weight='700',
                tracking=1.8, filt='glowMd')
    o += D.text(cx, 216, 'FULL-STACK DEVELOPER / CYBERSECURITY',
                size=10.7, fill=D.TEXT, tracking=.45)
    o += D.text(cx, 234, '/ AI SYSTEMS BUILDER', size=10.7,
                fill=D.TEXT, tracking=.45)
    o += D.rule(cx, 250, 220, h=1.3)

    for i, (_, key, val, col) in enumerate(ROWS):
        ry = 286 + i * 34
        o += D.text(cx, ry, key, size=11.8, fill=D.CYAN, tracking=1.3)
        o += D.text(cx + 90, ry, ':', size=11.8, fill=D.FAINT)
        o += D.text(cx + 108, ry, val, size=11.8, fill=col,
                    weight='600', tracking=.45)
        if key == 'STATUS':
            o += D.status_dot(cx + 108 + D.tw(val, 11.8, .45) + 13,
                              ry - 4, D.YELLOW, 3.5)

    o += D.hline(cx, 375, pw - 36, D.LINE, 1)
    o += D.globe(W / 2, 455, 64, D.GREEN_DIM, .75)
    o += D.text(W / 2, 541, 'MUSCAT, OMAN', size=10.5, fill=D.CYAN,
                tracking=1.4, anchor='middle')
    o += _bottom_divider(cx, 589, pw - 36)
    return D.doc(W, H, TITLE, DESC, o)
