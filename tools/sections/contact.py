"""Contact tiles.

Reference: 05_PLAY_SNAKE_CONTACT_REFERENCE.png — GET IN TOUCH lockup and four
accent-coded contact tiles with corner brackets.

Only verified destinations appear. No social account is invented: the profile
has no verified LinkedIn, X or Instagram URL, so none is shown.

Layout rule: a tile's height is derived from its wrapped copy, never assumed.
The narrow variant previously drew the description from a fixed offset taller
than the card itself, so every description rendered below its own border.
"""

import design as D

# (icon, accent, title, value, description)
TILES = [
    (D.i_globe,  D.CYAN,   'WEBSITE',   'aryaniq.com',
     'Portfolio, services and current work.'),
    (D.i_github, D.GREEN,  'GITHUB',    '@cybersec-iq',
     'Code, tooling and open builds.'),
    (D.i_pin,    D.YELLOW, 'LOCATION',  'Muscat, Oman',
     'Building globally, shipping locally.'),
    (D.i_mail,   D.BLUE,   'ENQUIRIES', 'via aryaniq.com',
     'Project, role or collaboration.'),
]

DESC = ('Contact and connect. Get in touch. Website aryaniq.com. '
        'GitHub at cybersec-iq. Location Muscat, Oman. Enquiries via aryaniq.com.')
TITLE = 'contact - get in touch'


def _tile_lines(body, w, size, pad):
    return D.wrap(body, D.fit_chars(w - pad * 2, size))


def _tile(x, y, w, icon, col, title, value, body,
          icon_px=30, title_px=14, value_px=13, body_px=11.5,
          pad=12, lh=16, show_body=True, fixed_h=None):
    """Centred tile laid out top-down. Returns (svg, height).

    The height is derived from the wrapped copy, with 20px clear below the last
    line. `fixed_h` lets a caller equalise a row after measuring every tile.
    """
    lines = _tile_lines(body, w, body_px, pad) if show_body else []

    y_icon = y + 20
    y_title = y_icon + icon_px + 22
    y_value = y_title + 22
    y_body = y_value + 22
    need = (y_body + max(0, len(lines) - 1) * lh) - y + 20   # 20px below last line
    h = fixed_h if fixed_h else need

    o = D.panel(x, y, w, h, fill=D.SURFACE_2, stroke=col, sw=1.3)
    o += D.brackets(x, y, w, h, color=col, arm=12, sw=1.6,
                    corners='tl,tr,bl,br', opacity=0.55)

    mid = x + w / 2
    o += icon(mid - icon_px / 2, y_icon, icon_px, col)
    o += D.text(mid, y_title, title, size=title_px, fill=col, weight='700',
                tracking=2.4, anchor='middle')
    o += D.text(mid, y_value, value, size=value_px, fill=D.TEXT_HI,
                tracking=0.4, anchor='middle')
    for i, ln in enumerate(lines):
        o += D.text(mid, y_body + i * lh, ln, size=body_px, fill=D.MUTED,
                    anchor='middle')
    return o, h


def _lockup(x, y, size, gap_icon):
    """GET IN TOUCH as one flowed text so the two colours cannot drift apart."""
    return D.rich(x + gap_icon, y,
                  [('GET IN ', D.GREEN), ('TOUCH', D.CYAN)],
                  size=size, tracking=1.6,
                  weight_for=lambda c: '700')


def wide():
    W, H = 1200, 300
    px, py, pw, ph = 22, 20, W - 44, 260

    o = D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
    o += D.brackets(px, py, pw, ph, color=D.YELLOW, arm=20, sw=2.2, corners='tl,tr')

    cx = px + 42
    o += D.label(cx, py + 44, '// CONTACT & CONNECT', size=13.5, fill=D.CYAN, tracking=3.6)
    o += D.i_mail(cx, py + 62, 40, D.GREEN)
    o += _lockup(cx, py + 100, 38, 56)
    o += D.text(cx, py + 140, 'Have a project, an idea, or just want to connect?',
                size=14, fill=D.TEXT, tracking=0.3)
    o += D.text(cx, py + 162, "Let's build something that holds up.",
                size=14, fill=D.MUTED, tracking=0.3)

    tx = px + 500
    tw_ = pw - 500 - 42
    gap = 14
    cw = (tw_ - gap * 3) / 4

    # measure every tile, then draw them all at the tallest so the row is even
    tall = max(_tile(0, 0, cw, ic, col, t, v, b)[1] for ic, col, t, v, b in TILES)
    for i, (ic, col, t, v, b) in enumerate(TILES):
        o += _tile(tx + i * (cw + gap), py + 34, cw, ic, col, t, v, b, fixed_h=tall)[0]

    return D.doc(W, max(H, py + 34 + tall + 24), TITLE, DESC, o)


def narrow():
    W = 440
    px, py, pw = 10, 20, W - 20
    cx = px + 18
    inner = pw - 36

    o = D.label(cx, py + 30, '// CONTACT & CONNECT', size=11.5, fill=D.CYAN, tracking=2.6)
    o += D.i_mail(cx, py + 42, 28, D.GREEN)
    o += _lockup(cx, py + 68, 26, 40)
    o += D.text(cx, py + 94, 'Have a project or an idea?', size=12.5, fill=D.TEXT)

    gy = py + 110
    gap = 10
    cw = (inner - gap) / 2

    # Measure every tile first, then lay them all out at the tallest height so
    # the grid stays even and nothing is clipped.
    measured = [_tile(0, 0, cw, ic, col, t, v, b,
                      icon_px=26, title_px=12.5, value_px=11.5, body_px=10,
                      pad=10, lh=14)[1]
                for ic, col, t, v, b in TILES]
    ch = max(measured)

    for i, (ic, col, t, v, b) in enumerate(TILES):
        c, r = i % 2, i // 2
        svg, _ = _tile(cx + c * (cw + gap), gy + r * (ch + gap), cw, ic, col, t, v, b,
                       icon_px=26, title_px=12.5, value_px=11.5, body_px=10,
                       pad=10, lh=14, fixed_h=ch)
        o += svg

    ph = gy + 2 * (ch + gap) + 4 - py
    H = py + ph + 12
    frame = (D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
             + D.brackets(px, py, pw, ph, color=D.YELLOW, arm=15, sw=2, corners='tl,tr'))
    return D.doc(W, H, TITLE, DESC, frame + o)
