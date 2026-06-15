# ADR-0002 — Single EU region with end-to-end data-boundary residency

## Status

Proposed

## Context

All processing, storage, logging, and inference — **including batch inference** — must remain within the EU/EEA data boundary. The specific EU region has not yet been selected. Every PaaS service in the architecture (LLM/embeddings, vector store, object storage, logging, monitoring) must offer EU residency and the required model SKUs.

Source: [01-requirements.md](../../01-requirements.md) §4, §6; [PRD](../prds/sofia-center-ai-assistant.md) NFR-006, NFR-009.

## Decision Drivers

- EU Data Boundary + GDPR are hard requirements.
- Batch inference is a common residency leak point.
- Required model tiers (flagship/balanced/efficient) must be available in-region.
- Latency benefits from regional proximity to EU users.

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **Single EU region, all services pinned** | Simplest residency assurance; lowest cross-region latency | Single-region availability ceiling |
| Multi-EU-region active/active | Higher availability | Complexity; must verify residency in each; cost |
| Global/non-EU deployment types | Capacity flexibility | **Excluded** — violates residency |

## Decision

Select **one EU region** (within the EU data boundary) where all required model SKUs and dependent PaaS services are available, and pin **every** service — including batch inference, logging, and monitoring — to that region. Validate model-tier availability before finalizing the region.

## Consequences

### Positive

- Clear, auditable residency story for GDPR/EU Data Boundary.
- Lower latency for EU users.

### Negative / Trade-offs

- Single-region availability ceiling vs the 99.5% target (acceptable, but confirm).
- Region choice constrained by model SKU availability.

### Follow-ups

- Verify flagship/balanced/efficient model availability in candidate EU region(s).
- Confirm batch-inference residency for chosen services.
- Re-evaluate multi-region if availability target rises above 99.5%.

## References

- [Requirements](../../01-requirements.md)
- [PRD](../prds/sofia-center-ai-assistant.md)
- ADR-0001 (landing zone), ADR-0003 (model capacity)
