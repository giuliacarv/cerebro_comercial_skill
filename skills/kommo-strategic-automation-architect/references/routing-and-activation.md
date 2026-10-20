# Specialist routing and activation

Use this map when a request spans the user's supplied source set or appears to require a separate skill, connector, or specialist.

## Know which layer you are invoking

| Layer | How it is made available | What this skill should do |
| --- | --- | --- |
| Internal specialist playbook | A Markdown file under this skill's `references/`; it is not a separate Codex skill. | Read the relevant module and apply its adapted method. |
| Independent Codex skill | A skill listed in the current Codex skill picker or otherwise confirmed installed in the current environment. | Invoke or consult it only when the task materially needs its specialty. Availability in another chat, profile, or repository does not prove availability here. |
| Connector, MCP, API, or UI tool | A tool actually enabled in the current chat with the needed scope. | Inspect its current capabilities and permissions before relying on it. A skill or source link does not grant tool access. |
| Upstream repository link | A source cited in `SOURCE_REGISTER.md`. | Use as research/attribution; do not treat the page as an installed skill or executable agent. |

Reading an internal playbook is how this orchestrator activates that specialty. Do not claim to have invoked a separate upstream skill unless Codex actually exposes that skill in this conversation. Never assume that an external GitHub URL can be loaded as a local skill or that a connector from another task is available.

## Route the supplied sources

The item numbers below refer to the user's original list. Read only the mapped module(s) relevant to the request.

| Source items | Internal module | Use for |
| --- | --- | --- |
| 0 | [discovery-and-context.md](discovery-and-context.md) | Company, offer, ICP, process context, evidence, and assumptions |
| 1, 2, 21, 22 | [workflow-architecture.md](workflow-architecture.md); [automation-governance.md](automation-governance.md) when writes, AI, or bulk changes are involved | Workflow and CRM integration design; reliability, dry-run, approval, batch, and recovery concepts |
| 3, 4, 6, 9 | [revops-and-pipeline.md](revops-and-pipeline.md) | RevOps, stage management, system architecture, and metric definitions |
| 5, 7 | [customer-lifecycle.md](customer-lifecycle.md) | Post-sale lifecycle and customer-success patterns; item 7 is a duplicate of item 5 |
| 8 | [automation-governance.md](automation-governance.md) | AI SDR pilot and outbound automation controls |
| 10a, 10c | [documentation-and-visuals.md](documentation-and-visuals.md) | Written and visual deliverables; use available Codex documentation skills when useful |
| 10b | No bundled module | Link only; license was not confirmed and no source text is redistributed |
| 11–18, 20 | [sales-operations.md](sales-operations.md) | Pipeline, hygiene, win/loss, deal review, forecast, triage, tiering, context, and explicit opportunity updates |
| 19 | [customer-lifecycle.md](customer-lifecycle.md); [sales-operations.md](sales-operations.md) when an existing opportunity or CRM update is in scope | Expansion evidence and handoff to sales operations |

## Use actual Codex specialists only when they help

- For Kommo API, UI, account data, mappings, or technical write/readback, use the independently installed `kommo-crm` skill as the technical authority. This orchestrator does not inline its procedures.
- For an ordinary reference or guide, consult `markdown-docs` only if it is available in this Codex environment and the output warrants that specialty.
- For a Markdown visual, consult `documd-visuals` only if it is currently available and a visual artifact improves the requested result.
- For skill authoring or package validation, consult `skill-creator` when available.
- For any other specialty, check current skill availability and task fit first. If none is installed, use the relevant internal playbook, narrow the deliverable, or explain the missing capability; never invent an activation.

These are conditional handoffs, not mandatory dependencies. Do not load every skill or tool for a request that one playbook and one verified data source can answer.

## When a source should become its own Codex skill

Keep a method as an internal reference when it is mainly a reusable analytical lens, overlaps other sources, assumes another CRM, or lacks a distinct reusable interface. Create a separately invokable skill only when there is a recurring user task with a clear trigger, distinct deliverable, and self-contained instructions that justify another picker entry. Write original, license-aware guidance; a source link does not grant permission to copy a skill package.
