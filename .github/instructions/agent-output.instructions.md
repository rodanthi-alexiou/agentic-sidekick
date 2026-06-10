---
applyTo: "agent-output/**/*.md"
---

# Agent Output File Rules

These rules apply to every markdown file under `agent-output/`.

## Required structure

- Preserve the YAML frontmatter from `agent-output/_template/`. Do not strip fields.
- Keep all section headers from the template. If a section is empty, write `[TBD — ask customer]`, not nothing.
- Do not change the numbered filename convention (`01-requirements.md`, `02-challenges.md`, etc.).

## Citations

- Inline links only: `[source](https://learn.microsoft.com/...)`.
- Microsoft Learn URLs preferred. Blog/forum citations must be labelled `(external — verify)`.
- For Preview features, include the fetch date: `(Preview as of YYYY-MM-DD)`.

## Tone

- Customer-shareable. No internal Microsoft jargon, no acronyms without expansion on first use.
- Tables and bullets over paragraphs.
- Mark uncertainty explicitly with `[TBD]`, `[verification needed]`, or `[assumption]`.

## What not to do

- Do not invent numbers, customer names, or quotes.
- Do not include screenshots from internal Microsoft systems.
- Do not commit customer-confidential data — engagement folders should be `.gitignore`d at the partner repo level for any real engagement.
