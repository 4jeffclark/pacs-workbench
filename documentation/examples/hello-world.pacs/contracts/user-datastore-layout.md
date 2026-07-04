# Hello World User Datastore Layout

Bind `userDatastore` to a host directory. Use this structure beneath it:

```text
{userDatastore}/
  reports/    # immutable report output folders
  inputs/     # optional user seed files (not required for hello-world)
```

Report folders are append-only. Do not overwrite an existing report folder.
