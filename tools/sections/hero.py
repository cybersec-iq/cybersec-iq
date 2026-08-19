"""Hero / command-center banner.

Reference: 01_MASTER_STYLE_COMMAND_CENTER.png (primary style anchor).
Adapted: GitHub owns the real profile sidebar and avatar, so the reference's
left identity column is not reproduced here; that content lives in the whoami
section instead.
"""

import design as D

EYEBROW = 'SYSTEM // OPERATOR'
DISCIPLINES = ['FULL-STACK DEVELOPER', 'CYBERSECURITY ENGINEER', 'AI SYSTEMS BUILDER']
QUOTE = ['I build systems. I break assumptions.', 'I secure what matters.']

CAPS = [
    ('FULL-STACK',    D.CYAN,   D.i_code,   ['Scalable web apps', '& robust systems']),
    ('CYBERSECURITY', D.GREEN,  D.i_shield, ['Secure by design', 'threat-aware']),
    ('AI SYSTEMS',    D.CYAN,   D.i_brain,  ['LLM-powered', 'intelligent tools']),
    ('AUTOMATION',    D.YELLOW, D.i_bolt,   ['Pipelines, bots', '& workflows']),
    ('ARCHITECTURE',  D.CYAN,   D.i_layers, ['Clean design', 'built to last']),
]

# Geographic nodes: San Francisco, Brazil, London, Muscat, Singapore, Tokyo,
# Sydney. Six connections keep the map legible instead of turning it into a
# network-line thicket.
NODES = [(0.16, 0.31), (0.37, 0.69), (0.50, 0.20), (0.66, 0.41),
         (0.79, 0.57), (0.89, 0.32), (0.92, 0.84)]
LINKS = [(0, 2), (1, 3), (2, 3), (3, 4), (3, 5), (4, 6)]

DESC = ('Command-center banner. SYSTEM // OPERATOR. ARYAN IQ. '
        'Full-stack developer, cybersecurity engineer, AI systems builder. '
        'I build systems. I break assumptions. I secure what matters. '
        'Current status: building. Nothing is impossible. '
        'Capabilities: full-stack, cybersecurity, AI systems, automation, architecture.')

TITLE = 'Aryan IQ - developer command center'


