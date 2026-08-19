# Showcase repositories — plan

The account has 0 public repositories and 12 private ones. That gap is the
weakest part of the profile: the README describes serious systems, but a
visitor cannot see evidence of any of them.

**This is not solved by making anything public.** No existing repository should
change visibility — they contain client work, credentials, infrastructure
detail and business logic. The fix is *new, documentation-only* repositories
that describe engineering decisions without shipping the code that implements
them.

Nothing here has been created. Each one needs owner review before it exists,
because only the owner can judge what a given client agreement permits.

---

## The rule that makes this safe

A showcase repository contains **prose, diagrams and generic illustrative
snippets only**. Concretely:

**Safe to publish**

- Architecture decisions and the reasoning behind them
- Problem statement, constraints, trade-offs considered
- Technology choices and why alternatives were rejected
- Generic code patterns rewritten from scratch as illustrations
- Redacted diagrams: boxes and arrows, no hostnames, no IPs
- Screenshots with all customer data replaced by obvious fixtures

**Never publish**

- Any file copied out of a private repository
- `.env` files, keys, tokens, connection strings, certificates
- Real hostnames, internal IPs, bucket names, queue names, database names
- Client names or logos without written permission
- Real customer, order, payment or user records — including in screenshots
- Schema dumps that reveal a client's commercial model

**Before every push:** `git diff --staged` in full, plus a secret scan. Enable
GitHub secret scanning and push protection on each new repository.

---

## Proposed repositories

Ordered by value-per-effort. Two or three well-built ones beat six thin ones.

### 1. `snake-protocol` — extract, highest value per hour

The playable Snake already built in this profile repository, lifted into a
standalone repository.

- **Why it works:** it is entirely original, has zero dependencies, ships with
  a real test suite and a CI pipeline, and it is already live. Nothing needs
  redacting because nothing is confidential.
- **Contents:** game source, `tests/snake.test.js`, the verify workflow, a
  README covering the fixed-timestep loop, input queueing to prevent
  180-degree reversal, DPR-aware canvas scaling and the reduced-motion path.
- **Effort:** an afternoon. It is a copy plus a README.

### 2. `commerce-platform-notes` — engineering write-up

Documentation-only case study of a multilingual commerce platform, generalised
away from any single client.

- **Contents:** i18n and content-model strategy, catalogue and pricing data
  modelling, checkout state machine, order-integrity constraints, caching and
  invalidation, deployment topology as a redacted diagram.
- **Redaction burden:** medium. Never name the client without permission;
  describe the domain, not the account.

### 3. `platform-hardening-checklist` — security credibility, zero risk

An opinionated, practical checklist for shipping a web platform safely.

- **Contents:** authentication and session handling, tenant isolation, secret
  management, dependency review cadence, CSP and security headers, backup and
  restore drills, incident runbook skeleton.
- **Why it works:** it demonstrates security judgement without claiming any
  certification, CVE, pentest engagement or offensive-security credential.
  Keep it that way — the value is in the reasoning, not in claimed authority.
- **Redaction burden:** none. Write it from scratch.

### 4. `ci-templates` — reusable and genuinely useful

The GitHub Actions workflows actually relied on day to day, generalised.

- **Contents:** least-privilege `permissions:` blocks, deploy gating,
  dependency-review workflow, reusable workflow patterns, concurrency groups.
- **Why it works:** other engineers can copy it, which is what earns stars
  honestly.
- **Redaction burden:** low — strip environment names, secret names and any
  self-hosted runner labels.

### 5. `ai-agent-patterns` — supports the AI positioning

Patterns for putting LLM features into production products.

- **Contents:** retrieval design and chunking trade-offs, tool-calling
  boundaries, prompt-injection mitigations, evaluation harness structure, cost
  and latency controls, failure and fallback behaviour.
- **Redaction burden:** medium. Describe patterns; never publish production
  prompts, model routing rules or vendor pricing terms.

---

## Standard shape for each repository

```text
<repo>/
  README.md              problem, constraints, decisions, outcome
  docs/
    architecture.md      redacted diagram + narrative
    decisions/           short ADRs: context, decision, consequences
  examples/              runnable illustrative snippets, written from scratch
  LICENSE               MIT for code, CC BY 4.0 for prose
  .github/workflows/     CI, even if it only lints Markdown and links
```

Every README should open with one line stating what it is and one stating what
it deliberately does not contain — that sentence is itself a security signal.

---

## Suggested sequence

| Step | Repository | Why this order |
| :--- | :--- | :--- |
| 1 | `snake-protocol` | Zero redaction risk, immediately pinnable |
| 2 | `platform-hardening-checklist` | Zero redaction risk, supports the security positioning |
| 3 | `ci-templates` | Low risk, genuinely reusable by others |
| 4 | `commerce-platform-notes` | Needs a client-permission decision first |
| 5 | `ai-agent-patterns` | Highest writing effort, do it when there is time to do it well |

Start with 1 and 2. Two real public repositories with working CI change the
profile more than five abandoned ones ever would.
