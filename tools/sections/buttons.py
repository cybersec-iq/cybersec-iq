"""Primary CTA buttons.

Reference: 01_MASTER_STYLE_COMMAND_CENTER.png — icon, title, subtitle, right
chevron, per-button accent colour and corner brackets.

Each button is its own SVG because GitHub can only wrap a whole image in a
link; four buttons therefore need four files. Every destination below resolves:
two in-README anchors, the live Pages game, and the verified website.
"""

import design as D

BUTTONS = [
    ('btn-explore',  'EXPLORE SYSTEMS', 'View projects & systems',   D.CYAN,   D.i_terminal),
    ('btn-overview', 'SYSTEM OVERVIEW', 'Tech stack & architecture', D.GREEN,  D.i_target),
    ('btn-snake',    'PLAY SNAKE',      'Snake Protocol console',    D.YELLOW, D.i_gamepad),
    ('btn-contact',  'GET IN TOUCH',    "Let's connect",             D.BLUE,   D.i_mail),
]


def button(title, sub, color, icon):
    # Four 198px assets plus Markdown whitespace fit GitHub's ~831px desktop
    # README column in one row. At phone widths two cannot fit side by side,
    # so normal inline wrapping produces a readable single column.
    W, H = 198, 70
    o = D.panel(1, 1, W - 2, H - 2, fill=D.SURFACE_2, stroke=color, sw=1.5)
    o += ('    <rect x="1" y="1" width="4" height="%d" fill="%s" opacity="0.9"/>\n'
          % (H - 2, color))
    o += D.brackets(1, 1, W - 2, H - 2, color=color, arm=11, sw=1.6,
                    corners='tl,br', opacity=0.5)
    o += icon(15, H / 2 - 10, 20, color)
    o += D.text(43, H / 2 - 3, title, size=10.8, fill=color, weight='700', tracking=.65)
    o += D.text(43, H / 2 + 15, sub, size=9.2, fill=D.MUTED, tracking=0)
    o += ('    <path d="M%d %d l7 7 l-7 7" fill="none" stroke="%s" stroke-width="2.2" '
          'stroke-linecap="square" opacity="0.85"/>\n' % (W - 18, H / 2 - 7, color))
    return D.doc(W, H, title, title + '. ' + sub, o, ground=False)


def all_buttons():
    return {name: button(title, sub, color, icon)
            for name, title, sub, color, icon in BUTTONS}
