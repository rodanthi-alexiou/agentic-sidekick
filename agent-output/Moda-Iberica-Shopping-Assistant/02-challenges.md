---
artifact: challenges
engagement: "Moda-Iberica-Shopping-Assistant"
based_on: 01-requirements.md
generated_by: challenger
generated_on: "2026-05-27"
status: draft
---

# Challenges — Moda Ibérica

Socratic stress-test of `01-requirements.md`. Each challenge raises a question the partner team should answer (with the customer) before architecture work begins.

## How to read this document

- **C-XX**: a single challenge. Open-ended question, not a verdict.
- **Red flags**: challenges that, if their assumption is true as currently stated, make the engagement risky.
- Resolve the red flags first. Park the rest for the architecture conversation.

---

## Challenges

### C-01: Define the MVP for Oct 2026

**Challenges requirement:** **Hard deadlines:** "Production by Oct 2026 to support Black Friday / Christmas 2026 peak; pilot live before peak season"

**Question:** What is the minimum *must-have* scope for the October 2026 production release versus what can wait until after peak season?

**Why it matters:** Without a hard MVP boundary, the program risks either missing the peak-season deadline or shipping something that cannot be safely operated.

**Evidence that would resolve this:** A prioritized backlog (MoSCoW), with explicit MVP acceptance criteria for web/mobile and for store associates.

---

### C-02: Clarify how success metrics will be measured

**Challenges requirement:** **Success metrics (6-month):** "15% lift in online conversion for sessions that engage the assistant"; "25% deflection of 'where is my order' and 'return policy' contacts"; "Store associates rate it ≥4/5"

**Question:** How will Moda Ibérica attribute uplift/deflection to the assistant (experiment design, segmentation, and definitions like what counts as an "engaged" session)?

**Why it matters:** If measurement is ambiguous, the assistant can be judged as a failure even if it’s creating value—or conversely over-credited.

**Evidence that would resolve this:** An analytics plan: baseline definitions, A/B or holdout plan, instrumentation events, and the precise survey method for associates.

---

### C-03: Budget realism vs. peak-season model consumption

**Challenges requirement:** **Year-one budget (build + run):** "€600K (board approved)" and **Cost ceiling (monthly):** "[TBD — ask customer]" (note: year-one budget stated as €600K)

**Question:** What is the "run" cost envelope Moda Ibérica will accept in peak months (Black Friday) versus normal months, and what cost overrun guardrails are required?

**Why it matters:** AI assistants can be cost-elastic with usage spikes; without guardrails, the peak event can blow the year-one budget.

**Evidence that would resolve this:** A monthly cost cap and an operating policy (rate limiting, model fallback, token budgets per session, and feature kill-switches).

---

### C-04: Peak concurrency assumptions and traffic shape

**Challenges requirement:** **Concurrent users at peak:** "~2,000 (Black Friday estimate); typical 200–300"

**Question:** Is "2,000" peak concurrency based on observed site analytics, or a guess—and what is the expected traffic shape (duration, bursts, average turns per chat)?

**Why it matters:** Capacity planning and resiliency design are dominated by peak-shape, not average traffic.

**Evidence that would resolve this:** Historical Black Friday web/app traffic metrics, plus an assumed chat interaction profile (turns/session, average prompt+response size).

---

### C-05: Store-associate workflow clarity

**Challenges requirement:** **Primary persona(s):** "Store associates (tablets) supporting in-store customers" and **Channel:** "Web + mobile app + in-store tablets"

**Question:** What are the top 3 associate workflows (e.g., "find a similar item in stock", "locate in nearby store", "policy answer") and what is the tolerance for errors in each?

**Why it matters:** Associate-facing UX has different failure modes (customer trust, staff time). The assistant may need a "show sources / show stock proof" experience.

**Evidence that would resolve this:** A short workflow inventory with success criteria and a "what the assistant is allowed to do" policy for associates.

---

### C-06: Multilingual expectations beyond translation

**Challenges requirement:** **Languages:** "Spanish, Catalan, Portuguese"

**Question:** Do they need *native* tone and brand voice per language (including regional variants), and who approves/maintains the localization over time?

**Why it matters:** Multilingual assistants often fail on tone, product terminology, and customer support phrasing—especially for returns and promotions.

**Evidence that would resolve this:** Language QA criteria, glossary/terminology list, and an owner for ongoing language review.

---

### C-07: Define "outfit recommendations" inputs and evaluation

**Challenges requirement:** **Core capabilities (as stated):** "Outfit recommendations"

