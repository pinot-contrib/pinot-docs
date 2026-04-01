# Monitoring

This guide covers the critical metrics to monitor in an Apache Pinot cluster, organized by component. It includes recommended alert thresholds and diagnosis patterns to help operators quickly identify and resolve issues.

For the full list of all available metrics, see the [Monitoring Metrics Reference](../../configuration-reference/monitoring-metrics.md).

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

<table>
  <thead>
    <tr>
      <th>Metric</th>
      <th>Type</th>
      <th>Description</th>
      <th>Alert Threshold</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`QUERIES`</td>
      <td>Meter</td>
      <td>Query rate (QPS) per table. Use to track traffic patterns.</td>
      <td>Baseline-dependent; alert on sudden drops (>50% below baseline) which may indicate client issues</td>
    </tr>
    <tr>
      <td>`BROKER_RESPONSES_WITH_PARTIAL_SERVERS_RESPONDED`</td>
      <td>Meter</td>
      <td>Queries where not all servers responded. Indicates servers are down or overloaded.</td>
      <td>> 0 sustained over 5 minutes</td>
    </tr>
    <tr>
      <td>`BROKER_RESPONSES_WITH_PROCESSING_EXCEPTIONS`</td>
      <td>Meter</td>
      <td>Queries with at least one processing exception from servers.</td>
      <td>> 1% of total QPS</td>
    </tr>
    <tr>
      <td>`QUERY_EXECUTION_EXCEPTIONS` (via timer)</td>
      <td>Timer</td>
      <td>Total query execution time. Monitor p99 for latency SLAs.</td>
      <td>p99 > your SLA (e.g., 500ms)</td>
    </tr>
    <tr>
      <td>`NO_SERVER_FOUND_EXCEPTIONS`</td>
      <td>Meter</td>
      <td>Queries where no server was found to serve data. Critical availability issue.</td>
      <td>> 0</td>
    </tr>
    <tr>
      <td>`REQUEST_TIMEOUT_BEFORE_SCATTERED_EXCEPTIONS`</td>
      <td>Meter</td>
      <td>Queries that timed out before being sent to servers.</td>
      <td>> 0 sustained</td>
    </tr>
    <tr>
      <td>`QUERY_QUOTA_EXCEEDED`</td>
      <td>Meter</td>
      <td>Queries rejected due to rate limiting.</td>
      <td>> 0 (if unexpected)</td>
    </tr>
    <tr>
      <td>`UNHEALTHY_SERVERS`</td>
      <td>Gauge</td>
      <td>Number of servers detected as unhealthy.</td>
      <td>> 0</td>
    </tr>
    <tr>
      <td>`HEAP_CRITICAL_LEVEL_EXCEEDED`</td>
      <td>Meter</td>
      <td>Times heap usage exceeded the critical threshold.</td>
      <td>> 0</td>
    </tr>
    <tr>
      <td>`JVM_HEAP_USED_BYTES`</td>
      <td>Gauge</td>
      <td>Current JVM heap usage on the broker.</td>
      <td>> 85% of max heap</td>
    </tr>
    <tr>
      <td>`QUERY_QUOTA_CAPACITY_UTILIZATION_RATE`</td>
      <td>Gauge</td>
      <td>Percentage of configured rate limit in use.</td>
      <td>> 80%</td>
    </tr>
  </tbody>
</table>

### Broker Query Latency Breakdown

These timers help identify which phase of query execution is slow:

<table>
  <thead>
    <tr>
      <th>Metric</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`REQUEST_COMPILATION`</td>
      <td>Time spent compiling the SQL query</td>
    </tr>
    <tr>
      <td>`AUTHORIZATION`</td>
      <td>Time spent checking table access permissions</td>
    </tr>
    <tr>
      <td>`QUERY_ROUTING`</td>
      <td>Time spent building the routing table for segments</td>
    </tr>
    <tr>
      <td>`SCATTER_GATHER`</td>
      <td>Time spent sending requests to servers and collecting responses</td>
    </tr>
    <tr>
      <td>`REDUCE`</td>
      <td>Time spent merging results from multiple servers</td>
    </tr>
    <tr>
      <td>`QUERY_EXECUTION`</td>
      <td>Total end-to-end query execution time</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>Metric</th>
      <th>Type</th>
      <th>Description</th>
      <th>Alert Threshold</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`REALTIME_INGESTION_DELAY_MS`</td>
      <td>Gauge</td>
      <td>Delay in milliseconds between event production and Pinot consumption. Per-partition metric.</td>
      <td>> 5 minutes (300000ms) for most use cases; adjust based on freshness SLA</td>
    </tr>
    <tr>
      <td>`LLC_PARTITION_CONSUMING`</td>
      <td>Gauge</td>
      <td>Binary: 1 if low-level consumption is healthy, 0 if unhealthy. Per table-partition.</td>
      <td>= 0 on any partition</td>
    </tr>
    <tr>
      <td>`REALTIME_CONSUMPTION_EXCEPTIONS`</td>
      <td>Meter</td>
      <td>Exceptions during real-time consumption.</td>
      <td>> 0 sustained</td>
    </tr>
    <tr>
      <td>`QUERY_EXECUTION_EXCEPTIONS`</td>
      <td>Meter</td>
      <td>Exceptions during query execution on the server.</td>
      <td>> 1% of queries</td>
    </tr>
    <tr>
      <td>`QUERIES`</td>
      <td>Meter</td>
      <td>Query rate hitting this server.</td>
      <td>Sudden drop or spike vs. baseline</td>
    </tr>
    <tr>
      <td>`NUM_MISSING_SEGMENTS`</td>
      <td>Meter</td>
      <td>Segments the broker expected but the server did not have.</td>
      <td>> 0 sustained</td>
    </tr>
    <tr>
      <td>`SEGMENT_DOWNLOAD_FAILURES`</td>
      <td>Meter</td>
      <td>Failures downloading segments from deep store.</td>
      <td>> 0</td>
    </tr>
    <tr>
      <td>`RELOAD_FAILURES`</td>
      <td>Meter</td>
      <td>Failures reloading segments after config changes.</td>
      <td>> 0</td>
    </tr>
    <tr>
      <td>`ROWS_WITH_ERRORS`</td>
      <td>Meter</td>
      <td>Rows that failed transformation or indexing during ingestion.</td>
      <td>> 0.1% of `REALTIME_ROWS_CONSUMED`</td>
    </tr>
    <tr>
      <td>`JVM_HEAP_USED_BYTES`</td>
      <td>Gauge</td>
      <td>Current JVM heap usage on the server.</td>
      <td>> 85% of max heap</td>
    </tr>
    <tr>
      <td>`HEAP_CRITICAL_LEVEL_EXCEEDED`</td>
      <td>Meter</td>
      <td>Times heap usage exceeded the critical threshold, triggering query killing.</td>
      <td>> 0</td>
    </tr>
    <tr>
      <td>`REALTIME_OFFHEAP_MEMORY_USED`</td>
      <td>Gauge</td>
      <td>Off-heap memory used by real-time segments.</td>
      <td>Approaching configured `MaxDirectMemorySize`</td>
    </tr>
  </tbody>
</table>

### Server Query Latency Breakdown

