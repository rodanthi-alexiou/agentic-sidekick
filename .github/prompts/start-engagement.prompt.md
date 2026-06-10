---
description: Start a new customer AI workload engagement. Creates the agent-output folder and kicks off requirements intake.
---

# /start-engagement

You are starting a new customer engagement.

**Engagement name:** `${input:engagementName:Engagement name (e.g., Contoso-RAG-KB)}`

Steps:

1. Create the folder `agent-output/${input:engagementName}/` if it doesn't already exist.
2. Copy every file from `agent-output/_template/` into the new engagement folder.
3. Open `agent-output/${input:engagementName}/01-requirements.md` for editing.
4. Switch to the **Requirements** agent (or remind the user to switch).
5. Begin the intake from Section 1 (Business context).

Do not skip ahead — do not propose architectures, costs, or patterns. Your only job right now is to set up the workspace and start the requirements interview.
