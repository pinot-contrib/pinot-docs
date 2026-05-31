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

The `accounting.workload.*` settings control host-side workload accounting and enforcement on brokers and servers.

### How it differs from related features

Workload isolation sits alongside, and is complementary to, other resource-management mechanisms in Pinot:

| Feature                           | Limits                                                            | Scope                                                                |
| --------------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Query Quotas**                  | QPS (queries per second)                                          | Per table, database, or application                                  |
| **Query Scheduling**              | Concurrency / fairness inside a single server                     | Per server, across resource groups                                   |
| **OOM Protection (auto-killing)** | JVM heap pressure on a single server                              | Per server, reactive &mdash; kills the most expensive query under pressure |
| **Workload Query Isolation**      | Cluster-wide CPU&nbsp;ns and memory&nbsp;bytes per named workload | Cluster-wide; enforced at every broker and server                    |

Quotas cap _how often_ queries can run. Workload isolation caps _how much resource_ a class of queries can consume in a time window.

## How It Works

### Workload configuration model

A `QueryWorkloadConfig` is a JSON document stored in ZooKeeper under `/CONFIGS/QUERYWORKLOAD`. It describes one workload and lists the CPU and memory budget that workload is allowed to consume on broker nodes and on server nodes.

* **`QueryWorkloadConfig`** &mdash; top level. Identified by `queryWorkloadName` (unique cluster-wide) and a list of `nodeConfigs`.
* **`NodeConfig`** &mdash; one entry per node type (`brokerNode` and/or `serverNode`). Carries an `enforcementProfile` and a `propagationScheme`.
* **`EnforcementProfile`** &mdash; the total `cpuCostNs` and `memoryCostBytes` allowed for that node type, per enforcement window.
* **`PropagationScheme`** &mdash; how the total budget should be split across instances. `propagationType` is either `table` (split among instances serving each listed table) or `tenant` (split among instances in each listed tenant). `propagationEntities` lists those tables or tenants, optionally with per-entity sub-budgets.

### Architecture

The controller is the source of truth for cluster-wide workload definitions. It computes per-instance budgets and pushes them to every broker and server. Each instance tracks usage and enforces budgets locally.

```
                   ┌──────────────────────────────┐
                   │   Pinot Controller           │
                   │                              │
   user writes ──► │ QueryWorkloadManager         │
                   │   • stores config in ZK      │
                   │   • splits budget per host   │
                   │   • POSTs to brokers/servers │
                   └──────────────┬───────────────┘
                                  │ HTTP refresh
                ┌─────────────────┼─────────────────┐
                ▼                                   ▼
        ┌───────────────┐                  ┌───────────────┐
        │   Brokers     │                  │   Servers     │
        │               │                  │               │
        │ WorkloadBudget│                  │ WorkloadBudget│
        │   Manager     │                  │   Manager     │
        │               │                  │ + Workload-   │
        │ Charges CPU/  │                  │   Scheduler   │
        │ mem during    │                  │ (admission    │
        │ compile +     │                  │  check)       │
        │ reduce        │                  │ Charges CPU/  │
        │               │                  │ mem during    │
        │               │                  │ prune/plan/   │
        │               │                  │ execute       │
        └───────────────┘                  └───────────────┘
```

The default cost splitter divides each entity's budget _equally_ among the instances that serve it. So if a TABLE-scoped workload gives `myTable_OFFLINE` 1,000,000 ns of CPU and three servers host that table, each of those servers gets a per-window budget of 333,333 ns for that workload.

### Broker enforcement

Each broker runs a `WorkloadBudgetManager` (default implementation: `DefaultWorkloadBudgetManager`). On every query, the thread accountant samples CPU time and allocated bytes, and the broker charges those values for the compilation and reduce phases against the workload named in the query's `workloadName` query option.

### Server enforcement

Each server runs the same `WorkloadBudgetManager` plus the `WorkloadScheduler` for admission control:

1. When a query arrives, `WorkloadScheduler.canAdmitQuery()` checks the workload's _remaining_ CPU budget. If it has dropped to zero or below, the query is rejected immediately with `QueryErrorCode.SERVER_RESOURCE_LIMIT_EXCEEDED`.
2. If the query is admitted, the server charges CPU time and allocated bytes during pruning, planning, and execution against the workload's budget.
3. Already-running queries are **not** killed mid-flight even if the workload's remaining budget goes negative.

### Budget windows and overage behavior

A scheduled task resets every workload's remaining budget to its configured value every `accounting.workload.enforcement.window.ms` (default 60 seconds).

Within the current window:

