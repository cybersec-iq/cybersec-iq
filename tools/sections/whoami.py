"""~/whoami — terminal identity module.

Reference: 02_WHOAMI_ABOUT_REFERENCE.png (prompt, name, ONLINE pill, the
LOCATION/STATUS/MISSION panel, wireframe globe) plus the tab device from the
supplementary HUD reference.

Deliberately NOT taken from the supplementary reference: the hooded-figure
avatar. The identity here is Aryan IQ and the shield mark, not an anonymous
hacker cliche.
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


def _online_pill(x, y, w=104, h=28):
    o = ('    <rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" '
         'stroke="%s" stroke-width="1.2" stroke-opacity="0.7"/>\n'
         % (x, y, w, h, D.SURFACE_2, D.GREEN))
    o += D.status_dot(x + 18, y + h / 2, D.GREEN, 4)
    o += D.text(x + 32, y + h / 2 + 4.5, 'ONLINE', size=12, fill=D.GREEN, tracking=2.2)
    return o


def wide():
    W, H = 1200, 520
    px, py, pw, ph = 22, 40, W - 44, 462

    o = D.tab(px + 26, py - 26, '~/whoami', color=D.CYAN, size=16)
    o += D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
    o += D.brackets(px, py, pw, ph, color=D.GREEN, arm=18, sw=2, corners='tl,br', opacity=0.75)

    cx = px + 46

    # wireframe globe, right side, clear of the copy
    o += D.globe(1000, 250, 116, D.GREEN_DIM, 0.75)
    o += ('    <rect x="932" y="384" width="136" height="26" rx="2" fill="%s" '
          'stroke="%s" stroke-width="1"/>\n' % (D.SURFACE_2, D.LINE_2))
    o += D.text(948, 402, 'MUSCAT, OMAN', size=11.5, fill=D.MUTED, tracking=1.8)

    # prompt line
    ps = 17
    o += D.text(cx, 92, USER, size=ps, fill=D.GREEN, weight='600')
    ux = cx + D.tw(USER, ps)
    o += D.text(ux, 92, ':~$', size=ps, fill=D.CYAN)
    o += D.text(ux + D.tw(':~$', ps) + 12, 92, 'whoami', size=ps, fill=D.TEXT_HI)
    o += _online_pill(px + pw - 150, 74)

    o += D.text(cx, 120, '>', size=ps, fill=D.GREEN_DIM)

    # name
    nx, ny, ns = cx, 200, 74
    o += D.text(nx, ny, 'ARYAN', size=ns, fill=D.GREEN, weight='700', tracking=5, filt='glowLg')
    ix = nx + D.tw('ARYAN', ns, 5) + 32
    o += D.text(ix, ny, 'IQ', size=ns, fill=D.CYAN, weight='700', tracking=5, filt='glowLg')
    o += D.caret(ix + D.tw('IQ', ns, 5) + 14, ny - 54, w=14, h=64, color=D.CYAN)

    o += D.text(cx, 234, DISCIPLINES, size=15.5, fill=D.TEXT, tracking=2.2, preserve=True)
    o += D.rule(cx, 250, 300, h=2.4)

    # LOCATION / STATUS / MISSION
    ix0, iy0 = cx, 284
    bw, bh = 780, 152
    o += D.panel(ix0, iy0, bw, bh, fill='#03110C', stroke=D.GREEN, sw=1.2)
    o += D.brackets(ix0, iy0, bw, bh, color=D.GREEN, arm=14, sw=1.8,
                    corners='tl,tr,bl,br', opacity=0.6)
    for i, (icon, key, val, col) in enumerate(ROWS):
        ry = iy0 + 44 + i * 40
        o += icon(ix0 + 26, ry - 15, 20, D.CYAN)
        o += D.text(ix0 + 60, ry, key, size=16, fill=D.CYAN, tracking=2.6)
        o += D.text(ix0 + 250, ry, ':', size=16, fill=D.FAINT)
        o += D.text(ix0 + 292, ry, val, size=16, fill=col, weight='600', tracking=1.8)
        if key == 'STATUS':
            o += D.status_dot(ix0 + 292 + D.tw(val, 16, 1.8) + 18, ry - 5, D.YELLOW, 5)

    o += D.prompt_bar(cx, 452, bw, '', h=44, user=USER, size=15)
    return D.doc(W, H, TITLE, DESC, o)


def narrow():
    W = 440
    px, py, pw = 10, 34, W - 20
    cx = px + 18
    inner = pw - 36

    o = D.tab(px + 14, py - 22, '~/whoami', color=D.CYAN, size=13)

    ps = 13
    o += D.text(cx, py + 40, USER, size=ps, fill=D.GREEN, weight='600')
    ux = cx + D.tw(USER, ps)
    o += D.text(ux, py + 40, ':~$', size=ps, fill=D.CYAN)
    o += D.text(ux + D.tw(':~$', ps) + 8, py + 40, 'whoami', size=ps, fill=D.TEXT_HI)

    o += D.globe(W - 74, py + 44, 44, D.GREEN_DIM, 0.55)

    nx, ny, ns = cx, py + 108, 44
    o += D.text(nx, ny, 'ARYAN', size=ns, fill=D.GREEN, weight='700', tracking=2, filt='glowMd')
    ix = nx + D.tw('ARYAN', ns, 2) + 16
    o += D.text(ix, ny, 'IQ', size=ns, fill=D.CYAN, weight='700', tracking=2, filt='glowMd')
    o += D.caret(ix + D.tw('IQ', ns, 2) + 9, ny - 32, w=9, h=38, color=D.CYAN)

    o += D.text(cx, ny + 26, 'FULL-STACK  /  CYBERSECURITY', size=12.5, fill=D.TEXT, tracking=1, preserve=True)
    o += D.text(cx, ny + 44, 'AI SYSTEMS BUILDER', size=12.5, fill=D.TEXT, tracking=1)
    o += D.rule(cx, ny + 54, 180, h=2)

    iy0 = ny + 74
    bh = 128
    o += D.panel(cx, iy0, inner, bh, fill='#03110C', stroke=D.GREEN, sw=1.2)
    o += D.brackets(cx, iy0, inner, bh, color=D.GREEN, arm=11, sw=1.6,
                    corners='tl,tr,bl,br', opacity=0.6)
    for i, (icon, key, val, col) in enumerate(ROWS):
        ry = iy0 + 34 + i * 34
        o += icon(cx + 14, ry - 12, 16, D.CYAN)
        o += D.text(cx + 40, ry, key, size=12.5, fill=D.CYAN, tracking=1.6)
        o += D.text(cx + 132, ry, ':', size=12.5, fill=D.FAINT)
        o += D.text(cx + 148, ry, val, size=12.5, fill=col, weight='600', tracking=0.8)

    by = iy0 + bh + 14
    o += D.prompt_bar(cx, by, inner, '', h=36, user=USER, size=12)

    ph = by + 36 + 16 - py
    H = py + ph + 12
    frame = (D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
             + D.brackets(px, py, pw, ph, color=D.GREEN, arm=14, sw=1.8,
                          corners='tl,br', opacity=0.75))
    return D.doc(W, H, TITLE, DESC, frame + o)
