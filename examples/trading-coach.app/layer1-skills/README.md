# Skills

Layer 1 reusable expert work units. **Each directory is a true [agentskills.io](https://agentskills.io/specification) Agent Skill.**

Framework baseline: [`docs/app-skills.md`](../../../docs/app-skills.md) in the AgentPlaybookPack standards repo.

## Directory shape

```text
layer1-skills/<skill-id>/
  SKILL.md
  scripts/run.py       # skill entrypoint (agentskills.io)
  scripts/README.md
  references/README.md
assets/tc-lib/         # shared Python helpers (pack instance)
```

Every skill includes `scripts/run.py`. See [`docs/app-skills.md`](../../../docs/app-skills.md).

Regenerate after skill logic changes: `python tools/materialize-skill-scripts.py` (workbench).

## Portfolio domain

| Skill | Legacy kind |
| --- | --- |
| `holdings-standards-map` | transform |
| `theme-map-inference` | transform |
| `thesis-registry-inference` | transform |
| `period-weight-reconstruction` | analyze |
| `portfolio-holdings-state` | transform |
| `portfolio-weights-table` | synthesize |
| `thesis-health` | analyze |
| `portfolio-period-flows` | analyze |
| `portfolio-evolution` | analyze |
| `portfolio-liquidity-analysis` | synthesize |
| `portfolio-concentration-resilience` | analyze |
| `market-environment` | retrieve |

## Interact

| Skill | Legacy kind |
| --- | --- |
| `holdings-map-confirmation` | interact |
| `theme-map-confirmation` | interact |
| `thesis-registry-confirmation` | interact |
| `evaluation-entry-interview` | interact |
| `exit-interview` | interact |

## Trading domain

| Skill | Legacy kind |
| --- | --- |
| `trading-activity-analysis` | analyze |
| `symbol-trading-analysis` | analyze |
| `stale-position-hygiene` | validate |
| `event-trade-context` | retrieve |

## Data domain

| Skill | Legacy kind |
| --- | --- |
| `datastore-inventory` | retrieve |
| `source-profile-insights` | synthesize |
