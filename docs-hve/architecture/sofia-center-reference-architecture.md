# Sofia Center AI Assistant — Reference Architecture (Mermaid)

> Source: [PRD](prds/sofia-center-ai-assistant.md) · ADRs [0001](decisions/2026-06-15-lightweight-landing-zone.md) · [0002](decisions/2026-06-15-eu-region-residency.md) · [0003](decisions/2026-06-15-model-capacity-hybrid.md) · [0004](decisions/2026-06-15-rag-vector-store.md)

## System architecture

```mermaid
flowchart TB
    User["EU Users<br/>students / staff / researchers"]
    Entra["Microsoft Entra ID<br/>SAML 2.0 / OIDC / WS-Fed<br/>federated SSO"]

    subgraph EU["EU Data Boundary — Single EU Region (ADR-0002)"]
        direction TB
        FD["Azure Front Door + WAF<br/>TLS · rate limit · DDoS"]

        subgraph LZ["Lightweight Application Landing Zone — Private Link (ADR-0001)"]
            direction TB
            APIM["API Management<br/>REST API + auth"]
            APP["App Tier (stateless)<br/>Chat GUI + REST API<br/>Container Apps / AKS"]
            CACHE["Semantic Cache<br/>Redis (EU)"]
            STATE["Session / State<br/>Redis / Cosmos (EU)"]
            ROUTER["Model Router<br/>tier select + route-down"]

            FLAG["Azure OpenAI / Foundry<br/>FLAGSHIP — PTU (ADR-0003)"]
            EFF["Azure OpenAI / Foundry<br/>EFFICIENT + BALANCED — PAYG (ADR-0003)"]
            SAFETY["AI Content Safety<br/>+ injection guardrails"]

            subgraph RAG["RAG Knowledge Plane (ADR-0004)"]
                direction TB
                INGEST["Ingestion<br/>parse · chunk · embed"]
                SEARCH["Azure AI Search (EU)<br/>hybrid search + citations"]
                BLOB["Document Storage<br/>Blob (EU)"]
            end

            BATCH["Batch Inference (EU)<br/>latency-insensitive jobs"]
        end

        subgraph CC["Cross-cutting"]
            direction LR
            KV["Key Vault (EU)"]
            MI["Managed Identity"]
            POLICY["Azure Policy<br/>residency · deny-public"]
            LOGS["Log Analytics +<br/>App Insights (EU)"]
            DEF["Defender for Cloud"]
        end
    end

    User -->|HTTPS| FD
    User <-->|SSO redirect| Entra
    FD --> APIM
    APIM --> APP
    APP --> CACHE
    APP --> STATE
    APP --> ROUTER
    ROUTER --> FLAG
    ROUTER --> EFF
    FLAG --> SAFETY
    EFF --> SAFETY
    APP --> INGEST
    INGEST --> SEARCH
    INGEST --> BLOB
    APP -->|retrieve| SEARCH
    BLOB -->|source| SEARCH
    ROUTER -.->|offline| BATCH
    BATCH --> BLOB

    APP -.-> LOGS
    APP -.-> KV
    APP -.-> MI
```

## Flow 1 — Interactive chat with RAG

```mermaid
sequenceDiagram
    actor U as EU User
    participant E as Entra ID
    participant FD as Front Door / WAF
    participant G as API Management
    participant A as App Tier
    participant C as Semantic Cache
    participant R as Model Router
    participant S as AI Search (EU)
    participant M as Model (PTU/PAYG)
    participant SF as Content Safety

    U->>E: Authenticate (SSO)
    E-->>U: Token
    U->>FD: Chat request + token
    FD->>G: Forward (TLS, rate-limited)
    G->>A: Authorized request
    A->>C: Check semantic cache
    alt Cache hit
        C-->>A: Cached answer
        A-->>U: Stream answer
    else Cache miss
        A->>R: Route by tier
        A->>S: Retrieve passages (hybrid)
        S-->>A: Top-k chunks + sources
        R->>M: Prompt + context
        M->>SF: Safety / injection check
        SF-->>M: Pass
        M-->>A: Streamed completion
        A->>C: Store in cache
        A-->>U: Stream cited answer
    end
```

## Flow 2 — Document upload & ingestion

```mermaid
sequenceDiagram
    actor U as EU User
    participant A as App Tier
    participant B as Blob Storage (EU)
    participant I as Ingestion
    participant EM as Embeddings Model (EU)
    participant S as AI Search (EU)

    U->>A: Upload document (PDF/DOCX/XLSX/PPTX/HTML)
    A->>B: Persist source document
    A->>I: Trigger ingestion
    I->>B: Read document
    I->>I: Parse + chunk
    I->>EM: Embed chunks
    EM-->>I: Vectors
    I->>S: Upsert index (vectors + metadata)
    S-->>A: Indexed (queryable)
    A-->>U: Ready for Q&A
```

## Flow 3 — Batch inference

```mermaid
sequenceDiagram
    participant Sch as Scheduler
    participant BA as Batch Inference (EU)
    participant B as Blob Storage (EU)
    participant S as AI Search (EU)

    Sch->>BA: Submit batch job (EU-resident)
    BA->>B: Read inputs
    BA->>BA: Process (latency-insensitive)
    BA->>B: Write results
    BA-->>S: Optional index update
    BA-->>Sch: Job complete
```

## Flow 4 — Authentication (federated SSO)

```mermaid
sequenceDiagram
    actor U as EU User
    participant A as App / Front Door
    participant E as Entra ID
    participant IdP as Institutional IdP<br/>(SAML/OIDC/WS-Fed)

    U->>A: Access platform
    A->>E: Redirect to sign-in
    E->>IdP: Federate to home institution
    IdP-->>E: Assertion / claims
    E-->>U: Issue token
    U->>A: Request + token
    A->>A: Validate token + RBAC
    A-->>U: Authorized session
```
