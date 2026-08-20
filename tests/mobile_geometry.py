#!/usr/bin/env python3
"""Dependency-free regression gates for the accepted mobile compositions."""

import importlib.util
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG = "{http://www.w3.org/2000/svg}"
failures = []
checks = 0


def check(condition, label, detail=""):
    global checks
    checks += 1
    if condition:
        print("  PASS  " + label)
    else:
        failures.append(label)
        print("  FAIL  " + label + ((" — " + detail) if detail else ""))


def text(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        return handle.read()


def root(rel):
    return ET.parse(os.path.join(ROOT, rel)).getroot()


def numeric(node, name):
    return float(node.attrib[name])


print("\n== CTA mobile geometry ==")
readme = text("README.md")
bands = [(334, "xs", 114), (355, "phone-sm", 124), (379, "md", 135),
         (405, "phone", 147), (434, "lg", 160), (464, "phone-xl", 174),
         (480, "phone-xxl", 189)]
for limit, suffix, expected in bands:
    check(f'(max-width: {limit}px)' in readme, f"CTA breakpoint <= {limit}px")
    for name in ("explore", "overview", "snake", "contact"):
        asset = root(f"assets/sections/btn-{name}-{suffix}.svg")
        check(float(asset.attrib["width"]) == expected and float(asset.attrib["height"]) in (92, 96, 98),
              f"CTA {name}-{suffix} has equal band geometry")

# Measured GitHub README rails are viewport - 82px at these phone widths.
def selected_width(viewport):
    return next(expected for limit, _, expected in bands if viewport <= limit)


for viewport in range(320, 441):
    card_w = selected_width(viewport)
    rail = viewport - 82
    group = card_w * 2 + 4
    per_row = int((rail + 4) // (card_w + 4))
    check(per_row == 2, f"CTA {viewport}px has exactly two columns", f"capacity={per_row}")
    check(group / rail >= .92, f"CTA {viewport}px fills >=92% of README rail", f"{group / rail:.3f}")
check(len(re.findall(r'<img src="assets/sections/btn-[^"]+\.svg"', readme)) == 4,
      "CTA has exactly four equal-card fallbacks")


print("\n== Activity mobile geometry ==")
spec = importlib.util.spec_from_file_location("render_activity", os.path.join(ROOT, "tools", "render_activity.py"))
activity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(activity)
metrics = dict(contributions=31, commits=29, prs=0, issues=0, repos=1, followers=1,
               longest=2, current=1, best=14, active=20, window=365, touched=4,
               stars=0, avg=0)
svg_text = activity.narrow(metrics, "cybersec-iq", "TEST UTC")
svg_root = ET.fromstring(svg_text)
check(svg_root.attrib.get("viewBox") == "0 0 340 578", "Activity narrow viewBox is intentional 340px composition")
labels = ["CONTRIBUTIONS", "COMMITS", "PULL REQUESTS", "ISSUES", "PUBLIC REPOS", "FOLLOWERS"]
nodes = list(svg_root.iter(SVG + "text"))
for label in labels:
    check(sum("".join(n.itertext()) == label for n in nodes) == 1, f"Activity has one {label} tile")
number_nodes = [n for n in nodes if "".join(n.itertext()) in {"31", "29", "0", "1"} and float(n.attrib.get("font-size", 0)) == 27]
check(len(number_nodes) == 6, "Activity has six solid metric numerals")
check(all("filter" not in n.attrib and "style" not in n.attrib for n in number_nodes),
      "Activity numerals have no blur/glow filter")
tile_x = sorted({numeric(n, "x") for n in number_nodes})
tile_y = sorted({numeric(n, "y") for n in number_nodes})
check(len(tile_x) == 2, "Activity has exactly two metric columns")
check(len(tile_y) == 3, "Activity has exactly three metric rows")
insight = next(n for n in nodes if "".join(n.itertext()) == "ACTIVITY INSIGHTS")
check(numeric(insight, "y") > max(tile_y), "Activity Insights is below the metric grid")
check('max-width: 500px' in readme and 'output/activity-narrow.svg' in readme,
      "README deterministically selects narrow Activity")
pages = text("docs/index.html")
check('max-width: 700px' in pages and 'output/activity-embed-narrow.svg' in pages,
      "Pages deterministically selects narrow Activity")
check('output/snake-framed-narrow.svg' in pages, "Pages deterministically selects narrow contribution grid")


print("\n== WHOAMI and stack geometry ==")
who = text("tools/sections/whoami.py")
check("cx + 74" in who and "cx + 88" in who, "README WHOAMI uses compact label | colon | value coordinates")
css = text("docs/styles.css")
check(not re.search(r"\.fact\s*\{[^}]*space-between", css, re.S),
      "Pages WHOAMI does not use space-between")
check(all(token in pages for token in ('class="fact__sep">:</span>', "LOCATION", "STATUS", "MISSION")),
      "Pages WHOAMI has explicit colon columns")
stack = root("assets/sections/stack-narrow.svg")
stack_nodes = list(stack.iter(SVG + "text"))
subtitle = next(n for n in stack_nodes if "".join(n.itertext()) == "TECHNOLOGY STACK & TOOLING")
frames = [n for n in stack.iter(SVG + "rect") if n.attrib.get("x") == "10" and n.attrib.get("y") == "82"]
clearance = numeric(frames[0], "y") - (numeric(subtitle, "y") + numeric(subtitle, "font-size") * .25)
check(bool(frames) and clearance >= 10, "Stack subtitle has >=10px frame clearance", f"{clearance:.1f}px")


print("\n== Contact, footer, and narrow viewBoxes ==")
contact = root("assets/sections/contact-narrow.svg")
cards = [n for n in contact.iter(SVG + "rect") if n.attrib.get("width") == "187.0" and n.attrib.get("height") == "146"]
contact_text = list(contact.iter(SVG + "text"))
check(len(cards) == 4, "Contact remains an exact 2x2 card grid")
for index, card in enumerate(cards, 1):
    left, top, right, bottom = numeric(card, "x"), numeric(card, "y"), numeric(card, "x") + numeric(card, "width"), numeric(card, "y") + numeric(card, "height")
    children = [n for n in contact_text if left <= numeric(n, "x") <= right and top <= numeric(n, "y") <= bottom]
    max_baseline = max(numeric(n, "y") for n in children)
    check(max_baseline <= bottom - 14, f"Contact card {index} text has >=14px bottom padding",
          f"{bottom - max_baseline:.1f}px")
footer = root("assets/sections/footer-narrow.svg")
footer_strings = ["".join(n.itertext()) for n in footer.iter(SVG + "text")]
for exact in ("Code is my craft.", "Security is my mindset.", "Impact is the goal."):
    check(exact in footer_strings, f'Footer preserves exact spacing: "{exact}"')
for name in ("hero", "whoami", "about", "stack", "systems", "snake-cta", "contact", "footer"):
    vb = root(f"assets/sections/{name}-narrow.svg").attrib["viewBox"].split()
    check(float(vb[2]) == 440, f"{name}-narrow uses the common 440px README rail")

print(f"\n{checks - len(failures)} passed, {len(failures)} failed\n")
sys.exit(1 if failures else 0)
