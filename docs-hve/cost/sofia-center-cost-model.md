<!-- markdownlint-disable-file -->
<!-- markdown-table-prettify-ignore-start -->
# Sofia Center AI Assistant — Cost & Sizing Model

> Status: **draft planning estimate** · 2026-06-15
> Source: [PRD](../prds/sofia-center-ai-assistant.md) · [Reference Architecture](../architecture/sofia-center-reference-architecture.md) · ADRs [0002](../decisions/2026-06-15-eu-region-residency.md) · [0003](../decisions/2026-06-15-model-capacity-hybrid.md) · [0004](../decisions/2026-06-15-rag-vector-store.md)

> ⚠️ **All figures are indicative planning estimates.** They depend on unconfirmed inputs (Q-003 concurrency, Q-004 token sizing) and indicative public rates. **Validate every rate against the Azure Pricing Calculator** for the chosen EU region and SKUs before any commitment. This model is built to **update cleanly** once the customer confirms the assumptions below.

## 1. Sizing inputs (assumptions — confirm with customer)

| Input | Low | Expected | High | Source |
|-------|-----|----------|------|--------|
| Registered users | 100,000 | 100,000 | 100,000 | Confirmed |
| Peak concurrent users | 5,000 | 6,000 | 7,000 | ASSUMPTION (Q-003) |
| Daily active users (% of registered) | 15% (15k) | 25% (25k) | 35% (35k) | ASSUMPTION |
| Messages / active user / day | 8 | 12 | 18 | ASSUMPTION |
| Active days / month | 22 | 22 | 22 | ASSUMPTION (academic calendar) |
| Input tokens / message (incl. RAG context) | 2,500 | 3,000 | 4,000 | ASSUMPTION |
| Output tokens / message | 500 | 600 | 800 | ASSUMPTION |

## 2. Token-volume engine

`Monthly messages = DAU × messages/user/day × active days`
`Monthly input tokens = messages × input tokens/message`
`Monthly output tokens = messages × output tokens/message`

| Metric | Low | Expected | High |
|--------|-----|----------|------|
| Monthly messages | ~2.6M | ~6.6M | ~13.9M |
| Monthly input tokens | ~6.6B | ~19.8B | ~55.5B |
| Monthly output tokens | ~1.3B | ~4.0B | ~11.1B |

## 3. Model tier mix (ADR-0003)

Model Router defaults to the efficient tier and escalates by task. Flagship served by **PTU (reserved)**; balanced + efficient served **PAYG (token-metered)**.

| Tier | Share | Capacity model | Indicative rate (per 1M tokens, in/out) |
|------|-------|----------------|------------------------------------------|
| Efficient (mini-class) | 70% | PAYG | ~$0.15 / ~$0.60 |
| Balanced (4o-class) | 25% | PAYG | ~$2.50 / ~$10.00 |
| Flagship (premium) | 5% | **PTU reserved** | priced as provisioned capacity, not per-token |

> Rates above are **indicative** GPT-4o / 4o-mini-class public figures; EU-region and current SKU rates must be confirmed.

## 4. Inference cost — PAYG tiers (efficient + balanced)

Expected case (6.6M messages, 95% of traffic is PAYG):

| Tier | Messages | Input cost | Output cost | Subtotal |
|------|----------|-----------|------------|----------|
| Efficient (70%) | ~4.62M | ~$2,080 | ~$1,660 | **~$3,740** |
| Balanced (25%) | ~1.65M | ~$12,380 | ~$9,900 | **~$22,280** |
| **PAYG total (expected)** | | | | **~$26,000 / month** |

| PAYG inference | Low | Expected | High |
|----------------|-----|----------|------|
| Monthly estimate | ~$10,000 | ~$26,000 | ~$60,000 |

> **Biggest cost lever:** the balanced-tier share. Shifting 5–10% of balanced traffic to efficient (via better routing/caching) materially reduces this line.

## 5. Inference cost — Flagship PTU (reserved)

Flagship uses provisioned throughput to guarantee latency at peak (NFR-001). PTU count is sized from confirmed peak token throughput — **blocked on Q-004**.

| Scenario | PTU (indicative) | Monthly (indicative) |
|----------|------------------|----------------------|
| Modest flagship demand | ~low double-digit PTU | ~$15,000 |
| Higher flagship demand | ~mid double-digit PTU | ~$40,000 |

