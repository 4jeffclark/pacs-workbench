# Future Pack Store

## Purpose

A Pack Store would help agents and humans discover, evaluate, install, and trust AgentPlaybookPacks.

The store is not required for the APP framework, but it gives the ecosystem a plausible distribution path.

## What A Pack Store Could Provide

- Pack discovery by domain, task, runtime compatibility, and license
- Version metadata and changelogs
- Dependency listing for skills, tools, schemas, and external references
- Trust signals such as publisher identity, signatures, audits, and usage
- Compatibility metadata for runtimes such as Cursor, VS Code, OpenClaw, and custom agents
- Validation results against APP schema and Agent Skills compatibility
- Examples, screenshots, report samples, and test fixtures

## Package Metadata

A store listing should be derivable from the pack manifest.

Minimum listing fields:

```yaml
packId: trading-coach
name: TradingCoach
description: Structured trading performance reviews and debriefs.
publisher: 4jeffclark
version: 1.0.0
license: TBD
domains:
  - investing
  - trading
playbooks:
  - aggregate-state-review
  - environment-review
skills:
  local: 12
  external: 3
compatibility:
  agentSkills: ">=1.0"
  appManifest: "0.1"
```

## Install Models

Potential install models:

- Git clone or submodule
- Archive download
- Registry package
- Runtime-managed install
- Workspace-local pack reference

## Trust Model

The store should distinguish:

- Pack source trust
- Skill dependency trust
- Tool permission risk
- Data access risk
- Network access risk
- Generated artifact risk

APP should describe the risks. Runtimes should enforce policy.

## Validation

A Pack Store validator could check:

- Required pack manifest fields
- Playbook manifest schema
- Agent Skills folder validity
- Broken local references
- Unpinned external references
- Missing licenses
- Missing compatibility notes
- Dangerous tool or script declarations

## Open Questions

- Is the Pack Store a central registry, an index over Git repos, or both?
- Should it host packs or only point to them?
- Should it validate external Agent Skill references transitively?
- Should it support private enterprise catalogs?
- Should store metadata live entirely in the pack manifest or in a separate listing file?
