# Engagement Output Template

This folder is the starting point for every new customer engagement. The `/start-engagement` prompt copies it into `agent-output/<engagement-name>/` when you begin intake.

## File map

| File | Owned by | Description |
|------|----------|-------------|
| `01-requirements.md` | Requirements agent | Structured intake — business context, users, data, NFRs, compliance, delivery preferences |
| `02-challenges.md` | Challenger agent | Socratic stress-test of `01-requirements.md` — questions, red flags |
| `03-pattern-decision.md` | Pattern Selector agent | Recommended Azure AI pattern with decision matrix and Learn citations |
| `04-architecture.md` | Architecture agent (Phase 2) | Reference architecture, AVM module list, diagram |
| `05-cost-model.md` | Cost agent (Phase 2) | PoC / pilot / prod cost scenarios |
| `06-rfp.md` | RFP agent (Phase 3) | RFP-ready section pack |
| `07-plan.md` | Plan agent (Phase 3) | Phased rollout, RACI, prerequisites |

## Conventions

- Numbered prefixes are required and immutable.
- All files are markdown with YAML frontmatter.
- Never delete a section from a template file — if empty, mark it `[TBD]`.

## Scope note (pre-sales)

These templates are planning artifacts. They should remain pre-sales (requirements, risks, decisions, architecture) and must not include implementation code or IaC.
