---
description: Evolve Pinot schemas safely by adding columns, reloading segments, and deciding when a new table is the cleaner path.
---

# Schema Evolution

Pinot schema evolution is intentionally narrow. The safe path is to add columns, reload the affected segments, and backfill only when the table type and data flow support it. If the change is more invasive than that, create a new table instead of forcing the old one to stretch.

## What is safe

Additive schema changes are the normal path. New columns can be introduced without rewriting the whole table, as long as the ingestion flow and segment reload behavior are understood.

## What is not safe

Renaming a column, dropping a column, or changing a column type is not a small schema tweak. Treat those as table redesign work.

## Typical flow

1. Add the new column to the schema (with an appropriate `defaultNullValue` when older rows should show a default).
2. Update the table config or ingestion config if the new field needs transforms, indexes, or upsert strategy entries.
3. Ensure **new consuming segments** start with the updated schema. For an explicit barrier, call [forceCommit](../../reference/api-reference/controller-api.md#post-tablestablenameforcecommit) and poll its status; for transform changes, prefer the pause procedure below.
4. Reload completed segments after that boundary so the segments committed under the old plan also expose the new column metadata (filled with `defaultNullValue` unless you backfill).
5. Backfill historical data if the use case needs real values instead of defaults (offline / hybrid path).

## Realtime consuming segments: when to pause, reload, or force commit

Older docs sometimes said “always pause consumption when adding a column.” That is stronger than necessary. Consuming segments are built with the schema and table config that were current when the mutable segment started. Rows already indexed in that mutable segment are not rewritten in place when you change the schema. The practical goal is:

* **Completed (immutable) segments** — reload so the new column appears (typically as `defaultNullValue`).
* **In-flight consuming segments** — commit them and start new consumers that load the latest schema/config.
* **Transforms / derived columns** — stop the old consumer from continuing with the transform plan it loaded when the mutable segment started.

Server reload of a consuming segment **requests a force commit** when `pinot.server.instance.reload.consumingSegment` is `true` (the default). The consumer seals asynchronously and a replacement consumer then starts with the latest schema and table config. Reload job completion is not a hard barrier that new consumers are already ONLINE. For an explicit barrier, call `POST /tables/{tableName}/forceCommit` and poll status; see the [force commit API](../../reference/api-reference/controller-api.md#post-tablestablenameforcecommit).

### Decision table (add a column on an existing table)

| Table situation | Risk if you only update schema and wait | Recommended steps |
| --- | --- | --- |
| **OFFLINE only** | None for stream consumers | Update schema → [reload segments](../../operate-pinot/segment-reload.md) → backfill/repush if you need non-default values. |
| **Realtime, plain column** (present in the stream or filled only via `defaultNullValue`; no new transform) | Current consuming segment keeps the old schema until it commits; queries on that mutable segment may omit the column or use a virtual default | 1) Update schema 2) `POST /segments/{table}/reload` (consuming reload requests a force commit when enabled) **or** `POST /tables/{table}/forceCommit` and poll it 3) Reload completed segments when they need physical column metadata or new indexes 4) Optional offline backfill for history |
| **Realtime with ingestion transforms** (new column populated by `transformConfigs` / Groovy / built-ins, or transform logic changes) | High: the active consumer keeps using its old transform plan, so the segment can contain incorrect or missing derived values | 1) Prefer **pause and wait for completion** → apply schema + table config → reload completed segments → **resume** (clean boundary), **or** 2) apply schema/config → **forceCommit and poll** → reload the segments committed under the old plan 3) Do not assume rows already indexed by the old consumer are repaired in place |
| **Realtime full upsert** | Same consumer-boundary issue as plain RT for an additive column; standard full-upsert metadata remains valid across a normal force commit | Follow the plain-RT steps for an additive schema change. Do **not** treat restart as a migration path for immutable upsert settings such as mode, primary/comparison columns, hash function, or delete/out-of-order fields; create a new table and reingest instead. |
| **Realtime partial upsert** | Same column/transform issues as above, plus force commit / reload-consuming is **blocked or skipped** in the default `RESTRICTED` mode because replicas can diverge on winner selection | 1) Update the additive schema/config 2) Before pause, force commit, or reload-consuming, set Helix **cluster config** `pinot.server.consuming.segment.consistency.mode=PROTECTED` (via controller cluster configs — not `pinot-server.conf`; see [Consuming Segment Consistency Mode](../ingestion/upsert-and-dedup/upsert.md#consuming-segment-consistency-mode)) 3) Use a maintenance window and verify upsert results 4) Allowed `partialUpsertStrategies` / `defaultPartialUpsertStrategy` changes require a controlled server restart and are not retroactive 5) Immutable core upsert settings require a new table and reingestion |
| **Hybrid (OFFLINE + REALTIME)** | Offline and realtime can disagree until both sides are updated | Evolve schema once → reload offline segments (and backfill) → treat the realtime side with the matching row in this table |

### Why incorrect values can appear

* A **consuming** segment’s mutable index is created with a fixed schema/transform pipeline at start. Adding a column or transform mid-segment does not retroactively recompute earlier rows in that mutable segment.
* **Completed** segments only gain the new column through reload (defaults) or rebuild/backfill (real values).
* **Upsert / dedup** keep cross-segment state inside the server table data manager. Allowed partial-upsert strategy changes require a controlled server restart and are not retroactive. Core upsert/dedup identity and ordering settings are immutable; use a new table and reingest instead of relying on restart.

### Minimal realtime runbook (additive column)

For a plain additive column:

```bash
# 1) Upload updated schema
curl -F schemaName=@myTable.schema http://localhost:9000/schemas

# 2) If transforms/indexes changed, PATCH/PUT the table config as well

# 3) For an explicit consumer barrier, force commit and poll
curl -X POST "http://localhost:9000/tables/myTable/forceCommit"
curl -X GET  "http://localhost:9000/tables/forceCommitStatus/<forceCommitJobId>"
# wait until numberOfSegmentsYetToBeCommitted == 0

# 4) If physical metadata/indexes are required, reload the completed segments.
# Use segment-specific reloads to avoid force-committing the replacement consumer.
curl -X POST "http://localhost:9000/segments/myTable/<committedSegmentName>/reload"
```

For a transform change, use a clean pause boundary:

```bash
# 1) Pause; pauseConsumption force-commits the current consumers
curl -X POST "http://localhost:9000/tables/myTable/pauseConsumption"
curl -X GET  "http://localhost:9000/tables/myTable/pauseStatus"
# wait until the consuming segments have committed

# 2) Upload the schema and table config

# 3) Reload completed segments while the table is paused
curl -X POST "http://localhost:9000/segments/myTable/reload?type=REALTIME"

# 4) Resume with consumers built from the new schema/config
curl -X POST "http://localhost:9000/tables/myTable/resumeConsumption"
```

## Reference material

Step-by-step offline quickstart walkthrough: [Schema Evolution tutorial](../../tutorials/data-ingestion/schema-evolution.md).

Operational APIs: [Segment reload](../../operate-pinot/segment-reload.md), [Force commit](../../reference/api-reference/controller-api.md#post-tablestablenameforcecommit), [Pause stream ingestion](../ingestion/stream-ingestion/README.md#pause-stream-ingestion).

## What this page covered

- The additive schema-evolution path and the cases where a new table is safer.
- When pause, reload, and forceCommit are required for realtime consumers.
- Upsert-specific limits (config changes vs schema adds).

## Next step

Read the ingestion pages to see how schema design affects batch and stream pipelines.

## Related pages

- [Data Modeling](README.md)
- [Schema and Table Shape](schema.md)
- [Logical Tables](logical-tables.md)
- [Ingestion transformations](../ingestion/ingestion-level-transformations.md)
- [Upsert](../ingestion/upsert-and-dedup/upsert.md)
- [Original Schema Evolution Tutorial](../../tutorials/data-ingestion/schema-evolution.md)
