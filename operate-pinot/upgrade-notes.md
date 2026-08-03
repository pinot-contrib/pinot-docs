---
description: >-
  Operator-facing behavior changes, migration hazards, and required actions
  for recent Apache Pinot releases.
---

# Upgrade notes

This page summarizes the behavior changes, new defaults, deprecations, and
migration hazards that operators should review before upgrading Apache Pinot.
For the full list of features and fixes in each release, see the
[release notes](../reference/releases/README.md).

For guidance on running the cross-release compatibility tester and the
recommended component upgrade order, see
[Upgrading Pinot](upgrading-pinot-cluster.md).

## Upcoming Release

### Singular live-brokers endpoint removed

The controller endpoint `GET /tables/{tableName}/livebrokers` has been
removed. Use `GET /tables/livebrokers` instead.

The replacement is not a path-only migration: the removed endpoint returned a
`List<String>` for one table, while the plural endpoint returns a
`Map<String, List<InstanceInfo>>` for the tables it resolves. External clients
that continue to call the singular endpoint receive `404` after upgrading.

**Action required.** Update controller API clients, scripts, and monitoring
integrations to call the plural endpoint. Select the requested table from the
response map and update deserialization logic to consume `InstanceInfo`
objects rather than broker-name strings.

The same change removes two deprecated `RequestUtils` methods used only by
out-of-tree Java callers. Recompile and migrate custom code that calls
`getFunctionExpression(String)` or `getOptionsFromJson(JsonNode, String)`.

