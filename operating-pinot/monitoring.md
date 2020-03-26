# Monitoring

## Key Metrics to Watch

Pinot exposes several metrics to monitor the service and ensure that pinot users are not experiencing issues. In this section we discuss some of the key metrics that are useful to monitor. A full list of metrics is available in the [Customizing Metrics](monitoring.md#customizing-metrics) section.

### Pinot Server

* Missing Segments - [NUM\_MISSING\_SEGMENTS](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/ServerMeter.java)
  * Number of missing segments that the broker queried for \(expected to be on the server\) but the server didn’t have. This can be due to retention or stale routing table.
* Query latency - [TOTAL\_QUERY\_TIME](https://github.com/apache/incubator-pinot/blob/ce2d9ee9dc73b2d7273a63a4eede774eb024ea8f/pinot-common/src/main/java/org/apache/pinot/common/metrics/ServerQueryPhase.java)
  * Total time to take from receiving to finishing executing the query.
* Query Execution Exceptions - [QUERY\_EXECUTION\_EXCEPTIONS](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/ServerMeter.java)
  * The number of exception which might have occurred during query execution.
* Realtime Consumption Status - [LLC\_PARTITION\_CONSUMING](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/ServerGauge.java)
  * This gives a binary value based on whether low-level consumption is healthy \(1\) or unhealthy \(0\). It’s important to ensure at least a single replica of each partition is consuming.
* Realtime Highest Offset Consumed - [HIGHEST\_STREAM\_OFFSET\_CONSUMED](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/ServerGauge.java)
  * The highest offset which has been consumed so far.

### Pinot Broker

* Incoming QPS \(per broker\) - [QUERIES](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/BrokerMeter.java)
  * The rate which an individual broker is receiving queries. Units are in QPS.
* Dropped Requests - [REQUEST\_DROPPED\_DUE\_TO\_SEND\_ERROR](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/BrokerMeter.java), [REQUEST\_DROPPED\_DUE\_TO\_CONNECTION\_ERROR](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/BrokerMeter.java), [REQUEST\_DROPPED\_DUE\_TO\_ACCESS\_ERROR](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/BrokerMeter.java)
  * These multiple metrics will indicate if a query is dropped, ie the processing of that query has been forfeited for some reason.
* Partial Responses - [BROKER\_RESPONSES\_WITH\_PARTIAL\_SERVERS\_RESPONDED](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/BrokerMeter.java)
  * Indicates a count of partial responses. A partial response is when at least 1 of the requested servers fails to respond to the query.
* Table QPS quota exceeded - [QUERY\_QUOTA\_EXCEEDED](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/BrokerMeter.java)
  * Binary metric which will indicate when the configured QPS quota for a table is exceeded \(1\) or if there is capacity remaining \(0\).
* Table QPS quota usage percent - [QUERY\_QUOTA\_CAPACITY\_UTILIZATION\_RATE](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/BrokerGauge.java)
  * Percentage of the configured QPS quota being utilized.

### Pinot Controller

Many of the controller metrics include a table name and thus are dynamically generated in the code. The metrics below point to the classes which generate the corresponding metrics.

To get the real metric name, the easiest route is to spin up a controller instance, create a table with the desired name and look through the generated metrics.

Todo

Give a more detailed explanation of how metrics are generated, how to identify real metrics names and where to find them in the code.

* Percent Segments Available - [PERCENT\_SEGMENTS\_AVAILABLE](https://github.com/apache/incubator-pinot/blob/ce2d9ee9dc73b2d7273a63a4eede774eb024ea8f/pinot-common/src/main/java/org/apache/pinot/common/metrics/ControllerGauge.java)
  * Percentage of complete online replicas in external view as compared to replicas in ideal state.
* Segments in Error State - [SEGMENTS\_IN\_ERROR\_STATE](https://github.com/apache/incubator-pinot/blob/ce2d9ee9dc73b2d7273a63a4eede774eb024ea8f/pinot-common/src/main/java/org/apache/pinot/common/metrics/ControllerGauge.java)
  * Number of segments in an `ERROR` state for a given table.
* Last push delay - Generated in the [ValidationMetrics](https://github.com/apache/incubator-pinot/blob/ce2d9ee9dc73b2d7273a63a4eede774eb024ea8f/pinot-common/src/main/java/org/apache/pinot/common/metrics/ValidationMetrics.java) class.
  * The time in hours since the last time an offline segment has been pushed to the controller.
* Percent of replicas up - [PERCENT\_OF\_REPLICAS](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/ControllerGauge.java)
  * Percentage of complete online replicas in external view as compared to replicas in ideal state.
* Table storage quota usage percent - [TABLE\_STORAGE\_QUOTA\_UTILIZATION](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/ControllerGauge.java)
  * Shows how much of the table’s storage quota is currently being used, metric will a percentage of a the entire quota.

## 

## Customizing Metrics

Pinot uses [yammer MetricsRegistry](https://metrics.dropwizard.io/4.0.0/) to collect metrics within our application components. These metrics can be published to a metrics server with the help of [MetricsRegistryRegistrationListener](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/MetricsRegistryRegistrationListener.java) interface. By default, metrics are published to JMX using the [JmxReporterMetricsRegistryRegistrationListener](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/JmxReporterMetricsRegistryRegistrationListener.java).

You can write a listener to publish metrics to another metrics server by implementing the `MetricsRegistryRegistrationListener` interface. This listener can be injected into the controller by setting the fully qualified name of the class in the controller configs for the property `pinot.controller.metrics.metricsRegistryRegistrationListeners`.

You would have to design your own systems to view and monitor these metrics. A list of all the metrics published for each component can be found in:

* [ControllerMeter](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/ControllerMeter.java)
* [ControllerGauge](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/ControllerGauge.java)
* [BrokerMeter](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/BrokerMeter.java)
* [BrokerGauge](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/BrokerGauge.java)
* [ServerMeter](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/ServerMeter.java)
* [ServerGauge](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/ServerGauge.java)
* [MinionMeter](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/MinionMeter.java)
* [MinionGauge](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/MinionGauge.java)

## JMX to Prometheus

Metrics published to JMX could also be exposed to Prometheus through tooling like [jmx\_reporter](https://github.com/prometheus/jmx_exporter).

To run as a javaagent, [download jmx\_prometheus\_javaagent jar](https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.12.0/jmx_prometheus_javaagent-0.12.0.jar) and [pinot.yml](https://raw.githubusercontent.com/fx19880617/jmx_exporter/master/example_configs/pinot.yml) run:

```text
ALL_JAVA_OPTS="-javaagent:jmx_prometheus_javaagent-0.12.0.jar=8080:pinot.yml -Xms4G -Xmx4G -XX:MaxDirectMemorySize=30g -Dlog4j2.configurationFile=conf/pinot-admin-log4j2.xml -Dplugins.dir=$BASEDIR/plugins"
bin/pinot-admin.sh ....
```

This will expose a port at _**8080**_ to dump metrics as Prometheus format for Prometheus scrapper to fetch.

