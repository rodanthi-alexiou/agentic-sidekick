# ADR-0004 — Azure AI Search (EU region) as the RAG vector store

## Status

Proposed

## Context

The platform requires retrieval-augmented generation (RAG) over uploaded documents (PDF, DOCX, XLSX, PPTX, HTML; ODF/CSV/TXT at the app layer) for ~100k users, returning cited answers. A vector/retrieval store is needed to embed and retrieve document passages. The choice must satisfy the EU data-boundary residency requirement, integrate quickly to meet the ~5-month deadline, and keep retrieval latency low enough to fit within the interactive latency budget (retrieval ≤ ~300 ms so first-token p95 < 1.5 s remains achievable).

Source: [01-requirements.md](../../01-requirements.md) §3, §4; [PRD](../prds/sofia-center-ai-assistant.md) FR-003, FR-004, NFR-001, NFR-006; Architecture Review Trade-off B.

## Decision Drivers

- EU/EEA data-boundary residency for the vector store and its data.
- Time-to-market within the ~5-month deadline (favor managed, integrated services).
- Retrieval latency must fit the interactive first-token budget.
- Hybrid (keyword + vector) search quality for document Q&A with citations.
- Operational simplicity given no existing platform foundation.

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **Azure AI Search (EU region)** | Managed; native hybrid (keyword + vector) search; integrated ingestion/skillsets; EU-resident; fast to adopt; supports citations | Higher cost at large scale; service-level capacity tuning |
| PostgreSQL + pgvector | Lower cost; SQL-native; full control | More operational burden; manual hybrid search; tuning/scaling effort |
| Dedicated third-party vector DB | Potential performance at scale | Extra residency verification; added vendor/ops; integration time |

## Decision

Use **Azure AI Search in the selected EU region** as the RAG vector store, leveraging its hybrid search and integrated ingestion to meet the deadline while preserving EU residency. Pin the service and its indexed data to the same EU region established in ADR-0002. Revisit PostgreSQL + pgvector as a cost-optimization option post-launch if scale economics warrant.

## Consequences

### Positive

- Fastest path to a working, citation-capable RAG pipeline within the timeline.
- Managed service reduces operational load given no platform foundation.
- Hybrid search improves answer relevance over pure-vector retrieval.

### Negative / Trade-offs

- Higher per-unit cost than self-managed pgvector at large scale.
- Capacity/replica sizing must be validated against the ~5–7k peak concurrency.

### Follow-ups

- Confirm Azure AI Search availability and tier in the chosen EU region (ADR-0002 dependency).
- Define ingestion pipeline (parsing, chunking, embedding) and citation strategy (FR-004).
- Capacity-test retrieval latency against the interactive budget at peak concurrency.
- Re-evaluate pgvector for cost optimization after launch.

## References

- [Requirements](../../01-requirements.md)
- [PRD](../prds/sofia-center-ai-assistant.md)
- ADR-0001 (landing zone), ADR-0002 (EU region & residency), ADR-0003 (model capacity)