def wide():
    W, H = 1200, 566
    px, py, pw, ph = 22, 62, W - 44, 482

    # ---- window chrome ----
    o = D.hline(0, 46, W, D.LINE)
    o += ('    <rect x="24" y="12" width="30" height="26" rx="2" fill="' + D.SURFACE_2 +
          '" stroke="' + D.GREEN + '" stroke-width="1.1" stroke-opacity="0.5"/>\n')
    o += ('    <g stroke="' + D.GREEN + '" stroke-width="1.8" fill="none" stroke-linecap="square">'
          '<path d="M32 20 l5 5 l-5 5"/><path d="M40 30 h7"/></g>\n')
    o += D.text(66, 30, '~/cybersec-iq', size=14, fill=D.GREEN, weight='600', tracking=0.6)
    o += D.i_branch(212, 13, 17, D.MUTED)
    o += D.text(236, 30, 'main', size=13.5, fill=D.MUTED, tracking=0.6)

    badge = 'DEVELOPER COMMAND CENTER'
    bw = D.tw(badge, 13, 3.2) + 44
    bx = (W - bw) / 2
    o += ('    <rect x="%.0f" y="10" width="%.0f" height="29" rx="14.5" fill="%s" '
          'stroke="%s" stroke-width="1.2" stroke-opacity="0.65"/>\n'
          % (bx, bw, D.SURFACE_2, D.CYAN))
    o += D.text(bx + 22, 30, badge, size=13, fill=D.CYAN, weight='600', tracking=3.2)

    o += D.status_dot(W - 196, 25, D.GREEN, 4.5)
    o += D.text(W - 182, 30, 'SYSTEM ONLINE', size=12.5, fill=D.GREEN, tracking=2.4)
    o += D.signal_bars(W - 46, 32, D.CYAN_DIM)

    # ---- main panel ----
    o += D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
    o += D.brackets(px, py, pw, ph, color=D.YELLOW, arm=20, sw=2.2, corners='tl,tr')
    o += D.brackets(px, py, pw, ph, color=D.LINE_3, arm=20, sw=2, corners='bl,br', opacity=0.9)

    cx = px + 42

    o += D.world_map(806, 86, 346, 176, dot=1.7, step=7.4, color=D.GREEN_DIM, opacity=0.95)
    o += D.node_web(806, 86, 346, 176, NODES, LINKS,
                    colors=(D.GREEN, D.CYAN, D.YELLOW, D.GREEN, D.CYAN))

    o += D.label(cx, 116, EYEBROW, size=13.5, fill=D.CYAN, tracking=5.5)
    o += D.i_shield_check(cx, 148, 72, D.GREEN)

    nx, ny, ns = cx + 100, 212, 78
    o += D.name_lockup(nx, ny, 'ARYAN', 'IQ', ns, 5)
    o += D.rule(nx, 236, 430, h=2.4)

    runs = []
    for i, part in enumerate(DISCIPLINES):
        runs.append((part, D.TEXT))
        if i < len(DISCIPLINES) - 1:
            runs.append(('  •  ', D.GREEN))
    o += D.rich(nx, 268, runs, size=16.5, tracking=2.4)

    qx, qy, qw, qh = cx, 300, 648, 96
    o += D.panel(qx, qy, qw, qh, fill='#03130C', stroke=D.GREEN, sw=1.2)
    o += '    <rect x="%d" y="%d" width="3" height="%d" fill="%s" opacity="0.8"/>\n' % (qx, qy, qh, D.GREEN)
    o += D.i_terminal(qx + 22, qy + 34, 24, D.GREEN)
    for i, ln in enumerate(QUOTE):
        o += D.text(qx + 62, qy + 40 + i * 28, ln, size=16.5, fill=D.TEXT_HI, tracking=0.4)

    sx, sy = qx + qw + 24, 300
    sw_, sh = pw - (qx - px) - qw - 24 - 42, 96
    o += D.panel(sx, sy, sw_, sh, fill=D.SURFACE_2, stroke=D.LINE_2)
    o += D.brackets(sx, sy, sw_, sh, color=D.CYAN, arm=13, sw=1.8,
                    corners='tl,tr,bl,br', opacity=0.7)
    o += D.label(sx + 22, sy + 28, 'CURRENT STATUS', size=11.5, fill=D.MUTED, tracking=2.8)
    o += D.text(sx + 22, sy + 58, 'BUILDING', size=22, fill=D.YELLOW, weight='700',
                tracking=2.6, filt='glowSm')
    o += D.status_dot(sx + 22 + D.tw('BUILDING', 22, 2.6) + 16, sy + 51, D.YELLOW, 5)
    o += D.label(sx + 22, sy + 80, 'NOTHING IS IMPOSSIBLE', size=11.5, fill=D.GREEN, tracking=2.2)

    kx, ky, kw, kh = cx, 424, pw - 84, 100
    o += D.panel(kx, ky, kw, kh, fill=D.SURFACE_2, stroke=D.LINE, sw=1)
    colw = kw / len(CAPS)
    for i, (name, col, icon, lines) in enumerate(CAPS):
        ox = kx + i * colw
        if i:
            o += D.vline(ox, ky + 16, kh - 32, D.LINE_2)
        o += icon(ox + colw / 2 - 16, ky + 13, 32, col)
        twid = D.tw(name, 12.5, 2.2)
        o += D.text(ox + colw / 2 - twid / 2, ky + 64, name, size=12.5, fill=col,
                    weight='700', tracking=2.2)
        for j, ln in enumerate(lines):
            lw = D.tw(ln, 11.5, 0.3)
            o += D.text(ox + colw / 2 - lw / 2, ky + 81 + j * 15, ln, size=11.5, fill=D.MUTED)

    return D.doc(W, H, TITLE, DESC, o)


