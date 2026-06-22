# Source Profile Playbook

## Playbook Version

1.1.0

## Playbook Id

source-profile

## Playbook Report Id

SourceProfile

## Product Id

trading-coach

## ASP Manifest

[source-profile.asp.yaml](source-profile.asp.yaml)

## Composition

```text
requires:
  - layer0-workflows/datastore-merge-and-validate
  - layer0-workflows/structured-input-discovery
uses:
  - layer1-skills/datastore-inventory
overlays:
  - overlays/source-profile-evaluation.asp.yaml    when evaluation: true
```

No entry interview in either mode. Data clarifications belong to Input Discovery.

## Inputs

```text
source-profile(
  sessionAttachments?: file[],
  dataStore: DataStore,
  evaluation: boolean,
  profileScopeStart: YYYYMMDD,
  profileScopeEnd: YYYYMMDD,
  dataSourceNotes?: text
)
```

## Core Output Phase

`datastore-inventory` — steps 1–5 (inventory through derived quality).

When knowledge tables exist, this playbook should inventory both:

- raw and canonical datastore coverage
- durable knowledge coverage under `{userDatastore}/data/knowledge/`

When `evaluation: false`: `Input Discovery complete. Generating quantification report.`

## Augmented Output Phase

When `evaluation: true`: `source-profile-insights` overlay — recommendations, scorecard, optional developer reflection, exit interview.

## Output Artifacts

```text
{userDatastore}/reports/<GenerationTimestamp>-SourceProfile-<ProfileScopeStart>-<ProfileScopeEnd>/
```

Legacy treatment id `DataStoreProfile` routes here.

## Manifest Metadata

Include `Output Mode`, `Capabilities Executed`, `Overlays Executed` with kinds.
