<!-- markdownlint-disable-file -->
<!-- markdown-table-prettify-ignore-start -->
# Sofia Center AI Assistant Platform - Product Requirements Document (PRD)
Version 0.1 | Status draft | Owner [TBD] | Team [TBD — partner pre-sales] | Target ~5 months from project start | Lifecycle Discovery

## Progress Tracker
| Phase | Done | Gaps | Updated |
|-------|------|------|---------|
| Context | Partial | Sponsor, budget owner, success metrics | 2026-06-15 |
| Problem & Users | Partial | Confirm channels (mobile/Teams), concurrency assumption | 2026-06-15 |
| Scope | Partial | Confirm in/out of scope with customer | 2026-06-15 |
| Requirements | Partial | Throughput, cost ceiling, retention periods | 2026-06-15 |
| Metrics & Risks | Partial | 6-month success metrics, risk owners | 2026-06-15 |
| Operationalization | Open | IaC, CI/CD, environments, platform foundation | 2026-06-15 |
| Finalization | Open | Pending Challenger + Architecture + Cost phases | 2026-06-15 |
Unresolved Critical Questions: 7 | TBDs: 12

## 1. Executive Summary
### Context
Sofia Center operates in the public education & research sector and needs an enterprise-grade, EU/EEA-resident AI assistant platform serving approximately 100,000 higher-education and research users (university students, academics/teaching staff, researchers). Source requirements are captured in [01-requirements.md](../../01-requirements.md); several figures are partner planning estimates pending customer confirmation.

### Core Opportunity
Provide a sovereign (EU data boundary) AI assistant that combines retrieval-augmented document Q&A with general chat/generation, delivered via web GUI and REST API, with a no-training data commitment and full GDPR compliance.

### Goals
| Goal ID | Statement | Type | Baseline | Target | Timeframe | Priority |
|---------|-----------|------|----------|--------|-----------|----------|
| G-001 | Deliver an EU/EEA-resident AI assistant to ~100k registered users | Outcome | No platform today | Production launch | ~5 months | High |
| G-002 | Ensure all processing, storage, logging, and inference remain within the EU data boundary | Compliance | N/A | 100% EU-resident | Launch | High |
| G-003 | Support RAG document Q&A across uploaded documents (PDF, DOCX, XLSX, PPTX, HTML) | Capability | N/A | RAG GA | Launch | High |
| G-004 | Offer tiered model access (flagship / balanced / efficient) | Capability | N/A | ≥1 production LLM per tier | Launch | Medium |
| G-005 | [TBD — define a measurable 6-month adoption/value metric with customer] | Outcome | [TBD] | [TBD] | 6 months | High |

### Objectives (Optional)
| Objective | Key Result | Priority | Owner |
|-----------|------------|----------|-------|
| Sovereign AI adoption | [TBD — e.g., % of target users active monthly] | High | [TBD] |

## 2. Problem Definition
### Current Situation
No EU-resident enterprise AI assistant exists for the institution today. Users lack a compliant, centrally governed way to use LLM-based chat and document Q&A on institutional materials.

### Problem Statement
Higher-education users need a GDPR-compliant, EU data-boundary AI assistant for chat, generation, and document Q&A, without their data being used for model training and without processing leaving the EU/EEA.

### Root Causes
* No existing platform or CAF Platform Landing Zone foundation in place.
* Strict data residency and GDPR constraints rule out general (non-EU) AI deployment types.

### Impact of Inaction
* Users adopt non-compliant shadow-IT AI tools, creating GDPR and data-sovereignty risk.
* Institution misses productivity and research-acceleration benefits of a governed AI platform.

## 3. Users & Personas
| Persona | Goals | Pain Points | Impact |
|---------|-------|------------|--------|
| University student | Study help, summarization, document Q&A | No compliant AI tool; uneven access | High volume of usage |
| Academic / teaching staff | Content generation, research support, document analysis | Data residency concerns; no governed tooling | Medium-high |
| Researcher | Literature Q&A, analysis over uploaded docs | Sensitivity of research data; sovereignty | Medium |

