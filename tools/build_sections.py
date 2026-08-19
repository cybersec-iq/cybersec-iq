#!/usr/bin/env python3
"""Emit every static README section SVG from the shared design system.

Each section ships in two forms:
  <name>.svg          wide composition for desktop README width
  <name>-narrow.svg   simplified layout on a 440-unit canvas for phones

README selects between them with
`<source media="(max-width: 500px)" srcset="...-narrow.svg">`, which GitHub's
HTML sanitizer preserves. That lets the desktop view carry the reference's
information density without shrinking mobile text into illegibility.

Run:  python tools/build_sections.py
"""

import os
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'sections'))

OUT = os.path.join(ROOT, 'assets', 'sections')

import hero, whoami, about, stack, systems, snakecta, contact, footer, buttons  # noqa: E402

SECTIONS = [
    ('hero', hero),
    ('whoami', whoami),
    ('about', about),
    ('stack', stack),
    ('systems', systems),
    ('snake-cta', snakecta),
    ('contact', contact),
    ('footer', footer),
]


def write(name, svg):
    ET.fromstring(svg)                      # fail loudly on malformed output
    path = os.path.join(OUT, name + '.svg')
    with open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(svg)
    return len(svg)


def main():
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for name, mod in SECTIONS:
        for suffix, fn in (('', mod.wide), ('-narrow', mod.narrow)):
            n = write(name + suffix, fn())
            total += n
            print('  %-34s %6.1f KB' % (name + suffix + '.svg', n / 1024))

    for name, svg in buttons.all_buttons().items():
        n = write(name, svg)
        total += n
        print('  %-34s %6.1f KB' % (name + '.svg', n / 1024))

    print('  %-34s %6.1f KB' % ('TOTAL', total / 1024))


if __name__ == '__main__':
    main()
