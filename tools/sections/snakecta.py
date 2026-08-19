"""PLAY SNAKE call to action.

Reference: 05_PLAY_SNAKE_CONTACT_REFERENCE.png — the oversized PLAY SNAKE
lockup, the glowing button, the controls/status panel and the board preview.

Data integrity: the reference's status panel shows SCORE 042 / HIGH SCORE 128 /
LENGTH 17. Those are mock values from a mockup, and a README image cannot know
a visitor's score, so they are replaced with the game's real fixed properties
(grid size, dependency count, storage model). Live score, high score and length
appear in the actual game on GitHub Pages, where they are real.
"""

import design as D

CONTROLS = [
    ('ARROWS / WASD', 'MOVE', D.CYAN),
    ('SPACE or P', 'PAUSE', D.CYAN),
    ('R', 'RESTART', D.CYAN),
]

FACTS = [
    ('BOARD', '21 x 21'),
    ('DEPENDENCIES', 'NONE'),
    ('TRACKERS', 'NONE'),
    ('HIGH SCORE', 'STORED LOCALLY'),
]

# Body pixels of the preview snake, in grid cells.
SNAKE_CELLS = [(2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8),
               (10, 8), (10, 7), (10, 6), (10, 5), (11, 5), (12, 5), (13, 5)]
FOOD_CELL = (5, 2)

DESC = ('Play Snake. Interactive console. A real, playable Snake: original build, '
        'no framework, no trackers, no dependencies. Controls: arrows or WASD to move, '
        'space or P to pause, R to restart. Board 21 by 21. High score stored locally '
        'in the browser. Hosted on GitHub Pages.')
TITLE = 'Play Snake - snake protocol'


def _board(x, y, w, h, cols=16, rows=11):
    cw = w / cols
    o = D.panel(x, y, w, h, fill='#020A06', stroke=D.GREEN, sw=1.2)
    o += D.brackets(x, y, w, h, color=D.GREEN, arm=12, sw=1.6,
                    corners='tl,tr,bl,br', opacity=0.6)
    o += '    <g stroke="%s" stroke-width="0.7" opacity="0.5">' % D.GREEN_DEEP
    for c in range(1, cols):
        o += '<path d="M%.1f %d V%d"/>' % (x + c * cw, y, y + h)
    for r in range(1, rows):
        o += '<path d="M%d %.1f H%d"/>' % (x, y + r * (h / rows), x + w)
    o += '</g>\n'

    s = min(cw, h / rows) - 3
    o += '    <g fill="%s">' % D.GREEN
    for i, (c, r) in enumerate(SNAKE_CELLS):
        op = 0.55 + 0.45 * (i / max(1, len(SNAKE_CELLS) - 1))
        o += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" opacity="%.2f"/>'
              % (x + c * cw + 1.5, y + r * (h / rows) + 1.5, s, s, op))
    o += '</g>\n'
    hc, hr = SNAKE_CELLS[-1]
    o += ('    <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" '
          'filter="url(#glowSm)"/>\n'
          % (x + hc * cw + 1.5, y + hr * (h / rows) + 1.5, s, s, D.LIME))
    fc, fr = FOOD_CELL
    o += ('    <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" '
          'class="live" filter="url(#glowSm)"/>\n'
          % (x + fc * cw + 1.5, y + fr * (h / rows) + 1.5, s, s, D.YELLOW))
    return o


