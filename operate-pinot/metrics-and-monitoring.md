# Monitoring

This guide covers the critical metrics to monitor in an Apache Pinot cluster, organized by component. It includes recommended alert thresholds and diagnosis patterns to help operators quickly identify and resolve issues.

For the full list of all available metrics, see the [Monitoring Metrics Reference](../reference/configuration-reference/monitoring-metrics.md).

## Metrics Overview

Pinot uses [Dropwizard Metrics](https://metrics.dropwizard.io/4.0.0/) (formerly Yammer Metrics) to collect metrics within each component. Every metric falls into one of three categories:

* **Gauge** -- A point-in-time value (e.g., segment count, heap usage)
* **Meter** -- A rate measured per unit of time (e.g., queries per second, exceptions per second)
* **Timer** -- Duration measurements with percentiles (e.g., query latency p99)

Metrics are available at two scopes:

* **Global** -- Per-instance metrics not tied to a specific table (e.g., total QPS, JVM heap)
* **Table-level** -- Metrics scoped to a specific table (e.g., documents scanned, ingestion delay)

---

## Broker Metrics

The broker receives queries, compiles them, routes them to servers, and merges responses. Monitoring the broker helps detect query failures, latency degradation, and capacity problems.

### Critical Broker Metrics

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|-----------------|
| `QUERIES` | Meter | Query rate (QPS) per table. Use to track traffic patterns. | Baseline-dependent; alert on sudden drops (>50% below baseline) which may indicate client issues |
| `BROKER_RESPONSES_WITH_PARTIAL_SERVERS_RESPONDED` | Meter | Queries where not all servers responded. Indicates servers are down or overloaded. | > 0 sustained over 5 minutes |
| `BROKER_RESPONSES_WITH_PROCESSING_EXCEPTIONS` | Meter | Queries with at least one processing exception from servers. | > 1% of total QPS |
| `QUERY_EXECUTION_EXCEPTIONS` (via timer) | Timer | Total query execution time. Monitor p99 for latency SLAs. | p99 > your SLA (e.g., 500ms) |
| `NO_SERVER_FOUND_EXCEPTIONS` | Meter | Queries where no server was found to serve data. Critical availability issue. | > 0 |
| `REQUEST_TIMEOUT_BEFORE_SCATTERED_EXCEPTIONS` | Meter | Queries that timed out before being sent to servers. | > 0 sustained |
| `QUERY_QUOTA_EXCEEDED` | Meter | Queries rejected due to rate limiting. | > 0 (if unexpected) |
| `UNHEALTHY_SERVERS` | Gauge | Number of servers detected as unhealthy. | > 0 |
| `HEAP_CRITICAL_LEVEL_EXCEEDED` | Meter | Times heap usage exceeded the critical threshold. | > 0 |
| `JVM_HEAP_USED_BYTES` | Gauge | Current JVM heap usage on the broker. | > 85% of max heap |
| `QUERY_QUOTA_CAPACITY_UTILIZATION_RATE` | Gauge | Percentage of configured rate limit in use. | > 80% |

For broker transport memory pressure, also monitor `GRPC_TOTAL_USED_DIRECT_MEMORY` and compare it with `GRPC_TOTAL_MAX_DIRECT_MEMORY`. These gauges cover the shaded Netty runtime used by the broker gRPC listener and MSE mailbox traffic.

### Broker Query Latency Breakdown

These timers help identify which phase of query execution is slow:

| Metric | Description |
|--------|-------------|
| `REQUEST_COMPILATION` | Time spent compiling the SQL query |
| `AUTHORIZATION` | Time spent checking table access permissions |
| `QUERY_ROUTING` | Time spent building the routing table for segments |
| `SCATTER_GATHER` | Time spent sending requests to servers and collecting responses |
| `REDUCE` | Time spent merging results from multiple servers |
| `QUERY_EXECUTION` | Total end-to-end query execution time |

### Broker Diagnosis Patterns

**If `BROKER_RESPONSES_WITH_PARTIAL_SERVERS_RESPONDED` is high:**
- Check `UNHEALTHY_SERVERS` gauge to identify affected servers
- Verify server health via the Pinot admin UI or `/health` endpoints
- Check for server GC pauses or network partitions
- Review server-side `HEAP_CRITICAL_LEVEL_EXCEEDED` metrics

**If `SCATTER_GATHER` latency is high but `REDUCE` is normal:**
- Servers are slow to respond; investigate server-side query latency
- Check `NETTY_CONNECTION_SEND_REQUEST_LATENCY` for network issues
- Look at server `SCHEDULER_WAIT` time for thread pool saturation

**If `REQUEST_COMPILATION` time is high:**
- Queries may be overly complex; review query patterns
- Check for `REQUEST_COMPILATION_EXCEPTIONS` for malformed queries

**If `QUERY_QUOTA_EXCEEDED` is increasing:**
- Increase broker query rate limit or add more broker instances
- Identify high-QPS tables via per-table `QUERIES` metric and optimize or throttle them

---

## Server Metrics

Servers store segments and execute queries. Monitoring servers helps detect ingestion problems, query performance issues, and resource exhaustion.

### Critical Server Metrics

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|-----------------|
| `REALTIME_INGESTION_DELAY_MS` | Gauge | Delay in milliseconds between event production and Pinot consumption. Per-partition metric. | > 5 minutes (300000ms) for most use cases; adjust based on freshness SLA |
| `LLC_PARTITION_CONSUMING` | Gauge | Binary: 1 if low-level consumption is healthy, 0 if unhealthy. Per table-partition. | = 0 on any partition |
| `REALTIME_CONSUMPTION_EXCEPTIONS` | Meter | Exceptions during real-time consumption. | > 0 sustained |
| `REALTIME_BYTES_CONSUMED` | Meter | Serialized bytes Pinot successfully consumes from a real-time stream. Use it with `REALTIME_ROWS_CONSUMED` to spot abrupt payload-size changes. | Sudden drop or spike vs. baseline |
| `REALTIME_BYTES_DROPPED` | Meter | Serialized bytes Pinot drops during real-time ingestion because records were filtered out or failed decode, transform, or indexing. | > 0 sustained |
| `QUERY_EXECUTION_EXCEPTIONS` | Meter | Exceptions during query execution on the server. | > 1% of queries |
| `QUERIES` | Meter | SSE query rate hitting this server. | Sudden drop or spike vs. baseline |
| `MSE_QUERIES` | Meter | MSE query rate hitting this server. | Sudden drop or spike vs. baseline |
| `NUM_MISSING_SEGMENTS` | Meter | Segments the broker expected but the server did not have. | > 0 sustained |
| `SEGMENT_DOWNLOAD_FAILURES` | Meter | Failures downloading segments from deep store. | > 0 |
| `RELOAD_FAILURES` | Meter | Failures reloading segments after config changes. | > 0 |
| `ROWS_WITH_ERRORS` | Meter | Rows that failed transformation or indexing during ingestion. | > 0.1% of `REALTIME_ROWS_CONSUMED` |
| `JVM_HEAP_USED_BYTES` | Gauge | Current JVM heap usage on the server. | > 85% of max heap |
| `HEAP_CRITICAL_LEVEL_EXCEEDED` | Meter | Times heap usage exceeded the critical threshold, triggering query killing. | > 0 |
| `REALTIME_OFFHEAP_MEMORY_USED` | Gauge | Off-heap memory used by real-time segments. | Approaching configured `MaxDirectMemorySize` |

For server transport memory pressure, also monitor `NETTY_TOTAL_USED_DIRECT_MEMORY` and `GRPC_TOTAL_USED_DIRECT_MEMORY`, and compare them with the corresponding `*_MAX_DIRECT_MEMORY` gauges. `NETTY_*` covers the server Netty query service, while `GRPC_*` covers the server gRPC query service and MSE mailbox traffic.

### Server Query Latency Breakdown

| Metric | Description |
|--------|-------------|
| `SCHEDULER_WAIT` | Time waiting in the scheduler queue before execution begins |
| `SEGMENT_PRUNING` | Time spent pruning irrelevant segments |
| `BUILD_QUERY_PLAN` | Time spent building the query execution plan |
| `QUERY_PLAN_EXECUTION` | Time spent executing the query plan against segments |
| `RESPONSE_SERIALIZATION` | Time spent serializing results to send back to the broker |
| `TOTAL_QUERY_TIME` | Total time from receiving the query to returning the response |

### Server Diagnosis Patterns

**If `REALTIME_INGESTION_DELAY_MS` is growing:**
- Check `REALTIME_CONSUMPTION_EXCEPTIONS` for stream connectivity issues
- Verify the stream (Kafka/Kinesis/Pulsar) is healthy and partitions are accessible
- Check `LLC_SIMULTANEOUS_SEGMENT_BUILDS` -- too many concurrent segment builds can stall consumption
- Look at `LAST_REALTIME_SEGMENT_COMPLETION_DURATION_SECONDS` for slow segment commits
- Verify server has sufficient CPU and memory resources

**If `LLC_PARTITION_CONSUMING` is 0 for a partition:**
- A partition has stopped consuming; check the Pinot controller logs for segment state machine errors
- Look at `REALTIME_CONSUMPTION_EXCEPTIONS` and `STREAM_CONSUMER_CREATE_EXCEPTIONS`
- Verify stream topic partitions are available and offsets are valid

**If `SCHEDULER_WAIT` time is high:**
- The server query thread pool is saturated
- Reduce query concurrency or add more server instances
- Check for expensive queries via `NUM_DOCS_SCANNED` and `NUM_ENTRIES_SCANNED_POST_FILTER`

**If `NUM_DOCS_SCANNED` or `NUM_ENTRIES_SCANNED_POST_FILTER` is very high:**
- Queries are scanning too many documents; add or improve indexes (inverted, range, sorted)
- Review segment pruning effectiveness via `NUM_SEGMENTS_PRUNED_BY_VALUE`
- Consider partitioning the table to enable partition-based pruning

**If `SEGMENT_DOWNLOAD_FAILURES` is increasing:**
- Deep store (S3/GCS/HDFS) may be unreachable or throttling
- Check network connectivity and cloud provider quotas
- Look at `SEGMENT_DOWNLOAD_FROM_REMOTE_FAILURES` vs. `SEGMENT_DOWNLOAD_FROM_PEERS_FAILURES` to distinguish deep store vs. peer download issues

---

## Controller Metrics

The controller manages cluster metadata, segment assignments, and periodic maintenance tasks. Monitoring the controller helps detect cluster-level health issues.

### Critical Controller Metrics

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|-----------------|
| `PERCENT_SEGMENTS_AVAILABLE` | Gauge | Percentage of segments with at least one online replica. Per table. | < 100% |
| `SEGMENTS_IN_ERROR_STATE` | Gauge | Number of segments in ERROR state. Per table. | > 0 |
| `NUMBER_OF_REPLICAS` | Gauge | Number of complete replicas available. Per table. | Less than configured replication factor |
| `LLC_STREAM_DATA_LOSS` | Meter | Indicates data loss: offsets in stream are ahead of stored offsets or segments lost in CONSUMING state. | > 0 |
| `LLC_ZOOKEEPER_UPDATE_FAILURES` | Meter | Failures updating segment metadata in ZooKeeper. | > 0 |
| `IDEAL_STATE_UPDATE_FAILURE` | Meter | Failures updating the table ideal state in ZooKeeper. | > 0 |
| `CONTROLLER_PERIODIC_TASK_ERROR` | Meter | Periodic maintenance tasks (retention, validation) that failed. | > 0 |
| `HELIX_ZOOKEEPER_RECONNECTS` | Meter | ZooKeeper reconnections. Frequent reconnects indicate ZooKeeper instability. | > 1 per hour |
| `HEALTHCHECK_BAD_CALLS` | Meter | Failed health check requests. | > 0 sustained |
| `TABLE_STORAGE_QUOTA_UTILIZATION` | Gauge | Percentage of table storage quota in use. | > 85% |
| `MISSING_CONSUMING_SEGMENT_TOTAL_COUNT` | Gauge | Partitions with missing consuming segments. | > 0 |
| `MAX_SUBTASK_WAIT_TIME_MS` | Gauge | Maximum current wait time, in milliseconds, across `WAITING` minion subtasks for a table and task type. The controller rewrites the gauge every emit cycle and resets it to `0` when the queue drains. | Above your table-specific queue SLA |
| `MAX_SUBTASK_RUNNING_TIME_MS` | Gauge | Maximum current runtime, in milliseconds, across `RUNNING` minion subtasks for a table and task type. The controller rewrites the gauge every emit cycle and resets it to `0` when no subtasks are running. | Above your table-specific runtime SLA |

### Controller Diagnosis Patterns

**If `PERCENT_SEGMENTS_AVAILABLE` < 100%:**
- Some segments are not online; check `SEGMENTS_IN_ERROR_STATE` for errored segments
- Review the Pinot admin UI for segment assignment issues
- Check if servers hosting those segments are down or overloaded
- Look at `SEGMENTS_WITH_LESS_REPLICAS` to identify under-replicated segments

**If `SEGMENTS_IN_ERROR_STATE` > 0:**
- Segments failed to load on the server; check server logs for the root cause
- Common causes: corrupted segment files, schema mismatches, insufficient disk space
- Try resetting the segment via the controller API: `POST /segments/{tableName}/{segmentName}/reset`

**If `LLC_STREAM_DATA_LOSS` > 0:**
- Data has been lost, likely due to stream topic retention expiring before Pinot consumed the data
- Increase stream topic retention or ensure Pinot ingestion keeps up with the stream
- Check for prolonged consumption pauses or stuck partitions

**If `IDEAL_STATE_UPDATE_FAILURE` or `LLC_ZOOKEEPER_UPDATE_FAILURES` > 0:**
- ZooKeeper is likely under pressure or experiencing connectivity issues
- Check ZooKeeper cluster health, latency, and connection count
- Look at `HELIX_ZOOKEEPER_RECONNECTS` for connection instability
- Verify the ZooKeeper `jute.maxbuffer` is sufficient (tracked by `ZK_JUTE_MAX_BUFFER` gauge)

**If `MISSING_CONSUMING_SEGMENT_TOTAL_COUNT` > 0:**
- Some partitions do not have a consuming segment; new data is not being ingested for those partitions
- Check `MISSING_CONSUMING_SEGMENT_MAX_DURATION_MINUTES` for how long this has persisted
- Review controller logs for segment assignment errors

---

## Minion Metrics

Minions run background tasks such as segment compaction, purge, and merge. These metrics help track task health.

For table-specific queue alerts, prefer the controller gauges `MAX_SUBTASK_WAIT_TIME_MS` and `MAX_SUBTASK_RUNNING_TIME_MS` listed above. They are emitted per table and task type and self-resolve to `0` after the queue clears.

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|-----------------|
| `NUMBER_OF_TASKS` | Gauge | Tasks currently running | Baseline-dependent |
| `NUMBER_TASKS_FAILED` | Meter | Tasks that failed | > 0 |
| `NUMBER_TASKS_FATAL_FAILED` | Meter | Tasks with unretryable failures | > 0 |
| `TASK_QUEUEING` | Timer | Time tasks spend waiting in queue | > 10 minutes |
| `TASK_EXECUTION` | Timer | Time tasks spend executing | Baseline-dependent; watch for sustained increases |

---

## Setting Up Metrics Export

### JMX (Default)

By default, all Pinot metrics are published to JMX via the `JmxReporterMetricsRegistryRegistrationListener`. You can view them using tools like JConsole, VisualVM, or `jmxterm`.

### Prometheus via JMX Exporter

The recommended approach for production monitoring is to expose JMX metrics to Prometheus using the [JMX Exporter](https://github.com/prometheus/jmx_exporter) as a Java agent.

**Step 1: Download the JMX Exporter agent and config**

```bash
# Download the JMX Exporter Java agent
wget https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.20.0/jmx_prometheus_javaagent-0.20.0.jar

# Download the Pinot-specific JMX config
wget https://raw.githubusercontent.com/fx19880617/jmx_exporter/master/example_configs/pinot.yml
```

**Step 2: Add the agent to each Pinot component's JVM options**

```bash
# For each Pinot component (broker, server, controller), add the agent to JAVA_OPTS.
# Use a different port for each component if running on the same host.

# Controller (port 9000 for metrics)
export JAVA_OPTS="-javaagent:jmx_prometheus_javaagent-0.20.0.jar=9000:pinot.yml ${JAVA_OPTS}"

# Broker (port 9001 for metrics)
export JAVA_OPTS="-javaagent:jmx_prometheus_javaagent-0.20.0.jar=9001:pinot.yml ${JAVA_OPTS}"

# Server (port 9002 for metrics)
export JAVA_OPTS="-javaagent:jmx_prometheus_javaagent-0.20.0.jar=9002:pinot.yml ${JAVA_OPTS}"
```

If starting via `pinot-admin.sh`, pass the agent in `ALL_JAVA_OPTS`:

```bash
ALL_JAVA_OPTS="-javaagent:jmx_prometheus_javaagent-0.20.0.jar=9002:pinot.yml -Xms4G -Xmx4G -XX:MaxDirectMemorySize=30g -Dlog4j2.configurationFile=conf/pinot-admin-log4j2.xml -Dplugins.dir=$BASEDIR/plugins"
bin/pinot-admin.sh StartServer ...
```

**Step 3: Configure Prometheus to scrape the endpoints**

Add scrape targets to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'pinot-controller'
    static_configs:
      - targets: ['controller-host:9000']
  - job_name: 'pinot-broker'
    static_configs:
      - targets: ['broker-host:9001']
  - job_name: 'pinot-server'
    static_configs:
      - targets: ['server-host:9002']
```

For Kubernetes deployments with Helm, Prometheus scraping can be enabled directly in the Helm chart values. See the [Prometheus and Grafana tutorial](monitor-pinot-using-prometheus-and-grafana.md) for a complete walkthrough.

### Kubernetes / Helm Setup

If deploying Pinot using the official Helm chart, enable Prometheus metrics export in your `values.yaml`:

```yaml
controller:
  jvmOpts: "-javaagent:/opt/pinot/etc/jmx_prometheus_javaagent/jmx_prometheus_javaagent.jar=9000:/opt/pinot/etc/jmx_prometheus_javaagent/configs/pinot.yml"
broker:
  jvmOpts: "-javaagent:/opt/pinot/etc/jmx_prometheus_javaagent/jmx_prometheus_javaagent.jar=9000:/opt/pinot/etc/jmx_prometheus_javaagent/configs/pinot.yml"
server:
  jvmOpts: "-javaagent:/opt/pinot/etc/jmx_prometheus_javaagent/jmx_prometheus_javaagent.jar=9000:/opt/pinot/etc/jmx_prometheus_javaagent/configs/pinot.yml"
```

### Custom Metrics Reporter

You can write a custom listener to publish metrics to any metrics backend by implementing the `MetricsRegistryRegistrationListener` interface. Register it via the config property:

```
pinot.controller.metrics.metricsRegistryRegistrationListeners=com.example.MyCustomMetricsListener
pinot.broker.metrics.metricsRegistryRegistrationListeners=com.example.MyCustomMetricsListener
pinot.server.metrics.metricsRegistryRegistrationListeners=com.example.MyCustomMetricsListener
```

---

## Recommended Grafana Dashboards

When building dashboards, organize panels by component and focus on these key views:

**Cluster Overview:**
- Total QPS across all brokers (`QUERIES` meter)
- Number of unhealthy servers (`UNHEALTHY_SERVERS` gauge)
- Segment availability percentage (`PERCENT_SEGMENTS_AVAILABLE`)
- Segments in error state across all tables (`SEGMENTS_IN_ERROR_STATE`)

**Broker Dashboard:**
- Query latency percentiles (p50, p95, p99) from `QUERY_EXECUTION` timer
- Error rates: `BROKER_RESPONSES_WITH_PROCESSING_EXCEPTIONS`, `NO_SERVER_FOUND_EXCEPTIONS`
- Query quota utilization (`QUERY_QUOTA_CAPACITY_UTILIZATION_RATE`)
- Partial server responses (`BROKER_RESPONSES_WITH_PARTIAL_SERVERS_RESPONDED`)

**Server Dashboard:**
- Real-time ingestion delay per table (`REALTIME_INGESTION_DELAY_MS`)
- Consumption health per partition (`LLC_PARTITION_CONSUMING`)
- Documents scanned per query (`NUM_DOCS_SCANNED`)
- JVM heap and off-heap memory usage
- Segment download and reload failures

**Controller Dashboard:**
- Segment availability and error state per table
- ZooKeeper reconnections and update failures
- Periodic task execution and errors
- Table storage quota utilization


## JVM diagnostics (Continuous JFR)

For low-overhead, always-on JVM profiling (CPU, memory, threads, locks), you can enable [Continuous Java Flight Recorder (JFR)](continuous-jfr.md). JFR recordings can be dumped on exit or inspected with JDK tools; configuration is dynamic via cluster config.

---

## Further Reading

- [Monitoring overview](monitoring.md) -- Landing page for all monitoring topics
- [Full Metrics Reference](../reference/configuration-reference/monitoring-metrics.md) -- Complete list of all Pinot metrics
- [Prometheus and Grafana Tutorial](monitor-pinot-using-prometheus-and-grafana.md) -- Step-by-step setup for Kubernetes
- [Continuous JFR](continuous-jfr.md) -- Always-on JVM profiling with Java Flight Recorder
