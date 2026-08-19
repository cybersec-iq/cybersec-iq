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
recomposed asset per band — scaling one asset down is what made the phone
layout unreadable.

The bands come from measuring the real profile page, not from guesswork. The
column is NOT viewport minus a constant: the avatar sidebar appears around
768px, so the column actually shrinks relative to the viewport there.

    viewport   320  390  430  768  1024  1200  1440
    column     238  308  348  383   575   751   846
    inter-image gap from Markdown whitespace: 4px

A band shows exactly N buttons per row when N*W + (N-1)*4 <= column and
(N+1)*W + N*4 > column. No single width satisfies that across a 3.5x column
range, which is why there are four tiers:

    <= 430px          xs    116 wide   2 fit, 3 cannot   -> 2 x 2
    431-900px         sm    170 wide   2 fit, 3 cannot   -> 2 x 2
    1001-1279px       md    134 wide   4 fit             -> 4 x 1
    901-1000, >=1280  wide  198 wide   2 x 2 / 4 x 1

Within each tier all four buttons are a fixed size, so a longer label can never
make one card bigger than its neighbours.
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


def _stacked(W, H, title, sub, color, icon, icon_px, title_px, sub_px, pad,
             title_y, sub_y, lh):
    """Icon and chevron on the top row, text below.

    Giving the top row to the icon and chevron frees the full card width for
    the text, which is what makes a narrow card readable. Both text blocks wrap
    to the measured inner width, so nothing can cross a border.
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


def _inline(W, H, title, sub, color, icon, icon_px, title_px, sub_px):
    """Icon left, text centre, chevron right — the wide/tablet composition."""
    tx = 20 + icon_px + 8
    text_w = W - tx - 26                      # keep clear of the chevron
    o = _frame(W, H, color, 11)
    o += icon(15, H / 2 - icon_px / 2, icon_px, color)
    lines = D.wrap(sub, D.fit_chars(text_w, sub_px))[:2]
    shift = 0 if len(lines) < 2 else -5
    o += D.text(tx, H / 2 - 3 + shift, title, size=title_px, fill=color,
                weight='700', tracking=.65)
    for i, ln in enumerate(lines):
        o += D.text(tx, H / 2 + 15 + shift + i * (sub_px + 2), ln,
                    size=sub_px, fill=D.MUTED, tracking=0)
    o += _chevron(W - 18, H / 2 - 7, color)
    return D.doc(W, H, title, title + '. ' + sub, o, ground=False)


def button(title, sub, color, icon):
    """Default / wide: the accepted desktop button, unchanged."""
    return _inline(198, 70, title, sub, color, icon, 20, 10.8, 9.2)


def button_sm(title, sub, color, icon):
    """431-900px: two per row, still an inline composition."""
    return _inline(170, 78, title, sub, color, icon, 18, 10.4, 8.6)


def button_md(title, sub, color, icon):
    """1001-1279px: compact enough that four fit the 575-751px column."""
    return _stacked(134, 80, title, sub, color, icon,
                    icon_px=16, title_px=11, sub_px=8, pad=10,
                    title_y=46, sub_y=64, lh=10)


def button_xs(title, sub, color, icon):
    """<=430px: the phone card. Title and subtitle both wrap in-card."""
    return _stacked(116, 100, title, sub, color, icon,
                    icon_px=16, title_px=11, sub_px=8, pad=10,
                    title_y=46, sub_y=76, lh=11)


def all_buttons():
    out = {}
    for name, title, sub, color, icon in BUTTONS:
        out[name] = button(title, sub, color, icon)
        out[name + '-sm'] = button_sm(title, sub, color, icon)
        out[name + '-md'] = button_md(title, sub, color, icon)
        out[name + '-xs'] = button_xs(title, sub, color, icon)
    return out