<table>
  <thead>
    <tr>
      <th>Metric</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`SCHEDULER_WAIT`</td>
      <td>Time waiting in the scheduler queue before execution begins</td>
    </tr>
    <tr>
      <td>`SEGMENT_PRUNING`</td>
      <td>Time spent pruning irrelevant segments</td>
    </tr>
    <tr>
      <td>`BUILD_QUERY_PLAN`</td>
      <td>Time spent building the query execution plan</td>
    </tr>
    <tr>
      <td>`QUERY_PLAN_EXECUTION`</td>
      <td>Time spent executing the query plan against segments</td>
    </tr>
    <tr>
      <td>`RESPONSE_SERIALIZATION`</td>
      <td>Time spent serializing results to send back to the broker</td>
    </tr>
    <tr>
      <td>`TOTAL_QUERY_TIME`</td>
      <td>Total time from receiving the query to returning the response</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>Metric</th>
      <th>Type</th>
      <th>Description</th>
      <th>Alert Threshold</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`PERCENT_SEGMENTS_AVAILABLE`</td>
      <td>Gauge</td>
      <td>Percentage of segments with at least one online replica. Per table.</td>
      <td>< 100%</td>
    </tr>
    <tr>
      <td>`SEGMENTS_IN_ERROR_STATE`</td>
      <td>Gauge</td>
      <td>Number of segments in ERROR state. Per table.</td>
      <td>> 0</td>
    </tr>
    <tr>
      <td>`NUMBER_OF_REPLICAS`</td>
      <td>Gauge</td>
      <td>Number of complete replicas available. Per table.</td>
      <td>Less than configured replication factor</td>
    </tr>
    <tr>
      <td>`LLC_STREAM_DATA_LOSS`</td>
      <td>Meter</td>
      <td>Indicates data loss: offsets in stream are ahead of stored offsets or segments lost in CONSUMING state.</td>
      <td>> 0</td>
    </tr>
    <tr>
      <td>`LLC_ZOOKEEPER_UPDATE_FAILURES`</td>
      <td>Meter</td>
      <td>Failures updating segment metadata in ZooKeeper.</td>
      <td>> 0</td>
    </tr>
    <tr>
      <td>`IDEAL_STATE_UPDATE_FAILURE`</td>
      <td>Meter</td>
      <td>Failures updating the table ideal state in ZooKeeper.</td>
      <td>> 0</td>
    </tr>
    <tr>
      <td>`CONTROLLER_PERIODIC_TASK_ERROR`</td>
      <td>Meter</td>
      <td>Periodic maintenance tasks (retention, validation) that failed.</td>
      <td>> 0</td>
    </tr>
    <tr>
      <td>`HELIX_ZOOKEEPER_RECONNECTS`</td>
      <td>Meter</td>
      <td>ZooKeeper reconnections. Frequent reconnects indicate ZooKeeper instability.</td>
      <td>> 1 per hour</td>
    </tr>
    <tr>
      <td>`HEALTHCHECK_BAD_CALLS`</td>
      <td>Meter</td>
      <td>Failed health check requests.</td>
      <td>> 0 sustained</td>
    </tr>
    <tr>
      <td>`TABLE_STORAGE_QUOTA_UTILIZATION`</td>
      <td>Gauge</td>
      <td>Percentage of table storage quota in use.</td>
      <td>> 85%</td>
    </tr>
    <tr>
      <td>`MISSING_CONSUMING_SEGMENT_TOTAL_COUNT`</td>
      <td>Gauge</td>
      <td>Partitions with missing consuming segments.</td>
      <td>> 0</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>Metric</th>
      <th>Type</th>
      <th>Description</th>
      <th>Alert Threshold</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`NUMBER_OF_TASKS`</td>
      <td>Gauge</td>
      <td>Tasks currently running</td>
      <td>Baseline-dependent</td>
    </tr>
    <tr>
      <td>`NUMBER_TASKS_FAILED`</td>
      <td>Meter</td>
      <td>Tasks that failed</td>
      <td>> 0</td>
    </tr>
    <tr>
      <td>`NUMBER_TASKS_FATAL_FAILED`</td>
      <td>Meter</td>
      <td>Tasks with unretryable failures</td>
      <td>> 0</td>
    </tr>
    <tr>
      <td>`TASK_QUEUEING`</td>
      <td>Timer</td>
      <td>Time tasks spend waiting in queue</td>
      <td>> 10 minutes</td>
    </tr>
    <tr>
      <td>`TASK_EXECUTION`</td>
      <td>Timer</td>
      <td>Time tasks spend executing</td>
      <td>Baseline-dependent; watch for sustained increases</td>
    </tr>
  </tbody>
</table>

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

For Kubernetes deployments with Helm, Prometheus scraping can be enabled directly in the Helm chart values. See the [Prometheus and Grafana tutorial](../../tutorials/operations/monitor-pinot-using-prometheus-and-grafana.md) for a complete walkthrough.

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

- [Monitoring overview](../../operate-pinot/monitoring.md) -- Landing page for all monitoring topics
- [Full Metrics Reference](../../configuration-reference/monitoring-metrics.md) -- Complete list of all Pinot metrics
- [Prometheus and Grafana Tutorial](../../tutorials/operations/monitor-pinot-using-prometheus-and-grafana.md) -- Step-by-step setup for Kubernetes
- [Continuous JFR](continuous-jfr.md) -- Always-on JVM profiling with Java Flight Recorder
