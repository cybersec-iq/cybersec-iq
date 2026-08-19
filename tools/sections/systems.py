"""~/systems — selected systems cards.

Reference: 03_STACK_CURRENTLY_BUILDING_REFERENCE.png (card grid, per-card accent
border, status marker, divider, metadata footer).

Data integrity: the reference's card content is mock — it invents a
"play-to-earn / blockchain / live on testnet" product and uptime targets. None
of that is carried over. Every field below is either verified (aryaniq.com
resolves over HTTPS), taken from the owner's own repository description, or
explicitly marked undisclosed. No status is claimed that cannot be supported.
"""

import design as D

# (name, accent, status, status_colour, domain, description lines, stack chips)
SYSTEMS = [
    ('ARYANIQ', D.CYAN, 'LIVE', D.GREEN,
     'Personal platform & engineering hub',
     ['Public home for the practice:', 'services, writing and contact.'],
     [('TypeScript', D.BLUE), ('Web', D.CYAN)]),

    ('KAMINO RECORDS', D.GREEN, 'PRIVATE', D.MUTED,
     'Music label platform',
     ['Catalogue, releases and artist', 'management on a headless CMS.'],
     [('Next.js', D.TEXT), ('Payload CMS', D.GREEN), ('PostgreSQL', D.BLUE)]),

    ('SHINEL SUPPLIER', D.YELLOW, 'PRIVATE', D.MUTED,
     'Multilingual commerce platform',
     ['Multi-language storefront and', 'supplier-side operations.'],
     [('TypeScript', D.BLUE), ('Web', D.CYAN)]),

    ('XPRIME', D.CYAN, 'PRIVATE', D.MUTED,
     'Product platform',
     ['Closed product build. Stack is', 'public, internals are not.'],
     [('TypeScript', D.BLUE)]),

    ('XOS', D.GREEN, 'UNDISCLOSED', D.FAINT,
     'Internal system',
     ['Details withheld. Named here for', 'completeness, not disclosure.'],
     []),

    ('XADMIN', D.YELLOW, 'UNDISCLOSED', D.FAINT,
     'Internal system',
     ['Details withheld. Named here for', 'completeness, not disclosure.'],
     []),
]

NOTE = ('Source, infrastructure topology and client data for private systems are not published. '
        'Nothing here claims scale, revenue or third-party endorsement.')

DESC = ('Selected systems. ARYANIQ, personal platform and engineering hub, live. '
        'KAMINO RECORDS, music label platform, private. '
        'SHINEL SUPPLIER, multilingual commerce platform, private. '
        'XPRIME, product platform, private. XOS and XADMIN, internal systems, undisclosed. '
        + NOTE)
TITLE = 'systems - selected work'


def _card(x, y, w, h, item, compact=False):
    name, accent, status, scol, domain, body, chips = item
    o = D.panel(x, y, w, h, fill=D.SURFACE_2, stroke=accent, sw=1.3, opacity=1)
    o += ('    <rect x="%d" y="%d" width="%d" height="2.5" fill="%s" opacity="0.85"/>\n'
          % (x, y, w, accent))
    o += D.brackets(x, y, w, h, color=accent, arm=11, sw=1.5, corners='tl,br', opacity=0.45)

    ns = 15 if not compact else 13
    o += D.text(x + 18, y + 34, name, size=ns, fill=accent, weight='700', tracking=1.8)

    sw_ = D.tw(status, 10.5, 1.6)
    o += D.status_dot(x + w - sw_ - 34, y + 29, scol, 4,
                      animate=(status == 'LIVE'))
    o += D.text(x + w - 18, y + 33, status, size=10.5, fill=scol,
                tracking=1.6, anchor='end')

    o += D.text(x + 18, y + 54, domain, size=11.5, fill=D.MUTED, tracking=0.4)
    o += D.hline(x + 18, y + 66, w - 36, D.LINE_2)

    # Lay the card out top-down rather than from fixed offsets, so a longer
    # description can never end up underneath the technology chips.
    bs = 12
    cy = y + 88
    for ln in D.wrap(' '.join(body), D.fit_chars(w - 36, bs)):
        o += D.text(x + 18, cy, ln, size=bs, fill=D.TEXT)
        cy += 18

    cy += 4
    if chips:
        c, _, _ = D.chip_row(x + 18, cy, chips, size=10.5, h=21,
                             max_w=w - 36, gap=6, lh=25)
        o += c
    else:
        o += D.text(x + 18, cy + 14, '— no public detail —', size=11, fill=D.FAINT)
    return o


def wide():
    W, H = 1200, 522
    px, py, pw = 22, 20, W - 44

    o = D.section_header(px + 24, py + 46, '~/systems', 'SELECTED SYSTEMS & PROJECTS',
                         right='ACCESS CONTROLLED', right_icon=D.i_lock, w=pw - 48)

    ph = 424
    o += D.panel(px, py + 76, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
    o += D.brackets(px, py + 76, pw, ph, color=D.YELLOW, arm=18, sw=2,
                    corners='tl,tr', opacity=0.7)

    cx = px + 30
    inner = pw - 60
    gap = 16
    cw = (inner - gap * 2) / 3
    ch = 158
    for i, item in enumerate(SYSTEMS):
        col, row = i % 3, i // 3
        o += _card(cx + col * (cw + gap), py + 106 + row * (ch + gap), cw, ch, item)

    ny = py + 106 + 2 * (ch + gap) + 6
    o += D.i_lock(cx, ny - 12, 16, D.FAINT)
    o += D.text(cx + 26, ny, NOTE, size=11.5, fill=D.FAINT)
    return D.doc(W, H, TITLE, DESC, o)


def narrow():
    W = 440
    px, py, pw = 10, 58, W - 20
    cx = px + 14
    inner = pw - 28

    o = D.section_header(px + 8, 34, '~/systems', 'SELECTED SYSTEMS & PROJECTS')

    ch = 152
    for i, item in enumerate(SYSTEMS):
        o += _card(cx, py + 16 + i * (ch + 12), inner, ch, item, compact=True)

    ny = py + 16 + len(SYSTEMS) * (ch + 12) + 8
    o += D.text(cx, ny, 'Private system internals are not', size=10.5, fill=D.FAINT)
    o += D.text(cx, ny + 15, 'published. No scale or revenue claims.', size=10.5, fill=D.FAINT)

    ph = ny + 26 - py
    H = py + ph + 12
    frame = (D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
             + D.brackets(px, py, pw, ph, color=D.YELLOW, arm=14, sw=1.8,
                          corners='tl,tr', opacity=0.7))
    return D.doc(W, H, TITLE, DESC, frame + o)
