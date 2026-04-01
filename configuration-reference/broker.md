# Broker

You can set broker properties in a configuration file. The file can be provided during startup time as follows -

```
bin/pinot-admin.sh StartBroker -configFileName /path/to/broker.conf
```

`broker.conf` can have the following properties. All properties are defined in this class.

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
      <td>pinot.broker.delayShutdownTimeMs</td>
      <td>10 seconds</td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.broker.enableTableLevelMetrics</td>
      <td>true</td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.broker.query.response.limit</td>
      <td>Integer.MAX\_VALUE</td>
      <td>When config `pinot.broker.enable.query.limit.override`is enabled, reset limit for selection query if it exceeds this value.</td>
    </tr>
    <tr>
      <td>pinot.broker.query.log.length</td>
      <td>Integer.MAX\_VALUE</td>
      <td></td>
    </tr>
    <tr>
      <td>pinot.broker.query.log.maxRatePerSecond</td>
      <td>10000.0</td>
      <td>Maximum queries to be logged per second. Queries with exceptions, or take longer than 1 second are always logged.</td>
    </tr>
    <tr>
      <td>pinot.broker.timeoutMs</td>
      <td>10 seconds</td>
      <td>Timeout for Broker Query in Milliseconds</td>
    </tr>
    <tr>
      <td>pinot.broker.startup.minResourcePercent</td>
      <td>100</td>
      <td>Configuration to consider the broker ServiceStatus as being STARTED if the percent of resources (tables) that are ONLINE for this this broker has crossed the threshold percentage of the total number of tables that it is expected to serve</td>
    </tr>
    <tr>
      <td>pinot.broker.enable.query.limit.override</td>
      <td>false</td>
      <td>Configuration to enable Query LIMIT Override to protect Pinot Broker and Server from fetch too many records back.</td>
    </tr>
    <tr>
      <td>pinot.broker.client.queryPort</td>
      <td>8099</td>
      <td>**(Deprecated: use `pinot.broker.client.access.protocols.http.port` instead.)** Legacy port to query broker via http.</td>
    </tr>
    <tr>
      <td>pinot.broker.client.access.protocols</td>
      <td></td>
      <td>Ingress protocols to query broker (http or https or http,https)</td>
    </tr>
    <tr>
      <td>pinot.broker.client.access.protocols.http.port</td>
      <td></td>
      <td>Port to query broker via http</td>
    </tr>
    <tr>
      <td>pinot.broker.client.access.protocols.https.port</td>
      <td></td>
      <td>Port to query broker via https</td>
    </tr>
    <tr>
      <td>pinot.broker.netty.enabled</td>
      <td>true</td>
      <td>Enable unsecured netty connections to pinot-server</td>
    </tr>
    <tr>
      <td>pinot.broker.nettytls.enabled</td>
      <td>false</td>
      <td>Enable secured netty connections to pinot-server</td>
    </tr>
    <tr>
      <td>pinot.broker.tls.keystore.path</td>
      <td></td>
      <td>Path to broker TLS keystore</td>
    </tr>
    <tr>
      <td>pinot.broker.tls.keystore.password</td>
      <td></td>
      <td>keystore password</td>
    </tr>
    <tr>
      <td>pinot.broker.tls.truststore.path</td>
      <td></td>
      <td>Path to broker TLS truststore</td>
    </tr>
    <tr>
      <td>pinot.broker.tls.truststore.password</td>
      <td></td>
      <td>truststore password</td>
    </tr>
    <tr>
      <td>pinot.broker.tls.requires\_client\_auth</td>
      <td>false</td>
      <td>toggle for requiring TLS client auth</td>
    </tr>
    <tr>
      <td>pinot.broker.http.server.thread.pool.corePoolSize</td>
      <td>2 \* cores</td>
      <td>Config for the thread-pool used by pinot-broker's http-server.</td>
    </tr>
    <tr>
      <td>pinot.broker.http.server.thread.pool.maxPoolSize</td>
      <td>2 \* cores</td>
      <td>Config for the thread-pool used by pinot-broker's http-server.</td>
    </tr>
    <tr>
      <td>pinot.broker.enable.bounded.jersey.threadpool.executor</td>
      <td>false</td>
      <td>Enable bounded Jersey thread-pool to handle async requests.</td>
    </tr>
    <tr>
      <td>pinot.broker.jersey.threadpool.executor.max.pool.size</td>
      <td>2 \* cores</td>
      <td>Config for the bounded Jersey thread-pool to handle async requests.</td>
    </tr>
    <tr>
      <td>pinot.broker.jersey.threadpool.executor.core.pool.size</td>
      <td>2 \* cores</td>
      <td>Config for the bounded Jersey thread-pool to handle async requests.</td>
    </tr>
    <tr>
      <td>pinot.broker.jersey.threadpool.executor.queue.size</td>
      <td>Integer.MAX\_VALUE</td>
      <td>Config for the bounded Jersey thread-pool to handle async requests.</td>
    </tr>
    <tr>
      <td>pinot.broker.max.query.response.size.bytes</td>
      <td>Long.MAX\_VALUE</td>
      <td>Config indicating the maximum serialized response size across all servers for a query. This value is // equally divided across all servers processing the query.</td>
    </tr>
    <tr>
      <td>pinot.broker.max.server.response.size.bytes</td>
      <td>Long.MAX\_VALUE</td>
      <td>Config indicating the maximum length of the serialized response per server for a query.</td>
    </tr>
    <tr>
      <td>pinot.broker.event.listener.factory.className</td>
      <td>org.apache.pinot.spi.eventlistener.query.NoOpBrokerQueryEventListener</td>
      <td>Config indicating the event listener class that will be loaded during broker starter and the `onQueryCompletion` will be called post query completion. It is on the implementation of this method that user can improve query level observability in their system.</td>
    </tr>
    <tr>
      <td>pinot.broker.event.listener.request.context.tracked.header.keys</td>
      <td></td>
      <td>Comma separated string values indicating the request-headers which will be tracked by the event listener class.</td>
    </tr>
    <tr>
      <td>pinot.broker.new.segment.expiration.seconds</td>
      <td>300 seconds (5 minutes)</td>
      <td>Config for broker to consider a new segment as an old segment and start tagging replica-group / instances as unavailable after this time period.</td>
    </tr>
    <tr>
      <td>pinot.broker.query.enable.null.handling</td>
      <td>false</td>
      <td>Config that allows enabling advanced null handling support for all queries by default (see [docs](../developers/advanced/null-value-support.md#advanced-null-handling-support))</td>
    </tr>
    <tr>
      <td>pinot.broker.multistage.lite.mode.leaf.stage.limit</td>
      <td>100000</td>
      <td>For MSE Lite Mode, this controls the maximum number of records that a given Leaf Stage instance on a server is allowed to return. Recommended value is 100k records or lower.</td>
    </tr>
    <tr>
      <td>pinot.broker.multistage.use.lite.mode</td>
      <td>false</td>
      <td>Default value of the query option `useLiteMode`. Only takes effect when `usePhysicalOptimizer=true` is also set.</td>
    </tr>
    <tr>
      <td>pinot.broker.multistage.run.in.broker</td>
      <td>true</td>
      <td>Whether to run the non-leaf stages in the broker by default. This controls the default value of the query option `runInBroker`. Only applicable for MSE Lite Mode.</td>
    </tr>
    <tr>
      <td>pinot.broker.default.query.limit</td>
      <td>10</td>
      <td>Default LIMIT applied to queries that don't specify one explicitly.</td>
    </tr>
    <tr>
      <td>pinot.broker.enable.query.cancellation</td>
      <td>true</td>
      <td>Whether to allow queries to be cancelled via the cancel API.</td>
    </tr>
    <tr>
      <td>pinot.broker.groupby.trim.threshold</td>
      <td>1000000</td>
      <td>Threshold for number of groups to trigger trimming at the broker level. Reducing this can lower memory usage at the cost of accuracy.</td>
    </tr>
    <tr>
      <td>pinot.broker.min.group.trim.size</td>
      <td>5000</td>
      <td>Minimum number of groups kept at the broker level after trimming. The actual number kept is `max(5 * LIMIT, minGroupTrimSize)`.</td>
    </tr>
    <tr>
      <td>pinot.broker.adaptive.server.selector.type</td>
      <td>NO_OP</td>
      <td>Type of adaptive server selector for intelligent query routing. Options: `NO_OP` (round-robin), `NUM_INFLIGHT_REQ` (least in-flight requests), `LATENCY` (lowest latency), `HYBRID` (combines latency and in-flight).</td>
    </tr>
    <tr>
      <td>pinot.broker.adaptive.server.selector.enable.stats.collection</td>
      <td>false</td>
      <td>Enable stats collection for the adaptive server selector. Must be true for `LATENCY` or `HYBRID` types.</td>
    </tr>
    <tr>
      <td>pinot.broker.adaptive.server.selector.ewma.alpha</td>
      <td>0.666</td>
      <td>EWMA (Exponentially Weighted Moving Average) alpha value for latency calculation. Higher values weight recent observations more heavily.</td>
    </tr>
    <tr>
      <td>pinot.broker.adaptive.server.selector.hybrid.score.exponent</td>
      <td>3</td>
      <td>Exponent used in the hybrid scoring formula to balance latency and in-flight request count.</td>
    </tr>
    <tr>
      <td>pinot.broker.multistage.use.physical.optimizer</td>
      <td>false</td>
      <td>Enable the physical optimizer for the multi-stage query engine.</td>
    </tr>
    <tr>
      <td>pinot.broker.multistage.infer.partition.hint</td>
      <td>false</td>
      <td>Infer partition hints to optimize data shuffling in the multi-stage query engine.</td>
    </tr>
    <tr>
      <td>pinot.broker.multistage.default.hash.function</td>
      <td>absHashCode</td>
      <td>Default hash function for data partitioning in the multi-stage engine.</td>
    </tr>
    <tr>
      <td>pinot.broker.request.handler.type</td>
      <td>netty</td>
      <td>Type of request handler for broker-to-server communication. Options: `netty`, `grpc`, `multistage`.</td>
    </tr>
    <tr>
      <td>pinot.broker.max.reduce.threads.per.query</td>
      <td>min(10, cores/2)</td>
      <td>Maximum number of threads used to reduce (merge) results from multiple servers for a single query.</td>
    </tr>
    <tr>
      <td>pinot.broker.failure.detector.type</td>
      <td>NO_OP</td>
      <td>Type of failure detector for detecting unhealthy servers. Options: `NO_OP`, `CONNECTION_BASED`.</td>
    </tr>
    <tr>
      <td>pinot.broker.use.fixed.replica</td>
      <td>false</td>
      <td>When true, routes queries to a fixed replica group for better cache locality.</td>
    </tr>
  </tbody>
</table>