**Question:** What data should the assistant use for outfit recommendations (catalog attributes, trend rules, style guide rules, user preferences, images), and how will Moda Ibérica evaluate that recommendations are "good"?

**Why it matters:** "Recommendations" can mean rules-based merchandising, collaborative filtering, or generative suggestions—each needs different data and guardrails.

**Evidence that would resolve this:** A recommendation spec: allowed inputs, constraints (e.g., modesty, seasonal), and an offline evaluation set curated by merchandising.

---

### C-08: WISMO ("where is my order") authentication and privacy

**Challenges requirement:** **Core capabilities (as stated):** "'Where is my order' support (order status)" and **Sources:** "Order history + customer profile ... includes customer PII"

**Question:** For order status, how will the assistant authenticate the requester (logged-in only? guest orders?) and prevent data leakage (e.g., returning order details to the wrong person)?

**Why it matters:** WISMO is high volume and high privacy risk. Strong authN/authZ is mandatory; otherwise the assistant becomes a PII breach vector.

**Evidence that would resolve this:** An authentication flow and authorization model, plus explicit redaction rules and audit requirements.

---

### C-09: Model constraint "GPT-5" vs. availability, approvals, and fallbacks

**Challenges requirement:** **Models customer asked for:** "GPT-5" and **Procurement / licensing:** "Not yet engaged on model licensing"

**Question:** If "GPT-5" is not available in the required EU region(s), not approved by procurement, or not cost-effective at peak, what is the acceptable fallback model strategy?

**Why it matters:** Tying the program to a single named model creates schedule and procurement risk, and can block the October deadline.

**Evidence that would resolve this:** A model selection policy (capabilities required, fallback ladder, procurement plan, and a decision date).

---

### C-10: Product description generation governance

**Challenges requirement:** **Additional capability request:** "Generate product descriptions for new SKUs"

**Question:** Are generated descriptions allowed to be customer-facing without human review, and what is the policy for factual claims (materials, care instructions, sustainability claims)?

**Why it matters:** Copy errors can create legal exposure, customer dissatisfaction, and brand damage; this may need a human-in-the-loop workflow and strict source-of-truth constraints.

**Evidence that would resolve this:** An editorial workflow, approval SLA, and a schema of fields that must be sourced from authoritative product data.

---

### C-11: Data classification and what can be sent to the model

**Challenges requirement:** **Sovereignty / residency:** "Customer PII cannot leave the EU" and **Sensitivity:** "Includes PII (GDPR); overall classification scheme [TBD — ask customer]"

**Question:** What is Moda Ibérica’s data classification policy per source, and what is explicitly allowed to be included in prompts, retrieval context, logs, and traces?

**Why it matters:** "EU-only" is necessary but not sufficient—teams often unintentionally leak PII via prompts, tool outputs, or observability data.

**Evidence that would resolve this:** A written policy mapping each data field/classification to allowed destinations (model input, vector index, logs) and required redaction.

---

### C-12: Right-to-be-forgotten and deletion propagation

**Challenges requirement:** **Retention and right-to-be-forgotten:** "[TBD — ask customer]"

**Question:** How will GDPR deletion requests propagate across conversation transcripts, analytics, retrieval indexes, caches, and backups?

**Why it matters:** Deletion is hard in distributed systems; without an end-to-end plan, compliance becomes a manual fire drill.

**Evidence that would resolve this:** A retention/deletion design with deletion SLAs, data lineage, and verification/audit evidence.

---

### C-13: Freshness requirements for catalog, promotions, and stock

**Challenges requirement:** **Update frequency:** "Catalog: nightly"; "Inventory: real-time"; "Style guide: quarterly"

**Question:** What user experience is acceptable when data is stale (e.g., a promo ends, stock changes), and should the assistant prefer live APIs over indexed content for certain questions?

**Why it matters:** Retail customers are sensitive to availability and promos; stale answers directly harm conversion and trust.

**Evidence that would resolve this:** A freshness policy by intent (promotion Q&A vs catalog discovery vs inventory), including caching rules.

---

### C-14: Latency targets by intent (not just "chat latency")

**Challenges requirement:** **Latency target:** "[TBD — ask customer: p50/p95 for chat responses and for transactional lookups]"

**Question:** What are the p50/p95 targets separately for (a) simple Q&A, (b) catalog browsing, and (c) real-time tool calls like inventory and order status?

**Why it matters:** Tool calls dominate p95; without intent-level latency targets, you can over-engineer the wrong path or under-deliver where it matters.

