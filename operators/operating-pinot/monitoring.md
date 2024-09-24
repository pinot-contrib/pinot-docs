# Monitoring

## Tutorial

If you are deploying using the helm chart with Kubernetes, see the tutorial on setting up Prometheus and Grafana to monitor Pinot.

[https://docs.pinot.apache.org/users/tutorials/monitor-pinot-using-prometheus-and-grafana](https://docs.pinot.apache.org/users/tutorials/monitor-pinot-using-prometheus-and-grafana)

## Key Metrics to Watch

Refer to key metrics documented in [monitoring pinot](../../configuration-reference/monitoring-metrics.md).

## Customizing Metrics

Pinot uses [yammer MetricsRegistry](https://metrics.dropwizard.io/4.0.0/) to collect metrics within our application components. These metrics can be published to a metrics server with the help of [MetricsRegistryRegistrationListener](https://github.com/apache/pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/MetricsRegistryRegistrationListener.java) interface. By default, metrics are published to JMX using the [JmxReporterMetricsRegistryRegistrationListener](https://github.com/apache/pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/metrics/JmxReporterMetricsRegistryRegistrationListener.java).

You can write a listener to publish metrics to another metrics server by implementing the `MetricsRegistryRegistrationListener` interface. This listener can be injected into the controller by setting the fully qualified name of the class in the controller configs for the property `pinot.controller.metrics.metricsRegistryRegistrationListeners`.

You would have to design your own systems to view and monitor these metrics. You can refer to complete list of supported metrics on our [Metrics reference page](../../configuration-reference/monitoring-metrics.md).&#x20;

## JMX to Prometheus

Metrics published to JMX could also be exposed to Prometheus through tooling like [jmx\_reporter](https://github.com/prometheus/jmx\_exporter).

To run as a javaagent, [download jmx\_prometheus\_javaagent jar](https://repo1.maven.org/maven2/io/prometheus/jmx/jmx\_prometheus\_javaagent/0.12.0/jmx\_prometheus\_javaagent-0.12.0.jar) and [pinot.yml](https://raw.githubusercontent.com/fx19880617/jmx\_exporter/master/example\_configs/pinot.yml) run:

```
ALL_JAVA_OPTS="-javaagent:jmx_prometheus_javaagent-0.12.0.jar=8080:pinot.yml -Xms4G -Xmx4G -XX:MaxDirectMemorySize=30g -Dlog4j2.configurationFile=conf/pinot-admin-log4j2.xml -Dplugins.dir=$BASEDIR/plugins"
bin/pinot-admin.sh ....
```

This will expose a port at _**8080**_ to dump metrics as Prometheus format for Prometheus scrapper to fetch.