def narrow():
    """440-unit canvas: renders close to 1:1 on a phone, so type stays legible."""
    W = 440
    px, py, pw = 10, 44, W - 20
    cx = px + 22
    inner = pw - 44

    o = D.hline(0, 34, W, D.LINE)
    o += ('    <rect x="10" y="7" width="23" height="21" rx="2" fill="' + D.SURFACE_2 +
          '" stroke="' + D.GREEN + '" stroke-width="1.1" stroke-opacity="0.5"/>\n')
    o += ('    <g stroke="' + D.GREEN + '" stroke-width="1.7" fill="none" stroke-linecap="square">'
          '<path d="M16 12 l4 4 l-4 4"/><path d="M22 20 h5"/></g>\n')
    o += D.text(41, 22, '~/cybersec-iq', size=13, fill=D.GREEN, weight='600')
    o += D.status_dot(W - 116, 18, D.GREEN, 4)
    o += D.text(W - 105, 22, 'SYSTEM ONLINE', size=11, fill=D.GREEN, tracking=1.4)

    o += D.world_map(W - 168, 60, 150, 78, dot=1.3, step=6.4, color=D.GREEN_DIM, opacity=0.55)

    o += D.label(cx, 74, EYEBROW, size=12, fill=D.CYAN, tracking=3.8)
    o += D.i_shield_check(cx, 92, 40, D.GREEN)

    nx, ny, ns = cx + 52, 132, 42
    o += D.name_lockup(nx, ny, 'ARYAN', 'IQ', ns, 2, filt='glowMd')
    o += D.rule(nx, 148, 196, h=2)

    y = 182
    for part in DISCIPLINES:
        o += D.text(cx + 2, y, '•', size=15, fill=D.GREEN)
        o += D.text(cx + 18, y, part, size=15, fill=D.TEXT, tracking=1.1)
        y += 24

    qy, qh = y + 12, 74
    o += D.panel(cx, qy, inner, qh, fill='#03130C', stroke=D.GREEN, sw=1.2)
    o += '    <rect x="%d" y="%d" width="3" height="%d" fill="%s" opacity="0.8"/>\n' % (cx, qy, qh, D.GREEN)
    o += D.i_terminal(cx + 14, qy + 26, 19, D.GREEN)
    for i, ln in enumerate(QUOTE):
        o += D.text(cx + 44, qy + 31 + i * 24, ln, size=13.5, fill=D.TEXT_HI)

    sy, sh = qy + qh + 16, 76
    o += D.panel(cx, sy, inner, sh, fill=D.SURFACE_2, stroke=D.LINE_2)
    o += D.brackets(cx, sy, inner, sh, color=D.CYAN, arm=11, sw=1.6,
                    corners='tl,tr,bl,br', opacity=0.7)
    o += D.label(cx + 16, sy + 24, 'CURRENT STATUS', size=11, fill=D.MUTED, tracking=2.2)
    o += D.text(cx + 16, sy + 50, 'BUILDING', size=19, fill=D.YELLOW, weight='700',
                tracking=2.2, filt='glowSm')
    o += D.status_dot(cx + 16 + D.tw('BUILDING', 19, 2.2) + 14, sy + 44, D.YELLOW, 4.5)
    o += D.label(cx + 16, sy + 68, 'NOTHING IS IMPOSSIBLE', size=11, fill=D.GREEN, tracking=1.6)

    ky = sy + sh + 18
    for i, (name, col, icon, lines) in enumerate(CAPS):
        ry = ky + i * 42
        o += icon(cx, ry, 21, col)
        o += D.text(cx + 32, ry + 12, name, size=13.5, fill=col, weight='700', tracking=1.8)
        o += D.text(cx + 32, ry + 29, lines[0] + ' ' + lines[1], size=11.5, fill=D.MUTED)

    ph = ky + len(CAPS) * 42 - py + 4
    H = py + ph + 12
    frame = (D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
             + D.brackets(px, py, pw, ph, color=D.YELLOW, arm=15, sw=2, corners='tl,tr')
             + D.brackets(px, py, pw, ph, color=D.LINE_3, arm=15, sw=2, corners='bl,br'))

    return D.doc(W, H, TITLE, DESC, frame + o)
