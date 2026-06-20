# TFY Simulator

Local development harness for previewing how TeamFoundry would ingest an APP pack, assemble assistant context, and translate the result into target engine deployable artifacts.

This tool is part of the TeamFoundry stack realignment program. Design lives in `docs/tfy-stack-realignment/tfy-design.md`.

## Status

Not implemented yet. This directory is reserved for the simulator scaffold and preview output.

## Intended Usage

```text
Input:
  APP pack path
  playbook id
  mock assistant profile
  mock customer context
  engine profile (default: openclaw)

Output:
  tools/tfy-simulator/output/assistant-construction-plan.md
  tools/tfy-simulator/output/translation-manifest.json
  tools/tfy-simulator/output/engine-preview/
  tools/tfy-simulator/output/warnings.txt
```

## Rules

- Do not treat this harness as TeamFoundry or OpenClaw.
- Do not require edits to `teamfoundry.ai` to run previews.
- Do not treat preview artifacts as production deployables.
