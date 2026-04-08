# Metrics Plugin

## Overview

The Metrics plugin controls which metrics library Pinot uses to collect and expose internal metrics. All Pinot components (broker, server, controller, minion) use the `PinotMetricsFactory` SPI to create metric registries, counters, gauges, meters, timers, and JMX reporters.

Pinot ships with three metrics implementations:

| Implementation | Class | Description |
| --- | --- | --- |
| **Dropwizard** | `DropwizardMetricsFactory` | Based on Dropwizard Metrics (formerly Codahale). This is the default. |
| **Yammer** | `YammerMetricsFactory` | Based on Yammer Metrics, used in older Pinot versions. |
| **Compound** | `CompoundPinotMetricsFactory` | A meta-implementation that fans metrics out to multiple registries simultaneously. Useful for comparing or migrating between metrics libraries. |

## Configuration

To configure which metrics factory Pinot uses, set the following property in the component configuration (broker, server, controller, or minion):

```properties
pinot.<component>.metrics.factory.className=org.apache.pinot.plugin.metrics.dropwizard.DropwizardMetricsFactory
```

Replace `<component>` with `broker`, `server`, `controller`, or `minion`.

### Dropwizard Configuration

The Dropwizard metrics plugin supports an optional JMX domain property:

```properties
pinot.metrics.dropwizard.domain=org.apache.pinot.common.metrics
```

If not set, the default domain `org.apache.pinot.common.metrics` is used.

### Yammer Configuration

The Yammer metrics plugin does not require any additional configuration beyond setting the factory class name.

### Compound Metrics Configuration

The Compound metrics factory reports to multiple metrics registries at once. This is useful for comparing behavior between different implementations during a migration.

```properties
pinot.<component>.metrics.factory.className=org.apache.pinot.plugin.metrics.compound.CompoundPinotMetricsFactory
```

The following additional properties control how the Compound factory discovers sub-factories:

| Property Suffix | Values | Description |
| --- | --- | --- |
| `compound.algorithm` | `CLASSPATH` (default), `SERVICE_LOADER`, `LIST` | How to discover sub-factories. |
| `compound.ignored` | Comma-separated class names | Metrics factory classes to exclude. |
| `compound.list` | Comma-separated class names | Explicit list of factory classes (used with `LIST` algorithm). |

## SPI Interface

To write a custom metrics plugin, implement the [PinotMetricsFactory](https://github.com/apache/pinot/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/annotations/metrics/PinotMetricsFactory.java) interface:

```java
public interface PinotMetricsFactory {
  void init(PinotConfiguration metricsConfiguration);
  PinotMetricsRegistry getPinotMetricsRegistry();
  PinotMetricName makePinotMetricName(Class<?> klass, String name);
  <T> PinotGauge<T> makePinotGauge(Function<Void, T> condition);
  PinotJmxReporter makePinotJmxReporter(PinotMetricsRegistry metricsRegistry);
  String getMetricsFactoryName();
}
```

### Key Methods

| Method | Description |
| --- | --- |
| `init(PinotConfiguration)` | Initializes the factory with Pinot configuration. |
| `getPinotMetricsRegistry()` | Returns the singleton metrics registry instance. |
| `makePinotMetricName(Class, String)` | Creates a metric name scoped to a class. |
| `makePinotGauge(Function)` | Creates a gauge metric backed by the provided function. |
| `makePinotJmxReporter(PinotMetricsRegistry)` | Creates a JMX reporter for the given registry. |
| `getMetricsFactoryName()` | Returns a human-readable name for the factory. |

## Writing a Custom Metrics Plugin

To implement a custom metrics plugin:

1. Create a class that implements `PinotMetricsFactory`.
2. Annotate it with `@AutoService(PinotMetricsFactory.class)` and `@MetricsFactory`.
3. Implement wrapper classes for the Pinot metric types (`PinotCounter`, `PinotGauge`, `PinotMeter`, `PinotTimer`, `PinotMetricsRegistry`, `PinotJmxReporter`).
4. Package it as a Pinot plugin (see [Write Custom Plugins](./)).
5. Place the plugin JAR in the Pinot `/plugins` directory.

A custom metrics plugin could be useful for integrating with monitoring systems such as Prometheus, Micrometer, or OpenTelemetry.
