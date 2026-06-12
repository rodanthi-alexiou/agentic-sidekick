---
name: ms-learn-grounding
description: How and when to use the Microsoft Learn MCP server to ground Azure AI claims. Use whenever a claim about Azure capabilities, regions, SKUs, or patterns is being made.
---

# Microsoft Learn Grounding Skill

Every agent in this repo must ground Azure claims in Microsoft Learn. This skill defines how.

## The MCP tools

The Microsoft Learn MCP server (`https://learn.microsoft.com/api/mcp`) is wired in `.vscode/mcp.json`. It exposes:

- **`microsoft_docs_search`** — semantic search across Microsoft Learn. Returns snippets, titles, URLs. Use for almost every lookup.
- **`microsoft_docs_fetch`** — retrieves the full content of a specific Learn page in markdown. Use only when the search snippet isn't enough.

## When to use

| Situation | Action |
|-----------|--------|
| About to assert "Foundry supports X in region Y" | `microsoft_docs_search("Azure AI Foundry region availability X Y")` |
| About to recommend an AVM module | `microsoft_docs_search("avm/res/<service> Azure Verified Module")` |
| Customer asks "is feature Z GA?" | `microsoft_docs_search("<feature Z> Azure GA preview status")` |
| Citing a pattern (AI LZ, AI Gateway, etc.) | `microsoft_docs_search("<pattern name> Azure landing zone")` then `fetch` the canonical page |
| About to claim a price or SKU | Microsoft Learn covers capability, not price. Fall back to a pricing MCP (Phase 2) or note `[price verification needed]` |

## How to cite

Every recommendation in an artifact must link the supporting Learn URL inline:

```markdown
The AI Landing Zone for Foundry uses Azure Verified Modules
([source](https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/ai/...)).
```

Multiple citations are fine. One per major claim is the minimum.

## When Learn doesn't have the answer

Three options, in order of preference:

1. **Reframe the question.** Often the answer exists under different terminology — search for the underlying service or pattern.
2. **Mark it `[verification needed]`** in the artifact and note what would resolve it (a partner technical specialist, a specific Microsoft contact, a public preview signup).
3. **Do not guess.** Never assert capability without a citation. The cost of a partner being wrong in front of a customer is higher than the cost of saying "I'll verify."

## Anti-patterns

- **Citing the search snippet text without the URL** — useless to the customer.
- **Citing a Learn page that doesn't actually support the claim** — read the snippet before citing; the title isn't enough.
- **Citing blogs, MSDN forums, GitHub issues, or third-party articles** as if they were Learn — those have lower trust. If you must reference one, label it as such.
- **Citing one Learn page for ten different claims** — each claim needs its own citation.

## Recency

Microsoft Learn pages have a "last updated" date. The MCP returns it. When a claim depends on a moving target (Preview/GA status, region availability, AVM module versions), include the fetch date in the artifact:

> "Foundry Agent Service is GA in West Europe as of [Learn fetched 2026-05-27]."

This protects the partner if the customer comes back two months later and the status has changed.
