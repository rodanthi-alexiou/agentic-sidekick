# AI Workload Planner — Project Instructions

Always-on context for every Copilot chat interaction in this workspace. All agents inherit this.

## Purpose of this repository

This repo guides a Microsoft partner through planning an AI workload on Azure, from initial customer conversation to a defensible architecture and RFP. The output is a numbered set of markdown artifacts under `agent-output/<engagement-name>/`.

## Hard rules

1. **Ground every Azure claim in Microsoft Learn.** Use the `microsoft_docs_search` and `microsoft_docs_fetch` MCP tools. Do not assert a feature exists, a region supports a service, a SKU price, or a pattern is recommended without a Learn citation. If Learn doesn't confirm it, say so.
2. **Never fabricate customer information.** If a requirement is unknown, mark it `[TBD — ask customer]`. Do not invent users, volumes, latencies, regions, or compliance scopes.
3. **All artifacts go under `agent-output/<engagement-name>/`** using the numbered convention (`01-requirements.md` through `07-plan.md`). Copy `agent-output/_template/` when starting a new engagement.
4. **Cite sources inline.** Every recommendation links to the Microsoft Learn URL it came from. Use the format `[source](https://learn.microsoft.com/...)`.
5. **No code generation in Phase 1.** The MVP agents produce planning artifacts only. IaC scaffolding is a Phase 3 concern.

## Tone

- Partner-facing. Plain Azure terminology, no internal Microsoft jargon (no "1ES", "FY26", "MSX", "MCAPS").
- Concise. Tables and bullets over paragraphs.
- Honest about uncertainty. Prefer "Microsoft Learn shows X as Preview as of [fetch date]" over confident claims.

## The AI workload journey (canonical)

```
Requirements  →  Challenger  →  Pattern Selector  →  (Architecture)  →  (Cost)  →  (RFP)  →  (Plan)
   01            02              03                    04               05         06         07
```

Phase 1 of this template ships agents 1-3. Steps 4-7 are placeholders in `agent-output/_template/`.

## Pattern vocabulary (be precise)

When discussing Azure AI patterns, use these exact names and link to their authoritative Learn pages on first mention:

- **AI Landing Zone for Foundry** — Foundry-centric application landing zone (Bicep + Terraform, AVM-based)
- **AI Gateway Landing Zone** — APIM-fronted gateway pattern in front of Foundry/AOAI
- **AI Hub Landing Zone** — older Hub-and-Project model (still valid for some scenarios)
- **Lightweight Accelerator** — single-resource-group quickstart, not enterprise-scale
- **Custom Build** — bespoke architecture when no LZ fits

If the customer already has a Platform Landing Zone (CAF ALZ), the AI LZ is an *application landing zone* deployed on top of it.

## File conventions

- Markdown only for planning artifacts.
- Use the YAML frontmatter present in each `_template/` file — do not strip it.
- Filenames are lowercase-kebab; engagement folder names use customer-recognizable PascalCase or kebab (e.g., `Contoso-RAG-KB`).

## What "done" means for each artifact

| File | Done when |
|------|-----------|
| `01-requirements.md` | Every section has either an answer or `[TBD — ask customer]`. No invented content. |
| `02-challenges.md` | At least 5 stress-test questions raised, each tied to a specific requirement line. |
| `03-pattern-decision.md` | One pattern recommended, two runners-up listed, decision matrix included, every claim cited to Learn. |