* In-flight queries continue to run; they are not killed mid-execution.
* CPU and memory continue to be charged, so the workload's remaining budget can go negative.
* **New** queries on that workload are rejected at admission. The `WORKLOAD_BUDGET_EXCEEDED` meter increments.

At the start of the next window the budget is reset and new queries are admitted again.

{% hint style="warning" %}
Because overage is allowed within a window, total CPU consumption for a workload can briefly exceed its configured `cpuCostNs`. Treat the budget as a steady-state target, not a hard per-query limit. Shorten the enforcement window if you need tighter control.
{% endhint %}

## Getting Started

### 1. Enable prerequisites on brokers and servers

Workload cost collection relies on thread-level CPU and memory sampling. Add the following to `broker.conf` and `server.conf` &mdash; without these, samples are zero and enforcement will never reject a query:

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

Use the matching `pinot.broker.*` keys on brokers.

### 2. Tag queries with a workload

Queries opt into a workload via the `workloadName` query option:

```sql
SET workloadName = 'analytics-workload';
SELECT COUNT(*) FROM myTable WHERE city = 'San Francisco'
```

When a query specifies a `workloadName`, Pinot charges the query's broker and server CPU and memory usage to that named workload. If enforcement is enabled and the workload's budget is exhausted, the next query on that workload is rejected at admission.

Queries that do not specify a `workloadName` are treated as belonging to the `default` workload and are always admitted (no budget enforcement).

### 3. Define a named workload

A workload is submitted as a single JSON document via the controller REST API:

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

Field reference:

| Field                                                                                  | Type   | Notes                                                                                                                                                |
| -------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `queryWorkloadName`                                                                    | string | Unique cluster-wide. The value queries put in their `workloadName` query option.                                                                      |
| `nodeConfigs[].nodeType`                                                               | enum   | `brokerNode` or `serverNode`.                                                                                                                         |
| `nodeConfigs[].enforcementProfile.cpuCostNs`                                           | long   | Total CPU budget (nanoseconds) for this node type, per enforcement window.                                                                            |
| `nodeConfigs[].enforcementProfile.memoryCostBytes`                                     | long   | Total memory budget (bytes) for this node type, per enforcement window.                                                                               |
| `nodeConfigs[].propagationScheme.propagationType`                                      | enum   | `table` or `tenant`. Determines what the listed `entity` values refer to.                                                                              |
| `nodeConfigs[].propagationScheme.propagationEntities[].entity`                         | string | Table name (with or without `_OFFLINE` / `_REALTIME` suffix) or tenant name. If a table name has no suffix, the budget applies to both types.         |
| `nodeConfigs[].propagationScheme.propagationEntities[].cpuCostNs` / `memoryCostBytes`  | long   | Optional per-entity sub-budget; inherits from the parent enforcement profile if omitted.                                                              |

