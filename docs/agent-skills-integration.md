# Agent Skills Integration

## Positioning

APP should treat Agent Skills as the default format for granular capabilities.

Agent Skills answer:

> How does an agent learn a specific capability or procedure?

APP answers:

> How does a domain package compose capabilities into complete user-intent workflows?

## Compatibility Principle

APP should not define a competing skill file format.

When a pack needs a reusable capability, it should prefer one of these forms:

1. Local Agent Skill directory
2. External Agent Skill reference
3. Literal skill definition for lightweight or embedded use

## Local Skills

Local skills use the agentskills.io structure. In a materialized APP pack, skills live under the canonical folder `layer1-skills/` (fixed by convention — see [`app-execution.md`](app-execution.md)):

```text
layer1-skills/
  skill-name/
    SKILL.md
    references/
    scripts/
    assets/
```

The `SKILL.md` file remains the source of truth for skill activation and procedure.

APP manifests may reference the skill by path:

```yaml
uses:
  - skill: ../../layer1-skills/normalize-broker-csv
    role: normalize source data
```

## External Skill References

External references let packs compose shared skills from public or private hubs.

```yaml
uses:
  - skillRef:
      type: git
      uri: https://github.com/example/agent-skills.git
      path: finance/normalize-broker-csv
      version: v1.2.0
```

Possible reference types:

- `git`
- `registry`
- `url`
- `local`

Security and trust should be enforced by the runtime or Pack Store policy.

## Literal Skill Definitions

Literal definitions are useful for small, pack-local procedures that do not deserve a standalone skill directory yet.

```yaml
uses:
  - skillLiteral:
      name: classify-position-intent
      description: Classify a position note as trade, investment, hedge, or cash management.
      instructions: |
        Read the position note and assign one primary intent.
        Return the intent and a short rationale.
```

Literal skills should be easy to extract into full Agent Skills later.

## Progressive Disclosure

APP should preserve the Agent Skills progressive disclosure pattern:

1. Pack catalog loads minimal pack and playbook metadata.
2. Playbook activation loads the selected playbook manifest and instructions.
3. Skill activation loads only the skills required by that playbook and resolved lenses.
4. References, assets, and scripts load only when needed.

## Open Questions

- Should APP require local skills to be valid Agent Skills, or merely recommend it?
- Should APP define a lockfile for external skill references?
- Should APP allow skill version ranges, or only pinned versions?
- Should literal skills be allowed in published packs?
- How should Pack Store trust metadata interact with Agent Skills licenses and compatibility fields?