### Journeys (Optional)
[TBD — to be detailed during UX phase: upload document → ask questions → cited answers; general chat session.]

## 4. Scope
### In Scope
* Web-based end-user chat GUI.
* REST API for programmatic access.
* RAG over uploaded documents (PDF, DOCX, XLSX, PPTX, HTML; ODF/CSV/TXT at app layer).
* Tiered LLM access (flagship / balanced / efficient).
* Tool/function calling, batch processing, file upload & document processing, prompt/template management.
* Microsoft Entra ID with federated institutional SSO (SAML 2.0 / OIDC / WS-Fed).

### Out of Scope (justify if empty)
* Global (non-EU/EEA) deployment types that process data outside the geography — excluded by residency requirement.
* [TBD — confirm: mobile app, Microsoft Teams channel — currently unconfirmed.]

### Assumptions
* Peak concurrency ~5,000–7,000 (partner estimate ~5–7% of 100k) — pending confirmation.
* Interactive latency targets are partner planning estimates — pending confirmation.

### Constraints
* EU/EEA data residency for all processing, storage, logging, and inference (including batch).
* No CAF Platform Landing Zone exists yet — requires platform foundation or lightweight alternative.
* Hard deadline: deployed within ~5 months of project start.

## 5. Product Overview
### Value Proposition
A sovereign, GDPR-compliant AI assistant that gives 100k education users governed access to chat, generation, and document Q&A — with data guaranteed to stay in the EU and never used for training.

### Differentiators (Optional)
* EU data-boundary guarantee end-to-end (including batch inference).
* No-training data commitment.
* Federated institutional SSO across existing identity providers.

### UX / UI (Conditional)
Web chat GUI with file upload and streaming responses. UX Status: [TBD — detail in UX phase]

## 6. Functional Requirements
| FR ID | Title | Description | Goals | Personas | Priority | Acceptance | Notes |
|-------|-------|------------|-------|----------|----------|-----------|-------|
| FR-001 | Chat interface | Web-based chat GUI with streaming responses | G-001 | All | High | User can hold a multi-turn streamed conversation | |
| FR-002 | REST API | Programmatic access to chat/generation endpoints | G-001 | Researcher | High | API authenticates and returns completions | |
| FR-003 | Document upload & processing | Upload and process PDF, DOCX, XLSX, PPTX, HTML (ODF/CSV/TXT at app layer) | G-003 | All | High | Supported file types parse and become queryable | |
| FR-004 | RAG document Q&A | Embeddings + retrieval to answer questions over uploaded docs with citations | G-003 | All | High | Answers cite source passages | |
| FR-005 | Tiered model selection | Expose flagship / balanced / efficient model tiers | G-004 | All | Medium | User/admin can route to a tier | |
| FR-006 | Tool / function calling | Support function/tool calling for actions | G-001 | Researcher | Medium | Model invokes registered tools | |
| FR-007 | Batch processing | Batch/offline inference within EU boundary | G-002 | Academic | Medium | Batch jobs run EU-resident | |
| FR-008 | Prompt/template management | Manage reusable prompts/templates | G-001 | Academic | Low | Users save & reuse templates | |
| FR-009 | Federated SSO | Entra ID federating SAML 2.0 / OIDC / WS-Fed | G-001 | All | High | Institutional users sign in via SSO | |

### Feature Hierarchy (Optional)
```plain
Sofia Center AI Assistant
├── Conversational AI (chat GUI, REST API, streaming)
├── Knowledge / RAG (upload, parse, embed, retrieve, cite)
├── Model tiers (flagship / balanced / efficient)
├── Extensibility (tool calling, batch, templates)
└── Identity & access (Entra ID federated SSO)
```

