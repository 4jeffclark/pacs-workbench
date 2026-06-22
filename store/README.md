# APP Pack Store

Home for Pack Store design in the [AgentPlaybookPack](https://github.com/4jeffclark/agent-playbook-pack) standards repo.

A Pack Store indexes AgentPlaybookPacks and helps runtimes and humans discover, evaluate, install, and trust domain workflow packages.

## Standards

Full store design: [`../docs/pack-store.md`](../docs/pack-store.md)

Related APP standards:

| Topic | Location |
| --- | --- |
| Pack shape and layers | [`../docs/framework.md`](../docs/framework.md) |
| Instance layout | [`../docs/app-execution.md`](../docs/app-execution.md) |
| Manifest fields | [`../schema/app-manifest-v0.1.md`](../schema/app-manifest-v0.1.md) |
| Reference distribution repo | [`../examples/`](../examples/) |

## What A Store Answers

- What packs are available?
- Which playbooks do they provide?
- Which Agent Skills do they depend on?
- Which tools or permissions do they require?
- Who published them?
- Which versions are trusted or validated?
- Are they compatible with this runtime?

The store complements Agent Skills hubs by indexing higher-level playbook packs and their dependencies.

## Planned Contents

```text
store/
  README.md                 # this file
  examples/
    trading-coach.listing.yaml   # future: derived from pack manifest
  listing.schema.json       # future
  trust-model.md            # future
  validation-rules.md       # future
```

Listings should be derivable from `pack.app.yaml` plus publisher metadata. See [`pack-store.md`](../docs/pack-store.md) for draft listing fields.

## Status

Design draft only. No registry, validator, or hosted listings yet. Reference pack: [`../examples/trading-coach.app/`](../examples/trading-coach.app/).