> PTU monthly cost depends on reservation term (monthly vs annual discount). Confirm PTU throughput-per-unit and EU-region availability before sizing. Annual reservation can cut this 20–40%.

## 6. Supporting services (monthly, indicative)

| Component | Service | Low | Expected | High | Notes |
|-----------|---------|-----|----------|------|-------|
| Vector store | Azure AI Search (EU) | $2,000 | $4,000 | $6,000 | Replicas/partitions scale with concurrency (ADR-0004) |
| App tier | Container Apps / AKS | $2,000 | $3,500 | $5,000 | Scaled for 5–7k peak; stateless |
| Cache + state | Redis (Premium, EU) | $1,000 | $2,000 | $3,000 | Semantic cache + session state |
| Document storage | Blob (EU) | $200 | $500 | $1,000 | Source docs + lifecycle tiers |
| Edge | Front Door + WAF | $300 | $600 | $1,000 | Single public surface |
| API gateway | API Management (Premium, VNet) | $2,800 | $2,800 | $5,600 | Premium needed for VNet injection |
| Observability | Log Analytics + App Insights | $500 | $1,500 | $3,000 | EU-resident; ingestion-driven |
| Networking | Private Link + egress | $200 | $500 | $800 | Private endpoints, egress |
| Content safety | AI Content Safety | $200 | $600 | $1,500 | Per-transaction filtering |
| **Supporting subtotal** | | **~$9,200** | **~$16,000** | **~$26,900** | |

## 7. Total monthly estimate (rolled up)

| Cost block | Low | Expected | High |
|------------|-----|----------|------|
| PAYG inference (efficient + balanced) | ~$10,000 | ~$26,000 | ~$60,000 |
| Flagship PTU (reserved) | ~$15,000 | ~$25,000 | ~$40,000 |
| Supporting services | ~$9,200 | ~$16,000 | ~$26,900 |
| **Total (indicative)** | **~$34,000** | **~$67,000** | **~$127,000** |

> Expected ≈ **$67k/month** (~$800k/year). Wide spread reflects unconfirmed sizing — closing Q-003/Q-004 will collapse this range substantially.

## 8. Cost optimization levers (priority order)

| # | Lever | Mechanism | Est. impact |
|---|-------|-----------|-------------|
| 1 | **Tier routing discipline** | Default to efficient; escalate only when needed | Largest — cuts balanced share |
| 2 | **Semantic + embedding cache** | Avoid recompute of repeated/similar queries | 10–30% inference reduction |
| 3 | **PTU reservation term** | Annual vs monthly commitment on flagship | 20–40% on PTU line |
| 4 | **Batch tier for offline work** | Route latency-insensitive jobs to batch (FR-007) | Lower $/token for batch |
| 5 | **Prompt/context trimming** | Cap RAG context tokens; rerank to fewer chunks | Reduces input tokens (largest token line) |
| 6 | **AI Search right-sizing** | Tune replicas/partitions to measured load | Avoids over-provisioning |
| 7 | **Log ingestion controls** | Sampling + retention tiers | Caps observability cost |

## 9. Open items blocking a firm number

| Item | Blocks | Owner |
|------|--------|-------|
| Q-003 — confirm peak concurrency (5–7k) | App tier, AI Search, PTU sizing | Customer |
| Q-004 — confirm token-per-request & daily volume | Entire inference model | Customer |
| Monthly cost ceiling (PRD §5) | Go/no-go vs budget | Budget owner |
| EU region + SKU rates | All indicative rates → actuals | Architect + Customer |
| PTU throughput-per-unit (EU) | Flagship PTU count | Architect (validate in Azure) |
| Tier mix validation | PAYG split (70/25/5) | Pilot telemetry |

## 10. Recommended next steps

1. **Confirm Q-003 / Q-004** with the customer — single biggest driver of accuracy.
2. **Validate indicative rates** in the Azure Pricing Calculator for the chosen EU region.
3. **Confirm PTU throughput-per-unit** and EU availability for the flagship model.
4. **Run a small pilot** to measure real tier mix, tokens/request, and cache hit-rate, then re-run this model.
5. **Set the monthly cost ceiling** (PRD §5) and check it against the Expected/High totals.

Generated 2026-06-15 — Cost & Sizing phase (planning estimate; not a quote).
<!-- markdown-table-prettify-ignore-end -->
