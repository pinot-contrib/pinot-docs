# Controller

Most of the properties in Pinot are set in Zookeeper via Helix. However, you can also set properties in `controller.conf` file. You can specify the path to configuration file at the startup time as follows:

```
bin/pinot-admin.sh StartController -configFileName /path/to/controller.conf
```

`Controller.conf` can have the following properties.

## Primary configuration

| Property                                                     | Default                                                                  | Description                                                                                                                                                                                                                                                 |
| ------------------------------------------------------------ | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| controller.vip.host                                          | same as `controller.host`                                                | The VIP hostname used to set the download URL for segments                                                                                                                                                                                                  |
| controller.vip.port                                          | same as `controller.port`                                                |                                                                                                                                                                                                                                                             |
| controller.vip.protocol                                      |                                                                          |                                                                                                                                                                                                                                                             |
| controller.host                                              | localhost                                                                | The ip of the host on which controller is running                                                                                                                                                                                                           |
| controller.port                                              | 9000                                                                     | The port on which controller should run                                                                                                                                                                                                                     |
| controller.access.protocol                                   |                                                                          |                                                                                                                                                                                                                                                             |
| controller.data.dir                                          | ${java.io.tmpdir}/PinotController                                        | Directory to host segment data                                                                                                                                                                                                                              |
| controller.local.temp.dir                                    |                                                                          |                                                                                                                                                                                                                                                             |
| controller.zk.str                                            | localhost:2181                                                           | zookeeper host:port string to connect                                                                                                                                                                                                                       |
| controller.update\_segment\_state\_model                     | false                                                                    |                                                                                                                                                                                                                                                             |
| controller.helix.cluster.name                                |                                                                          | Pinot Cluster Name, required.                                                                                                                                                                                                                               |
| cluster.tenant.isolation.enable                              | true                                                                     | <p>Enable Tenant Isolation, default is single tenant cluster.<br>If enabled, each server or broker added into the cluster will be tagged with DefaultTenant.</p>                                                                                            |
| controller.enable.split.commit                               | false                                                                    | **(Deprecated)** Enable split commit protocol for real-time segment commit.                                                                                                                                                                                 |
| controller.query.console.useHttps                            | false                                                                    | use https instead of http for cluster                                                                                                                                                                                                                       |
| controller.upload.onlineToOfflineTimeout                     | 2 minutes                                                                |                                                                                                                                                                                                                                                             |
| controller.mode                                              | `dual`                                                                   | Should be one of `helix_only`, `pinot_only` or `dual`                                                                                                                                                                                                       |
| controller.resource.rebalance.strategy                       | `org.apache.helix.controller. rebalancer.strategy.AutoRebalanceStrategy` |                                                                                                                                                                                                                                                             |
| controller.resource.rebalance.delay\_ms                      | 5 minutes                                                                | <p>How long the helix waits to rebalance partitions after a controller is lost.</p><p>Longer time values allow for more time for a controller to recover.</p><p>Shorter time values prevent cluster operations like segment sealing from being blocked.</p> |
| controller.realtime.segment.commit.timeoutSeconds            | 120 seconds                                                              | request timeout for segment commit                                                                                                                                                                                                                          |
| controller.max.segment.completion.time.millis                | 300000 (5 minutes)                                                       | maximum allowed time for real-time segment completion (build + upload). Increase for tables with large segments where build and upload to deep store exceeds 5 minutes.                                                                                          |
| controller.deleted.segments.retentionInDays                  | 7 days                                                                   | duration for which to retain deleted segments                                                                                                                                                                                                               |
| controller.admin.access.control.factory.class                | `org.apache.pinot.controller. api.access.AllowAllAccessFactory`          |                                                                                                                                                                                                                                                             |
| controller.segment.upload.timeoutInMillis                    | 10 minutes                                                               | timeout for upload of segments.                                                                                                                                                                                                                             |
| controller.realtime.segment.metadata.commit.numLocks         | 64                                                                       |                                                                                                                                                                                                                                                             |
| controller.enable.storage.quota.check                        | true                                                                     |                                                                                                                                                                                                                                                             |
| controller.enable.batch.message.mode                         | false                                                                    |                                                                                                                                                                                                                                                             |
| controller.storage.factory.class.file                        | `org.apache.pinot.spi. filesystem.LocalPinotFS`                          |                                                                                                                                                                                                                                                             |
| table.minReplicas                                            | 1                                                                        |                                                                                                                                                                                                                                                             |
| controller.access.protocols                                  | http                                                                     | Ingress protocols to access controller (http or https or http,https)                                                                                                                                                                                        |
| controller.access.protocols.http.port                        |                                                                          | Port to access controller via http                                                                                                                                                                                                                          |
| controller.broker.protocols.https.port                       |                                                                          | Port to access controller via https                                                                                                                                                                                                                         |
| controller.broker.protocol                                   | http                                                                     | protocol for forwarding query requests (http or https)                                                                                                                                                                                                      |
| controller.broker.port.override                              |                                                                          | override for broker port when forwarding query requests (use in multi-ingress scenarios)                                                                                                                                                                    |
| controller.tls.keystore.path                                 |                                                                          | Path to controller TLS keystore                                                                                                                                                                                                                             |
| controller.tls.keystore.password                             |                                                                          | keystore password                                                                                                                                                                                                                                           |
| controller.tls.truststore.path                               |                                                                          | Path to controller TLS truststore                                                                                                                                                                                                                           |
| controller.tls.truststore.password                           |                                                                          | truststore password                                                                                                                                                                                                                                         |
| controller.tls.client.auth                                   | false                                                                    | toggle for requiring TLS client auth                                                                                                                                                                                                                        |
| pinot.controller.http.server.thread.pool.corePoolSize        | 2 \* cores                                                               | Config for the thread-pool used by pinot-controller's http-server.                                                                                                                                                                                          |
| pinot.controller.http.server.thread.pool.maxPoolSize         | 2 \* cores                                                               | Config for the thread-pool used by pinot-controller's http-server.                                                                                                                                                                                          |
| pinot.controller.segment.fetcher.http.client.maxConnTotal    |                                                                          | Config for the http-client used by HttpSegmentFetcher for downloading segments                                                                                                                                                                              |
| pinot.controller.segment.fetcher.http.client.maxConnPerRoute |                                                                          | Config for the http-client used by HttpSegmentFetcher for downloading segments                                                                                                                                                                              |

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

