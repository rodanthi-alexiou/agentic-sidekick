---
name: ai-landing-zone-decision
description: Decision logic for choosing between Azure AI Landing Zone for Foundry, AI Gateway LZ (APIM-centric), Lightweight Accelerator, and Custom Build. Use when recommending an Azure AI pattern.
---

# Azure AI Pattern Decision Skill

Reference logic for the Pattern Selector agent. Captures partner field experience — the kind of judgment that isn't on a single Microsoft Learn page but emerges from comparing them.

> **Verify currency.** Microsoft Learn is the authoritative source for current capabilities. Any specific feature, AVM module, region, or status claim made in this skill must be re-verified via `microsoft_docs_search` before being repeated to a customer. The skill captures *decision logic*, not feature lists.

## The five patterns at a glance

> **Important distinction — the AI Gateway LZ is complementary to the Foundry LZ, not an alternative.**
> - **AI Gateway LZ** controls *how external consumers reach AI models* (APIM layer). It sits in front of the Foundry LZ; the two are used together.
>
> **Note on the legacy Hub-Project topology.** Microsoft's current baseline Foundry LZ guidance explicitly de-recommends the centralised Foundry Hub-sharing topology (the Hub-Project model now lives under `foundry-classic` docs). Recommend the workload-owned Foundry LZ instead; this guide does not treat Hub-Project as a selectable pattern.

| Pattern | Best when | Watch out for |
|---------|-----------|---------------|
| **AI Landing Zone for Foundry** | Enterprise workload, regulated or production-grade, CAF Platform LZ exists or is planned, private networking required | Heavier upfront; expects platform LZ underneath; AVM module versions move fast |
| **AI Gateway Landing Zone** | Multiple AI consumers, multi-model routing, quotas/throttling, central observability, BYO models | Adds APIM latency and cost; needs an API platform owner. **Not an alternative to Foundry LZ — sits in front of it.** |
| **Lightweight Accelerator** | 4-8 week PoC, single team, no compliance scope, willingness to redo for prod | Do not let this leak into prod — it has no governance bones |
| **Custom Build** | Edge / sovereign / on-prem hybrid / highly specialized SKUs / scenarios no LZ supports | You own all the design decisions an LZ would have made for you |

## Decision tree (canonical)

```
START
  │
  ├─ Red flags unresolved from Challenger?  ──► STOP, resolve first
  │
  ├─ Regulated data + enterprise scale + private networking?
  │     ├─ Platform LZ exists or planned?  ──► AI Landing Zone for Foundry
  │     └─ No platform LZ context at all?   ──► AI LZ Foundry + flag prerequisite
  │
  ├─ Primary need is multi-consumer governance, quotas, multi-model routing?
  │     ──► AI Gateway Landing Zone (APIM LZ Accelerator)
  │       NOTE: this governs ACCESS to AI models — it is complementary to,
  │       not a replacement for, the Foundry LZ behind it.
  │
  ├─ Customer insists on Hub-Project shared Foundry topology?
  │     ──► CHALLENGE FIRST (see Disqualifiers)
  │       Recommend workload-owned Foundry LZ; the Hub-Project topology
  │       is de-recommended and is not a selectable pattern here
  │
  ├─ PoC, single team, ≤ 8 weeks, no compliance scope?
  │     ──► Lightweight Accelerator
  │       (explicitly note: redo before prod)
  │
  └─ None of the above fit?
        ──► Custom Build
            (must justify why each LZ was rejected)
```

## Disqualifiers (apply before the tree)

A disqualifier overrides the tree's recommendation.

- **Sovereign cloud requirement** → verify Learn for the specific cloud (US Gov, China, sovereign Europe). LZ support varies. Often pushes toward Custom Build with LZ patterns as guidance.
- **On-prem or edge inference required** → none of the LZs cover this. Custom Build with Azure Arc / Azure Local guidance.
- **No internet egress allowed** → check that the chosen pattern's required Microsoft endpoints are reachable via Private Link or service tags. Some Foundry features need egress.
- **Customer demands single-region with active-active HA** → not all AI services support this; verify per service.
- **Customer asks for Hub-Project shared Foundry topology (greenfield)** → challenge against current Microsoft guidance. The [Baseline Foundry LZ architecture](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone) explicitly states: *"we don't recommend this topology… the workload as the owner of the Foundry resource [is] the recommended approach."* Hub-Project docs now live under `foundry-classic`. Recommend workload-owned Foundry LZ instead. If an existing Hub-Project investment genuinely cannot be migrated, treat it as a documented Custom Build constraint rather than a recommended pattern.

## Scoring rubric (for the decision matrix)

Score each candidate pattern 1-5 on each criterion. Use this rubric for consistency.

### Fit to requirements
- 5: Pattern was built for this scenario
- 3: Pattern fits with some customization
- 1: Pattern works against the requirement

### Time to prod
- 5: 4-8 weeks
- 3: 2-4 months
- 1: 6+ months

### Operational complexity
- 5: Single team can operate
- 3: Needs a platform team
- 1: Needs platform + AI + network + security teams in lockstep

### Cost predictability
- 5: Mostly consumption-based, easy to model
- 3: Mix of fixed (gateway, networking) and consumption
- 1: Many variable cost surfaces, hard to budget

### Governance maturity
- 5: Built-in identity, network, audit, policy
- 3: Some built-in, some needs adding
- 1: Bring your own everything

### Exit cost
- 5: Easy to swap models or unwind
- 3: Some lock-in to LZ structure
- 1: Significant rework to leave

## Anti-patterns to call out

If the requirements push toward any of these, surface it explicitly:

- **"Accelerator → prod"**: customers often want to skip the LZ and promote a PoC. State the cost of redoing.
- **"Foundry without networking"**: any regulated workload exposing Foundry on public endpoints is a red flag.
- **"Fine-tune first"**: most teams who ask for fine-tuning have not yet exhausted prompt engineering + RAG. Challenge before agreeing.
- **"Multi-agent for everything"**: agents add operational and cost complexity. Sometimes a workflow with one or two well-prompted calls is enough.
- **"We'll figure out evaluation later"**: if there's no eval harness in the plan, the workload will not reach prod reliably.

## How to use this skill

The Pattern Selector agent should consult this skill alongside live Microsoft Learn lookups. The skill provides *how to decide*; Learn provides *what is currently true*.

Cite Learn URLs in the customer-facing artifact. The skill itself is internal — do not include "as per the partner skill file" in customer output.
