# The Bigger Story — Where This Template Fits

This repository (**AI Workload Planner**) is one stage in a larger partner journey: taking a customer from *"we want to do something with AI"* all the way to a governed, multi-tenant workload running on Azure. Each stage has its own assets, and each is driven by GitHub Copilot — skills, agents, and ready-to-paste prompts.

This file is the **single map** of that journey. Use it to orient a partner, decide where to jump in, and find the exact Copilot asset that automates each step.

> **Grounding rule (inherited from [copilot-instructions.md](.github/copilot-instructions.md)):** every Azure claim is backed by a Microsoft Learn link. Links marked `[TBD — add link]` are intentional placeholders for you to fill with your own preferred source.

---

## The journey at a glance

```
  1. BASE          2. STANDARDIZE      3. PLAN              4. LAND             5. DEPLOY
  Learn the    →   Reusable skills  →  THIS repo        →  Landing Zone     →  APEX AI
  fundamentals     & rubrics           (pre-sales pack)    target              (agentic IaC)

  concepts         skills/rubrics      agent-output/       AI LZ for Foundry   apex-ai repo
  model · RAG      checklists          00 … 08 artifacts   AI Gateway LZ       jonathan-vella/apex
  security         grounding           pattern decision    pattern → topology  + apex-ai (WIP)
```

