---
description: Operator decision guide for choosing the right segment operation — reset, reload, refresh, rebalance, force commit, or a Minion repair task.
---

# Segment Lifecycle and Repair

Pinot exposes several segment-level operations that serve different purposes. This page helps operators decide which operation to use for a given scenario, and links to the detailed reference pages for each one.

## Decision guide

Use the table below to match your situation to the right operation. The sections that follow explain each operation in more detail.

| Situation | Operation | Scope |
|---|---|---|
| A segment is stuck in ERROR state | [Reset](#reset-a-segment) | Single segment or all error segments on a table |
| You changed the table config or schema and want indexes or column metadata updated on existing segments | [Reload](#reload-a-segment) | All segments on a table, or a single segment |
| You need segments fully rebuilt with new indexes, added columns, or compatible data-type changes | [RefreshSegmentTask](#refresh-segments-with-a-minion-task) | Automated via Minion; targets stale segments |
| Segments are unevenly distributed after adding or removing servers | [Rebalance](#rebalance-segments) | Entire table |
| A consuming segment is buffering stale data after a schema change, or you need to prep a real-time table for rebalance | [Force commit](#force-commit-consuming-segments) | All or selected consuming segments on a table |
| You need to delete specific records for compliance or data-quality reasons | [PurgeTask](#purge-records-from-segments) | Automated via Minion; processes eligible segments |
| You need to roll back a bad offline data push | [Consistent push rollback](#roll-back-a-bad-data-push) | Table-level lineage revert |
| You want to compact or aggregate old real-time segments into offline segments | [MergeRollupTask / RealtimeToOfflineSegmentsTask](#compact-and-convert-segments) | Automated via Minion |

## Reset a segment
**What it does.** Resets a segment by transitioning it through the OFFLINE state in the Helix state machine and back to ONLINE (for offline segments) or CONSUMING (for real-time segments). This forces the server to reinitialize the segment without deleting its data.

**When to use it.** Use reset when a segment is in ERROR state — for example, because a consumer threw an unrecoverable exception or a segment download failed during a state transition.

**API.**

```
# Reset a single segment
POST /segments/{tableNameWithType}/{segmentName}/reset

# Reset all error segments on a table
POST /segments/{tableNameWithType}/reset?errorSegmentsOnly=true
```

**UI.** The Pinot Data Explorer table detail screen includes a **Reset Segment** action. You can also filter segments by the ERROR state to find candidates quickly.

{% hint style="warning" %}
Reset does **not** re-download or rebuild the segment. If the underlying segment data on the server is corrupted, follow up with a [reload](#reload-a-segment) using `forceDownload=true`.
{% endhint %}

## Reload a segment

**What it does.** Sends a message to every server hosting the segment, asking it to re-read the segment from local disk (or from deep store when `forceDownload=true`) and rebuild in-memory structures such as indexes and metadata. The operation is asynchronous and returns a job ID for status tracking.
**When to use it.** Reload is the standard response to table-config or schema changes that affect how a segment is served — for example, after adding an inverted index column or changing a default null value. It is lighter than a full segment rebuild because the server re-processes the existing segment file rather than regenerating it from raw data.

**API.**

```
# Reload all segments on an offline table
POST /segments/{tableName}/reload?type=OFFLINE

# Reload a single segment
POST /segments/{tableName}/{segmentName}/reload

# Force re-download immutable segments from deep store before reloading
POST /segments/{tableName}/reload?type=OFFLINE&forceDownload=true

# Poll job status
GET /segments/segmentReloadStatus/{jobId}
```

`targetInstance` is available on both reload endpoints when you want to reload only one server's copy. `instanceToSegmentsMap` is also available on the table-level endpoint when you need to reload a specific set of segments on specific servers.

**UI.** The Cluster Manager offers **Reload All Segments** at the table level and **Reload Segment** at the individual segment level.

For a step-by-step walkthrough, see [Reload a Table Segment](segment-reload.md).

{% hint style="info" %}
Reload applies config changes to the segment's existing data. If you need the segment rebuilt with new columns or compatible data-type changes applied to every record, use [RefreshSegmentTask](#refresh-segments-with-a-minion-task) instead.
{% endhint %}

## Refresh segments with a Minion task
**What it does.** The RefreshSegmentTask is a Minion task that detects segments whose last-refresh timestamp is older than the table config or schema modification time. For each stale segment it downloads the data, regenerates the segment from scratch using the current config and schema, and uploads the result.

**When to use it.** Use RefreshSegmentTask when you need structural changes applied that reload alone cannot handle — for example, adding a column that must be back-filled with default values across all records, removing an index that should no longer be stored on disk, or changing a column to a compatible data type.

**How to enable it.** Add the task to your table config and optionally schedule it with a cron expression:

```json
{
  "task": {
    "taskTypeConfigsMap": {
      "RefreshSegmentTask": {
        "tableMaxNumTasks": "10",
        "schedule": "0 0 3 * * ?"
      }
    }
  }
}
```

You can also trigger it manually:

```
POST /tasks/schedule?taskType=RefreshSegmentTask&tableName=myTable_OFFLINE
```

For full configuration details, see [RefreshSegmentTask](refresh-segment-task.md).
### Reload vs. RefreshSegmentTask

| Aspect | Reload | RefreshSegmentTask |
|---|---|---|
| Runs on | Server (in-place) | Minion (downloads, rebuilds, uploads) |
| Adds new indexes | Yes | Yes |
| Back-fills new columns with default values across all records | No — adds the column to metadata only | Yes — rewrites every record |
| Changes column data types | No | Yes (compatible types) |
| Requires Minion | No | Yes |
| Typical latency | Seconds to minutes | Minutes to hours, depending on segment size |

## Rebalance segments

**What it does.** Recalculates the ideal segment-to-server assignment for a table and moves segments to match. By default the operation runs in no-downtime mode, keeping at least one replica available while segments are migrated.

**When to use it.** Rebalance after any capacity change — adding or removing servers, tagging or untagging servers from a tenant, or changing the replication factor. Also use it when segment placement has drifted from the configured assignment strategy.

**API.**

```
POST /tables/{tableName}/rebalance?type=OFFLINE
POST /tables/{tableName}/rebalance?type=REALTIME
```

Key parameters:

- `dryRun=true` — preview the plan without making changes.
- `downtime=true` — skip no-downtime safety checks for faster execution.
- `includeConsuming=true` — include consuming segments (real-time tables).
- `bootstrap=true` — ignore current assignment and reassign from scratch.
For full details, see [Rebalance](rebalance/README.md).

{% hint style="info" %}
For real-time tables, consider running a [force commit](#force-commit-consuming-segments) before rebalance so that consuming segments are converted to completed segments first.
{% endhint %}

## Force commit consuming segments

**What it does.** Forces all (or selected) consuming segments on a real-time table to seal and commit as completed segments, then restarts consumption from the stream at the current offset. The operation is asynchronous and returns a job ID.

**When to use it.** Use force commit in two main scenarios:

1. **After a schema or table-config change on a real-time table.** Consuming segments were built with the old config. Force-committing them and allowing fresh consuming segments to start ensures new data is ingested under the updated schema.
2. **Before a rebalance of a real-time table.** Rebalance works on completed segments. Force commit converts consuming segments so they are included in the rebalance plan.

**API.**

```
POST /tables/{tableName}/forceCommit
```

Optional query parameters: `partitions`, `segments`, `batchSize`.

## Purge records from segments

**What it does.** The PurgeTask is a Minion task that iterates over records in eligible segments, applies custom `RecordPurger` or `RecordModifier` logic, and generates replacement segments with the matching records removed or modified.

**When to use it.** Use PurgeTask for compliance-driven deletion (for example, GDPR right-to-erasure requests), data-quality cleanup, or removing records that match specific business rules. Because purge requires custom plugin code, it is not a generic "delete rows by query" operation.
For configuration and scheduling details, see [PurgeTask](purge-task.md).

## Roll back a bad data push

**What it does.** The consistent push and rollback protocol uses segment lineage entries in ZooKeeper to track which segments replaced which. When a push is in COMPLETED state, the broker routes queries to the new segments. Reverting a lineage entry switches routing back to the original segments atomically.

**When to use it.** Use this when a batch ingestion job has pushed incorrect data to an OFFLINE REFRESH table and you need to revert to the previous snapshot without re-running the full ingestion pipeline.

**Steps.**

1. List lineage entries: `GET /lineage/{tableName}`.
2. Identify the entry ID for the bad push.
3. Revert: `POST /segments/{tableName}/revertReplaceSegments?lineageEntryId={id}`.
4. Verify the entry state is REVERTED.

For setup and detailed instructions, see [Consistent Push and Rollback](consistent-push-and-rollback.md).

## Compact and convert segments

Two Minion tasks handle long-term segment hygiene:

- **MergeRollupTask** merges small segments and optionally aggregates (rolls up) metric columns. It supports multiple merge levels (for example, hourly into daily, daily into monthly) and tracks progress with a watermark. See [Minion Merge Rollup Task](minion-merge-rollup-task.md).
- **RealtimeToOfflineSegmentsTask** converts completed real-time segments into optimized offline segments, optionally filtering by time window and aggregating data. See [Pinot Managed Offline Flows](pinot-managed-offline-flows.md).

Both tasks are configured in the table's `taskTypeConfigsMap` and run automatically on a schedule or on demand via `POST /tasks/schedule?taskType={taskType}`.
## Common multi-step workflows

### Apply a new index to an existing offline table

1. Update the table config to include the new index column.
2. Run `POST /segments/{tableName}/reload` to rebuild indexes in-place on every server.
3. Monitor reload job status via `GET /segments/segmentReloadStatus/{jobId}`.

If the table has RefreshSegmentTask enabled, the task will also detect the config change and rebuild stale segments on its next run.

### Add a column to a real-time table

1. Update the schema with the new column and its default value.
2. Force commit consuming segments: `POST /tables/{tableName}/forceCommit`.
3. New consuming segments will pick up the column automatically.
4. For completed segments, either reload (adds column metadata only) or let RefreshSegmentTask rebuild them with back-filled defaults.

### Recover a table with segments in ERROR state

1. Open the Pinot Data Explorer and filter segments by the ERROR state to identify affected segments.
2. Check server logs for the root cause (download failure, corrupt segment, consumer exception).
3. If the segment data on the server is intact, reset the segment:
   `POST /segments/{tableNameWithType}/{segmentName}/reset`
4. If the segment data is corrupt or missing, reload with a forced deep-store download:
   `POST /segments/{tableName}/{segmentName}/reload?forceDownload=true`
5. If the segment is still in ERROR after reload, check that the segment exists in deep store and that the server has connectivity and disk space.

### Scale out servers and rebalance

1. Add the new servers and tag them to the appropriate tenant.
2. (Real-time tables) Force commit consuming segments.
3. Run a dry-run rebalance to preview the plan:
   `POST /tables/{tableName}/rebalance?type=OFFLINE&dryRun=true`
4. Execute the rebalance:
   `POST /tables/{tableName}/rebalance?type=OFFLINE`
5. Monitor rebalance status via `GET /tables/{tableName}/rebalance/status/{jobId}`.
