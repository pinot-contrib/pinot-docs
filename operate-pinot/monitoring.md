# Monitoring

This section covers how to observe and troubleshoot an Apache Pinot cluster -- metrics collection, alerting, JVM diagnostics, and dashboard setup.

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
