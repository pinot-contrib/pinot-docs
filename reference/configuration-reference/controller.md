# Controller

Most of the properties in Pinot are set in Zookeeper via Helix. However, you can also set properties in `controller.conf` file. You can specify the path to configuration file at the startup time as follows:

```
bin/pinot-admin.sh StartController -configFileName /path/to/controller.conf
```

`Controller.conf` can have the following properties.

{% hint style="warning" %}
**Duplicate Keys in Configuration File**

Starting from Apache Pinot 1.3.0, duplicate keys in the configuration file will cause a `ConfigurationException` to be thrown during startup. Previously, duplicate keys would be silently merged into a list. If you encounter this error, ensure that each configuration property appears only once in your configuration file. The exception will include the exact file path, duplicate key name, and the line numbers where the duplicates were found.

Example error:
```
ConfigurationException: Duplicate key found in /path/to/controller.conf at line 10 and line 15: controller.port
```
{% endhint %}


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
| cluster.tenant.isolation.enable | true | Enable Tenant Isolation, default is single tenant cluster. If enabled, each server or broker added into the cluster will be tagged with DefaultTenant. |
| controller.enable.split.commit                               | false                                                                    | **(Deprecated)** Enable split commit protocol for real-time segment commit.                                                                                                                                                                                 |
| controller.query.console.useHttps                            | false                                                                    | use https instead of http for cluster                                                                                                                                                                                                                       |
| controller.upload.onlineToOfflineTimeout                     | 2 minutes                                                                |                                                                                                                                                                                                                                                             |
| controller.mode                                              | `dual`                                                                   | Should be one of `helix_only`, `pinot_only` or `dual`                                                                                                                                                                                                       |
| controller.resource.rebalance.strategy                       | `org.apache.helix.controller. rebalancer.strategy.AutoRebalanceStrategy` |                                                                                                                                                                                                                                                             |
| controller.resource.rebalance.delay\_ms | 5 minutes | How long the helix waits to rebalance partitions after a controller is lost. Longer time values allow for more time for a controller to recover. Shorter time values prevent cluster operations like segment sealing from being blocked. |
| controller.realtime.segment.commit.timeoutSeconds            | 120 seconds                                                              | request timeout for segment commit                                                                                                                                                                                                                          |
| controller.executor.numThreads                               | not set (`-1`)                                                           | Size of the controller async executor used for background controller work such as multiget helpers. If unset or set to `0`/negative, Pinot uses a cached thread pool. If set to a positive value, Pinot uses a fixed-size thread pool.                                                                                                                                    |
| controller.executor.rebalance.numThreads                     | not set (`-1`)                                                           | Size of the dedicated controller executor used for table and tenant rebalance work. If unset or set to `0`/negative, Pinot uses a cached thread pool. If set to a positive value, Pinot uses a fixed-size thread pool.                                                                                                                                                     |
| controller.deleted.segments.retentionInDays                  | 7 days                                                                   | duration for which to retain deleted segments                                                                                                                                                                                                               |
| controller.admin.access.control.factory.class                | `org.apache.pinot.controller. api.access.AllowAllAccessFactory`          |                                                                                                                                                                                                                                                             |
| controller.segment.upload.timeoutInMillis                    | 10 minutes                                                               | timeout for upload of segments.                                                                                                                                                                                                                             |
| controller.startup.continueWithoutDeepStore                  | false                                                                    | When `true`, the controller continues startup even if Pinot fails to validate or create `controller.data.dir` through PinotFS during boot. When `false`, the controller fails fast on that startup check.                                                                                                                                                                        |
| controller.startup.exitOnTableConfigCheckFailure             | true                                                                     | When `true`, the controller exits during startup if any table is missing its `TableConfig`. When `false`, the controller stays up and reports the missing-table-config count via `tableWithoutTableConfigCount`.                                                                                                                                                               |
| controller.startup.exitOnSchemaCheckFailure                  | true                                                                     | When `true`, the controller exits during startup if any table is missing its `Schema`. When `false`, the controller stays up and reports the missing-schema count via `tableWithoutSchemaCount`.                                                                                                                                                                               |
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

If you temporarily disable either startup check to keep the controller running while you repair legacy tables, watch the controller gauges `tableWithoutTableConfigCount` and `tableWithoutSchemaCount` to confirm the invalid-table count returns to zero.

