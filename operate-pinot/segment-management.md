---
description: Assign, distribute, maintain, compact, and repair segments across your Pinot cluster.
---

# Segment Management

## Purpose

Segments are the fundamental storage and query unit in Apache Pinot. Every table is divided into segments, and how those segments are assigned to servers, maintained over time, and compacted directly affects query performance, storage cost, and operational resilience. This section covers the full segment lifecycle -- from initial assignment through ongoing maintenance tasks.

## Segment assignment and placement

Decide how segments land on servers and how servers are selected for a table.

<table>
  <thead>
    <tr>
      <th>Page</th>
      <th>What it covers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Segment Assignment](../operators/operating-pinot/segment-assignment.md)</td>
      <td>Balanced, replica-group, and partitioned replica-group assignment strategies</td>
    </tr>
    <tr>
      <td>[Instance Assignment](../operators/operating-pinot/instance-assignment.md)</td>
      <td>Tag-based isolation, replica-group instance partitioning, pool-based assignment, and mirroring across tables</td>
    </tr>
  </tbody>
</table>

## Segment lifecycle and repair

Understand the operations available when segments need to be reset, reloaded, refreshed, or repaired.

<table>
  <thead>
    <tr>
      <th>Page</th>
      <th>What it covers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Segment Lifecycle and Repair](../operators/operating-pinot/segment-lifecycle-and-repair.md)</td>
      <td>Decision guide for choosing between reset, reload, refresh, rebalance, force commit, purge, and rollback</td>
    </tr>
    <tr>
      <td>[Reload a Table Segment](../tutorials/operations/segment-reload.md)</td>
      <td>Step-by-step instructions for reloading segments via the Controller API or Admin Console</td>
    </tr>
  </tbody>
</table>

## Rebalance

Redistribute segments after capacity changes, config updates, or tenant modifications.

<table>
  <thead>
    <tr>
      <th>Page</th>
      <th>What it covers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Rebalance overview](../operators/operating-pinot/rebalance/)</td>
      <td>When and why to rebalance -- servers, brokers, and tenants</td>
    </tr>
    <tr>
      <td>[Rebalance Servers](../operators/operating-pinot/rebalance/rebalance-servers/)</td>
      <td>Server rebalance API, parameters, and operational guidance</td>
    </tr>
    <tr>
      <td>[Rebalance Servers -- Examples and Scenarios](../operators/operating-pinot/rebalance/rebalance-servers/examples-and-scenarios.md)</td>
      <td>Worked examples for common rebalance situations</td>
    </tr>
    <tr>
      <td>[Rebalance Brokers](../operators/operating-pinot/rebalance/rebalance-brokers.md)</td>
      <td>Broker rebalance after adding or removing broker instances</td>
    </tr>
    <tr>
      <td>[Rebalance Tenant](../operators/operating-pinot/rebalance/rebalance-tenant.md)</td>
      <td>Rebalance all tables belonging to a tenant after tagging changes</td>
    </tr>
  </tbody>
</table>

## Tiered storage

Move older or less-queried data to cheaper storage tiers while keeping recent data on fast disks.

<table>
  <thead>
    <tr>
      <th>Page</th>
      <th>What it covers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Separating Data Storage by Age](../operators/operating-pinot/separating-data-storage-by-age/)</td>
      <td>Overview of tiered storage strategies</td>
    </tr>
    <tr>
      <td>[Moving Segments Across Tenants](../operators/operating-pinot/separating-data-storage-by-age/moving-segments-across-tenants.md)</td>
      <td>Use tag overrides to move completed segments to a different server tier</td>
    </tr>
    <tr>
      <td>[Using Multiple Directories](../operators/operating-pinot/separating-data-storage-by-age/using-multiple-directories.md)</td>
      <td>Configure multiple data directories on a single server to span storage devices</td>
    </tr>
  </tbody>
</table>

## Minion tasks for segment maintenance

Automate compaction, merging, purging, and ingestion using Pinot Minion.

