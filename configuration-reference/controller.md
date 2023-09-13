# Controller

Most of the properties in Pinot are set in Zookeeper via Helix. However, you can also set properties in `controller.conf` file. You can specify the path to configuration file at the startup time as follows:

```
bin/pinot-admin.sh StartController -configFileName /path/to/controller.conf
```

`Controller.conf` can have the following properties.

## Primary configuration

| Property                                                     | Default                                                                  | Description                                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| controller.vip.host                                          | same as `controller.host`                                                | The VIP hostname used to set the download URL for segments                               |
| controller.vip.port                                          | same as `controller.port`                                                |                                                                                          |
| controller.vip.protocol                                      |                                                                          |                                                                                          |
| controller.host                                              | localhost                                                                | The ip of the host on which controller is running                                        |
| controller.port                                              | 9000                                                                     | The port on which controller should run                                                  |
| controller.access.protocol                                   |                                                                          |                                                                                          |
| controller.data.dir                                          | ${java.io.tmpdir}/PinotController                                        | Directory to host segment data                                                           |
| controller.local.temp.dir                                    |                                                                          |                                                                                          |
| controller.zk.str                                            | localhost:2181                                                           | zookeeper host:port string to connect                                                    |
| controller.update\_segment\_state\_model                     | false                                                                    |                                                                                          |
| controller.helix.cluster.name                                |                                                                          | Pinot Cluster Name, required.                                                            |
| controller.tenant.isolation.enable                           | true                                                                     | Enable Tenant Isolation, default is single tenant cluste                                 |
| controller.enable.split.commit                               | false                                                                    |                                                                                          |
| controller.query.console.useHttps                            | false                                                                    | use https instead of http for cluster                                                    |
| controller.upload.onlineToOfflineTimeout                     | 2 minutes                                                                |                                                                                          |
| controller.mode                                              | `dual`                                                                   | Should be one of `helix_only`, `pinot_only` or `dual`                                    |
| controller.resource.rebalance.strategy                       | `org.apache.helix.controller. rebalancer.strategy.AutoRebalanceStrategy` |                                                                                          |
| controller.realtime.segment.commit.timeoutSeconds            | 120 seconds                                                              | request timeout for segment commit                                                       |
| controller.deleted.segments.retentionInDays                  | 7 days                                                                   | duration for which to retain deleted segments                                            |
| controller.admin.access.control.factory.class                | `org.apache.pinot.controller. api.access.AllowAllAccessFactory`          |                                                                                          |
| controller.segment.upload.timeoutInMillis                    | 10 minutes                                                               | timeout for upload of segments.                                                          |
| controller.realtime.segment.metadata.commit.numLocks         | 64                                                                       |                                                                                          |
| controller.enable.storage.quota.check                        | true                                                                     |                                                                                          |
| controller.enable.batch.message.mode                         | false                                                                    |                                                                                          |
| controller.allow.hlc.tables                                  | true                                                                     |                                                                                          |
| controller.storage.factory.class.file                        | `org.apache.pinot.spi. filesystem.LocalPinotFS`                          |                                                                                          |
| table.minReplicas                                            | 1                                                                        |                                                                                          |
| controller.access.protocols                                  | http                                                                     | Ingress protocols to access controller (http or https or http,https)                     |
| controller.access.protocols.http.port                        |                                                                          | Port to access controller via http                                                       |
| controller.broker.protocols.https.port                       |                                                                          | Port to access controller via https                                                      |
| controller.broker.protocol                                   | http                                                                     | protocol for forwarding query requests (http or https)                                   |
| controller.broker.port.override                              |                                                                          | override for broker port when forwarding query requests (use in multi-ingress scenarios) |
| controller.tls.keystore.path                                 |                                                                          | Path to controller TLS keystore                                                          |
| controller.tls.keystore.password                             |                                                                          | keystore password                                                                        |
| controller.tls.truststore.path                               |                                                                          | Path to controller TLS truststore                                                        |
| controller.tls.truststore.password                           |                                                                          | truststore password                                                                      |
| controller.tls.client.auth                                   | false                                                                    | toggle for requiring TLS client auth                                                     |
| pinot.controller.http.server.thread.pool.corePoolSize        | 2 \* cores                                                               | Config for the thread-pool used by pinot-controller's http-server.                       |
| pinot.controller.http.server.thread.pool.maxPoolSize         | 2 \* cores                                                               | Config for the thread-pool used by pinot-controller's http-server.                       |
| pinot.controller.segment.fetcher.http.client.maxTotalConn    |                                                                          | Config for the http-client used by HttpSegmentFetcher for downloading segments           |
| pinot.controller.segment.fetcher.http.client.maxConnPerRoute |                                                                          | Config for the http-client used by HttpSegmentFetcher for downloading segments           |

## Periodic task configuration

