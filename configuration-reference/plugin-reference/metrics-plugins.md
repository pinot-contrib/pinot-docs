---
description: >-
  Configure Pinot's metrics system using pluggable metrics backends.
---

# Metrics Plugins

Apache Pinot uses a pluggable metrics factory to support multiple metrics backends. Each Pinot component (Server, Broker, Controller, Minion) can be independently configured with a metrics implementation.

## Available Implementations

<table>
  <thead>
    <tr>
      <th>Plugin</th>
      <th>Class Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>**Yammer** (default)</td>
      <td>`org.apache.pinot.plugin.metrics.yammer.YammerMetricsFactory`</td>
      <td>Lightweight, default metrics implementation</td>
    </tr>
    <tr>
      <td>**Dropwizard**</td>
      <td>`org.apache.pinot.plugin.metrics.dropwizard.DropwizardMetricsFactory`</td>
      <td>Full Dropwizard Metrics integration with sliding time window reservoirs</td>
    </tr>
    <tr>
      <td>**Compound**</td>
      <td>`org.apache.pinot.plugin.metrics.compound.CompoundPinotMetricsFactory`</td>
      <td>Registers metrics in multiple backends simultaneously</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Default</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot.<component>.metrics.dropwizard.domain`</td>
      <td>`org.apache.pinot.common.metrics`</td>
      <td>JMX domain name for metrics</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Default</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot.<component>.metrics.compound.algorithm`</td>
      <td>`CLASSPATH`</td>
      <td>Discovery algorithm: `CLASSPATH`, `SERVICE_LOADER`, or `LIST`</td>
    </tr>
    <tr>
      <td>`pinot.<component>.metrics.compound.ignored`</td>
      <td>(empty)</td>
      <td>Comma-separated list of factory class names to exclude</td>
    </tr>
    <tr>
      <td>`pinot.<component>.metrics.compound.list`</td>
      <td>(empty)</td>
      <td>Comma-separated list of factory class names to include (only with `algorithm=LIST`)</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>Type</th>
      <th>Description</th>
      <th>Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>**Counter**</td>
      <td>Discrete event counts</td>
      <td>Total queries processed</td>
    </tr>
    <tr>
      <td>**Meter**</td>
      <td>Event rates</td>
      <td>Queries per second</td>
    </tr>
    <tr>
      <td>**Timer**</td>
      <td>Latency and throughput</td>
      <td>Query execution time</td>
    </tr>
    <tr>
      <td>**Histogram**</td>
      <td>Value distributions</td>
      <td>Query result sizes</td>
    </tr>
    <tr>
      <td>**Gauge**</td>
      <td>Point-in-time values</td>
      <td>Segment count, heap usage</td>
    </tr>
  </tbody>
</table>

## JMX Reporting

All metrics implementations include a JMX reporter enabled by default. The `JmxReporterMetricsRegistryRegistrationListener` is automatically registered when the metrics system initializes.

To configure additional metrics reporting (e.g., Prometheus, Grafana), see [Monitor Pinot Using Prometheus and Grafana](../../tutorials/operations/monitor-pinot-using-prometheus-and-grafana.md).
