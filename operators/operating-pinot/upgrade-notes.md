---
description: >-
  Operator-facing behavior changes, migration hazards, and required actions
  for recent Apache Pinot releases.
---

# Upgrade notes

This page summarizes the behavior changes, new defaults, deprecations, and
migration hazards that operators should review before upgrading Apache Pinot.
For the full list of features and fixes in each release, see the
[release notes](../../basics/releases/README.md).

For guidance on running the cross-release compatibility tester and the
recommended component upgrade order, see
[Upgrading Pinot](upgrading-pinot-cluster.md).

## Upcoming Release

### Removal of deprecated controller configuration constants

The following 12 controller configuration constants that were deprecated since v0.8.0 (2020-2021) have been removed:

| Deprecated Constant | Replacement Constant | Property Name |
| --- | --- | --- |
| `DEPRECATED_RETENTION_MANAGER_FREQUENCY_IN_SECONDS` | `RETENTION_MANAGER_FREQUENCY_PERIOD` | `controller.retention.frequencyPeriod` |
| `DEPRECATED_OFFLINE_SEGMENT_INTERVAL_CHECKER_FREQUENCY_IN_SECONDS` | `OFFLINE_SEGMENT_INTERVAL_CHECKER_FREQUENCY_PERIOD` | `controller.offline.segment.interval.checker.frequencyPeriod` |
| `DEPRECATED_REALTIME_SEGMENT_VALIDATION_FREQUENCY_IN_SECONDS` | `REALTIME_SEGMENT_VALIDATION_FREQUENCY_PERIOD` | `controller.realtime.segment.validation.frequencyPeriod` |
| `DEPRECATED_STATUS_CHECKER_FREQUENCY_IN_SECONDS` | `STATUS_CHECKER_FREQUENCY_PERIOD` | `controller.status.checker.frequencyPeriod` |
| `DEPRECATED_OFFLINE_SEGMENT_INTERVAL_CHECKER_INITIAL_DELAY_IN_SECONDS` | `OFFLINE_SEGMENT_INTERVAL_CHECKER_INITIAL_DELAY_IN_SECONDS` | `controller.offlineSegmentIntervalChecker.initialDelayInSeconds` |
| `DEPRECATED_REALTIME_SEGMENT_VALIDATION_INITIAL_DELAY_IN_SECONDS` | `REALTIME_SEGMENT_VALIDATION_INITIAL_DELAY_IN_SECONDS` | `controller.realtime.segment.validation.initialDelayInSeconds` |
| `DEPRECATED_STATUS_CHECKER_INITIAL_DELAY_IN_SECONDS` | `STATUS_CHECKER_INITIAL_DELAY_IN_SECONDS` | `controller.status.checker.initialDelayInSeconds` |
| `DEPRECATED_RETENTION_MANAGER_INITIAL_DELAY_IN_SECONDS` | `RETENTION_MANAGER_INITIAL_DELAY_IN_SECONDS` | `controller.retentionManager.initialDelayInSeconds` |
| `DEPRECATED_BROKER_RESOURCE_VALIDATION_FREQUENCY_IN_SECONDS` | `BROKER_RESOURCE_VALIDATION_FREQUENCY_PERIOD` | `controller.broker.resource.validation.frequencyPeriod` |
| `DEPRECATED_LEAD_CONTROLLER_RESOURCE_ENABLED` | `LEAD_CONTROLLER_RESOURCE_ENABLED` | `controller.leadController.resource.enabled` |
| `DEPRECATED_SEGMENT_RELOCATOR_FREQUENCY_IN_SECONDS` | `SEGMENT_RELOCATOR_FREQUENCY_PERIOD` | `controller.segment.relocator.frequencyPeriod` |
| `DEPRECATED_SEGMENT_RELOCATOR_INITIAL_DELAY_IN_SECONDS` | `SEGMENT_RELOCATOR_INITIAL_DELAY_IN_SECONDS` | `controller.segment.relocator.initialDelayInSeconds` |

These constants have had explicit replacements available since v0.8.0, which have been in production use for several years.

