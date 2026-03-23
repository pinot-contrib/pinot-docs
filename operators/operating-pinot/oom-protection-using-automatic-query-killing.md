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

#### Configuration to control which queries are chosen as victims

In panic mode, all queries are killed.

In critical mode, queries below a certain threshold (expressed as a ratio of total heap memory) are not killed.

```
pinot.query.scheduler.accounting.min.memory.footprint.to.kill.ratio=0.025 (default)
```

## Configuration

Here are the configurations that can be commonly applied to server/broker:

&#x20;

<table><thead><tr><th width="274.99609375">Config</th><th width="179.61848958333331">Default</th><th>Description</th></tr></thead><tbody><tr><td><p>pinot.broker.instance.enableThreadAllocatedBytesMeasurement<br></p><p>pinot.server.instance.enableThreadAllocatedBytesMeasurement</p></td><td>false </td><td>Use true if one intend to enable this feature to kill  queries by bytes allocated</td></tr><tr><td>pinot.server.instance.enableThreadCpuTimeMeasurement<br><br>pinot.server.instance.enableThreadCpuTimeMeasurement</td><td>false</td><td>Use true if one intend to enable this feature to kill  queries by cpu time</td></tr><tr><td>pinot.query.scheduler.accounting.factory.name</td><td>Only hardens timeout but no preemption</td><td>Use <code>org.apache.pinot.core.accounting.ResourceUsageAccountantFactory</code> if one intend to enable this feature</td></tr><tr><td>pinot.query.scheduler.accounting.enable.thread.memory.sampling</td><td>false</td><td>Account for threads' memory usage of a query, works only for hotspot jvm. If enabled, the killing decision will be based on memory allocated.</td></tr><tr><td>pinot.query.scheduler.accounting.enable.thread.cpu.sampling</td><td>false</td><td>Account for threads' CPU time of a query. If memory sampling is disabled/unavailable, the killing decision will be based on CPU time. If both are disabled, the framework will not able to pick the most expensive query.</td></tr><tr><td>pinot.query.scheduler.accounting.oom.enable.killing.query</td><td>false</td><td>Whether the framework will actually commit to kill queries per memory usage. If disabled, only error message will be logged.</td></tr><tr><td>pinot.query.scheduler.accounting.cpu.time.based.killing.enabled</td><td>false</td><td>Whether the framework will actually commit to kill queries per CPU usage. If disabled, only error message will be logged.</td></tr><tr><td>pinot.query.scheduler.accounting.publishing.jvm.heap.usage</td><td>false</td><td>Whether the framework periodically publishes the heap usage to Pinot metrics.</td></tr><tr><td>pinot.query.scheduler.accounting.oom.panic.heap.usage.ratio</td><td>0.99</td><td>When the heap usage exceeds this ratio, the frame work will kill all the queries. This can be set to be >1 to prevent a full killing from happening.</td></tr><tr><td>pinot.query.scheduler.accounting.oom.critical.heap.usage.ratio</td><td>0.96</td><td>When the heap usage exceeds this ratio, the frame work will kill the most expensive query.</td></tr><tr><td>pinot.query.scheduler.accounting.oom.alarming.usage.ratio</td><td>0.75</td><td>When the heap usage exceeds this ratio, the framework will run more frequently to gather stats and prepare to kill queries timely.</td></tr><tr><td>pinot.query.scheduler.accounting.sleep.ms</td><td>30ms</td><td>The periodical task for query killing wakes up every 30ms</td></tr><tr><td>pinot.query.scheduler.accounting.sleep.time.denominator</td><td>3 (corresponding to 10ms sleep time at alarming level heap usage)</td><td>When the heap usage exceeds this alarming level, the sleep time will be <br><code>sleepTime/denominator</code></td></tr><tr><td>pinot.query.scheduler.accounting.min.memory.footprint.to.kill.ratio</td><td>0.025</td><td>If a query allocates memory below this ratio of total heap size (Xmx) it will not be killed. This is to prevent aggressive killing when the heap memory is not mainly allocated for queries</td></tr><tr><td>pinot.query.scheduler.accounting.cpu.time.based.killing.threshold.ms</td><td>30000ms</td><td>If a query's CPU usage (across all threads) is beyond this threshold, it will be killed when CPU based query killing is enabled.</td></tr></tbody></table>

## Relevant Metrics

These are the relevant metrics to monitor when using Pinot's OOM protection

```
QUERIES_KILLED
JVM_HEAP_USED_BYTES
HEAP_CRITICAL_LEVEL_EXCEEDED
HEAP_PANIC_LEVEL_EXCEEDED
```

## Related pages

* [Performance tuning overview](tuning/) -- all tuning categories at a glance
* [Query Scheduling](tuning/query-scheduling.md) -- control query concurrency and prioritization
* [Workload-Based Query Isolation](tuning/workload-query-isolation.md) -- isolate production vs. ad-hoc query resources with CPU/memory budgets
* [Pause Ingestion Based on Resource Utilization](pause-ingestion-based-on-resource-utilization.md) -- auto-pause ingestion when disk usage is high