## Periodic task configuration

The following period tasks are

### BrokerResourceValidationManager

This task rebuilds the BrokerResource if the instance set has changed.

| Config | Default Value |
| --- | --- |
| controller.broker.resource.validation.frequencyPeriod | 1h |
| controller.broker.resource.validation.initialDelayInSeconds | between 2m-5m |

### ResponseStoreCleaner

This task removes expired cursor response-store entries from brokers. Cursor expiration itself is controlled by the broker setting `pinot.broker.cursor.response.store.expiration`.

| Config | Default Value |
| --- | --- |
| controller.cluster.response.store.cleaner.frequencyPeriod | 1h |
| controller.cluster.response.store.cleaner.initialDelay | between 2m-5m |

### StaleInstancesCleanupTask

This task periodically cleans up stale Pinot broker/server/minion instances.

| Config | Default Value |
| --- | --- |
| controller.stale.instances.cleanup.task.frequencyPeriod | 1h |
| controller.stale.instances.cleanup.task.initialDelaySeconds | between 2m-5m |
| controller.stale.instances.cleanup.task.minOfflineTimeBeforeDeletionPeriod | 1h |

### OfflineSegmentIntervalChecker

This task manages the segment ValidationMetrics (missingSegmentCount, offlineSegmentDelayHours, lastPushTimeDelayHours, TotalDocumentCount, NonConsumingPartitionCount, SegmentCount), to ensure that all offline segments are contiguous (no missing segments) and that the offline push delay isn't too high.

| Config | Default Value |
| --- | --- |
| controller.offline.segment.interval.checker.frequencyPeriod | 24h |
| controller.statuschecker.waitForPushTimePeriod | 10m |
| controller.offlineSegmentIntervalChecker.initialDelayInSeconds | between 2m-5m |

### PinotTaskManager

This task schedules and manages Pinot minion tasks. It periodically generates tasks for each table based on the task configurations defined in the table config. Common minion tasks include `MergeRollupTask`, `RealtimeToOfflineSegmentsTask`, `SegmentGenerationAndPushTask`, and `ConvertToRawIndexTask`.

| Config | Default Value |
| --- | --- |
| controller.task.frequencyPeriod | 1h |
| controller.task.manager.initialDelayInSeconds | between 2m-5m |

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

| Config | Default Value |
| --- | --- |
| controller.realtime.segment.validation.frequencyPeriod | 1h |
| controller.realtime.segment.validation.initialDelayInSeconds | between 2m-5m |
| controller.realtime.segment.deepStoreUploadRetryEnabled | false |
| controller.realtime.segment.deepStoreUploadRetry.timeoutMs | -1 |
| controller.realtime.segment.deepStoreUploadRetry.parallelism | 1 |
| controller.segment.error.autoReset | false |
| controller.realtime.segment.partialOfflineReplicaRepairEnabled | false |
| controller.segment.disaster.recovery.mode | DEFAULT |

`controller.segment.error.autoReset` controls whether the controller's periodic offline and realtime segment validation tasks automatically reset segments in `ERROR` state so they can retry normal recovery. Pinot leaves this disabled by default.

When `controller.realtime.segment.partialOfflineReplicaRepairEnabled` is enabled, the controller's periodic validation task automatically resets OFFLINE replicas back to CONSUMING for IN_PROGRESS segments that have a mix of CONSUMING and OFFLINE replicas. This handles cases where a replica's startup fails (for example, due to Kafka consumer initialization errors) while other replicas continue normally. Enable only after verifying that OFFLINE replicas are caused by transient failures rather than persistent errors.

`controller.segment.disaster.recovery.mode` sets the cluster-wide default disaster-recovery policy used by the controller's realtime segment validation task for pauseless ingestion. Supported values are `DEFAULT` and `ALWAYS`, matching the table-level `disasterRecoveryMode` setting in `streamIngestionConfig`. You can set this in `controller.conf`, or update the same key through cluster configs so the controller picks up the new mode without restart.

### RetentionManager

This task manages retention of segments for all tables. During the run, it looks at the `retentionTimeUnit` and `retentionTimeValue` inside the `segmentsConfig` of every table, and deletes segments which are older than the retention. The deleted segments are moved to a DeletedSegments folder colocated with the dataDir on segment store, and permanently deleted from that folder in a configurable number of days.