The following period tasks are

### BrokerResourceValidationManager

This task rebuilds the BrokerResource if the instance set has changed.

<table><thead><tr><th width="539.7793259820547">Config</th><th>Default Value</th></tr></thead><tbody><tr><td>controller.broker.resource.validation.frequencyPeriod</td><td>1h</td></tr><tr><td>controller.broker.resource.validation.initialDelayInSeconds</td><td>between 2m-5m</td></tr></tbody></table>

### StaleInstancesCleanupTask

This task periodically cleans up stale Pinot broker/server/minion instances.

<table><thead><tr><th width="539.7793259820547">Config</th><th>Default Value</th></tr></thead><tbody><tr><td>controller.stale.instances.cleanup.task.frequencyPeriod</td><td>1h</td></tr><tr><td>controller.stale.instances.cleanup.task.initialDelaySeconds</td><td>between 2m-5m</td></tr><tr><td>controller.stale.instances.cleanup.task.minOfflineTimeBeforeDeletionPeriod</td><td>1h</td></tr></tbody></table>

### OfflineSegmentIntervalChecker

This task manages the segment ValidationMetrics (missingSegmentCount, offlineSegmentDelayHours, lastPushTimeDelayHours, TotalDocumentCount, NonConsumingPartitionCount, SegmentCount), to ensure that all offline segments are contiguous (no missing segments) and that the offline push delay isn't too high.

<table><thead><tr><th width="530.7793259820547">Config</th><th>Default Value</th></tr></thead><tbody><tr><td>controller.offline.segment.interval.checker.frequencyPeriod</td><td>24h</td></tr><tr><td>controller.statuschecker.waitForPushTimePeriod</td><td>10m</td></tr><tr><td>controller.offlineSegmentIntervalChecker.initialDelayInSeconds</td><td>between 2m-5m</td></tr></tbody></table>

### PinotTaskManager

TBD

### RealtimeSegmentValidationManager

This task validates the ideal state and segment zk metadata of real-time tables by doing the following:&#x20;

* fixing any partitions which have stopped consuming
* starting consumption from new partitions
* uploading segments to deep store if segment download url is missing

This task ensures that the consumption of the real-time tables gets fixed and keeps going when met with erroneous conditions.

{% hint style="danger" %}
This task does not fix consumption stalled due to

* CONSUMING segment being deleted
* Kafka OOR exceptions
{% endhint %}

<table><thead><tr><th width="530.7793259820547">Config</th><th>Default Value</th></tr></thead><tbody><tr><td>controller.realtime.segment.validation.frequencyPeriod</td><td>1h</td></tr><tr><td>controller.realtime.segment.validation.initialDelayInSeconds</td><td>between 2m-5m</td></tr></tbody></table>

### RetentionManager

This task manages retention of segments for all tables. During the run, it looks at the `retentionTimeUnit` and `retentionTimeValue` inside the `segmentsConfig` of every table, and deletes segments which are older than the retention. The deleted segments are moved to a DeletedSegments folder colocated with the dataDir on segment store, and permanently deleted from that folder in a configurable number of days.

<table><thead><tr><th width="501.62051915945614">Config</th><th>Default Value</th></tr></thead><tbody><tr><td>controller.retention.frequencyPeriod</td><td>6h</td></tr><tr><td>controller.retentionManager.initialDelayInSeconds</td><td>between 2m-5m</td></tr><tr><td>controller.deleted.segments.retentionInDays</td><td>7d</td></tr></tbody></table>

### SegmentRelocator

This task is applicable only if you have tierConfig or tagOverrideConfig. It runs rebalance in the background to

1. relocate COMPLETED segments to tag overrides
2. relocate ONLINE segments to tiers if tier configs are set&#x20;

At most one replica is allowed to be unavailable during rebalance.

<table><thead><tr><th width="530.7775334537681">Config</th><th>Default Value</th></tr></thead><tbody><tr><td>controller.segment.relocator.frequencyPeriod</td><td>1h</td></tr><tr><td>controller.segmentRelocator.initialDelayInSeconds</td><td>between 2m-5m</td></tr></tbody></table>

### SegmentStatusChecker

This task manages segment status metrics such as realtimeTableCount, offlineTableCount, disableTableCount, numberOfReplicas, percentOfReplicas, percentOfSegments, idealStateZnodeSize, idealStateZnodeByteSize, segmentCount, segmentsInErrorState, tableCompressedSize.

<table><thead><tr><th width="530.7775334537681">Config</th><th>Default Value</th></tr></thead><tbody><tr><td>controller.statuschecker.frequencyPeriod</td><td>5m</td></tr><tr><td>controller.statusChecker.initialDelayInSeconds</td><td>between 2m-5m</td></tr></tbody></table>

### TaskMetricsEmitter

TBD
