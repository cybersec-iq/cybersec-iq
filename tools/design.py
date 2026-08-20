"""cybersec-iq — shared SVG design system.

Every generated asset in this repository is emitted through this module, so the
hero, whoami, stack, systems, activity, snake frame, contact and footer cannot
drift into looking like unrelated templates. Tokens and primitives live here;
the builders only compose them.

Zero dependencies: standard library only.
"""

# --------------------------------------------------------------------------
# tokens
# --------------------------------------------------------------------------

VOID      = '#03070A'   # page ground
SURFACE   = '#050D13'   # panel fill
SURFACE_2 = '#08141C'   # raised panel / tile fill
SURFACE_3 = '#0B1A23'   # title bars

LINE      = '#12242E'   # hairline
LINE_2    = '#1B3541'   # visible border
LINE_3    = '#284653'   # strong border

GREEN     = '#39FF14'
GREEN_HI  = '#48FF24'
GREEN_DIM = '#1B7A10'
GREEN_DEEP= '#0C3A08'

CYAN      = '#00E5FF'
CYAN_2    = '#00CFE8'
CYAN_DIM  = '#0A6C7C'
CYAN_DEEP = '#04303A'

YELLOW    = '#FFE600'
LIME      = '#DFFF00'
YELLOW_DIM= '#6E6300'

BLUE      = '#2979FF'
BLUE_DIM  = '#1A3E7A'

TEXT      = '#C3CDD6'
TEXT_HI   = '#EAF2F7'
MUTED     = '#6E828F'
FAINT     = '#3A4C58'

MONO = ('ui-monospace, "JetBrains Mono", "IBM Plex Mono", "Space Mono", '
        '"SFMono-Regular", Menlo, Consolas, monospace')

# Monospace advance width as a fraction of font-size. Used for chip sizing and
# manual centring, since SVG cannot measure text.
ADV = 0.60


def tw(text, size, tracking=0.0):
    """Approximate rendered width of monospace text."""
    n = len(text)
    return n * size * ADV + max(0, n - 1) * tracking


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


# --------------------------------------------------------------------------
# document scaffolding
# --------------------------------------------------------------------------

def defs(extra='', reduce_classes=()):
    """Shared gradients, patterns, filters and motion rules."""
    rm = ', '.join('.' + c for c in reduce_classes) if reduce_classes else '.noop'
    return f'''  <defs>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="{LINE}" stroke-width="1"/>
    </pattern>
    <pattern id="grid-fine" width="10" height="10" patternUnits="userSpaceOnUse">
      <path d="M10 0H0V10" fill="none" stroke="#0B1820" stroke-width="0.7"/>
    </pattern>
    <pattern id="scan" width="3" height="3" patternUnits="userSpaceOnUse">
      <rect width="3" height="1" fill="{CYAN}" opacity="0.035"/>
    </pattern>
    <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{SURFACE_3}"/><stop offset="100%" stop-color="{SURFACE}"/>
    </linearGradient>
    <linearGradient id="ruleGreen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{GREEN}" stop-opacity="0.95"/>
      <stop offset="55%" stop-color="{CYAN}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{CYAN}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="ruleCyan" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{CYAN}" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="{CYAN}" stop-opacity="0"/>
    </linearGradient>
    <filter id="glowSm" x="-40%" y="-80%" width="180%" height="260%">
      <feGaussianBlur stdDeviation="1.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glowMd" x="-40%" y="-80%" width="180%" height="260%">
      <feGaussianBlur stdDeviation="3.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glowLg" x="-35%" y="-70%" width="170%" height="240%">
      <feGaussianBlur stdDeviation="6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
{extra}    <style>
      .m {{ font-family: {MONO}; }}
      .blink {{ animation: blink 1.15s steps(1) infinite; }}
      .live  {{ animation: live 2.8s ease-in-out infinite; }}
      .flow  {{ stroke-dasharray: 4 8; animation: flow 3.2s linear infinite; }}
      .rise  {{ animation: rise .55s ease-out both; }}
      @keyframes blink {{ 0%,49% {{ opacity: 1; }} 50%,100% {{ opacity: 0; }} }}
      @keyframes live  {{ 0%,100% {{ opacity: .38; }} 50% {{ opacity: 1; }} }}
      @keyframes flow  {{ to {{ stroke-dashoffset: -24; }} }}
      @keyframes rise  {{ from {{ opacity: 0; transform: translateY(7px); }}
                          to {{ opacity: 1; transform: translateY(0); }} }}
      @media (prefers-reduced-motion: reduce) {{
        .blink, .live, .flow, .rise{', ' + rm if reduce_classes else ''} {{ animation: none; }}
      }}
    </style>
  </defs>
'''


