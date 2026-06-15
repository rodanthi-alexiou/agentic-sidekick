---
artifact: evidence-pack
engagement: "[engagement-name]"
customer: "[customer-name]"
source_rfp: "[path or name of the customer RFP / requirements document this pack answers]"
generated_by: evidence-pack
generated_on: "[YYYY-MM-DD]"
status: draft
---

# Evidence Pack — [Customer Name]

> Source-linked Azure AI capability evidence answering the customer's RFP / requirements document.
> Every populated row cites a specific Microsoft source and the date it was verified. No link, no claim.

## 0. Audience (partner side)

This evidence pack is intended for partner pre-sales and bid teams, and should be usable by:

- **Solution architect / pre-sales architect** — capability fit, gaps, disqualifiers
- **App developer / lead engineer** — supported integration surfaces and limits
- **Infra/platform engineer** — region/sovereignty, networking, identity capability evidence
- **Security/compliance lead** — compliance, data-handling, and certification evidence
- **Commercial / bid lead** — lift-and-paste evidence for the RFP / proposal response

## Metadata

- **Source RFP / document:** [TBD — name the customer document]
- **Requirement areas covered:** [count]
- **Azure subscription connected for live verification?** [Yes / No — if No, live-data cells are `[TBD — needs subscription]`]
- **Primary source:** Microsoft Learn (`https://learn.microsoft.com`)
- **Verification window:** [earliest – latest verification date in this pack]

## Coverage summary

One row per requirement area. `Supported` rolls up the area's individual asks (Yes = all asks supported, Partial = some, No = none).

| # | Requirement area | Asks | Supported (Yes/Partial/No) | Key gaps / caveats |
|---|------------------|------|----------------------------|--------------------|
| 1 | [area name] | [n] | [TBD] | [TBD] |
| 2 | [area name] | [n] | [TBD] | [TBD] |

---

## Evidence tables

Repeat one `## N. <area>` section per requirement area from the source RFP.

For each area: quote or paraphrase the source requirement, break it into discrete testable asks, and add one row per ask using the column contract below.

### Column contract

| Column | Meaning |
|--------|---------|
| Requirement | The discrete, testable ask derived from the RFP |
| Azure capability / service | The service/feature that addresses it |
| Supported (Yes/Partial/No) | Honest verdict — `Partial`/`No` are valuable evidence |
| Region / sovereignty | Region(s)/sovereignty applicable, or `[TBD — ask customer]` |
| Evidence summary | One-line factual statement of what the source confirms |
| GA/Preview | GA, Preview, or Retiring — never present Preview as production-ready |
| Source link | `[source](https://learn.microsoft.com/...)` — required |
| Source date / verified | Learn last-updated and/or date you verified (YYYY-MM-DD) |
| Gaps & caveats | Limits, conditions, missing facts, or `[TBD — …]` markers |

---

## 1. [Requirement area]

**Source requirement:** [quote or paraphrase the relevant RFP text]

| Requirement | Azure capability / service | Supported (Yes/Partial/No) | Region / sovereignty | Evidence summary | GA/Preview | Source link | Source date / verified | Gaps & caveats |
|-------------|----------------------------|----------------------------|----------------------|------------------|------------|-------------|------------------------|----------------|
| [ask] | [service] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |

## 2. [Requirement area]

**Source requirement:** [quote or paraphrase the relevant RFP text]

| Requirement | Azure capability / service | Supported (Yes/Partial/No) | Region / sovereignty | Evidence summary | GA/Preview | Source link | Source date / verified | Gaps & caveats |
|-------------|----------------------------|----------------------------|----------------------|------------------|------------|-------------|------------------------|----------------|
| [ask] | [service] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |

---

## Open questions

Facts that could not be verified and what would resolve them.

- [ ] [question] — resolves via [Learn page / subscription connection / customer answer]

## Source references

Consolidated list of every source cited above.

| # | Claim it supports | URL | Verified (YYYY-MM-DD) |
|---|-------------------|-----|------------------------|
| 1 | [claim] | [https://learn.microsoft.com/...] | [TBD] |