## 7. Non-Functional Requirements
| NFR ID | Category | Requirement | Metric/Target | Priority | Validation | Notes |
|--------|----------|------------|--------------|----------|-----------|-------|
| NFR-001 | Performance | Interactive first-token latency | p95 < 1.5 s | High | Load test | ASSUMPTION — confirm |
| NFR-002 | Performance | Full-response latency (streaming) | p50 ≤ 3 s, p95 ≤ 8 s | High | Load test | ASSUMPTION — confirm |
| NFR-003 | Reliability | Availability | 99.5% target | High | Monitoring | Confirm SLA vs internal target |
| NFR-004 | Scalability | Concurrent users at peak | ~5,000–7,000 | High | Load test | ASSUMPTION — confirm |
| NFR-005 | Scalability | Throughput at peak | [TBD — TPM/RPM/PTU sizing] | High | Capacity test | Derive after concurrency confirmed |
| NFR-006 | Residency | EU/EEA-only processing, storage, logging, inference | 100% EU boundary | High | Architecture review | Includes batch |
| NFR-007 | Security | Private networking / private endpoints; restrict public access | No public data-plane exposure | High | Network review | Confirm topology |
| NFR-008 | Privacy | No-training commitment on customer data | Contractual / config enforced | High | Config audit | |
| NFR-009 | Compliance | GDPR + EU Data Boundary | Compliant | High | Compliance review | |
| NFR-010 | Identity | Federated SSO via Entra ID | SAML/OIDC/WS-Fed | High | Auth test | |

## 8. Data & Analytics (Conditional)
### Inputs
Uploaded documents: PDF, DOCX, XLSX, PPTX, HTML (and ODF / CSV / TXT at app layer). Specific source systems, per-source volumes, and classification levels [TBD — ask customer].

### Outputs / Events
Chat completions, cited RAG answers, batch inference results. [TBD — define telemetry events.]

### Instrumentation Plan
| Event | Trigger | Payload | Purpose | Owner |
|-------|---------|--------|---------|-------|
| [TBD] | [TBD] | [TBD] | Usage & cost attribution | [TBD] |

### Metrics & Success Criteria
| Metric | Type | Baseline | Target | Window | Source |
|--------|------|----------|--------|--------|--------|
| [TBD — adoption] | Outcome | [TBD] | [TBD] | 6 months | [TBD] |

## 9. Dependencies
| Dependency | Type | Criticality | Owner | Risk | Mitigation |
|-----------|------|------------|-------|------|-----------|
| Platform foundation (no CAF Platform LZ today) | Infra | High | [TBD] | Blocks AI landing zone | Stand up platform foundation or lightweight alternative |
| EU region selection (within EU boundary) | Infra | High | [TBD] | Affects residency & capacity | Select region during Architecture phase |
| Institutional identity providers (SAML/OIDC/WS-Fed) | Identity | High | [TBD] | SSO federation complexity | Validate federation early |

## 10. Risks & Mitigations
| Risk ID | Description | Severity | Likelihood | Mitigation | Owner | Status |
|---------|-------------|---------|-----------|-----------|-------|--------|
| R-001 | No Platform Landing Zone may delay deployment | High | Medium | Lightweight platform foundation | [TBD] | Open |
| R-002 | Unconfirmed traffic/token sizing risks cost & capacity mis-estimate | High | High | Confirm concurrency, run sizing | [TBD] | Open |
| R-003 | Partner NFR assumptions (latency, concurrency) may not match reality | Medium | Medium | Validate with customer | [TBD] | Open |
| R-004 | ~5-month deadline is aggressive given missing foundation | High | Medium | Phase delivery, MVP scope | [TBD] | Open |

## 11. Privacy, Security & Compliance
### Data Classification
Regulated — GDPR-scoped personal data of students/staff. Specific classification levels [TBD — ask customer].

### PII Handling
GDPR data-subject rights apply (incl. right-to-be-forgotten). No-training commitment required. Retention periods [TBD].

### Threat Considerations
Private networking, restricted public access, EU-resident logging. [TBD — full threat model in Architecture phase.]

### Regulatory / Compliance (Conditional)
| Regulation | Applicability | Action | Owner | Status |
|-----------|--------------|--------|-------|--------|
| GDPR | In scope | Data-subject rights, DPIA | [TBD] | Open |
| EU Data Boundary | In scope | EU-resident services only | [TBD] | Open |

