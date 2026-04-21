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
#### Configuration to control which queries are chosen as victims

In panic mode, all queries are killed.

In critical mode, queries below a certain threshold (expressed as a ratio of total heap memory) are not killed.

```
pinot.query.scheduler.accounting.min.memory.footprint.to.kill.ratio=0.025 (default)
```

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
| pinot.query.scheduler.accounting.oom.alarming.usage.ratio | 0.75 | When the heap usage exceeds this ratio, the framework will run more frequently to gather stats and prepare to kill queries timely. |
| pinot.query.scheduler.accounting.sleep.ms | 30ms | The periodical task for query killing wakes up every 30ms |
| pinot.query.scheduler.accounting.sleep.time.denominator | 3 (corresponding to 10ms sleep time at alarming level heap usage) | When the heap usage exceeds this alarming level, the sleep time will be `sleepTime/denominator` |
| pinot.query.scheduler.accounting.min.memory.footprint.to.kill.ratio | 0.025 | If a query allocates memory below this ratio of total heap size (Xmx) it will not be killed. This is to prevent aggressive killing when the heap memory is not mainly allocated for queries |
| pinot.query.scheduler.accounting.cpu.time.based.killing.threshold.ms | 30000ms | If a query's CPU usage (across all threads) is beyond this threshold, it will be killed when CPU based query killing is enabled. |

## Relevant Metrics

These are the relevant metrics to monitor when using Pinot's OOM protection

```
QUERIES_KILLED
JVM_HEAP_USED_BYTES
HEAP_CRITICAL_LEVEL_EXCEEDED
HEAP_PANIC_LEVEL_EXCEEDED
```
