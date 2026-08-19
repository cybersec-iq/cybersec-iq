"""Contact tiles.

Reference: 05_PLAY_SNAKE_CONTACT_REFERENCE.png — GET IN TOUCH lockup and four
accent-coded contact tiles with corner brackets.

Only verified destinations appear. No social account is invented: the profile
has no verified LinkedIn, X or Instagram URL, so none is shown.
"""

import design as D

TILES = [
    (D.i_globe,  D.CYAN,   'WEBSITE',   'aryaniq.com',
     ['Portfolio, services', 'and current work.']),
    (D.i_github, D.GREEN,  'GITHUB',    '@cybersec-iq',
     ['Code, tooling and', 'open builds.']),
    (D.i_pin,    D.YELLOW, 'LOCATION',  'Muscat, Oman',
     ['Building globally,', 'shipping locally.']),
    (D.i_mail,   D.BLUE,   'ENQUIRIES', 'via aryaniq.com',
     ['Project, role or', 'collaboration.']),
]

DESC = ('Contact and connect. Get in touch. Website aryaniq.com. '
        'GitHub at cybersec-iq. Location Muscat, Oman. Enquiries via aryaniq.com.')
TITLE = 'contact - get in touch'


def _tile(x, y, w, h, icon, col, title, value, body, compact=False):
    o = D.panel(x, y, w, h, fill=D.SURFACE_2, stroke=col, sw=1.3)
    o += D.brackets(x, y, w, h, color=col, arm=12, sw=1.6,
                    corners='tl,tr,bl,br', opacity=0.55)
    cxm = x + w / 2
    o += icon(cxm - 15, y + 22, 30, col)
    twid = D.tw(title, 14, 2.4)
    o += D.text(cxm - twid / 2, y + 78, title, size=14, fill=col, weight='700', tracking=2.4)
    vwid = D.tw(value, 13, 0.4)
    o += D.text(cxm - vwid / 2, y + 102, value, size=13, fill=D.TEXT_HI, tracking=0.4)
    if not compact:
        for i, ln in enumerate(body):
            lw = D.tw(ln, 11.5, 0.2)
            o += D.text(cxm - lw / 2, y + 128 + i * 17, ln, size=11.5, fill=D.MUTED)
    return o


def wide():
    W, H = 1200, 300
    px, py, pw, ph = 22, 20, W - 44, 260

    o = D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
    o += D.brackets(px, py, pw, ph, color=D.YELLOW, arm=20, sw=2.2, corners='tl,tr')

    cx = px + 42
    o += D.label(cx, py + 44, '// CONTACT & CONNECT', size=13.5, fill=D.CYAN, tracking=3.6)
    o += D.i_mail(cx, py + 62, 40, D.GREEN)
    o += D.text(cx + 56, py + 100, 'GET IN', size=38, fill=D.GREEN, weight='700',
                tracking=2.4, filt='glowMd')
    o += D.text(cx + 56 + D.tw('GET IN', 38, 2.4) + 20, py + 100, 'TOUCH', size=38,
                fill=D.CYAN, weight='700', tracking=2.4, filt='glowMd')
    o += D.text(cx, py + 140, 'Have a project, an idea, or just want to connect?',
                size=14, fill=D.TEXT, tracking=0.3)
    o += D.text(cx, py + 162, "Let's build something that holds up.",
                size=14, fill=D.MUTED, tracking=0.3)

    tx = px + 500
    tw_ = pw - 500 - 42
    gap = 14
    cw = (tw_ - gap * 3) / 4
    for i, (icon, col, title, value, body) in enumerate(TILES):
        o += _tile(tx + i * (cw + gap), py + 34, cw, ph - 68, icon, col, title, value, body)
    return D.doc(W, H, TITLE, DESC, o)


def narrow():
    W = 440
    px, py, pw = 10, 20, W - 20
    cx = px + 18
    inner = pw - 36

    o = D.label(cx, py + 30, '// CONTACT & CONNECT', size=11.5, fill=D.CYAN, tracking=2.6)
    o += D.i_mail(cx, py + 42, 28, D.GREEN)
    o += D.text(cx + 40, py + 68, 'GET IN', size=26, fill=D.GREEN, weight='700',
                tracking=1.6, filt='glowMd')
    o += D.text(cx + 40 + D.tw('GET IN', 26, 1.6) + 14, py + 68, 'TOUCH', size=26,
                fill=D.CYAN, weight='700', tracking=1.6, filt='glowMd')
    o += D.text(cx, py + 94, 'Have a project or an idea?', size=12.5, fill=D.TEXT)

    gy = py + 110
    gap = 10
    cw = (inner - gap) / 2
    ch = 118
    for i, (icon, col, title, value, body) in enumerate(TILES):
        c, r = i % 2, i // 2
        o += _tile(cx + c * (cw + gap), gy + r * (ch + gap), cw, ch, icon, col, title, value, body)

    ph = gy + 2 * (ch + gap) + 6 - py
    H = py + ph + 12
    frame = (D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
             + D.brackets(px, py, pw, ph, color=D.YELLOW, arm=15, sw=2, corners='tl,tr'))
    return D.doc(W, H, TITLE, DESC, frame + o)
