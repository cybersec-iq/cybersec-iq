/* Renders the public-activity card from live GitHub data.
 *
 * Exists because the popular third-party stats services are frequently rate
 * limited or down (the one this replaced was returning 503 for every request),
 * and a profile should not depend on someone else's free Vercel quota to
 * render. Zero dependencies: Node 20's global fetch plus string building.
 *
 * Usage:  GITHUB_TOKEN=... PROFILE_USER=cybersec-iq node tools/render-stats.mjs dist/profile-stats.svg
 */

import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname } from 'node:path';

const USER = process.env.PROFILE_USER || 'cybersec-iq';
const TOKEN = process.env.GITHUB_TOKEN;
const OUT = process.argv[2] || 'dist/profile-stats.svg';

if (!TOKEN) {
  console.error('GITHUB_TOKEN is required');
  process.exit(1);
}

const QUERY = `
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
      contributionCalendar { totalContributions }
    }
  }
}`;

const response = await fetch('https://api.github.com/graphql', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${TOKEN}`,
    'Content-Type': 'application/json',
    'User-Agent': 'cybersec-iq-profile'
  },
  body: JSON.stringify({ query: QUERY, variables: { login: USER } })
});

if (!response.ok) {
  console.error(`GitHub API returned ${response.status}`);
  process.exit(1);
}

const payload = await response.json();
if (payload.errors) {
  console.error(JSON.stringify(payload.errors, null, 2));
  process.exit(1);
}

const user = payload.data.user;
const contrib = user.contributionsCollection;

// restrictedContributionsCount is non-zero only once the owner opts in to
// showing private contributions; until then it is honestly reported as 0.
const calendar = contrib.contributionCalendar.totalContributions;

const METRICS = [
  ['CONTRIBUTIONS', calendar, '12 MONTHS'],
  ['COMMITS', contrib.totalCommitContributions, '12 MONTHS'],
  ['PULL REQUESTS', contrib.totalPullRequestContributions, '12 MONTHS'],
  ['ISSUES', contrib.totalIssueContributions, '12 MONTHS'],
  ['PUBLIC REPOS', user.repositories.totalCount, 'OWNED'],
  ['STARS EARNED', user.repositories.nodes.reduce((sum, r) => sum + r.stargazerCount, 0), 'TOTAL'],
  ['FOLLOWERS', user.followers.totalCount, 'TOTAL'],
  ['REPOS TOUCHED', contrib.totalRepositoriesWithContributedCommits, '12 MONTHS']
];

const format = (n) => (n >= 10000 ? (n / 1000).toFixed(1) + 'k' : String(n));
const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' }[c]));

const stamp = new Date().toISOString().slice(0, 10);

const COLS = 4;
const CELL_W = 209;
const CELL_H = 82;
const GRID_X = 24;
const GRID_Y = 74;

const cells = METRICS.map(([label, value, note], i) => {
  const col = i % COLS;
  const row = Math.floor(i / COLS);
  const x = GRID_X + col * (CELL_W + 4);
  const y = GRID_Y + row * (CELL_H + 4);
  const accent = row === 0 ? '#39FF14' : '#00E5FF';
  const delay = (0.12 * i).toFixed(2);

  return `    <g class="cell" style="animation-delay:${delay}s">
      <rect x="${x}" y="${y}" width="${CELL_W}" height="${CELL_H}" fill="#0C1218" stroke="#1B2733" stroke-width="1"/>
      <rect x="${x}" y="${y}" width="3" height="${CELL_H}" fill="${accent}"/>
      <text x="${x + 18}" y="${y + 26}" fill="#7C8B99" font-size="10.5" letter-spacing="2">${esc(label)}</text>
      <text x="${x + 18}" y="${y + 60}" fill="${accent}" font-size="30" font-weight="700" letter-spacing="1.5">${esc(format(value))}</text>
      <text x="${x + CELL_W - 18}" y="${y + 60}" fill="#2A3946" font-size="9.5" letter-spacing="1.6" text-anchor="end">${esc(note)}</text>
    </g>`;
}).join('\n');

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 268" width="900" height="268" role="img" aria-labelledby="sTitle sDesc" preserveAspectRatio="xMidYMid meet">
  <title id="sTitle">Public GitHub activity for ${esc(USER)}</title>
  <desc id="sDesc">${METRICS.map(([l, v]) => `${esc(l)}: ${v}`).join('. ')}. Public activity only, generated ${stamp}.</desc>

  <defs>
    <linearGradient id="sBar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#141C25"/><stop offset="100%" stop-color="#0E141B"/>
    </linearGradient>
    <pattern id="sGrid" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M30 0H0V30" fill="none" stroke="#111A22" stroke-width="1"/>
    </pattern>
    <clipPath id="sClip"><rect x="0" y="0" width="900" height="268" rx="4"/></clipPath>
    <style>
      .mono { font-family: ui-monospace, "JetBrains Mono", "Fira Code", "SFMono-Regular", Menlo, Consolas, monospace; }
      .cell { animation: rise .5s ease-out both; }
      .live { animation: live 2.6s ease-in-out infinite; }
      @keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
      @keyframes live { 0%,100% { opacity: .4; } 50% { opacity: 1; } }
      @media (prefers-reduced-motion: reduce) { .cell, .live { animation: none; } }
    </style>
  </defs>

  <g clip-path="url(#sClip)" class="mono">
    <rect width="900" height="268" fill="#0A0E13"/>
    <rect width="900" height="268" fill="url(#sGrid)"/>

    <rect width="900" height="42" fill="url(#sBar)"/>
    <line x1="0" y1="42" x2="900" y2="42" stroke="#1B2733" stroke-width="1"/>
    <text x="24" y="27" fill="#00E5FF" font-size="13" font-weight="700" letter-spacing="3.4">PUBLIC ACTIVITY</text>
    <text x="222" y="27" fill="#2A3946" font-size="13">/</text>
    <text x="244" y="27" fill="#7C8B99" font-size="13" letter-spacing="2">@${esc(USER)}</text>
    <g transform="translate(806 21)">
      <circle class="live" cx="0" cy="0" r="4" fill="#39FF14"/>
      <text x="14" y="4.5" fill="#39FF14" font-size="11" letter-spacing="2">LIVE</text>
    </g>

${cells}

    <text x="24" y="252" fill="#4A5A68" font-size="10.5" letter-spacing="1.6">PUBLIC ACTIVITY ONLY &#183; PRIVATE CONTRIBUTIONS ARE NOT COUNTED</text>
    <text x="876" y="252" fill="#4A5A68" font-size="10.5" letter-spacing="1.6" text-anchor="end">GENERATED ${stamp}</text>

    <rect x="0.75" y="0.75" width="898.5" height="266.5" rx="4" fill="none" stroke="#1B2733" stroke-width="1.5"/>
  </g>
</svg>
`;

mkdirSync(dirname(OUT), { recursive: true });
writeFileSync(OUT, svg, 'utf8');

console.log(`Rendered ${OUT}`);
for (const [label, value] of METRICS) {
  console.log(`  ${label.padEnd(16)} ${value}`);
}