| Stage | You are… | Primary output | Copilot drives it with |
|-------|----------|----------------|------------------------|
| 1. Base | Learning the building blocks | Shared understanding | [`ms-learn-grounding`](.github/skills/ms-learn-grounding/SKILL.md) skill |
| 2. Standardize | Adopting reusable rubrics | Consistent decisions | [`azure-evidence`](.github/skills/azure-evidence/SKILL.md), [`ai-landing-zone-decision`](.github/skills/ai-landing-zone-decision/SKILL.md) skills |
| 3. Plan (**this repo**) | Running a pre-sales engagement | `00`–`08` artifact pack | Agents `00-evidence-pack` … `08-developer-guide` + [`/start-engagement`](.github/prompts/start-engagement.prompt.md) |
| 4. Land | Picking a deployment target | Pattern decision → LZ | [`03-pattern-selector`](.github/agents/03-pattern-selector.agent.md) + [`ai-landing-zone-decision`](.github/skills/ai-landing-zone-decision/SKILL.md) |
| 5. Deploy | Shipping infrastructure | Deployed Azure workload | [APEX](https://github.com/jonathan-vella/apex) agents (separate repo); [APEX AI](https://github.com/rodanthi-alexiou/apex-ai) AI-first variant — *work in progress* |

---

## 1. Base — Learn the fundamentals

**What it is.** The concepts a partner needs before designing anything: which model to pick, how Retrieval-Augmented Generation works, how to engineer prompts, and how to keep an AI workload safe and responsible.

**When to use it.** First customer conversation; onboarding a new engineer; whenever someone asks "but *why* this model / pattern?"

**Assets & links.**

| Concept | Microsoft Learn |
|---------|-----------------|
| Choosing a model (Foundry model catalog) | [Microsoft Foundry Models overview](https://learn.microsoft.com/azure/foundry/concepts/foundry-models-overview) |
| Enterprise RAG | [Retrieval-augmented generation (RAG) in Azure AI Search](https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview) · [RAG and indexes in Foundry](https://learn.microsoft.com/azure/ai-foundry/concepts/retrieval-augmented-generation) |
| Prompt engineering | [TBD — add link] |
| AI security & content safety | [Responsible AI in Azure workloads (WAF)](https://learn.microsoft.com/azure/well-architected/ai/responsible-ai) · [Foundry guardrails / responsible use of AI](https://learn.microsoft.com/azure/foundry/responsible-use-of-ai-overview) |

**How to drive it with Copilot.**

| Skill · Agent · Prompt | What it automates | Output |
|------------------------|-------------------|--------|
| [`ms-learn-grounding`](.github/skills/ms-learn-grounding/SKILL.md) skill | Pulls authoritative Learn answers via the Microsoft Learn MCP server instead of guessing | Cited explanations |

**Ready-to-paste prompt.**

```
Using the ms-learn-grounding skill, explain the trade-offs between PTU and
pay-as-you-go for an Azure OpenAI workload, and cite the Microsoft Learn
pages you used.
```

---

## 2. Standardize — Reusable skills & rubrics

**What it is.** The repeatable decision aids that keep every engagement consistent: an enterprise Azure AI checklist, the AI Landing Zone decision rubric, and the Microsoft Learn grounding standard.

**When to use it.** Before you make a recommendation you'll have to defend — so the *how we decided* is identical across customers and reviewers.

**Assets & links.**

| Rubric | Where it lives |
|--------|----------------|
| Evidence verification standard & source priority | [`azure-evidence`](.github/skills/azure-evidence/SKILL.md) skill |
| AI Landing Zone decision rubric | [`ai-landing-zone-decision`](.github/skills/ai-landing-zone-decision/SKILL.md) skill |
| Microsoft Learn grounding best practices | [`ms-learn-grounding`](.github/skills/ms-learn-grounding/SKILL.md) skill |
| Enterprise Azure AI checklist | [TBD — add link] (e.g. your org's AI readiness checklist) |
| Reference: AI workload design (WAF) | [Azure architecture pattern for AI workloads](https://learn.microsoft.com/azure/well-architected/ai/architecture-pattern) |

**How to drive it with Copilot.** These skills are loaded automatically by the agents below — you rarely invoke them directly. To customize the standard, edit the `SKILL.md` file; every agent that uses it picks up the change.

**Ready-to-paste prompt.**

```
Review the azure-evidence skill and tell me what verification standard each
evidence-pack row must meet before I can mark a capability "Supported".
```

---

## 3. Plan — This repo (AI Workload Planner)

**What it is.** This template. It turns a customer conversation into a full pre-sales artifact pack (`00`–`08`), grounded in live Microsoft Learn docs and reviewed by you.

**When to use it.** Any pre-sales / solutioning engagement where you need defensible requirements, a pattern decision, and an architecture before writing IaC.

**Assets & links.** See the artifact convention and roster in [README.md](README.md) and [AGENTS.md](AGENTS.md).

**How to drive it with Copilot.**

| Skill · Agent · Prompt | What it automates | Output |
|------------------------|-------------------|--------|
| [`/start-engagement`](.github/prompts/start-engagement.prompt.md) prompt | Scaffolds a new engagement folder | `agent-output/<engagement>/` |
| [`00-evidence-pack`](.github/agents/00-evidence-pack.agent.md) agent | Source-linked capability evidence from an RFP | `00-evidence-pack.md` |
| [`01-requirements`](.github/agents/01-requirements.agent.md) agent | Structured customer intake | `01-requirements.md` |
| [`02-challenger`](.github/agents/02-challenger.agent.md) agent | Socratic stress-test of the requirements | `02-challenges.md` |
| [`03-pattern-selector`](.github/agents/03-pattern-selector.agent.md) agent | Recommends an Azure AI pattern with citations | `03-pattern-decision.md` |
| [`04-architecture`](.github/agents/04-architecture.agent.md) agent | Reference architecture + rendered diagrams | `04-architecture.md` |
| [`08-developer-guide`](.github/agents/08-developer-guide.agent.md) agent | Developer implementation guide with code | `08-developer-guide.md` |

**Ready-to-paste prompt.**

```
/start-engagement Contoso-RAG-Knowledge-Base
```

> Then follow the hand-off chain: Evidence Pack → Requirements → Challenger → Pattern Selector → Architecture → Developer Guide, resolving `[TBD — ask customer]` items between steps.

---

## 4. Land — Choose a Landing Zone target

**What it is.** The output of stage 3's Pattern Selector points at a concrete landing zone. The two enterprise options are the **AI Landing Zone for Foundry** (Foundry-centric application landing zone) and the **AI Gateway Landing Zone** (an APIM layer in front of Foundry for multi-consumer governance).

> **Naming note.** "AI Citadel Landing Zone" is an internal codename for the **AI Landing Zone for Foundry**. This repo uses the Microsoft-published name throughout — see [What the Pattern Selector chooses between](README.md) for the full pattern vocabulary.

**When to use it.** Once the pattern decision is made and the customer needs a governed, private-networked target — typically because a CAF Platform Landing Zone already exists or is planned.

**Assets & links.**

| Pattern | Microsoft Learn |
|---------|-----------------|
| AI Landing Zone for Foundry | [Baseline Microsoft Foundry chat in an Azure landing zone](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone) · [Baseline Microsoft Foundry chat](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-azure-ai-foundry-chat) |
| Application vs. platform landing zones | [Deploy Azure landing zones](https://learn.microsoft.com/azure/architecture/landing-zones/landing-zone-deploy) |
| AI Gateway Landing Zone | [TBD — add link] (APIM-fronted gateway pattern) |

**How to drive it with Copilot.**

| Skill · Agent · Prompt | What it automates | Output |
|------------------------|-------------------|--------|
| [`03-pattern-selector`](.github/agents/03-pattern-selector.agent.md) agent | Maps requirements + challenges to a landing zone, with a decision matrix | `03-pattern-decision.md` |
| [`ai-landing-zone-decision`](.github/skills/ai-landing-zone-decision/SKILL.md) skill | The decision logic the agent applies | (loaded by the agent) |

**Ready-to-paste prompt.**

```
Using 01-requirements.md and 02-challenges.md, recommend a landing zone target
and justify it with the ai-landing-zone-decision rubric and Microsoft Learn
citations.
```

---

## 5. Deploy — APEX (and the APEX AI variant)

**Start here: [APEX](https://github.com/jonathan-vella/apex) by Jonathan Vella.** APEX is the original, production-proven implementation. It turns Azure platform engineering requirements into verified, deploy-ready IaC — powered by GitHub Copilot agents, real-time pricing, and built-in compliance. This is the recommended deploy stage today.

> **APEX AI is work in progress.** [APEX AI](https://github.com/rodanthi-alexiou/apex-ai) is an AI-first variant of APEX, focused on **multi-tenant, cost-attributed AI SaaS workloads** (agentic IaC with Bicep + Terraform). It builds on the upstream APEX foundation and is **not yet GA** — track it, but use the original [APEX](https://github.com/jonathan-vella/apex) for live engagements.

**When to use it.** After stage 3/4 — when the pattern decision selected a landing zone and the customer is ready to provision. This is where requirements become deployed Azure resources.

**What APEX gives you.**

- GitHub Copilot agents that turn platform requirements into deploy-ready IaC
- Real-time Azure pricing baked into the design loop
- Built-in compliance and verification before you ship

**What the APEX AI variant adds (in progress).**

- Multi-tenant agent isolation (per-customer data separation)
- Per-customer cost projections and PTU break-even analysis
- Governance discovery against *actual* Azure Policy assignments
- AVM-based Bicep/Terraform that scales from a handful of customers to hundreds

**How to drive it with Copilot.** Each repo ships its own agents and skills. Create from the template, open in the dev container, and run its requirements → architect → IaC flow. See the [APEX README](https://github.com/jonathan-vella/apex) (and the [APEX AI README](https://github.com/rodanthi-alexiou/apex-ai) for the WIP variant).

**Ready-to-paste prompt** (run inside an APEX / APEX AI repo, not here):

```
Generate a deploy-ready Bicep architecture for the pattern selected in our
03-pattern-decision.md, with real-time pricing and compliance checks.
```

---

## How the pieces connect

| Stage | Repo / location | Copilot asset | Produces | Feeds |
|-------|-----------------|---------------|----------|-------|
| 1. Base | Microsoft Learn | `ms-learn-grounding` | Grounded understanding | Stage 2 |
| 2. Standardize | `.github/skills/` (this repo) | `azure-evidence`, `ai-landing-zone-decision`, `ms-learn-grounding` | Decision rubrics | Stage 3 |
| 3. Plan | `agent-output/` (this repo) | Agents `00`–`08` + `/start-engagement` | Pre-sales artifact pack | Stage 4 |
| 4. Land | `03-pattern-decision.md` (this repo) | `03-pattern-selector` | Pattern + landing zone choice | Stage 5 |
| 5. Deploy | [jonathan-vella/apex](https://github.com/jonathan-vella/apex) (original) · [apex-ai](https://github.com/rodanthi-alexiou/apex-ai) (WIP variant) | APEX Copilot agents | Deployed, verified IaC | Production |

### Hand-off between repos

The bridge from **Plan** (this repo) to **Deploy** (APEX) is two artifacts:

- [`03-pattern-decision.md`](agent-output/_template/03-pattern-decision.md) — *which* landing zone and *why*.
- [`04-architecture.md`](agent-output/_template/04-architecture.md) — the reference architecture, identity/monitoring/governance stance, and diagrams.

Carry these two files into your [APEX](https://github.com/jonathan-vella/apex) repo (or the WIP [APEX AI](https://github.com/rodanthi-alexiou/apex-ai) variant) and feed them to its requirements/architect agents — they become the input that drives IaC generation. No re-discovery needed; the planning decisions travel with you.