*Source: [PR #19142](https://github.com/apache/pinot/pull/19142)*

### Legacy valid-doc-ID REST endpoints removed

Pinot servers no longer expose these deprecated endpoints:

| Removed endpoint | Replacement |
| --- | --- |
| `GET /segments/{table}/{segment}/validDocIds` | `GET /segments/{table}/{segment}/validDocIdsBitmap` |
| `GET /tables/{table}/validDocIdMetadata` | `POST /tables/{table}/validDocIdsMetadata` |

External operator scripts and third-party upsert or compaction tooling that
still call the removed paths receive `404` after upgrading. The replacement
table-level endpoint also changes the HTTP method from `GET` to `POST`.

**Action required.** Search automation and integrations for the two legacy
paths, migrate them to the replacements above, and verify request bodies and
response handling before upgrading servers.

This release also removes deprecated Java APIs including `SegmentName`,
`TableConfigBuilder.setLLC`, replication-number accessors on
`SegmentsValidationAndRetentionConfig`, and several controller/minion helpers.
Recompile out-of-tree code that depends on those APIs.

*Source: [PR #19141](https://github.com/apache/pinot/pull/19141)*

### SegmentAdminClient segment selection now honors all filters

`SegmentAdminClient.selectSegments` now uses
`GET /segments/{tableName}` instead of the deprecated
`GET /segments/{tableName}/select` endpoint. The deprecated endpoint remains
available so controllers can continue serving clients from an earlier release
during a rolling upgrade.

Two previously ignored inputs now affect results:

- Passing `excludeReplacedSegments=false` includes replaced segments. The old
  endpoint always excluded them, so callers that pass `false` can receive a
  larger result set after upgrading.
- The `database` header is now honored when selecting segments.

**Action required for Java client users.** Review code that calls
`selectSegments` with `excludeReplacedSegments=false`, and ensure it can handle
replaced segments in the returned list. Verify database-scoped clients pass the
intended database header.

This change also removes deprecated Java APIs for custom controller and index
extensions, including two `PinotHelixResourceManager` methods and the
four-argument `OnHeapGuavaBloomFilterCreator` constructor. Recompile any
out-of-tree code that calls those APIs.

*Source: [PR #19140](https://github.com/apache/pinot/pull/19140)*

### Pre-1.0 deprecated Java and plugin APIs removed

Pinot has removed a group of public APIs deprecated between 2016 and 2022. This
is primarily a compatibility change for custom plugins and out-of-tree Java
code; it does not change configuration keys, wire formats, or data stored in
ZooKeeper.

The removed APIs include legacy `Schema`, `GenericRow`, `FieldConfig`,
`ConnectionFactory`, `FileUploadDownloadClient`, component-starter, segment
pruner, and minion task-factory entry points. In particular, stale plugin jars
that call `GenericRow.putField`, `Schema.addField(String, FieldSpec)`, or the
five-argument `FieldConfig` constructor can fail at runtime with
`NoSuchMethodError`.

**Action required for plugin and client authors.** Rebuild custom record
readers, record extractors, record transformers, minion tasks, and other
out-of-tree Pinot integrations against the new Pinot artifacts before
upgrading servers or minions. Migrate to the non-deprecated replacements,
including `GenericRow.putValue` / `putValues`, `Schema.addField(FieldSpec)`, the
`FieldConfig` list constructor or builder, URL-string `ConnectionFactory`
methods, and the two-argument `PinotTaskExecutorFactory.init` method.

The Pinot controller now calls the plural `GET /tables/{table}/size` server
endpoint. The deprecated singular endpoint remains available for rolling
upgrade compatibility.

*Source: [PR #19139](https://github.com/apache/pinot/pull/19139)*

### REST schema APIs now reject deprecated `TimeFieldSpec`

Apache Pinot now formally deprecates `TimeFieldSpec` and rejects schema payloads
that use `fieldType=TIME` on the controller REST validation paths:

- `POST /schemas`
- `PUT /schemas/{schemaName}`
- `/schemas/validate`

Use `DateTimeFieldSpec` through `dateTimeFieldSpecs` for all new or updated
schemas submitted through the controller. Pinot still allows older schemas that
already exist in cluster metadata to load internally for backward compatibility,
so the change affects submission and validation, not startup of existing legacy
tables.

**Action required.** Audit any schema-generation tooling, CI validation, or
operator runbooks that still emit `TimeFieldSpec`, and migrate them to
`DateTimeFieldSpec` before upgrading. If you maintain a record reader or other
schema-aware plugin, treat `DateTimeFieldSpec` as the default contract and keep
legacy `TimeFieldSpec` handling only where backward compatibility requires it.

*Source: [PR #18502](https://github.com/apache/pinot/pull/18502)*

### Removal of deprecated PinotTaskManager scheduleTasks wrapper methods

The following `@Deprecated(forRemoval = true)` wrapper methods in `PinotTaskManager` have been removed. These methods were deprecated since v1.4.0 (Feb 2025):

- `scheduleAllTasksForAllTables(String)`
- `scheduleAllTasksForDatabase(String, String)`
- `scheduleAllTasksForTable(String, String)`
- `scheduleTaskForAllTables(String, String)`
- `scheduleTaskForDatabase(String, String, String)`
- `scheduleTaskForTable(String, String, String)`
- `protected scheduleTasks(List<String>, boolean, String)`
- `protected scheduleTask(String, List<String>, String)`

**Action required for plugin authors and custom controllers.** If your custom code or minion plugins call any of these methods, migrate to `scheduleTasks(TaskSchedulingContext)` instead. This is a programmatic API change affecting only direct callers of `PinotTaskManager` methods; the REST API endpoints for task scheduling remain unchanged.

*Source: [PR #18275](https://github.com/apache/pinot/pull/18275)*

### Segment SPI upgrade for custom segment and index extensions

Apache Pinot 1.6.0 changes several `@InterfaceAudience.Private` types in
`pinot-segment-spi`. This is a developer-facing compatibility change for
custom code that implements Pinot's segment-level interfaces. It does not
change query syntax, table configuration, or normal segment readability for
clusters that only use built-in Pinot components.

The breaking changes in [PR #18280](https://github.com/apache/pinot/pull/18280)
include:

- `ColumnMetadata` now requires explicit implementations for
  `isMinMaxValueInvalid()`, `getLengthOfShortestElement()`,
  `getLengthOfLongestElement()`, `isAscii()`, `getNumIndexes()`,
  `getIndexType()`, `getIndexSize()`, and `getIndexSizeFor()`.
- `ColumnMetadata.getIndexSizeMap()` has been removed.
- `ColumnMetadata.INDEX_NOT_FOUND` has been renamed to `UNAVAILABLE`.
- `ColumnMetadata.getColumnMaxLength()` is deprecated for removal. Migrate to
  `getLengthOfLongestElement()`.
- `MapIndexReader` no longer has the reader generic parameter, and the API has
  been simplified from `getKeyIndexes()` / `getKeyMetadata()` to
  `getIndexes()` / `getColumnMetadata()`. The legacy helper methods
  `getKeyReader()`, `getKeyFieldSpec()`, and `getKeyStoredType()` were also
  removed.
- `ColumnPartitionMetadata.extractPartitions(...)` now returns `IntSet`
  instead of `Set<Integer>`, so downstream binaries must be recompiled.

Segment backward compatibility is preserved. Pinot still reads the legacy
`lengthOfEachEntry` metadata key when `lengthOfLongestElement` is absent, and
new segments additionally persist `lengthOfShortestElement`,
`lengthOfLongestElement`, and `isAscii`.

**Action required for extension authors.** Rebuild and retest any custom code
that implements `ColumnMetadata` or `MapIndexReader`, or that calls
`ColumnPartitionMetadata.extractPartitions(...)`, before upgrading to Pinot
1.6.0.

### IndexType SPI now requires explicit dictionary-contract methods

Apache Pinot 1.6.0 also changes the `IndexType<C, IR, IC>` SPI for custom
index implementations. [PR #18365](https://github.com/apache/pinot/pull/18365)
adds two new abstract methods that every `IndexType` implementation must
define:

- `requiresDictionary(FieldSpec, C)` returns `true` when the index's on-disk
  representation depends on dictionary IDs and cannot be built or read without
  a dictionary on the column.
- `shouldInvalidateOnDictionaryChange(FieldSpec, C)` returns `true` when the
  existing on-disk index must be deleted and rebuilt if the column gains or
  loses a dictionary across segment reload.

Pinot uses these hooks during segment creation and reload to decide whether it
must materialize a shared standalone dictionary for RAW forward-index columns
and whether existing index files can be reused safely. Built-in inverted, FST,
and IFST indexes require a dictionary. The built-in range index can still work
without a dictionary for numeric RAW columns, but any RAW forward index with a
dictionary-backed range index must use range index version 2; range index
version 1 is rejected for RAW + dictionary.

[PR #17269](https://github.com/apache/pinot/pull/17269) adds the related column
shape where a RAW forward index can share a standalone dictionary with
dictionary-backed secondary indexes. Existing configs that combine legacy
`tableIndexConfig.noDictionaryColumns` or `tableIndexConfig.noDictionaryConfig`
with dictionary-backed secondary indexes still need a config migration before
validation succeeds. Move the column to `fieldConfigList`, keep
`encodingType: RAW`, remove the legacy no-dictionary entry, and declare
`indexes.dictionary` with the secondary index, for example `indexes.inverted`,
`indexTypes: ["FST"]`, or `indexTypes: ["IFST"]`.

**Action required for custom index authors.** Recompile any external
`IndexType` plugin against Pinot 1.6.0 and implement both methods before
upgrading. Older binaries will fail with `AbstractMethodError` until updated.

### `JsonIndexReader` now returns a read-only bitmap contract

Apache Pinot also changes the `JsonIndexReader` SPI for custom JSON index
readers and any code that calls the reader directly. [PR
#18694](https://github.com/apache/pinot/pull/18694) changes all
`getMatchingDocIds(...)` overloads to return `ImmutableRoaringBitmap` instead
of `MutableRoaringBitmap`.

This is a developer-facing compatibility change. Pinot's built-in `JSON_MATCH`
behavior is unchanged, but direct SPI callers must now treat the returned
bitmap as read-only. A reader may return a borrowed bitmap backed by the
index's underlying storage, so the bitmap is only valid while the segment or
index stays open and must not be mutated in place.

The built-in OSS readers still return a fresh mutable bitmap through a
covariant override, so custom readers can keep that behavior if they want. The
important contract change is on the caller side:

- Use `ImmutableRoaringBitmap` in code that stores the return value from
  `getMatchingDocIds(...)`.
- Call `toMutableRoaringBitmap()` first if your code needs to mutate the
  bitmap.
- Revalidate any custom JSON index reader, filter operator, or other
  `pinot-segment-spi` integration that depends on this API before upgrading.

### `extractRawTimeValues` replaces Avro `enableLogicalTypes`

Apache Pinot 1.6.0 changes the ingestion config for Avro logical types and
adds the same raw-value control to Parquet readers. `AvroRecordReaderConfig`
and `ParquetRecordReaderConfig` now expose `extractRawTimeValues`, which
defaults to `false`. In the default mode, Pinot continues converting temporal
logical types during extraction. Set `extractRawTimeValues` to `true` only
when you need raw integer values for `date`, `time-*`, or `timestamp-*`
fields. `decimal` and `uuid` still convert in all cases.

**Action required.** If your Avro ingestion config still uses
`enableLogicalTypes`, remove it. To keep the default converted behavior, omit
the new setting or set `extractRawTimeValues: false`. If you previously
disabled logical-type conversion to preserve raw temporal values, move to
`extractRawTimeValues: true` and revalidate any `decimal` or `uuid` fields,
because those types no longer have a raw passthrough mode.

*Source: [PR #18400](https://github.com/apache/pinot/pull/18400)*

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
| `accounting.workload.sleep.time.ms` | `1` | Polling interval for enforcement |
| `accounting.secondary.workload.name` | `defaultSecondary` | Name of the secondary workload |
| `accounting.secondary.workload.cpu.percentage` | `0.0` | CPU percentage cap for the secondary workload |

This feature adds accounting-based workload budgets on brokers and servers.
The later `workload` scheduler can build on the same workload names, but these
configs do not require that scheduler.

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
