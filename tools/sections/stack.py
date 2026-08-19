"""~/stack — technology system map.

Reference: 03_STACK_CURRENTLY_BUILDING_REFERENCE.png — section header with the
prompt glyph, category columns with icon + purpose line + chips, and the
right-hand summary panel.

The reference's summary reads "16+ / 10+"; those are replaced with counts
derived from the chips actually rendered below, so the panel cannot drift out
of sync with what it summarises.
"""

import design as D

CATEGORIES = [
    ('FRONTEND', D.CYAN, D.i_code, 'Modern UI/UX',
     [('React', D.CYAN), ('Next.js', D.TEXT), ('TypeScript', D.BLUE), ('JavaScript', D.YELLOW)]),
    ('BACKEND', D.GREEN, D.i_terminal, 'Robust APIs',
     [('Node.js', D.GREEN), ('Python', D.TEXT), ('REST APIs', D.CYAN)]),
    ('DATA', D.CYAN, D.i_db, 'Data & storage',
     [('PostgreSQL', D.BLUE)]),
    ('INFRASTRUCTURE', D.YELLOW, D.i_cube, 'Deploy & scale',
     [('Docker', D.CYAN), ('Linux', D.YELLOW), ('Git', D.GREEN), ('GitHub Actions', D.TEXT)]),
]

WIDE_ROW2 = [
    ('SECURITY PRACTICE', D.GREEN, D.i_shield, 'Secure by design',
     [('Secure SDLC', D.GREEN), ('Threat Modelling', D.GREEN), ('Dependency Hygiene', D.GREEN),
      ('Hardening', D.GREEN)]),
    ('TOOLS & AUTOMATION', D.YELLOW, D.i_bolt, 'Productivity & automation',
     [('GitHub Actions', D.YELLOW), ('CI/CD Pipelines', D.YELLOW), ('Automation Bots', D.YELLOW)]),
]

DESC = ('Technology stack. Frontend: React, Next.js, TypeScript, JavaScript. '
        'Backend: Node.js, Python, REST APIs. Data: PostgreSQL. '
        'Infrastructure: Docker, Linux, Git, GitHub Actions. '
        'Security practice: secure SDLC, threat modelling, dependency hygiene, hardening. '
        'Tools and automation: GitHub Actions, CI/CD pipelines, automation bots.')
TITLE = 'stack - technology system map'


def _counts():
    tech = sum(len(c[4]) for c in CATEGORIES)
    tools = sum(len(c[4]) for c in WIDE_ROW2)
    return tech, tools, len(CATEGORIES) + len(WIDE_ROW2)


def _category(x, y, w, name, col, icon, purpose, chips, chip_size=12.5):
    o = icon(x, y, 30, col)
    o += D.text(x + 42, y + 15, name, size=15, fill=col, weight='700', tracking=2.4)
    o += D.text(x + 42, y + 34, purpose, size=12, fill=D.MUTED, tracking=0.5)
    c, rows, bottom = D.chip_row(x, y + 54, chips, size=chip_size, max_w=w, lh=32)
    return o + c, bottom


def wide():
    W, H = 1200, 522
    px, py, pw = 22, 20, W - 44

    o = D.section_header(px + 24, py + 46, '~/stack', 'TECHNOLOGY STACK & TOOLING',
                         right='SYSTEM MAP', right_icon=D.i_grid, w=pw - 48)

    ph = 424
    o += D.panel(px, py + 76, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
    o += D.brackets(px, py + 76, pw, ph, color=D.GREEN, arm=18, sw=2,
                    corners='tl,tr,bl,br', opacity=0.55)

    cx = px + 34
    inner = pw - 68

    # ---- row 1: four categories in a bordered band ----
    b1y, b1h = py + 104, 178
    o += D.panel(cx, b1y, inner, b1h, fill=D.SURFACE_2, stroke=D.LINE)
    colw = inner / 4
    for i, (name, col, icon, purpose, chips) in enumerate(CATEGORIES):
        ox = cx + i * colw
        if i:
            o += D.vline(ox, b1y + 18, b1h - 36, D.LINE_2)
        c, _ = _category(ox + 22, b1y + 26, colw - 44, name, col, icon, purpose, chips)
        o += c

    # ---- row 2: security + tooling, with a derived summary ----
    b2y, b2h = b1y + b1h + 18, 180
    lw = inner * 0.66
    o += D.panel(cx, b2y, lw, b2h, fill=D.SURFACE_2, stroke=D.LINE)
    for i, (name, col, icon, purpose, chips) in enumerate(WIDE_ROW2):
        ox = cx + i * (lw / 2)
        if i:
            o += D.vline(ox, b2y + 18, b2h - 36, D.LINE_2)
        c, _ = _category(ox + 22, b2y + 26, lw / 2 - 44, name, col, icon, purpose, chips)
        o += c

    sx = cx + lw + 16
    sw_ = inner - lw - 16
    o += D.panel(sx, b2y, sw_, b2h, fill=D.SURFACE_2, stroke=D.LINE)
    tech, tools, cats = _counts()
    summary = [
        ('Technologies listed', str(tech), D.GREEN),
        ('Core categories', str(cats), D.CYAN),
        ('Tooling & practice', str(tools), D.YELLOW),
        ('Security first', 'Always', D.GREEN),
    ]
    for i, (k, v, col) in enumerate(summary):
        ry = b2y + 44 + i * 34
        o += D.text(sx + 22, ry, '>', size=14, fill=D.GREEN_DIM)
        o += D.text(sx + 44, ry, k, size=13.5, fill=D.TEXT, tracking=0.4)
        o += D.text(sx + sw_ - 22, ry, v, size=15, fill=col, weight='700',
                    tracking=0.8, anchor='end')

    return D.doc(W, H, TITLE, DESC, o)


def narrow():
    W = 440
    px, py, pw = 10, 58, W - 20
    cx = px + 16
    inner = pw - 32

    o = D.section_header(px + 8, 34, '~/stack', 'TECHNOLOGY STACK & TOOLING')

    y = py + 22
    groups = CATEGORIES + WIDE_ROW2
    for name, col, icon, purpose, chips in groups:
        o += icon(cx, y, 22, col)
        o += D.text(cx + 32, y + 11, name, size=12.5, fill=col, weight='700', tracking=1.6)
        o += D.text(cx + 32, y + 27, purpose, size=10.5, fill=D.MUTED)
        c, rows, bottom = D.chip_row(cx, y + 38, chips, size=11, max_w=inner, h=22, lh=28)
        o += c
        y = bottom + 16

    tech, tools, cats = _counts()
    sy = y + 2
    sh = 34
    o += D.panel(cx, sy, inner, sh, fill=D.SURFACE_2, stroke=D.LINE)
    parts = [('TECH', str(tech), D.GREEN), ('CATEGORIES', str(cats), D.CYAN),
             ('TOOLING', str(tools), D.YELLOW)]
    step = inner / len(parts)
    for i, (k, v, col) in enumerate(parts):
        ox = cx + i * step + 14
        o += D.rich(ox, sy + 21, [(k + '  ', D.MUTED), (v, col)], size=10.5,
                    tracking=1.2, weight_for=lambda c: None if c == D.MUTED else '700')

    ph = sy + sh + 16 - py
    H = py + ph + 12
    frame = (D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
             + D.brackets(px, py, pw, ph, color=D.GREEN, arm=14, sw=1.8,
                          corners='tl,tr,bl,br', opacity=0.55))
    return D.doc(W, H, TITLE, DESC, frame + o)
