---
artifact: challenges
engagement: "Sofia-Center"
based_on: 01-requirements.md
generated_by: challenger
generated_on: "2026-06-12"
status: draft
---

# Challenges — Sofia Center

Socratic stress-test of `01-requirements.md`. Each challenge records the question, the reasoning, the partner's answer, and the outcome. This is a **conversation log** — blank answer fields mean the question still needs a customer session to resolve.

## 0. Audience (partner side)

Use this in a pre-sales workshop with:

- **Solution architect / pre-sales architect** (decision gates + risks)
- **App developer / lead engineer** (integration + tool semantics)
- **Infra/platform engineer** (network/identity/ops constraints)
- **Security/compliance lead** (data handling + audit/retention)

## How to read this document

- **C-XX**: a single challenge. Open-ended question, not a verdict.
- **Answer (recorded)**: what the partner knew at time of challenge session. ⏳ means still needs customer input.
- **Outcome**: ✅ Closed / ⚠️ Risk surfaced / 🚫 Blocker.
- **Red flags**: challenges with a Blocker outcome. Resolve before architecture work begins.

---

## Challenges

### C-01: RAG vs open-ended general-purpose assistant

**Challenges requirement:** §3 AI capabilities — "RAG (embeddings + document Q&A) plus general chat/generation; multimodal and batch inference also referenced."

**Question:** Is the answer space bounded by a defined document corpus, or do you expect open-ended general chat (literature review, coding, free-form generation) across ~100k students, academics, and researchers?

**Why it matters:** A bounded RAG assistant and an open-ended general-purpose chatbot have very different cost, safety, evaluation, and abuse profiles. "Both" usually means the harder one drives the architecture — and the project is sized for the easier one.

**Evidence that would resolve this:** A one-line scope statement: "grounded answers from curated sources only" vs "general assistant with retrieval as one feature," plus the top 3 intended use cases per persona.

**Answer (recorded):** ⏳ No answer yet — needs customer input. Requirements capture both RAG and "general chat/generation" without a primary.

**Outcome:** ⚠️ Risk surfaced — scope is currently unbounded; must be narrowed before pattern selection and cost modelling.

---

### C-02: 5-month deadline with no Platform Landing Zone in place

**Challenges requirement:** §8 "Deployed within ~5 months" combined with §6 "No — no Platform Landing Zone in place yet."

**Question:** In 5 months you intend to stand up a CAF platform foundation, an AI workload landing zone, EU-resident private networking, multi-institution identity federation, the end-user application, and production hardening for ~100k users — what is the must-have production scope at month 5 versus what can be a pilot?

**Why it matters:** Building the platform foundation *and* the workload *and* a custom application to production grade in 5 months is aggressive. Without an agreed minimum viable scope, the date and the scope cannot both hold.

**Evidence that would resolve this:** A phased definition — what "go-live" means (which personas, which institutions, which features) and what is explicitly deferred to a later phase.

**Answer (recorded):** Partner confirmed: no Platform Landing Zone exists yet; hard deadline is ~5 months. No agreed phasing yet.

**Outcome:** 🚫 Blocker — the deadline is not credible against the stated scope until a phased "minimum at month 5" is agreed with the customer.

---

### C-03: Peak concurrency is a partner assumption, and education load is bursty

**Challenges requirement:** §2 "Concurrent users at peak: ~5,000–7,000 concurrent _(ASSUMPTION — partner planning estimate)_."

**Question:** Education traffic spikes hard around class hours, assignment deadlines, and exam periods — is 5–7% peak concurrency realistic, or could a synchronized event (e.g. 50,000 students at exam time) push concurrency 3–5× higher?

**Why it matters:** Peak concurrency drives quota / PTU sizing and therefore both cost and the risk of throttling at the worst possible moment. Under-sizing here produces a visible outage during exams.

**Evidence that would resolve this:** Historical login/usage curves from any existing platform, or the customer's stated worst-case simultaneous-use scenario.