| Config | Default Value |
| --- | --- |
| controller.retention.frequencyPeriod | 6h |
| controller.retentionManager.initialDelayInSeconds | between 2m-5m |
| controller.deleted.segments.retentionInDays | 7d |
| controller.enable.hybrid.table.retention.strategy | false |

If `controller.enable.hybrid.table.retention.strategy` is set to true, the retention manager will use the hybrid 
retention strategy. In this strategy, the retention manager calculates a time boundary by looking at the maximum end
time of offline segments and the segment ingestion frequency specified for the OFFLINE table. Segments older than the 
time boundary are deleted from the REALTIME table. The time boundary calculation is as mentioned in the 
[Time Boundary](../../basics/concepts/time-boundary.md) section. This type of strategy is useful to prevent data loss when
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

| Config | Default Value |
| --- | --- |
| controller.segment.relocator.frequencyPeriod | 1h |
| controller.segmentRelocator.initialDelayInSeconds | between 2m-5m |

### SegmentStatusChecker

This task manages segment status metrics such as realtimeTableCount, offlineTableCount, disableTableCount, numberOfReplicas, percentOfReplicas, percentOfSegments, idealStateZnodeSize, idealStateZnodeByteSize, segmentCount, segmentsInErrorState, tableCompressedSize.

| Config | Default Value |
| --- | --- |
| controller.statuschecker.frequencyPeriod | 5m |
| controller.statusChecker.initialDelayInSeconds | between 2m-5m |

### RebalanceChecker

Currently, table rebalance triggered by user runs at best effort. It could fail if the controller running it got restarted; or some servers were not stable, making the rebalance timed out while waiting for external view to converge with ideal state, etc. This task checks for failed rebalance and retry them automatically, up to certain times as configured.

| Config | Default Value |
| --- | --- |
| controller.rebalance.checker.frequencyPeriod | 5m |
| controller.rebalanceChecker.initialDelayInSeconds | between 2m-5m |

### TaskMetricsEmitter

This task periodically emits metrics about minion tasks, including task counts by state (RUNNING, WAITING, ERROR, COMPLETED) and task latencies. These metrics are useful for monitoring the health and throughput of the minion task system.

| Config | Default Value |
| --- | --- |
| controller.task.metrics.emitter.frequencyPeriod | 5m |

### ResourceUtilizationChecker

The periodic task `ResourceUtilizationChecker` runs periodically and fetches disk-usage information from Pinot server instances via `GET /instance/diskUtilization`.

| Config | Default Value | Description |
| --- | --- | --- |
| controller.enable.resource.utilization.check | false | Master switch for enforcing resource-utilization checks during real-time ingestion validation and minion task generation. |
| controller.enable.all.resource.utilization.checkers | true | Registers all resource-utilization checkers for backward compatibility. |
| controller.enable.disk.utilization.checker | false | Registers the disk-utilization checker when `controller.enable.all.resource.utilization.checkers` is `false`. |
| controller.resource.utilization.checker.frequency | 300 | Value is in seconds. Setting the value to `-1` disables the periodic checker task. |
| controller.resource.utilization.checker.initial.delay | 300 (or 0 when collect.usage.at.startup is true) | Initial delay for the resource-utilization checker in seconds. Automatically set to 0 when `controller.resource.utilization.checker.collect.usage.at.startup` is enabled. |
| controller.resource.utilization.checker.collect.usage.at.startup | false | When set to `true`, the controller waits for the resource utilization checker (disk usage cache) to be populated before marking itself as healthy. This prevents segment push requests from being accepted when disk usage is already high (e.g., 90%) immediately after a restart. When enabled, `controller.resource.utilization.checker.initial.delay` is automatically set to 0 so the checker runs immediately. If the checker times out, the controller still becomes healthy (fail-open). |
| controller.disk.utilization.threshold | 0.95 | Disk-usage threshold expressed as a fraction between 0 and 1. |
| controller.disk.utilization.check.timeoutMs | 30000 | Timeout in milliseconds for collecting disk-usage responses from servers. |
| controller.disk.utilization.path | /home/pinot/data | Compatibility config sent by the controller when requesting disk usage. The current server endpoint ignores this value and always measures the server `instanceDataDir`. |
