---
name: evaluation-entry-interview
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: evaluation-entry-interview
metadata:
  legacyCapabilityKind: interact
  sourcePath: capabilities/evaluation-entry-interview
  sourceRepository: trading-coach
---

1. Run only after Input Discovery, map confirmation (when applicable), and factual market context for the playbook
2. Ask targeted questions per active overlay (portfolio evaluation, rebalancing, risk, trade lifecycle, etc.)
3. Preserve complete Q&A verbatim
4. Store in `Interview.md` and embed in `Report.md` Appendix A
5. After completion say: `Interview complete. Generating report.`

Portfolio-specific themes when `aggregate-state-review`: see [overlays/portfolio-evaluation.md](../playbooks/aggregate-state-review/overlays/portfolio-evaluation.md).

## Scripts

Run from this skill directory. Paths are relative to the skill root per [agentskills.io](https://agentskills.io/specification).

| Script | Purpose |
| --- | --- |
| `scripts/run.py` | Execute skill logic; writes workspace artifacts and `skill-result.json` |

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE" --evaluation true
```

Set `compatibility: Requires Python 3.11+` when the runtime must execute bundled scripts.

## Outputs

- `Interview.md`
- Gate: `entry-interview-complete`

## Used by

- Evaluation overlays on portfolio, trade, and activity playbooks