---
artifact: pattern-decision
engagement: "Sofia-Center"
based_on:
  - 01-requirements.md
  - 02-challenges.md
generated_by: pattern-selector
generated_on: "[YYYY-MM-DD]"
status: draft
---

# Pattern Decision — Sofia Center

## 0. Audience (partner side)

This pre-sales decision is intended for:

- **Solution architect / pre-sales architect** (recommendation + tradeoffs + gates)
- **Infra/platform engineer** (network/identity/governance implications)
- **App developer / lead engineer** (integration + delivery implications)
- **Security/compliance lead** (risk + controls + audit/retention)

> **⚠️ Conditional recommendation — read first.** Challenge **C-02** (5-month deadline with no Platform Landing Zone yet, plus an unscoped platform + workload + application build) is an open **blocker** in [02-challenges.md](02-challenges.md). The pattern below is the right *target* for this customer profile, but committing to a production milestone is **gated on C-02 being resolved** (an agreed phased scope). Do not let this decision be read as "we can ship all of it in 5 months."

## Recommendation

**Recommended pattern:** **AI Landing Zone for Foundry** — a *workload-owned* Microsoft Foundry chat/RAG workload deployed as an **application landing zone** on top of a Cloud Adoption Framework (CAF) **platform landing zone** that must be established first.

**One-line rationale:** It is the only pattern Microsoft positions for a regulated, private-networked, production-grade Foundry workload at this scale, with built-in identity/network/governance — and EU-only processing can be enforced within it via Azure Policy + Data Zone deployments.

**Primary citation:** [Baseline Microsoft Foundry chat reference architecture in an Azure landing zone](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone)

