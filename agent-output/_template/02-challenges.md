---
artifact: challenges
engagement: "[engagement-name]"
based_on: 01-requirements.md
generated_by: challenger
generated_on: "[YYYY-MM-DD]"
status: draft
---

# Challenges — [Customer Name]

Socratic stress-test of `01-requirements.md`. Each challenge records the question, the reasoning, the partner's answer, and the outcome. This is a **conversation log** — blank answer fields mean the question still needs a customer session to resolve.

## 0. Audience (partner side)

Use this in a pre-sales workshop with:

- **Solution architect / pre-sales architect** (decision gates + risks)
- **App developer / lead engineer** (integration + tool semantics)
- **Infra/platform engineer** (network/identity/ops constraints)
- **Security/compliance lead** (data handling + audit/retention)

## How to read this document

- **C-XX**: a single challenge. Open-ended question, not a verdict.
- **Answer (recorded)**: what the partner knew at time of challenge session. ⏳ means still needs customer input.
- **Outcome**: ✅ Closed / ⚠️ Risk surfaced / 🚫 Blocker.
- **Red flags**: challenges with a Blocker outcome. Resolve before architecture work begins.

---

## Challenges

### C-01: [short title]

**Challenges requirement:** [section name and exact text being challenged]

**Question:** [one focused, open-ended question]

**Why it matters:** [one or two sentences on the consequence if the assumption is wrong]

**Evidence that would resolve this:** [what answer / data / proof closes the question]

**Answer (recorded):** [partner's answer verbatim, or "⏳ No answer yet — needs customer input"]

**Outcome:** [✅ Closed — / ⚠️ Risk surfaced — / 🚫 Blocker —]

---

### C-02: [short title]

**Challenges requirement:** [...]

**Question:** [...]

**Why it matters:** [...]

**Evidence that would resolve this:** [...]

**Answer (recorded):** [...]

**Outcome:** [...]

---

*(Add C-03, C-04, ... as needed. Minimum 5 total. All fields required.)*

---

## Red flags

List any challenges that are blocking-level. If empty, write "None identified."

- [ ] **C-XX**: [one-line description of why this is a red flag]

---

## Recommendation

- **Total challenges asked:** [count]
- **Answered / closed:** [count]
- **Open (needs customer input):** [count]
- **Blockers:** [count]
- **Recommendation:** [ready for Pattern Selector / resolve red flags first / resolve open items with customer before proceeding]

## Next workshop (pre-sales)

List who should attend to close the red flags and open items:

- **Customer security/identity owner:** [TBD]
- **Customer application owner:** [TBD]
- **Customer data owner:** [TBD]
- **Customer operations/SRE:** [TBD]
