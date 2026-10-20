# Source register

The user supplied this source list on 2026-10-20. The repository uses original guidance informed by these references; it does not vendor their `SKILL.md` files. Verify upstream content and licensing again before future reuse because repositories can change.

| User item | Supplied source | License / source note | Adaptation in this project |
| --- | --- | --- | --- |
| 0 | [LeadMagic: GTM context bootstrap](https://github.com/LeadMagic/gtm-skills/blob/main/skills/foundation/gtm-context-bootstrap/SKILL.md) | LeadMagic repository MIT license | Evidence-linked context, facts vs assumptions, freshness, owner validation; no company facts imported. |
| 1 | [a275618631: workflow automation agent](https://github.com/a275618631/codex-agent-skills/blob/main/skills/workflow-automation-agent/SKILL.md) | Repository MIT license | Trigger, eligibility, side effects, approval, idempotency, failure, audit, dry run, and recovery as original checklist. |
| 2 | [LeadMagic: CRM integration](https://github.com/LeadMagic/gtm-skills/blob/main/skills/automation/crm-integration/SKILL.md) | LeadMagic repository MIT license | Data ownership, lifecycle, deduplication, source of truth, and reporting; examples require Kommo/account validation. |
| 3 | [Corey Haines: RevOps](https://github.com/coreyhaines31/marketingskills/blob/main/skills/revops/SKILL.md) | Repository MIT license | Lifecycle, routing, pipeline, and measurement concepts; no source benchmark becomes a target. |
| 4 | [LeadMagic: pipeline management](https://github.com/LeadMagic/gtm-skills/blob/main/skills/sales-revops/pipeline-management/SKILL.md) | LeadMagic repository MIT license | Stage purpose, entry/exit evidence, handoffs, and review; WbD/MEDDIC or ACV assumptions stay optional. |
| 5 | [Claude for Customer Success](https://github.com/t0ddc3by/claude-for-customer-success) | Upstream repository redirects to `successcoaching/claude-for-customer-success`; Apache-2.0 | Lifecycle and modular architecture pattern only; named methodology, plugins, prompts, and connectors are not installed. |
| 6 | [LeadMagic: GTM metrics](https://github.com/LeadMagic/gtm-skills/blob/main/skills/analytics/gtm-metrics/SKILL.md) | LeadMagic repository MIT license | Metric contract, cohorts, units, and source fields; SaaS benchmarks are excluded as defaults. |
| 7 | [Claude for Customer Success](https://github.com/t0ddc3by/claude-for-customer-success) | Duplicate of item 5; same redirect and Apache-2.0 repository | Counted once for unique sources; see item 5. |
| 8 | [LeadMagic: AI SDR setup](https://github.com/LeadMagic/gtm-skills/blob/main/skills/automation/ai-sdr-setup/SKILL.md) | LeadMagic repository MIT license | Pilot, suppression, evidence, human handoff, stop conditions; not permission to message and not legal guidance. |
| 9 | [LeadMagic: GTM system architecture](https://github.com/LeadMagic/gtm-skills/blob/main/skills/analytics/gtm-system-architecture/SKILL.md) | LeadMagic repository MIT license | System-boundary and staged-roadmap concepts; subjective scoring and SaaS assumptions are not adopted. |
| 10a | [documd-visuals](https://github.com/markdown-viewer/skills/blob/main/documd-visuals/SKILL.md) | Skill metadata identifies CC-BY-4.0; existing Codex skill is referenced, not copied. | Optional route for visual Markdown deliverables only. |
| 10b | [Codex Excalidraw skill](https://github.com/fabricioartur/codex-excalidraw-skill/blob/main/skill/SKILL.md) | License not confirmed during review; source linked only, no content redistributed. | Not installed; external upload behavior is not assumed or authorized. |
| 10c | [markdown-docs](https://github.com/arjunprabhulal/agent-skills/blob/main/skills/docs/markdown-docs/SKILL.md) | Repository MIT license; existing Codex skill is referenced, not copied. | Optional route for task-focused written deliverables. |
| 11 | [Anthropic: pipeline review](https://github.com/anthropics/knowledge-work-plugins/blob/main/sales/skills/pipeline-review/SKILL.md) | Repository Apache-2.0 | Scoped read-only review and evidence-backed flags; connector details and fixed thresholds excluded. |
| 12 | [Anthropic: CRM hygiene check](https://github.com/anthropics/knowledge-work-plugins/blob/main/sales/skills/crm-hygiene-check/SKILL.md) | Repository Apache-2.0 | Read-only audit and proposals; no Salesforce/HubSpot entity assumptions. |
| 13 | [Anthropic: win/loss review](https://github.com/anthropics/knowledge-work-plugins/blob/main/sales/skills/win-loss-review/SKILL.md) | Repository Apache-2.0 | Sample size, source, outcome counts, and cautious qualitative review. |
| 14 | [Anthropic: deal review](https://github.com/anthropics/knowledge-work-plugins/blob/main/sales/skills/deal-review/SKILL.md) | Repository Apache-2.0 | Supported/contradicted/unknown evidence; static probability adjustments excluded. |
| 15 | [Anthropic: forecast](https://github.com/anthropics/knowledge-work-plugins/blob/main/sales/skills/forecast/SKILL.md) | Repository Apache-2.0 | Local forecast categories and snapshots; no official forecast submission by implication. |
| 16 | [Anthropic: lead triage](https://github.com/anthropics/knowledge-work-plugins/blob/main/sales/skills/lead-triage/SKILL.md) | Repository Apache-2.0 | Evidence-backed fit, intent, deduplication, and reason codes; fixed priority shares and SLAs excluded. |
| 17 | [Anthropic: account tiering](https://github.com/anthropics/knowledge-work-plugins/blob/main/sales/skills/account-tiering/SKILL.md) | Repository Apache-2.0 | Transparent fit/engagement criteria; weights and cutoffs require local calibration. |
| 18 | [Anthropic: account context](https://github.com/anthropics/knowledge-work-plugins/blob/main/sales/skills/account-context/SKILL.md) | Repository Apache-2.0 | Context assembly with source boundaries and freshness; use only authorized connected sources. |
| 19 | [Anthropic: expansion whitespace](https://github.com/anthropics/knowledge-work-plugins/blob/main/sales/skills/expansion-whitespace/SKILL.md) | Repository Apache-2.0 | Evidence-backed hypotheses presented for discovery before opportunity creation. |
| 20 | [Anthropic: update opportunity](https://github.com/anthropics/knowledge-work-plugins/blob/main/sales/skills/update-opportunity/SKILL.md) | Repository Apache-2.0 | Explicit before/after scope and readback; no unrequested field writes. |
| 21 | [HubSpot: workflow automation](https://github.com/HubSpot/agent-cli-skills/blob/main/workflow-automation/SKILL.md) | Repository Apache-2.0 | Dry-run, change digest, rollback, and verification concepts; HubSpot CLI/workflow instructions excluded. |
| 22 | [HubSpot: bulk operations](https://github.com/HubSpot/agent-cli-skills/blob/main/bulk-operations/SKILL.md) | Repository Apache-2.0 | Pagination, bounded batches, preview, and readback concepts; no HubSpot CLI or API claims for Kommo. |

## Coverage

- 23 numbered positions supplied by the user.
- 25 URL entries because item 10 groups three sources and item 5/7 repeats one repository.
- 24 unique URLs after deduplicating item 7.
- No third-party instruction file, credential, CRM export, customer list, or account snapshot is included.

## License handling

The repository's [`LICENSE`](LICENSE) applies to the original materials in this project only. It does not override third-party license terms. This source register records attribution and whether a license was checked; it is not legal advice. Recheck each repository's current license and the individual file's terms before copying, redistributing, or adapting expressive text. The project intentionally links to the upstream sources instead of bundling their skill files.
