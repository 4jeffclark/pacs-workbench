# Agent Skills Integration

## Positioning

APP **layer1-skills** are [agentskills.io](https://agentskills.io/specification) Agent Skills. APP composes them into playbooks; it does not define an alternate skill format or scripting mode.

Normative skill shape and scripting baseline: [`app-skills.md`](app-skills.md).

Agent Skills answer:

> How does an agent learn a specific capability or procedure?

APP answers:

> How does a domain package compose capabilities into complete user-intent workflows?

## Compatibility Principle

APP must not define a competing skill file format.

When a pack needs a reusable capability, it should prefer one of these forms:

1. Local Agent Skill directory under `layer1-skills/`
2. External Agent Skill reference
3. Literal skill definition for lightweight or embedded use (extract to full skills when they grow)

## Local Skills

Local skills use the agentskills.io directory structure under `layer1-skills/` (see [`app-execution.md`](app-execution.md)):

```text
layer1-skills/
  skill-name/
    SKILL.md          # required
    scripts/          # required directory; bundled code when present
    references/       # optional
    assets/           # optional
```

`SKILL.md` is the source of truth for activation, procedure, and when to run bundled scripts.

APP manifests reference skills by path:

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

Literal skills should be extracted into full Agent Skills directories (with `scripts/` baseline) when they grow.

## Progressive Disclosure

APP preserves the Agent Skills progressive disclosure pattern:

1. Pack catalog loads minimal pack and playbook metadata.
2. Playbook activation loads the selected playbook manifest and instructions.
3. Skill activation loads only the skills required by that playbook and resolved lenses.
4. `references/`, `assets/`, and `scripts/` load only when needed.

## Open Questions

- Should APP define a lockfile for external skill references?
- Should APP allow skill version ranges, or only pinned versions?
- Should literal skills be allowed in published packs?
- How should Pack Store trust metadata interact with Agent Skills licenses and `compatibility` fields?
