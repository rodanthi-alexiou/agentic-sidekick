---
artifact: developer-guide
engagement: "[engagement-name]"
based_on:
  - 01-requirements.md
  - 03-pattern-decision.md
  - 04-architecture.md
generated_by: developer-guide
generated_on: "[YYYY-MM-DD]"
status: draft
---

# Developer Implementation Guide — [Customer Name]

## 0. Audience

This guide is for the **partner app developer / lead engineer** implementing the agentic AI workload. It assumes:

- Familiarity with Python or TypeScript
- Azure subscription with Foundry provisioned
- Architecture decisions from `04-architecture.md` are finalized

## 1. Model Selection & Availability

### 1.1 Recommended models

| Use case | Model | Rationale | Deployment type |
|----------|-------|-----------|-----------------|
| [TBD — from architecture] | [TBD] | [TBD] | Standard / Provisioned |

### 1.2 Region availability

- Primary region: [TBD — from 01-requirements.md]
- Failover region: [TBD — from 04-architecture.md]

### 1.3 Quota & capacity

- Current quota tier: [TBD — ask customer]
- How to request increases: [TBD — cite Learn]
- Provisioned throughput vs pay-as-you-go decision: [TBD]

## 2. Resource Connectivity

### 2.1 Connection map

| Resource | Auth method | SDK connection pattern |
|----------|-------------|----------------------|
| AI Foundry Project | Managed Identity | [TBD] |
| AI Search | Managed Identity | [TBD] |
| Cosmos DB | Managed Identity | [TBD] |
| Storage Account | Managed Identity | [TBD] |

### 2.2 Local development setup

- [TBD — DefaultAzureCredential chain explanation]

### 2.3 Connection code

```python
# [TBD — connection setup example]
```

## 3. Tool Integration Strategy

### 3.1 Decision matrix

| Tool type | When to use | Complexity | Scaling |
|-----------|-------------|------------|---------|
| MCP tools | External services with existing MCP servers | Low | Independent |
| Function calling (inline) | Simple logic in orchestrator | Low | With orchestrator |
| Azure Functions | Complex logic, independent scaling | Medium | Independent |
| Built-in (code interpreter, file search) | Foundry-native capabilities | Low | Managed |
| OpenAPI tools | Wrapping existing REST APIs | Medium | Independent |

### 3.2 Tool registration examples

```python
# [TBD — tool registration per type]
```

## 4. Agent Framework Recommendation

### 4.1 Primary: Microsoft Agent Framework SDK

- Package: `azure-ai-projects` / `azure-ai-agent`
- Hosting: Azure AI Foundry Agent Service (managed)
- [TBD — cite Learn for current SDK status]

### 4.2 Framework comparison

| Criterion | Microsoft Agent Framework SDK | Semantic Kernel | AutoGen | Direct API |
|-----------|------------------------------|-----------------|---------|------------|
| When to use | [TBD] | [TBD] | [TBD] | [TBD] |
| Hosting | Foundry Agent Service | Self-hosted | Self-hosted | Self-hosted |
| Tool support | [TBD] | [TBD] | [TBD] | [TBD] |
| Observability | [TBD] | [TBD] | [TBD] | [TBD] |

### 4.3 Why not Semantic Kernel?

[TBD — explain when SK still makes sense vs when Agent Framework SDK is preferred]

## 5. Code Examples

### 5.1 Agent creation

```python
# [TBD — create agent with model and instructions]
```

### 5.2 Tool registration

```python
# [TBD — register function calling + MCP tools]
```

### 5.3 Thread & conversation management

```python
# [TBD — create thread, add messages, run agent]
```

### 5.4 Streaming responses

```python
# [TBD — streaming pattern]
```

### 5.5 Error handling & retry

```python
# [TBD — error handling patterns]
```

## 6. Operational Wiring

### 6.1 Observability & tracing

- [TBD — Foundry built-in tracing setup]
- [TBD — Application Insights integration]

### 6.2 Content safety

- [TBD — content safety filter configuration]

### 6.3 Evaluation hooks

- [TBD — how to wire evaluation SDK for quality monitoring]

### 6.4 Error handling patterns

- [TBD — retry, fallback, circuit breaker patterns]

## 7. Package dependencies

```bash
# Python
pip install azure-ai-projects azure-identity azure-ai-evaluation

# TypeScript
npm install @azure/ai-projects @azure/identity
```

## Citations

| # | Claim | Learn URL | Fetched |
|---|-------|-----------|---------|
| 1 | [TBD] | [TBD] | [TBD] |