<table>
  <thead>
    <tr>
      <th>Page</th>
      <th>What it covers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Pinot Managed Offline Flows](../operators/operating-pinot/pinot-managed-offline-flows.md)</td>
      <td>Automatically move data from real-time tables to offline tables (RealtimeToOfflineSegmentsTask)</td>
    </tr>
    <tr>
      <td>[Merge Rollup Task](../operators/operating-pinot/minion-merge-rollup-task.md)</td>
      <td>Merge small segments into larger time-aligned segments with optional rollup aggregation</td>
    </tr>
    <tr>
      <td>[Segment Generation and Push Task](../operators/operating-pinot/segment-generation-and-push-task.md)</td>
      <td>Batch ingestion via Minion -- read files, build segments, push to the cluster</td>
    </tr>
    <tr>
      <td>[Refresh Segment Task](../operators/operating-pinot/refresh-segment-task.md)</td>
      <td>Automatically rebuild segments when the table config or schema changes</td>
    </tr>
    <tr>
      <td>[Purge Task](../operators/operating-pinot/purge-task.md)</td>
      <td>Remove or modify records for compliance or data-quality reasons</td>
    </tr>
    <tr>
      <td>[Upsert Compaction Task](../operators/operating-pinot/upsert-compaction-task.md)</td>
      <td>Reclaim space by removing invalidated records from upsert-enabled tables</td>
    </tr>
    <tr>
      <td>[Upsert Compact Merge Task](../operators/operating-pinot/upsert-compact-merge-task.md)</td>
      <td>Merge small segments while compacting -- reduces segment count in upsert tables</td>
    </tr>
    <tr>
      <td>[Upsert Merge Compact Task](../operators/operating-pinot/upsert-merge-compact-task.md)</td>
      <td>Alternative merge-compact task for upsert tables</td>
    </tr>
  </tbody>
</table>

## Consistent push and rollback

Guarantee atomicity when replacing offline segments and quickly revert a bad data push.

<table>
  <thead>
    <tr>
      <th>Page</th>
      <th>What it covers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Consistent Push and Rollback](../operators/operating-pinot/consistent-push-and-rollback.md)</td>
      <td>Segment lineage protocol for atomic push and one-click rollback of offline table refreshes</td>
    </tr>
  </tbody>
</table>

## When to use what

<table>
  <thead>
    <tr>
      <th>Goal</th>
      <th>Recommended action</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Newly added servers have no segments</td>
      <td>Run a [rebalance](../operators/operating-pinot/rebalance/rebalance-servers/)</td>
    </tr>
    <tr>
      <td>Segment stuck in ERROR state</td>
      <td>[Reset](../operators/operating-pinot/segment-lifecycle-and-repair.md) the segment, then reload if data is corrupt</td>
    </tr>
    <tr>
      <td>Schema or index config changed</td>
      <td>[Reload](../tutorials/operations/segment-reload.md) all segments, or schedule a [RefreshSegmentTask](../operators/operating-pinot/refresh-segment-task.md) for full rebuild</td>
    </tr>
    <tr>
      <td>Too many small segments</td>
      <td>Schedule a [MergeRollupTask](../operators/operating-pinot/minion-merge-rollup-task.md) or [UpsertCompactMergeTask](../operators/operating-pinot/upsert-compact-merge-task.md)</td>
    </tr>
    <tr>
      <td>Stale records in upsert table wasting space</td>
      <td>Schedule an [UpsertCompactionTask](../operators/operating-pinot/upsert-compaction-task.md)</td>
    </tr>
    <tr>
      <td>Need to delete specific records (GDPR)</td>
      <td>Schedule a [PurgeTask](../operators/operating-pinot/purge-task.md)</td>
    </tr>
    <tr>
      <td>Bad offline push needs rollback</td>
      <td>Use [Consistent Push and Rollback](../operators/operating-pinot/consistent-push-and-rollback.md)</td>
    </tr>
    <tr>
      <td>Recent data needs fast disks, old data can be on HDDs</td>
      <td>Configure [tiered storage](../operators/operating-pinot/separating-data-storage-by-age/)</td>
    </tr>
  </tbody>
</table>