**Answer (recorded):** Partner instructed to use a reasonable planning estimate (~5–7k); this is not a customer-validated figure.

**Outcome:** ⚠️ Risk surfaced — sizing rests on an unvalidated assumption; confirm a worst-case (exam-period) peak with the customer before committing capacity or cost.

---

### C-04: EU-only residency constrains which flagship models are available

**Challenges requirement:** §3 "flagship / balanced / efficient" tiers + §4 "EU-only for all processing... including batch" + §8 "Global (non-EU/EEA) deployment types must be excluded."

**Question:** If the newest flagship reasoning models are only offered as Global (non-residency) deployments in your target EU region, will you accept an older EU-available model for the flagship tier, or relax residency for inference?

**Why it matters:** You cannot have "newest flagship model" and "strict EU residency" simultaneously if that model is Global-only in-region. This is a direct tradeoff the customer must own, not a detail to discover during build.

**Evidence that would resolve this:** Microsoft Learn's Data Zone Batch availability table shows EU regions (France Central, Germany West Central, Poland Central, Sweden Central, West Europe) offering `gpt-4.1` / `gpt-4o` families but **not** `gpt-5` / `gpt-5.1` for Data Zone Batch ([Region availability — Data Zone Batch](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-region-availability#data-zone-batch), fetched 2026-06-12). Resolve by confirming the exact target region and the per-deployment-type model list there.

**Answer (recorded):** ⏳ No answer yet — needs customer input on the residency-vs-model tradeoff.

**Outcome:** ⚠️ Risk surfaced — "newest flagship" and "EU-only batch" may be mutually exclusive in-region; the customer must choose. (Pattern/region selection deferred to Pattern Selector.)

---

### C-05: Right-to-be-forgotten into the vector store and chat history

**Challenges requirement:** §4 "No-training commitment required; GDPR data-subject rights apply."

**Question:** When a data subject requests erasure, how does that propagate to the embeddings/vector index, cached prompts, conversation history, and any logs — and what is your committed turnaround for completing it?

**Why it matters:** Erasure is easy to promise and hard to implement once content has been chunked, embedded, indexed, and logged. If the deletion path is not designed up front, the platform cannot honour GDPR Article 17.

**Evidence that would resolve this:** A documented deletion flow covering source documents, derived embeddings/index entries, transcripts, and diagnostic logs, with a target completion time.

**Answer (recorded):** ⏳ No answer yet — needs customer input on retention periods and erasure SLA.

**Outcome:** ⚠️ Risk surfaced — erasure design is undefined; must be specified before handling regulated personal data.

---

### C-06: Identity federation across many institutions

**Challenges requirement:** §6 "Microsoft Entra ID federating institutional SAML 2.0 / OpenID Connect / WS-Fed identity providers; federated SSO."

**Question:** How many distinct institutional identity providers will federate in (one national IdP, or dozens of individual schools/universities), and who owns onboarding, trust, and de-provisioning for each?

**Why it matters:** "Federate institutional IdPs" for an education sector can mean 1 or 100+ trust relationships. The number drives the identity architecture (single federation vs External ID / B2B vs per-tenant), the onboarding effort, and the 5-month timeline.

**Evidence that would resolve this:** A count (or order of magnitude) of IdPs, their protocols, and whether a single national identity federation already exists that can be reused.

**Answer (recorded):** ⏳ No answer yet — needs customer input.

**Outcome:** ⚠️ Risk surfaced — federation scale is unknown and materially affects identity design and timeline.

---

### C-07: No cost ceiling, public-sector budget

**Challenges requirement:** §5 "Cost ceiling (monthly): [TBD]."

**Question:** As a public-sector buyer, is there a fixed annual budget envelope this must fit inside — and is that ceiling for infrastructure only, or all-in including model token consumption at ~100k users?

