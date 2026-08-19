"""Closing quote strip and status bar.

Reference: 05_PLAY_SNAKE_CONTACT_REFERENCE.png — the dotted quote panel with
oversized quote marks and coloured keywords, plus the bottom status strip.

Data integrity: the reference's status strip shows LOCAL TIME, UPTIME 7D 14H 32M
and FOCUS MODE. A static README image cannot measure any of that, and inventing
it would be fake telemetry. The strip keeps the reference's visual rhythm but
carries only verifiable facts: the owner's timezone, the repository licence, the
source path, and the UI theme name.
"""

import design as D

QUOTE = [('Code', D.GREEN), (' is my craft.  ', D.TEXT),
         ('Security', D.CYAN), (' is my mindset.  ', D.TEXT),
         ('Impact', D.YELLOW), (' is the goal.', D.TEXT)]

FACTS = [
    (D.i_clock,  'TIME ZONE', 'Asia/Muscat (UTC+4)', D.TEXT),
    (D.i_grid,   'UI THEME',  'CYBERSEC-IQ',         D.CYAN),
    (D.i_lock,   'LICENCE',   'MIT',                 D.GREEN),
    (D.i_repo,   'SOURCE',    'cybersec-iq', D.TEXT),
]

DESC = ('Closing strip. Code is my craft. Security is my mindset. Impact is the goal. '
        'Time zone Asia/Muscat UTC+4. UI theme cybersec-iq. Licence MIT. '
        'Source cybersec-iq/cybersec-iq. Nothing is impossible.')
TITLE = 'footer - nothing is impossible'


def wide():
    W, H = 1200, 224
    px, pw = 22, 1200 - 44

    o = D.quote_strip(px, 16, pw, 86, QUOTE)
    o += D.dot_field(px + 26, 40, 7, 5, step=7, color=D.YELLOW_DIM, r=1.5, opacity=0.55)
    o += D.dot_field(px + pw - 74, 40, 7, 5, step=7, color=D.YELLOW_DIM, r=1.5, opacity=0.55)

    sy, sh = 118, 62
    o += D.panel(px, sy, pw, sh, fill=D.SURFACE, stroke=D.LINE_2)
    step = (pw - 300) / len(FACTS)
    for i, (icon, k, v, col) in enumerate(FACTS):
        ox = px + 26 + i * step
        if i:
            o += D.vline(ox - 20, sy + 14, sh - 28, D.LINE)
        o += icon(ox, sy + 20, 20, D.CYAN_DIM)
        o += D.label(ox + 30, sy + 26, k, size=10.5, fill=D.MUTED, tracking=2)
        o += D.text(ox + 30, sy + 45, v, size=12.5, fill=col, tracking=0.6)

    tx = px + pw - 290
    o += D.panel(tx, sy + 10, 280, sh - 20, fill=D.SURFACE_2, stroke=D.GREEN, sw=1.1)
    o += D.i_terminal(tx + 14, sy + 21, 20, D.GREEN)
    o += D.text(tx + 44, sy + 30, 'cybersec-iq:~$ whoami', size=11.5, fill=D.GREEN)
    o += D.text(tx + 44, sy + 46, 'Aryan IQ — Full-Stack Developer', size=11, fill=D.MUTED)

    o += D.text(W / 2 - D.tw('NOTHING IS IMPOSSIBLE.', 15, 4.5) / 2, 206,
                'NOTHING IS IMPOSSIBLE.', size=15, fill=D.GREEN, weight='700',
                tracking=4.5, filt='glowSm')
    return D.doc(W, H, TITLE, DESC, o)


def narrow():
    W = 440
    px, pw = 10, 420

    parts = [('Code', D.GREEN), (' is my craft.', D.TEXT)]
    o = D.panel(px, 14, pw, 96, fill=D.SURFACE, stroke=D.LINE_2)
    o += ('    <g fill="%s" opacity="0.6" font-size="34" font-weight="700">'
          '<text x="%d" y="%d">&#8220;</text></g>\n' % (D.GREEN_DIM, px + 16, 52))
    lines = [[('Code', D.GREEN), (' is my craft.', D.TEXT)],
             [('Security', D.CYAN), (' is my mindset.', D.TEXT)],
             [('Impact', D.YELLOW), (' is the goal.', D.TEXT)]]
    # One flowed <text> per line. Advancing x per phrase needs the viewer's
    # exact glyph metrics, and when the real font is wider than the estimate
    # the phrases collide - that is what produced "Codeis my craft.".
    for i, runs in enumerate(lines):
        o += D.rich(px + 46, 42 + i * 22, runs, size=13, tracking=0,
                    weight_for=lambda c: None if c == D.TEXT else '600')

    sy = 122
    rowh = 30
    o += D.panel(px, sy, pw, rowh * len(FACTS) + 12, fill=D.SURFACE, stroke=D.LINE_2)
    for i, (icon, k, v, col) in enumerate(FACTS):
        ry = sy + 12 + i * rowh
        o += icon(px + 16, ry + 2, 16, D.CYAN_DIM)
        o += D.label(px + 40, ry + 14, k, size=10, fill=D.MUTED, tracking=1.6)
        o += D.text(px + 150, ry + 14, v, size=11, fill=col)

    fy = sy + rowh * len(FACTS) + 34
    o += D.text(W / 2 - D.tw('NOTHING IS IMPOSSIBLE.', 12.5, 2.6) / 2, fy,
                'NOTHING IS IMPOSSIBLE.', size=12.5, fill=D.GREEN, weight='700',
                tracking=2.6, filt='glowSm')
    return D.doc(W, fy + 16, TITLE, DESC, o)
