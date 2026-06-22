---
name: market-environment
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: market-environment
metadata:
  legacyCapabilityKind: retrieve
  sourcePath: capabilities/market-environment
  sourceRepository: trading-coach
---

1. Broad regime narrative across confirmed windows
2. When embedded in portfolio playbook: summary suitable for Report market sections
3. When standalone: full `environment-review` playbook depth
4. Write a working copy to `MarketResearch.md` for agents and tooling
5. **Embed full source citations in `Report.md` Appendix C** — title, publisher, date, URL or sufficient locator. Appendix C must be self-contained; do **not** end with a pointer to `MarketResearch.md`.
6. Body sections may summarize context; Appendix C holds the complete citation list.

When `evaluation: false`, describe context without coaching judgments.

## Scripts

Run from this skill directory. Paths are relative to the skill root per [agentskills.io](https://agentskills.io/specification).

| Script | Purpose |
| --- | --- |
| `scripts/run.py` | Execute skill logic; writes workspace artifacts and `skill-result.json` |

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE" --period-start YYYYMMDD --period-end YYYYMMDD
```

Set `compatibility: Requires Python 3.11+` when the runtime must execute bundled scripts.

## Outputs

- `MarketResearch.md`
- Report market context sections

## Used by

- `layer3-playbooks/aggregate-state-review` (embeds)
- `layer3-playbooks/environment-review` (full)
- `layer3-playbooks/unit-decision-review` (optional)