def doc(width, height, title, desc, body, extra_defs='', ground=True):
    """Wrap a composed body in a complete, validating SVG document."""
    bg = ''
    if ground:
        bg = (f'    <rect width="{width}" height="{height}" fill="{VOID}"/>\n'
              f'    <rect width="{width}" height="{height}" fill="url(#grid)" opacity="0.5"/>\n'
              f'    <rect width="{width}" height="{height}" fill="url(#scan)"/>\n')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="t d" preserveAspectRatio="xMidYMid meet">
  <title id="t">{esc(title)}</title>
  <desc id="d">{esc(desc)}</desc>
{defs(extra_defs)}  <g class="m">
{bg}{body}  </g>
</svg>
'''


# --------------------------------------------------------------------------
# panel geometry
# --------------------------------------------------------------------------

def panel(x, y, w, h, fill=SURFACE, stroke=LINE_2, rx=3, sw=1.2, opacity=1.0):
    return (f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{sw}"/>\n')


def notch(x, y, w, h, cut=12, fill=SURFACE, stroke=LINE_2, sw=1.2):
    """HUD panel with clipped top-left and bottom-right corners."""
    p = (f'M{x + cut} {y} H{x + w} V{y + h - cut} L{x + w - cut} {y + h} '
         f'H{x} V{y + cut} Z')
    return f'    <path d="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'


def brackets(x, y, w, h, color=YELLOW, arm=16, sw=2, corners='tl,br', opacity=0.85):
    """Corner brackets. The reference uses yellow, asymmetrically placed."""
    seg = []
    if 'tl' in corners: seg.append(f'M{x} {y + arm} V{y} H{x + arm}')
    if 'tr' in corners: seg.append(f'M{x + w - arm} {y} H{x + w} V{y + arm}')
    if 'bl' in corners: seg.append(f'M{x} {y + h - arm} V{y + h} H{x + arm}')
    if 'br' in corners: seg.append(f'M{x + w - arm} {y + h} H{x + w} V{y + h - arm}')
    if not seg:
        return ''
    return (f'    <g stroke="{color}" stroke-width="{sw}" fill="none" '
            f'opacity="{opacity}">' + ''.join(f'<path d="{d}"/>' for d in seg) + '</g>\n')


def rule(x, y, w, grad='ruleGreen', h=1.5):
    return f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{grad})"/>\n'


def hline(x, y, w, color=LINE_2, h=1):
    return f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>\n'


def vline(x, y, h, color=LINE, w=1):
    return f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>\n'


# --------------------------------------------------------------------------
# text
# --------------------------------------------------------------------------

def text(x, y, s, size=14, fill=TEXT, weight=None, tracking=None,
         anchor=None, opacity=None, cls=None, filt=None, style=None,
         preserve=False):
    a = [f'x="{x}"', f'y="{y}"', f'font-size="{size}"', f'fill="{fill}"']
    if preserve:
        # SVG collapses runs of whitespace; keep them when the spacing is
        # deliberate (letterspaced wordmarks, aligned separators).
        a.append('xml:space="preserve"')
    if weight:   a.append(f'font-weight="{weight}"')
    if tracking is not None: a.append(f'letter-spacing="{tracking}"')
    if anchor:   a.append(f'text-anchor="{anchor}"')
    if opacity is not None:  a.append(f'opacity="{opacity}"')
    if cls:      a.append(f'class="{cls}"')
    if filt:     a.append(f'filter="url(#{filt})"')
    if style:    a.append(f'style="{style}"')
    return f'    <text {" ".join(a)}>{esc(s)}</text>\n'


def label(x, y, s, size=11, fill=MUTED, tracking=2.6, **kw):
    """Small letterspaced system label."""
    return text(x, y, s, size=size, fill=fill, tracking=tracking, **kw)


def rich(x, y, runs, size=14, tracking=0.3, anchor=None, weight_for=None):
    """Multi-colour inline text as ONE <text> with <tspan> children.

    Manually advancing x per run would need the viewer's exact monospace
    metrics, which differ between JetBrains Mono (0.60 advance) and Consolas
    (0.55). Letting tspans flow removes the guesswork, so coloured phrases
    never drift apart mid-sentence on someone else's machine.
    """
    a = ['x="%s"' % x, 'y="%s"' % y, 'font-size="%s"' % size,
         'letter-spacing="%s"' % tracking,
         # Without this a leading space in a tspan can be collapsed away and
         # adjacent phrases render welded together ("Codeis my craft.").
         'xml:space="preserve"']
    if anchor:
        a.append('text-anchor="%s"' % anchor)
    parts = []
    for item in runs:
        s, col = item[0], item[1]
        w = item[2] if len(item) > 2 else (weight_for(col) if weight_for else None)
        attrs = 'fill="%s"' % col
        if w:
            attrs += ' font-weight="%s"' % w
        parts.append('<tspan %s>%s</tspan>' % (attrs, esc(s)))
    return '    <text %s>%s</text>\n' % (' '.join(a), ''.join(parts))


def wrap(s, max_chars):
    """Greedy word wrap. Used where copy has to fit a fixed card width."""
    words, lines, cur = str(s).split(), [], ''
    for w in words:
        cand = (cur + ' ' + w).strip()
        if len(cand) <= max_chars or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_chars(width, size, tracking=0.0):
    """How many monospace characters fit in `width` at `size`."""
    adv = size * ADV + tracking
    return max(1, int(width / adv))


def paras(x, y, lines, size=14, fill=TEXT, lh=22, tracking=0.2):
    out = ''
    for i, ln in enumerate(lines):
        out += text(x, y + i * lh, ln, size=size, fill=fill, tracking=tracking)
    return out


# --------------------------------------------------------------------------
# components
# --------------------------------------------------------------------------

def name_lockup(x, y, first, second, size, tracking, c1=GREEN, c2=CYAN,
                caret=True, caret_color=None, filt='glowLg'):
    """ARYAN IQ with a trailing block caret, as one flowed text.

    The two words and the caret ride the same text flow, so none of them needs
    an x estimated from font metrics - which is what previously risked the
    caret landing on top of the last glyph on a wider font.
    """
    runs = [(first, c1), (' ', c1), (second, c2)]
    body = rich(x, y, runs, size=size, tracking=tracking,
                weight_for=lambda c: '700')
    if not caret:
        return body if not filt else body.replace('<text ', '<text filter="url(#%s)" ' % filt, 1)
    # the caret is a separate tspan so it can blink on its own
    a = ['x="%s"' % x, 'y="%s"' % y, 'font-size="%s"' % size,
         'letter-spacing="%s"' % tracking, 'xml:space="preserve"']
    if filt:
        a.append('filter="url(#%s)"' % filt)
    parts = ['<tspan fill="%s" font-weight="700">%s</tspan>' % (c1, esc(first)),
             '<tspan fill="%s" font-weight="700"> </tspan>' % c1,
             '<tspan fill="%s" font-weight="700">%s</tspan>' % (c2, esc(second)),
             '<tspan fill="%s" font-weight="700" class="blink">█</tspan>'
             % (caret_color or c2)]
    return '    <text %s>%s</text>\n' % (' '.join(a), ''.join(parts))


def status_dot(x, y, color=GREEN, r=4.5, animate=True):
    c = ' class="live"' if animate else ''
    return f'    <circle cx="{x}" cy="{y}" r="{r}" fill="{color}"{c}/>\n'


def caret(x, y, w=13, h=30, color=GREEN, animate=True):
    c = ' class="blink"' if animate else ''
    return (f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"'
            f'{c} filter="url(#glowSm)"/>\n')


def chip(x, y, s, color=CYAN, size=12.5, pad=11, h=25, fill=None, tracking=0.6):
    """Bordered technology chip. Returns (svg, width)."""
    w = tw(s, size, tracking) + pad * 2
    bg = fill if fill else SURFACE_2
    out = (f'    <rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="2" '
           f'fill="{bg}" stroke="{color}" stroke-width="1" stroke-opacity="0.55"/>\n')
    out += text(x + pad, y + h / 2 + size * 0.36, s, size=size, fill=color, tracking=tracking)
    return out, w


def chip_row(x, y, items, size=12.5, gap=8, h=25, max_w=None, lh=33):
    """Lay chips out left to right, wrapping when max_w is exceeded."""
    out, cx, cy, rows = '', x, y, 1
    for s, color in items:
        w = tw(s, size, 0.6) + 22
        if max_w and cx > x and cx + w > x + max_w:
            cx, cy, rows = x, cy + lh, rows + 1
        c, w = chip(cx, cy, s, color, size=size, h=h)
        out += c
        cx += w + gap
    return out, rows, cy + h


def prompt_bar(x, y, w, cmd='', h=44, user='cybersec-iq@github', path=':~$',
               size=15, cursor=True):
    """The terminal prompt strip used as a section separator."""
    out = panel(x, y, w, h, fill='#040F16', stroke=LINE_2)
    ty = y + h / 2 + size * 0.36
    out += text(x + 18, ty, user, size=size, fill=GREEN, weight='600')
    ux = x + 18 + tw(user, size)
    out += text(ux, ty, path, size=size, fill=CYAN)
    cx = ux + tw(path, size) + 10
    if cmd:
        out += text(cx, ty, cmd, size=size, fill=TEXT)
        cx += tw(cmd, size) + 10
    if cursor:
        out += (f'    <rect x="{cx:.1f}" y="{y + h / 2 - size * 0.55:.1f}" width="{size * 0.6:.1f}" '
                f'height="{size * 1.1:.1f}" fill="{GREEN}" class="blink"/>\n')
    return out


def tab(x, y, s, w=None, h=30, color=CYAN, size=15):
    """Angled tab label attached to the top edge of a panel (ref 02 / 06)."""
    w = w or tw(s, size, 1.2) + 34
    p = f'M{x} {y + h} V{y + 6} L{x + 6} {y} H{x + w - 14} L{x + w} {y + h} Z'
    out = (f'    <path d="{p}" fill="{SURFACE_3}" stroke="{color}" '
           f'stroke-width="1.2" stroke-opacity="0.6"/>\n')
    out += text(x + 16, y + h / 2 + size * 0.36, s, size=size, fill=color,
                weight='600', tracking=1.2)
    return out


def section_header(x, y, path_label, sub, right=None, right_icon=None,
                   w=None, accent=YELLOW):
    """`>_  ~/stack` + subtitle, with an optional right-hand system label."""
    out = ''
    # prompt glyph in a bracket box
    out += (f'    <rect x="{x}" y="{y - 22}" width="34" height="30" rx="2" fill="{SURFACE_2}" '
            f'stroke="{GREEN}" stroke-width="1.2" stroke-opacity="0.5"/>\n')
    out += (f'    <g stroke="{GREEN}" stroke-width="2" fill="none" stroke-linecap="square">'
            f'<path d="M{x + 9} {y - 15} l6 6 l-6 6"/><path d="M{x + 18} {y + 1} h8"/></g>\n')
    out += text(x + 48, y + 4, path_label, size=27, fill=accent, weight='700', tracking=0.6)
    out += label(x + 49, y + 26, sub, size=11.5, fill=MUTED, tracking=3)
    if right and w:
        rx = x + w
        out += label(rx, y - 2, right, size=11.5, fill=CYAN_DIM, tracking=3, anchor='end')
        if right_icon:
            out += right_icon(rx - tw(right, 11.5, 3) - 26, y - 13, 15, CYAN_DIM)
    return out


def metric_tile(x, y, w, h, label_s, value, note, color, icon=None,
                pad=16, icon_px=16, label_px=10.5, value_px=34, note_px=10,
                glow=None):
    """Activity metric tile (ref 04), laid out as a fixed vertical rhythm:

        pad -> icon + label row -> gap -> number -> gap -> meta -> pad

    `glow` is None by default. A Gaussian halo behind a numeral survives fine
    at desktop size, but these tiles are downscaled on a phone, where the halo
    compresses into the glyph and reads as blur. Crisp fill on a dark tile is
    already bright enough.
    """
    out = panel(x, y, w, h, fill=SURFACE_2, stroke=color, sw=1.2)
    out += f'    <rect x="{x}" y="{y}" width="{w}" height="2.5" fill="{color}" opacity="0.85"/>\n'

    row_y = y + pad + icon_px * 0.78          # baseline of the label row
    ix = x + pad
    if icon:
        out += icon(ix, y + pad, icon_px, color)
        ix += icon_px + 8
    out += label(ix, row_y, label_s, size=label_px, fill=MUTED, tracking=1.6)

    out += text(x + pad, row_y + 10 + value_px * 0.74, str(value), size=value_px,
                fill=color, weight='700', tracking=0.5, filt=glow)
    out += label(x + pad, h + y - pad + 2, note, size=note_px, fill=FAINT, tracking=1.5)
    return out


def cta_button(x, y, w, h, title, sub, color, icon=None, chevron=True):
    """Rich CTA button (ref 01)."""
    out = panel(x, y, w, h, fill=SURFACE_2, stroke=color, sw=1.4)
    out += brackets(x, y, w, h, color=color, arm=10, sw=1.6, corners='tl,br', opacity=0.5)
    tx = x + 20
    if icon:
        out += icon(x + 18, y + h / 2 - 11, 22, color)
        tx = x + 52
    out += text(tx, y + h / 2 - 2, title, size=14.5, fill=color, weight='700', tracking=1.6)
    out += text(tx, y + h / 2 + 18, sub, size=12, fill=MUTED, tracking=0.4)
    if chevron:
        cx, cy = x + w - 24, y + h / 2
        out += (f'    <path d="M{cx} {cy - 6} l6 6 l-6 6" fill="none" stroke="{color}" '
                f'stroke-width="2" stroke-linecap="square" opacity="0.8"/>\n')
    return out


def kv_row(x, y, w, key, value, color_v=TEXT, icon=None, size=15, key_w=150):
    out = ''
    kx = x
    if icon:
        out += icon(x, y - 13, 17, CYAN)
        kx = x + 28
    out += text(kx, y, key, size=size, fill=CYAN, tracking=2.2)
    out += text(x + key_w, y, ':', size=size, fill=FAINT)
    out += text(x + key_w + 26, y, value, size=size, fill=color_v, tracking=1.4, weight='600')
    return out


def quote_strip(x, y, w, h, parts):
    """Footer quote with coloured key words and large quote marks (ref 05)."""
    out = panel(x, y, w, h, fill=SURFACE, stroke=LINE_2)
    out += f'''    <g fill="{GREEN_DIM}" opacity="0.65" font-size="46" class="m" font-weight="700">
      <text x="{x + 26}" y="{y + h / 2 + 6}">&#8220;</text>
      <text x="{x + w - 52}" y="{y + h / 2 + 6}">&#8221;</text>
    </g>\n'''
    # Centred as a single flowed text so the colour runs stay joined whatever
    # monospace face the viewer has.
    out += rich(x + w / 2, y + h / 2 + 6, parts, size=17, tracking=1.1,
                anchor='middle', weight_for=lambda c: None if c == TEXT else '600')
    return out


# --------------------------------------------------------------------------
# decorative motifs
# --------------------------------------------------------------------------

# Simplified continent outlines in longitude/latitude pairs. These deliberate
# silhouettes replace the old rectangular land boxes, so the Americas,
# Europe/Africa, Asia and Australia remain recognizable even at README scale.
_LAND = [
    # North America
    [(-168, 70), (-145, 72), (-126, 61), (-110, 58), (-98, 50), (-82, 48),
     (-60, 53), (-52, 46), (-67, 40), (-80, 26), (-97, 17), (-110, 22),
     (-117, 32), (-128, 48), (-151, 58)],
    # Central America
    [(-101, 22), (-86, 22), (-77, 8), (-88, 8)],
    # Greenland
    [(-55, 82), (-23, 80), (-19, 63), (-43, 59), (-62, 69)],
    # South America
    [(-81, 12), (-66, 10), (-50, 2), (-35, -8), (-45, -23), (-52, -35),
     (-66, -55), (-73, -42), (-76, -20)],
    # Europe
    [(-11, 36), (-10, 52), (1, 59), (18, 70), (32, 67), (40, 53),
     (29, 42), (13, 36)],
    # Africa
    [(-18, 35), (9, 37), (34, 31), (51, 12), (42, -12), (31, -34),
     (16, -35), (2, -18), (-10, 4)],
    # Asia
    [(28, 41), (38, 55), (61, 72), (103, 76), (145, 70), (179, 63),
     (170, 49), (143, 39), (130, 23), (109, 19), (103, 5), (91, 9),
     (79, 23), (63, 26), (50, 40)],
    # Arabian peninsula / India / SE Asia
    [(35, 31), (59, 29), (57, 12), (46, 12)],
    [(67, 29), (90, 28), (79, 7), (72, 8)],
    [(92, 23), (122, 20), (142, 2), (123, -10), (101, 1)],
    # Japan
    [(130, 45), (145, 43), (142, 30), (132, 32)],
    # Australia and New Zealand
    [(112, -11), (132, -10), (154, -22), (150, -39), (127, -43), (114, -31)],
    [(165, -34), (179, -38), (176, -48), (168, -45)],
]


def _inside_polygon(lon, lat, polygon):
    inside = False
    j = len(polygon) - 1
    for i, (xi, yi) in enumerate(polygon):
        xj, yj = polygon[j]
        if ((yi > lat) != (yj > lat)):
            cross = (xj - xi) * (lat - yi) / ((yj - yi) or 1e-9) + xi
            if lon < cross:
                inside = not inside
        j = i
    return inside


def world_map(x, y, w, h, dot=1.7, step=9, color=GREEN, opacity=0.5):
    """Dotted continents on an equirectangular projection."""
    out = [f'    <g fill="{color}" opacity="{opacity}">']
    cols = max(1, int(w / step))
    rows = max(1, int(h / step))
    for r in range(rows + 1):
        lat = 78 - (r / rows) * 134          # 78N .. 56S
        for c in range(cols + 1):
            lon = -180 + (c / cols) * 360
            for polygon in _LAND:
                if _inside_polygon(lon, lat, polygon):
                    # deterministic thinning gives a ragged coastline
                    if ((c * 7 + r * 13) % 12) < 9:
                        out.append(f'<circle cx="{x + c * step:.0f}" cy="{y + r * step:.0f}" r="{dot}"/>')
                    break
    out.append('</g>')
    return ''.join(out) + '\n'


def node_web(x, y, w, h, nodes, links, colors=(GREEN, CYAN, LIME)):
    """Connected node constellation drawn over the map."""
    pts = [(x + u * w, y + v * h) for u, v in nodes]
    out = f'    <g stroke="{CYAN}" stroke-width="1" fill="none" opacity="0.4">'
    for a, b in links:
        out += f'<path class="flow" d="M{pts[a][0]:.0f} {pts[a][1]:.0f} L{pts[b][0]:.0f} {pts[b][1]:.0f}"/>'
    out += '</g>\n'
    out += '    <g>'
    for i, (px, py) in enumerate(pts):
        c = colors[i % len(colors)]
        out += (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="3.2" fill="{c}" class="live" '
                f'style="animation-delay:{-0.4 * i:.1f}s"/>')
    out += '</g>\n'
    return out


def signal_bars(x, y, color=CYAN, n=4, opacity=0.7):
    out = f'    <g fill="{color}" opacity="{opacity}">'
    for i in range(n):
        out += f'<rect x="{x + i * 5}" y="{y - 3 - i * 4}" width="3" height="{4 + i * 4}"/>'
    return out + '</g>\n'


def dot_field(x, y, cols, rows, step=7, color=GREEN_DIM, r=1.4, opacity=0.6):
    out = f'    <g fill="{color}" opacity="{opacity}">'
    for c in range(cols):
        for rw in range(rows):
            out += f'<circle cx="{x + c * step}" cy="{y + rw * step}" r="{r}"/>'
    return out + '</g>\n'


# --------------------------------------------------------------------------
# icons — 24-unit design grid, stroked, scaled by `s`
# --------------------------------------------------------------------------

def _ico(x, y, s, color, body, sw=1.9, fill='none'):
    k = s / 24.0
    return (f'    <g transform="translate({x} {y}) scale({k:.4f})" fill="{fill}" '
            f'stroke="{color}" stroke-width="{sw / k:.2f}" stroke-linecap="square" '
            f'stroke-linejoin="miter" vector-effect="non-scaling-stroke">{body}</g>\n')


def i_terminal(x, y, s, c): return _ico(x, y, s, c, '<path d="M3 6 l6 6 l-6 6"/><path d="M13 18 h8"/>')
def i_shield(x, y, s, c):   return _ico(x, y, s, c, '<path d="M12 2 L21 6 v6 c0 5.4-4.2 8.6-9 10.4C7.2 20.6 3 17.4 3 12 V6 Z"/>')
def i_shield_check(x, y, s, c): return _ico(x, y, s, c, '<path d="M12 2 L21 6 v6 c0 5.4-4.2 8.6-9 10.4C7.2 20.6 3 17.4 3 12 V6 Z"/><path d="M8 12 l3 3 l5.5-6"/>')
def i_code(x, y, s, c):     return _ico(x, y, s, c, '<path d="M9 6 L3.5 12 L9 18"/><path d="M15 6 L20.5 12 L15 18"/>')
def i_brain(x, y, s, c):    return _ico(x, y, s, c, '<path d="M12 3 L19 7 v8 l-7 4 l-7-4 V7 Z"/><circle cx="12" cy="11" r="2.4"/><path d="M12 3 v5.6M5 7 l4.8 2.8M19 7 l-4.8 2.8M12 13.4 v5.6"/>')
def i_bolt(x, y, s, c):     return _ico(x, y, s, c, '<path d="M13.5 2 L5 13.5 h5.5 L9.5 22 L19 10 h-6 Z"/>')
def i_layers(x, y, s, c):   return _ico(x, y, s, c, '<path d="M12 3 L21 8 L12 13 L3 8 Z"/><path d="M3 12.5 L12 17.5 L21 12.5"/><path d="M3 16.8 L12 21.8 L21 16.8"/>')
def i_pin(x, y, s, c):      return _ico(x, y, s, c, '<path d="M12 2 a7 7 0 0 1 7 7 c0 5.4-7 13-7 13 S5 14.4 5 9 a7 7 0 0 1 7-7 Z"/><circle cx="12" cy="9" r="2.6"/>')
def i_pulse(x, y, s, c):    return _ico(x, y, s, c, '<path d="M2 12 h4 l3-7.5 l4.5 15 l3-7.5 h5.5"/>')
def i_target(x, y, s, c):   return _ico(x, y, s, c, '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.6"/><circle cx="12" cy="12" r="1.1" fill="' + c + '"/>')
def i_db(x, y, s, c):       return _ico(x, y, s, c, '<ellipse cx="12" cy="6" rx="8" ry="3.2"/><path d="M4 6 v12 c0 1.8 3.6 3.2 8 3.2 s8-1.4 8-3.2 V6"/><path d="M4 12 c0 1.8 3.6 3.2 8 3.2 s8-1.4 8-3.2"/>')
def i_cube(x, y, s, c):     return _ico(x, y, s, c, '<path d="M12 2.5 L21 7.2 v9.6 L12 21.5 L3 16.8 V7.2 Z"/><path d="M3 7.2 L12 12 l9-4.8M12 12 v9.5"/>')
def i_mail(x, y, s, c):     return _ico(x, y, s, c, '<rect x="2.5" y="5" width="19" height="14" rx="1"/><path d="M2.5 6.2 L12 13.4 L21.5 6.2"/>')
def i_globe(x, y, s, c):    return _ico(x, y, s, c, '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="3.9" ry="9"/><path d="M3 12 h18M4.6 7 h14.8M4.6 17 h14.8"/>')
def i_play(x, y, s, c):     return _ico(x, y, s, c, '<path d="M7 4.5 L19 12 L7 19.5 Z"/>')
def i_gamepad(x, y, s, c):  return _ico(x, y, s, c, '<rect x="2.5" y="7" width="19" height="10.5" rx="4"/><path d="M7 10.4 v3.7M5.2 12.2 h3.7"/><circle cx="16.2" cy="11.4" r="1.1" fill="' + c + '"/><circle cx="18.4" cy="13.8" r="1.1" fill="' + c + '"/>')
def i_github(x, y, s, c):   return _ico(x, y, s, c, '<path d="M12 2.2 a9.8 9.8 0 0 0-3.1 19.1 c.5.1.7-.2.7-.5 v-1.8 c-2.7.6-3.3-1.3-3.3-1.3 -.4-1.1-1.1-1.4-1.1-1.4 -.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .9 1.5 2.3 1.1 2.9.8 .1-.6.3-1.1.6-1.3 -2.2-.2-4.5-1.1-4.5-4.9 0-1.1.4-2 1-2.7 -.1-.3-.4-1.3.1-2.7 0 0 .8-.3 2.7 1 a9.4 9.4 0 0 1 4.9 0 c1.9-1.3 2.7-1 2.7-1 .5 1.4.2 2.4.1 2.7 .6.7 1 1.6 1 2.7 0 3.8-2.3 4.7-4.5 4.9 .4.3.7.9.7 1.9 v2.8 c0 .3.2.6.7.5 A9.8 9.8 0 0 0 12 2.2 Z"/>')
def i_users(x, y, s, c):    return _ico(x, y, s, c, '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20 c0-3.6 2.9-6 6.5-6 s6.5 2.4 6.5 6"/><path d="M17 5.2 a3.4 3.4 0 0 1 0 6.4M18.5 14.6 c2.1.7 3.5 2.6 3.5 5.4"/>')
def i_repo(x, y, s, c):     return _ico(x, y, s, c, '<path d="M4 3.5 h13.5 v17 H6 a2 2 0 0 1-2-2 Z"/><path d="M4 17 h13.5"/><path d="M7.5 7 h6"/>')
def i_pr(x, y, s, c):       return _ico(x, y, s, c, '<circle cx="6.5" cy="5.5" r="2.6"/><circle cx="6.5" cy="18.5" r="2.6"/><path d="M6.5 8.1 v7.8"/><circle cx="17.5" cy="18.5" r="2.6"/><path d="M17.5 15.9 V9 a3 3 0 0 0-3-3 h-3"/>')
def i_issue(x, y, s, c):    return _ico(x, y, s, c, '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.2"/>')
def i_commit(x, y, s, c):   return _ico(x, y, s, c, '<circle cx="12" cy="12" r="3.6"/><path d="M2.5 12 h5.9M15.6 12 h5.9"/>')
def i_chart(x, y, s, c):    return _ico(x, y, s, c, '<path d="M3 20 h18"/><rect x="5" y="12" width="3.4" height="6"/><rect x="10.3" y="7.5" width="3.4" height="10.5"/><rect x="15.6" y="4" width="3.4" height="14"/>')
def i_clock(x, y, s, c):    return _ico(x, y, s, c, '<circle cx="12" cy="12" r="9"/><path d="M12 6.6 V12 l4 2.4"/>')
def i_lock(x, y, s, c):     return _ico(x, y, s, c, '<rect x="4.5" y="10.5" width="15" height="10.5" rx="1"/><path d="M8 10.5 V7.6 a4 4 0 0 1 8 0 v2.9"/>')
def i_grid(x, y, s, c):     return _ico(x, y, s, c, '<rect x="3.5" y="3.5" width="6.5" height="6.5"/><rect x="14" y="3.5" width="6.5" height="6.5"/><rect x="3.5" y="14" width="6.5" height="6.5"/><rect x="14" y="14" width="6.5" height="6.5"/>')
def i_snake(x, y, s, c):    return _ico(x, y, s, c, '<path d="M3 18 h5 v-5 h5 v-5 h5" stroke-width="2.6"/><rect x="17.5" y="6" width="4" height="4" fill="' + c + '" stroke="none"/>', sw=2.4)
def i_trophy(x, y, s, c):   return _ico(x, y, s, c, '<path d="M7 4 h10 v5 a5 5 0 0 1-10 0 Z"/><path d="M7 5.5 H4 v2 a3 3 0 0 0 3 3M17 5.5 h3 v2 a3 3 0 0 1-3 3"/><path d="M12 14 v3.5M8.5 20.5 h7"/>')
def i_flame(x, y, s, c):    return _ico(x, y, s, c, '<path d="M12 2.5 c3.5 4 6.5 6.5 6.5 11 a6.5 6.5 0 0 1-13 0 c0-2.6 1.4-4.2 2.8-6 .4 1.6 1.2 2.4 2.2 2.8 -.6-3 .2-5.6 1.5-7.8 Z"/>')
def i_calendar(x, y, s, c): return _ico(x, y, s, c, '<rect x="3.5" y="5" width="17" height="16" rx="1"/><path d="M3.5 10 h17M8 3 v4M16 3 v4"/>')
def i_star(x, y, s, c):     return _ico(x, y, s, c, '<path d="M12 3 l2.8 6 6.2.7 -4.6 4.2 1.3 6.1 -5.7-3.2 -5.7 3.2 1.3-6.1 -4.6-4.2 6.2-.7 Z"/>')
def i_branch(x, y, s, c):   return _ico(x, y, s, c, '<circle cx="6.5" cy="5.5" r="2.6"/><circle cx="6.5" cy="18.5" r="2.6"/><circle cx="17.5" cy="9" r="2.6"/><path d="M6.5 8.1 v7.8M17.5 11.6 c0 3.4-4 3.2-6.6 4.2"/>')
def i_map(x, y, s, c):      return _ico(x, y, s, c, '<path d="M3 6 l6-2.5 6 2.5 6-2.5 v14.5 l-6 2.5 -6-2.5 -6 2.5 Z"/><path d="M9 3.5 v14.5M15 6 v14.5"/>')
