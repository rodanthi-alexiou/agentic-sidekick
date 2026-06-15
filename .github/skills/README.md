# Skills Index — Repo Skill Set

Curated registry of the custom Copilot skills that live in this repository. Every
skill under `.github/skills/<name>/SKILL.md` is auto-discovered by VS Code Copilot;
this file is the **single place to see the whole set and keep it under control**.

> **Convention:** whenever you add a new skill, register it in the table below in
> the same change. A skill that isn't listed here is considered untracked.

## The skill set

| Skill | Purpose | Triggers (when it fires) |
|---|---|---|
| [ai-landing-zone-decision](ai-landing-zone-decision/SKILL.md) | Decision logic for choosing an Azure AI pattern (AI LZ for Foundry, AI Gateway LZ, Lightweight Accelerator, Custom Build). | Recommending an Azure AI pattern. |
| [azure-evidence](azure-evidence/SKILL.md) | Verification standard, source priority, and evidence-table column contract for `00-evidence-pack.md`. | Populating the evidence pack from a customer RFP. |
| [ms-learn-grounding](ms-learn-grounding/SKILL.md) | How and when to use the Microsoft Learn MCP server to ground Azure claims with citations. | Any claim about Azure capabilities, regions, SKUs, or patterns. |
| [doc-banner](doc-banner/SKILL.md) | Generate an AI-rendered hero / flow banner (via Foundry `MAI-Image-2.5`) for the top of a markdown doc and embed it under the H1. | "doc banner", "header image", "hero image", "flow banner", "banner for the top of the file". |

## Categories

- **Planning & grounding:** `ai-landing-zone-decision`, `azure-evidence`, `ms-learn-grounding`
- **Document presentation:** `doc-banner`

## How to add a new skill

1. Create `.github/skills/<name>/SKILL.md` with YAML frontmatter:

   ```yaml
   ---
   name: <kebab-id>
   description: <what it does + the trigger phrases that should invoke it>
   ---
   ```

2. Write the body: when to use / when not to use, then the reference logic,
   tables, or templates. Match the style of the existing skills.
3. Keep any helper scripts under `.github/skills/<name>/scripts/`.
4. **Register the skill in the table above** (purpose + triggers) in the same PR.
5. If the skill makes Azure claims, it must defer to Microsoft Learn — see
   [ms-learn-grounding](ms-learn-grounding/SKILL.md).

## Conventions

- Skill ids are lowercase-kebab and match the folder name and the `name:` field.
- `description:` is the trigger contract — write the phrases a user would actually
  say. Vague descriptions cause the skill to misfire or never fire.
- Skills capture **reusable decision logic / process**, not engagement-specific
  content (that belongs under `agent-output/<engagement>/`).
