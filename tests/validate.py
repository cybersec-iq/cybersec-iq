#!/usr/bin/env python3
"""Static integrity checks for the cybersec-iq profile repository.

Dependency-free on purpose: the standard library is enough, and a profile
repository should not need a toolchain to prove its own links work.

Checks
  1. every SVG asset is well-formed XML
  2. every local path referenced by README.md exists on disk
  3. every local href/src referenced by the Pages site exists on disk
  4. outbound links use https
"""

import os
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

failures = []
checks = 0


def ok(label):
    global checks
    checks += 1
    print("  PASS  " + label)


def bad(label, detail):
    global checks
    checks += 1
    failures.append(label)
    print("  FAIL  " + label)
    print("        " + detail)


# ---------------------------------------------------------------- 1. SVG

print("\n== SVG well-formedness ==")
svgs = []
for base, dirs, files in os.walk(os.path.join(ROOT, "assets")):
    dirs[:] = [d for d in dirs if d != ".git"]
    for name in sorted(files):
        if name.endswith(".svg"):
            svgs.append(os.path.join(base, name))

if not svgs:
    bad("assets contain SVGs", "no .svg files found under assets/")

for path in svgs:
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    try:
        ET.parse(path)
        ok(rel)
    except ET.ParseError as exc:
        bad(rel, str(exc))


# ----------------------------------------------- 1b. final UI regressions

print("\n== Final profile UI regressions ==")


def read_text(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        return handle.read()


who_wide = read_text("assets/sections/whoami.svg")
who_narrow = read_text("assets/sections/whoami-narrow.svg")
who_source = read_text("tools/sections/whoami.py")
pages_html = read_text("docs/index.html")
pages_css = read_text("docs/styles.css")
pages_js = read_text("docs/app.js")
readme_text = read_text("README.md")
snake_wide = read_text("assets/sections/snake-cta.svg")

if "globe-rotate" not in who_wide + who_narrow + who_source + pages_html + pages_css:
    ok("WHOAMI has no rotating-globe implementation")
else:
    bad("WHOAMI has no rotating-globe implementation", "legacy globe-rotate code remains")

if all(token in who_wide for token in ("<clipPath", "attributeName=\"width\"", "repeatCount=\"indefinite\"")):
    ok("README WHOAMI includes an SVG typewriter loop")
else:
    bad("README WHOAMI includes an SVG typewriter loop", "missing clip/reveal animation")

if all(token in pages_js for token in ("whoTyped", "prefers-reduced-motion", "mission --status")):
    ok("Pages WHOAMI includes typewriter and reduced-motion handling")
else:
    bad("Pages WHOAMI includes typewriter and reduced-motion handling", "expected JS hooks missing")

cta_tags = re.findall(r'<img src="assets/sections/btn-[^"]+\.svg"[^>]*>', readme_text)
if len(cta_tags) == 4 and all("width=" not in tag for tag in cta_tags):
    ok("README CTA row uses four intrinsic compact buttons")
else:
    bad("README CTA row uses four intrinsic compact buttons", "expected four buttons without forced widths")

if 'viewBox="0 0 1200 442"' in snake_wide and all(label in snake_wide for label in ("DEPENDENCIES", "TRACKERS", "STORED LOCALLY")):
    ok("wide Snake CTA contains its complete properties panel")
else:
    bad("wide Snake CTA contains its complete properties panel", "wide layout or property rows missing")


# ------------------------------------------------------- 2 + 3. local links

def is_external(url):
    return bool(urlparse(url).scheme) or url.startswith("//")


def check_local(source_rel, source_dir, url, label):
    target = unquote(url.split("#")[0].split("?")[0])
    if target in ("", "."):
        return
    resolved = os.path.normpath(os.path.join(source_dir, target))
    if os.path.exists(resolved):
        ok(label)
        return
    # A directory reference such as ./snake/ resolves to its index.html.
    if os.path.exists(os.path.join(resolved, "index.html")):
        ok(label)
        return
    bad(label, "missing target: " + target + "  (from " + source_rel + ")")


print("\n== README local references ==")
readme = os.path.join(ROOT, "README.md")
if not os.path.exists(readme):
    bad("README.md exists", "not found")
else:
    with open(readme, encoding="utf-8") as handle:
        text = handle.read()

    refs = re.findall(r'!\[[^\]]*\]\(([^)\s]+)', text)
    refs += re.findall(r'<img[^>]+src="([^"]+)"', text)
    refs += re.findall(r'<source[^>]+srcset="([^"]+)"', text)
    refs += re.findall(r'(?<!\!)\[[^\]]*\]\(([^)\s]+)\)', text)
    refs += re.findall(r'<a[^>]+href="([^"]+)"', text)

    local = sorted({r for r in refs if not is_external(r) and not r.startswith("mailto:")})
    if not local:
        bad("README references local assets", "none found")
    for ref in local:
        check_local("README.md", ROOT, ref, "README -> " + ref)

    # Every <img> must carry alt text.
    imgs = re.findall(r"<img\b[^>]*>", text)
    missing_alt = [tag for tag in imgs if 'alt="' not in tag]
    if missing_alt:
        bad("every README image has alt text",
            str(len(missing_alt)) + " <img> tag(s) without alt")
    elif imgs:
        ok("every README image has alt text (" + str(len(imgs)) + ")")


print("\n== Pages site references ==")
pages = []
for base, dirs, files in os.walk(os.path.join(ROOT, "docs")):
    dirs[:] = [d for d in dirs if d != ".git"]
    for name in sorted(files):
        if name.endswith(".html"):
            pages.append(os.path.join(base, name))

if not pages:
    bad("docs/ contains pages", "no .html files found")

for path in pages:
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    with open(path, encoding="utf-8") as handle:
        html = handle.read()

    urls = re.findall(r'(?:href|src)="([^"]+)"', html)
    for url in urls:
        if url.startswith("data:") or url.startswith("#") or url.startswith("mailto:"):
            continue
        if is_external(url):
            continue
        check_local(rel, os.path.dirname(path), url, rel + " -> " + url)

    # Outbound links must be https and must not leak the opener.
    for tag in re.findall(r"<a\b[^>]*>", html):
        href = re.search(r'href="([^"]+)"', tag)
        if not href or not is_external(href.group(1)):
            continue
        target = href.group(1)
        if not target.startswith("https://"):
            bad(rel + " outbound https", target + " is not https")
        elif 'target="_blank"' in tag and "noopener" not in tag:
            bad(rel + " outbound rel", target + ' uses target="_blank" without rel="noopener"')
        else:
            ok(rel + " outbound " + target)


print("\n----------------------------------------")
print("  " + str(checks - len(failures)) + " passed, " + str(len(failures)) + " failed")
print("----------------------------------------\n")

sys.exit(1 if failures else 0)
