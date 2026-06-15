# ADR-0001 — Lightweight application landing zone instead of full CAF Platform Landing Zone

## Status

Proposed

## Context

Sofia Center has **no CAF Platform Landing Zone** in place and a hard deadline of **~5 months** to production for an EU-resident AI assistant serving ~100k users. A full CAF Platform Landing Zone provides enterprise-grade governance but is unlikely to be stood up and matured within the timeline. The solution must still guarantee EU data-boundary residency, private networking, and policy-based governance.

Source: [01-requirements.md](../../01-requirements.md) §6, §8; [PRD](../prds/sofia-center-ai-assistant.md) §4, §9, R-001, R-004.

## Decision Drivers

- Hard ~5-month deadline to production.
- EU/EEA data-boundary residency must be enforced from day one.
- GDPR governance and private networking are non-negotiable.
- No existing platform foundation to build on.
- Desire to avoid expensive rework later.

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| Full CAF Platform Landing Zone | Enterprise-grade, future-proof, complete separation of platform/workload | Too slow to mature within 5 months; high upfront effort |
| **Lightweight application landing zone** (single platform-light subscription, hub VNet, Private Link, Azure Policy guardrails, EU region pin) | Fast to deploy, meets residency/compliance, governs the workload | Some later refactor to align with full CAF |
| No landing zone / direct deploy | Fastest | Fails governance and residency assurance; unacceptable risk |

## Decision

Adopt a **lightweight application landing zone**: a single platform-light subscription pinned to one EU region, with a hub VNet, Private Link/private endpoints for all data-plane services, Azure Policy guardrails enforcing EU residency and deny-public-access, and managed identities. Design it to be **forward-compatible** with a future full CAF Platform Landing Zone.

## Consequences

### Positive

- Meets the deadline while preserving residency and governance guarantees.
- Provides a clean migration path to full CAF later.

### Negative / Trade-offs

- Some governance capabilities (centralized connectivity, full management group hierarchy) deferred.
- Later refactor effort to align with enterprise CAF.

### Follow-ups

- Confirm target EU region (ADR-0002 dependency).
- Define Azure Policy set enforcing EU residency and private networking.
- Revisit CAF alignment post-launch.

## References

- [Requirements](../../01-requirements.md)
- [PRD](../prds/sofia-center-ai-assistant.md)
- ADR-0002 (EU region & residency), ADR-0003 (model capacity)
