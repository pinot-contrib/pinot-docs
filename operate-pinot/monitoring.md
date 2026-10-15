# Monitoring

This section covers how to observe and troubleshoot an Apache Pinot cluster -- metrics collection, alerting, JVM diagnostics, and dashboard setup.

## Filtering broker new-segment routing logs

The two INFO messages from `org.apache.pinot.broker.routing.instanceselector.BaseInstanceSelector` describing new segments discovered through ZooKeeper metadata or existing states carry the Log4j2 marker `ROUTING_NEW_SEGMENTS`. To suppress just these messages, add the following filter to that broker logger in your Log4j2 configuration:

```xml
<MarkerFilter marker="ROUTING_NEW_SEGMENTS" onMatch="DENY" onMismatch="NEUTRAL"/>
```

Pinot's shipped logging configuration is unchanged: these messages remain at INFO unless you configure filtering. This marker does not change routing behavior or replica-health metrics.

*Source: [PR #19785](https://github.com/apache/pinot/pull/19785)*

## Why monitoring matters

Pinot clusters serve real-time analytics workloads where latency spikes, ingestion delays, and segment failures directly affect end users. Proactive monitoring lets you catch problems before they become incidents.

## What Pinot exposes

Every Pinot component (controller, broker, server, minion) publishes metrics via [Dropwizard Metrics](https://metrics.dropwizard.io/4.0.0/) in three forms:

| Metric type | What it measures | Example |
|-------------|-----------------|---------|
| **Gauge** | Point-in-time value | Segment count, JVM heap usage, ingestion delay |
| **Meter** | Rate per unit of time | Queries per second, exceptions per second |
| **Timer** | Duration with percentiles | Query latency p50/p95/p99 |

Metrics are available at **global** scope (per-instance) and **table-level** scope (per-table).

## Metrics export paths

| Method | Best for | How it works |
|--------|----------|-------------|
| **JMX (default)** | Development, ad-hoc inspection | Metrics published via `JmxReporterMetricsRegistryRegistrationListener`; view with JConsole or VisualVM |
| **Prometheus via JMX Exporter** | Production Kubernetes and bare-metal | Attach the JMX Exporter Java agent to each component; Prometheus scrapes the `/metrics` endpoint |
| **Custom reporter** | Datadog, InfluxDB, or other backends | Implement `MetricsRegistryRegistrationListener` and register via config |

## Key metrics to watch

A concise summary of the most important metrics per component:

- **Broker**: query rate (`QUERIES`), partial server responses, processing exceptions, query latency percentiles, heap usage
- **Server**: real-time ingestion delay, consumption health per partition, segment download failures, documents scanned, heap and off-heap usage
- **Controller**: segment availability percentage, segments in error state, ZooKeeper reconnects, stream data loss, missing consuming segments
- **Minion**: task failure count, task queue time, task execution time

For the complete list of metrics, alert thresholds, and diagnosis patterns, see the [Monitoring guide](monitoring.md).

## Broker routing rebuild metrics

Use these broker metrics to distinguish frequent assignment changes from slow or failing routing rebuilds. Table-level metrics use the table name with its type (`_OFFLINE` or `_REALTIME`).

| Metric name | Type and scope | Meaning |
| --- | --- | --- |
| `routingTableUpdateTime` | Timer, per table and global | Successful assignment-change rebuild duration, including reads of the ideal state and external view and rebuilding routing components |
| `routingTableUpdateSuccess` | Meter, per table | Successful routing updates triggered by an ideal-state or external-view version change |
| `routingTableUpdateFailure` | Meter, per table | Exceptions during assignment-change updates; not included in the success meter or timer |
| `routingTableSegments` | Gauge, per table | Online segments in the ideal state retained by the segment pre-selector, not total stored segments or replica count |

The success/failure meters and timer cover assignment-change rebuilds, not full routing builds such as those caused by table configuration changes. Missing ideal state or external view skips an update without counting an exception failure. After an exception, the routing entry retains its old versions so the next change can retry. The segment gauge is set on a successful full build and refreshed after assignment-change processing; it is removed when the table's routing is removed.

The existing JMX exporter rules in `broker.yml` and `pinot.yml` export these metrics; Prometheus names and labels follow those exporter rules. See [apache/pinot#19784](https://github.com/apache/pinot/pull/19784).

## JVM diagnostics with Continuous JFR

For low-overhead, always-on JVM profiling, Pinot supports **Continuous Java Flight Recorder (JFR)**. JFR captures CPU, memory, GC, thread, and lock events into `.jfr` files. Pinot provides cluster-level runtime control through `ContinuousJfrStarter` -- operators can toggle recording on/off or adjust settings without restarting processes.

Key configuration: set `pinot.jfr.enabled=true` in cluster config. Start with `configuration=default` for production safety; use `configuration=profile` only during active investigations.

For the full runbook, see [Continuous JFR](continuous-jfr.md).

## Setting up Prometheus and Grafana

The recommended production monitoring stack is Prometheus for metrics collection and Grafana for dashboards. The setup involves:

1. Attach the JMX Exporter Java agent to each Pinot component's JVM options
2. Configure Prometheus scrape targets (or use Kubernetes pod annotations for auto-discovery)
3. Import a Pinot dashboard into Grafana

For a complete Kubernetes walkthrough, see [Monitor Pinot using Prometheus and Grafana](monitor-pinot-using-prometheus-and-grafana.md).

## Prerequisites

- Pinot cluster deployed and running
- For Prometheus: JMX Exporter agent JAR and Pinot-specific JMX config (`pinot.yml`)
- For Grafana: a running Grafana instance with Prometheus configured as a data source
- For JFR: JDK 11+ (JFR is included in OpenJDK since Java 11)

## Child pages

| Page | Description |
|------|-------------|
| [Monitoring guide](monitoring.md) | Critical metrics reference with alert thresholds and diagnosis patterns for every component |
| [Continuous JFR](continuous-jfr.md) | Runbook for always-on Java Flight Recorder profiling with dynamic cluster-level control |
| [Monitor Pinot using Prometheus and Grafana](monitor-pinot-using-prometheus-and-grafana.md) | Step-by-step Kubernetes setup for Prometheus scraping and Grafana dashboards |

## Next step

With monitoring in place, tune your cluster for optimal performance. Continue to Performance tuning.