## 12. Operational Considerations
| Aspect | Requirement | Notes |
|--------|------------|-------|
| Deployment | [TBD — IaC tool] | Customer delivery preferences open |
| Rollback | [TBD] | |
| Monitoring | EU-resident monitoring | Confirm tooling |
| Alerting | [TBD] | |
| Support | [TBD] | |
| Capacity Planning | Derive from confirmed concurrency/throughput | Drives Cost phase |

## 13. Rollout & Launch Plan
### Phases / Milestones
| Phase | Date | Gate Criteria | Owner |
|-------|------|--------------|-------|
| Requirements (done) | 2026-06 | Intake captured | Partner |
| Challenger / gap closure | [TBD] | Assumptions confirmed | [TBD] |
| Architecture + ADRs | [TBD] | Pattern & region selected | [TBD] |
| Cost & sizing | [TBD] | TPM/PTU & ceiling agreed | [TBD] |
| Build / MVP | [TBD] | Core FRs delivered | [TBD] |
| Launch | ~5 months from start | All gates pass | [TBD] |

### Feature Flags (Conditional)
| Flag | Purpose | Default | Sunset Criteria |
|------|---------|--------|----------------|
| [TBD] | | | |

### Communication Plan (Optional)
[TBD]

## 14. Open Questions
| Q ID | Question | Owner | Deadline | Status |
|------|----------|-------|---------|--------|
| Q-001 | Who is the sponsor / decision maker and budget owner? | Partner→Customer | [TBD] | Open |
| Q-002 | What are the measurable 6-month success metrics? | Partner→Customer | [TBD] | Open |
| Q-003 | Confirm peak concurrency (~5–7k) and latency targets | Partner→Customer | [TBD] | Open |
| Q-004 | Throughput/token sizing and monthly cost ceiling | Partner→Customer | [TBD] | Open |
| Q-005 | Per-user / per-segment usage limits & cost attribution needs? | Partner→Customer | [TBD] | Open |
| Q-006 | Delivery preferences: IaC, source control, CI/CD, environments? | Partner→Customer | [TBD] | Open |
| Q-007 | Channels beyond web/API (mobile, Teams)? | Partner→Customer | [TBD] | Open |
| Q-008 | Existing vendor lock-ins? | Partner→Customer | [TBD] | Open |
| Q-009 | Specific retention periods & data classification levels? | Partner→Customer | [TBD] | Open |

## 15. Changelog
| Version | Date | Author | Summary | Type |
|---------|------|-------|---------|------|
| 0.1 | 2026-06-15 | PRD Builder | Initial PRD generated from requirements intake | Created |

## 16. References & Provenance
| Ref ID | Type | Source | Summary | Conflict Resolution |
|--------|------|--------|---------|--------------------|
| REF-001 | Document | [01-requirements.md](../../01-requirements.md) | Sofia Center requirements intake | Source of truth for this PRD |
| REF-002 | Document | evidence-pack.md (referenced by REF-001) | Illustrative/generalized requirements with rounded figures | Treated as draft pending customer confirmation |

### Citation Usage
All confirmed facts derive from REF-001. Items marked ASSUMPTION are partner planning estimates; items marked [TBD] require customer input.

## 17. Appendices (Optional)
### Glossary
| Term | Definition |
|------|-----------|
| RAG | Retrieval-Augmented Generation — grounding LLM answers in retrieved documents |
| PTU | Provisioned Throughput Unit — reserved model capacity |
| TPM/RPM | Tokens/Requests per minute — throughput quota units |
| CAF | Cloud Adoption Framework |
| LZ | Landing Zone |

### Additional Notes
This PRD is an early draft generated from a pre-sales requirements intake. Open questions (§14) should be closed during the Challenger and Architecture/Cost phases before finalization.

Generated 2026-06-15T00:00:00Z by PRD Builder (mode: full)
<!-- markdown-table-prettify-ignore-end -->
