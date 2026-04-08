---
description: Operational guidance for running the multi-stage engine (MSE) in production, including resource model, guardrails, and known limitations.
---

# Run the Multi-Stage Engine in Production

This page provides operator-level guidance for running the multi-stage engine (MSE) in production. It covers the intended use-cases, the execution and resource model, operational guardrails, and known limitations.

For a high-level comparison of the two query engines, see [Query Engines (SSE vs MSE)](../../build-with-pinot/querying-and-sql/sse-vs-mse.md). For MSE internals, see the [Multi-Stage Query](../../build-with-pinot/querying-and-sql/multi-stage-query/README.md) section.

## What MSE is for

MSE is Pinot's supported engine for queries that require relational operators beyond scatter-gather execution. It was introduced in Pinot 1.0.0 and has continued to mature across subsequent releases.

MSE is **not** a general-purpose batch query engine. It is designed for interactive-latency queries that need SQL features unavailable in the single-stage engine (SSE).

## Recommended production use-cases

MSE is well-suited for the following workloads:

| Use-case | Why MSE |
| --- | --- |
| Interactive joins | Joining a fact table with a dimension table or between two fact tables at interactive latency. Supports hash joins, lookup joins, colocated joins, and partition-based joins. |
| Window functions | `ROW_NUMBER`, `RANK`, `SUM OVER`, and other window functions require multi-stage execution. |
| Subqueries and CTEs | Common table expressions and correlated subqueries are planned as separate stages. |
| Advanced SQL with distributed stages | `INTERSECT`, `EXCEPT`, `UNION`, and complex multi-table queries that SSE cannot express. |

**Workloads that are a poor fit for MSE:**

- Large-scale ETL or batch joins that scan entire tables without selective filters. MSE executes in-memory without spill-to-disk, so unbounded intermediate result sets can exceed available memory. Use an external engine such as Trino or Spark for these workloads.
- Simple scatter-gather queries (filter, aggregate, top-K) where SSE has lower overhead.

## Resource model

Understanding how MSE uses cluster resources is essential for capacity planning and incident response.

### In-memory execution

All intermediate data in MSE is held in memory. There is no spill-to-disk mechanism. This means:

- The memory footprint of a query is proportional to the size of intermediate result sets (join build sides, window partitions, shuffle buffers).
- A single query with large intermediates can put memory pressure on the servers processing its stages.
- Operators should set overflow limits (see [Operational guardrails](#operational-guardrails)) to bound memory consumption.

### Stage-based distributed execution

MSE breaks a query into a tree of stages. Each stage runs on one or more servers in parallel:

- **Leaf stages** scan table segments on the servers that host them, similar to SSE.
- **Intermediate stages** perform joins, aggregations, window functions, and sorts. They run on servers selected by the broker and exchange data via mailbox channels.
- **Root stage** collects final results and returns them to the client through the broker.

Data moves between stages through network shuffles. The number of stages, the parallelism of each stage, and the volume of data shuffled all affect query latency and resource consumption.

For details on stage mechanics, see [Understanding Stages](../../build-with-pinot/querying-and-sql/multi-stage-query/understanding-stages.md).

### Not a spill-heavy batch engine

Unlike Trino or Spark, MSE does not write intermediate results to disk when memory is exhausted. If a stage exceeds available memory, the query fails with an out-of-memory error or is killed by overflow guards. This is by design: MSE targets interactive latency, not unbounded batch processing.

## Operational guardrails

The controls below help operators protect cluster stability when MSE is enabled.

### Query quotas

Use [Query Quotas](../../build-with-pinot/querying-and-sql/query-execution-controls/query-quotas.md) to rate-limit queries at the table, database, or application level. Quotas apply to both SSE and MSE queries and prevent a single tenant or application from monopolizing broker capacity.

### Workload isolation

The `workloadName` and `isSecondaryWorkload` query options assign queries to named workloads with resource budgets. Combined with the `workload` or `binary_workload` query scheduler, this lets operators isolate MSE traffic from latency-sensitive SSE traffic on the same servers.

See [Workload-Based Query Resource Isolation](../tuning/workload-query-isolation.md) for configuration details.

### Join and window overflow controls

These query options bound the memory consumed by join and window operations:

| Option | Default | Description |
| --- | --- | --- |
| `maxRowsInJoin` | 1,048,576 (2^20) | Maximum rows in a join hash table and joined output. |
| `joinOverflowMode` | `THROW` | `THROW` fails the query; `BREAK` returns partial results. |
| `maxRowsInWindow` | 1,048,576 (2^20) | Maximum rows in a window function partition. |
| `windowOverflowMode` | `THROW` | `THROW` fails the query; `BREAK` returns partial results. |

Set these at the cluster level via `pinot.query.join.max.rows` and `pinot.query.window.max.rows`, or override per-query using query options.

For production clusters, review whether the defaults are appropriate for your data volumes. Lowering these limits reduces the blast radius of expensive queries.

### Concurrency and thread controls

| Control | Description |
| --- | --- |
| `maxExecutionThreads` | Per-query option that limits the number of CPU threads used by a single query. Useful for preventing a heavy MSE query from consuming all server threads. |
| `pinot.broker.mse.max.server.query.threads` | Broker-side concurrency throttle for multi-stage queries, expressed as estimated server query threads. This broker-local setting overrides the cluster fallback `pinot.beta.multistage.engine.max.server.query.threads` when set to a positive value. |
| `pinot.broker.mse.max.server.query.threads.exceed.strategy` | Broker behavior when a query would exceed the broker-side throttle. `WAIT` blocks until capacity is available. `LOG` allows the query through and emits a warning instead of throttling it. |
| `pinot.server.query.executor.mse.max.execution.threads` | Server-side hard limit for concurrently executing multi-stage tasks. When set to a positive value, it overrides the cluster-derived hard limit. When left non-positive, Pinot derives a hard limit from `pinot.beta.multistage.engine.max.server.query.threads * pinot.beta.multistage.engine.max.server.query.threads.hardlimit.factor` if both cluster values are positive. |
| `pinot.server.query.executor.mse.max.execution.threads.exceed.strategy` | Server behavior when the hard limit is exceeded. `ERROR` rejects additional work immediately. `LOG` allows execution to continue and emits a warning. |
| `timeoutMs` | Per-query timeout. Set this to a value appropriate for interactive workloads (e.g. 10-30 seconds) to prevent runaway queries from holding resources indefinitely. |

The broker and server controls protect different parts of the system:

* The broker throttle limits how much multi-stage work a broker dispatches concurrently across the cluster.
* The server hard limit caps how many multi-stage executor tasks can run at the same time on an individual server.
* The cluster config `pinot.beta.multistage.engine.max.server.query.threads` is only a fallback. Broker-local and server-local configs take precedence when they are set to positive values.

{% hint style="warning" %}
Changing the broker-side throttle from disabled to enabled, or from enabled to disabled, requires a broker restart to take effect. Updating the limit value while the throttle remains enabled is applied dynamically.
{% endhint %}

### Broker pruning and routing

The MSE query optimizer supports broker-side segment pruning (`useBrokerPruning`, enabled by default). This allows the broker to skip segments that cannot match the query predicates before dispatching work to servers.

For tables with time-based or partition-based segment boundaries, broker pruning significantly reduces the number of segments scanned by leaf stages.

### Explain plan and stage stats for debugging

Use these tools to understand and optimize MSE query behavior in production:

- **`EXPLAIN PLAN FOR`** shows the logical and physical query plan, including stage boundaries, join strategies, and shuffle types. See [Explain Plan](../../build-with-pinot/querying-and-sql/multi-stage-query/explain-plan-1.md).
- **Stage stats** provide per-stage runtime metrics (rows processed, time spent, memory used) after query execution. See [Understanding Stage Stats](../../build-with-pinot/querying-and-sql/multi-stage-query/understanding-stage-stats.md).
- **`EXPLAIN IMPLEMENTATION PLAN FOR`** returns the physical plan as executed by the servers, useful for verifying that the physical optimizer is making expected decisions.

## Choosing between standard MSE and Lite Mode

MSE supports two execution modes:

| | Standard MSE | Lite Mode (Beta, since 1.4.0) |
| --- | --- | --- |
| **Execution model** | Fully distributed stages across servers with network shuffles. | Scatter-gather leaf stages (like SSE) with non-leaf stages running single-threaded in the broker. |
| **Join execution** | Distributed across servers. | Runs in the broker. |
| **Leaf stage row limit** | No built-in limit. | Configurable per-instance limit (default 100,000 rows). |
| **Target workload** | Queries that need distributed joins or large intermediate result sets. | High-QPS use-cases that need window functions, subqueries, or small joins without the risk of full table scans. |
| **Activation** | `SET useMultistageEngine=true;` | `SET useMultistageEngine=true; SET usePhysicalOptimizer=true; SET useLiteMode=true;` |

{% hint style="warning" %}
Lite Mode is currently in Beta. It requires the Physical Optimizer (`usePhysicalOptimizer=true`), which is also Beta.
{% endhint %}

**When to use Lite Mode:**

- You want to expose window functions or subqueries to users at high QPS without the risk of unbounded full-table scans.
- Your joins operate on small, pre-filtered datasets that fit comfortably in broker memory.
- You want scatter-gather routing guarantees (segment pruning, replica-group routing) that standard MSE does not fully support.

**When to use standard MSE:**

- You need distributed joins across large datasets.
- You need parallelism across servers for intermediate stages.
- Your queries exceed the Lite Mode leaf-stage row limit.

See [Multistage Lite Mode](../../build-with-pinot/querying-and-sql/multi-stage-query/multistage-lite-mode.md) for configuration details.

## Known limitations vs workload misfit

Some behaviors are current limitations of the MSE implementation. Others reflect a genuine workload misfit where a different tool is a better choice.

### Current limitations

These are areas where MSE behavior differs from SSE or from standard SQL expectations. They may be addressed in future releases:

- **Multi-value column support is limited.** Predicates and GROUP BY on multi-value columns require wrapping with `arrayToMv()`. See [Troubleshoot MSE](../troubleshooting/troubleshoot-multi-stage-query-engine.md).
- **Schema prefixes are not supported.** Queries like `SELECT * FROM schema.table` are not valid.
- **Table and column names are case-sensitive** in MSE (unlike SSE).
- **Type casting is stricter.** Implicit type conversions that work in SSE may require explicit `CAST` in MSE.
- **Some custom functions are unsupported.** `histogram`, `timeConvert`, and `dateTimeConvertWindowHop` are not available in MSE. See the [troubleshooting page](../troubleshooting/troubleshoot-multi-stage-query-engine.md) for the full list.
- **Default projection names differ.** Function-call projections return names like `EXPR$0` instead of `count(*)`.
- **No spill-to-disk.** Intermediate results that exceed memory cause query failure.

### Workload misfit

These are not bugs or planned improvements. They reflect design boundaries:

- **Full-table-scan ETL joins** -- MSE is not designed for joins that scan billions of rows without selective predicates. Use Trino, Spark, or a similar batch engine.
- **Long-running batch aggregations** -- Queries that run for minutes or hours are outside MSE's design point. Set `timeoutMs` to enforce this boundary.
- **High-concurrency simple queries** -- If the query does not need joins, window functions, or subqueries, SSE is the better choice. It has lower per-query overhead.

## Version milestones

MSE has matured steadily since its introduction:

| Release | Notable MSE changes |
| --- | --- |
| 1.0.0 | MSE introduced as the v2 query engine with support for joins, window functions, and distributed stages. |
| 1.1.0 | Null handling support added for MSE when column-based null storing is enabled. |
| 1.2.0 | Explain plan improvements and additional join strategy support. |
| 1.3.0 | Application-level query quotas added, applicable to MSE workloads. |
| 1.4.0 | Physical Optimizer (Beta), Lite Mode (Beta), workload-based query isolation, stage-level spooling, and broker pruning for MSE. |

Refer to the [Release Notes](../../reference/release-notes/README.md) for the complete changelog for each version.

## Related pages

- [Query Engines (SSE vs MSE)](../../build-with-pinot/querying-and-sql/sse-vs-mse.md)
- [Multi-Stage Query (internals)](../../build-with-pinot/querying-and-sql/multi-stage-query/README.md)
- [Understanding Stages](../../build-with-pinot/querying-and-sql/multi-stage-query/understanding-stages.md)
- [Multistage Lite Mode](../../build-with-pinot/querying-and-sql/multi-stage-query/multistage-lite-mode.md)
- [Physical Optimizer](../../build-with-pinot/querying-and-sql/multi-stage-query/physical-optimizer.md)
- [Query Options](../../build-with-pinot/querying-and-sql/query-execution-controls/query-options.md)
- [Query Quotas](../../build-with-pinot/querying-and-sql/query-execution-controls/query-quotas.md)
- [Workload-Based Query Resource Isolation](../tuning/workload-query-isolation.md)
- [Optimizing Joins](../../build-with-pinot/querying-and-sql/multi-stage-query/optimizing-joins.md)
- [Troubleshoot MSE](../troubleshooting/troubleshoot-multi-stage-query-engine.md)
- [Running Pinot in Production](../running-pinot-in-production.md)
