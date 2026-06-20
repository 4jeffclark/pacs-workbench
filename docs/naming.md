# Naming Notes

## Current Candidate

AgentPlaybookPack, abbreviated APP.

## Why This Name Works

- It avoids the word "skill" and reduces confusion with agentskills.io.
- It makes "playbook" the primary unit of value.
- It suggests repeatable, domain-specific workflows rather than one-off prompts.
- It can sit naturally above Agent Skills in the integration stack.

## Potential Concern

APP may be confused with "application" in some contexts.

Mitigations:

- Use the full name in formal docs.
- Treat APP as a friendly shorthand, not the only brand.
- Use manifest names like `pack.app.yaml` only if the acronym proves acceptable.

## Other Names Considered

| Name | Impression |
| --- | --- |
| AgenticWorkflowPack | Clear and descriptive, but more generic |
| AgenticBehaviorPack | Broad, but may imply personality, rules, or policy steering |
| AgenticJobPack | Outcome-oriented, but can sound like batch execution |
| DomainPlaybookPack | Very clear and less buzzword-heavy |
| WorkflowPack | Simple, but too broad without context |
| PlaybookPack | Clean, but less agent-specific |

## Current Recommendation

Use AgentPlaybookPack for the framework baseline and describe it as:

> A domain workflow package that composes Agent Skills, tools, workflows, contracts, overlays, and outputs into complete agent-run playbooks.
