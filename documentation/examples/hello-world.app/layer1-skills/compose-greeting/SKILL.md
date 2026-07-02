---
name: compose-greeting
description: Compose the core Hello World greeting for a named recipient. Use during hello-world playbook core output phase.
compatibility: Requires Python 3.11+ when running bundled scripts
outputCompleteness: complete
metadata:
  packId: hello-world
  layer: '1'
---

## Procedure

1. Read resolved playbook input `recipient` (default `World`)
2. Run `scripts/run.py` with `--recipient`, `--datastore`, and `--workspace` pointing at the active ephemeral workspace for this run (see APP `app-execution.md`)
3. Read `greeting.txt` and `skill-result.json` from the workspace run directory; use `skill-result.json` to verify `recipient` and `greeting` before report assembly
4. Use the greeting text as the core **Greeting** section in `Report.md` (report assembly is agent responsibility)

## Scripts

| Script | Purpose |
| --- | --- |
| `scripts/run.py` | Write `greeting.txt` and `skill-result.json` to the agent workspace |

```bash
python scripts/run.py --recipient "$RECIPIENT" --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE"
```

```powershell
python scripts/run.py --recipient $env:RECIPIENT --datastore $env:USER_DATASTORE --workspace $env:AGENT_WORKSPACE
```

Pass `--workspace` as the active ephemeral directory for this run (execution agent chooses when `{agentWorkspace}` is not supplied). Pass `--datastore` as the bound `{userDatastore}` even when the script does not read it.

## References

- `references/greeting-format.md` — greeting text conventions

## Outputs

- `{agentWorkspace}/greeting.txt` — single-line greeting (used in report **Greeting** section)
- `{agentWorkspace}/skill-result.json` — structured skill result for workspace verification before report assembly

## Used by

- `layer3-playbooks/hello-world`