This task schedules and manages Pinot minion tasks. It periodically generates tasks for each table based on the task configurations defined in the table config. Common minion tasks include `MergeRollupTask`, `RealtimeToOfflineSegmentsTask`, `SegmentGenerationAndPushTask`, and `ConvertToRawIndexTask`.

<table><thead><tr><th width="530.7793259820547">Config</th><th>Default Value</th></tr></thead><tbody><tr><td>controller.task.frequencyPeriod</td><td>1h</td></tr><tr><td>controller.task.manager.initialDelayInSeconds</td><td>between 2m-5m</td></tr></tbody></table>

### RealtimeSegmentValidationManager

This task validates the ideal state and segment zk metadata of real-time tables by doing the following:

* fixing any partitions which have stopped consuming
* starting consumption from new partitions
* uploading segments to deep store if segment download url is missing

This task ensures that the consumption of the real-time tables gets fixed and keeps going when met with erroneous conditions.

{% hint style="danger" %}
This task does not fix consumption stalled due to

* CONSUMING segment being deleted
* Kafka OOR exceptions
{% endhint %}

<table><thead><tr><th width="530.7793259820547">Config</th><th>Default Value</th></tr></thead><tbody><tr><td>controller.realtime.segment.validation.frequencyPeriod</td><td>1h</td></tr><tr><td>controller.realtime.segment.validation.initialDelayInSeconds</td><td>between 2m-5m</td></tr><tr><td>controller.realtime.segment.deepStoreUploadRetryEnabled</td><td>false</td></tr><tr><td>controller.realtime.segment.deepStoreUploadRetry.timeoutMs</td><td>-1</td></tr><tr><td>controller.realtime.segment.deepStoreUploadRetry.parallelism</td><td>1</td></tr><tr><td>controller.realtime.segment.partialOfflineReplicaRepairEnabled</td><td>false</td></tr></tbody></table>

When `controller.realtime.segment.partialOfflineReplicaRepairEnabled` is enabled, the controller's periodic validation task automatically resets OFFLINE replicas back to CONSUMING for IN_PROGRESS segments that have a mix of CONSUMING and OFFLINE replicas. This handles cases where a replica's startup fails (for example, due to Kafka consumer initialization errors) while other replicas continue normally. Enable only after verifying that OFFLINE replicas are caused by transient failures rather than persistent errors.

### RetentionManager

