---
description: Query-level switches that shape execution, diagnostics, and resource use.
---

# Query Options

Query options are per-query switches that let you choose the execution engine, control runtime limits, and adjust diagnostics.

## The options that matter most

- `useMultistageEngine` selects the multi-stage engine for queries that need advanced SQL features.
- `timeoutMs` bounds how long Pinot should spend on the query.
- `clientQueryId` gives the query a stable identifier for tracking and cancellation.
- `explainPlanVerbose` asks Pinot for richer plan output.
- `maxExecutionThreads` limits concurrency for expensive queries.

```sql
SET useMultistageEngine = true;
SET timeoutMs = 5000;
SET clientQueryId = 'query-2026-03-24-001';
SELECT city, COUNT(*)
FROM stores
GROUP BY city
LIMIT 10;
```

## When to reach for options

Use query options when you want to change behavior without changing table configuration.

Typical cases include:

- lowering timeout for a user-facing request
- forcing multi-stage execution for a query that needs joins
- attaching a custom query ID for logs and cancellation
- widening or narrowing execution resources for a single query

## Where the deeper knobs live

Some query behavior is controlled by dedicated pages rather than a raw option list:

- use [Query quotas](query-quotas.md) for rate limiting
- use [Query cancellation](query-cancellation.md) when a query must be stopped
- use [Cursor pagination](query-using-cursors.md) when the result set is too large

## What this page covered

This page covered the main query-level switches, why you would set them, and which dedicated pages handle related controls.

## Next step

If you need to track or stop a query, read [Query cancellation](query-cancellation.md). If you need to shape result delivery, read [Cursor pagination](query-using-cursors.md).

## Related pages

- [Querying Pinot](../querying-pinot.md)
- [SQL syntax](../sql-syntax.md)
- [Query quotas](query-quotas.md)
- [Correlation IDs](query-correlation-id.md)
---
description: This document contains all the available query options
---

# Query Options

## Supported Query Options

