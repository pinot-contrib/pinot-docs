# Monitoring

### JMX to Prometheus

Pinot publishes metrics to JMX, those metrics could be exposed to Prometheus through tooling like [jmx\_reporter](https://github.com/prometheus/jmx_exporter).

To run as a javaagent, [download jmx\_prometheus\_javaagent jar](https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.12.0/jmx_prometheus_javaagent-0.12.0.jar) and [pinot.yml](https://raw.githubusercontent.com/fx19880617/jmx_exporter/master/example_configs/pinot.yml) run:

```text
ALL_JAVA_OPTS="-javaagent:jmx_prometheus_javaagent-0.12.0.jar=8080:pinot.yml -Xms4G -Xmx4G -XX:MaxDirectMemorySize=30g -Dlog4j2.configurationFile=conf/pinot-admin-log4j2.xml -Dplugins.dir=$BASEDIR/plugins"
bin/pinot-admin.sh ....
```

This will expose a port at _**8080**_ to dump metrics as Prometheus format for Prometheus scrapper to fetch.