This task manages retention of segments for all tables. During the run, it looks at the `retentionTimeUnit` and `retentionTimeValue` inside the `segmentsConfig` of every table, and deletes segments which are older than the retention. The deleted segments are moved to a DeletedSegments folder colocated with the dataDir on segment store, and permanently deleted from that folder in a configurable number of days.

<table>
    <thead>
        <tr><th width="501.62051915945614">Config</th><th>Default Value</th></tr>
    </thead>
    <tbody><tr><td>controller.retention.frequencyPeriod</td><td>6h</td></tr>
        <tr><td>controller.retentionManager.initialDelayInSeconds</td><td>between 2m-5m</td></tr>
        <tr><td>controller.deleted.segments.retentionInDays</td><td>7d</td></tr>
        <tr><td>controller.enable.hybrid.table.retention.strategy</td><td>false</td></tr>
    </tbody>
</table>

If `controller.enable.hybrid.table.retention.strategy` is set to true, the retention manager will use the hybrid 
retention strategy. In this strategy, the retention manager calculates a time boundary by looking at the maximum end
time of offline segments and the segment ingestion frequency specified for the OFFLINE table. Segments older than the 
time boundary are deleted from the REALTIME table. The time boundary calculation is as mentioned in the 
[Time Boundary](../basics/concepts/time-boundary.md) section. This type of strategy is useful to prevent data loss when
there are failures in moving the data from REALTIME table to OFFLINE table.

{% hint style="info" %}
When the offline part of the hybrid table is unused or not-required, it's recommended to delete the OFFLINE table. 
Otherwise, the REALTIME table will keep growing and the retention manager will not be able to delete the segments.
{% endhint %}

### SegmentRelocator

This task is applicable only if you have tierConfig or tagOverrideConfig. It runs rebalance in the background to

1. relocate COMPLETED segments to tag overrides
2. relocate ONLINE segments to tiers if tier configs are set

At most one replica is allowed to be unavailable during rebalance.

<table><thead><tr><th width="530.7775334537681">Config</th><th>Default Value</th></tr></thead><tbody><tr><td>controller.segment.relocator.frequencyPeriod</td><td>1h</td></tr><tr><td>controller.segmentRelocator.initialDelayInSeconds</td><td>between 2m-5m</td></tr></tbody></table>

### SegmentStatusChecker

This task manages segment status metrics such as realtimeTableCount, offlineTableCount, disableTableCount, numberOfReplicas, percentOfReplicas, percentOfSegments, idealStateZnodeSize, idealStateZnodeByteSize, segmentCount, segmentsInErrorState, tableCompressedSize.

<table><thead><tr><th width="530.7775334537681">Config</th><th>Default Value</th></tr></thead><tbody><tr><td>controller.statuschecker.frequencyPeriod</td><td>5m</td></tr><tr><td>controller.statusChecker.initialDelayInSeconds</td><td>between 2m-5m</td></tr></tbody></table>

### RebalanceChecker

Currently, table rebalance triggered by user runs at best effort. It could fail if the controller running it got restarted; or some servers were not stable, making the rebalance timed out while waiting for external view to converge with ideal state, etc. This task checks for failed rebalance and retry them automatically, up to certain times as configured.

<table><thead><tr><th width="530.7775334537681">Config</th><th>Default Value</th></tr></thead><tbody><tr><td>controller.rebalance.checker.frequencyPeriod</td><td>5m</td></tr><tr><td>controller.rebalanceChecker.initialDelayInSeconds</td><td>between 2m-5m</td></tr></tbody></table>

### TaskMetricsEmitter

This task periodically emits metrics about minion tasks, including task counts by state (RUNNING, WAITING, ERROR, COMPLETED) and task latencies. These metrics are useful for monitoring the health and throughput of the minion task system.

<table><thead><tr><th width="530.7775334537681">Config</th><th>Default Value</th></tr></thead><tbody><tr><td>controller.task.metrics.emitter.frequencyPeriod</td><td>5m</td></tr></tbody></table>

### ResourceUtilizationChecker

The periodic task ResourceUtilizationChecker runs periodically and computes the disk usage info of the Pinot server instances.

<table><thead><tr><th width="530.7775334537681">Config</th><th>Default Value</th><th>Description</th></tr></thead><tbody><tr><td>controller.resource.utilization.checker.frequency</td><td>300</td><td>Value is in seconds. Setting the value to -1 would disable the task.</td></tr><tr><td>controller.disk.utilization.path</td><td>/home/pinot/data</td><td>Disk utilization is calculated for this path.</td></tr></tbody></table>
