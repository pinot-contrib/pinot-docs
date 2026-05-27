---
description: >-
  Classify queries into named workloads and enforce per-workload CPU and memory
  budgets across Pinot brokers and servers.
---

# Query Workload Isolation

Query Workload Isolation lets a Pinot operator group queries into named **workloads** (for example `analytics`, `dashboards`, `adhoc`) and assign each workload a CPU and memory budget. Brokers and servers track the resources every workload consumes during a configurable enforcement window, and reject new queries from a workload once that workload has exhausted its budget. This prevents one expensive or runaway workload from starving the others.

* Design doc: [https://tinyurl.com/2p9vuzbd](https://tinyurl.com/2p9vuzbd)

The feature is **OFF by default**. Both _cost collection_ and _cost enforcement_ are independent toggles &mdash; you can enable collection first, observe per-workload usage in metrics, and then enable enforcement once you have sized the budgets.

## How it differs from related features

Query Workload Isolation sits alongside, and is complementary to, other resource-management mechanisms in Pinot:

| Feature                             | Limits                                                              | Scope                                                                |
| ----------------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Query Quotas**                    | QPS (queries per second)                                            | Per table, database, or application                                  |
| **Query Scheduling**                | Concurrency / fairness inside a single server                       | Per server, across resource groups                                   |
| **OOM Protection (auto-killing)**   | JVM heap pressure on a single server                                | Per server, reactive — kills the most expensive query under pressure |
| **Query Workload Isolation**        | Cluster-wide CPU&nbsp;ns and memory&nbsp;bytes per named workload   | Cluster-wide; enforced at every broker and server                    |

Quotas cap _how often_ queries can run. Workload Isolation caps _how much resource_ a class of queries can consume in a time window.

## How it works

A `QueryWorkloadConfig` is a JSON document stored in ZooKeeper. It describes one workload and lists the CPU and memory budget that workload is allowed to consume on broker nodes and on server nodes. The controller fans the config out to the relevant instances, and each instance tracks usage locally.

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

### Workload configuration model

* **`QueryWorkloadConfig`** — top level. Identified by `queryWorkloadName` (unique cluster-wide) and a list of `nodeConfigs`.
* **`NodeConfig`** — one entry per node type (`brokerNode` and/or `serverNode`). Carries an `enforcementProfile` and a `propagationScheme`.
* **`EnforcementProfile`** — the total `cpuCostNs` and `memoryCostBytes` allowed for that node type, per enforcement window.
* **`PropagationScheme`** — how the total budget should be split across instances. `propagationType` is either `TABLE` (split among instances serving each listed table) or `TENANT` (split among instances in each listed tenant). `propagationEntities` lists those tables or tenants, optionally with per-entity sub-budgets.

### Controller responsibilities

`QueryWorkloadManager` (in `pinot-controller`) owns the workload lifecycle:

1. Persists workload configs in the ZK PropertyStore.
2. Uses the cost-split strategy to compute the per-instance share of each workload's budget, based on which instances currently serve a given table or tenant.
3. POSTs the resulting per-instance budget map to each broker and server's `/queryWorkloadConfigs` endpoint.
4. Listens to ZK changes on instance partitions, broker resources, and tenant membership, and re-propagates affected workloads automatically.

The default cost splitter divides each entity's budget _equally_ among the instances that serve it. So if a TABLE-scoped workload gives `myTable_OFFLINE` 1,000,000 ns of CPU and three servers host that table, each of those servers gets a per-window budget of 333,333 ns for that workload.

### Broker and server enforcement

Each broker and server runs a `WorkloadBudgetManager` (default implementation: `DefaultWorkloadBudgetManager`):

* **Cost collection** &mdash; on each query, the thread accountant samples CPU time and allocated bytes. The broker charges those values for compilation and reduce; the server charges them for pruning, planning, and execution. The charges accrue against the workload named in the query's `workloadName` query option (default: `default`).
* **Admission control** &mdash; on the server, `WorkloadScheduler.canAdmitQuery()` checks the workload's _remaining_ CPU budget. If it has dropped to zero or below, the new query is rejected immediately with `QueryErrorCode.SERVER_RESOURCE_LIMIT_EXCEEDED` and the `WORKLOAD_BUDGET_EXCEEDED` meter is incremented. Already-running queries are **not** killed mid-flight.
* **Budget windows** &mdash; a scheduled task resets every workload's remaining budget to its initial value every `workload.enforcement.window.ms` (default 60 seconds). Overage **within** a window is allowed (the remaining budget can go negative); only queries arriving in the **next** window get rejected.

## Prerequisites

Before turning on cost collection or enforcement, the resource-accounting infrastructure has to be enabled on every broker and server, otherwise the workload manager has nothing to charge. Set these in `broker.conf` and `server.conf`:

```
# Per-thread CPU / memory measurement (instance-level)
pinot.broker.instance.enableThreadCpuTimeMeasurement=true
pinot.broker.instance.enableThreadAllocatedBytesMeasurement=true
pinot.server.instance.enableThreadCpuTimeMeasurement=true
pinot.server.instance.enableThreadAllocatedBytesMeasurement=true

# Resource-usage accountant (replaces the default no-op accountant)
pinot.query.scheduler.accounting.factory.name=org.apache.pinot.core.accounting.ResourceUsageAccountantFactory
pinot.query.scheduler.accounting.enable.thread.cpu.sampling=true
pinot.query.scheduler.accounting.enable.thread.memory.sampling=true
```

{% hint style="warning" %}
If `accounting.factory.name` is left at the default no-op accountant, CPU and memory samples will be zero, so collection will report nothing and enforcement will never reject a query.
{% endhint %}

## Enabling the feature

The workload-isolation toggles live in the `accounting` namespace:

| Config                                    | Default            | Description                                                                                                                                                |
| ----------------------------------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `accounting.workload.enable.cost.collection` | `false`         | When `true`, each broker and server tracks CPU and memory consumed per workload. Must be on for any of the rest to do useful work.                          |
| `accounting.workload.enable.cost.enforcement` | `false`        | When `true`, new queries are rejected once their workload has exhausted its budget for the current window. Leave `false` while sizing budgets.              |
| `accounting.workload.enforcement.window.ms` | `10000` (10 sec)  | Length of the budget window. Budgets reset at the end of every window.                                                                                       |
| `accounting.workload.sleep.time.ms`       | `100`              | Sleep between background budget-enforcement passes.                                                                                                          |
| `accounting.workload.enable.cost.emission` | `false`            | When `true`, per-workload cost is also emitted as metrics for monitoring.                                                                                    |
| `accounting.secondary.workload.name`      | `defaultSecondary` | Name reserved for the implicit lower-priority workload used by the legacy `BinaryWorkloadScheduler` / `SET isSecondaryWorkload=true` option.                  |
| `accounting.secondary.workload.cpu.percentage` | `0.0`         | Fraction (0.0&ndash;1.0) of total server CPU that the secondary workload is allowed to use.                                                                  |


**Recommended rollout**: turn on `enable.cost.collection` only, observe the `WORKLOAD_QUERIES` and per-workload cost metrics for at least one busy hour, size each workload's `cpuCostNs` and `memoryCostBytes` from that data, and only then flip `enable.cost.enforcement` to `true`.


## Defining a workload

A workload is defined as a single JSON document and submitted via the controller REST API. The example below creates a workload named `analytics` with separate budgets for brokers (split across two tables) and servers (split across two tenants):

```json
{
  "queryWorkloadName": "analytics",
  "nodeConfigs": [
    {
      "nodeType": "brokerNode",
      "enforcementProfile": {
        "cpuCostNs": 1000000,
        "memoryCostBytes": 10000000
      },
      "propagationScheme": {
        "propagationType": "TABLE",
        "propagationEntities": [
          { "entity": "myTable_OFFLINE",  "cpuCostNs": 500000, "memoryCostBytes": 5000000 },
          { "entity": "myTable_REALTIME", "cpuCostNs": 500000, "memoryCostBytes": 5000000 }
        ]
      }
    },
    {
      "nodeType": "serverNode",
      "enforcementProfile": {
        "cpuCostNs": 2000000,
        "memoryCostBytes": 20000000
      },
      "propagationScheme": {
        "propagationType": "TENANT",
        "propagationEntities": [
          { "entity": "DefaultTenant", "cpuCostNs": 1000000, "memoryCostBytes": 10000000 },
          { "entity": "PremiumTenant", "cpuCostNs": 1000000, "memoryCostBytes": 10000000 }
        ]
      }
    }
  ]
}
```

Field reference:

| Field                                       | Type     | Notes                                                                                                                                              |
| ------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `queryWorkloadName`                         | string   | Unique cluster-wide. This is the value queries put in their `workloadName` query option.                                                            |
| `nodeConfigs[].nodeType`                    | enum     | `brokerNode` or `serverNode`.                                                                                                                       |
| `nodeConfigs[].enforcementProfile.cpuCostNs` | long    | Total CPU budget (nanoseconds) for this node type, per enforcement window.                                                                          |
| `nodeConfigs[].enforcementProfile.memoryCostBytes` | long | Total memory budget (bytes) for this node type, per enforcement window.                                                                          |
| `nodeConfigs[].propagationScheme.propagationType` | enum  | `TABLE` or `TENANT`. Determines what the listed `entity` values refer to.                                                                            |
| `nodeConfigs[].propagationScheme.propagationEntities[].entity` | string | Table name (with or without `_OFFLINE` / `_REALTIME` suffix) or tenant name. If the table name has no suffix, the budget applies to both types.   |
| `nodeConfigs[].propagationScheme.propagationEntities[].cpuCostNs` / `memoryCostBytes` | long | Optional per-entity sub-budget; inherits from the parent enforcement profile if omitted.                                              |

## Controller REST API

All endpoints live on the Pinot controller and operate on workload configs stored in ZK.

| Method | Path                                                    | Purpose                                                                                                       |
| ------ | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| GET    | `/queryWorkloadConfigs`                                 | List all workload configs in the cluster.                                                                     |
| GET    | `/queryWorkloadConfigs/{name}`                          | Fetch one workload by name.                                                                                   |
| GET    | `/queryWorkloadConfigs/instance/{instanceName}`         | Return the per-workload budget that's been allocated to one broker or server (useful for debugging splits).   |
| POST   | `/queryWorkloadConfigs`                                 | Create or update a workload. Body is a `QueryWorkloadConfig` JSON (see previous section).                     |
| DELETE | `/queryWorkloadConfigs/{name}`                          | Delete a workload and tell every instance to forget its budget.                                               |
| POST   | `/queryWorkloadConfigs/refresh?resourceType=…&resourceNames=…&nodeType=…` | Force re-propagation. `resourceType` is one of `workload`, `table`, `tenant`. `nodeType` is optional. |

Examples:

```bash
# Create or update the "analytics" workload
curl -X POST 'http://localhost:9000/queryWorkloadConfigs' \
  -H 'Content-Type: application/json' \
  -d @analytics-workload.json

# Read back what was stored
curl 'http://localhost:9000/queryWorkloadConfigs/analytics'

# See what budget the controller has allocated to one server
curl 'http://localhost:9000/queryWorkloadConfigs/instance/Server_192.0.2.10_8098'

# Force a re-propagation for one table (e.g. after rebalance)
curl -X POST 'http://localhost:9000/queryWorkloadConfigs/refresh?resourceType=table&resourceNames=myTable_OFFLINE&nodeType=SERVER_NODE'

# Delete the workload
curl -X DELETE 'http://localhost:9000/queryWorkloadConfigs/analytics'
```

### Broker / server instance endpoints

Brokers and servers also expose `/queryWorkloadConfigs` (POST / GET / DELETE) on their own admin ports. The controller is the only client that calls them in normal operation, but they are useful for debugging — `GET /queryWorkloadConfigs?workloadNames=analytics` on a specific broker returns the live budget statistics (`cpuBudgetNs`, `cpuRemainingNs`, `memoryBudgetBytes`, `memoryRemainingBytes`) for that workload on that one host.

## Tagging a query with a workload

Queries opt into a workload via the `workloadName` query option:

```sql
SET workloadName='analytics';
SELECT col1, count(*) FROM myTable GROUP BY col1;
```


If a query does not set `workloadName`, it is charged to the workload named `default`. You can define a `QueryWorkloadConfig` for `default` just like any other workload to bound the budget for unclassified queries.

A separate, legacy option exists for binary primary/secondary classification: Disabled by default

```sql
SET isSecondaryWorkload=true;
SELECT … FROM myTable;
```

This routes the query through `BinaryWorkloadScheduler` into the workload named by `accounting.secondary.workload.name` (default `defaultSecondary`), constrained to `accounting.secondary.workload.cpu.percentage` of total server CPU. New deployments should prefer named workloads via `workloadName`.

## What happens when a budget is exceeded

Within the current enforcement window:


* CPU and memory continue to be charged, so the workload's remaining budget can go negative.
* **New** queries on that workload are rejected at the server admission step with `QueryErrorCode.SERVER_RESOURCE_LIMIT_EXCEEDED`. The `WORKLOAD_BUDGET_EXCEEDED` meter (server-level and table-level) increments. Running queries can be terminated as well based on the sampling and enforcement window

At the start of the next window the budget is reset to its configured value and new queries are admitted again.

{% hint style="warning" %}
Because overage is allowed within a window, total CPU consumption for a workload can briefly exceed its configured `cpuCostNs`. Treat the budget as a steady-state target, not a hard per-query limit. Shorten the enforcement window if you need tighter control.
{% endhint %}

## Metrics

| Metric                                              | Where      | Meaning                                                          |
| --------------------------------------------------- | ---------- | ---------------------------------------------------------------- |
| `WORKLOAD_QUERIES`                                  | Server     | Queries handled per workload.                                    |
| `WORKLOAD_BUDGET_EXCEEDED`                          | Server     | Queries rejected because the workload's budget was exhausted.    |
| `QUERY_WORKLOAD_PROPAGATION_COUNT`                  | Controller | Workload config propagations sent to instances.                  |
| `QUERY_WORKLOAD_PROPAGATION_ERROR`                  | Controller | Propagations that failed (network, instance down, etc.).         |
| `QUERY_WORKLOAD_REQUEST_DROPPED`                    | Controller | Propagations dropped because the work queue was full.            |
| `QUERY_WORKLOAD_PROPAGATE_TIME_MS`                  | Controller | End-to-end propagation latency.                                  |
| `QUERY_WORKLOAD_COMPUTE_INSTANCE_COST_TIME_MS`      | Controller | Latency of computing each instance's share of a workload budget. |

## Operational notes & FAQ

* **How should I pick `cpuCostNs` and `memoryCostBytes`?** Turn on `accounting.workload.enable.cost.collection` (and `enable.cost.emission`) but leave enforcement off. Observe the `WORKLOAD_QUERIES` and per-workload cost values for a representative period. Pick budgets that cover your typical peak usage with some headroom, then enable enforcement.
* **What happens during a table rebalance or tenant change?** `QueryWorkloadManager` listens for ZK changes on instance partitions, broker resources, and tenants, and re-runs the cost split automatically. If you ever suspect a stuck or stale budget on a host, hit the controller's `/queryWorkloadConfigs/refresh` endpoint.
* **Can the same query land in two workloads?** No — a query carries a single `workloadName`. Multi-stage queries spanning multiple tables also charge to the one workload named by the submitter.

## See also

{% content-ref url="oom-protection-using-automatic-query-killing.md" %}
[oom-protection-using-automatic-query-killing.md](oom-protection-using-automatic-query-killing.md)
{% endcontent-ref %}

{% content-ref url="tuning/query-scheduling.md" %}
[query-scheduling.md](tuning/query-scheduling.md)
{% endcontent-ref %}

{% content-ref url="../../users/user-guide-query/query-quotas.md" %}
[query-quotas.md](../../users/user-guide-query/query-quotas.md)
{% endcontent-ref %}

{% content-ref url="../../users/user-guide-query/query-options.md" %}
[query-options.md](../../users/user-guide-query/query-options.md)
{% endcontent-ref %}

{% content-ref url="../../basics/components/cluster/tenant.md" %}
[tenant.md](../../basics/components/cluster/tenant.md)
{% endcontent-ref %}
