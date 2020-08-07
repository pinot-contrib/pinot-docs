# Controller

Most of the properties in Pinot are set in Zookeeper via Helix. However, you can also set properties in `controller.conf` file. You can specify the path to config file at the startup time as follows -

```text
bin/pinot-admin.sh StartController -configFileName /path/to/controller.conf
```

`Controller.conf` can have the following properties - 

### Primary Configuration

| Property | Default | Description |
| :--- | :--- | :--- |
| controller.vip.host | localhost |  |
| controller.vip.port | same as `controller.port` |  |
| controller.vip.protocol |  |  |
| controller.host | localhost | The ip of the host on which controller is running |
| controller.port |  | The port on which controller is running |
| controller.access.protocol |  |  |
| controller.data.dir |  |  |
| controller.local.temp.dir |  |  |
| controller.zk.str |  | zookeeper host:port string to connect |
| controller.update\_segment\_state\_model | false |  |
| controller.helix.cluster.name |  |  |
| controller.tenant.isolation.enable | true |  |
| controller.enable.split.commit | false |  |
| controller.query.console.useHttps | false | use https instead of http for cluster |
| controller.upload.onlineToOfflineTimeout | 2 minutes |  |
| controller.mode | `dual` | Should be one of `helix_only`, `pinot_only` or `dual`  |
| controller.resource.rebalance.strategy | `org.apache.helix.controller. rebalancer.strategy.AutoRebalanceStrategy` |  |
| controller.realtime.segment.commit.timeoutSeconds | 120 seconds | request timeout for segment commit |
| controller.deleted.segments.retentionInDays | 7 days | duration for which to retain deleted segments |
| controller.admin.access.control.factory.class | `org.apache.pinot.controller. api.access.AllowAllAccessFactory` |  |
| controller.segment.upload.timeoutInMillis | 10 minutes  | timeout for upload of segments. |
| controller.realtime.segment.metadata.commit.numLocks | 64 |  |
| controller.enable.storage.quota.check | true |  |
| controller.enable.batch.message.mode | false |  |
| controller.allow.hlc.tables | true |  |
| controller.storage.factory.class.file | `org.apache.pinot.spi. filesystem.LocalPinotFS` |  |
| table.minReplicas | 1 |  |



### Periodic Tasks Configuration

| Property | Default | Description |
| :--- | :--- | :--- |
| controller.retention.frequencyInSeconds | 6 hours | frequency at which to trigger retention checking tasks |
| controller.validation.frequencyInSeconds \(Deprecated\) | 1 hour |  |
| controller.offline.segment.interval.checker.frequencyInSeconds | 24 hours |  |
| controller.realtime.segment.validation.frequencyInSeconds | 1 hour |  |
| controller.broker.resource.validation.frequencyInSeconds | 1 hour |  |
| controller.broker.resource.validation.initialDelayInSeconds | 120-300 seconds |  |
| controller.statuschecker.frequencyInSeconds | 5 minutes |  |
| controller.statuschecker.waitForPushTimeInSeconds | 10 minutes |  |
| controller.task.frequencyInSeconds | -1 \(disabled\) |  |
| controller.realtime.segment.relocator.frequency | 1 hour |  |
| controller.segment.level.validation.intervalInSeconds | 24 hours |  |
| controller.statuschecker.intialDelayInSeconds | 120-300 seconds |  |
| controller.retentionManager.initialDelayInSeconds | 120-300 seconds |  |
| controller.offlineSegmentIntervalChecker.initialDelayInSeconds | 120-300 seconds |  |
| controller.realtimeSegmentRelocation.initialDelayInSeconds | 120-300 seconds |  |

