# Scripts

| Script | Purpose |
| --- | --- |
| `run.py` | Execute this skill; writes artifacts under `--workspace` and `skill-result.json` |

Requires **Python 3.11+** (stdlib only). Shared library: `../../assets/tc-lib/`.

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE" --input-dir "$AGENT_WORKSPACE/thesis-registry-inference"
```
