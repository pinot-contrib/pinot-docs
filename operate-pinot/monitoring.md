# Monitoring

This section covers how to observe and troubleshoot an Apache Pinot cluster -- metrics collection, alerting, JVM diagnostics, and dashboard setup.

## Why monitoring matters

Pinot clusters serve real-time analytics workloads where latency spikes, ingestion delays, and segment failures directly affect end users. Proactive monitoring lets you catch problems before they become incidents.

## What Pinot exposes

Every Pinot component (controller, broker, server, minion) publishes metrics via [Dropwizard Metrics](https://metrics.dropwizard.io/4.0.0/) in three forms:

<table>
  <thead>
    <tr>
      <th>Metric type</th>
      <th>What it measures</th>
      <th>Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>**Gauge**</td>
      <td>Point-in-time value</td>
      <td>Segment count, JVM heap usage, ingestion delay</td>
    </tr>
    <tr>
      <td>**Meter**</td>
      <td>Rate per unit of time</td>
      <td>Queries per second, exceptions per second</td>
    </tr>
    <tr>
      <td>**Timer**</td>
      <td>Duration with percentiles</td>
      <td>Query latency p50/p95/p99</td>
    </tr>
  </tbody>
</table>

Metrics are available at **global** scope (per-instance) and **table-level** scope (per-table).

## Metrics export paths

<table>
  <thead>
    <tr>
      <th>Method</th>
      <th>Best for</th>
      <th>How it works</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>**JMX (default)**</td>
      <td>Development, ad-hoc inspection</td>
      <td>Metrics published via `JmxReporterMetricsRegistryRegistrationListener`; view with JConsole or VisualVM</td>
    </tr>
    <tr>
      <td>**Prometheus via JMX Exporter**</td>
      <td>Production Kubernetes and bare-metal</td>
      <td>Attach the JMX Exporter Java agent to each component; Prometheus scrapes the `/metrics` endpoint</td>
    </tr>
    <tr>
      <td>**Custom reporter**</td>
      <td>Datadog, InfluxDB, or other backends</td>
      <td>Implement `MetricsRegistryRegistrationListener` and register via config</td>
    </tr>
  </tbody>
</table>

## Key metrics to watch

A concise summary of the most important metrics per component:

- **Broker**: query rate (`QUERIES`), partial server responses, processing exceptions, query latency percentiles, heap usage
- **Server**: real-time ingestion delay, consumption health per partition, segment download failures, documents scanned, heap and off-heap usage
- **Controller**: segment availability percentage, segments in error state, ZooKeeper reconnects, stream data loss, missing consuming segments
- **Minion**: task failure count, task queue time, task execution time

For the complete list of metrics, alert thresholds, and diagnosis patterns, see the [Monitoring guide](../operators/operating-pinot/monitoring.md).

## JVM diagnostics with Continuous JFR

For low-overhead, always-on JVM profiling, Pinot supports **Continuous Java Flight Recorder (JFR)**. JFR captures CPU, memory, GC, thread, and lock events into `.jfr` files. Pinot provides cluster-level runtime control through `ContinuousJfrStarter` -- operators can toggle recording on/off or adjust settings without restarting processes.

Key configuration: set `pinot.jfr.enabled=true` in cluster config. Start with `configuration=default` for production safety; use `configuration=profile` only during active investigations.

For the full runbook, see [Continuous JFR](../operators/operating-pinot/continuous-jfr.md).

## Setting up Prometheus and Grafana

The recommended production monitoring stack is Prometheus for metrics collection and Grafana for dashboards. The setup involves:

1. Attach the JMX Exporter Java agent to each Pinot component's JVM options
2. Configure Prometheus scrape targets (or use Kubernetes pod annotations for auto-discovery)
3. Import a Pinot dashboard into Grafana

For a complete Kubernetes walkthrough, see [Monitor Pinot using Prometheus and Grafana](../tutorials/operations/monitor-pinot-using-prometheus-and-grafana.md).

## Prerequisites

- Pinot cluster deployed and running
- For Prometheus: JMX Exporter agent JAR and Pinot-specific JMX config (`pinot.yml`)
- For Grafana: a running Grafana instance with Prometheus configured as a data source
- For JFR: JDK 11+ (JFR is included in OpenJDK since Java 11)

## Child pages

<table>
  <thead>
    <tr>
      <th>Page</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Monitoring guide](../operators/operating-pinot/monitoring.md)</td>
      <td>Critical metrics reference with alert thresholds and diagnosis patterns for every component</td>
    </tr>
    <tr>
      <td>[Continuous JFR](../operators/operating-pinot/continuous-jfr.md)</td>
      <td>Runbook for always-on Java Flight Recorder profiling with dynamic cluster-level control</td>
    </tr>
    <tr>
      <td>[Monitor Pinot using Prometheus and Grafana](../tutorials/operations/monitor-pinot-using-prometheus-and-grafana.md)</td>
      <td>Step-by-step Kubernetes setup for Prometheus scraping and Grafana dashboards</td>
    </tr>
  </tbody>
</table>

## Next step

With monitoring in place, tune your cluster for optimal performance. Continue to Performance tuning.