**Evidence that would resolve this:** An intent catalog with p50/p95 targets and degradation behavior ("partial answer", "handoff").

---

### C-15: Availability, incident response, and peak-event readiness

**Challenges requirement:** **Availability SLA:** "[TBD — ask customer]" and **Compliance scopes:** "GDPR; Spanish LOPDGDD; DORA readiness work in progress"

**Question:** What uptime/availability is required during peak events, and what is the incident response expectation (on-call coverage, runbooks, rollback plan)?

**Why it matters:** Peak events are when the assistant matters most; operational readiness is usually the hidden risk, especially under DORA-related scrutiny.

**Evidence that would resolve this:** SLA/SLO targets, DR expectations, runbooks, and a peak-readiness exercise plan.

---

### C-16: Identity split between customers and store associates

**Challenges requirement:** **Identity provider:** "[TBD — ask customer] (separate needs likely for customers vs store associates)"

**Question:** What identity systems will authenticate (a) customers and (b) associates, and what authorization scopes are needed (e.g., associates can see store stock; customers can only see their own orders)?

**Why it matters:** Mixing identity domains without a clear authZ model is a common cause of data leakage.

**Evidence that would resolve this:** Identity architecture decisions and a role/permissions matrix for each tool action.

---

### C-17: Network constraints vs. third-party SaaS integrations

**Challenges requirement:** **Network constraints:** "[TBD — ask customer]" and **Existing vendor lock-ins:** "SAP Commerce Cloud; Salesforce Service Cloud; OMS (REST API); SharePoint"

**Question:** Does the CISO require private networking only—and if so, how will the assistant reach SaaS systems (Salesforce, SAP Commerce Cloud, SharePoint) reliably?

**Why it matters:** A strict private-only stance can become the critical path if core dependencies are SaaS with limited private connectivity options.

**Evidence that would resolve this:** A network policy statement and an integration connectivity plan per dependency (including egress controls).

---

### C-18: EU-only requirement precision (EU boundary vs. specific country)

**Challenges requirement:** **Sovereignty / residency:** "Customer PII cannot leave the EU" and **Approved Azure regions:** "[TBD — ask customer]"

**Question:** Is the requirement "data must remain in the EU" or "data must remain in Spain" (or another single country), and how will they validate residency for transient data (logs, backups, support access)?

**Why it matters:** "EU" vs "single-country" leads to different region selection, DR approach, and service eligibility.

**Evidence that would resolve this:** A written data residency requirement and approved-region list from the CISO/security team.

---

### C-19: Delivery model and toolchain split (Azure DevOps vs GitHub)

**Challenges requirement:** **Source control:** "Mixed today: Azure DevOps (commerce platform) and GitHub (data team)" and **CI/CD platform:** "[TBD — ask customer]" and **IaC tool:** "[TBD — ask customer]"

**Question:** Who will own the end-to-end delivery pipeline, and is the organization willing to standardize on one repo/pipeline system for the assistant (or define strict integration boundaries)?

**Why it matters:** Toolchain ambiguity creates security gaps (secrets, approvals) and slows delivery—especially with a fixed October deadline.

**Evidence that would resolve this:** A delivery decision (repo + CI/CD + IaC), environment promotion model, and security controls (approvals, branch protections).

---

### C-20: Build vs buy (Copilot Studio question) with clear decision criteria

**Challenges requirement:** **Open questions from partner:** "Should we just buy Copilot Studio? Why would we build this?"

**Question:** What are the decision criteria for "buy" versus "build" (time-to-market, EU/PII constraints, tool integrations, omnichannel support, cost predictability, and ability to enforce guardrails)?

**Why it matters:** If the decision is not made early, the team can waste months prototyping the wrong platform.

**Evidence that would resolve this:** A short decision matrix and a time-boxed proof (e.g., 2–3 weeks) comparing the top options against requirements.

---

## Red flags

- [ ] **C-08**: WISMO requires strong authentication/authorization; otherwise high PII breach risk.
- [ ] **C-09**: Model choice and licensing/procurement not started; risk to Oct 2026 deadline.
- [ ] **C-11 / C-18**: EU-only constraint is underspecified (EU vs country) and needs enforceable prompt/logging rules.
- [ ] **C-15**: DORA readiness + peak-season reliability without defined SLOs/on-call/runbooks.
- [ ] **C-17**: Network stance unknown; could block SaaS integrations (Salesforce/SAP/SharePoint).

---

## Recommendation

- **Total challenges raised:** 20
- **Red flags:** 5
- **Recommendation:** resolve red flags first
