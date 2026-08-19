"""Primary CTA buttons.

Reference: 01_MASTER_STYLE_COMMAND_CENTER.png — icon, title, subtitle, right
chevron, per-button accent colour and corner brackets.

Each button is its own SVG because GitHub can only wrap a whole image in a
link; four buttons therefore need four files.

Responsive strategy
-------------------
A README cannot use CSS, so the number of buttons per row is decided purely by
each image's intrinsic width against the rendered column. `<picture>` with
width media queries (which GitHub's sanitizer preserves) swaps in a genuinely
recomposed asset per band rather than scaling one asset down — scaling is what
made the phone layout unreadable.

  <= 450px   btn-*-xs.svg   140 wide   two fit, three cannot  -> 2 x 2
  451-660px  btn-*.svg      198 wide   two fit, three cannot  -> 2 x 2
  661-960px  btn-*-md.svg   300 wide   two fit, three cannot  -> 2 x 2
  >= 961px   btn-*.svg      198 wide   all four fit           -> 4 x 1

Each variant is laid out from its own geometry, so the icon column, text block
and arrow inset are computed rather than eyeballed, and all four buttons in a
band are identical in width and height regardless of label length.
"""

import design as D

BUTTONS = [
    ('btn-explore',  'EXPLORE SYSTEMS', 'View projects & systems',   D.CYAN,   D.i_terminal),
    ('btn-overview', 'SYSTEM OVERVIEW', 'Tech stack & architecture', D.GREEN,  D.i_target),
    ('btn-snake',    'PLAY SNAKE',      'Snake Protocol console',    D.YELLOW, D.i_gamepad),
    ('btn-contact',  'GET IN TOUCH',    "Let's connect",             D.BLUE,   D.i_mail),
]


def _frame(W, H, color, arm):
    o = D.panel(1, 1, W - 2, H - 2, fill=D.SURFACE_2, stroke=color, sw=1.5)
    o += ('    <rect x="1" y="1" width="4" height="%d" fill="%s" opacity="0.9"/>\n'
          % (H - 2, color))
    o += D.brackets(1, 1, W - 2, H - 2, color=color, arm=arm, sw=1.6,
                    corners='tl,br', opacity=0.5)
    return o


def _chevron(x, y, color, sw=2.2, size=7):
    return ('    <path d="M%s %s l%s %s l-%s %s" fill="none" stroke="%s" '
            'stroke-width="%s" stroke-linecap="square" opacity="0.85"/>\n'
            % (x, y, size, size, size, size, color, sw))


def button(title, sub, color, icon):
    """Desktop / default: four across GitHub's ~896px README column."""
    W, H = 198, 70
    o = _frame(W, H, color, 11)
    o += icon(15, H / 2 - 10, 20, color)
    o += D.text(43, H / 2 - 3, title, size=10.8, fill=color, weight='700', tracking=.65)
    o += D.text(43, H / 2 + 15, sub, size=9.2, fill=D.MUTED, tracking=0)
    o += _chevron(W - 18, H / 2 - 7, color)
    return D.doc(W, H, title, title + '. ' + sub, o, ground=False)


def button_md(title, sub, color, icon):
    """Tablet: two across, with room to breathe."""
    W, H = 300, 80
    o = _frame(W, H, color, 12)
    o += icon(20, H / 2 - 13, 26, color)
    o += D.text(60, H / 2 - 3, title, size=13, fill=color, weight='700', tracking=1.1)
    o += D.text(60, H / 2 + 17, sub, size=10, fill=D.MUTED, tracking=0)
    o += _chevron(W - 24, H / 2 - 8, color, sw=2.4, size=8)
    return D.doc(W, H, title, title + '. ' + sub, o, ground=False)


def button_xs(title, sub, color, icon):
    """Phone: a genuinely different composition, not the wide one shrunk.

    The icon and chevron take the top row so the full card width is available
    to the text, and the subtitle wraps to the measured inner width instead of
    running past the border.
    """
    W, H = 140, 92
    pad = 12
    inner = W - pad * 2                      # 116px of usable text width

    o = _frame(W, H, color, 9)
    o += icon(pad, 12, 18, color)
    o += _chevron(W - 22, 14, color, sw=2, size=6)

    o += D.text(pad, 50, title, size=11, fill=color, weight='700', tracking=.7)

    sub_size = 8.5
    for i, ln in enumerate(D.wrap(sub, D.fit_chars(inner, sub_size))[:2]):
        o += D.text(pad, 66 + i * 12, ln, size=sub_size, fill=D.MUTED, tracking=0)

    return D.doc(W, H, title, title + '. ' + sub, o, ground=False)


def all_buttons():
    out = {}
    for name, title, sub, color, icon in BUTTONS:
        out[name] = button(title, sub, color, icon)
        out[name + '-md'] = button_md(title, sub, color, icon)
        out[name + '-xs'] = button_xs(title, sub, color, icon)
    return out
