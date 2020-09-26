# Server

Server configuration can be provided as part of the server startup parameters.

```text
bin/pinot-admin.sh StartServer -configFileName /path/to/server.conf
```

`server.conf` can have the following properties

<table>
  <thead>
    <tr>
      <th style="text-align:left">Property</th>
      <th style="text-align:left">Default</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">pinot.server.netty.port</td>
      <td style="text-align:left">8098</td>
      <td style="text-align:left">Port to query Pinot Server</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.netty.host</td>
      <td style="text-align:left"></td>
      <td style="text-align:left">Pinot server hostname</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.adminapi.port</td>
      <td style="text-align:left">8097</td>
      <td style="text-align:left">Port for Pinot Server Admin UI</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.instance.id</td>
      <td style="text-align:left"></td>
      <td style="text-align:left">By default the server instance id used by Helix is <em>Server_hostname_port </em>where
        the hostname and port are configured through host and port config values
        above. This config overwrites the default setting. User can put server
        id independent of the server&apos;s hostname and port.</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.instance.dataDir</td>
      <td style="text-align:left"><code>java.io.tmpdir</code> + <code>/PinotServer/index</code>
      </td>
      <td style="text-align:left">
        <p></p>
        <p>Directory to hold all the data</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.instance.consumerDir</td>
      <td style="text-align:left"></td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.instance.segmentTarDir</td>
      <td style="text-align:left"><code>java.io.tmpdir</code> + <code>/PinotServer/segmentTar</code>
      </td>
      <td style="text-align:left">Directory to hold temporary segments downloaded from Controller or Deep
        Store</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.instance.readMode</td>
      <td style="text-align:left"><code>mmap</code>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.instance.reload.consumingSegment</td>
      <td style="text-align:left">false</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.instance.data.manager.class</td>
      <td style="text-align:left"><code>org.apache.pinot.server.</code>
        <br /><code>starter.helix.HelixInstanceDataManager</code>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.query.executor.pruner.class</td>
      <td style="text-align:left"><code>ValidSegmentPruner,DataSchemaSegmentPruner,<br />ColumnValueSegmentPruner,SelectionQuerySegmentPruner</code>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.query.executor.timeout</td>
      <td style="text-align:left">15 seconds</td>
      <td style="text-align:left">Timeout for Server to process Query in Milliseconds</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.query.executor.class</td>
      <td style="text-align:left"><code>org.apache.pinot.core.query.</code>
        <br /><code>executor.ServerQueryExecutorV1Impl</code>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.requestHandlerFactory.class</td>
      <td style="text-align:left"><code>org.apache.pinot.server.</code>
        <br /><code>request.SimpleRequestHandlerFactory</code>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.instance.segment.format.version</td>
      <td style="text-align:left"></td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.instance.enable.split.commit</td>
      <td style="text-align:left"></td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.instance.enable.commitend.metadata</td>
      <td style="text-align:left"></td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.instance.realtime.max.parallel.segment.builds</td>
      <td style="text-align:left">0</td>
      <td style="text-align:left">Specifies how many parallel realtime segments can be built. Value of &lt;=
        0 indicates unlimited.</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.instance.realtime.alloc.offheap</td>
      <td style="text-align:left">false</td>
      <td style="text-align:left">Boolean value to control whether memory for realtime consuming segments
        should be allocated off-heap.</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.instance.realtime.alloc.offheap.direct</td>
      <td style="text-align:left">false</td>
      <td style="text-align:left">If &apos;realtime.alloc.offheap&apos; is set to true, this boolean value
        controls whether the corresponding allocation should be direct or not (false
        indicate mmap allocation)</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.startup.minResourcePercent</td>
      <td style="text-align:left">100</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.starter.realtimeConsumptionCatchupWaitMs</td>
      <td style="text-align:left">0</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.startup.timeoutMs</td>
      <td style="text-align:left">10 minutes</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.startup.enableServiceStatusCheck</td>
      <td style="text-align:left">true</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.startup.serviceStatusCheckIntervalMs</td>
      <td style="text-align:left">10 seconds</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.shutdown.timeoutMs</td>
      <td style="text-align:left">10 minutes</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.shutdown.enableQueryCheck</td>
      <td style="text-align:left">true</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.shutdown.noQueryThresholdMs</td>
      <td style="text-align:left">15 seconds</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.shutdown.enableResourceCheck</td>
      <td style="text-align:left">false</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.shutdown.resourceCheckIntervalMs</td>
      <td style="text-align:left">10 seconds</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.admin.access.control.factory.class</td>
      <td style="text-align:left"><code>org.apache.pinot.server.</code>
        <br /><code>api.access.AllowAllAccessFactory</code>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"></td>
      <td style="text-align:left"></td>
      <td style="text-align:left"></td>
    </tr>
  </tbody>
</table>







