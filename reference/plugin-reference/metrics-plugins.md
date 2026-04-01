---
description: >-
  Configure Pinot's metrics system using pluggable metrics backends.
---

# Metrics Plugins

Apache Pinot uses a pluggable metrics factory to support multiple metrics backends. Each Pinot component (Server, Broker, Controller, Minion) can be independently configured with a metrics implementation.

## Available Implementations

| Plugin | Class Name | Description |
|--------|-----------|-------------|
| **Yammer** (default) | `org.apache.pinot.plugin.metrics.yammer.YammerMetricsFactory` | Lightweight, default metrics implementation |
| **Dropwizard** | `org.apache.pinot.plugin.metrics.dropwizard.DropwizardMetricsFactory` | Full Dropwizard Metrics integration with sliding time window reservoirs |
| **Compound** | `org.apache.pinot.plugin.metrics.compound.CompoundPinotMetricsFactory` | Registers metrics in multiple backends simultaneously |

## Configuration

Configure the metrics factory for any component using:

```properties
pinot.<component>.metrics.factory.className=<factory-class-name>
```

Where `<component>` is one of: `server`, `broker`, `controller`, `minion`.

### Yammer Metrics (Default)

The default metrics backend. No additional configuration required.

```properties
pinot.server.metrics.factory.className=org.apache.pinot.plugin.metrics.yammer.YammerMetricsFactory
```

### Dropwizard Metrics

Provides full Dropwizard Metrics library integration with sliding 15-minute time window reservoirs, detailed histograms and timers, and JMX reporting.

```properties
pinot.server.metrics.factory.className=org.apache.pinot.plugin.metrics.dropwizard.DropwizardMetricsFactory
```

**Additional properties:**

| Property | Default | Description |
|----------|---------|-------------|
| `pinot.<component>.metrics.dropwizard.domain` | `org.apache.pinot.common.metrics` | JMX domain name for metrics |

**Example:**

```properties
pinot.server.metrics.factory.className=org.apache.pinot.plugin.metrics.dropwizard.DropwizardMetricsFactory
pinot.server.metrics.dropwizard.domain=my.company.pinot.metrics
```

### Compound Metrics (Multi-Backend)

The Compound metrics plugin registers metrics in multiple backends simultaneously. This is useful for comparing metric implementations or reporting to multiple monitoring systems.

```properties
pinot.server.metrics.factory.className=org.apache.pinot.plugin.metrics.compound.CompoundPinotMetricsFactory
```

**Additional properties:**

| Property | Default | Description |
|----------|---------|-------------|
| `pinot.<component>.metrics.compound.algorithm` | `CLASSPATH` | Discovery algorithm: `CLASSPATH`, `SERVICE_LOADER`, or `LIST` |
| `pinot.<component>.metrics.compound.ignored` | (empty) | Comma-separated list of factory class names to exclude |
| `pinot.<component>.metrics.compound.list` | (empty) | Comma-separated list of factory class names to include (only with `algorithm=LIST`) |

**Example: Use both Yammer and Dropwizard:**

```properties
pinot.server.metrics.factory.className=org.apache.pinot.plugin.metrics.compound.CompoundPinotMetricsFactory
pinot.server.metrics.compound.algorithm=LIST
pinot.server.metrics.compound.list=org.apache.pinot.plugin.metrics.yammer.YammerMetricsFactory,org.apache.pinot.plugin.metrics.dropwizard.DropwizardMetricsFactory
```

**Example: Classpath discovery excluding Yammer:**

```properties
pinot.server.metrics.factory.className=org.apache.pinot.plugin.metrics.compound.CompoundPinotMetricsFactory
pinot.server.metrics.compound.algorithm=CLASSPATH
pinot.server.metrics.compound.ignored=org.apache.pinot.plugin.metrics.yammer.YammerMetricsFactory
```

{% hint style="warning" %}
When using Compound metrics, ensure JMX MBean names don't conflict between registries. Conflicting MBean names may cause unpredictable metric values.
{% endhint %}

## Metric Types

Pinot exposes the following metric primitives through all backends:

| Type | Description | Example |
|------|-------------|---------|
| **Counter** | Discrete event counts | Total queries processed |
| **Meter** | Event rates | Queries per second |
| **Timer** | Latency and throughput | Query execution time |
| **Histogram** | Value distributions | Query result sizes |
| **Gauge** | Point-in-time values | Segment count, heap usage |

## JMX Reporting

All metrics implementations include a JMX reporter enabled by default. The `JmxReporterMetricsRegistryRegistrationListener` is automatically registered when the metrics system initializes.

To configure additional metrics reporting (e.g., Prometheus, Grafana), see [Monitor Pinot Using Prometheus and Grafana](../../operate-pinot/monitor-pinot-using-prometheus-and-grafana.md).
