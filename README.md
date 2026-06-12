# AI Workload Planner — Copilot Template

A GitHub template repository for Microsoft partners that turns a customer conversation about an AI workload into a full pre-sales artifact pack — grounded in live Microsoft Learn docs, written by Copilot agents, reviewed by you.

Built on GitHub Copilot custom agents, skills, and the Microsoft Learn MCP server.

---

## The delivery flow

Each agent hands off to the next. You stay in VS Code throughout.

```
Customer conversation
        │
        ▼
┌───────────────────┐
│  1. Requirements  │  Structured intake → 01-requirements.md
│     (Phase 1)     │  Business outcome, users, data, latency,
└────────┬──────────┘  sovereignty, compliance, IaC preference
         │ hand off
         ▼
┌───────────────────┐
│  2. Challenger    │  Socratic stress-test → 02-challenges.md
│     (Phase 1)     │  Surfaces ambiguities before any design work
└────────┬──────────┘  begins. Read-only — never edits requirements.
         │ hand off
         ▼
┌───────────────────┐
│  3. Pattern       │  Azure AI pattern decision → 03-pattern-decision.md
│     Selector      │  Recommends one of five patterns (see below),
│     (Phase 1)     │  decision matrix, and live Microsoft Learn citations.
└────────┬──────────┘
         │ hand off
         ▼
┌───────────────────┐
│  4. Architecture  │  Reference architecture → 04-architecture.md
│     (Phase 2)     │  PoC → pilot → production scaling path, identity,
└────────┬──────────┘  networking, security, observability. Mermaid
         │             diagrams rendered to PNG under images/.
         ▼
┌───────────────────┐  ┌──────────────────────────────────────────────┐
│  5. Cost Model    │  │ Three-scenario cost estimate (PoC / pilot /  │
│     (planned)     │  │ prod) against Azure Pricing.                 │
└────────┬──────────┘  └──────────────────────────────────────────────┘
         ▼
┌───────────────────┐  ┌──────────────────────────────────────────────┐
│  6. RFP           │  │ Scope, deliverables, assumptions, pricing    │
│     (planned)     │  │ model — ready to paste into a proposal.      │
└────────┬──────────┘  └──────────────────────────────────────────────┘
         ▼
┌───────────────────┐  ┌──────────────────────────────────────────────┐
│  7. Plan          │  │ Phased rollout, RACI, prerequisites,         │
│     (planned)     │  │ success gates.                               │
└───────────────────┘  └──────────────────────────────────────────────┘
```

Every agent writes its artifact to `agent-output/<engagement-name>/` using the numbered convention. Nothing is shared with the customer until you review it.

---

## What the Pattern Selector chooses between

| Pattern | Use when |
|---------|----------|
| **AI Landing Zone for Foundry** | Enterprise or regulated workload; CAF Platform LZ exists or is planned; private networking required |
| **AI Gateway Landing Zone** | Multiple consumers, multi-model routing, central token quotas, or cross-team access governance (APIM layer — complements Foundry LZ) |
| **Lightweight Accelerator** | 4–8 week PoC, single team, no compliance scope, explicit willingness to rebuild for production |
| **Custom Build** | Edge, sovereign, on-prem hybrid, or highly specialised SKUs where no LZ fits |

---

## Who uses the artifacts (and how)

| Role | Primary artifact | What they take away |
|------|-----------------|---------------------|
| Solution / pre-sales architect | 03-pattern-decision, 04-architecture | Decision narrative, risks, gates, next workshop agenda |
| App developer / lead engineer | 04-architecture | Integration surfaces, tool calls, data flows, failure modes |
| Infra / platform engineer | 04-architecture | Networking stance, identity boundaries, environment separation |
| Security / compliance lead | 04-architecture | Data handling, sovereignty, auditability, retention |
| Commercial / account team | 05-cost-model, 06-rfp | Three-scenario pricing, RFP-ready scope and assumptions |

---

## Quick start

1. Click **Use this template → Create a new repository**. Choose **Private**.
2. Open the repo in VS Code with the GitHub Copilot extension (Business or Enterprise license recommended).
3. When prompted, allow the workspace to use the Microsoft Learn MCP server (configured in `.vscode/mcp.json`).
4. Open Copilot Chat, select the **Requirements** agent, and type:

   ```
   /start-engagement Contoso-RAG-Knowledge-Base
   ```

5. The agent creates `agent-output/Contoso-RAG-Knowledge-Base/` and guides you through intake. When it's done, click **Hand off to Challenger**.
6. Follow the handoff chain — Challenger → Pattern Selector → Architecture — reviewing and resolving `[TBD — ask customer]` items between steps.

---

## Project structure

```
.github/
  agents/                        # Custom Copilot agents
    requirements.agent.md
    challenger.agent.md
    pattern-selector.agent.md
    architecture.agent.md
  skills/                        # Reusable domain knowledge loaded by agents
    ai-landing-zone-decision/SKILL.md
    ms-learn-grounding/SKILL.md
  instructions/                  # File-scoped rules (glob-targeted)
    agent-output.instructions.md
  prompts/                       # Reusable /commands
    start-engagement.prompt.md
  copilot-instructions.md        # Always-on context inherited by all agents
.vscode/
  mcp.json                       # Microsoft Learn MCP server wiring
agent-output/
  _template/                     # Numbered artifact templates (01–07)
  <engagement-name>/             # One folder per customer engagement
AGENTS.md                        # Agent roster and hand-off rules
```

---

## Status

| Phase | Agents | Artifacts |
|-------|--------|-----------|
| 1 | Requirements, Challenger, Pattern Selector | `01` `02` `03` — **included** |
| 2 | Architecture | `04` — **included** |
| 2 | Cost & Sizing | `05` — templates only, agent planned |
| 3 | RFP, Plan | `06` `07` — templates only, agents planned |
| 3 | IaC scaffolding | Bicep/Terraform gated by pattern decision — planned |

---

## Requirements

- VS Code (latest stable) with GitHub Copilot extension
- GitHub Copilot Business or Enterprise license (recommended for org-level agent sharing)
- Internet access — the Microsoft Learn MCP server is a hosted endpoint, no auth required

## Customization

| What to change | Where |
|---------------|-------|
| AI LZ pattern decision rules | `.github/skills/ai-landing-zone-decision/SKILL.md` |
| Challenger tone (socratic vs. evaluative) | `.github/agents/challenger.agent.md` |
| Architecture depth / sections | `.github/agents/architecture.agent.md` |
| Add an MCP server (Azure Pricing, etc.) | `.vscode/mcp.json` + each agent's `tools:` list |

## License

MIT (suggested). Add your organization's license file before sharing externally.
