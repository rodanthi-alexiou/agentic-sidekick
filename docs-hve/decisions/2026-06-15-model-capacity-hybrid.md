# ADR-0003 — Hybrid model capacity: PTU for flagship tier, PAYG for efficient tier

## Status

Proposed

## Context

The platform exposes three model tiers (flagship / balanced / efficient) and must serve an estimated ~5,000–7,000 peak concurrent users with interactive latency targets (first-token p95 < 1.5 s). Throughput/token sizing is **not yet confirmed** (open question Q-004), which directly drives the capacity model and cost ceiling. Provisioned Throughput Units (PTU) give predictable latency at peak but carry fixed cost; pay-as-you-go (PAYG) is elastic but risks throttling at high concurrency.

Source: [01-requirements.md](../../01-requirements.md) §3, §5; [PRD](../prds/sofia-center-ai-assistant.md) NFR-001, NFR-004, NFR-005, R-002.

## Decision Drivers

- Interactive latency SLA at peak concurrency.
- Cost predictability and avoidance of over-provisioning.
- Unconfirmed throughput sizing (must remain flexible).
- Tiered models already align cost to task complexity.

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| All PTU (provisioned) | Predictable latency across all tiers | High fixed cost; needs accurate sizing |
| All PAYG | Elastic, no commitment | Throttling risk at 5–7k peak; latency variance |
| **Hybrid: PTU for flagship, PAYG for efficient/balanced** | Latency SLA where it matters; cost-efficient elsewhere | More complex routing/ops |

## Decision

Adopt a **hybrid capacity model**: provisioned (PTU) capacity for the **flagship tier** to guarantee latency at peak, and **PAYG** for the efficient (and initially balanced) tiers with route-down/circuit-breaker on throttling. **Final PTU sizing is deferred to the Cost phase** pending confirmed concurrency and token-per-request figures.

## Consequences

### Positive

- Meets interactive latency SLA for premium workloads while controlling cost.
- Tier routing enables graceful degradation under load.

### Negative / Trade-offs

- Operational complexity of mixed capacity models and routing logic.
- Decision is provisional until sizing inputs (Q-004) are confirmed.

### Follow-ups

- Close Q-003 (concurrency) and Q-004 (throughput/token sizing).
- Run capacity load test to validate PTU units for flagship tier.
- Define route-down policy and circuit-breaker thresholds.

## References

- [Requirements](../../01-requirements.md)
- [PRD](../prds/sofia-center-ai-assistant.md)
- ADR-0001 (landing zone), ADR-0002 (EU region)
