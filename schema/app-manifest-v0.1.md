# APP Manifest v0.1 Draft

This is a sketch of the first AgentPlaybookPack manifest shape.

The goal is to describe pack-level identity, playbook composition, skill dependencies, overlays, contracts, outputs, and compatibility without replacing Agent Skills metadata.

## Pack Manifest

Recommended filename:

```text
pack.app.yaml
```

Draft fields:

```yaml
appVersion: "0.1"
kind: pack
packId: trading-coach
name: TradingCoach
version: "1.0.0"
description: Structured trading performance reviews and debriefs.
license: TBD

compatibility:
  agentSkills: ">=1.0"
  runtimes:
    - cursor
    - openclaw

paths:
  playbooks: playbooks/
  skills: skills/
  workflows: workflows/
  overlays: overlays/
  contracts: contracts/

playbooks:
  - id: aggregate-state-review
    path: playbooks/aggregate-state-review/playbook.app.yaml
```

## Playbook Manifest

Recommended filename:

```text
playbook.app.yaml
```

Draft fields:

```yaml
appVersion: "0.1"
kind: playbook
id: aggregate-state-review
packId: trading-coach
version: "1.0.0"
description: Review portfolio state and change over a confirmed period.

inputs:
  evaluation:
    type: boolean
    default: true
  analysisPeriodStart:
    type: date
  analysisPeriodEnd:
    type: date

requires:
  - workflow: workflows/input-discovery
  - workflow: workflows/scope-confirmation

uses:
  - skill: ../../skills/normalize-broker-csv
  - skillRef:
      type: git
      uri: https://github.com/example/finance-agent-skills.git
      path: portfolio/weight-reconstruction
      version: v1.0.0
  - skillLiteral:
      name: classify-liquidity
      description: Classify cash and cash-equivalent positions.
      instructions: |
        Identify cash, money market, treasury, and short-duration bond positions.

overlays:
  - id: portfolio-evaluation
    kind: evaluation
    when: evaluation == true

gates:
  - inputs-resolved
  - period-confirmed

outputs:
  primary:
    type: report
    pathTemplate: reports/{timestamp}-{playbookId}-{scope}/Report.md
  manifest:
    pathTemplate: reports/{timestamp}-{playbookId}-{scope}/Manifest.md
```

## Manifest Kinds

Initial kinds:

- `pack`
- `playbook`
- `workflow`
- `overlay`
- `contract`

APP should not need a `skill` manifest kind if it adopts Agent Skills directly. APP references skills rather than redefining them.

## Composition Verbs

Suggested verbs:

- `requires`: must complete before the playbook can proceed
- `uses`: invoked by the playbook
- `embeds`: included inline in the output artifact
- `references`: linked or optionally consulted
- `overlays`: optional augmentation units

## Run Manifest

A run manifest records what actually happened:

```yaml
packId: trading-coach
playbookId: aggregate-state-review
packVersion: "1.0.0"
playbookVersion: "1.0.0"
appVersion: "0.1"
startedAt: "2026-06-20T17:00:00Z"
completedAt: "2026-06-20T17:15:00Z"
inputsResolved:
  evaluation: true
  analysisPeriodStart: "2026-05-01"
  analysisPeriodEnd: "2026-05-31"
skillsExecuted:
  - normalize-broker-csv
  - portfolio-weight-reconstruction
overlaysExecuted:
  - portfolio-evaluation
outputs:
  - Report.md
  - Manifest.md
```

## Open Questions

- Should APP use `.app.yaml`, `.playbook.yaml`, or another extension to avoid confusion with application manifests?
- Should manifests support JSON Schema validation from the start?
- Should pack manifests include trust and permissions directly, or delegate to store metadata?
- Should skill references be resolved eagerly at install time or lazily at execution time?
