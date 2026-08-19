#!/usr/bin/env python3
"""Wrap the generated contribution snake in the cybersec-iq command-center frame.

Reference: 04_ACTIVITY_SNAKE_REFERENCE.png — the contribution grid is presented
as a panel of the dashboard, not as a loose third-party widget pasted into the
page.

The snake SVG produced by Platane/snk declares no ids and uses class names
(c, c0, s0..s3, u, u0) that do not collide with this design system's classes
(m, blink, live, flow, rise), so its content can be nested inside a child <svg>
element without touching its animation. The child keeps its own viewBox, which
also handles snk's negative viewBox origin cleanly.

Usage: python tools/frame_snake.py <snake.svg> <outdir>
"""

import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import design as D  # noqa: E402

TITLE = 'Contribution grid - animated snake'
DESC = ('Animated contribution grid for cybersec-iq. A snake traverses the GitHub '
        'contribution graph, consuming each day of activity. Regenerated daily by '
        'GitHub Actions from the live contribution calendar.')


def read_snake(path):
    src = open(path, encoding='utf-8').read()
    m = re.search(r'<svg\b([^>]*)>', src)
    if not m:
        raise SystemExit('not an SVG: ' + path)
    attrs = m.group(1)
    vb = re.search(r'viewBox="([^"]+)"', attrs)
    if not vb:
        raise SystemExit('snake SVG has no viewBox')
    view = vb.group(1)
    parts = [float(v) for v in view.replace(',', ' ').split()]
    inner = src[m.end():src.rindex('</svg>')]
    return view, parts[2], parts[3], inner


def frame(view, iw, ih, inner, width, compact=False):
    px = 10 if compact else 22
    pw = width - px * 2
    pad = 14 if compact else 18

    head_h = 44 if compact else 76
    avail = pw - pad * 2
    scale = avail / iw
    sh = ih * scale

    ptop = head_h
    ph = sh + pad * 2

    if compact:
        o = D.section_header(px + 8, 34, '~/contribution-grid', 'ANIMATED SNAKE')
    else:
        o = D.section_header(px + 24, 46, '~/contribution-grid',
                             'ANIMATED CONTRIBUTION SNAKE',
                             right='REGENERATED DAILY', right_icon=D.i_calendar,
                             w=pw - 48)

    o += D.panel(px, ptop, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
    o += D.brackets(px, ptop, pw, ph, color=D.GREEN, arm=16 if compact else 18,
                    sw=2, corners='tl,tr,bl,br', opacity=0.5)

    o += ('    <svg x="%.1f" y="%.1f" width="%.1f" height="%.1f" viewBox="%s" '
          'preserveAspectRatio="xMidYMid meet">%s</svg>\n'
          % (px + pad, ptop + pad, avail, sh, view, inner))

    H = ptop + ph + (10 if compact else 14)
    return D.doc(width, H, TITLE, DESC, o)


def main():
    if len(sys.argv) < 3:
        raise SystemExit('usage: frame_snake.py <snake.svg> <outdir>')
    src, out = sys.argv[1], sys.argv[2]
    view, iw, ih, inner = read_snake(src)
    os.makedirs(out, exist_ok=True)

    for name, width, compact in (('snake-framed.svg', 1200, False),
                                 ('snake-framed-narrow.svg', 440, True)):
        svg = frame(view, iw, ih, inner, width, compact)
        ET.fromstring(svg)
        with open(os.path.join(out, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(svg)
        print('  %-28s %5.1f KB' % (name, len(svg) / 1024))


if __name__ == '__main__':
    main()