**Why it matters:** Token consumption at this user scale is typically the dominant cost and is highly sensitive to the C-01 scope answer. Without a ceiling, there are no guardrails, and a public-sector overspend is a hard failure.
**Evidence that would resolve this:** A monthly or annual budget figure and confirmation of whether it includes model consumption, plus appetite for PTU reservation vs pay-as-you-go.

**Answer (recorded):** ⏳ No answer yet — needs customer input. (Cost modelling deferred to the Cost phase once scope and traffic are confirmed.)

**Outcome:** ⚠️ Risk surfaced — no budget guardrail; cost cannot be bounded until C-01 (scope) and C-03 (peak) are resolved.

---

### C-08: Who builds and owns the end-user application?

**Challenges requirement:** §2 "Web-based end-user GUI / chat application + REST API"; evidence-pack note that GUI, localization, and conversation features are application-layer (partner-built or an accelerator), not native Azure.

**Question:** Is the end-user web application, its localization, conversation history/export, and admin console being built by the partner, taken from the *Chat with your data* accelerator, or owned by the customer — and is that effort inside the 5-month deadline?

**Why it matters:** Azure supplies the model + platform layer; the application is a separate, substantial build. If it is in scope and not yet resourced, the 5-month deadline (C-02) is at further risk.

**Evidence that would resolve this:** A clear statement of application ownership and whether the accelerator is acceptable as-is or needs significant customisation.

**Answer (recorded):** ⏳ No answer yet — needs customer input.

**Outcome:** ⚠️ Risk surfaced — application ownership and effort are undefined and compound the timeline risk.

---

### C-09: 99.5% — internal target or contractual SLA, and single-region resilience

**Challenges requirement:** §5 "Availability SLA: 99.5% target" + §6 "An EU region (within EU data boundary)... specific region not yet selected."

**Question:** Is 99.5% an internal aspiration or a contractual commitment with penalties, and does it have to be met from a single EU region — what is the expectation if that region has an incident during an exam period?

**Why it matters:** A contractual SLA with EU-only residency and a single region constrains the resilience design (and may need a second EU region or graceful degradation). Default platform SLAs and the chosen support plan also affect what can be committed.

**Evidence that would resolve this:** Confirmation of SLA status (target vs contractual), the chosen Azure support plan, and acceptable behaviour during a regional incident.

**Answer (recorded):** ⏳ No answer yet — needs customer input.

**Outcome:** ⚠️ Risk surfaced — SLA intent and single-region resilience expectations are unconfirmed.

---

## Red flags

List any challenges that are blocking-level. If empty, write "None identified."

- [ ] **C-02**: 5-month deadline with no Platform Landing Zone yet, plus an unscoped platform + workload + application build — not credible until a phased "minimum at month 5" is agreed. **Blocker.**
- [ ] **C-04**: Strict EU-only residency may exclude the newest flagship models in-region (per Learn) — the customer must own the model-vs-residency tradeoff. **High risk.**

---

## Recommendation

- **Total challenges asked:** 9
- **Answered / closed:** 0 fully closed (C-02 and C-03 have partner context recorded but remain open pending customer input)
- **Open (needs customer input):** 9
- **Blockers:** 1 (C-02)
- **Recommendation:** **Resolve red flags first.** Enough is captured to brief the customer, but C-02 (phased scope vs deadline) and C-04 (residency vs flagship models) should be worked in a customer session before the Pattern Selector commits to a pattern. C-01 (scope) and C-03/C-07 (peak/cost) should be closed in the same session because they cascade into pattern and cost.

## Next workshop (pre-sales)

List who should attend to close the red flags and open items:

- **Customer security/identity owner:** needed for C-06 (federation scale)
- **Customer application owner:** needed for C-01 (scope), C-08 (app ownership)
- **Customer data owner / DPO:** needed for C-05 (right-to-be-forgotten), C-04 (residency tradeoff)
- **Customer operations/SRE:** needed for C-03 (peak load), C-09 (SLA/resilience), C-07 (budget owner also required)

