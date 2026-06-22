---
name: stale-position-hygiene
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: stale-position-hygiene
metadata:
  legacyCapabilityKind: validate
  sourcePath: capabilities/stale-position-hygiene
  sourceRepository: trading-coach
---

1. Establish hold duration, drawdown from peak, thesis drift vs original entry rationale
2. Compare position size to portfolio context when holdings data exists
3. Document stale-risk rules (max age, max drawdown, thesis refresh triggers)
4. Quantification: factual timeline and metrics only
5. Evaluation overlay: judgment on whether hold vs exit was sound

## Scripts

Run from this skill directory. Paths are relative to the skill root per [agentskills.io](https://agentskills.io/specification).

| Script | Purpose |
| --- | --- |
| `scripts/run.py` | Execute skill logic; writes workspace artifacts and `skill-result.json` |

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE" --symbol SYMBOL
```

Set `compatibility: Requires Python 3.11+` when the runtime must execute bundled scripts.

## Used by

- `layer3-playbooks/unit-decision-review`