**Key prerequisite (ties to C-02):** No platform landing zone exists today ([01-requirements.md](01-requirements.md), §6). Per CAF, AI is "just another workload" deployed into an application landing zone *on top of a platform landing zone* — the platform foundation is a prerequisite, not part of the AI workload ([AI in Azure landing zones](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/#ai-in-azure-landing-zones); [Ready your Azure environment for workloads](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/)).

---

## Decision matrix

Scoring: 1 (poor fit) — 5 (excellent fit). See `.github/skills/ai-landing-zone-decision/SKILL.md` for the rubric.

| Criterion              | AI LZ Foundry | AI Gateway LZ | Accelerator | Custom |
|------------------------|:-------------:|:-------------:|:-----------:|:------:|
| Fit to requirements    | 5             | 3             | 2           | 3      |
| Time to prod           | 2             | 3             | 5           | 1      |
| Operational complexity | 2             | 2             | 5           | 1      |
| Cost predictability    | 3             | 3             | 4           | 2      |
| Governance maturity    | 5             | 4             | 1           | 2      |
| Exit cost              | 3             | 3             | 2           | 1      |
| **Score (sum)**        | **20**        | **18**        | **19**      | **10** |

> **Why the winner is not just "highest sum":** the Lightweight Accelerator (19) scores close on speed but **governance maturity = 1** is disqualifying for GDPR-scoped personal data at ~100k users ([01-requirements.md](01-requirements.md), §4). The rubric and skill explicitly warn against promoting an Accelerator to production for regulated workloads. AI LZ Foundry wins on both the highest sum **and** the absence of a disqualifying criterion.

---

## Why the recommended pattern wins

- **Built for this exact scenario.** Microsoft's reference architecture deploys the baseline Foundry chat workload into an application landing zone, with the *workload as the owner of the Foundry resource* explicitly called the recommended approach ([Baseline Foundry LZ](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone)).
- **Private networking is native, not bolted on.** The pattern uses spoke/hub virtual networks, private endpoints for Foundry/Storage/Key Vault/AI Search, NSGs, UDRs, and controlled egress through a platform firewall — matching the "private endpoints, restricted public access" requirement ([Baseline Foundry LZ — Networking](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone#networking); [01-requirements.md](01-requirements.md), §6).
- **EU-only processing is enforceable inside the pattern.** Azure administrators can use **Azure Policy to prohibit "Global" deployment types**, and **Data Zone (EU)** deployments keep inference within EU Member Nations while data at rest stays in the resource's Geo ([EU Data Boundary — optional capabilities](https://learn.microsoft.com/privacy/eudb/eu-data-boundary-transfers-for-optional-capabilities); [Deployment types — data processing locations](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/deployment-types#azure-ai-foundry-deployment-data-processing-locations)). This is the mechanism that resolves the C-04 residency-vs-model tradeoff.
- **Governance/identity/audit are in the box.** The pattern integrates Azure Policy (incl. platform DINE policies), centralized + workload Azure Monitor/Application Insights logging, and Entra-based access — matching the GDPR audit/retention and federated-identity requirements ([Baseline Foundry LZ — Monitor resources](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone#monitor-resources)).
- **There is a usable IaC starting point.** The platform foundation can be stood up with the **Azure Landing Zones IaC Accelerator** (AVM, Bicep/Terraform) ([Platform landing zone implementation options](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/implementation-options)), and the AI workload has an AVM pattern module and a reference implementation ([AI Landing Zone for Foundry — AVM/docs](https://aka.ms/ailz/website); [Foundry baseline LZ reference implementation](https://github.com/Azure-Samples/microsoft-foundry-baseline-landing-zone)). _[verification needed — confirm current AVM module version and Preview status at build time; AVM modules move fast.]_

---

## Runners-up

### Runner-up 1 — AI Gateway Landing Zone (APIM-fronted)

**Why considered:** Researchers are heavy API consumers (~15–20% of users) and the customer wants per-segment quotas, rate limits, and policy — exactly what an APIM AI gateway provides, with central observability and multi-model routing.

**Why not chosen:** It is **complementary to, not a replacement for**, the Foundry LZ — it governs *how consumers reach* the models and sits *in front of* Foundry. Best added as a later phase/component on top of the AI LZ Foundry, not selected instead of it.

### Runner-up 2 — Lightweight Accelerator

**Why considered:** The ~5-month deadline and the value of an early PoC/pilot make a single-resource-group quickstart attractive for proving scope (C-01) fast.

**Why not chosen:** It has **no governance, identity, network, or audit foundations** — unacceptable for GDPR-scoped personal data at ~100k users, and promoting it to production would mean significant rework. Usable only as a throwaway PoC, explicitly redone before prod.

---

## Patterns eliminated

- **Custom Build:** No disqualifier present that an LZ cannot handle — there is no sovereign-cloud, edge, on-prem-hybrid, or specialized-SKU constraint. EU residency is satisfied inside the LZ via Data Zone + Azure Policy, so a bespoke build would only add design burden and exit cost.

---

## Disqualifiers checked

- [x] Sovereign cloud requirement — **No.** Requirement is EU Data Boundary (public Azure EU regions), satisfied by Data Zone deployments + Azure Policy, not a sovereign cloud ([EU Data Boundary](https://learn.microsoft.com/privacy/eudb/eu-data-boundary-transfers-for-optional-capabilities)).
- [x] On-prem or edge inference required — **No** _(nothing in 01/02 indicates this; confirm at workshop)_.
- [x] No internet egress allowed — **N/A / TBD.** Pattern supports controlled egress via platform firewall; confirm exact egress stance with customer ([Baseline Foundry LZ — Networking](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone#networking)).
- [x] Single-region active-active HA demanded — **Open (C-09).** 99.5% target + single EU region. Data Zone routes within the EU zone for availability, but a regional outage impacts traffic routed there; a second EU region or graceful degradation may be needed for a contractual SLA ([Deployment types — data processing locations](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/deployment-types#azure-ai-foundry-deployment-data-processing-locations); [BCDR for Azure OpenAI](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/business-continuity-disaster-recovery#standard-deployments)).

---

## Open items for Architecture phase

Deferred to the Architecture agent (Phase 2):

- Specific EU target region and the per-deployment-type model availability there (closes C-04).
- Hub/spoke topology specifics, private DNS zone ownership, and the Agent Service private-endpoint dependency set ([Baseline Foundry LZ — Networking](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone#networking)).
- Single- vs dual-EU-region resilience design for the 99.5% target (C-09).
- Whether/when to add the APIM AI gateway for per-segment quotas (runner-up 1).
- Current AVM module versions and any Preview status for the AI LZ pattern module.
- Right-to-be-forgotten deletion flow across vector index / transcripts / logs (C-05).

---

## Pre-sales decision gates (must be closed before build)

- **Gate A (Foundation + PoC approval):** Agree the **phased scope that resolves C-02** (what "go-live at month 5" means vs deferred); confirm platform-landing-zone ownership and the EU target region; confirm identity federation scope (C-06); confirm RAG-vs-general-assistant scope (C-01). **This gate clears the blocker.**
- **Gate B (Pilot approval):** Confirm EU residency enforcement design (Azure Policy denying Global deployment types + Data Zone model list, C-04); confirm data-subject erasure flow (C-05); confirm per-segment quota/policy approach and whether the APIM gateway is in pilot scope.
- **Gate C (Production / peak):** Confirm worst-case (exam-period) peak concurrency and capacity/PTU strategy (C-03); confirm 99.5% is target vs contractual and the single- vs multi-region resilience stance (C-09); confirm cost ceiling and budget owner (C-07); confirm audit/retention and governance processes.

---

## Next workshop agenda (pre-sales)

- **Objective:** Close **C-02** (phased scope vs deadline) and **C-04** (residency vs flagship model) so the Architecture phase can begin; confirm AI LZ Foundry fit.
- **Required attendees:**
  - **Customer sponsor / budget owner** — phasing decision, cost ceiling (C-02, C-07) `[TBD — ask customer]`
  - **Customer platform/network owner** — platform landing zone ownership + EU region + egress stance (C-02, networking) `[TBD — ask customer]`
  - **Customer security/identity owner / DPO** — federation scope (C-06), residency enforcement + erasure (C-04, C-05) `[TBD — ask customer]`
  - **Customer application owner** — RAG-vs-general scope and app ownership (C-01, C-08) `[TBD — ask customer]`
  - **Customer operations/SRE** — peak load + SLA/resilience (C-03, C-09) `[TBD — ask customer]`
- **Top questions to answer:**
  1. What is the agreed minimum production scope at month 5, and what is deferred? (C-02 — blocker)
  2. Who owns the platform landing zone, and can it be stood up via the ALZ IaC Accelerator in time?
  3. For the chosen EU region, are the required flagship-tier models available as EU Data Zone deployments, or must the model tier be relaxed? (C-04)
  4. Is 99.5% contractual, and is single-EU-region acceptable for it? (C-09)

---

## Citations

| Claim | Source | Fetch date |
|-------|--------|------------|
| Workload-owned Foundry is the recommended LZ topology | [Baseline Microsoft Foundry chat reference architecture in an Azure landing zone](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone) | 2026-06-12 |
| Private networking model (hub/spoke, private endpoints, controlled egress, private DNS) | [Baseline Foundry LZ — Networking](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone#networking) | 2026-06-12 |
| Workload + platform monitoring/Azure Policy/governance model | [Baseline Foundry LZ — Monitor resources](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone#monitor-resources) | 2026-06-12 |
| AI is "just another workload" in an application LZ on a platform LZ | [AI in Azure landing zones](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/#ai-in-azure-landing-zones) | 2026-06-12 |
| Platform landing zone is the prerequisite foundation | [Ready your Azure environment for workloads](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/) | 2026-06-12 |
| ALZ IaC Accelerator (AVM Bicep/Terraform) to stand up the platform foundation | [Platform landing zone implementation options](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/implementation-options) | 2026-06-12 |
| Azure Policy can prohibit "Global" deployment types; Data Zone keeps EU processing in EU | [EU Data Boundary — optional capabilities](https://learn.microsoft.com/privacy/eudb/eu-data-boundary-transfers-for-optional-capabilities) | 2026-06-12 |
| Global vs Data Zone vs Azure geography deployment data-processing locations | [Deployment types — data processing locations](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/deployment-types#azure-ai-foundry-deployment-data-processing-locations) | 2026-06-12 |
| Single-region outage impact; Data Zone BCDR guidance | [BCDR for Azure OpenAI](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/business-continuity-disaster-recovery#standard-deployments) | 2026-06-12 |
| AI Landing Zone for Foundry AVM pattern module / docs | [AI Landing Zone for Foundry](https://aka.ms/ailz/website) | 2026-06-12 |

---

## Status of recommendation

- **Customer review:** pending
- **Partner technical specialist review:** pending
- **Ready for Architecture phase:** Yes — *conditional*: Architecture work can begin on the AI LZ Foundry pattern, but the C-02 phasing blocker must be closed at Gate A before any production milestone is committed.
