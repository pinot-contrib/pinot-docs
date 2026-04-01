# Server

Server configuration can be provided as part of the server startup parameters.

```
bin/pinot-admin.sh StartServer -configFileName /path/to/server.conf
```

`server.conf` can have the following properties

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Default</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>pinot.server.netty.port</td>
      <td>8098</td>
      <td>Port to query Pinot Server</td>
    </tr>
    <tr>
      <td>pinot.server.netty.host</td>
      <td></td>
      <td>Pinot server hostname</td>
    </tr>
    <tr>
      <td>pinot.server.adminapi.port</td>
      <td>8097</td>
      <td>Port for Pinot Server Admin UI</td>
    </tr>
    <tr>
      <td>pinot.server.instance.id</td>
      <td></td>
      <td>By default the server instance id used by Helix is _Server\_hostname\_port_ where the hostname and port are configured through host and port config values above. This config overwrites the default setting. User can put server id independent of the server's hostname and port.</td>
    </tr>
    <tr>
      <td>pinot.server.instance.dataDir</td>
      <td>`java.io.tmpdir` + `/PinotServer/index`</td>
      <td>Directory to hold all the data</td>
    </tr>
    <tr>
      <td>pinot.server.instance.consumerDir</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.server.instance.segmentTarDir</td>
      <td>`java.io.tmpdir` + `/PinotServer/segmentTar`</td>
      <td>Directory to hold temporary segments downloaded from Controller or Deep Store</td>
    </tr>
    <tr>
      <td>pinot.tar.compression.codec.name</td>
      <td>`gzip`</td>
      <td>Compression codec used for segment tar archives during upload and download. Supported values: `gzip` (default), `lz4_framed` (fast, lower compression ratio), `zstandard` (good balance of speed and ratio). Introduced in 1.3.0. File extensions: `.tar.gz`, `.tar.lz4`, `.tar.zst` respectively.</td>
    </tr>
    <tr>
      <td>pinot.server.instance.readMode</td>
      <td>`mmap`</td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.server.instance.reload.consumingSegment</td>
      <td>true</td>
      <td>Specifies if the reload segment API should reload the consuming segments. This is useful when the corresponding schema is updated and we want the changes to be reflected in the consuming segment.</td>
    </tr>
    <tr>
      <td>pinot.server.instance.data.manager.class</td>
      <td><p><code>org.apache.pinot.server.</code><br><code>starter.helix.HelixInstanceDataManager</code></p></td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.query.scheduler.name</td>
      <td>`fcfs`</td>
      <td>Currently only FCFS (first-come-first-serve) is supported</td>
    </tr>
    <tr>
      <td>pinot.query.scheduler.query\_runner\_threads</td>
      <td>CPU cores</td>
      <td>Main thread to execute the queries (one thread per query)</td>
    </tr>
    <tr>
      <td>pinot.query.scheduler.query\_worker\_threads</td>
      <td>2 \* CPU cores</td>
      <td>Worker thread to process the segments (multiple threads per query)</td>
    </tr>
    <tr>
      <td>pinot.query.scheduler.query.log.maxRatePerSecond</td>
      <td>unlimited</td>
      <td>**(Deprecated: use `pinot.server.query.log.maxRatePerSecond` instead.)** Maximum queries to be logged per second. Queries with exceptions and costly queries are always logged.</td>
    </tr>
    <tr>
      <td>pinot.server.query.executor.class</td>
      <td><p><code>org.apache.pinot.core.query.</code><br><code>executor.ServerQueryExecutorV1Impl</code></p></td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.server.query.executor.pruner.class</td>
      <td><p><code>ValidSegmentPruner,DataSchemaSegmentPruner,</code><br><code>ColumnValueSegmentPruner,SelectionQuerySegmentPruner</code></p></td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.server.query.executor.timeout</td>
      <td>`15000`</td>
      <td>Timeout for Server to process Query in Milliseconds</td>
    </tr>
    <tr>
      <td>pinot.server.query.executor.max.execution.threads</td>
      <td>`-1` (unlimited)</td>
      <td>Maximum number of execution threads allowed for a query. Limiting this can prevent a single expensive query from occupying all the execution threads.</td>
    </tr>
    <tr>
      <td>pinot.server.query.executor.max.init.group.holder.capacity</td>
      <td>`10000`</td>
      <td>Initial capacity of the group key holder. Increasing this value can reduce the resizing of the group key holder, but increase the heap usage for small group-by queries.</td>
    </tr>
    <tr>
      <td>pinot.server.query.executor.num.groups.limit</td>
      <td>`100000`</td>
      <td>Maximum number of groups kept from each segment during query execution. Once this limit is reached, no more groups will be taken (will still aggregate on existing groups).</td>
    </tr>
    <tr>
      <td>pinot.server.query.executor.min.segment.group.trim.size</td>
      <td>`-1` (do not trim)</td>
      <td>Minimum number of groups kept at segment level during query execution. If there are enough groups found in a segment, pinot will trim the groups to `max(5 * LIMIT, minSegmentgroupTrimSize)` groups based on the order-by clause. Increasing this value can increase the accuracy of the results, but also increase the heap usage of the group-by queries.</td>
    </tr>
    <tr>
      <td>pinot.server.query.executor.min.server.group.trim.size</td>
      <td>`5000`</td>
      <td>Minimum number of groups kept at server level during query execution. If there are enough groups found in a server, pinot will trim the groups to `max(5 * LIMIT, minServergroupTrimSize)` groups based on the order-by clause. Increasing this value can increase the accuracy of the results, but also increase the heap usage and data transfer cost of the group-by queries.</td>
    </tr>
    <tr>
      <td>pinot.server.query.executor.groupby.trim.threshold</td>
      <td>`1000000`</td>
      <td>Threshold for number of groups to trigger the server group trimming. Increasing this value can reduce the times of trimming, but also increase the heap usage of the group-by queries.</td>
    </tr>
    <tr>
      <td>pinot.server.requestHandlerFactory.class</td>
      <td><p><code>org.apache.pinot.server.</code><br><code>request.SimpleRequestHandlerFactory</code></p></td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.server.instance.segment.format.version</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.server.instance.enable.split.commit</td>
      <td></td>
      <td>**(Deprecated)** Enable split commit protocol for real-time segment commit.</td>
    </tr>
    <tr>
      <td>pinot.server.instance.enable.commitend.metadata</td>
      <td></td>
      <td>**(Deprecated)** Enable metadata commit at the end of segment commit.</td>
    </tr>
    <tr>
      <td>pinot.server.instance.max.parallel.refresh.threads</td>
      <td>1</td>
      <td>Number of simultaneous segments that can be refreshed on one server.</td>
    </tr>
    <tr>
      <td>pinot.server.instance.realtime.max.parallel.segment.builds</td>
      <td>0</td>
      <td>Specifies how many parallel real-time segments can be built. Value of <= 0 indicates unlimited.</td>
    </tr>
    <tr>
      <td>pinot.server.instance.realtime.alloc.offheap</td>
      <td>true</td>
      <td>Boolean value to control whether memory for real-time consuming segments should be allocated off-heap.</td>
    </tr>
    <tr>
      <td>pinot.server.instance.realtime.alloc.offheap.direct</td>
      <td>false</td>
      <td>If 'real-time.alloc.offheap' is set to true, this boolean value controls whether the corresponding allocation should be direct or not (false indicate mmap allocation)</td>
    </tr>
    <tr>
      <td>pinot.server.startup.minResourcePercent</td>
      <td>100</td>
      <td>The percentage of tables that need to be in an `ONLINE` state before the server is marked as `STARTED` to server queries</td>
    </tr>
    <tr>
      <td>pinot.server.startup.timeoutMs</td>
      <td>10 minutes</td>
      <td>The total amount of time a server will wait for all status checks before server is marked as `STARTED` to server queries</td>
    </tr>
    <tr>
      <td>pinot.server.starter.realtimeConsumptionCatchupWaitMs</td>
      <td>0</td>
      <td><p>On it's own, this is a static amount of time servers will wait for consuming segments before server is marked as <code>STARTED</code> to server queries<br><br>When paired with <code>pinot.server.starter.enableRealtimeOffsetBasedConsumptionStatusChecker</code> or <code>pinot.server.starter.enableRealtimeFreshnessBasedConsumptionStatusChecker</code>, this is how long those status checkers will wait for segments to turn <code>GOOD</code><br><br>This should not be set to more than <code>pinot.server.startup.timeoutMs</code> as it will not be respected</p></td>
    </tr>
    <tr>
      <td>pinot.server.starter.enableRealtimeOffsetBasedConsumptionStatusChecker</td>
      <td>false</td>
      <td>When `true`, the server will collect the current, latest offsets for all consuming segments and will mark those segments as `GOOD` once they have caught up to those offsets</td>
    </tr>
    <tr>
      <td>pinot.server.starter.enableRealtimeFreshnessBasedConsumptionStatusChecker</td>
      <td>false</td>
      <td><p>When <code>true</code>, the server will not be marked as <code>STARTED</code> or serve queries until</p><p><br>1) the server has caught up to the latest available offset or the latest consumed event for each segment is at least within <code>pinot.server.starter.realtimeMinFreshnessMs</code> of the current time<br>2) <code>pinot.server.startup.timeoutMs</code> has elapsed</p></td>
    </tr>
    <tr>
      <td>pinot.server.starter.realtimeMinFreshnessMs</td>
      <td>10 seconds</td>
      <td><p>When <code>pinot.server.starter.enableRealtimeFreshnessBasedConsumptionStatusChecker=true</code>, this configures the minimum freshness (now - last_event_time) for the server status checker to consider a consuming segment <code>GOOD</code></p><p>This only applies when <code>pinot.server.starter.enableRealtimeFreshnessBasedConsumptionStatusChecker=true</code></p></td>
    </tr>
    <tr>
      <td>pinot.server.starter.realtimeFreshnessIdleTimeoutMs</td>
      <td>0</td>
      <td>When `pinot.server.starter.enableRealtimeFreshnessBasedConsumptionStatusChecker=true`, this will mark a segment as `GOOD` after this timeout if it has not consumed any events.</td>
    </tr>
    <tr>
      <td>pinot.server.startup.exitOnServiceStatusCheckFailure</td>
      <td>false</td>
      <td>When `true`, the server will shutdown after `pinot.server.shutdown.timeoutMs` rather than be marked as `STARTED` if the status has not turned `GOOD`</td>
    </tr>
    <tr>
      <td>pinot.server.startup.enableServiceStatusCheck</td>
      <td>true</td>
      <td><p><code>true</code> - server will run all configured checks<br><br><code>false</code> - server will be marked as <code>STARTED</code> without performing an startup checks</p></td>
    </tr>
    <tr>
      <td>pinot.server.startup.serviceStatusCheckIntervalMs</td>
      <td>10 seconds</td>
      <td>Interval at which server will perform service stats checks</td>
    </tr>
    <tr>
      <td>pinot.server.shutdown.timeoutMs</td>
      <td>10 minutes</td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.server.shutdown.enableQueryCheck</td>
      <td>true</td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.server.shutdown.noQueryThresholdMs</td>
      <td>15 seconds</td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.server.shutdown.enableResourceCheck</td>
      <td>false</td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.server.shutdown.resourceCheckIntervalMs</td>
      <td>10 seconds</td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.server.admin.access.control.factory.class</td>
      <td><p><code>org.apache.pinot.server.</code><br><code>api.access.AllowAllAccessFactory</code></p></td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.server.adminapi.access.protocols</td>
      <td>http</td>
      <td>Ingress protocols to access server admin api (http or https or http,https)</td>
    </tr>
    <tr>
      <td>pinot.server.adminapi.access.protocols.http.port</td>
      <td></td>
      <td>Port to access server admin api via http</td>
    </tr>
    <tr>
      <td>pinot.server.adminapi.broker.protocols.https.port</td>
      <td></td>
      <td>Port to access server admin api via https</td>
    </tr>
    <tr>
      <td>pinot.server.tls.keystore.path</td>
      <td></td>
      <td>Path to server TLS keystore</td>
    </tr>
    <tr>
      <td>pinot.server.tls.keystore.password</td>
      <td></td>
      <td>keystore password</td>
    </tr>
    <tr>
      <td>pinot.server.tls.truststore.path</td>
      <td></td>
      <td>Path to server TLS truststore</td>
    </tr>
    <tr>
      <td>pinot.server.tls.truststore.password</td>
      <td></td>
      <td>truststore password</td>
    </tr>
    <tr>
      <td>inot.server.tls.client.auth</td>
      <td>false</td>
      <td>toggle for requiring TLS client auth</td>
    </tr>
    <tr>
      <td>pinot.server.netty.enabled</td>
      <td>true</td>
      <td>toggle for enabling unsecured netty connections to server</td>
    </tr>
    <tr>
      <td>pinot.server.netty.port</td>
      <td></td>
      <td>Port for accessing pinot server via unsecured netty</td>
    </tr>
    <tr>
      <td>pinot.server.nettytls.enabled</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.server.nettytls.port</td>
      <td></td>
      <td>Port for accessing pinot server via TLS-secured netty</td>
    </tr>
    <tr>
      <td>pinot.server.http.server.thread.pool.corePoolSize</td>
      <td>2 \* cores</td>
      <td>Config for the thread-pool used by pinot-server's http-server.</td>
    </tr>
    <tr>
      <td>pinot.server.http.server.thread.pool.maxPoolSize</td>
      <td>2 \* cores</td>
      <td>Config for the thread-pool used by pinot-server's http-server.</td>
    </tr>
    <tr>
      <td>pinot.server.segment.fetcher.http.client.maxConnTotal</td>
      <td></td>
      <td>Config for the http-client used by HttpSegmentFetcher for downloading segments</td>
    </tr>
    <tr>
      <td>pinot.server.segment.fetcher.http.client.maxConnPerRoute</td>
      <td></td>
      <td>Config for the http-client used by HttpSegmentFetcher for downloading segments</td>
    </tr>
    <tr>
      <td>pinot.server.segment.fetcher.http.client.connectionTimeoutMs</td>
      <td></td>
      <td>Config for the segment fetcher to wait to establish a connection</td>
    </tr>
    <tr>
      <td>pinot.server.segment.fetcher.http.request.socketTimeoutMs</td>
      <td></td>
      <td>Config for the segment fetcher to wait for the segment to download</td>
    </tr>
    <tr>
      <td>pinot.server.segment.fetcher.http.request.connectionRequestTimeoutMs</td>
      <td></td>
      <td>Config for the segment fetcher to wait for a connection from the pool</td>
    </tr>
    <tr>
      <td>pinot.server.instance.max.segment.preload.threads</td>
      <td>0</td>
      <td><p>Number of threads that should be created to preload the segments in an upsert table.<br><br>Value should be greater than 0 otherwise preload is synchronous.</p></td>
    </tr>
    <tr>
      <td>pinot.server.consuming.segment.consistency.mode</td>
      <td>`RESTRICTED`</td>
      <td>Controls how the server handles segment reloads and force commits for partial upsert tables and tables with `dropOutOfOrder=true`. **RESTRICTED**: disables reloads and force commits (safest, default). **PROTECTED**: enables reloads/force commits with metadata reversion; requires `ParallelSegmentConsumptionPolicy` set to `DISALLOW_ALWAYS` or `ALLOW_DURING_BUILD_ONLY`. **UNSAFE**: allows reloads without metadata reversion.</td>
    </tr>
    <tr>
      <td>pinot.server.query.regex.class</td>
      <td>JAVA\_UTIL</td>
      <td>Determine the regex class used for query execution. Valid options are `JAVA_UTIL` and `RE2J`</td>
    </tr>
    <tr>
      <td>pinot.server.instance.consumer.client.id.suffix</td>
      <td></td>
      <td>Configures a suffix to differentiate consumer instances. When multiple replicas of a real-time consuming segment have the same client ID (formatted as `TableName-TopicName-Partition`), this suffix can be used add a unique server level identity.</td>
    </tr>
    <tr>
      <td>pinot.server.segment.uploader.protocol</td>
      <td>http</td>
      <td>Configure the http protocol when server upload segments to controller. This is required</td>
    </tr>
    <tr>
      <td>pinot.server.segment.uploader.https.enabled</td>
      <td>false</td>
      <td>Enable https for server upload protocol, note that you need to configure `pinot.server.segment.uploader.protocol=https`</td>
    </tr>
    <tr>
      <td>pinot.server.segment.uploader.https.ssl.xxxx</td>
      <td></td>
      <td>All the ssl related configures goes here</td>
    </tr>
    <tr>
      <td>pinot.server.segment.uploader.upload.request.timeout.ms</td>
      <td>300\_000</td>
      <td>default is 300 seconds/5mins</td>
    </tr>
    <tr>
      <td>pinot.server.segment.uploader.auth.xxx</td>
      <td></td>
      <td>Auth related configs go here</td>
    </tr>
    <tr>
      <td>pinot.server.segment.uploader.http.client.maxConnTotal</td>
      <td></td>
      <td>uploader http client config</td>
    </tr>
    <tr>
      <td>pinot.server.segment.uploader.http.client.maxConnPerRoute</td>
      <td></td>
      <td>uploader http client config</td>
    </tr>
    <tr>
      <td>pinot.server.segment.uploader.http.client.disableDefaultUserAgent</td>
      <td></td>
      <td>uploader http client config</td>
    </tr>
    <tr>
      <td>pinot.server.lucene.min.refresh.interval.ms</td>
      <td>10</td>
      <td>Wait time before each round of refreshing Lucene indexes config</td>
    </tr>
    <tr>
      <td>pinot.server.lucene.max.refresh.threads</td>
      <td>1</td>
      <td>Number of threads that concurrently refresh Lucene indexes config</td>
    </tr>
    <tr>
      <td>pinot.server.shutdown.timeoutMs</td>
      <td>600000 (10 minutes)</td>
      <td>Timeout in milliseconds for the shutdown checks to complete before the server shuts down regardless.</td>
    </tr>
    <tr>
      <td>pinot.server.shutdown.enableQueryCheck</td>
      <td>true</td>
      <td>When `true`, the server will wait for in-flight queries to complete before shutting down.</td>
    </tr>
    <tr>
      <td>pinot.server.shutdown.noQueryThresholdMs</td>
      <td>15000</td>
      <td>The server waits until no queries are received for this duration before proceeding with shutdown.</td>
    </tr>
    <tr>
      <td>pinot.server.shutdown.enableResourceCheck</td>
      <td>false</td>
      <td>When `true`, the server will check that external visibility (e.g., Helix routing tables) has been updated before shutting down.</td>
    </tr>
    <tr>
      <td>pinot.server.shutdown.resourceCheckIntervalMs</td>
      <td>10000</td>
      <td>Interval in milliseconds between resource checks during shutdown.</td>
    </tr>
    <tr>
      <td>pinot.server.query.executor.mse.max.execution.threads</td>
      <td>-1 (CPU cores)</td>
      <td>Maximum number of execution threads for multi-stage engine queries on this server. `-1` means use the number of CPU cores.</td>
    </tr>
    <tr>
      <td>pinot.server.max.segment.preprocess.parallelism</td>
      <td>Integer.MAX_VALUE</td>
      <td>Maximum number of segments that can be preprocessed (index building on load) in parallel. Reduce this to limit CPU/memory usage during segment loading.</td>
    </tr>
    <tr>
      <td>pinot.server.max.segment.download.parallelism</td>
      <td>Integer.MAX_VALUE</td>
      <td>Maximum number of segments that can be downloaded in parallel from deep store or peers.</td>
    </tr>
    <tr>
      <td>pinot.server.max.segment.startree.preprocess.parallelism</td>
      <td>Integer.MAX_VALUE</td>
      <td>Maximum number of star-tree indexes that can be built in parallel during segment preprocessing.</td>
    </tr>
    <tr>
      <td>pinot.server.lucene.max.refresh.threads</td>
      <td>1</td>
      <td>Maximum number of threads used to refresh Lucene indexes (for text and FST indexes on real-time tables).</td>
    </tr>
    <tr>
      <td>pinot.server.lucene.min.refresh.interval.ms</td>
      <td>10</td>
      <td>Minimum interval in milliseconds between Lucene index refreshes for real-time tables.</td>
    </tr>
    <tr>
      <td>pinot.server.consumption.rate.limit</td>
      <td>0.0 (no limit)</td>
      <td>Maximum number of rows per second that can be consumed across all real-time tables on this server. `0` means no limit.</td>
    </tr>
    <tr>
      <td>pinot.server.enableThreadCpuTimeMeasurement</td>
      <td>false</td>
      <td>Enable per-thread CPU time measurement for query execution. Provides more detailed metrics but adds overhead.</td>
    </tr>
    <tr>
      <td>pinot.server.enableThreadAllocatedBytesMeasurement</td>
      <td>false</td>
      <td>Enable per-thread memory allocation measurement. Provides detailed memory allocation metrics per query but adds overhead.</td>
    </tr>
    <tr>
      <td>pinot.server.enableThrottlingOnHeapUsage</td>
      <td>false</td>
      <td>Enable throttling queries when heap usage exceeds a threshold. When enabled, queries are queued instead of immediately executed when memory pressure is high.</td>
    </tr>
  </tbody>
</table>

