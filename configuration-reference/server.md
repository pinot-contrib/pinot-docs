# Server

Server configuration can be provided as part of the server startup parameters.

```text
bin/pinot-admin.sh StartServer -configFileName /path/to/server.conf
```

`server.conf` can have the following properties

| Property | Default | Description |
| :--- | :--- | :--- |
| pinot.server.netty.port | 8098 |  |
| pinot.server.adminapi.port | 8097 |  |
| pinot.server.instance.dataDir | `java.io.tmpdir` + `/PinotServer/index` |  |
| pinot.server.instance.consumerDir |  |  |
| pinot.server.instance.segmentTarDir | `java.io.tmpdir` + `/PinotServer/segmentTar` |  |
| pinot.server.instance.readMode | `mmap` |  |
| pinot.server.instance.reload.consumingSegment | false |  |
| pinot.server.instance.data.manager.class | `org.apache.pinot.server.` `starter.helix.HelixInstanceDataManager` |  |
| pinot.server.query.executor.pruner.class | `ValidSegmentPruner,DataSchemaSegmentPruner, ColumnValueSegmentPruner,SelectionQuerySegmentPruner` |  |
| pinot.server.query.executor.timeout | 15 seconds |  |
| pinot.server.query.executor.class | `org.apache.pinot.core.query.` `executor.ServerQueryExecutorV1Impl` |  |
| pinot.server.requestHandlerFactory.class | `org.apache.pinot.server.` `request.SimpleRequestHandlerFactory` |  |
| pinot.server.instance.segment.format.version |  |  |
| pinot.server.instance.enable.split.commit |  |  |
| pinot.server.instance.enable.commitend.metadata |  |  |
| pinot.server.instance.realtime.alloc.offheap |  |  |
| pinot.server.instance.realtime.alloc.offheap.direct |  |  |
| pinot.server.startup.minResourcePercent | 100 |  |
| pinot.server.starter.realtimeConsumptionCatchupWaitMs | 0 |  |
| pinot.server.startup.timeoutMs | 10 minutes |  |
| pinot.server.startup.enableServiceStatusCheck | true |  |
| pinot.server.startup.serviceStatusCheckIntervalMs | 10 seconds |  |
| pinot.server.shutdown.timeoutMs | 10 minutes |  |
| pinot.server.shutdown.enableQueryCheck | true |  |
| pinot.server.shutdown.noQueryThresholdMs | 15 seconds |  |
| pinot.server.shutdown.enableResourceCheck | false |  |
| pinot.server.shutdown.resourceCheckIntervalMs | 10 seconds |  |
| pinot.server.admin.access.control.factory.class | `org.apache.pinot.server.` `api.access.AllowAllAccessFactory` |  |
|  |  |  |