def wide():
    W, H = 1200, 442
    px, py, pw, ph = 22, 20, W - 44, 402

    o = D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
    o += D.brackets(px, py, pw, ph, color=D.YELLOW, arm=20, sw=2.2, corners='tl,tr')

    cx = px + 42
    o += D.label(cx, py + 46, '// INTERACTIVE CONSOLE', size=13.5, fill=D.CYAN, tracking=3.6)

    o += D.i_snake(cx, py + 62, 44, D.GREEN)
    o += D.text(cx + 60, py + 108, 'PLAY SNAKE', size=54, fill=D.GREEN, weight='700',
                tracking=3, filt='glowLg')

    o += D.text(cx, py + 142, 'Challenge the terminal. Beat the system.',
                size=16, fill=D.TEXT_HI, tracking=0.4)

    # button
    bx, by, bw, bh = cx, py + 166, 470, 62
    o += D.panel(bx, by, bw, bh, fill='#04170A', stroke=D.GREEN, sw=2)
    o += D.panel(bx + 5, by + 5, bw - 10, bh - 10, fill='none', stroke=D.GREEN, sw=1, opacity=0)
    o += D.i_play(bx + 26, by + bh / 2 - 12, 24, D.GREEN)
    o += D.text(bx + 76, by + bh / 2 + 8, 'PLAY SNAKE', size=21, fill=D.GREEN,
                weight='700', tracking=9, filt='glowSm')
    o += ('    <path d="M%d %d l8 8 l-8 8" fill="none" stroke="%s" stroke-width="2.4" '
          'stroke-linecap="square"/>\n' % (bx + bw - 40, by + bh / 2 - 8, D.GREEN))

    o += D.text(cx, py + 258, 'A real, playable Snake — original build, no framework,',
                size=13.5, fill=D.MUTED)
    o += D.text(cx, py + 277, 'no trackers, no dependencies.', size=13.5, fill=D.MUTED)

    o += D.i_code(cx, py + 296, 17, D.GREEN)
    o += D.rich(cx + 26, py + 310,
                [('cybersec-iq.github.io/cybersec-iq', D.BLUE), ('  — command center', D.MUTED)],
                size=13.5)
    o += D.rich(cx + 26, py + 331,
                [('/snake', D.BLUE), ('  — SNAKE PROTOCOL', D.MUTED)], size=13.5)

    # right: spec + board
    rx = px + 560
    rw = pw - 560 - 42
    o += D.panel(rx, py + 34, rw, ph - 68, fill=D.SURFACE_2, stroke=D.LINE_2)

    o += D.text(rx + 24, py + 64, 'SNAKE PROTOCOL', size=14, fill=D.TEXT_HI,
                weight='600', tracking=2)
    o += D.status_dot(rx + rw - 84, py + 59, D.GREEN, 4)
    o += D.text(rx + rw - 70, py + 64, 'LIVE', size=12, fill=D.GREEN, tracking=1.8)
    o += D.hline(rx + 24, py + 78, rw - 48, D.LINE_2)

    o += D.label(rx + 24, py + 104, '// CONTROLS', size=12, fill=D.CYAN, tracking=2.4)
    for i, (keys, act, col) in enumerate(CONTROLS):
        ry = py + 130 + i * 26
        o += D.text(rx + 24, ry, keys, size=13, fill=col, tracking=0.8)
        o += D.text(rx + 210, ry, act, size=13, fill=D.TEXT, tracking=1.6)

    o += D.label(rx + 24, py + 236, '// PROPERTIES', size=12, fill=D.CYAN, tracking=2.4)
    for i, (k, v) in enumerate(FACTS):
        ry = py + 262 + i * 24
        o += D.text(rx + 24, ry, k, size=12, fill=D.MUTED, tracking=1.4)
        o += D.text(rx + 210, ry, v, size=12, fill=D.LIME, tracking=1.2)

    o += _board(rx + 340, py + 96, rw - 372, 224)
    return D.doc(W, H, TITLE, DESC, o)


def narrow():
    W = 440
    px, py, pw = 10, 20, W - 20
    cx = px + 20
    inner = pw - 40

    o = D.label(cx, py + 32, '// INTERACTIVE CONSOLE', size=11.5, fill=D.CYAN, tracking=2.6)
    o += D.i_snake(cx, py + 44, 30, D.GREEN)
    o += D.text(cx + 42, py + 76, 'PLAY SNAKE', size=34, fill=D.GREEN, weight='700',
                tracking=1.6, filt='glowMd')
    o += D.text(cx, py + 102, 'Challenge the terminal.', size=13, fill=D.TEXT_HI)
    o += D.text(cx, py + 120, 'Beat the system.', size=13, fill=D.TEXT_HI)

    bx, by, bh = cx, py + 136, 54
    o += D.panel(bx, by, inner, bh, fill='#04170A', stroke=D.GREEN, sw=2)
    o += D.i_play(bx + 18, by + bh / 2 - 10, 20, D.GREEN)
    o += D.text(bx + 56, by + bh / 2 + 6, 'PLAY SNAKE', size=16, fill=D.GREEN,
                weight='700', tracking=5.5, filt='glowSm')
    o += ('    <path d="M%d %d l7 7 l-7 7" fill="none" stroke="%s" stroke-width="2.2" '
          'stroke-linecap="square"/>\n' % (bx + inner - 30, by + bh / 2 - 7, D.GREEN))

    o += _board(cx, by + bh + 16, inner, 150, cols=16, rows=11)

    ky = by + bh + 182
    o += D.label(cx, ky, '// CONTROLS', size=11, fill=D.CYAN, tracking=2.2)
    for i, (keys, act, col) in enumerate(CONTROLS):
        ry = ky + 22 + i * 22
        o += D.text(cx, ry, keys, size=12, fill=col)
        o += D.text(cx + 190, ry, act, size=12, fill=D.TEXT, tracking=1.2)

    fy = ky + 22 + len(CONTROLS) * 22 + 14
    o += D.label(cx, fy, '// PROPERTIES', size=11, fill=D.CYAN, tracking=2.2)
    for i, (k, v) in enumerate(FACTS):
        ry = fy + 22 + i * 21
        o += D.text(cx, ry, k, size=10.8, fill=D.MUTED, tracking=.8)
        o += D.text(cx + 190, ry, v, size=10.8, fill=D.LIME, tracking=.5)

    ny = fy + 22 + len(FACTS) * 21 + 14
    o += D.text(cx, ny, 'Original build — no framework,', size=11, fill=D.MUTED)
    o += D.text(cx, ny + 15, 'no trackers, no dependencies.', size=11, fill=D.MUTED)

    ph = ny + 46 - py
    H = py + ph + 12
    frame = (D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
             + D.brackets(px, py, pw, ph, color=D.YELLOW, arm=15, sw=2, corners='tl,tr'))
    return D.doc(W, H, TITLE, DESC, frame + o)
