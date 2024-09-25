---
description: Pinot's built in heap usage monitoring and OOM protection
---

# OOM Protection Using Automatic Query Killing

Pinot has implemented a mechanism to monitor the total JVM heap size and per query memory allocation approximation for server.&#x20;

* Support for Single-Stage Queries:  [https://github.com/apache/pinot/pull/9727](https://github.com/apache/pinot/pull/9727)
* Support for Multi-Stage Queries (available in 1.3.0) : [https://github.com/apache/pinot/pull/13598](https://github.com/apache/pinot/pull/13598)

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
pinot.query.scheduler.accounting.factory.name=org.apache.pinot.core.accounting.PerQueryCPUMemAccountantFactory
pinot.query.scheduler.accounting.enable.thread.memory.sampling=true
```

#### Debug APIs&#x20;

Once memory sampling has been enabled, the following DEBUG APIs can be used to check memory usage on a broker or server. Note that there are no APIs that aggregate usage across all servers and brokers for a query.

**/debug/query/resourceUsage**

Returns resource usage aggregated by queryId

```json
[
  {
    "cpuTimeNs": 0,
    "queryId": "Broker_192.168.0.107_8000_174733410000000095_O",
    "allocatedBytes": 3239944
  },
  {
    "cpuTimeNs": 0,
    "queryId": "Broker_192.168.0.107_8000_174733410000000094_O",
    "allocatedBytes": 3239944
  },
  {
    "cpuTimeNs": 0,
    "queryId": "Broker_192.168.0.107_8000_174733410000000093_O",
    "allocatedBytes": 3239944
  },
  {
    "cpuTimeNs": 0,
    "queryId": "Broker_192.168.0.107_8000_174733410000000082_O",
    "allocatedBytes": 4520488
  },
  {
    "cpuTimeNs": 0,
    "queryId": "Broker_192.168.0.107_8000_174733410000000092_O",
    "allocatedBytes": 2599672
  },
  {
    "cpuTimeNs": 0,
    "queryId": "Broker_192.168.0.107_8000_174733410000000087_O",
    "allocatedBytes": 3880216
  },
  {
    "cpuTimeNs": 0,
    "queryId": "Broker_192.168.0.107_8000_174733410000000088_O",
    "allocatedBytes": 2599672
  },
  {
    "cpuTimeNs": 0,
    "queryId": "Broker_192.168.0.107_8000_174733410000000096_O",
    "allocatedBytes": 1959400
  }
]
```

**/debug/threads/resourceUsage**

Returns resource usage of a thread and the queryId of the task.

```json
[
  {
    "taskId": -1,
    "queryId": "174733410000001465",
    "cputimeMS": 0,
    "allocatedBytes": 0
  },
  {
    "taskId": -1,
    "queryId": "174733410000001466",
    "cputimeMS": 0,
    "allocatedBytes": 0
  },
  {
    "taskId": -1,
    "queryId": "174733410000001467",
    "cputimeMS": 0,
    "allocatedBytes": 0
  },
  {
    "taskId": -1,
    "queryId": "Broker_192.168.0.107_8000_174733410000001466_O",
    "cputimeMS": 0,
    "allocatedBytes": 0
  },
  {
    "taskId": 0,
    "queryId": "Broker_192.168.0.107_8000_174733410000001466_O",
    "cputimeMS": 0,
    "allocatedBytes": 3239680
  },
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
pinot.query.scheduler.accounting.oom.alarming.heap.usage.ratio=0.75f (default)
pinot.query.scheduler.accounting.sleep.time.denominator=3 (Run every 30/3=10ms)
```

#### Configuration to control which queries are chosen as victims

In panic mode, all queries are killed.

In critical mode, queries below a certain threshold (expressed as a ratio of total heap memory) are not killed.

```
pinot.query.scheduler.accounting.min.memory.footprint.to.kill.ratio=0.025f
```

Once the watcher task kills a few queries, it will trigger a GC to reclaim memory. The configuration is:

```
pinot.query.scheduler.accounting.gc.backoff.count=5
```

## Configuration

Here are the configurations that can be commonly applied to server/broker:

&#x20;

| Config                                                                                                                                   | Default                                                                             | Description                                                                                                                                                                                                               |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p>pinot.broker.instance.enableThreadAllocatedBytesMeasurement<br></p><p>pinot.server.instance.enableThreadAllocatedBytesMeasurement</p> | false                                                                               | Use true if one intend to enable this feature to kill  queries by bytes allocated                                                                                                                                         |
| <p>pinot.server.instance.enableThreadCpuTimeMeasurement<br><br>pinot.server.instance.enableThreadCpuTimeMeasurement</p>                  | false                                                                               | Use true if one intend to enable this feature to kill  queries by cpu time                                                                                                                                                |
| pinot.query.scheduler.accounting.factory.name                                                                                            | `DefaultThreadResourceUsageAccountant` which only hardens timeout but no preemption | Use `org.apache.pinot.core.accounting.PerQueryCPUMemAccountantFactory`If one intend to enable this feature                                                                                                                |
| pinot.query.scheduler.accounting.enable.thread.memory.sampling                                                                           | false                                                                               | Account for threads' memory usage of a query, works only for hotspot jvm. If enabled, the killing decision will be based on memory allocated.                                                                             |
| pinot.query.scheduler.accounting.enable.thread.cpu.sampling                                                                              | false                                                                               | Account for threads' cpu time of a query. If memory sampling is disabled/unavailable, the killing decision will be based on CPU time. If both are disabled, the framework will not able to pick the most expensive query. |
| pinot.query.scheduler.accounting.oom.enable.killing.query                                                                                | false                                                                               | Whether the framework will actually commit to kill queries. If disabled, only error message will be logged.                                                                                                               |
| pinot.query.scheduler.accounting.publishing.jvm.heap.usage                                                                               | false                                                                               | Whether the framework periodically publishes the heap usage to Pinot metrics.                                                                                                                                             |
| pinot.query.scheduler.accounting.oom.panic.heap.usage.ratio                                                                              | 0.99                                                                                | When the heap usage exceeds this ratio, the frame work will kill all the queries. This can be set to be >1 to prevent a full killing from happening.                                                                      |
| pinot.query.scheduler.accounting.oom.critical.heap.usage.ratio                                                                           | 0.96                                                                                | When the heap usage exceeds this ratio, the frame work will kill the most expensive query.                                                                                                                                |
| pinot.query.scheduler.accounting.oom.alarming.heap.usage.ratio                                                                           | 0.75                                                                                | When the heap usage exceeds this ratio, the framework will run more frequently to gather stats and prepare to kill queries timely.                                                                                        |
| pinot.query.scheduler.accounting.sleep.ms                                                                                                | 30ms                                                                                | The periodical task for query killing wakes up every 30ms                                                                                                                                                                 |
| pinot.query.scheduler.accounting.sleep.time.denominator                                                                                  | 3 (corresponding to 10ms sleep time at alarming level heap usage)                   | <p>When the heap usage exceeds this alarming level, the sleep time will be <br><code>sleepTime/denominator</code></p>                                                                                                     |
| pinot.query.scheduler.accounting.min.memory.footprint.to.kill.ratio                                                                      | 0.025                                                                               | If a query allocates memory below this ratio of total heap size (Xmx) it will not be killed. This is to prevent aggressive killing when the heap memory is not mainly allocated for queries                               |
| pinot.query.scheduler.accounting.gc.backoff.count                                                                                        | 5                                                                                   | When the framework consecutively kills this many expensive queries it will explicitly trigger gc to reclaim the memory. Should consider use -XX:+ExplicitGCInvokesConcurrent to avoid STW for some gc algorithms.         |
| pinot.query.scheduler.accounting.oom.critical.heap.usage.ratio.delta.after.gc                                                            | 0.15                                                                                | if after gc the heap usage is still above this, kill the most expensive query use this to prevent heap size oscillation and repeatedly triggering gc                                                                      |

