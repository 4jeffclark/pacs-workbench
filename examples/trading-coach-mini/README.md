# TradingCoach Mini Example

This example shows how a TradingCoach-style domain pack might look under the AgentPlaybookPack model.

It is intentionally small and illustrative. It is not a runnable TradingCoach migration.

## Example Shape

```text
trading-coach-mini/
  pack.app.yaml
  playbooks/
    portfolio-snapshot/
      playbook.app.yaml
      README.md
  skills/
    summarize-holdings/
      SKILL.md
    classify-liquidity/
      SKILL.md
  workflows/
    input-discovery.md
    period-confirmation.md
  overlays/
    coaching-evaluation.md
  contracts/
    report-contract.md
```

## Pack Intent

The pack answers:

> What do I hold, how is it allocated, and what changed over the selected period?

## Playbook

`portfolio-snapshot` is the user-intent workflow.

It requires:

- Input discovery
- Period confirmation
- Holdings source validation

It uses:

- `summarize-holdings` as a local Agent Skill
- `classify-liquidity` as a local Agent Skill
- An optional external market-context skill

It can activate:

- `coaching-evaluation` overlay when the user asks for evaluation

## Local Skill Example

```text
skills/summarize-holdings/SKILL.md
```

```markdown
---
name: summarize-holdings
description: Summarize portfolio holdings, weights, and major concentration points from broker position data.
---

Read the provided holdings table.
Calculate position weights when market values are available.
Group holdings by the selected rollup lens.
Return a concise holdings summary and a structured weights table.
```

## Playbook Manifest Sketch

```yaml
appVersion: "0.1"
kind: playbook
id: portfolio-snapshot
packId: trading-coach-mini
version: "0.1.0"
description: Summarize portfolio holdings and optional coaching evaluation.

inputs:
  evaluation:
    type: boolean
    default: false
  analysisPeriod:
    type: dateRange

requires:
  - workflow: workflows/input-discovery
  - workflow: workflows/period-confirmation

uses:
  - skill: ../../skills/summarize-holdings
  - skill: ../../skills/classify-liquidity
  - skillRef:
      type: registry
      uri: agentskills:market-context
      version: "1.0.0"
      optional: true

overlays:
  - id: coaching-evaluation
    kind: evaluation
    when: evaluation == true

outputs:
  primary:
    type: report
    pathTemplate: reports/{timestamp}-PortfolioSnapshot/Report.md
```

## What This Demonstrates

- APP owns playbook composition.
- Agent Skills own granular skill instructions.
- Overlays add optional product behavior.
- Workflows handle shared lifecycle gates.
- Contracts define output and persistence rules.
