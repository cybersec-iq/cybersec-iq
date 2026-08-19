"""~/about — operating principles panel.

Reference: 02_WHOAMI_ABOUT_REFERENCE.png — the `~/about` tab, the highlighted
body copy, the HOW I WORK rule and the icon/heading principle cards.
The reference shows four cards; five principles are carried here because that
is the set the profile already stands behind.
"""

import design as D

BODY = [
    [('I design and ship ', D.TEXT), ('production systems', D.GREEN), (' end to end — interface, API,', D.TEXT)],
    [('data layer, infrastructure and the automation that keeps them running.', D.TEXT)],
    [],
    [('Most of my work sits where ', D.TEXT), ('product engineering meets security', D.CYAN),
     (': platforms', D.TEXT)],
    [('that handle real users, real payments and real data, built so that the', D.TEXT)],
    [('boring parts are ', D.TEXT), ('automated', D.GREEN), (' and the risky parts are ', D.TEXT),
     ('deliberate', D.YELLOW), ('.', D.TEXT)],
]

PRINCIPLES = [
    (D.i_shield, D.GREEN,  ['SECURITY', 'FIRST'],
     ['Security is a design', 'input, not a review', 'step. Threat', 'assumptions get', 'written down first.']),
    (D.i_bolt,   D.YELLOW, ['AUTOMATE THE', 'REPEATABLE'],
     ['If a task happens', 'twice it becomes a', 'script, a pipeline', 'or a bot.', '']),
    (D.i_cube,   D.CYAN,   ['BORING INFRA,', 'INTERESTING PRODUCTS'],
     ['Predictable deploys', 'are what make', 'ambitious features', 'affordable.', '']),
    (D.i_target, D.GREEN,  ['OWN THE', 'WHOLE PATH'],
     ['From git init to the', 'production incident', 'at 2am. No handoff', 'to hide behind.', '']),
    (D.i_pulse,  D.CYAN,   ['SHIP, MEASURE,', 'HARDEN'],
     ['Working beats', 'perfect. Then perfect', 'the parts that carry', 'risk.', '']),
]

DESC = ('About panel. I design and ship production systems end to end: interface, API, '
        'data layer, infrastructure and automation. Most of my work sits where product '
        'engineering meets security. How I work: security first; automate the repeatable; '
        'boring infrastructure, interesting products; own the whole path; ship, measure, harden.')
TITLE = 'about - operating principles'


def _rich(x, y, runs, size, tracking=0.3):
    return D.rich(x, y, runs, size=size, tracking=tracking,
                  weight_for=lambda c: None if c == D.TEXT else '600')


def wide():
    W, H = 1200, 530
    px, py, pw, ph = 22, 40, W - 44, 466

    o = D.tab(px + 26, py - 26, '~/about', color=D.CYAN, size=16)
    o += D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
    o += D.brackets(px, py, pw, ph, color=D.GREEN, arm=18, sw=2, corners='tr,bl', opacity=0.75)

    cx = px + 40
    for i, runs in enumerate(BODY):
        if runs:
            o += _rich(cx, 86 + i * 26, runs, 16)

    o += D.label(cx, 248, 'HOW I WORK', size=13, fill=D.CYAN, tracking=4)
    o += D.hline(cx + 156, 243, pw - 196, D.LINE_2)

    cw, gap = 213, 12
    ky, kh = 274, 202
    for i, (icon, col, name, lines) in enumerate(PRINCIPLES):
        ox = cx + i * (cw + gap)
        o += D.panel(ox, ky, cw, kh, fill=D.SURFACE_2, stroke=D.LINE_2)
        o += ('    <rect x="%d" y="%d" width="%d" height="2" fill="%s" opacity="0.8"/>\n'
              % (ox, ky, cw, col))
        o += icon(ox + 16, ky + 16, 24, col)
        for j, hl in enumerate(name):
            o += D.text(ox + 16, ky + 58 + j * 16, hl, size=11.5, fill=col,
                        weight='700', tracking=1.2)
        for j, ln in enumerate(lines):
            if ln:
                o += D.text(ox + 16, ky + 100 + j * 17, ln, size=12, fill=D.MUTED)

    return D.doc(W, H, TITLE, DESC, o)


NARROW_BODY = [
    [('I design and ship ', D.TEXT), ('production', D.GREEN)],
    [('systems', D.GREEN), (' end to end — interface, API,', D.TEXT)],
    [('data layer, infrastructure and the', D.TEXT)],
    [('automation that keeps them running.', D.TEXT)],
    [],
    [('Most of my work sits where ', D.TEXT)],
    [('product engineering meets security', D.CYAN), (':', D.TEXT)],
    [('platforms handling real users, real', D.TEXT)],
    [('payments and real data — boring parts', D.TEXT)],
    [('', D.TEXT)],
]


def narrow():
    W = 440
    px, py, pw = 10, 34, W - 20
    cx = px + 18
    inner = pw - 36

    o = D.tab(px + 14, py - 22, '~/about', color=D.CYAN, size=13)

    lines = [
        [('I design and ship ', D.TEXT), ('production', D.GREEN)],
        [('systems', D.GREEN), (' end to end — interface,', D.TEXT)],
        [('API, data layer, infrastructure and', D.TEXT)],
        [('the automation that keeps them running.', D.TEXT)],
        [],
        [('Most of my work sits where ', D.TEXT)],
        [('product engineering meets security', D.CYAN), (':', D.TEXT)],
        [('platforms that handle real users, real', D.TEXT)],
        [('payments and real data, built so the', D.TEXT)],
        [('boring parts are ', D.TEXT), ('automated', D.GREEN), (' and the', D.TEXT)],
        [('risky parts are ', D.TEXT), ('deliberate', D.YELLOW), ('.', D.TEXT)],
    ]
    y0 = py + 34
    for i, runs in enumerate(lines):
        if runs:
            o += _rich(cx, y0 + i * 19, runs, 11.5, tracking=0.1)

    hy = y0 + len(lines) * 19 + 10
    o += D.label(cx, hy, 'HOW I WORK', size=12, fill=D.CYAN, tracking=3)
    o += D.hline(cx + 108, hy - 5, inner - 108, D.LINE_2)

    ky = hy + 16
    rowh = 86
    for i, (icon, col, name, body) in enumerate(PRINCIPLES):
        ry = ky + i * rowh
        o += D.panel(cx, ry, inner, rowh - 8, fill=D.SURFACE_2, stroke=D.LINE_2)
        o += ('    <rect x="%d" y="%d" width="3" height="%d" fill="%s" opacity="0.85"/>\n'
              % (cx, ry, rowh - 8, col))
        o += icon(cx + 14, ry + 13, 20, col)
        o += D.text(cx + 44, ry + 21, ' '.join(name), size=11.5, fill=col,
                    weight='700', tracking=0.8)
        # Wrap to the card width instead of truncating: a principle that stops
        # mid-sentence reads worse than one that takes an extra line.
        flat = ' '.join(x for x in body if x)
        bs = 10.5
        for j, ln in enumerate(D.wrap(flat, D.fit_chars(inner - 58, bs))[:3]):
            o += D.text(cx + 44, ry + 38 + j * 14, ln, size=bs, fill=D.MUTED)

    ph = ky + len(PRINCIPLES) * rowh + 8 - py
    H = py + ph + 12
    frame = (D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
             + D.brackets(px, py, pw, ph, color=D.GREEN, arm=14, sw=1.8,
                          corners='tr,bl', opacity=0.75))
    return D.doc(W, H, TITLE, DESC, frame + o)
