"""Primary CTA buttons.

Reference: 01_MASTER_STYLE_COMMAND_CENTER.png — icon, title, subtitle, right
chevron, per-button accent colour and corner brackets.

Each button is its own SVG because GitHub can only wrap a whole image in a
link; four buttons therefore need four files.

Responsive strategy
-------------------
A README cannot use CSS, so how many buttons land in a row is decided purely by
each image's intrinsic width against the rendered column. `<picture>` with
width media queries (which GitHub's sanitizer preserves) selects a genuinely
recomposed asset per band.

Columns measured on the real profile page (the avatar sidebar appears around
768px, so the column is NOT viewport minus a constant):

    viewport   320  360  375  390  393  414  430  768  1024  1280  1440
    column     238  278  293  308  311  332  348  383   575   831   846

Markdown whitespace puts a 4px gap between adjacent images, so a band shows
exactly N per row when  N*W + (N-1)*4 <= column  and  (N+1)*W + N*4 > column.
Every band below keeps at least 15px of slack on BOTH sides of that
inequality, so a small difference in a real device's column cannot tip a row
from two buttons to three — which is the defect being fixed.

    <= 375px            xs    112   2 fit / 3 cannot     -> 2 x 2
    376-480px           md    135   2 fit / 3 cannot     -> 2 x 2
    481-900px           tab   175   2 fit / 3 cannot     -> 2 x 2
    1001-1279px         md    135   4 fit                -> 4 x 1
    901-1000, >=1280    wide  198   2 x 2 / 4 x 1

The 198px desktop asset is emitted byte-identically to the accepted version.
"""

import design as D

BUTTONS = [
    ('btn-explore',  'EXPLORE SYSTEMS', 'View projects & systems',   D.CYAN,   D.i_terminal),
    ('btn-overview', 'SYSTEM OVERVIEW', 'Tech stack & architecture', D.GREEN,  D.i_target),
    ('btn-snake',    'PLAY SNAKE',      'Snake Protocol console',    D.YELLOW, D.i_gamepad),
    ('btn-contact',  'GET IN TOUCH',    "Let's connect",             D.BLUE,   D.i_mail),
]


def _n(v):
    """Drop a trailing .0 so integral coordinates stay integers in the output."""
    return int(v) if float(v).is_integer() else v


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
            % (_n(x), _n(y), size, size, size, size, color, sw))


def _stacked(W, H, title, sub, color, icon, icon_px, title_px, sub_px, pad,
             title_y, sub_y, lh):
    """Icon and chevron on the top row, text below.

    Giving the top row to the icon and chevron frees the full card width for
    the text, which is what makes a narrow card readable. Both blocks wrap to
    the measured inner width, so nothing can cross a border.
    """
    inner = W - pad * 2
    o = _frame(W, H, color, 9)
    o += icon(pad, 11, icon_px, color)
    o += _chevron(W - pad - 8, 13, color, sw=2, size=6)

    for i, ln in enumerate(D.wrap(title, D.fit_chars(inner, title_px, 0.5))[:2]):
        o += D.text(pad, title_y + i * (title_px + 2), ln, size=title_px,
                    fill=color, weight='700', tracking=0.5)

    for i, ln in enumerate(D.wrap(sub, D.fit_chars(inner, sub_px))[:2]):
        o += D.text(pad, sub_y + i * lh, ln, size=sub_px, fill=D.MUTED, tracking=0)

    return D.doc(W, H, title, title + '. ' + sub, o, ground=False)


def button(title, sub, color, icon):
    """Default / wide: the accepted desktop button, byte-identical."""
    W, H = 198, 70
    o = _frame(W, H, color, 11)
    o += icon(15, H / 2 - 10, 20, color)
    o += D.text(43, H / 2 - 3, title, size=10.8, fill=color, weight='700', tracking=.65)
    o += D.text(43, H / 2 + 15, sub, size=9.2, fill=D.MUTED, tracking=0)
    o += _chevron(W - 18, H / 2 - 7, color)
    return D.doc(W, H, title, title + '. ' + sub, o, ground=False)


def button_tab(title, sub, color, icon):
    """481-900px: two per row, inline composition with a wrapped subtitle."""
    W, H = 175, 80
    tx = 44
    text_w = W - tx - 26
    o = _frame(W, H, color, 11)
    o += icon(15, H / 2 - 9, 18, color)
    lines = D.wrap(sub, D.fit_chars(text_w, 8.6))[:2]
    shift = 0 if len(lines) < 2 else -5
    o += D.text(tx, H / 2 - 3 + shift, title, size=10.4, fill=color,
                weight='700', tracking=.6)
    for i, ln in enumerate(lines):
        o += D.text(tx, H / 2 + 14 + shift + i * 11, ln, size=8.6, fill=D.MUTED)
    o += _chevron(W - 18, H / 2 - 7, color)
    return D.doc(W, H, title, title + '. ' + sub, o, ground=False)


def button_md(title, sub, color, icon):
    """376-480px (2 up) and 1001-1279px (4 up): one line each, comfortably."""
    return _stacked(135, 80, title, sub, color, icon,
                    icon_px=16, title_px=11, sub_px=8, pad=10,
                    title_y=46, sub_y=64, lh=10)


def button_xs(title, sub, color, icon):
    """<=375px: the tightest phone card. Title and subtitle both wrap in-card."""
    return _stacked(112, 98, title, sub, color, icon,
                    icon_px=15, title_px=10.5, sub_px=7.8, pad=9,
                    title_y=45, sub_y=74, lh=11)


def all_buttons():
    out = {}
    for name, title, sub, color, icon in BUTTONS:
        out[name] = button(title, sub, color, icon)
        out[name + '-xs'] = button_xs(title, sub, color, icon)
        out[name + '-md'] = button_md(title, sub, color, icon)
        out[name + '-tab'] = button_tab(title, sub, color, icon)
    return out
