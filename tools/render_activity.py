#!/usr/bin/env python3
"""Render the ~/activity section from live GitHub data.

Reference: 04_ACTIVITY_SNAKE_REFERENCE.png — the row of accent-coded metric
tiles and the ACTIVITY INSIGHTS panel.

Data integrity notes
--------------------
* Every number here is fetched or derived at render time. Nothing is typed in.
* The reference also shows a 53-week contribution heatmap and a RECENT ACTIVITY
  timeline. Both are omitted deliberately: the animated contribution snake in
  the section directly below already visualises the same grid, and this account
  currently exposes a single public event, so a "recent activity" feed would be
  padding. Duplicating an almost-empty grid twice would emphasise the gap
  rather than the work.
* Streaks, best day, active days and the average are computed from the real
  contribution calendar rather than copied from the mockup.
* The card states on its face that it counts public activity only, so the
  figures cannot be mistaken for private work.

Usage:
    GITHUB_TOKEN=... PROFILE_USER=cybersec-iq python tools/render_activity.py <outdir>
"""

import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import design as D  # noqa: E402

API = 'https://api.github.com/graphql'

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false) {
      totalCount
      nodes { stargazerCount }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalRepositoriesWithContributedCommits
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch(user, token):
    body = json.dumps({'query': QUERY, 'variables': {'login': user}}).encode()
    req = urllib.request.Request(API, data=body, headers={
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
        'User-Agent': 'cybersec-iq-profile',
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if 'errors' in payload:
        raise SystemExit('GitHub API error: ' + json.dumps(payload['errors']))
    return payload['data']['user']


def derive(user):
    cc = user['contributionsCollection']
    cal = cc['contributionCalendar']
    days = [d for w in cal['weeks'] for d in w['contributionDays']]

    longest = run = current = 0
    for d in days:
        if d['contributionCount'] > 0:
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    for d in reversed(days):
        if d['contributionCount'] > 0:
            current += 1
        else:
            break

    active = sum(1 for d in days if d['contributionCount'] > 0)
    best = max((d['contributionCount'] for d in days), default=0)
    total = cal['totalContributions']
    avg = total / len(days) if days else 0.0

    return {
        'contributions': total,
        'commits': cc['totalCommitContributions'],
        'prs': cc['totalPullRequestContributions'],
        'issues': cc['totalIssueContributions'],
        'repos': user['repositories']['totalCount'],
        'followers': user['followers']['totalCount'],
        'stars': sum(r['stargazerCount'] for r in user['repositories']['nodes']),
        'touched': cc['totalRepositoriesWithContributedCommits'],
        'longest': longest,
        'current': current,
        'active': active,
        'best': best,
        'window': len(days),
        'avg': avg,
    }


def tiles(m):
    return [
        ('CONTRIBUTIONS', m['contributions'], '12 MONTHS', D.YELLOW, D.i_calendar),
        ('COMMITS',       m['commits'],       '12 MONTHS', D.CYAN,   D.i_commit),
        ('PULL REQUESTS', m['prs'],           '12 MONTHS', D.GREEN,  D.i_pr),
        ('ISSUES',        m['issues'],        '12 MONTHS', D.CYAN,   D.i_issue),
        ('PUBLIC REPOS',  m['repos'],         'OWNED',     D.YELLOW, D.i_repo),
        ('FOLLOWERS',     m['followers'],     'TOTAL',     D.GREEN,  D.i_users),
    ]


def insights(m):
    return [
        (D.i_flame,  'Longest streak',     '%d %s' % (m['longest'], 'day' if m['longest'] == 1 else 'days'), D.GREEN),
        (D.i_pulse,  'Current streak',     '%d %s' % (m['current'], 'day' if m['current'] == 1 else 'days'), D.CYAN),
        (D.i_trophy, 'Best day',           '%d' % m['best'], D.YELLOW),
        (D.i_chart,  'Active days',        '%d of %d' % (m['active'], m['window']), D.CYAN),
        (D.i_star,   'Repos contributed',  '%d' % m['touched'], D.GREEN),
    ]


def desc(m, stamp):
    t = tiles(m)
    return ('Public GitHub activity. ' +
            '. '.join('%s: %s' % (k, v) for k, v, _, _, _ in t) +
            '. Longest streak %d days. Current streak %d days. Best day %d contributions. '
            'Active on %d of %d days. Public activity only, generated %s.'
            % (m['longest'], m['current'], m['best'], m['active'], m['window'], stamp))


def wide(m, user, stamp, header=True):
    """Wide activity card.

    `header=True` prints the `>_ ~/activity` section header above the panel and
    is what the README embeds, since nothing there supplies a heading of its
    own. `header=False` drops it and moves the title inside the panel as the
    card's own header row: the Pages site already renders `~/activity` above
    the card, and two identical titles stacked together read as a mistake.
    Both share the same data and the same geometry below the header.
    """
    W = 1200
    px, pw = 22, W - 44
    cx = px + 30
    inner = pw - 60
    right = cx + inner

    if header:
        ptop, ph, tiles_y, iy, H = 76, 292, 104, 226, 386
    else:
        # No section header, so the panel starts at the top and everything
        # shifts up by 26px rather than leaving a gap where the title was.
        ptop, ph, tiles_y, iy, H = 16, 326, 78, 200, 356

    o = ''
    if header:
        o += D.section_header(px + 24, 46, '~/activity', 'PUBLIC GITHUB ACTIVITY',
                              right='LIVE DATA', right_icon=D.i_pulse, w=pw - 48)
        o += D.text(px + pw - 172, 44, '@' + user, size=12.5, fill=D.CYAN,
                    tracking=1.4, anchor='end')
        o += D.text(px + pw - 160, 44, '|', size=12.5, fill=D.LINE_3)

    o += D.panel(px, ptop, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
    o += D.brackets(px, ptop, pw, ph, color=D.CYAN, arm=18, sw=2,
                    corners='tl,tr,bl,br', opacity=0.55)

    if not header:
        o += D.text(cx, 46, 'PUBLIC GITHUB ACTIVITY', size=14, fill=D.CYAN,
                    weight='700', tracking=3.2)
        o += D.label(right, 46, 'LIVE DATA', size=11.5, fill=D.CYAN_DIM,
                     tracking=3, anchor='end')
        lw = D.tw('LIVE DATA', 11.5, 3)
        o += D.i_pulse(right - lw - 26, 33, 15, D.CYAN_DIM)
        o += D.text(right - lw - 38, 46, '|', size=12.5, fill=D.LINE_3, anchor='end')
        o += D.text(right - lw - 50, 46, '@' + user, size=12.5, fill=D.CYAN,
                    tracking=1.4, anchor='end')
        o += D.hline(cx, 62, inner, D.LINE_2)

    gap = 12
    n = 6
    tw_ = (inner - gap * (n - 1)) / n
    for i, (lab, val, note, col, icon) in enumerate(tiles(m)):
        o += D.metric_tile(cx + i * (tw_ + gap), tiles_y, tw_, 104, lab, val, note, col, icon)

    ih = 122
    lw = inner * 0.60
    o += D.panel(cx, iy, lw, ih, fill=D.SURFACE_2, stroke=D.LINE)
    o += D.label(cx + 20, iy + 26, 'ACTIVITY INSIGHTS', size=11.5, fill=D.CYAN, tracking=2.8)
    rows = insights(m)
    for i, (icon, k, v, col) in enumerate(rows[:4]):
        ry = iy + 52 + i * 20
        o += icon(cx + 20, ry - 12, 15, D.CYAN_DIM)
        o += D.text(cx + 44, ry, k, size=12.5, fill=D.TEXT)
        o += D.text(cx + lw - 20, ry, v, size=12.5, fill=col, weight='600', anchor='end')

    sx = cx + lw + 16
    sw_ = inner - lw - 16
    o += D.panel(sx, iy, sw_, ih, fill=D.SURFACE_2, stroke=D.LINE)
    o += D.label(sx + 20, iy + 26, 'SCOPE', size=11.5, fill=D.CYAN, tracking=2.8)
    o += D.text(sx + 20, iy + 50, 'Public activity only. Private', size=12, fill=D.MUTED)
    o += D.text(sx + 20, iy + 68, 'contributions are not counted.', size=12, fill=D.MUTED)
    o += D.i_clock(sx + 20, iy + 82, 15, D.CYAN_DIM)
    o += D.text(sx + 44, iy + 94, 'LAST SYNC  ' + stamp, size=11.5, fill=D.FAINT, tracking=1.2)
    o += D.status_dot(sx + sw_ - 26, iy + 22, D.GREEN, 4)

    return D.doc(W, H, 'Public GitHub activity for ' + user, desc(m, stamp), o)


def narrow(m, user, stamp, header=True):
    """Phone composition for the activity card.

    Designed on a 340-unit canvas rather than 440. README images are capped at
    the column width, so a 440 canvas was being shrunk to ~0.70 on a 390px
    phone and every label lost a third of its size. At 340 the same card
    renders near 1:1 between 390 and 440, and scales UP on wider phones, which
    is lossless for SVG.

    This is a real recomposition, not the wide card scaled: 2-column metric
    grid, insights full width beneath it, and scope/sync stacked below rather
    than squeezed alongside.
    """
    W = 340
    px, pw = 8, W - 16
    # 66, not 46: the subtitle baseline sits 26px below the title, so a panel
    # starting at 46 would be drawn straight through "PUBLIC GITHUB ACTIVITY".
    py = 66 if header else 12
    cx = px + 11
    inner = pw - 22

    o = ''
    if header:
        o += D.section_header(px + 4, 30, '~/activity', 'PUBLIC GITHUB ACTIVITY')
        top = py + 14
    else:
        o += D.text(cx, py + 22, 'PUBLIC GITHUB ACTIVITY', size=11, fill=D.CYAN,
                    weight='700', tracking=1.8)
        o += D.status_dot(cx + inner - 38, py + 18, D.GREEN, 3.5)
        o += D.label(cx + inner, py + 22, 'LIVE', size=9.5, fill=D.GREEN,
                     tracking=1.6, anchor='end')
        o += D.text(cx, py + 38, '@' + user, size=9.5, fill=D.MUTED, tracking=1)
        o += D.hline(cx, py + 48, inner, D.LINE_2)
        top = py + 60

    # ---- 2-column metric grid ----
    gap = 8
    tw_ = (inner - gap) / 2
    th = 82
    for i, (lab, val, note, col, icon) in enumerate(tiles(m)):
        c, r = i % 2, i // 2
        o += D.metric_tile(cx + c * (tw_ + gap), top + r * (th + gap),
                           tw_, th, lab, val, note, col, icon,
                           pad=11, icon_px=13, label_px=8.6, value_px=27,
                           note_px=8.2, glow=None)

    # ---- insights, full width ----
    iy = top + 3 * (th + gap) + 8
    rows = insights(m)
    ih = 26 + len(rows) * 20
    o += D.panel(cx, iy, inner, ih, fill=D.SURFACE_2, stroke=D.LINE)
    o += D.label(cx + 12, iy + 18, 'ACTIVITY INSIGHTS', size=9.5, fill=D.CYAN, tracking=2)
    for i, (icon, k, v, col) in enumerate(rows):
        ry = iy + 38 + i * 20
        o += icon(cx + 12, ry - 10, 12, D.CYAN_DIM)
        o += D.text(cx + 30, ry, k, size=10.5, fill=D.TEXT)
        o += D.text(cx + inner - 12, ry, v, size=10.5, fill=col, weight='600', anchor='end')

    # ---- scope + sync, stacked below (never beside on a phone) ----
    sy = iy + ih + 10
    sh = 62
    o += D.panel(cx, sy, inner, sh, fill=D.SURFACE_2, stroke=D.LINE)
    o += D.label(cx + 12, sy + 17, 'SCOPE', size=9.5, fill=D.CYAN, tracking=2)
    o += D.text(cx + 12, sy + 32, 'Public activity only. Private', size=9.5, fill=D.MUTED)
    o += D.text(cx + 12, sy + 44, 'contributions are not counted.', size=9.5, fill=D.MUTED)
    o += D.i_clock(cx + 12, sy + 50, 11, D.CYAN_DIM)
    o += D.text(cx + 28, sy + 59, 'LAST SYNC  ' + stamp, size=8.6, fill=D.FAINT, tracking=.8)

    ph = sy + sh + 12 - py
    H = py + ph + 10
    frame = (D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
             + D.brackets(px, py, pw, ph, color=D.CYAN, arm=12, sw=1.6,
                          corners='tl,tr,bl,br', opacity=0.55))
    return D.doc(W, H, 'Public GitHub activity for ' + user, desc(m, stamp), frame + o)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else 'dist'
    user = os.environ.get('PROFILE_USER', 'cybersec-iq')
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        raise SystemExit('GITHUB_TOKEN is required')

    m = derive(fetch(user, token))
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    os.makedirs(out, exist_ok=True)
    # `activity*` carries its own section header, because the README embeds it
    # bare. `activity-embed` omits it: the Pages site renders `~/activity`
    # above the card, and printing it twice reads as a mistake. Pages scales
    # the wide card responsively, so no narrow embed variant is emitted.
    for name, svg in (('activity.svg', wide(m, user, stamp)),
                      ('activity-narrow.svg', narrow(m, user, stamp)),
                      ('activity-embed.svg', wide(m, user, stamp, header=False)),
                      ('activity-embed-narrow.svg', narrow(m, user, stamp, header=False))):
        ET.fromstring(svg)
        with open(os.path.join(out, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(svg)
        print('  %-24s %5.1f KB' % (name, len(svg) / 1024))

    for k in ('contributions', 'commits', 'prs', 'issues', 'repos', 'followers',
              'longest', 'current', 'best', 'active', 'window'):
        print('  %-20s %s' % (k, m[k]))


if __name__ == '__main__':
    main()
