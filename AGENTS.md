# Agents Overview

This repo defines a multi-agent workflow for planning AI workloads on Azure. Agents are defined in `.github/agents/*.agent.md` and consume shared skills from `.github/skills/`.

## Agent roster (Phase 1 — MVP)

| Agent | Purpose | Input | Output | Hands off to |
|-------|---------|-------|--------|--------------|
| **Evidence Pack** | Source-linked Azure capability evidence from a customer RFP | customer RFP / requirements doc | `00-evidence-pack.md` | Requirements |
| **Requirements** | Structured customer intake | `00-evidence-pack.md` (optional) | `01-requirements.md` | Challenger |
| **Challenger** | Socratic stress-test of requirements | `01-requirements.md` | `02-challenges.md` | Pattern Selector |
| **Pattern Selector** | Recommends Azure AI pattern with citations | `01-requirements.md`, `02-challenges.md` | `03-pattern-decision.md` | Architecture |

Evidence Pack is an optional starting point when the partner already has a customer RFP. Without an RFP, start at Requirements.

## Agent roster (Phase 2)

| Agent | Purpose | Input | Output | Hands off to |
|-------|---------|-------|--------|--------------|
| Architecture | Reference architecture (PoC → prod scaling) + diagram(s) rendered to PNG under `images/<mermaid-case>/` | `01`, `02`, `03` | `04-architecture.md` | Developer Guide |
| Cost & Sizing | Three-scenario cost model (PoC / pilot / prod) backed by Azure Pricing MCP | — | `05-cost-model.md` | — |

## Agent roster (Phase 3 — planned)

| Agent | Purpose | Input | Output | Hands off to |
|-------|---------|-------|--------|--------------|
| RFP | RFP-ready section pack (scope, deliverables, assumptions, pricing model) | 01–04 | `06-rfp.md` | Plan |
| Plan | Phased rollout, RACI, prerequisites, success gates | 01–06 | `07-plan.md` | Developer Guide |
| **Developer Guide** | Developer-focused agentic AI implementation: Foundry models/quotas, resource connectivity, tool integration (MCP vs custom), Microsoft Agent Framework SDK, code examples | `01`, `03`, `04` | `08-developer-guide.md` | Build |
| Build (optional) | Scaffolds Bicep/Terraform if the pattern decision selected an LZ | 03, 04, 08 | IaC files | — |

## Switching agents

In VS Code Copilot Chat, open the agent picker (the persona icon next to the chat input) and choose the agent. The workflow expects you to follow the handoff buttons that appear at the end of each agent's response — they pre-fill the next agent's prompt with the right context.

## Tool restrictions

Each agent declares its tools in YAML frontmatter:

- **Evidence Pack**: edit, search, fetch, microsoft-learn — reads a customer RFP, writes only `00-evidence-pack.md`
- **Requirements**: edit, search, microsoft-learn
- **Challenger**: search, microsoft-learn — **no edit access** to architecture files, only writes its own challenges file
- **Pattern Selector**: edit, search, microsoft-learn
- **Architecture**: edit, search, microsoft-learn — produces `04-architecture.md` with explicit identity/monitoring/governance and rendered diagrams
- **Developer Guide**: edit, search, execute, microsoft-learn — produces `08-developer-guide.md` with code snippets and Learn-grounded implementation guidance

Tool restrictions are enforced by VS Code Copilot based on the agent's `tools:` array.

Agent files are named with a numeric prefix matching their artifact (`00-evidence-pack.agent.md` … `08-developer-guide.agent.md`). The filename stem is the agent id used in each `handoffs[].agent` reference, so the handoff chain is `00 → 01 → 02 → 03 → 04 → 08`.

## Hard rules (inherited by all agents)

See `.github/copilot-instructions.md`. The non-negotiables:

1. Ground every Azure claim in Microsoft Learn.
2. Never fabricate customer information.
3. All artifacts under `agent-output/<engagement>/` with the numbered convention.
4. Cite Learn URLs inline.
5. Phase 1 agents produce planning artifacts only — no code, no IaC.
6. Phase 3 agents (Developer Guide, Build) may produce code snippets and IaC respectively.
