# Profile settings — recommendations

Everything in this file is an **owner action**. None of it was applied
automatically: GitHub account metadata requires the `user` OAuth scope, and the
CLI session used to build this repository holds only `gist`, `read:org`, `repo`
and `workflow`. Contribution-visibility is a web-only setting with no API at
all.

---

## 1. Enable private contributions on the profile — highest impact

**Settings → Profile → Contributions → “Include private contributions on my
profile”**

This is the single change that most improves the profile, and it costs nothing
in privacy: GitHub shows only that activity occurred, never the repository
name, the diff or the commit message.

Why it matters right now:

| Signal | Today | After enabling |
| :--- | :--- | :--- |
| Public contribution graph | 1 day of activity | Reflects real daily work |
| Contribution snake animation | Renders an almost empty grid | Renders a full year of activity |
| GitHub stats card | Near-zero commit count | Counts real commits |

Verified during setup: commits across the private repositories are correctly
authored as `283434677+cybersec-iq@users.noreply.github.com` and are already
attributed to this account — so the activity exists, it is simply hidden. The
graph fills in as soon as the setting is on; nothing needs to be recommitted.

---

## 2. Bio

**Current**

> Cybersecurity-minded Full Stack Developer building websites, apps, bots,
> automation tools and APIs with React, Next.js, Python and Node.js.

It is accurate but reads as a tool list, and it spends its first words on a
hedge (“-minded”).

**Recommended** (159 characters, within GitHub’s 160 limit)

```text
Full-stack engineer building secure products, AI features and automation.
TypeScript · Next.js · Node · Python · PostgreSQL · Docker. Muscat, Oman.
```

**Shorter alternative** (98 characters)

```text
Full-stack engineer. Secure products, AI systems and automation. TypeScript, Node, Python, Docker.
```

Both state only what the repositories already support — no certifications,
employers, clients or security credentials are implied.

---

## 3. Location

**Current:** `oman ` (lowercase, trailing space)
**Recommended:** `Muscat, Oman`

Matches the profile README and the website, and reads as deliberate.

---

## 4. Website

**Current:** `aryaniq.com` — correct, verified reachable over HTTPS during
setup. No change needed.

---

## 5. Social links

**Settings → Profile → Social accounts**

Left empty deliberately. No LinkedIn or Instagram URL was added anywhere in
this profile because none could be verified as belonging to this account, and
inventing a link is worse than omitting one.

If those accounts exist, add them in the profile settings — GitHub renders them
in the sidebar automatically, which is cleaner than badges in the README. Send
the verified URLs and they can be added to the README contact table too.

---

## 6. Pinned repositories

**Profile → Customize your pins**

Pins currently have nothing to show: the account has 0 public repositories.
Once this repository is public, pin it first — it is a real, working artefact
with CI, tests and a deployed site.

Recommended pin order as public repositories appear:

1. `cybersec-iq` — this profile repository (Pages site + playable Snake + CI)
2. A documentation-only showcase repository (see `SHOWCASE_REPOSITORIES_PLAN.md`)
3. A second showcase repository, ideally a different domain to the first
4. Any genuinely reusable open-source utility extracted from private work

Pin quality over quantity. Three strong pins read better than six weak ones.

---

## 7. Things deliberately not changed

| Item | Why |
| :--- | :--- |
| Avatar | Out of scope; explicitly excluded |
| Username | Out of scope; explicitly excluded |
| Account security settings | Out of scope; explicitly excluded |
| Private repository visibility | No existing repository was made public |
| Any other repository | Only `cybersec-iq/cybersec-iq` was created or touched |
