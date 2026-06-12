---
artifact: requirements
engagement: "Sofia-Center"
customer: "Sofia Center"
captured_by: "[partner-name]"
captured_on: "2026-06-12"
status: draft
---

# Requirements — Sofia Center

## 0. Audience (partner side)

This document is intended for partner pre-sales delivery and should be usable by:

- **Solution architect / pre-sales architect**
- **App developer / lead engineer**
- **Infra/platform engineer**
- **Security/compliance lead**

> **Source note:** Items below marked _(from evidence pack)_ are derived from `evidence-pack.md`, which states it contains illustrative/generalized requirements with rounded figures. Treat all such values as **draft, pending customer confirmation**. Items with no source are `[TBD — ask customer]`.

## 1. Business context
- **Industry:** Public education & research sector _(from evidence pack)_
- **Business outcome (one sentence):** Provide an enterprise-grade, EU/EEA-resident AI assistant platform to ~100,000 higher-education & research users (university students, academics, researchers) _(derived from evidence pack — confirm exact wording with customer)_
- **Success metrics (6-month):** [TBD — ask customer]
- **Sponsor / decision maker:** [TBD — ask customer]
- **Budget owner:** [TBD — ask customer]

## 2. Users and usage
- **Primary persona(s):** University students, academics / teaching staff, researchers _(from evidence pack)_
- **Concurrent users at peak:** ~5,000–7,000 concurrent _(ASSUMPTION — partner planning estimate: ~5–7% peak concurrency of ~100k registered users, typical for bursty education usage; confirm with customer)_
- **Geographic distribution:** EU _(customer-confirmed: EU data boundary)_
- **Channel:** Web-based end-user GUI / chat application + REST API _(from evidence pack — confirm whether mobile / Teams also in scope)_

## 3. AI capabilities needed
- **Pattern hypothesis:** RAG (embeddings + document Q&A) plus general chat/generation; multimodal and batch inference also referenced _(from evidence pack — confirm primary pattern with customer)_
- **Models customer asked for:** ≥1 production LLM mapped to three tiers — flagship / balanced / efficient — captured as a tiered requirement rather than specific SKUs _(from evidence pack)_
- **Tools/actions the AI needs:** Tool/function calling, batch processing, file upload & document processing, prompt/template management _(from evidence pack)_

## 4. Data
- **Sources:** Uploaded documents — PDF, DOCX, XLSX, PPTX, HTML (and ODF / CSV / TXT at app layer) _(from evidence pack)_; specific source systems, per-source volumes, and classification [TBD — ask customer]
- **Update frequency:** [TBD — ask customer]
- **Sovereignty / residency:** EU/EEA-only for all processing, storage, logging, and inference (including batch) _(from evidence pack — strong requirement; confirm exact boundary)_
- **Sensitivity:** Regulated — GDPR-scoped personal data of students/staff _(from evidence pack — confirm classification levels with customer)_
- **Retention and right-to-be-forgotten:** No-training commitment required; GDPR data-subject rights apply _(from evidence pack)_; specific retention periods [TBD — ask customer]

## 5. Non-functional requirements
- **Latency target:** First-token p95 < 1.5 s; full-response p50 ≤ 3 s, p95 ≤ 8 s (streaming) _(ASSUMPTION — partner planning estimate for interactive chat; confirm with customer)_
- **Availability SLA:** 99.5% target _(from evidence pack — confirm whether contractual SLA or internal target)_
- **Throughput at peak:** [TBD — ask customer] _(pack references TPM/RPM quota and PTU; sizing to be derived from confirmed peak concurrency)_
- **Cost ceiling (monthly):** [TBD — ask customer] _(no planning estimate possible without confirmed traffic/token assumptions; defer to Cost phase)_

## 6. Security, compliance, governance
- **Compliance scopes:** GDPR + EU Data Boundary _(from evidence pack — confirm any sector-specific scopes)_
- **Identity provider:** Microsoft Entra ID federating institutional SAML 2.0 / OpenID Connect / WS-Fed identity providers; federated SSO _(from evidence pack)_
- **Network constraints:** Private networking / private endpoints expected; public network access to be restricted _(from evidence pack — confirm exact topology)_
- **Existing CAF Platform Landing Zone:** No — no Platform Landing Zone in place yet _(customer-confirmed)_
- **Approved Azure regions:** An EU region (within EU data boundary) _(customer-confirmed boundary; specific region not yet selected)_

## 7. Delivery preferences
- **IaC tool:** [TBD — ask customer]
- **Source control:** [TBD — ask customer]
- **CI/CD platform:** [TBD — ask customer]
- **Existing AI assets to reuse:** [TBD — ask customer] _(pack notes the "Chat with your data" accelerator as a possible delivery option, not a confirmed customer asset)_
- **Target environments:** [TBD — ask customer]

## 8. Constraints and known unknowns
- **Hard deadlines:** Deployed within ~5 months of project start _(customer-confirmed)_
- **Existing vendor lock-ins:** [TBD — ask customer]
- **Explicit "do not want":** Global (non-EU/EEA) deployment types that process data outside the geography must be excluded _(derived from residency requirement in evidence pack)_
- **Open questions from partner:**
  - Sponsor / decision maker and budget owner?
  - Success metrics (6-month)?
  - Confirm the partner ASSUMPTIONS: peak concurrency (~5–7k) and latency targets.
  - Throughput/token sizing and monthly cost ceiling (drives Cost phase).
  - Per-user / per-segment usage limits and cost attribution needs?
  - Delivery preferences: IaC tool, source control, CI/CD, target environments?
  - Note: no Platform Landing Zone yet — the AI LZ would need a platform foundation or a lightweight alternative (defer to Pattern/Architecture phases).

---

## Intake summary (filled by Requirements agent at close)

- **Sections complete:** 6 / 8 _(Sections 1–6 substantially populated; 7 mostly open, 8 partially open)_
- **Sections [TBD]:** §1 (sponsor, budget owner, success metrics), §5 (throughput, cost ceiling), §7 (all delivery preferences), §8 (vendor lock-ins)
- **Biggest gap blocking architecture work:** No CAF Platform Landing Zone exists yet, and traffic/token sizing is unconfirmed — both affect pattern selection and cost. Several NFRs are partner assumptions pending customer confirmation.
- **Ready for Challenger:** Yes — enough is captured to stress-test; open items are flagged for the Challenger and Pattern Selector phases.
