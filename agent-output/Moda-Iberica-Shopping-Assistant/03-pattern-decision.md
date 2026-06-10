---
artifact: pattern-decision
engagement: "Moda-Iberica-Shopping-Assistant"
based_on:
  - 01-requirements.md
  - 02-challenges.md
generated_by: pattern-selector
generated_on: "2026-05-27"
status: draft
---

# Pattern Decision — Moda Ibérica

## Recommendation

**Recommended pattern:** Pattern selection deferred — resolve red flags first

**One-line rationale:** `02-challenges.md` identifies five blocking unknowns (PII/authN for WISMO, EU-only enforcement, network stance, peak reliability/DORA readiness expectations, and model licensing/procurement), and selecting a landing zone pattern before those are answered would be speculative.

**Primary citation:** Azure landing zones are the recommended foundation for workloads, and AI workloads are deployed into application landing zones rather than requiring a separate dedicated AI landing zone ([source](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/#application-landing-zone-accelerators)).

---

## Decision matrix

Scoring: 1 (poor fit) — 5 (excellent fit). See `.github/skills/ai-landing-zone-decision/SKILL.md` for the rubric.

**Scoring deferred:** until the red flags are resolved, any numeric scoring would embed assumptions that could flip the recommendation.

| Criterion              | AI LZ Foundry | AI Gateway LZ | AI Hub LZ | Accelerator | Custom |
|------------------------|---------------|---------------|-----------|-------------|--------|
| Fit to requirements    | TBD           | TBD           | TBD       | TBD         | TBD    |
| Time to prod           | TBD           | TBD           | TBD       | TBD         | TBD    |
| Operational complexity | TBD           | TBD           | TBD       | TBD         | TBD    |
| Cost predictability    | TBD           | TBD           | TBD       | TBD         | TBD    |
| Governance maturity    | TBD           | TBD           | TBD       | TBD         | TBD    |
| Exit cost              | TBD           | TBD           | TBD       | TBD         | TBD    |
| **Score (sum)**        | TBD           | TBD           | TBD       | TBD         | TBD    |

---

## Tradeoffs (what changes the answer)

Use this table in the next customer workshop to converge quickly once red flags are closed.

| If the customer answers… | Then prefer… | Why (Learn-grounded) |
|---|---|---|
| "We need private networking / enterprise governance and we’re willing to build on Azure landing zones" | **AI Landing Zone for Foundry** | Microsoft provides a baseline Foundry chat reference architecture designed for deployment inside an Azure landing zone, including private endpoints and an application-vs-platform landing zone split ([source](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone)). |
| "We need a central throttling / quota / policy enforcement layer in front of one or many model endpoints" | **AI Gateway Landing Zone** (APIM-fronted) | The API Management landing zone accelerator includes a generative AI gateway scenario and points to the gateway offloading pattern for GenAI model access ([source](https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/app-platform/api-management/landing-zone-accelerator#generative-ai-gateway-scenario); [source](https://learn.microsoft.com/azure/architecture/ai-ml/guide/azure-openai-gateway-guide)). |
| "We need hub-and-project sharing across multiple teams" | **AI Hub Landing Zone** | Foundry (classic) describes hubs as a way to share configurations like data connections across projects and centrally manage security settings and spend ([source](https://learn.microsoft.com/azure/foundry-classic/how-to/hub-create-projects#create-a-hub-project); [source](https://learn.microsoft.com/azure/foundry-classic/concepts/ai-resources#create-a-hub-based-project)). |
| "This must ship fast as a pilot and we accept rework before full production hardening" | **Lightweight Accelerator** | Microsoft documents the concept of application landing zone accelerators to speed deployment of workloads in application landing zones ([source](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/#application-landing-zone-accelerators)). *Note:* a Moda Ibérica-specific “single-resource-group accelerator” pattern is not uniquely defined on Microsoft Learn; treat any such approach as a time-boxed pilot design and re-validate before production. |
| "We have constraints none of the above patterns can satisfy (sovereign cloud / on-prem inference / strict egress restrictions)" | **Custom Build** | When the environment requires constraints outside standard landing zone assumptions, you must explicitly design for those constraints and verify service connectivity/egress requirements ([source](https://learn.microsoft.com/azure/cloud-adoption-framework/ai/ready#establish-an-ai-foundation)). |

---

## Why the recommended pattern wins

This engagement cannot defensibly pick a pattern yet. The gating items materially affect whether the assistant can be built as an internet-facing workload with appropriate security posture and operational readiness.

- **Private networking and workload placement are not decided** (C-17). Microsoft’s Foundry-in-landing-zone guidance assumes significant networking dependencies (private endpoints + DNS) and a platform/workload split, which requires early alignment ([source](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone#networking)).
- **EU-only and PII handling needs enforceable design rules** (C-11/C-18). This impacts which services can be used and where telemetry/conversation data can be stored ([source](https://learn.microsoft.com/azure/cloud-adoption-framework/ai/ready#establish-an-ai-foundation)).
- **If an AI gateway becomes required, it changes the landing zone shape** (C-03/C-04/C-09). Microsoft documents a GenAI gateway approach using API Management and a dedicated landing zone accelerator for APIM ([source](https://learn.microsoft.com/azure/api-management/genai-gateway-capabilities); [source](https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/app-platform/api-management/landing-zone-accelerator#generative-ai-gateway-scenario)).

---

## Runners-up

### AI Landing Zone for Foundry

**Why considered:** Strong fit for an EU-resident, production-grade conversational assistant that likely needs private endpoints and enterprise governance.

**Why not chosen:** Cannot validate key prerequisites yet (network stance, identity/authZ, EU-only enforcement scope, retention/deletion, operational SLOs) (see C-08, C-11/C-18, C-15, C-17).

### AI Gateway Landing Zone (APIM-fronted)

**Why considered:** If Moda Ibérica needs centralized throttling/rate limiting, token usage tracking, or routing across multiple model endpoints (especially at Black Friday peak), a gateway can be a first-class requirement.

**Why not chosen:** It’s only justified once model hosting strategy and peak-load controls are agreed; it also introduces extra cost and latency surfaces (C-03/C-04/C-09).

---

## Patterns eliminated

- **AI Hub Landing Zone**: Not eliminated, but needs confirmation that Moda Ibérica truly needs shared hub governance across multiple teams/projects, and whether they are using Foundry (classic) hub model intentionally ([source](https://learn.microsoft.com/azure/foundry-classic/concepts/ai-resources#create-a-hub-based-project)).
- **Lightweight Accelerator**: Not eliminated, but cannot be selected as a production pattern until “pilot vs production” scope and governance requirements are explicit ([source](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/#application-landing-zone-accelerators)).
- **Custom Build**: Not eliminated, but should only be chosen if the customer has a disqualifier constraint that prevents using the landing zone patterns (for example, strict egress prohibitions or on-prem-only inference) ([source](https://learn.microsoft.com/azure/cloud-adoption-framework/ai/ready#establish-an-ai-foundation)).

---

## Disqualifiers checked

Confirm each disqualifier from the skill was evaluated. Mark each yes/no/n-a.

- [ ] Sovereign cloud requirement (TBD)
- [ ] On-prem or edge inference required (TBD)
- [ ] No internet egress allowed (TBD)
- [ ] Single-region active-active HA demanded (TBD)

---

## Open items for Architecture phase

Items deliberately deferred to the Architecture agent (Phase 2):

- Region selection + disaster recovery strategy that satisfies "PII stays in the EU" and the peak-season availability target (depends on customer-approved region list).
- Private networking shape (private endpoints, DNS, egress routing) including dependencies for Foundry and Agent Service as outlined in the baseline landing-zone architecture ([source](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone#networking)).
- Observability, retention, and deletion design for chat transcripts and traces (depends on the GDPR retention/right-to-be-forgotten stance).

---

## Citations

| Claim | Source | Fetch date |
|-------|--------|------------|
| Azure landing zones are the recommended foundation; AI doesn’t require a separate dedicated landing zone | https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/#application-landing-zone-accelerators | 2026-05-27 |
| Foundry chat reference architecture deployed in an Azure landing zone (application vs platform, enterprise setup) | https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone | 2026-05-27 |
| Foundry landing-zone architecture networking dependencies (private endpoints + DNS) | https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone#networking | 2026-05-27 |
| APIM landing zone accelerator includes GenAI gateway scenario | https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/app-platform/api-management/landing-zone-accelerator#generative-ai-gateway-scenario | 2026-05-27 |
| Gateway offloading pattern for Azure OpenAI and other LMs | https://learn.microsoft.com/azure/architecture/ai-ml/guide/azure-openai-gateway-guide | 2026-05-27 |
| AI gateway capabilities in Azure API Management | https://learn.microsoft.com/azure/api-management/genai-gateway-capabilities | 2026-05-27 |
| Foundry hubs/projects relationship and hub purpose (classic) | https://learn.microsoft.com/azure/foundry-classic/how-to/hub-create-projects#create-a-hub-project | 2026-05-27 |
| Hub resources overview (classic) | https://learn.microsoft.com/azure/foundry-classic/concepts/ai-resources#create-a-hub-based-project | 2026-05-27 |
| Establish an AI foundation (CAF) | https://learn.microsoft.com/azure/cloud-adoption-framework/ai/ready#establish-an-ai-foundation | 2026-05-27 |

---

## Status of recommendation

- **Customer review:** pending
- **Partner technical specialist review:** pending
- **Ready for Architecture phase:** no
