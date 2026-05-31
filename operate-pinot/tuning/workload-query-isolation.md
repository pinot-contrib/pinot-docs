---
description: Isolate query resources across workloads to prevent noisy-neighbor problems and enforce resource budgets.
---

# Workload-Based Query Resource Isolation

{% hint style="info" %}
This feature was introduced in **Apache Pinot 1.4.0** ([PR #15109](https://github.com/apache/pinot/pull/15109)).
{% endhint %}

## Overview

In multi-tenant Pinot deployments, different query workloads often compete for shared resources such as CPU and memory on broker and server instances. A heavy ad-hoc analytics query can starve latency-sensitive production queries, causing a "noisy-neighbor" problem.

Workload-based query resource isolation addresses this by allowing administrators to:

* Define named workloads with CPU and memory budgets.
* Classify incoming queries into workloads using query options.
* Enforce resource budgets so that one workload cannot consume more than its allocated share.
* Interrupt over-budget queries or reject them at admission time, depending on the isolation mechanism you enable.

The `accounting.workload.*` settings control host-side workload accounting and enforcement on brokers and servers. Pinot can also layer scheduler-based isolation on top through the `binary_workload` and `workload` schedulers.

Pinot provides two scheduler implementations for workload isolation:

| Scheduler | Config Name | Approach |
| --- | --- | --- |
| **BinaryWorkloadScheduler** | `binary_workload` | Splits queries into two classes: primary (unbounded) and secondary (thread-limited). Simple and effective when you only need to protect production queries from ad-hoc traffic. |
| **WorkloadScheduler** | `workload` | Uses the `WorkloadBudgetManager` to enforce per-workload CPU and memory budgets. Supports an arbitrary number of named workloads via the `workloadName` query option. |

## Configuration

### Prerequisites

Workload cost collection relies on thread-level CPU and memory sampling. Enable the following server and broker configs before using workload isolation:

```properties
# Accounting factory (required)
pinot.server.accounting.factory.name=org.apache.pinot.core.accounting.ResourceUsageAccountantFactory

# Thread sampling (required)
pinot.server.accounting.enable.thread.cpu.sampling=true
pinot.server.accounting.enable.thread.memory.sampling=true
pinot.server.accounting.enable.thread.sampling.mse=true

# Instance-level JVM measurement (required)
pinot.server.instance.enableThreadCpuTimeMeasurement=true
pinot.server.instance.enableThreadAllocatedBytesMeasurement=true
```

### Selecting a Scheduler

Set the query scheduler on each **server** instance:

```properties
# For BinaryWorkloadScheduler (primary vs. secondary):
pinot.query.scheduler.name=binary_workload

# For WorkloadScheduler (named workloads with budgets):
pinot.query.scheduler.name=workload
```

### Workload Budget Configs

These configs apply to host-side workload accounting and enforcement on each broker and server under the `accounting.workload.*` prefix. They do not require `pinot.query.scheduler.name=workload`, although the `workload` scheduler can use the same workload names.

| Config | Default | Description |
| --- | --- | --- |
| `accounting.workload.enable.cost.collection` | `false` | Enable workload cost collection for CPU and memory. |
| `accounting.workload.enable.cost.enforcement` | `false` | Enable enforcement of workload budgets. When enabled, Pinot interrupts queries whose workload exhausts its remaining CPU or memory budget within the current enforcement window. |
| `accounting.workload.enforcement.window.ms` | `60000` (1 minute) | Duration of the enforcement window in milliseconds. Budgets are reset at the end of each window. |
| `accounting.workload.sleep.time.ms` | `1` | Sleep interval in milliseconds for the accounting thread. |

### Controller Propagation Configs

The controller computes per-instance workload budgets and pushes them to broker and server admin APIs. These `controller.*` settings let you tune that control-plane work:

| Config | Default | Description |
| --- | --- | --- |
| `controller.enable.instance.change.propagation` | `false` | Automatically recompute and re-propagate server-side workload budgets when `InstancePartitions` change, such as after server rebalances or serving-instance membership changes. |
| `controller.enable.table.change.propagation` | `false` | Automatically recompute and re-propagate broker-side workload budgets when the `brokerResource` table-to-broker mapping changes. |
| `controller.workload.propagation.requestsPerSecond` | `1000.0` | Rate limit for outbound workload propagation requests from the controller to brokers and servers. |
| `controller.workload.executor.threads` | `5` | Threads used to compute workload-to-instance budget assignments on the controller. |
| `controller.workload.executor.queueSize` | `10000` | Queue size for controller workload propagation tasks. |
| `controller.workload.http.executor.threads` | `5` | Threads used by the controller's async HTTP workload client for callback processing. |
| `controller.workload.http.executor.queueSize` | `10000` | Queue size for controller HTTP workload callback handling. |
| `controller.workload.propagation.timeoutSeconds` | `120` | Timeout for controller-side workload propagation and cost computation tasks. |

### Secondary Workload Configs

For a simpler setup that only distinguishes between primary and secondary queries:

| Config | Default | Description |
| --- | --- | --- |
| `accounting.secondary.workload.name` | `defaultSecondary` | Name assigned to the secondary workload budget. |
| `accounting.secondary.workload.cpu.percentage` | `0.0` | Fraction of total CPU capacity allocated to the secondary workload (e.g., `0.1` for 10%). The budget is computed as `enforcementWindow * 1,000,000 * availableProcessors * percentage`. Set to a value greater than 0 to activate. |

### BinaryWorkloadScheduler Configs

When using the `binary_workload` scheduler, these additional configs control secondary query behavior:

| Config | Default | Description |
| --- | --- | --- |
| `binarywlm.maxSecondaryRunnerThreads` | `5` | Maximum number of runner threads dedicated to processing secondary queries concurrently. |
| `binarywlm.maxPendingSecondaryQueries` | `20` | Maximum number of secondary queries that can be queued. Queries beyond this limit receive an out-of-capacity error. |
| `binarywlm.secondaryQueueQueryTimeout` | `40` (seconds) | Time in seconds before a queued secondary query expires and is removed from the queue. |
| `binarywlm.queueWakeupMs` | `1` | Interval in milliseconds at which the scheduler checks for schedulable secondary queries. |

### Controller APIs

Named workload configs (with CPU and memory budgets) are managed through the controller REST API:

```
GET    /queryWorkloadConfigs                           # List all workload configs
GET    /queryWorkloadConfigs/{queryWorkloadName}      # Get a specific workload config
GET    /queryWorkloadConfigs/instance/{instanceName}  # Show the computed budgets for one broker/server instance
POST   /queryWorkloadConfigs                           # Create or update a workload config
DELETE /queryWorkloadConfigs/{queryWorkloadName}      # Delete a workload config
POST   /queryWorkloadConfigs/refresh?...              # Recompute and re-push budgets after topology changes
```

A workload config defines resource budgets and propagation rules. Example:

```json
{
  "queryWorkloadName": "analytics-workload",
  "nodeConfigs": [
    {
      "nodeType": "brokerNode",
      "enforcementProfile": {
        "cpuCostNs": 1500,
        "memoryCostBytes": 12000
      },
      "propagationScheme": {
        "propagationType": "table",
        "propagationEntities": [
          {
            "entity": "myTable",
            "cpuCostNs": 1500,
            "memoryCostBytes": 12000
          }
        ]
      }
    },
    {
      "nodeType": "serverNode",
      "enforcementProfile": {
        "cpuCostNs": 5000,
        "memoryCostBytes": 40000
      },
      "propagationScheme": {
        "propagationType": "tenant",
        "propagationEntities": [
          {
            "entity": "analyticsTenant",
            "cpuCostNs": 5000,
            "memoryCostBytes": 40000
          }
        ]
      }
    }
  ]
}
```

Workload configs are stored in ZooKeeper under `/CONFIGS/QUERYWORKLOAD`. The controller is the source of truth for the cluster-wide definition, and it computes the per-instance budgets each broker or server should enforce.

**Propagation schemes** control which instances receive a workload config:

* **TABLE**: Config is pushed to all instances serving the specified tables.
* **TENANT**: Config is pushed to all instances belonging to the specified tenants.

**Cost splitting**: The controller evenly divides a workload's total resource budget across all eligible instances. For example, if a workload has a CPU budget of 1000 ns and there are 4 servers, each server receives a budget of 250 ns.

### Propagation Lifecycle

1. The controller stores the workload definition in ZooKeeper and computes per-instance budgets for the current broker and server topology.
2. The controller pushes those computed budgets to broker and server admin APIs over HTTP(S) by calling each instance's `/queryWorkloadConfigs` endpoint.
3. Brokers and servers also fetch their assigned budgets asynchronously during startup from `GET /queryWorkloadConfigs/instance/{instanceName}`, so a restart does not need to wait for a later manual refresh.
4. For local debugging, each broker and server admin API exposes `GET /queryWorkloadConfigs` and `GET /queryWorkloadConfigs?workloadNames=...` so you can inspect the budgets currently loaded on that instance.

### Refreshing Budgets After Topology Changes

Per-instance budgets depend on which brokers or servers currently serve a workload's tables or tenants. When that serving topology changes, the budget split can change too.

Use the controller refresh API to recompute and re-push budgets without recreating the workload config:

```bash
curl -X POST "http://localhost:9000/queryWorkloadConfigs/refresh?resourceType=table&resourceNames=myTable_REALTIME&nodeType=serverNode"
```

You can also refresh by `workload` or `tenant` instead of `table`. The optional `nodeType` filter accepts `brokerNode` or `serverNode`.

If you want Pinot to do this automatically after serving-instance changes, enable:

* `controller.enable.instance.change.propagation=true` to refresh server-side budgets when `InstancePartitions` change.
* `controller.enable.table.change.propagation=true` to refresh broker-side budgets when the `brokerResource` mapping changes.

See [Controller API Examples](../../reference/api-reference/controller-api.md#query-workload-propagation) for end-to-end `curl` examples.

## Query Options

### workloadName

Assigns a query to a named workload for CPU and memory accounting and workload budget enforcement. When the `workload` scheduler is enabled, the same option also selects the scheduler-managed workload.

```sql
SET workloadName = 'analytics-workload';
SELECT COUNT(*) FROM myTable WHERE city = 'San Francisco'
```

When a query specifies a `workloadName`, Pinot charges the query's broker and server CPU or memory usage to that named workload. If accounting-based enforcement is enabled and the workload budget is exhausted, Pinot interrupts queries in that workload. When the `workload` scheduler is enabled, the same workload name is also used for scheduler-side admission control.

Queries that do not specify a `workloadName` are treated as belonging to the `default` workload and are always admitted (no budget enforcement).

### isSecondaryWorkload

Marks a query as belonging to the secondary workload. Use this with either the `binary_workload` or `workload` scheduler.

```sql
SET isSecondaryWorkload = 'true';
SELECT * FROM myTable WHERE id = 12345
```

With the `binary_workload` scheduler, secondary queries are routed to a dedicated queue with limited runner threads and bounded parallelism. With the `workload` scheduler, the `isSecondaryWorkload` flag maps the query to the configured secondary workload name (default: `defaultSecondary`) for budget enforcement.

## How It Works

### BinaryWorkloadScheduler

The `BinaryWorkloadScheduler` classifies all queries into exactly two categories:

1. **Primary queries** (default): Executed immediately using unbounded resources. These are your production, latency-sensitive queries.
2. **Secondary queries** (tagged with `isSecondaryWorkload=true`): Placed into a dedicated `SecondaryWorkloadQueue` and executed with constrained resources:
   * Limited number of concurrent runner threads (`binarywlm.maxSecondaryRunnerThreads`).
   * Limited number of worker threads per query and across all in-progress secondary queries.
   * A bounded pending queue (`binarywlm.maxPendingSecondaryQueries`) with a timeout for stale queries.

This two-tier approach is straightforward and effective when you need to protect production traffic from exploratory or ad-hoc queries.

### WorkloadScheduler

The `WorkloadScheduler` provides finer-grained control using the `WorkloadBudgetManager`:

1. Each workload has a CPU and memory budget for a configurable enforcement window (default: 60 seconds).
2. When a query arrives, the scheduler checks `canAdmitQuery(workloadName)`.
3. If the workload's remaining CPU or memory budget is positive, the query is admitted.
4. If the budget is exhausted, the query is rejected and a `WORKLOAD_BUDGET_EXCEEDED` metric is emitted.
5. At the end of each enforcement window, all workload budgets are automatically reset.

Resource usage (CPU time, allocated bytes) is tracked at the thread level and charged against the workload budget during query execution.

## Metrics and Monitoring

### BinaryWorkloadScheduler Metrics

| Metric | Type | Description |
| --- | --- | --- |
| `NUM_SECONDARY_QUERIES` | Meter (per-table) | Number of secondary queries received. |
| `NUM_SECONDARY_QUERIES_SCHEDULED` | Meter (per-table) | Number of secondary queries that were dequeued and scheduled for execution. |
| `SECONDARY_Q_WAIT_TIME_MS` | Timer (per-table) | Time a secondary query spent waiting in the queue before being scheduled. |
| `SECONDARY_WORKLOAD_QUERY_TOTAL_TIME_MS` | Timer (global) | End-to-end broker query time for secondary-workload queries only. |
| `SECONDARY_WORKLOAD_BROKER_RESPONSES_WITH_TIMEOUTS` | Meter (global) | Number of secondary-workload queries that timed out. |
| `SECONDARY_WORKLOAD_BROKER_RESPONSES_WITH_PARTIAL_SERVERS_RESPONDED` | Meter (global) | Number of secondary-workload queries that returned partial results because not all servers responded. |

These broker metrics are the secondary-workload counterparts of the standard broker timeout, partial-response, and total-query-time metrics, so they let you separate ad-hoc or background query health from primary query traffic.

### WorkloadScheduler Metrics

| Metric | Type | Description |
| --- | --- | --- |
| `WORKLOAD_BUDGET_EXCEEDED` | Meter (per-workload, per-table, global) | Number of queries rejected because the workload budget was exhausted. |

Monitor these metrics to detect workload saturation and tune budgets accordingly.

## Tuning Guidance

### Choosing a Scheduler

* Use `binary_workload` when you have a simple split between production and ad-hoc queries. It requires minimal configuration and provides strong isolation through thread limiting.
* Use `workload` when you need to isolate multiple distinct workloads with individual CPU and memory budgets.

### Sizing Budgets

* Start with the `accounting.workload.enable.cost.collection=true` flag and `accounting.workload.enable.cost.enforcement=false` to observe resource usage patterns before enforcing budgets.
* Monitor the `WORKLOAD_BUDGET_EXCEEDED` metric. A high rate of rejections indicates the budget is too low or the enforcement window is too short.
* The enforcement window (`accounting.workload.enforcement.window.ms`) controls the granularity of budget enforcement. Shorter windows provide tighter isolation but may cause more bursty rejections. The default of 60 seconds works well for most deployments.

### BinaryWorkloadScheduler Tuning

* Increase `binarywlm.maxSecondaryRunnerThreads` if secondary queries are timing out in the queue but server CPU is not saturated.
* Increase `binarywlm.maxPendingSecondaryQueries` if you see frequent out-of-capacity errors for secondary queries.
* Decrease `binarywlm.secondaryQueueQueryTimeout` if stale secondary queries are consuming queue capacity.

### Secondary Workload CPU Budget

* The `accounting.secondary.workload.cpu.percentage` config allocates a percentage of total CPU to secondary queries. For example, setting it to `0.1` (10%) on a 16-core server with a 60-second window yields a budget of approximately `96 billion` CPU nanoseconds per window.
* Set this to `0.0` (the default) to disable secondary workload budgeting entirely.
