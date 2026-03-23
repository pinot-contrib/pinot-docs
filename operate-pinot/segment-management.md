---
description: Assign, distribute, maintain, compact, and repair segments across your Pinot cluster.
---

# Segment Management

## Purpose

Segments are the fundamental storage and query unit in Apache Pinot. Every table is divided into segments, and how those segments are assigned to servers, maintained over time, and compacted directly affects query performance, storage cost, and operational resilience. This section covers the full segment lifecycle -- from initial assignment through ongoing maintenance tasks.

## Segment assignment and placement

Decide how segments land on servers and how servers are selected for a table.

| Page | What it covers |
|---|---|
| [Segment Assignment](../operators/operating-pinot/segment-assignment.md) | Balanced, replica-group, and partitioned replica-group assignment strategies |
| [Instance Assignment](../operators/operating-pinot/instance-assignment.md) | Tag-based isolation, replica-group instance partitioning, pool-based assignment, and mirroring across tables |

## Segment lifecycle and repair

Understand the operations available when segments need to be reset, reloaded, refreshed, or repaired.

| Page | What it covers |
|---|---|
| [Segment Lifecycle and Repair](../operators/operating-pinot/segment-lifecycle-and-repair.md) | Decision guide for choosing between reset, reload, refresh, rebalance, force commit, purge, and rollback |
| [Reload a Table Segment](../tutorials/operations/segment-reload.md) | Step-by-step instructions for reloading segments via the Controller API or Admin Console |

## Rebalance

Redistribute segments after capacity changes, config updates, or tenant modifications.

| Page | What it covers |
|---|---|
| [Rebalance overview](../operators/operating-pinot/rebalance/) | When and why to rebalance -- servers, brokers, and tenants |
| [Rebalance Servers](../operators/operating-pinot/rebalance/rebalance-servers/) | Server rebalance API, parameters, and operational guidance |
| [Rebalance Servers -- Examples and Scenarios](../operators/operating-pinot/rebalance/rebalance-servers/examples-and-scenarios.md) | Worked examples for common rebalance situations |
| [Rebalance Brokers](../operators/operating-pinot/rebalance/rebalance-brokers.md) | Broker rebalance after adding or removing broker instances |
| [Rebalance Tenant](../operators/operating-pinot/rebalance/rebalance-tenant.md) | Rebalance all tables belonging to a tenant after tagging changes |

## Tiered storage

Move older or less-queried data to cheaper storage tiers while keeping recent data on fast disks.

| Page | What it covers |
|---|---|
| [Separating Data Storage by Age](../operators/operating-pinot/separating-data-storage-by-age/) | Overview of tiered storage strategies |
| [Moving Segments Across Tenants](../operators/operating-pinot/separating-data-storage-by-age/moving-segments-across-tenants.md) | Use tag overrides to move completed segments to a different server tier |
| [Using Multiple Directories](../operators/operating-pinot/separating-data-storage-by-age/using-multiple-directories.md) | Configure multiple data directories on a single server to span storage devices |

## Minion tasks for segment maintenance

Automate compaction, merging, purging, and ingestion using Pinot Minion.

| Page | What it covers |
|---|---|
| [Pinot Managed Offline Flows](../operators/operating-pinot/pinot-managed-offline-flows.md) | Automatically move data from real-time tables to offline tables (RealtimeToOfflineSegmentsTask) |
| [Merge Rollup Task](../operators/operating-pinot/minion-merge-rollup-task.md) | Merge small segments into larger time-aligned segments with optional rollup aggregation |
| [Segment Generation and Push Task](../operators/operating-pinot/segment-generation-and-push-task.md) | Batch ingestion via Minion -- read files, build segments, push to the cluster |
| [Refresh Segment Task](../operators/operating-pinot/refresh-segment-task.md) | Automatically rebuild segments when the table config or schema changes |
| [Purge Task](../operators/operating-pinot/purge-task.md) | Remove or modify records for compliance or data-quality reasons |
| [Upsert Compaction Task](../operators/operating-pinot/upsert-compaction-task.md) | Reclaim space by removing invalidated records from upsert-enabled tables |
| [Upsert Compact Merge Task](../operators/operating-pinot/upsert-compact-merge-task.md) | Merge small segments while compacting -- reduces segment count in upsert tables |
| [Upsert Merge Compact Task](../operators/operating-pinot/upsert-merge-compact-task.md) | Alternative merge-compact task for upsert tables |

## Consistent push and rollback

Guarantee atomicity when replacing offline segments and quickly revert a bad data push.

| Page | What it covers |
|---|---|
| [Consistent Push and Rollback](../operators/operating-pinot/consistent-push-and-rollback.md) | Segment lineage protocol for atomic push and one-click rollback of offline table refreshes |

## When to use what

| Goal | Recommended action |
|---|---|
| Newly added servers have no segments | Run a [rebalance](../operators/operating-pinot/rebalance/rebalance-servers/) |
| Segment stuck in ERROR state | [Reset](../operators/operating-pinot/segment-lifecycle-and-repair.md) the segment, then reload if data is corrupt |
| Schema or index config changed | [Reload](../tutorials/operations/segment-reload.md) all segments, or schedule a [RefreshSegmentTask](../operators/operating-pinot/refresh-segment-task.md) for full rebuild |
| Too many small segments | Schedule a [MergeRollupTask](../operators/operating-pinot/minion-merge-rollup-task.md) or [UpsertCompactMergeTask](../operators/operating-pinot/upsert-compact-merge-task.md) |
| Stale records in upsert table wasting space | Schedule an [UpsertCompactionTask](../operators/operating-pinot/upsert-compaction-task.md) |
| Need to delete specific records (GDPR) | Schedule a [PurgeTask](../operators/operating-pinot/purge-task.md) |
| Bad offline push needs rollback | Use [Consistent Push and Rollback](../operators/operating-pinot/consistent-push-and-rollback.md) |
| Recent data needs fast disks, old data can be on HDDs | Configure [tiered storage](../operators/operating-pinot/separating-data-storage-by-age/) |

## Related pages

* [Performance tuning](../operators/operating-pinot/tuning/) -- query routing, scheduling, memory, and real-time tuning
* [Segment Operations Throttling](../tutorials/operations/segment-operations-throttling.md) -- limit parallelism of segment downloads and index rebuilds
* [Production guides](production-guides.md) -- deployment, monitoring, and security for production clusters