**Action required.** If your cluster still uses any of the deprecated configuration keys (the old property names shown above), you must migrate to the replacement property names before upgrading to this release. The controller will no longer recognize or fall back to the deprecated configuration keys.

Check your controller configuration files and any automation that generates controller configurations to ensure they use the new property names.

*Source: [PR #18001](https://github.com/apache/pinot/pull/18001)*



## 1.4.0

### Schema enforcement on controller startup

The controller now validates that every table has both a `TableConfig` and a
`Schema` when it starts up. If either is missing, the controller exits by
default.

Two controller properties control this behavior:

| Property | Default | Effect |
| --- | --- | --- |
| `controller.startup.exitOnTableConfigCheckFailure` | `true` | Exit if any table is missing its `TableConfig` |
| `controller.startup.exitOnSchemaCheckFailure` | `true` | Exit if any table is missing its `Schema` |

**Action required.** Before upgrading, verify that every table has a schema. If
you have tables without schemas (for example, legacy tables created before
schema enforcement existed), either add the missing schemas or set both
properties to `false` until you can fix them.

*Source:
[BaseControllerStarter.java — `enforceTableConfigAndSchema()`](https://github.com/apache/pinot/pull/15333)*

### Default segment load mode changed to MMAP

The default value of `loadMode` in `TableConfig` changed from `HEAP` to `MMAP`
for newly created tables. Existing tables are not affected; their `loadMode`
stays as configured.

If your deployment relies on heap-based segment loading for new tables, set
`loadMode` to `HEAP` explicitly in the table config.

*Source:
[TableConfigBuilder.java — `DEFAULT_LOAD_MODE`](https://github.com/apache/pinot/pull/15089)*

### Workload-based query resource isolation

A new `QueryWorkloadConfig` model lets administrators define named workloads
with CPU and memory budgets. Queries are assigned to workloads using the
`WORKLOAD_NAME` query option.

Key cluster-level configuration properties:

| Property | Default | Description |
| --- | --- | --- |
| `accounting.workload.enable.cost.collection` | `false` | Enable workload cost tracking |
| `accounting.workload.enable.cost.enforcement` | `false` | Enable enforcement of budgets |
| `accounting.workload.enforcement.window.ms` | `60000` | Enforcement window duration (ms) |
| `accounting.workload.sleep.time.ms` | `100` | Polling interval for enforcement |
| `accounting.secondary.workload.name` | `defaultSecondary` | Name of the secondary workload |
| `accounting.secondary.workload.cpu.percentage` | `0.0` | CPU percentage cap for the secondary workload |

This feature extends the
[binary workload scheduler](tuning/workload-query-isolation.md) introduced in
1.3.0 with configurable per-workload budgets.

**Action required.** None unless you want to adopt workload isolation. The
feature is opt-in and disabled by default.

*Source:
[QueryWorkloadConfig.java](https://github.com/apache/pinot/pull/15109)*

### Server-level segment batching for rebalance

A new `batchSizePerServer` parameter on the rebalance API controls how many
segment moves are applied per server in each rebalance step. The default is
`-1` (disabled — all segments are moved in a single step, as before).

Setting a positive value, such as `100`, reduces the blast radius of each
rebalance step and gives the cluster time to recover between batches.

**Action required.** None unless you want to adopt batched rebalancing.
Consider enabling it for large tables or latency-sensitive clusters.

*Source:
[RebalanceConfig.java — `batchSizePerServer`](https://github.com/apache/pinot/pull/15617)*

### Upsert config deprecations: `enableSnapshot` and `enablePreload`

The boolean fields `enableSnapshot` and `enablePreload` in `UpsertConfig` are
deprecated in favor of the `Enablement` enum fields `snapshot` and `preload`.
The `Enablement` enum accepts `ENABLE`, `DISABLE`, or `DEFAULT`.

Using `DEFAULT` causes the table to inherit the instance-level setting,
which was not possible with the old boolean fields.

The old boolean setters still work for backward compatibility, but new table
configs should use the enum fields.

**Action required.** Update table configs at your convenience. The old fields
still function but will be removed in a future release.

*Source:
[UpsertConfig.java](https://github.com/apache/pinot/pull/15528)*

### Task throttling based on heap usage

Server-side MSE and segment-split tasks are now throttled when heap usage
exceeds a configurable threshold. Queued tasks resume when heap usage drops.

| Property | Default | Description |
| --- | --- | --- |
| `accounting.oom.alarming.heap.usage.ratio` | `0.75` | Log warnings above this ratio |
| `accounting.oom.critical.heap.usage.ratio` | `0.96` | Begin throttling tasks above this ratio |
| `accounting.oom.panic.heap.usage.ratio` | `0.99` | Aggressive back-off above this ratio |

**Action required.** None. The defaults are conservative, but you should
verify they are compatible with your heap-sizing strategy, especially on
servers that run large MSE queries.

*Source:
[ThrottleOnCriticalHeapUsageExecutor.java](https://github.com/apache/pinot/pull/16271)*

### Pauseless consumption (new feature)

Pinot 1.4.0 introduces pauseless consumption, which allows real-time ingestion
to continue while the previous segment is being built and uploaded. This is a
new opt-in feature; it does not change behavior for existing tables.

Operators enabling pauseless consumption should review the
[pauseless consumption runbook](pauseless-consumption.md) and
be aware that it is compatible with dedup and partial-upsert tables.

### Row-level security (new feature)

Row-level security (RLS) policies can now restrict which rows are visible to
different users or groups. This is relevant in multi-tenant deployments. No
existing behavior changes; RLS must be explicitly configured.

*Source: [PR #16043](https://github.com/apache/pinot/pull/16043)*

### Logical type support enabled by default in Avro

The Pinot Avro ingestion plugin now automatically handles Avro logical types
such as timestamps and decimals. Previously this required manual configuration.

**Action required.** If your ingestion pipeline relied on raw Avro bytes for
logical-type fields (for example, treating a timestamp as a plain long), verify
that the new automatic conversion does not change your stored values.

*Source: [PR #15654](https://github.com/apache/pinot/pull/15654)*

### Segment reindex throttle

A new `ClusterConfigChangeHandler` on servers adds throttling for segment
reindexing operations triggered by cluster configuration changes. This
prevents excessive I/O when many segments need reindexing simultaneously.

*Source: [PR #14894](https://github.com/apache/pinot/pull/14894)*

---

## 1.3.0

### Binary workload scheduler for query isolation

The `BinaryWorkloadScheduler` categorizes queries into a primary workload
(unbounded, FCFS) and a secondary workload with strict concurrency and thread
limits. Secondary queries that exceed the queue limit are pruned.

| Property | Default | Description |
| --- | --- | --- |
| `binarywlm.maxSecondaryRunnerThreads` | `5` | Max worker threads for the secondary workload |

To assign a query to the secondary workload, set the query option
`isSecondaryWorkload=true`.

**Action required.** None unless you want to isolate ad-hoc or low-priority
traffic. The feature is opt-in via the query scheduler algorithm selection.

*Source:
[BinaryWorkloadScheduler.java](https://github.com/apache/pinot/pull/13847)*

### Database-level query quota

Operators can now impose query-rate limits at the database level. Quotas are
configured per database via a `DatabaseConfig` znode in the Helix property
store.

| API | Method | Path |
| --- | --- | --- |
| Set quota | POST | `/databases/{databaseName}/quotas?maxQueriesPerSecond=` |
| Get quota | GET | `/databases/{databaseName}/quotas` |

A default cluster-wide limit can be set with the cluster config key
`databaseMaxQueriesPerSecond`. The default in code is `-1` (disabled); the
release notes reference a default of `1000`, which is the suggested starting
value.

Per-broker quotas adjust dynamically based on the number of live brokers.

**Action required.** If you use the database construct, consider setting
database-level quotas to prevent noisy-neighbor issues.

*Source: [PR #13544](https://github.com/apache/pinot/pull/13544)*

### Cursor-based query pagination

Cursor support lets clients consume large result sets in smaller chunks. A new
`numRows` parameter on `POST /query/sql` enables pagination, and a
`/resultStore` API manages result sets.

No behavior change for existing queries. Operators should be aware that the
result store consumes broker memory; monitor heap usage if cursors are enabled.

*Source: [PR #14110](https://github.com/apache/pinot/pull/14110)*

### Multi-stream ingestion — Kafka bug warning

{% hint style="warning" %}
Multi-stream ingestion for Kafka contains a known bug in 1.3.0 and is **not
production-ready** in this release. The fix is available in
[PR #15094](https://github.com/apache/pinot/pull/15094) and is included in
1.4.0.
{% endhint %}

**Action required.** Do not use multi-stream Kafka ingestion in 1.3.0. Wait
for 1.4.0 or cherry-pick the fix.

### TLS support for multi-stage engine mailboxes

TLS can now be configured between brokers and servers for the multi-stage
engine. Previously, inter-component traffic for MSE was unencrypted even when
TLS was enabled for other channels.

**Action required.** If your deployment requires end-to-end encryption,
configure TLS for MSE mailboxes after upgrading.

*Source: [PR #14476](https://github.com/apache/pinot/pull/14476),
[PR #14387](https://github.com/apache/pinot/pull/14387)*

### OOM protection for multi-stage queries

Guard rails are now in place to limit memory consumption during MSE query
execution, including per-block row tracking for cross joins and configurable
max-rows-in-join limits.

**Action required.** Review the default limits if you run large joins. The
defaults protect against runaway queries but may need tuning for legitimate
large-join workloads.

*Source: [PR #13598](https://github.com/apache/pinot/pull/13598),
[PR #13955](https://github.com/apache/pinot/pull/13955)*

---

## 1.2.0

### Column-major segment builder on by default

New tables default to `columnMajorSegmentBuilderEnabled = true`. This skips
the intermediate row-major conversion during segment commits and is both
faster and more space-efficient.

Existing tables are unaffected. If you need the legacy row-major builder for a
new table, explicitly set `columnMajorSegmentBuilderEnabled` to `false` in the
table config's `IndexingConfig`.

*Source:
[IndexingConfig.java](https://github.com/apache/pinot/pull/12770)*

### Lucene upgraded to 9.11.1

The bundled Apache Lucene version was upgraded from 9.x to 9.11.1. This is a
transparent dependency upgrade with no configuration changes required, but
operators should be aware of it when troubleshooting text-index behavior
changes.

{% hint style="info" %}
The `master` branch has since moved to Lucene 9.12.0.
{% endhint %}

*Source: [PR #13505](https://github.com/apache/pinot/pull/13505)*

### Minion resource isolation

Minions now support instance-tag-based resource isolation. You can configure a
tag per task type per table, allowing arbitrary assignment of minion nodes to
workloads.

**Action required.** None for existing setups. Operators who want isolation
should tag minion instances and update table-level task configs.

*Source: [PR #12459](https://github.com/apache/pinot/pull/12459)*

### Consistent upsert table view

A new `upsertConfig.consistencyMode` field accepts `NONE`, `SYNC`, or
`SNAPSHOT`. The default is `NONE` (no change from prior behavior).

| Mode | Trade-off |
| --- | --- |
| `NONE` | Best throughput; no consistency guarantee across segments |
| `SYNC` | Strong freshness; higher query latency; suited for low-QPS tables |
| `SNAPSHOT` | High-QPS/high-ingestion; periodic snapshot refresh controlled by `upsertViewFreshnessMs` query option |

**Action required.** None unless you need stronger consistency for upsert
queries. Evaluate `SYNC` or `SNAPSHOT` based on your latency and freshness
requirements.

*Source: [PR #12976](https://github.com/apache/pinot/pull/12976)*

### CLP compression codec for forward indexes

The [CLP](https://github.com/y-scope/clp) compression codec is now available
for forward indexes. It offers high compression ratios for log-like string
columns. Enable it by setting `compressionCodec: CLP` in the column's
`fieldConfigList`.

**Action required.** Opt-in only. Test compression ratios and query
performance on a staging cluster before enabling in production.

*Source: [PR #12504](https://github.com/apache/pinot/pull/12504)*

---
