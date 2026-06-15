---
name: azure-evidence
description: Verification standard, source priority, and the evidence-table column contract for building a source-linked Azure AI evidence pack from a customer RFP. Use when populating 00-evidence-pack.md.
---

# Azure Evidence Skill

This skill defines how the Evidence Pack agent turns a customer RFP into a verified, source-linked
capability pack (`00-evidence-pack.md`). It pairs with `ms-learn-grounding` (how to use the Learn MCP).

The rule that governs everything here: **evidence, not opinion. No link, no claim.**

## Source priority

Use sources in this order. Always prefer the highest tier that confirms the fact.

1. **Microsoft Learn** (`https://learn.microsoft.com`) — primary source for capability, limits, region, GA/Preview status, quotas, and architectural guidance. Use `microsoft_docs_search`, then `microsoft_docs_fetch` for the canonical page.
2. **Live Azure data** — pricing, model/SKU/region availability, quota, deployed catalog. Only when an Azure subscription is connected in the host. Stamp every such cell with the query date.
3. **Other Microsoft sources** (Azure Updates, official product blogs) — only when Learn does not yet cover a fact. Label the source type explicitly.

Never cite third-party blogs, forums, or GitHub issues as authoritative. Never invent services, SKUs, model names, limits, preview features, or GA dates.

## Verification standard (per row)

A row may only be marked `Yes` / `Partial` / `No` when:

- The verdict is backed by a **specific source link** (a deep link to the page that states the fact, not a search query).
- The row carries a **verification date** (`YYYY-MM-DD`) — the Learn last-updated date and/or the date you checked.
- **GA vs Preview** is stated. Never present a Preview or Retiring capability as production-ready.

If any of those three is missing, the cell is not yet verified — use the correct TBD marker below.

## Region & sovereignty rules

- Capability existing globally does **not** imply availability in the customer's required region. Verify region availability separately and record it in the `Region / sovereignty` column.
- Distinguish "data stays in the EU" from "data stays in one specific country" — they have different service footprints. If the RFP is ambiguous, mark `[TBD — ask customer]`.
- For sovereign / air-gapped cloud requirements, confirm against the sovereign cloud Learn pages, not the public-cloud pages.

## TBD markers (use exactly these)

| Marker | Use when |
|--------|----------|
| `[TBD — needs verification]` | The fact is checkable on Learn but you have not yet confirmed it |
| `[TBD — needs subscription]` | The fact requires live Azure data and no subscription is connected |
| `[TBD — ask customer]` | The RFP does not state a customer fact you need (region, volume, classification) |

Never leave a cell blank and never guess. Separate confirmed source facts from interpretation.

## Evidence-table column contract

Every ask becomes one row with these columns, in this order:

`Requirement | Azure capability / service | Supported (Yes/Partial/No) | Region / sovereignty | Evidence summary | GA/Preview | Source link | Source date / verified | Gaps & caveats`

- **Requirement** — a single discrete, testable ask derived from the RFP (split compound asks).
- **Azure capability / service** — the specific service/feature addressing it.
- **Supported** — honest verdict. `Partial` and `No` are valuable RFP evidence; record them.
- **Region / sovereignty** — region(s)/sovereignty applicable, or a TBD marker.
- **Evidence summary** — one factual line of what the source confirms (no marketing language).
- **GA/Preview** — GA / Preview / Retiring.
- **Source link** — `[source](https://learn.microsoft.com/...)`. Required for any non-TBD verdict.
- **Source date / verified** — `YYYY-MM-DD`.
- **Gaps & caveats** — limits, conditions, or a TBD marker.

## Output contract

- Write to `agent-output/<engagement>/00-evidence-pack.md`, preserving the template structure and YAML frontmatter.
- One `## N. <area>` section + one evidence table per requirement area in the RFP.
- Fill the metadata block, the coverage-summary table (one row per area), the open-questions list, and the consolidated source references.
- A single flat wide table for all areas is acceptable **only if the customer asks for one sheet** — keep the same columns.

## Honesty bar

- Record `Partial` and `No` truthfully — a documented gap is stronger RFP evidence than an unsupported `Yes`.
- Never claim overall production readiness unless identity, networking, governance, observability, validation, and operations are each evidenced.
- Never write secrets, tenant IDs, subscription IDs, or customer-confidential values into the pack.