| Key | Description | Default Behavior |
| --- | --- | --- |
| **timeoutMs** | Timeout of the query in milliseconds | Use table/broker level timeout |
| **enableNullHandling** | Enables advanced null handling. See [Null value support](../null-value-support.md) for more information.(since 0.11.0) | `false` (disabled) |
| **explainPlanVerbose** | Return verbose result for `EXPLAIN` query (since 0.11.0) | `false` (not verbose) |
| **useMultistageEngine** | Use multi-stage engine to execute the query (since 0.11.0) | `false` (use single-stage engine) |
| **maxExecutionThreads** | Maximum threads to use to execute the query. Useful to limit the resource usage for expensive queries | Half of the CPU cores for non-group-by queries; all CPU cores for group-by queries |
| **numReplicaGroupsToQuery** | When replica-group based routing is enabled, use it to query multiple replica-groups (since 0.11.0) | `1` (only query servers within the same replica-group) |
| **sortAggregateLimitThreshold** | For group-by query, in case of ordering by all group keys, use sort-aggregation when query `LIMIT` is below this threshold. Under such cases, sort-aggregation allows trimming that does not affect result correctness, and is often more efficient than hash aggregation due to significantly reduced memory pressure. Example query that uses sort-aggregation: `SELECT col1, COUNT(*) FROM t1 GROUP BY col1, col2 ORDER BY col1, col2 DESC LIMIT X; `, where `X` is smaller than this threshold. | `10000` |
| **sortAggregateSingleThreadedNumSegmentsThreshold** | When sort-aggregation is used under the above cases described in `sortAggregateLimitThreshold`, use single-threaded sequential combine instead of parallel pair-wise combine when the number of segments to merge is below this threshold. | Number of CPU cores |
| **allowReverseOrder** | For single-stage selection queries, allow Pinot to read a sorted segment in descending order for `ORDER BY ... DESC` instead of scanning the segment in ascending order and reordering it. This can enable early termination when the full sorted prefix of the `ORDER BY` clause is descending and the query has a small `LIMIT`. If the segment cannot provide descending blocks, or if later `ORDER BY` expressions still require additional ordering work, Pinot falls back to the normal path and can still scan the full segment. | `false` |
| **minSegmentGroupTrimSize** | Minimum groups to keep when trimming groups at the segment level for group-by queries. See [#configuration-parameters](../grouping-algorithm.md#configuration-parameters) | Server level config |
| **minServerGroupTrimSize** | Minimum groups to keep when trimming groups at the server level for group-by queries. See [#configuration-parameters](../grouping-algorithm.md#configuration-parameters) | Server level config |
| **serverReturnFinalResult** | For aggregation and group-by queries, ask servers to directly return final results instead of intermediate results for aggregations. Can be applied when the group key is server partitioned, i.e. the column(s) is partitioned, and all the data for a partition is served by the same server. | `true` when a single server is queried, `false` otherwise |
| **serverReturnFinalResultKeyUnpartitioned** | For group-by queries, ask servers to directly return final results instead of intermediate results for aggregations. Different from **serverReturnFinalResult**, this option should be used when the group key is not server partitioned, but the aggregated column is server partitioned. It is particularly useful for distinct count queries. When this option is enabled, server will return final results, but won't directly trim the result to the query limit. | `false` |
| **skipIndexes** | Which indexes to skip usage of (i.e. scan instead), per-column. This is useful for side-by-side comparison/debugging. There can be cases where the use of an index is actually more expensive than performing a scan of the docs which match other filters. One such example could be a low-selectivity inverted index used in conjunction with another highly selective filter. Config can be specified using url parameter format: `skipIndexes='col1=inverted,range&col2=inverted'` Possible index types to skip are: `sorted, range, inverted, H3`. To find out which indexes are used to resolve a given query, use the `EXPLAIN` query. | `null/empty` (use all available indexes) |
| **skipPlannerRules** | Which defaultly enabled query planner rules should be disabled. This is useful when `EXPLAIN PLAN FOR` suggests a rule evaluation is taking too long or when it is known that a rule produces sub-optimal plan for the query. Currently this only applies to rules in optProgram that are mostly logical transformations. Config can be specified using rule names delimited by comma: `skipPlannerRules='FilterProjectTranspose,PruneEmptySort'` The rule name used here is consistent with the output of `EXPLAIN PLAN FOR`, which is the rule description. | `null/empty` (no defaultly enabled rules are skipped) |
| **usePlannerRules** | Which query planner rules that are disabled by default should be used. This is useful when the defaultly disabled rules could help query execution. Config can be specified using rule names delimited by comma: `usePlannerRules='AggregateJoinTransposeExtended,JoinToEnrichedJoin'`. This query option only applies to the set of defaultly disabled rules listed in [#default-disabled-rules](../default-disabled-rules.md) At this point, Pinot does not have a cost-based optimizer and the multi-stage query engine uses Calcite's HepPlanner for query optimization. The rules that are disabled by default are those that are only helpful under certain circumstances. For a more detailed description on what these rules do and when are they helpful, please see [#default-disabled-rules](../default-disabled-rules.md). | `null/empty` (no defaultly disabled rules are used) |
| **skipUpsert** | For upsert-enabled table, skip the effect of upsert and query all the records. See [upsert.md](../../ingestion/upsert-and-dedup/upsert.md) | `false` (exclude the replaced records) |
| **upsertViewFreshnessMs** | For upsert tables using `SNAPSHOT` consistency mode, override the query-time freshness window for the upsert view. By default, Pinot uses the table's `upsertViewRefreshIntervalMs`. Smaller values can refresh the view sooner for a query, and `0` forces a refresh for every query. See [upsert.md](../../ingestion/upsert-and-dedup/upsert.md) for the table-level setting and consistency-mode details. | Use the table's `upsertViewRefreshIntervalMs` |
| **skipUpsertView** | For debugging upsert tables, bypass the consistent upsert view maintained by `SYNC` or `SNAPSHOT` consistency mode and query as if the table were using `NONE` mode. See [upsert.md](../../ingestion/upsert-and-dedup/upsert.md) for the upsert-view behavior this skips. | `false` |
| **useStarTree** | Useful to debug the star-tree index (since 0.11.0) | `true` (use star-tree if available) |
| **AndScanReordering** | [See detailed description](../../../operate-pinot/performance-optimization-configurations.md) | disabled |
| **maxRowsInJoin** | Configure maximum rows allowed in a join operation. This limit is applied to both the hash table build phase for the join's right input as well as the number of joined rows emitted after matching with the join's left input. | default value read from cluster config``pinot.query.join.max.rows `` if not set, the default will be **2^20 (1024*1024)** |
| **inPredicatePreSorted** | (Only apply to STRING columns) Indicates that the values in the IN clause is already sorted, so that Pinot doesn't need to sort them again at query time | `false` (values in IN predicate is not pre-sorted) |
| **inPredicateLookupAlgorithm** | (Only apply to STRING columns) The algorithm to use to look up the dictionary ids for the IN clause values. - `DIVIDE_BINARY_SEARCH`: Sort the IN clause values and do binary search on both dictionary and IN clause values at same time to reduce the value lookups - `SCAN`: Sort the IN clause values and scan both dictionary and IN clause values to get the matching dictionary ids - `PLAIN_BINARY_SEARCH`: Do not sort the IN clause values, but directly binary search each IN clause value in the dictionary | `DIVIDE_BINARY_SEARCH` |
| **maxServerResponseSizeBytes** | Long value config indicating the maximum length of the serialized response per server for a query. | Overriding priortiy order: 1. QueryOption -> maxServerResponseSizeBytes 2. QueryOption -> maxQueryResponseSizeBytes 3. TableConfig -> maxServerResponseSizeBytes 4. TableConfig -> maxQueryResponseSizeBytes 5. BrokerConfig -> maxServerResponseSizeBytes 6. BrokerConfig -> maxServerResponseSizeBytes |
| **maxQueryResponseSizeBytes** | Long value config indicating the maximum serialized response size across all servers for a query. This value is equally divided across all servers processing the query. | Overriding priortiy order: 1. QueryOption -> maxServerResponseSizeBytes 2. QueryOption -> maxQueryResponseSizeBytes 3. TableConfig -> maxServerResponseSizeBytes 4. TableConfig -> maxQueryResponseSizeBytes 5. BrokerConfig -> maxServerResponseSizeBytes 6. BrokerConfig -> maxServerResponseSizeBytes |
| **filteredAggregationsSkipEmptyGroups** | This config can be set to `true` to avoid computing all the groups in a group by query with only filtered aggregations (and no non-filtered aggregations). By default, the groups are computed over all the rows returned by the main filter, even if certain rows will never match any of the aggregation filters. This is the standard SQL behavior. However, if the selectivity of the main filter is very high as compared to the selectivity of the aggregation filters, this query option can help provide a big performance boost if the empty groups aren't required. For instance, a query like `SELECT SUM(X) FILTER (WHERE Y = 1) FROM mytable` will compute the groups over all the rows in the table by default since there's no main query filter. Setting this query option to `true` in such cases can massively improve performance if there's an inverted index on column `Y` for instance. | `false` (i.e., all groups are computed by default as per standard SQL) |
| **dropResults** | Set dropResults=true in the config to drop the resultTable from the response. Use this option to troubleshoot a customer's query (which may have sensitive data in the result) using metadata only. | `false` |
| **skipUnavailableServers** | Set skipUnavailableServers=true in the config to continue sending queries to remaining servers if dispatching a query fails. | `false` |
| **ignoreMissingSegments** | Ignore `SERVER_SEGMENT_MISSING` exceptions when a routed segment is unavailable on a server. When enabled, Pinot filters those exceptions during server execution and broker-side reduce so the query can continue. This is useful during short routing propagation windows after segment deletion or movement, but the query can succeed while silently omitting data from the missing segments. | `false` |
| **sampler** | Selects a named table sampler from the table config. Use this to run a query against a sampled subset of segments, for example `SET sampler='small'`. See [Table](../../../reference/configuration-reference/table.md#table-samplers) for the table-level configuration. | `null/empty` (normal routing, no table sampler) |
| **clientQueryId** | Set to define a [custom correlation ID](query-correlation-id.md) for a query and to [cancel queries](query-cancellation.md). | `null/empty` |
| **accurateGroupByWithoutOrderBy** | Improves correctness of group-by queries with LIMIT but without ORDER BY by applying better trimming on servers. See PR #15844. Set `accurateGroupByWithoutOrderBy=true` to enable | `false` (disabled) |
| **traceRuleProductions** | Trace planner rule productions. Specify `SET traceRuleProductions=true` to collect and return planner rules that successfully produced new relations and the relation subtree before and after the production in time order along with rule attempt timing. Useful for debugging query planning. | `false` |
| **excludeVirtualColumns** | When you want to ignore virtual columns (those starting with $) in a query — such as a NATURAL JOIN where they shouldn't be participating in join condition matching. This option helps remove all virtual columns from the schema during query planning and execution making NATURAL JOIN successful. This is currently implemented in MSE. | `false` (virtual columns are included by default for all queries during join-match) |
| **usePhysicalOptimizer** | Enable the Physical Optimizer for the multi-stage engine (MSE). The Physical Optimizer can automatically eliminate or simplify redundant Exchanges (shuffles) for arbitrarily complex queries without requiring query hints. Must be used with `useMultistageEngine=true`. See [physical-optimizer.md](../multi-stage-query/physical-optimizer.md) for details. (introduced in 1.4.0, Beta) | `false` (disabled) |
| **useLiteMode** | Enable Multistage Engine Lite Mode, which runs MSE queries using a scatter-gather paradigm (like the single-stage engine) with a configurable limit on rows returned by each leaf stage instance (default 100k). This allows safe access to MSE features like window functions, subqueries, and joins at high QPS with minimal reliability risks. Requires both `useMultistageEngine=true` and `usePhysicalOptimizer=true`. See [multistage-lite-mode.md](../multi-stage-query/multistage-lite-mode.md) for details. (introduced in 1.4.0, Beta) | `false` (disabled) |
| **orderedPreferredPools** | Specify a prioritized list of server pools for broker query routing, provided as a vertical bar (`\|`) separated list of pool identifiers (integers). The broker uses the list as a routing hint, attempting to route queries to the specified pools in order and falling back gracefully to other available replicas if none of the preferred pools are available. Useful for canary deployments where directing traffic to specific replica groups is desired. Currently supported for Balanced and ReplicaGroup routing strategies with Adaptive Server Selection in non-MSE mode. (introduced in 1.4.0) | `null/empty` (no pool preference; use default routing) |
| **workloadName** | Assigns the query to a named workload for resource budget enforcement. Requires the `workload` query scheduler. See [Workload-Based Query Resource Isolation](../../../operate-pinot/tuning/workload-query-isolation.md) (introduced in 1.4.0) | `null/empty` (query belongs to the default workload with no budget enforcement) |
| **isSecondaryWorkload** | Marks the query as a secondary workload query. With the `binary_workload` scheduler, secondary queries run with limited threads. With the `workload` scheduler, maps to the configured secondary workload budget. See [Workload-Based Query Resource Isolation](../../../operate-pinot/tuning/workload-query-isolation.md) (introduced in 1.4.0) | `false` |
| **enableMultiClusterRouting** | Enable multi-cluster querying (federation) to route queries across multiple Pinot clusters. Requires broker to be configured with remote cluster connections using `MultiClusterHelixBrokerStarter`, and only applies to logical tables. See [Multi-Cluster Querying](../multi-cluster-querying.md) for details. | `false` (queries only execute against local cluster) |

### Cursor Pagination

| Key | Description | Default Behavior |
| --- | --- | --- |
| **getCursor** | When set to `true`, a cursor is returned instead of the complete result set. This allows clients to fetch query results incrementally, which is useful for large result sets. | `false` (return full result set) |
| **cursorNumRows** | Number of rows each cursor page should contain. Only applies when `getCursor=true`. | Broker level config |

### Explain Plan

| Key | Description | Default Behavior |
| --- | --- | --- |
| **explainAskingServers** | Controls the explain behavior in the multi-stage engine. When set to `true`, servers are asked to return the physical plan. When `false`, only the logical plan is returned (mimics behavior of Pinot 1.2.0 and earlier). | `true` |

### Group-By Trim

| Key | Description | Default Behavior |
| --- | --- | --- |
| **minBrokerGroupTrimSize** | Minimum number of groups to keep when trimming groups at the broker level for group-by queries (SSE only). Similar to **minSegmentGroupTrimSize** and **minServerGroupTrimSize** but applied at the broker reduce phase. Setting to a non-positive value disables broker-level trim. See [#configuration-parameters](../grouping-algorithm.md#configuration-parameters) | Broker level config (default `5000`) |
| **groupTrimThreshold** | Threshold for group-by trimming at the broker level. Controls the maximum number of groups that can be held before trimming is triggered during the broker reduce phase. | Broker level config (default `1000000`) |

### Multi-Stage Engine Group-By Streaming

| Key | Description | Default Behavior |
| --- | --- | --- |
| **streamingGroupByFlushThreshold** | For GROUP BY queries in the multi-stage engine, flushes partial group-by results when the accumulated number of groups reaches this threshold. This bounds server memory usage for high-cardinality GROUP BY queries by periodically emitting intermediate results instead of buffering all groups in memory. When set to a positive value, enables the `StreamingGroupByCombineOperator` which flushes partial results; when unset or 0, uses the standard `GroupByCombineOperator` (backward compatible). This is a middle ground between completely skipping leaf-stage group by (`is_skip_leaf_stage_group_by=true`) and full leaf-stage group by (the default). Note: result trimming is disabled in streaming mode to prevent incorrect partial aggregates. Recommended for queries with GROUP BY cardinality exceeding typical memory limits. | `0` (disabled; uses standard GroupByCombineOperator) |

#### Example: Streaming Group-By with Flush Threshold

For a high-cardinality GROUP BY query that might cause memory pressure, you can enable streaming mode:

```sql
-- Enable multi-stage engine with streaming group-by
SET useMultistageEngine = true;
SET streamingGroupByFlushThreshold = 5000;

-- Query with potentially high cardinality GROUP BY
SELECT user_id, country, COUNT(*) as event_count
FROM events
WHERE date = '2026-04-01'
GROUP BY user_id, country
LIMIT 100000;
```

In this example, the query will flush partial group-by results every time the number of accumulated groups reaches 5000, preventing unbounded memory growth. This is especially useful for queries where the GROUP BY cardinality is unknown or very high.

### Join and Window Overflow

| Key | Description | Default Behavior |
| --- | --- | --- |
| **joinOverflowMode** | Controls behavior when a join operation exceeds **maxRowsInJoin**. Possible values: `THROW` (throw an exception) or `BREAK` (stop processing and return partial results). | `THROW` |
| **maxRowsInWindow** | Configure maximum rows allowed in a window function operation. This helps prevent excessive memory usage when processing large window frames. | Default value read from cluster config `pinot.query.window.max.rows`; if not set, defaults to **2^20 (1024*1024)** |
| **windowOverflowMode** | Controls behavior when a window operation exceeds **maxRowsInWindow**. Possible values: `THROW` (throw an exception) or `BREAK` (stop processing and return partial results). | `THROW` |

### Multi-Cluster Routing

| Key | Description | Default Behavior |
| --- | --- | --- |
| **enableMultiClusterRouting** | Enable multi-cluster querying (federation) to route queries across multiple Pinot clusters. Requires broker to be configured with remote cluster connections using `MultiClusterHelixBrokerStarter`, and only applies to logical tables. See [Multi-Cluster Querying](../multi-cluster-querying.md) for details. | `false` (queries only execute against local cluster) |

### Broker Pruning

| Key | Description | Default Behavior |
| --- | --- | --- |
| **useBrokerPruning** | When set to `true`, enables broker-side segment pruning logic in the multi-stage engine. This allows the broker to prune segments before dispatching queries to servers, reducing unnecessary computation. Only supported by the MSE query optimizer. | Broker level config (default `true`) |
| **useIndexBasedDistinctOperator** | When `true`, routes eligible `SELECT DISTINCT jsonExtractIndex(col, path, type)` queries to `JsonIndexDistinctOperator`, which reads distinct values directly from the JSON index without scanning documents. Requires the queried JSON path to have a backing JSON index. Supports INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL, and STRING result types. | `false` (disabled) |

### DISTINCT Early-Termination (Single-Stage Engine)

| Key | Description | Default Behavior |
| --- | --- | --- |
| **maxRowsInDistinct** | Maximum number of rows to scan across all segments in a DISTINCT query before early termination. When this limit is reached, the query stops scanning additional segments and returns partial results. Only applies to single-stage engine (SSE/v1) DISTINCT queries. See `maxRowsInDistinctReached` in the response to determine if this limit was triggered. | `null/empty` (no limit) |
| **maxRowsWithoutChangeInDistinct** | Maximum number of rows to scan in a DISTINCT query without producing any new distinct values before early termination. This option is useful to optimize queries when the distinct value set converges quickly. When this limit is reached, the query stops scanning and returns partial results. Only applies to single-stage engine (SSE/v1) DISTINCT queries. See `maxRowsWithoutChangeInDistinctReached` in the response to determine if this limit was triggered. | `null/empty` (no limit) |
| **maxExecutionTimeMsInDistinct** | Wall-clock time budget in milliseconds for the combine operator in a DISTINCT query. When this time limit is exceeded, the query returns partial results. Only applies to single-stage engine (SSE/v1) DISTINCT queries. See `maxExecutionTimeInDistinctReached` in the response to determine if this limit was triggered. | `null/empty` (no limit) |

#### Example DISTINCT Queries with Early Termination

```sql
-- Stop after scanning 100,000 rows
SELECT DISTINCT country FROM users
OPTION (maxRowsInDistinct=100000)

-- Stop after 10,000 rows without new distinct values
SELECT DISTINCT state FROM users
OPTION (maxRowsWithoutChangeInDistinct=10000)

-- Stop after 5 seconds of execution
SELECT DISTINCT user_id FROM events
OPTION (maxExecutionTimeMsInDistinct=5000)

-- Combine multiple limits
SELECT DISTINCT product_id FROM orders
OPTION (maxRowsInDistinct=50000, maxRowsWithoutChangeInDistinct=5000)
```

When any of these early-termination budgets is exceeded, the response will include the following flags to indicate which limit was reached:

- `partialResult` (boolean): Set to `true` when the result is partial due to early termination
- `maxRowsInDistinctReached` (boolean): Set to `true` if `maxRowsInDistinct` limit was exceeded
- `maxRowsWithoutChangeInDistinctReached` (boolean): Set to `true` if `maxRowsWithoutChangeInDistinct` limit was exceeded
- `maxExecutionTimeInDistinctReached` (boolean): Set to `true` if `maxExecutionTimeMsInDistinct` limit was exceeded

#### Example Response with Early Termination

```json
{
  "resultTable": {
    "dataSchema": {
      "columnNames": ["country"],
      "columnDataTypes": ["STRING"]
    },
    "rows": [
      ["USA"],
      ["Canada"],
      ["Mexico"]
    ]
  },
  "numDocsScanned": 100000,
  "numEntriesScannedInFilter": 100000,
  "numEntriesScannedPostFilter": 100000,
  "totalDocs": 10000000,
  "numSegmentsQueried": 10,
  "numSegmentsProcessed": 6,
  "partialResult": true,
  "maxRowsInDistinctReached": true,
  "maxRowsWithoutChangeInDistinctReached": false,
  "maxExecutionTimeInDistinctReached": false,
  "timeUsedms": 245
}
```
