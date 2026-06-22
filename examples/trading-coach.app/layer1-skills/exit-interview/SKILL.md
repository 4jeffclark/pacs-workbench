---
name: exit-interview
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: exit-interview
metadata:
  legacyCapabilityKind: interact
  sourcePath: capabilities/exit-interview
  sourceRepository: trading-coach
---

1. Ask concise exit interview questions per playbook overlay
2. Store responses in `ExitInterview.md`
3. Embed verbatim in `Report.md` Appendix E
4. Generate PDFs when available after integration

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

- `ExitInterview.md`

## Used by

- Evaluation overlays