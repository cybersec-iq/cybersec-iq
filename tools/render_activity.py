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


def wide(m, user, stamp):
    W, H = 1200, 386
    px, pw = 22, 1200 - 44

    o = D.section_header(px + 24, 46, '~/activity', 'PUBLIC GITHUB ACTIVITY',
                         right='LIVE DATA', right_icon=D.i_pulse, w=pw - 48)

    ph = 292
    o += D.panel(px, 76, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
    o += D.brackets(px, 76, pw, ph, color=D.CYAN, arm=18, sw=2,
                    corners='tl,tr,bl,br', opacity=0.55)

    o += D.text(px + pw - 172, 44, '@' + user, size=12.5, fill=D.CYAN,
                tracking=1.4, anchor='end')
    o += D.text(px + pw - 160, 44, '|', size=12.5, fill=D.LINE_3)

    cx = px + 30
    inner = pw - 60
    gap = 12
    n = 6
    tw_ = (inner - gap * (n - 1)) / n
    for i, (lab, val, note, col, icon) in enumerate(tiles(m)):
        o += D.metric_tile(cx + i * (tw_ + gap), 104, tw_, 104, lab, val, note, col, icon)

    iy, ih = 226, 122
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


def narrow(m, user, stamp):
    W = 440
    px, py, pw = 10, 58, W - 20
    cx = px + 14
    inner = pw - 28

    o = D.section_header(px + 8, 34, '~/activity', 'PUBLIC GITHUB ACTIVITY')

    gap = 10
    tw_ = (inner - gap) / 2
    th = 84
    for i, (lab, val, note, col, icon) in enumerate(tiles(m)):
        c, r = i % 2, i // 2
        o += D.metric_tile(cx + c * (tw_ + gap), py + 16 + r * (th + gap),
                           tw_, th, lab, val, note, col, icon)

    iy = py + 16 + 3 * (th + gap) + 6
    rows = insights(m)
    ih = 30 + len(rows) * 22
    o += D.panel(cx, iy, inner, ih, fill=D.SURFACE_2, stroke=D.LINE)
    o += D.label(cx + 14, iy + 20, 'ACTIVITY INSIGHTS', size=10.5, fill=D.CYAN, tracking=2.2)
    for i, (icon, k, v, col) in enumerate(rows):
        ry = iy + 44 + i * 22
        o += icon(cx + 14, ry - 11, 14, D.CYAN_DIM)
        o += D.text(cx + 36, ry, k, size=11.5, fill=D.TEXT)
        o += D.text(cx + inner - 14, ry, v, size=11.5, fill=col, weight='600', anchor='end')

    ny = iy + ih + 20
    o += D.text(cx, ny, 'Public activity only. Private', size=10.5, fill=D.FAINT)
    o += D.text(cx, ny + 14, 'contributions are not counted.', size=10.5, fill=D.FAINT)
    o += D.text(cx, ny + 30, 'LAST SYNC  ' + stamp, size=10.5, fill=D.FAINT, tracking=1)

    ph = ny + 42 - py
    H = py + ph + 12
    frame = (D.panel(px, py, pw, ph, fill=D.SURFACE, stroke=D.LINE_2, rx=4)
             + D.brackets(px, py, pw, ph, color=D.CYAN, arm=14, sw=1.8,
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
    for name, svg in (('activity.svg', wide(m, user, stamp)),
                      ('activity-narrow.svg', narrow(m, user, stamp))):
        ET.fromstring(svg)
        with open(os.path.join(out, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(svg)
        print('  %-24s %5.1f KB' % (name, len(svg) / 1024))

    for k in ('contributions', 'commits', 'prs', 'issues', 'repos', 'followers',
              'longest', 'current', 'best', 'active', 'window'):
        print('  %-20s %s' % (k, m[k]))


if __name__ == '__main__':
    main()
