# Broker

You can set broker properties in a configuration file. The file can be provided during startup time as follows - 

```text
bin/pinot-admin.sh StartBroker -configFileName /path/to/broker.conf
```

`broker.conf` can have the following properties. All properties are defined in this class.

| Property | Default | Description |
| :--- | :--- | :--- |
| pinot.broker.delayShutdownTimeMs | 10 seconds |  |
| pinot.broker.enableTableLevelMetrics | true |  |
| pinot.broker.query.response.limit | Integer.MAX\_VALUE |  |
| pinot.broker.query.log.length | Integer.MAX\_VALUE |  |
| pinot.broker.query.log.maxRatePerSecond | 10000.0 |  |
| pinot.broker.timeoutMs | 10 seconds |  |
| pinot.broker.startup.minResourcePercent | 100 |  |
| pinot.broker.enable.query.limit.override | true |  |
|  |  |  |





