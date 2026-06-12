---
artifact: pattern-decision
engagement: "[engagement-name]"
based_on:
  - 01-requirements.md
  - 02-challenges.md
generated_by: pattern-selector
generated_on: "[YYYY-MM-DD]"
status: draft
---

# Pattern Decision — [Customer Name]

## 0. Audience (partner side)

This pre-sales decision is intended for:

- **Solution architect / pre-sales architect** (recommendation + tradeoffs + gates)
- **Infra/platform engineer** (network/identity/governance implications)
- **App developer / lead engineer** (integration + delivery implications)
- **Security/compliance lead** (risk + controls + audit/retention)

## Recommendation

**Recommended pattern:** [AI Landing Zone for Foundry / AI Gateway LZ / Lightweight Accelerator / Custom Build]

**One-line rationale:** [why this pattern wins for this customer]

**Primary citation:** [Microsoft Learn URL]

---

## Decision matrix

Scoring: 1 (poor fit) — 5 (excellent fit). See `.github/skills/ai-landing-zone-decision/SKILL.md` for the rubric.

| Criterion              | AI LZ Foundry | AI Gateway LZ | Accelerator | Custom |
|------------------------|---------------|---------------|-------------|--------|
| Fit to requirements    |               |               |             |        |
| Time to prod           |               |               |             |        |
| Operational complexity |               |               |             |        |
| Cost predictability    |               |               |             |        |
| Governance maturity    |               |               |             |        |
| Exit cost              |               |               |             |        |
| **Score (sum)**        |               |               |             |        |

---

## Why the recommended pattern wins

[3-5 bullets explaining the fit. Each bullet cites Microsoft Learn for any capability claim.]

- [Reason 1] ([source](https://learn.microsoft.com/...))
- [Reason 2] ([source](https://learn.microsoft.com/...))

---

## Runners-up

### [Runner-up 1]

**Why considered:** [one sentence]

**Why not chosen:** [one sentence]

### [Runner-up 2]

**Why considered:** [one sentence]

**Why not chosen:** [one sentence]

---

## Patterns eliminated

For each pattern not in the runner-up list, one line on why it was eliminated.

- **[Pattern]**: [reason]
- **[Pattern]**: [reason]

---

## Disqualifiers checked

Confirm each disqualifier from the skill was evaluated. Mark each yes/no/n-a.

- [ ] Sovereign cloud requirement
- [ ] On-prem or edge inference required
- [ ] No internet egress allowed
- [ ] Single-region active-active HA demanded

---

## Open items for Architecture phase

Items deliberately deferred to the Architecture agent (Phase 2):

- [Item 1 — e.g., specific AVM module versions]
- [Item 2 — e.g., regional pairing strategy]

---

## Pre-sales decision gates (must be closed before build)

List the minimum decisions required to proceed. Use `[TBD — ask customer]` if unknown.

- **Gate A (PoC approval):** identity model + data handling rules + network stance
- **Gate B (Pilot approval):** high-risk tools (for example WISMO) authZ rules + monitoring/runbooks
- **Gate C (Production/peak):** quotas/throttling strategy + audit/retention + governance processes

---

## Next workshop agenda (pre-sales)

- **Objective:** close the gates above and confirm pattern fit
- **Required attendees:** security/identity owner, application owner, platform/network owner, operations owner [TBD — ask customer]
- **Top questions to answer:** [TBD — copy from red flags / open items]

---

## Citations

| Claim | Source | Fetch date |
|-------|--------|------------|
| [...] | [Learn URL] | [YYYY-MM-DD] |
| [...] | [Learn URL] | [YYYY-MM-DD] |

---

## Status of recommendation

- **Customer review:** [pending / approved / contested]
- **Partner technical specialist review:** [pending / approved]
- **Ready for Architecture phase:** [yes / no]
