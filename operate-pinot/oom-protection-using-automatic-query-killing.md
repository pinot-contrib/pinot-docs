---
description: Pinot's built in heap usage monitoring and OOM protection
---

# OOM Protection Using Automatic Query Killing

Pinot has implemented a mechanism to monitor the total JVM heap size and per query memory allocation approximation for server.&#x20;

* Support for Single-Stage Queries:  [https://github.com/apache/pinot/pull/9727](https://github.com/apache/pinot/pull/9727)
* Support for Multi-Stage Queries (available in 1.3.0) : [https://github.com/apache/pinot/pull/13598](https://github.com/apache/pinot/pull/13598)
* Major refactor of query killing mechanism (available in 1.5.0): [https://github.com/apache/pinot/pull/16728](https://github.com/apache/pinot/pull/16728)

**The feature is OFF by default.** When enabled, this mechanism can help to protect the servers and brokers from OOM caused by expensive queries (e.g. distinctcount + group by on high cardinality columns). Upon an immediate risk of heap depletion, this mechanism will kick in and kill from the most expensive query(s).

The feature has two components on each broker and server:

* Statistics framework that tracks resource usage for each query thread.
* Query killing mechanism.

## Usage

### Enable Thread Statistics Collection

```
# Turn on resource usage tracking in statistics framework.
# Configuration has to be set in broker and server config files.
pinot.broker.instance.enableThreadAllocatedBytesMeasurement=true
pinot.server.instance.enableThreadAllocatedBytesMeasurement=true
pinot.query.scheduler.accounting.factory.name=org.apache.pinot.core.accounting.ResourceUsageAccountantFactory
pinot.query.scheduler.accounting.enable.thread.memory.sampling=true
```

#### Debug APIs&#x20;

Once memory sampling has been enabled, the following DEBUG APIs can be used to check memory usage on a broker or server. Note that there are no APIs that aggregate usage across all servers and brokers for a query.

**/debug/queries/resourceUsage**

Returns resource usage aggregated by queryId

```json
[
  {
    "executionContext": {
      "queryType": "SSE",
      "requestId": 174733410000000095,
      ...
    }
    "cpuTimeNs": 0,
    "allocatedBytes": 3239944
  },
  {
    "executionContext": {
      "queryType": "SSE",
      "requestId": 174733410000000094,
      ...
    }
    "cpuTimeNs": 0,
    "allocatedBytes": 3239944
  },
  ...
]
```

**/debug/threads/resourceUsage**

Returns resource usage of a thread and the queryId of the task.

```json
[
  {
    "threadContext": {
      "executionContext": {
        "queryType": "SSE",
        "requestId": 174733410000000095,
        ...
      },
      "mseWorkerInfo": null
    },
    "cputimeMS": 0,
    "allocatedBytes": 3239680
  },
  {
    "threadContext": null
    "cputimeMS": 0,
    "allocatedBytes": 0
  },
  ...
]
```

### OOM Pause Mechanism (Before Kill)

Before resorting to query killing when heap transitions to critical level, Pinot can pause all query execution threads to give the JVM a chance to reclaim memory through garbage collection. This pause mechanism is useful for workloads that experience occasional memory spikes.

When heap usage exceeds the critical threshold:
1. All query execution threads are paused for a configurable timeout window.
2. `System.gc()` is called once to encourage memory reclamation.
3. If heap recovers below critical level during the pause, threads resume and no queries are killed.
4. If heap remains critical after the timeout, the existing kill-most-expensive-query logic proceeds.

**Off by default.** This feature is disabled by default and can be dynamically toggled via cluster config without restarting.

Enable with:

```
# Enable pause before kill mechanism
accounting.oom.critical.query.pause.enabled=true
# How long to pause (in milliseconds)
accounting.oom.critical.query.pause.timeout.ms=1000
```

Per-role overrides are also supported:

```
pinot.broker.query.accounting.oom.critical.query.pause.enabled=true
pinot.broker.query.accounting.oom.critical.query.pause.timeout.ms=1000
pinot.server.query.accounting.oom.critical.query.pause.enabled=true
pinot.server.query.accounting.oom.critical.query.pause.timeout.ms=1000
```

### Enable Query Killing Mechanism

The statistics framework also starts a watcher task. The watcher task takes decisions on killing queries.&#x20;

* By default the watcher task does not take any actions.&#x20;
* queries\_killed meter tracks the number of queries killed.

The killing mechanism is enabled with the following config:

```
# Set in broker and server
pinot.query.scheduler.accounting.oom.enable.killing.query=true
# Enable metrics for killed queries
pinot.query.scheduler.accounting.query.killed.metric.enabled=true
```

The watcher task can be in 3 modes depending on the level of heap usage:

* Normal
* Critical
* Panic

The thresholds for these levels is defined by the following configs:

```
pinot.query.scheduler.accounting.oom.critical.heap.usage.ratio=0.96f (default)
pinot.query.scheduler.accounting.oom.panic.heap.usage.ratio=0.99f (default)
```

The watcher task runs periodically. The frequency of the watcher task can be configured with:

```
pinot.query.scheduler.accounting.sleep.ms=30 (default)
```

However under stress, the task can run faster so that it can react to increase in heap usage faster. The watcher task has to be configured with&#x20;

* a threshold when to shift to higher frequency
* the frequency expressed as a ratio of the default frequency.

```
pinot.query.scheduler.accounting.oom.alarming.usage.ratio=0.75f (default)
pinot.query.scheduler.accounting.sleep.time.denominator=3 (Run every 30/3=10ms)
```


### Role-Specific Accounting Configuration

As of Pinot 1.6.0, you can configure accounting settings independently for brokers and servers using role-specific config prefixes. This allows fine-tuned control over OOM protection and query budgets per component.

**Configuration Prefixes:**

1. **Broker-specific:** `pinot.broker.query.accounting.*`
2. **Server-specific:** `pinot.server.query.accounting.*`
3. **Legacy (still supported):** `pinot.query.scheduler.accounting.*`

**Precedence:** Role-specific values override the legacy prefix on their respective roles.

**Example:**

```
# Legacy (still supported, applies to both broker and server unless overridden)
pinot.query.scheduler.accounting.oom.enable.killing.query=true

# Override for broker only
pinot.broker.query.accounting.oom.enable.killing.query=false

# Override for server only
pinot.server.query.accounting.oom.enable.killing.query=false
```

**Deprecation Note:** The legacy prefix `pinot.query.scheduler.accounting.*` is marked for removal in a future release after 1.6.0. While still fully functional, new deployments should prefer role-specific prefixes for better configurability.

### Scan-Based Query Killing on Servers

Pinot servers can also stop a query when cumulative scan work crosses configured thresholds. This path is separate from heap-based and CPU-based killing: server operators report scan deltas as the query runs, and Pinot checks the cumulative totals at block boundaries.

Scan-based killing evaluates these counters:

* `numEntriesScannedInFilter`: entries examined while evaluating filters
* `numDocsScanned`: documents scanned by the query
* `numEntriesScannedPostFilter`: entries examined after filtering, such as projected values processed by aggregation, group-by, or selection operators

Use the following server config to enable it:

```properties
# Server only. Set at least one threshold for the feature to take effect.
pinot.query.scheduler.accounting.scan.based.killing.mode=logOnly
pinot.query.scheduler.accounting.scan.based.killing.max.entries.scanned.in.filter=500000000
pinot.query.scheduler.accounting.scan.based.killing.max.docs.scanned=50000000
pinot.query.scheduler.accounting.scan.based.killing.max.entries.scanned.post.filter=100000000
```

Valid modes are `disabled`, `logOnly`, and `enforce`.

* `disabled`: turns scan-based killing off
* `logOnly`: records the dry-run log line and metric, but does not terminate the query
* `enforce`: terminates the query when a threshold is exceeded

Leaving an individual threshold unset disables that specific check. If all three thresholds are unset, enabling the mode has no effect until you configure at least one threshold.

You can also override the cluster-level thresholds and mode per table with the table's `query` config:

```json
"query": {
  "maxEntriesScannedInFilter": 250000000,
  "maxDocsScanned": 25000000,
  "maxEntriesScannedPostFilter": 50000000,
  "scanKillingMode": "enforce"
}
```

`scanKillingMode` is validated when the table config is submitted. If a table does not set `scanKillingMode`, Pinot falls back to the cluster-level mode. Scan-based killing config updates are also hot-reloaded on servers, so you can tune thresholds without restarting them.

#### Configuration to control which queries are chosen as victims

In panic mode, all queries are killed.

In critical mode, queries below a certain threshold (expressed as a ratio of total heap memory) are not killed.

```
pinot.query.scheduler.accounting.min.memory.footprint.to.kill.ratio=0.025 (default)
```

### Realtime Ingestion OOM Protection on Servers

Pinot servers can also apply heap-based backpressure to realtime ingestion. This path is separate from automatic query
killing: it uses the same JVM heap signal, but instead of selecting a query victim, the server waits before the next
realtime fetch while heap usage stays above the configured threshold.

**Off by default.** With the default mode `DISABLE`, Pinot does not hold realtime ingestion unless a table explicitly
opts in.

Set the server-level policy in the server instance config:

```properties
pinot.server.instance.ingestion.oom.protection.mode=UPSERT_DEDUP_ONLY
pinot.server.instance.ingestion.oom.protection.heapUsageThrottleThreshold=0.95
pinot.server.instance.ingestion.oom.protection.heapUsageRecoveryThreshold=0.90
pinot.server.instance.ingestion.oom.protection.checkIntervalMs=1000
pinot.server.instance.ingestion.oom.protection.gcIntervalMs=30000
```

The same full `pinot.server.instance.*` keys can also be set through Pinot cluster config. Cluster config values
override the server instance config while they are present, and servers reload them at runtime without a restart.

#### Server Modes

| Mode | Effect |
| --- | --- |
| `ENABLE` | Protect all realtime tables unless a table sets `oomProtection=DISABLE`. |
| `UPSERT_DEDUP_ONLY` | Protect only upsert and dedup realtime tables unless a table opts in or out. |
| `DISABLE` | Leave the server policy off unless a table sets `oomProtection=ENABLE`. |

#### Server Configuration

| Property | Default | Description |
| --- | --- | --- |
| `pinot.server.instance.ingestion.oom.protection.mode` | `DISABLE` | Server-wide policy. Valid values are `ENABLE`, `UPSERT_DEDUP_ONLY`, and `DISABLE`. |
| `pinot.server.instance.ingestion.oom.protection.heapUsageThrottleThreshold` | `0.95` | Heap usage ratio that starts realtime ingestion backpressure. |
| `pinot.server.instance.ingestion.oom.protection.heapUsageRecoveryThreshold` | `0.90` | Heap usage ratio at or below which ingestion resumes. This value must be lower than `heapUsageThrottleThreshold`. |
| `pinot.server.instance.ingestion.oom.protection.checkIntervalMs` | `1000` | Wait interval, in milliseconds, between throttle checks while a consuming thread is paused. |
| `pinot.server.instance.ingestion.oom.protection.gcIntervalMs` | `30000` | Minimum interval, in milliseconds, between explicit JVM GC requests while throttled. Set to `0` or a negative value to disable the explicit GC request. |

#### Table Override

Each realtime table can override the server policy under `ingestionConfig.streamIngestionConfig`:

```json
{
  "ingestionConfig": {
    "streamIngestionConfig": {
      "oomProtection": "ENABLE"
    }
  }
}
```

`oomProtection` supports the following values:

* `DEFAULT` (default): Follow the server mode.
* `ENABLE`: Protect this realtime table even when the server mode is `DISABLE` or would otherwise skip it.
* `DISABLE`: Skip protection for this realtime table even when the server mode would protect it.

Thresholds remain server-level only and are shared by all enrolled consuming threads on the server.

#### Runtime Behavior

When protection is active for a realtime segment, the server waits before the next stream fetch instead of advancing
ingestion into higher heap pressure. Pinot rechecks the shared throttle state every `checkIntervalMs` and resumes
ingestion after heap usage drops to the recovery threshold.

* The protection applies only while a segment is in `INITIAL_CONSUMING`; catch-up paths do not wait on this guard.
* The throttle is server-local. It does not pause the table through controller APIs, and stream offsets do not advance while Pinot is waiting to fetch the next batch.
* Pinot uses hysteresis: throttling starts when heap usage is at or above `heapUsageThrottleThreshold` and releases when heap usage drops to `heapUsageRecoveryThreshold` or lower.
* While throttled, Pinot can request `System.gc()` at most once every `gcIntervalMs`.
* Pinot rechecks stop and segment-end conditions between waits, so force commits and normal segment rollover still proceed.

Monitor the global server gauge `REALTIME_INGESTION_OOM_PROTECTION_ACTIVE`, which is `1` while the realtime ingestion
throttle is active and `0` otherwise.

## Configuration

Here are the configurations that can be commonly applied to server/broker:

&#x20;

| Config | Default | Description |
| --- | --- | --- |
| pinot.broker.instance.enableThreadAllocatedBytesMeasurement pinot.server.instance.enableThreadAllocatedBytesMeasurement | false | Use true if one intend to enable this feature to kill queries by bytes allocated |
| pinot.server.instance.enableThreadCpuTimeMeasurement pinot.server.instance.enableThreadCpuTimeMeasurement | false | Use true if one intend to enable this feature to kill queries by cpu time |
| pinot.query.scheduler.accounting.factory.name | Only hardens timeout but no preemption | Use `org.apache.pinot.core.accounting.ResourceUsageAccountantFactory` if one intend to enable this feature |
| pinot.query.scheduler.accounting.enable.thread.memory.sampling | false | Account for threads' memory usage of a query, works only for hotspot jvm. If enabled, the killing decision will be based on memory allocated. |
| pinot.query.scheduler.accounting.enable.thread.cpu.sampling | false | Account for threads' CPU time of a query. If memory sampling is disabled/unavailable, the killing decision will be based on CPU time. If both are disabled, the framework will not able to pick the most expensive query. |
| pinot.query.scheduler.accounting.oom.enable.killing.query | false | Whether the framework will actually commit to kill queries per memory usage. If disabled, only error message will be logged. |
| pinot.query.scheduler.accounting.cpu.time.based.killing.enabled | false | Whether the framework will actually commit to kill queries per CPU usage. If disabled, only error message will be logged. |
| pinot.query.scheduler.accounting.publishing.jvm.heap.usage | false | Whether the framework periodically publishes the heap usage to Pinot metrics. |
| pinot.query.scheduler.accounting.oom.panic.heap.usage.ratio | 0.99 | When the heap usage exceeds this ratio, the frame work will kill all the queries. This can be set to be >1 to prevent a full killing from happening. |
| pinot.query.scheduler.accounting.oom.critical.heap.usage.ratio | 0.96 | When the heap usage exceeds this ratio, the frame work will kill the most expensive query. |
| accounting.oom.critical.query.pause.enabled | false | Enable pausing query threads before killing when heap reaches critical level. |
| accounting.oom.critical.query.pause.timeout.ms | 1000 | Duration (in milliseconds) to pause query threads before proceeding with kill logic. |
| pinot.query.scheduler.accounting.oom.alarming.usage.ratio | 0.75 | When the heap usage exceeds this ratio, the framework will run more frequently to gather stats and prepare to kill queries timely. |
| pinot.query.scheduler.accounting.sleep.ms | 30ms | The periodical task for query killing wakes up every 30ms |
| pinot.query.scheduler.accounting.sleep.time.denominator | 3 (corresponding to 10ms sleep time at alarming level heap usage) | When the heap usage exceeds this alarming level, the sleep time will be `sleepTime/denominator` |
| pinot.query.scheduler.accounting.min.memory.footprint.to.kill.ratio | 0.025 | If a query allocates memory below this ratio of total heap size (Xmx) it will not be killed. This is to prevent aggressive killing when the heap memory is not mainly allocated for queries |
| pinot.query.scheduler.accounting.cpu.time.based.killing.threshold.ms | 30000ms | If a query's CPU usage (across all threads) is beyond this threshold, it will be killed when CPU based query killing is enabled. |
| pinot.query.scheduler.accounting.scan.based.killing.mode | disabled | Server-side scan-based killing mode. Valid values are `disabled`, `logOnly`, and `enforce`. |
| pinot.query.scheduler.accounting.scan.based.killing.max.entries.scanned.in.filter | disabled | Server-side threshold for `numEntriesScannedInFilter`. When this threshold is exceeded, Pinot logs or kills the query based on the configured mode. |
| pinot.query.scheduler.accounting.scan.based.killing.max.docs.scanned | disabled | Server-side threshold for `numDocsScanned`. When this threshold is exceeded, Pinot logs or kills the query based on the configured mode. |
| pinot.query.scheduler.accounting.scan.based.killing.max.entries.scanned.post.filter | disabled | Server-side threshold for `numEntriesScannedPostFilter`. When this threshold is exceeded, Pinot logs or kills the query based on the configured mode. |
| pinot.broker.query.accounting.* | - | Broker-specific accounting config (e.g., `pinot.broker.query.accounting.oom.enable.killing.query`). Takes precedence over legacy prefix on broker. |
| pinot.server.query.accounting.* | - | Server-specific accounting config (e.g., `pinot.server.query.accounting.oom.enable.killing.query`). Takes precedence over legacy prefix on server. |
| pinot.query.scheduler.accounting.* | - | **Deprecated (since 1.6.0, for removal).** Legacy prefix still supported for backward compatibility. Use role-specific prefixes instead. |

## Relevant Metrics

These are the relevant metrics to monitor when using Pinot's OOM protection

```
QUERIES_KILLED
QUERIES_KILLED_SCAN
QUERIES_KILLED_SCAN_DRY_RUN
QUERIES_KILLED_SCAN_ERROR
JVM_HEAP_USED_BYTES
REALTIME_INGESTION_OOM_PROTECTION_ACTIVE
HEAP_CRITICAL_LEVEL_EXCEEDED
HEAP_PANIC_LEVEL_EXCEEDED
```