See the [Controller REST API](#controller-rest-api) section for the `POST /queryWorkloadConfigs` call to submit this document.

### 4. Recommended rollout

Don't flip enforcement on cold. Run the feature in observation mode first:

1. Turn on `accounting.workload.enable.cost.collection=true` cluster-wide, but leave `accounting.workload.enable.cost.enforcement=false`.
2. Observe the `WORKLOAD_QUERIES` and `WORKLOAD_BUDGET_EXCEEDED` (in dry-run, this will be zero) metrics for at least one busy hour.
3. Pick `cpuCostNs` and `memoryCostBytes` for each workload from that data, with headroom.
4. Submit the workload configs via `POST /queryWorkloadConfigs`.
5. Flip `accounting.workload.enable.cost.enforcement=true`.

## Configuration Reference

### Workload Budget Configs

Host-side accounting and enforcement on each broker and server. These do not require `pinot.query.scheduler.name=workload`, although the `workload` scheduler can use the same workload names.

| Config                                       | Default            | Description                                                                                                                                                                          |
| -------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `accounting.workload.enable.cost.collection` | `false`            | Enable workload cost collection for CPU and memory. Required before any of the rest does useful work.                                                                                 |
| `accounting.workload.enable.cost.enforcement` | `false`            | Enable enforcement of workload budgets. When enabled, Pinot interrupts queries whose workload exhausts its remaining CPU or memory budget within the current enforcement window.       |
| `accounting.workload.enforcement.window.ms`  | `60000` (1 minute) | Duration of the enforcement window in milliseconds. Budgets are reset at the end of each window.                                                                                       |
| `accounting.workload.sleep.time.ms`          | `1`                | Sleep interval in milliseconds for the accounting thread.                                                                                                                              |
| `accounting.workload.enable.cost.emission`   | `false`            | When `true`, per-workload cost is also emitted as metrics for monitoring.                                                                                                              |

### Controller Propagation Configs

The controller computes per-instance budgets and pushes them to brokers and servers. These flags gate **automatic** re-propagation on topology changes &mdash; both default off, so without them you must call the `refresh` endpoint manually whenever instances or table-to-broker mappings change.

| Config                                              | Default  | Description                                                                                                                                                                              |
| --------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `controller.enable.instance.change.propagation`     | `false`  | Automatically recompute and re-propagate server-side workload budgets when `InstancePartitions` change (e.g. after server rebalances). Recommended `true` for production.                |
| `controller.enable.table.change.propagation`        | `false`  | Automatically recompute and re-propagate broker-side workload budgets when the `brokerResource` table-to-broker mapping changes. Recommended `true` for production.                       |
| `controller.workload.propagation.requestsPerSecond` | `1000.0` | Rate limit for outbound workload propagation requests from the controller to brokers and servers.                                                                                         |
| `controller.workload.executor.threads`              | `5`      | Threads used to compute workload-to-instance budget assignments on the controller.                                                                                                        |
| `controller.workload.executor.queueSize`            | `10000`  | Queue size for controller workload propagation tasks. When full, new tasks are dropped and `QUERY_WORKLOAD_REQUEST_DROPPED` fires.                                                        |
| `controller.workload.http.executor.threads`         | `5`      | Threads used by the controller's async HTTP workload client for callback processing.                                                                                                      |
| `controller.workload.http.executor.queueSize`       | `10000`  | Queue size for controller HTTP workload callback handling.                                                                                                                                |
| `controller.workload.propagation.timeoutSeconds`    | `120`    | Timeout for controller-side workload propagation and cost computation tasks.                                                                                                              |

### Async HTTP client tuning

The controller uses an async HTTP client to push budgets to brokers and servers. The defaults are sized for a 40-core controller handling ~50 propagation requests per second. Touch these only when you see connection-related propagation failures or `QUERY_WORKLOAD_REQUEST_DROPPED` is non-zero.

| Config                                            | Default | Description                                                              |
| ------------------------------------------------- | ------- | ------------------------------------------------------------------------ |
| `workload.async.http.client.maxConnTotal`         | `1000`  | Maximum concurrent HTTP connections from the controller across all hosts. |
| `workload.async.http.client.maxConnPerRoute`      | `2`     | Maximum concurrent connections to any single broker / server host.        |
| `workload.async.http.client.connectionTimeoutMs`  | `60000` | TCP connect timeout for a propagation request.                            |
| `workload.async.http.client.socketTimeoutMs`      | `60000` | Socket read timeout while waiting for the broker / server to respond.     |
| `workload.async.http.client.requestTimeoutMs`     | `60000` | End-to-end timeout for a single HTTP propagation request.                 |
| `workload.async.http.client.ioThreadCount`        | `1`     | I/O thread count for the async HTTP client.                               |

## Controller REST API

All endpoints live on the Pinot controller and operate on workload configs stored in ZK.

| Method | Path                                                                       | Purpose                                                                                                       |
| ------ | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| GET    | `/queryWorkloadConfigs`                                                    | List all workload configs in the cluster.                                                                     |
| GET    | `/queryWorkloadConfigs/{queryWorkloadName}`                                | Fetch one workload by name.                                                                                   |
| GET    | `/queryWorkloadConfigs/instance/{instanceName}`                            | Return the per-workload budget allocated to one broker or server (useful for debugging splits).                |
| POST   | `/queryWorkloadConfigs`                                                    | Create or update a workload. Body is a `QueryWorkloadConfig` JSON.                                             |
| DELETE | `/queryWorkloadConfigs/{queryWorkloadName}`                                | Delete a workload and tell every instance to forget its budget.                                                |
| POST   | `/queryWorkloadConfigs/refresh?resourceType=&resourceNames=&nodeType=`     | Force re-propagation. `resourceType` is one of `workload`, `table`, `tenant`. `nodeType` is optional.          |

### Create or update a workload

```bash
curl -X POST 'http://localhost:9000/queryWorkloadConfigs' \
  -H 'Content-Type: application/json' \
  -d @analytics-workload.json
```

### Read

```bash
# Fetch a single workload config
curl 'http://localhost:9000/queryWorkloadConfigs/analytics-workload'

# See what budget the controller has allocated to one server
curl 'http://localhost:9000/queryWorkloadConfigs/instance/Server_192.0.2.10_8098'
```

### Refresh after a topology change

Per-instance budgets depend on which brokers or servers currently serve a workload's tables or tenants. When that serving topology changes, the budget split can change too. Use the refresh API to recompute and re-push without recreating the workload config:

```bash
curl -X POST "http://localhost:9000/queryWorkloadConfigs/refresh?resourceType=table&resourceNames=myTable_REALTIME&nodeType=serverNode"
```

`resourceType` accepts `workload`, `table`, or `tenant`. The optional `nodeType` filter accepts `brokerNode` or `serverNode`.

To let Pinot do this automatically on serving-instance changes, enable `controller.enable.instance.change.propagation` and `controller.enable.table.change.propagation`. See [Controller API Examples](../../reference/api-reference/controller-api.md#query-workload-propagation) for end-to-end `curl` examples.

### Broker / server debug endpoints

Brokers and servers also expose `/queryWorkloadConfigs` (POST / GET / DELETE) on their own admin ports. The controller is the only client that calls them in normal operation, but they are useful for debugging:

* `GET /queryWorkloadConfigs?workloadNames=analytics-workload` on a specific broker returns the live budget statistics (`cpuBudgetNs`, `cpuRemainingNs`, `memoryBudgetBytes`, `memoryRemainingBytes`) for that workload on that one host.
* `POST /queryWorkloadConfigs` accepts a JSON map of `workloadName` &rarr; `{cpuCostNs, memoryCostBytes}` to manually inject a budget &mdash; the controller normally drives this.
* `DELETE /queryWorkloadConfigs?workloadNames=...` removes the workload's in-memory budget from that host.

### Propagation lifecycle

1. The controller stores the workload definition in ZooKeeper and computes per-instance budgets for the current broker and server topology.
2. The controller pushes those computed budgets to broker and server admin APIs over HTTP(S) by calling each instance's `/queryWorkloadConfigs` endpoint.
3. Brokers and servers also fetch their assigned budgets asynchronously during startup from `GET /queryWorkloadConfigs/instance/{instanceName}`, so a restart does not need to wait for a later manual refresh.
4. When the `controller.enable.*.change.propagation` flags are on, the controller re-runs the propagation flow automatically whenever the relevant ZK state changes.

## Monitoring

### Workload budget metrics

| Metric                     | Type                                       | Description                                                                                |
| -------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------ |
| `WORKLOAD_BUDGET_EXCEEDED` | Meter (per-workload, per-table, global)    | Number of queries rejected because the workload budget was exhausted.                       |
| `WORKLOAD_QUERIES`         | Meter (server)                             | Queries handled per workload. Useful for sizing budgets before turning enforcement on.      |

### Controller propagation metrics

| Metric                                          | Type                | Description                                                                                                       |
| ----------------------------------------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `QUERY_WORKLOAD_PROPAGATION_COUNT`              | Meter (controller)  | Workload config propagations sent to instances.                                                                    |
| `QUERY_WORKLOAD_PROPAGATION_ERROR`              | Meter (controller)  | Propagations that failed (network, instance down, etc.).                                                           |
| `QUERY_WORKLOAD_REQUEST_DROPPED`                | Meter (controller)  | Propagations dropped because the work queue was full &mdash; increase `controller.workload.executor.queueSize`.    |
| `QUERY_WORKLOAD_PROPAGATE_TIME_MS`              | Timer (controller)  | End-to-end propagation latency.                                                                                    |
| `QUERY_WORKLOAD_COMPUTE_INSTANCE_COST_TIME_MS`  | Timer (controller)  | Latency of computing each instance's share of a workload budget.                                                   |

## Tuning & Operational Notes

### Sizing budgets

* Start with `accounting.workload.enable.cost.collection=true` and `accounting.workload.enable.cost.enforcement=false` to observe resource usage patterns before enforcing budgets.
* Monitor `WORKLOAD_BUDGET_EXCEEDED`. A high rate of rejections indicates the budget is too low or the enforcement window is too short.
* Shorter `accounting.workload.enforcement.window.ms` windows provide tighter isolation but may cause more bursty rejections. The default of 60 seconds works well for most deployments.

## See Also

* [OOM Protection Using Automatic Query Killing](../oom-protection-using-automatic-query-killing.md)
* [Query Scheduling](query-scheduling.md)
* [Query Quotas](../../build-with-pinot/querying-and-sql/query-execution-controls/query-quotas.md)
* [Query Options](../../build-with-pinot/querying-and-sql/query-execution-controls/query-options.md)
* [Tenant](../../basics/components/cluster/tenant.md)
* [Controller API: Query Workload Propagation](../../reference/api-reference/controller-api.md#query-workload-propagation)
