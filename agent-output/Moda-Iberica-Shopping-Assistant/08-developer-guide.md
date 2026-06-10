---
artifact: developer-guide
engagement: "Moda-Iberica-Shopping-Assistant"
customer: "Moda Ibérica"
based_on:
  - 01-requirements.md
  - 03-pattern-decision.md
  - 04-architecture.md
generated_by: developer-guide
generated_on: "2026-06-03"
status: draft
---

# Developer Implementation Guide — Moda Ibérica Shopping Assistant

## 0. Audience

This guide is for the **partner app developer / lead engineer** implementing the Moda Ibérica conversational shopping assistant on Azure. It assumes:

- Familiarity with Python or TypeScript
- Azure subscription with a Microsoft Foundry project provisioned in an EU region
- Architecture decisions from `04-architecture.md` are understood (Foundry Agent Service + AI Search RAG + tool calling for OMS/Salesforce)

---

## 1. Model Selection & Availability

### 1.1 Recommended models for Moda Ibérica

The Foundry model catalog offers over 1,900 models from Microsoft, OpenAI, Meta, Mistral, and others ([source](https://learn.microsoft.com/azure/foundry/concepts/foundry-models-overview)). For this workload:

| Use case | Recommended model | Rationale | Deployment type |
|----------|-------------------|-----------|-----------------|
| Chat orchestration (product Q&A, policy, recommendations) | **gpt-4.1** | Best balance of quality, speed, and cost for conversational RAG; supports tool calling | DataZone Standard (EU) |
| Reasoning-heavy tasks (complex outfit recommendations, multi-step tool orchestration) | **o4-mini** | Strong reasoning at lower cost than o3; supports tool calling | Global Standard or DataZone |
| Embeddings (catalog + content indexing) | **text-embedding-3-large** | High-quality embeddings for multilingual retrieval (ES/CA/PT) | Standard |
| Fallback / cost optimization | **gpt-4.1-nano** | Lightweight model for simple policy Q&A to reduce costs at peak | DataZone Standard (EU) |

> **Note:** The customer originally asked for "GPT-5" — model procurement is [TBD — ask customer]. The models above are available today.

### 1.2 Region availability (EU constraint)

Models are available in EU regions relevant to Moda Ibérica's data residency requirement ([source](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-region-availability)):

| Region | gpt-4.1 | o4-mini | o3-mini | gpt-4o | text-embedding-3-large |
|--------|----------|---------|---------|--------|------------------------|
| **Spain Central** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Sweden Central** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **West Europe** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Poland Central** | ✅ | ✅ | ✅ | ✅ | ✅ |

**Deployment types and data residency:**
- **DataZone Standard** — prompts and responses processed within the EU data zone only ([source](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/deployment-types#azure-ai-foundry-deployment-data-processing-locations))
- **Global Standard** — may be processed in any region (NOT suitable if strict EU-only is confirmed)
- **Standard (Regional)** — processed in the specific deployment region

**Recommendation for Moda Ibérica:** Use **DataZone Standard** deployment type to ensure EU-only processing while maintaining high availability across EU regions.

### 1.3 Quota & capacity

Quota is assigned per subscription, per region, per model in **Tokens-per-Minute (TPM)** units ([source](https://learn.microsoft.com/azure/foundry/openai/how-to/quota#introduction-to-quota)).

| Model | Default quota | RPM:TPM ratio | Peak estimate (2K concurrent) |
|-------|---------------|---------------|-------------------------------|
| gpt-4.1 | [TBD — check subscription] | 6 RPM per 1K TPM | [TBD — load test required] |
| o4-mini | [TBD — check subscription] | 1 RPM per 1K TPM | [TBD — load test required] |

**How to request increases:**
1. View current quota: Foundry portal → **Operate** → **Quota** ([source](https://learn.microsoft.com/azure/foundry/openai/how-to/quota#view-and-request-quotas-in-foundry-portal))
2. Request increase: [quota increase form](https://aka.ms/oai/stuquotarequest)
3. Programmatic check: Use the Usages API or Model Capacities API ([source](https://learn.microsoft.com/azure/foundry/openai/how-to/quota#programmatically-check-quota-and-capacity))

**For Black Friday peak (2K concurrent users):** Consider provisioned throughput for guaranteed capacity. Provisioned deployments reserve capacity in PTU units and are recommended for consistent high-volume workloads ([source](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/provisioned-get-started)).

---

## 2. Resource Connectivity

### 2.1 Connection map

Based on `04-architecture.md`, the agent must connect to:

| Resource | Purpose | Auth method | Notes |
|----------|---------|-------------|-------|
| Foundry Project | Agent runtime + model inference | Managed Identity | Primary connection |
| Azure AI Search | RAG retrieval (catalog, marketing, policy) | Managed Identity | Index: product catalog + content |
| Azure Key Vault | Secrets for external APIs | Managed Identity | OMS API keys, Salesforce credentials |
| OMS Inventory API | Real-time store stock | API Key (via Key Vault) | External REST; managed identity not supported |
| Salesforce Service Cloud | Order status (WISMO) | OAuth 2.0 (via Key Vault) | External; high PII risk |
| Azure Storage | Document ingestion artifacts | Managed Identity | SharePoint content staging |

### 2.2 Authentication pattern

Use `DefaultAzureCredential` which tries multiple credential sources in order ([source](https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview)):

```python
# pip install azure-identity azure-ai-projects
from azure.identity import DefaultAzureCredential

# DefaultAzureCredential tries (in order):
# 1. Environment variables (AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET)
# 2. Workload Identity (AKS)
# 3. Managed Identity (App Service, Container Apps, VM)
# 4. Azure CLI (local dev: `az login`)
# 5. Azure PowerShell
# 6. Interactive browser (fallback)
credential = DefaultAzureCredential()
```

**For production:** The App Service / Container App hosting the orchestrator should have a **system-assigned managed identity** with the following role assignments:

| Resource | Role |
|----------|------|
| Foundry Project | **Foundry User** |
| Azure AI Search | **Search Index Data Reader** |
| Key Vault | **Key Vault Secrets User** |
| Storage Account | **Storage Blob Data Reader** |

### 2.3 Foundry project connection

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Endpoint format: https://<AIFoundryResourceName>.services.ai.azure.com/api/projects/<ProjectName>
project_endpoint = os.environ["PROJECT_ENDPOINT"]
credential = DefaultAzureCredential()

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=credential,
)
```

The project endpoint can be found in the Foundry portal under **Libraries** → **Foundry** ([source](https://learn.microsoft.com/azure/foundry-classic/agents/quickstart#configure-and-run-an-agent)).

---

## 3. Tool Integration Strategy

### 3.1 Decision matrix for Moda Ibérica

| Tool type | When to use | Moda Ibérica use case | Complexity |
|-----------|-------------|----------------------|------------|
| **Function calling** | Simple, stateless logic that lives in the orchestrator | Catalog search query formatting, price formatting | Low |
| **OpenAPI tools** | Wrapping existing REST APIs with an OpenAPI spec | OMS Inventory API, Salesforce WISMO API | Medium |
| **MCP tools** | External services with existing MCP servers | Microsoft Learn search, future partner integrations | Low |
| **Built-in: File Search** | Searching uploaded documents natively | Style guide PDF, policy documents | Low |
| **Built-in: Code Interpreter** | Running Python for data analysis | Product analytics, report generation (Phase 2) | Low |
| **Azure Functions** | Complex tool logic with own dependencies/scaling | Content indexing pipeline, batch catalog sync | Medium |

### 3.2 Tool registration patterns

#### Function calling (inline)

For simple tools like formatting or validation:

```python
from azure.ai.projects.models import FunctionTool

# Define the function schema
inventory_check_function = {
    "type": "function",
    "function": {
        "name": "check_store_inventory",
        "description": "Check real-time inventory for a product at a specific store",
        "parameters": {
            "type": "object",
            "properties": {
                "product_sku": {"type": "string", "description": "Product SKU code"},
                "store_id": {"type": "string", "description": "Store identifier"},
            },
            "required": ["product_sku", "store_id"],
        },
    },
}
```

#### OpenAPI tools (for OMS/Salesforce)

Connect external APIs using an OpenAPI 3.0 spec. Supports `anonymous`, `API key`, and `managed identity` authentication ([source](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/openapi)):

```python
from azure.ai.projects.models import OpenApiTool, OpenApiFunctionDefinition, OpenApiKeyAuthDetails

# Load the OMS inventory API spec
with open("oms_inventory_openapi.json", "r") as f:
    oms_spec = f.read()

oms_tool = OpenApiTool(
    openapi=OpenApiFunctionDefinition(
        name="oms_inventory",
        spec=oms_spec,
        description="Check real-time store inventory via OMS REST API",
        auth=OpenApiKeyAuthDetails(
            # References a project connection that stores the API key securely
            project_connection_id="oms-api-connection"
        ),
    )
)
```

#### MCP tools (remote MCP server)

Connect to any remote MCP server endpoint. Foundry hosts and manages the MCP execution ([source](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)):

```python
from azure.ai.projects.models import MCPToolDefinition

# Connect to a remote MCP server (e.g., for future partner integrations)
mcp_tool = MCPToolDefinition(
    server_label="partner_crm",
    server_url="https://partner-mcp-server.example.com/mcp",
)
# Optionally restrict which tools the agent can call
mcp_tool.allowed_tools = ["search_customers", "get_order_status"]
```

**MCP security considerations:**
- Treat all credentials as secrets
- Only provide minimum required headers
- Review the MCP server provider's data handling practices
- For governance controls (rate limits, IP restrictions), see [Govern MCP tools by using an AI gateway](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/governance)

#### Built-in: File Search

For the style guide PDF and policy documents:

```python
from azure.ai.projects.models import FileSearchTool

# Upload file and create vector store first (via project_client)
# Then attach to agent
file_search_tool = FileSearchTool(vector_store_ids=[style_guide_vector_store.id])
```

### 3.3 Tool selection for Moda Ibérica MVP

| Use case | Tool type | Why |
|----------|-----------|-----|
| Product catalog search | **Function calling** + AI Search SDK | Agent formats query, code calls AI Search directly |
| Store inventory check | **OpenAPI tool** | OMS has a REST API; wrap it with OpenAPI spec |
| WISMO order status | **OpenAPI tool** (gated by auth) | Salesforce REST API; require authenticated user context |
| Policy/returns/sizing Q&A | **Built-in File Search** | Documents are uploaded to Foundry; native RAG |
| Style guide lookup | **Built-in File Search** | Same as above |
| Marketing content | **Function calling** + AI Search | Indexed in AI Search alongside catalog |

---

## 4. Agent Framework Recommendation

### 4.1 Primary: Microsoft Agent Framework SDK

The recommended framework is the **Azure AI Projects SDK** (`azure-ai-projects`) which provides the Python/JS client for Foundry Agent Service — a managed agent runtime ([source](https://learn.microsoft.com/azure/foundry/agents/overview)).

```bash
# Python
pip install azure-ai-projects azure-identity

# TypeScript
npm install @azure/ai-projects @azure/identity
```

### 4.2 Framework comparison

| Criterion | Azure AI Projects SDK (Foundry Agent Service) | Semantic Kernel | AutoGen | Direct API |
|-----------|-----------------------------------------------|-----------------|---------|------------|
| **When to use** | Default for Foundry-hosted agents; managed runtime | Existing SK plugin ecosystem; complex orchestration patterns | Multi-agent research/experimentation | Maximum control, no framework overhead |
| **Hosting** | Foundry Agent Service (managed) | Self-hosted (App Service, AKS) | Self-hosted | Self-hosted |
| **Tool support** | Native: code interpreter, file search, functions, OpenAPI, MCP, Azure Functions, Bing, A2A | Plugins/functions, manual wiring | Tools/functions | Raw function calling |
| **Observability** | Built-in tracing + evaluation via Foundry ([source](https://learn.microsoft.com/azure/foundry/concepts/observability)) | Manual instrumentation | Manual instrumentation | Manual instrumentation |
| **Multi-agent** | A2A protocol support ([source](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/agent-to-agent)) | Orchestration patterns | Native multi-agent | DIY |
| **State management** | Threads managed server-side | Manual | Session-based | Manual |
| **Deployment** | Prompt agents (server-side) or Hosted agents (containerized) ([source](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)) | App Service / AKS | App Service / AKS | App Service / AKS |

### 4.3 Why not Semantic Kernel for this workload?

Semantic Kernel remains viable if the partner already has a significant SK plugin library. However, for **new Foundry-native workloads** like Moda Ibérica:

- Foundry Agent Service provides **managed hosting, built-in tools, and tracing** that SK requires you to build yourself
- SK requires self-hosting the orchestration layer; Foundry Agent Service handles this
- The native MCP and OpenAPI tool integrations reduce custom code vs. writing SK plugins
- Built-in evaluation and content safety are integrated without additional setup

**Use Semantic Kernel if:** the partner already has SK plugins for their systems, needs fine-grained orchestration control not available in Agent Service, or must run completely self-hosted.

---

## 5. Code Examples

### 5.1 Agent creation

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool, OpenApiTool, OpenApiFunctionDefinition, OpenApiKeyAuthDetails

# Environment variables (never hardcode)
project_endpoint = os.environ["PROJECT_ENDPOINT"]
model_deployment = os.environ["MODEL_DEPLOYMENT_NAME"]  # e.g., "gpt-4.1"

credential = DefaultAzureCredential()
project_client = AIProjectClient(endpoint=project_endpoint, credential=credential)

# Create the shopping assistant agent
agent = project_client.agents.create_agent(
    model=model_deployment,
    name="moda-iberica-shopping-assistant",
    instructions="""You are the Moda Ibérica Shopping Assistant. You help customers with:
- Product discovery and recommendations
- Store stock availability
- Returns, sizing, and promotions questions
- Order status (only for authenticated users)

Rules:
- Always cite your sources when answering from documents.
- If you cannot find an answer, say so — do not guess.
- Never reveal customer PII in responses.
- Respond in the customer's language (Spanish, Catalan, or Portuguese).
""",
    tools=[
        # File search for policy docs + style guide
        *FileSearchTool(vector_store_ids=[os.environ["VECTOR_STORE_ID"]]).definitions,
    ],
)
print(f"Agent created: {agent.id}")
```

### 5.2 Adding OpenAPI tools (OMS inventory)

```python
import json

# Load the OMS OpenAPI specification
with open("specs/oms_inventory_openapi.json", "r") as f:
    oms_spec = json.loads(f.read())

# Create agent with the OpenAPI tool
agent = project_client.agents.create_agent(
    model=model_deployment,
    name="moda-shopping-assistant",
    instructions="...",  # Same as above
    tools=[
        OpenApiTool(
            openapi=OpenApiFunctionDefinition(
                name="store_inventory",
                spec=oms_spec,
                description="Check real-time product availability at Moda Ibérica stores",
                auth=OpenApiKeyAuthDetails(
                    project_connection_id=os.environ["OMS_CONNECTION_ID"]
                ),
            )
        ).definitions[0],
    ],
)
```

### 5.3 Thread & conversation management

```python
# Create a conversation thread
thread = project_client.agents.threads.create()
print(f"Thread: {thread.id}")

# Add a user message
project_client.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="¿Tenéis la chaqueta modelo Aria en talla M en la tienda de Serrano?",
)

# Run the agent on the thread
run = project_client.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id,
)

# Retrieve the assistant's response
if run.status == "completed":
    messages = project_client.agents.messages.list(thread_id=thread.id)
    for msg in messages:
        if msg.role == "assistant":
            print(msg.content[0].text.value)
```

### 5.4 Streaming responses

For the chat UI to show incremental output:

```python
from azure.ai.projects.models import AgentStreamEvent

# Create a streaming run
with project_client.agents.runs.stream(
    thread_id=thread.id,
    agent_id=agent.id,
) as stream:
    for event_type, event_data, _ in stream:
        if event_type == AgentStreamEvent.THREAD_MESSAGE_DELTA:
            # Send delta text to the frontend via WebSocket/SSE
            for content_part in event_data.delta.content:
                if hasattr(content_part, "text"):
                    print(content_part.text.value, end="", flush=True)
        elif event_type == AgentStreamEvent.THREAD_RUN_REQUIRES_ACTION:
            # Handle tool calls that require custom processing
            pass
```

### 5.5 Error handling & retry

```python
import time
from azure.core.exceptions import HttpResponseError, ServiceRequestError

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

def run_agent_with_retry(project_client, thread_id, agent_id):
    """Run agent with exponential backoff for transient failures."""
    for attempt in range(MAX_RETRIES):
        try:
            run = project_client.agents.runs.create_and_process(
                thread_id=thread_id,
                agent_id=agent_id,
            )
            if run.status == "completed":
                return run
            elif run.status == "failed":
                # Log the failure reason for observability
                print(f"Run failed: {run.last_error}")
                if run.last_error and "rate_limit" in str(run.last_error):
                    time.sleep(RETRY_DELAY_SECONDS * (2 ** attempt))
                    continue
                raise RuntimeError(f"Agent run failed: {run.last_error}")
        except HttpResponseError as e:
            if e.status_code == 429:  # Rate limited
                time.sleep(RETRY_DELAY_SECONDS * (2 ** attempt))
                continue
            raise
        except ServiceRequestError:
            # Transient network error
            time.sleep(RETRY_DELAY_SECONDS * (2 ** attempt))
            continue
    raise RuntimeError("Max retries exceeded")
```

---

## 6. Operational Wiring

### 6.1 Observability & tracing

Foundry provides three core observability capabilities: **evaluation**, **monitoring**, and **tracing** — all integrated with Azure Monitor Application Insights ([source](https://learn.microsoft.com/azure/foundry/concepts/observability#core-observability-capabilities)).

**Setup tracing:**

```python
# Install tracing support
# pip install azure-ai-projects opentelemetry-sdk azure-monitor-opentelemetry-exporter

from opentelemetry import trace
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configure Application Insights exporter
exporter = AzureMonitorTraceExporter(
    connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
)
provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)
```

Foundry Agent Service includes built-in tracing for agent threads, runs, and tool calls. View traces in the Foundry portal under **Thread logs** ([source](https://learn.microsoft.com/azure/foundry-classic/how-to/develop/trace-agents-sdk#view-thread-results-in-the-foundry-agents-playground)).

**Key metrics to track:**
- Response latency (p50/p95) per use case
- Tool call success rate (especially OMS and Salesforce)
- Token consumption per session
- Content safety filter triggers

### 6.2 Content safety

Foundry includes built-in content safety evaluation for: hateful/unfair content, sexual content, violent content, self-harm content, and protected material ([source](https://learn.microsoft.com/azure/foundry/concepts/safety-evaluations-transparency-note#the-basics-of-microsoft-foundry-risk-and-safety-evaluations)).

**For Moda Ibérica:** Configure content filters in the model deployment settings in the Foundry portal. The agent should never:
- Generate inappropriate fashion/body commentary
- Leak customer PII in responses
- Produce competitor brand recommendations

### 6.3 Evaluation hooks

Use the Foundry evaluation SDK to measure agent quality in pre-production and production ([source](https://learn.microsoft.com/azure/foundry/concepts/observability#the-three-stages-of-ai-application-lifecycle-evaluation)):

```python
# pip install azure-ai-projects>=2.2.0

# Run evaluation against agent traces
# Built-in evaluators: coherence, fluency, groundedness, relevance, 
# tool call accuracy, task completion
evaluation_result = project_client.evaluations.create(
    evaluation={
        "displayName": "moda-shopping-assistant-eval",
        "data": {"type": "trace", "agentId": f"{agent.name}:1"},
        "evaluators": {
            "groundedness": {"id": "azureai://built-in/groundedness"},
            "relevance": {"id": "azureai://built-in/relevance"},
            "coherence": {"id": "azureai://built-in/coherence"},
        },
    }
)
```

**Evaluation regions:** AI-assisted evaluators are available in East US 2, Sweden Central, US North Central, France Central, and Switzerland West ([source](https://learn.microsoft.com/azure/ai-foundry/concepts/observability#building-trust-through-systematic-evaluation)).

### 6.4 Degradation patterns for Moda Ibérica

| Failure | Agent behavior | User message |
|---------|----------------|--------------|
| OMS inventory API timeout | Skip inventory, answer from catalog only | "No puedo verificar el stock en este momento. Te recomiendo llamar a la tienda directamente." |
| Salesforce (WISMO) unavailable | Disable order status tool | "El servicio de estado de pedidos no está disponible ahora. Intenta de nuevo más tarde." |
| Model rate limit (429) | Retry with backoff; if exhausted, fallback to gpt-4.1-nano | "Un momento, por favor..." |
| Content safety trigger | Block response, log event | "No puedo responder a esa pregunta. ¿Puedo ayudarte con algo más?" |

---

## 7. Package dependencies

```bash
# Python — core
pip install azure-ai-projects>=2.1.0 azure-identity

# Python — observability
pip install opentelemetry-sdk azure-monitor-opentelemetry-exporter

# Python — evaluation (optional, for CI/CD quality gates)
pip install azure-ai-projects[evaluation]>=2.2.0
```

```bash
# TypeScript — core
npm install @azure/ai-projects @azure/identity

# TypeScript — observability
npm install @opentelemetry/sdk-node @azure/monitor-opentelemetry-exporter
```

---

## 8. MVP Implementation Checklist

| # | Task | Depends on | Status |
|---|------|-----------|--------|
| 1 | Provision Foundry project in Spain Central or Sweden Central | Azure subscription | [TBD] |
| 2 | Deploy gpt-4.1 model (DataZone Standard) + text-embedding-3-large | Step 1 | [TBD] |
| 3 | Request quota increase for Black Friday peak | Step 2 | [TBD] |
| 4 | Create AI Search index: product catalog (85K SKUs) | SAP export pipeline | [TBD] |
| 5 | Create AI Search index: marketing + policy content | SharePoint connector | [TBD] |
| 6 | Upload style guide PDF to Foundry File Search | Style guide PDF | [TBD] |
| 7 | Create OpenAPI spec for OMS Inventory API | OMS API documentation | [TBD] |
| 8 | Create agent with tools (File Search + OpenAPI) | Steps 2, 6, 7 | [TBD] |
| 9 | Implement chat API orchestration layer (App Service) | Step 8 | [TBD] |
| 10 | Wire Application Insights tracing | Step 9 | [TBD] |
| 11 | Implement streaming WebSocket/SSE for chat UI | Step 9 | [TBD] |
| 12 | Content safety filter configuration | Step 2 | [TBD] |
| 13 | Load test at 300 concurrent (typical) | Steps 8-11 | [TBD] |
| 14 | Define evaluation dataset (50+ test cases per use case) | Domain expert | [TBD] |
| 15 | WISMO integration (Phase B — after auth model confirmed) | Identity decision | [TBD — blocked by C-08] |

---

## Citations

| # | Claim | Source | Fetched |
|---|-------|--------|---------|
| 1 | Foundry model catalog: 1,900+ models | https://learn.microsoft.com/azure/foundry/concepts/foundry-models-overview | 2026-06-03 |
| 2 | Model region availability (EU regions) | https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-region-availability | 2026-06-03 |
| 3 | DataZone deployment: processed within EU | https://learn.microsoft.com/azure/ai-foundry/openai/how-to/deployment-types#azure-ai-foundry-deployment-data-processing-locations | 2026-06-03 |
| 4 | Quota management: TPM-based allocation | https://learn.microsoft.com/azure/foundry/openai/how-to/quota#introduction-to-quota | 2026-06-03 |
| 5 | View/request quotas in Foundry portal | https://learn.microsoft.com/azure/foundry/openai/how-to/quota#view-and-request-quotas-in-foundry-portal | 2026-06-03 |
| 6 | Programmatic quota/capacity check APIs | https://learn.microsoft.com/azure/foundry/openai/how-to/quota#programmatically-check-quota-and-capacity | 2026-06-03 |
| 7 | Provisioned throughput for guaranteed capacity | https://learn.microsoft.com/azure/ai-foundry/openai/how-to/provisioned-get-started | 2026-06-03 |
| 8 | Managed identities for service-to-service auth | https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview | 2026-06-03 |
| 9 | Foundry Agent Service quickstart (project endpoint) | https://learn.microsoft.com/azure/foundry-classic/agents/quickstart#configure-and-run-an-agent | 2026-06-03 |
| 10 | OpenAPI tools with managed identity/API key auth | https://learn.microsoft.com/azure/foundry/agents/how-to/tools/openapi | 2026-06-03 |
| 11 | MCP tool integration with Foundry agents | https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol | 2026-06-03 |
| 12 | MCP governance via AI gateway | https://learn.microsoft.com/azure/foundry/agents/how-to/tools/governance | 2026-06-03 |
| 13 | Foundry Agent Service overview | https://learn.microsoft.com/azure/foundry/agents/overview | 2026-06-03 |
| 14 | Hosted agent deployment (containerized) | https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent | 2026-06-03 |
| 15 | A2A protocol for multi-agent | https://learn.microsoft.com/azure/foundry/agents/how-to/tools/agent-to-agent | 2026-06-03 |
| 16 | Observability: evaluation, monitoring, tracing | https://learn.microsoft.com/azure/foundry/concepts/observability#core-observability-capabilities | 2026-06-03 |
| 17 | Content safety evaluations | https://learn.microsoft.com/azure/foundry/concepts/safety-evaluations-transparency-note#the-basics-of-microsoft-foundry-risk-and-safety-evaluations | 2026-06-03 |
| 18 | Evaluation region support | https://learn.microsoft.com/azure/ai-foundry/concepts/observability#building-trust-through-systematic-evaluation | 2026-06-03 |
| 19 | azure-ai-projects Python SDK: create agent example | https://learn.microsoft.com/python/api/overview/azure/ai-agents-readme?view=azure-python#examples | 2026-06-03 |
| 20 | Agent Framework hosted MCP tools | https://learn.microsoft.com/agent-framework/agents/tools/hosted-mcp-tools | 2026-06-03 |
| 21 | Build and register MCP server | https://learn.microsoft.com/azure/foundry/mcp/build-your-own-mcp-server#connect-the-mcp-server-to-agent-service | 2026-06-03 |
| 22 | Foundry features regional availability | https://learn.microsoft.com/azure/foundry/reference/region-support | 2026-06-03 |
| 23 | Agent Service region availability | https://learn.microsoft.com/azure/foundry/agents/concepts/limits-quotas-regions#supported-regions | 2026-06-03 |
